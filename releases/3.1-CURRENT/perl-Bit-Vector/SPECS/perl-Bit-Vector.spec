#
# spec file for package perl-Bit-Vector
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Bit-Vector
%define revision	$Rev$
%define name		perl-%{module}
%define	version		6.4
%define	release		%_revrel
%define	pdir		Bit

Summary: 	%{module} module for perl
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/%{pdir}/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(Carp::Clan)

%description
%{module} module for perl.
Bit::Vector is an efficient C library which allows you to handle
bit vectors, sets (of integers), "big integer arithmetic" and
boolean matrices, all of arbitrary sizes.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
chmod -R u+w examples


%build
perl Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="$RPM_OPT_FLAGS"


%check
LANG=C %make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,755)
%{_mandir}/man3/Bit::Vector*
%dir %{perl_vendorarch}/Bit
%{perl_vendorarch}/Bit/Vector*
%dir %{perl_vendorarch}/auto/Bit
%{perl_vendorarch}/auto/Bit/Vector*

%files doc
%defattr(-,root,root)
%doc CHANGES.txt CREDITS.txt INSTALL.txt README.txt examples


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 6.4
- rebuild

* Wed May 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.4
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.4
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.4-1avx
- first build for Annvix (required by perl-Date-Calc)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
