%define buildfor $(awk '{print $4}' /etc/mandrake-release)
%{expand:%%define buildfor7_2 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 7.2 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor8_0 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 8.0 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor8_1 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 8.1 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor8_2 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 8.2 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor9_0 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 9.0 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor9_1 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 9.1 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor9_2 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 9.2 ]; then echo 1; else echo 0; fi)}

%define xml_version_required 2.5.6
%define major 1
%define libname %mklibname xslt %{major}

%if %buildfor7_2 || %buildfor8_0
%define py_ver      2.0
%endif

%if %buildfor8_1
%define py_ver      2.1
%endif

%if %buildfor8_2 || %buildfor9_0 || %buildfor9_1
%define py_ver      2.2
%endif

%if %buildfor9_2
%define py_ver      2.3
%endif

%if %buildfor9_2
%define pylibxml2   python-libxml2
%else
%define pylibxml2   libxml2-python
%endif

Summary: Library providing XSLT support
Name:    libxslt
Version: 1.0.33
Release: 1mdk
License: MIT
Group: System/Libraries
Source: ftp://xmlsoft.org/libxslt-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: libxml2 >= %{xml_version_required}
BuildRequires: libxml2-devel >= %{xml_version_required}
BuildRequires: python-devel >= %{py_ver}
BuildRequires: %{pylibxml2} >= %{xml_version_required}

URL: http://xmlsoft.org/XSLT/

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.

%package proc
Summary: XSLT processor using libxslt
Group: System/Libraries
Requires: %{libname} = %{version}

%description proc
This package provides an XSLT processor based on the libxslt C library. 
It allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 


%package -n %{libname}
Summary: Library providing XSLT support
Group: System/Libraries
Requires: libxml2 >= %{xml_version_required}

%description  -n %{libname}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 
A xslt processor based on this library, named xsltproc, is provided by 
the libxslt-proc package.

%package python
Summary: Python bindings for the libxslt library
Group: Development/Python
Requires: %{libname} = %{version}
Requires: python >= %{py_ver}
Requires: %{pylibxml2} >= %{xml_version_required}

%description python
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the libxml2-python
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.


%package -n %{libname}-devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} = %{version}
Requires: libxml2-devel >= %{xml_version_required}

%description -n %{libname}-devel
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 

%prep
%setup -q

%build
%if %buildfor7_2 || %buildfor8_0 || %buildfor8_1
%define __libtoolize /bin/true
%configure
%else
%configure2_5x
%endif

%make 

make check

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%if %buildfor7_2 || %buildfor8_0 || %buildfor8_1
make DESTDIR=$RPM_BUILD_ROOT install
%else
%makeinstall_std
%endif

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
  $RPM_BUILD_ROOT%{_libdir}/python%{py_ver}/site-packages/*.{la,a}

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig 

%postun -n %{libname} -p /sbin/ldconfig

%files proc
%defattr(-, root, root)
%{_bindir}/xsltproc
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README Copyright FEATURES
%doc doc/*.html
%{_libdir}/lib*.so.*

%files python
%defattr(-, root, root)
%doc AUTHORS ChangeLog README Copyright FEATURES
%{_libdir}/python%{py_ver}/site-packages/*.so
%{_libdir}/python%{py_ver}/site-packages/*.py
%doc python/libxsltclass.txt
%doc python/tests/*.py


%files -n %{libname}-devel
%defattr(-, root, root)
%doc doc/tutorial doc/html
%{_mandir}/man3/*
%{_libdir}/lib*.so
%{_libdir}/*a
%{_libdir}/*.sh
%{_includedir}/*
%{_bindir}/xslt-config
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*

%changelog
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

