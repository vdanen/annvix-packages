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

%define libxext		%mklibname xext 6

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


%package -n %{libxext}
Summary:	Misc X Extension Library
Group:		Development/C
Conflicts:	libxorg-x11 < 7.0
Provides:	%{name} = %{version}

%description -n %{libxext}
Misc X Extension Library


%package -n %{libxext}-devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libxext} = %{version}
Requires:	x11-proto-devel >= 1.0.0
Provides:	libxext-devel = %{version}-%{release}
Conflicts:	libxorg-x11-devel < 7.0

%description -n %{libxext}-devel
Development files for %{name}


%package -n %{libxext}-static-devel
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{libxext}-devel = %{version}
Provides:	libxext-static-devel = %{version}-%{release}
Conflicts:	libxorg-x11-static-devel < 7.0

%description -n %{libxext}-static-devel
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


%post -n %{libxext} -p /sbin/ldconfig
%postun -n %{libxext} -p /sbin/ldconfig

%files -n %{libxext}
%defattr(-,root,root)
%{_libdir}/libXext.so.6
%{_libdir}/libXext.so.6.4.0

%files -n %{libxext}-devel
%defattr(-,root,root)
%{_libdir}/libXext.so
%{_libdir}/libXext.la
%{_libdir}/pkgconfig/xext.pc
%{_mandir}/man3/*.3*.bz2

%files -n %{libxext}-static-devel
%defattr(-,root,root)
%{_libdir}/libXext.a


%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8