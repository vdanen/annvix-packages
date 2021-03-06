#
# spec file for package perl-Tie-IxHash
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module  	Tie-IxHash
%define revision	$Rev$
%define name		perl-%{module}
%define version 	1.21
%define release 	%_revrel
%define	pdir		Tie


Summary: 	%{module} module for perl
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group: 		Development/Perl
URL:            http://search.cpan.org/search?dist=%{module}
Source0: 	ftp://ftp.perl.org/pub/CPAN/modules/by-module/%{pdir}/%{module}-%{version}.tar.gz

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildArch: 	noarch
BuildRequires:	perl-devel

%description
%{module} module for perl.  This Perl module implements ordered
in-memory associative arrays.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(444,root,root,755)
%{_mandir}/*/*
%{perl_vendorlib}/Tie/IxHash.pm

%files doc
%defattr(-,root,root)
%doc Changes README


%changelog
* Sat May 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.21
- rebuild against perl 5.8.8
- create -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.21
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.21
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.21-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.21-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.21-2avx
- bootstrap build

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.21-1avx
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
