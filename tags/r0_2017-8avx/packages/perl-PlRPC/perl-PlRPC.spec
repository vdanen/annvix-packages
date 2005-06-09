%define module 	PlRPC
%define name	perl-%{module}
%define version 0.2017
%define release 8avx

Summary:	%{module} perl module
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		ftp://ftp.funet.fi/pub/languages/perl/CPAN/authors/id/JWIED
Source0:	%{module}-%{version}.tar.bz2

BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	perl-Net-Daemon perl-devel
Buildarch:	noarch

%description
%{module} - module for perl

%prep
%setup -q -n %{module}-%{version}

%build

%{__perl} Makefile.PL INSTALLDIRS=vendor --defaultdeps
%{__make}

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README MANIFEST ChangeLog 
%{perl_vendorlib}/Bundle/*
%{perl_vendorlib}/RPC/*
%_mandir/man3*/*

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 0.2017-8avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen@annvix.org> 0.2017-7avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 0.2017-6avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.2017-5sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 0.2017-4sls
- rebuild for new perl

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 0.2017-3sls
- OpenSLS build
- tidy spec
- remove redundant perl-Storable BuildReq (part of perl)

* Thu Aug 14 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 0.2017-2mdk
- rebuild for new perl
- drop PREFIX
- use %%makeinstall_std macro

* Mon Jun 30 2003 Fran�ois Pons <fpons@mandrakesoft.com> 0.2017-1mdk
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

