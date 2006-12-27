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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
