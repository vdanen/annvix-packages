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
%define devname		%mklibname %{name} -d
%define devname_gmpxx	%mklibname %{name}xx -d
%define devname_mp	%mklibname %{name}mp -d

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
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7

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


%package -n %{devname}
Summary:	Development tools for the GNU MP arbitrary precision library
Group:		Development/C
Requires(post):	info-install
Requires(preun): info-install
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 3 -d

%description -n %{devname}
The static libraries, header files and documentation for using the GNU MP
arbitrary precision library in applications.


%package -n %{libname_gmpxx}
Summary:	C++ support for GMP
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	libgmpxx = %{version}-%{release}

%description -n	%{libname_gmpxx}
C++ support for GMP.


%package -n %{devname_gmpxx}
Summary:	C++ Development tools for the GMP
Group:		Development/C++
Requires:	%{devname} = %{version}
Requires:	%{libname_gmpxx} = %{version}
Provides:	libgmpxx-devel = %{version}-%{release}
Provides:	gmpxx-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name}xx 3 -d

%description -n %{devname_gmpxx}
C++ Development tools for the GMP.


%package -n %{libname_mp}
Summary:	Berkley MP compatibility library for GMP
Group:		System/Libraries
Provides:	libgmp_mp = %{version}-%{release}

%description -n %{libname_mp}
Berkley MP compatibility library for GMP.


%package -n %{devname_mp}
Summary:	Development tools for Berkley MP compatibility library for GMP
Group:		Development/C
Requires:	%{libname_mp} = %{version}
Provides:	libgmpmp-devel = %{version}-%{release}
Provides:	mp-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name}mp 3 -d

%description -n %{devname_mp}
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


%post -n %{devname}
%_install_info %{name}.info
%_install_info mpfr.info

%preun -n %{devname}
%_remove_install_info %{name}.info
%_remove_install_info mpfr.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libgmp.so.*

%files -n %{devname}
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

%files -n %{devname_gmpxx}
%defattr(-,root,root)
%{_libdir}/libgmpxx.so
%{_libdir}/libgmpxx.a
%{_libdir}/libgmpxx.la
%{_includedir}/gmpxx.h

%files -n %{libname_mp}
%defattr(-,root,root)
%{_libdir}/libmp.so.*

%files -n %{devname_mp}
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
* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4
- implement devel naming policy
- implement library provides policy

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
