#
# spec file for package gd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gd
%define version		2.0.33
%define release		%_revrel

%define major		2
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d
%define odevname	%mklibname %{name} 2 -d
%define staticdevname	%mklibname %{name} -d -s

Summary:	A library used to create PNG, JPEG, or WBMP images
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-style
Group:		System/Libraries
URL:		http://www.boutell.com/gd/
Source0:	http://www.boutell.com/gd/http/%{name}-%{version}.tar.bz2
Patch0:		gd-2.0.33-CAN-2004-0941.patch
Patch1:		gd-2.0.33-CVE-2006-2906.patch
Patch2:		gd-2.0.33-CVE-2007-0455.patch
Patch3:		gd-cvs-CVE-2007-2756.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	x11-devel
BuildRequires:	xpm-devel
BuildRequires:	zlib-devel

%description
gd is a graphics library. It allows your code to quickly draw
images complete with lines, arcs, text, multiple colors, cut and
paste from other images, and flood fills, and write out the result
as a PNG or JPEG file. This is particularly useful in World Wide
Webapplications, where PNG and JPEG are two of the formats
accepted for inlineimages by most browsers.


%package -n %{libname}
Summary:	A library used to create PNG, JPEG, or WBMP images
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	%{libname} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	%{name}

%description -n	%{libname}
This package contains the library needed to run programs
dynamically linked with libgd

gd is a graphics library. It allows your code to quickly draw
images complete with lines, arcs, text, multiple colors, cut and
paste from other images, and flood fills, and write out the result
as a PNG or JPEG file. This is particularly useful in World Wide
Webapplications, where PNG and JPEG are two of the formats
accepted for inlineimages by most browsers.


%package -n %{devname}
Summary:	The development libraries and header files for gd
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{odevname}

%description -n	%{devname}
These are the development libraries and header files for gd,
the .png and .jpeg graphics library.

gd is a graphics library. It allows your code to quickly draw
images complete with lines, arcs, text, multiple colors, cut and
paste from other images, and flood fills, and write out the result
as a PNG or JPEG file. This is particularly useful in World Wide
Webapplications, where PNG and JPEG are two of the formats
accepted for inlineimages by most browsers.


%package -n %{staticdevname}
Summary:	Static GD library
Group:		Development/C
Requires:	%{devname} = %{version}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 2 -d -s

%description -n	%{staticdevname}
This package contains static gd library.


%package utils
Summary:	The Utils files for gd
Group:		System/Libraries
Requires:	%{libname} = %{version}

%description utils
gd is a graphics library. It allows your code to quickly draw
images complete with lines, arcs, text, multiple colors, cut and
paste from other images, and flood fills, and write out the result
as a PNG or JPEG file. This is particularly useful in World Wide
Webapplications, where PNG and JPEG are two of the formats
accepted for inlineimages by most browsers.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n gd-%{version}
%patch0 -p1 -b .CAN-2004-0941
%patch1 -p1 -b .cve-2006-2906
%patch2 -p1 -b .cve-2007-0455
%patch3 -p0 -b .cve-2007-2756


%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal-1.7; automake-1.7 --copy --add-missing; autoconf

%configure2_5x

%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall
%multiarch_binaries %{buildroot}%{_bindir}/gdlib-config
%multiarch_includes %{buildroot}%{_includedir}/gd.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_bindir}/gdlib-config
%multiarch %{multiarch_bindir}/gdlib-config
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*.h
%multiarch %{multiarch_includedir}/*.h

%files -n %{staticdevname}
%defattr(-,root,root)
%{_libdir}/lib*.a

%files utils
%defattr(-,root,root)
%{_bindir}/annotate
%{_bindir}/bdftogd
%{_bindir}/gd2copypal
%{_bindir}/gd2topng
%{_bindir}/gdparttopng
%{_bindir}/gdtopng
%{_bindir}/pngtogd
%{_bindir}/pngtogd2
%{_bindir}/webpng
%{_bindir}/gd2togif
%{_bindir}/gdcmpgif
%{_bindir}/giftogd2

%files doc
%defattr(-,root,root)
%doc README.TXT index.html


%changelog
* Fri Jul 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.33
- P3: security fix for CVE-2007-2756
- implement devel naming policy
- implement library provides policy

* Thu Jun 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.33
- buildrequires fontconfig

* Thu Apr 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.33
- build against modular X

* Tue Feb 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.33
- P2: security fix for CVE-2007-0455

* Sat Dec 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.33
- rebuild against new gettext
- spec cleanups

* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.33
- add -doc subpackage
- rebuild with gcc4
- P1: security fix for CVE-2006-2906

* Fri Apr 21 2006 Vincent Daen <vdanen-at-build.annvix.org> 2.0.33
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
