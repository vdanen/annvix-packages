%define module 	Net-Daemon
%define name	perl-%{module}
%define version 0.37
%define release 9avx

Summary:	%{module} perl module
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		ftp://ftp.funet.fi/pub/languages/perl/CPAN/authors/id/JWIED 
Source0:	%{module}-%{version}.tar.bz2

Buildrequires:  perl-devel >= 5.8.0
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
Buildarch:	noarch

Requires: 	perl

%description
%{module} - module for perl

%prep
%setup -q -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README MANIFEST
%{perl_vendorlib}/Net/*.pm
%{perl_vendorlib}/Net/Daemon/
%{_mandir}/*/*

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 0.37-9avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 0.37-8avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 0.37-7avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.37-6sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 0.37-5sls
- rebuild for new perl

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 0.37-4sls
- OpenSLS build
- tidy spec

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

