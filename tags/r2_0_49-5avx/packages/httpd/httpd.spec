%define name	apache2
%define version	2.0.49
%define release	5avx

#
#(ie. use with rpm --rebuild):
#
#	--with debug	Compile with debugging code
# 
#  enable build with debugging code: will _not_ strip away any debugging code,
#  will _add_ -g3 to CFLAGS, will _add_ --enable-maintainer-mode to 
#  configure.

# this is only a embryo (different mpm's), someone should merge 
# the stuff Peter Poeml at suse has done, check here:
# http://www.deserve-it.com/Cooker/apache2.spec.txt
# http://ftp.gwdg.de/pub/linux/suse/ftp.suse.com/projects/apache/
# actually this stuff origins from redhat, not suse and is included
# in the provided spec file from the tarball, any takers?

%define mpm	prefork
%define dbver	db4
%define dbmver	db4

# not everyone uses this, so define it here
%define distribution	Annvix
%define build_debug	0
%define build_distcache	0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_debug: %{expand: %%define build_debug 1}}
%{?_with_distcache: %{expand: %%define build_distcache 1}}

%if %{build_debug}
# disable build root strip policy
%define __spec_install_post %{_prefix}/lib/rpm/brp-compress || :

# This gives extra debuggin and huge binaries
%{expand:%%define optflags %{optflags} %([ ! $DEBUG ] && echo '-g3')}
%endif

%define ap_ldap_libs -lldap -llber -lsasl2 -lssl -lcrypto

%if %{build_distcache}
%define ap_ssl_libs -lssl -lcrypto -ldistcache -lnal
%else
%define ap_ssl_libs -lssl -lcrypto
%endif

%define real_version	2.0.49
%define ap_version	%{version}
%define ap_release	%{release}
%define sourcename	httpd-%{version}

#New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}

#If you change these, change also ADVX-build
%define ap_name		apache2
%define apr_name	%mklibname apr 0

Summary:		The Apache2 web server.
Name:			%{ap_name}
Version:		%{ap_version}
Release:		%{ap_release}
License:		Apache License
Group:			System/Servers
URL:			http://www.advx.org
Source0:		%{sourcename}.tar.gz
Source1:		%{sourcename}.tar.gz.asc
Source2: 		README.ADVX
Source3:		apache-old-changelog
Source4:		apache2_transparent_png_icons.tar.bz2
Source5: 		gentestcrt.sh.bz2
Source7:		apache2.run
Source8:		apache2-log.run
# please keep this logic.
Source30:		30_mod_proxy.conf.bz2
Source40: 		40_mod_ssl.conf.bz2
Source41: 		41_mod_ssl.default-vhost.conf.bz2
Source45: 		45_mod_dav.conf.bz2
Source46: 		46_mod_ldap.conf.bz2
Source55:		55_mod_cache.conf.bz2
Source56:		56_mod_disk_cache.conf.bz2
Source57:		57_mod_mem_cache.conf.bz2
Source58:		58_mod_file_cache.conf.bz2
Source59:		59_mod_deflate.conf.bz2
Source60:		03_apache2.afterboot

Patch0:			httpd-2.0.46-sslink.patch.bz2
Patch1:			httpd-2.0.36-suexec.patch.bz2
Patch2:			httpd-2.0.40-apxs.patch.bz2
# OE: prepare for the mod_limitipconn module found here:
# http://dominia.org/djao/limitipconn.html
Patch3:			apachesrc.diff.bz2
# JMD: fix suexec path so we can have both versions of Apache and both
# versions of suexec
Patch4:			apache2-suexec.patch.bz2
# OE: http://distcache.sourceforge.net/
Patch5:			httpd-2.0.48-distcache.patch.bz2
# OE: http://bitbrook.de/software/mod_log_mysql/
Patch6:			httpd-2.0.49-mod_log_mysql.diff.bz2
Patch7:			apache-2.0-can-2004-0488.patch.bz2
Patch8:			apache-2.0.49-CAN-2004-0493.patch.bz2
# OE: stolen from redhat
Patch40:		httpd-2.0.45-cnfdir.patch.bz2
Patch41:		httpd-2.0.45-parallel.patch.bz2

BuildRoot:		%{_tmppath}/%{ap_name}-%{version}-buildroot
BuildPreReq:		ADVX-build >= 9.2
BuildRequires:		byacc
BuildRequires:		%{dbver}-devel
BuildRequires:		gif2png
BuildRequires:		glibc-devel
BuildRequires:		expat-devel
BuildRequires:		gdbm-devel
BuildRequires:		openldap-devel
BuildRequires:		libsasl-devel
BuildRequires:		libtool >= 1.4.2
BuildRequires:		openssl-devel
BuildRequires:		perl >= 0:5.600
BuildRequires:		zlib-devel
%if %{build_distcache}
BuildRequires:		libdistcache1 >= 1.4.2
BuildRequires:		distcache-devel >= 1.4.2
%endif
BuildConflicts: 	BerkeleyDB-devel

PreReq:			%{ap_name}-conf >= 2.0.46-2mdk
PreReq:			%{ap_name}-common
PreReq: 		%{ap_name}-modules = %{ap_version}
PreReq:			%{apr_name} = %{ap_version}
PreReq:			afterboot srv rpm-helper
Requires:		libtool  >= 1.4.2
Provides:		webserver 
Provides:		apache
#2.0.45 is binary compatible with 2.0.44, permit use of modules
#from the old version
Provides:		%{ap_name} = 2.0.44


%description
This package contains the main binary of %{ap_name}, a powerful, full-featured, 
efficient and freely-available Web server. Apache is also the most popular Web
server on the Internet.

This version of %{ap_name} is fully modular, and many modules are available in
pre-compiled formats, like PHP4 and mod_auth_external.

You can build %{ap_name} with some conditional build swithes;

(ie. use with rpm --rebuild):
--with debug   Compile with debugging code

%package common
Summary:	Files common for %{ap_name} and %{ap_name}-mod_perl installations
Group:		System/Servers
Prereq:		rpm-helper
Prereq:		%{apr_name} = %{ap_version}
Obsoletes:	apache-common
Provides:	apache-common

