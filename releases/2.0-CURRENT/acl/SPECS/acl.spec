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
%define version 	2.2.31
%define release 	%_revrel

%define libname_orig	lib%{name}
%define major		1
%define libname		%mklibname %{name} %{major}

Summary:	Command for manipulating access control lists
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-buildroot
BuildRequires:	attr-devel
BuildRequires:	libtool

Requires:	%{libname} = %{version}

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.


%package -n %{libname}
Summary:	Main library for %{libname_orig}
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n %{libname}
This package contains the l%{libname_orig} dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.


%package -n %{libname}-devel
Summary:	Access control list static libraries and headers
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	acl-devel = %{version}-%{release}
Obsoletes:	acl-devel

%description -n %{libname}-devel
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

%files -n %{libname}-devel
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
* Tue Jul 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.31
- spec cleanups

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

* Fri Aug 29 2003 Juan Quintela <quintela@mandrakesoft.com> 2.2.13-2mdk
- /usr/include/acl belongs to acl-devel.

* Fri Aug  8 2003 Juan Quintela <quintela@mandrakesoft.com> 2.2.13-1mdk
- 2.2.13

* Tue Aug  5 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.10-2mdk
- Enforce current practise to BuildRequires: libacl-devel

* Fri Jul 18 2003 Juan Quintela <quintela@mandrakesoft.com> 2.2.10-1mdk
- 2.2.10.

* Wed Jun 18 2003 Juan Quintela <quintela@trasno.org> 2.2.4-1mdk
- mklibname (different way).
- 2.2.4.

* Mon Jun 14 2003 Götz Waschk <waschk@linux-mandrake.com> 2.1.1-2mdk
- configure2_5x macro
- mklibname macro

* Thu Jun 13 2003 Vincent Danen <vdanen@mandrakesoft.com> 2.1.1-1mdk
- 2.1.1

* Fri May 23 2003 Götz Waschk <waschk@linux-mandrake.com> 2.0.11-2mdk
- clean out unpackaged files
- rebuild for devel provides

* Wed Jul 24 2002 Buchan Milne <bgmilne@linux-mandrake.com> 2.0.11-1mdk
- 2.0.11

* Wed Jul 10 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.9-1mdk
- 2.0.9

* Fri Mar 22 2002 David BAUDENS <baudens@mandrakesoft.com> 2.0.0-2mdk
- BuildRequires: libattr1, libattr1-devel
- Requires: %%{version}-%%{release} and not only %%{version} or %%{name}

* Thu Mar  7 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.0.0-1mdk
- 2.0.0

* Sat Sep 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.3-1mdk
- 1.1.3.

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.2-2mdk
- Fix provides.

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.2-1mdk
- Rework the .spec.
- Make libs in subpackage.
- 1.1.2.

* Wed May  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.1-1mdk
- First attempt.