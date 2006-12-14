# spec file for package perl-IO-Socket-SSL
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		IO-Socket-SSL
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.999
%define release		%_revrel

Summary:	%{module} perl module
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/IO/
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/IO/%{module}-%{version}.tar.gz

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(Net::SSLeay)
BuildArch:	noarch

Requires:	perl(Net::SSLeay) >= 1.08

%description
IO::Socket::SSL is a class implementing an object oriented
interface to SSL sockets. The class is a descendent of
IO::Socket::INET and provides a subset of the base class's
interface methods.


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


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{perl_vendorlib}/IO/Socket/*

%files doc
%defattr(-,root,root)
%doc README Changes util docs certs


%changelog
* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org>  0.999
- 0.999

* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org>  0.97
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy
- BuildRequires: perl(Net::SSLeay)

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.97
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.97
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.97-1avx
- first Annvix build (for new spamassassin)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
