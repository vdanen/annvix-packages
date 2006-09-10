#
# spec file for package perl-Authen-SASL
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Authen-SASL
%define revision	$Rev$
%define name		perl-%{module}
%define version 	2.10
%define release 	%_revrel

%define _requires_exceptions	perl\(GSSAPI\)

Summary:	%{module} module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://search.cpan.org/CPAN/authors/id/G/GB/GBARR/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
SASL authentication module for perl.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor </dev/null
%make


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
%{perl_vendorlib}/Authen

%files doc
%doc Changes api.txt

%changelog
* Sat May 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.10
- don't require the optional perl GSSAPI module

* Wed May 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.10
- 2.10
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.09
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.09
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.09-1avx
- 2.09
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.04-9avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.04-8avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.04-7avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.04-6avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.04-5sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 2.04-4sls
- rebuild for new perl
- some spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 2.04-3sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.04-2mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Fri May 23 2003 François Pons <fpons@mandrakesoft.com> 2.04-1mdk
- 2.04.

* Fri Jan 24 2003 François Pons <fpons@mandrakesoft.com> 2.03-1mdk
- 2.03.

* Fri Jul 19 2002 François Pons <fpons@mandrakesoft.com> 2.02-1mdk
- initial release (needed by perl-ldap >= 0.26).

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
