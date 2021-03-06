#
# spec file for package perl-Date-Calc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Date-Calc
%define revision	$Rev$
%define name		perl-%{module}
%define	version		5.4
%define	release		%_revrel
%define	pdir		Date

Summary: 	Gregorian calendar date calculations
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/%{pdir}/%{module}-%{version}.tar.bz2

Buildroot:	%{_buildroot}/%{name}-%{version}-buildroot
BuildRequires:	perl-devel
# this versioned require is expressed in README, but not in module
BuildRequires:	perl-Bit-Vector >= 5.7

Requires:	perl-Bit-Vector >= 5.7

%description
This library provides all sorts of date calculations based on the Gregorian
calendar (the one used in all western countries today), thereby complying
with all relevant norms and standards: ISO/R 2015-1971, DIN 1355 and, to
some extent, ISO 8601 (where applicable).


%prep
%setup -q -n %{module}-%{version}
chmod -R u+w examples

%build
%{__perl} -pi -e 's,^#!perl,#!/usr/bin/perl,' examples/*.{pl,cgi}
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make}

%check
%{__make} test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,755)
%doc README.txt CHANGES.txt CREDITS.txt EXAMPLES.txt examples
%{_mandir}/man3/Date::*
%dir %{perl_vendorarch}/Date
%{perl_vendorarch}/Date/*
%dir %{perl_vendorarch}/auto/Date
%{perl_vendorarch}/auto/Date/Calc


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.4-1avx
- first Annvix build (for swatch)

* Wed Jun 15 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 5.4-3mdk
- Rebuild, cleanup, %check

* Mon Nov 15 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.4-2mdk
- rebuild for new perl

* Tue Nov 09 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.4-1mdk
- 5.4

* Thu Feb 12 2004 Luca Berra <bluca@vodka.it> 5.3-8mdk
- rebuild for perl 5.8.3

* Tue Dec 30 2003 Luca Berra <bluca@vodka.it> 5.3-7mdk
- add parent dirs (distriblint)

* Thu Dec 25 2003 Luca Berra <bluca@vodka.it> 5.3-6mdk
- changed requires syntax for perl-Bit-Vector
- fixed permissions on examples

* Wed Oct 15 2003 Luca Berra <bluca@vodka.it> 5.3-5mdk
- added examples to documentation

* Sun Oct 05 2003 Luca Berra <bluca@vodka.it> 5.3-4mdk
- removed Carp::Clam (provided in own package)

* Wed Aug 13 2003 Per ?yvind Karlsen <peroyvind@linux-mandrake.com> 5.3-3mdk
- rebuild for new perl
- drop Prefix tag
- don't use PREFIX
- use %%makeinstall_std macro
- use %%make macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.3-2mdk
- fix unpackaged files
- rebuild for new auto{prov,req}

* Wed Oct 16 2002 Fran?ois Pons <fpons@mandrakesoft.com> 5.3-1mdk
- 5.3.

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 5.0-3mdk
- rebuild for perl thread-multi

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 5.0-2mdk
- rebuild for perl 5.8.0

* Thu Oct 25 2001 Christian Belisle <cbelisle@mandrakesoft.com> 5.0-1mdk
- 5.0 is out.

* Tue Oct 16 2001 Stefan van der Eijk <stefan@eijk.nu> 4.3-5mdk
- BuildRequires: perl-devel

* Sun Jun 24 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.3-4mdk
- .so is packaged now (thanx to Sebastian Dransfeld)

* Wed Jun 20 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.3-3mdk
- Make a clean RPM with the right directories
- Fixed distribution tag
- Changed description

* Sun Jun 17 2001 Geoffrey Lee <snaitalk@mandrakesoft.com> 4.3-2mdk
- Make a RPM for the latest perl.

* Thu Aug 31 2000 Enzo Maggi <enzo@mandrakesoft.com> 4.3-1mdk
- packaged 4.3

* Mon Aug  7 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 4.2-1mdk
- First mandrake package

* Tue May 11 1999 root <root@alien.devel.redhat.com>
- Spec file was autogenerated. 
