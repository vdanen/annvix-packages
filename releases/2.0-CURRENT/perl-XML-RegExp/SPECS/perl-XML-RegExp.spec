#
# spec file for package perl-XML-RegExp
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		XML-RegExp
%define	revision	$Rev$
%define	name		perl-%{module}
%define	version		0.03
%define	release		%_revrel

Summary: 	XML::RegExp - regular expressions for XML tokens
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group: 		Development/Perl
URL: 		http://search.cpan.org/dist/%{module}
Source: 	http://search.cpan.org/CPAN/authors/id/T/TJ/TJMATHER/%{module}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires: 	perl-devel
BuildArch:	noarch

%description
This package contains regular expressions for the following XML
tokens: BaseChar, Ideographic, Letter, Digit, Extender, CombiningChar,
NameChar, EntityRef, CharRef, Reference, Name, NmToken, and AttValue.


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
%{perl_vendorlib}/XML/RegExp.pm
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.03
- first Annvix build (needed by perl-XML-DOM)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
