%define	name	perl-IO-Tty
%define	module	IO-Tty
%define	version	1.02
%define	release	7mdk

Summary:	IO-Tty perl module: interface to pseudo tty's
Name: 		%{name}
Version: 	%{version}
Release:	%{release} 
License: 	GPL
Group: 		Development/Perl
Url:		http://www.cpan.org
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/IO/%{module}-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires:	perl-devel
Requires: 	perl 

%description
The IO::Tty and IO::Pty modules provide an interface to pseudo tty's.


%prep
%setup -q -n %{module}-%{version}

%build

CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
%make
make test

%install
%makeinstall_std

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%dir %{perl_vendorlib}/%{_arch}-linux-thread-multi/auto/IO/Tty
%{perl_vendorlib}/%{_arch}-linux-thread-multi/auto/IO/Tty/*
%{perl_vendorlib}/%{_arch}-linux-thread-multi/IO/*.pm
%dir %{perl_vendorlib}/%{_arch}-linux-thread-multi/IO/Tty
%{perl_vendorlib}/%{_arch}-linux-thread-multi/IO/Tty/*
%{_mandir}/*/*

%changelog
* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.02-7mdk
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
