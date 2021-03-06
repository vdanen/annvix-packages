#
# spec file for package perl-Carp-Clan
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define	module		Carp-Clan
%define name		perl-%{module}
%define	version		5.3
%define	release		1avx
%define	pdir		Carp

Summary: 	%{module} module for perl
Name: 		perl-%{module}
Version: 	%{version}
Release:	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/%{pdir}/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
%{module} module for perl.
This module reports errors from the perspective of the caller of a
"clan" of modules, similar to "Carp.pm" itself. But instead of giving
it a number of levels to skip on the calling stack, you give it a
pattern to characterize the package names of the "clan" of modules
which shall never be blamed for any error.


%prep
%setup -q -n %{module}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make


%check
LANG=C %make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%doc CHANGES.txt README.txt
%{_mandir}/man3/Carp::Clan*
%dir %{perl_vendorlib}/Carp
%{perl_vendorlib}/Carp/Clan*


%changelog
* Sat Sep 24 2005 Vincent Danen <vdanen@annvix.org> 5.3-1avx
- first build for Annvix (needed by perl-Bit-Vector)

* Sat Jun 04 2005 Luca Berra <bluca@vodka.it> 5.3-2mdk 
- rebuild

* Wed May 05 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 5.3-1mdk
- 5.3

* Wed Apr 21 2004 Per ?yvind Karlsen <peroyvind@linux-mandrake.com> 5.2-1mdk
- 5.2
- drop $RPM_OPT_FLAGS, noarch..

* Thu Feb 12 2004 Luca Berra <bluca@vodka.it> 5.1-3mdk
- rebuild for perl 5.8.3

* Tue Dec 30 2003 Luca Berra <bluca@vodka.it> 5.1-2mdk
- add parent dirs (distriblint)

* Sun Oct 05 2003 Luca Berra <bluca@vodka.it> 5.1-1mdk
- Initial build.
