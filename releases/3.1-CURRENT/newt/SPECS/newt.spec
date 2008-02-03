#
# spec file for package newt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		newt
%define version 	0.52.6
%define release 	%_revrel

%define major		0.52
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	A development library for text mode user interfaces
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
Source:		ftp://ftp.redhat.com/pub/redhat/linux/code/newt/newt-%{version}.tar.gz
Patch0:		newt-gpm-fix.diff
Patch1:		newt-0.52.6-mdvconf.patch
Patch2:		newt-0.51.4-fix-wstrlen-for-non-utf8-strings.patch
Patch3:		newt-0.52.6-fdr-entry.patch
Patch4:		newt-0.52.6-fdr-countitems.patch
Patch5:		newt-0.52.6-fdr-cursor.patch
Patch6:		newt-0.52.6-fdr-memleaks.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glibc-static-devel
BuildRequires:	popt-devel
BuildRequires:	python-devel >= 2.2
BuildRequires:	slang-devel

Requires:	slang
Provides:	python-snack

%description
Newt is a programming library for color text mode, widget based user
interfaces.  Newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package contains a
/usr/bin/dialog replacement called whiptail.  Newt is based on the
slang library.


%package -n %{libname}
Summary:	Newt windowing toolkit development files library
Group:		Development/C
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
Newt is a programming library for color text mode, widget based user
interfaces.  Newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package contains the
shared library needed by programs built with newt. Newt is based on the
slang library.


%package -n %{devname}
Summary:	Newt windowing toolkit development files
Group:		Development/C
Requires:	slang-devel %{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0.51 -d

%description -n %{devname}
The newt-devel package contains the header files and libraries
necessary for developing applications which use newt.  Newt is
a development library for text mode user interfaces.  Newt is
based on the slang library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p0 -b .entry
%patch4 -p0 -b .countitems
%patch5 -p0 -b .cursor
%patch6 -p0 -b .memleaks


%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
%configure \
    --without-gpm-support \
    --without-tcl

%make
%make shared


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}
%makeinstall
ln -sf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}

rm -rf  %{buildroot}%{_libdir}/python{1.5,2.0,2.1,2.2,2.3.2.4}

%find_lang %{name}
%kill_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr (-,root,root)
%{_libdir}/libnewt.so.*

%files 
%defattr (-,root,root)
%{_bindir}/whiptail
%{_libdir}/python%{pyver}/site-packages/*
%{_mandir}/man1/whiptail.1*

%files -n %{devname}
%defattr (-,root,root)
%{_includedir}/newt.h
%{_libdir}/libnewt.a
%{_libdir}/libnewt.so

%files doc
%defattr (-,root,root)
%doc COPYING CHANGES
%doc tutorial.sgml


%changelog
* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.52.6
- 0.52.6
- updated P1 from Mandriva
- P3, P4, P5, P6: assorted fixes from Fedora
- provide python-snack instead of snack
- build against new slang
- implement devel naming policy
- implement library provides policy

* Fri May 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6
- rebuild againt new python

* Sat Jun 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6
- rebuild against new python
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6-5avx
- rebuild against new python

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6-4avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6-2avx
- bootstrap build
- don't apply P3 and build with stack protection

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6-1avx
- 0.51.6
- use %%pyver macro
- spec cleanups
- P3: don't compile the test file -static as it freaks out with our
  __guard symbols and such (from SSP)

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.51.4-10avx
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 0.51.4-9sls
- minor spec cleanups
- remove %%build_opensls macro

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 0.51.4-8sls
- sync with 7mdk (gbeauchesne): fix mklibnamization

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 0.51.4-7sls
- OpenSLS build
- tidy spec
- use %%build_opensls to build without gpm support

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
