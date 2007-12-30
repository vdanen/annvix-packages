#
# spec file for package perl-File-Tail
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		File-Tail
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.99.1
%define release		%_revrel

Summary:	File::Tail module for Perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{module}/
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel
BuildRequires:	perl(Time::HiRes)

%description
This Perl modules allows to read from continously updated files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/File
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.99.1        
- rebuild

* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.1
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.1
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.99.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.99.1-1avx
- first Annvix build (required by swatch)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
