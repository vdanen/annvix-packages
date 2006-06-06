#
# spec file for package swig
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		swig
%define version		1.3.27
%define release		%_revrel

Summary:	Simplified Wrapper and Interface Generator (SWIG)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		Development/Other
URL:		http://www.swig.org/
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch1:		swig-1.3.23-pylib.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	python-devel perl-devel php php-devel
BuildRequires:	libstdc++-devel
BuildRequires:  automake1.7 autoconf2.5

%description
SWIG takes an interface description file written in a combination of C/C++
and special directives and produces interfaces to Perl, Python, and Tcl.
It allows scripting languages to use C/C++ code with minimal effort.


%package devel
Summary:	Header files and libraries for developing apps which will use %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}

%description devel
SWIG takes an interface description file written in a combination of C/C++
and special directives and produces interfaces to Perl, Python, and Tcl.
It allows scripting languages to use C/C++ code with minimal effort.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1 -b .pylib


%build
./autogen.sh
%configure2_5x

%make
#%make runtime


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
%makeinstall_std \
    install-lib \
    install-main \
    M4_INSTALL_DIR=%{buildroot}%{_datadir}/aclocal

install -m 0644 ./Source/DOH/doh.h -D %{buildroot}%{_includedir}/doh.h


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,755)
%{_bindir}/*
%{_datadir}/swig

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files doc
%defattr(-,root,root)
%doc CHANGES* LICENSE README ANNOUNCE FUTURE NEW TODO Doc/Devel Examples Doc/Manual


%changelog
* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.27
- rebuild against new python

* Tue May 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.27
- drop down to 1.3.27; some python files are missing that subversion
  needs and are found in 1.3.27

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.29
- 1.3.29
- rebuild against perl 5.8.8
- create -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Oct 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25-1avx
- first Annvix build (for subversion)
- drop the doc package

* Wed Oct 05 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.3.25-1mdk
- 1.3.25
- Fix Group

* Mon Jul 18 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.3.24-2mdk
- Rebuild

* Fri Dec 24 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.3.24-1mdk
- 1.3.24
- do libtoolize again
- drop P0 (fixed upstream)
- libraries are no more
- pick up python libdir correctly (P1 from fedora)

* Mon Dec 20 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.3.21-6mdk
- Rebuild for new perl

* Mon Jun 07 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.3.21-5mdk 
- rebuilt with gcc v3.4.x
- use macros

* Thu Apr 15 2004 Michael Scherer <misc@mandrake.org> 1.3.21-4mdk 
- moved .so to -devel, to remove useless dependencies
- split docs from main package

* Thu Jan 15 2004 Ben Reser <ben@reser.org> 1.3.21-3mdk
- Patch to fix python support on amd64.

* Wed Jan 14 2004 Ben Reser <ben@reser.org> 1.3.21-2mdk
- devel package should require the same version-release of the main
  package.

* Wed Jan 14 2004 Ben Reser <ben@reser.org> 1.3.21-1mdk
- 1.3.21
- Remove the symlink that was causing it to ship the currently installed
  binary on the build host.  The 1.3.20 version actually had the 1.3.19
  binary in it.  And as such produced code that wouldn't build against
  the headers.
- Drop the symlink to the binary in the doc dir.
- Ship CHANGES.current, ANNOUNCE, FUTURE, NEW and TODO in the doc dir.

* Sat Jan 03 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.3.20-1mdk
- 1.3.20

* Wed Apr 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.3.19-1mdk
- 1.3.19
- drop Patch0 & Patch1 (merged upstream)
- don't manually install swig.h anymore(it automatically get's installed now)
- change path to doh.h to install from
- updated documentation (drop VERSION, no longer exists, include devel docs for
  devel package)
- fix library-without-ldconfig-post*

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.11-4mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Jul 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.11-3mdk
- Automated rebuild with gcc3.2

* Mon Feb 18 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.3.11-2mdk
- add patch #1 from Sam Liddicott <sam.liddicott@ananova.com> to fix php

* Sun Feb  3 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.3.11-1mdk
- new version
  - remove patch #0 to detect Ruby, no more needed
  - adds support for php which needs a patch for detection of location
  - no more needed to specify hard paths for python and tcl
- fix invalid-url
- fix invalid-license (BSD-like seemed the most appropriate)

* Fri Jun 22 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.3a5-1mdk
- new version so that we get Ruby support
- tcl and python will re-work
- include Examples

* Fri Nov 17 2000 David BAUDENS <baudens@mandrakesoft.com> 1.3a3-2mdk
- Rebuild with gcc-2.96 & glibc-2.2

* Wed Jul 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3a3-1mdk
- BM.
- Clean up specs.
- 1.3a3.

* Tue Jun 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1p5-5mdk
- Use makeinstall macros.

* Mon Apr 10 2000 Francis Galiegue <fg@mandrakesoft.com> 1.1p5-4mdk

- Provides: swig

* Mon Apr  3 2000 Pixel <pixel@mandrakesoft.com> 1.1p5-3mdk
- rebuild with new perl
- cleanup

* Wed Mar 22 2000 Francis Galiegue <fg@mandrakesoft.com> 1.1p5-2mdk

- Rebuilt on kenobi
- Don't use prefix

* Fri Mar 10 2000 Francis Galiegue <francis@mandrakesoft.com> 1.1p5-1mdk
- First RPM for Mandrake

