#
# spec file for package httpd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		httpd
%define version		2.2.3
%define release		%_revrel

# not everyone uses this, so define it here
%define distribution	Annvix
%define build_test	1

%define ap_version	%{version}
%define ap_release	%{release}
%define srcdir		%{_prefix}/src/httpd-%{version}

# the name for libapr will be different on 64bit
%define libapr		%mklibname apr 1

Summary:	Apache web server (prefork mpm)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://httpd.apache.org
Source0:	http://archive.apache.org/dist/httpd/httpd-%{version}.tar.gz
Source1:	http://archive.apache.org/dist/httpd/httpd-%{version}.tar.gz.asc
Source2: 	httpd-README.urpmi
Source3:	apache2_transparent_png_icons.tar.bz2
Source4:	perl-framework.tar.bz2
Source6:	certwatch.tar.bz2

Source30:	30_mod_proxy.conf
Source31:	31_mod_proxy_ajp.conf
Source40:	40_mod_ssl.conf
Source41:	41_mod_ssl.default-vhost.conf
Source45: 	45_mod_dav.conf
Source46: 	46_mod_ldap.conf
Source47:	47_mod_authnz_ldap.conf
Source55:	55_mod_cache.conf
Source56:	56_mod_disk_cache.conf
Source57:	57_mod_mem_cache.conf
Source58:	58_mod_file_cache.conf
Source59:	59_mod_deflate.conf
Source60:	60_mod_dbd.conf
Source61:	61_mod_authn_dbd.conf
Source67:	67_mod_userdir.conf
Source68:	default-vhosts.conf
Source100:	buildconf

Patch0:		httpd-2.0.45-deplibs.patch
Patch1:		httpd-2.0.45-encode.patch
Patch2:		httpd-2.0.40-xfsz.patch
Patch3:		httpd-2.0.48-corelimit.patch
Patch4:		httpd-2.0.48-debuglog.patch
# http://lists.debian.org/debian-apache/2003/11/msg00109.html
Patch5:		httpd-2.0.48-bsd-ipv6-fix.diff
#
# OE: prepare for the mod_limitipconn module found here:
# http://dominia.org/djao/limitipconn.html
Patch6:		apachesrc.diff
# JMD: fix suexec path so we can have both versions of Apache and both
# versions of suexec
Patch7:		apache2-suexec.patch
Patch8:		httpd-2.1.10-apxs.patch
Patch9:		httpd-2.1.10-disablemods.patch
Patch10:	httpd-2.1.10-pod.patch
Patch11:	httpd-2.2.0-mod_ssl_memcache.diff
# http://qa.mandriva.com/show_bug.cgi?id=19542
Patch12:	httpd-2.2.2-french_fixes.diff
Patch13:	httpd-2.2.0-authnoprov.patch
Patch14:	certwatch-avx-annvix.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	apr-devel >= 1:1.2.7
BuildRequires:	apr-util-devel >= 1.2.7
BuildRequires:	pcre-devel >= 5.0
BuildRequires:	byacc
BuildRequires:	db4-devel
BuildRequires:	expat-devel
BuildRequires:	gdbm-devel
BuildRequires:	openldap-devel
BuildRequires:	libsasl-devel
BuildRequires:	libtool >= 1.4.2
BuildRequires:	openssl-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRequires:	multiarch-utils >= 1.0.3
%if %{build_test}
BuildRequires:	perl(CGI) >= 1:3.11
BuildRequires:	perl(HTML::Parser)
BuildRequires:	perl(Tie::IxHash)
BuildRequires:	perl(URI)
BuildRequires:	perl(BSD::Resource)
#BuildRequires:	subversion
BuildRequires:	perl(HTTP::DAV)
BuildRequires:	perl-libwww-perl
BuildRequires:	perl-perldoc
%endif


Requires:	libapr-util >= 1.2.7
Requires:	%{libapr} >= 1:1.2.7
Requires:	httpd-conf >= 2.2.2
Requires:	httpd-common = %{version}-%{release}
Requires:	httpd-modules = %{version}-%{release}
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= 2.2.2-1avx
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(preun): libapr-util >= 1.2.7
Requires(preun): %{libapr} >= 1:1.2.7
Requires(post):	libapr-util >= 1.2.7
Requires(post):	%{libapr} >= 1:1.2.7
Requires(postun): rpm-helper
Provides:	webserver
Provides:	apache
Provides:	apache2
Provides:	apache-mpm
Provides:	apache2-prefork
Provides:	httpd-mpm
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


