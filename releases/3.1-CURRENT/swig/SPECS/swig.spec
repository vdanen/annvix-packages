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
%define version		1.3.31
%define release		%_revrel

%define _provides_exceptions	perl(Test::More)\\perl(Test::Builder)

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
BuildRequires:	python-devel
BuildRequires:	perl-devel
BuildRequires:	php
BuildRequires:	php-devel
BuildRequires:	libstdc++-devel
BuildRequires:  automake1.7
BuildRequires:	autoconf2.5

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
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.3.31
- remove some unwanted perl provides

* Fri May 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.3.31
- rebuild against new python

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.31
- 1.3.31

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
