
/* ====================================================================
 * Copyright (c) 1995 The Apache Group.  All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * 3. All advertising materials mentioning features or use of this
 *    software must display the following acknowledgment:
 *    "This product includes software developed by the Apache Group
 *    for use in the Apache HTTP server project (http://www.apache.org/)."
 *
 * 4. The names "Apache Server" and "Apache Group" must not be used to
 *    endorse or promote products derived from this software without
 *    prior written permission.
 *
 * 5. Redistributions of any form whatsoever must retain the following
 *    acknowledgment:
 *    "This product includes software developed by the Apache Group
 *    for use in the Apache HTTP server project (http://www.apache.org/)."
 *
 * THIS SOFTWARE IS PROVIDED BY THE APACHE GROUP ``AS IS'' AND ANY
 * EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE APACHE GROUP OR
 * IT'S CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 * ====================================================================
 *
 * This software consists of voluntary contributions made by many
 * individuals on behalf of the Apache Group and was originally based
 * on public domain software written at the National Center for
 * Supercomputing Applications, University of Illinois, Urbana-Champaign.
 * For more information on the Apache Group and the Apache HTTP server
 * project, please see <http://www.apache.org/>.
 *
 */


/*
 * http_auth_msql: authentication
 *
 * Rob McCool & Brian Behlendorf.
 *
 * Adapted to Shambhala by rst.
 *
 * converted to use MySQL by Vivek Khera <khera@kciLink.com>
 */

/*
 * Module definition information - the part between the -START and -END
 * lines below is used by Configure. This could be stored in a separate
 * instead.
 *
 * MODULE-DEFINITION-START
 * Name: mysql_auth_module
 * ConfigStart
     MYSQL_LIB="-L/usr/local/lib/mysql -lmysqlclient -lm"
     if [ "X$MYSQL_LIB" != "X" ]; then
         LIBS="$LIBS $MYSQL_LIB"
         echo " + using $MYSQL_LIB for MySQL support"
     fi
 * ConfigEnd
 * MODULE-DEFINITION-END
 */


/*
 * Tracks user/passwords/group in MySQL database.  A suitable table
 * might be:
 *
 * CREATE TABLE user_info (
 *   user_name CHAR(30) NOT NULL,
 *   user_passwd CHAR(20) NOT NULL,
 *   user_group CHAR(10),
 *     [ any other fields if needed ]
 *   PRIMARY KEY (user)
 * )
 *
 * User_name must be a unique, non-empty field.  Its length is however
 * long you want it to be.  Password length of 20 follows new-style
 * crypt() usage; the older crypt uses shorter encrypted passwords.
 * Any other fields in the named table will be ignored.  The actual
 * field names are configurable using the parameters listed below.
 * The defaults are "user_name" and "user_passwd" respectively, for
 * the user ID and the password, and "user_group" for the group which
 * is optional.  If you like to store passwords in clear text, set
 * AuthMySQLCryptedPasswords to Off.  I think this is a bad idea, but
 * people have requested it.
 *
 * Usage in per-directory access conf file:
 *
 *  AuthName MySQL Testing
 *  AuthType Basic
 *  AuthGroupFile /dev/null
 *  AuthMySQLHost localhost
 *  AuthMySQLDB test
 *  AuthMySQLUserTable user_info
 *  require valid-user
 *
 * The following parameters are optional in the config file.  The defaults
 * values are shown here.
 *
 *  AuthMySQLUser <no default -- NULL>
 *  AuthMySQLPassword <no default -- NULL>
 *  AuthMySQLNameField user_name
 *  AuthMySQLPasswordField user_passwd
 *  AuthMySQLCryptedPasswords On
 *  AuthMySQLKeepAlive Off
 *  AuthMySQLAuthoritative On
 *  AuthMySQLNoPasswd Off
 *  AuthMySQLGroupField <no default>
 *  AuthMySQLGroupTable <defaults to value of AuthMySQLUserTable>
 *
 * The Host of "localhost" means use the MySQL socket instead of a TCP
 * connection to the database.  DB is the database name on the server,
 * and UserTable is the actual table name within that database.
 *
 * If AuthMySQLAuthoritative is Off, then iff the user is not found in
 * the database, let other auth modules try to find the user.  Default
 * is On.
 *
 * If AuthMySQLKeepAlive is "On", then the server instance will keep
 * the MySQL server connection open.  In this case, the first time the
 * connection is made, it will use the current set of Host, User, and
 * Password settings.  Subsequent changes to these will not affect
 * this server, so they should all be the same in every htaccess file.
 * If you need to access multiple MySQL servers for this authorization
 * scheme from the same web server, then keep this setting "Off" --
 * this will open a new connection to the server every time it needs
 * one.  The values of the DB and various tables and fields are always
 * used from the current htaccess file settings.
 *
 * If AuthMySQLNoPasswd is "On", then any password the user enters will
 * be accepted as long as the user exists in the database.  Setting this
 * also overrides the setting for AuthMySQLPasswordField to be the same
 * as AuthMySQLNameField (so that the SQL statements still work when there
 * is no password at all in the database, and to remain backward-compatible
 * with the default values for these fields.)
 *
 * For groups, we use the same AuthMySQLNameField as above for the
 * user ID, and AuthMySQLGroupField to specify the group name.  There
 * is no default for this parameter.  Leaving it undefined means
 * groups are not implemented using MySQL tables.  AuthMySQLGroupTable
 * specifies the table to use to get the group info.  It defaults to
 * the value of AuthMySQLUserTable.  If you are not using groups, you
 * do not need a "user_group" field in your database, obviously.
 *
 * A user can be a member of multiple groups, but in this case the
 * user id field *cannot* be PRIMARY KEY.  You need to have multiple
 * rows with the same user ID, one per group to which that ID belongs.
 * In this case, you MUST put the GroupTable on a separate table from
 * the user table.  This is to help prevent the user table from having
 * inconsistent passwords in it.  If each user is only in one group,
 * then the group field can be in the same table as the password
 * field.  A group-only table might look like this:
 *
 *  CREATE TABLE user_group (
 *    user_name char(50) DEFAULT '' NOT NULL,
 *    user_group char(20) DEFAULT '' NOT NULL,
 *    create_date int,
 *    expire_date int,
 *    PRIMARY KEY (user_name,user_group)
 *  );
 *
 * note that you still need a user table which has the passwords in it.
 *
 * based on my "mod_auth_msql.c,v 1.13 1996/12/19 18:42:48"
 * $Id: mod_auth_mysql.c,v 1.11 2001/08/30 18:37:11 khera Exp $
 * */