%description common
This package contains files required for both %{ap_name} and %{ap_name}-mod_perl
package installations. Install this if you want to install %{ap_name} or/and
%{ap_name} with mod_perl.

%package modules
Summary:	Standard modules for %{ap_name}
Group:		System/Servers
Provides:	%{ap_name}-mod_access = %{version}
Provides:	%{ap_name}-mod_actions = %{version}
Provides:	%{ap_name}-mod_alias = %{version}
Provides:	%{ap_name}-mod_asis = %{version}
Provides:	%{ap_name}-mod_auth = %{version}
Provides:	%{ap_name}-mod_auth_anon = %{version}
Provides:	%{ap_name}-mod_auth_dbm = %{version}
Provides:	%{ap_name}-mod_auth_digest = %{version}
Provides:	%{ap_name}-mod_autoindex = %{version}
Provides:	%{ap_name}-mod_case_filter = %{version}
Provides:	%{ap_name}-mod_case_filter_in = %{version}
Provides:	%{ap_name}-mod_cern_meta = %{version}
Provides:	%{ap_name}-mod_cgi = %{version}
Provides:	%{ap_name}-mod_cgid = %{version}
Provides:	%{ap_name}-mod_charset_lite = %{version}
Provides:	%{ap_name}-mod_dir = %{version}
Provides:	%{ap_name}-mod_env = %{version}
Provides:	%{ap_name}-mod_expires = %{version}
Provides:	%{ap_name}-mod_ext_filter = %{version}
Provides:	%{ap_name}-mod_headers = %{version}
Provides:	%{ap_name}-mod_imap = %{version}
Provides:	%{ap_name}-mod_include = %{version}
Provides:	%{ap_name}-mod_info = %{version}
Provides:	%{ap_name}-mod_log_config = %{version}
Provides:	%{ap_name}-mod_logio = %{version}
Provides:	%{ap_name}-mod_mime = %{version}
Provides:	%{ap_name}-mod_mime_magic = %{version}
Provides:	%{ap_name}-mod_negotiation = %{version}
Provides:	%{ap_name}-mod_rewrite = %{version}
Provides:	%{ap_name}-mod_setenvif = %{version}
Provides:	%{ap_name}-mod_speling = %{version}
Provides:	%{ap_name}-mod_status = %{version}
Provides:	%{ap_name}-mod_unique_id = %{version}
Provides:	%{ap_name}-mod_userdir = %{version}
Provides:	%{ap_name}-mod_usertrack = %{version}
Provides:	%{ap_name}-mod_vhost_alias = %{version}

%description modules
This package contains standard modules for %{ap_name}. It is required
for normal operation of the web server.

%package mod_dav
Summary:	Distributed Authoring and Versioning (WebDAV)
Group:		System/Servers
Prereq:		%{ap_name}-conf
Prereq:		%{ap_name}-common
Prereq:		%{ap_name}-modules = %{ap_version}
Prereq:		%{apr_name} = %{ap_version}
Provides:	%{ap_name}-mod_dav_fs = %{version}

