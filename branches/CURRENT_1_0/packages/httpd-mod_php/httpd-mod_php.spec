%define name	%{ap_name}-%{mod_name}
%define version %{ap_version}_%{phpversion}
%define release	2avx

%define phpsource	%{_prefix}/src/php-devel
%{expand:%(cat /usr/src/php-devel/PHP_BUILD||(echo -e "error: failed build dependencies:\n        php-devel >= 430 (4.3.0) is needed by this package." >/dev/stderr;kill -2 $PPID))}

%ifarch x86_64 amd64
%define dbver	lib64db4.1
%else
%define dbver	libdb4.1
%endif
%define ldb	-ldb-4.1

# Module-Specific definitions
%define mod_name	mod_php
%define mod_conf	70_%{mod_name}.conf
%define mod_so		%{mod_name}4.so
%define phpsource	/usr/src/php-devel
%define extname		apache2handler

# New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}
%{expand:%%global ap_version %(%{apxs} -q ap_version)}

Summary:	The PHP4 HTML-embedded scripting language for use with %{ap_name}.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net/ 
Source1:	%{mod_conf}.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:  %{dbver}-devel
BuildRequires:	gdbm-devel
BuildRequires:	byacc
BuildRequires:	glibc-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	expat-devel
BuildRequires:	zlib-devel
BuildRequires:	php%{libversion}-devel
BuildRequires:	pam-devel libintl
BuildRequires:	db1-devel
BuildRequires:	php-devel >= 4.3.0
# Standard ADVX requires
BuildRequires:	%{ap_name}-devel >= 2.0.44-1mdk
BuildPreReq:	ADVX-build >= 9.2

Requires:	%{dbver}
Requires:	openssl
Requires:	php-ini
Provides:	mod_php3
Provides:	php3
Provides:	phpfi
Obsoletes:	mod_php3
Provides:	php3
Provides:	phpfi
Provides:	mod_php
Provides:	php
Provides:	php4
Provides:	php%{libversion}
Provides:	phpapache
Provides:	php430
Obsoletes:	php430
# Standard ADVX requires
Prereq:		%{ap_name} = %{ap_version}
Prereq:		%{ap_name}-conf
Provides: 	ADVXpackage
Provides:	AP20package

%description
PHP is an HTML-embedded scripting language.  PHP attempts to make it
easy for developers to write dynamically generated web pages.  PHP
also offers built-in database integration for several commercial
and non-commercial database management systems, so writing a
database-enabled web page with PHP is fairly simple.  The most
common use of PHP coding is probably as a replacement for CGI
scripts.  The %{name} module enables the %{ap_name} web server to
understand and process the embedded PHP language in web pages.

This package contains PHP version 4. You'll also need to install the
%{ap_name} web server.

%prep

[ -e ./%{extname} ] && rm -fr ./%{extname}
cp -dpR %{phpsource}/sapi/%{extname} .
cd %{extname}

cp %{phpsource}/PHP_FAQ.php .

%build
cd %{extname}
#Seems apxs (or libtool) is broken, and we can't use the -o %{mod_so}
#so instead we rename the 1st code file, and apxs will choose that name
#for the soname.

cp sapi_apache2.c mod_php4.c
cp %{phpsource}/internal_functions.c .

%{apxs} \
    `php-config --includes` \
    `apr-config --link-ld --libs` \
    `apu-config --link-ld --libs` \
    -I%{phpsource} \
    -I. -lphp_common %{ldb}  \
    -c mod_php4.c apache_config.c php_functions.c  \
    internal_functions.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
cd %{extname}

%ADVXinstlib
%ADVXinstconf %{SOURCE1} %{mod_conf}
%ADVXinstdoc %{name}-%{version}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ -e ./%{extname} ] && rm -fr ./%{extname}

%post
%ADVXpost

%postun
%ADVXpost

%files
%defattr(-,root,root)
%doc %{extname}/PHP_FAQ.php 
%config(noreplace) %{ap_confd}/%{mod_conf}
%{ap_extralibs}/%{mod_so}
%{ap_webdoc}/*

%changelog
* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49_4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_4.3.7-1sls
- php 4.3.7

* Fri May 09 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_4.3.6-1sls
- build for php 4.3.6 and apache 2.0.49

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_4.3.4-4sls
- fix the wierd BuildRequires for php-devel

* Tue Jan 06 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_4.3.4-3sls
- BuildRequires: libintl, not libintl2; db4-devel not libdb4.1-devel (for
  amd64)

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_4.3.4-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_4.3.4-1mdk
- fix versioning

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_4.3.4-1mdk
- built for php 4.3.4
- fix explicit-lib-dependency

* Mon Jul 21 2003 David BAUDENS <baudens@mandrakesoft.com> 2.0.47_4.3.2-2mdk
- Rebuild to fix Bad siganture

* Wed Jul 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_4.3.2-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Wed Jun 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_4.3.2-3mdk
- require php-ini (;))

* Wed Jun 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_4.3.2-2mdk
- require php.ini
- updated S1
- misc spec file fixes

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_4.3.2-1mdk
- rebuild for apache v2.0.46 and php v4.3.2
- use the new apache2handler SAPI instead
- misc spec file fixes
- build against db4 not both db3 and db4

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_4.3.1-1mdk
- cosmetic rebuild for apache v2.0.45

* Thu Feb 20 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_4.3.1-2mdk
- fix provides

* Mon Feb 17 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_4.3.1-1mdk
- rebuild for it to show new PHP version in signature
  (even if nothing has changed)

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_4.3.0-2mdk
- rebuild

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_4.3.0-1mdk
- rebuilt for apache v2.0.44

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_4.3.0-6mdk
- fix buildrequires apache2-devel >= 2.0.43-5mdk, as 
  pointed out by Olivier Thauvin

* Sun Jan 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_4.3.0-5mdk
- really rebuilt against rebuilt buildrequires

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_4.3.0-4mdk
- rebuilt against rebuilt buildrequires

* Thu Jan 08 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.43_4.3.0-3mdk
- Rebuilt with the new apache-devel that uses /usr/sbin/apxs2 and
  /usr/include/apache2

* Thu Jan 08 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.43_4.3.0-2mdk
- Rebuild on the cluster, try #1, will need to be rebuilt again
  when everything is synchronized

* Mon Jan 06 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.43_4.3.0-1mdk
- rebuilt for new PHP 4.3.0
- macroize db3/db4 so we can easily recompile between 9.0 and Cooker
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Sat Nov 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_4.2.3-2mdk
- rebuilt for/against apache2 where dependencies has changed in apr
- a lot of requires and buildrequires changes

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_4.2.3-1mdk
- rebuilt for/against new apache2 version 2.0.43 (even though 2.0.42 and 
  2.0.43 are binary compatible, we have to consider rpm dependencies)
- sanitize rpm package versioning
- misc spec file fixes

* Thu Sep 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42_4.2.3-2mdk
- rebuilt against new apache v2.0.42

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX_4.2.3-1mdk
- 4.2.3 maintenance release

* Wed Sep  3 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX_4.2.2-2mdk
- Add BuildRequires ADVX-build

* Wed Aug 28 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX_4.2.2-1mdk
- First Apache 2 module to comply with the ADVX policy at:
  http://advx.org/devel/policy.php
