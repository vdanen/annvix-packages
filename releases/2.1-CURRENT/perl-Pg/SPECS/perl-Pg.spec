#
# spec file for package perl-Pg
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Pg
%define revision	$Rev$
%define name		perl-%{module}
%define version		2.1.1
%define release		%_revrel

Summary:	A libpq-based PostgreSQL interface for Perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://gborg.postgresql.org/project/pgperl/projdisplay.php
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	postgresql-devel
BuildRequires:	postgresql-libs-devel

%description
pgperl is an interface between Perl and PostgreSQL. This uses the
Perl5 API for C extensions to call the PostgreSQL libpq interface.
Unlike DBD:pg, pgperl tries to implement the libpq interface as
closely as possible.

You have a choice between two different interfaces: the old
C-style interface and a new one, using a more Perl-ish style. The
old style has the benefit that existing libpq applications can
easily be ported to perl. The new style uses class packages and
might be more familiar to C++ programmers.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
# perl path hack
find . -type f | xargs perl -p -i -e "s|^#\!/usr/local/bin/perl|#\!/usr/bin/perl|g"


%build
export POSTGRES_INCLUDE=`pg_config --includedir`
export POSTGRES_LIB=`pg_config --libdir`
perl Makefile.PL INSTALLDIRS=vendor </dev/null
%make


%check
# make test needs a running PostgreSQL server
#make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/*/*/Pg/Pg.so
%{perl_vendorlib}/*/*/Pg/autosplit.ix
%{perl_vendorlib}/*/Pg.pm
%{_mandir}/man3*/*

%files doc
%defattr(-,root,root)
%doc Changes README


%changelog
* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1
- rebuild against new postgresql

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1
- rebuild against new postgresql

* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1
- rebuild against new postgresql

* Sat May 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1
- build against new postgresql

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1.
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1-1avx
- 2.1.1
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2-11avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2-10avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2-9avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2-8avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.0.2-7sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 2.0.2-6sls
- rebuild for new perl

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 2.0.2-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
