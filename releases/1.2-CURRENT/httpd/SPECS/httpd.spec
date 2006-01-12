#
# spec file for package httpd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		httpd
%define version		2.0.54
%define release		4avx

#
#(ie. use with rpm --rebuild):
#
#	--with debug	Compile with debugging code
# 
#  enable build with debugging code: will _not_ strip away any debugging code,
#  will _add_ -g3 to CFLAGS, will _add_ --enable-maintainer-mode to 
#  configure.

%define mmn		20020903

%define dbver		db4
%define dbmver		db4

# not everyone uses this, so define it here
%define distribution	Annvix
%define build_debug	0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_debug: %{expand: %%define build_debug 1}}

%if %{build_debug}
# disable build root strip policy
%define __spec_install_post %{_prefix}/lib/rpm/brp-compress || :

# This gives extra debuggin and huge binaries
%{expand:%%define optflags %{optflags} %([ ! $DEBUG ] && echo '-g3')}
%endif

%define ap_ldap_libs	-lldap -llber -lsasl2 -lssl -lcrypto
%define ap_ssl_libs	-lssl -lcrypto

%define ap_version	%{version}
%define ap_release	%{release}
%define sourcename	httpd-%{version}
%define srcdir		%{_prefix}/src/httpd-%{version}

# the name for libapr will be different on 64bit
%define libapr		%mklibname apr 0

Summary:	Apache web server (prefork mpm)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://httpd.apache.org
Source0:	http://archive.apache.org/dist/httpd/%{sourcename}.tar.gz
Source1:	http://archive.apache.org/dist/httpd/%{sourcename}.tar.gz.asc
Source2: 	httpd-README.urpmi
Source3:	apache2_transparent_png_icons.tar.bz2
Source4:	mod_backtrace.c.bz2
Source5:	mod_whatkilledus.c.bz2
Source6:	test_char.h.bz2
# please keep this logic.
Source30:	30_mod_proxy.conf.bz2
Source45: 	45_mod_dav.conf.bz2
Source46: 	46_mod_ldap.conf.bz2
Source55:	55_mod_cache.conf.bz2
Source56:	56_mod_disk_cache.conf.bz2
Source57:	57_mod_mem_cache.conf.bz2
Source58:	58_mod_file_cache.conf.bz2
Source59:	59_mod_deflate.conf.bz2
Source67:	67_mod_userdir.conf.bz2
# Provide a simpler buildconf script
Source100:	buildconf.bz2

# OE: from Fedora
# build/scripts patches
Patch1:		httpd-2.0.40-apctl.patch.bz2
Patch2:		httpd-2.0.36-apxs.patch.bz2
Patch3:		httpd-2.0.48-linkmods.patch.bz2
Patch4:		httpd-2.0.45-deplibs.patch.bz2
Patch5:		httpd-2.0.47-pie.patch.bz2
Patch6:		httpd-2.0.45-syspcre.patch.bz2
Patch8:		httpd-2.0.48-vpathinc.patch.bz2
Patch9:		httpd-2.0.52-apctlopts.patch.bz2
#
# Bug fixes
Patch20:	httpd-2.0.45-encode.patch.bz2
Patch21:	httpd-2.0.45-davetag.patch.bz2
Patch22:	httpd-2.0.47-ldapshm.patch.bz2
Patch23:	httpd-2.0.48-vhost.patch.bz2
Patch24:	httpd-2.0.46-sslmutex.patch.bz2
Patch25:	httpd-2.0.46-md5dig.patch.bz2
Patch26:	httpd-2.0.48-proxy11.patch.bz2
Patch27:	httpd-2.0.48-sslpphrase.patch.bz2
Patch28:	httpd-2.0.48-worker.patch.bz2
Patch29:	httpd-2.0.48-workerhup.patch.bz2
Patch30:	httpd-2.0.48-davmisc.patch.bz2
Patch31:	httpd-2.0.54-ssltrans.patch.bz2
Patch32:	httpd-2.0.54-userdir.patch.bz2
Patch33:	httpd-2.0.54-ldapconn.patch.bz2
Patch34:	httpd-2.0.52-pipedlog1.patch.bz2
Patch35:	httpd-2.0.52-pipedlog2.patch.bz2
#
# Features/functional changes
Patch71:	httpd-2.0.40-xfsz.patch.bz2
Patch72:	httpd-2.0.40-pod.patch.bz2
Patch73:	httpd-2.0.40-noshmht.patch.bz2
Patch74:	httpd-2.0.45-export.patch.bz2
Patch75:	httpd-2.0.48-dynlimit.patch.bz2
Patch76:	httpd-2.0.48-dynamic.patch.bz2
Patch77:	httpd-2.0.48-sslstatus.patch.bz2
Patch78:	httpd-2.0.48-corelimit.patch.bz2
Patch80:	httpd-2.0.48-distcache.patch.bz2
Patch81:	httpd-2.0.48-debuglog.patch.bz2
Patch82:	httpd-2.0.48-abench.patch.bz2
Patch84:	httpd-2.0.48-sslheader.patch.bz2
Patch85:	httpd-2.0.48-sslvars2.patch.bz2
Patch89:	httpd-2.0.49-headerssl.patch.bz2
Patch90:	httpd-2.0.49-workerstack.patch.bz2
Patch91:	httpd-2.0.46-testhook.patch.bz2
Patch92:	httpd-2.0.46-dumpcerts.patch.bz2
#
# http://lists.debian.org/debian-apache/2003/11/msg00109.html
Patch100:	httpd-2.0.48-bsd-ipv6-fix.diff.bz2
#
# OE: prepare for the mod_limitipconn module found here:
# http://dominia.org/djao/limitipconn.html
Patch101:	apachesrc.diff.bz2
# JMD: fix suexec path so we can have both versions of Apache and both
# versions of suexec
Patch102:	apache2-suexec.patch.bz2
Patch103:	httpd-2.0.49-mod_ldap_cache_file_location.diff.bz2
# OE: add the peruser mpm
# http://www.telana.com/peruser.php
Patch104:       http://www.telana.com/files/httpd-2.0.52-peruser-0.1.5.patch.bz2
Patch105:	httpd-2.0.55-cvs-pemcallback.patch.bz2
# security fixes
Patch122:	httpd-2.0.52-CAN-2005-1268.patch.bz2
Patch123:	httpd-2.0.52-CAN-2005-2088.patch.bz2
Patch124:	httpd-2.0.52-CAN-2005-2700.patch.bz2
Patch125:	httpd-2.0.52-CAN-2005-2728.patch.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	apr-devel >= 0.9.6-4avx, apr-util-devel >= 0.9.6-4avx, pcre-devel >= 5.0, byacc
BuildRequires:	%{dbver}-devel, expat-devel, gdbm-devel, openldap-devel, libsasl-devel
BuildRequires:	libtool >= 1.4.2, openssl-devel, autoconf2.5, automake1.7, pkgconfig, zlib-devel
BuildRequires:	multiarch-utils >= 1.0.3

Requires:	libapr-util >= 0.9.6-4avx, %{libapr} >= 1:0.9.6-4avx
Requires:	httpd-conf >= 2.0.54-1avx, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(pre):	rpm-helper, httpd-conf >= 2.0.54-1avx, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(preun): libapr-util >= 0.9.6-4avx, %{libapr} >= 1:0.9.6-4avx
Requires(post):	libapr-util >= 0.9.6-4avx, %{libapr} >= 1:0.9.6-4avx
Requires(postun): rpm-helper
Provides:	webserver apache apache2 apache-mpm apache2-prefork httpd-mpm
Provides:	httpd-prefork = %{version}-%{release}
Obsoletes:	apache2

%description
This package contains the main binary of Apache, a powerful,
full-featured, efficient and freely-available Web server. Apache
is also the most popular Web server on the Internet.

This version of Apache is fully modular, and many modules are
available in pre-compiled formats, like PHP4 and
mod_auth_external.

You can build Apache with some conditional build switches;

(ie. use with rpm --rebuild):
--with debug   Compile with debugging code


%package worker
Summary:	Apache web server (worker mpm)
Group:		System/Servers
Requires:	libapr-util >= 0.9.6-4avx, %{libapr} >= 1:0.9.6-4avx
Requires:	httpd-conf >= 2.0.54-1avx, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(pre):	rpm-helper, httpd-conf >= 2.0.54-1avx, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(preun): libapr-util >= 0.9.6-4avx, %{libapr} >= 1:0.9.6-4avx
Requires(post):	libapr-util >= 0.9.6-4avx, %{libapr} >= 1:0.9.6-4avx
Requires(postun): rpm-helper
Provides:	webserver apache apache2 apache-mpm apache2-worker httpd-mpm
Provides:	%{name} = %{version}-%{release}
Obsoletes:	apache2-worker

%description worker
This package contains the main binary of Apache, a powerful,
full-featured, efficient and freely-available Web server. Apache
is also the most popular Web server on the Internet.

This version of Apache is fully modular, and many modules are
available in pre-compiled formats, like PHP4 and mod_auth_external.

I M P O R T A N T
-----------------

Note that the worker mpm (this package) requires thread safe
modules. This  package is totally experimental and may not be stable
or suitable at any time, in any way, or for any kind production
usage. Be warned.


%package common
Summary:	Files common for httpd and httpd-mod_perl installations
Group:		System/Servers
Requires:	libapr-util >= 0.9.6-4avx, %{libapr} >= 1:0.9.6-4avx
Requires(pre):	rpm-helper
Requires(preun): libapr-util >= 0.9.6-4avx, %{libapr} >= 1:0.9.6-4avx
Requires(post):	libapr-util >= 0.9.6-4avx, %{libapr} >= 1:0.9.6-4avx
Requires(postun): rpm-helper
Prereq:		rpm-helper
Prereq:		libapr-util >= 0.9.6-4avx
Prereq:		%{libapr} >= 1:0.9.6-4avx
Obsoletes:	apache2-common
Provides:	apache2-common

%description common
This package contains files required for both httpd and httpd-mod_perl
package installations. Install this if you want to install Apache and/
or Apache with mod_perl.


