#
# spec file for package perl-MDV-Packdrakeng
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id: perl-DB_File.spec 5113 2006-01-12 19:01:07Z vdanen $

%define revision	$Rev: 5113 $
%define name		perl-%{module}
%define module		MDV-Packdrakeng
%define version		1.01
%define release		%_revrel

%define _requires_exceptions perl(Compress::Zlib)

Summary:	Simple Archive Extractor/Builder
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/soft/perl-%{module}/
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-Compress-Zlib


%description
MDV::Packdrakeng is a simple indexed archive builder and extractor using
standard compression methods.


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
%doc ChangeLog README
%{_mandir}/*/*
%{perl_vendorlib}/MDV/Packdrakeng
%{perl_vendorlib}/MDV/Packdrakeng.pm


%changelog
* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.01
- first Annvix build

* Wed Feb 15 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.01-2mdk
- Rebuild; use mkrel (misc)

* Fri Nov 04 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.01-1mdk
- 1.01

* Fri Oct 28 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.00-1mdk
- Initial MDV release
