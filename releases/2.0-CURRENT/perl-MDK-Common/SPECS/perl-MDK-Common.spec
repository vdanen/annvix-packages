#
# spec file for package perl-MDK-Common
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		MDK-Common
%define revision	$Rev$
%define name		perl-%{module}
%define version 	1.2.2
%define release 	%_revrel

%ifarch x86_64
%define build_option	PERL_CHECKER_TARGET='debug-code BCSUFFIX=""'
%define require_ocaml	/usr/bin/ocamlrun
%else
%define build_option	%nil
%define require_ocaml	%nil
%endif

Summary:	Various simple functions for Mandriva Linux tools
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/soft/perl-MDK-Common/
Source0:	%{name}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ocaml >= 3.08

%description
Various simple functions created for DrakX


%package devel
Summary:	Various verifying scripts
Group:		Development/Perl
AutoReqProv:	0
Requires:	perl-base >= 2:5.8.0 %{require_ocaml}

%description devel
Various verifying scripts created for DrakX


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}


%build
make %{build_option}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std %{build_option}

# remove unwanted files
rm -rf %{buildroot}%{_sysconfdir}/emacs


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{perl_vendorlib}/MDK
%{perl_vendorlib}/MDK/*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{perl_vendorlib}/perl_checker_fake_packages
%{_datadir}/vim/ftplugin/*

%files doc
%defattr(-,root,root)
%doc COPYING index.html tutorial.html perl_checker.src/perl_checker.html


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2
- 1.2.2
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1.24
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.24
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.24-1avx
- 1.1.24
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.22-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.22-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.22-2avx
- bootstrap build

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.22-1avx
- 1.1.22
- don't call "make test" as "make" is doing all that's needed and
  otherwise MDK/Common.pm is not generated when needed due to missing
  dependencies (pixel)

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.21-1avx
- 1.1.21

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.18-2avx
- rebuild against new perl

* Tue Sep 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.1.18-1avx
- 1.1.18
- remove unwanted emacs files
- require newer ocaml

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.1.6-7avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.1.6-6sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 1.1.6-5sls
- rebuild for new perl
- spec cleanups
- own %%{perl_vendorlib}/MDK

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 1.1.6-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