%package common
Summary:	Files common for httpd and httpd-mod_perl installations
Group:		System/Servers
Requires:	libapr-util >= 1.2.7
Requires:	%{libapr} >= 1:1.2.7
Requires(pre):	rpm-helper
Requires(preun): libapr-util >= 1.2.7
Requires(preun): %{libapr} >= 1:1.2.7
Requires(post):	libapr-util >= 1.2.7
Requires(post):	%{libapr} >= 1:1.2.7
Requires(postun): rpm-helper
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
Provides:	httpd-mod_actions = %{version}
Provides:	httpd-mod_alias = %{version}
Provides:	httpd-mod_asis = %{version}
Provides:	httpd-mod_auth_basic = %{version}
Provides:	httpd-mod_auth_digest = %{version}
Provides:	httpd-mod_authn_anon = %{version}
Provides:	httpd-mod_authn_dbm = %{version}
Provides:	httpd-mod_authn_default = %{version}
Provides:	httpd-mod_authn_file = %{version}
Provides:	httpd-mod_authz_dbm = %{version}
Provides:	httpd-mod_authz_default = %{version}
Provides:	httpd-mod_authz_groupfile = %{version}
Provides:	httpd-mod_authz_host = %{version}
Provides:	httpd-mod_authz_owner = %{version}
Provides:	httpd-mod_authz_user = %{version}
Provides:	httpd-mod_autoindex = %{version}
Provides:	httpd-mod_bucketeer = %{version}
Provides:	httpd-mod_case_filter = %{version}
Provides:	httpd-mod_case_filter_in = %{version}
Provides:	httpd-mod_cern_meta = %{version}
Provides:	httpd-mod_cgi = %{version}
Provides:	httpd-mod_cgid = %{version}
Provides:	httpd-mod_charset_lite = %{version}
Provides:	httpd-mod_deflate = %{version}
Provides:	httpd-mod_dir = %{version}
Provides:	httpd-mod_dumpio = %{version}
Provides:	httpd-mod_echo = %{version}
Provides:	httpd-mod_env = %{version}
Provides:	httpd-mod_example = %{version}
Provides:	httpd-mod_expires = %{version}
Provides:	httpd-mod_ext_filter = %{version}
Provides:	httpd-mod_filter = %{version}
Provides:	httpd-mod_headers = %{version}
Provides:	httpd-mod_ident = %{version}
Provides:	httpd-mod_imagemap = %{version}
Provides:	httpd-mod_include = %{version}
Provides:	httpd-mod_info = %{version}
Provides:	httpd-mod_log_config = %{version}
Provides:	httpd-mod_log_forensic = %{version}
Provides:	httpd-mod_logio = %{version}
Provides:	httpd-mod_mime = %{version}
Provides:	httpd-mod_mime_magic = %{version}
Provides:	httpd-mod_negotiation = %{version}
Provides:	httpd-mod_optional_fn_export = %{version}
Provides:	httpd-mod_optional_fn_import = %{version}
Provides:	httpd-mod_optional_hook_export = %{version}
Provides:	httpd-mod_optional_hook_import = %{version}
Provides:	httpd-mod_rewrite = %{version}
Provides:	httpd-mod_setenvif = %{version}
Provides:	httpd-mod_speling = %{version}
Provides:	httpd-mod_status = %{version}
Provides:	httpd-mod_unique_id = %{version}
Provides:	httpd-mod_usertrack = %{version}
Provides:	httpd-mod_version = %{version}
Provides:	httpd-mod_vhost_alias = %{version}
# these have been removed or renamed in 2.2.0
Obsoletes:	httpd-mod_access
Obsoletes:	httpd-mod_imap
Obsoletes:	httpd-mod_auth
Obsoletes:	httpd-mod_auth_anon
Obsoletes:	httpd-mod_auth_dbm
Obsoletes:	httpd-mod_auth_digest


%description modules
This package contains standard modules for Apache. It is required
for normal operation of the web server.


%package mod_dav
Summary:	Distributed Authoring and Versioning (WebDAV)
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper
Provides:	httpd-mod_dav_fs = %{version}
Provides:	httpd-mod_dav_lock = %{version}

%description mod_dav
This module provides class 1 and class 2 WebDAV ('Web-based
Distributed Authoring and Versioning') functionality for Apache.

This extension to the HTTP protocol allows creating, moving,
copying, and deleting resources and collections on a remote web
server.


%package mod_ldap
Summary:	LDAP connection pooling and result caching DSO:s
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper
Provides:	httpd-mod_authnz_ldap = %{version}
Obsoletes:	httpd-mod_auth_ldap

%description mod_ldap
This module was created to improve the performance of websites
relying on backend connections to LDAP servers. In addition to the
functions provided by the standard LDAP libraries, this module adds
an LDAP connection pool and an LDAP shared memory cache.


%package mod_cache
Summary:	Content cache keyed to URIs
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper

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
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(pre):	httpd-mod_cache = %{version}-%{release}
Requires(postun): rpm-helper
Obsoletes:	httpd-htcacheclean
Provides:	httpd-htcacheclean

%description mod_disk_cache
mod_disk_cache implements a disk based storage manager. It is
primarily of use in conjunction with mod_proxy.

Content is stored in and retrieved from the cache using URI-based
keys. Content with access protection is not cached.


%package mod_mem_cache
Summary:	Implements a memory based storage manager
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(pre):	httpd-mod_cache = %{version}-%{release}
Requires(postun): rpm-helper

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
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper

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
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper
Provides:	mod_gzip
Obsoletes:	mod_gzip

%description mod_deflate
The mod_deflate module provides the DEFLATE output filter that
allows output from your server to be compressed before being sent
to the client over the network.


%package mod_proxy
Summary:	HTTP/1.1 proxy/gateway server
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(pre):	httpd-mod_cache = %{version}-%{release}
Requires(pre):	httpd-mod_disk_cache = %{version}-%{release}
Requires(postun): rpm-helper
Provides:	httpd-mod_proxy_balancer = %{version}
Provides:	httpd-mod_proxy_connect = %{version}
Provides:	httpd-mod_proxy_ftp = %{version}
Provides:	httpd-mod_proxy_http = %{version}

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


%package mod_proxy_ajp
Summary:	Provides support for the Apache JServ Protocol version 1.3 (AJP13)
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(pre):	httpd-mod_cache = %{version}-%{release}
Requires(pre):	httpd-mod_proxy = %{version}-%{release}
Requires(postun): rpm-helper

%description mod_proxy_ajp
This module requires the service of mod_proxy. It provides support
for the Apache JServ Protocol version 1.3 (hereafter AJP13). Thus,
in order to get the ability of handling AJP13 protocol, mod_proxy
and mod_proxy_ajp have to be present in the server.


%package mod_userdir
Summary:	User-specific directories
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper

%description mod_userdir
This module allows user-specific directories to be accessed using the
http://example.com/~username/ syntax.


%package mod_ssl
Summary:	Strong cryptography using the SSL, TLS and distcache protocols
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(postun): rpm-helper
Requires:	openssl
Provides:	mod_ssl
Obsoletes:	mod_ssl

%description mod_ssl
This module provides SSL v2/v3 and TLS v1 support for the Apache
HTTP Server. It was contributed by Ralf S. Engeschall based on
his mod_ssl project and originally derived from work by Ben
Laurie.

This module relies on OpenSSL to provide the cryptography engine.


%package mod_dbd
Summary:	Manages SQL database connections
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(pre):	%mklibname apr-util 1
Requires(postun): rpm-helper

%description mod_dbd
mod_dbd manages SQL database connections using apr_dbd. It provides database
connections on request to modules requiring SQL database functions, and takes
care of managing databases with optimal efficiency and scalability for both
threaded and non-threaded MPMs.


%package mod_authn_dbd
Summary:	User authentication using an SQL database
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(pre):	httpd-conf >= %{version}
Requires(pre):	httpd-common = %{version}-%{release}
Requires(pre):	httpd-modules = %{version}-%{release}
Requires(pre):	httpd-mod_dbd = %{version}-%{release}
Requires(postun): rpm-helper

%description mod_authn_dbd
This module provides authentication front-ends such as mod_auth_digest and
mod_auth_basic to authenticate users by looking up users in SQL tables. Similar
functionality is provided by, for example, mod_authn_file. This module relies
on mod_dbd to specify the backend database driver and connection parameters,
and manage the database connections.


%package devel
Summary:	Module development tools for the Apache web server
Group:		Development/C
Requires:	apr-devel >= 1.2.7
Requires:	apr-util-devel >= 1.2.7
Requires:	pcre-devel >= 5.0
Requires:	byacc
Requires:	db4-devel
Requires:	expat-devel
Requires:	gdbm-devel
Requires:	openldap-devel
Requires:	libsasl-devel
Requires:	libtool >= 1.4.2
Requires:	openssl-devel
Requires:	autoconf2.5
Requires:	automake1.7
Requires:	pkgconfig
Requires:	perl-devel
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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version} -a 4 -a 6
%patch0 -p1 -b .deplibs.droplet
%patch1 -p1 -b .encode.droplet
%patch2 -p0 -b .xfsz.droplet
%patch3 -p1 -b .corelimit.droplet
%patch4 -p1 -b .debuglog.droplet
%patch5 -p1 -b .bsd-ipv6.droplet
%patch6 -p1 -b .apachesrc.droplet
%patch7 -p0 -b .apache2-suexec.droplet
%patch8 -p1 -b .apxs.droplet
%patch9 -p1 -b .disablemods.droplet
%patch10 -p1 -b .pod.droplet
%patch11 -p0 -b .memcache.droplet
%patch12 -p1 -b .french_fixes.droplet
%patch13 -p1 -b .authnoprov.droplet
%patch14 -p0 -b .certwatch.droplet

# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# don't install or use bundled pcreposix.h
rm -f include/pcreposix.h

# Fix apxs
perl -pi -e 's|\@exp_installbuilddir\@|%{_libdir}/httpd/build|;' support/apxs.in
perl -pi -e 's|get_vars\("prefix"\)|"%{_libdir}/httpd/build"|;' support/apxs.in
perl -pi -e 's|get_vars\("sbindir"\) . "/envvars"|"\$installbuilddir/envvars"|;' support/apxs.in

# Correct perl paths
find -type f|xargs perl -pi -e "s|/usr/local/bin/perl|perl|g;\
    s|/usr/local/bin/perl5|perl|g;s|/path/to/bin/perl|perl|g;"

perl -pi -e 's|" PLATFORM "|%{distribution}/%{release}|;' \
    server/core.c

# this is really better and easier than a stupid static patch...
# for some reason you have to use ">>" here (!)

cat >> config.layout << EOF
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
    proxycachedir: /var/cache/httpd/mod_proxy
</Layout>     
EOF

# Fix DYNAMIC_MODULE_LIMIT
perl -pi -e "s/DYNAMIC_MODULE_LIMIT 64/DYNAMIC_MODULE_LIMIT 128/;" include/httpd.h

# don't try to touch srclib
perl -pi -e "s|^SUBDIRS = .*|SUBDIRS = os server modules support|g" Makefile.in

# bump server limit
perl -pi -e "s|DEFAULT_SERVER_LIMIT 256|DEFAULT_SERVER_LIMIT 1024|g" server/mpm/prefork/prefork.c