%package modules
Summary:	Standard modules for Apache
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Provides:	httpd-mod_access = %{version}
Provides:	httpd-mod_actions = %{version}
Provides:	httpd-mod_alias = %{version}
Provides:	httpd-mod_asis = %{version}
Provides:	httpd-mod_auth = %{version}
Provides:	httpd-mod_auth_anon = %{version}
Provides:	httpd-mod_auth_dbm = %{version}
Provides:	httpd-mod_auth_digest = %{version}
Provides:	httpd-mod_autoindex = %{version}
Provides:	httpd-mod_case_filter = %{version}
Provides:	httpd-mod_case_filter_in = %{version}
Provides:	httpd-mod_cern_meta = %{version}
Provides:	httpd-mod_cgi = %{version}
Provides:	httpd-mod_cgid = %{version}
Provides:	httpd-mod_charset_lite = %{version}
Provides:	httpd-mod_dir = %{version}
Provides:	httpd-mod_env = %{version}
Provides:	httpd-mod_expires = %{version}
Provides:	httpd-mod_ext_filter = %{version}
Provides:	httpd-mod_headers = %{version}
Provides:	httpd-mod_imap = %{version}
Provides:	httpd-mod_include = %{version}
Provides:	httpd-mod_info = %{version}
Provides:	httpd-mod_log_config = %{version}
Provides:	httpd-mod_logio = %{version}
Provides:	httpd-mod_log_forensic = %{version}
Provides:	httpd-mod_mime = %{version}
Provides:	httpd-mod_mime_magic = %{version}
Provides:	httpd-mod_negotiation = %{version}
Provides:	httpd-mod_rewrite = %{version}
Provides:	httpd-mod_setenvif = %{version}
Provides:	httpd-mod_speling = %{version}
Provides:	httpd-mod_status = %{version}
Provides:	httpd-mod_unique_id = %{version}
Provides:	httpd-mod_userdir = %{version}
Provides:	httpd-mod_usertrack = %{version}
Provides:	httpd-mod_vhost_alias = %{version}
Provides:	httpd-mod_dumpio = %{version}
%if %{build_debug}
Provides:	httpd-mod_backtrace = %{version}
Provides:	apacee-mod_whatkilledus = %{version}
%endif
Obsoletes:	apache2-mod_access apache2-mod_actions apache2-mod_alias apache2-mod_asis apache2-mod_auth apache2-mod_auth_anon
Obsoletes:	apache2-mod_auth_dbm apache2-mod_auth_digest apache2-mod_autoindex apache2-mod_case_filter apache2-mod_case_filter_in
Obsoletes:	apache2-mod_cern_meta apache2-mod_cgi apache2-mod_cgid apache2-mod_charset_lite apache2-mod_dir apache2-mod_env
Obsoletes:	apache2-mod_expires apache2-mod_ext_filter apache2-mod_headers apache2-mod_imap apache2-mod_include apache2-mod_info
Obsoletes:	apache2-mod_log_config apache2-mod_logio apache2-mod_log_forensic apache2-mod_mime apache2-mod_mime_magic
Obsoletes:	apache2-mod_negotiation apache2-mod_rewrite apache2-mod_setenvif apache2-mod_speling apache2-mod_status
Obsoletes:	apache2-mod_unique_id apache2-mod_userdir apache2-mod_usertrack apache2-mod_vhost_alias apache2-mod_dumpio apache2-modules
Provides:	apache2-mod_access apache2-mod_actions apache2-mod_alias apache2-mod_asis apache2-mod_auth apache2-mod_auth_anon
Provides:	apache2-mod_auth_dbm apache2-mod_auth_digest apache2-mod_autoindex apache2-mod_case_filter apache2-mod_case_filter_in
Provides:	apache2-mod_cern_meta apache2-mod_cgi apache2-mod_cgid apache2-mod_charset_lite apache2-mod_dir apache2-mod_env
Provides:	apache2-mod_expires apache2-mod_ext_filter apache2-mod_headers apache2-mod_imap apache2-mod_include apache2-mod_info
Provides:	apache2-mod_log_config apache2-mod_logio apache2-mod_log_forensic apache2-mod_mime apache2-mod_mime_magic
Provides:	apache2-mod_negotiation apache2-mod_rewrite apache2-mod_setenvif apache2-mod_speling apache2-mod_status
Provides:	apache2-mod_unique_id apache2-mod_userdir apache2-mod_usertrack apache2-mod_vhost_alias apache2-mod_dumpio apache2-modules


%description modules
This package contains standard modules for Apache. It is required
for normal operation of the web server.


%package mod_dav
Summary:	Distributed Authoring and Versioning (WebDAV)
Group:		System/Servers
Requires(pre):	rpm-helper, httpd-conf >= %{version}, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper
Prereq:		httpd-conf
Prereq:		httpd-common = %{version}
Prereq:		httpd-modules = %{version}
Provides:	httpd-mod_dav_fs = %{version}
Obsoletes:	apache2-mod_dav apache2-mod_dav_fs
Provides:	apache2-mod_dav = %{version}, apache2-mod_dav_fs = %{version}

%description mod_dav
This module provides class 1 and class 2 WebDAV ('Web-based
Distributed Authoring and Versioning') functionality for Apache.

This extension to the HTTP protocol allows creating, moving,
copying, and deleting resources and collections on a remote web
server.


%package mod_ldap
Summary:	LDAP connection pooling and result caching DSO:s
Group:		System/Servers
Requires(pre):	rpm-helper, httpd-conf >= %{version}, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper
Provides:	httpd-mod_auth_ldap = %{version}
Obsoletes:	apache2-mod_ldap apache2-mod_auth_ldap
Provides:	apache2-mod_ldap = %{version}, apache2-mod_auth_ldap = %{version}

%description mod_ldap
This module was created to improve the performance of websites
relying on backend connections to LDAP servers. In addition to the
functions provided by the standard LDAP libraries, this module adds
an LDAP connection pool and an LDAP shared memory cache.


%package mod_cache
Summary:	Content cache keyed to URIs
Group:		System/Servers
Requires(pre):	rpm-helper, httpd-conf >= %{version}, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper
Obsoletes:	apache2-mod_cache
Provides:	apache2-mod_cache = %{version}

%description mod_cache
mod_cache implements an RFC 2616 compliant HTTP content cache that
can be used to cache either local or proxied content. mod_cache
requires the services of one or more storage management modules.

Two storage management modules are included in the base Apache
distribution:

* mod_disk_cache - implements a disk based storage manager for
  use with mod_proxy.
* mod_mem_cache - implements an in-memory based storage manager.

mod_mem_cache can be configured to operate in two modes: caching
open file descriptors or caching objects in heap storage.

mod_mem_cache is most useful when used to cache locally generated
content or to cache backend server content for mod_proxy
configured for ProxyPass (aka reverse proxy)


%package mod_disk_cache
Summary:	Implements a disk based storage manager
Group:		System/Servers
Requires(pre):	rpm-helper, httpd-conf >= %{version}, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(pre):	httpd-mod_cache = %{version}-%{release}
Requires(postun): rpm-helper
Obsoletes:	apache2-mod_cache
Provides:	apache2-mod_cache = %{version}

%description mod_disk_cache
mod_disk_cache implements a disk based storage manager. It is
primarily of use in conjunction with mod_proxy.

Content is stored in and retrieved from the cache using URI-based
keys. Content with access protection is not cached.


%package mod_mem_cache
Summary:	Implements a memory based storage manager
Group:		System/Servers
Requires(pre):	rpm-helper, httpd-conf >= %{version}, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(pre):	httpd-mod_cache = %{version}-%{release}
Requires(postun): rpm-helper
Obsoletes:	apache2-mod_mem_cache
Provides:	apache2-mod_mem_cache = %{version}

%description mod_mem_cache
This module requires the service of mod_cache. It acts as a
support module for mod_cache and provides a memory based storage
manager. mod_mem_cache can be configured to operate in two modes:
caching open file descriptors or caching objects in heap storage.
mod_mem_cache is most useful when used to cache locally generated
content or to cache backend server content for mod_proxy configured
for ProxyPass (aka reverse proxy).

Content is stored in and retrieved from the cache using URI-based
keys. Content with access protection is not cached.


%package mod_file_cache
Summary:	Caches a static list of files in memory
Group:		System/Servers
Requires(pre):	rpm-helper, httpd-conf >= %{version}, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper
Obsoletes:	apache2-mod_file_cache
Provides:	apache2-mod_file_cache = %{version}

%description mod_file_cache
Caching frequently requested files that change very infrequently
is a technique for reducing server load. mod_file_cache provides
two techniques for caching frequently requested static files.

Through configuration directives, you can direct mod_file_cache to
either open then mmap()a file, or to pre-open a file and save the
file's open file handle. Both techniques reduce server load when
processing requests for these files by doing part of the work
(specifically, the file I/O) for serving the file when the server
is started rather than during each request.

Notice: You cannot use this for speeding up CGI programs or other
files which are served by special content handlers. It can only be
used for regular files which are usually served by the Apache core
content handler.

This module is an extension of and borrows heavily from the
mod_mmap_static module in Apache 1.3.


%package mod_deflate
Summary:	Compress content before it is delivered to the client
Group:		System/Servers
Requires(pre):	rpm-helper, httpd-conf >= %{version}, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper
Provides:	mod_gzip
Obsoletes:	mod_gzip
Obsoletes:	apache2-mod_deflate
Provides:	apache2-mod_deflate = %{version}

%description mod_deflate
The mod_deflate module provides the DEFLATE output filter that
allows output from your server to be compressed before being sent
to the client over the network.


%package mod_proxy
Summary:	HTTP/1.1 proxy/gateway server
Group:		System/Servers
Requires(pre):	rpm-helper, httpd-conf >= %{version}, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(pre):	httpd-mod_cache = %{version}-%{release}, httpd-mod_disk_cache = %{version}-%{release}
Requires(postun): rpm-helper
Provides:	httpd-mod_proxy_connect = %{version}
Provides:	httpd-mod_proxy_ftp = %{version}
Provides:	httpd-mod_proxy_http = %{version}
Obsoletes:	apache2-mod_proxy apache2-mod_proxy_http apache2-mod_proxy_ftp apache2-mod_proxy-connect
Provides:	apache2-mod_proxy = %{version}, apache2-mod_proxy_http = %{version}
Provides:	apache2-mod_proxy_ftp = %{version}, apache2-mod_proxy-connect = %{version}

%description mod_proxy
This module implements a proxy/gateway for Apache. It implements
proxying capability for FTP, CONNECT (for SSL), HTTP/0.9,
HTTP/1.0, and HTTP/1.1. The module can be configured to connect
to other proxy modules for these and other protocols.

This module was experimental in Apache 1.1.x. Improvements and
bugfixes were made in Apache v1.2.x and Apache v1.3.x, then the
module underwent a major overhaul for Apache v2.0. The protocol
support was upgraded to HTTP/1.1, and filter support was enabled.

Please note that the caching function present in mod_proxy up
to Apache v2.0.39 has been removed from mod_proxy and is 
incorporated into a new module, mod_cache.


%package mod_userdir
Summary:	User-specific directories
Group:		System/Servers
Requires(pre):	rpm-helper, httpd-conf >= %{version}, httpd-common = %{version}-%{release}, httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper
Provides:	apache2-mod_userdir = %{version}
Obsoletes:	apache2-mod_userdir

%description mod_userdir
This module allows user-specific directories to be accessed using the
http://example.com/~username/ syntax.


%package devel
Summary:	Module development tools for the Apache web server
Group:		Development/C
Requires:	apr-devel >= 0.9.6-4avx, apr-util-devel >= 0.9.6-4avx, pcre-devel >= 5.0, byacc
Requires:	%{dbver}-devel, expat-devel, gdbm-devel, openldap-devel, libsasl-devel
Requires:	libtool >= 1.4.2, openssl-devel, autoconf2.5, automake1.7, pkgconfig
Provides:	httpd-devel httpd-mod_ssl-devel
Provides:	apache2-devel apache2-mod_ssl-devel apache-mod_ssl-devel
Obsoletes:	apache2-devel apache2-mod_ssl-devel

%description devel
The httpd-devel package contains the source code for the Apache
Web server and the APXS binary you'll need to build Dynamic
Shared Objects (DSOs) for Apache.


%package source
Summary:	The Apache Source
Group:		Development/C

%description source
The Apache Source, including %{distribution} patches. Use this package to
build httpd-mod_perl, or your own custom version.


%prep
%setup -q -n %{sourcename}
# OE: from Fedora
%patch1 -p1 -b .apctl.droplet
%patch2 -p1 -b .apxs.droplet
%patch3 -p1 -b .linkmods.droplet
%patch4 -p1 -b .deplibs.droplet
%patch6 -p1 -b .syspcre.droplet
%patch8 -p1 -b .vpathinc.droplet
%patch9 -p1 -b .apctlopts.droplet
#
%patch20 -p1
%patch21 -p1 -b .davetag.droplet
%patch22 -p1 -b .ldapshm.droplet
%patch23 -p1 -b .vhost.droplet
%patch24 -p1 -b .sslmutex.droplet
%patch25 -p1 -b .md5dig.droplet
%patch26 -p1 -b .proxy11.droplet
%patch27 -p1 -b .sslpphrase.droplet
%patch28 -p1 -b .worker.droplet
%patch29 -p1 -b .workerhup.droplet
%patch30 -p1 -b .davmisc.droplet
%patch31 -p1 -b .ssltrans.droplet
%patch32 -p1 -b .userdir.droplet
%patch33 -p1 -b .ldapconn.droplet
%patch34 -p1 -b .pipedlog1.droplet
%patch35 -p1 -b .pipedlog2.droplet
%patch71 -p0 -b .xfsz.droplet
%patch72 -p1 -b .pod.droplet
%patch73 -p1 -b .noshmht.droplet
%patch74 -p1 -b .export.droplet
%patch75 -p1 -b .dynlimit.droplet
%patch76 -p1 -b .dynamic.droplet
%patch77 -p1 -b .sslstatus.droplet
%patch78 -p1 -b .corelimit.droplet
%patch80 -p1 -b .distcache.droplet
%patch81 -p1 -b .debuglog.droplet
%patch82 -p1 -b .abench.droplet
%patch84 -p1 -b .sslheader.droplet
%patch85 -p1 -b .sslvars2.droplet
%patch89 -p1 -b .headerssl.droplet
%patch90 -p1 -b .workerstack.droplet
%patch91 -p1 -b .testhook.droplet
%patch92 -p1 -b .dumpcerts.droplet
#
%patch100 -p1 -b .bsd-ipv6.droplet
%patch101 -p1 -b .apachesrc.droplet
%patch102 -p0 -b .apache2-suexec.droplet
%patch103 -p0 -b .mod_ldap_cache_file_location.droplet
%patch104 -p1 -b .peruser.droplet
%patch105 -p0 -b .pemcallback.droplet
#
%patch122 -p1 -b .can-2005-1268
%patch123 -p1 -b .can-2005-2088
%patch124 -p1 -b .can-2005-2700
%patch125 -p1 -b .can-2005-2728

# Touch mod_ssl expression parser sources to prevent regenerating it
touch modules/ssl/ssl_expr_*.[chyl]

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR |  cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
    : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}.
    : Update the mmn macro and rebuild.
    exit 1
