#
# spec file for package libsm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libsm
%define version 	1.0.1
%define release 	%_revrel

%define libsm		%mklibname sm 6

Summary:	X Session Management Library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Development/C
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libSM-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	x11-xtrans-devel >= 1.0.0
BuildRequires:	libice-devel >= 1.0.0


%description
X Session Management Library.


%package -n %{libsm}
Summary:	X Session Management Library
Group:		Development/C
Conflicts:	libxorg-x11 < 7.0
Provides:	%{name} = %{version}

%description -n %{libsm}
This is the X Session Management Library.


%package -n %{libsm}-devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libsm} = %{version}
Requires:	libice-devel >= 1.0.0
Requires:	x11-proto-devel >= 1.0.0
Provides:	libsm-devel = %{version}-%{release}
Conflicts:	libxorg-x11-devel < 7.0

%description -n %{libsm}-devel
Development files for %{name}


%package -n %{libsm}-static-devel
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{libsm}-devel = %{version}
Provides:	libsm-static-devel = %{version}-%{release}
Conflicts:	libxorg-x11-static-devel < 7.0

%description -n %{libsm}-static-devel
Static development files for %{name}


%prep
%setup -q -n libSM-%{version}


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


%post -n %{libsm} -p /sbin/ldconfig
%postun -n %{libsm} -p /sbin/ldconfig

%files -n %{libsm}
%defattr(-,root,root)
%{_libdir}/libSM.so.6
%{_libdir}/libSM.so.6.0.0

%files -n %{libsm}-devel
%defattr(-,root,root)
%{_libdir}/libSM.so
%{_libdir}/libSM.la
%{_libdir}/pkgconfig/sm.pc
%{_includedir}/X11/SM/SM.h
%{_includedir}/X11/SM/SMlib.h
%{_includedir}/X11/SM/SMproto.h

%files -n %{libsm}-static-devel
%defattr(-,root,root)
%{_libdir}/libSM.a


%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.1
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
