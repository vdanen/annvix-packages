#
# spec file for package php
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		php
%define version		4.4.2
%define release		%_revrel
%define epoch		2

%define libversion	4
%define libname		%mklibname php_common %{libversion}

%define phpdir		%{_libdir}/php
%define	peardir		%{_datadir}/pear
%define	phpsrcdir	%{_usrsrc}/php-devel

%global harden          1
%{?_without_harden:     %global harden 0}

%define _requires_exceptions BEGIN\\|mkinstalldirs

%define build_debug 	0

%{?_with_debug: %{expand: %%define build_debug 1}}

%if %{build_debug}
# disable build root strip policy
%define __spec_install_post %{_prefix}/lib/rpm/brp-compress || :

# This gives extra debuggin and huge binaries
%{expand:%%define optflags %{optflags} %([ ! $DEBUG ] && echo '-g3')}
%endif

Summary:	The PHP4 scripting language
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	PHP License
Group:		Development/Other
URL:		http://www.php.net
Source0:	http://static.php.net/www.php.net/distributions/php-%{version}.tar.bz2
Source3:	FAQ.php
Source4:	php-4.3.10-php-test
Patch0:		php-4.3.0-mdk-init.patch
Patch1:		php-4.3.6-mdk-shared.patch
Patch2:		php-4.3.0-mdk-imap.patch
Patch4:		php-4.3.4RC3-mdk-64bit.patch
Patch5:		php-4.4.2-avx-lib64.patch
Patch7:		php-4.3.11-mdk-libtool.patch
Patch9:		php-4.3.11-mdk-no_egg.patch
Patch10:	php-4.4.0RC1-mdk-phpize.diff
Patch11:	php-4.4.0RC2-mdk-run-tests.diff
# from PLD (20-40)
Patch20:	php-4.3.0-pld-mail.patch
Patch21:	php-4.3.10-pld-mcal-shared-lib.patch
Patch22:	php-4.3.6-pld-msession-shared-lib.patch
Patch23:	php-4.3.11-pld-cpdf-fix.patch
Patch24:	php-4.3.11-pld-db-shared.patch
Patch25:	php-4.3.0-pld-hyperwave-fix.patch
Patch27:	php-4.3.3RC3-pld-sybase-fix.patch
Patch28:	php-4.3.0-pld-wddx-fix.patch
Patch29:	php-4.3.0-pld-xmlrpc-fix.patch
# from Fedora (50-60)
Patch50:	php-4.3.6-rh-dlopen.patch
Patch51:	php-4.2.1-fdr-ldap-TSRM.patch
Patch52:	php-4.2.2-fdr-cxx.patch
Patch53:	php-4.3.2-fdr-libtool15.patch
Patch54:	php-4.3.1-fdr-odbc.patch
Patch56:	php-4.3.10-fdr-umask.patch
# General fixes (70+)
# make the tests work better
Patch70:	php-4.3.3-mdk-make_those_darn_tests_work.patch
# Bug fixes:
Patch71:	php-4.3.4-mdk-bug-22414.patch
# http://www.hardened-php.net/
Patch100:	http://www.hardened-php.net/hardening-patch-4.4.2-0.4.12.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
# this is to prevent that it will build against old libs
BuildConflicts:	%{libname}
BuildConflicts:	php_common
BuildConflicts:	php-devel
# Those two modules have tests that fail
BuildConflicts:	php-mhash
BuildConflicts:	php-mbstring
BuildRequires:	chrpath >= 0.12
BuildRequires:	bison
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	openssl-devel >= 0.9.6, openssl >= 0.9.6
BuildRequires:	pam-devel
BuildRequires:	zlib-devel
BuildRequires:	multiarch-utils >= 1.0.3, automake1.7

%description
PHP4 is an HTML-embeddable scripting language.  PHP offers built-in database
integration for several commercial and non-commercial database management
systems, so writing a database-enabled script with PHP is fairly simple.  The
most common use of PHP coding is probably as a replacement for CGI scripts.

You can build %{name} with some conditional build swithes;

(ie. use with rpm --rebuild):
--with debug   Compile with debugging code


%package cli
Summary:	Command-line interface to PHP
Epoch:		%{epoch}
Group:		Development/Other
URL:		http://php.net
PreReq:		php-ini
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	php
Provides:	php3
Provides:	php4
Provides:	php%{libversion} 
Obsoletes:	php
Obsoletes:	php3

%description cli
PHP4 is an HTML-embeddable scripting language.  PHP offers built-in database
integration for several commercial and non-commercial database management
systems, so writing a database-enabled script with PHP is fairly simple.  The
most common use of PHP coding is probably as a replacement for CGI scripts.

This package contains a command-line (CLI) version of php. You must also
install libphp_common. 

If you need apache module support, you also need to install the mod_php
package.


%package cgi
Summary:	CGI interface to PHP
Epoch:		%{epoch}
Group:		Development/Other
URL:		http://php.net
PreReq:		php-ini
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	php
Provides:	php3
Provides:	php4
Provides:	php%{libversion}
Obsoletes:	php
Obsoletes:	php3

%description cgi
PHP4 is an HTML-embeddable scripting language.  PHP offers built-in database
integration for several commercial and non-commercial database management
systems, so writing a database-enabled script with PHP is fairly simple.  The
most common use of PHP coding is probably as a replacement for CGI scripts.

This package contains a standalone (CGI) version of php. You must also
install libphp_common. 

If you need apache module support, you also need to install the mod_php
package.


%package -n %{libname}
Summary:	Shared library for php
Epoch:		%{epoch}
Group:		Development/Other
URL:		http://www.php.net
Provides:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	libphp_common = %{version}-%{release}
Provides:	php-common

