#
# spec file for package perl-Mail-SPF-Query
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$


%define module		Mail-SPF-Query
%define revision	$Rev$
%define name		perl-%{module}
%define version		1.999.1
%define release		%_revrel

Summary:	Query Sender Policy Framework for an IP,email,helo 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source:		http://search.cpan.org/CPAN/authors/id/J/JM/JMEHNLE/mail-spf-query/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl(Net::CIDR::Lite)
BuildRequires:	perl(Net::DNS)
BuildRequires:  perl(URI)
BuildRequires:  perl(Sys::Hostname::Long)
BuildArch:	noarch

%description
The SPF protocol relies on sender domains to describe their designated outbound
mailers in DNS. Given an email address, Mail::SPF::Query determines the
legitimacy of an SMTP client IP.


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
%{perl_vendorlib}/Mail
%{_mandir}/*/*
%{_bindir}/*

%files doc
%defattr(-,root,root)
%doc CHANGES README


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.999.1
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Sat Mar 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.999.1
- first Annvix build

* Wed Mar 01 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.999.1-1mdk
- New release 1.999.1

* Fri Jan 20 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.998-2mdk
- fix buildrequires

* Tue Jan 03 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.998-1mdk
- New release 1.998
- fix sources URL

* Thu Sep 29 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.997-3mdk
- fix buildrequires

* Mon Dec 20 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.997-2mdk
- fix buildrequires in a backward compatible way

* Sun Nov 14 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.997-1mdk 
- first mdk release
