%define name	mod_php
%define release	1avx

#New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}

%define phpsource       %{_prefix}/src/php-devel
%define _docdir %{_datadir}/doc/%{name}-%{version}
%{expand:%(cat /usr/src/php-devel/PHP_BUILD||(echo -e "error: failed build dependencies:\n        php-devel >= 432 (4.3.2) is needed by this package." >/dev/stderr;kill -2 $PPID))}

%{expand:%%define apache_version %(rpm -q apache-devel|sed 's/apache-devel-\([0-9].*\)-.*$/\1/')}
%{expand:%%define apache_release %(rpm -q apache-devel|sed 's/apache-devel-[0-9].*-\(.*\)$/\1/')}

%{expand:%%define mm_major %(mm-config --version|sed 's/MM \([0-9]\)\.\([0-9.].*\) \(.*\)$/\1/')}
%{expand:%%define mm_minor %(mm-config --version|sed 's/MM \([0-9]\)\.\([0-9.].*\) \(.*\)$/\2/')}
%define mm_version %{mm_major}.%{mm_minor}

Summary:	The PHP4 HTML-embedded scripting language for use with Apache
Name:		%{name}
Version:	%{phpversion}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net/ 
Source1:	php.conf

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	ADVX-build >= 9.2
BuildRequires:	php%{libversion}-devel 
BuildRequires:	apache-devel 
BuildRequires:	mm-devel 
BuildRequires:	perl
BuildRequires:	libgdbm-devel
BuildRequires:	db3-devel
BuildRequires:	db1-devel
BuildRequires:  glibc-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel

Requires:	php-ini
Prereq: 	perl
Prereq:		apache = %{apache_version}
Prereq:		apache-common >= %{apache_version}
Prereq:		apache-conf >= %{apache_version}
Prereq:		mm = %{mm_major}.%{mm_minor}

#glibc-devel provides libpthread.so
Provides:	php php4 php%{libversion}
Provides:	phpapache
Provides:	mod_php3
Provides:	php3
Provides:	phpfi
Provides: 	ADVXpackage
Provides:	AP13package
Obsoletes:	mod_php3
Obsoletes:	php3
Obsoletes:	phpfi

%description
PHP is an HTML-embedded scripting language.  PHP attempts to make it
easy for developers to write dynamically generated web pages.  PHP
also offers built-in database integration for several commercial
and non-commercial database management systems, so writing a
database-enabled web page with PHP is fairly simple.  The most
common use of PHP coding is probably as a replacement for CGI
scripts.  The %{name} module enables the Apache web server to
understand and process the embedded PHP language in web pages.

This package contains PHP version 4. You'll also need to install the
Apache web server.


