#
# spec file for package perl-XML-DOM
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		XML-DOM
%define	revision	$Rev$
%define	name		perl-%{module}
%define	version		1.44
%define	release		%_revrel

Summary: 	XML::DOM - build DOM Level 1 compliant document structures
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group: 		Development/Perl
URL: 		http://search.cpan.org/dist/%{module}
Source: 	http://search.cpan.org/CPAN/authors/id/T/TJ/TJMATHER/%{module}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires: 	perl-devel, perl(XML::Parser) >= 2.30, perl(XML::RegExp), perl-libwww-perl
BuildArch:	noarch

%description
This is a Perl extension to XML::Parser. It adds a new 'Style' to
XML::Parser, called 'Dom', that allows XML::Parser to build an Object
Oriented datastructure with a DOM Level 1 compliant interface.
However, there is a new DOM module, XML::GDOME which is under active
development and significantly faster than XML::DOM, since it is based
on the libgdome C library.


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

# get tid of old utf8 stuff
rm -f t/dom_jp_attr.t
rm -f t/dom_jp_cdata.t
rm -f t/dom_jp_example.t
rm -f t/dom_jp_minus.t
rm -f t/dom_jp_modify.t
rm -f t/dom_jp_print.t


%check
# if we want to run make test, we also need perl-libxml-perl >= 0.07
# but i'm sick of adding all these flippin' perl deps
#make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{perl_vendorlib}/XML/DOM
%{perl_vendorlib}/XML/DOM.pm
%{perl_vendorlib}/XML/DOM/*.pod
%{perl_vendorlib}/XML/DOM/*.pm
%{perl_vendorlib}/XML/Handler/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.44
- first Annvix build (needed by perl-HTTP-DAV)
- don't make test as we'd then also need perl-libxml-perl
