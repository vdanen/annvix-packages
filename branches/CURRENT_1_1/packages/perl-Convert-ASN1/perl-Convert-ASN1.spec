%define module	Convert-ASN1
%define name	perl-%{module}
%define version 0.18
%define release 4avx

Summary: 	ASN.1 Encode/Decode library for perl
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group: 		Development/Perl
URL: 		http://www.cpan.org
Source: 	http://www.cpan.org/authors/id/GBARR/%{module}-%{version}.tar.bz2

BuildRoot: 	%{_tmppath}/%{name}-buildroot/
BuildArch: 	noarch
BuildRequires:	perl-devel

Prefix: 	%{_prefix}
Requires:	perl >= 5.6

%description
Perl module used to encode and decode ASN.1 data structures using
BER/DER rules.

Needed by webmin to handle the OpenLDAP modules properly.

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
%defattr(-,root,root)
%doc ChangeLog MANIFEST README examples/*
%{perl_vendorlib}/Convert/*
%{_mandir}/*/*

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 0.18-4avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 0.18-3avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 0.18-2avx
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
- rm -rf $RPM_BUILD_ROOT in %%install, not %%build
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
