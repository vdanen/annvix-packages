#
# spec file for package perl-Geography-Countries
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$


%define module		Geography-Countries
%define revision    $Rev$
%define name        perl-%{module}
%define version     1.4
%define release     %_revrel

Summary:	Maps 2-letter, 3-letter, and numerical codes for countries
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
Source:		http://search.cpan.org/CPAN/authors/id/A/AB/ABIGAIL/%{module}-%{version}.tar.bz2
Url:		http://search.cpan.org/dist/%{module}/
BuildRequires:	perl-devel
BuildArch:	noarch
BuildRoot:  %{_buildroot}/%{name}-%{version}

%description
This module maps country names, and their 2-letter, 3-letter and
numerical codes, as defined by the ISO-3166 maintenance agency,
and defined by the UNSD.

%prep
%setup -q -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make

%check
%{__make} test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{perl_vendorlib}/Geography
%{_mandir}/*/*

%changelog
* Sun Mar 12 2006 Ying-Hung Chen <ying@annvix.org> 1.4
- first Annvix Build

* Mon Jan 23 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.4-3mdk
- spe cleanup
- rpmbuildupdate aware
- %%mkrel
- enable tests
- better URL

* Fri Jan 21 2005 Abel Cheung <deaddog@mandrake.org> 1.4-2mdk
- rebuild

* Sun Dec 14 2003 Abel Cheung <deaddog@deaddog.org> 1.4-1mdk
- First Mandrake package
