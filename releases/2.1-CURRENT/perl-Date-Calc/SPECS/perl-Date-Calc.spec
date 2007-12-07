#
# spec file for package perl-Date-Calc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Date-Calc
%define revision	$Rev$
%define name		perl-%{module}
%define	version		5.4
%define	release		%_revrel
%define	pdir		Date

Summary: 	Gregorian calendar date calculations
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/%{pdir}/%{module}-%{version}.tar.bz2

Buildroot:	%{_buildroot}/%{name}-%{version}-buildroot
BuildRequires:	perl-devel
# this versioned require is expressed in Makefile.PL, but not in module
BuildRequires:	perl(Bit::Vector) >= 6.4
BuildRequires:	perl(Carp::Clan) >= 5.3

Requires:	perl(Bit::Vector) >= 6.4
Requires:	perl(Carp::Clan) >= 5.3

%description
This library provides all sorts of date calculations based on the Gregorian
calendar (the one used in all western countries today), thereby complying
with all relevant norms and standards: ISO/R 2015-1971, DIN 1355 and, to
some extent, ISO 8601 (where applicable).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
chmod -R u+w examples

%build
perl -pi -e 's,^#!perl,#!/usr/bin/perl,' examples/*.{pl,cgi}
perl Makefile.PL INSTALLDIRS=vendor
make CFLAGS="%{optflags}"


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,755)
%{_mandir}/man3/Date::*
%dir %{perl_vendorarch}/Date
%{perl_vendorarch}/Date
%{perl_vendorarch}/auto/Date

%files doc
%defattr(-,root,root)
%doc README.txt CHANGES.txt CREDITS.txt EXAMPLES.txt examples


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.4
- rebuild

* Thu May 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.4
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.4
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.4-1avx
- first Annvix build (for swatch)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
