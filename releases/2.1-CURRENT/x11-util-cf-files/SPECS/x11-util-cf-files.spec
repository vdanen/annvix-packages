#
# spec file for package x11-util-cf-files
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		x11-util-cf-files
%define version 	1.0.2
%define release 	%_revrel

Summary:	Templates for imake
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Development/C
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/util/xorg-cf-files-%{version}.tar.bz2
Patch0:		xorg-cf-files-1.0.2-mdv-mdvconfig.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Templates for imake.


%prep
%setup -q -n xorg-cf-files-%{version}
%patch0 -p1 -b .mdvconfig


%build
%configure2_5x \
    --with-config-dir=%{_datadir}/X11/config \
    --x-includes=%{_includedir}\
    --x-libraries=%{_libdir}

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_datadir}/X11/config
%{_datadir}/X11/config/*


%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
