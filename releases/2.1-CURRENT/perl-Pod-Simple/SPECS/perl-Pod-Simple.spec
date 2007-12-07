#
# spec file for package perl-Pod-Simple
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Pod-Simple
%define revision	$Rev$
%define name		perl-%{module}
%define version		3.04
%define release 	%_revrel

Summary:	Perl module to parse Pod
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://search.cpan.org/CPAN/authors/id/A/AR/ARANDAL/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(Pod::Escapes)
BuildArch:	noarch

%description
Pod::Simple is a module suite for parsing Pod.


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
%{perl_vendorlib}/Pod
%{perl_vendorlib}/*.pod
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc ChangeLog README


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.04
- rebuild

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.04
- first Annvix build (needed by perl-perldoc)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
