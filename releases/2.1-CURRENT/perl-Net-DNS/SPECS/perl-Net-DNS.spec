#
# spec file for package perl-Net-DNS
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Net-DNS
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.60
%define release		%_revrel

Summary:	Perl interface to the DNS resolver
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source0:	http://search.cpan.org/CPAN/authors/id/O/OL/OLAF/%{module}-%{version}.tar.gz

BuildRequires:	perl-devel
BuildRequires:	perl(Digest::HMAC)
BuildRequires:	perl(Net::IP)

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Net::DNS is a collection of Perl modules that act as a Domain Name System (DNS)
resolver. It allows the programmer to perform DNS queries that are beyond the
capabilities of gethostbyname and gethostbyaddr.

The programmer should be somewhat familiar with the format of a DNS packet and
its various sections. See RFC 1035 or DNS and BIND (Albitz & Liu) for details.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version} 


%build
perl Makefile.PL INSTALLDIRS=vendor </dev/null
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
%{perl_vendorarch}/auto/Net
%{perl_vendorarch}/Net

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Tue Jul 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.60
- 0.60 (fixes CVE-2007-3409 and CVE-2007-3377)

* Wed Nov 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.59
- 0.59

* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.57
- 0.57
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy
- redirect from /dev/null rather than using yes

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.53
- use yes to enable tests or the Makefile will stall waiting for input
  and mess up any rebuilding scripts

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.53
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.53
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.53
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.53-1avx
- first build for Annvix (required by spamd)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
