%define module	Devel-Symdump
%define version 2.03
%define release 4mdk

Packager: Jean-Michel Dault <jmdault@mandrakesoft.com>

Summary:	%{module} module for perl
Name:		perl-%{module}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
Source0:	%{module}-%{version}.tar.bz2
Url:		http://www.cpan.org
BuildRequires:	perl-devel >= 0:5.600
BuildRoot:	%{_tmppath}/%{name}-buildroot/
BuildArch:	noarch

%description
%{module} module for perl

%prep
%setup -q -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%files
%defattr(-,root,root)
%doc ChangeLog README
%{perl_vendorlib}/Devel
%{_mandir}/*/*

%changelog
* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.03-4mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.03-3mdk
- rebuild for new auto{prov,req}

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 2.03-2mdk
- rebuild for perl 5.8.0

* Mon May 13 2002 François Pons <fpons@mandrakesoft.com> 2.03-1mdk
- 2.03.

* Tue Mar 26 2002 François Pons <fpons@mandrakesoft.com> 2.02-1mdk
- remove filelist and use a right %%files.
- updated License.
- 2.02.

* Tue Oct 16 2001 Stefan van der Eijk <stefan@eijk.nu> 2.01-5mdk
- BuildRequires: perl-devel

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.01-4mdk
- Rebuild this against the latest perl.
- Remove hardcoded references to Distribution and Vendor.

* Tue Mar 13 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.01-3mdk
- BuildArch: noarch
- add docs
- rename spec file
- clean spec a bit
- run automated tests

* Sat Sep 16 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 2.01-2mdk
- Call spec-helper before creating filelist

* Wed Aug 09 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.01-1mdk
- Macroize package
