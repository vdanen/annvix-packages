#
# spec file for package perl-MD5
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		MD5
%define revision	$Rev$
%define name		perl-%{module}
%define version		2.03
%define release		%_revrel

Summary:	The Perl interface to the RSA Message Digest Algorithm
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/author/GAAS/%{module}-%{version}/
Source:		ftp://ftp.perl.org//pub/CPAN/modules/by-module/%{module}/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel

%description
The perl-MD5 package provides the MD5 module for the Perl
programming language.  MD5 is a Perl interface to the RSA Data
Security Inc. Message Digest Algorithm, which allows Perl
programs to use the algorithm.


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


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
rm -f %{buildroot}%{perl_archlib}/perllocal.pod


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/*.pm
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc README


%changelog
* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.03
- first Annvix build (needed by perl-HTTP-DAV)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