#include "httpd.h"
#include "http_config.h"
#include "http_core.h"
#include "http_log.h"
#include "http_protocol.h"
#include <mysql/mysql.h>

/*
 * structure to hold the configuration details for the request
 */
typedef struct  {
  char *mysqlhost;		/* host name of db server */
  char *mysqluser;		/* user ID to connect to db server */
  char *mysqlpasswd;		/* password to connect to db server */
  char *mysqlDB;		/* DB name */
  char *mysqlpwtable;		/* user password table */
  char *mysqlgrptable;		/* user group table */
  char *mysqlNameField;		/* field in password/grp table with username */
  char *mysqlPasswordField;	/* field in password table with password */
  char *mysqlGroupField;	/* field in group table with group name */
  int  mysqlCrypted;		/* are passwords encrypted? */
  int  mysqlKeepAlive;		/* keep connection persistent? */
  int  mysqlAuthoritative;	/* are we authoritative? */
  int  mysqlNoPasswd;		/* do we ignore password? */
} mysql_auth_config_rec;

/*
 * Global handle to db.  If not null, assume it is still valid.
 * MySQL in recent incarnations will re-connect automatically if the
 * connection is closed, so we don't worry about that here.
 */
static MYSQL *mysql_handle = NULL;

/*
 * Callback to close mysql handle when necessary.  Also called when a
 * child httpd process is terminated.
 */
static void
mod_auth_mysql_cleanup (void *notused)
{
  if (mysql_handle) mysql_close(mysql_handle);
  mysql_handle = NULL;		/* make sure we don't try to use it later */
}

/*
 * empty function necessary because register_cleanup requires it as one
 * of its parameters
 */
static void
mod_auth_mysql_cleanup_child (void *notused)
{
  /* nothing */
}

/*
 * handler to do cleanup on child exit
 */
static void
child_exit(server_rec *s, pool *p)
{
  mod_auth_mysql_cleanup(NULL);
}


/*
 * open connection to DB server if necessary.  Return TRUE if connection
 * is good, FALSE if not able to connect.  If false returned, reason
 * for failure has been logged to error_log file already.
 */
