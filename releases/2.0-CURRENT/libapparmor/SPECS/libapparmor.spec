#
# spec file for package libapparmor
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libapparmor
%define version		2.0
%define release		%_revrel

%define major		1
%define libname		%mklibname apparmor %{major}

Summary:	Library to provide key AppArmor symbols
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	%{name}-%{version}-6288.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glibc-devel

%description
This package provides the libapparmor library, which contains the
change_hat(2) symbol, used for sub-process confinement by AppArmor.
Applications that wish to make use of change_hat(2) need to link
against this library.


%package -n %{libname}
Summary:        Library to provide key AppArmor symbols
Group:          System/Libraries
Provides:	libapparmor = %{version}-%{release}

%description -n %{libname}
This package provides the libapparmor library, which contains the
change_hat(2) symbol, used for sub-process confinement by AppArmor.
Applications that wish to make use of change_hat(2) need to link
against this library.


%package -n %{libname}-devel
Summary:        The libapparmor include files and link library
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:       libapparmor-devel = %{version}-%{release}

%description -n %{libname}-devel
The development header / link library for libapparmor.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
make CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} LIB=/%{_lib} VERSION=%{version} RELEASE=%{major} install


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/sys/*.h
%{_libdir}/*.so
%{_libdir}/*.a

%files doc
%defattr(-,root,root)
%doc COPYING.LGPL


%changelog
* Wed Aug 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- make lib(64)apparmor1 provide libapparmor too

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- first Annvix package
