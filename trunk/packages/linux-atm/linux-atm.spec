%define name	linux-atm
%define version	2.4.1
%define release	5sls

%define major		1
%define libname		lib%{name}
%define fulllibname	%mklibname %{name} %{major}

Summary:	Tools and libraries for ATM
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://linux-atm.sourceforge.net
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	flex

%description
Tools and libraries to support ATM (Asynchronous Transfer Mode)
networking and some types of DSL modems.

%package -n %{fulllibname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{fulllibname}
This package contains libraries needed to run programs linked with %{name}.

%package -n %{fulllibname}-devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{fulllibname} = %{version}-%{release}
Provides:	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{fulllibname}-devel
This package contains development files needed to compile programs which
use %{name}.

%prep
%setup -q

%build
%configure --enable-shared
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %{fulllibname} -p /sbin/ldconfig

%postun -n %{fulllibname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog NEWS THANKS BUGS
%doc COPYING COPYING.GPL COPYING.LGPL
%config(noreplace) %{_sysconfdir}/atmsigd.conf
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man4/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files -n %{fulllibname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{fulllibname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la

%changelog
* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 2.4.1-5sls
- minor spec cleanups

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 2.4.1-4sls
- OpenSLS build
- tidy spec

* Fri Aug 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.4.1-3mdk
- rebuild

* Tue Jul 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.4.1-2mdk
- rebuild for new rpm devel computation

* Fri Jun 13 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.4.1-1mdk
- 2.4.1

* Sun Apr 30 2003 Stefan van der Eijk <stefan@eijk.nu> 2.4.0-3mdk
- BuildRequires

* Sat Jan 04 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.4.0-2mdk
- rebuild

* Wed Aug 21 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.4.0-1mdk 
- first mdk release
