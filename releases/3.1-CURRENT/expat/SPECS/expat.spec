#
# spec file for package expat
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		expat
%define version 	2.0.1
%define release 	%_revrel

%define major		1
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	Expat is an XML parser written in C
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MPL or GPL
Group:		Development/Other
URL:		http://www.jclark.com/xml/expat.html
Source:		http://prdownloads.sourceforge.net/expat/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	%{libname} = %{version}-%{release}

%description
Expat is an XML 1.0 parser written in C by James Clark.  It aims to be
fully conforming. It is currently not a validating XML parser.


%package -n %{libname}
Summary:	Main library for expat
Group:		Development/C
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with expat.


%package -n %{devname}
Summary:	Development environment for the expat XML parser
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d

%description -n %{devname}
Development environment for the expat XML parser


%prep
%setup -q


%build
%configure
%make

 
%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall man1dir=%{buildroot}%{_mandir}/man1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/xmlwf
%{_mandir}/man*/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libexpat.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/libexpat.so
%{_includedir}/expat.h
%{_includedir}/expat_external.h
%{_libdir}/libexpat.a
%{_libdir}/libexpat.la


%changelog
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.1
- get rid of %%odevname

* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.1
- rebuild

* Sat Jun 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.1
- 2.0.1
- clean up provides/obsoletes
- implement devel naming policy
- implement library provides policy

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.95.8
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.95.8
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.95.8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.95.8-1avx
- 1.95.8
- drop unneeded patch

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.95.6-10avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.95.6-9avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.95.6-8avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> - 1.95.6-7avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> - 1.95.6-6sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> - 1.95.6-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
