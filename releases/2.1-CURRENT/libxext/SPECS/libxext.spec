#
# spec file for package libxext
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libxext
%define version 	1.0.3
%define release 	%_revrel

%define major		6
%define libname		%mklibname xext %{major}
%define devname		%mklibname xext -d
%define odevname	%mklibname xext 6 -d
%define staticdevname	%mklibname xext -d -s
%define ostaticdevname	%mklibname xext 6 -d -s

Summary:	Misc X Extension Library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Development/C
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libXext-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	libxau-devel >= 1.0.0
BuildRequires:	libx11-devel >= 1.0.0
BuildRequires:	libxdmcp-devel >= 1.0.0


%description
Misc X Extension Library.


%package -n %{libname}
Summary:	Misc X Extension Library
Group:		Development/C
Conflicts:	libxorg-x11 < 7.0
Provides:	%{name} = %{version}

%description -n %{libname}
Misc X Extension Library


%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	x11-proto-devel >= 1.0.0
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{odevname}
Conflicts:	libxorg-x11-devel < 7.0

%description -n %{devname}
Development files for %{name}


%package -n %{staticdevname}
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{devname} = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%{ostaticdevname}
Conflicts:	libxorg-x11-static-devel < 7.0

%description -n %{staticdevname}
Static development files for %{name}


%prep
%setup -q -n libXext-%{version}


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
%{_libdir}/libXext.so.%{major}*

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/libXext.so
%{_libdir}/libXext.la
%{_libdir}/pkgconfig/xext.pc
%{_mandir}/man3/*.3*.bz2

%files -n %{staticdevname}
%defattr(-,root,root)
%{_libdir}/libXext.a


%changelog
* Sun Sep 9 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- implement devel naming policy
- implement library provides policy

* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
