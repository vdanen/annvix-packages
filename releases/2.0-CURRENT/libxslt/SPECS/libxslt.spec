#
# spec file for package libxslt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libxslt
%define version		1.1.16
%define release		%_revrel

%define xml_ver_req	2.6.17
%define major		1
%define libname		%mklibname xslt %{major}

%define pylibxml2   	python-libxml2

Summary:	Library providing XSLT support
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
URL:		http://xmlsoft.org/XSLT/
Source:		ftp://xmlsoft.org/libxslt-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libxml2-devel >= %{xml_ver_req}
BuildRequires:	python-devel >= %{pyver}
BuildRequires:	%{pylibxml2} >= %{xml_ver_req}
BuildRequires:	multiarch-utils >= 1.0.3

Requires:	libxml2 >= %{xml_ver_req}

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.


%package proc
Summary:	XSLT processor using libxslt
Group:		System/Libraries
Requires:	%{libname} = %{version}

%description proc
This package provides an XSLT processor based on the libxslt C library. 
It allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 


%package -n %{libname}
Summary:	Library providing XSLT support
Group:		System/Libraries
Requires:	libxml2 >= %{xml_ver_req}

%description  -n %{libname}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 
A xslt processor based on this library, named xsltproc, is provided by 
the libxslt-proc package.


%package python
Summary:	Python bindings for the libxslt library
Group:		Development/Python
Requires:	%{libname} = %{version}
Requires:	python >= %{pyver}
Requires:	%{pylibxml2} >= %{xml_ver_req}

%description python
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the libxml2-python
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.


%package -n %{libname}-devel
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	libxml2-devel >= %{xml_ver_req}

%description -n %{libname}-devel
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 

%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x

%make 


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall

rm -rf python-examples
mv %{buildroot}%{_docdir}/%{name}-python-%{version}/examples python-examples && rm -rf %{buildroot}%{_docdir}/%{name}-python-%{version}

