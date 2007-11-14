#
# spec file for package perl-Locale-gettext
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Locale-gettext
%define revision	$Rev$
%define name		perl-%{module}
%define version		1.05
%define release		%_revrel

Summary:	Message handling functions for Perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org/modules/by-module/Locale
Source:		http://www.cpan.org/modules/by-module/Locale/gettext-%{version}.tar.bz2
Patch2:		gettext-1.04-add-iconv.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext-devel
BuildRequires:	perl-devel

%description
The gettext module permits access from perl to the gettext() family of
functions for retrieving message strings from databases constructed to
internationalize software.

It provides gettext(), dgettext(), dcgettext(), textdomain() and
bindtextdomain().


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n gettext-%{version}
%patch2 -p0


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
%defattr(-,root,root)
%{perl_vendorarch}/Locale/*
%{perl_vendorarch}/auto/Locale/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README


%changelog
* Wed Nov 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.05
- rebuild against new gettext

* Sat Dec 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.05
- rebuild against new gettext

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.05
- spec cleanups

* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.05
- rebuild against perl 5.8.8
- create -doc subpackage
- clean up requirements

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.05
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.05
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.05-1avx
- 1.05
- rebuild against new perl 5.8.7 and new gettext

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.01-17avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.01-16avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.01-15avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.01-14avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 1.01-13sls
- in my "add iconv" patch, tag the SV* as UTF8 when output charset is
  UTF8, to fix #7156 with some modifications in urpmi too (gc)
- rebuild against new libintl

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.01-12sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 1.01-11sls
- rebuild for new perl

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.01-10sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
