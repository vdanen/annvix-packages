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
%define libname		%mklibname jpeg %{major}
%define devname		%mklibname jpeg -d
%define odevname	%mklibname jpeg 62 -d
%define staticdevname	%mklibname jpeg -d -s
%define ostaticdevname	%mklibname jpeg 62 -d -s

Summary:	A library for manipulating JPEG image format files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL-like
Group:		System/Libraries
URL:		http://www.ijg.org/
Source0:	ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v6b.tar.bz2
Source1:	http://jpegclub.org/droppatch.tar.bz2
Source2:	http://jpegclub.org/jpegexiforient.c
Source3:	http://jpegclub.org/exifautotran.txt
Patch0:		jpeg-6b-autoconf-vars.patch
Patch1:		jpeg-6b-mdv-c++fixes.patch

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


%package -n %{devname}
Summary:	Development tools for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	jpeg-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{odevname}

%description -n %{devname}
The libjpeg-devel package includes the header files necessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.


%package -n %{staticdevname}
Summary:	Static libraries for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	jpeg-static-devel = %{version}-%{release}
Obsoletes:	%{ostaticdevname}

%description -n %{staticdevname}
The libjpeg-devel package includes the static librariesnecessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.


%package -n jpeg-progs
Summary:	Programs for manipulating JPEG format image files
Group:		Graphics
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-progs = %{version}-%{release}
Obsoletes:	%{name}-progs

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
%setup -q -T -D -a 1 -n jpeg-6b
rm -f jpegtran
%patch0 -p1
%patch1 -p1

cp `which libtool` .
cp %{_sourcedir}/jpegexiforient.c .
cp %{_sourcedir}/exifautotran.txt exifautotran


%build
%configure \
    --prefix=%{_prefix} \
    --enable-shared \
    --enable-static \
    --disable-rpath

%make
LD_LIBRARY_PATH=$PWD make test

gcc %{optflags} -o jpegexiforient jpegexiforient.c


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_libdir},%{_includedir},%{_mandir}/man1}

%makeinstall mandir=%{buildroot}/%{_mandir}/man1

install -m 0644 jpegint.h %{buildroot}%{_includedir}/jpegint.h
install -m 0755 jpegexiforient %{buildroot}%{_bindir}
install -m 0755 exifautotran %{buildroot}%{_bindir}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*.h
%{_libdir}/*.la

%files -n %{staticdevname}
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
* Sat Sep 8 2007 Vincent Danen <vdanen-at-build.annvix.org> 6b
- implement devel naming policy
- implement library provides policy
- drop P2 and add S1 to replace it (lossless cropping of JPEG files and lossless
  pasting of one JPEG into another)
- added S2 and S3; sources to allow automatic lossless rotation of JPEG images
  with orientation markings in EXIF data
- P4: add guards for C++ code (i.e. OpenVRML); from Mandriva
- remove P0 and build-hack for arm support
- remove P1; we don't build for ia64
- renumber patches

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
