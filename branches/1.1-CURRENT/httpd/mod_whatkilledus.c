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

/*
 * Documentation:
 *
 * mod_whatkilledus is an experimental module for Apache httpd 2.x which
 * tracks the current request and logs a report of the active request
 * when a child process crashes.  You should verify that it works reasonably
 * on your system before putting it in production.
 *
 * mod_whatkilledus is called during request processing to save information
 * about the current request.  It also implements a fatal exception hook
 * that will be called when a child process crashes.
 *
 * Apache httpd requirements for mod_whatkilledus:
 *
 *   Apache httpd >= 2.0.49 must be built with the --enable-exception-hook
 *   configure option and mod_so enabled.
 *
 * Compiling mod_whatkilledus:
 *
 *   apxs -ci -I/path/to/httpd-2.0/server mod_whatkilledus.c
 *
 * Activating mod_whatkilledus:
 *
 *   1. Load it like any other DSO.
 *
 *        LoadModule whatkilledus_module modules/mod_whatkilledus.so
 *
 *   2. Enable exception hooks for modules like mod_whatkilledus:
 *        EnableExceptionHook On
 *
 *   3. Choose where the report on current activity should be written.  If
 *      you want it reported to some place other than the error log, use the
 *      WhatKilledUsLog directive to specify a fully-qualified filename for
 *      the log.  Note that the web server user id (e.g., "nobody") must
 *      be able to create or append to this log file, as the log file is
 *      not opened until a crash occurs.
 */

#include <unistd.h>

#include "httpd.h"
#include "http_config.h"
#include "http_protocol.h"
#include "http_connection.h"
#include "http_log.h"
#include "ap_mpm.h"
#include "test_char.h" /* an odd one, from server subdir in source tree */

#include "apr_strings.h"
#include "apr_network_io.h"
#include "apr_thread_mutex.h"
#include "apr_anylock.h"

#if !AP_ENABLE_EXCEPTION_HOOK
#error Apache must be built with --enable-exception-hook
#endif

module AP_MODULE_DECLARE_DATA whatkilledus_module;

typedef struct wku_req_info_tag {
    const char *buf;
    request_rec *r; /* possibly dangerous to access the contents
                     * after a crash; we'll log the address as
                     * a head start for somebody looking in core
                     */
} wku_req_info_t;

typedef struct wku_conn_info_tag {
    struct wku_conn_info_tag *next;
    struct wku_conn_info_tag *prev;
    apr_pool_t *p;
    conn_rec *c;
#if APR_HAS_THREADS
    pthread_t tid;
#endif
    wku_req_info_t *reqinfo; /* or NULL if not currently processing request */
} wku_conn_info_t;

static wku_conn_info_t *active_connections;
static char *log_fname;
static apr_anylock_t mutex;
static pid_t real_pid;

#if APR_HAS_THREADS
static void set_my_tid(wku_conn_info_t *conninfo)
{
    conninfo->tid = pthread_self();
}

static int has_my_tid(wku_conn_info_t *conninfo)
{
    return conninfo->tid == pthread_self();
}
#else
#define set_my_tid(conninfo)
#define has_my_tid(conninfo) 1
#endif

static void wku_child_init(apr_pool_t *p, server_rec *s)
{
#if APR_HAS_THREADS
    apr_status_t rv;

    mutex.type = apr_anylock_threadmutex;
    rv = apr_thread_mutex_create(&mutex.lock.tm,
                                 APR_THREAD_MUTEX_DEFAULT,
                                 p);
    ap_assert(rv == APR_SUCCESS);
#else
    mutex.type = apr_anylock_none;
#endif    
    real_pid = getpid(); /* linuxthreads foo */
}

static wku_conn_info_t *get_new_ci(conn_rec *c)
{
    wku_conn_info_t *conninfo;

    conninfo = (wku_conn_info_t *)apr_pcalloc(c->pool, sizeof(*conninfo));
    ap_set_module_config(c->conn_config, &whatkilledus_module, conninfo);
    set_my_tid(conninfo);

    APR_ANYLOCK_LOCK(&mutex);
    conninfo->next = active_connections;
    active_connections = conninfo;
    if (conninfo->next) {
        conninfo->next->prev = conninfo;
    }
    APR_ANYLOCK_UNLOCK(&mutex);

    return conninfo;
}

