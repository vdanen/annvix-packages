#
# spec file for package libxdmcp
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libxdmcp
%define version 	1.0.2
%define release 	%_revrel

%define libxdmcp	%mklibname xdmcp 6

Summary:	X Display Manager Control Protocol library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Development/C
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libXdmcp-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1


%description
X Display Manager Control Protocol library


%package -n %{libxdmcp}
Summary:	Development files for %{name}
Group:		Development/C
Conflicts:	libxorg-x11 < 7.0
Provides:	%{name} = %{version}

%description -n %{libxdmcp}
X Display Manager Control Protocol library


%package -n %{libxdmcp}-devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libxdmcp} = %{version}
Requires:	x11-proto-devel >= 1.0.0
Provides:	libxdmcp-devel = %{version}-%{release}
Conflicts:	libxorg-x11-devel < 7.0

%description -n %{libxdmcp}-devel
Development files for %{name}


%package -n %{libxdmcp}-static-devel
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{libxdmcp}-devel = %{version}
Provides:	libxdmcp-static-devel = %{version}-%{release}
Conflicts:	libxorg-x11-static-devel < 7.0

%description -n %{libxdmcp}-static-devel
Static development files for %{name}


%prep
%setup -q -n libXdmcp-%{version}


%build
%configure2_5x \
    --x-includes=%{_includedir} \
    --x-libraries=%{_libdir}

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libxdmcp} -p /sbin/ldconfig
%postun -n %{libxdmcp} -p /sbin/ldconfig

%files -n %{libxdmcp}
%defattr(-,root,root)
%{_libdir}/libXdmcp.so.6
%{_libdir}/libXdmcp.so.6.0.0

%files -n %{libxdmcp}-devel
%defattr(-,root,root)
%{_libdir}/libXdmcp.la
%{_libdir}/libXdmcp.so
%{_libdir}/pkgconfig/xdmcp.pc
%{_includedir}/X11/Xdmcp.h

%files -n %{libxdmcp}-static-devel
%defattr(-,root,root)
%{_libdir}/libXdmcp.a


%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
