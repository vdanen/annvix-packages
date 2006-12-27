#
# spec file for package perl-libwww-perl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		libwww-perl
%define revision	$Rev$
%define name		perl-%{module}
%define version 	5.803
%define release 	%_revrel

%define _requires_exceptions Authen::NTLM\\|HTTP::GHTTP\\|Win32

Summary:	Libwww-perl module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel
BuildRequires:	rpm-build >= 4.2-7mdk
BuildRequires:	perl(HTML::Parser)
BuildRequires:	perl(URI)

Requires:	perl(HTML::Parser)
Requires:	perl(URI) >= 1.10
Requires:	perl(MIME::Base64)
Requires:	perl(Digest::MD5)


%description
libwww-perl module for perl.


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
%{_bindir}/*
%{_mandir}/*/*
%{perl_vendorlib}/LWP.pm
%{perl_vendorlib}/*.pod
%{perl_vendorlib}/Net
%{perl_vendorlib}/File
%{perl_vendorlib}/HTML
%{perl_vendorlib}/WWW
%{perl_vendorlib}/HTTP
%{perl_vendorlib}/Bundle
%{perl_vendorlib}/LWP

%files doc
%defattr(-,root,root)
%doc README README.SSL Changes


%changelog
* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.803
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.803
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.803
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.803-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.803-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.803-2avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.803-1avx
- 5.803
- restore installation of GET, HEAD, and POST in /usr/bin (rgarciasuarez)

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.79-3avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.79-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 5.79-1sls
- 5.79
- remove P0; merged upstream
- minor spec cleanups

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 5.69-4sls
- rebuild for new perl
- remove %%{prefix} tag

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 5.69-3sls
- OpenSLS build
- tidy spec
- comment out make test for the time being

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
