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
%define version		5.2.2
%define release		%_revrel
%define epoch		2

%define libversion	5
%define libname		%mklibname php_common %{libversion}

%define suhosin_ver	5.2.2rc2-0.9.6.2

%define _requires_exceptions BEGIN\\|mkinstalldirs\\|pear(\\|/usr/bin/tclsh

Summary:	The PHP5 scripting language
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net
Source0:	http://static.php.net/www.php.net/distributions/php-%{version}.tar.bz2
#
# Mandriva/Annvix patches
#
Patch0:		php-4.3.0-mdk-init.patch
Patch1:		php-5.2.0-mdv-shared.patch
Patch2:		php-4.3.0-mdk-imap.patch
Patch3:		php-4.3.4RC3-mdk-64bit.patch
Patch4:		php-5.1.2-mdk-lib64.patch
Patch5:		php-4.3.11-mdk-libtool.patch
Patch6:		php-5.2.0-mdv-no_egg.patch
Patch7:		php-5.1.2-mdk-phpize.patch
Patch8:		php-5.1.0RC4-mdk-remove_bogus_iconv_deps.patch
Patch9:		php-5.1.0RC1-mdk-phpbuilddir.patch
# http://www.outoforder.cc/projects/apache/mod_transform/patches/php5-apache2-filters.patch
Patch10:	php5-apache2-filters.patch
# P11 fixes the way we package the extensions to not check if the dep are installed or compiled in
Patch11:	php-5.1.3-mdk-extension_dep_macro_revert.patch
Patch12:	php-5.1.2-mdk-no_libedit.patch
Patch13:	php-5.2.1-mdv-extraimapcheck.patch
#
# from PLD (20-40)
#
Patch20:	php-4.3.0-pld-mail.patch
Patch21:	php-4.3.3RC3-pld-sybase-fix.patch
Patch25:	php-5.0.3-pld-dba-link.patch
Patch27:	php-4.4.1-pld-zlib-for-getimagesize.patch
Patch28:	php-5.0.0b3-pld-zlib.patch
#
# from Fedora (50-60)
#
Patch50:	php-5.1.0b1-fdr-cxx.patch
Patch51:	php-4.3.3-fdr-install.patch
Patch52:	php-5.0.4-fdr-norpath.patch
Patch53:	php-5.2.1-fdr-umask.patch
#
# General fixes (70+)
#
Patch70:	php-4.3.1-mdk-odbc.patch
Patch71:	php-4.3.11-mdk-shutdown.patch
# Functional changes
Patch72:	php-5.0.4-mdk-dlopen.patch
# Fixes for tests
Patch73:	php-5.1.0RC4-mdk-tests-dashn.patch
Patch74:	php-5.1.0b1-mdk-tests-wddx.patch
# http://bugs.php.net/bug.php?id=29119
Patch76:	php-5.0.4-bug29119.diff
Patch77:	php-5.1.0RC6-CVE-2005-3388.diff
Patch78:	php-5.2.0-mdv-libc-client-php.patch
Patch80:	php-5.2.0-CVE-2006-6383.patch
# http://www.hardened-php.net/
Patch100:	suhosin-patch-%{suhosin_ver}.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	httpd-devel >= 2.0.54
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	bison
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6
BuildRequires:	libxslt-devel >= 1.1.0
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	openssl >= 0.9.7
BuildRequires:	pcre-devel >= 6.6
BuildRequires:	pam-devel
BuildRequires:	multiarch-utils >= 1.0.3

%description
PHP5 is an HTML-embeddable scripting language.  PHP offers built-in database
integration for several commercial and non-commercial database management
systems, so writing a database-enabled script with PHP is fairly simple.  The
most common use of PHP coding is probably as a replacement for CGI scripts.


%package cli
Summary:	Command-line interface to PHP
Epoch:		%{epoch}
Group:		Development/PHP
URL:		http://www.php.net
Requires(pre):	php-ini
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Requires:	php-ftp >= %{version}
Requires:	php-pcre >= %{version}
Requires:	php-gettext >= %{version}
Requires:	php-posix >= %{version}
Requires:	php-ctype >= %{version}
Requires:	php-session >= %{version}
Requires:	php-sysvsem >= %{version}
Requires:	php-sysvshm >= %{version}
Requires:	php-tokenizer >= %{version}
Requires:	php-simplexml >= %{version}
Requires:	php-hash >= %{version}
Requires:	php-suhosin >= 0.9.10
Requires:	php-filter >= 0.11.0
Requires:	php-json >= 1.2.1
Provides:	php = %{version}
Provides:	php5 = %{version}
Provides:	php%{libversion} = %{version}
Obsoletes:	php

%description cli
PHP5 is an HTML-embeddable scripting language.  PHP offers built-in database
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
Group:		Development/PHP
URL:		http://www.php.net
Requires(pre):	php-ini
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Requires:	php-ftp >= %{version}
Requires:	php-pcre >= %{version}
Requires:	php-gettext >= %{version}
Requires:	php-posix >= %{version}
Requires:	php-ctype >= %{version}
Requires:	php-session >= %{version}
Requires:	php-sysvsem >= %{version}
Requires:	php-sysvshm >= %{version}
Requires:	php-tokenizer >= %{version}
Requires:	php-simplexml >= %{version}
Requires:	php-hash >= %{version}
Requires:	php-suhosin >= 0.9.10
Requires:	php-filter >= 0.11.0
Requires:	php-json >= 1.2.1
Provides:	php = %{version}
Provides:	php5 = %{version}
Provides:	php%{libversion} = %{version}
Obsoletes:	php

%description cgi
PHP5 is an HTML-embeddable scripting language.  PHP offers built-in database
integration for several commercial and non-commercial database management
systems, so writing a database-enabled script with PHP is fairly simple.  The
most common use of PHP coding is probably as a replacement for CGI scripts.

This package contains a standalone (CGI) version of php. You must also
install libphp_common. 

If you need apache module support, you also need to install the mod_php
package.


%package fcgi
Summary:	FastCGI interface to PHP
Epoch:		%{epoch}
Group:		Development/PHP
URL:		http://www.php.net
Requires(pre):	php-ini
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Requires:	php-ftp >= %{version}
Requires:	php-pcre >= %{version}
Requires:	php-gettext >= %{version}
Requires:	php-posix >= %{version}
Requires:	php-ctype >= %{version}
Requires:	php-session >= %{version}
Requires:	php-sysvsem >= %{version}
Requires:	php-sysvshm >= %{version}
Requires:	php-tokenizer >= %{version}
Requires:	php-simplexml >= %{version}
Requires:	php-hash >= %{version}
Requires:	php-suhosin >= 0.9.10
Requires:	php-filter >= 0.11.0
Requires:	php-json >= 1.2.1
Provides:	php = %{version}
Provides:	php5 = %{version}
Provides:	php%{libversion} = %{version}
Obsoletes:	php

%description fcgi
PHP5 is an HTML-embeddable scripting language. PHP5 offers built-in
database integration for several commercial and non-commercial
database management systems, so writing a database-enabled script
with PHP5 is fairly simple.  The most common use of PHP5 coding is
probably as a replacement for CGI scripts.

This package contains a standalone (CGI) version of php with FastCGI
support. You must also install libphp5_common. If you need apache
module support, you also need to install the apache-mod_php
package.


%package -n %{libname}
Summary:	Shared library for php
Epoch:		%{epoch}
Group:		Development/PHP
URL:		http://www.php.net
Provides:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	libphp_common = %{version}
Provides:	php-common = %{version}
Provides:	php-pcre = %{version}
Provides:	php-xml = %{version}
Obsoletes:	php-pcre
Obsoletes:	php-xml

%description -n	%{libname}
This package provides the common files to run with different
implementations of PHP. You need this package if you install the php
standalone package or a webserver with php support (ie: mod_php).

%package devel
Summary:	Development package for PHP5
Group:		Development/C
URL:		http://www.php.net
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Requires:	autoconf2.5
Requires:	automake1.7
Requires:	bison
Requires:	byacc
Requires:	flex
Requires:	libtool
Requires:	libxml2-devel >= 2.6
Requires:	libxslt-devel >= 1.1.0
Requires:	openssl >= 0.9.7
Requires:	openssl-devel >= 0.9.7
Requires:	pcre-devel >= 6.6
Requires:	pam-devel
Requires:	chrpath
Requires(post):	%{libname} >= %{epoch}:%{version}
Requires(preun): %{libname} >= %{epoch}:%{version}
Provides:	libphp_common-devel = %{version}

%description devel
The php-devel package lets you compile dynamic extensions to PHP5. Included
here is the source for the php extensions. Instead of recompiling the whole
php binary to add support for, say, oracle, install this package and use the
new self-contained extensions support. For more information, read the file
SELF-CONTAINED-EXTENSIONS.


%package pear
Summary:	The PHP PEAR files
Group:		Development/Other
Requires:	php-cli

%description pear
PEAR is short for "PHP Extension and Application Repository" and is
pronounced just like the fruit. The purpose of PEAR is to provide:

    * A structured library of open-sourced code for PHP users
    * A system for code distribution and package maintenance
    * A standard style for code written in PHP, specified here
    * The PHP Foundation Classes (PFC), see more below
    * The PHP Extension Code Library (PECL), see more below
    * A web site, mailing lists and download mirrors to support the
      PHP/PEAR community


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.



%prep
%setup -q -n php-%{version}
# use .avx suffix to delete patch backups so they don't end up in php-devel
%patch0 -p1 -b .init.avx
%patch1 -p1 -b .shared.avx
%patch2 -p0 -b .imap.avx
%patch3 -p1 -b .64bit.avx
%patch4 -p1 -b .lib64.avx
%patch5 -p0 -b .libtool.avx
%patch6 -p1 -b .no_egg.avx
%patch7 -p1 -b .phpize.avx
%patch8 -p0 -b .remove_bogus_iconv_deps.avx
%patch9 -p1 -b .phpbuilddir.avx
%patch10 -p0 -b .apache2-filters.avx
%patch11 -p1 -b .extension_dep_macro_revert.avx
%patch12 -p0 -b .no_libedit.avx
%patch13 -p0 -b .extraimapcheck.avx
# from PLD
%patch20 -p1 -b .mail.avx
%patch21 -p1 -b .sybase-fix.avx
%patch25 -p1 -b .dba-link.avx
%patch27 -p1 -b .zlib-for-getimagesize.avx
%patch28 -p1 -b .zlib.avx
# from Fedora
%patch50 -p0 -b .cxx.avx
%patch51 -p1 -b .install.avx
%patch52 -p1 -b .norpath.avx
%patch53 -p0 -b .umask.avx
#
%patch70 -p1 -b .odbc.avx
%patch71 -p1 -b .shutdown.avx
%patch72 -p1 -b .dlopen.avx
#
#%patch73 -p1 -b .tests-dashn.avx
%patch74 -p1 -b .tests-wddx.avx

# make the tests worky
%patch76 -p0 -b .bug29119.avx
%patch77 -p0 -b .cve-2005-3388.avx
%patch78 -p0 -b .libc-client-php.avx
%patch80 -p1 -b .cve-2006-6383.avx

%patch100 -p1 -b .suhosin.avx

# Change perms otherwise rpm would get fooled while finding requires
find -name "*.inc" | xargs chmod 0644
find -name "*.php*" | xargs chmod 0644
find -name "*README*" | xargs chmod 0644

mkdir -p php-devel/extensions
mkdir -p php-devel/sapi

# cleanup php-devel
cp -a tests php-devel/

cp -dpR ext/* php-devel/extensions/
rm -f php-devel/extensions/informix/stub.c
rm -f php-devel/extensions/standard/.deps
rm -f php-devel/extensions/skeleton/EXPERIMENTAL
rm -f php-devel/extensions/ncurses/EXPERIMENTAL

# windows sources are not wanted
rm -rf php-devel/extensions/com
rm -rf php-devel/extensions/dotnet
rm -rf php-devel/extensions/printer
rm -rf php-devel/extensions/w32api

cp -dpR sapi/* php-devel/sapi/ 
rm -f php-devel/sapi/thttpd/stub.c
rm -f php-devel/sapi/cgi/php.sym
rm -f php-devel/sapi/fastcgi/php.sym
rm -f php-devel/sapi/pi3web/php.sym

# remove other unwanted files
find php-devel -name "*.dsp" | xargs rm -f
find php-devel -name "*.mak" | xargs rm -f
find php-devel -name "*.w32" | xargs rm
find php-devel -name "*.avx" | xargs rm -f

cat > php-devel/buildext <<EOF
#!/bin/bash
gcc -Wall -fPIC -shared %{optflags} \\
    -I. \`%{_bindir}/php-config --includes\` \\
    -I%{_includedir}/libxml2 \\
    -I%{_includedir}/freetype \\
    -I%{_includedir}/openssl \\
    -I%{_usrsrc}/php-devel/ext \\
    -I%{_includedir}/\$1 \\
    \$4 \$2 -o \$1.so \$3 -lc
EOF

chmod 0755 php-devel/buildext


%build
# this _has_ to be executed!
#export WANT_AUTOCONF_2_5=1

rm -f configure; aclocal-1.7 && autoconf --force && autoheader
#./buildconf --force

perl -pi -e "s|'\\\$install_libdir'|'%{_libdir}'|" ltmain.sh

export oldstyleextdir=yes
export EXTENSION_DIR="%{_libdir}/php/extensions"
export PROG_SENDMAIL="%{_sbindir}/sendmail"
export CFLAGS="%{optflags} -fPIC -L%{_libdir}"

# never use "--disable-rpath", it does the opposite
# Configure php
for i in cgi cli fcgi apxs; do
    ./configure \
        `[ $i = apxs ] && echo --with-apxs2=%{_sbindir}/apxs` \
        `[ $i = fcgi ] && echo --enable-fastcgi --with-fastcgi=%{_prefix} --disable-cli --enable-force-cgi-redirect` \
        `[ $i = cgi ] && echo --enable-discard-path --disable-cli --enable-force-cgi-redirect` \
        `[ $i = cli ] && echo --disable-cgi --enable-cli` \
        --cache-file=config.cache \
        --build=%{_build} \
        --prefix=%{_prefix} \
        --exec-prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_localstatedir} \
        --mandir=%{_mandir} \
        --enable-shared=yes \
        --enable-static=no \
        --with-libdir=%{_lib} \
        --disable-all \
        --with-config-file-path=%{_sysconfdir} \
        --with-config-file-scan-dir=%{_sysconfdir}/php.d \
        --disable-debug \
        --enable-pic \
        --enable-inline-optimization \
        --with-exec-dir=%{_bindir} \
        --with-pcre=%{_prefix} \
        --with-pcre-regex=%{_prefix} \
        --with-ttf \
        --with-freetype-dir=%{_prefix} \
        --with-zlib=%{_prefix} \
        --with-png-dir=%{_prefix} \
        --with-regex=php \
        --enable-magic-quotes \
        --enable-safe-mode \
        --with-zlib=%{_prefix} \
        --with-zlib-dir=%{_prefix} \
        --with-openssl=%{_prefix} \
        --enable-libxml=%{_prefix} \
        --with-libxml-dir=%{_prefix} \
        --enable-spl=%{_prefix} \
        --enable-track-vars \
        --enable-trans-sid \
        --enable-memory-limit \
        --with-versioning \
        --with-mod_charset \
        --with-pear=%{_datadir}/pear \
        --with-pcre-regex \
        --enable-xml
#        --without-pear

    cp -f Makefile Makefile.$i
    cp -f main/php_config.h php_config.h.$i

    perl -pi -e 's|-prefer-non-pic -static||g' Makefile.$i
done

# remove all confusion...
perl -pi -e "s|^#define CONFIGURE_COMMAND .*|#define CONFIGURE_COMMAND \"This is irrelevant, look inside the %{_docdir}/libphp_common%{libversion}-%{version}/configure_command file. urpmi is your friend, use it to install extensions not shown below.\"|g" main/build-defs.h
cp config.nice configure_command; chmod 0644 configure_command

%make

# make php-fcgi
cp -af php_config.h.fcgi main/php_config.h
%make -f Makefile.fcgi sapi/cgi/php
cp -rp sapi/cgi sapi/fcgi
perl -pi -e "s|sapi/cgi|sapi/fcgi|g" sapi/fcgi/php
rm -rf sapi/cgi/.libs; rm -f sapi/cgi/*.lo sapi/cgi/php

# make php-cgi
cp -af php_config.h.cgi main/php_config.h
%make -f Makefile.cgi sapi/cgi/php

cp -af php_config.h.apxs main/php_config.h


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/php/extensions
mkdir -p %{buildroot}%{_usrsrc}/php-devel
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_bindir}

make -f Makefile.apxs install \
    INSTALL_ROOT=%{buildroot} \
    INSTALL_IT="\$(LIBTOOL) --mode=install install libphp5_common.la %{buildroot}%{_libdir}/" \
    INSTALL_CLI="\$(LIBTOOL) --silent --mode=install install sapi/cli/php %{buildroot}%{_bindir}/php"

./libtool --silent --mode=install install sapi/fcgi/php %{buildroot}%{_bindir}/php-fcgi
./libtool --silent --mode=install install sapi/cgi/php %{buildroot}%{_bindir}/php-cgi

cp -dpR php-devel/* %{buildroot}%{_usrsrc}/php-devel/
install -m 0644 run-tests*.php %{buildroot}%{_usrsrc}/php-devel/
install -m 0644 main/internal_functions.c %{buildroot}%{_usrsrc}/php-devel/
install -m 0755 scripts/phpize %{buildroot}%{_bindir}/
install -m 0755 scripts/php-config %{buildroot}%{_bindir}/

install -m 0644 sapi/cli/php.1 %{buildroot}%{_mandir}/man1/
install -m 0644 scripts/man1/phpize.1 %{buildroot}%{_mandir}/man1/
install -m 0644 scripts/man1/php-config.1 %{buildroot}%{_mandir}/man1/

ln -snf extensions %{buildroot}%{_usrsrc}/php-devel/ext

# fix docs
cp Zend/LICENSE Zend/ZEND_LICENSE
cp README.SELF-CONTAINED-EXTENSIONS SELF-CONTAINED-EXTENSIONS
pushd ext
    for i in `ls -1`
    do
        if [ -f "$i/CREDITS" ]; then
            cp $i/CREDITS ../CREDITS.$i
        fi
        if [ -f "$i/README" ]; then
            cp $i/README ../README.$i
        fi
    done
popd

# cgi docs
cp sapi/cgi/CREDITS CREDITS.cgi

# fcgi docs
cp sapi/cgi/README.FastCGI README.fcgi
cp sapi/cgi/CREDITS CREDITS.fcg

# cli docs
cp sapi/cli/CREDITS CREDITS.cli
cp sapi/cli/README README.cli
cp sapi/cli/TODO TODO.cli

# other docs
cp -a ext/dom/examples php-dom-examples
mkdir php-exif-examples && cp -a ext/exif/{example.php,test.php,test.txt} php-exif-examples/
cp -a ext/simplexml/examples php-simplexml-examples

# house cleaning
rm -f %{buildroot}%{_libdir}/*.a

# fix one strange weirdo
perl -pi -e "s|^libdir=.*|libdir='%{_libdir}'|g" %{buildroot}%{_libdir}/*.la

%multiarch_includes %{buildroot}%{_includedir}/php/main/build-defs.h
%multiarch_includes %{buildroot}%{_includedir}/php/main/config.w32.h
%multiarch_includes %{buildroot}%{_includedir}/php/main/php_config.h

# fix PEAR
rm -rf %{buildroot}/.{channels,depdb,depdblock,filemap,lock}
rm -rf %{buildroot}/%{_datadir}/pear/.{depdb,depdblock,lock}
rm -f %{buildroot}%{_sysconfdir}/pear.conf


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%pre cgi
update-alternatives --remove php %{_bindir}/php-cgi
update-alternatives --remove php %{_bindir}/php-fcgi
update-alternatives --remove php %{_bindir}/php-cli


%pre fcgi
update-alternatives --remove php %{_bindir}/php-cgi
update-alternatives --remove php %{_bindir}/php-fcgi
update-alternatives --remove php %{_bindir}/php-cli


%pre cli
update-alternatives --remove php %{_bindir}/php-cgi
update-alternatives --remove php %{_bindir}/php-fcgi
update-alternatives --remove php %{_bindir}/php-cli


%post pear
if [ ! -f /etc/pear.conf ]; then
    echo "Creating initial /etc/pear.conf"
    %{_bindir}/pear config-create /usr/share /etc/pear.conf >/dev/null
    %{_bindir}/pear config-set bin_dir %{_bindir} >/dev/null
    %{_bindir}/pear config-set ext_dir %{_libdir}/php/extensions >/dev/null
    %{_bindir}/pear config-set php_dir %{_datadir}/pear >/dev/null
    # unfortunately, pear's config-set modifies the user's .pearrc instead of the system-wide one
    mv -f $HOME/.pearrc /etc/pear.conf
fi


%files cgi
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/php-cgi

%files fcgi
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/php-fcgi

%files cli
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/php
%attr(0644,root,root) %{_mandir}/man1/php.1*

%files -n %{libname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/libphp5_common.so.*

%files devel
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/php-config
%attr(0755,root,root) %{_bindir}/phpize
%attr(0755,root,root) %{_libdir}/libphp5_common.so
%attr(0755,root,root) %{_libdir}/libphp5_common.la
%dir %{_libdir}/php/build
%{_libdir}/php/build/*
%{_usrsrc}/php-devel
%multiarch %{multiarch_includedir}/php/main/build-defs.h
%multiarch %{multiarch_includedir}/php/main/config.w32.h
%multiarch %{multiarch_includedir}/php/main/php_config.h
%{_includedir}/php
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/phpize.1*

%files pear
%defattr(-,root,root)
%dir %{_datadir}/pear
%{_datadir}/pear/*
%{_datadir}/pear/.filemap
%{_datadir}/pear/.registry
%{_datadir}/pear/.channels
%{_bindir}/pear
%{_bindir}/peardev
%{_bindir}/pecl

%files doc
%defattr(-,root,root)
%doc CREDITS* README* TODO* Zend/ZEND_*
%doc INSTALL LICENSE NEWS php.ini-dist php.ini-recommended configure_command
%doc SELF-CONTAINED-EXTENSIONS CODING_STANDARDS TODO EXTENSIONS
%doc php-dom-examples
%doc php-exif-examples
%doc php-simplexml-examples


%changelog
* Mon May 28 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.2
- add php-fcgi

* Fri May 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.2
- versioned provides
- drop some (useless and inacurrate) provides/obsoletes for php3/php4
- provide/obsolete php-xml; it's been built here for a while now and is
  useful enough to build right into the core

* Fri May 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.2
- php 5.2.2 (fixes for CVE-2007-1001, CVE-2007-1718, CVE-2007-1717,
  CVE-2007-1649, CVE-2007-1583, CVE-2007-1484, CVE-2007-1521, CVE-2007-1460,
  CVE-2007-1461, CVE-2007-1375, CVE-2007-1285, CVE-2007-1396, CVE-2007-1864)
- updated suhosin (5.2.2-rc2-0.9.6.2)
- drop upstream patches P75, P81
- fix dependency exceptions

* Thu May 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- drop the php-xml and php-xmlrpc requires on php-pear as they don't seem necessary

* Wed Feb 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- php 5.2.1
- updated suhosin (5.2.1-0.9.6.2)
- updated P53
- drop P79 - merged upstream
- P13: extra safe_mode/open_basedir checks for imap support from Mandriva

* Wed Feb 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- P80: security fix for CVE-2006-6383
- P81: security fix for CVE-2007-0455
 
* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- apache 2.2.4

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- build against new libxml2 and libxslt

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- rebuild against new pam

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- don't install our pear.conf but run the pear command to create the
  config on intial install

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- 5.2.0
- suhosin patch 0.9.6.2
- P78: to make the imap build cleaner
- updated P1, P6 from Mandriva
- drop P22, P24, P26
- drop the buildconflicts on php
- require php-filter and php-json (from pecl) to mimic a default php build
- don't make test
- P79: add support for curl 7.16.0
- produce php-pear here rather than in a separate package

* Fri Oct 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- remove the version requirements on php-suhosin since it's using it's
  own version, not php's

* Fri Oct 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- P100: use the suhosin patch instead of the hardened patch
- requires php-suhosin

* Thu Sep 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- 5.1.6 (multiple security fixes)
- updated hardening patch

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new openssl
- spec cleanups
- hardening patch 0.4.14
- disable one test that the new hardening patch seems to have broken

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- hardening patch 0.4.12: fixes CVE-2006-2563, CVE-2006-2660, CVE-2006-1990,
  CVE-2006-3011
- spec cleanups

* Sun Jun 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new pam

* Sat Jun 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new libxml2
- really add -doc subpackage
- put all the docs for the various extensions here too

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- 5.1.4
- rediff P1, P6, P11
- updated P4 (no more ext/msession)
- drop P7; merged upstream
- hardened php 5.1.4-0.4.11
- disable tests/basic/021.phpt as it fails even on a vanilla (unpatched)
  5.1.4 so although it claims it's fixed (bug #37276) that doesn't seem to
  be the case
- add -doc subpackage
- rebuild with gcc4

* Mon Apr 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- add some sane default requires for php-cgi and php-cli
- put back the BuildConflicts on php otherwise all the tests fail

* Thu Mar 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- remove .avx files, not .droplet files
- disable the sunfuncts test as it's not 100% precise on x86_64 but it's
  so close the difference is really minor so don't let php fail on this
- find the .avx files after we copy in from sapi/ or we end up missing
  what we patched in there

* Wed Mar 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- 5.1.2
- remove debug conditional build
- add "pear(" to _requires_exceptions
- change group to Development/PHP
- drop S4 (php-test)
- sync most patches with Mandriva's 5.1.2-5mdk
- update various requires and buildrequires
- use php-devel rather than php[ver]-devel
- drop the phpdir, peardir, and phpsrcdir defines

* Wed Jan 18 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- 4.4.2
- hardening patch 0.4.8 for php 4.4.2
- rediffed P5
- dropped P6; doesn't look like it's needed any longer
- dropped P12; fixed upstream
- add a --without harden option to build without the hardening patch;
  the default is to build with it

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Tue Dec 13 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-2avx
- P12: fix php bug #35067; should fix a squirrelmail issue
- don't bzip patches or unnecessary source files anymore

* Wed Nov 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-1avx
- 4.4.1; fixes several security issues (see http://www.php.net/release_4_4_1.php)
- hardening patch 4.4.1-0.4.5

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-2avx
- hardening patch 4.4.0-0.4.3

* Wed Sep 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-1avx
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
