#
# spec file for package blt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		blt
%define version		2.4z
%define release		%_revrel

%define major		2
%define	libname		%mklibname %{name} %{major}
%define	devname		%mklibname %{name} -d

Summary:	A Tk toolkit extension, including widgets, geometry managers, etc
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
URL:		http://www.sourceforge.net/projects/blt
Source0:	BLT%{version}.tar.bz2
Patch0:		blt2.4z-patch-2.patch
Patch1:		blt2.4z-configure.in-disable-rpath.patch
Patch2:		blt2.4z-libdir.patch
Patch3:		blt2.4z-mkdir_p.patch
Patch4:		blt2.4z-64bit-fixes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  libx11-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	autoconf2.1

Requires:	%{libname}

%description
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.


%package scripts
Summary:	TCL Libraries for BLT
Group:		System/Libraries

%description scripts
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.


%package -n %{libname}
Summary:	Shared libraries needed to use BLT
Group:		System/Libraries
Requires:	blt-scripts = %{version}
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

This package provides libraries needed to use BLT.


%package -n %{devname}
Summary:	Headers of BLT
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 2 -d

%description -n %{devname}
BLT is an extension to the Tk toolkiy. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to any patching
of the Tcl or Tk source file to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

This package provides headers needed to build packages based on BLT.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1 -b .rpath
%patch2 -p1 -b .libdir
%patch3 -p1 -b .mkdir_p
%patch4 -p1 -b .64bit-fixes
autoconf-2.13


%build
%configure
%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

ln -sf libBLT24.so %{buildroot}%{_libdir}/libBLT.so
ln -sf libBLTlite24.so %{buildroot}%{_libdir}/libBLTlite.so
ln -sf bltwish24 %{buildroot}%{_bindir}/bltwish
ln -sf bltsh24 %{buildroot}%{_bindir}/bltsh

# Dadou - 2.4u-2mdk - Don't put in %%{_libdir} things which should be in %%{_docdir}
rm -fr %{buildroot}/%{_prefix}/lib/blt2.4/demos
rm -fr %{buildroot}/%{_prefix}/lib/blt2.4/NEWS
rm -fr %{buildroot}/%{_prefix}/lib/blt2.4/PROBLEMS
rm -fr %{buildroot}/%{_prefix}/lib/blt2.4/README

# Dadou - 2.4u-2mdk - Remove +x permissions in %%{_docdir} to be sure that RPM
#                     will don't want some strange dependencies
perl -pi -e "s|local/||" %{_builddir}/%{name}%{version}/demos/scripts/page.tcl
perl -pi -e "s|local/||" %{_builddir}/%{name}%{version}/html/hiertable.html

# Dadou - 2.4u-2mdk - Prevent conflicts with other packages
for i in bitmap graph tabset tree watch; do
    mv %{buildroot}/%{_mandir}/mann/$i{,-blt}.n
done

%multiarch_includes %{buildroot}%{_includedir}/bltHash.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/mann/*
%{_mandir}/man3/*

%files scripts
%defattr(-,root,root,-)
%dir %{_prefix}/lib/blt2.4
%{_prefix}/lib/blt2.4/*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/*.so

%files -n %{devname}
%defattr(-,root,root,-)
%{_includedir}/*.h
%multiarch %{multiarch_includedir}/*.h
%{_libdir}/*.a

%files doc
%defattr(-,root,root,-)
%doc MANIFEST NEWS PROBLEMS README
%doc demos/
%doc examples/
%doc html/


%changelog
* Fri Dec 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.4z
- rebuild against new tcl, tk

* Fri Sep 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.4z
- use autoconf-2.13 explicitly
- implement devel naming policy
- implement library provides policy

* Thu Apr 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.4z
- build against modular X

* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4z
- rebuild against new tcl and tk
- fix deps

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4z
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4z
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4z
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4z-12avx
- rebuild against new tcltk

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4z-11avx
- bootstrap build (new gcc, new glibc)
- multiarch

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4z-10avx
- bootstrap build
- spec cleanups

* Mon Aug 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4z-9avx
- fix dangling symlinks

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4z-8avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 2.4z-7sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 2.4z-6sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
