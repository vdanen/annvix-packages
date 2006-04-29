#
# spec file for package perl-MDV-Distribconf
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		perl-%{module}
%define module		MDV-Distribconf
%define version		1.01
%define release		%_revrel

Summary:	Read and write config of a Mandriva Linux distribution tree
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{dist}/
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl perl-Config-IniFiles


%description
MDV::Distribconf is a module to get/write the configuration of a Mandriva Linux
or urpmi-using distribution tree.


%prep
%setup -q -n %{module}-%{version}


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
%doc ChangeLog
%{_mandir}/*/*
%{perl_vendorlib}/MDV/Distribconf
%{perl_vendorlib}/MDV/Distribconf.pm


%changelog
* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.01
- first Annvix build

* Tue Dec 06 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.01-1mdk
- 1.01

* Fri Oct 28 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.00-1mdk
- Initial MDV release
