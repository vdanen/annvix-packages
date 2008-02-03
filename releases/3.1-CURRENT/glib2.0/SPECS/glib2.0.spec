#
# spec file for package glib2.0
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		glib%{api_version}
%define version		2.14.4
%define release		%_revrel

%define api_version	2.0
%define major		0
%define libname		%mklibname %{name}_ %{major}
%define devname		%mklibname %{name} -d

Summary:	GIMP Toolkit and GIMP Drawing Kit support library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://www.gtk.org
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/glib/2.14/glib-%{version}.tar.bz2
Source1:	glib20.sh
Source2:	glib20.csh

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext
BuildRequires:	pkgconfig >= 0.12
BuildRequires:	libtool >= 1.4.2-2mdk
BuildRequires:	locales-en

Requires:	common-licenses

%description
Glib is a handy library of utility functions. This C library is designed to
solve some portability problems and provide other useful functionality which
most programs require.

Glib is used by GDK, GTK+ and many applications.


%package -n %{libname}
Summary:	GIMP Toolkit and GIMP Drawing Kit support library
Group:		System/Libraries
Provides:	glib2 = %{version}-%{release}
Provides:	libglib2 = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Conflicts:	libglib1.3_13

%description -n %{libname}
Glib is a handy library of utility functions. This C library is designed to
solve some portability problems and provide other useful functionality which
most programs require.

Glib is used by GDK, GTK+ and many applications.

This package contains the library needed to run programs dynamically linked
with the glib.


%package -n %{devname}
Summary:	Static libraries and header files of %{name}
Group:		Development/C
Provides:	glib2-devel = %{version}-%{release}
Provides:	libglib2-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	pkgconfig >= 0.12
Requires:	glib-gettextize >= %{version}
Conflicts:	libglib1.3_13-devel
Obsoletes:	%mklibname %{name}_ 0 -d

%description -n %{devname}
Static libraries and header files for the support library for the GIMP's X
libraries, which are available as public libraries.  GLIB includes generally
useful data structures.


%package -n glib-gettextize
Summary:	Gettextize replacement
Group:		Development/Other

%description -n glib-gettextize
%{name} package is designed to replace gettextize completely.  Various
gettext related files are modified in glib and gtk+ to allow better and more
flexible i18n; however gettextize overwrites them with its own copy of
files, thus nullifying the changes.  If this replacement of gettextize is
run instead, then all gnome packages can potentially benefict from the
changes.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -n glib-%{version} -q


%build
#we don't use libtool 1.5 yet
%define __libtoolize /bin/true

%configure2_5x \
    --enable-static \
    --enable-gtk-doc=no

%make
# see http://bugzilla.gnome.org/show_bug.cgi?id=440544
#make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 0644 %{_sourcedir}/glib20.sh %{buildroot}%{_sysconfdir}/profile.d/20glib20.sh
install -m 0644 %{_sourcedir}/glib20.csh %{buildroot}%{_sysconfdir}/profile.d/20glib20.csh

%kill_lang glib20
%find_lang glib20


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname} -f glib20.lang
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*
%{_libdir}/libglib-%{api_version}.so.*
%{_libdir}/libgmodule-%{api_version}.so.*
%{_libdir}/libgthread-%{api_version}.so.*
%{_libdir}/libgobject-%{api_version}.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a
%{_libdir}/glib-%{api_version}
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man1/*
%{_datadir}/aclocal/glib-%{api_version}.m4
%{_bindir}/glib-genmarshal
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query

%files -n glib-gettextize
%defattr(-,root,root)
%{_bindir}/glib-gettextize
%{_datadir}/aclocal/glib-gettext.m4
%{_datadir}/glib-%{api_version}

%files doc
%defattr(-,root,root)
%doc README AUTHORS ChangeLog NEWS
%doc %{_datadir}/gtk-doc/html/*


%changelog
* Sat Dec 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.14.4
- order the profile.d/ scripts and drop executable bit

* Wed Dec 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.14.4
- 2.14.4

* Wed Nov 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.14.3
- 2.14.3
- rebuild against new gettext

* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.14.0
- 2.14.0
- make profile scripts executable and fix them so there doesn't end
  up a bogus requires on tcsh
- implement devel naming policy
- implement library provides policy
- disable make check; broken upstream (ref gnome bug #440544)

* Mon Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12.1
- 2.12.1
- spec cleanups
- remove locale files

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.1 
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.1
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.1-1avx
- 2.8.1

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-4avx
- bootstrap build (new gcc, new glibc)

* Sat Jul 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-3avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-2avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-1avx
- 2.6.3
- fix download url

* Sun Sep 12 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.6-1avx
- 2.4.6

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3-4avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.2.3-3sls
- minor spec cleanups
- remove %%build_opensls macro

* Mon Dec 22 2003 Vincent Danen <vdanen@opensls.org> 2.2.3-2sls
- OpenSLS build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