# prepare the httpd-source package
rm -rf $RPM_BUILD_DIR/tmp-httpd-%{version}; mkdir -p $RPM_BUILD_DIR/tmp-httpd-%{version}/usr/src
cp -dpR $RPM_BUILD_DIR/httpd-%{version} $RPM_BUILD_DIR/tmp-httpd-%{version}/usr/src/httpd-%{version}
rm -rf $RPM_BUILD_DIR/tmp-httpd-%{version}/usr/src/httpd-%{version}/certwatch
rm -rf $RPM_BUILD_DIR/tmp-httpd-%{version}/usr/src/httpd-%{version}/perl-framework
rm -rf $RPM_BUILD_DIR/tmp-httpd-%{version}/usr/src/httpd-%{version}/tmp-httpd-%{version}/usr/src
rm -f $RPM_BUILD_DIR/tmp-httpd-%{version}%{_usrsrc}/httpd-%{version}/*.spec

# use my nice converted transparent png icons
tar -jxf %{_sourcedir}/apache2_transparent_png_icons.tar.bz2
mv icons/*.png docs/icons/

# add the changes file
cp %{_sourcedir}/httpd-README.urpmi README.urpmi


%build
#########################################################################################
# configure and build phase
#
export WANT_AUTOCONF_2_5="1"

# use a minimal buildconf instead
cp %{_sourcedir}/buildconf buildconf
sh ./buildconf

CFLAGS="%{optflags}"
CPPFLAGS="-DSSL_EXPERIMENTAL_ENGINE -DLDAP_DEPRECATED"
if pkg-config openssl; then
    # configure -C barfs with trailing spaces in CFLAGS
    CFLAGS="%{optflags} $CPPFLAGS"
    CPPFLAGS="$CPPFLAGS `pkg-config --cflags openssl | sed 's/ *$//'`"
    AP_LIBS="$AP_LIBS `pkg-config --libs openssl`"
else
    CFLAGS="%{optflags}"
    CPPFLAGS="$CPPFLAGS"
    AP_LIBS="$AP_LIBS -lssl -lcrypto"
fi
export CFLAGS CPPFLAGS AP_LIBS

APVARS="--enable-layout=AVX \
    --cache-file=../config.cache \
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
    --with-perl=%{_bindir}/perl \
    --with-apr=%{_bindir}/apr-1-config \
    --with-apr-util=%{_bindir}/apu-1-config \
    --with-pcre=%{_prefix} \
    --with-z=%{_prefix} \
    --with-devrandom \
    --enable-exception-hook \
    --enable-forward \
    --with-program-name=httpd"

for mpm in prefork; do
    mkdir build-${mpm}
    pushd build-${mpm}
        ln -s ../configure .

        if [ "${mpm}" = "prefork" ]; then
            %configure2_5x $APVARS \
                --with-mpm=prefork \
                --enable-modules=all \
                --enable-mods-shared=all \
                --with-ldap --enable-ldap=shared --enable-authnz-ldap=shared \
                --enable-cache=shared --enable-disk-cache=shared --enable-file-cache=shared --enable-mem-cache=shared \
                --enable-ssl --with-ssl=%{_prefix} \
                --enable-deflate=shared \
                --enable-cgid=shared \
                --enable-proxy=shared --enable-proxy-connect=shared --enable-proxy-ftp=shared \
                --enable-proxy-http=shared --enable-proxy-ajp=shared --enable-proxy-balancer=shared \
                --enable-dav=shared --enable-dav-fs=shared --enable-dav-lock=shared \
                --enable-version=shared \
                --enable-bucketeer=shared --enable-case-filter=shared --enable-case-filter-in=shared --enable-echo=shared \
                --enable-example=shared --enable-optional-fn-export=shared --enable-optional-fn-import=shared \
                --enable-optional-hook-export=shared --enable-optional-hook-import=shared \
                --enable-charset_lite=shared --enable-authn_alias=shared
        else
            %configure2_5x $APVARS \
                --with-mpm=${mpm} \
                --enable-modules=none
            # don't build support tools
            perl -pi -e "s|^SUBDIRS = .*|SUBDIRS = os server modules|g" Makefile
        fi

        # Copy configure flags to a file in the httpd-source rpm.
        cp config.nice $RPM_BUILD_DIR/tmp-httpd-%{version}%{_usrsrc}/httpd-%{version}/config.nice.${mpm}

        # if libexpat0-devel is installed on x86_64 somehow the EXTRA_LDLAGS is set 
        # to -L/usr/lib, fix that with a conditional hack...
        %ifarch x86_64
            find -type f | xargs perl -pi -e "s|/usr/lib\b|%{_libdir}|g"
        %endif

        # finally doing the build stage
        %make

    popd
done

# build the certwatch stuff
gcc %{optflags} -o certwatch/certwatch -Wall -Werror certwatch/certwatch.c -lcrypto

%if %{build_test}
# run the test suite, quite a hack, but works, sometimes...
TEST_DIR="`pwd`/TEST"
make -C build-prefork DESTDIR=${TEST_DIR} \
    manualdir=${TEST_DIR}/var/www/html/manual \
    install

perl -pi -e "s|%{_libdir}/httpd/|${TEST_DIR}%{_libdir}/httpd/|g" ${TEST_DIR}%{_sysconfdir}/httpd/conf/*
perl -pi -e "s|^#Include|Include|g" ${TEST_DIR}%{_sysconfdir}/httpd/conf/httpd.conf
perl -pi -e "s|/etc|${TEST_DIR}/etc|g" ${TEST_DIR}%{_sysconfdir}/httpd/conf/httpd.conf ${TEST_DIR}%{_sysconfdir}/httpd/conf/extra/*.conf
perl -pi -e  "s|%{_libdir}/httpd/build|${TEST_DIR}%{_libdir}/httpd/build|g" ${TEST_DIR}%{_sbindir}/apxs

# fool apxs
cat >> ${TEST_DIR}%{_libdir}/httpd/build/config_vars.mk << EOF
bindir = ${TEST_DIR}/usr/bin
sbindir = ${TEST_DIR}/usr/sbin
exec_prefix = ${TEST_DIR}/usr
datadir = ${TEST_DIR}/var/www
localstatedir = ${TEST_DIR}/var
libdir = ${TEST_DIR}%{_libdir}
libexecdir = ${TEST_DIR}%{_libdir}/httpd
includedir = ${TEST_DIR}/usr/include/httpd
sysconfdir = ${TEST_DIR}/etc/httpd/conf
installbuilddir = ${TEST_DIR}%{_libdir}/httpd/build
runtimedir = ${TEST_DIR}/var/run
proxycachedir = ${TEST_DIR}/var/cache/httpd/mod_proxy
prefix = ${TEST_DIR}/usr
EOF
 
pushd perl-framework
    #svn checkout --ignore-externals http://svn.apache.org/repos/asf/httpd/test/trunk/perl-framework perl-framework
    #svn checkout http://svn.apache.org/repos/asf/httpd/test/trunk/perl-framework perl-framework
    #svn up

    # disable test cases for bugs that has not been fixed yet,are too old, or
    # it is unclear who to blaim, either the php or ASF folks...
    rm -f t/php/arg.t
    rm -f t/php/func5.t

    # this test works with php-5.0 but not with php-5.1, yuck!
    rm -f t/php/virtual.t

    # if not using LC_ALL=C t/php/getlastmod.t can fail at
    # testing : getlastmod()
    # expected: november
    # received: November
    export LC_ALL=C

    perl Makefile.PL -apxs ${TEST_DIR}%{_sbindir}/apxs \
        -httpd_conf ${TEST_DIR}%{_sysconfdir}/httpd/conf/httpd.conf \
        -httpd ${TEST_DIR}%{_sbindir}/httpd
    make test
popd
%endif


# prevent some insane linkage
pushd build-prefork/support
    for i in htcacheclean logresolve rotatelogs; do
        rm -f ${i} ${i}.o
        %make AP_LIBS="`apr-1-config --apr-la-file`" $i
    done
popd


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
#########################################################################################
# install phase
#

mkdir -p %{buildroot}%{_libdir}/httpd
mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
mkdir -p %{buildroot}%{_localstatedir}/dav
mkdir -p %{buildroot}/var/{www,cache/httpd/mod_proxy}

#EXCLUDE_FROM_STRIP="%{buildroot}/%{_sbindir}/httpd"


# install source
tar c -C $RPM_BUILD_DIR/tmp-httpd-%{version} usr/src | tar x -C %{buildroot}

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
	proxycachedir=%{buildroot}/var/cache/httpd/mod_proxy
popd

# do some house cleaning 
for f in `find %{buildroot} -type f -name ".orig"` \
    `find %{buildroot} -type f -name ".deps"` \
    `find %{buildroot} -type f -name "NW*"` \
    `find %{buildroot} -type f -name "*.droplet"` \
    `find %{buildroot} -type f -name "*.zip"` \
    `find %{buildroot} -type f -name "*.dsp"`; do
    rm -f $f
done

# this is needed to generate the vanilla config
make -C build-prefork DESTDIR=`pwd` install-conf

#Fix config_vars.mk, and add some MDK flags so all other modules 
#can simply do "apxs -q VARIABLE" and know, for example, the exact
#release of httpd-devel or the exact directory where the source is
#located. 
CVMK="%{buildroot}%{_libdir}/httpd/build/config_vars.mk"
perl -pi -e "s|%{_builddir}/httpd-%{version}|%{srcdir}|g" $CVMK
perl -pi -e "s|%{buildroot}||g" $CVMK
perl -pi -e "s|^EXTRA_INCLUDES.*|EXTRA_INCLUDES = `apr-1-config --includes` -I%{_includedir}/httpd -I%{_includedir}/openssl|g" $CVMK

# fix libtool invocation
perl -pi -e "s|^LIBTOOL.*|LIBTOOL = libtool|g" $CVMK
perl -pi -e "s|^SH_LIBTOOL.*|SH_LIBTOOL = libtool|g" $CVMK


# if the following 3 lines needs to be enabled again, use the ".*" wildcard as in
# "s|bla bla =.*|bla bla = replaced whatever text after the equal char...|g"
#perl -pi -e "s|installbuilddir =.*|installbuilddir = %{_libdir}/httpd/build|g" $CVMK
#perl -pi -e "s|htdocsdir =.*|htdocsdir = /var/www/html|g" $CVMK
#perl -pi -e "s|logfiledir =.*|logfiledir = /var/log/httpd|g" $CVMK

echo "ap_version = %{version}" >> $CVMK
echo "ap_release = %{release}" >> $CVMK

#########################################################################################
# fix some bugs and other stuff
#
perl -pi -e "s|%{_builddir}/httpd-%{version}|%{srcdir}|g" %{buildroot}%{_libdir}/httpd/build/apr_rules.mk

mv %{buildroot}%{_sbindir}/envvars %{buildroot}%{_libdir}/httpd/build/

# named config.nice files are in the devel package
rm -f %{buildroot}%{_libdir}/httpd/build/config.nice


# Link build dir
ln -s ../../..%{_libdir}/httpd/build %{buildroot}%{_sysconfdir}/httpd/build

##################################################################

# install module conf files for the "modules.d" dir loading structure
install -d %{buildroot}/%{_sysconfdir}/httpd/modules.d
cp %{_sourcedir}/30_mod_proxy.conf %{buildroot}/%{_sysconfdir}/httpd/modules.d/30_mod_proxy.conf
cp %{_sourcedir}/31_mod_proxy_ajp.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/31_mod_proxy_ajp.conf
cp %{_sourcedir}/40_mod_ssl.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/40_mod_ssl.conf
cp %{_sourcedir}/41_mod_ssl.default-vhost.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/41_mod_ssl.default-vhost.conf
cp %{_sourcedir}/45_mod_dav.conf %{buildroot}/%{_sysconfdir}/httpd/modules.d/45_mod_dav.conf
cp %{_sourcedir}/46_mod_ldap.conf %{buildroot}/%{_sysconfdir}/httpd/modules.d/46_mod_ldap.conf
cp %{_sourcedir}/47_mod_authnz_ldap.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/47_mod_authnz_ldap.conf
cp %{_sourcedir}/55_mod_cache.conf %{buildroot}/%{_sysconfdir}/httpd/modules.d/55_mod_cache.conf
cp %{_sourcedir}/56_mod_disk_cache.conf %{buildroot}/%{_sysconfdir}/httpd/modules.d/56_mod_disk_cache.conf
cp %{_sourcedir}/57_mod_mem_cache.conf %{buildroot}/%{_sysconfdir}/httpd/modules.d/57_mod_mem_cache.conf
cp %{_sourcedir}/58_mod_file_cache.conf %{buildroot}/%{_sysconfdir}/httpd/modules.d/58_mod_file_cache.conf
cp %{_sourcedir}/59_mod_deflate.conf %{buildroot}/%{_sysconfdir}/httpd/modules.d/59_mod_deflate.conf
cp %{_sourcedir}/60_mod_dbd.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/60_mod_dbd.conf
cp %{_sourcedir}/61_mod_authn_dbd.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/61_mod_authn_dbd.conf
cp %{_sourcedir}/67_mod_userdir.conf %{buildroot}/%{_sysconfdir}/httpd/modules.d/67_mod_userdir.conf

# install missing files
install -m 0755 build-prefork/support/split-logfile %{buildroot}%{_sbindir}/split-logfile
install -m 0755 support/list_hooks.pl %{buildroot}%{_sbindir}/list_hooks.pl
install -m 0755 build-prefork/support/logresolve.pl %{buildroot}%{_sbindir}/logresolve.pl
install -m 0755 build-prefork/support/log_server_status %{buildroot}%{_sbindir}/log_server_status
install -m 0755 build-prefork/support/checkgid %{buildroot}%{_sbindir}/checkgid
install -m 0755 support/check_forensic %{buildroot}%{_sbindir}/check_forensic

# fix a msec safe cache for the ssl stuff
install -d %{buildroot}/var/cache/httpd/mod_ssl
touch %{buildroot}/var/cache/httpd/mod_ssl/scache.dir
touch %{buildroot}/var/cache/httpd/mod_ssl/scache.pag
touch %{buildroot}/var/cache/httpd/mod_ssl/scache.sem

# fix a msec safe cache for the mod_ldap LDAPSharedCacheFile
touch %{buildroot}/var/cache/httpd/mod_ldap_cache

# install the certwatch stuff
mkdir -p %{buildroot}{%{_sysconfdir}/cron.daily,%{_mandir}/man8,%{_sbindir}}
install -m 0755 certwatch/certwatch %{buildroot}%{_sbindir}/certwatch
install -m 0755 certwatch/certwatch.cron %{buildroot}%{_sysconfdir}/cron.daily/certwatch
install -m 0644 certwatch/certwatch.8 %{buildroot}%{_mandir}/man8/certwatch.8

%multiarch_includes %{buildroot}%{_includedir}/httpd/ap_config_layout.h

mkdir -p %{buildroot}%{_sysconfdir}/ssl/httpd

# add two important documentation files in the plain ASCII format
cp docs/manual/upgrading.html.en upgrading.html
cp docs/manual/new_features_2_2.html.en new_features_2_2.html

lynx -dump -nolist upgrading.html > upgrading.txt
lynx -dump -nolist new_features_2_2.html > new_features_2_2.txt

mkdir modules-doc
cp -a modules/README* modules-doc/
cp -a modules/proxy/CHANGES modules-doc/CHANGES.proxy

# cleanup
rm -f %{buildroot}%{_sbindir}/suexec
rm -f  %{buildroot}%{_mandir}/man8/suexec.8*
rm -rf %{buildroot}/var/www/html/index*
rm -rf %{buildroot}/var/www/html/apach*
rm -rf %{buildroot}/var/www/cgi-bin/printenv
rm -rf %{buildroot}/var/www/cgi-bin/test-cgi
rm -rf %{buildroot}/var/www/html/manual
rm -rf %{buildroot}%{_sysconfdir}/httpd/conf/{extra,original,httpd.conf,magic,mime.types}

#########################################################################################
# install phase done
#


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# Clean up "install source" and other generated dirs
[ "$RPM_BUILD_DIR/tmp-httpd-%{version}%{srcdir}" != "/" ] && rm -rf $RPM_BUILD_DIR/tmp-httpd-%{version}%{srcdir}
[ "$RPM_BUILD_DIR/usr/src" != "/" ] && rm -rf $RPM_BUILD_DIR/usr/src
[ "$RPM_BUILD_DIR/tmp-httpd-%{version}" != "/" ] && rm -rf $RPM_BUILD_DIR/tmp-httpd-%{version}


%post mod_proxy
%_post_srv httpd


%postun mod_proxy
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_proxy_ajp
%_post_srv httpd


%postun mod_proxy_ajp
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_dav
%_post_srv httpd


%postun mod_dav
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_ldap
%create_ghostfile /var/cache/httpd/mod_ldap_cache apache root 0600
%_post_srv httpd


%postun mod_ldap
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_cache
%_post_srv httpd


%postun mod_cache
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_disk_cache
%_post_srv httpd


%postun mod_disk_cache
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_mem_cache
%_post_srv httpd


%postun mod_mem_cache
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_file_cache
%_post_srv httpd


%postun mod_file_cache
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_deflate
%_post_srv httpd


%postun mod_deflate
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_userdir
%_post_srv httpd


%postun mod_userdir
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_ssl
if [ "$1" = "1" ]; then 
    if [ -d %{_sysconfdir}/ssl/httpd ]; then
        umask 077

        if [ ! -f %{_sysconfdir}/ssl/httpd/server.key ]; then
            %{_bindir}/openssl genrsa -rand /proc/apm:/proc/cpuinfo:/proc/dma:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/pci:/proc/rtc:/proc/uptime 1024 > \
                %{_sysconfdir}/ssl/httpd/server.key 2> /dev/null
        fi

        FQDN=`hostname`
        if [ "x${FQDN}" = "x" ]; then
            FQDN=localhost.localdomain
        fi

        if [ ! -f %{_sysconfdir}/ssl/httpd/server.crt ] ; then
            cat << EOF | %{_bindir}/openssl req -new -key %{_sysconfdir}/ssl/httpd/server.key -x509 -days 365 -set_serial $RANDOM -out %{_sysconfdir}/ssl/httpd/server.crt 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
root@${FQDN}
EOF
        fi
    fi
fi

# create some ghost files
%create_ghostfile /var/cache/httpd/mod_ssl/scache.dir apache root 0600
%create_ghostfile /var/cache/httpd/mod_ssl/scache.pag apache root 0600
%create_ghostfile /var/cache/httpd/mod_ssl/scache.sem apache root 0600

%_post_srv httpd


%postun mod_ssl
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_dbd
%_post_srv httpd


%postun mod_dbd
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%post mod_authn_dbd
%_post_srv httpd


%postun mod_authn_dbd
if [ "$1" = "0" ]; then
    %_post_srv httpd
fi


%pre common
%_pre_useradd apache /var/www /bin/sh 74


%postun common
%_postun_userdel apache


%post modules
%_post_srv httpd


%post
%_post_srv httpd


%postun
%_post_srv httpd


%files
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/httpd


%files modules
%defattr(-,root,root)
%dir %{_libdir}/httpd
%{_libdir}/httpd/mod_actions.so
%{_libdir}/httpd/mod_alias.so
%{_libdir}/httpd/mod_asis.so
%{_libdir}/httpd/mod_auth_basic.so
%{_libdir}/httpd/mod_auth_digest.so
%{_libdir}/httpd/mod_authn_alias.so
%{_libdir}/httpd/mod_authn_anon.so
%{_libdir}/httpd/mod_authn_dbm.so
%{_libdir}/httpd/mod_authn_default.so
%{_libdir}/httpd/mod_authn_file.so
%{_libdir}/httpd/mod_authz_dbm.so
%{_libdir}/httpd/mod_authz_default.so
%{_libdir}/httpd/mod_authz_groupfile.so
%{_libdir}/httpd/mod_authz_host.so
%{_libdir}/httpd/mod_authz_owner.so
%{_libdir}/httpd/mod_authz_user.so
%{_libdir}/httpd/mod_autoindex.so
%{_libdir}/httpd/mod_bucketeer.so
%{_libdir}/httpd/mod_case_filter.so
%{_libdir}/httpd/mod_case_filter_in.so
%{_libdir}/httpd/mod_cern_meta.so
%{_libdir}/httpd/mod_cgi.so
%{_libdir}/httpd/mod_cgid.so
%{_libdir}/httpd/mod_charset_lite.so
%{_libdir}/httpd/mod_dir.so
%{_libdir}/httpd/mod_dumpio.so
%{_libdir}/httpd/mod_echo.so
%{_libdir}/httpd/mod_env.so
%{_libdir}/httpd/mod_example.so
%{_libdir}/httpd/mod_expires.so
%{_libdir}/httpd/mod_ext_filter.so
%{_libdir}/httpd/mod_filter.so
%{_libdir}/httpd/mod_headers.so
%{_libdir}/httpd/mod_ident.so
%{_libdir}/httpd/mod_imagemap.so
%{_libdir}/httpd/mod_include.so
%{_libdir}/httpd/mod_info.so
%{_libdir}/httpd/mod_log_config.so
%{_libdir}/httpd/mod_log_forensic.so
%{_libdir}/httpd/mod_logio.so
%{_libdir}/httpd/mod_mime.so
%{_libdir}/httpd/mod_mime_magic.so
%{_libdir}/httpd/mod_negotiation.so
%{_libdir}/httpd/mod_optional_fn_export.so
%{_libdir}/httpd/mod_optional_fn_import.so
%{_libdir}/httpd/mod_optional_hook_export.so
%{_libdir}/httpd/mod_optional_hook_import.so
%{_libdir}/httpd/mod_rewrite.so
%{_libdir}/httpd/mod_setenvif.so
%{_libdir}/httpd/mod_speling.so
%{_libdir}/httpd/mod_status.so
%{_libdir}/httpd/mod_unique_id.so
%{_libdir}/httpd/mod_usertrack.so
%{_libdir}/httpd/mod_version.so
%{_libdir}/httpd/mod_vhost_alias.so
%{_libdir}/httpd/httpd.exp

%files mod_proxy
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_proxy.conf
%{_libdir}/httpd/mod_proxy_balancer.so
%{_libdir}/httpd/mod_proxy_connect.so
%{_libdir}/httpd/mod_proxy_ftp.so
%{_libdir}/httpd/mod_proxy_http.so
%{_libdir}/httpd/mod_proxy.so
%attr(0770,root,apache) %dir /var/cache/httpd/mod_proxy

%files mod_proxy_ajp
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_proxy_ajp.conf
%{_libdir}/httpd/mod_proxy_ajp.so

%files mod_dav
%defattr(-,root,root)
%attr(-,apache,apache) %dir %{_localstatedir}/dav
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_dav.conf
%{_libdir}/httpd/mod_dav.so
%{_libdir}/httpd/mod_dav_fs.so
%{_libdir}/httpd/mod_dav_lock.so

%files mod_ldap
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_ldap.conf
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_authnz_ldap.conf
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ldap_cache
%{_libdir}/httpd/mod_ldap.so
%{_libdir}/httpd/mod_authnz_ldap.so

%files mod_cache
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_cache.conf
%{_libdir}/httpd/mod_cache.so

%files mod_disk_cache
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_disk_cache.conf
%{_libdir}/httpd/mod_disk_cache.so
%attr(0755,root,root) %{_sbindir}/htcacheclean
%{_mandir}/man8/htcacheclean.8*

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

%files mod_ssl
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_ssl.default-vhost.conf
%dir %{_sysconfdir}/ssl/httpd
%{_sysconfdir}/cron.daily/certwatch
%attr(0755,root,root) %{_sbindir}/certwatch
%{_libdir}/httpd/mod_ssl.so
%attr(0700,apache,root) %dir /var/cache/httpd/mod_ssl
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ssl/scache.dir
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ssl/scache.pag
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ssl/scache.sem
%{_mandir}/man8/certwatch.8*

%files mod_dbd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_dbd.conf
%{_libdir}/httpd/mod_dbd.so

%files mod_authn_dbd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_authn_dbd.conf
%{_libdir}/httpd/mod_authn_dbd.so

%files common
%defattr(-,root,root)
%attr(0700,apache,root) %dir /var/cache/httpd
%dir /var/www/error
%dir /var/www/error/include
%config(noreplace,missingok) /var/www/error/README
%config(noreplace,missingok) /var/www/error/*.var
%config(noreplace,missingok) /var/www/error/include/*.html
/var/www/icons/README*
/var/www/icons/*.gif
/var/www/icons/*.png
/var/www/icons/small/README*
/var/www/icons/small/*.gif
/var/www/icons/small/*.png
%{_mandir}/*/*
%exclude %{_mandir}/man8/htcacheclean.8*
%attr(0755,root,root) %{_sbindir}/ab
%attr(0755,root,root) %{_sbindir}/apachectl
%attr(0755,root,root) %{_sbindir}/check_forensic
%attr(0755,root,root) %{_sbindir}/checkgid
%attr(0755,root,root) %{_sbindir}/dbmmanage
%attr(0755,root,root) %{_sbindir}/htdbm
%attr(0755,root,root) %{_sbindir}/htdigest
%attr(0755,root,root) %{_sbindir}/htpasswd
%attr(0755,root,root) %{_sbindir}/httxt2dbm
%attr(0755,root,root) %{_sbindir}/list_hooks.pl
%attr(0755,root,root) %{_sbindir}/logresolve
%attr(0755,root,root) %{_sbindir}/logresolve.pl
%attr(0755,root,root) %{_sbindir}/log_server_status
%attr(0755,root,root) %{_sbindir}/rotatelogs
%attr(0755,root,root) %{_sbindir}/split-logfile

