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
%defattr(-, root, root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING docs/*.html
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


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Mon Sep 08 2003 Stefan van der Eijk <stefan@eijk.nu> 1.2.10-11mdk
- rebuild to force new upload (alpha)

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.10-10mdk
- Rebuild

* Tue May 20 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.10-9mdk
- rebuild to obtain automatic devel provides

* Sat Apr 26 2003 Stefan van der Eijk <stefan@eijk.nu> - 1.2.10-8mdk
- rebuild

* Fri Apr 11 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.2.10-7mdk
- mklibname
- devel package requires pkgconfig (Götz)

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.10-6mdk
- Libtoolize to get updated config.{sub,guess}

* Mon Jun 17 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.2.10-5mdk
- Patch1: fix glib-config to not give -L/usr/lib for --libs (Geoffrey Lee)

* Thu Oct  4 2001 DindinX <odin@mandrakesoft.com> 1.2.10-4mdk
- don't include %{_infodir}/dir

* Thu Aug 30 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.2.10-3mdk
- Patch0: Add #pragma GCC system_header to supress warnings when in -pedantic mode (Rawhide)

* Mon Jul 30 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.2.10-2mdk
- Add missing files (pkgconfig, html, info)
- Fix provides

* Thu Mar 22 2001 DindinX <odin@mandrakesoft.com> 1.2.10-1mdk
- 1.2.10 (bugfixes release)

* Fri Mar  2 2001 DindinX <odin@mandrakesoft.com> 1.2.9-1mdk
- 1.2.9
- temporary remove of the strjoin patch

* Thu Dec  7 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.2.8-10mdk
- run automated tests at build time

* Tue Nov 28 2000 DindinX <odin@mandrakesoft.com> 1.2.8-9mdk
- Add some obsoletes: tags
- use more macros

* Mon Nov 27 2000 DindinX <odin@mandrakesoft.com> 1.2.8-8mdk
- use 1.2 as the major number

* Mon Nov 27 2000 DindinX <odin@mandrakesoft.com> 1.2.8-7mdk
- Grr. _Really_ use the new naming policy...

* Mon Nov 27 2000 DindinX <odin@mandrakesoft.com> 1.2.8-6mdk
- new policy
- but COPYING file back, until we have a clear statement about this issue

* Fri Nov 17 2000 Pixel <pixel@mandrakesoft.com> 1.2.8-5mdk
- move doc to -devel, removed doc COPYING

* Fri Nov 03 2000 DindinX <odin@mandrakesoft.com> 1.2.8-4mdk
- rebuild with gcc-2.96

* Mon Oct 23 2000 DindinX <odin@mandrakesoft.com> 1.2.8-3mdk
- Patch g_strconcat(), g_strjoin() and g_strjoinv() so they are executed
  in O(n) instead of O(n*n).

* Tue Aug 01 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.8-2mdk
- rebuild for the BM
- misc fixes to spec
- rebuild with macros

* Tue Jun 6 2000 DindinX <odin@mandrakesoft.com> 1.2.8-1mdk
- 1.2.8
- Removed desc translation from spec

* Tue Mar 21 2000 DindinX <odin@mandrakesoft.com> 1.2.7-3mdk
- corrected the path in glib-config

* Mon Mar 20 2000 DindinX <odin@mandrakesoft.com> 1.2.7-2mdk
- Group and spec fixes

* Fri Feb 18 2000 DindinX <odin@mandrakesoft.com> 1.2.7-1mdk
- Fixed a little typo
- 1.2.7

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Enable SMP build/check
- 1.2.6

* Wed Sep 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 1.2.5.


* Thu Aug 26 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 1.2.4

* Wed Jul 14 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- changed %{prefix}/man/man1 to %{prefix}/man/man1/*
- added back descriptions from RH 5.2

* Wed May 12 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 1.2.3

* Tue Apr 27 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 1.2.2
- bzip2 man pages

* Thu Mar 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.1

* Fri Feb 26 1999 Michael Fulbright <drmike@redhat.com>
- Version 1.2

* Thu Feb 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.0pre1

* Tue Feb 23 1999 Cristian Gafton <gafton@redhat.com>
- new description tags 

* Sun Feb 21 1999 Michael Fulbright <drmike@redhat.com>
- removed libtoolize from %build

* Thu Feb 11 1999 Michael Fulbright <drmike@redhat.com>
- added libgthread to file list

* Fri Feb 05 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.15

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.14

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.13

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.12

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- updated in preparation for the GNOME freeze

* Mon Apr 13 1998 Marc Ewing <marc@redhat.com>
- Split out glib package

