#
# spec file for package perl-Carp-Clan
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Carp-Clan
%define revision	$Rev$
%define name		perl-%{module}
%define	version		5.3
%define	release		%_revrel
%define	pdir		Carp

Summary: 	%{module} module for perl
Name: 		perl-%{module}
Version: 	%{version}
Release:	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/%{pdir}/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
%{module} module for perl.
This module reports errors from the perspective of the caller of a
"clan" of modules, similar to "Carp.pm" itself. But instead of giving
it a number of levels to skip on the calling stack, you give it a
pattern to characterize the package names of the "clan" of modules
which shall never be blamed for any error.


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
LANG=C %make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%{_mandir}/man3/Carp::Clan*
%dir %{perl_vendorlib}/Carp
%{perl_vendorlib}/Carp/Clan*

%files doc
%defattr(644,root,root,755)
%doc CHANGES.txt README.txt


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.3
- rebuild

* Wed May 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.3
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.3
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.3-1avx
- first build for Annvix (needed by perl-Bit-Vector)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
