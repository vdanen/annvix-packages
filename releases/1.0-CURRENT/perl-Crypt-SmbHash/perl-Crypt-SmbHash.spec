%define module	Crypt-SmbHash
%define name	perl-%{module}
%define version	0.12
%define release	1avx

Summary:	Crypt::SmbHash Perl module - generate LM/NT hashes like smbpasswd
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://www.cpan.org/modules/by-module/Crypt/%{module}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	perl-devel
BuildArch:	noarch

%description
This module provides functions to generate LM/NT hashes used in
Samba's 'password' files, like smbpasswd.

%prep
%setup -q -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make

%{!?_without_tests:%{__make} test}

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/Crypt/SmbHash.pm
%{_mandir}/man3/*

%changelog
* Tue Feb 15 2005 Vincent Danen <vdanen@annvix.org> 0.12-1avx
- initial Annvix package for new smbldap-tools in samba-3.0.11
- major spec cleanup

* Thu Feb 10 2005 Buchan Milne <bgmilne@linux-mandrake.com> 0.12-1mdk
- initial package (PLD import) for new smbldap-tools in samba-3.0.11
