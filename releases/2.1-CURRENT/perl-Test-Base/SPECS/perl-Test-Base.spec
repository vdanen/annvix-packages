#
# spec file for package perl-Test-Base
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module 		Test-Base
%define revision	$Rev$
%define name		perl-%{module}
%define version 	0.50
%define release 	%_revrel

%define _requires_exceptions Module::Install

Summary:	A data driven perl testing framework
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://cpan.mirrors.easynet.fr/authors/id/I/IN/INGY/%{module}-%{version}.tar.bz2

Buildrequires:  perl-devel
BuildRequires:	perl(Spiffy) >= 0.29
BuildRoot: 	%{_buildroot}/%{name}-%{version}
Buildarch:	noarch

%description
Perl gives you a standard way to run tests with Test::Harness, and basic
testing primitives with Test::More. After that you are pretty much on your own
to develop a testing framework and philosophy. Test::More encourages you to
make your own framework by subclassing Test::Builder, but that is not trivial.
Test::Base gives you a way to write your own test framework base class that is
trivial.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%{perl_vendorlib}/Test/*
%{perl_vendorlib}/Module/Install/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.50
- rebuild

* Wed May 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.50
- first Annvix build (for perl-YAML)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
