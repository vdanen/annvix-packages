%define name zlib
%define version	1.1.4
%define release 8mdk
%define lib_major 1
%define lib_name %{name}%{lib_major}

%define build_biarch 0
# Enable bi-arch build on x86-64
%ifarch x86_64
%define build_biarch 1
%endif

Name: %{name}
Summary: The zlib compression and decompression library
Version: %{version}
Release: %{release}
Source: http://prdownloads.sourceforge.net/libpng/zlib-%version.tar.bz2
Patch0:	zlib-1.1.3-glibc.patch.bz2
Patch1: zlib-1.1.4-multibuild.patch.bz2
Patch2: zlib-1.1.4-build-fPIC.patch.bz2
Patch3: zlib-1.1.4-gzprintf.patch.bz2
Group: System/Libraries
URL: http://www.gzip.org/zlib/
License: BSD
Packager: Guillaume Cottenceau <gc@mandrakesoft.com>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The zlib compression library provides in-memory compression and
decompression functions, including integrity checks of the uncompressed
data.  This version of the library supports only one compression method
(deflation), but other algorithms may be added later, which will have
the same stream interface.  The zlib library is used by many different
system programs.

%package -n %{lib_name}
Summary: The zlib compression and decompression library
Group: System/Libraries
Obsoletes: libz, libz1, %{name}
Provides: libz = %{version}-%{release} libz1 = %{version}-%{release} %{name} = %{version}-%{release}

%description -n %{lib_name}
The zlib compression library provides in-memory compression and
decompression functions, including integrity checks of the uncompressed
data.  This version of the library supports only one compression method
(deflation), but other algorithms may be added later, which will have
the same stream interface.  The zlib library is used by many different
system programs.

%package -n %{lib_name}-devel
Summary: Header files and libraries for developing apps which will use zlib
Group: Development/C
Requires: %{lib_name} = %{version}-%{release}
Obsoletes: libz1-devel, libz-devel, zlib-devel
Provides: libz-devel = %{version}-%{release} libz1-devel = %{version}-%{release} %{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

Install the zlib-devel package if you want to develop applications that
will use the zlib library.

%prep
%setup -q -n zlib-%{version}
%patch0 -p1
%patch1 -p1 -b .multibuild
%patch2 -p1 -b .build-fPIC
%patch3 -p1 -b .gzprintf

%build
mkdir objs
pushd objs
  CFLAGS="$RPM_OPT_FLAGS" \
  ../configure --shared --prefix=%{_prefix} --libdir=%{_libdir}
  %make
  make test
popd

%if %{build_biarch}
mkdir objs32
pushd objs32
  CFLAGS="$RPM_OPT_FLAGS" CC="%{__cc} -m32" \
  ../configure --shared --prefix=%{_prefix}
  %make
  make test
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_prefix}
install -d $RPM_BUILD_ROOT/%{_libdir}

make install -C objs prefix=$RPM_BUILD_ROOT%{_prefix} libdir=$RPM_BUILD_ROOT%{_libdir}
%if %{build_biarch}
make install-libs -C objs32 prefix=$RPM_BUILD_ROOT%{_prefix}
%endif

install -m644 zutil.h $RPM_BUILD_ROOT/%{_includedir}/zutil.h
install -d $RPM_BUILD_ROOT/%{_mandir}/man3
install -m644 zlib.3 $RPM_BUILD_ROOT/%{_mandir}/man3

install -d $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/*.so.* $RPM_BUILD_ROOT/%{_lib}/
ln -s ../../%{_lib}/libz.so.%{version} $RPM_BUILD_ROOT%{_libdir}/

%if %{build_biarch}
install -d $RPM_BUILD_ROOT/lib
mv $RPM_BUILD_ROOT%{_prefix}/lib/*.so.* $RPM_BUILD_ROOT/lib/
ln -s ../../lib/libz.so.%{version} $RPM_BUILD_ROOT%{_prefix}/lib/
%endif

%clean
rm -fr $RPM_BUILD_ROOT

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
%doc README ChangeLog algorithm.txt
%{_libdir}/*.a
%{_libdir}/*.so
%if %{build_biarch}
%{_prefix}/lib/*.a
%{_prefix}/lib/*.so
%endif
%{_includedir}/*
%{_mandir}/*/*

%changelog
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
