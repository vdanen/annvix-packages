#
# spec file for package xpm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		xpm
%define version		3.4k
%define release		%_revrel

%define	major		4
%define	LIBVER		4.11
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	A pixmap library for the X Window System
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
URL:		http://freshmeat.net/redir/libxpm/18465/url_homepage/
Source0:	ftp://ftp.x.org/contrib/libraries/xpm-%{version}.tar.bz2
Source3:	ftp://ftp.x.org/contrib/libraries/xpm-FAQ.html
Source4:	ftp://ftp.x.org/contrib/libraries/xpm-README.html
Source5:	ftp://ftp.x.org/contrib/libraries/xpm_examples.tar.bz2
Patch0:		xpm-3.4k-shlib.patch
Patch1:		xpm-3.4k-fixes.patch
Patch2:		xpm-3.4k-alpha.patch
Patch3:		xpm-3.4k-xfree43merge.patch
Patch4:		xpm-3.4k-64bit-fixes.patch
Patch5:		xpm-3.4-CAN-2004-0687-0688.patch
Patch6:		xpm-3.4k-CAN-2004-0914.patch
Patch7:		xpm-3.4k-s_popen-xpm_write.patch
Patch8:		xpm-3.4k-avx-norman.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	imake
BuildRequires:	libx11-devel
BuildRequires:	libxt-devel
BuildRequires:	libxext-devel

%description
The xpm package contains the XPM pixmap library for the X Window
System.  The XPM library allows applications to display color,
pixmapped images, and is used by many popular X programs.


%package -n %{libname}
Summary:	A pixmap library for the X Window System
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
The xpm package contains the XPM pixmap library for the X Window
System.  The XPM library allows applications to display color,
pixmapped images, and is used by many popular X programs.


%package -n %{devname}
Summary:	Tools for developing apps which will use the XPM pixmap library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 4 -d

%description -n %{devname}
The xpm-devel package contains the development libraries and header
files  necessary for developing applications which will use the XPM
library.  The XPM library is used by many programs for displaying
pixmaps in the X Window System.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .shlib
%patch1 -p1 -b .fixes
%patch2 -p1 -b .alpha
%patch3 -p1 -b .xf86-4.3-merge
%patch4 -p1 -b .64bit-fixes
%patch5 -p1 -b .CAN-2004-0687-0688
%patch6 -p1 -b .CAN-2004-0914
%patch7 -p1 -b .s_popen-xpm_write

for i in xpm-FAQ.html xpm-README.html xpm_examples.tar.bz2 ; do
    cp %{_sourcedir}/${i} .
done


%build
xmkmf
make Makefiles

mkdir -p exports/include/X11
cp lib/*.h exports/include/X11
# %%make doesn't work on more than 2 cpu
%make CDEBUGFLAGS="%{optflags}" CXXDEBUGFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
#ln -sf libXpm.so.%{LIBVER} %{buildroot}%{prefix}/%{_lib}/libXpm.so


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libXpm.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/X11/*
%{_libdir}/libXpm.so

%files doc
%defattr(-,root,root)
%doc xpm-FAQ.html xpm-README.html xpm_examples.tar.bz2
%doc CHANGES COPYRIGHT FAQ.html FILES README.html


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.4k
- rebuild against new libx11

* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.4k
- implement devel naming policy
- implement library provides policy

* Thu Apr 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.4k
- rebuild against new libx11 and (many) friends

* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.4k
- rebuild (needed to build php-gd)
- clean some provides and obsoletes
- don't use %%libnamedev macro
- buildreq: X11-devel instead of XFree86-devel

* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4k
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4k
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4k-5105avx
- Obfuscate email addresses and new tagging
- Uncompress patches
- drop the PS files

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4k-33avx
- P5: fix for CAN-2004-0687 and CAN-2004-0688
- P6: fix for CAN-2004-0914
- P8: don't use rman so we don't have to add xorg as a BuildReq

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4k-32avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4k-31avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.4k-30avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 3.4k-29sls
- minor spec cleanups
- remove postscript docs

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 3.4k-28sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