#ifndef TRUE
#define TRUE 1
#endif
#ifndef FALSE
#define FALSE 0
#endif

static int
open_db_handle(request_rec *r, mysql_auth_config_rec *m)
{
  static MYSQL mysql_conn;
  char *db_host;

  if (mysql_handle) return TRUE; /* already open */

  if (!m->mysqlhost || strcmp(m->mysqlhost,"localhost") == 0) {
    db_host = NULL;
  } else {
    db_host = m->mysqlhost;
  }

  mysql_handle=mysql_connect(&mysql_conn,db_host,m->mysqluser,m->mysqlpasswd);

  if (mysql_handle) {

    if (!m->mysqlKeepAlive) {
      /* close when request done */
      ap_register_cleanup(r->pool, (void *)NULL,
			  mod_auth_mysql_cleanup,
			  mod_auth_mysql_cleanup_child);
    } /* ELSE...
       * Child process is notified when it is terminated so we
       * do a graceful close to the server in that handler.
       */

  } else {			/* failed to get MySQL connection */
    ap_log_error (APLOG_MARK, APLOG_ERR, r->server,
		  "MySQL error: %s", mysql_error(&mysql_conn));
    return FALSE;
  }

  return TRUE;
}


static void *
create_mysql_auth_dir_config (pool *p, char *d)
{
  mysql_auth_config_rec *m = ap_pcalloc (p, sizeof(mysql_auth_config_rec));
  if (!m) return NULL;		/* failure to get memory is a bad thing */

  /* defaults values */
  m->mysqlNameField = "user_name";
  m->mysqlPasswordField = "user_passwd";
  m->mysqlCrypted = 1;		/* passwords are encrypted */
  m->mysqlKeepAlive = 0;	/* do not keep persistent connection */
  m->mysqlAuthoritative = 1;	/* we are authoritative source for users */
  m->mysqlNoPasswd = 0;		/* we require password */
  return (void *)m;
}

static
command_rec mysql_auth_cmds[] = {
  { "AuthMySQLHost", ap_set_string_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlhost),
    OR_AUTHCFG, TAKE1, "mysql server host name" },
  { "AuthMySQLUser", ap_set_string_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqluser),
    OR_AUTHCFG, TAKE1, "mysql server user name" },
  { "AuthMySQLPassword", ap_set_string_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlpasswd),
    OR_AUTHCFG, TAKE1, "mysql server user password" },
  { "AuthMySQLDB", ap_set_string_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlDB),
    OR_AUTHCFG, TAKE1, "mysql database name" },
  { "AuthMySQLUserTable", ap_set_string_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlpwtable),
    OR_AUTHCFG, TAKE1, "mysql user table name" },
  { "AuthMySQLGroupTable", ap_set_string_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlgrptable),
    OR_AUTHCFG, TAKE1, "mysql group table name" },
  { "AuthMySQLNameField", ap_set_string_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlNameField),
    OR_AUTHCFG, TAKE1, "mysql User ID field name within table" },
  { "AuthMySQLGroupField", ap_set_string_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlGroupField),
    OR_AUTHCFG, TAKE1, "mysql Group field name within table" },
  { "AuthMySQLPasswordField", ap_set_string_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlPasswordField),
    OR_AUTHCFG, TAKE1, "mysql Password field name within table" },
  { "AuthMySQLCryptedPasswords", ap_set_flag_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlCrypted),
    OR_AUTHCFG, FLAG, "mysql passwords are stored encrypted if On" },
  { "AuthMySQLKeepAlive", ap_set_flag_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlKeepAlive),
    OR_AUTHCFG, FLAG, "mysql connection kept open across requests if On" },
  { "AuthMySQLAuthoritative", ap_set_flag_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlAuthoritative),
    OR_AUTHCFG, FLAG, "mysql lookup is authoritative if On" },
  { "AuthMySQLNoPasswd", ap_set_flag_slot,
    (void*)XtOffsetOf(mysql_auth_config_rec, mysqlNoPasswd),
    OR_AUTHCFG, FLAG, "If On, only check if user exists; ignore password" },
  { NULL }
};

module mysql_auth_module;

/*
 * Fetch and return password string from database for named user.
 * If we are in NoPasswd mode, returns user name instead.
 * If user or password not found, returns NULL
 */
