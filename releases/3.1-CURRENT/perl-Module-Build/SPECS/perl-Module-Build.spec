#
# spec file for package perl-Module-Build
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Module-Build
%define	revision	$Rev$
%define	name		perl-%{module}
%define version 	0.2805
%define release 	%_revrel

Summary:	Build and install Perl modules
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/Module/%{module}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

BuildRequires:	perl-devel
BuildRequires:	perl(YAML)

%description
Module::Build is a system for building, testing, and installing Perl modules.
It is meant to be a replacement for ExtUtils::MakeMaker. Developers may alter
the behavior of the module through subclassing in a much more straightforward
way than with MakeMaker. It also does not require a make on your system - most
of the Module::Build code is pure-perl and written in a very cross-platform
way. In fact, you don't even need a shell, so even platforms like MacOS
(traditional) can use it fairly easily. Its only prerequisites are modules that
are included with perl 5.6.0, and it works fine on perl 5.005 if you can
install a few additional modules.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
perl Build.PL installdirs=vendor
./Build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
./Build install destdir=%{buildroot}


%check
./Build test


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%{_bindir}/config_data
%{perl_vendorlib}/Module
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc Changes INSTALL README


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.2805
- rebuild

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2805
- 0.2805

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2801
- 0.2801

* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2612
- 0.2612
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2611
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2611
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2611-1avx
- 0.2611
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2608-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2608-2avx
- bootstrap build

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2608-1avx
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
