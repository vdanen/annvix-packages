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

%define prefix		/usr/X11R6
%define	major		4
%define	LIBVER		4.11
%define libname		%mklibname %{name} %{major}
%define libnamedev	%mklibname %{name} %{major} -d

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
BuildRequires:	XFree86-devel

%description
The xpm package contains the XPM pixmap library for the X Window
System.  The XPM library allows applications to display color,
pixmapped images, and is used by many popular X programs.


%package -n %{libname}
Summary:	A pixmap library for the X Window System
Group:		System/Libraries
Provides:	%{name}
Provides:	xpm3.4k
Obsoletes:	%{name}
Provides:	xpm3.4k

%description -n %{libname}
The xpm package contains the XPM pixmap library for the X Window
System.  The XPM library allows applications to display color,
pixmapped images, and is used by many popular X programs.


%package -n %{libnamedev}
Summary:	Tools for developing apps which will use the XPM pixmap library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel
Provides:	lib%{name}-devel
Provides:	xpm3.4k-devel
Obsoletes:	%{name}-devel
Obsoletes:	xpm3.4k-devel

%description -n %{libnamedev}
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

# we have to patch the Makefiles after they're made
cat %{_sourcedir}/xpm-3.4k-avx-norman.patch | patch -p1

mkdir -p exports/include/X11
cp lib/*.h exports/include/X11
# %%make doesn't work on more than 2 cpu
%make CDEBUGFLAGS="%{optflags}" CXXDEBUGFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
ln -sf libXpm.so.%{LIBVER} %{buildroot}%{prefix}/%{_lib}/libXpm.so


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{prefix}/%{_lib}/libXpm.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%{prefix}/bin/*
%{prefix}/include/X11/*
%{prefix}/%{_lib}/libXpm.a
%{prefix}/%{_lib}/libXpm.so

%files doc
%defattr(-,root,root)
%doc xpm-FAQ.html xpm-README.html xpm_examples.tar.bz2
%doc CHANGES COPYRIGHT FAQ.html FILES README.html


%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.4k
- rebuild (needed to build php-gd)

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
