#
# spec file for package perl-Hdlist
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Hdlist
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.08
%define release 	%_revrel

Summary:	Perl bindings to use rpmlib and manage hdlist files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://cvs.mandrakesoft.com/cgi-bin/cvsweb.cgi/soft/perl-Hdlist/
Source:		%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel >= 5.8.0, rpm-devel, perl-Digest-SHA1, librpmconstant-devel, rpmtools, gnupg

Requires:	perl

%description
This module provides a perl interface to the rpmlib.

It allows to write scripts to:
  - query rpm headers,
  - query rpm database,
  - build rpm specs,
  - install/uninstall specfiles,
  - check dependencies.

It include:
- genrepository, a tools to generate hdlists
- rpm_produced, give what rpm will be produced by a src.rpm or a specfile.

This module is still under development, and is provided for
testing and development purposes only. API may change.


%prep
%setup -q -n %{module}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make

%make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc ChangeLog README
%doc examples
%{_bindir}/*
%{perl_vendorarch}/*
%{_mandir}/*/*

%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.08-3avx
- rebuild against new rpm

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.08-2avx
- rebuild against perl 5.8.7

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.08-1avx
- 0.08

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.07-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.07-2avx
- bootstrap build

* Mon Mar 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.07-1avx
- first Annvix build

* Tue Mar 22 2005 Olivier Thauvin <nanardon@mandrake.org> 0.07-1mdk
- fix segfault in newdep()
- allow to pass undef

* Tue Mar 15 2005 Olivier Thauvin <nanardon@zarb.org> 0.06-1mdk
- update doc
- minor fix

* Tue Mar 08 2005 Olivier Thauvin <nanardon@mandrake.org> 0.05-1mdk
- update doc
- fix build*()

* Mon Mar 07 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.04-1mdk
- add hrpmreb
- allow to pass cookies from installsrpms to newspec
- allow to pass force / anyarch to newspec
- remove forgot debug fprintf
 
* Sat Mar 05 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.03-1mdk
- fix spec build
- add expandnumeric()
- add resetrc
- fix rpmlog()

* Fri Mar 04 2005 Olivier Thauvin <nanardon@mandrake.org> 0.02-1mdk
- BuildRequires (Christiaan Welvaart <cjw@daneel.dyndns.org>)
- split doc

* Tue Feb 22 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.01-1mdk
- use rpmconstant
- lot of fix
 
* Tue Jan 11 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.01-0.20050111.1mdk
- 20040111

* Wed Dec 22 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.01-0.20041222.1mdk
- cvs 20041222

* Tue Nov 16 2004 Michael Scherer <misc@mandrake.org> 0.01-0.20040809.3mdk
- Rebuild for new perl

* Mon Aug 09 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.01-0.20040809.2mdk
- add missing file (/me sucks)

* Mon Aug 09 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.01-0.20040809.1mdk
- cvs 20040809

* Mon Aug 02 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.01-0.20040802.1mdk
- first package
 
* Thu Jul 22 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.01-0.1mdk
- initialize spec
