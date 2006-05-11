#
# spec file for package perl-Convert-ASN1
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Convert-ASN1
%define revision	$Rev$
%define name		perl-%{module}
%define version 	0.20
%define release 	%_revrel

Summary: 	ASN.1 Encode/Decode library for perl
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group: 		Development/Perl
URL: 		http://search.cpan.org/dist/%{real_name}/
Source: 	http://www.cpan.org/authors/id/GBARR/%{module}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildArch: 	noarch
BuildRequires:	perl-devel

%description
Perl module used to encode and decode ASN.1 data structures using
BER/DER rules.


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
%{perl_vendorlib}/Convert/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc ChangeLog README examples/*


%changelog
* Wed May 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.20
- 0.20
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.19
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.19
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.19-1avx
- 0.19
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.18-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.18-4avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.18-3avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.18-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.18-1sls
- 0.18

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 0.16-6sls
- rebuild for new perl

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 0.16-5sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.16-4mdk
- rebuild for new perl
- don't use PREFIX
- rm -rf %{buildroot} in %%install, not %%build
- use %%makeinstall_std macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.16-3mdk
- rebuild for auto{req,prov}

* Fri Jan 24 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.16-2mdk
- rebuild

* Tue Oct 15 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.16-1mdk
- from  Daniel Lacroix <dlacroix@erasme.org>
	- 0.16

* Mon Aug 05 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 0.15-4mdk
- Make rpmlint happy by chmod 644'ing Convert tar.bz2

* Mon Aug 05 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 0.15-3mdk
- Make it Require Perl >= 5.6, so that it can be installed on Perl 5.8 systems

* Tue Jul 23 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.15-2mdk
- rebuild with new perl

* Mon Jun 17 2002 Vincent Danen <vdanen@mandrakesoft.com> 0.15-1mdk
- first Mandrake spec
