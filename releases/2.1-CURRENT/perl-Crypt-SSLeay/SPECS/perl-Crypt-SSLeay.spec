#
# spec file for package perl-Crypt-SSLeay
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Crypt-SSLeay
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.57
%define release		%_revrel

Summary:	Support for the https protocol under LWP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source:		ftp://ftp.cpan.org/pub/CPAN/modules/by-module/Crypt/Crypt-SSLeay-%{version}.tar.gz
Patch0:		perl-Crypt-SSLeay-cryptdef.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	openssl-devel
BuildRequires:	perl(URI)

%description
This perl module provides support for the https protocol under LWP, so
that a LWP::UserAgent can make https GET & HEAD requests.

The Crypt::SSLeay package contains Net::SSL, which is automatically
loaded by LWP::Protocol::https on https requests, and provides the
necessary SSL glue for that module to work via these deprecated modules:

This product includes cryptographic software written by
Eric Young (eay@cryptsoft.com)


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
%patch0 -p1 -b .cryptdef


%build
CFLAGS="%{optflags}" echo | perl Makefile.PL INSTALLDIRS=vendor
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
%{perl_vendorarch}/auto/Crypt
%{perl_vendorarch}/Crypt
%{perl_vendorarch}/Net
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.57
- 0.57
- drop P1, no longer required
- drop P2, merged upstream

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51
- rebuild against new openssl
- spec cleanups

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51
- first Annvix build (needed by perl-HTTP-DAV)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
