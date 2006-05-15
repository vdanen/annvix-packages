#
# spec file for package perl-ldap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		perl-ldap
%define version 	0.33
%define release 	%_revrel

Summary:	Perl module for ldap
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%name/
Source:		http:///www.cpan.org/authors/id/G/GB/GBARR/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel >= 5.8.0
BuildRequires:	perl(Convert::ASN1) >= 0.07
BuildRequires:	perl(IO::Socket::SSL)

Requires:	perl(Authen::SASL) >= 2.00
Requires:	perl(XML::Parser)
Requires:	perl(Convert::ASN1) >= 0.07

%description
The perl-ldap distribution is a collection of perl modules
which provide an object-oriented interface to LDAP servers.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make


%check
%make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{perl_vendorlib}/LWP
%{perl_vendorlib}/Bundle
%{perl_vendorlib}/Net

%files doc
%defattr(-,root,root)
%doc CREDITS README


%changelog
* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.33
- 0.33
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy
- update description
- fix license
- BuildRequires: perl(Convert::ASN1), perl(IO::Socket::SSL)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.31
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.31
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.31-6avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.31-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.31-4avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.31-3avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.31-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.31-1sls
- 0.31
- own dirs

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 0.29-3sls
- rebuild for new perl

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 0.29-2sls
- OpenSLS build
- tidy spec

* Thu Aug 21 2003 François Pons <fpons@mandrakesoft.com> 0.29-1mdk
- 0.29.

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.28-2mdk
- rebuild for new perl
- drop Prefix tag
- don't use PREFIX
- use %%makeinstall_std macro
- drop $RPM_OPT_FLAGS, noarch..
- quiet setup

* Fri May 23 2003 François Pons <fpons@mandrakesoft.com> 0.28-1mdk
- 0.28.

* Fri Apr 25 2003 François Pons <fpons@mandrakesoft.com> 0.27.01-2mdk
- added missing requires to perl-Convert-ASN1 (bug 3473).

* Tue Jan 28 2003 François Pons <fpons@mandrakesoft.com> 0.27.01-1mdk
- 0.2701.

* Sun Jul 21 2002 Pixel <pixel@mandrakesoft.com> 0.26-2mdk
- fix require

* Fri Jul 19 2002 François Pons <fpons@mandrakesoft.com> 0.26-1mdk
- 0.26.

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 0.25-2mdk
- rebuild for perl 5.8.0

* Thu Nov 08 2001 François Pons <fpons@mandrakesoft.com> 0.25-1mdk
- make it noarch.
- added documentation.
- added url tag.
- removed perllocal.pod.
- 0.25.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 0.24-2mdk
- BuildRequires: perl-devel
- Copyright --> License

* Wed Aug  8 2001 Vincent Saugey <vince@mandrakesoft.com> 0.24-1mdk
- First mdk release
