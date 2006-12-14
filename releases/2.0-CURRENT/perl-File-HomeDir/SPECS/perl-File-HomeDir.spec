#
# spec file for package perl-File-Homedir
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id: perl-AppConfig.spec 6158 2006-09-10 00:05:46Z vdanen $

%define module		File-HomeDir
%define revision	$Rev: 6158 $
%define name		perl-%{module}
%define	version		0.58
%define release		%_revrel

Summary:  	Get home directory for self or other users
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://www.cpan.org/modules/by-module/File/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel

%description
A Perl module to get home directory portably for self or other users.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
find lib -name *.pm | xargs chmod 0644
chmod 0644 Changes


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
%{perl_vendorlib}/File
%{_mandir}/*/*

%files doc
%doc README Changes


%changelog
* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.58
- first Annvix build (needed by perl-AppConfig)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
