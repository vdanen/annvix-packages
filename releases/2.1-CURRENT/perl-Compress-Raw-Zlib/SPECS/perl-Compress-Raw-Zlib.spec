#
# spec file for package perl-Compress-Raw-Zlib
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Compress-Raw-Zlib
%define	revision	$Rev$
%define	name		perl-%{module}
%define	version		2.005
%define	release		%_revrel

Summary:	Low-level interface to the zlib compression library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/%{module}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	zlib-devel

%description
Low-level interface to the zlib compression library.


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
%{_mandir}/*/*
%{perl_vendorarch}/Compress
%{perl_vendorarch}/auto/Compress

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Mon Jul 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.005
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
