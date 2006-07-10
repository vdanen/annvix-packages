#
# spec file for package gmp
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gmp
%define version		4.1.4
%define release		%_revrel

%define major		3
%define major_gmpxx	3
%define major_mp	3
%define libname		%mklibname %{name} %{major}
%define libname_gmpxx	%mklibname %{name}xx %{major_gmpxx}
%define libname_mp	%mklibname %{name}mp %{major_mp}

Summary:	A GNU arbitrary precision library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL 
Group:		System/Libraries
URL:		http://www.swox.com/gmp/
Source:		ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.bz2
Patch0:		gmp-4.1.3-x86_64.patch
Patch1:		gmp-4.1-gcc-version.patch
Patch3:		gmp-4.1.4-fpu.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, automake1.7

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands.

GNU MP is fast for several reasons:
   - it uses fullwords as the basic arithmetic type,
   - it uses fast algorithms,
   - it carefully optimizes assembly code for many CPUs' most common
     inner loops
   - it generally emphasizes speed over simplicity/elegance in its
     operations


%package -n %{libname}
Summary:	A GNU arbitrary precision library
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands.

GNU MP is fast for several reasons:
  - it uses fullwords as the basic arithmetic type,
  - it uses fast algorithms
  - it carefully optimizes assembly code for many CPUs' most common
    inner loops
  - it generally emphasizes speed over simplicity/elegance in its
    operations


%package -n %{libname}-devel
Summary:	Development tools for the GNU MP arbitrary precision library
Group:		Development/C
Requires(post):	info-install
Requires(preun): info-install
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
The static libraries, header files and documentation for using the GNU MP
arbitrary precision library in applications.


%package -n %{libname_gmpxx}
Summary:	C++ support for GMP
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	libgmpxx = %{version}-%{release}

%description -n	%{libname_gmpxx}
C++ support for GMP.


%package -n %{libname_gmpxx}-devel
Summary:	C++ Development tools for the GMP
Group:		Development/C++
Requires:	%{libname}-devel = %{version}-%{release}
Requires:	%{libname_gmpxx} = %{version}-%{release}
Provides:	lib%{name}xx-devel = %{version}-%{release}
Provides:	gmpxx-devel = %{version}-%{release}

%description -n %{libname_gmpxx}-devel
C++ Development tools for the GMP.


%package -n %{libname_mp}
Summary:	Berkley MP compatibility library for GMP
Group:		System/Libraries
Provides:	libgmp_mp = %{version}-%{release}

%description -n %{libname_mp}
Berkley MP compatibility library for GMP.


%package -n %{libname_mp}-devel
Summary:	Development tools for Berkley MP compatibility library for GMP
Group:		Development/C
Requires:	%{libname_mp} = %{version}-%{release}
Provides:	lib%{name}mp-devel = %{version}-%{release}
Provides:	mp-devel = %{version}-%{release}

%description -n %{libname_mp}-devel
Development tools for Berkley MP compatibility library for GMP.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
# Don't bother touching to configure.in for the following two
# patches. Instead, patch out configure directly.
%patch0 -p1 -b .x86_64
%patch1 -p1 -b .gcc-version
%patch3 -p1


%build
libtoolize --copy --force
aclocal-1.7 -I mpfr
automake-1.7
autoconf-2.5x
%configure2_5x \
    --enable-cxx \
    --disable-fft \
    --enable-mpbsd \
    --enable-mpfr

%make


%check
# All tests must pass
%make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}/%{_libdir} %{buildroot}/%{_infodir} %{buildroot}/%{_includedir}
%makeinstall
rm -f %{buildroot}%{_infodir}/dir


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname_gmpxx} -p /sbin/ldconfig
%postun -n %{libname_gmpxx} -p /sbin/ldconfig

%post -n %{libname_mp} -p /sbin/ldconfig
%postun -n %{libname_mp} -p /sbin/ldconfig


%post -n %{libname}-devel
%_install_info %{name}.info
%_install_info mpfr.info

%preun -n %{libname}-devel
%_remove_install_info %{name}.info
%_remove_install_info mpfr.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libgmp.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libgmp.so
%{_libdir}/libgmp.a
%{_libdir}/libgmp.la 
%{_includedir}/gmp.h
%{_infodir}/gmp.info*
# mpfr
%{_libdir}/libmpfr.a
%{_includedir}/mpf2mpfr.h
%{_includedir}/mpfr.h
%{_includedir}/mpfrxx.h
%{_infodir}/mpfr.info*

%files -n %{libname_gmpxx}
%defattr(-,root,root)
%{_libdir}/libgmpxx.so.*

%files -n %{libname_gmpxx}-devel
%defattr(-,root,root)
%{_libdir}/libgmpxx.so
%{_libdir}/libgmpxx.a
%{_libdir}/libgmpxx.la
%{_includedir}/gmpxx.h

