#
# spec file for package perl-MDV-Packdrakeng
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
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
BuildRequires:	perl(Compress::Zlib)


%description
MDV::Packdrakeng is a simple indexed archive builder and extractor using
standard compression methods.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


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
%{_mandir}/*/*
%{perl_vendorlib}/MDV/Packdrakeng
%{perl_vendorlib}/MDV/Packdrakeng.pm

%files doc
%defattr(-,root,root)
%doc ChangeLog README


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.01
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.01
- first Annvix build

* Wed Feb 15 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.01-2mdk
- Rebuild; use mkrel (misc)

* Fri Nov 04 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.01-1mdk
- 1.01

* Fri Oct 28 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.00-1mdk
- Initial MDV release

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