static char *
get_mysql_pw(request_rec *r, char *user, mysql_auth_config_rec *m)
{
  MYSQL_RES *result;
  char *pw = NULL;		/* password retrieved */
  char *sql_safe_user = NULL;
  int ulen;
  char query[MAX_STRING_LEN];

  if(!open_db_handle(r,m)) {
    return NULL;		/* failure reason already logged */
  }

  if (mysql_select_db(mysql_handle,m->mysqlDB) != 0) {
    ap_log_error (APLOG_MARK, APLOG_ERR, r->server,
		  "MySQL error: %s", mysql_error(mysql_handle));
    return NULL;
  }

  /*
   * If we are not checking for passwords, there may not be a password field
   * in the database.  We just look up the name field value in this case
   * since it is guaranteed to exist.
   */
  if (m->mysqlNoPasswd) {
    m->mysqlPasswordField = m->mysqlNameField;
  }

  ulen = strlen(user);
  sql_safe_user = ap_pcalloc(r->pool, ulen*2+1);
  mysql_escape_string(sql_safe_user,user,ulen);
  ap_snprintf(query,sizeof(query)-1,"SELECT %s FROM %s WHERE %s='%s'",
	      m->mysqlPasswordField, m->mysqlpwtable,
	      m->mysqlNameField, sql_safe_user);
  if (mysql_query(mysql_handle, query) != 0) {
    ap_log_error (APLOG_MARK, APLOG_ERR, r->server,
		  "MySQL error %s: %s", mysql_error(mysql_handle),r->uri);
    return NULL;
  }

  result = mysql_store_result(mysql_handle);
  if (result && (mysql_num_rows(result) == 1)) {
    MYSQL_ROW data = mysql_fetch_row(result);
    if (data[0]) {
      pw = ap_pstrdup(r->pool, data[0]);
    } else {		/* no password in mysql table returns NULL */
      /* this should never happen, but test for it anyhow */
      ap_log_error(APLOG_MARK, APLOG_NOERRNO|APLOG_ERR, r->server,
		   "MySQL user %s has no valid password: %s", user, r->uri);
      mysql_free_result(result);
      return NULL;
    }
  }

  if (result) mysql_free_result(result);

  return pw;
}

/*
 * get list of groups from database.  Returns array of pointers to strings
 * the last of which is NULL.  returns NULL pointer if user is not member
 * of any groups.
 */
static char **
get_mysql_groups(request_rec *r, char *user, mysql_auth_config_rec *m)
{
  MYSQL_RES *result;
  char **list = NULL;
  char query[MAX_STRING_LEN];
  char *sql_safe_user;
  int ulen;

  if(!open_db_handle(r,m)) {
    return NULL;		/* failure reason already logged */
  }

  if (mysql_select_db(mysql_handle,m->mysqlDB) != 0) {
    ap_log_error (APLOG_MARK, APLOG_ERR, r->server,
		  "MySQL error %s: %s", mysql_error(mysql_handle),r->uri);
    return NULL;
  }

  ulen = strlen(user);
  sql_safe_user = ap_pcalloc(r->pool, ulen*2+1);
  mysql_escape_string(sql_safe_user,user,ulen);
  ap_snprintf(query,sizeof(query)-1,"SELECT %s FROM %s WHERE %s='%s'",
	      m->mysqlGroupField, m->mysqlgrptable,
	      m->mysqlNameField, sql_safe_user);
  if (mysql_query(mysql_handle, query) != 0) {
    ap_log_error (APLOG_MARK, APLOG_ERR, r->server,
		  "MySQL error %s: %s", mysql_error(mysql_handle),r->uri);
    return NULL;
  }

  result = mysql_store_result(mysql_handle);
  if (result && (mysql_num_rows(result) > 0)) {
    int i = mysql_num_rows(result);
    list = (char **)ap_pcalloc(r->pool, sizeof(char *) * (i+1));
    list[i] = NULL;		/* last element in array is NULL */
    while (i--) {		/* populate the array elements */
      MYSQL_ROW data = mysql_fetch_row(result);
      if (data[0])
	list[i] = ap_pstrdup(r->pool, data[0]);
      else
	list[i] = "";		/* if no data, make it empty, not NULL */
    }
  }

  if (result) mysql_free_result(result);

  return list;
}

/*
 * callback from Apache to do the authentication of the user to his
 * password.
 */
