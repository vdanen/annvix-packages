#
# spec file for package perl-Compress-Zlib
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Compress-Zlib
%define	revision	$Rev$
%define	name		perl-%{module}
%define	version		1.37
%define	release		%_revrel

Summary:	%{module} module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel zlib-devel

Requires:	perl

%description
The Compress::Zlib module provides a Perl interface to the zlib compression
library.


%prep
%setup -q -n %{module}-%{version}


%build
CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS=vendor
%make
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README
%{_mandir}/*/*
%{perl_vendorarch}/Compress
%{perl_vendorarch}/auto/Compress


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.37-1avx
- 1.37
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35-2avx
- bootstrap build (new gcc, new glibc)

* Thu Jul 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35-1avx
- 1.35

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.33-2avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.33-1avx
- first Annvix build (required for rpmtools)

* Wed Nov 15 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.33-2mdk
- Rebuild for new perl

* Wed Apr 21 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.33-1mdk
- 1.33
- spec cosmetics

* Sun Nov 30 2003 Stefan van der Eijk <stefan@eijk.nu> 1.32-1mdk
- 1.32

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.22-2mdk
- rebuild for new perl
- use %%make macro
- use %%makeinstall_std macro

* Mon Jun 30 2003 François Pons <fpons@mandrakesoft.com> 1.22-1mdk
- 1.22.

* Fri May 23 2003 François Pons <fpons@mandrakesoft.com> 1.21-1mdk
- 1.21.

* Fri Apr 18 2003 François Pons <fpons@mandrakesoft.com> 1.20-1mdk
- 1.20.

* Mon Nov 04 2002 François Pons <fpons@mandrakesoft.com> 1.19-1mdk
- 1.19.

* Fri Oct 25 2002 François Pons <fpons@mandrakesoft.com> 1.17-1mdk
- 1.17.

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 1.16-5mdk
- rebuild for perl thread-multi

* Wed Jul 10 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.16-4mdk
- add 'make test'.

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.16-3mdk
- rebuild for perl 5.8.0

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.16-2mdk
- Automated rebuild in gcc3.1 environment

* Thu Jan 03 2002 François Pons <fpons@mandrakesoft.com> 1.16-1mdk
- 1.16.

* Thu Nov 08 2001 François Pons <fpons@mandrakesoft.com> 1.14-1mdk
- 1.14.

* Tue Oct 16 2001 Stefan van der Eijk <stefan@eijk.nu> 1.13-2mdk
- BuildRequires: perl-devel zlib-devel

* Fri Aug 31 2001 François Pons <fpons@mandrakesoft.com> 1.13-1mdk
- 1.13.
- updated license.
- remove filelist, now use globing and macros.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandarkesoft.com> 1.10-2mdk
- Build against the latest perl 5.6.1.
- Rename spec file.

* Tue Feb 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.10-1mdk
- up to 1.10.
- remove Vendor and Distribution tag (jmd sucks!!)

* Sat Sep 16 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 1.08-2mdk
- Call spec-helper before creating filelist

* Wed Aug 09 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.08-1mdk
- Macroize package
