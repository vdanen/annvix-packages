#
# spec file for package perl-Expect
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Expect
%define revision	$Rev$
%define name		perl-%{module}
%define version 	1.17
%define release 	%_revrel

Summary:	Expect perl module
Name: 		%{name}
Version: 	%{version}
Release:	%{release} 
License: 	GPL
Group: 		Development/Perl
URL:		http://www.cpan.org
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/Expect/Expect-%{version}.tar.gz
Patch0:		%{name}-paths.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl(IO::Tty) >= 1.03
BuildRequires:	perl-devel

Requires: 	perl
Requires:	perl(IO::Tty) >= 1.03


%description
Expect perl module.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
%patch -p1


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
%defattr(644,root,root,755)
%{perl_vendorlib}/*.pm
%{perl_vendorlib}/*.pod
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc Changes README examples tutorial


%changelog
* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.17
- 1.17

* Thu May 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-14avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-13avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-12avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-11avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.15-10avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.15-9sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 1.15-8sls
- rebuild for new perl
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.15-7sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
