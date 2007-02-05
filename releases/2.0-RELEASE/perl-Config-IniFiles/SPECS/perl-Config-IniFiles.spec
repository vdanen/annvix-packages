#
# spec file for package perl-Config-IniFiles
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Config-IniFiles
%define revision	$Rev$
%define name		perl-%{module}
%define version		2.39
%define release		%_revrel

Summary:	Config-IniFiles module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License: 	GPL
Group: 		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source: 	Config-IniFiles-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires: 	perl-devel >= 5.8.0

%description
This perl module allows you to access to config files written in the 
.ini style. 


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
chmod 0644 README IniFiles.pm
perl Makefile.PL INSTALLDIRS=vendor
%make


%check
%make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/Config
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README


%changelog
* Wed May 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.39
- 2.39
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.38
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.38
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.38-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.38-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.38-2avx
- bootstrap build

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.38-1avx
- first Annvix build, for rpmtools

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
