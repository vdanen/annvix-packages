#
# spec file for package perl-Archive-Tar
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$  

%define	module		Archive-Tar
%define revision	$Rev$
%define	name		perl-%{module}
%define version		1.30
%define release		%_revrel

Summary:	Perl module for manipulation of tar archives
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/Archive/%{module}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
Perl module for manipulation of tar archives.


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
%{perl_vendorlib}/Archive
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/*

%files doc
%doc README


%changelog
* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.30
- 1.30

* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.29
- rebuild against perl 5.8.8
- create -doc subpackage

* Tue Mar 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.29
- first Annvix build (for spamassassin)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