%build
[ -e ./%{name}-%{version} ] && rm -rf ./%{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}
cp %{phpsource}/sapi/apache/* .
cp %{phpsource}/internal_functions.c .

/usr/sbin/apxs -c -I. -I -I./main \
    `php-config --includes` \
    -I%{phpsource} \
    -lphp_common -lpthread -lgdbm -lmm \
    -DHAVE_AP_COMPAT_H \
    php_apache.c sapi_apache.c mod_php4.c internal_functions.c -o libphp4.so 

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
cd %{name}-%{version}

mkdir -p %{buildroot}%{_libdir}/apache-extramodules
mkdir -p %{buildroot}%{ap_base}/conf/addon-modules

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
cp %{phpsource}/PHP_FAQ.php \
	%{buildroot}%{_docdir}/%{name}-%{version}

install -m 644 %{SOURCE1} \
	%{buildroot}%{ap_base}/conf/addon-modules/php.conf
install -m 755 -s libphp4.so \
	%{buildroot}%{_libdir}/apache-extramodules/

mkdir -p %{buildroot}%{ap_webdoc}
pushd %{buildroot}%{ap_webdoc}
ln -s ../../../..%{_docdir}/%{name}-%{version} %{name}
popd


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ -e ./%{name}-%{version} ] && rm -rf ./%{name}-%{version}

%pre
#Check config file sanity
%AP13pre

%post
if [ $1 = "1" ]; then 
   #We're in Install mode, add module to the config files
   for config in %{ap_base}/conf/{httpd,httpd-perl}.conf; do
     if [ -x %{_sbindir}/advxaddmod -a -e $config ]; then
       %{_sbindir}/advxaddmod $config \
	extramodules/libphp4.so mod_php4.c php4_module \
	before=perl define=HAVE_PHP4 addconf=conf/addon-modules/php.conf
     fi
   done
   %ADVXpost
fi

if [ $1 -gt 1 ]; then 
   #We're in *upgrade mode*. Since we can't be sure the configuration files
   #are sane, remove module from the conf files to clean them, re-add again 
   #in a way that the older module we're replacing won't try to erase (the 
   #post scripts were broken on some packages), and finally clean the module
   #specific config file so it's compatible with the upgrade.
   for config in %{ap_base}/conf/{httpd,httpd-perl}.conf; do
     if [ -x %{_sbindir}/advxdelmod -a -e $config ]; then
       %{_sbindir}/advxdelmod $config \
	extramodules/libphp4.so mod_php4.c php4_module \
	define=HAVE_PHP4 addconf=conf/addon-modules/php.conf
     fi
     if [ -x %{_sbindir}/advxaddmod -a -e $config ]; then
       %{_sbindir}/advxaddmod $config \
	extramodules/libphp4.so mod_php4.c php4_module \
	before=perl define=HAVE_PHP4 addconf=conf/addon-modules/php.conf
     fi
   done
   if [ -x %{_sbindir}/advxfixconf ]; then
       %{_sbindir}/advxfixconf %{ap_base}/conf/addon-modules/php.conf \
	libphp4.so mod_php4.c php4_module ifmodule
   fi
   %ADVXpost
fi

%postun
if [ $1 = "0" ]; then 
   for config in %{ap_base}/conf/{httpd,httpd-perl}.conf; do
     if [ -x %{_sbindir}/advxdelmod -a -e $config ]; then
       %{_sbindir}/advxdelmod $config \
	extramodules/libphp4.so mod_php4.c php4_module \
	define=HAVE_PHP4 addconf=conf/addon-modules/php.conf
     fi
   done
   %ADVXpost
fi


%files 
%defattr(-,root,root)
%{_libdir}/apache-extramodules/libphp4.so
%config(noreplace) %{ap_base}/conf/addon-modules/php.conf
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/*
%{ap_webdoc}/*

%changelog
* Tue Jun 22 2004 Vincent Danen <vdanen@annvix.org> 4.3.7-1avx
- Annvix build
- php 4.3.7

* Mon May 17 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- first OpenSLS build
- tidy spec
- apache 1.3.31
- php 4.3.6

* Sun Nov 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for apache 1.3.29
- built for php 4.3.4

* Thu Sep 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3.3-3mdk
- fix deps

* Mon Sep 15 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.3-2mdk
- require php-ini

* Mon Sep 15 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.3-1mdk
- rebuild for new apache

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.3.2-3mdk
- yet another buildrequires

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.3.2-2mdk
- buildrequires

* Thu Jun 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built against php v4.3.2
- misc spec file fixes

* Mon Feb 17 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.1-1mdk
- rebuild for it to show new PHP version in signature
  (even if nothing has changed)

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-3mdk
- new macros from ADVX-build

* Sat Jan 18 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-2mdk
- rebuilt with new openssl

* Mon Jan  6 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-1mdk
- New 4.3.0 release
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Fri Nov  8 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-3mdk
- Rebuild for Cooker

* Mon Oct 28 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-2mdk
- Rebuild with new apache

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3 maintenance release

* Thu Aug 22 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.2-1mdk
- 4.2.2 security update

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 4.2.1-3mdk
- rebuild (so that it builds with "-D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64")
  => fix segfault

* Wed Jun 26 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-2mdk
- new apache.

* Wed May 22 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- Build with new php.

* Thu May 16 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-2mdk
- Build with gcc 3.1.

* Tue Apr 30 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- misc spec file fixes
	- PHP 4.2.0

* Mon Apr 15 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.2-2mdk
- Apache 1.3.24.
- Update perl version in BuildRequires.

* Mon Mar 02 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-1mdk
- 4.1.2 = 4.1.1 + patch, but needed to recompile because Zend optimizer and
  other addons won't work if the API doesn't say 4.1.2

* Mon Feb 04 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-2mdk
- Rebuild against latest apache.

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-1mdk
- PHP 4.1.1.

* Tue Dec 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-1mdk
- PHP 4.1.0.

* Thu Nov 22 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-8mdk
- Rebuild to fix invalid-packager warning (rpmlint).

* Tue Oct 16 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-7mdk
- apache 1.3.22.

* Thu Oct 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-6mdk
- make rpmlint happier.

* Mon Sep 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-5mdk
- Provides the Obsoletes for compatibility.

* Wed Aug 29 2001 Philippe Libat <philippe@mandrakesoft.com> 4.0.6-4mdk
- libgdbm2

* Wed Jul 11 2001 Philippe Libat <philippe@mandrakesoft.com> 4.0.6-3mdk
- new apache version

* Mon Jul  9 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-2mdk
- removed Obsoletes: php-mysql

* Wed Jul  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-1mdk
- 4.0.6
- s/Copyright/License/

* Thu Apr 12 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-6mdk
- fix requires

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-5mdk
- fix upgrade scripts (for good this time I hope)

* Wed Mar 28 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-4mdk
- Put mod_php into its own package so we don't have to recompile php
  for each apache minor release
