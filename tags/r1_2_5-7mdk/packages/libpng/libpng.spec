%define lib_name_orig	libpng
%define lib_major	3
%define lib_name	%mklibname png %{lib_major}

Summary: 	A library of functions for manipulating PNG image format files
Name: 		libpng
Version: 	1.2.5
Release:	7mdk
License: 	GPL-like
Group: 		System/Libraries
BuildRequires: 	zlib-devel
URL: 		http://www.libpng.org/pub/png/libpng.html
Source: 	ftp://ftp.uu.net/graphics/png/src/%{name}-%{version}.tar.bz2
Patch0:		libpng-1.2.5-mdkconf.patch.bz2
Buildroot: 	%{_tmppath}/%{name}-%{version}-root
Epoch: 		2

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG is
a bit-mapped graphics format similar to the GIF format.  PNG was created to
replace the GIF format, since GIF uses a patented data compression
algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package -n %{lib_name}
Summary: A library of functions for manipulating PNG image format files.
Group: System/Libraries
Obsoletes: %{name}
Provides: %{name} = %{version}-%{release}
Conflicts: gdk-pixbuf < 0.11.0-6mdk

# fredl: to allow upgrades to work, list all the libs from 8.1 packages that
# depends on libpng2:
Conflicts: Epplets < 0.5-8mdk
Conflicts: gdk-pixbuf-loaders < 0.16.0-1mdk
Conflicts: gnome-core < 1.4.0.6-1mdk
Conflicts: kdeaddons < 2.2.2-2mdk
Conflicts: kdebase < 2.2.2-37mdk
Conflicts: kdebase-nsplugins < 2.2.2-37mdk
Conflicts: kdebindings < 2.2.2-4mdk
Conflicts: kdegames < 2.2.2-4mdk
Conflicts: kdegraphics < 2.2.2-4mdk
Conflicts: kdelibs < 2.2.2-29mdk
Conflicts: kdelibs-sound < 2.2.2-29mdk
Conflicts: kdemultimedia < 2.2.2-3mdk
Conflicts: kdemultimedia-aktion < 2.2.2-3mdk
Conflicts: kdenetwork < 2.2.2-11mdk
Conflicts: kdepim < 2.2.2-2mdk
Conflicts: kdesdk < 2.2.2-4mdk
Conflicts: kdetoys < 2.2.2-6mdk
Conflicts: kdeutils < 2.2.2-6mdk
Conflicts: kdevelop < 2.0.2-4mdk
Conflicts: koffice < 1.1.1-8mdk
Conflicts: kvirc < 2.1.1-5mdk
Conflicts: libSDL_image1.2 < 1.2.1-1mdk
Conflicts: libclanlib1-png < 0.5.1-5mdk
Conflicts: libcups1 < 1.1.12-3mdk
Conflicts: libeel0 < 1.0.2-6mdk
Conflicts: libfnlib0 < 0.5-2mdk
Conflicts: libgd1 < 1.8.4-4mdk
Conflicts: libgtk+2 < 1.3.12-4mdk
Conflicts: libgtkxmhtml1 < 1.4.1.4-1mdk
Conflicts: libimlib1 < 1.9.11-8mdk
Conflicts: libqt2 < 2.3.1-24mdk
Conflicts: libwraster2 < 0.80.0-2mdk
Conflicts: linuxconf < 1.26r5-2mdk
Conflicts: nautilus < 1.0.6-8mdk
Conflicts: sawfish < 1.0-7mdk


%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n %{lib_name}-devel
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{lib_name} = %version-%release zlib-devel
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	png-devel = %{version}-%{release}

%description -n %{lib_name}-devel
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install the
libpng package.

%package -n %{lib_name}-static-devel
Summary:	Development static libraries
Group:		Development/C
Requires:	%{lib_name}-devel = %version-%release zlib-devel
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	png-static-devel = %{version}-%{release}

%description -n %{lib_name}-static-devel
Libpng development static libraries.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .mdkconf
ln -s scripts/makefile.linux ./Makefile
perl -pi -e 's|^prefix=.*|prefix=%{_prefix}|' Makefile

%build
%make
make test

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}
%makeinstall LIBPATH="\$(prefix)/%{_lib}"
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{3,5}
install -m 644 {libpng,libpngpf}.3 $RPM_BUILD_ROOT%{_mandir}/man3
install -m 644 png.5 $RPM_BUILD_ROOT%{_mandir}/man5/png3.5

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_prefix}/man

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root)
%doc *.txt example.c README TODO CHANGES
%{_libdir}/libpng.so.*
%{_libdir}/libpng12.so.*
%{_mandir}/man5/*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc *.txt example.c README TODO CHANGES
%{_bindir}/libpng12-config
%{_includedir}/*
%{_libdir}/libpng.so
%{_libdir}/libpng12.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%files -n %{lib_name}-static-devel
%defattr(-,root,root)
%doc README
%{_libdir}/libpng*.a


%clean
rm -rf %buildroot

%changelog
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
- Requires: %%version-%%release and not only %%version

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

