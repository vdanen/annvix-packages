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
%define version		1.2.8
%define release		%_revrel
%define epoch		2

%define lib_major	3
%define libname		%mklibname png %{lib_major}

Summary: 	A library of functions for manipulating PNG image format files
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
Epoch: 		%{epoch}
License: 	GPL-like
Group: 		System/Libraries
URL: 		http://www.libpng.org/pub/png/libpng.html
Source: 	http://prdownloads.sourceforge.net/libpng/%{name}-%{version}.tar.bz2
Patch0:		libpng-1.2.5-mdkconf.patch
Patch1:		libpng-1.2.6-lib64.patch

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


%package -n %{libname}-devel
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}-%{release} zlib-devel
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	png-devel = %{epoch}:%{version}-%{release}

%description -n %{libname}-devel
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.


%package -n %{libname}-static-devel
Summary:	Development static libraries
Group:		Development/C
Requires:	%{libname}-devel = %{epoch}:%{version}-%{release} zlib-devel
Provides:	%{name}-static-devel = %{epoch}:%{version}-%{release}
Provides:	png-static-devel = %{epoch}:%{version}-%{release}

%description -n %{libname}-static-devel
Libpng development static libraries.


%prep
%setup -q
%patch0 -p1 -b .mdkconf
%patch1 -p1 -b .lib64

perl -pi -e 's|^prefix=.*|prefix=%{_prefix}|' scripts/makefile.linux
perl -pi -e 's|^(LIBPATH=.*)/lib\b|\1/%{_lib}|' scripts/makefile.linux

ln -s scripts/makefile.linux ./Makefile


%build
%make
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}
%makeinstall

mkdir -p %{buildroot}%{_mandir}/man{3,5}
install -m 0644 {libpng,libpngpf}.3 %{buildroot}%{_mandir}/man3
install -m 0644 png.5 %{buildroot}%{_mandir}/man5/png3.5

