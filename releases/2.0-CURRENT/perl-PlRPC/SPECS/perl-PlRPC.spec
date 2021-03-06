#
# spec file for package perl-PlRPC
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module 		PlRPC
%define revision	$Rev$
%define name		perl-%{module}
%define version 	0.2018
%define release 	%_revrel

Summary:	%{module} perl module
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		ftp://ftp.funet.fi/pub/languages/perl/CPAN/authors/id/JWIED
Source0:	%{module}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(Net::Daemon)
Buildarch:	noarch

%description
%{module} - module for perl


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor --defaultdeps
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/Bundle/*
%{perl_vendorlib}/RPC/*
%{_mandir}/man3*/*

%files doc
%defattr(-,root,root)
%doc README ChangeLog 


%changelog
* Sat May 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2018
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2018
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2018
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2018-1avx
- 0.2018

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2017-9avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2017-8avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2017-7avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.2017-6avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.2017-5sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 0.2017-4sls
- rebuild for new perl

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 0.2017-3sls
- OpenSLS build
- tidy spec
- remove redundant perl-Storable BuildReq (part of perl)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
