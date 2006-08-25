#
# spec file for package php-pgsql
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		php-%{modname}
%define version		%{phpversion}
%define release		%_revrel

%define phpversion	4.4.4
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define realname	PostgreSQL
%define modname		pgsql
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		39_%{modname}.ini
%define mod_src		pgsql.c
%define mod_lib		"-lpq -lssl -lcrypto"
%define mod_def		"-DHAVE_PQESCAPE -DHAVE_PQSETNONBLOCKING -DHAVE_PGSQL_WITH_MULTIBYTE_SUPPORT -DHAVE_PQCMDTUPLES -DCOMPILE_DL_PGSQL -DHAVE_PGSQL"

Summary:	The %{realname} module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php4-devel
BuildRequires:	postgresql-devel, openssl-devel

Requires:	php4


%description
The %{name} package is a dynamic shared object (DSO) that adds
%{realname} support to PHP. PHP is an HTML-embedded scripting language. 
If you need %{realname} support for PHP applications, you will need to 
install this package in addition to the php package.


%prep
%setup -c -T
cp -dpR %{phpsource}/extensions/%{dirname}/* .


%build
phpize
%configure2_5x \
  --with-pgsql=shared,%{_prefix}

%make
mv modules/*.so .


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/

cat > README.%{modname} <<EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
To activate it, make sure a file /etc/php.d/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%doc README
%config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%{phpdir}/extensions/%{soname}


%changelog
* Thu Aug 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.4
- php 4.4.4

* Wed Aug 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.3
- php 4.4.3

* Wed Jan 18 2006 Vincent Danen <vdanen-at-build.annvix.org>
- php 4.4.2

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Nov 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-1avx
- php 4.4.1

* Wed Sep 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-1avx
- php 4.4.0

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-2avx
- rebuild

* Sat May 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-1avx
- php 4.3.11

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-3avx
- spec cleanups

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-2avx
- rebuild against latest openssl

* Fri Dec 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-1avx
- php 4.3.10

* Thu Sep 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.9-1avx
- php 4.3.9

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-2avx
- rebuild against new openssl

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
- use phpize and %%configure2_5x macro (oden)
- move scandir to /etc/php.d
- docdir

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- php 4.3.7

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- php 4.3.6

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-3sls
- minor spec cleanups

* Fri Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Mon Oct 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- 4.3.3

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-5mdk
- built for 4.3.3
- fix explicit-lib-dependency
- misc spec file fixes

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 4.3.2-4mdk
- Rebuild to fix bad signature

* Sun Jun 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-3mdk
- really build against new PostgreSQL libs

* Sun Jun 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-2mdk
- built against new PostgreSQL libs
- fix buildrequires: libpq3-devel

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild
- misc spec file fixes

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-4mdk
- rebuild

* Sat Jan 18 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-3mdk
- rebuilt with new openssl

* Thu Jan 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-2mdk
- corrected the mod_lib, mod_def, rlibs and blibs macros after
  some config.m4 and "pg_config --configure" investigation.

* Sun Jan  5 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-1mdk
- New 4.3.0 release
- Totally macroize based on suggestions from Alexander Skwar
- New method of installing extensions thanks to Oden Eriksson
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3 maintenance release
- Do not reload apache

* Sun May 26 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-2mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.1

* Mon Apr 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.0

* Mon Mar 04 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-1mdk
- PHP 4.1.2

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-1mdk
- PHP 4.1.1.

* Tue Dec 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-1mdk
- PHP 4.1.0.

* Thu Nov 15 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-4mdk
- Fix no-url and invalid-packager warnings in rpmlint
- Update postgresql version to 7.1.3.

* Mon Sep 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-3mdk
- Provides the Obsoletes (made a mistake in 2mdk).

* Mon Sep 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-2mdk
- Provides the Obsoletes for compatibility.

* Wed Jul  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-1mdk
- 4.0.6
- s/Copyright/License/

* Thu Apr 12 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-6mdk
- fix requires

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-5mdk
- fix post scripts for good 

* Mon Apr  2 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-4mdk
- Split pgsql package from php package so that when a new pgsql 
  package comes out, we don't have to recompile php, only this module

