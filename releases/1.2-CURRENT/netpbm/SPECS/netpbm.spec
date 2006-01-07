#
# spec file for package netpbm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		netpbm
%define version 	10.29
%define release 	%_revrel

%define major		10
%define libname		%mklibname %{name} %{major}


Summary:	Tools for manipulating graphics files in netpbm supported formats
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL Artistic MIT
Group:		Graphics
URL:		http://netpbm.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Source1:	mf50-netpbm_filters
Source2:	test-images.tar.bz2
Source3:	%{name}doc-%{version}.tar.bz2
Patch0:		netpbm-10.17-time.patch
Patch1:		netpbm-9.24-strip.patch
Patch2:		netpbm-10.18-manpath.patch
Patch3:		netpbm-10.19-message.patch
Patch4:		netpbm-10.22-security2.patch
Patch5:		netpbm-10.22-cmapsize.patch
Patch6:		netpbm-10.28-gcc4.patch
Patch7:		netpbm-10.23-security.patch
#Patch8:	netpbm-10.23-pngtopnm.patch.bz2
Patch9:		netpbm-10.26-libm.patch
Patch11:	netpbm-10.24-nodoc.patch
#Patch12:	pstopnm_dsafer.diff.bz2
Patch13:	netpbm-10.27-bmptopnm.patch
Patch14:	netpbm-10.28-CAN-2005-2471.patch
Patch15:	netpbm-10.29-CAN-2005-2978.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	flex, png-devel, jpeg-devel, tiff-devel

Requires:	%{libname} = %{version}-%{release}
Obsoletes:	libgr-progs, libgr1-progs
Provides:	libgr-progs, libgr1-progs

%description
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.


%package -n %{libname}
Summary:        A library for handling different graphics file formats
Group:          System/Libraries
Provides:	lib%{name}
Provides:	libgr, libgr1, libnetpbm1
Obsoletes:      libgr, libgr1, libnetpbm1

%description -n %{libname}
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.


%package -n %{libname}-devel
Summary:	Development tools for programs which will use the netpbm libraries
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel
Obsoletes:	libgr-devel, libgr1-devel, libnetpbm1-devel
Provides:	libgr-devel, libgr1-devel, libnetpbm1-devel, netpbm-devel

%description -n %{libname}-devel
The netpbm-devel package contains the header files and programmer's
documentation for developing programs which can handle the various
graphics file formats supported by the netpbm libraries.


%package -n %{libname}-static-devel
Summary:	Static libraries for the netpbm libraries
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel
Obsoletes:	libgr-static-devel, libgr1-static-devel, libnetpbm1-static-devel
Provides:	libgr-static-devel, libgr1-static-devel, libnetpbm1-static-devel, netpbm-static-devel

%description -n %{libname}-static-devel
The netpbm-devel package contains the static libraries (.a)
for developing programs which can handle the various
graphics file formats supported by the netpbm libraries.


%prep
%setup -q -a 2
%patch0 -p1 -b .time
%patch1 -p1 -b .strip
%patch2 -p1 -b .manpath
%patch3 -p1 -b .message
%patch4 -p1 -b .security2
%patch5 -p1 -b .cmapsize
%patch7 -p1 -b .security
%patch6 -p1 -b .gcc4
#%patch8 -p1 -b .pngtopnm
%patch9 -p1 -b .libm
%patch11 -p1 -b .nodoc
#%patch12 -p0 -b .dsafer
%patch13 -p1 -b .bmptopnm
%patch14 -p1 -b .CAN-2005-2471
%patch15 -p1 -b .can-2005-2978

#mv shhopt/shhopt.h shhopt/pbmshhopt.h
#perl -pi -e 's|shhopt.h|pbmshhopt.h|g' `find -name "*.c" -o -name "*.h"` ./GNUmakefile

tar xjf %{SOURCE2}


%build
./configure <<EOF
















EOF

TOP=`pwd`
make \
    CC=%{__cc} \
    CFLAGS="%{optflags} -fPIC" \
    LDFLAGS="-L$TOP/pbm -L$TOP/pgm -L$TOP/pnm -L$TOP/ppm" \
    JPEGINC_DIR=%{_includedir} \
    PNGINC_DIR=%{_includedir} \
    TIFFINC_DIR=%{_includedir} \
    JPEGLIB_DIR=%{_libdir} \
    PNGLIB_DIR=%{_libdir} \
    TIFFLIB_DIR=%{_libdir}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}
make package pkgdir=%{buildroot}%{_prefix}

# Ugly hack to have libs in correct dir on 64bit archs.
mkdir -p %{buildroot}%{_libdir}
if [ "%{_libdir}" != "/usr/lib" ]; then
    mv %{buildroot}/usr/lib/lib* %{buildroot}%{_libdir}
fi

cp -af lib/libnetpbm.a %{buildroot}%{_libdir}/libnetpbm.a
ln -sf libnetpbm.so.%{major} %{buildroot}%{_libdir}/libnetpbm.so

mkdir -p %{buildroot}%{_mandir}
tar jxf %{SOURCE3} -C %{buildroot}%{_mandir}