fi

# Conditionally enable PIE support
if echo 'static int foo[30000]; int main () { return 0; }' | 
    gcc -pie -fpie -O2 -xc - -o pietest && 
    ./pietest; then
%patch5 -p1 -b .pie
    : PIE support enabled
else
    : WARNING: PIE support not enabled
fi

# nuke the pietest binary
rm -f pietest

# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# don't install or use bundled pcreposix.h
rm -f include/pcreposix.h

#Fix apxs
%{__perl} -pi -e 's|\@exp_installbuilddir\@|%{_libdir}/httpd/build|;' support/apxs.in
%{__perl} -pi -e 's|get_vars\("prefix"\)|"%{_libdir}/httpd/build"|;' support/apxs.in
%{__perl} -pi -e 's|get_vars\("sbindir"\) . "/envvars"|"\$installbuilddir/envvars"|;' support/apxs.in

#Correct perl paths
find -type f|xargs perl -pi -e " s|/usr/local/bin/perl|%{__perl}|g; \
    s|/usr/local/bin/perl5|%{__perl}|g; \
    s|/path/to/bin/perl|%{__perl}|g; \
    "
%{__perl} -pi -e 's|" PLATFORM "|%{distribution}/%{release}|;' \
    server/core.c

# use my nice converted transparent png icons
tar -jxf %{SOURCE3}
mv icons/*.png docs/icons/

# "install" the 2 extra modules
bzcat %{SOURCE4} > modules/experimental/mod_backtrace.c
bzcat %{SOURCE5} > modules/experimental/mod_whatkilledus.c
bzcat %{SOURCE6} > modules/experimental/test_char.h

# this is really better and easier than a stupid static patch...
# for some reason you have to use ">>" here (!)

%{__cat} >> config.layout << EOF
<Layout AVX>
    prefix:        %{_sysconfdir}/httpd
    exec_prefix:   %{_prefix}
    bindir:        %{_bindir}
    sbindir:       %{_sbindir}
    libdir:        %{_libdir}
    libexecdir:    %{_libdir}/httpd
    mandir:        %{_mandir}
    infodir:       %{_infodir}
    includedir:    %{_includedir}/httpd
    sysconfdir:    %{_sysconfdir}/httpd/conf
    datadir:       /var/www
    installbuilddir: %{_libdir}/httpd/build
    errordir:      /var/www/error
    iconsdir:      /var/www/icons
    htdocsdir:     /var/www/html
    manualdir:
    cgidir:        /var/www/cgi-bin
    localstatedir: /var
    runtimedir:    /var/run
    logfiledir:    /var/log/httpd
    proxycachedir: /var/cache/httpd
</Layout>     
EOF

#Fix DYNAMIC_MODULE_LIMIT
perl -pi -e "s/DYNAMIC_MODULE_LIMIT 64/DYNAMIC_MODULE_LIMIT 128/;" \
    include/httpd.h

# don't try to touch srclib
perl -pi -e "s|^SUBDIRS = .*|SUBDIRS = os server modules support|g" Makefile.in

# bump server limit
perl -pi -e "s|DEFAULT_SERVER_LIMIT 256|DEFAULT_SERVER_LIMIT 1024|g" server/mpm/prefork/prefork.c

# add the changes file
cp %{SOURCE2} README.urpmi

%build
#########################################################################################
# configure and build phase
#

export WANT_AUTOCONF_2_5="1"

# We need to re-run ./buildconf because of any applied patch(es)
#./buildconf

# use a minimal buildconf instead
bzcat %{SOURCE100} > buildconf
sh ./buildconf

%serverbuild

#JMD: -fno-strict-aliasing -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 is used by mod_perl
#export CFLAGS="%{optflags} -fno-strict-aliasing -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
#export CPPFLAGS="-fno-strict-aliasing -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
#JMD: but only when we manage to fix the conflict between HAVE_SENDFILE and
#JMD: HAVE_LARGEFILE in the APR sources.
#export SSL_BASE="SYSTEM"

# NOTE! "--enable-modules=all --enable-mods-shared=all" won't 
# enable _all_ modules, that's why I had to specify all of them...

CFLAGS="%{optflags}"
CPPFLAGS="-DSSL_EXPERIMENTAL_ENGINE"
if pkg-config openssl; then
    # configure -C barfs with trailing spaces in CFLAGS
    CPPFLAGS="$CPPFLAGS `pkg-config --cflags openssl | sed 's/ *$//'`"
    SSL_LIBS="`pkg-config --libs openssl`"
fi
export CFLAGS CPPFLAGS SSL_LIBS

####
#Copy pre-patched apache source so we can package an httpd-source rpm and
#use it to build mod_perl
rm -rf ../tmp-%{sourcename}
install -d ../tmp-%{sourcename}/usr/src
cp -dpR %{_builddir}/%{sourcename} ../tmp-%{sourcename}%{srcdir}

APVARS="--enable-layout=AVX \
    --cache-file=../config.cache \
    --with-apr=%{_prefix} \
    --with-apr-util=%{_prefix} \
    --with-pcre=%{_prefix} \
%if %{build_debug}
    --enable-debug \
    --enable-maintainer-mode \
    --enable-exception-hook \
%endif
    --prefix=%{_sysconfdir}/httpd \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --libexecdir=%{_libdir}/httpd \
    --sysconfdir=%{_sysconfdir}/httpd/conf \
    --localstatedir=/var \
    --includedir=%{_includedir}/httpd \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --datadir=/var/www \
    --with-port=80 \
    --with-perl=%{__perl} \
    --enable-access=shared \
    --enable-auth=shared \
    --enable-auth_dbm=shared \
    --enable-auth_anon=shared \
    --enable-auth_digest=shared \
    --enable-alias=shared \
    --enable-file-cache=shared \
    --disable-echo \
    --enable-charset-lite=shared \
    --enable-cache=shared \
    --enable-disk-cache=shared \
    --enable-mem-cache=shared \
    --disable-example \
    --enable-ext-filter=shared \
    --enable-case_filter=shared \
    --enable-case-filter-in=shared \
    --enable-deflate=shared \
    --with-z=%{_prefix} \
    --enable-mime-magic=shared \
    --enable-cern-meta=shared \
    --enable-expires=shared \
    --enable-headers=shared \
    --enable-usertrack=shared \
    --enable-unique-id=shared \
    --enable-proxy=shared \
    --enable-proxy-connect=shared \
    --enable-proxy-ftp=shared \
    --enable-proxy-http=shared \
    --disable-optional-hook-export \
    --disable-optional-hook-import \
    --disable-optional-fn-import \
    --disable-optional-fn-export \
    --disable-bucketeer \
    --enable-info=shared \
    --enable-include=shared \
    --enable-cgi=shared \
    --enable-cgid=shared \
    --enable-dav=shared \
    --enable-dav-fs=shared \
    --enable-vhost-alias=shared \
    --enable-speling=shared \
    --enable-rewrite=shared \
    --enable-log_config=shared \
    --enable-logio=shared \
    --enable-log_forensic=shared \
    --enable-env=shared \
    --enable-setenvif=shared \
    --enable-mime=shared \
    --enable-status=shared \
    --enable-autoindex=shared \
    --enable-asis=shared \
    --enable-negotiation=shared \
    --enable-dir=shared \
    --enable-imap=shared \
    --enable-actions=shared \
    --enable-userdir=shared \
    --enable-alias=shared \
    --enable-auth-ldap=shared \
    --enable-ldap=shared \
    --enable-dumpio=shared \
    --enable-forward \
    --with-program-name=httpd"

# provide useful info for making some of the modules from 
# their own source rpm packages
mkdir build-nothing
pushd build-nothing
    ln -s ../configure .
    %configure2_5x $APVARS \
        --with-mpm=prefork \
        --enable-ssl=shared \
        --with-ssl=%{_prefix}

    # make ab-ssl
    %make -C support CFLAGS="%{optflags} -DUSE_SSL -DHAVE_OPENSSL" ab
    cp -p support/ab ../ab-ssl

    # this makes us able to do "apxs2 -c `cat mod_ssl.txt` -lssl -lcrypto" from an external source rpm package
    grep "^mod_ssl.la" modules/ssl/modules.mk | cut -d\: -f2 | perl -pi -e "s|\.[s]lo|\.c|g" > ../../tmp-%{sourcename}%{srcdir}/modules/ssl/mod_ssl.txt
    grep "^mod_ldap.la" modules/experimental/modules.mk | cut -d\: -f2 | perl -pi -e "s|\.[s]lo|\.c|g" > ../../tmp-%{sourcename}%{srcdir}/modules/experimental/mod_ldap.txt
popd

for mpm in prefork worker; do
    mkdir build-${mpm}
    pushd build-${mpm}
        ln -s ../configure .
        %configure2_5x $APVARS --with-mpm=${mpm}

        # Copy configure flags to a file in the httpd-source rpm.
        echo "$APVARS --with-mpm=${mpm}" > ../../tmp-%{sourcename}%{srcdir}/APVARS.${mpm}

        # OE: avoid linking of *everything* against all libs, mucho gracias suse!
        for lib in ldap lber sasl sasl2 ssl crypto; do
            %{__perl} -pi -e "s|-l$lib||g" build/config_vars.mk
        done

        %{__sed}  '/SH_LINK.*util_ldap/ s/$/ %{ap_ldap_libs}/' modules/experimental/modules.mk > tmp; %{__mv} tmp modules/experimental/modules.mk
        %{__sed}  '/SH_LINK.*auth_ldap/ s/$/ %{ap_ldap_libs}/' modules/experimental/modules.mk > tmp; %{__mv} tmp modules/experimental/modules.mk
        %{__sed}  '/SH_LINK.*mod_ssl/ s/$/ %{ap_ssl_libs}/' modules/ssl/modules.mk > tmp; %{__mv} tmp modules/ssl/modules.mk

        # only build what's required.
        if ! [ "${mpm}" == "prefork" ]; then
            %{__perl} -pi -e "s|^MODULE_DIRS = .*|MODULE_DIRS = http mappers|g" build/config_vars.mk
        fi

        # finally doing the build stage
        %make

    popd
done

# Verify that the same modules were built into the two httpd binaries
./build-prefork/httpd -l | grep -v prefork > ./prefork.mods
./build-worker/httpd -l | grep -v worker > ./worker.mods
if [ "`diff -u prefork.mods worker.mods >/dev/null 2>&1 && echo $?`" == "1" ]; then
    : Different modules built into httpd binaries, will not proceed
    exit 1
fi


%if %{build_debug}
# this won't work..., too bad...
#    --add-module=experimental:modules/experimental/mod_backtrace.c --enable-backtrace=shared \
#    --add-module=experimental:modules/experimental/mod_whatkilledus.c --enable-whatkilledus=shared \
pushd build-prefork
    cp support/apxs apxs_test; chmod 755 apxs_test
    perl -pi -e  "s|%{_libdir}/httpd/build|./build|g" apxs_test
    ./apxs_test -I../include -I../os/unix -I./include `apr-config --includes` -c ../modules/experimental/mod_backtrace.c
    ./apxs_test -I../include -I../os/unix -I./include `apr-config --includes` -c ../modules/experimental/mod_whatkilledus.c
popd
%endif


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
#########################################################################################
# install phase
#

%if %{build_debug}
export DONT_STRIP=1
%endif

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
mkdir -p %{buildroot}%{_localstatedir}/dav
mkdir -p %{buildroot}/var/{www,cache/httpd}

EXCLUDE_FROM_STRIP="%{buildroot}/%{_sbindir}/httpd %{buildroot}/%{_sbindir}/httpd-worker"

# make mr. lint happy and do some house cleaning...
pushd ../tmp-%{sourcename}%{srcdir}
    rm -rf autom4te.cache icons *.zip
    # if we delete these we have to maintain an "linux only" patch in %%setup too, mark my words!
    #rm -rf build/win32 modules/arch support/win32
    #rm -rf os/beos os/bs2000 os/netware os/os2 os/tpf os/win32
    #rm -rf server/mpm/beos server/mpm/mpmt_os2 server/mpm/netware server/mpm/winnt
    for f in `find . -type f -name ".orig"` \
	`find . -type f -name ".deps"` \
	`find . -type f -name ".indent.pro"` \
	`find . -type f -name ".gdbinit"` \
	`find . -type f -name "NW*"` \
	`find . -type f -name "*.droplet"` \
	`find . -type f -name "*.dsp"`; do
	rm -f $f
    done
    find . -type f | xargs %{__perl} -pi -e "s|%{_builddir}/%{sourcename}|%{srcdir}|g"
popd

# install source
tar c -C ../tmp-%{sourcename} usr/src | tar x -C %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

pushd build-prefork
    make install \
	prefix=%{buildroot}%{_prefix} \
	bindir=%{buildroot}%{_bindir} \
	sbindir=%{buildroot}%{_sbindir} \
	libdir=%{buildroot}%{_libdir} \
	libexecdir=%{buildroot}%{_libdir}/httpd \
	mandir=%{buildroot}%{_mandir} \
	sysconfdir=%{buildroot}%{_sysconfdir}/httpd/conf \
	includedir=%{buildroot}%{_includedir}/httpd \
	localstatedir=%{buildroot}/var \
	runtimedir=%{buildroot}/var/run \
	installbuilddir=%{buildroot}%{_libdir}/httpd/build  \
	datadir=%{buildroot}/var/www \
	errordir=%{buildroot}/var/www/error \
	iconsdir=%{buildroot}/var/www/icons \
	htdocsdir=%{buildroot}/var/www/html \
	manualdir=%{buildroot}/var/www/html/manual \
	cgidir=%{buildroot}/var/www/cgi-bin \
	runtimedir=%{buildroot}/var/run \
	logdir=%{buildroot}/var/log/httpd \
	logfiledir=%{buildroot}/var/log/httpd \
	proxycachedir=%{buildroot}/var/cache/httpd
popd

rm -f %{buildroot}%{_sbindir}/suexec
rm -f %{buildroot}%{_mandir}/man8/suexec.8 

#Fix config_vars.mk, and add some MDK flags so all other modules 
#can simply do "apxs -q VARIABLE" and know, for example, the exact
#release of httpd-devel or the exact directory where the source is
#located. 
CVMK="%{buildroot}%{_libdir}/httpd/build/config_vars.mk"
%{__perl} -pi -e "s|%{_builddir}/%{sourcename}|%{srcdir}|g" $CVMK
%{__perl} -pi -e "s|%{buildroot}||g" $CVMK
%{__perl} -pi -e "s|^EXTRA_INCLUDES.*|EXTRA_INCLUDES = `apr-config --includes` -I%{_includedir}/httpd -I%{_includedir}/openssl|g" $CVMK

# fix libtool invocation
%{__perl} -pi -e "s|^LIBTOOL.*|LIBTOOL = libtool|g" $CVMK
%{__perl} -pi -e "s|^SH_LIBTOOL.*|SH_LIBTOOL = libtool|g" $CVMK


# if the following 3 lines needs to be enabled again, use the ".*" wildcard as in
# "s|bla bla =.*|bla bla = replaced whatever text after the equal char...|g"
#%{__perl} -pi -e "s|installbuilddir =.*|installbuilddir = %{_libdir}/httpd/build|g" $CVMK
#%{__perl} -pi -e "s|htdocsdir =.*|htdocsdir = /var/www/html|g" $CVMK
#%{__perl} -pi -e "s|logfiledir =.*|logfiledir = /var/log/httpd|g" $CVMK

echo "ap_version = %{version}" >> $CVMK
echo "ap_release = %{release}" >> $CVMK

#########################################################################################
# fix some bugs and other stuff
#
%{__perl} -pi -e "s|%{_builddir}/%{sourcename}|%{srcdir}|g" %{buildroot}%{_libdir}/httpd/build/apr_rules.mk

mv %{buildroot}%{_sbindir}/envvars %{buildroot}%{_libdir}/httpd/build/

##################################################################

# first tuck away the vanilla httpd*.conf file
%{__perl} -pi -e "s|%{buildroot}/usr|/etc/httpd|g" %{buildroot}%{_sysconfdir}/httpd/conf/*.conf
%{__perl} -pi -e "s|%{buildroot}%{_libdir}/httpd|modules|g" %{buildroot}%{_sysconfdir}/httpd/conf/*.conf
%{__perl} -pi -e "s|%{buildroot}/var/log/httpd|logs|g" %{buildroot}%{_sysconfdir}/httpd/conf/*.conf
cp %{buildroot}%{_sysconfdir}/httpd/conf/highperformance.conf highperformance.conf
cp %{buildroot}%{_sysconfdir}/httpd/conf/httpd.conf httpd-VANILLA.conf
cp %{buildroot}%{_sysconfdir}/httpd/conf/ssl.conf ssl.conf
cp %{buildroot}%{_sysconfdir}/httpd/conf/ssl-std.conf ssl-std.conf
cp %{buildroot}%{_sysconfdir}/httpd/conf/highperformance-std.conf highperformance-std.conf
cp %{buildroot}%{_sysconfdir}/httpd/conf/httpd-std.conf httpd-std.conf
rm -rf %{buildroot}%{_sysconfdir}/httpd/conf

# Link build dir
ln -s ../../..%{_libdir}/httpd/build %{buildroot}%{_sysconfdir}/httpd/build

##################################################################

# install module conf files for the "modules.d" dir loading structure
install -d %{buildroot}/%{_sysconfdir}/httpd/modules.d
bzcat %{SOURCE30} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/30_mod_proxy.conf
bzcat %{SOURCE45} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/45_mod_dav.conf
bzcat %{SOURCE46} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/46_mod_ldap.conf
bzcat %{SOURCE55} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/55_mod_cache.conf
bzcat %{SOURCE56} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/56_mod_disk_cache.conf
bzcat %{SOURCE57} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/57_mod_mem_cache.conf
bzcat %{SOURCE58} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/58_mod_file_cache.conf
bzcat %{SOURCE59} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/59_mod_deflate.conf
bzcat %{SOURCE67} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/67_mod_userdir.conf

%if %{build_debug}
# fix the mod_backtrace.conf

cat << EOF > %{buildroot}/%{_sysconfdir}/httpd/modules.d/ZZ90_mod_backtrace.conf
<IfDefine HAVE_BACKTRACE>
  <IfModule !mod_backtrace.so.c>
    LoadModule backtrace_module		extramodules/mod_backtrace.so
  </IfModule>
</IfDefine>

<IfModule mod_backtrace.c>
    EnableExceptionHook On
    BacktraceLog logs/backtrace_log
</IfModule>
EOF

# fix the mod_whatkilledus.conf
cat << EOF > %{buildroot}/%{_sysconfdir}/httpd/modules.d/ZZ91_mod_whatkilledus.conf
<IfDefine HAVE_WHATKILLEDUS>
  <IfModule !mod_whatkilledus.so.c>
    LoadModule whatkilledus_module		extramodules/mod_whatkilledus.so
  </IfModule>
</IfDefine>

<IfModule mod_whatkilledus.c>
    EnableExceptionHook On
    WhatKilledUsLog logs/whatkilledus_log
</IfModule>
EOF

# install the dso's
install -m 0755 modules/experimental/.libs/mod_backtrace.so %{buildroot}%{_libdir}/httpd-extramodules/
install -m 0755 modules/experimental/.libs/mod_whatkilledus.so %{buildroot}%{_libdir}/httpd-extramodules/

# provide log files too
touch %{buildroot}/var/log/httpd/backtrace_log
touch %{buildroot}/var/log/httpd/whatkilledus_log
%endif

install -d %{buildroot}%{_localstatedir}/dav

# Move mod_ldap.so and mod_auth_ldap.so to %{_libdir}/httpd-extramodules
mv %{buildroot}%{_libdir}/httpd/mod_ldap.so %{buildroot}%{_libdir}/httpd-extramodules
mv %{buildroot}%{_libdir}/httpd/mod_auth_ldap.so %{buildroot}%{_libdir}/httpd-extramodules

# make libtool a (dangling) symlink
ln -snf ../../../bin/libtool %{buildroot}%{_libdir}/httpd/build/libtool

# we only want to provide png files...
find %{buildroot}/var/www/icons -type f -name "*.gif" | xargs rm

# install missing files
install -m 0755 build-prefork/support/split-logfile %{buildroot}%{_sbindir}/split-logfile
install -m 0755 support/list_hooks.pl %{buildroot}%{_sbindir}/list_hooks.pl
install -m 0755 build-prefork/support/logresolve.pl %{buildroot}%{_sbindir}/logresolve.pl
install -m 0755 build-prefork/support/log_server_status %{buildroot}%{_sbindir}/log_server_status
install -m 0755 build-prefork/support/checkgid %{buildroot}%{_sbindir}/checkgid
install -m 0755 support/check_forensic %{buildroot}%{_sbindir}/check_forensic
install -m 0755 ab-ssl %{buildroot}%{_sbindir}/ab-ssl

install -d %{buildroot}/var/cache/httpd

# cleanup
rm -rf %{buildroot}/var/www/html/index*
rm -rf %{buildroot}/var/www/html/apach*
rm -rf %{buildroot}%{_sbindir}/apachectl
rm -rf %{buildroot}/var/www/cgi-bin/printenv
rm -rf %{buildroot}/var/www/cgi-bin/test-cgi
rm -rf %{buildroot}/var/www/html/manual

# fix a msec safe cache for the mod_ldap stuff
touch %{buildroot}/var/cache/httpd/mod_ldap_cache

# install the worker stuff
install -m 0755 build-worker/httpd %{buildroot}%{_sbindir}/httpd-worker

%if !%{build_debug}
# these won't get stripped for some reason...
chmod 0755 %{buildroot}%{_sbindir}/*
strip %{buildroot}%{_sbindir}/ab
strip %{buildroot}%{_sbindir}/checkgid
strip %{buildroot}%{_sbindir}/htdbm
strip %{buildroot}%{_sbindir}/htdigest
strip %{buildroot}%{_sbindir}/htpasswd
strip %{buildroot}%{_sbindir}/logresolve
strip %{buildroot}%{_sbindir}/rotatelogs
strip %{buildroot}%{_sbindir}/httpd
strip %{buildroot}%{_sbindir}/httpd-worker
%endif


%multiarch_includes %{buildroot}%{_includedir}/httpd/ap_config_layout.h

#########################################################################################
# install phase done
#


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# Clean up "install source" and other generated dirs
[ "../tmp-%{sourcename}%{srcdir}" != "/" ] && rm -rf ../tmp-%{sourcename}%{srcdir}
[ "../usr/src" != "/" ] && rm -rf ../usr/src
[ "../tmp-%{sourcename}" != "/" ] && rm -rf ../tmp-%{sourcename}


%post mod_proxy
%_post_srv httpd

%postun mod_proxy
%_post_srv httpd

%post mod_dav
%_post_srv httpd

%postun mod_dav
%_post_srv httpd

%post mod_ldap
%create_ghostfile /var/cache/httpd/mod_ldap_cache apache root 0600
%_post_srv httpd

%postun mod_ldap
%_post_srv httpd

%post mod_cache
%_post_srv httpd

%postun mod_cache
%_post_srv httpd

%post mod_disk_cache
%_post_srv httpd

%postun mod_disk_cache
%_post_srv httpd

%post mod_mem_cache
%_post_srv httpd

%postun mod_mem_cache
%_post_srv httpd

%post mod_file_cache
%_post_srv httpd

%postun mod_file_cache
%_post_srv httpd

%post mod_deflate
%_post_srv httpd

%postun mod_deflate
%_post_srv httpd

%post mod_userdir
%_post_srv httpd

%postun mod_userdir
%_post_srv httpd

%pre common
%_pre_useradd apache /var/www /bin/sh 74

%postun common
%_postun_userdel apache

%post modules
%create_ghostfile /var/log/httpd/backtrace_log apache apache 0644
%create_ghostfile /var/log/httpd/whatkilledus_log apache apache 0644
%_post_srv httpd

%post
#JMD: do *not* use _post_service here, it is used in httpd-conf, since we
#can have both httpd and httpd-mod_perl
%_post_srv httpd

%postun
#JMD: do *not* use _post_service here, otherwise it will uninstall
#httpd-mod_perl as well!!
%_post_srv httpd

%post worker
%_post_srv httpd

%postun worker
%_post_srv httpd


%files
%defattr(-,root,root)
%doc highperformance.conf httpd-VANILLA.conf ssl.conf ssl-std.conf highperformance-std.conf httpd-std.conf
%attr(0755,root,root) %{_sbindir}/httpd

%files worker
%defattr(-,root,root)
%doc highperformance.conf httpd-VANILLA.conf ssl.conf ssl-std.conf highperformance-std.conf httpd-std.conf
%attr(0755,root,root) %{_sbindir}/httpd-worker


%files modules
%defattr(-,root,root)
%doc modules/README*
%dir %{_libdir}/httpd
%{_libdir}/httpd/mod_access.so
%{_libdir}/httpd/mod_actions.so
%{_libdir}/httpd/mod_alias.so
%{_libdir}/httpd/mod_asis.so
%{_libdir}/httpd/mod_auth.so
%{_libdir}/httpd/mod_auth_anon.so
%{_libdir}/httpd/mod_auth_dbm.so
%{_libdir}/httpd/mod_auth_digest.so
%{_libdir}/httpd/mod_autoindex.so
%{_libdir}/httpd/mod_case_filter.so
%{_libdir}/httpd/mod_case_filter_in.so
%{_libdir}/httpd/mod_cern_meta.so
%{_libdir}/httpd/mod_cgi.so
%{_libdir}/httpd/mod_cgid.so
%{_libdir}/httpd/mod_charset_lite.so
%{_libdir}/httpd/mod_dir.so
%{_libdir}/httpd/mod_env.so
%{_libdir}/httpd/mod_expires.so
%{_libdir}/httpd/mod_ext_filter.so
%{_libdir}/httpd/mod_headers.so
%{_libdir}/httpd/mod_imap.so
%{_libdir}/httpd/mod_include.so
%{_libdir}/httpd/mod_info.so
%{_libdir}/httpd/mod_log_config.so
%{_libdir}/httpd/mod_logio.so
%{_libdir}/httpd/mod_log_forensic.so
%{_libdir}/httpd/mod_mime.so
%{_libdir}/httpd/mod_mime_magic.so
%{_libdir}/httpd/mod_negotiation.so
%{_libdir}/httpd/mod_rewrite.so
%{_libdir}/httpd/mod_setenvif.so
%{_libdir}/httpd/mod_speling.so
%{_libdir}/httpd/mod_status.so
%{_libdir}/httpd/mod_unique_id.so
%{_libdir}/httpd/mod_usertrack.so
%{_libdir}/httpd/mod_vhost_alias.so
%{_libdir}/httpd/mod_dumpio.so
%{_libdir}/httpd/httpd.exp
%dir %{_libdir}/httpd-extramodules
%dir %{_sysconfdir}/httpd
%exclude %{_sysconfdir}/httpd/build/
%{_sysconfdir}/httpd/*
%if %{build_debug}
%config(noreplace) %{_sysconfdir}/httpd/modules.d/ZZ90_mod_backtrace.conf
%config(noreplace) %{_sysconfdir}/httpd/modules.d/ZZ91_mod_whatkilledus.conf
%{_libdir}/httpd-extramodules/mod_backtrace.so
%{_libdir}/httpd-extramodules/mod_whatkilledus.so
%attr(0644,apache,apache) %ghost /var/log/httpd/backtrace_log
%attr(0644,apache,apache) %ghost /var/log/httpd/whatkilledus_log
%endif

%files mod_proxy
%defattr(-,root,root)
%doc modules/proxy/CHANGES
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_proxy.conf
%{_libdir}/httpd/mod_proxy_connect.so
%{_libdir}/httpd/mod_proxy_ftp.so
%{_libdir}/httpd/mod_proxy_http.so
%{_libdir}/httpd/mod_proxy.so
%attr(0770,root,apache) %dir /var/cache/httpd

%files mod_dav
%defattr(-,root,root)
%attr(-,apache,apache) %dir %{_localstatedir}/dav
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_dav.conf
%{_libdir}/httpd/mod_dav.so
%{_libdir}/httpd/mod_dav_fs.so

%files mod_ldap
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_ldap.conf
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ldap_cache
%{_libdir}/httpd-extramodules/mod_ldap.so
%{_libdir}/httpd-extramodules/mod_auth_ldap.so

%files mod_cache
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_cache.conf
%{_libdir}/httpd/mod_cache.so

%files mod_disk_cache
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_disk_cache.conf
%{_libdir}/httpd/mod_disk_cache.so

%files mod_mem_cache
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_mem_cache.conf
%{_libdir}/httpd/mod_mem_cache.so

%files mod_file_cache
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_file_cache.conf
%{_libdir}/httpd/mod_file_cache.so

%files mod_deflate
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_deflate.conf
%{_libdir}/httpd/mod_deflate.so

%files mod_userdir
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_userdir.conf
%{_libdir}/httpd/mod_userdir.so

%files common
%defattr(-,root,root)
%doc README.urpmi
%dir /var/www/error
%dir /var/www/error/include
%config(noreplace,missingok) /var/www/error/README
%config(noreplace,missingok) /var/www/error/*.var
%config(noreplace,missingok) /var/www/error/include/*.html
/var/www/icons/README*
/var/www/icons/*.png
/var/www/icons/small/README*
/var/www/icons/small/*.png
%{_mandir}/*/*
%attr(0755,root,root) %{_sbindir}/ab
%attr(0755,root,root) %{_sbindir}/ab-ssl
%attr(0755,root,root) %{_sbindir}/checkgid
%attr(0755,root,root) %{_sbindir}/htdbm
%attr(0755,root,root) %{_sbindir}/htdigest
%attr(0755,root,root) %{_sbindir}/htpasswd
%attr(0755,root,root) %{_sbindir}/logresolve
%attr(0755,root,root) %{_sbindir}/rotatelogs
%attr(0755,root,root) %{_sbindir}/split-logfile
%attr(0755,root,root) %{_sbindir}/dbmmanage
%attr(0755,root,root) %{_sbindir}/list_hooks.pl
%attr(0755,root,root) %{_sbindir}/logresolve.pl
%attr(0755,root,root) %{_sbindir}/log_server_status
%attr(0755,root,root) %{_sbindir}/check_forensic

