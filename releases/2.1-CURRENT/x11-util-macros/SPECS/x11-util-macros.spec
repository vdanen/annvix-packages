#
# spec file for package x11-util-macros
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		x11-util-macros
%define version 	1.1.5
%define release 	%_revrel

Summary:	Macros used for X.org development
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Development/C
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/util/util-macros-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

%description
Macros used for x.org development.


%prep
%setup -q -n util-macros-%{version}


%build
%configure
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_datadir}/aclocal/xorg-macros.m4
%{_datadir}/aclocal/xorgversion.m4


%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.1.5
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
