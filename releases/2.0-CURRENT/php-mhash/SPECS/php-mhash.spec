#
# spec file for package php-mhash
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

%define phpversion	5.1.4
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		mhash
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		30_%{modname}.ini

Summary:	The Mhash module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= 5.1.4
BuildRequires:	libmhash-devel

Requires:	php

%description
This is a dynamic shared object (DSO) for PHP that will add mhash
support.


%prep
%setup -c -T
cp -dpR %{phpsource}/extensions/%{dirname}/* .


%build
phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{phpdir}/extensions/%{soname}


%changelog
* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new mhash

* Sun Jun 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- remove docs

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- php 5.1.4

* Wed Apr 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- php 5.1.2
- stricter permissions and spec cleanups
- group is now Development/PHP

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Nov 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-1avx
- php 4.4.1

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-2avx
- rebuild against new mhash

* Wed Sep 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-1avx
- php 4.4.0

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-2avx
- rebuild

* Sat May 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-1avx
- php 4.3.11

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-2avx
- spec cleanups

* Fri Dec 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-1avx
- php 4.3.10

* Thu Sep 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.9-1avx
- php 4.3.9

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
- use %%configure2_5x macro (oden)
- move scandir to /etc/php.d
- own docdir

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- php 4.3.7

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- php 4.3.6

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-4sls
- minor spec cleanups

* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-3sls
- fix Reqs/BuildReq's for amd64 (not very clean, but fix in mhash spec
  later)

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Wed Aug 27 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- built for php 4.3.3
- misc spec file fixes

* Thu Jun 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-2mdk
- built against new libmhash2

* Wed Jun 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Wed Feb 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- rebuilt against php-4.3.1

* Sun Jan 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-3mdk
- really rebuilt against rebuilt buildrequires

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-2mdk
- rebuilt against rebuilt buildrequires

* Fri Jan 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-1mdk
- built against php-4.3.0
- follow the spec file design as in main

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.3-2mdk
- rebuilt against latest BuildRequires

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3 maintenance release
- Do not reload apache

* Thu Aug 22 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.2-1mdk
- Rebuild for 4.2.2
- Macroize a bit more, make version depend on "php -v"

* Sun Jun  2 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.1-4mdk
- rebuilt against latest BuildRequires

* Mon May 27 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.1-3mdk
- rebuilt against php-4.2.1 this time (klama is wierd...)
- added Requires: php-common

* Mon May 27 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.1-2mdk
- misc spec file fixes

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.1

* Sun May 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.0-4mdk
- rebuilt with gcc3.1
- misc spec file fixes

* Thu May  2 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 4.2.0-3mdk
- Upload to contrib
- Rewrite SPEC to use the "generic" SPEC version as used in php-recode et.al.
- Somewhat based on Oden Eriksson's SPEC for php-mhash

* Sun Apr 28 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.0-2mdk
- misc spec file fixes

* Fri Apr 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.0-1mdk
- initial cooker contrib
- PHP 4.2.0

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
