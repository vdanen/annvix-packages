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
%define version 	1.95.8
%define release 	%_revrel

%define libname_orig	libexpat
%define major		0
%define libname		%mklibname %{name} %{major}

Summary:	Expat is an XML parser written in C
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MPL or GPL
Group:		Development/Other
URL:		http://www.jclark.com/xml/expat.html
Source:		http://prdownloads.sourceforge.net/expat/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	%{libname} = %{version}-%{release}

%description
Expat is an XML 1.0 parser written in C by James Clark.  It aims to be
fully conforming. It is currently not a validating XML parser.


%package -n %{libname}
Summary:	Main library for expat
Group:		Development/C
Obsoletes:	libexpat1_95
Provides:	libexpat1_95 = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with expat.


%package -n %{libname}-devel
Summary:	Development environment for the expat XML parser
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:       %{libname_orig}-devel = %{version}-%{release} %{name}-devel = %{version}-%{release}
Obsoletes:      %{name}-devel
Obsoletes:      libexpat1_95-devel
Provides:       libexpat1_95-devel = %{version}-%{release}

%description -n %{libname}-devel
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

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libexpat.so
%{_includedir}/expat.h
%{_includedir}/expat_external.h
%{_libdir}/libexpat.a
%{_libdir}/libexpat.la


%changelog
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

* Wed Jul  9 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.95.6-4mdk
- Rebuild for new deps

* Mon Jun  2 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 1.95.6-3mdk
- patch to fix XML_Status enum in expat.h (fix Sablotron build)

* Wed May 14 2003 Stefan van der Eijk <stefan@eijk.nu> 1.95.6-2mdk
- rebuild

* Sat Apr 26 2003 Stefan van der Eijk <stefan@eijk.nu> 1.95.6-1mdk
- 1.95.6

* Thu Dec  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.95.5-1mdk
- 1.95.5
- use %%mklibname

* Wed Jun 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.95.2-4mdk
- libtoolize to get updated config.guess, rebuild with gcc3.1

* Wed May  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.95.2-3mdk
- corrected libification
- link xmlwf dynamically

  * Wed May 1 2002 Vaclav Slavik <vaclav.slavik@matfyz.cz> 1.95.2-3mdk
- correctly install documentation
- move .la file to libexpat-devel

* Thu Feb 14 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.95.2-2mdk
- parallel make is broken

* Mon Jul 30 2001 Daouda LO <daouda@mandrakesoft.com> 1.95.2-1mdk
- release 1.95.2
- libification.

* Sat Jun 23 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.95.1-4mdk
- remove trailing "/" from install path, to fix build

* Thu Feb 15 2001  Daouda Lo <daouda@mandrakesoft.com> 1.95.1-3mdk
- real version is 1.95.1 
- reenable optimisations 

* Thu Feb 15 2001  Daouda Lo <daouda@mandrakesoft.com> 1.95-1mdk
- release .

* Sun Jan 07 2001 David BAUDENS <baudens@mandrakesoft.com> 1.1-2mdk
- Don't try to use optimizations
- Bzip2 sources

* Mon Nov 20 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.1-1mdk
- first version

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
