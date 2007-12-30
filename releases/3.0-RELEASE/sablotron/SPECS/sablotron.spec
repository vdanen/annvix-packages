#
# spec file for package sablotron
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		sablotron
%define version 	1.0.2
%define release 	%_revrel

%define	altname		Sablot
%define major		0
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary: 	XSLT, XPath and DOM processor
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	MPL/GPL
Group: 		Development/Other
URL:		http://www.gingerall.cz
Source0:	http://download-1.gingerall.cz/download/sablot/%{altname}-%{version}.tar.bz2
Patch0:		Sablot-1.0.2-libs.diff
Patch1:		sablot-lib-1.0.1-gcc3.4.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  expat-devel >= 1.95.2
BuildRequires:	perl-XML-Parser
BuildRequires:	ncurses-devel
BuildRequires:	libstdc++-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.9 >= 1.9.2
BuildRequires:	js-devel >= 1.5
BuildRequires:	multiarch-utils >= 1.0.3

Requires:	expat >= 1.95.2
Requires:	%{libname}

%description
Sablotron is a fast, compact and portable XML toolkit
implementing XSLT, DOM and XPath.

The goal of this project is to create a lightweight,
reliable and fast XML library processor conforming to the W3C
specification, which is available for public and can be used as a base
for multi-platform XML applications.


%package -n %{libname}
Summary:	Main library for sablotron
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
Contains the library for sablotron.


%package -n %{devname}
Summary: 	The development libraries and header files for Sablotron
Requires: 	sablotron = %{version}
Group: 		System/Libraries
Requires: 	%{libname} = %{version}
Provides: 	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d

%description -n %{devname}
These are the development libraries and header files for Sablotron


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{altname}-%{version}
%patch0 -p1
%patch1 -p1


%build
export CPLUS_INCLUDE_PATH=%{_includedir}/js
export CXXFLAGS="%{optflags}"
%configure2_5x \
    --enable-javascript

%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/sablot-config

# nuke installed docs
rm -rf %{buildroot}%{_datadir}/doc
# fix permissions
chmod 0644 %{buildroot}%{_mandir}/man1/*

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(755,root,root)
%{_bindir}/sabcmd
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libsablot.so.*

%files -n %{devname}
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/sablot-config
%{_bindir}/sablot-config
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_includedir}/*.h

%files doc
%defattr(-,root,root)
%doc README RELEASE


%changelog
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- get rid of %%odevname

* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- rebuild against new ncurses

* Thu Jun 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- implement devel naming policy
- implement library provides policy
- rebuild against new expat

* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- rebuild against new ncurses
- clean spec

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2-1avx
- 1.0.2
- no need to run ldconfig on the main package
- add a bunch of BuildRequires
- multiarch support
- disable readline support

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.98-7avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.98-6avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.98-5avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.98-4sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 0.98-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
