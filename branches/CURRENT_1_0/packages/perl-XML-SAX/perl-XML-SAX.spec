%define module	XML-SAX
%define name	perl-%{module}
%define version 0.12
%define release 6sls

Summary:	%{module} module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2
Patch:		%{name}-0.05-build.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot/
BuildArch:	noarch
BuildRequires:	perl-devel perl-XML-NamespaceSupport

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

%prep
%setup -q -n %{module}-%{version}
%patch -p0

chmod 644 Changes README

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changes MANIFEST README
%{perl_vendorlib}/XML
%{_mandir}/*/*

%changelog
* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.12-6sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 0.12-5sls
- rebuild for new perl
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 0.12-4sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.12-3mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Thu May 22 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.12-2mdk
- rebuild for new autoreq
- fix provides

* Thu Nov 28 2002 François Pons <fpons@mandrakesoft.com> 0.12-1mdk
- 0.12.

* Tue Nov  5 2002 Pixel <pixel@mandrakesoft.com> 0.11-1mdk
- fix license
- new release

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 0.10-2mdk
- rebuild for perl 5.8.0
- cleanup

* Tue Mar 26 2002 François Pons <fpons@mandrakesoft.com> 0.10-1mdk
- removed filelist.
- 0.10.

* Tue Jan 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.05-1mdk
- initial RPM
- include patch for building.
