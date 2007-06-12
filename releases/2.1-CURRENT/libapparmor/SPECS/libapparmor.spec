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
%define version		2.0.1
%define release		%_revrel

%define svnrel		305

%define major		1
%define libname		%mklibname apparmor %{major}
%define devname		%mklibname apparmor -d
%define odevname	%mklibname apparmor 1 -d

Summary:	Library to provide key AppArmor symbols
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	%{name}-%{version}-%{svnrel}.tar.gz

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
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package provides the libapparmor library, which contains the
change_hat(2) symbol, used for sub-process confinement by AppArmor.
Applications that wish to make use of change_hat(2) need to link
against this library.


%package -n %{devname}
Summary:        The libapparmor include files and link library
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:	%{odevname}

%description -n %{devname}
The development header / link library for libapparmor.


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

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/sys/*.h
%{_libdir}/*.so
%{_libdir}/*.a


%changelog
* Tue Jun 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.1
- 2.0.1-305 (March 07 snapshot)

* Fri Nov 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- r132 (October snapshot)
- drop the -doc package (only contained the COPYING.LGPL file)

* Wed Aug 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- make lib(64)apparmor1 provide libapparmor too

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