%description mod_dav
This module provides class 1 and class 2 WebDAV ('Web-based
Distributed Authoring and Versioning') functionality for Apache.

This extension to the HTTP protocol allows creating, moving,
copying, and deleting resources and collections on a remote web
server.

%package mod_ssl
Summary:	Strong cryptography using the SSL and TLS protocols
Group:		System/Servers
Prereq:		%{ap_name}-conf
Prereq:		%{ap_name}-common
Prereq:		%{ap_name}-modules = %{ap_version}
Prereq:		%{apr_name} = %{ap_version}
%if %{build_distcache}
#Requires:	distcache
Requires:	libdistcache1 >= 1.4.2
%endif

%description mod_ssl
This module provides SSL v2/v3 and TLS v1 support for the Apache
HTTP Server. It was contributed by Ralf S. Engeschall based on
his mod_ssl project and originally derived from work by Ben
Laurie.

It also includes ab-ssl, the Apache Benchmarks for SSL.

This module relies on OpenSSL to provide the cryptography engine.

%package mod_ldap
Summary:	LDAP connection pooling and result caching DSO:s
Group:		System/Servers
Prereq:		%{ap_name}-conf
Prereq:		%{ap_name}-common
Prereq:		%{ap_name}-modules = %{ap_version}
Prereq:		%{apr_name} = %{ap_version}
Provides:	%{ap_name}-mod_auth_ldap.so = %{version}

%description mod_ldap
This module was created to improve the performance of websites
relying on backend connections to LDAP servers. In addition to the
functions provided by the standard LDAP libraries, this module
adds an LDAP connection pool and an LDAP shared memory cache.

%package mod_cache
Summary:	Content cache keyed to URIs
Group:		System/Servers
Prereq:		%{ap_name}-conf
Prereq:		%{ap_name}-common
Prereq:		%{ap_name}-modules = %{ap_version}
Prereq:		%{apr_name} = %{ap_version}

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
Prereq:		%{ap_name}-conf
Prereq:		%{ap_name}-common
Prereq:		%{ap_name}-modules = %{ap_version}
Prereq:		%{apr_name} = %{ap_version}
Prereq:		%{ap_name}-mod_cache = %{ap_version}

%description mod_disk_cache
mod_disk_cache implements a disk based storage manager. It is
primarily of use in conjunction with mod_proxy.

Content is stored in and retrieved from the cache using URI
based keys. Content with access protection is not cached.

%package mod_mem_cache
Summary:	Implements a memory based storage manager
Group:		System/Servers
Prereq:		%{ap_name}-conf
Prereq:		%{ap_name}-common
Prereq:		%{ap_name}-modules = %{ap_version}
Prereq:		%{apr_name} = %{ap_version}
Prereq:		%{ap_name}-mod_cache = %{ap_version}

%description mod_mem_cache
This module requires the service of mod_cache. It acts as a
support module for mod_cache and provides a memory based storage
manager. mod_mem_cache can be configured to operate in two modes:
caching open file descriptors or caching objects in heap storage.
mod_mem_cache is most useful when used to cache locally generated
content or to cache backend server content for mod_proxy
configured for ProxyPass (aka reverse proxy).

Content is stored in and retrieved from the cache using URI based
keys. Content with access protection is not cached.

%package mod_file_cache
Summary:	Caches a static list of files in memory
Group:		System/Servers
Prereq:		%{ap_name}-conf
Prereq:		%{ap_name}-common
Prereq:		%{ap_name}-modules = %{ap_version}
Prereq:		%{apr_name} = %{ap_version}

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
Prereq:		%{ap_name}-conf
Prereq:		%{ap_name}-common
Prereq:		%{ap_name}-modules = %{ap_version}
Prereq:		%{apr_name} = %{ap_version}
Provides:	mod_gzip
Obsoletes:	mod_gzip

%description mod_deflate
The mod_deflate module provides the DEFLATE output filter that
allows output from your server to be compressed before being sent
to the client over the network.

%package mod_proxy
Summary:	HTTP/1.1 proxy/gateway server
Group:		System/Servers
Prereq:		%{ap_name}-conf
Prereq:		%{ap_name}-common
Prereq:		%{ap_name}-modules = %{ap_version}
Prereq:		%{apr_name} = %{ap_version}
Prereq:		%{ap_name}-mod_cache = %{ap_version}
Prereq:		%{ap_name}-mod_disk_cache = %{ap_version}
Provides:	%{ap_name}-mod_proxy_connect = %{ap_version}
Provides:	%{ap_name}-mod_proxy_ftp = %{ap_version}
Provides:	%{ap_name}-mod_proxy_http = %{ap_version}

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

%package -n %{apr_name}
Summary:	The Apache Portable Runtime library
Group:		System/Libraries
Provides:	libapr apr
Obsoletes:	libapr apr

%description -n	%{apr_name}
The Apache Portable Run-time libraries have been designed to provide a
common interface to low level routines across any platform.

%package devel
Group:		Development/C
Summary:	Module development tools for the %{ap_name} web server.
Requires:	perl >= 0:5.600
#JMD: You *don't* need the apache binaries to develop modules...
#Requires:	%{ap_name} = %{ap_version}
#JMD: But you now need ADVX-build...
Requires:	ADVX-build >= 9.2
Requires:	%{apr_name} = %{ap_version}
Requires:	gdbm-devel
Requires:	expat-devel
Requires:	glibc-devel
Requires:	openssl-devel
Requires:	libtool  >= 1.4.2
Requires:	pcre-devel
%if %{build_distcache}
Requires:	distcache-devel >= 1.4.2
%endif
Provides:	%{ap_name}-mod_ssl-devel
Obsoletes:	%{ap_name}-mod_ssl-devel
Provides:	libapr-devel apr-devel
Obsoletes:	libapr-devel apr-devel

%description devel
The %{ap_name}-devel package contains the source code for the %{ap_name}
Web server and the APXS binary you'll need to build Dynamic
Shared Objects (DSOs) for %{ap_name}.

It also provides the includes and linker libraries for development with APR.

If you are installing the %{ap_name} Web server and
you want to be able to compile or develop additional modules
for %{ap_name}, you'll need to install this package.

%package source
Summary:	The %{ap_name} Source
Group:		Development/C
#No use to install it if you don't have libgdbm.so and libpthread.so!
Requires:	db1-devel
#Do not require libdb*-devel, it breaks the upgrade from 9.0 to 9.1.
#Instead, each Apache module that requires libdb* to compile should add it to its
#buildrequires
#Requires:	%{dbver}-devel
Requires:	gdbm-devel
Requires:	glibc-devel

%description source
The %{ap_name} Source, including %{distribution} patches. Use this package to
build %{ap_name}-mod_perl, or your own custom version.

%prep

%setup -q -n %{sourcename}
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p1
%patch4 -p0

# OE: patch the source anyway, this way one could compile 
# the mod_ssl module with the distcache support from the 
# apache-source package, will try this later on.
%patch5 -p1

# OE: http://bitbrook.de/software/mod_log_mysql/
%patch6 -p1

# security
%patch7 -p1 -b .can-2004-0488
%patch8 -p0 -b .can-2004-0493

# OE: stolen from redhat
#%patch40 -p1
%patch41 -p0

#Fix apxs
%{__perl} -pi -e 's|\@exp_installbuilddir\@|%{ap_installbuilddir}|;' support/apxs.in
%{__perl} -pi -e 's|get_vars\("prefix"\)|"%{ap_installbuilddir}"|;' support/apxs.in
%{__perl} -pi -e 's|get_vars\("sbindir"\) . "/envvars"|"\$installbuilddir/envvars"|;' support/apxs.in

#Correct perl paths
find -type f|xargs perl -pi -e " s|/usr/local/bin/perl|%{__perl}|g; \
        s|/usr/local/bin/perl5|%{__perl}|g; \
        s|/path/to/bin/perl|%{__perl}|g; \
        "
%{__perl} -pi -e 's|PRODUCT "Apache"|PRODUCT "Apache-AdvancedExtranetServer"|;' \
	include/ap_release.h


%{__perl} -pi -e 's|" PLATFORM "|%{distribution}/%{ap_release}|;' \
        server/core.c

# use my nice converted transparent png icons
tar -jxf %{SOURCE4}
mv icons/*.png docs/icons/

# this is really better and easier than a stupid static patch...
# for some reason you have to use ">>" here (!)

%{__cat} >> config.layout << EOF
<Layout ADVX>
    prefix:        %{ap_prefix}
    exec_prefix:   %{_prefix}
    bindir:        %{_bindir}
    sbindir:       %{_sbindir}
    libdir:        %{_libdir}
    libexecdir:    %{ap_libexecdir}
    mandir:        %{_mandir}
    infodir:       %{_infodir}
    includedir:    %{ap_includedir}
    sysconfdir:    %{ap_sysconfdir}
    datadir:       %{ap_datadir}
    installbuilddir: %{ap_installbuilddir}
    errordir:      %{ap_datadir}/error
    iconsdir:      %{ap_datadir}/icons
    htdocsdir:     %{ap_htdocsdir}
    manualdir:     %{ap_htdocsdir}/manual
    cgidir:        %{ap_datadir}/cgi-bin
    localstatedir: /var
    runtimedir:    /var/run
    logfiledir:    %{ap_logfiledir}
    proxycachedir: %{ap_proxycachedir}
</Layout>     
EOF

# OE: we need to do this on APR and APR-UTIL as a
# work around for stupid PLD logic. (!?)

%{__cat} >> srclib/apr/config.layout << EOF
<Layout ADVX>
    prefix:        %{ap_prefix}
    exec_prefix:   %{_prefix}
    bindir:        %{_bindir}
    sbindir:       %{_sbindir}
    libdir:        %{_libdir}
    libexecdir:    %{ap_libexecdir}
    mandir:        %{_mandir}
    infodir:       %{_infodir}
    includedir:    %{ap_includedir}
    sysconfdir:    %{ap_sysconfdir}
    datadir:       %{ap_datadir}
    installbuilddir: %{ap_installbuilddir}
    errordir:      %{ap_datadir}/error
    iconsdir:      %{ap_datadir}/icons
    htdocsdir:     %{ap_htdocsdir}
    manualdir:     %{ap_htdocsdir}/manual
    cgidir:        %{ap_datadir}/cgi-bin
    localstatedir: /var
    runtimedir:    /var/run
    logfiledir:    %{ap_logfiledir}
    proxycachedir: %{ap_proxycachedir}
    libsuffix:     -\${APR_MAJOR_VERSION}
</Layout>     
EOF

%{__cat} >> srclib/apr-util/config.layout << EOF
<Layout ADVX>
    prefix:        %{ap_prefix}
    exec_prefix:   %{_prefix}
    bindir:        %{_bindir}
    sbindir:       %{_sbindir}
    libdir:        %{_libdir}
    libexecdir:    %{ap_libexecdir}
    mandir:        %{_mandir}
    infodir:       %{_infodir}
    includedir:    %{ap_includedir}
    sysconfdir:    %{ap_sysconfdir}
    datadir:       %{ap_datadir}
    installbuilddir: %{ap_installbuilddir}
    errordir:      %{ap_datadir}/error
    iconsdir:      %{ap_datadir}/icons
    htdocsdir:     %{ap_htdocsdir}
    manualdir:     %{ap_htdocsdir}/manual
    cgidir:        %{ap_datadir}/cgi-bin
    localstatedir: /var
    runtimedir:    /var/run
    logfiledir:    %{ap_logfiledir}
    proxycachedir: %{ap_proxycachedir}
    libsuffix:     -\${APRUTIL_MAJOR_VERSION}
</Layout>     
EOF

#Fix DYNAMIC_MODULE_LIMIT
perl -pi -e "s/DYNAMIC_MODULE_LIMIT 64/DYNAMIC_MODULE_LIMIT 96/;" \
	include/httpd.h

# update config.{sub,guess}
%{?__cputoolize: %{__cputoolize} -c srclib/apr}
%{?__cputoolize: %{__cputoolize} -c srclib/pcre}
%{?__cputoolize: %{__cputoolize} -c srclib/apr-util/xml/expat}
%{?__cputoolize: %{__cputoolize} -c srclib/apr-util}

%build
#########################################################################################
# configure and build phase
#

export WANT_AUTOCONF_2_5="1"

%serverbuild

#JMD: -fno-strict-aliasing -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 is used by mod_perl
#export CFLAGS="%{optflags} -fno-strict-aliasing -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
#export CPPFLAGS="-fno-strict-aliasing -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
#JMD: but only when we manage to fix the conflict between HAVE_SENDFILE and
#JMD: HAVE_LARGEFILE in the APR sources.
export SSL_BASE="SYSTEM"

# NOTE! "--enable-modules=all --enable-mods-shared=all" won't 
# enable _all_ modules, that's why I had to specify all of them...

# We need to re-run ./buildconf because of any applied patch(es)
./buildconf

APVARS="--with-mpm=%{mpm} \
%if %{build_debug}
    --enable-debug \
    --enable-maintainer-mode \
%endif
    --with-dbm=%{dbmver} \
    --with-expat=%{_prefix} \
    --with-pcre=%{_prefix} \
    --enable-layout=ADVX \
    --prefix=%{ap_prefix} \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --libexecdir=%{ap_libexecdir} \
    --sysconfdir=%{ap_sysconfdir} \
    --localstatedir=/var \
    --includedir=%{ap_includedir} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --datadir=%{ap_datadir} \
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
    --enable-ssl=shared \
    --with-ssl=%{_prefix} \
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
    --with-ldap \
    --enable-forward \
%ifarch %ix86
%ifnarch i386 i486
    --enable-nonportable-atomics=yes \
%endif
%endif
%if %{build_distcache}
    --enable-distcache \
%endif
    --with-program-name=%{ap_progname}"

%configure2_5x $APVARS

# OE: avoid linking of *everything* against all libs, mucho gracias suse!
for lib in ldap lber sasl sasl2 ssl crypto distcache nal; do
    %{__perl} -pi -e "s|-l$lib||g" build/config_vars.mk
done

%{__sed}  '/SH_LINK.*util_ldap/ s/$/ %{ap_ldap_libs}/' modules/experimental/modules.mk > tmp; %{__mv} tmp modules/experimental/modules.mk
%{__sed}  '/SH_LINK.*auth_ldap/ s/$/ %{ap_ldap_libs}/' modules/experimental/modules.mk > tmp; %{__mv} tmp modules/experimental/modules.mk
%{__sed}  '/SH_LINK.*mod_ssl/ s/$/ %{ap_ssl_libs}/' modules/ssl/modules.mk > tmp; %{__mv} tmp modules/ssl/modules.mk

mv README.distcache modules/ssl/

####
#Copy pre-patched %{ap_name} source so we can package an %{ap_name}-source rpm and
#use it to build mod_perl
rm -rf ../tmp-%{sourcename}
install -d ../tmp-%{sourcename}/usr/src
cp -dpR $RPM_BUILD_DIR/%{sourcename} ../tmp-%{sourcename}%{ap_abs_srcdir}

#Copy configure flags to a file in the %{ap_name}-source rpm.
echo $APVARS > ../tmp-%{sourcename}%{ap_abs_srcdir}/APVARS

# finally doing the build stage
%make

# make the ab2-ssl addon
pushd support
    rm ab .libs/ab ab.lo ab.o
    make ab CFLAGS="%{optflags} -DUSE_SSL -lcrypto -lssl -I%{_includedir}/openssl -L%{_libdir}"
    mv ab ab-ssl; mv .libs/ab .libs/ab-ssl; rm ab.lo ab.o
    make ab
popd

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
#########################################################################################
# install phase
#

install -d %{buildroot}

# make mr. lint happy and do some house cleaning...
pushd ../tmp-%{sourcename}%{ap_abs_srcdir}
    make clean; rm -rf autom4te.cache icons
    for f in `find . -type f -name ".orig"` \
	`find . -type f -name ".deps"` \
	`find . -type f -name ".indent.pro"` \
	`find . -type f -name ".gdbinit"` \
	`find . -type f -name "NW*"`; do
	rm -f $f
    done
    find . -type f | xargs %{__perl} -pi -e "s|%{_builddir}/%{sourcename}|%{ap_abs_srcdir}|g"
popd

# install source
tar c -C ../tmp-%{sourcename} usr/src | tar x -C %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

make install \
	prefix=%{buildroot}%{_prefix} \
	bindir=%{buildroot}%{_bindir} \
	sbindir=%{buildroot}%{_sbindir} \
	libdir=%{buildroot}%{_libdir} \
	libexecdir=%{buildroot}%{ap_libexecdir} \
	mandir=%{buildroot}%{_mandir} \
	sysconfdir=%{buildroot}%{ap_sysconfdir} \
	includedir=%{buildroot}%{ap_includedir} \
	localstatedir=%{buildroot}/var \
	runtimedir=%{buildroot}/var/run \
	installbuilddir=%{buildroot}%{ap_installbuilddir}  \
	datadir=%{buildroot}%{ap_datadir} \
	errordir=%{buildroot}%{ap_datadir}/error \
	iconsdir=%{buildroot}%{ap_datadir}/icons \
	htdocsdir=%{buildroot}%{ap_htdocsdir} \
	manualdir=%{buildroot}%{ap_htdocsdir}/manual \
	cgidir=%{buildroot}%{ap_datadir}/cgi-bin \
	runtimedir=%{buildroot}/var/run \
	logdir=%{buildroot}%{ap_logfiledir} \
	logfiledir=%{buildroot}%{ap_logfiledir} \
	proxycachedir=%{buildroot}%{ap_proxycachedir}

pushd %{buildroot}%{_sbindir}
    rm -f suexec
popd

pushd %{buildroot}%{_mandir}/man8
    rm -f suexec.8 
popd

#Fix config_vars.mk, and add some MDK flags so all other modules 
#can simply do "apxs -q VARIABLE" and know, for example, the exact
#release of apache-devel or the exact directory where the source is
#located. 
CVMK="%{buildroot}%{ap_installbuilddir}/config_vars.mk"
%{__perl} -pi -e "s|%{_builddir}/%{sourcename}|%{ap_abs_srcdir}|g" $CVMK
%{__perl} -pi -e "s|%{buildroot}||g" $CVMK

# if the following 3 lines needs to be enabled again, use the ".*" wildcard as in
# "s|bla bla =.*|bla bla = replaced whatever text after the equal char...|g"
#%{__perl} -pi -e "s|installbuilddir =.*|installbuilddir = %{ap_installbuilddir}|g" $CVMK
#%{__perl} -pi -e "s|htdocsdir =.*|htdocsdir = %{ap_htdocsdir}|g" $CVMK
#%{__perl} -pi -e "s|logfiledir =.*|logfiledir = %{ap_logfiledir}|g" $CVMK

echo "ap_version = %{ap_version}" >> $CVMK
echo "ap_release = %{ap_release}" >> $CVMK

#########################################################################################
# fix some bugs and other stuff
#

%{__perl} -p -i -e "s|%{buildroot}||g" %{buildroot}%{_bindir}/ap*-config
%{__perl} -p -i -e "s|APU_SOURCE_DIR=.*|APU_SOURCE_DIR=\"%{ap_abs_srcdir}/srclib/apr-util\"|g" %{buildroot}%{_bindir}/apu-config
%{__perl} -p -i -e "s|APU_BUILD_DIR=.*|APU_BUILD_DIR=\"%{ap_abs_srcdir}/srclib/apr-util\"|g" %{buildroot}%{_bindir}/apu-config
%{__perl} -p -i -e "s|APR_SOURCE_DIR=.*|APR_SOURCE_DIR=\"%{ap_abs_srcdir}/srclib/apr\"|g" %{buildroot}%{_bindir}/apr-config
%{__perl} -p -i -e "s|-pthread|-lpthread|g" %{buildroot}%{_libdir}/lib*.la
%{__perl} -pi -e "s|%{_builddir}/%{sourcename}|%{ap_abs_srcdir}|g" %{buildroot}%{ap_installbuilddir}/apr_rules.mk

# OE: make the apu-config file more correct
for lib in ldap lber sasl sasl2; do
    %{__perl} -pi -e "s|-l$lib||g" %{buildroot}%{_bindir}/apu-config
done

mv %{buildroot}%{_sbindir}/envvars %{buildroot}%{ap_installbuilddir}/

##################################################################

# first tuck away the vanilla httpd*.conf file
cp %{buildroot}%{ap_prefix}/conf/highperformance.conf highperformance.conf
cp %{buildroot}%{ap_prefix}/conf/httpd2.conf httpd2-VANILLA.conf
cp %{buildroot}%{ap_prefix}/conf/ssl.conf ssl.conf
cp %{buildroot}%{ap_prefix}/conf/ssl-std.conf ssl-std.conf
cp %{buildroot}%{ap_prefix}/conf/highperformance-std.conf highperformance-std.conf
cp %{buildroot}%{ap_prefix}/conf/httpd-std.conf httpd-std.conf
rm -rf %{buildroot}%{ap_prefix}/conf

# Link with main conf dir
ln -sf ../conf %{buildroot}%{ap_prefix}/conf

# Link build dir
ln -s ../../..%{ap_installbuilddir} %{buildroot}%{ap_prefix}/build

# Apxs needs this to pickup the right lib for install
ln -sf ../../..%{_libdir} %{buildroot}%{ap_prefix}/lib

# Link log directory
ln -sf ../../..%{ap_logfiledir} %{buildroot}%{ap_prefix}/logs

# Link modules dir
ln -sf ../../..%{ap_libexecdir} %{buildroot}%{ap_prefix}/modules

# Link extra modules
ln -sf ../../..%{ap_extralibs} %{buildroot}%{ap_prefix}/extramodules

##################################################################

#Move mod_ssl.so to %{ap_extralibs}
install -d %{buildroot}%{ap_extralibs}
mv %{buildroot}%{ap_libexecdir}/mod_ssl.so %{buildroot}%{ap_extralibs}

install -d %{buildroot}%{ap_ssldir}
bzcat %{SOURCE5} > %{buildroot}%{ap_ssldir}/gentestcrt.sh

# install module conf files for the "conf.d" dir loading structure
install -d %{buildroot}/%{ap_confd}
bzcat %{SOURCE30} > %{buildroot}/%{ap_confd}/30_mod_proxy.conf
bzcat %{SOURCE40} > %{buildroot}/%{ap_confd}/40_mod_ssl.conf
bzcat %{SOURCE41} > %{buildroot}/%{ap_confd}/41_mod_ssl.default-vhost.conf
bzcat %{SOURCE45} > %{buildroot}/%{ap_confd}/45_mod_dav.conf
bzcat %{SOURCE46} > %{buildroot}/%{ap_confd}/46_mod_ldap.conf
bzcat %{SOURCE55} > %{buildroot}/%{ap_confd}/55_mod_cache.conf
bzcat %{SOURCE56} > %{buildroot}/%{ap_confd}/56_mod_disk_cache.conf
bzcat %{SOURCE57} > %{buildroot}/%{ap_confd}/57_mod_mem_cache.conf
bzcat %{SOURCE58} > %{buildroot}/%{ap_confd}/58_mod_file_cache.conf
bzcat %{SOURCE59} > %{buildroot}/%{ap_confd}/59_mod_deflate.conf

install -d %{buildroot}%{ap_sslconf}
cat > %{buildroot}%{ap_sslconf}/README.test-certificates <<EOF
Use the %{ap_ssldir}/gentestcrt.sh script to generate your own,
self-signed certificates to replace the localhost server name.
EOF

install -d %{buildroot}%{ap_davdir}

#Move mod_ldap.so and mod_auth_ldap.so to %{ap_extralibs}
mv %{buildroot}%{ap_libexecdir}/mod_ldap.so %{buildroot}%{ap_extralibs}
mv %{buildroot}%{ap_libexecdir}/mod_auth_ldap.so %{buildroot}%{ap_extralibs}

# make libtool a (dangling) symlink
ln -snf ../../../bin/libtool %{buildroot}%{ap_installbuilddir}/libtool

# we only want to provide png files...
find %{buildroot}%{ap_datadir}/icons -type f -name "*.gif" | xargs rm

# install missing files
install -m755 support/split-logfile %{buildroot}%{_sbindir}/split-logfile
install -m755 support/list_hooks.pl %{buildroot}%{_sbindir}/list_hooks.pl
install -m755 support/logresolve.pl %{buildroot}%{_sbindir}/logresolve.pl
install -m755 support/log_server_status %{buildroot}%{_sbindir}/log_server_status
install -m755 support/.libs/ab-ssl %{buildroot}%{_sbindir}/ab-ssl

cp %{SOURCE2} $RPM_BUILD_DIR/%{sourcename}

cp %{SOURCE3} $RPM_BUILD_DIR/%{sourcename}

#Put README.ADVX into %{ap_name}-devel so other packages can use it
cp %{SOURCE2} %{buildroot}/%{ap_includedir}

install -d %{buildroot}%{ap_proxycachedir}

#Fix apxs name if necessary
pushd %{buildroot}%{_sbindir}
    mv apxs %{apxs_name}
    rm -rf %{buildroot}%{ap_htdocsdir}/index*
    rm -rf %{buildroot}%{ap_htdocsdir}/apach*
    rm -rf %{buildroot}%{_sbindir}/apachectl
    rm -rf %{buildroot}%{ap_datadir}/cgi-bin/printenv
    rm -rf %{buildroot}%{ap_datadir}/cgi-bin/test-cgi
popd

# fix a msec safe cache for the ssl stuff
install -d %{buildroot}%{ap_proxycachedir}/mod_ssl
touch %{buildroot}%{ap_proxycachedir}/mod_ssl/scache.dir
touch %{buildroot}%{ap_proxycachedir}/mod_ssl/scache.pag
touch %{buildroot}%{ap_proxycachedir}/mod_ssl/scache.sem
touch %{buildroot}%{ap_proxycachedir}/mod_ssl/ssl_scache

#########################################################################################
# install phase done
#

# OE: argh!!! it took me a while to find this offending stuff...
# I _want_ to be able to provide unstripped stuff.
# Maybe EXCLUDE_FROM_STRIP="%{buildroot}/%{_sbindir}/httpd2" would have worked?

%if !%{build_debug}
#Strip everything *except httpd2* manually for now...
#JMD: there must be an easier way...
%{__strip} -s %{buildroot}/%{ap_libexecdir}/*.so
%{__strip} -s %{buildroot}/%{ap_extralibs}/*.so
%{__strip} -s %{buildroot}/%{_libdir}/*.so*
file %{buildroot}/%{_sbindir}/*|grep linked|grep -v httpd2|cut -f1 -d:| \
	xargs %{__strip} -s
%endif

mkdir -p %{buildroot}%{_srvdir}/httpd2/log
mkdir -p %{buildroot}%{_srvlogdir}/httpd2
install -m 0755 %{SOURCE7} %{buildroot}%{_srvdir}/httpd2/run
install -m 0755 %{SOURCE8} %{buildroot}%{_srvdir}/httpd2/log/run

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE60} %{buildroot}%{_datadir}/afterboot/03_apache2

# remove manual
rm -rf %{buildroot}%{ap_htdocsdir}/manual

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

#Clean up "install source" and other generated dirs
[ "../tmp-%{sourcename}%{ap_abs_srcdir}" != "/" ] && rm -rf ../tmp-%{sourcename}%{ap_abs_srcdir}
[ "../usr/src" != "/" ] && rm -rf ../usr/src
[ "../tmp-%{sourcename}" != "/" ] && rm -rf ../tmp-%{sourcename}

%post -n %{apr_name} -p /sbin/ldconfig
%postun -n %{apr_name} -p /sbin/ldconfig

%post mod_proxy
%_post_srv httpd2

%postun mod_proxy
%_post_srv httpd2

%post mod_ssl
if [ $1 = "1" ]; then 
  #Create a self-signed server key and certificate 
  #The script checks first if they exists, if yes, it exits, 
  #otherwise, it creates them.
  if [ -d %{ap_sslconf} ];then
    pushd %{ap_sslconf} > /dev/null
    yes ""|%{ap_ssldir}/gentestcrt.sh >/dev/null 
    popd > /dev/null
  fi
  %{ADVXdir}/mod_ssl-migrate-20
fi
%create_ghostfile %{ap_proxycachedir}/mod_ssl/scache.dir  apache root 0600
%create_ghostfile %{ap_proxycachedir}/mod_ssl/scache.pag  apache root 0600
%create_ghostfile %{ap_proxycachedir}/mod_ssl/scache.sem  apache root 0600
%create_ghostfile %{ap_proxycachedir}/mod_ssl/ssl_scache  apache root 0600
%_post_srv httpd2

%postun mod_ssl
%_post_srv httpd2

%post mod_dav
%_post_srv httpd2

%postun mod_dav
%_post_srv httpd2

%post mod_ldap
%_post_srv httpd2

%postun mod_ldap
%_post_srv httpd2

%post mod_cache
%_post_srv httpd2

%postun mod_cache
%_post_srv httpd2

%post mod_disk_cache
%_post_srv httpd2

%postun mod_disk_cache
%_post_srv httpd2

%post mod_mem_cache
%_post_srv httpd2

%postun mod_mem_cache
%_post_srv httpd2

%post mod_file_cache
%_post_srv httpd2

%postun mod_file_cache
%_post_srv httpd2

%post mod_deflate
%_post_srv httpd2

%postun mod_deflate
%_post_srv httpd2

%post devel -p /sbin/ldconfig
%preun devel -p /sbin/ldconfig

%pre common
%_pre_useradd apache %{ap_datadir} /bin/sh 74

%postun common
%_postun_userdel apache

%post modules
%_post_srv httpd2

%post
#JMD: do *not* use _post_service here, it is used in %{ap_name}-conf, since we
#can have both %{ap_name} and %{ap_name}-mod_perl
%_mkafterboot
%_post_srv httpd2

%postun
#JMD: do *not* use _post_service here, otherwise it will uninstall
#apache-mod_perl as well!!
%_mkafterboot
%_post_srv httpd2

%files
%defattr(-,root,root)
%doc highperformance.conf
%doc httpd2-VANILLA.conf
%doc ssl.conf
%doc ssl-std.conf
%doc highperformance-std.conf
%doc httpd-std.conf
%doc apache-old-changelog
%{_sbindir}/%{ap_progname}
%dir %{_srvdir}/httpd2
%dir %{_srvdir}/httpd2/log
%{_srvdir}/httpd2/run
%{_srvdir}/httpd2/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/httpd2
%{_datadir}/afterboot/03_apache2

%files modules
#Do not put apache.apache here, otherwise anyone with web access can 
#tamper with the files!!!!
%defattr(-,root,root)
%doc modules/README*
%dir %{ap_libexecdir}
%{ap_libexecdir}/mod_access.so
%{ap_libexecdir}/mod_actions.so
%{ap_libexecdir}/mod_alias.so
%{ap_libexecdir}/mod_asis.so
%{ap_libexecdir}/mod_auth.so
%{ap_libexecdir}/mod_auth_anon.so
%{ap_libexecdir}/mod_auth_dbm.so
%{ap_libexecdir}/mod_auth_digest.so
%{ap_libexecdir}/mod_autoindex.so
%{ap_libexecdir}/mod_case_filter.so
%{ap_libexecdir}/mod_case_filter_in.so
%{ap_libexecdir}/mod_cern_meta.so
%{ap_libexecdir}/mod_cgi.so
%{ap_libexecdir}/mod_cgid.so
%{ap_libexecdir}/mod_charset_lite.so
%{ap_libexecdir}/mod_dir.so
%{ap_libexecdir}/mod_env.so
%{ap_libexecdir}/mod_expires.so
%{ap_libexecdir}/mod_ext_filter.so
%{ap_libexecdir}/mod_headers.so
%{ap_libexecdir}/mod_imap.so
%{ap_libexecdir}/mod_include.so
%{ap_libexecdir}/mod_info.so
%{ap_libexecdir}/mod_log_config.so
%{ap_libexecdir}/mod_logio.so
%{ap_libexecdir}/mod_mime.so
%{ap_libexecdir}/mod_mime_magic.so
%{ap_libexecdir}/mod_negotiation.so
%{ap_libexecdir}/mod_rewrite.so
%{ap_libexecdir}/mod_setenvif.so
%{ap_libexecdir}/mod_speling.so
%{ap_libexecdir}/mod_status.so
%{ap_libexecdir}/mod_unique_id.so
%{ap_libexecdir}/mod_userdir.so
%{ap_libexecdir}/mod_usertrack.so
%{ap_libexecdir}/mod_vhost_alias.so
%{ap_libexecdir}/*.exp
%dir %{ap_extralibs}
%dir %{ap_prefix}
%exclude %{ap_prefix}/build/
%{ap_prefix}/*

%files mod_proxy
%defattr(-,root,root)
%doc modules/proxy/CHANGES
%config(noreplace) %{ap_confd}/*_mod_proxy.conf
%{ap_libexecdir}/mod_proxy_connect.so
%{ap_libexecdir}/mod_proxy_ftp.so
%{ap_libexecdir}/mod_proxy_http.so
%{ap_libexecdir}/mod_proxy.so
%attr(0770,root,apache) %dir %{ap_proxycachedir}

%files mod_ssl
%defattr(-,root,root)
%{_sbindir}/ab-ssl
%{ap_extralibs}/mod_ssl.so
%doc modules/ssl/README
%config(noreplace) %{ap_confd}/*_mod_ssl.conf
%config(noreplace) %{ap_confd}/*_mod_ssl.default-vhost.conf
%config(noreplace) %{ap_sslconf}/README*
%dir %{ap_ssldir}
%attr(0755,root,root) %{ap_ssldir}/gentestcrt.sh
##JMD: Not yet, conflicts with the old mod_ssl
##%dir %{ap_sslconf}
%attr(0700,apache,root) %dir %{ap_proxycachedir}/mod_ssl
%attr(0600,apache,root) %ghost %{ap_proxycachedir}/mod_ssl/scache.dir
%attr(0600,apache,root) %ghost %{ap_proxycachedir}/mod_ssl/scache.pag
%attr(0600,apache,root) %ghost %{ap_proxycachedir}/mod_ssl/scache.sem
%attr(0600,apache,root) %ghost %{ap_proxycachedir}/mod_ssl/ssl_scache

%files mod_dav
%defattr(-,root,root)
%attr(-,apache,apache) %dir %{ap_davdir}
%config(noreplace) %{ap_confd}/*_mod_dav.conf
%{ap_libexecdir}/mod_dav.so
%{ap_libexecdir}/mod_dav_fs.so

%files mod_ldap
%defattr(-,root,root)
%{ap_extralibs}/mod_ldap.so
%{ap_extralibs}/mod_auth_ldap.so
%config(noreplace) %{ap_confd}/*_mod_ldap.conf

%files mod_cache
%defattr(-,root,root)
%config(noreplace) %{ap_confd}/*_mod_cache.conf
%{ap_libexecdir}/mod_cache.so

%files mod_disk_cache
%defattr(-,root,root)
%config(noreplace) %{ap_confd}/*_mod_disk_cache.conf
%{ap_libexecdir}/mod_disk_cache.so

%files mod_mem_cache
%defattr(-,root,root)
%config(noreplace) %{ap_confd}/*_mod_mem_cache.conf
%{ap_libexecdir}/mod_mem_cache.so

%files mod_file_cache
%defattr(-,root,root)
%config(noreplace) %{ap_confd}/*_mod_file_cache.conf
%{ap_libexecdir}/mod_file_cache.so

%files mod_deflate
%defattr(-,root,root)
%config(noreplace) %{ap_confd}/*_mod_deflate.conf
%{ap_libexecdir}/mod_deflate.so

%files common
#Do not put apache.apache for the rest, otherwise anyone with web access can 
#tamper with the files!!!!
%defattr(-,root,root)
%doc README.ADVX
%dir %{ap_datadir}/error
%dir %{ap_datadir}/error/include
%config(noreplace,missingok) %{ap_datadir}/error/README
%config(noreplace,missingok) %{ap_datadir}/error/*.var
%config(noreplace,missingok) %{ap_datadir}/error/include/*.html
%{ap_datadir}/icons/README*
%{ap_datadir}/icons/*.png
%{ap_datadir}/icons/small/README*
%{ap_datadir}/icons/small/*.png
%{_mandir}/*/*
%attr(0755,root,root) %{_sbindir}/ab
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
#JMD: Removed for Apache2 since mm is not used anymore
#Maybe we'll add it again someday.
#(By the way, 1333 is the *right* permission.)
#%attr(1333,apache,apache) %dir /var/apache-mm

%files -n %{apr_name}
#Do not put apache.apache here, otherwise anyone with web access can 
#tamper with the files!!!!
%defattr(-,root,root)
%doc srclib/apr/CHANGES srclib/apr/README*
%attr(0755,root,root) %{_libdir}/libapr-*.so.*
%attr(0755,root,root) %{_libdir}/libaprutil-*.so.*

%files devel
#Do not put apache.apache here, otherwise anyone with web access can 
#tamper with the files!!!!
%defattr(-,root,root)
%{ap_includedir}
%attr(0755,root,root) %dir %{ap_installbuilddir}
%attr(0755,root,root) %dir %{ap_prefix}/build
%attr(0644,root,root) %{ap_installbuilddir}/*.mk
%attr(0755,root,root) %{ap_installbuilddir}/*.sh
%attr(0755,root,root) %{ap_installbuilddir}/envvars
%attr(0755,root,root) %{ap_installbuilddir}/libtool
%attr(0755,root,root) %{ap_installbuilddir}/config.nice
%attr(0755,root,root) %{_sbindir}/envvars-std
%{apxs}
%doc srclib/apr/CHANGES srclib/apr/README* srclib/apr/docs/*
%attr(0755,root,root) %{_bindir}/ap*-config
%attr(0644,root,root) %{_libdir}/*.exp
%attr(0755,root,root) %{_libdir}/libapr-*.so
%attr(0755,root,root) %{_libdir}/libapr-*.la
%attr(0755,root,root) %{_libdir}/libapr-*.a
%attr(0755,root,root) %{_libdir}/libaprutil-*.a
%attr(0755,root,root) %{_libdir}/libaprutil-*.la
%attr(0755,root,root) %{_libdir}/libaprutil-*.so

%files source
#Do not put apache.apache here, otherwise anyone with web access can 
#tamper with the files!!!!
%defattr(-,root,root)
%{ap_abs_srcdir}

%changelog
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

