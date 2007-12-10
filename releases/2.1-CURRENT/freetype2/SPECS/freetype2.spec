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
%define	version		2.3.5
%define release		%_revrel

%define major		6
%define libname		%mklibname freetype %{major}
%define devname		%mklibname freetype -d
%define staticdevname	%mklibname freetype -d -s

Summary:	A free and portable TrueType font rendering engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	FreeType License/GPL
Group:		System/Libraries
URL:		http://www.freetype.org/
Source0:	http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	zlib-devel
BuildRequires:	multiarch-utils
BuildRequires:	pkgconfig

%description
The FreeType2 engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of
platforms and environments. Note that FreeType2 is a library, not a
stand-alone application, though some utility applications are included


%package -n %{libname}
Summary:	Shared libraries for a free and portable TrueType font rendering engine
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	%{name}

%description -n %{libname}
The FreeType2 engine is a free and portable TrueType font rendering
engine.  It has been developed to provide TT support to a great
variety of platforms and environments. Note that FreeType2 is a
library, not a stand-alone application, though some utility
applications are included


%package -n %{devname}
Summary:	Header files and static library for development with FreeType2
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	zlib-devel
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname freetype 6 -d

%description -n %{devname}
This package is only needed if you intend to develop or compile applications
which rely on the FreeType2 library. If you simply want to run existing
applications, you won't need this package.


%package -n %{staticdevname}
Summary:	Static libraries for programs which will use the FreeType2 library
Group:		Development/C
Requires:	%{devname} = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%mklibname freetype 6 -d -s

%description -n %{staticdevname}
This package includes the static libraries necessary for 
developing programs which will use the FreeType2 library.


%prep
%setup -q -n freetype-%{version}


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
%{_libdir}/*.so.%{major}*

%files -n %{devname}
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


%files -n %{staticdevname}
%defattr(-, root, root)
%{_libdir}/*.a


%changelog
* Sun Dec 09 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- 2.3.5
- drop all patches, merged upstream
- update download url
- buildrequires pkgconfig

* Fri Jul 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10
- P10: security fix for CVE-2007-2754
- implement devel naming policy
- implement library provides policy

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
