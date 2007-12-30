#
# spec file for package zlib
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		zlib
%define version		1.2.3
%define release 	%_revrel

%define major		1
%define libname		%{name}%{major}

%define build_biarch	0

# Enable bi-arch build on x86-64, sparc64, and ppc64
%ifarch x86_64 sparc64 ppc64
    %define build_biarch 1
%endif

Summary:	The zlib compression and decompression library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://www.gzip.org/zlib/

Source:		http://prdownloads.sourceforge.net/libpng/%{name}-%{version}.tar.bz2
Patch0:		zlib-1.2.1-glibc.patch
Patch1:		zlib-1.2.1-multibuild.patch
Patch2:		zlib-1.2.2.2-build-fPIC.patch
Patch3:		zlib-1.2.1.1-deb-alt-inflate.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The zlib compression library provides in-memory compression and
decompression functions, including integrity checks of the uncompressed
data.  This version of the library supports only one compression method
(deflation), but other algorithms may be added later, which will have
the same stream interface.  The zlib library is used by many different
system programs.


%package -n %{libname}
Summary:	The zlib compression and decompression library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name}

%description -n %{libname}
The zlib compression library provides in-memory compression and
decompression functions, including integrity checks of the uncompressed
data.  This version of the library supports only one compression method
(deflation), but other algorithms may be added later, which will have
the same stream interface.  The zlib library is used by many different
system programs.


%package devel
Summary:	Header files and libraries for developing apps which will use zlib
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{libname}-devel = %{version}-%{release}
Obsoletes:	%{libname}-devel

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .multibuild
%patch2 -p1 -b .build-fPIC

%build
mkdir objs
pushd objs
    CFLAGS="%{optflags}" \
        ../configure \
            --shared \
            --prefix=%{_prefix} \
            --libdir=%{_libdir}
    %make
    make test
    ln -s ../zlib.3 .
popd

%if %{build_biarch}
    OPT_FLAGS="%{optflags}"
    %ifarch sparc64
        OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g' -e 's/-m32//g' -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g'`
    %endif
    mkdir objs32
    pushd objs32
        CFLAGS="$OPT_FLAGS" CC="%{__cc} -m32" \
            ../configure \
                --shared \
                --prefix=%{_prefix}
        %make
        make test
    popd
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}

make install -C objs prefix=%{buildroot}%{_prefix} libdir=%{buildroot}%{_libdir}
%if %{build_biarch}
    make install-libs -C objs32 prefix=%{buildroot}%{_prefix}
%endif

install -d %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}/%{_lib}/
ln -s ../../%{_lib}/libz.so.%{version} %{buildroot}%{_libdir}/

%if %{build_biarch}
    install -d %{buildroot}/lib
    mv %{buildroot}%{_prefix}/lib/*.so.* %{buildroot}/lib/
    ln -s ../../lib/libz.so.%{version} %{buildroot}%{_prefix}/lib/
%endif


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-, root, root)
/%{_lib}/libz.so.*
%{_libdir}/libz.so.*
%if %{build_biarch}
/lib/libz.so.*
%{_prefix}/lib/libz.so.*
%endif

%files devel
%defattr(-, root, root)
%{_libdir}/*.a
%{_libdir}/*.so
%if %{build_biarch}
%{_prefix}/lib/*.a
%{_prefix}/lib/*.so
%endif
%{_includedir}/*
%{_mandir}/*/*

%files doc
%defattr(-, root, root)
%doc README ChangeLog algorithm.txt


%changelog
* Sun Sep 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3
- implement devel naming policy
- implement library provides policy

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3
- add -doc subpackage
- rebuild with gcc4
- make it biarch on ppc64 too

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3
- Clean rebuild

* Wed Dec 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3-3avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3-2avx
- rebuild against new gcc
- spec cleanups

* Tue Jul 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3-1avx
- 1.2.3; also fixes CAN-2005-1849
- remove P4; merged upstream

* Tue Jul 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2.2-2avx
- P4: patch to fix CAN-2005-2096

* Wed Jun 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2.2-1avx
- 1.2.2.2
- enable biarch build for sparc64 (stefan)
- updated P0 and P1 from Mandriva; old P3 merged upstream
- new P3 from debian for fixes (flepied)
- updated P2: make sure we are compiling DSO with -fPIC in configure
  tests (gbeauchesne)
- start work to make specs more readable and "clean"

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.4-12avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.1.4-11avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 1.1.4-10sls
- minor spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 1.1.4-9sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
