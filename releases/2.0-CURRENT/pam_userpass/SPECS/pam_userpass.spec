#
# spec file for package pam_userpass
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		pam_userpass
%define version 	1.0
%define release 	%_revrel

Summary:	PAM module for USER/PASS-style protocols
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	relaxed BSD and (L)GPL-compatible
Group:		System/Libraries
URL: 		http://www.openwall.com/pam
Source0:	ftp://ftp.openwall.com/pub/projects/pam/modules/%{name}/%{name}-%{version}.tar.gz

BuildRoot: 	%{_buildroot}/%{name}-%{version}

%description
pam_userpass is a PAM authentication module for use specifically by
services implementing non-interactive protocols and wishing to verify
a username/password pair.  This module doesn't do any actual
authentication, -- other modules, such as pam_tcb, should be stacked
after it to provide the authentication.


%package devel
Summary:	Libraries and header files for developing pam_userpass-aware applications.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}, pam-devel

%description devel
This package contains development libraries and header files required
for building pam_userpass-aware applications.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
CFLAGS="-Wall -fPIC %{optflags}" %make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%make install DESTDIR="%{buildroot}"


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
/%{_lib}/security/*so*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/security/*

%files doc
%defattr(-,root,root)
%doc LICENSE README


%changelog
* Sat Jul 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- first Annvix package (for tcb support)
