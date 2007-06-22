#
# spec file for package libxau
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libxau
%define version 	1.0.3
%define release 	%_revrel

%define libname		%mklibname xau 6
%define devname		%mklibname xau -d
%define staticdevname	%mklibname xau -d -s
%define odevname	%mklibname xau 6 -d

Summary:	X authorization file management library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Development/C
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libXau-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1


%description
X authorization file management library


%package -n %{libname}
Summary:	X authorization file management library
Group:		Development/C
Conflicts:	libxorg-x11 < 7.0
Provides:	%{name} = %{version}

%description -n %{libname}
X authorization file management library


%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	x11-proto-devel >= 1.0.0
Provides:	%{name}-devel = %{version}-%{release}
Provides:	xau-devel = %{version}-%{release}
Obsoletes:	%{odevname}
Conflicts:	libxorg-x11-devel < 7.0

%description -n %{devname}
Development files for %{name}


%package -n %{staticdevname}
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{libname}-devel >= %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	xau-static-devel = %{version}-%{release}
Conflicts:	libxorg-x11-static-devel < 7.0

%description -n %{staticdevname}
Static development files for %{name}


%prep
%setup -q -n libXau-%{version}


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
%{_libdir}/libXau.so.6
%{_libdir}/libXau.so.6.0.0

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/pkgconfig/xau.pc
%{_includedir}/X11/Xauth.h
%{_libdir}/libXau.la
%{_libdir}/libXau.so
%{_mandir}/man3/Xau*

%files -n %{staticdevname}
%defattr(-,root,root)
%{_libdir}/libXau.a

%changelog
* Thu Jun 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- implement devel naming policy
- implement library provides policy

* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
