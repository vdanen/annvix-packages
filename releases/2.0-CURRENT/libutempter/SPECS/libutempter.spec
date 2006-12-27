#
# spec file for package libutempter
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libutempter
%define version		1.1.4
%define release		%_revrel
%define sname		utempter

%define major		0
%define libname		%mklibname %{sname} %{major}


Summary:	Priviledged helper for utmp/wtmp updates
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://www.altlinux.org
Source:		ftp://ftp.altlinux.org/pub/people/ldv/utempter/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.altlinux.org/pub/people/ldv/utempter/%{name}-%{version}.tar.bz2.asc

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	%{libname} = %{version}

%description
Utempter is a utility which allows some non-privileged programs to
have required root access without compromising system
security. Utempter accomplishes this feat by acting as a buffer
between root and the programs.


%package -n %{libname}
Summary:	Library used by %{name}
Group:		System/Libraries
Provides:	utempter = %{version}-%{release}
Obsoletes:	utempter
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(postun): rpm-helper

%description -n %{libname}
Libutempter is an library which allows some non-privileged
programs to have required root access without compromising system
security. It accomplishes this feat by acting as a buffer
between root and the programs.


%package -n %{libname}-devel
Summary:	Devel files for %{name}
Group:		Development/C
Provides:	%{name}-devel
Provides:	%{sname}-devel
Requires:	%{libname} = %{version}

%description -n %{libname}-devel
Header files for writing apps using libutempter


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
make CC=gcc libexecdir="%{_libexecdir}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre -n %{libname}
%_pre_groupadd utempter 26

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%attr(710,root,utempter) %dir %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter
%{_libdir}/libutempter.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libutempter.so
%{_libdir}/libutempter.a
%{_includedir}/utempter.h

%files doc
%defattr(-,root,root)
%doc COPYING README


%changelog
* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1.4
- 1.1.4
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1.1
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1.1
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.1-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.1-4avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.1-3avx
- bootstrap build

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.1.1-2avx
- require packages not files
- Annvix build

* Mon May 10 2004 Vincent Danen <vdanen@opensls.org> 1.1.1-1sls
- change to libutempter 1.1.1 from altlinux for better security than RH's
  utempter
- group utempter has static gid 26

* Fri Apr 16 2004 Vincent Danen <vdanen@opensls.org> 0.5.2-16sls
- security fix for problem found by Steve Grubb

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 0.5.2-15sls
- minor spec cleanups
- docs only in main package

* Fri Feb 06 2004 Vincent Danen <vdanen@opensls.org> 0.5.2-14sls
- don't call groupadd to add group utmp as that's in setup already

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 0.5.2-13sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
