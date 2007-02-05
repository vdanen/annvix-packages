#
# spec file for package perl-Spiffy
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module 		Spiffy
%define revision	$Rev$
%define name		perl-%{module}
%define version 	0.30
%define release 	%_revrel

Summary:	Spiffy perl interface framework
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://search.cpan.org/CPAN/authors/id/I/IN/INGY/%{module}-%{version}.tar.bz2

BuildRequires:  perl-devel
BuildRoot: 	%{_buildroot}/%{name}-%{version}
Buildarch:	noarch

%description
"Spiffy" is a framework and methodology for doing object oriented (OO)
programming in Perl. Spiffy combines the best parts of Exporter.pm,
base.pm, mixin.pm and SUPER.pm into one magic foundation class. It
attempts to fix all the nits and warts of traditional Perl OO, in a clean,
straightforward and (perhaps someday) standard way.

Spiffy borrows ideas from other OO languages like Python, Ruby, Java and
Perl 6. It also adds a few tricks of its own.


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
%{perl_vendorlib}/Spiffy.pm
%{_mandir}/man*/*

%files doc
%defattr(-,root,root)
%doc Changes README


%changelog
* Wed May 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.30
- first Annvix build (for perl-Test-Base)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
