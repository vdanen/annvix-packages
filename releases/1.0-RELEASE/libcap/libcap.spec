%define name 	libcap
%define version	1.10
%define release	1avx
%define sname	cap

%define major	1
%define minor	10
%define libname	%mklibname %sname %major

Summary:	Library for getting and setting POSIX.1e capabilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like and LGPL
Group:		System/Libraries
Source:		ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/%{name}-%{version}.tar.bz2
Patch0:		libcap-1.10-fdr-userland.patch.bz2
Patch1:		libcap-1.10-fdr-shared.patch.bz2
Patch2:		libcap-1.10-fdr-ia64.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root

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
Requires:	%{libname} = %{version}-%{release}

%description -n %{libname}-devel
Development files (Headers, libraries for static linking, etc) for libcap.

libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install libcap-devel if you want to develop or compile applications using
libcap.

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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

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
* Wed Jun 23 2004 Vincent Danen <vdanen@annvix.org> 1.10-1avx
- first Annvix build, based on Fedora spec
