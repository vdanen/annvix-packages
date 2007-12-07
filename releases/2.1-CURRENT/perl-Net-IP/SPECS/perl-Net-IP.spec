#
# spec file for package perl-Net-IP
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Net-IP
%define revision	$Rev$
%define name 		perl-%{module}
%define version		1.25
%define release 	%_revrel

Summary:	Net::IP perl module
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	http://www.cpan.org/modules/by-module/Net/%{module}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
This module provides functions to deal with IPv4/IPv6 addresses.
The module can be used as a class, allowing the user to instantiate
IP objects, which can be single IP addresses, prefixes, or ranges of
addresses. There is also a procedural way of accessing most of the
functions. Most subroutines can take either IPv4 or IPv6 addresses
transparently.


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
%defattr(-,root,root)
%{_bindir}/ipcount
%{_bindir}/iptab
%{perl_vendorlib}/Net
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.25
- rebuild

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.25
- 1.25

* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.24
- 1.24
- rebuild against perl 5.8.8
- create -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.23
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.23
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.23-1avx
- first Annvix build (needed by perl-Net-DNS)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
