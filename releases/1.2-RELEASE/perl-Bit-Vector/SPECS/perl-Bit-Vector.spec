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

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl-Carp-Clan

%description
%{module} module for perl.
Bit::Vector is an efficient C library which allows you to handle
bit vectors, sets (of integers), "big integer arithmetic" and
boolean matrices, all of arbitrary sizes.


%prep
%setup -q -n %{module}-%{version}
chmod -R u+w examples


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
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
%doc CHANGES.txt CREDITS.txt INSTALL.txt README.txt examples
%{_mandir}/man3/Bit::Vector*
%dir %{perl_vendorarch}/Bit
%{perl_vendorarch}/Bit/Vector*
%dir %{perl_vendorarch}/auto/Bit
%{perl_vendorarch}/auto/Bit/Vector*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.4-1avx
- first build for Annvix (required by perl-Date-Calc)

* Sun Nov 21 2004 Stefan van der Eijk <stefan@mandrake.org> 6.4-2mdk
- BuildRequires

* Mon Nov 15 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 6.4-1mdk
- New version 6.4

* Thu Feb 12 2004 Luca Berra <bluca@vodka.it> 6.3-4mdk
- rebuild for perl 5.8.3

* Tue Dec 30 2003 Luca Berra <bluca@vodka.it> 6.3-3mdk
- add parent dirs (distriblint)
- fixed permissions on examples

* Wed Oct 15 2003 Luca Berra <bluca@vodka.it> 6.3-2mdk
- added examples to documentation

* Sun Oct 05 2003 Luca Berra <bluca@vodka.it> 6.3-1mdk
- Initial build.
