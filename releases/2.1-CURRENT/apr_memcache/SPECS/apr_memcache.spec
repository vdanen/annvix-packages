#
# spec file for package apr_memcache
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		apr_memcache
%define version		0.7.0
%define release		%_revrel

%define major		0
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	A client for memcached
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Libraries
URL:		http://www.outoforder.cc/projects/libs/apr_memcache/
Source0:	http://www.outoforder.cc/downloads/apr_memcache/%{name}-%{version}.tar.bz2
Patch0:		apr_memcache-from_apr-util_HEAD.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	automake1.9
BuildRequires:	libtool
BuildRequires:	apr-devel >= 1.2.2
BuildRequires:	apr-util-devel >= 1.2.2

%description
apr_memcache is a client for memcached written in C, using APR and APR-Util. It
provides pooled client connections and is thread safe, making it perfect for
use inside Apache Modules.


%package -n %{libname}
Summary:	A client for memcached
Group: 		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
apr_memcache is a client for memcached written in C, using APR and APR-Util. It
provides pooled client connections and is thread safe, making it perfect for
use inside Apache Modules. 


%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = :%{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
apr_memcache is a client for memcached written in C, using APR and APR-Util. It
provides pooled client connections and is thread safe, making it perfect for
use inside Apache Modules.

This package contains the development files for %{name}.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1


%build
%serverbuild

sh ./autogen.sh

%configure2_5x \
    --enable-shared \
    --enable-static \
    --with-apr=%{_bindir}/apr-1-config \
    --with-apr-util=%{_bindir}/apu-1-config

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*

%files -n %{devname}
%defattr(-,root,root,-)
%dir %{_includedir}/apr_memcache-%{major}
%{_includedir}/apr_memcache-%{major}/*  
%{_libdir}/lib*.*a
%{_libdir}/lib*.so

%files doc
%defattr(-,root,root)
%doc LICENSE NOTICE test


%changelog
* Fri Sep 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.7.0
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
