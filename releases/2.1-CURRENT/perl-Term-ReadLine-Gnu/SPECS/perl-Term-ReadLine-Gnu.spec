#
# spec file for package perl-Term-ReadLine-Gnu
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Term-ReadLine-Gnu
%define revision	$Rev$
%define name		perl-%{module}
%define version 	1.15
%define release 	%_revrel

Summary:	GNU Readline for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	termcap-devel
BuildRequires:	perl-devel
BuildRequires:	readline-devel

Obsoletes:	perl-Term-Readline-Gnu
Provides:	perl-Term-Readline-Gnu

%description
This is an implementation of the interface to the GNU Readline
Library.  This module gives you input line editing facility, input
history management facility, word completion facility, etc.  It uses
the real GNU Readline Library.  And this module has the interface with
the almost all variables and functions which are documented in the GNU
Readline/History Library.  So you can program your custom editing
function, your custom completion function, and so on with Perl.  This
may be useful for prototyping before programming with C.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
find -type f -exec chmod 0644 '{}' \;
perl Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="%{optflags}"


%check
if [ -n "$DISPLAY" ]; then
    TERM=linux make test
else
    echo "make test not done because DISPLAY var is not set"
fi

chmod 0644 README


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
# Fix bogus dependancy on /usr/local/bin/perl:
perl -pi -e 's!/usr/local/bin/perl!/usr/bin/perl!g' %{buildroot}%{perl_vendorarch}/Term/ReadLine/Gnu/{euc_jp,XS}.pm


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%dir %{perl_vendorarch}/Term
%{perl_vendorarch}/Term
%dir %{perl_vendorarch}/auto/Term
%{perl_vendorarch}/auto/Term

%files doc
%defattr(-,root,root)
%doc README


%changelog
* Sun Jun 24 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- rebuild against new readline

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- rebuild against new readline

* Sat May 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- rebuild against perl 5.8.8
- create -doc subpackage
- fix permissions
- provide the package we obsolete

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-5avx
- rebuild against perl 5.8.7

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-4avx
- rebuild against new readline

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-2avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-1avx
- 1.15

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.14-9avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.14-8avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.14-7sls
- rebuild for perl 5.8.4
- own dir

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 1.14-6sls
- rebuild for new perl
- don't make test if $DISPLAY is not set (it will fail) (thauvin)

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.14-5sls
- OpenSLS build
- tidy spec
- pkg name change from perl-Term-Readline-Gnu to perl-Term-ReadLine-Gnu to
  follow our spec of perl-%%{module}
- Obsoletes perl-Term-Readline-Gnu; anything that requires it will have to
  change their req's as we don't use dumb provides

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
