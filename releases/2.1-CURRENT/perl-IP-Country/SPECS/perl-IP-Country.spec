#
# spec file for package perl-IP-Country
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#

%define module		IP-Country
%define revision	$Rev$
%define name		perl-%{module}
%define version		2.20
%define release		%_revrel

Summary:	IP::Country modules for Perl 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	http://cpan.uwinnipeg.ca/cpan/authors/id/N/NW/NWETTERS/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(Geography::Countries)
BuildArch:	noarch

Requires:	perl(Geography::Countries)

%description
IP lookup modules for Perl. This package also provides the ip2cc utility, to
lookup country from IP address or hostname.


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


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/IP
%{_mandir}/*/*
%{_bindir}/*

%files doc
%defattr(-,root,root)
%doc CHANGES README


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.20
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Tue Mar 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.20
- spec cleanups

* Sun Mar 12 2006 Ying-Hung Chen <ying-at-annvix.org> 2.20
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
