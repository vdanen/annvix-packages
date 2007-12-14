#
# spec file for package acl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		acl
%define version 	2.2.44
%define release 	%_revrel

%define major		1
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	Command for manipulating access control lists
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-1.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	attr-devel
BuildRequires:	libtool

Requires:	%{libname} = %{version}

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.


%package -n %{libname}
Summary:	Main library for %{libname_orig}
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the libacl dynamic library which contains the POSIX
1003.1e draft standard 17 functions for manipulating access control lists.


%package -n %{devname}
Summary:	Access control list static libraries and headers
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 -d

%description -n %{devname}
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.


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
    --libdir=/%{_lib} \
    --sbindir=/bin
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/
make install-lib DIST_ROOT=%{buildroot}/

perl -pi -e 's,\s(/%{_lib})(.*attr\.la),%{_libdir}/$2,g' %{buildroot}/%{_libdir}/%{_lib}acl.la

rm -rf %{buildroot}%{_docdir}/acl

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/*.so.*

%files -n %{devname}
%defattr(-,root,root)
/%{_lib}/*.so
/%{_lib}/*a
%{_libdir}/*.so
%{_libdir}/*a
%{_mandir}/man[235]/*
%dir %{_includedir}/acl
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h

%files doc
%defattr(-,root,root)
%doc doc/extensions.txt doc/COPYING doc/libacl.txt doc/CHANGES.gz README


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.44
- rebuild against new attr

* Mon Jun 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.44
- rebuild with SSP

* Mon Jun 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.44
- 2.2.44
- implement devel naming policy
- implement library provides policy
- fix changelog

* Sat Sep 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.39
- minor spec cleanups

* Mon Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.39
- 2.4.39
- spec cleanups
- remove locale files

* Tue Jul 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.31
- spec cleanups
- remove pre-Annvix changelog

* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.31
- add -doc subpackage
- rebuild with gcc4
- BuildRequires: libtool
- fix rpmlint requires-on-release

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.31
- Clean rebuild

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.31
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.31-1avx
- 2.2.31

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.23-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.23-3avx
- rebuild

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.23-2avx
- if we list the libattr libtool file in our libtool file, at least
  ensure the location is right (bgmilne)

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.2.23-1avx
- 2.2.23
- Annvix build

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 2.2.22-1sls
- 2.2.22
- libname fixes

* Mon Feb 09 2004 Vincent Danen <vdanen@opensls.org> 2.2.13-4sls
- more spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.2.13-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