# remove unpackaged files
rm -rf %{buildroot}%{_docdir}/%{name}-%{version} \
  %{buildroot}%{_libdir}/python%{pyver}/site-packages/*.{la,a}

%multiarch_binaries %{buildroot}%{_bindir}/xslt-config


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig 
%postun -n %{libname} -p /sbin/ldconfig


%files proc
%defattr(-,root,root)
%{_bindir}/xsltproc
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files python
%defattr(-,root,root)
%{_libdir}/python%{pyver}/site-packages/*.so
%{_libdir}/python%{pyver}/site-packages/*.py


%files -n %{libname}-devel
%defattr(-,root,root)
%{_mandir}/man3/*
%{_libdir}/lib*.so
%{_libdir}/*a
%{_libdir}/*.sh
%{_includedir}/*
%multiarch %{multiarch_bindir}/xslt-config
%{_bindir}/xslt-config
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*

%files doc
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README Copyright FEATURES
%doc doc/*.html
%doc doc/tutorial doc/html
%doc python/libxsltclass.txt
%doc python/tests/*.py python-examples


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1.16
- move the python pkg docs too
- put make check in %%check

* Tue May 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1.16
- add -doc subpackage
- rebuild against new libxml2
- rebuild against new python
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1.15
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1.15
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.15-1avx
- 1.1.15
- requires libxml2 2.6.17
- multiarch

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.12-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.12-2avx
- bootstrap build

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.12-1avx
- 1.1.12
- use %%pyver macro

* Wed Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.33-4avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.0.33-3sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 1.0.33-2sls
- OpenSLS build
- tidy spec
- remove support for older mdk versions

* Fri Sep 12 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.33-1mdk
- Release 1.0.33

* Mon Aug 11 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0.32-1mdk
- Release 1.0.32

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.31-2mdk
- mklibname

* Thu Jul 10 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0.31-1mdk
- Release 1.0.31

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.30-3mdk
- Rebuild

* Tue May 13 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.30-2mdk
- Fix libxml2 dep (bug #3886)

* Wed May 07 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0.30-1mdk
- Release 1.0.30

* Fri Apr 11 2003 Frederic Crozat <fcrozat@mandrakesoft.com 1.0.29-1mdk
- Release 1.0.29

* Fri Feb 28 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0.27-1mdk
- Release 1.0.27 (many bug fixes)

* Thu Feb  6 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.25-1mdk
- Release 1.0.25

* Thu Jan 16 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.24-1mdk
- Release 1.0.24

* Wed Nov 27 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.23-1mdk
- Release 1.0.23

* Thu Nov 14 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.22-1mdk
- Release 1.0.22
- Fix build for Cooker/9.1

* Tue Oct  8 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.21-1mdk
- Release 1.0.21
- Remove patches 0 & 1 (merged upstream)
- Parallel compilation is back

* Mon Aug 19 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.19-4mdk
- Patch1 (CVS): fix problem for Docbook users

* Wed Jul 31 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 1.0.19-3mdk
- Build for mandrake-release 9.0, not 8.3

* Tue Jul 16 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.19-2mdk
- Patch0: Correctly guess PYTHON_SITE_PACKAGES

* Mon Jul  8 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.19-1mdk
- Release 1.0.19
- Fixes rpmlint errors
- Remove patch0 (merged upstream)

* Mon Jun  3 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.18-1mdk
- Release 1.0.18

* Tue Apr 30 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.17-2mdk
- Fix provides

* Tue Apr 30 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.17-1mdk
- Release 1.0.17

* Tue Apr 16 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.16-1mdk
- Release 1.0.16

* Wed Mar 27 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.15-3mdk
- Fix compile on 8.0

* Tue Mar 26 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.0.15-2mdk
- added missing tutorial

* Tue Mar 26 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.15-1mdk
- Release 1.0.15

* Mon Mar 25 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.14-2mdk
- Fix compile on 8.1

* Wed Mar 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.14-1mdk
- Release 1.0.14

* Tue Feb 12 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.12-1mdk
- Release 1.0.12
- Parallel compilation is broken

* Mon Feb 11 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.11-1mdk
- Release 1.0.11
- Add python subpackage

* Fri Jan 18 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.10-1mdk
- Release 1.0.10

* Tue Dec 11 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.9-1mdk
- Release 1.0.9

* Mon Nov 26 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.8-1mdk
- Release 1.0.8

* Thu Nov 15 2001 David BAUDENS <baudens@mandrakesoft.com> 1.0.7-2mdk
- Fix build on 7.2 and 8.0

* Mon Nov 12 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.0.7-1mdk
- release 1.0.7

* Tue Nov  6 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.0.6-2mdk
- patch to define LIBXSLT_PUBLIC to nil

* Tue Oct 30 2001 Philippe Libat <philippe@mandrakesoft.com> 1.0.6-1mdk
- release 1.0.6

* Tue Oct  9 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.0.4-1mdk
- release 1.0.4

* Fri Aug 24 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.0.3-1mdk
- release 1.0.3 in sync with libxml2 2.4.3

* Tue Aug 21 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.0.2-1mdk
- new version

* Tue Jul 24 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.0.1-2mdk
- updated requires on libxml2

* Tue Jul 24 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.0.1-1mdk
- new version

* Wed Jul 11 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.0.0-1mdk
- first stable version; many thanks to Daniel Veillard for this really 
wonderful lib (as well as libxml2).

* Tue Jul 10 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.14.0-1mdk
- new version

* Thu Jun 28 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.13.0-1mdk
- new version

* Tue Jun 12 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.11.0-1mdk
- new version

* Fri May  4 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.9.0-1mdk
- new version, patch not needed anymore

* Wed Apr 25 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.8.0-2mdk
- patch for multiple parameters in xsltproc

* Tue Apr 24 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.8.0-1mdk
- new version

* Thu Apr 19 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.7.0-1mdk
- first Mandrake release
- libification
- macroszification
- satisfaction ;-)

* Mon Jan 22 2001 Daniel.Veillard <Daniel.Veillard@imag.fr>

- created based on libxml2 spec file

