#
# spec file for package perl-HTML-Parser
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		HTML-Parser
%define revision	$Rev$
%define name		perl-%{module}
%define version 	3.51
%define release 	%_revrel

Summary: 	Perl module to parse HTML documents
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group: 		Development/Perl
URL: 		http://search.cpan.org/dist/%{module}/
Source:		ftp://ftp.cpan.org/pub/CPAN/modules/by-module/HTML/%{module}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(HTML::Tagset)

Requires: 	perl(HTML::Tagset) >= 3.03

%description
HTML::Parser module for perl to parse and extract information
from HTML documents.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
# compile with default options (prompt() checks for STDIN being a terminal).
# yes to not ask for automate rebuild
yes | perl Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="%{optflags}"


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/HTML

%files doc
%defattr(-,root,root)
%doc README TODO Changes


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.51
- 3.51
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.45
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.45
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.45-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.45-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.45-2avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.45-1avx
- 3.45
- own dirs (thauvin)

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.31-6avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.31-5avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 3.31-4sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 3.31-3sls
- rebuild for new perl

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 3.31-2sls
- OpenSLS build
- tidy spec

* Thu Aug 21 2003 François Pons <fpons@mandrakesoft.com> 3.31-1mdk
- 3.31.

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.28-4mdk
- rebuild for new perl
- drop Prefix tag
- drop Distribution tag
- don't use PREFIX
- use %%makeinstall_std macro
- use %%make macro

* Fri Jun 06 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 3.28-3mdk
- do not wait a reply from term for automate rebuild

* Tue May 13 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.28-2mdk
- rebuild for new perl provides/requires

* Fri Apr 18 2003 François Pons <fpons@mandrakesoft.com> 3.28-1mdk
- 3.28.

* Fri Jan 24 2003 François Pons <fpons@mandrakesoft.com> 3.27-1mdk
- 3.27.

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 3.26-3mdk
- rebuild for perl thread-multi

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 3.26-2mdk
- rebuild for perl 5.8.0

* Tue Mar 26 2002 François Pons <fpons@mandrakesoft.com> 3.26-1mdk
- 3.26.

* Thu Nov 08 2001 François Pons <fpons@mandrakesoft.com> 3.25-3mdk
- build release.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 3.25-2mdk
- BuildRequires: perl-devel perl-HTML-Tagset

* Tue Jul 03 2001 François Pons <fpons@mandrakesoft.com> 3.25-1mdk
- 3.25.

* Wed Jun 20 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.18-3mdk
- Fixed distribution tag.
- Updated Requires.
- Added an option to %makeinstall.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.18-2mdk
- Rebuild against the latest perl.

* Tue Feb 27 2001 François Pons <fpons@mandrakesoft.com> 3.18-1mdk
- 3.18.

* Tue Jan 30 2001 François Pons <fpons@mandrakesoft.com> 3.15-1mdk
- 3.15.

* Tue Dec 05 2000 François Pons <fpons@mandrakesoft.com> 3.14-1mdk
- 3.14.

* Thu Oct 12 2000 François Pons <fpons@mandrakesoft.com> 3.13-1mdk
- 3.13.

* Tue Aug 29 2000 François Pons <fpons@mandrakesoft.com> 3.11-1mdk
- 3.11.

* Thu Aug 03 2000 François Pons <fpons@mandrakesoft.com> 3.10-2mdk
- macroszifications.
- add doc.

* Tue Jul 18 2000 François Pons <fpons@mandrakesoft.com> 3.10-1mdk
- removed perllocal.pod from files.
- 3.10.

* Tue Jun 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 3.08-1mdk
- update to 3.08

* Wed May 17 2000 David BAUDENS <baudens@mandrakesoft.com> 3.05-4mdk
- Fix build for i486
- Use %%{_buildroot} for BuildRoot

* Fri Mar 31 2000 Pixel <pixel@mandrakesoft.com> 3.05-3mdk
- rebuild, new group, cleanup

* Tue Feb 29 2000 Jean-Michel Dault <jmdault@netrevolution.com> 3.0.5-1mdk
- upgrade to 3.05

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- final cleanup for Mandrake 7

* Thu Dec 30 1999 Jean-Michel Dault <jmdault@netrevolution.com>
-updated to 3.02

* Sun Aug 29 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- bzip2'd sources
- updated to 2.23

* Tue May 11 1999 root <root@alien.devel.redhat.com>
- Spec file was autogenerated. 

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
