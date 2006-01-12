#
# spec file for package perl-Tie-IxHash
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module  	Tie-IxHash
%define revision	$Rev$
%define name		perl-%{module}
%define version 	1.21
%define release 	%_revrel
%define	pdir		Tie


Summary: 	%{module} module for perl
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group: 		Development/Perl
URL:            http://search.cpan.org/search?dist=%{module}
Source0: 	ftp://ftp.perl.org/pub/CPAN/modules/by-module/%{pdir}/%{module}-%{version}.tar.gz

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildArch: 	noarch
BuildRequires:	perl-devel

Requires: 	perl

%description
%{module} module for perl.  This Perl module implements ordered
in-memory associative arrays.


%prep
%setup -q -n %{module}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(444,root,root,755)
%doc Changes README
%{_mandir}/*/*
%{perl_vendorlib}/Tie/IxHash.pm


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.21-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.21-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.21-2avx
- bootstrap build

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.21-1avx
- first Annvix build

* Thu Sep 23 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.21-7mdk
- rebuild

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.21-6mdk
- don't use PREFIX
- use %%makeinstall_std macro

* Tue Aug 12 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.21-5mdk
- rebuild

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.21-4mdk
- rebuild for new auto{prov,req}

* Sat Feb 01 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.21-3mdk
- rebuild

* Thu Jul 11 2002 Pixel <pixel@mandrakesoft.com> 1.21-2mdk
- rebuild for perl 5.8.0

* Mon Jun 10 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.21-1mdk
- from Peter Chen <petechen@netilla.com> :
	- 1.21
