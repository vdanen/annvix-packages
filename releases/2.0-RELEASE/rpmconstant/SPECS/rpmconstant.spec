#
# spec file for package rpmconstant
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rpmconstant
%define version		0.1.2
%define release 	%_revrel

%define major		0
%define libname		%mklibname %{name} %{major}

Summary:	A library to bind rpm constant
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL 
Group:		Development/C
URL:		http://rpm.zarb.org/
Source0:	http://rpm.zarb.org/download/%{name}-%{version}.tar.bz2
Patch0:		rpmconstant-0.1.2-avx-for_rpm_4.4.5.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	rpm-devel

%description
This library provides basics functions to map internal rpm constant value
with their name. This is useful for perl/python or other language which has
binding over rpmlib.


%package -n %{libname}
Summary:	A library to bind rpm constant
Group:		Development/C
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This library provides basics functions to map internal rpm constant value
with their name. This is useful for perl/python or other language which has
binding over rpmlib.


%package -n %{libname}-devel
Summary:	Development files from librpmconstant
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{libname}-devel
This library provides basics functions to map internal rpm constant value
with their name. This is useful for perl/python or other language which has
binding over rpmlib.

You need this package to build applications using librpmconstant.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0 -b .avx


%build
%configure
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib%{name}.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/%{name}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.la

%files doc
%defattr(-,root,root)
%doc constant.c AUTHORS ChangeLog README


%changelog
* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.1.2
- 0.1.2
- P0: remove some definitions that are not present in rpm 4.4.5
- update URLs
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.0.5
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.0.5
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.0.5-2avx
- rebuild against new rpm

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.0.5-1avx
- 0.0.5

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.0.4-2avx
- bootstrap build

* Mon Mar 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.0.4-1avx
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
