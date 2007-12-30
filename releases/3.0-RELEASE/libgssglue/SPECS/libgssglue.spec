#
# spec file for package libgssglue
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libgssglue
%define version		0.1
%define release		%_revrel

%define	major		1
%define libname		%mklibname gssglue %{major}
%define devname		%mklibname gssglue -d

Summary:	A mechanism-switch gssapi library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		System/Libraries
URL:		http://www.citi.umich.edu/projects/nfsv4/linux/
Source0:        http://www.citi.umich.edu/projects/nfsv4/linux/%{name}/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	krb5-devel >= 1.3

%description
libgssglue provides a gssapi interface, but does not implement any
gssapi mechanisms itself; instead it calls other gssapi functions
(e.g., those provided by MIT Kerberos), depending on the requested
mechanism, to do the work.


%package -n %{libname}
Summary:	A mechanism-switch gssapi library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%mklibname gssapi 2

%description -n	%{libname}
libgssglue provides a gssapi interface, but does not implement any
gssapi mechanisms itself; instead it calls other gssapi functions
(e.g., those provided by MIT Kerberos), depending on the requested
mechanism, to do the work.


%package -n %{devname}
Summary:	Static library and header files for the libgssapi library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	gssglue-devel = %{version}-%{release}
Obsoletes:	%mklibname gssapi 2 -d

%description -n	%{devname}
libgssglue provides a gssapi interface, but does not implement any
gssapi mechanisms itself; instead it calls other gssapi functions
(e.g., those provided by MIT Kerberos), depending on the requested
mechanism, to do the work.

This package contains the static libgssglue library and its
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

%files -n %{devname}
%defattr(-,root,root)
%defattr(-,root,root)
%multiarch %{multiarch_includedir}/gssglue/gssapi/gssapi.h
%{_includedir}/gssglue/gssapi/gssapi.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/libgssglue.pc

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README


%changelog
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.1
- rebuild against new krb5

* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.1
- libgssglue 0.1 replace libgssapi 0.10

* Thu Dec 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.10
- first Annvix build (for nfsv4 support)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
