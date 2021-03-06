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
%define version 	0.4
%define release 	%_revrel
	
Summary:	Script to change authentification method (local, NIS, LDAP)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://svn.annvix.org/cgi-bin/viewvc.cgi/tools/chkauth/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	perl >= 5.0

%description
chkauth is a program to change the authentication method on a system.

Two kinds of authentication are accepted : local (tcb), and LDAP. 


%prep
%setup -q


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
%{_sbindir}/chkauth
%{_mandir}/man8/chkauth.8*


%changelog
* Sat Feb 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.4
- 0.4: complete rewrite in bash (although still required perl);
  removes NIS and file support and adds tcb support

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.3
- remove pre-Annvix changelog

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
