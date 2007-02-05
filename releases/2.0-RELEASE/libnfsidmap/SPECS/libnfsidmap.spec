#
# spec file for package libnfsidmap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$rev: 6159 $
%define name		libnfsidmap
%define version		0.16
%define release		%_revrel

%define	major		0
%define libname		%mklibname nfsidmap %{major}

Summary:	Library to help mapping id's, mainly for NFSv4
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		System/Libraries
URL:		http://www.citi.umich.edu/projects/nfsv4/linux/
Source0:	http://www.citi.umich.edu/projects/nfsv4/linux/libnfsidmap/libnfsidmap-%{version}.tar.bz2
Patch0:		nfsidmap-0.11-portable.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	automake1.7
BuildRequires:	autoconf2.5
BuildRequires:	pkgconfig
BuildRequires:	libtool

%description
libnfsidmap is a library holding mulitiple methods of mapping
names to id's and visa versa, mainly for NFSv4. 

When NFSv4 is using AUTH_GSS (which currently only supports
Kerberos v5), the NFSv4 server mapping functions MUST use
secure communications.


%package -n %{libname}
Summary:	Library to help mapping id's, mainly for NFSv4
Group:		System/Libraries
Provides:	libnfsidmap
Provides:	nfsidmap

%description -n	%{libname}
libnfsidmap is a library holding mulitiple methods of mapping
names to id's and visa versa, mainly for NFSv4. 

When NFSv4 is using AUTH_GSS (which currently only supports
Kerberos v5), the NFSv4 server mapping functions MUST use
secure communications.


%package -n %{libname}-devel
Summary:	Static library and header files for the nfsidmap library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libnfsidmap-devel = %{version}
Provides:	nfsidmap-devel  = %{version}

%description -n	%{libname}-devel
libnfsidmap is a library holding mulitiple methods of mapping
names to id's and visa versa, mainly for NFSv4. 

When NFSv4 is using AUTH_GSS (which currently only supports
Kerberos v5), the NFSv4 server mapping functions MUST use
secure communications.

This package contains the static libnfsidmap library and its
header files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0


%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force && aclocal-1.7 && autoconf && automake-1.7 --gnu

%configure2_5x

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname} 
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_mandir}/man3/*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/libnfsidmap.pc

%files doc
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING README


%changelog
* Thu Dec 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.16
- first Annvix build (for nfsv4 support)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
