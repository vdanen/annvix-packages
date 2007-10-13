#
# spec file for package perl-RPC-XML
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		RPC-XML
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.59
%define release		%_revrel

Summary:	A set of classes for core data, message and XML handling
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://www.cpan.org/modules/by-module/RPC/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	perl(LWP::UserAgent)
BuildArch:	noarch

%description
The RPC::XML package is a reference implementation of the XML-RPC
standard. As a reference implementation, it is geared more towards clarity and
readability than efficiency.

The package provides a set of classes for creating values to pass to the
constructors for requests and responses. These are lightweight objects, most
of which are implemented as tied scalars so as to associate specific type
information with the value. Classes are also provided for requests, responses,
faults (errors) and a parser based on the XML::Parser package from CPAN.

This module does not actually provide any transport implementation or
server basis. For these, see RPC::XML::Client and RPC::XML::Server,
respectively.


%package Apache
Summary:	RPC server as an Apache/mod_perl content handler
Group:		Development/Perl

%description Apache
RPC server as an Apache/mod_perl content handler.


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
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*
%{perl_vendorlib}/RPC
%{perl_vendorlib}/auto/RPC
%{_mandir}/man3/*
%exclude %{_mandir}/man3/Apache*
%{_mandir}/man1/*

%files Apache
%defattr(-,root,root)
%{perl_vendorlib}/Apache
%{_mandir}/man3/Apache*

%files doc
%defattr(-,root,root)
%doc README* ChangeLog


%changelog
* Fri Oct 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.59
- first Annvix build (required by apparmor-utils)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
