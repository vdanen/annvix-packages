%define module 	Net-Daemon
%define version 0.37
%define release 3mdk

Summary:	%{module} perl module
Name: 		perl-%{module}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		ftp://ftp.funet.fi/pub/languages/perl/CPAN/authors/id/JWIED 
Source0:	%{module}-%{version}.tar.bz2
Requires: 	perl
Buildrequires:  perl-devel >= 5.8.0
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
Buildarch:	noarch

%description
%{module} - module for perl

%prep
%setup -q -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc README MANIFEST
%{perl_vendorlib}/Net/*.pm
%{perl_vendorlib}/Net/Daemon/
%{_mandir}/*/*

%changelog
* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.37-3mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Fri May 16 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 0.37-2mdk
- rebuild for dependencies

* Fri Apr 25 2003 François Pons <fpons@mandrakesoft.com> 0.37-1mdk
- 0.37.

* Wed Jan 29 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.36-3mdk
- rebuild

* Wed Jul 31 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.36-2mdk
- rebuild with new perl

* Fri Mar 01 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.36-1mdk
- 0.36

* Wed Aug 29 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.35-1mdk
- added by Christian Zoffoli <czoffoli@linux-mandrake.com> :
	- first mandrake release

