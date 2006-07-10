#
# spec file for package apparmor-utils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		apparmor-utils
%define version		2.0
%define release		%_revrel

%define _requires_exceptions perl(Immunix::Ycp)

Summary:	AppArmor userlevel utilities that are useful in creating AppArmor profiles
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Configuration
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	%{name}-%{version}-6377.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	perl(Date::Parse), perl(DBI), perl(File::Tail), perl(DBD::SQLite)
Requires:	apparmor-parser

%description
This package provides the aa-logprof, aa-genprof, aa-autodep,
aa-enforce, and aa-complain tools to assist with profile authoring;
this package also provides the aa-unconfined server information tool
and the aa-eventd event reporting system.


%prep
%setup -q


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} \
     BINDIR=%{buildroot}%{_sbindir} \
     PERLDIR=%{buildroot}%{perl_vendorlib}/Immunix \
     install

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%config %attr(0640,root,root) /etc/apparmor/*
%attr(0750,root,root) %{_sbindir}/*
%{perl_vendorlib}/Immunix
%dir %attr(0700,root,root) /var/log/apparmor


%changelog
* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- drop P0 as we've moved logger to /bin

* Wed Jun 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- P0: fix location of logger in genprof
- fix permissions

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- first Annvix package
