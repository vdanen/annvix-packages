#
# spec file for package freetype2
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		freetype2
%define	version		2.1.10
%define release		%_revrel

%define major		6
%define libname		%mklibname freetype %{major}

Summary:	A free and portable TrueType font rendering engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	FreeType License/GPL
Group:		System/Libraries
URL:		http://www.freetype.org/
Source0:	ftp://ftp.freetype.org/pub/freetype/freetype2/freetype-%{version}.tar.bz2
# (fc) 2.1.10-2mdk CVS bug fixes, mostly for embolding
Patch0:		freetype-2.1.10-cvsfixes.patch
# (fc) 2.1.10-3mdk put back internal API, used by xorg (Mdk bug #14636) (David Turner)
Patch1:		freetype-2.1.10-xorgfix.patch
# (fc) 2.1.10-5mdk fix autofit render setup (CVS)
Patch2:		freetype-2.1.10-fixautofit.patch
# (fc) 2.1.10-5mdk fix memleak (CVS)
Patch3:		freetype-2.1.10-memleak.patch
Patch4:		freetype-2.1.10-CVE-2006-0747.patch
Patch5:		freetype-2.1.10-ttkern-dos.patch
Patch6:		freetype-2.1.10-CVE-2006-2661.patch
Patch7:		freetype-2.1.10-CVE-2006-1861.patch
Patch8:		freetype-2.1.10-CVE-2006-1861-2.patch
Patch9:		freetype-2.1.10-CVE-2006-3467.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	zlib-devel
BuildRequires:	multiarch-utils

%description
The FreeType2 engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of
platforms and environments. Note that FreeType2 is a library, not a
stand-alone application, though some utility applications are included


%package -n %{libname}
Summary:	Shared libraries for a free and portable TrueType font rendering engine
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
The FreeType2 engine is a free and portable TrueType font rendering
engine.  It has been developed to provide TT support to a great
variety of platforms and environments. Note that FreeType2 is a
library, not a stand-alone application, though some utility
applications are included


%package -n %{libname}-devel
Summary:	Header files and static library for development with FreeType2
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	zlib-devel
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libfreetype-devel = %{version}-%{release}

%description -n %{libname}-devel
This package is only needed if you intend to develop or compile applications
which rely on the FreeType2 library. If you simply want to run existing
applications, you won't need this package.


%package -n %{libname}-static-devel
Summary:	Static libraries for programs which will use the FreeType2 library
Group:		Development/C
Requires:	%{libname}-devel = %{version}
Obsoletes:	%{name}-static-devel
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n %{libname}-static-devel
This package includes the static libraries necessary for 
developing programs which will use the FreeType2 library.


%prep
%setup -q -n freetype-%{version}
%patch0 -p1 -b .cvsfixes
%patch1 -p1 -b .xorgfix
%patch2 -p1 -b .fixautofit
%patch3 -p1 -b .memleak
%patch4 -p1 -b .cve-2006-0747
%patch5 -p1 -b .ttkern-dos
%patch6 -p1 -b .cve-2006-2661
%patch7 -p1 -b .cve-2006-1861
%patch8 -p1 -b .cve-2006-1861-2
%patch9 -p1 -b .cve-2006-3467


%build
%{?__cputoolize: %{__cputoolize} -c builds/unix}
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

%multiarch_binaries %{buildroot}%{_bindir}/freetype-config
%multiarch_includes %{buildroot}%{_includedir}/freetype2/freetype/config/ftconfig.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%{_bindir}/freetype-config
%{_libdir}/*.so
%{_libdir}/*.la
%dir %{_includedir}/freetype2
%{_includedir}/freetype2/*
%{_includedir}/ft2build.h
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%multiarch %{multiarch_bindir}/freetype-config
%multiarch %dir %{multiarch_includedir}/freetype2
%multiarch %{multiarch_includedir}/freetype2/*


%files -n %{libname}-static-devel
%defattr(-, root, root)
%{_libdir}/*.a


%changelog
* Fri Feb 02 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10
- P4: security fix for CVE-2006-0747
- P5: security fix for ttkern DoS
- P6: security fix for CVE-2006-2661
- P7: security fix for CVE-2006-1861
- P8: security fix for CVE-2006-1861 (additional fixes)
- P9: security fix for CVE-2006-3467

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10
- Obfuscate email addresses and new tagging
- Uncompress patches
- rpmlint fix: %%{libname}-devel also provides libfreetype-devel

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10-2avx
- drop P4; not needed

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10-1avx
- 2.1.10
- sync patches with mandriva 2.1.10-6mdk (not that we really care about
  having a 100% freetype, but it's no real skin off our back)
- drop the docs
- multiarch support

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.4-11avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.4-10avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen@opensls.org> 2.1.4-9avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.1.4-8sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.1.4-7sls
- OpenSLS build
- tidy spec
- remove PLF stuff

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
