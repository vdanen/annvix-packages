#
# spec file for package perl-version
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module 		version
%define revision	$Rev$
%define name		perl-%{module}
%define version 	0.74
%define release 	%_revrel

Summary:	Perl extension for Version Objects
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://search.cpan.org/CPAN/authors/id/J/JP/JPEACOCK/version-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Test::More)
BuildRoot: 	%{_buildroot}/%{name}-%{version}

%description
Overloaded version objects for all versions of Perl. This module implements
all of the features of version objects which will be part of Perl 5.10.0
except automatic version object creation.

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
%{perl_vendorarch}/version*
%{perl_vendorarch}/auto/version
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc Changes README


%changelog
* Sun Dec 09 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.74
- first Annvix build (needed by SpamAssassin)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
