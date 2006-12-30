#
# spec file for package libxml2
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libxml2
%define version		2.6.27
%define release		%_revrel

%define major		2
%define libname		%mklibname xml %{major}
%define py_ver		2.3

Summary:	Library providing XML and HTML support
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group: 		System/Libraries
URL:		http://www.xmlsoft.org/
Source0:	ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
# (fc) 2.4.23-3mdk remove references to -L/usr/lib
Patch1:		libxml2-2.4.23-libdir.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	python-devel >= %{pyver}
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.9

%description
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.


%if "%{libname}" != "%{name}"
%package -n %{libname}
Summary:	Shard libraries providing XML and HTML support
Group: 		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified.
%endif


%package utils
Summary:	Utilities to manipulate XML files
Group:		System/Libraries
Requires:	%{libname} >= %{version}

%description utils
This packages contains utils to manipulate XML files.


%package -n %{libname}-python
Summary:	Python bindings for the libxml2 library
Group:		Development/Python
Requires:	%{libname} >= %{version}
Requires:	python >= %{pyver}
Provides:	python-%{name} = %{version}-%{release}

%description -n %{libname}-python
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.


%package -n %{libname}-devel
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	zlib-devel
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.



%prep
%setup -q
%patch1 -p1 -b .libdir

# needed by patch 1
aclocal-1.9
automake-1.9
autoconf


%build
%configure2_5x

%make

# all tests must pass
# use TARBALLURL_2="" TARBALLURL="" TESTDIRS="" to disable xstc test which are using remote tarball
make TARBALLURL_2="" TARBALLURL="" TESTDIRS="" check

# doc handling
mkdir python-doc
cp -a python/{libxml2class.txt,TODO} python-doc/
cp -a python/tests/*.py python-doc/


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std
(cd doc/examples ; make clean ; rm -rf .deps)
gzip -9 doc/libxml2-api.xml

# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/xml2-config

# remove unpackaged files
rm -rf	%{buildroot}%{_prefix}/doc \
    %{buildroot}%{_datadir}/doc \
    %{buildroot}%{_datadir}/gtk-doc \
    %{buildroot}%{_libdir}/python%{pyver}/site-packages/*.{la,a}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/lib*.so.*

%files utils
%defattr(-, root, root)
%{_bindir}/xmlcatalog
%{_bindir}/xmllint
%{_mandir}/man1/xmlcatalog*
%{_mandir}/man1/xmllint*

%files -n %{libname}-python
%defattr(-, root, root)
%{_libdir}/python%{pyver}/site-packages/*.so
%{_libdir}/python%{pyver}/site-packages/*.py

%files -n %{libname}-devel
%defattr(-, root, root)
%multiarch %{multiarch_bindir}/xml2-config
%{_bindir}/xml2-config
%{_libdir}/*a
%{_libdir}/*.so
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*
%{_mandir}/man1/xml2-config*
%{_mandir}/man3/*
%{_includedir}/*
%{_datadir}/aclocal/*

%files doc
%defattr(-, root, root)
%doc AUTHORS NEWS README Copyright TODO 
%doc python-doc
%doc doc/*.py doc/python.html
%doc doc/*.html doc/*.gif doc/*.png doc/html doc/examples doc/tutorial
%doc doc/libxml2-api.xml.gz


%changelog
* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.27
- 2.6.27

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.24
- rebuild against new readline

* Tue May 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.24
- 2.6.24
- add -doc subpackage
- drop P1; merged upstream
- rebuild against new python
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.21
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.21
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.21-2avx
- P2: various fixes from cvs (fcrozat)

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.21-1avx
- 2.6.21
- rebuild against new readline and python

* Tue Aug 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.20-1avx
- 2.6.20
- remove the compiler profiling as it ends up complaining about
  hidden symbols in libgcov.a

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.17-2avx
- bootstrap build

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.17-1avx
- 2.6.17
- multiarch support
- use %%pyver macro
- integrated profiling stuff from Fedora

* Fri Nov  5 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.11-6avx
- P3: patch to fix CAN-2004-0989

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.11-5avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.5.11-4sls
- remove duplicate docs
- more complete fix for CAN-2004-0110

* Mon Mar 01 2004 Vincent Danen <vdanen@opensls.org> 2.5.11-3sls
- remove %%build_opensls macros
- P2: fix CAN-2004-0110
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 2.5.11-2sls
- OpenSLS build
- tidy spec
- drop support for mdk 8.1-9.1
- use %%build_opensls to exclude BuildReq on gtk-doc

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
