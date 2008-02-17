#
# spec file for package perl-Net-Netmask
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Net-Netmask
%define revision	$Rev$
%define name		perl-%{module}
%define	version		1.9015
%define	release		%_revrel

Summary: 	%{module} module for Perl
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
License: 	Public Domain
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://www.cpan.org/authors/id/M/MU/MUIR/modules/Net-Netmask-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
Net::Netmask parses and understands IPv4 CIDR blocks. It's built with an
object-oriented interface. Nearly all functions are methods that operate on a
Net::Netmask object.

There are methods that provide the nearly all bits of information about a
network block that you might want.


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
%defattr(-,root,root,755)
%{_mandir}/man3/*
%{perl_vendorlib}/Net


%changelog
* Sun Feb 17 2008 Vincent Danen <vdanen-at-build.annvix.org> 1.9015
- first Annvix build for mrtg-contribs

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
