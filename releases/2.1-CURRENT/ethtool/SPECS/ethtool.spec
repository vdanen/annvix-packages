#
# spec file for package ethtool
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ethtool
%define version		3
%define release		%_revrel

Summary:	Ethernet settings tool for network cards
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://sourceforge.net/projects/gkernel/
Source:		http://prdownloads.sourceforge.net/gkernel/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
This utility allows querying and changing of ethernet card settings, such
as speed, port, and autonegotiation.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{_sbindir}/ethtool

%files doc
%defattr(-,root,root)
%doc AUTHORS NEWS


%changelog
* Tue Jul 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 3
- first Annvix package (needed by new initscripts)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
