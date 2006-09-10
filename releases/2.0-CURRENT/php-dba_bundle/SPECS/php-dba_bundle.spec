#
# spec file for package php-dba_bundle
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		php-%{modname}_bundle
%define version		%{phpversion}
%define release		%_revrel

%define phpversion	5.1.4
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		dba
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		16_%{modname}.ini


Summary:	The DBA extension module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= 5.1.4
BuildRequires:	gdbm-devel, db4-devel

Requires:	php >= 5.1.2

%description
This is a dynamic shared object (DSO) for PHP that will add flat-file
databases (DBA) support (gdbm, db4, cdb, etc.).

%prep
%setup -c -T
cp -dpR %{_usrsrc}/php-devel/extensions/%{dirname}/* .


%build
phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-gdbm \
    --with-db4 \
    --with-cdb \
    --with-flatfile \
    --with-inifile

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
* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new db4

* Sun Jun 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- remove docs

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- php 5.1.4

* Thu Mar 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- php 5.1.2
- stricter permissions and spec cleanups
- group is now Development/PHP

* Wed Jan 18 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- php 4.4.2

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
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

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-2avx
- rebuild against new gdbm

* Thu Dec 16 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-1avx
- php 4.3.10

* Wed Sep 29 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.9-1avx
- php 4.3.9

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
- use the %%configure2_5x macro (oden)
- move scandir to /etc/php.d
- own docdir

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

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-4mdk
- built for 4.3.3
- misc spec file fixes
- fix explicit-lib-dependency

* Sun Aug 24 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-3mdk
- rebuild against libdb4.1

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 4.3.2-2mdk
- Rebuild to fix bad signature

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild

* Thu Feb 20 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-4mdk
- fix requires

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-3mdk
- rebuild

* Thu Jan 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-2mdk
- added db4 support

* Sun Jan  5 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-1mdk
- New 4.3.0 release
- Totally macroize based on suggestions from Alexander Skwar
- New method of installing extensions thanks to Oden Eriksson
- Use phpize since it now works with this module
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3 maintenance release
- Do not reload apache

* Thu Aug 22 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.2-1mdk
- Rebuild for 4.2.2
- Macroize a bit more, make version depend on "php -v"

* Fri May 31 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-2mdk
- rebuild.

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.1

* Thu May 02 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-2mdk
- fix error in Prereq (thanks to Oden).

* Wed May 01 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- renamed the php-dba_gdbm_db3 package to php-dba_bundle
	- added cdb support
	- PHP 4.2.0

* Mon Mar 04 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-1mdk
- PHP 4.1.2

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-1mdk
- PHP 4.1.1.

* Tue Dec 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-1mdk
- PHP 4.1.0.

* Thu Oct 18 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-5mdk
- new db3

* Mon Sep 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-4mdk
- Provides the Obsoletes for compatibility.

* Tue Aug 28 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-3mdk
- s/libgdbm1/libgdbm2

* Fri Jul 13 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-2mdk
- rebuild against db3.2

* Wed Jul  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-1mdk
- 4.0.6
- s/Copyright/License/

* Thu Apr 12 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-6mdk
- fix requires

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-5mdk
- fix post scripts for good 

* Mon Apr  2 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-4mdk
- Split dba_gdbm_db3 package from php package so that when a new gdbm, db2
  or db3 package comes out, we don't have to recompile php, only this module



# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
