#
# spec file for package perl-Sys-Hostname-Long
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id: perl-YAML.spec 5248 2006-02-28 05:12:35Z vdanen $


%define module		Sys-Hostname-Long
%define revision	$Rev: 5248 $
%define name		perl-%{module}
%define version		1.4
%define	release		%_revrel

Summary:	Try every conceivable way to get full hostname
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	%{module}-%{version}.tar.bz2
Patch0:		Sys-Hostname-Long-1.4-no_win32.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
How to get the host full name in perl on multiple operating systems.


%prep
%setup -q -n %{module}-%{version}
%patch0 -p0


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
%doc Changes README
%{perl_vendorlib}/Sys/Hostname/*
%{_mandir}/*/*


%changelog
* Sat Mar 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4
- first Annvix build

* Mon Oct 17 2005 Oden Eriksson <oeriksson@mandriva.com> 1.4-2mdk
- remove win32 calls

* Mon Oct 17 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.4-1mdk
- Initial Mandriva release.
