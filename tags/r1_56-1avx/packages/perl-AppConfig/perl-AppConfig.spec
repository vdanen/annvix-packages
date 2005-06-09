%define module	AppConfig
%define name	perl-%{module}
%define	version	1.56
%define release	1avx

Summary:  	Perl5 modules for reading configuration
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://www.perl.com/CPAN/authors/id/ABW/
Source:		http://www.perl.com/CPAN/authors/id/ABW/%{module}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel

%description
AppConfig has a powerful but easy to use module for parsing configuration
files. It also has a simple and efficient module for parsing command line
arguments.

%prep
%setup -q -n %{module}-%{version}

%build
CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS=vendor
%make
%{__make} test

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

%clean
%{__rm} -fr %{buildroot}

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root) 
%doc README
%{perl_vendorlib}/AppConfig/*
%{perl_vendorlib}/AppConfig.pm
%{_mandir}/*/*

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 1.56-1avx
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
