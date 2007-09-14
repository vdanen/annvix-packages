#
# spec file for package libgssapi
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libgssapi
%define version		0.10
%define release		%_revrel

%define	major		2
%define libname		%mklibname gssapi %{major}

Summary:	A mechanism-switch gssapi library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		System/Libraries
URL:		http://www.citi.umich.edu/projects/nfsv4/linux/
Source0:        http://www.citi.umich.edu/projects/nfsv4/linux/%{name}/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	krb5-devel >= 1.3
BuildRequires:	autoconf2.5
BuildRequires:	pkgconfig
BuildRequires:	libtool

%description
libgssapi provides a gssapi interface, but does not implement any
gssapi mechanisms itself; instead it calls other gssapi functions
(e.g., those provided by MIT Kerberos), depending on the requested
mechanism, to do the work.


%package -n %{libname}
Summary:	A mechanism-switch gssapi library
Group:		System/Libraries

%description -n	%{libname}
libgssapi provides a gssapi interface, but does not implement any
gssapi mechanisms itself; instead it calls other gssapi functions
(e.g., those provided by MIT Kerberos), depending on the requested
mechanism, to do the work.

%package -n %{libname}-devel
Summary:	Static library and header files for the libgssapi library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libgssapi-devel = %{version}
Provides:	gssapi-devel = %{version}

%description -n	%{libname}-devel
libgssapi provides a gssapi interface, but does not implement any
gssapi mechanisms itself; instead it calls other gssapi functions
(e.g., those provided by MIT Kerberos), depending on the requested
mechanism, to do the work.

This package contains the static libgssapi library and its
header files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

# lib64 fix
perl -pi -e "s|/usr/lib|%{_libdir}|g" gssapi_mech.conf
perl -pi -e "s|/lib/|/%{_lib}/|g" configure*


%build
%configure2_5x

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}

%makeinstall_std

%multiarch_includes %{buildroot}%{_includedir}/gssglue/gssapi/gssapi.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%defattr(-,root,root)
%multiarch %{multiarch_includedir}/gssglue/gssapi/gssapi.h
%{_includedir}/gssglue/gssapi/gssapi.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/libgssapi.pc

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README


%changelog
* Thu Dec 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.10
- first Annvix build (for nfsv4 support)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
