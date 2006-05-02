#
# spec file for package chkauth
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		chkauth
%define version 	0.3
%define release 	%_revrel
	
Summary:	Script to change authentification method (local, NIS, LDAP)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
Source0:	%{name}-%{version}.tar.bz2
Patch0:		chkauth-0.3-avx-misc_fixes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	perl >= 5.0

%description
Chkauth is a program to change the authentification method 
on a system. Chkauth always set the file method in first place, but 
you can only select the second authentification method this way. 

Three kinds of authentification is accepted : local (file), NIS (yp) 
and LDAP. 


%prep
%setup -q
%patch0 -p0


%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_mandir}/man8/
mkdir -p %{buildroot}/%{_sbindir}
install -m 0750 chkauth %{buildroot}/%{_sbindir}
install -m 0644 chkauth.8 %{buildroot}/%{_mandir}/man8/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/*/*


%changelog
* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.3
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.3
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3-8avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3-7avx
- rebuild

* Mon Mar 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3-6avx
- update P0 with minor fixes

* Tue Mar 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3-5avx
- update P0 to made chkauth tell exactly what rpms are needed for LDAP
  all at once rather than one at a time
- fix some grammer annoyances

* Wed Jun 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.3-4avx
- fix chkauth to use pam_unix rather than pam_pwdb for password
  handling in system-auth when using LDAP (so we can use passwd to
  change LDAP passwords); updated P0

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.3-3avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 0.3-2sls
- minor spec cleanups
- remove %%prefix
- P1: to fix pam auth, should use pam_unix not pam_pwdb

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 0.3-1sls
- OpenSLS build
- tidy spec

* Fri Oct 17 2003  Vincent Danen <vdanen@mandrakesoft.com> 0.3-0.1.92mdk
- 0.3: don't use paths in system-auth so we don't have to worry about /lib
  vs. /lib64

* Wed Oct 15 2003  Vincent Danen <vdanen@mandrakesoft.com> 0.2-1.1.92mdk
- remove P0
- proper fixes for LDAP, use pam_pwdb, make sure it got integrated into CVS

* Tue Aug 26 2003 Pixel <pixel@mandrakesoft.com> 0.2-1mdk
- configure automount for ldap in nsswitch.conf (thanks to Buchan Milne)

* Mon May  5 2003  <vdanen@mandrakesoft.com> 0.1-8mdk
- fix LDAP stuff for system-auth (P0)

* Wed Aug  7 2002  <amaury@ke.mandrakesoft.com> 0.1-7mdk
- fixed numerous typos in the specfile

* Sat Feb 23 2002 Pixel <pixel@mandrakesoft.com> 0.1-6mdk
- fix stupid, dumb and ugly Makefile 
(including having the non-bzipped manpage chkauth.8 instead of chkauth.8.bz2, 
thanks to J.A. Magallon)

* Fri Feb 22 2002 Pixel <pixel@mandrakesoft.com> 0.1-5mdk
- fix ldap added twice in nsswitch.conf cuz code is crappy
- fix some temporary files in /tmp

* Fri Sep 21 2001 Vincent Saugey <vince@mandrakesoft.com> 0.1-4mdk
- Correct bug, in ldap host not found

* Thu Sep 20 2001 Vincent Saugey <vince@mandrakesoft.com> 0.1-3mdk
- Now use start/tls by default for LDAP auth

* Mon Jul  9 2001 Vincent Saugey <vince@mandrakesoft.com> 0.1-2mdk
- Add --pixel flag

* Thu Jul  5 2001 Vincent Saugey <vince@mandrakesoft.com> 0.1-1mdk
- First release !!

