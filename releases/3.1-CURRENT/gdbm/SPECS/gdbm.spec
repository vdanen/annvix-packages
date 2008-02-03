#
# spec file for package gdbm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gdbm
%define version 	1.8.3
%define release 	%_revrel

%define major		3
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	A GNU set of database routines which use extensible hashing
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.gnu.org/software/gdbm/
Source:		ftp://ftp.gnu.org/pub/gnu/gdbm/%{name}-%{version}.tar.bz2
Patch0:		gdbm-1.8.0-jbj.patch
# (deush) regenerate patch to apply with -p1
Patch1:		gdbm-1.8.3-asnonroot.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7

%description
Gdbm is a GNU database indexing library, including routines
which use extensible hashing.  Gdbm works in a similar way to standard UNIX
dbm routines.  Gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.


%package -n %{libname}
Summary:	Main library for gdbm
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	%{name}

%description -n %{libname}
This package provides library needed to run programs dynamically linked
with gdbm.


%package -n %{devname}
Summary:	Development libraries and header files for the gdbm library
Group:		Development/Databases
Requires:	%{libname} = %{version}
Requires(post):	info-install
Requires(preun): info-install
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Obsoletes:	%mklibname gdbm 3 -d
Conflicts:	%mklibname gdbm 2 -d

%description -n %{devname}
Gdbm-devel contains the development libraries and header files
for gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .jbj
%patch1 -p1

libtoolize -f
aclocal-1.7
FORCE_AUTOCONF_2_5=1 autoconf
autoheader


%build
%configure
%make all info


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall install-compat includedir=%{buildroot}%{_includedir}/gdbm man3dir=%{buildroot}%{_mandir}/man3
ln -sf gdbm/gdbm.h %{buildroot}%{_includedir}/gdbm.h

chmod 0644 COPYING INSTALL NEWS README


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post -n %{devname}
%_install_info gdbm.info

%preun -n %{devname}
%_remove_install_info gdbm.info


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libgdbm*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/libgdbm*.so
%{_libdir}/libgdbm*.la
%{_libdir}/libgdbm*.a
%dir %{_includedir}/gdbm
%{_includedir}/gdbm/*.h
%{_includedir}/gdbm.h
%{_infodir}/gdbm*
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc NEWS README


%changelog
* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3
- implement devel naming policy
- implement library provides policy

* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3
- add -doc subpackage
- rebuild with gcc4
- fix prereq

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3
- Obfuscate email addresses and new tagging
- Uncompress patches
- remove useless provides on %%{libname}-devel

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3-2avx
- bootstrap build

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3-1avx
- 1.8.3
- sync with cooker 1.8.3-2mdk:
  - force the use of autoconf2.5 and automake1.7 (peroyvind)
  - change major name (daouda)
  - added compat libs (daouda)
  - conflicts libgdbm2-devel (gb)
  - drop P2 and P3


* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.8.0-27avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.8.0-26sls
- minor spec cleanups

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 1.8.0-25sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
