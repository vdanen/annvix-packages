#
# spec file for package linux-atm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		linux-atm
%define version		2.4.1
%define release		%_revrel

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
Patch0:		linux-atm-2.4.1-gcc3.4-fix.patch
Patch1:		linux-atm-2.4.1-libtool-fixes.patch
Patch2:		linux-atm-2.4.1-64bit-fixes.patch
Patch3:		linux-atm-2.4.1-gcc4.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	flex, bison, automake1.4

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
%patch0 -p1 -b .gcc3.4
%patch1 -p1 -b .libtool-fixes
%patch2 -p1 -b .64bit-fixes
%patch3 -p1 -b .gcc4

# stick to builtin libtool 1.4
%define __libtoolize /bin/true
autoconf
automake-1.4 --foreign


%build
%configure2_5x --enable-shared
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
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-9avx
- P3: gcc4 fixes mostly from fedora (gbeauchesne)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-8avx
- bootstrap build (new gcc, new glibc)
- patches from mdk for gcc, libtool, and 64bit fixes
- BuildRequires: bison

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-7avx
- rebuild

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-6avx
- Annvix build

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
