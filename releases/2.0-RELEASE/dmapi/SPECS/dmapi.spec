#
# spec file for package dmapi
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	revision	$Rev$
%define	name		dmapi
%define	version		2.2.5
%define	release		%_revrel

%define lib_name_orig	libdm
%define lib_major	0
%define lib_name	%mklibname dm %{lib_major}

Summary:	Data Management API runtime environment
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-1.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	xfs-devel
BuildRequires:	libext2fs-devel
BuildRequires:	libtool

%description
Files required by system software using the Data Management API
(DMAPI).  This is used to implement the interface defined in the
X/Open document:  Systems Management: Data Storage Managment
(XDSM) API dated February 1997.  This interface is implemented
by the libdm library.


%package -n %{lib_name}
Summary:	Main library for %{lib_name_orig}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with %{lib_name_orig}.


%package -n %{lib_name}-devel
Summary:	Data Management API static libraries and headers
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	dm-devel = %{version}-%{release}
Obsoletes:	dm-devel

%description -n	%{lib_name}-devel
dmapi-devel contains the libraries and header files needed to
develop programs which make use of the Data Management API
(DMAPI).  If you install dmapi-devel, you'll also want to install
the dmapi (runtime) package and the xfsprogs-devel package.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
aclocal && autoconf
%configure2_5x \
    --libdir=/%{_lib}
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/

# (sb) installed but unpackaged files
rm -rf %{buildroot}%{_datadir}/doc/dmapi


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig


%files -n %{lib_name}
%defattr(-,root,root)
/%{_lib}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
/%{_lib}/*.so
/%{_lib}/*a
%{_libdir}/*.so
%{_libdir}/*a
%{_mandir}/man3/*
%{_includedir}/*/*

%files doc
%defattr(-,root,root)
%doc doc/PORTING doc/CHANGES.gz doc/COPYING README


%changelog
* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5
- rebuild against new xfs-devel

* Mon Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5
- 2.2.5
- spec cleanups
- rebuild against new xfsprogs, and e2fsprogs
- buildrequires libtool

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.1
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.1
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.1-1avx
- 2.2.1

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.0-5avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.0-4avx
- rebuild for new gcc
- BuildRequires: libext2fs-devel

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.0-3avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.0-2avx
- Annvix build

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 2.1.0-1sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
