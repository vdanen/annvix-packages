#
# spec file for package linux-atm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		linux-atm
%define version		2.4.1
%define release		%_revrel

%define major		1
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	Tools and libraries for ATM
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://linux-atm.sourceforge.net
Source:		%{name}-%{version}.tar.bz2
Patch0:		linux-atm-2.4.1-gcc3.4-fix.patch
Patch1:		linux-atm-2.4.1-libtool-fixes.patch
Patch2:		linux-atm-2.4.1-64bit-fixes.patch
Patch3:		linux-atm-2.4.1-gcc4.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	automake1.4

%description
Tools and libraries to support ATM (Asynchronous Transfer Mode)
networking and some types of DSL modems.


%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This package contains libraries needed to run programs linked with %{name}.


%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 -d

%description -n %{devname}
This package contains development files needed to compile programs which
use %{name}.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .gcc3.4
%patch1 -p1 -b .libtool-fixes
%patch2 -p1 -b .64bit-fixes
%patch3 -p1 -b .gcc4

# stick to builtin libtool 1.4
%define __libtoolize /bin/true
autoconf
automake-1.4 --foreign


%build
%configure2_5x --enable-shared
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/atmsigd.conf
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man4/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la

%files doc
%defattr(-,root,root)
%doc README AUTHORS ChangeLog NEWS THANKS BUGS
%doc COPYING COPYING.GPL COPYING.LGPL


%changelog
* Sun Sep 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1
- implement devel naming policy
- implement library provides policy

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-9avx
- P3: gcc4 fixes mostly from fedora (gbeauchesne)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-8avx
- bootstrap build (new gcc, new glibc)
- patches from mdk for gcc, libtool, and 64bit fixes
- BuildRequires: bison

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-7avx
- rebuild

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-6avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 2.4.1-5sls
- minor spec cleanups

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 2.4.1-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
