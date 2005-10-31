/* Copyright 2004 The Apache Software Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#if !defined(__linux__) && !defined(__FreeBSD__)
#error This module is currently implemented only for Linux and FreeBSD.
#endif

/*
 * Documentation:
 *
 * mod_backtrace is an experimental module for Apache httpd 2.x which
 * collects backtraces when a child process crashes.  Currently it is
 * implemented only on Linux and FreeBSD, but other platforms could be
 * supported in the future.  You should verify that it works reasonably
 * on your system before putting it in production.
 *
 * It implements a fatal exception hook that will be called when a child
 * process crashes.  In the exception hook it uses system library routines
 * to obtain information about the call stack, and it writes the call
 * stack to a log file or the web server error log.  The backtrace is a
 * critical piece of information when determining the failing software
 * component that caused the crash.  Note that the backtrace written by
 * mod_backtrace may not have as much information as a debugger can
 * display from a core dump.
 *
 * Apache httpd requirements for mod_backtrace:
 *
 *   Apache httpd >= 2.0.49 must be built with the --enable-exception-hook
 *   configure option and mod_so enabled.
 *
 * Compiling mod_backtrace:
 *
 *   Linux:
 *     apxs -ci mod_backtrace.c
 *
 *   FreeBSD:
 *     install libexecinfo from the Ports system then
 *     apxs -ci -L/usr/local/lib -lexecinfo mod_backtrace.c
 *
 * Activating mod_backtrace:
 *
 *   1. Load it like any other DSO:
 *        LoadModule backtrace_module modules/mod_backtrace.so
 *
 *   2. Enable exception hooks for modules like mod_backtrace:
 *        EnableExceptionHook On
 *
 *   3. Choose where backtrace information should be written.
 *      If you want backtraces from crashes to be reported some place other
 *      than the error log, use the BacktraceLog directive to specify a
 *      fully-qualified filename for the log to which backtraces will be
 *      written.  Note that the web server user id (e.g., "nobody") must
 *      be able to create or append to this log file, as the log file is
 *      not opened until a crash occurs.
 */

#include "httpd.h"
#include "http_config.h"
#include "ap_mpm.h"

#include "apr_strings.h"

#include <unistd.h>
#include <execinfo.h>
#include <fcntl.h>

static pid_t real_pid;
static const char *log_fname;

static int bt_exception_hook(ap_exception_info_t *ei)
{
    int msg_len;
    int logfd;
    char msg_prefix[60];
    char buffer[512];
    time_t now;
    char *newline;
    int using_errorlog = 1;
    size_t size;
    void *array[20];
    extern int main(void);

    time(&now);
    apr_snprintf(msg_prefix, sizeof msg_prefix,
                 "[%s pid %" APR_PID_T_FMT " mod_backtrace",
                 asctime(localtime(&now)),
                 real_pid);
    newline = strchr(msg_prefix, '\n'); /* dang asctime() */
    if (newline) {                      /* silly we are */
        *newline = ']';
    }

    if (log_fname) {
        logfd = open(log_fname, O_WRONLY|O_APPEND|O_CREAT, 0644);
        if (logfd == -1) {
            logfd = 2; /* unix, so fd 2 is the web server error log */
            apr_snprintf(buffer, sizeof buffer,
                         "%s error %d opening %s\n",
                         msg_prefix, errno, log_fname);
            write(logfd, buffer, strlen(buffer));
        }
        else {
            using_errorlog = 0;
        }
    }
    else {
        logfd = 2;
    }

    msg_len = apr_snprintf(buffer, sizeof buffer,
                           "%s backtrace for sig %d (thread \"pid\" %"
                           APR_PID_T_FMT ")\n",
                           msg_prefix, ei->sig, getpid());
    write(logfd, buffer, msg_len);

    /* the address of main() can be useful if we're on old 
     * glibc and get only addresses for stack frames... knowing
     * the location of main() is then a useful clue
     */
    msg_len = apr_snprintf(buffer, sizeof buffer,
                           "%s main() is at %pp\n",
                           msg_prefix,
                           main);/* don't you DARE put parens after "main" */
    write(logfd, buffer, msg_len);

    size = backtrace(array, sizeof array / sizeof array[0]);
    backtrace_symbols_fd(array, size, logfd);
    msg_len = apr_snprintf(buffer, sizeof buffer,
                           "%s end of backtrace\n",
                           msg_prefix);
    write(logfd, buffer, msg_len);
    
    if (!using_errorlog) {
        close(logfd);
    }
    return OK;
}

static void bt_child_init(apr_pool_t *p, server_rec *s)
{
    real_pid = getpid(); /* linuxthreads foo */
}

static void bt_register_hooks(apr_pool_t *p)
{
    ap_hook_child_init(bt_child_init, NULL, NULL, APR_HOOK_MIDDLE);
    ap_hook_fatal_exception(bt_exception_hook, NULL, NULL,
                            APR_HOOK_MIDDLE);
}

static const char *bt_cmd_file(cmd_parms *cmd, void *dummy, const char *fname)
{
    log_fname = apr_pstrdup(cmd->pool, fname);
    return NULL;
}

static const command_rec bt_cmds[] =
{
    AP_INIT_TAKE1("BacktraceLog", bt_cmd_file, NULL, RSRC_CONF,
                  "the fully-qualified filename of the mod_backtrace "
                  "logfile"),
    {NULL}
};

module AP_MODULE_DECLARE_DATA backtrace_module = {
    STANDARD20_MODULE_STUFF,
    NULL,
    NULL,
    NULL,
    NULL,
    bt_cmds,
    bt_register_hooks
};
