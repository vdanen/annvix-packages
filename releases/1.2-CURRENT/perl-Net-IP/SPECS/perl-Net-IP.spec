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
%define version		1.23
%define release 	%_revrel

Summary:	Net::IP perl module
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRequires:	perl-devel
BuildRoot:	%{_buildroot}/%{name}-buildroot
BuildArch:	noarch

Requires:	perl

%description
This module provides functions to deal with IPv4/IPv6 addresses.
The module can be used as a class, allowing the user to instantiate
IP objects, which can be single IP addresses, prefixes, or ranges of
addresses. There is also a procedural way of accessing most of the
functions. Most subroutines can take either IPv4 or IPv6 addresses
transparently.


%prep
%setup -q -n %{module}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%__make


%check
%__make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README Changes
%{_bindir}/ipcount
%{_bindir}/iptab
%{perl_vendorlib}/*
%{_mandir}/*/*


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.23-1avx
- first Annvix build (needed by perl-Net-DNS)

* Fri Jun 10 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.23-1mdk
- 1.23
- spec cleanup

* Thu Jun 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.22-1mdk
- 1.22

* Sat Feb 05 2005  Sylvie Terjan <erinmargault@mandrake.org> 1.21-1mdk
- 1.21-1
- rebuild for new perl

* Sat Aug 28 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.20-2mdk
- rebuild for perl

* Mon Mar 29 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.20-1mdk
- 1st mdk spec
