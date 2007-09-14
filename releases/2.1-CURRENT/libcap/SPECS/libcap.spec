#
# spec file for package libcap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		libcap
%define version		1.10
%define release		%_revrel

%define major		1
%define libname		%mklibname cap %{major}
%define devname		%mklibname cap -d

Summary:	Library for getting and setting POSIX.1e capabilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like and LGPL
Group:		System/Libraries
URL:		ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4
Source:		ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/%{name}-%{version}.tar.bz2
Patch0:		libcap-1.10-fdr-userland.patch
Patch1:		libcap-1.10-fdr-shared.patch
Patch2:		libcap-1.10-fdr-ia64.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.


%package -n %{libname}
Summary:	Library for getting and setting POSIX.1e capabilities
Group:		System/Libraries
Provides:	libcap = %{version}-%{release}
Obsoletes:	libcap

%description -n %{libname}
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.


%package -n %{devname}
Summary:	Development files for libcap
Group:		Development/Libraries
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname cap 1 -d

%description -n %{devname}
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Development files (Headers, libraries for static linking, etc) for libcap.


%package utils
Summary:	Administration tools for POSIX.1e capabilities
Group:		System/Base
Requires:	%{libname} = %{version}

%description utils
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

This package contains utilities to control these capabilities.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .userland
%patch1 -p1 -b .shared
%patch2 -p1 -b .ia64


%build
make PREFIX=%{_prefix} LIBDIR=%{_libdir} 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make install FAKEROOT=%{buildroot} \
    LIBDIR=%{buildroot}%{_libdir} \
    SBINDIR=%{buildroot}%{_sbindir} \
    INCDIR=%{buildroot}%{_includedir} \
    MANDIR=%{buildroot}%{_mandir}/ \
    COPTFLAG="%{optflags}"

chmod +x %{buildroot}%{_libdir}/*.so.*

# remove manpages that are already in man-pages
rm -rf %{buildroot}%{_mandir}/man2


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files utils
%defattr(-,root,root)
%{_sbindir}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc CHANGELOG License README


%changelog
* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.10
- implement devel naming policy  
- implement library provides policy

* Sat Mar 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.10
- remove capget.2 and capset.2 as they're already in man-pages

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.10
- rebuild with gcc4
- add -doc subpackage
- add -doc subpackage
- fix calls to ldconfig
- spec cleanups

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.10
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.10
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.10-4avx
- minor spec cleanups

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.10-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.10-2avx
- bootstrap build

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.10-1avx
- first Annvix build, based on Fedora spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
