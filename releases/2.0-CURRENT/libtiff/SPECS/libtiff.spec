#
# spec file for package libtiff
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libtiff
%define	version		3.8.2
%define release 	%_revrel

%define picver		3.8.0
%define lib_version	3.8.2
%define lib_major	3
%define libname		%mklibname tiff %{lib_major}

Summary:	A library of functions for manipulating TIFF format image files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		System/Libraries
URL:		http://www.libtiff.org/
Source0:	ftp://ftp.remotesensing.org/pub/libtiff/tiff-%{version}.tar.gz
Source1:	ftp://ftp.remotesensing.org/pub/libtiff/pics-%{picver}.tar.gz
Patch0:		tiffsplit-overflow.patch
Patch1:		tiff.tiff2pdf-octal-printf.patch


BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libjpeg-devel
BuildRequires:	zlib-devel

%description
The libtiff package contains a library of functions for manipulating TIFF
(Tagged Image File Format) image format files. TIFF is a widely used file
format for bitmapped images. TIFF files usually end in the .tif extension
and they are often quite large.


%package progs
Summary:	Binaries needed to manipulate TIFF format image files
Group:		Graphics
Requires:	%{libname} = %{version}
Obsoletes:	libtiff3-progs
Provides:	libtiff3-progs = %{version}-%{release}

%description progs
This package provides binaries needed to manipulate TIFF format image files.


%package -n %{libname}
Summary:	A library of functions for manipulating TIFF format image files
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
The libtiff package contains a library of functions for manipulating TIFF
(Tagged Image File Format) image format files. TIFF is a widely used file
format for bitmapped images. TIFF files usually end in the .tif extension
and they are often quite large.


%package -n %{libname}-devel
Summary:	Development tools for programs which will use the libtiff library
Group:		Development/C
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	tiff-devel = %{version}-%{release}

%description -n %{libname}-devel
This package contains the header files and .so libraries for developing
programs which will manipulate TIFF format image files using the libtiff
library.


%package -n %{libname}-static-devel
Summary:	Static libraries for programs which will use the libtiff library
Group:		Development/C
Requires:	%{libname}-devel = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	tiff-static-devel = %{version}-%{release}

%description -n %{libname}-static-devel
This package contains the static libraries for developing
programs which will manipulate TIFF format image files using the libtiff
library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n tiff-%{version} -a 1
%patch0 -p1 -b .can-2005-2452
%patch1 -p1 -b .cve-2005-1544

ln -s pics-* pics


%build
find . -type 'd' -name 'CVS' | xargs rm -fr
%{?__cputoolize: %{__cputoolize}}

./configure \
    --with-GCOPTS="%{optflags}" \
    --prefix=%{_prefix} \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir} \
    --localstatedir=%{_localstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

%make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/{%{_bindir},%{_datadir}}

%makeinstall

install -m 0644 libtiff/tiffiop.h %{buildroot}%{_includedir}/
install -m 0644 libtiff/tif_dir.h %{buildroot}%{_includedir}/

rm -rf %{buildroot}%{_docdir}/tiff-%{version}

%multiarch_includes %{buildroot}%{_includedir}/tiffconf.h


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files progs
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root,0755)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/*.so
%{_mandir}/man3/*

%files -n %{libname}-static-devel
%defattr(-,root,root,-)
%{_libdir}/*.a

%files doc
%defattr(-,root,root,-)
%doc COPYRIGHT README TODO VERSION html


%changelog
* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.8.2
- 3.8.2
- drop all patches; merged upstream
- P0: security fix for CVE-2006-2656
- P1: security fix for CVE-2006-2193
- put make test in %%check
- add -doc subpackage
- rebuild with gcc4

* Fri Feb 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.6.1
- P15: security fix for CVE-2005-1544

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.6.1
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.6.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.1-1avx
- 3.6.1
- sync patches with mandrake 3.6.1-12mdk
- includes patch to fix CAN-2005-2452

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.5.7-18avx
- bootstrap build (new gcc, new glibc)

* Sat Jul 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.5.7-17avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.5.7-16avx
- bootstrap build

* Wed Oct 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.5.7-15avx
- P7-P10: security fixes for CAN-2004-0803, CAN-2004-0804, and
  CAN-2004-0886

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.5.7-14avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 3.5.7-13sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 3.5.7-12sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
