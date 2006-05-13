#
# spec file for package perl-CIDR-Lite
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$


%define module		Net-CIDR-Lite
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.20
%define release		%_revrel

Summary:	Perl extension for merging IPv4 or IPv6 CIDR addresses
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://search.cpan.org/CPAN/authors/id/D/DO/DOUGW/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

%description
Faster alternative to Net::CIDR when merging a large number of CIDR address
ranges. Works for IPv4 and IPv6 addresses.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%check
make test


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/Net
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc Changes README


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.20
- rebuild against perl 5.8.8
- create -doc subpackage

* Sat Mar 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.20
- first Annvix build

* Wed Mar 01 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.20-1mdk
- New release 0.20

* Thu Feb 09 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.19-1mdk
- New release 0.19
- %%mkrel

* Wed Jun 01 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.18-1mdk
- New release 0.18
- spec cleanup
- make test in %%check

* Mon Dec 20 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.15-2mdk
- fix buildrequires in a backward compatible way

* Sun Nov 14 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.15-1mdk 
- first mdk release
