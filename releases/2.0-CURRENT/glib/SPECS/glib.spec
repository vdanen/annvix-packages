#
# spec file for package glib
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		glib
%define version		1.2.10
%define release		%_revrel

%define major    	1.2
%define libname  	%mklibname %{name} %{major}

Summary:	A library of handy utility functions
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://www.gtk.org
Source:		ftp://ftp.gtk.org/pub/gtk/v1.2/%{name}-%{version}.tar.bz2
# (fc) 1.2.10-3mdk Suppress warnings about varargs macros for -pedantic (Rawhide)
Patch0:		glib-1.2.10-isowarning.patch
# (fc) 1.2.10-5mdk don't set -L/usr/lib in glib-config
Patch1:		glib-1.2.10-libdir.patch
Patch2:		glib-1.2.10-fdr-gcc34.patch
Patch3:		glib-1.2.10-fdr-underquoted.patch
Patch4:		glib-1.2.10-mdk-pic.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	automake1.4

%description
Glib is a handy library of utility functions. This C
library is designed to solve some portability problems
and provide other useful functionality which most
programs require.

Glib is used by GDK, GTK+ and many applications.


%package -n %{libname}
Summary:	Main library for glib
Group:		System/Libraries
Provides:	glib = %{version}-%{release}
Obsoletes:	glib

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with the glib.


%package -n %{libname}-devel
Summary:	GIMP Toolkit and GIMP Drawing Kit support library
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	pkgconfig
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	glib-devel

%description -n %{libname}-devel
Static libraries and header files for the support library for the GIMP's X
libraries, which are available as public libraries.  GLIB includes generally
useful data structures.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .isowarnings
%patch1 -p1 -b .libdir
%patch2 -p1 -b .gcc34
%patch3 -p1 -b .underquoted
%patch4 -p1 -b .pic
automake-1.4


%build
%configure

%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

%multiarch_binaries %{buildroot}%{_bindir}/glib-config


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname}-devel
%_install_info %{name}.info

%preun -n %{libname}-devel
%_remove_install_info %{name}.info


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/*a
%{_libdir}/pkgconfig/*
%{_libdir}/glib
%{_includedir}/*
%{_mandir}/man1/*
%{_datadir}/aclocal/*
%{_bindir}/glib-config
%multiarch %{multiarch_bindir}/*
%{_infodir}/%{name}*

%files doc
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README COPYING docs/*.html


%changelog
* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.10
- add -doc subpackage
- rebuild with gcc4
- put make check in %%check

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.10
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.10
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.10-18avx
- bootstrap build (new gcc, new glibc)

* Sat Jul 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.10-17avx
- rebuild against new gcc
- enable multiarch

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.10-16avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.10-15avx
- P2: fix build with gcc 3.4 (fedora)
- P3: fix underquoted m4 definitions (fedora)
- P4: build static glib library with PIC as pam modules need it
  (gbeauchesne)

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.10-14avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.2.10-13sls
- minor spec cleanups
- remove COPYING from %%{libname}

* Mon Dec 22 2003 Vincent Danen <vdanen@opensls.org> 1.2.10-12sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
