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
%define sname		cap

%define major		1
%define libname		%mklibname %{sname} %{major}

Summary:	Library for getting and setting POSIX.1e capabilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like and LGPL
Group:		System/Libraries
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
Obsoletes:	libcap
Provides:	libcap
Provides:	libcap = %{version}

%description -n %{libname}
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.


%package -n %{libname}-devel
Summary:	Development files for libcap
Group:		Development/Libraries
Obsoletes:	libcap-devel
Provides:	libcap-devel = %{version}-%{release}
Requires:	%{libname} = %{version}

%description -n %{libname}-devel
Development files (Headers, libraries for static linking, etc) for libcap.

libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.


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


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_sbindir}/*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man2/*
%{_mandir}/man3/*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org>
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
