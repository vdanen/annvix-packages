%define module	XML-NamespaceSupport
%define name	perl-%{module}
%define version 1.08
%define release 4sls

Summary:	%{module} module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MPL
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot/
BuildArch:	noarch
BuildRequires:	perl-devel 

Requires:	perl

%description
%{module} module for perl
This module offers a simple to process namespaced XML names
(unames) from within any application that may need them. It
also helps maintain a prefix to namespace URI map, and provides
a number of basic checks.

%prep
%setup -q -n %{module}-%{version}

chmod 644 Changes MANIFEST README

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%files
%defattr(-,root,root)
%doc Changes README
%{perl_vendorlib}/XML/*.pm
%{_mandir}/*/*


%changelog
* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.08-4sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.08-3mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Thu May 22 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.08-2mdk
- rebuild for new autoreq

* Thu Nov 28 2002 François Pons <fpons@mandrakesoft.com> 1.08-1mdk
- 1.08.

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.07-2mdk
- rebuild for perl 5.8.0

* Tue May 28 2002 François Pons <fpons@mandrakesoft.com> 1.07-1mdk
- removed filelist.
- 1.07.

* Wed Jan 30 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.04-2mdk
- Fix changelog

* Tue Jan 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.04-1mdk
- initial RPM
