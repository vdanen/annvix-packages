#
# spec file for package perl-Crypt-SmbHash
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Crypt-SmbHash
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.12
%define release		%_revrel

Summary:	Crypt::SmbHash Perl module - generate LM/NT hashes like smbpasswd
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://www.cpan.org/modules/by-module/Crypt/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
This module provides functions to generate LM/NT hashes used in
Samba's 'password' files, like smbpasswd.


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


%check
%make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%{perl_vendorlib}/Crypt/SmbHash.pm
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc Changes README


%changelog
* Wed May 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.12
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.12
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-2avx
- bootstrap build

* Tue Feb 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-1avx
- initial Annvix package for new smbldap-tools in samba-3.0.11
- major spec cleanup

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
