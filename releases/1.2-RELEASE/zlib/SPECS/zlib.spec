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

%define lib_major	1
%define lib_name	%{name}%{lib_major}

%define build_biarch	0

# Enable bi-arch build on x86-64 and sparc64
%ifarch x86_64 sparc64
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


%package -n %{lib_name}
Summary:	The zlib compression and decompression library
Group:		System/Libraries
Obsoletes:	libz, libz1, %{name}
Provides:	libz = %{version}-%{release} libz1 = %{version}-%{release} %{name} = %{version}-%{release}

%description -n %{lib_name}
The zlib compression library provides in-memory compression and
decompression functions, including integrity checks of the uncompressed
data.  This version of the library supports only one compression method
(deflation), but other algorithms may be added later, which will have
the same stream interface.  The zlib library is used by many different
system programs.


%package -n %{lib_name}-devel
Summary:	Header files and libraries for developing apps which will use zlib
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Obsoletes:	libz1-devel, libz-devel, zlib-devel
Provides:	libz-devel = %{version}-%{release} libz1-devel = %{version}-%{release} %{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

Install the zlib-devel package if you want to develop applications that
will use the zlib library.


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


%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig


%files -n %{lib_name}
%defattr(-, root, root)
%doc README
/%{_lib}/libz.so.*
%{_libdir}/libz.so.*
%if %{build_biarch}
/lib/libz.so.*
%{_prefix}/lib/libz.so.*
%endif

%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc ChangeLog algorithm.txt
%{_libdir}/*.a
%{_libdir}/*.so
%if %{build_biarch}
%{_prefix}/lib/*.a
%{_prefix}/lib/*.so
%endif
%{_includedir}/*
%{_mandir}/*/*


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Dec 28 2005 Vincent Danen <vdanen-at-build.annvix.org>
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

* Tue Jul  8 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.4-8mdk
- rebuild for new devel provides

* Mon May 12 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.1.4-7mdk
- Rebuild to get new devel dep/requires

* Sat Apr 26 2003 Stefan van der Eijk <stefan@eijk.nu> 1.1.4-6mdk
- rebuild

* Fri Mar 14 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.1.4-5mdk
- fix gzprintf() vuln (CAN-2003-107)

* Thu Jan 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1.4-4mdk
- Enable biarch build on x86-64
- Patch1: Enable separate build dirs
- Patch2: Build all flavors of libs if necessary

* Fri Jun  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1.4-3mdk
- make test in %%build
- rpmlint fixes: strange-permission, configure-without-libdir-spec,
  hardcoded-library-path

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1.4-2mdk
- Automated rebuild in gcc3.1 environment

* Fri Mar 22 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.4-1mdk
- new version

* Tue Feb 19 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.3-19mdk
- rebuild

* Tue Oct 16 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.3-18mdk
- fix shlib-with-non-pic-code

* Tue Oct 16 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.3-17mdk
- fix strange-permission
- fix no-documentation

* Tue Sep 11 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.3-16mdk
- rebuild
- undadouize specfile

* Mon Feb 26 2001 Pixel <pixel@mandrakesoft.com> 1.1.3-15mdk
- move the lib to /lib

* Wed Jan 17 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.1.3-14mdk
- obsoletes zlib to be able to upgrade...

* Fri Jan 12 2001 David BAUDENS <baudens@mandrakesoft.com> 1.1.3-13mdk
- Fix libdification disastear
- s/Copyright/License
- Fix Requires section
- Macros
- Spec clean up

# Dadou - 1.1.3-13mdk - This one was 1.1.3-12mdk
* Thu Jan 11 2001 Francis Galiegue <fg@mandrakesoft.com> 1.1.3-1mdk
- New lib policy:
  * s,zlib,libz1,
  * Obsoletes and provides zlib (and -devel)
- Some spec file fixes

* Thu Aug 31 2000 Etienne Faure <etienne@mandrakesoft.com> 1.1.3-11mdk
- rebuilt with %doc and _mandir macros

* Mon Apr 03 2000 Jerome Martin <jerome@mandrakesoft.com> 1.1.3-10mdk
- specfile updated to work with spec-helper
- fixed group

* Wed Nov  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build Release.

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Tue Jul 12 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.de>
- handle RPM_OPT_FLAGS

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- link against glibc

* Mon Jul 27 1998 Jeff Johnson <jbj@redhat.com>
- upgrade to 1.1.3

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.1.2
- buildroot

* Tue Oct 07 1997 Donnie Barnes <djb@redhat.com>
- added URL tag (down at the moment so it may not be correct)
- made zlib-devel require zlib

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
