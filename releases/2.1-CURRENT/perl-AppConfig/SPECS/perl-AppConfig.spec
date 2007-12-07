#
# spec file for package perl-AppConfig
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		AppConfig
%define revision	$Rev$
%define name		perl-%{module}
%define	version		1.63
%define release		%_revrel

Summary:  	Perl5 modules for reading configuration
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://www.perl.com/CPAN/authors/id/ABW/
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/AppConfig/%{module}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel
BuildRequires:	perl(File::HomeDir)

%description
AppConfig has a powerful but easy to use module for parsing configuration
files. It also has a simple and efficient module for parsing command line
arguments.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root) 
%{perl_vendorlib}/AppConfig
%{perl_vendorlib}/AppConfig.pm
%{_mandir}/*/*

%files doc
%doc README


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.63
- rebuild

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.63
- 1.63

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.56
- really remove the docs from the main package

* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.56
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.56
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.56
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.56-3avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.56-2avx
- bootstrap build (new gcc, new glibc)
- remove %%postun calling ldconfig (what?!?)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.56-1avx
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
