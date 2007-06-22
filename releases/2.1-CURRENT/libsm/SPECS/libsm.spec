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

%define libname		%mklibname sm 6
%define devname		%mklibname sm -d
%define staticdevname	%mklibname sm -d -s
%define odevname	%mklibname sm 6 -d

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


%package -n %{libname}
Summary:	X Session Management Library
Group:		Development/C
Conflicts:	libxorg-x11 < 7.0
Provides:	%{name} = %{version}

%description -n %{libname}
This is the X Session Management Library.


%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	libice-devel >= 1.0.0
Requires:	x11-proto-devel >= 1.0.0
Provides:	%{name}-devel = %{version}-%{release}
Provides:	sm-devel = %{version}-%{release}
Obsoletes:	%{odevname}
Conflicts:	libxorg-x11-devel < 7.0

%description -n %{devname}
Development files for %{name}


%package -n %{staticdevname}
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{devname} = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	sm-static-devel = %{version}-%{release}
Conflicts:	libxorg-x11-static-devel < 7.0

%description -n %{staticdevname}
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


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libSM.so.6
%{_libdir}/libSM.so.6.0.0

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/libSM.so
%{_libdir}/libSM.la
%{_libdir}/pkgconfig/sm.pc
%{_includedir}/X11/SM/SM.h
%{_includedir}/X11/SM/SMlib.h
%{_includedir}/X11/SM/SMproto.h

%files -n %{staticdevname}
%defattr(-,root,root)
%{_libdir}/libSM.a


%changelog
* Thu Jun 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.1
- implement devel naming policy
- implement library provides policy

* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.1
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
