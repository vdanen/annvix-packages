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
%define version		2.0
%define release		%_revrel

%define aa_profilesdir	%{_sysconfdir}/apparmor/profiles

Summary:	AppArmor profiles that are loaded into the apparmor kernel module
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	%{name}-%{version}-35.tar.gz

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

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/apparmor.d
%dir %{_sysconfdir}/apparmor.d/abstractions
%dir %{_sysconfdir}/apparmor.d/program-chunks
%dir %{_sysconfdir}/apparmor.d/tunables
%dir %{aa_profilesdir}
%dir %{aa_profilesdir}/extras
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/apparmor.d/*
%attr(0640,root,root) %config(noreplace) %{aa_profilesdir}/extras/*


%changelog
* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- first Annvix package
