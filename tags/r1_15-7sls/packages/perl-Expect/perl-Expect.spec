%define module	Expect
%define name	perl-%{module}
%define version 1.15
%define release 7sls

Summary:	Expect perl module
Name: 		%{name}
Version: 	%{version}
Release:	%{release} 
License: 	GPL
Group: 		Development/Perl
URL:		http://www.cpan.org
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/Expect/Expect-%{version}.tar.bz2
Patch0:		%{name}-paths.patch.bz2

BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildArch:	noarch
BuildRequires:	perl-IO-Tty >= 1.02, perl-devel

Prefix:		%{_prefix}
Requires: 	perl, perl-IO-Tty


%description
Expect perl module.

%prep
%setup -q -n %{module}-%{version}

%patch -p1

%build

%{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean 
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,root,root,755)
%doc Changes README examples tutorial
%{perl_vendorlib}/*.pm
%{perl_vendorlib}/*.pod
%{_mandir}/*/*

%changelog
* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.15-7sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.15-6mdk
- rebuild for new perl
- rm -rf $RPM_BUILD_ROOT in %%install, not %%prep
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.15-5mdk
- rebuild for new auto{prov,req}

* Fri May  2 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.15-4mdk
- BuildRequires

* Tue Apr 28 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.15-3mdk
- drop perl-IO-Stty BuildRequires (distriblint), add missing .pod file

* Tue Aug  6 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.15-2mdk
- Requires perl-IO-Tty

* Wed Jul 24 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.15-1mdk
- 1.15

* Tue Sep 25 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.12-1mdk
- added by Max Heijndijk <cchq@wanadoo.nl> :
	- Initial wrap
