#
# spec file for package m4
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		m4
%define version 	1.4.10
%define release 	%_revrel

Summary:	The GNU macro processor
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.seindal.dk/rene/gnu/
Source0:	ftp://ftp.gnu.org/pub/gnu/m4/m4-%{version}.tar.bz2
Source1:	ftp://ftp.gnu.org/pub/gnu/m4/m4-%{version}.tar.bz2.sig

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires(post):	info-install
Requires(preun): info-install

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.


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
%makeinstall_std infodir=%{_datadir}/info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info


%preun
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%{_bindir}/m4
%{_infodir}/*
%{_mandir}/man1/*

%files doc
%defattr(-,root,root)
%doc NEWS README COPYING BACKLOG THANKS


%changelog
* Sun Nov 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.4.10
- 1.4.10
- don't package ChangeLog, we already have NEWS

* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.8
- 1.4.8

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3 
- add -doc subpackage
- rebuild with gcc4
- put make check in %%check

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3-1avx
- 1.4.3
- dropped P0; not required

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4ppre2-9avx
- bootstrap build (new gcc, new glibc)
- s/mandrake/annvix/

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4ppre2-8avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4ppre2-7avx
- require packages not files
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.4ppre2-6sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 1.4ppre2-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
