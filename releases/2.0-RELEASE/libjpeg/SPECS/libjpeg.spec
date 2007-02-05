#
# spec file for package libjpeg
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libjpeg
%define	version		6b
%define release 	%_revrel

%define major		62
%define libname_orig	libjpeg
%define libname		%mklibname jpeg %{major}

Summary:	A library for manipulating JPEG image format files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL-like
Group:		System/Libraries
URL:		http://www.ijg.org/
Source0:	ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v6b.tar.bz2
Patch0:		libjpeg-6b-arm.patch
Patch1:		libjpeg-ia64-acknowledge.patch
# Patch for lossless cropping and joining of JPEG files from 
# http://sylvana.net/jpegcrop/
# This patch is derived by "diff"ing the source files of
# http://sylvana.net/jpegcrop/droppatch.tar.gz with the appropriate
# original source files
Patch2:		jpegv6b-losslesscropndrop.patch
# Use autoconf variables to know libdir et al.
Patch3:		jpeg-6b-autoconf-vars.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtool

%description
The libjpeg package contains a shared library of functions for loading,
manipulating and saving JPEG format image files.


%package -n %{libname}
Summary:	A library for manipulating JPEG image format files
Group:		System/Libraries
Obsoletes:	%{name}
Provides:       %{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libjpeg.


%package -n %{libname}-devel
Summary:	Development tools for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	jpeg-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel

%description -n %{libname}-devel
The libjpeg-devel package includes the header files necessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.


%package -n %{libname}-static-devel
Summary:	Static libraries for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	jpeg-static-devel = %{version}-%{release}

%description -n %{libname}-static-devel
The libjpeg-devel package includes the static librariesnecessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.


%package -n jpeg-progs
Summary:	Programs for manipulating JPEG format image files
Group:		Graphics
Requires:	%libname = %{version}-%{release}
Provides:	libjpeg-progs = %{version}-%{release}
Obsoletes:	libjpeg-progs

%description -n jpeg-progs
The jpeg-progs package contains simple client programs for accessing 
the libjpeg functions.  Libjpeg client programs include cjpeg, djpeg, 
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into JPEG
format. Djpeg decompresses a JPEG file into a regular image file.  Jpegtran
can perform various useful transformations on JPEG files.  Rdjpgcom displays
any text comments included in a JPEG file.  Wrjpgcom inserts text
comments into a JPEG file.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n jpeg-6b
%patch0 -p1 
%patch1 -p1
%patch2 -p0
%patch3 -p1
cp `which libtool` .

%build
%configure \
    --prefix=%{_prefix} \
    --enable-shared \
    --enable-static \
    --disable-rpath

#cat > have_stdlib.sed <<\EOF
#s/#define HAVE_STDLIB_H/#ifndef HAVE_STDLIB_H\
#&\
#endif/g
#EOF
#sed -f have_stdlib.sed jconfig.h > jconfig.tmp && mv jconfig.tmp jconfig.h
#rm -f have_stdlib.sed
#perl -pi -e 's,hardcode_libdir_flag_spec=",#hardcode_libdir_flag_spec=",;' libtool


%make
%ifnarch armv4l
#FIX MEEE: we know this will fail on arm
LD_LIBRARY_PATH=$PWD make test
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_libdir},%{_includedir},%{_mandir}/man1}
%makeinstall mandir=%{buildroot}/%{_mandir}/man1


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*.h
%{_libdir}/*.la

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

%files -n jpeg-progs
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files doc
%defattr(-,root,root)
%doc README change.log
%doc usage.doc wizard.doc coderules.doc libjpeg.doc structure.doc example.c


%changelog
* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 6b
- add -doc subpackage
- rebuild with gcc4
- buildrequires: libtool

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 6b
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 6b
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 6b-38avx
- rename libjpeg-progs to jpeg-progs

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 6b-37avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 6b-36avx
- bootstrap build

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 6b-35avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 6b-34sls
- minor spec cleanups
- get rid of same docs in multiple packages

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 6b-33sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
