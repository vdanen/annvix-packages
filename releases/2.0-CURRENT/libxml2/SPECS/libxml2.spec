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
%define version		2.6.21
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
Source0:	ftp://xmlsoft.org/%{name}-%{version}.tar.bz2
# (fc) 2.4.23-3mdk remove references to -L/usr/lib
Patch1:		libxml2-2.4.23-libdir.patch
Patch2:		libxml2-2.6.21-cvsfixes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	python-devel >= %{pyver}, readline-devel, zlib-devel, autoconf2.5, automake1.9

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
Summary: Utilities to manipulate XML files
Group: System/Libraries
Requires: %{libname} >= %{version}

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


%prep
%setup -q
%patch1 -p1 -b .libdir
%patch2 -p1 -b .cvsfixes

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


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/xml2-config

# remove unpackaged files
rm -rf	%{buildroot}%{_prefix}/doc \
    %{buildroot}%{_datadir}/doc \
    %{buildroot}%{_libdir}/python%{pyver}/site-packages/*.{la,a}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-, root, root)
%doc AUTHORS NEWS README Copyright TODO 
%doc doc/*.html doc/*.gif
%{_libdir}/lib*.so.*

%files utils
%defattr(-, root, root)
%{_bindir}/xmlcatalog
%{_bindir}/xmllint
%{_mandir}/man1/xmlcatalog*
%{_mandir}/man1/xmllint*

%files -n %{libname}-python
%defattr(-, root, root)
%doc python/TODO
%doc python/libxml2class.txt
%doc python/tests/*.py
%{_libdir}/python%{pyver}/site-packages/*.so
%{_libdir}/python%{pyver}/site-packages/*.py

%files -n %{libname}-devel
%defattr(-, root, root)
%doc doc/html/* 
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


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Tue Sep 09 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.5.11-1mdk
- Release 2.5.11

* Tue Aug 26 2003 Götz Waschk <waschk@linux-mandrake.com> 2.5.10-2mdk
- buildrequires autoconf2.5

* Tue Aug 19 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.5.10-1mdk
- Release 2.5.10

* Mon Aug 11 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.5.9-1mdk
- Release 2.5.9

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5.8-3mdk
- Provides: python-libxml2 for interested parties (e.g. libxslt)

* Fri Aug  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5.8-2mdk
- mklibname, enable threads, nuke more unpackaged files

* Wed Jul  9 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.5.8-1mdk
- Release 2.5.8

* Thu May 22 2003 Stefan van der Eijk <stefan@eijk.nu> - 2.5.7-2mdk
- rebuild for new deps

* Fri Apr 25 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.5.7-1mdk
- Release 2.5.7
- disable thread support until our glibc is fixed

* Thu Apr  3 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.5.6-1mdk
- Release 2.5.6

* Wed Feb 26 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.5.4-1mdk
- Release 2.5.4 (many bug fixes)

* Thu Feb  6 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.5.2-1mdk
- Release 2.5.2

* Thu Jan  9 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.5.1-1mdk
- Release 2.5.1

* Tue Jan  7 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.5.0-1mdk
- Release 2.5.0

* Thu Dec 12 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.30-1mdk
- Release 2.4.30
- Remove patch2 (merged upstream)

* Thu Nov 28 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 2.4.28-2mdk
- Add patch2 : fix compile kde doc

* Wed Nov 27 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.28-1mdk
- Release 2.4.28

* Thu Nov 14 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.26-1mdk
- Release 2.4.26
- Remove patch2 (merged upstream)

* Thu Oct 10 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.25-2mdk
- Patch2 (CVS): fix crash on validation seen on scrollkeeper
- Fix build for cooker

* Tue Oct  8 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.25-1mdk
- Release 2.4.25
- Remove patch0 (merged upstream)
- Parallel compilation is back

* Mon Jul 29 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.23-4mdk
- Fix build: s/8.3/9.0/ for mandrake release number

* Mon Jul 22 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.23-3mdk
- Patch1: no longer add -L/usr/lib to LDFLAGS

* Tue Jul 16 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.23-2mdk
- Fix Patch0 (python-libdir) to really install modules in the right directory

* Mon Jul  8 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.23-1mdk
- Release 2.4.23
- Fix rpmlint errors

* Mon Jul  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.22-2mdk
- Make check in %%build stage
- Patch0: correctly guess PYTHON_SITE_PACKAGES

* Mon Jun  3 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.22-1mdk
- Release 2.4.22

* Tue Apr 30 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.21-1mdk
- Release 2.4.21

* Wed Apr 17 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.20-2mdk
- Add BuildRequires on gtk-doc (DUCLOS Andre)

* Tue Apr 16 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.20-1mdk
- Release 2.4.20
- Remove patch0 (merged upstream)

* Sat Mar 30 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.19-3mdk
- Fix include in m4 file (Thanks to Michael Reinsch)

* Wed Mar 27 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 2.4.19-2mdk
- Fix compile on 8.0

* Tue Mar 26 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.19-1mdk
- Release 2.4.19

* Mon Mar 25 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 2.4.18-2mdk
- Fix compile on 8.1

* Wed Mar 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.18-1mdk
- Release 2.4.18

* Tue Mar  5 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.16-2mdk
- s/_py_ver/py_ver/ in BuildRequires, to fix build
- Use %%configure2_5x when not building for 7.2 or 8.0

* Wed Feb 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.16-1mdk
- Release 2.4.16

* Tue Feb 12 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.15-1mdk
- Release 2.4.15
- Disable parallel compilation, it is broken

* Mon Feb 11 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.14-1mdk
- Release 2.4.14
- Add python subpackage

* Tue Feb  5 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.13-3mdk
- Add explicit requires on main package in -utils (Thanks to Camille)

* Wed Jan 23 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.13-2mdk
- Create -utils package to get xmlcatalog and xmlint without -devel package

* Fri Jan 18 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.13-1mdk
- Release 2.4.13

* Tue Dec 11 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.12-1mdk
- Release 2.4.12
- Fix url

* Mon Nov 26 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.4.11-1mdk
- Release 2.4.11
- Move manpage to devel package

* Thu Nov 15 2001 David BAUDENS <baudens@mandrakesoft.com> 2.4.10-3mdk
- Fix build on 7.2 and 8.0

* Thu Nov 15 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.4.10-2mdk
- re-added small libtool script to fix building on mdk ppc 8.0

* Mon Nov 12 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.4.10-1mdk
- release 2.4.10

* Fri Nov  9 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.4.9-2mdk
- removed "provides libxml-devel" which was wrongly added

* Tue Nov  6 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.4.9-1mdk
- release 2.4.9

* Tue Nov  6 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.4.8-1mdk
- release 2.4.8

* Tue Oct 30 2001 Philippe Libat <philippe@mandrakesoft.com> 2.4.7-1mdk
- release 2.4.7

* Tue Oct 16 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.5-2mdk
- provides libxml-devel
- man-pages describe utilities thus belong to main package not devel one
- minor rpmlint fix

* Tue Oct  9 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.4.5-1mdk
- release 2.4.5

* Fri Aug 24 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.4.3-1mdk
- release 2.4.3, in sync with libxslt 1.0.3

* Tue Jul 24 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.4.1-1mdk
- new version

* Wed Jul 11 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.4.0-1mdk
- new stable version needed by libxslt 1.0

* Sun Jul 08 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3.14-1mdk
- Bump out newest and shiniest source.

* Fri Jun 29 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.3.13-1mdk
- new version

* Wed Jun 27 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.3.12-1mdk
- new version

* Tue Jun 12 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.3.10-1mdk
- new version

* Tue May 22 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.3.9-1mdk
- Release 2.3.9

* Thu May 03 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.3.8-1mdk
- new release

* Thu Apr 26 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.3.7-3mdk
- patch to processing-instruction() in xpath (from Daniel Veillard)

* Tue Apr 24 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.3.7-2mdk
- patch for processing instructions output in html context 
(from author Daniel Veillard)

* Tue Apr 24 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 2.3.7-1mdk
- Release 2.3.7

* Mon Apr 09 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3.6-1mdk
- Release 2.3.6.

* Wed Mar 14 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.3.4-1mdk
- Release 2.3.4

* Mon Feb 26 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3.2-1mdk
- 2.3.2 and integrate patch from Abel Cheung <doglist@linuxhall.org>:
  - Add readline-devel to the buildrequires.
  - Add more documentation.

* Sat Feb 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3.1-1mdk
- 2.3.1 hot from the oven.

* Thu Feb 15 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.3.0-2mdk
- Remove conflict with libxml-devel
- Add more doc

* Tue Feb 15 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3.0-1mdk
- Release 2.3.0.

* Thu Jan 11 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.2.11-1mdk
- Release 2.2.11
- Add missing files
- libxml2-devel now officially conflicts with libxml-devel

* Fri Dec 01 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.10-1mdk
- new and shiny source, no need for library  policy for this package.

* Tue Nov 14 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.8-1mdk
- bump up the version.

* Fri Nov 03 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.7-1mdk
- new and shiny version.

*  Sun Oct 29 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.6-1mdk
- shiny version.


* Sun Oct 15 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.4-1mdk
- very new and shiny version.

* Sat Aug 26 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.2.2-2mdk
- corrected bug reported by 
  Reinhard Katzmann <reinhard.katzmann@neckar-alb.de> :
  Requires : %{name} = {PACKAGE_VERSION}

* Tue Aug 22 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.2.2-1mdk
- updated to libxml version 2.2.2

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.8.9-3mdk
- automatically added BuildRequires

* Fri Jul 28 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.8.9-2mdk
- rebuild 

* Sat Jul 22 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 1.8.9-1mdk
- new version
- big move

* Thu Jul  6 2000 dam's <damien@mandrakesoft.com> 1.8.8-4mdk
- spec cleanup.

* Thu Jul 06 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 1.8.8-3mdk
- use some macros

* Tue Jul  4 2000 dam's <damien@mandrakesoft.com> 1.8.8-2mdk
- moved xml-config to devel package. Thanx to Stefan

* Tue Jul  4 2000 dam's <damien@mandrakesoft.com> 1.8.8-1mdk
- updated.
- spec cleanup.

* Tue Apr 18 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.8.7-1mdk
- fix release tag

* Sun Apr 16 2000 Daouda Lo <daouda@mandrakesoft.com> 1.8.7-1mdk
- release from helix stuffs.

* Wed Mar 22 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.8.6-2mdk
- fix group
 
* Sun Feb 20 2000 Axalon Bloodstone <axalon@mandrakesoft.com> 1.8.6-1mdk
- 1.8.6
  
* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- SMP build/check
- 1.7.3
   
* Fri Sep 24 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 1.7.1
    
* Thu Jul 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.4.
	  
* Wed Jun 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.2.0.    

* Tue May 11 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Mandrake adaptions
 
* Thu Mar 04 1999 Michael Fulbright <drmike@redhat.com>
- version 1.0.0
  
* Fri Feb 12 1999 Michael Fulbright <drmike@redhat.com>
- version 0.99.5 built against gnome-libs-0.99.8
   
* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- version 0.99.5
   
* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- made clean section work again
	 
* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- bumped to 0.99.0 for GNOME freeze
	  
* Sun Oct  4 1998 Daniel Veillard <Daniel.Veillard@w3.org>
- Added xml-config to the package
	   
* Thu Sep 24 1998 Michael Fulbright <msf@redhat.com>
- Built release 0.30                                   