%description -n	%{libname}
This package provides the common files to run with different
implementations of PHP. You need this package if you install the php
standalone package or a webserver with php support (ie: mod_php).

%package -n php%{libversion}-devel
Summary:	Development package for PHP4
Epoch:		%{epoch}
Group:		Development/C
URL:		http://www.php.net
Provides:	libphp_common-devel = %{version}-%{release}
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Requires:	autoconf2.5
Requires:	automake1.7
Requires:	bison
Requires:	byacc
Requires:	chrpath >= 0.12
Requires:	flex
Requires:	gettext-devel
Requires:	libtool
Requires:	openssl-devel >= 0.9.6
Requires:	pam-devel
Requires:	php-cli = %{epoch}:%{version}-%{release}
Requires:	zlib-devel
Provides:	php-devel
Obsoletes:	php-devel

%description -n	php%{libversion}-devel
The php-devel package lets you compile dynamic extensions to PHP4. Included
here is the source for the php extensions. Instead of recompiling the whole
php binary to add support for, say, oracle, install this package and use the
new self-contained extensions support. For more information, read the file
SELF-CONTAINED-EXTENSIONS.


%prep
%setup -q -n php-%{version}
%patch0 -p1 -b .init
%patch1 -p1 -b .shared

# fix soname (libversion)
perl -pi -e "s|_PHP_SONAME_|%{libversion}|g" Makefile.global

%patch2 -p0 -b .imap
%patch4 -p1
%patch5 -p1
%patch7 -p0 -b .libtool
%patch9 -p1
%patch10 -p1 -b .phpize
%patch11 -p0
# from PLD
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p0
%patch24 -p0
%patch25 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
# from Fedora
%patch50 -p0 -b .dlopen
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch56 -p1
#
%patch70 -p0 -b .make_those_darn_tests_work
%patch71 -p1 -b .22414
%if %{harden}
%patch100 -p1 -b .hardened
%endif

