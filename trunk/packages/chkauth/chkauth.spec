%define name	chkauth
%define version 0.3
%define release 1sls
	
Summary:	Script to change authentification method (local, NIS, LDAP)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Boot and Init
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch:	noarch

Prefix:		%{_prefix}
Requires:	perl >= 5.0

%description
Chkauth is a program to change the authentification method 
on a system. Chkauth always set the file method in first place, but 
you can only select the second authentification method this way. 

Three kind of authentification are accepted : local (file), NIS (yp) 
and LDAP. 

%prep
%setup

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8/
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
install chkauth $RPM_BUILD_ROOT/%{_sbindir}
install chkauth.8 $RPM_BUILD_ROOT/%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/*/*

%changelog
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

