#
# spec file for package libxt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libxt
%define version 	1.0.5
%define release 	%_revrel

%define libxt		%mklibname xt 6

Summary:	X Toolkit Library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Development/C
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libXt-%{version}.tar.bz2
Patch1:		libxt-1.0.2-mdv-linking_cplusplus.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	libx11-devel >= 1.0.0
BuildRequires:	libsm-devel >= 1.0.0

%description
X Toolkit Library


%package -n %{libxt}
Summary:	X Toolkit Library
Group:		Development/C
Conflicts:	libxorg-x11 < 7.0
Provides:	%{name} = %{version}

%description -n %{libxt}
X Toolkit Library


%package -n %{libxt}-devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libxt} = %{version}
Requires:	x11-proto-devel >= 1.0.0
Requires:	libx11-devel >= 1.0.0
Requires:	libsm-devel >= 1.0.0
Provides:	libxt-devel = %{version}-%{release}
Conflicts:	libxorg-x11-devel < 7.0

%description -n %{libxt}-devel
Development files for %{name}


%package -n %{libxt}-static-devel
Summary:	Static development files for %{name}
Group:		Development/C
Requires:	%{libxt}-devel = %{version}
Provides:	libxt-static-devel = %{version}-%{release}
Conflicts:	libxorg-x11-static-devel < 7.0

%description -n %{libxt}-static-devel
Static development files for %{name}


%prep
%setup -q -n libXt-%{version}
%patch1 -p1 -b .cplusplus


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


%post -n %{libxt} -p /sbin/ldconfig
%postun -n %{libxt} -p /sbin/ldconfig


%files -n %{libxt}
%defattr(-,root,root)
%{_libdir}/libXt.so.6
%{_libdir}/libXt.so.6.0.0

%files -n %{libxt}-devel
%defattr(-,root,root)
%{_bindir}/makestrs
%{_libdir}/libXt.so
%{_libdir}/libXt.la
%{_libdir}/pkgconfig/xt.pc
%{_includedir}/X11/Core.h
%{_includedir}/X11/VarargsI.h
%{_includedir}/X11/RectObj.h
%{_includedir}/X11/TranslateI.h
%{_includedir}/X11/Vendor.h
%{_includedir}/X11/CallbackI.h
%{_includedir}/X11/ResConfigP.h
%{_includedir}/X11/IntrinsicI.h
%{_includedir}/X11/IntrinsicP.h
%{_includedir}/X11/ConstrainP.h
%{_includedir}/X11/Constraint.h
%{_includedir}/X11/InitialI.h
%{_includedir}/X11/EventI.h
%{_includedir}/X11/ObjectP.h
%{_includedir}/X11/Xtos.h
%{_includedir}/X11/CreateI.h
%{_includedir}/X11/Intrinsic.h
%{_includedir}/X11/CoreP.h
%{_includedir}/X11/Object.h
%{_includedir}/X11/CompositeP.h
%{_includedir}/X11/HookObjI.h
%{_includedir}/X11/RectObjP.h
%{_includedir}/X11/ConvertI.h
%{_includedir}/X11/Shell.h
%{_includedir}/X11/ShellI.h
%{_includedir}/X11/ShellP.h
%{_includedir}/X11/StringDefs.h
%{_includedir}/X11/VendorP.h
%{_includedir}/X11/SelectionI.h
%{_includedir}/X11/PassivGraI.h
%{_includedir}/X11/Composite.h
%{_includedir}/X11/ThreadsI.h
%{_includedir}/X11/ResourceI.h
%{_mandir}/man3/Xt*.3*.bz2
%{_mandir}/man3/Menu*
%{_mandir}/man1/makestrs.1*.bz2

%files -n %{libxt}-static-devel
%defattr(-,root,root)
%{_libdir}/libXt.a


%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.5
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
