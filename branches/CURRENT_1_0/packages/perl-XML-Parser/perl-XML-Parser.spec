%define	module	XML-Parser
%define	name	perl-%{module}
%define	version	2.34
%define	release	5avx

Summary: 	A perl module for parsing XML documents
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Development/Perl
URL: 		http://www.cpan.org
Source: 	http://www.cpan.org/authors/id/C/CO/COOPERCL/%{module}-%{version}.tar.bz2
Source1:	http://uucode.com/xml/perl/enc.tar.bz2

BuildRoot: 	%{_tmppath}/%{name}-buildroot/
BuildRequires: 	libexpat-devel perl-devel perl-libwww-perl perl-HTML-Parser

Requires: 	perl, libexpat1_95

%description
A perl module for parsing XML documents

Needed by eGrail

%prep
%setup -q -n %{module}-%{version} -a 1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="$RPM_OPT_FLAGS"
make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
install -m 644 enc/koi8-r.enc $RPM_BUILD_ROOT%{perl_vendorarch}/XML/Parser/Encodings

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README Changes
%{_mandir}/*/*
%{perl_vendorarch}/XML/Parser*
%{perl_vendorarch}/auto/XML/Parser*


%changelog
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 2.34-5avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.34-4sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 2.34-3sls
- rebuild for new perl
- minor spec cleanups

* Mon Dec 13 2003 Vincent Danen <vdanen@opensls.org> 2.34-2sls
- OpenSLS build
- tidy spec

* Thu Aug 21 2003 François Pons <fpons@mandrakesoft.com> 2.34-1mdk
- 2.34.

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.31-8mdk
- rebuild for new perl
- drop Prefix tag
- drop Distribution tag
- don't use PREFIX
- use %%make macro
- use %%makeinstall_std macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.31-7mdk
- rebuild for new auto{prov,req}

* Mon Oct 28 2002 Pixel <pixel@mandrakesoft.com> 2.31-6mdk
- small cleanup

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 2.31-5mdk
- rebuild for perl thread-multi
- add BuildRequires on perl-libwww-perl and perl-HTML-Parser (for make test)

* Tue Jul 23 2002 François Pons <fpons@mandrakesoft.com> 2.31-4mdk
- added russian encoding from Oleg A. Paraschenko.

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 2.31-3mdk
- oops, add XML/Parser.pm

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 2.31-2mdk
- rebuild for perl 5.8.0
- replace XML with XML/Parser in %%files

* Thu Apr 11 2002 François Pons <fpons@mandrakesoft.com> 2.31-1mdk
- 2.31.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 2.30-5mdk
- BuildRequires: perl-devel

* Tue Sep 11 2001 Pixel <pixel@mandrakesoft.com> 2.30-4mdk
- don't need expat, just need libexpat

* Thu Jun 21 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.30-3mdk
- Fixed distribution tag.
- Put the right directories.
- Description and Summary more explicit

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.30-2mdk
- Rebuild for the latest perl.
- Remove the Distribution and Vendor Tag.

* Mon Feb 19 2001  Daouda Lo <daouda@mandrakesoft.com> 2.30-1mdk
- release 
- use of extern expat module (thanx mad hansen )

* Sat Sep 16 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 2.29-2mdk
- Call spec-helper before creating filelist

* Wed Aug 09 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.29-1mdk
- Macroize package
