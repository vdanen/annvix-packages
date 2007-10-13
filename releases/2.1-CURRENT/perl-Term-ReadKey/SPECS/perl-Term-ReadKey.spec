#
# spec file for package perl-Term-ReadKey
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#

%define module		Term-ReadKey
%define revision	$Rev$
%define name		perl-%{module}
%define version		2.30
%define release		%_revrel

Summary:	Term::ReadKey modules for Perl 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/TermReadKey/
Source0:	http://search.cpan.org/CPAN/authors/id/J/JS/JSTOWE/TermReadKey-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel

Requires:	perl(Geography::Countries)

%description
This module, ReadKey, provides ioctl control for terminals so the input modes
can be changed (thus allowing reads of a single character at a time), and
also provides non-blocking reads of stdin, as well as several other terminal
related features, including retrieval/modification of the screen size, and
retrieval/modification of the control characters.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n TermReadKey-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor </dev/null
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
%{perl_vendorlib}/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README


%changelog
* Fri Oct 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.30
- first Annvix build (required by apparmor-utils)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
