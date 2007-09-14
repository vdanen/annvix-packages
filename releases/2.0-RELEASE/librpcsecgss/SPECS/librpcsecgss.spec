#
# spec file for package librpcsecgss
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		librpcsecgss
%define version		0.12
%define release		%_revrel

%define	major		2
%define libname		%mklibname rpcsecgss %{major}

Summary:	Allows secure rpc communication using the rpcsec_gss protocol
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		System/Libraries
URL:		http://www.citi.umich.edu/projects/nfsv4/linux/
Source0:	http://www.citi.umich.edu/projects/nfsv4/linux/%{name}/%{name}-%{version}.tar.bz2
Patch0:		librpcsecgss-0.14-CVE-2007-3999.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libgssapi-devel >= 0.9
BuildRequires:  automake1.7
BuildRequires:  autoconf2.5
BuildRequires:  pkgconfig
BuildRequires:  libtool

%description
Allows secure rpc communication using the rpcsec_gss protocol
librpcsecgss allows secure rpc communication using the rpcsec_gss
protocol.


%package -n %{libname}
Summary:	Allows secure rpc communication using the rpcsec_gss protocol
Group:		System/Libraries

%description -n	%{libname}
Allows secure rpc communication using the rpcsec_gss protocol
librpcsecgss allows secure rpc communication using the rpcsec_gss
protocol.


%package -n %{libname}-devel
Summary:	Static library and header files for the librpcsecgss library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	librpcsecgss-devel = %{version}
Provides:	rpcsecgss-devel = %{version}

%description -n	%{libname}-devel
Allows secure rpc communication using the rpcsec_gss protocol
librpcsecgss allows secure rpc communication using the rpcsec_gss
protocol.

This package contains the static librpcsecgss library and its
header files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .cve-2007-3999
# lib64 fix
perl -pi -e "s|/lib/|/%{_lib}/|g" configure*


%build
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

%files  -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/rpcsecgss
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/librpcsecgss.pc

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README


%changelog
* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.12
- P0: security fix for CVE-2007-3999

* Thu Dec 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.12
- first Annvix build (for nfsv4 support)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