%files devel
%defattr(-,root,root)
%multiarch %{multiarch_includedir}/httpd/ap_config_layout.h
%{_includedir}/httpd
%attr(0755,root,root) %dir %{_libdir}/httpd/build
%attr(0755,root,root) %dir %{_sysconfdir}/httpd/build
%attr(0644,root,root) %{_libdir}/httpd/build/*.mk
%attr(0755,root,root) %{_libdir}/httpd/build/*.sh
%attr(0755,root,root) %{_libdir}/httpd/build/envvars
%attr(0755,root,root) %{_libdir}/httpd/build/libtool
%attr(0755,root,root) %{_libdir}/httpd/build/config.nice
%attr(0755,root,root) %{_sbindir}/envvars-std
%attr(0755,root,root) %{_sbindir}/apxs

%files source
%defattr(-,root,root)
%{srcdir}


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Sep 17 2005 Vincent Danen <vdanen@annvix.org> 2.0.54-4avx
- rebuild against new pcre

* Thu Sep 15 2005 Vincent Danen <vdanen@annvix.org> 2.0.54-3avx
- make httpd-worker provide httpd
- new style PreReq

* Fri Sep 09 2005 Vincent Danen <vdanen@annvix.org> 2.0.54-2avx
- P124: patch to fix CAN-2005-2700
- P125: patch to fix CAN-2005-2728
- provide all the modules we obsoleted in httpd-modules

* Wed Sep 07 2005 Vincent Danen <vdanen@annvix.org> 2.0.54-1avx
- 2.0.54
- the great apache2->httpd/httpd2->http migration
- sync patches with mandrake 2.0.54-10mdk
- use modules.d to load modules rather than modules.d
- P122: security fix for CAN-2005-1268
- P123: security fix for CAN-2005-2088
- added README.urpmi
- mod_userdir is it's own sub-package
- BuildRequires: zlib-devel

* Tue Aug 23 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-4avx
- drop the requirements of libtool for apache2
- fix deps

* Tue Aug 23 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-4avx
- P54: from SVN, to fix compilation of mod_ssl with openssl 0.9.8

* Fri Aug 19 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-2avx
- rebuild

* Fri Feb 25 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-1avx
- 2.0.53
- drop P105, P106 (upstream)
- this isn't really AdvancedExtranetServer anymore...
- get rid of all ADVX-build stuff
- put apachectl back in (needed by ZendStudioServer, and possibly other
  apps)
- P48: fix for wrongly assuming IPv6 on listen
- fix the config_vars.mk file again (oden)
- provide logfiles in the debug build (oden)
- comment in some multiarch stuff for when we move to it
- P95: LDAP socket timeout patch (oden)

* Thu Feb 03 2005 Vincent Danen <vdanen@annvix.org> 2.0.52-5avx
- rebuild against new gdbm

* Thu Jan 06 2005 Vincent Danen <vdanen@annvix.org> 2.0.52-4avx
- rebuild against new openssl

* Wed Nov 10 2004 Vincent Danen <vdanen@annvix.org> 2.0.52-3avx
- P106: patch to fix CAN-2004-0942

* Fri Nov  5 2004 Vincent Danen <vdanen@annvix.org> 2.0.52-2avx
- P105: patch to fix CAN-2004-0885

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52-1avx
- 2.0.52
- added patches from Fedora: P53, P93, P94
- updated patches from Fedora: P1, P3, P25, P39, P84, P86
- dropped patches: P8, P50, P52, P85, P200, P201, P202, P203 (merged
  upstream), P26, P88 (no longer needed?)
- move the runscripts and afterboot snippet to apache-conf
- merge with cooker 2.0.50-7mdk:
  - lib64 fixes (gbeauchesne)
  - from oden:
    - added security fixes to the source for mod_ssl from ASF (P202, P203)
      that address CAN-2004-0747 and CAN-2004-0809
    - added security fixes to the source for mod_ssl from SUSE (P200, P201)
      that address CAN-2004-0748 and CAN-2004-0751
    - added fix P39 (fedora)
    - enable mod_log_forensic
    - drop P46, P48, P49, P51, P53, P54, P55, P81, P89, and P90, these are
      integrated upstream as well as fixes for CAN-2004-0488 and CAN-2004-0493
    - move mod_ssl to an external source rpm package
    - remove distcache stuff as we build it using an external source rpm package
    - sync with fedora (P7, P55) (2.0.49-7)
  - from jmd:
    - use fcntl for mutexes instead of posix mutexes (which won't work on
      non-NPTL kernels and some older processors), or sysvsem which are not
      resistant under high load
    - should fix bug #9101 at last
    - tested under heavy load: 100,000 hits in 4 minutes, 1000 simultaneous
      connections, load average went up to 835.40, not a single failed request
    - tested under NPTL kernel and User-Mode Linux kernel using linuxthreads
  - from oden:
    - sync with fedora (P52, P53, P54, P72, P91, P92, P300)
    - drop P100 in favour of P54
    - bump server limit again
    - fix deps
    - provide a cleaner source package
    - add the metux mpm (P104)
    - bump DEFAULT_SERVER_LIMIT for the prefork mpm
    - use the %%configure2_5x macro
    - use --enable-exception-hook if a debug build
    - added P103 (fix mod_ldap cache file location) and add the ghostfile
    - new P90 (jorton) fix #9120
    - added S6 and S7 (mod_backtrace and mod_whatkilledus is built if a debug build)
    - sync with fedroa (P51, P90)
    - split out the apr suite as apr-0.9.5-1avx and apr-util-0.9.5-1avx
    - borrowed a lot of stuff from fedora
    - removed a lot of patches
    - made a lot of spec file changes
    - require new ADVX-build >= 10 (and fix #5732)

* Tue Sep 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-8avx
- P9-P13: security patches for CAN-2004-0748, CAN-2004-0751, 
  CAN-2004-0747, CAN-2004-0786, and CAN-2004-0809
- updated runscripts

* Thu Aug 19 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-7avx
- log/run was still logging to /var/log/supervise/apache2 rather than
  ../httpd2; fixed

* Fri Aug 13 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-6avx
- rebuild against new openssl

* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-5avx
- use %%_post_srv rather than %%ADVXctl although this is less
  than efficient (in either case) because apache will start and
  stop a dozen times if you upgrade a dozen modules (need hooks
  in urpmi perhaps?)
- update the afterboot man-snippet
- remove ADVX Provides
- fix __spec_install_post
- apache2-devel requires pcre-devel
- don't enable debug by default
- sync with 2.0.48-6mdk:
  - /var/lib/dav owned by apache, otherwise mod_dav doesn't work
    properly (misc)
  - fix #6308 (mod_ssl error due to incorrect perms) (misc)
  - fix various [DIRM],[CFLP] (misc)

* Mon Jun 28 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-4avx
- P8: security fix for CAN-2004-0493

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-3avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 2.0.49-2sls
- P7: security fix for CAN-2004-0488

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49-1sls
- 2.0.49
- rediff and update P6

* Fri Feb 20 2004 Vincent Danen <vdanen@opensls.org> 2.0.48-8sls
- fix supervise log run script 
- add a conftest to each start, the output is sent to the supervise logs

* Wed Feb 11 2004 Vincent Danen <vdanen@opensls.org> 2.0.48-7sls
- remove %%build_opensls macros
- remove the manual package
- README.ADVX only in the common package
- more spec cleanups
- apache gets static uid/gid 74
- PreReq: srv, afterboot, rpm-helper
- add afterboot snippet

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 2.0.48-6sls
- sync with 5mdk (jmdault):
  - fix mod_auth_ldap (link with ldap, ber, crypto, ssl)
- supervise scripts

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48-5sls
- OpenSLS build
- tidy spec

* Sun Dec 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48-4mdk
- fix #6556
- updated P5

* Sun Dec 07 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48-3mdk
- rebuilt to fix missing package in the repository

* Sun Nov 02 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48-2mdk
- added P6 (check: http://bitbrook.de/software/mod_log_mysql/)

* Tue Oct 28 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48-1mdk
- 2.0.48 ([CAN-2003-0789], [CAN-2003-0542])
- merged in house stuff with vdanens stuff
- fix the httpd2-VANILLA.conf file
- include the other *.conf files as well in %%doc
- drop P50, pause P40, rediffed P5, updated S2
- build debug per default until mdk10(?) final 
- fix the mod_ssl cache location and ghost files
- don't ship novell stuff in the source package
- fix explicit-lib-dependency

* Wed Oct 22 2003 Vincent Danen <vdanen@mandrakesoft.com> 2.0.47-6.1.92mdk
- don't use the new mod_cgi as it causes more problems than it fixes
- fix mod_proxy config since it was entirely insecure

* Mon Sep 15 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.47-6mdk
- fix CGI
- took mod_cgi.c from httpd-2.1-dev since it fixes a nasty bug 
  (and potential DoS attack) [Apache Bug 22030]
- put the ssl_scache file into /var/cache to avoid log rotation and
  segfaults

* Thu Aug 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.47-5mdk
- Fix dependencies (aka remove autorequired packages)

* Mon Jul 21 2003 David BAUDENS <baudens@mandrakesoft.com> 2.0.47-4mdk
- Rebuild to fix bad signature

* Sun Jul 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47-3mdk
- fix the apu-config file
- fix requires
- misc spec file fixes

* Tue Jul 15 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47-2mdk
- rebuilt against new db4.1, openldap and sasl2
- added P50
- misc spec file fixes

* Wed Jul 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47-1mdk
- 2.0.47, fixes [CAN-2003-0192], [CAN-2003-0253], [CAN-2003-0254], [VU#379828]
- require %%{ap_name}-conf >= 2.0.46-2mdk

* Wed Jun 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46-5mdk
- fix typo in requires for the apr package (sooooo annoying...)

* Wed Jun 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46-4mdk
- build options against new shared distcache libs, use --with distcache
  or wait for a mod_ssl_dc module in contribs
- added spec file magic with ideas from suse to prevent everything to
  be built against all libs, also all requires changed because of this.
- use the %%configure2_5x macro
- use --enable-nonportable-atomics for i586 and upwards
- updated S46, note that the mod_ldap stuff is still market experimental...
- misc spec file fixes

* Wed Jun 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46-3mdk
- added distcache support as a conditional switch 
  (--with distcache), currently not enabled by default
- added a distcache entry in S40
- don't require libdb3.3

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46-2mdk
- remove useless modules
- broke out mod_deflate, cache and proxy modules
- misc spec file fixes
- require new ADVX-build >= 9.2

* Wed May 28 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46-1mdk
- security release (CAN-2003-0245, CAN-2003-0189)
- stole P40 & P41 from redhat
- misc spec file fixes

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45-5mdk
- require libopenssl0.9.7 and not libopenssl0

* Fri Apr 11 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.45-4mdk
- Link apache2-extramodules-2.0.44 with 2.0.45, even if directory is empty,
  so it's possible to install modules for 2.0.44 on 2.0.45.

* Mon Apr 07 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.45-3mdk
- 2.0.45 is binary compatible with 2.0.44, migrate old modules to new
  modules directory.

* Mon Apr 07 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.45-2mdk
- Rebuild for 9.1 security update

* Tue Apr 01 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45-1mdk
- 2.0.45

* Tue Mar  4 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-11mdk
- I was out of coffee, so I messed up the last package. Went to the store,
  bought a dozen kilos of French Roast, Colombian and Espresso beans, so
  I'll be okay for a while.
- Really fix the manuals this time, I swear!

* Tue Mar  4 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-10mdk
- add post script for manual package, and provide a /manual/2.0 alias as
well.

* Mon Mar  3 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-9mdk
- re-add obsoletes on manual package, since the 9.0 manual package had a weird
  dependency on mm = 1.1.3 (jmdault sucks ;-)

* Sun Mar  2 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-8mdk
- fix manual config file (thanks Ryan!)

* Fri Feb 28 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-7mdk
- Do not require libdb*-devel, it breaks the upgrade from 9.0 to 9.1.
  Instead, each Apache module that requires libdb* to compile should add it to its
  buildrequires
- Make -devel, -manual and -source package not obsolete their old versions,
  since they can be installed in parallel.
- Do not use a symlink for the manual, but use a config file instead, to be
  able to install both the 1.3 and 2.0 manuals.

* Sat Feb 22 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-6mdk
- Change DYNAMIC_MODULE_LIMIT from 64 to 96 
  (Wow! We really have *lots* of apache modules ;-)

* Fri Feb 21 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-5mdk
- fix suexec path so we can have both versions of Apache and both
  versions of suexec
- fix images (use gif2png)

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-4mdk
- rebuild
- remove fake ASF root, it gives a bunch of danglink symlinks which rpmlint
  doesn't like... Dumb modules will have to be fixed if they need this.

* Wed Feb 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44-3mdk
- arrgh!!! forgot to pass --enable-forward to the configure 
  line to get "-DRECORD_FORWARD" correctly added...

* Wed Feb 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44-2mdk
- add P3 (for mod_limitipconn)

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44-1mdk
- 2.0.44
- drop obsolete P3, P4 & P5
- misc spec file fixes

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43-8mdk
- fix buildrequires ADVX-build >= 1.1
- fix fake ASF root, make it easier to point to, if nessesary when
  building dumb third party modules
- fix the distribution macro insertion

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43-7mdk
- rebuild against openssl-0.9.7
- misc spec file fixes

* Wed Jan 08 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.43-6mdk
- Rebuilt with db4 

* Mon Jan 06 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.43-5mdk
- Change apxs to apxs2 and /usr/include/apache to /usr/include/apache2
  to be able to work on Apache 1.3 and 2.0 at the same time.
- Macroize the db version (3.3 vs 4.0) to be able to easily switch from 9.0 
  to Cooker.
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 
- Likewise, add Provides: AP13package and AP20package in the same
  manner

* Wed Nov 06 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43-4mdk
- enable build with debugging code, used ideas from Han Boetes and his
  fluxbox package, but the RedHat way. rpm --rebuild --with debug 
  apache2-2.0.43-4mdk.src.rpm will _not_ strip away any debugging code,
  will _add_ -g3 to CFLAGS, will _add_ --enable-maintainer-mode to 
  configure.

* Sat Nov 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43-3mdk
- enable the ldap stuff and build against db4

* Fri Oct 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43-2mdk
- new P5 (for mod_logio; check www.rexursive.com)

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43-1mdk
- new version (security fixes + mod_logio)
- dropped P5
- new P4 (mod_logio)

* Wed Oct 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42-6mdk
- added P5 [CAN-2002-0840] (will be in 2.0.43 + mod_dav fixes + 
  mod_logio, release probably tomorrow)

* Sat Sep 28 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42-5mdk
- added P4 (mod_logio)

* Fri Sep 27 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42-4mdk
- added P3 (from CVS) that fixes apr-util to honor LIBNAME

* Thu Sep 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42-3mdk
- installbuilddir, htdocsdir and logfiledir is suddenly set ok in
  config_vars.mk, no need to fix that with perl. (it was doubled!,
  i'm blind...)

* Thu Sep 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42-2mdk
- bring back ugly spec file hacks, but now it's even uglier... :-)
- finally got mod_ldap to compile, but chose not to enable it
- put generated httpd2.conf in docdir as httpd2-VANILLA.conf
- misc spec file fixes

* Wed Sep 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42-1mdk
- the httpd-2.0.36-cnfdir.patch patch by RH is merged upstream, 
  therefore remove it from this package
- remove the ADVX rpm package naming scheme
- merge changes from my last 2.0.40-*mdk package
- provide my nice converted transparent png icons (S4)
- added the gnupg signurature as S1

* Tue Sep  3 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX-8mdk
- change version to 2.0.40ADVX so we can easily synchronize Contribs. We'll
  remove the ADVX suffix for final release.
- mod_ssl will be in apache2-mod_ssl module, since it requires
  openssl, and we want to avoid forcing crypto into the main distro.
  Thus we also put ab-ssl in this package. 
- Fix gentestcrt to generate a random certificate authority as well as a
  random certificate name, so that multiple test certificate don't conflict.
- apache2-devel provides apache2-mod_ssl-devel
- modules do not require libapr0

* Wed Aug 28 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40-7mdk
- macroize completely according to the ADVX policy
  (http://advx.org/devel/policy.php)
- move non-version-dependant stuff and directories to apache2-conf
- put less strict Requires, since apache2-common is now version-independant
- patch apxs so we only need apache2-devel to build modules, and that no
  other package is required.
- pick up more stuff (htdbm, etc) from the /support directory

* Wed Aug 28 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40-6mdk
- add ap_confd macro (for the /etc/httpd/conf.d include directory)
- use DONT_STRIP=1, it's needed for some modules, such as mod_perl and
  HTML-Embperl, until we find a way to build them statically with Apache.
- merged some of Oden's changes in Contribs, up the release to 6mdk so there
  is no confusion.

* Tue Aug 19 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40-2mdk
- macroize specfile completely
- Fix a few minor bugs in package and make rpmlint happy.
- Put old changelog for Apache 1 in doc/apache-old-changelog in case we
  forgot some old 1.3 features in 2.0

* Mon Aug 12 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40-1mdk
- New, final 2.0.40 release
- Split mod_ssl, mod_dav and mod_gzip outside of the main Apache tree,
  because of some configuration issues when updating. They will be in their
  separate packages.
- Put apr-devel inside apache-devel, since it created conflicts for some
  files, and besides, you can't use apr-devel if you don't have the Apache 
  headers anyway.
- Move apachebase to /etc/httpd/2.0

* Thu Aug  8 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40-0.20020805.2mdk
- Totally rebuilt SPEC. This is the result of hundreds of hours of intensive 
  testing, install/uninstall/rollback, and I could write a novel with all
  the changes. However, those were the general goals of the rewrite:
- 1) Take as much possible from Oden's excellent work
- 2) Remain compatible with the previous ADVX spec files
- 3) Make upgrades possible and still keep previous configuration files
     so sysadmins don't have to re-configure everything
- 4) Rework apache2-common, so that the package contains only icons, man files, 
     cgi-bin and only essential directories. Move /etc/httpd/* to
     /etc/httpd/2.0 since they're really release-dependant, and move
     them to the apache2-modules package.
- 5) Work with possible rollback to 1.3 in case the user needs some module
     that works only with 1.3 (frontpage, auth_ldap). In the case of a
     rollback, the only thing to do should be to remove the apache2 package,
     we should be able to keep the config files and the new apache2-common, 
     since they are not version-specific. The only problem will be mod_ssl, 
     mod_ldap and mod_gzip, since both the 1.3 and 2.0 versions contain
     common files, which will conflict. In that case, if there is a problem
     with the upgrade, those modules will be disabled. This means some 
     functionality will be lost, but at least we don't break the entire web 
     server.
- 6) Of course, if it's a brand-new install, everything should work
     perfectly ;-)

* Mon Aug  5 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020805.1mdk
- new CVS version (possible the last CVS snapshot)

* Thu Aug  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020801.1mdk
- new CVS version
- built against new OpenSSL
- fix suexec and mod_userdir conf (thanks to David Walser for reporting this)

* Wed Jul 31 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020731.1mdk
- new CVS version (mainly doc fixes and one nasty bug)
- built with latest system compiler

* Thu Jul 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020725.1mdk
- new CVS version

* Tue Jul 23 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020723.1mdk
- new CVS version

* Thu Jul 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020718.2mdk
- new CVS version
- fixed the initscript (duh!)
- misc spec file fixes

* Thu Jul 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020718.1mdk
- new CVS version
- mod_proxy requires mod_disk_cache (since a while back, sorry about that),
  fixed S30 to reflect this
- improved initscript
- misc spec file fixes

* Wed Jul 17 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020717.1mdk
- new CVS version
- there's no such thing as "httpd2 -k configtest" (thanks to Lonnie Borntreger for
  pointing it out)

* Tue Jul 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020716.1mdk
- new CVS version
- add apache user (as in apache1 by flepied)
- better initscript (stole stuff from here and there...)
- relocated the SSL certificates to /etc/ssl/apache2/

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 2.0.40-0.20020710.2mdk
- use a Serial in perl require

* Wed Jul 10 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020710.1mdk
- new CVS version
- don't use the scoreboardfile (it's broken it seems)

* Sun Jul  7 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020707.1mdk
- new CVS version

* Sat Jul  6 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020706.1mdk
- new CVS version
- added the new MaxMemFree directory to httpd2.conf (yet undocumented, and 
  therefore commented out)
- added ab-ssl to the mod_ssl package
- fix P1 (apxs didn't work with php-4.3.0-dev)

* Wed Jul  3 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020703.1mdk
- new CVS version

* Mon Jul  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020701.1mdk
- new CVS version

* Sat Jun 29 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020629.1mdk
- new CVS version

* Fri Jun 28 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020628.1mdk
- new CVS version
- construct the "include/ap_config_layout.h" file from the spec file since it's not
  done properly by apache... (!) (I wonder why???)
- ship the migration guide stolen from RedHat

* Thu Jun 27 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020627.1mdk
- new CVS version

* Wed Jun 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020626.1mdk
- new CVS version
- bzip2 all sources

* Sun Jun 23 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020623.1mdk
- new CVS version
- misc spec and conf file fixes (thanks to Yura Gusev for
  reporting some of the stuff)

* Tue Jun 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020618.2mdk
- minor spec file and conf file fixes
- added the ScoreBoardFile

* Tue Jun 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020618.1mdk
- new CVS version
- removed flood, will be a separate package

* Mon Jun 17 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020617.1mdk
- new version, new CVS version

* Sun Jun 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.39-0.20020617.1mdk
- new CVS version (2.0.38 is alpha, might as well go for cvs)
- can't tag with cvs version, php needs -dev to build (stupid php)
- fix flood %%configure 

* Sun Jun 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.38-0.20020616.2mdk
- new CVS version
- mod_ssl should really require mod_setenvif and mod_vhost_alias
- changed the %%description
- added missing split-logfile (not installed per default...)
- broke out the icons as a subpackage to enable using themes for mod_autoindex
- misc spec file fixes
- fix permission on flood
- added P5
- 2.0.38-0.20020616.1mdk was lost in cyberspace...

* Sat Jun 15 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.38-0.20020615.3mdk
- missing header files in apache2-devel (GRRRR)

* Sat Jun 15 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.38-0.20020615.2mdk
- added S100 (subpackage: flood)
- accidently uploaded apache2-common which is no more...

* Sat Jun 15 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.38-0.20020615.1mdk
- new CVS version (2.0.38 will be final soon...)
- fix the "ServerRoot/conf.d" stuff.
- fix the manual alias, and provide only *.html 
- provide only *.png files (check with unisys...)
- HUGE spec file modifications (mega split)
- added P3 (require and link with openssl only for mod_ssl)
- added P4
- added S100 (flood)

* Fri Jun 14 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.38-0.20020614.1mdk
- new CVS version
- don't use %%exclude, rpm in 8.2 is broken...
- misc spec file fixes

* Thu Jun 13 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.38-0.20020613.1mdk
- new CVS version
- Use Redhats version instead of PLDs to ignore invalid files in the 
  "ServerRoot/conf?/" dir (P0)
- Mentally prepare to use the "ServerRoot/conf.d/" dir (beware!), soon I'll probably
  be numbering all files in this dir a'la PLD... There may be a split where all/most
  modules has their own rpm package... If you don't like this _speak up now!_

* Thu Jun 12 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.38-0.20020612.1mdk
- new version, new CVS version
- misc spec file fixes
- stole some ideas from RedHat :-)

* Thu Jun  6 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020606.1mdk
- new CVS version
- rediff P1

* Sat Jun  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020601.1mdk
- new CVS version

* Wed May 29 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020529.1mdk
- new CVS version

* Sun May 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020526.1mdk
- new CVS version

* Thu May 23 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020523.1mdk
- new CVS version

* Sun May 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020519.1mdk
- new CVS version
- fix perl path and suexec log file; reported by Liam R. E. Quin
- misc spec file fixes
- added P2
- fix S4 & S10

* Sat May 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020518.1mdk
- new CVS version

* Thu May 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020516.1mdk
- new CVS version (SSLLog and SSLLogLevel is no more)
- new S10

* Wed May 15 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020515.1mdk
- new CVS version (apr-util and apxs fixes)
- fix P1

* Mon May 13 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020513.1mdk
- new CVS version (apr fixes)
- misc spec file fixes

* Sat May 11 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020511.1mdk
- new CVS version
- broke out suexec and apr stuff `a la PLD, but with a twist :)
- added P0 to prepare for possible use of a conf/[0-9]_*.conf system (?)
- added P1 to make apxs work (?)
- more Mr. rpmlint fixes
- build against db3 for now

* Tue May  7 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020507.2mdk
- Mr. rpmlint fixes

* Tue May  7 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.37-0.20020507.1mdk
- new CVS version
- made it possible to run apache1 and apache2 on the same box
- cleaned up the spec file a bit
- removed P0, construct a dynamic config.layout file on the fly instead...
- ripped the gentestcrt.sh things from the mod_ssl spec file
- enhanced the httpd.conf file a bit

* Mon Apr 24 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.36-0.20020424.1mdk
- new CVS version
 
* Mon Apr 15 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.36-0.20020415.2mdk
- spec file fix

* Mon Apr 15 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.36-0.20020415.1mdk
- new CVS version
- don't require apache-conf just yet...
- forgot to provide S9 & S10

* Sun Apr 14 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.36-0.20020414.1mdk
- new CVS version

* Fri Apr 12 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.36-0.20020412.1mdk
- new CVS version
- a lot of specfile fixes

* Mon Apr  8 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.35-1mdk
- new version

