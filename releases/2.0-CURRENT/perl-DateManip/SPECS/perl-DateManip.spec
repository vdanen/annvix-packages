#
# spec file for package perl-DateManip
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		DateManip
%define revision	$Rev$
%define name		perl-%{module}
%define	version		5.44
%define	release		%_revrel

Summary: 	%{module} module for perl
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/Date/%{module}-%{version}.tar.bz2
Patch0:		DateManip-COT.patch
Patch1:		DateManip-SORT.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}-buildroot
BuildRequires:	perl-devel
BuildArch:	noarch

%description
This is a set of routines designed to make any common date/time
manipulation easy to do. Operations such as comparing two times,
calculating a time a given amount of time from another, or parsing
international times are all easily done.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
%patch0 -p1 -b .cot
%patch1 -p0 -b .sort


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
%defattr(-,root,root,755)
%{_mandir}/man3/*
%{perl_vendorlib}/Date

%files doc
%defattr(-,root,root)
%doc README HISTORY INSTALL TODO


%changelog
* Thu May 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.44
- first Annvix package (needed by swatch)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
