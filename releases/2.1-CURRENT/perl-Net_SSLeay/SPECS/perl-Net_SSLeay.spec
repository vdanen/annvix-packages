#
# spec file for package perl-Net_SSLeay
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Net_SSLeay
%define revision	$Rev$
%define name 		perl-%{module}
%define version		1.30
%define release		%_revrel

Summary:        Net::SSLeay (module for perl)
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	BSD-like
Group: 		Development/Perl
URL: 		http://search.cpan.org/dist/%{module}
Source: 	http://www.cpan.org/modules/by-module/Net/%{module}.pm-%{version}.tar.bz2
Patch0:		perl-Net_SSLeay-1.30-large-tcp-read.patch
Patch2:		perl-Net_SSLeay-1.2.5-CVE-2005-0106.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel
BuildRequires:	perl-devel

Requires: 	openssl >= 0.9.3a

%description
Net::SSLeay module for perl.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}.pm-%{version}
%patch0 -p0 -b .large_tcp
%patch2 -p1 -b .cve-2005-0106

chmod 0755 examples
# openssl_path is /usr here, therefore don't -I/usr/include and
# especially don't (badly) hardcode standard library search path
# /usr/lib
if [[ "%{_prefix}" = "/usr" ]]; then
    perl -pi -e "s@-[LI]\\\$openssl_path[^\s\"]*@@g" Makefile.PL
fi


%build
# note the %{_prefix} which must passed to Makefile.PL, weird but necessary :-(
perl Makefile.PL %{_prefix} INSTALLDIRS=vendor 
%make OPTIMIZE="%{optflags}"
perl -p -i -e 's|/usr/local/bin|/usr/bin|g;' *.pm examples/*


%check
#make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorarch}/auto/Net
%{perl_vendorarch}/Net
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc Changes Credits README examples QuickRef


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.30
- rebuild against new openssl

* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.30
- rebuild
- don't make test as secure.worldgaming.net no longer exists

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.30
- spec cleanups

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.30
- rebuild against new openssl
- spec cleanups

* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.30
- 1.30
- rebuild against perl 5.8.8
- create -doc subpackage
- update P0
- drop P1

* Fri Feb 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.25
- P2: security fix for CVE-2005-0106

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.25
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-11avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-9avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-8avx
- rebuild against new perl

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-7avx
- rebuild against latest openssl

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.25-6avx
- rebuild against new openssl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.25-5avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.25-4sls
- rebuild for perl 5.8.4
- keep autosplitted method, this package does not handle it well if you
  remove them (fpons)

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 1.25-3sls
- rebuild for new perl
- P1: don't try doing an external test to bakus.pt because it doesn't seem
  to exist and causes the tests to fail

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.25-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
