#
# spec file for package perl-URI
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		URI
%define revision	$Rev$
%define name		perl-%{module}
%define version 	1.35
%define release 	%_revrel

%define _requires_exceptions perl(Business::ISBN)

Summary: 	URI module for perl
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group: 		Development/Perl
URL: 		http://search.cpan.org/dist/%{module}/
Source: 	http://www.cpan.org/authors/id/GAAS/%{module}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildArch: 	noarch
BuildRequires:	perl-devel rpm-build >= 4.2-7mdk

Requires: 	perl

%description
This perl module implements the URI class. Object of this class
represent Uniform Resource Identifier (URI) references as specified
in RFC 2396.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/URI.pm
%{perl_vendorlib}/URI
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc Changes README rfc2396.txt


%changelog
* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.35
- rebuild against perl 5.8.8
- create -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.35
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35-2avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35-1avx
- 1.35
- update description

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.25-5avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.25-4sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 1.25-3sls
- rebuild for new perl

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.25-2sls
- OpenSLS build
- tidy spec

* Thu Aug 21 2003 François Pons <fpons@mandrakesoft.com> 1.25-1mdk
- 1.25.

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.23-4mdk
- rebuild for new perl
- drop Prefix tag
- don't use PREFIX
- use %%makeinstall_std macro
- drop $RPM_OPT_FLAGS, noarch..

* Tue May 13 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.23-3mdk
- fix requires by adding some exceptions for unavailable perl modules

* Tue May 13 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.23-2mdk
- rebuild for new perl provides/requires

* Thu Jan 09 2003 François Pons <fpons@mandrakesoft.com> 1.23-1mdk
- 1.23.

* Fri Oct 11 2002 François Pons <fpons@mandrakesoft.com> 1.22-1mdk
- 1.22.

* Fri Jul 19 2002 François Pons <fpons@mandrakesoft.com> 1.20-1mdk
- 1.20.

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.19-2mdk
- rebuild for perl 5.8.0

* Mon May 13 2002 François Pons <fpons@mandrakesoft.com> 1.19-1mdk
- 1.19.

* Thu Jan 03 2002 François Pons <fpons@mandrakesoft.com> 1.18-1mdk
- 1.18.

* Tue Oct 23 2001 François Pons <fpons@mandrakesoft.com> 1.17-1mdk
- 1.17.

* Fri Aug 24 2001 François Pons <fpons@mandrakesoft.com> 1.15-1mdk
- 1.15.

* Sat Jul 07 2001 Stefan van der Eijk <stefan@eijk.nu> 1.12-3mdk
- BuildRequires:	perl-devel

* Tue Jul 03 2001 François Pons <fpons@mandrakesoft.com> 1.12-2mdk
- fixed reference to perl version number explicitely.
- added missing files in packages (?!).

* Thu Jun 21 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.12-1mdk
- 1.12.
- Clean up spec a little bit
- Needed by eGrail.
- Macronize a little bit more.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.10-2mdk
- Rebuild for the latest perl.

* Tue Jan 30 2001 François Pons <fpons@mandrakesoft.com> 1.10-1mdk
- 1.10.

* Tue Aug 29 2000 François Pons <fpons@mandrakesoft.com> 1.09-1mdk
- 1.09.

* Thu Aug 03 2000 François Pons <fpons@mandrakesoft.com> 1.08-1mdk
- macroszifications.
- update requires on perl version.
- noarch as no compilation done.
- added documentation.
- updated description.
- 1.08.

* Tue Jun 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.07-1mdk
- update to 1.07

* Fri Mar 31 2000 Pixel <pixel@mandrakesoft.com> 1.05-2mdk
- new group, rebuild, cleanup

* Tue Feb 29 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- upgraded to 1.05

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- final cleanup for Mandrake 7

* Thu Dec 30 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- rebuilt for Mandrake 7

* Sun Aug 29 1999 Jean-Michel Dault <jmdault@netrevolution.com?
- bzip2'd sources
- updated to 1.04

* Tue May 11 1999 root <root@alien.devel.redhat.com>
- Spec file was autogenerated. 
