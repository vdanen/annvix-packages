#
# spec file for package perl-XML-SAX
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		XML-SAX
%define revision	$Rev$
%define name		perl-%{module}
%define version 	0.12
%define release 	%_revrel

Summary:	%{module} module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2
Patch:		%{name}-0.05-build.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel
BuildRequires:	perl(XML::NamespaceSupport)

Requires:	perl
Provides:	perl(XML::SAX::PurePerl::DTDDecls)
Provides:	perl(XML::SAX::PurePerl::DocType)
Provides:	perl(XML::SAX::PurePerl::EncodingDetect)
Provides:	perl(XML::SAX::PurePerl::XMLDecl)

%description
%{module} module for perl
XML::SAX consists of several framework classes for using and building
Perl SAX2 XML parsers, filters, and drivers. It is designed around the
need to be able to "plug in" different SAX parsers to an application
without requiring programmer intervention. Those of you familiar with
the DBI will be right at home. Some of the designs come from the Java
JAXP specification (SAX part), only without the javaness.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
%patch -p0

chmod 0644 Changes README


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
%{perl_vendorlib}/XML
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc Changes README


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.12
- rebuild

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.12
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.12
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-11avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-9avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-8avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.12-7avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.12-6sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 0.12-5sls
- rebuild for new perl
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 0.12-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
