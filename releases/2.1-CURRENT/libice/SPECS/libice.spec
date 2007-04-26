#
# spec file for package libice
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libice
%define version 	1.0.3
%define release 	%_revrel

%define libice		%mklibname ice 6

Summary:	X Inter Client Exchange Library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Development/C
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libICE-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	x11-xtrans-devel >= 1.0.0


%description
libice provides an interface to ICE, the Inter-Client Exchange protocol.
Motivated by issues arising from the need for X Window System clients to
share data with each other, the ICE protocol provides a generic framework for
building protocols on top of reliable, byte-stream transport connections. It
provides basic mechanisms for setting up and shutting down connections, for
performing authentication, for negotiating versions, and for reporting
errors.


%package -n %{libice}
Summary:	X Inter Client Exchange Library
Group:		Development/C
Conflicts:	libxorg-x11 < 7.0
Provides:	%{name} = %{version}

%description -n %{libice}
libice provides an interface to ICE, the Inter-Client Exchange protocol.
Motivated by issues arising from the need for X Window System clients to
share data with each other, the ICE protocol provides a generic framework for
building protocols on top of reliable, byte-stream transport connections. It
provides basic mechanisms for setting up and shutting down connections, for
performing authentication, for negotiating versions, and for reporting
errors.


%package -n %{libice}-devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libice} = %{version}
Requires:	x11-proto-devel >= 1.0.0
Provides:	libice-devel = %{version}-%{release}
Conflicts:	libxorg-x11-devel < 7.0

%description -n %{libice}-devel
Development files for %{name}


%package -n %{libice}-static-devel
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{libice}-devel = %{version}
Provides:	libice-static-devel = %{version}-%{release}
Conflicts:	libxorg-x11-static-devel < 7.0

%description -n %{libice}-static-devel
Static development files for %{name}


%prep
%setup -q -n libICE-%{version}


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


%post -n %{libice} -p /sbin/ldconfig
%postun -n %{libice} -p /sbin/ldconfig

%files -n %{libice}
%defattr(-,root,root)
%{_libdir}/libICE.so.6
%{_libdir}/libICE.so.6.3.0

%files -n %{libice}-devel
%defattr(-,root,root)
%{_libdir}/libICE.so
%{_libdir}/libICE.la
%{_libdir}/pkgconfig/ice.pc
%{_includedir}/X11/ICE/ICEutil.h
%{_includedir}/X11/ICE/ICE.h
%{_includedir}/X11/ICE/ICEproto.h
%{_includedir}/X11/ICE/ICEconn.h
%{_includedir}/X11/ICE/ICElib.h
%{_includedir}/X11/ICE/ICEmsg.h

%files -n %{libice}-static-devel
%defattr(-,root,root)
%{_libdir}/libICE.a


%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
