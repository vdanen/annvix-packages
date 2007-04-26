#
# spec file for package libx11
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libx11
%define version 	1.1.1
%define release 	%_revrel

%define libx11		%mklibname x11_ 6
%define libxorgoldname	%mklibname xorg-x11

Summary:	X library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Development/C
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libX11-%{version}.tar.bz2
Patch0:		libx11-CVE-2007-1667.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libxau-devel >= 1.0.0
BuildRequires:	libxdmcp-devel >= 1.0.0
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	x11-xtrans-devel >= 1.0.0

Provides:	libxorg-x11
Obsoletes:	libxorg-x11

%description
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).


%package -n %{libx11}
Summary:	X Library
Group:		Development/C
Conflicts:	%{libxorgoldname} < 7.0
Provides:	%{name} = %{version}

%description -n %{libx11}
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).


%package -n %{libx11}-devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libx11} = %{version}
Requires:	x11-proto-devel >= 1.0.0
Provides:	libx11-devel = %{version}-%{release}
Conflicts:	%{libxorgoldname}-devel < 7.0

%description -n %{libx11}-devel
%{name} includes the libraries, header files and documentation
you'll need to develop programs which run in X clients. X11 includes
the base Xlib library as well as the Xt and Xaw widget sets.


%package -n %{libx11}-static-devel
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{libx11}-devel = %{version}
Conflicts:	%{libxorgoldname}-static-devel < 7.0
Provides:	libx11-static-devel = %{version}-%{release}

%description -n %{libx11}-static-devel
Static development files for %{name}


%package common
Summary:	Common files used by the X.org
Group:		System/X11

%description common
Common files used by X.org


%prep
%setup -q -n libX11-%{version}
%patch0 -p1 -b .cve-2007-1667


%build
aclocal && libtoolize --force && automake && autoconf
%configure2_5x \
    --x-includes=%{_includedir} \
    --x-libraries=%{_libdir} \
    --without-xcb

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libx11}
grep -q "^%{_prefix}/X11R6/lib$" /etc/ld.so.conf || echo "%{_prefix}/X11R6/lib" >> /etc/ld.so.conf
/sbin/ldconfig


%postun -n %{libx11}
if [ "$1" = "0" ]; then
    rm -f /etc/ld.so.conf.new
    grep -v "^%{_prefix}/X11R6/lib$" /etc/ld.so.conf > /etc/ld.so.conf.new
    mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi
/sbin/ldconfig


%files -n %{libx11}
%defattr(-,root,root)
%{_libdir}/libX11.so.6
%{_libdir}/libX11.so.6.2.0

%files -n %{libx11}-devel
%defattr(-,root,root)
%{_mandir}/man3/*.3.bz2
%{_libdir}/libX11.so
%{_libdir}/libX11.la
%{_libdir}/pkgconfig/x11.pc
%{_includedir}/X11/cursorfont.h
%{_includedir}/X11/ImUtil.h
%{_includedir}/X11/Xlocale.h
%{_includedir}/X11/Xcms.h
%{_includedir}/X11/Xlibint.h
%{_includedir}/X11/Xlib.h
%{_includedir}/X11/Xresource.h
%{_includedir}/X11/Xregion.h
%{_includedir}/X11/Xutil.h
%{_includedir}/X11/XlibConf.h
%{_includedir}/X11/XKBlib.h

%files -n %{libx11}-static-devel
%defattr(-,root,root)
%{_libdir}/libX11.a

%files common
%defattr(-,root,root)
%dir %{_datadir}/X11
%dir %{_datadir}/X11/locale
%{_datadir}/X11/locale/*
%{_libdir}/X11/Xcms.txt
%{_datadir}/X11/XErrorDB
%{_datadir}/X11/XKeysymDB

%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.1.5
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
