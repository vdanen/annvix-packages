%define name	perl-HTML-Tagset
%define	module	HTML-Tagset
%define	version	3.03
%define	release	7mdk

Summary: 	This module contains data tables useful in dealing with HTML.
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Development/Perl
Source:		http://www.cpan.org/authors/id/S/SB/SBURKE/%{module}-%{version}.tar.bz2
URL:		http://www.cpan.org
BuildArch:	noarch
BuildRequires:	perl-devel
BuildRoot: 	%{_tmppath}/%{name}-buildroot/
Requires: 	perl

%description
This module contains data tables useful in dealing with HTML.

It provides no functions or methods.

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
%doc README ChangeLog
%{_mandir}/*/*
%{perl_vendorlib}/HTML

%changelog
* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.03-7mdk
- rebuild against new perl
- drop Prefix tag
- drop $RPM_OPT_FLAGS, noarch..
- don't use PREFIX
- use %%makeinstall_std macro
- drop %%real_name macro, use the already existing %%module macro in stead

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.03-6mdk
- rebuild for new auto{prov,req}

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 3.03-5mdk
- rebuild for perl 5.8.0

* Tue Mar 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.03-4mdk
- should be noarch

* Mon Nov 12 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.03-3mdk
- Remove Distribution Tag.
- Fix no-url-tag and invalid-packager warnings.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 3.03-2mdk
- BuildRequires: perl-devel

* Wed Jun 20 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.03-1mdk
- First Mandrake Release.