# Change perms otherwise rpm would get fooled while finding requires
chmod 0644 tests/lang/*.inc
chmod 0644 ext/interbase/tests/*.inc

cp Zend/LICENSE Zend/ZEND_LICENSE
mv README.SELF-CONTAINED-EXTENSIONS SELF-CONTAINED-EXTENSIONS

rm -f ext/tokenizer/EXPERIMENTAL
rm -f ext/w32api/EXPERIMENTAL
rm -f ext/dio/EXPERIMENTAL
rm -f ext/mime_magic/EXPERIMENTAL
rm -f ext/fribidi/EXPERIMENTAL
rm -f ext/mysql/libmysql/dll.c
rm -f ext/sysvmsg/EXPERIMENTAL

mkdir -p php-devel/extensions
mkdir -p php-devel/sapi
mkdir -p php-devel/pear

# Install test files in php-devel
mkdir -p php-devel/pear/Console
cp -a pear/Console/tests php-devel/pear/Console
cp -a tests php-devel

cp -dpR ext/* php-devel/extensions/
rm -f php-devel/extensions/informix/stub.c
rm -f php-devel/extensions/standard/.deps
rm -f php-devel/extensions/skeleton/EXPERIMENTAL
rm -f php-devel/extensions/ncurses/EXPERIMENTAL

# don't ship MS Windows source
rm -rf php-devel/extensions/com
rm -rf php-devel/extensions/dotnet
rm -rf php-devel/extensions/printer
rm -rf php-devel/extensions/w32api

# likewise with these:
find php-devel -name "*.dsp" | xargs rm
find php-devel -name "*.mak" | xargs rm

cp -dpR sapi/* php-devel/sapi/ 
rm -f php-devel/sapi/thttpd/stub.c
rm -f php-devel/sapi/cgi/php.sym
rm -f php-devel/sapi/fastcgi/php.sym
rm -f php-devel/sapi/pi3web/php.sym

cat %{SOURCE3} > php-devel/PHP_FAQ.php

cat > php-devel/buildext <<EOF
#!/bin/bash
gcc -Wall -fPIC -shared %{optflags} \\
    -I. \`%{_bindir}/php-config --includes\` \\
    -I%{_includedir}/freetype \\
    -I%{_includedir}/openssl \\
    -I%{phpsrcdir}/ext \\
    -I%{_includedir}/\$1 \\
    \$4 \$2 -o \$1.so \$3 -lc
EOF

chmod 0755 php-devel/buildext


%build
# this _has_ to be executed!
#./buildconf --force
export WANT_AUTOCONF_2_5=1
rm -f configure; aclocal-1.7 && autoconf --force && autoheader

%serverbuild

#For eventual compatibility with RedHat
#%{!?nokerberos:krb5libs="-L%{_prefix}/kerberos/lib -lgssapi_krb5 -lkrb5 -lk5crypto -lcom_err"}

#LIBS="$LIBS -lpthread $krb5libs"; export LIBS
#LIBS="$LIBS $krb5libs"; export LIBS
export oldstyleextdir=yes
export EXTENSION_DIR="%{phpdir}/extensions"
export PROG_SENDMAIL="%{_sbindir}/sendmail"
export CFLAGS="%{optflags} -fPIC -L%{_libdir}"

# define the array of extensions not being built in (only the most common)
%define external_modules mysql pgsql gd imap ldap bcmath bz2 calendar curl db dba dbase dbx dio domxml exif filepro gmp iconv mbstring mcal mime_magic ming odbc overload pcntl pspell qtdom readline recode shmop sockets sybase sybase_ct sysvmsg tokenizer wddx xml xmlrpc xslt

#DO NOT PUT THESE EXTENSIONS AS EXTERNAL:
# Here are reasons for each extension
# 1) Extension not require any external library except libc.so and ld-linux.so
#    plus zlib (needed by hundreds of packages, including rpm itself.
# 2) Extension contains features needed by many common scripts
# 3) Extension is needed for compliance with POSIX standards
# 4) Extension provides functionality needed by some important customers
# 5) Extension is built by default on most platforms
# 6) Extension was built into previous PHP versions and is kept here for
#    compatibility purposes
# - ftp [1] [4] [6] 
# - posix [1] [3] [5] [6]
# - session [1] [2] [4] [5] [6]
# - sysvsem [1] [3] [6]
# - sysvshm [1] [3] [6]
# - yp [1] [3] [4] [6] 
# - zlib [1] [2] [4(Including MandrakeExpert)] [6]
# - pcre [1] [5]
# - gettext [2] [4] [6]
# - ctype [1] [2] [5]
# Openssl was added to have https:// support with fopen.

echo "#define EXTERNAL_MANDRAKE_MODULES \"%{external_modules}\"" >> ext/standard/info.h

cat > Readme1st <<EOF
- Install the mod_php package to get Apache support
- Install php-[extension].rpm packages to get a specific extension

Here follows a list of extensions not been compiled into the main
php package, but that can be installed as external modules:

`for i in %{external_modules}; do echo php-${i}; done`

EOF

# Configure php

%configure2_5x \
    --enable-discard-path \
    --disable-force-cgi-redirect \
    --enable-shared \
    --disable-static \
    --disable-debug \
    --disable-rpath \
    --enable-pic \
    --enable-inline-optimization \
    --enable-memory-limit \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --with-pear=%{peardir} \
    --enable-magic-quotes \
%if %{build_debug}
    --enable-maintainer-mode \
    --enable-debug \
%endif
    --enable-debugger \
    --enable-track-vars \
    --with-exec-dir=%{_bindir} \
    --with-versioning \
    --with-mod_charset \
    --with-regex=php \
    --enable-track-vars \
    --enable-trans-sid \
    --enable-safe-mode \
    --enable-ctype \
    --enable-ftp \
    --with-gettext=%{_prefix} \
    --enable-posix \
    --enable-session \
    --enable-sysvsem \
    --enable-sysvshm \
    --enable-yp \
    --with-openssl=%{_prefix} \
    --without-kerberos \
    --with-ttf \
    --with-freetype-dir=%{_prefix} \
    --with-zlib=%{_prefix} \
    --with-zlib=%{_prefix} \
    --with-zlib-dir=%{_prefix} \
    --without-dba \
    `for i in %{external_modules}; do echo --without-${i} --disable-${i}; done` \
    --without-ndbm \
    --without-db2 \
    --without-db3 \
    --without-db4 \
    --without-dbm \
    --without-cdb \
    --without-flatfile \
    --without-inifile \
    --without-gdbm \
    --without-pear

###	This configuration makes a dependency on those libs:
#	-ldl -lpam -lcrypt -lresolv -lm -lz

# remove all confusion...
perl -pi -e "s|^#define CONFIGURE_COMMAND .*|#define CONFIGURE_COMMAND \"This is irrelevant, look inside the %{_docdir}/%{name}-%{version}/configure_command file. urpmi is your friend, use it to install extensions not shown below.\"|g" main/build-defs.h
cp config.nice configure_command; chmod 644 configure_command

%make

chrpath -d sapi/cli/php
chrpath -d sapi/cgi/php


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# OE: make this somewhat short-circuitable
if ! [ -f libphp_common.so.%{libversion} ]; then
    cp libphp_common.so libphp_common.so.%{libversion}
    ln -snf libphp_common.so.%{libversion} libphp_common.so
fi

export LD_LIBRARY_PATH="."
export INSTALL_ROOT="%{buildroot}"
export PHP_PEAR_INSTALL_DIR="%{peardir}"

#Do a make test
export PHPRC="."
export NO_INTERACTION=1
export REPORT_EXIT_STATUS=1

# OE: Tue May 27 2003
# Make a php.ini file for testing..., if not the tests 
# will fail. P30 and this one is the way to go...
# OE: Wed Aug 27 2003
# php will use the php.ini in current dir, so there's no
# need to hardcode the path in P30, the php folks claim 
# it's a feature not a bug..., oh well...

cat > php.ini <<EOF
; This file was used when running "make test" at rpm build time by
; %{packager} at `date`.
;
; You need to ask root set some reasonable values for shared memory
; for the session and semaphore tests to work, maybe something like
; this:
; echo "33554432" > /proc/sys/kernel/shmmax
; echo "4096" > /proc/sys/kernel/shmmni
; echo "300 90000 100 150" > /proc/sys/kernel/sem

[PHP]

open_basedir=
safe_mode=0
output_buffering=0
output_handler=0
magic_quotes_runtime=
extensions_dir=

[Session]
; We use this as the saved files is cleaned by the rpm build 
; process. (but not with php-test, yet...)
session.save_path="."

EOF

# tuck away the php.ini file used for the test, it may come handy(?)
cp php.ini php-devel/

# FIXME: The following tests (except 021) are known to fail on 64-bit
# architectures
%ifarch x86_64
disable_tests="ext/session/tests/019.phpt \
    ext/session/tests/021.phpt \
    ext/standard/tests/math/pow.phpt \
    ext/standard/tests/math/round.phpt \
    ext/standard/tests/math/abs.phpt "
%endif

[[ -n "$disable_tests" ]] && \
for f in $disable_tests; do
    [[ -f "$f" ]] && mv $f $f.disabled
done

make test
make install

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{phpsrcdir}
install -d %{buildroot}%{_mandir}/man1

install -m 0755 libphp_common.so.%{libversion} %{buildroot}%{_libdir}/
ln -snf libphp_common.so.%{libversion} %{buildroot}%{_libdir}/libphp_common.so

install -m 0755 sapi/cli/php %{buildroot}%{_bindir}/php
install -m 0755 sapi/cgi/php %{buildroot}%{_bindir}/php-cgi

cat %{SOURCE4} > %{buildroot}%{_bindir}/php-test
cp -dpR php-devel/* %{buildroot}%{phpsrcdir}/
install -m 0644 run-tests*.php %{buildroot}%{phpsrcdir}/
install -m 0644 main/internal_functions.c %{buildroot}%{phpsrcdir}/

ln -snf extensions %{buildroot}%{phpsrcdir}/ext

# house cleaning
rm -rf %{buildroot}%{peardir}
rm -f %{buildroot}%{_bindir}/pear

# make libtool a (dangling) symlink
ln -snf ../../../bin/libtool %{buildroot}%{phpdir}/build/libtool

# install the man page
install -m 0644 sapi/cli/php.1 %{buildroot}%{_mandir}/man1/

%multiarch_includes %{buildroot}%{_includedir}/php/main/build-defs.h
%multiarch_includes %{buildroot}%{_includedir}/php/main/php_config.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%pre cgi
update-alternatives --remove php %{_bindir}/php-cgi
update-alternatives --remove php %{_bindir}/php-cli

%pre cli
update-alternatives --remove php %{_bindir}/php-cgi
update-alternatives --remove php %{_bindir}/php-cli


%files cgi
%defattr(-,root,root)
%doc Readme1st
%attr(0755,root,root) %{_bindir}/php-cgi

%files cli
%defattr(-,root,root)
%doc Readme1st
%attr(0755,root,root) %{_bindir}/php
%attr(0644,root,root) %{_mandir}/man1/php.1*

%files -n %{libname}
%defattr(-,root,root)
%doc CREDITS INSTALL LICENSE NEWS Zend/ZEND_LICENSE php.ini-dist php.ini-recommended configure_command
%doc Changelog.secfix
%attr(0755,root,root) %{_libdir}/libphp_common.so.%{libversion}

%files -n php%{libversion}-devel
%defattr(-,root,root)
%doc SELF-CONTAINED-EXTENSIONS CODING_STANDARDS README.* TODO EXTENSIONS configure_command
%doc Zend/ZEND_*
%attr(0755,root,root) %{_bindir}/php-config
%attr(0755,root,root) %{_bindir}/phpize
%attr(0755,root,root) %{_bindir}/php-test
%attr(0755,root,root) %{_libdir}/libphp_common.so
%dir %{phpdir}/build
%{phpdir}/build/*
%{phpsrcdir}
%multiarch %{multiarch_includedir}/php/main/build-defs.h
%multiarch %{multiarch_includedir}/php/main/php_config.h
%{_includedir}/php
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/phpize.1*


%changelog
* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org>
- hardening patch 0.4.12: fixes CVE-2006-2563, CVE-2006-2660,
  CVE-2006-1990, CVE-2006-3011

* Mon May 08 2006 Vincent Danen <vdanen-at-build.annvix.org>
- P72: security fixes from hardened-php.net for the security fixes
  found in 5.1.3/5.1.4

* Wed Jan 18 2006 Vincent Danen <vdanen-at-build.annvix.org>
- 4.4.2
- hardening patch 0.4.8 for php 4.4.2
- rediffed P5
- dropped P6; doesn't look like it's needed any longer
- dropped P12; fixed upstream
- add a --without harden option to build without the hardening patch;
  the default is to build with it

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Tue Dec 13 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.41-2avx
- P12: fix php bug #35067; should fix a squirrelmail issue
- don't bzip patches or unnecessary source files anymore

* Wed Nov 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.41-1avx
- 4.4.1; fixes several security issues (see http://www.php.net/release_4_4_1.php)
- hardening patch 4.4.1-0.4.5

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.40-2avx
- hardening patch 4.4.0-0.4.3

* Wed Sep 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.40-1avx
- 4.4.0
- P100: re-introduce the hardened php stuff (4.4.0-0.4.1)
- rediffed P5, P10, P11 from Mandriva

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-2avx
- rebuild

* Sat May 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-1avx
- 4.3.11: security fixes for CAN-2005-0524, CAN-2005-0525, CAN-2005-1042,
  and CAN-2005-1043
- rediffed patches P5, P7, P9, P10, P23, P24 from Mandriva

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-5avx
- rebuild against new libxml2 and libxslt
- enable multiarch stuff

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-4avx
- drop P3 and P8
- drop the hardened-php patch; for one it breaks compatibility with external
  3rd party products (like Zend) and for another including it in the build is
  against the php license
- enable building with -fstack-protector

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-3avx
- rebuild against latest openssl

* Fri Dec 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-2avx
- include the hardened-php patch (4.3.10-0.2.4)
- drop P55
- drop S5 as it's redundant
- rename S4
- use the lib64 patch from mandrake (P5)
- rediff P21

* Thu Dec 16 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-1avx
- 4.3.10
- rediff P5, P55, P56
- drop P26

* Wed Sep 29 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.9-1avx
- 4.3.9
- rediff P5, P9, P10
- drop P57, P58, P72 (applied upstream)

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-2avx
- P72: fix anthill #965; patch from CVS

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-1avx
- 4.3.8; security fix for CAN-2004-0594 and CAN-2004-0595
- remove %%build_propolice macro
- enforce new patch-naming policy
- sync with 4.3.7-5mdk:
  - remove the ADVXpackage provides (oden)
  - sync with fedora (P57, P58) (4.3.7-3) (oden)
  - fix deps
  - add P11 (fixes one minor annoyance while running the tests) (oden)
  - add P56 (fedora) (oden)
  - nuke some patch -b backups as they pollute the -devel package (oden)
  - rediffed P5, P21, P22 (oden)
  - added P23-P29 from PLD, slightly adjusted (oden)
  - added P21-P25 from fedora (oden)
  - use the %%configure2_5x macro (oden)
  - added P10 to make phpize work (oden)
  - move scandir to /etc/php.d (oden)
  - rediffed P1 and P20 (oden)
  - drop P40, it's included (oden)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- 4.3.7

* Tue Apr 13 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- 4.3.6
- more epoch fixes
- don't build with %%debug by default
- fix bug22414.phpbt (jmd)
- rediff P1, P20 (oden)
- spec cleanups/macros/etc. (oden)
- libversion is 4, not 432
- remove some unneeded BuildConflicts, Obsoletes, and Provides

* Tue Apr 13 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-5sls
- fix epoch in requires

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-4sls
- minor spec cleanups

* Fri Jan 09 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-3sls
- rediff P5; fix lib64 build (aka php-dba_bundle wasn't compiling)

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec
- use %%build_propolice to add -fno-stack-protector until we can sort out
  the build problems with __guard/etc. symbols

* Tue Nov 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- 4.3.4

* Wed Oct 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-0.1mdk
- 4.3.4RC3
- rediff P1, P4 & P5
- had to use --without-pear
- use _requires_exceptions magic to filter out some weirdness

* Wed Aug 27 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-2mdk
- php-devel should require openssl-devel (buchan?)
- drop php-killrpath (S1), use chrpath instead
- do not own certain directories (php-devel)
- fixed the make test stuff again
- fix the configure string as for example sysconfdir was unset (wrong)

* Mon Aug 25 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- 4.3.3
- rediffed P5 & P30
- fixed the EXTERNAL_MANDRAKE_MODULES array
- new S5

* Wed Aug 20 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3.2-10mdk
- Fix lib64 patch for phpize
- Provides: libphp_common{,-devel} more convenient for compares

* Thu Aug 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3.2-9mdk
- Dependencies clean-ups, lib64 & libtool fixes

* Mon Jul 21 2003 David BAUDENS <baudens@mandrakesoft.com> 4.3.2-8mdk
- Rebuild to fix Bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-7mdk
- rebuild

* Thu Jun 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-6mdk
- fix a faulty symlink

* Wed Jun 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-5mdk
- really apply P20
- put session.save_path in current dir so that it will be cleaned in %%clean

* Wed Jun 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-4mdk
- require openssl to have the make test work as pointed out 
  by Stefan van der Eijk 
- added P20 from rh rawhide
- added php-cli man page
- misc spec file fixes

* Mon Jun 02 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-3mdk
- third try..., php430 was installed and linked against..., duh!
- added adodb & mmcache to the extensions array
- added apd cybercash, cybermut, cyrus, mono, mqseries, netools,
  python spplus & spread to the extensions array (possible upcoming
  stuff)

* Sat May 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-2mdk
- second try...

* Sat May 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- change libversion to 432 since 430 is not binary compatible with 432
- fix P1
- increase epoch
- Obsoletes libphp_common430-devel
- Provides libphp_common430-devel = 4.3.0-%{release}

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- 4.3.2
- added S4
- use epoch as pointed out by warly (thanks man!).
- misc spec file fixes

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-0.3mdk
- revert back again... someone needs to delete the offending packages,
  otherwise we're stucked using 14mdk, 15mdk, etc.

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-0.2mdk
- have to stick with the old versioning for now...

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-0.1mdk
- 4.3.2RC4
- drop P7, P8 & P11, it's incuded upstream
- new P1 & P2
- new P14 from PLD
- deactivated P20 (it's incuded upstream?, J-M?)
- added P30 + spec file magic to make the tests work
- misc spec file fixes

* Wed May 07 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-13mdk
- really require libopenssl0.9.7 and not libopenssl0 as pointed
  out by J.A. Magallon

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-12mdk
- require libopenssl0.9.7 and not libopenssl0

* Thu Mar 06  2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.1-11mdk
- fix showstopper bugs in streams, openssl, file and passthru functions
- add make test **** 270 tests total! ****
- add /usr/bin/php-test to the -devel package. This way, QA only has to run
  a single command to see if every module works .
- Bug #22414 (passthru command not working) VERY IMPORTANT ONE!
- Bug #21131 (fopen with 'a+' and rewind() doesn't work)
- Bug #21713 (include remote files leaks temporary files + descriptors)
- Bug #21185 (move_uploaded_file() does not ignore open_basedir)
- Bug #22362 (fwrite(), fread() and fseek() produce unexpected results)
- Bug #21986 (openssl test failure).
- Bug #22383 (getcvs not handling quoting correctly)

* Mon Mar 03  2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.1-10mdk
- add Obsoletes: php-devel so we don't remove that package when doing an
  upgrade.

* Mon Feb 17 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.1-9mdk
- 4.3.1 security release (within a few minutes of the announce!)
- get rid of the update-alternative scheme and use /usr/bin/php for the
  command line interface, as is now the convention. It will maybe break
  a couple of setups, but with all the fuss with this security release, 
  it's the right thing to do.
- keep -9mdk so we don't have to change libversion and recompile everything

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-8mdk
- use %%mklibname
- add BuildConflicts %{libname} since it tries to link with a previous version
  of itself.

* Fri Jan 17 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-7mdk
- re-add ctype, since it's enabled by default since php 4.2.0, does not use
  any external library besides glibc,  and several scripts depend on these 
  functions.

* Wed Jan 15 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-6mdk
- merged unofficial rpm releases up to 6mdk (my packages)
- rebuilt against openssl-0.9.7
- added P9, P10 & P11 (packager credits, no eastern egg and jmdaults
  scandir patch)
- added apache2 fix from CVS (P8) (php bugs: #21045 & #17098)
- added ctype, overload, imagick, pam_auth smbauth, tokenizer and rrdtool
  to the EXTENSIONS HACK, this prevents for example ctype, overload and
  tokenizer to be built in. 
- enable build with debugging code, used ideas from my apache2 package
- fix the buildext script
- remove aspell from spec file (it's gone)
- ignore all MS stuff (don't ship it, duh!)
- added P7 (db4 support from CVS) Yihaa!
- misc spec file fixes

* Tue Jan 07 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-2mdk
- Put all extensions in the EXTERNAL_MANDRAKE_MODULES hack.
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Fri Jan 03 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-1mdk
- Shiny new version, remade all patches
- Add command-line interface in package php-cli and renamed the main
  package as php-cgi
- Use update-alternatives to determine whether php-cgi or php-cli will be
  called as the main php binary.
- Add openssl to be able to call fopen with https://
- Make rpmlint totally happy
- rename php-common to libphp_common430 
- rename php-devel to php430-devel
- move php.ini to a php-ini RPM so we can modify the ini files more easily,
  specially with the new scan-dir approach and the new php-cli.ini file.
  (Oden, have fun ;-)
- put a new PHP_BUILD file with rpm global defines, a bit like ADVX-build,
  since php -v doesn't give the version number alone, but puts it within a
  couple of lines of misc. information.
- put php-killrpath into the -devel package so we can use it for the extensions
  as well.
- fix Requires and BuildRequires
- remove pear, will be in a new package, built directly from pear.php.net.
  This will enable us not to ship XML as part of the main package
- pick up internal_functions.c, since this is needed to build mod_php and
  apache2-mod_php, and symlink extensions/ to ext/ as well, because of some
  includes of internal_functions.c

* Wed Nov 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.3-3mdk
- Patch4: Temptative 64-bit fixes
- Patch5: Teach it wonderful life of lib64
- Ship with pearize and phptar, don't know what's that maintainer will
  please clear this out

* Tue Oct 29 2002 Stefan van der Eijk <stefan@eijk.nu> 4.2.3-2mdk
- BuildRequires: zlib-devel

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3 maintenance release
- remove patches 18 and 22, re-made patches 13 and 15.

* Thu Aug 22 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.2-2mdk
- Put back gettext support (a lot of people complained about that)
- Fix include_path in php.ini so the directories have a trailing slash 
  (to be able to do include "a.php" instead of include "/usr/lib/php/a.php", 
  as Alexander Skwar pointed out)
- clean up spec a bit

* Thu Aug 22 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.2-1mdk
- PHP 4.2.2 security update
- Update php.ini
- SSL is now an external module, since it's marked as experimental, and its
  API may change in future releases without notice. 
- Put back these modules into the main PHP lib (see note at top of the spec):
  ftp, posix, session, sysvsem, sysvshm, yp, zlib, pcre
- Remove all "--disable" entries with phpinfo, and correct wording for
  availability of external modules 

* Wed Jul 03 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-8mdk
- updated by Alexander Skwar <ASkwar@DigitalProjects.com>
	- Fix PEAR
	- Move PEAR to %{peardir}
	- Move PEAR files from devel to pear package
	- Make php.ini readable on 80 col displays
	- Add %{peardir} to include_path in ini

* Fri May 31 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-7mdk
- add xmlrpc.so in php.ini.

* Thu May 30 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-6mdk
- add tclink.so in php.ini.

* Tue May 28 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-5mdk
- php-pear requires php-xmlrpc.

* Mon May 27 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-4mdk
- fix provides in php-devel

* Sun May 26 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-3mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- added the %{phpdir}/*.php files that so mysteriousely disappeared,
	  those belong to the pear package (?)
	- broke out the xmlrpc stuff as an external module php-xmlrpc, added that
	  to php.ini
	- removed "-lpthread" (--enable-experimental-zts broke apache1); check:
	  http://www.mandrake.com/en/archives/cooker/2002-05/msg01099.php

* Wed May 22 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-2mdk
- add BuildRequires&Requires libxmlrpc (for the temporary --with-xmlrpc)

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- keep xmlrpc changes.
- make a separate php-pear package.
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- new version
	- added P10-P22 (stolen from PLD)
	- fix php.ini
	- misc spec file fixes

* Thu May 16 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-2mdk
- build against latest openssl.
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- misc spec file fixes
	- rebuilt with latest system compiler (gcc3.1)
	- force mail() inclusion
	- added more extensions to php.ini

* Mon Apr 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net> :
	- new Source6
	- made it possible to have most common extensions as modules, and a more
	  clever way to do it and expose it (Patch3 + spec file hack).
	- added requires openssl (forgot about that :))
	- new version
	- adjusted Patch1
	- misc spec file fixes
	- added "--with-openssl" to be able to build the new imap and snmp extensions.

* Mon Mar 02 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-1mdk
- 4.1.2 is the same as 4.1.1+patch, but the Zend optimizer will not link
  properly if the release number is not the same...
- Removec expat because of segfaults when different versions of expat are
  linked statically in different pieces of apache.

* Wed Feb 27 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-4mdk
- File uploads security fix.

* Tue Jan 15 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-3mdk
- Remove --with-mm because of a bug with libmm & /tmp/session_mm.sem (Thanks to Thor).

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-2mdk
- Added smtpdaemon in BuildRequires (needed to include mail()).

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-1mdk
- 4.1.1 (bug fixes)

* Wed Dec 12 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-2mdk
- Patch2 to be able to compile php-imap.

* Tue Dec 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-1mdk
- 4.1.0.

* Sat Sep 09 2001 David BAUDENS <baudens@mandrakesoft.com> 4.0.6-5mdk
- Clean after build
- Remove french locale from Summary
- Fix Provides and Requires
- Bzip2 patches
- Use %%make
- Add missing file

* Tue Aug 28 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-4mdk
- s/libgdbm1/libgdbm2 (Thanx to Digital Wokan).
- Fixed some rpmlint warnings and errors.

* Tue Jul 24 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.6-3mdk
- removed Obsoletes: php-devel for devel subpackage

* Mon Jul  9 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-2mdk
- removed Obsoletes: php-mysql

* Wed Jul  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-1mdk
- 4.0.6
- remove -DHAVE_CONFIG_H from buildext script so that modules build
- fix PEAR installation by specifying peardir explicitly
- s/Copyright/License/

* Thu Apr 12 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-6mdk
- recreate php.ini in case someone uses rpm -Uvh *, since rpm handles
  config files in a weird way when movig the config file to a different
  sub-package. *Very important* since it can render php useless when
  updating from the 7.2 updates from 8.0

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-5mdk
- use serverbuild macro

* Tue Mar 27 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-4mdk
- completely remade spec file
- renamed library to fit the libtool philosophy
- created libphp package, the php package is now only the standalone. People
  shouldn't have to install the standalone package if they don't want to,
  and rpmlint doesn't want a binary and a library in same package
- put manual and all sub-modules into their own package. It will be easier
  this way, since we can, say, recompile only php-mysql without touching the
  other modules
- changed builddefs so people see --external-modules=mysql,pgsql,etc...
  instead of --without-mysql which fooled people in thinking they had to
  recompile when they only had to install the right module
- removed RPATH since it could be a security problem
- fix upgrade scripts for good

* Mon Jan 22 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.4pl1-3mdk
- fix upgrade scripts

* Sun Jan 21 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.4pl1-2mdk
- rebuild against new MySQL for php-mysql

* Thu Jan 18 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.4pl1-1mdk
- 4.0.4pl1; security fixes for PHP directive problems

* Thu Dec 21 2000 Vincent Danen <vdanen@mandrakesoft.com> 4.0.4-1mdk
- 4.0.4

* Tue Dec 12 2000 Vincent Saugey <vince@mandrakesoft.com> 4.0.3pl1-3mdk
- declare top_srcdir at build step 

* Sat Nov 11 2000 Daouda Lo <daouda@mandrakesoft.com> 4.0.3pl1-2mdk
- correct php-pgsql preuninstall typo (thanx Florent Guillaume)

* Sun Oct 22 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.3pl1-1mdk
- Bugfix + Security release

* Wed Sep 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.2-4mdk
- Fixed requires
- Rebuilt for new Apache
- Removed security patch SRADV00001 because it was causing segfaults with
  POST and multipart/form-data
- Removed CVS junk files in php-manual

* Fri Sep  8 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.2-3mdk
- Added security patch from Vincent Danen for (SRADV00001) Arbitrary file
  disclosure through PHP file upload
- Patched aclocal.m4 and acinclude.m4... Looks like every release they
  break something!
- imap was also broken. Added -lpam to the flags.
- compiled php with -lpthread to fix damn segfaults
- new MySQL release: compile with lmysqlclient_r
- removed conflict with midgard (i heard that both can coexist now)
- mysql: Tested phpMyAdmin - success! Tested also standalone with
  code from: php-manual/function.mysql-pconnect.html
- gd: Tested generation of png graphics with truetype, both in standalone
  and apache module
- pgsql: tested with standalone binary and the example code contained in
  php-manual/ref.pgsql.html. After a "createuser apache" in postgres, also
  tested successfully the apache mode
- imap: tested imap_open and imap_close on port 110 with standalone
  and in apache module
- ldap: tested functions in php-manual/function.ldap-add.html
  with standalone and apache module
- split dba_gdbm_db2 and readline from the main package. The first, because we
  might support db3 eventually, and the lase because it required 3
  additional libraries, and was only for the standalone version.
- tested dba_gdbm_db2 with standalone and apache module with sample code from
  php-manual/ref.dba.html
- tested readline with standalone (it is interactive so it won't work with
  apache) with code from php-manual/ref.readline.html
- we now use a libphp4_shared: this saves space and permits to use
  any module with any server API
- put the SAPI files into the php-devel package so we can compile eventually
  thttpd, roxen, or the servlet API
- put php_standalone into the main php package to be able to use the new
  PEAR interface (like CPAN, but for PHP4)
- renamed all modules. They are now called php-something instead of
  mod_php-something. The reason is they can be used with either php-thttpd,
  php-standalone, php-servlet or under apache (where this module is still
  called mod_php, to be consistent with mod_perl, mod_jserv, etc..).

* Fri Sep  1 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.2-2mdk
- Heavy use of perl s///g to make it install at the right place

* Thu Aug 31 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.2-1mdk
- shiny new 4.0.2!!
- removed db3 support: it crashes the configure script, and besides, it's
  not in the distro (only in contribs). We use GDBM and DB2.

* Thu Aug 24 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.1pl2-6mdk
- created extensions package
- fixed mysql support

* Wed Aug  9 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.1pl2-5mdk
- link mysql.so with libmysqlclient.so

* Wed Aug  9 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.1pl2-4mdk
- Compile with latest MySQL
- Changed paths for FHS
- Macroize
- Fixed the BuildRequires (please, don't auto-regenerate)

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1pl2-3mdk
- automatically added BuildRequires

* Fri Jul 14 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.1pl2-2mdk
- added recode
- rebuilt for new EAPI
- use new AESctl script for %post
- Bonnne Fete la France! =)

* Sat Jul 08 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.1pl2-1mdk
- update to 4.0.1pl2 (lots of bug fixes)
- moved php binary to php-standalone package
- fixed module compilation (specially the again badly broken pgsql)

* Tue Jun 20 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.0-1mdk
- update to PHP 4.0.0
- compile in two pass so that the extensions work both with PHP and mod_php
- include development package. This will enable us to compile dynamic
  extensions outside the main PHP4 package. This will come handy for
  the Oracle, Sybase, swf, etc. modules.
- spent long nights figuring how to make GD+ttf+t1lib with PHP4
- many fixes to remain RH-compatible a bit, but to keep our improvements,
  and have a working config (RH handles extensions poorly and makes php
  require postgres, ldap and imap even if the use won't use it).
- change most of the Requires to Prereqs, because the post edits config files
- change most of the postuns to preuns in case php gets removed before subpkgs
- make subpackages require php = %{version}
- add Obsoletes: phpfi, because their content handler names are the same
- add standalone binary
- change license from "GPL" to "PHP"

* Wed Jun 14 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 3.0.16-6mdk
- last version, PHP4 is on the way (hurray! ;-)
- added -llber to the ldap package
- split gd library out of the main package so it doesn't require
  XFree-libs!
- removed Dadou's hack for i486 compilation. When cross-compiling,
  first build Apache, then install apache and apache-devel before
  you compile other apache modules. It will then compile for the
  same architecture that apache has been compiled with.

* Thu May 18 2000 David BAUDENS <baudens@mandrakesoft.com> 3.0.16-5mdk
- Better fix for i486

* Mon May 15 2000 David BAUDENS <baudens@mandrakesoft.com> 3.0.16-4mdk
- Fix build for i486
- Fix some typos
- Fix build as user

* Mon May 08 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 3.0.16-3mdk
- added Prereq so it doesn't complain about missing php3.ini
- rebuild with EAPI 2.6.4 (bugfixes)
- include /usr/bin/* 
- removed old manual from sources

* Thu Apr  6 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 3.0.16-2mdk
- rebuit with EAPI 2.6.3
- moved doc
- added -DHAVE_PQCMDTUPLES
- put ldap in separate module

* Thu Apr  6 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 3.0.16-1mdk
- 3.0.16 bugfix release

* Mon Apr  3 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 3.0.15-4mdk
- fixed group
- created MySQL as a separate module to fix dependancies

* Tue Feb 29 2000 Jean-Michel Dault <jmdault@netrevolution.com> 3.0.15-3mdk
- rebuild for EAPI 2.6.1
- updated manual

* Mon Feb 27 2000 Jean-Michel Dault <jmdault@netrevolution.com> 3.0.15-2mdk
- re-made gd+ttf patch. (again)

* Mon Feb 27 2000 Jean-Michel Dault <jmdault@netrevolution.com> 3.0.15-1mdk
- added many BuildRequires (this is a very complex package!)
- upgraded to 3.0.15 (security updates)
- updated mysql client to 3.22.32
- added patch suggested by jeff b <jeff@univrel.pr.uconn.edu> to
  decrease the TOKEN_BITS from 20 to 18. This allows large applications
  written in PHP to not bomb out due to running out of tokens.

* Tue Jan 18 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- upgraded to 3.0.14
- updated mysql client to 3.22.30
- added support for ftp

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- final cleanup for Mandrake 7

* Mon Jan 3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- upgraded to 3.0.13
- fixed png support
- fixed reversed ttf fonts
- fixed imap and pgsql for good, made apache restart when installing these
  packages
- updated mysql client to 3.22.29

* Thu Dec 30 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- rebuilt for Oxygen and new mm-1.0.12 in Apache
- added ttf and t1lib, which are now part of Mandrake
- added gd support (png only, to enable gifs, you have to rebuild the rpm
  with the old library)

* Fri Sep 3 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- rebuilt for new mm-1.0.10 in Apache

* Thu Aug 26 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- added Conflicts line

* Fri Aug 19 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- Solaris adaptations

* Wed Aug 18 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- modified post scripts

* Sat Jul 31 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- upgraded to 3.0.12

* Wed Jul 21 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- upgraded to 3.0.11
- added RPM_OPT_FLAGS
- added fr locale
- "mandrakized" package again

* Mon Jun 14 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 3.0.9
- fixed postgresql module and made separate package
- separated manual into separate documentation package

* Mon May 24 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 3.0.8, which fixes problems with glibc 2.1.
- took some ideas grom Gomez's RPM.

* Tue May 04 1999 Preston Brown <pbrown@redhat.com>
- hacked in imap support in an ugly way until imap gets an official
  shared library implementation

* Fri Apr 16 1999 Preston Brown <pbrown@redhat.com>
- pick up php3.ini

* Wed Mar 24 1999 Preston Brown <pbrown@redhat.com>
- build against apache 1.3.6

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 3.0.7.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Sun Feb 07 1999 Preston Brown <pbrown@redhat.com>
- upgrade to php 3.0.6, built against apache 1.3.4

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- rebuild for apache 1.3.3

* Thu Oct 08 1998 Preston Brown <pbrown@redhat.com>
- updated to 3.0.5, fixes nasty bugs in 3.0.4.

* Sun Sep 27 1998 Cristian Gafton <gafton@redhat.com>
- updated to 3.0.4 and recompiled for apache 1.3.2

* Thu Sep 03 1998 Preston Brown <pbrown@redhat.com>
- improvements; builds with apache-devel package installed.

* Tue Sep 01 1998 Preston Brown <pbrown@redhat.com>
- Made initial cut for PHP3.
