#
# spec file for package perl-Pod-Escapes
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Pod-Escapes
%define revision	$Rev$
%define name		perl-%{module}
%define version		1.04
%define release 	%_revrel

Summary:	Perl module to resolve Pod E<...> sequences
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://search.cpan.org/CPAN/authors/id/S/SB/SBURKE/%{module}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
Pod::Escapes is a module to resolve Pod E<...> sequences.


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
%defattr(-,root,root)
%{perl_vendorlib}/Pod
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc ChangeLog README


%changelog
* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.04
- first Annvix build (needed by perl-Pod-Simple)
