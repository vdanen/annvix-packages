%define name	libtiff
%define	version	3.5.7
%define release 12sls

%define lib_version	3.5
%define lib_major	3
%define lib_name_orig	%mklibname tiff
%define lib_name	%{lib_name_orig}%{lib_major}

Summary:	A library of functions for manipulating TIFF format image files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		System/Libraries
URL:		http://www.libtiff.org/
Source0:	ftp://ftp.remotesensing.org/pub/libtiff/tiff-v%{version}.tar.bz2
Patch0:		tiff-v3.5-shlib.patch.bz2
Patch1:		%{name}-3.5.5-codecs.patch.bz2
Patch2:		%{name}-3.5.5-stupid_cd_output.patch.bz2
Patch3:		%{name}-3.5.5-buildroot.patch.bz2
Patch4:		tiff-v3.5.7-64bit.patch.bz2
Patch5:		tiff-v3.5.7-x86_64.patch.bz2
Patch6:		tiff-v3.5.7-deps.patch.bz2

BuildRoot:	%_tmppath/%{name}-%{version}-root
BuildRequires:	libjpeg-devel, 	zlib-devel

%description
The libtiff package contains a library of functions for manipulating TIFF
(Tagged Image File Format) image format files. TIFF is a widely used file
format for bitmapped images. TIFF files usually end in the .tif extension
and they are often quite large.

%package progs
Summary:	Binaries needed to manipulate TIFF format image files
Group:		Graphics
Requires:	%{lib_name} = %{version}-%{release}
Obsoletes:	libtiff3-progs
Provides:	libtiff3-progs = %{version}-%{release}

%description progs
This package provides binaries needed to manipulate TIFF format image files.

%package -n %{lib_name}
Summary:	A library of functions for manipulating TIFF format image files
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n %{lib_name}
The libtiff package contains a library of functions for manipulating TIFF
(Tagged Image File Format) image format files. TIFF is a widely used file
format for bitmapped images. TIFF files usually end in the .tif extension
and they are often quite large.

%package -n %{lib_name}-devel
Summary:	Development tools for programs which will use the libtiff library
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	tiff-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package contains the header files and .so libraries for developing
programs which will manipulate TIFF format image files using the libtiff
library.

%package -n %{lib_name}-static-devel
Summary:	Static libraries for programs which will use the libtiff library
Group:		Development/C
Requires:	%{lib_name}-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	tiff-static-devel = %{version}-%{release}

%description -n %{lib_name}-static-devel
This package contains the static libraries for developing
programs which will manipulate TIFF format image files using the libtiff
library.

%prep
%setup -q -n tiff-v%{version}
%patch0 -p1 -b .shlib
%patch1 -p1 -b .codecs
%patch2 -p1 -b .cd
%patch3 -p1 -b .buildroot
%patch4 -p1 -b .64bit
%patch5 -p1 -b .x86_64
%patch6 -p1 -b .deps

%build
find . -type 'd' -name 'CVS' | xargs rm -fr
perl -pi -e 's|(DIR_.*)="?/usr/lib"?|\1="%{_libdir}"|' config.site
%{?__cputoolize: %{__cputoolize}}
./configure --target=%{_target_platform} \
	--with-GCOPTS="$RPM_OPT_FLAGS" << EOF
no
%{_bindir}
%{_libdir}
%{_includedir}
%{_mandir}
%{_defaultdocdir}/%{name}-progs-%{version}
bsd-source-cat
yes
EOF
cd libtiff
ln -s libtiff.so.%{lib_version} libtiff.so
cd ..
COPTS="%{optflags}" make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/{%{_bindir},%{_datadir}}
make install
install -m644 %{name}/%{name}.so.%{lib_version} %{buildroot}/%{_libdir}

cd %{buildroot}/%{_libdir}
ln -sf %{name}.so.%{lib_version} %{name}.so
ln -sf %{name}.so.%{lib_version} %{name}.so.%{lib_major}

%post   -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files progs
%defattr(-,root,root,-)
#%doc Readme
%_bindir/*
%_mandir/man1/*

%files -n %{lib_name}
%defattr(-,root,root,-)
#%doc Readme
%_libdir/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root,-)
%doc COPYRIGHT README TODO VERSION html
%_includedir/*
%_libdir/*.so
%_mandir/man3/*

%files -n %{lib_name}-static-devel
%defattr(-,root,root,-)
%doc COPYRIGHT README TODO VERSION
%_libdir/*.a

%changelog
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
- provides %%version-%%release

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
- Use %%_tmppath for BuildRoot
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

