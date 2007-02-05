#
# spec file for package libevent
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libevent
%define version		1.2a
%define release		%_revrel

%define	major		1
%define libname		%mklibname event %{major}

Summary:	Abstract asynchronous event notification library
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License:	BSD
URL:		http://www.monkey.org/~provos/libevent/
Source0:	http://www.monkey.org/~provos/%{name}-%{version}.tar.gz
Patch0:		libevent-version-info-only.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	libtool

%description
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

%package -n %{libname}
Summary:	Abstract asynchronous event notification library
Group:          System/Libraries

%description -n	%{libname}
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

%package -n %{libname}-devel
Summary:	Static library and header files for the libevent library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

This package contains the static libevent library and its header files needed
to compile applications such as stegdetect, etc.


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
libtoolize --copy --force; aclocal; autoconf --force; autoheader; automake

export CFLAGS="%{optflags} -fPIC"

%configure2_5x

%make

%check
pushd test
    make verify
popd

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# don't enforce python deps here
rm -f %{buildroot}%{_bindir}/event_rpcgen.py

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc README event_rpcgen.py


%changelog
* Thu Dec 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2a
- first Annvix build (for nfsv4 support)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
