#
# spec file for package perl-IO-Tty
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define	module		IO-Tty
%define	name		perl-%{module}
%define	version		1.02
%define	release		16avx

Summary:	IO-Tty perl module: interface to pseudo tty's
Name: 		%{name}
Version: 	%{version}
Release:	%{release} 
License: 	GPL
Group: 		Development/Perl
URL:		http://www.cpan.org
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/IO/%{module}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel

Requires: 	perl 

%description
The IO::Tty and IO::Pty modules provide an interface to pseudo tty's.


%prep
%setup -q -n %{module}-%{version}


%build
CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS=vendor
%make
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%doc ChangeLog README
%dir %{perl_vendorarch}/auto/IO/Tty
%{perl_vendorarch}/auto/IO/Tty/*
%{perl_vendorarch}/IO/*.pm
%dir %{perl_vendorarch}/IO/Tty
%{perl_vendorarch}/IO/Tty/*
%{_mandir}/*/*


%changelog
* Sat Sep 10 2005 Vincent Danen <vdanen@annvix.org> 1.02-16avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen@annvix.org> 1.02-15avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 1.02-14avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 1.02-13avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 1.02-12avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.02-11sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 1.02-10sls
- rebuild for new perl
- minor spec cleanups

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 1.02-9sls
- sync with 8mdk (gbeauchesne): fix build on amd64

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.02-8sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.02-7mdk
- rebuild for new perl
- use %%make macro
- use %%makeinstall_std macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.02-6mdk
- rebuild for new auto{prov,req}

* Tue Apr 22 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.02-5mdk
- fix buildrequires

* Tue Jan 28 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.02-4mdk
- better summary & description
- remove non existent doc

* Tue Aug  6 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.02-3mdk
- rebuild with new threaded perl

* Mon Jul 29 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.02-2mdk
- not all arches use i386-linux

* Wed Jul 24 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.02-1mdk
- 1.02

* Wed Jul 24 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.05-3mdk
- fix files section

* Wed Jul 24 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.05-2mdk
- rebuild with new perl

* Fri Mar 01 2002  Lenny Cartier <lenny@mandrakesoft.com> 0.05-1mdk
- 0.05

* Mon Sep 24 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.04-1mdk
- added by Max Heijndijk <cchq@wanadoo.nl> :
	- Initial wrap
