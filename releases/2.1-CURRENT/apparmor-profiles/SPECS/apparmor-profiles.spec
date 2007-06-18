#
# spec file for package apparmor-profiles
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		apparmor-profiles
%define version		2.0.2
%define release		%_revrel

%define svnrel		563

%define aa_profilesdir	%{_sysconfdir}/apparmor/profiles

Summary:	AppArmor profiles that are loaded into the apparmor kernel module
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	%{name}-%{version}-%{svnrel}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	apparmor-parser

%description
Base profiles. AppArmor is a file and network mandatory access control
mechanism. AppArmor confines processes to the resources allowed by the
systems administrator and can constrain the scope of potential security
vulnerabilities.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} \
     EXTRASDIR=%{buildroot}%{aa_profilesdir}/extras/ \
     install

# remove the profiles we don't want as profiles are shipped per-package now
rm -f %{buildroot}%{_profiledir}/{bin,sbin,usr.sbin,usr.bin}.*

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_profiledir}
%dir %{_profiledir}/abstractions
%dir %{_profiledir}/program-chunks
%dir %{_profiledir}/tunables
%dir %{aa_profilesdir}
%dir %{aa_profilesdir}/extras
%attr(0640,root,root) %config(noreplace) %{_profiledir}/*
%attr(0640,root,root) %config(noreplace) %{aa_profilesdir}/extras/*


%changelog
* Mon Jul 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- remove the profiles we don't want (leave the "extras" stuff as examples)

* Tue Jul 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- 2.0.2-563

* Fri Nov 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- r119 (October snapshot)
- drop P0-P2: applied upstream

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- don't leave patch suffixes lying around

* Wed Aug 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- sync some patches with SUSE to match support in SLE10:
  - updated to revision 50
  - P0: add support for the new m flag and Px/Ux modes
  - P1: fixes for named slave zone transfers
  - P2: other profile fixes

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- remove locales

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