static wku_conn_info_t *get_cur_ci(conn_rec *c)
{
    if (c) {
        return (wku_conn_info_t *)ap_get_module_config(c->conn_config,
                                                       &whatkilledus_module);
    }
    else {
        /* search for saved info! */
        wku_conn_info_t *cur;

        APR_ANYLOCK_LOCK(&mutex);
        cur = active_connections;
        while (cur) {
            if (has_my_tid(cur)) {
                APR_ANYLOCK_UNLOCK(&mutex);
                return cur;
            }
            cur = cur->next;
        }
        APR_ANYLOCK_UNLOCK(&mutex);
    }
    return NULL; /* bad news! */
}

static void free_ci(wku_conn_info_t *conninfo)
{
    /* just remove it from the linked list; storage goes away as the
     * pool is cleaned up
     */
    APR_ANYLOCK_LOCK(&mutex);
    if (conninfo->prev) {
        conninfo->prev->next = conninfo->next;
    }
    else {
        active_connections = conninfo->next;
    }
    if (conninfo->next) {
        conninfo->next->prev = conninfo->prev;
    }
    APR_ANYLOCK_UNLOCK(&mutex);
}

static int wku_fatal_exception(ap_exception_info_t *ei)
{
    wku_conn_info_t *conninfo;
    int msg_len;
    int logfd;
    char msg_prefix[60];
    char buffer[512];
    time_t now;
    char *newline;
    int using_errorlog = 1;

    time(&now);
    apr_snprintf(msg_prefix, sizeof msg_prefix,
                 "[%s pid %" APR_PID_T_FMT " mod_whatkilledus",
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
                           "%s sig %d crash\n",
                           msg_prefix, ei->sig);
    write(logfd, buffer, msg_len);

    conninfo = get_cur_ci(NULL); /* no conn_rec avail */
    if (conninfo) {
        msg_len = apr_snprintf(buffer, sizeof buffer,
                               "%s active connection: "
                               "%pI->%pI (conn_rec %pp)\n",
                               msg_prefix,
                               conninfo->c->remote_addr,
                               conninfo->c->local_addr,
                               conninfo->c);
    }
    else {
        msg_len = apr_snprintf(buffer, sizeof buffer,
                               "%s no active connection at crash\n",
                               msg_prefix);
    }

    write(logfd, buffer, msg_len);

    if (conninfo && conninfo->reqinfo) {
        msg_len = apr_snprintf(buffer, sizeof buffer,
                               "%s active request (request_rec %pp):\n",
                               msg_prefix,
                               conninfo->reqinfo->r);
        write(logfd, buffer, msg_len);
        write(logfd, conninfo->reqinfo->buf, strlen(conninfo->reqinfo->buf));
    }
    else {
        msg_len = apr_snprintf(buffer, sizeof buffer,
                               "%s no request active at crash\n",
                               msg_prefix);
        write(logfd, buffer, msg_len);
    }

    msg_len = apr_snprintf(buffer, sizeof buffer,
                           "%s end of report\n",
                           msg_prefix);
    write(logfd, buffer, msg_len);
    if (!using_errorlog) {
        close(logfd);
    }

    free_ci(conninfo);

    return OK;
}

static apr_status_t wku_connection_end(void *void_ci)
{
    wku_conn_info_t *ci = void_ci;

    free_ci(ci);
    return APR_SUCCESS;
}

static int wku_pre_connection(conn_rec *c, void *vcsd)
{
    wku_conn_info_t *conninfo;

    conninfo = get_new_ci(c);
    conninfo->c = c;
    conninfo->p = c->pool;

    apr_pool_cleanup_register(c->pool, conninfo, wku_connection_end, apr_pool_cleanup_null);

    return DECLINED;
}

/* e is the first _invalid_ location in q
   N.B. returns the terminating NUL.
 */