mkdir -p %{buildroot}%{_datadir}/%{name}-%{version}
mv %{buildroot}/usr/misc/*.map %{buildroot}%{_datadir}/%{name}-%{version}
rm -rf %{buildroot}/usr/README
rm -rf %{buildroot}/usr/VERSION
rm -rf %{buildroot}/usr/link
rm -rf %{buildroot}/usr/misc
rm -rf %{buildroot}/usr/man
rm -rf %{buildroot}/usr/pkginfo
rm -rf %{buildroot}/usr/config_template

mkdir -p %{buildroot}%{_datadir}/printconf/mf_rules
cp %{SOURCE1} %{buildroot}%{_datadir}/printconf/mf_rules/

mkdir -p %{buildroot}%{_datadir}/printconf/tests
cp test-images/* %{buildroot}%{_datadir}/printconf/tests/

# multiarch
%multiarch_includes %{buildroot}%{_includedir}/pm_config.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files 	-n %{libname}
%defattr(-,root,root)
%doc doc/*
%attr(755,root,root) %{_libdir}/lib*.so.*

%files 	-n %{libname}-devel
%defattr(-,root,root)
%doc doc/COPYRIGHT.PATENT doc/Netpbm.programming
%{_includedir}/*.h
%multiarch %{multiarch_includedir}/pm_config.h
%attr(755,root,root) %{_libdir}/lib*.so
%{_mandir}/man3/*

%files 	-n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man[15]/*
%{_datadir}/%{name}-%{version}/*.map
%{_datadir}/printconf/mf_rules/*
%{_datadir}/printconf/tests/*


%changelog
* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Oct 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 10.29-3avx
- P15: fix for CAN-2005-2978

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 10.29-2avx
- rebuild against new libtiff

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 10.29-1avx
- 10.29
- sync with cooker 10.29-1mdk

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.24-13avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.24-12avx
- rebuild

* Fri Sep 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.24-11avx
- include missing security patch for CAN-2003-0924
- spec cleanups

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.24-10avx
- require packages not files
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 9.24-9sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 9.24-8sls
- OpenSLS build
- tidy spec

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.24-7mdk
- Patch4: lib64 fixes
- Factor out mklibname invocations
- Provides: netbpm{,-static}-devel
- BuildRequires: jpeg-devel, tiff-devel

* Fri May 23 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 9.24-6mdk
- spec file changes (Per Øyvind Karlsen <peroyvind@sintrax.net>)
	use %mklibname
	added licenses(also released under Artistic and MIT)

* Tue Apr 1 2003 Vincent Danen <vdanen@mandrakesoft.com> 9.24-5mdk
- security patches

* Sun Jul  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.24-4mdk
- Move mapfiles to %_datadir/%{name}-%{version}/

* Mon Jul 01 2002 Yves Duret <yduret@mandrakesoft.com> 9.24-3mdk
- fix obsolets/provides of static-devel package thanx Frederic Crozat.

* Fri May 17 2002 Yves Duret <yduret@mandrakesoft.com> 9.24-2mdk
- 9.0 lib policy: added %libname-static-devel

* Fri Apr 19 2002 Yves Duret <yduret@mandrakesoft.com> 9.24-1mdk
- version 9.24.
- merged with redhat.
- fixed build (why are still some guys that does not use GNU autotools ??)
- added missing files.
- buildrequires

* Sun Jan 27 2002 Stefan van der Eijk <stefan@eijk.nu> 9.20-2mdk
- BuildRequires

* Tue Jan 22 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 9.20-1mdk
- Merge with RH.
- 9.20 (whooooooooooo).

* Wed Oct 10 2001 Till Kamppeter <till@mandrakesoft.com> 9.10-8mdk
- Another attempt to recompile it with libpng3

* Fri Oct 05 2001 Yves Duret <yduret@mandrakesoft.com> 9.10-7mdk
- recompiled with libpng3
- macros

* Sat Sep 09 2001 David BAUDENS <baudens@mandrakesoft.com> 9.10-6mdk
- Fix %%major number
- Requires %%{version}-%%{release} and not only %%{version}
- Fix %%doc

* Mon Aug 27 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.10-5mdk
- Explicitly use /sbin/ldconfig

* Wed Aug 08 2001 Yves Duret <yduret@mandrakesoft.com> 9.10-4mdk
- added a builrequires to zlib-devel (Buchan Milne <bgmilne@cae.co.za>)
- corrected the 4 no-ldconfig-symlink errors (thx titi)

* Fri Jul 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 9.10-3mdk
- added missing obsoletes on libgr1-progs

* Fri Jul 27 2001 Yves Duret <yduret@mandrakesoft.com> 9.10-2mdk
- added patch2 to fix bad include netpbm-shhopt.h
- added provides libgr

* Tue Jul 24 2001 Yves Duret <yduret@mandrakesoft.com> 9.10-1mdk
- first MandrakeSoft package (stolen from d3bi4n and PLD)
    Obsoletes libgr libgr-progs libgr-devel
