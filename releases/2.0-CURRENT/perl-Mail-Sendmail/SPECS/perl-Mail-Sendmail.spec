#
# spec file for package perl-Mail-Sendmail
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Mail-Sendmail
%define revision	$Rev$
%define name		perl-%{module}
%define	version		0.79
%define	release		%_revrel

Summary: 	Simple platform-independent mailer
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://www.cpan.org/authors/id/M/MI/MIVKOVIC/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}-buildroot
BuildRequires:	perl-devel
BuildArch:	noarch

%description
Mail::Sendmail is a Perl module for sending mail through a sendmail SMTP
server.


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
%defattr(-,root,root,755)
%{_mandir}/man3/*
%{perl_vendorlib}/Mail

%files doc
%defattr(-,root,root)
%doc Changes README Todo


%changelog
* Thu May 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.79
- first Annvix package (needed by swatch)