static int
mysql_authenticate_basic_user (request_rec *r)
{
  mysql_auth_config_rec *sec =
    (mysql_auth_config_rec *)ap_get_module_config (r->per_dir_config,
						   &mysql_auth_module);
  conn_rec *c = r->connection;
  const char *sent_pw, *real_pw;
  int res;

  if ((res = ap_get_basic_auth_pw (r, &sent_pw)))
    return res;

  if(!sec->mysqlpwtable)	/* not configured for mysql authorization */
    return DECLINED;

  if(!(real_pw = get_mysql_pw(r, c->user, sec))) {
    /* user not found in database */
    if (!sec->mysqlAuthoritative)
      return DECLINED;		/* let other schemes find user */

    ap_log_error(APLOG_MARK, APLOG_NOERRNO|APLOG_ERR, r->server,
		 "MySQL user %s not found: %s", c->user, r->uri);
    ap_note_basic_auth_failure (r);
    return AUTH_REQUIRED;
  }

  /* if we don't require password, just return ok since they exist */
  if (sec->mysqlNoPasswd) {
    return OK;
  }

  /* compare the password, possibly encrypted */
  if(strcmp(real_pw, sec->mysqlCrypted ? crypt(sent_pw,real_pw) : sent_pw)) {
    ap_log_error(APLOG_MARK, APLOG_NOERRNO|APLOG_ERR, r->server,
		 "user %s: password mismatch: %s", c->user, r->uri);
    ap_note_basic_auth_failure (r);
    return AUTH_REQUIRED;
  }
  return OK;
}

/*
 * check if user is member of at least one of the necessary group(s)
 */
static int
mysql_check_auth(request_rec *r)
{
  mysql_auth_config_rec *sec =
    (mysql_auth_config_rec *)ap_get_module_config(r->per_dir_config,
						  &mysql_auth_module);
  char *user = r->connection->user;
  int method = r->method_number;

  const array_header *reqs_arr = ap_requires(r);
  require_line *reqs = reqs_arr ? (require_line *)reqs_arr->elts : NULL;

  register int x;
  char **groups = NULL;

  if (!sec->mysqlGroupField) return DECLINED; /* not doing groups here */
  if (!reqs_arr) return DECLINED; /* no "require" line in access config */

  /* if the group table is not specified, use the same as for password */
  if (!sec->mysqlgrptable) sec->mysqlgrptable = sec->mysqlpwtable;

  for(x = 0; x < reqs_arr->nelts; x++) {
    const char *t, *want;

    if (!(reqs[x].method_mask & (1 << method))) continue;

    t = reqs[x].requirement;
    want = ap_getword(r->pool, &t, ' ');

    if(!strcmp(want,"group")) {
      /* check for list of groups from database only first time thru */
      if (!groups && !(groups = get_mysql_groups(r, user, sec))) {
	ap_log_error(APLOG_MARK, APLOG_NOERRNO|APLOG_ERR, r->server,
		     "mysql user %s not in group table %s: %s",
		     user, sec->mysqlgrptable, r->uri);
	ap_note_basic_auth_failure(r);
	return AUTH_REQUIRED;
      }

      /* loop through list of groups specified in htaccess file */
      while(t[0]) {
	int i = 0;
	want = ap_getword(r->pool, &t, ' ');
	/* compare against each group to which this user belongs */
	while(groups[i]) {	/* last element is NULL */
	  if(!strcmp(groups[i],want))
	    return OK;		/* we found the user! */
	  ++i;
	}
      }
      ap_log_error(APLOG_MARK, APLOG_NOERRNO|APLOG_ERR, r->server,
		   "mysql user %s not in right group: %s",user,r->uri);
      ap_note_basic_auth_failure(r);
      return AUTH_REQUIRED;
    }
  }

  return DECLINED;
}


module mysql_auth_module = {
   STANDARD_MODULE_STUFF,
   NULL,			/* initializer */
   create_mysql_auth_dir_config, /* dir config creater */
   NULL,			/* dir merger --- default is to override */
   NULL,			/* server config */
   NULL,			/* merge server config */
   mysql_auth_cmds,		/* command table */
   NULL,			/* handlers */
   NULL,			/* filename translation */
   mysql_authenticate_basic_user, /* check_user_id */
   mysql_check_auth,		/* check auth */
   NULL,			/* check access */
   NULL,			/* type_checker */
   NULL,			/* fixups */
   NULL,			/* logger */
   NULL,			/* header parser */
   NULL,			/* child_init */
   child_exit,			/* child_exit */
   NULL				/* post read-request */
};