# remove unpackaged files
rm -rf %{buildroot}%{_prefix}/man


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%doc *.txt example.c README TODO CHANGES
%{_libdir}/libpng.so.*
%{_libdir}/libpng12.so.*
%{_mandir}/man5/*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/libpng12-config
%{_bindir}/libpng-config
%{_includedir}/*
%{_libdir}/libpng.so
%{_libdir}/libpng12.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/libpng*.a


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Wed Aug 27 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.5-7mdk
- Patch0: Nuke DT_RPATH, add correct DT_NEEDED entries

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.5-6mdk
- Enforce current practise of libpng-devel

* Mon Jul 28 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.5-5mdk
- mklibname

* Tue Jul  8 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.5-4mdk
- rebuild for new devel provides

* Thu May 15 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 1.2.5-3mdk
- add 's|^prefix=.*|prefix=%{_prefix}|' Makefile (thanks to Oden Eriksson)

* Tue Feb 18 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.2.5-2mdk
- rebuild without hack

* Mon Feb 10 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 1.2.5-1mdk
- new version

* Mon Dec  9 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.4-4mdk
- Add missing files (Gotz Waschk, Han Boetes)

* Sat Jul 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.4-3mdk
- Depixelize: don't explicitly provide libpng.so.3, do create a library
  linked against new libpng. This is an interim solution until everything
  is rebuilt against the latest libpng.

* Fri Jul 19 2002 Pixel <pixel@mandrakesoft.com> 1.2.4-2mdk
- ensure the symlink libpng.so.3 points to libpng.so.3.* otherwise ldconfig removes it
- explictly provide libpng.so.3 
  (find-provides doesn't do it automagically in such a weird case)
- ensure .a's are in -static-devel and .so's are in -devel
- ensure %%install can be done twice using --short-circuit

* Thu Jun 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.1-9mdk
- Fix install to also patch out LIBPATH variable
- Don't explicitly add system include dir into search path

* Thu May 16 2002 Yves Duret <yduret@mandrakesoft.com> 1.2.1-8mdk
- 9.0 lib policy: added %libname-static-devel

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.1-7mdk
- Automated rebuild in gcc3.1 environment

* Mon Mar 04 2002 David BAUDENS <baudens@mandrakesoft.com> 1.2.1-6mdk
- Remove kups and libqtcups2 from list of Conflicts:
- Requires: %%{version}-%%{release} and not only %%{version}

* Wed Feb 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.2.1-5mdk
- added old sawfish version to Conflicts:

* Sat Feb 16 2002 David BAUDENS <baudens@mandrakesoft.com> 1.2.1-4mdk
- Remove quanta from list of Conflicts:

* Thu Jan 31 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.2.1-3mdk
- added Conflicts: to ease upgrade

* Thu Jan 17 2002 Yves Duret <yduret@mandrakesoft.com> 1.2.1-2mdk
- added Conflicts: gdk-pixbuf < 0.11.0-6mdk by fcrozat request on libpng3

* Fri Jan 11 2002 Yves Duret <yduret@mandrakesoft.com> 1.2.1-1mdk
- version 1.2.1 (thanx fcrozat)

* Fri Oct 12 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.0-3mdk
- respect lib policy -> use version-release in Provides

* Wed Oct 10 2001 Yves Duret <yduret@mandrakesoft.com> 1.2.0-2mdk
- fix upgrade conflict (man renamed to png3)

* Fri Sep 28 2001 Yves Duret <yduret@mandrakesoft.com> 1.2.0-1mdk
- version 1.2.0
- warning: shared-library (.so) numbers have been bumped from 2 to 3.

* Mon Jul 16 2001 Yves Duret <yduret@mandrakesoft.com> 1.0.12-2mdk
- rebuild
- s/Serial/Epoch/

* Mon Jun 11 2001 Yves Duret <yduret@mandrakesoft.com> 1.0.12-1mdk
- version 1.0.12
- libpng-devel requires zlib-devel (since png.h includes zlib.h) #38883 (rh)

* Sun Apr 29 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.11-1mdk
- 1.0.11 out for everyone.

* Sun Apr 07 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.10-1mdk
- Put 1.0.10 out for everyone.

* Thu Feb 01 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.9-1mdk
- new and shiny source.

* Tue Dec 26 2000 Yves Duret <yduret@mandrakesoft.com> 1.0.8-4mdk
- added obsoltes

* Sun Dec 24 2000 Yves Duret <yduret@mandrakesoft.com> 1.0.8-3mdk
- fixed no-major-in-name
- added URL:

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.8-2mdk
- automatically added BuildRequires

* Tue Jul 25 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.8-1mdk
- new release
- spec cleaning
- BM

* Tue Jul 18 2000 Alexandre Dussart <adussart@mandrakesoft.com> 1.0.7-1mdk
- 1.0.7

* Mon Jun 26 2000 Alexandre Dussart <adussart@mandrakesoft.com> 1.0.6-1mdk
- 1.0.6
- Patch 1.0.6a(official)
- Patch 1.0.6b(official)
- Patch 1.0.6c(official)
- Updated mdkconf patch(some parts was obsoletes)

* Fri May 19 2000 Pixel <pixel@mandrakesoft.com> 1.0.5-3mdk
- fix *ugly* install of man pages
- add soname

* Mon Mar 27 2000 Daouda Lo <daouda@mandrakesoft.com> 1.0.5-2mdk
- fix group

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 1.0.5
- redo patch with perl (yay perl)
- SMP check/build

* Mon Jul 12 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- libpng.so.2.1.0.3 is not a man pages lets not put it in usr/man/man3 

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Sun Feb 07 1999 Michael Johnson <johnsonm@redhat.com>
- rev to 1.0.3

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Wed Sep 23 1998 Cristian Gafton <gafton@redhat.com>
- we are Serial: 1 now because we are reverting the 1.0.2 version from 5.2
  beta to this prior one
- install man pages; set defattr defaults

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- devel subpackage moved to Development/Libraries

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.0.1
- added buildroot

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- updated to new version
- spec file cleanups

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

