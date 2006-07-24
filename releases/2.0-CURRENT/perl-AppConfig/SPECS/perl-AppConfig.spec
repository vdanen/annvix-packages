#
# spec file for package perl-AppConfig
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		AppConfig
%define revision	$Rev$
%define name		perl-%{module}
%define	version		1.56
%define release		%_revrel

Summary:  	Perl5 modules for reading configuration
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://www.perl.com/CPAN/authors/id/ABW/
Source:		http://www.perl.com/CPAN/authors/id/ABW/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel

%description
AppConfig has a powerful but easy to use module for parsing configuration
files. It also has a simple and efficient module for parsing command line
arguments.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS=vendor
%make
%{__make} test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root) 
%{perl_vendorlib}/AppConfig/*
%{perl_vendorlib}/AppConfig.pm
%{_mandir}/*/*

%files doc
%doc README


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.56
- really remove the docs from the main package

* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.56
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.56
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.56
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.56-3avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.56-2avx
- bootstrap build (new gcc, new glibc)
- remove %%postun calling ldconfig (what?!?)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.56-1avx
- first Annvix build

* Tue May 04 2004 Michael Scherer <misc@mandrake.org> 1.56-1mdk
- remove unused Tag
- 1.56
- rpmbuildupdate aware
 
* Sat Aug 02 2003 Ben Reser <ben@reser.org> 1.52-7mdk
- Remove Packager tag in package.
- mv rm buildroot to %%install from %%prep
- %%makeinstall_std
- macroize

* Wed Jul 16 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.52-6mdk
- fix buildrequires (Michael Scherer)

* Wed May 28 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.52-5mdk
- fix build
- rebuild for new auto{prov,req}

* Tue Jan 21 2003 Antoine Ginies <aginies@mandrakesoft.com> 1.52-4mdk
- fix requires error

* Fri Oct 18 2002 Clic-dev <clic-dev-public@mandrakesoft.com> 1.52-3mdk
- build with perl 5.8
- add perl version define

* Thu Jul 11 2002 Antoine Ginies <aginies@mandrakesoft.com> 1.52-2mdk
- Build on 8.2 with perl 5.6

* Thu Apr 4 2002 Antoine Ginies <aginies@mandrakesoft.com> 1.52-1mdk
- first release for Mandrakesoft
