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
%define version 	10.34
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
Source0:	http://prdownloads.sourceforge.net/netpbm/%{name}-%{version}.tar.bz2
Source1:	mf50-netpbm_filters
Source2:	test-images.tar.bz2
Source3:	http://prdownloads.sourceforge.net/netpbm/%{name}doc-%{version}.tar.bz2
Patch0:		netpbm-10.17-time.patch
Patch1:		netpbm-9.24-strip.patch
Patch3:		netpbm-10.32-message.patch
Patch4:		netpbm-10.22-security2.patch
Patch5:		netpbm-10.22-cmapsize.patch
Patch6:		netpbm-10.30-gcc4.patch
Patch7:		netpbm-10.34-security.patch
Patch11:	netpbm-10.24-nodoc.patch
Patch13:	netpbm-10.34-bmptopnm.patch
Patch14:	netpbm-10.28-CAN-2005-2471.patch
Patch15:	netpbm-10.33-ppmtompeg.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	flex
BuildRequires:	png-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	X11-devel
BuildRequires:	libxml2-devel

Requires:	%{libname} = %{version}-%{release}
Obsoletes:	libgr-progs
Obsoletes:	libgr1-progs
Provides:	libgr-progs
Provides:	libgr1-progs

%description
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.


%package -n %{libname}
Summary:        A library for handling different graphics file formats
Group:          System/Libraries
Provides:	lib%{name}
Provides:	libgr
Provides:	libgr1
Provides:	libnetpbm1
Obsoletes:      libgr
Obsoletes:	libgr1
Obsoletes:	libnetpbm1

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
Provides:	libgr-devel
Provides:	libgr1-devel
Provides:	libnetpbm1-devel
Provides:	netpbm-devel
Obsoletes:	libgr-devel
Obsoletes:	libgr1-devel
Obsoletes:	libnetpbm1-devel

%description -n %{libname}-devel
The netpbm-devel package contains the header files and programmer's
documentation for developing programs which can handle the various
graphics file formats supported by the netpbm libraries.


%package -n %{libname}-static-devel
Summary:	Static libraries for the netpbm libraries
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel
Provides:	libgr-static-devel
Provides:	libgr1-static-devel
Provides:	libnetpbm1-static-devel
Provides:	netpbm-static-devel
Obsoletes:	libgr-static-devel
Obsoletes:	libgr1-static-devel
Obsoletes:	libnetpbm1-static-devel

%description -n %{libname}-static-devel
The netpbm-devel package contains the static libraries (.a)
for developing programs which can handle the various
graphics file formats supported by the netpbm libraries.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 2
%patch0 -p1 -b .time
%patch1 -p1 -b .strip
%patch3 -p1 -b .message
%patch4 -p1 -b .security2
%patch5 -p1 -b .cmapsize
%patch7 -p1 -b .security
%patch6 -p1 -b .gcc4
%patch11 -p1 -b .nodoc
%patch13 -p1 -b .bmptopnm
%patch14 -p1 -b .CAN-2005-2471
%patch15 -p1 -b .ppmtompeg

tar xjf %{SOURCE2}
chmod 0644 doc/*


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
    LINUXSVGALIB="NONE" \
    X11LIB=%{_prefix}/X11R6/%{_lib}/libX11.so \
    TIFFLIB_DIR=%{_libdir}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}
make package pkgdir=%{buildroot}%{_prefix} LINUXSVGALIB="NONE"

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


%files -n %{libname}
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*.h
%multiarch %{multiarch_includedir}/pm_config.h
%attr(755,root,root) %{_libdir}/lib*.so
%{_mandir}/man3/*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man[15]/*
%{_datadir}/%{name}-%{version}
%dir %{_datadir}/printconf
%dir %{_datadir}/printconf/mf_rules
%dir %{_datadir}/printconf/tests
%{_datadir}/printconf/mf_rules/*
%{_datadir}/printconf/tests/*

%files doc
%defattr(-,root,root)
%doc doc/*


%changelog
* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 10.34
- build against new libxml2 

* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 10.34
- lib64 fix

* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 10.34
- 10.34
- buildrequires: libxml2-devel, X11-devel
- updated P3, P6, P7
- drop P2, P9, P13, P15 and commented P8, P12
- P15 from Fedora
- own it's own %%_datadir directories
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 10.29
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 10.29
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