%files -n %{libname_mp}
%defattr(-,root,root)
%{_libdir}/libmp.so.*

%files -n %{libname_mp}-devel
%defattr(-,root,root)
%{_includedir}/mp.h
%{_libdir}/libmp.a
%{_libdir}/libmp.so
%{_libdir}/libmp.la

%files doc
%defattr(-,root,root)
%doc COPYING.LIB NEWS README
%doc doc demos


%changelog
* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4
- add -doc subpackage
- rebuild with gcc4
- fix prereq

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Mon Aug 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4-1avx
- 4.1.4
- P3: fix build (neoclust)
- drop P2; merged upstream
- disable FFT code and enable CXX, MPBDS, and MPFR code (walluck)

* Sat Jun 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.2-7avx
- bootstrap build

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.1.2-6avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 4.1.2-5sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.1.2-4sls
- OpenSLS build
- tidy spec

* Thu Jul 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1.2-3mdk
- Fix libification
- Patch2: Fix mpz_gcd_ui() on longlong limb systems (upstream patch)

* Thu Jul 10 2003 Götz Waschk <waschk@linux-mandrake.com> 4.1.2-2mdk
- rebuild for new rpm

* Wed Jan 22 2003 Warly <warly@mandrakesoft.com> 4.1.2-1mdk
- new version

* Mon Dec  2 2002 Warly <warly@mandrakesoft.com> 4.1.1-1mdk
- new version

* Sun Jul  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1-3mdk
- Patch4: Nuke broken assert in randraw.c (upstream patch)

* Thu Jul  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1-2mdk
- Patch1: Correctly check for gcc version
- Patch2: Don't inline fudge() in t-cmp_d since gcc 3.1+ is now too
  smart at inlining C, thus rendering the "fudge" inoperant
- Patch3: Fix t-scanf. i.e. Don't assume va-functions (<things>, ...)
  are equivalent to (<things>, void *)

* Mon Jul  3 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.1-1mdk
- New and shiny gmp aka bump release.
- Remove patch for ia64 --it seems to be already integrated.
- %%configure-ize.

* Thu Jun 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-8mdk
- Libtoolize to get updated config.guess.
- Make check in %%build stage.

* Fri May 24 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.1.1-7mdk
- License should be LGPL.

* Mon Oct 29 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-6mdk
- Patch1: get_str.c: decrement s pointer until it's below or equal to
  str, not simply equal to str. For some reason, that pointer could
  have been already set to something below str. This is a workaround
  to Sawfish crashes on IA-64, under Gnome for example.

* Thu Oct 25 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-5mdk
- Patch0: Fix IA-64 support (RH patch)
- Make rpmlint happier and fix:
  - E: gmp description-line-too-long
  - W: gmp strange-permission gmp.spec 0664

* Thu Aug 30 2001 Warly <warly@mandrakesoft.com> 3.1.1-4mdk
- some rpmlint fixes

* Sun Mar 18 2001 David BAUDENS <baudens@mandrakesoft.com> 3.1.1-3mdk
- Fix build on PPC
- Requires: %%{version}-%%{release} and not only %%{version}

* Tue Mar 13 2001 Warly <warly@mandrakesoft.com> 3.1.1-2mdk
- fix optimizations flag not used

* Mon Mar  5 2001 Warly <warly@mandrakesoft.com> 3.1.1-1mdk
- new version

* Fri Jan 12 2001 Francis Galiegue <fg@mandrakesoft.com> 2.0.2-17mdk

- Fixed file list
- Some spec file changes
- Fixed Requires

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.2-16mdk
- fix bad script

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.2-15mdk
- BM
- add doc

* Thu Jul 13 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 2.0.2-14mdk
- makeinstall macro
- macroszifications

* Sat Mar 25 2000 Daouda Lo <daouda@mandrasoft.com> 2.0.2-13mdk
- fix group

* Sun Nov 28 1999 John Buswell <johnb@mandrakesoft.com>
- Added PPC support

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Release version.

* Tue Jul 22 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- add french description

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- .spec optimizations

* Thu Feb 11 1999 Michael Johnson <johnsonm@redhat.com>
- include the private header file gmp-mparam.h because several
  apps seem to assume that they are building against the gmp
  source tree and require it.  Sigh.

* Tue Jan 12 1999 Michael K. Johnson <johnsonm@redhat.com>
- libtoolize to work on arm

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
- yet another touch of the spec file

* Wed Sep  2 1998 Michael Fulbright <msf@redhat.com>
- looked over before inclusion in RH 5.2

* Sat May 24 1998 Dick Porter <dick@cymru.net>
- Patch Makefile.in, not Makefile
- Don't specify i586, let configure decide the arch

* Sat Jan 24 1998 Marc Ewing <marc@redhat.com>
- started with package from Toshio Kuratomi <toshiok@cats.ucsc.edu>
- cleaned up file list
- fixed up install-info support
