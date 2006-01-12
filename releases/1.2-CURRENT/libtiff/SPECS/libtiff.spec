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
%define	version		3.6.1
%define release 	%_revrel

%define lib_version	3.6.1
%define lib_major	3
%define libname		%mklibname tiff %{lib_major}

Summary:	A library of functions for manipulating TIFF format image files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		System/Libraries
URL:		http://www.libtiff.org/
Source0:	ftp://ftp.remotesensing.org/pub/libtiff/tiff-v%{version}.tar.bz2
Source1:	ftp://ftp.remotesensing.org/pub/libtiff/pics-%{version}.tar.bz2
Patch0:		tiff-v3.6-shlib.patch
Patch1:		%{name}-3.6.1-codecs.patch
Patch2:		%{name}-3.5.5-stupid_cd_output.patch
Patch3:		%{name}-3.5.5-buildroot.patch
Patch4:		tiff-v3.6.1-64bit.patch
Patch5:		tiff-v3.5.7-x86_64.patch
Patch6:		tiff-v3.5.7-deps.patch
Patch8:		libtiff-3.6.1-tiffsplit_range.patch
# security fixes
Patch10:	libtiff-3.6.1-alt-bound.patch
Patch11:	libtiff-3.6.1-chris-bound.patch
Patch12:	libtiff-3.5.7-bound-fix2.patch
Patch13:	libtiff-3.6.x-iDefense.patch
Patch14:	libtiff-3.6.x-CAN-2005-2452.patch


BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libjpeg-devel, 	zlib-devel

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


%prep
%setup -q -n tiff-v%{version} -a 1
%patch0 -p1 -b .shlib
%patch1 -p1 -b .codecs
%patch2 -p1 -b .cd
%patch3 -p1 -b .buildroot
%patch4 -p1 -b .64bit
%patch5 -p1 -b .x86_64
%patch6 -p1 -b .deps
%patch8 -p1 -b .range
# security fixes
%patch10 -p1 -b .alt-bound
%patch11 -p1 -b .chris-bound
%patch12 -p1 -b .bound-fix2
%patch13 -p1 -b .idefense
%patch14 -p1 -b .can-2004-2452

ln -s pics-* pics


%build
find . -type 'd' -name 'CVS' | xargs rm -fr
perl -pi -e 's|(DIR_.*)="?/usr/lib"?|\1="%{_libdir}"|' config.site
%{?__cputoolize: %{__cputoolize}}
./configure \
    --target=%{_target_platform} \
    --with-GCOPTS="%{optflags}" << EOF
no
%{_bindir}
%{_libdir}
%{_includedir}
%{_mandir}
%{_defaultdocdir}/%{name}-progs-%{version}
bsd-source-cat
yes
EOF

pushd libtiff
    ln -s libtiff.so.%{lib_version} libtiff.so
popd
%make

make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/{%{_bindir},%{_datadir}}

%makeinstall

install -m 0644 %{name}/%{name}.so.%{lib_version} %{buildroot}/%{_libdir}

pushd %{buildroot}%{_libdir}
    ln -sf %{name}.so.%{lib_version} %{name}.so
    ln -sf %{name}.so.%{lib_version} %{name}.so.%{lib_major}
popd

install -m 0644 libtiff/tiffiop.h %{buildroot}%{_includedir}/
install -m 0644 libtiff/port.h %{buildroot}%{_includedir}/
install -m 0644 libtiff/tif_dir.h %{buildroot}%{_includedir}/

%multiarch_includes %{buildroot}%{_includedir}/port.h


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
%defattr(-,root,root,-)
%doc COPYRIGHT README TODO VERSION html
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/*

%files -n %{libname}-static-devel
%defattr(-,root,root,-)
%{_libdir}/*.a


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Thu Oct  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.5.7-11mdk
- build libtiff with -lm

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.5.7-10mdk
- mkbliname, cputoolize, fixlets

* Tue Jul  8 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.5.7-9mdk
- rebuild for new devel provides

* Fri May 23 2003 Stefan van der Eijk <stefan@eijk.nu> 3.5.7-8mdk
- rebuild

* Mon May 05 2003 Stefan van der Eijk <stefan@eijk.nu> 3.5.7-7mdk
- fix %%doc (comment out "Readme")

* Fri Oct 11 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.5.7-6mdk
- Update Patch4 (64bit) and check for standard _LP64 define.
- Patch5: Add check for x86_64 untill gcc is fixed to make it LP64 too.

* Sun Jul  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.5.7-5mdk
- Correctly set DIR_{JPEG,GZ}LIB

* Thu May 16 2002 Yves Duret <yduret@mandrakesoft.com> 3.5.7-4mdk
- 9.0 lib policy: added %libname-static-devel

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.5.7-3mdk
- Automated rebuild in gcc3.1 environment

* Sun Apr 21 2002 Yves Duret <yduret@mandrakesoft.com> 3.5.7-2mdk
- fix dangling symlinks (found by  Alexander Skwar <ASkwar@digitalprojects.com>)

* Tue Mar 19 2002 Yves Duret <yduret@mandrakesoft.com> 3.5.7-1mdk
- version 3.5.7
- use %%libname everywhere, more macros
- fix build
- sync with connectiva
- provides %%{version}-%%{release}

* Mon Oct 22 2001 Yves Duret <yduret@mandrakesoft.com> 3.5.5-8mdk
- rebuild for sir rpmlint : fix dir perm

* Tue Jul 10 2001 Stefan van der Eijk <stefan@eijk.nu> 3.5.5-8mdk
- BuildRequires:	libjpeg-devel
- BuildRequires:	zlib-devel
- Buildroot --> BuildRoot

* Tue Jun 19 2001 Yves Duret <yduret@mandrakesoft.com> 3.5.5-7mdk
- nopin rpmlint (c) un wolof from Ouro Sogui

* Wed Mar 07 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.5.5-6mdk
- added patch for JPEG and ZIP codecs, as well as "steve" and "test"
  patches from RedHat. Now ImageMagick Jpeg/PNG -> TIF conversion
  works.
- added man pages.

* Sat Jan 20 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.5.5-5mdk
- tools dynamic linked now.
- real optization.   

* Tue Dec 26 2000 Yves Duret <yduret@mandrakesoft.com> 3.5.5-4mdk
- changed Copyright: into BSD-like instead of distributable

* Sun Dec 17 2000 David BAUDENS <baudens@mandrakesoft.com> 3.5.5-3mdk
- Use %%{_buildroot} for BuildRoot
- Use %%make macro
- Libdification
- Remove CVS stuff

* Wed Jul 19 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.5.5-2mdk
- fix URL
- use new macros
- BM
- let spechelper do the strip & compress job

* Mon Jun 26 2000 Alexandre Dussart <adussart@mandrakesoft.com> 3.5.5-1mdk
- 3.5.5
- Removed obsolete patch(check for libc6).
- Rewrittent some spec section to be more generic.
- Updated shlib patch.
- Removed LIBVER define.

* Tue Apr 18 2000 Warly <warly@linux-mandrake.com> 3.4-10mdk 
- New group

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Enable SMP check/build
- Use good macro (old one may have bziped whole dirs)
- defattr

* Mon Jul 12 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- bzip manpages

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Wed Jan 13 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Wed Jun 10 1998 Michael Fulbright <msf@redhat.com>
- rebuilt against fixed jpeg libs (libjpeg-6b)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 13 1997 Donnie Barnes <djb@redhat.com>
- new version to replace the one from libgr
- patched for glibc
- added shlib support

