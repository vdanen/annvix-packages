#
# spec file for package perl-IO-Compress-Zlib
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		IO-Compress-Zlib
%define	revision	$Rev$
%define	name		perl-%{module}
%define	version		2.008
%define	release		%_revrel

Summary:	Perl interface to allow reading and writing gzip and zip files/buffers
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/IO-Compress-Zlib-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(Compress::Raw::Zlib) >= %{version}
BuildRequires:	perl(IO::Compress::Base) >= %{version}
BuildArch:	noarch

%description
A Perl interface to allow reading and writing of RFC 1950, 1951, 1952
(i.e. gzip) and zip files/buffers.


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
%{perl_vendorlib}/*

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.008
- 2.008

* Mon Jul 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.005
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
