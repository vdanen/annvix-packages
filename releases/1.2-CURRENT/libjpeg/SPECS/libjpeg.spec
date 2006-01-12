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
%doc README change.log
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc usage.doc wizard.doc coderules.doc libjpeg.doc structure.doc example.c
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


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Sat Aug  9 2003 Till Kamppeter <till@mandrakesoft.com> 6b-32mdk
- Replaced Patch 2 by a patch for lossless cropping and joining of JPEG
  images to "jpegtran" (in "libjpeg-progs" package) from
  http://sylvana.net/jpegcrop/.

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6b-31mdk
- Enforce current practise of libjpeg-devel

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6b-30mdk
- mklibname

* Tue Jul  8 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 6b-29mdk
- rebuild for new devel provides

* Tue May 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 6b-28mdk
- rebuild to make rpm pick up provides

* Sat Apr 26 2003 Stefan van der Eijk <stefan@eijk.nu> 6b-27mdk
- rebuild

* Fri Oct  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6b-26mdk
- Patch3: Use autoconf variables to know libdir et al. Aka, fix *.la
  on lib64 platforms

* Sun Aug 18 2002 Till Kamppeter <till@mandrakesoft.com> 6b-25mdk
- Added patch for lossless cropping of JPEG images to "jpegtran"
  (in "libjpeg-progs" package) from http://sylvana.net/jpegcrop/.

* Wed Jun 26 2002 Yves Duret <yduret@mandrakesoft.com> 6b-24mdk
- put back .the .la files where they should always be, ie in -devel (thx fcrozat).

* Thu May 16 2002 Yves Duret <yduret@mandrakesoft.com> 6b-23mdk
- 9.0 lib policy: added %lib_name-static-devel

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6b-22mdk
- Automated rebuild in gcc3.1 environment

* Sat Feb 16 2002 Yves Duret <yduret@mandrakesoft.com> 6b-21mdk
- clean up spec file

* Sun Jun 24 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 6b-20mdk
- Overwrite package-included libtool script with build system
  libtool script, to fix build on Alpha.

* Tue Mar 13 2001 Francis Galiegue <fg@mandrakesoft.com> 6b-19mdk
- Added patch to make it recognise ia64

* Fri Jan 12 2001 David BAUDENS <baudens@mandrakesoft.com> 6b-18mdk
- Obsoletes: libjpeg-devel
- Fix Requires section
- Spec clean up

* Fri Jan  5 2001 Yves Duret <yduret@mandrakesoft.com> 6b-17mdk
- changed the progs package name to libjpeg-progs

* Wed Jan  3 2001 Yves Duret <yduret@mandrakesoft.com> 6b-16mdk
- macroization
- added URL:, %%doc
- split into libjpeg, libjpeg-progs and libjpeg-devel

* Fri Jul 26 2000 <adussart@mandrakesoft.com> 6b-15mdk
- Updated %%files section. 

* Thu May 04 2000 <adussart@mandrakesoft.com> 6b-14mdk
- Fixed HAVE_STDLIB_H redefine bug.

* Tue Apr 18 2000 Warly <warly@mandrakesoft.com> 6b-13mdk 
- New group 

* Thu Jan 13 2000 Pixel <pixel@mandrakesoft.com>
- libtoolize --force
- fix strange ./libtool needed by forcing LIBTOOL=libtool

* Wed Nov  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)

* Wed Jan 13 1999 Cristian Gafton <gafton@redhat.com>
- patch to build on arm
- build for glibc 2.1

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries

* Mon Aug  3 1998 Jeff Johnson <jbj@redhat.com>
- fix buildroot problem.

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Thu Jun 04 1998 Marc Ewing <marc@redhat.com>
- up to release 4
- remove patch that set (improper) soname - libjpeg now does it itself

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- fixed build on manhattan

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 6b

* Wed Oct 08 1997 Donnie Barnes <djb@redhat.com>
- new package to remove jpeg stuff from libgr and put in it's own package