static char *log_escape(char *q, const char *e, const char *p)
{
    for ( ; *p ; ++p) {
        ap_assert(q < e);
        if (test_char_table[*(unsigned char *)p]&T_ESCAPE_FORENSIC) {
            ap_assert(q+2 < e);
            *q++ = '%';
            sprintf(q, "%02x", *(unsigned char *)p);
            q += 2;
        }
        else
            *q++ = *p;
    }
    ap_assert(q < e);
    *q = '\0';

    return q;
}

typedef struct hlog {
    char *log;
    char *pos;
    char *end;
    apr_size_t count;
} hlog;

static int count_string(const char *p)
{
    int n;

    for (n = 0 ; *p ; ++p, ++n)
        if (test_char_table[*(unsigned char *)p]&T_ESCAPE_FORENSIC)
            n += 2;
    return n;
}

static int count_headers(void *h_, const char *key, const char *value)
{
    hlog *h = h_;

    h->count += count_string(key)+count_string(value)+2;

    return 1;
}

static int log_headers(void *h_, const char *key, const char *value)
{
    hlog *h = h_;

    /* note that we don't have to check h->pos here, coz its been done
       for us by log_escape */
    *h->pos++ = '|';
    h->pos = log_escape(h->pos, h->end, key);
    *h->pos++ = ':';
    h->pos = log_escape(h->pos, h->end, value);

    return 1;
}

static apr_status_t wku_request_end(void *void_ci)
{
    wku_conn_info_t *conninfo = void_ci;

    /* end of request,
     * just note that we are not processing anything
     */
    conninfo->reqinfo = NULL;
    return APR_SUCCESS;
}

static int wku_post_read_request(request_rec *r)
{
    wku_conn_info_t *conninfo;
    hlog h;
    
    if (r->prev) { /* we were already called for this internal redirect */
        return DECLINED;
    }

    conninfo = get_cur_ci(r->connection);
    conninfo->reqinfo = apr_pcalloc(r->pool, sizeof(*conninfo->reqinfo));
    conninfo->reqinfo->r = r;

    h.count = 0;

    apr_table_do(count_headers, &h, r->headers_in, NULL);
    h.count += count_string(r->the_request);
    h.count += 2; /* terminating '\n\0' */
    h.log = apr_palloc(r->pool, h.count);
    h.pos = h.log;
    h.end = h.log + h.count;

    h.pos = log_escape(h.pos, h.end, r->the_request);

    apr_table_do(log_headers, &h, r->headers_in, NULL);
    *h.pos++ = '\n';
    *h.pos++ = '\0';
    ap_assert(h.pos == h.end);

    conninfo->reqinfo->buf = h.log;

    apr_pool_cleanup_register(r->pool, conninfo, wku_request_end, apr_pool_cleanup_null);

    return OK;
}

static void wku_register_hooks(apr_pool_t *p)
{
    ap_hook_child_init(wku_child_init, NULL, NULL, APR_HOOK_MIDDLE);
    ap_hook_pre_connection(wku_pre_connection, NULL, NULL,
                           APR_HOOK_REALLY_FIRST); /* precede crashes */
    ap_hook_post_read_request(wku_post_read_request, NULL, NULL,
                              APR_HOOK_REALLY_FIRST); /* precede crashes */
    ap_hook_fatal_exception(wku_fatal_exception, NULL, NULL, APR_HOOK_MIDDLE);
}

static const char *wku_cmd_file(cmd_parms *cmd, void *dummy, const char *arg)
{
    log_fname = apr_pstrdup(cmd->pool, arg);
    return NULL;
}

static const command_rec wku_cmds[] =
{
    AP_INIT_TAKE1("WhatKilledUsLog", wku_cmd_file, NULL, RSRC_CONF,
                  "the fully-qualified filename of the mod_whatkilledus "
                  "logfile"),
    {NULL}
};

module AP_MODULE_DECLARE_DATA whatkilledus_module = {
    STANDARD20_MODULE_STUFF,
    NULL,
    NULL,
    NULL,
    NULL,
    wku_cmds,
    wku_register_hooks
};
