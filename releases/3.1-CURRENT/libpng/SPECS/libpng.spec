#
# spec file for package libpng
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libpng
%define version		1.2.23
%define release		%_revrel
%define epoch		2

%define major		3
%define libname		%mklibname png %{major}
%define devname		%mklibname png -d
%define staticdevname	%mklibname png -d -s

Summary: 	A library of functions for manipulating PNG image format files
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
Epoch: 		%{epoch}
License: 	GPL-like
Group: 		System/Libraries
URL: 		http://www.libpng.org/pub/png/libpng.html
Source: 	http://prdownloads.sourceforge.net/libpng/%{name}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires: 	zlib-devel

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG is
a bit-mapped graphics format similar to the GIF format.  PNG was created to
replace the GIF format, since GIF uses a patented data compression
algorithm.


%package -n %{libname}
Summary:	A library of functions for manipulating PNG image format files
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{epoch}:%{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libpng.


%package -n %{devname}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}
Requires:	zlib-devel
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	png-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname png 3 -d

%description -n %{devname}
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.


%package -n %{staticdevname}
Summary:	Development static libraries
Group:		Development/C
Requires:	%{devname} = %{epoch}:%{version}
Requires:	zlib-devel
Provides:	%{name}-static-devel = %{epoch}:%{version}-%{release}
Provides:	png-static-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname png 3 -d -s

%description -n %{staticdevname}
Libpng development static libraries.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%ifnarch %{ix86}
export CFLAGS="%{optflags} -DPNG_NO_MMX_CODE"
%else
export CFLAGS="%{optflags}"
%endif

%configure2_5x
%make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_mandir}/man{3,5}
install -m 0644 {libpng,libpngpf}.3 %{buildroot}%{_mandir}/man3
install -m 0644 png.5 %{buildroot}%{_mandir}/man5/png3.5

# remove unpackaged files
rm -rf %{buildroot}%{_prefix}/man
rm -rf %{buildroot}{%{_prefix}/man,%{_libdir}/lib*.la}

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/libpng12-config


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*
%{_libdir}/libpng12.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_bindir}/libpng12-config
%{_bindir}/libpng-config
%multiarch %{multiarch_bindir}/libpng12-config
%{_includedir}/*
%{_libdir}/libpng.so
%{_libdir}/libpng12.so
%{_libdir}/pkgconfig/*
%{_mandir}/man?/*

%files -n %{staticdevname}
%defattr(-,root,root)
%{_libdir}/libpng*.a

%files doc
%defattr(-,root,root)
%doc *.txt example.c README TODO CHANGES


%changelog
* Tue Nov 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.23
- 1.2.23 (fixes CVE-2007-5269)
- move the man5 manpages to the -devel package
- drop P2 and export -DPNG_NO_MMX_CODE for non-x86 instead
- drop P0 and P1; use configure instead

* Fri Jul 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.18
- 1.2.18 (fixes CVE-2007-2445)
- implement devel naming policy
- implement library provides policy

* Mon Apr 23 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.16
- 1.2.16
- updated P0, P1 from Mandriva
- use %%multiarch
- move the test to %%check
- drop P2, security fix merged upstream
- new P2 to make sure to enable MMX optimisations on 32-bit x86
  platforms only (gbeauchesne)

* Fri Feb 02 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.8
- P2: security fix for CVE-2006-5793

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.8
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.8
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.8-1avx
- 1.2.8
- dropped P1; security fixes merged upstream
- new P1: lib64 fixes to pkconfig files (gbeauchesne)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.5-17avx
- bootstrap build (new gcc, new glibc)

* Sat Jul 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.5-16avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.5-15avx
- bootstrap build

* Wed Aug 04 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.5-14avx
- replace P1 and P2 with an official patch from the libpng team, which also
  fixes CAN-2004-0597, CAN-2004-0598, and CAN-2004-599

* Mon Jun 28 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.5-13avx
- P2: security fix for CAN-2002-1363 which I had fixed in mdk a long time
  ago and which a maintainer for this package never applied to in cooker =(

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.5-12avx
- Annvix build

* Mon Apr 19 2004 Vincent Danen <vdanen@opensls.org> 1.2.5-11sls
- P1: fix CAN-2004-0421

* Mon Apr 12 2004 Vincent Danen <vdanen@opensls.org> 1.2.5-10sls
- fix epoch in requires

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.2.5-9sls
- minor spec cleanups
- get rid of duplicated doc files

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 1.2.5-8sls
- OpenSLS build
- tidy spec
- remove the 8.1-upgrade-conflicts stuff

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
