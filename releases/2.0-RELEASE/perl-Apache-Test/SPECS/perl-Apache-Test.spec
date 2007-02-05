#
# spec file for package perl-Apache-Test
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Apache-Test
%define revision	$Rev$
%define name		perl-%{module}
%define version		1.29
%define release		%_revrel

%define _requires_exceptions perl(Apache2::Const)\\|perl(ModPerl::Config)

Summary:	Apache::Test - Test.pm wrapper with helpers for testing Apache
Name: 		%{name}
Version: 	%{version}
Release:	%{release} 
License:	GPL or Artistic
Group: 		Development/Perl
URL:		http://search.cpan.org/~gozer/Apache-Test/
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/Apache/Apache-Test-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel

Requires:	httpd-mod_perl
Requires:	perl(Compress::Zlib)
Requires:	perl(Module::Build)
Provides:	perl(Apache::TestConfigParse)
Provides:	perl(Apache::TestConfigPerl)

%description
Apache::Test is a test toolkit for testing an Apache server with
any configuration. It works with Apache 1.3 and Apache 2.0 and any
of its modules, including mod_perl 1.0 and 2.0. It was originally
developed for testing mod_perl 2.0.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


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
%{perl_vendorlib}/Apache/*.pm
%{perl_vendorlib}/Bundle/*.pm
%{_mandir}/*/*

%files doc
%doc CONTRIBUTORS Changes INSTALL LICENSE README SUPPORT ToDo


%changelog
* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.29
- 1.29

* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.28
- 1.28
- perl policy
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.25
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-2avx
- rebuild against perl 5.8.7
- requires httpd-mod_perl, not apache2-mod_perl

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-1avx
- 1.25
- rule out some perl auto-requires

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.20-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.20-2avx
- bootstrap build

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.20-1avx
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
