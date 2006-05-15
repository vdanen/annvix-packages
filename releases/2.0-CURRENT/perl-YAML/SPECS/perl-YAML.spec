#
# spec file for package perl-YAML
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		YAML
%define revision	$Rev$
%define name		perl-%{module}
%define version 	0.58
%define release 	%_revrel

Summary:	YAML Ain't Markup Language (tm)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://search.cpan.org/CPAN/authors/id/I/IN/INGY/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel

%description
The YAML.pm module implements a YAML Loader and Dumper based on the YAML 1.0
specification. http://www.yaml.org/spec/

YAML is a generic data serialization language that is optimized for human
readability. It can be used to express the data structures of most modern
programming languages. (Including Perl!!!)

For information on the YAML syntax, please refer to the YAML specification.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor <<EOF
EOF
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
%{_bindir}/*
%{perl_vendorlib}/YAML*
%{perl_vendorlib}/Test/YAML*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc Changes README


%changelog
* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.58
- 0.58
- rebuild against perl 5.8.8
- create -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.39
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.39
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.39-1avx
- 0.39
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.36-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.36-2avx
- bootstrap build

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.36-1avx
- first Annvix build

* Mon Jan 31 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.36-1mdk
- 0.36
- add tests

* Mon Dec 20 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.35-3mdk
- fix buildrequires in a backward compatible way

* Fri Jul 23 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.35-2mdk 
- rpmbuildupdate aware

* Fri Dec 05 2003 Guillaume Rousse <guillomovitch@mandrake.org> 0.35-1mdk
- first mdk release