%files devel
%defattr(-,root,root)
%multiarch %{multiarch_includedir}/httpd/ap_config_layout.h
%{_includedir}/httpd
%attr(0755,root,root) %dir %{_libdir}/httpd/build
%attr(0755,root,root) %dir %{_sysconfdir}/httpd/build
%attr(0644,root,root) %{_libdir}/httpd/build/*.mk
%attr(0755,root,root) %{_libdir}/httpd/build/*.sh
%attr(0755,root,root) %{_libdir}/httpd/build/envvars
%attr(0755,root,root) %{_sbindir}/envvars-std
%attr(0755,root,root) %{_sbindir}/apxs

%files source
%defattr(-,root,root)
%{srcdir}

%files doc
%defattr(-,root,root)
%doc etc/httpd/conf/httpd.conf etc/httpd/conf/extra/*.conf
%doc README.urpmi upgrading.txt new_features_2_2.txt
%doc modules-doc


%changelog
* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- fix obsoletes/provides on mod_disk_cache

* Mon Nov 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- rebuild against new pcre

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- rebuild against new openssl
- rebuild against new openldap
- spec cleanups
- remove all apache* module obsoletes/provides

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- 2.2.3 (fixes CVE-2006-3747)

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2
- move the README file from httpd-conf to httpd

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2
- rebuild against new db4

* Mon May 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2
- change back the /etc/pki//tls/private/localhost.* stuff to our
  preferred /etc/ssl/httpd/server.*
- drop the htcacheclean initscript; it daemonizes itself to the background
  so we can't supervise this, however it does run out of cron so we'll add
  htcacheclean itself to the httpd-mod_disk_cache package and drop the
  -htcacheclean subpackage
- remove left-over prereq's

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2
- 2.2.2
- major spec changes
- remove the mod_whatkilledus and mod_backtrace modules
- update requires for new apr/apr-util (1.2.7)
- add mod_proxy_ajp, mod_dbd, mod_authn_dbd, htcacheclean packages
- move mod_ssl to this package rather than it being a standalone-module
- add the perl-framework
- add htcacheclean to cleanup after mod_cache
- add -doc subpackage
- rebuild with gcc4

* Fri Feb 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55
- P104: security fix for CVE-2005-3352
- P105: security fix for CVE-2005-3357 (doesn't affect us since we don't use
  the worker mpm; if it did we would have to rebuild mod_ssl too) -- apply
  it for completeness

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55
- 2.0.55; includes fixes for CAN-2005-2088, CAN-2005-2700, CAN-2005-2491,
  CAN-2005-2728, CAN-2005-1268 (only CAN-2005-2491 was previously unpatched)
- drop the worker mpm; it needs thread-safe modules which excludes a
  whole whack of stuff
- rediff P22
- drop P32, P33, P34, P35, P105, P122, P123, P124, P125; merged upstream
- drop P104; we don't ship/use the peruser mpm

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54
- Clean rebuild

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-4avx
- rebuild against new pcre

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-3avx
- make httpd-worker provide httpd
- new style PreReq

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-2avx
- P124: patch to fix CAN-2005-2700
- P125: patch to fix CAN-2005-2728
- provide all the modules we obsoleted in httpd-modules

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-1avx
- 2.0.54
- the great apache2->httpd/httpd2->http migration
- sync patches with mandrake 2.0.54-10mdk
- use modules.d to load modules rather than modules.d
- P122: security fix for CAN-2005-1268
- P123: security fix for CAN-2005-2088
- added README.urpmi
- mod_userdir is it's own sub-package
- BuildRequires: zlib-devel

* Tue Aug 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-4avx
- drop the requirements of libtool for apache2
- fix deps

* Tue Aug 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-4avx
- P54: from SVN, to fix compilation of mod_ssl with openssl 0.9.8

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-2avx
- rebuild

* Fri Feb 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-1avx
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

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52-5avx
- rebuild against new gdbm

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52-4avx
- rebuild against new openssl

* Wed Nov 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52-3avx
- P106: patch to fix CAN-2004-0942

* Fri Nov  5 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52-2avx
- P105: patch to fix CAN-2004-0885

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52-1avx
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

* Tue Sep 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49-8avx
- P9-P13: security patches for CAN-2004-0748, CAN-2004-0751, 
  CAN-2004-0747, CAN-2004-0786, and CAN-2004-0809
- updated runscripts

* Thu Aug 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49-7avx
- log/run was still logging to /var/log/supervise/apache2 rather than
  ../httpd2; fixed

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49-6avx
- rebuild against new openssl

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49-5avx
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

* Mon Jun 28 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49-4avx
- P8: security fix for CAN-2004-0493

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49-3avx
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
