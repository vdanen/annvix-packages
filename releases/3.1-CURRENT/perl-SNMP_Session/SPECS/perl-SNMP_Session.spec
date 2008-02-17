#
# spec file for package perl-SNMP_Session
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		SNMP_Session
%define revision	$Rev$
%define name		perl-%{module}
%define	version		1.11
%define	release		%_revrel

Summary: 	SNMP support for Perl
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
License: 	Artistic
Group:		Development/Perl
URL:		http://www.switch.ch/misc/leinen/snmp/perl/
Source:		http://www.switch.ch/misc/leinen/snmp/perl/dist/SNMP_Session-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
Pure Perl SNMP v1 and SNMP v2 support for Perl 5.

The SNMP operations currently supported are "get", "get-next", "get-bulk"
and "set", as well as trap generation and reception.


%prep
%setup -q -n %{module}-%{version}
perl -pi -e 's|^#!/usr/local/bin/perl\b|#!/usr/bin/perl|' test/*


%build
perl Makefile.PL INSTALLDIRS=vendor
make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod 0644 %{buildroot}/%{perl_vendorlib}/*.pm


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/*.pm


%changelog
* Sun Feb 17 2008 Vincent Danen <vdanen-at-build.annvix.org> 1.11
- first Annvix build for mrtg-contribs

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
