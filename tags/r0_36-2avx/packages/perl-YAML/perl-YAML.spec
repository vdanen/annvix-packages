%define module	YAML
%define name	perl-%{module}
%define version 0.36
%define release 2avx

Summary:	YAML Ain't Markup Language (tm)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://search.cpan.org/CPAN/authors/id/I/IN/INGY/%{module}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot/
BuildArch:	noarch
BuildRequires:	perl-devel

%description
The YAML.pm module implements a YAML Loader and Dumper based on the YAML 1.0
specification. http://www.yaml.org/spec/

YAML is a generic data serialization language that is optimized for human
readability. It can be used to express the data structures of most modern
programming languages. (Including Perl!!!)

For information on the YAML syntax, please refer to the YAML specification.

%prep
%setup -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor <<EOF
EOF
%make
make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc Changes README
%{_bindir}/*
%{perl_vendorlib}/YAML*
%{_mandir}/*/*

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 0.36-2avx
- bootstrap build

* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 0.36-1avx
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
