%define name	rpmconstant
%define version	0.0.4
%define release 1avx

%define major	0
%define libname	%mklibname %{name} %{major}

Summary:	A library to bind rpm constant
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL 
Group:		Development/C
URL:		http://cvs.mandrakesoft.com/cgi-bin/cvsweb.cgi/soft/perl-Hdlist/rpmconstant/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
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

%prep
%setup -q

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
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog README
%{_libdir}/lib%{name}.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc constant.c AUTHORS ChangeLog README
%{_includedir}/%{name}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.la

%changelog
* Mon Mar 28 2005 Vincent Danen <vdanen@annvix.org> 0.0.4-1avx
- first Annvix build

* Sun Mar 06 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.4-2mdk
- use %%mkrel

* Wed Feb 16 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.4-1mdk
- 0.0.4

* Fri Feb 11 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.3-1mdk
- 0.0.3

* Mon Feb 07 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.2-1mdk
- 0.0.2

* Sun Feb 06 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.1-1mdk
- First mdk spec
