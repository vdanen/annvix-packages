%define module 	PlRPC
%define version 0.2017
%define release 2mdk

Summary:	%{module} perl module
Name: 		perl-%{module}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		ftp://ftp.funet.fi/pub/languages/perl/CPAN/authors/id/JWIED
Source0:	%{module}-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	perl-Net-Daemon perl-Storable perl-devel
Buildarch:	noarch

%description
%{module} - module for perl

%prep
%setup -q -n %{module}-%{version}

%build

%{__perl} Makefile.PL INSTALLDIRS=vendor --defaultdeps
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc README MANIFEST ChangeLog 
%{perl_vendorlib}/Bundle/*
%{perl_vendorlib}/RPC/*
%_mandir/man3*/*

%changelog
* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.2017-2mdk
- rebuild for new perl
- drop PREFIX
- use %%makeinstall_std macro

* Mon Jun 30 2003 François Pons <fpons@mandrakesoft.com> 0.2017-1mdk
- 0.2017.

* Fri May 16 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 0.2016-4mdk
- rebuild for dependencies

* Mon May 05 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.2016-3mdk
- buildrequires

* Wed Mar 12 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.2016-2mdk
- fix build & fix requires

* Mon Mar 04 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.2016-1mdk
- 0.2016

* Tue Sep 25 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.2015-1mdk
- added by Christian Zoffoli <czoffoli@linux-mandrake.com> :
	- first mandrake release

