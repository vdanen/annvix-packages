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
%define version		3.06
%define release		%_revrel

Summary:	Read and write config of a Mandriva Linux distribution tree
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{dist}/
Source0:	%{module}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl
BuildRequires:	perl(Config::IniFiles)


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
%{_bindir}/checkdistrib
%{_mandir}/*/*
%{perl_vendorlib}/MDV/Distribconf
%{perl_vendorlib}/MDV/Distribconf.pm


%changelog
* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.06
- 3.06

* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.01
- rebuild against perl 5.8.8
- drop the docs (was just the changelog)

* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.01
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
