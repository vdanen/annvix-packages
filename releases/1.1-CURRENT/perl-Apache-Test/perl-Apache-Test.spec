#
# spec file for package perl-Apache-Test
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define module		Apache-Test
%define name		perl-%{module}
%define version		1.25
%define release		2avx

%define _requires_exceptions perl(Apache2::Const)\\|perl(ModPerl::Config)

Summary:	Apache::Test - Test.pm wrapper with helpers for testing Apache
Name: 		%{name}
Version: 	%{version}
Release:	%{release} 
License:	GPL or Artistic
Group: 		Development/Perl
URL:		http://search.cpan.org/~gozer/Apache-Test/
Source0:	http://search.cpan.org/CPAN/authors/id/G/GO/GOZER/Apache-Test-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel

Requires:	perl-Compress-Zlib, httpd-mod_perl, perl-Module-Build
Provides:	perl(Apache::TestConfigParse)
Provides:	perl(Apache::TestConfigPerl)

%description
Apache::Test is a test toolkit for testing an Apache server with
any configuration. It works with Apache 1.3 and Apache 2.0 and any
of its modules, including mod_perl 1.0 and 2.0. It was originally
developed for testing mod_perl 2.0.


%prep
%setup -q -n %{module}-%{version} 


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS Changes INSTALL LICENSE README SUPPORT ToDo
%{perl_vendorlib}/Apache/*.pm
%{perl_vendorlib}/Bundle/*.pm
%{_mandir}/*/*


%changelog
* Sat Sep 10 2005 Vincent Danen <vdanen@annvix.org> 1.25-2avx
- rebuild against perl 5.8.7
- requires httpd-mod_perl, not apache2-mod_perl

* Wed Sep 07 2005 Vincent Danen <vdanen@annvix.org> 1.25-1avx
- 1.25
- rule out some perl auto-requires

* Thu Aug 11 2005 Vincent Danen <vdanen@annvix.org> 1.20-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 1.20-2avx
- bootstrap build

* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 1.20-1avx
- first Annvix build

* Sat Jan 22 2005 Oden Eriksson <oden.eriksson@linux-mandrake.com> 1.20-1mdk
- 1.20
- drop upstream P0

* Sat Jan 15 2005 Oden Eriksson <oden.eriksson@linux-mandrake.com> 1.19-4mdk
- fix deps

* Sat Jan 15 2005 Oden Eriksson <oden.eriksson@linux-mandrake.com> 1.19-3mdk
- fix deps

* Thu Jan 13 2005 Oden Eriksson <oden.eriksson@linux-mandrake.com> 1.19-2mdk
- added P0 to nuke bad regexp (Stas Bekman)

* Wed Jan 12 2005 Oden Eriksson <oden.eriksson@linux-mandrake.com> 1.19-1mdk
- initial mandrake package
