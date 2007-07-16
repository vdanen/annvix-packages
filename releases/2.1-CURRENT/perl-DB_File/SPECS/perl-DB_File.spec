#
# spec file for package perl-DB_File
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		perl-%{module}
%define module		DB_File
%define version		1.815
%define release		%_revrel

Summary:	Perl module for use of the Berkeley DB version 1
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/%{module}-%{version}.tar.gz
Patch:		%{module}-1.805-makefile.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	db-devel
BuildRequires:	perl-devel

%description
DB_File is a module which allows Perl programs to make use of the
facilities provided by Berkeley DB version 1. (DB_File can be built with
version 2 or 3 of Berkeley DB, but it will only support the 1.x
features).

If you want to make use of the new features available in Berkeley DB
2.x or 3.x, use the Perl module BerkeleyDB instead.

Berkeley DB is a C library which provides a consistent interface to a
number of database formats. DB_File provides an interface to all three
of the database types (hash, btree and recno) currently supported by
Berkeley DB.

For further details see the documentation included at the end of the
file DB_File.pm.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
%patch -p1
chmod 0644 README DB_File.pm


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
%{perl_vendorarch}/*.pm
%{perl_vendorarch}/auto/DB_File
%{_mandir}/man3*/DB_File.*

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Mon Jul 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.815
- 1.815

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.814
- rebuild against new db4

* Thu May 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.814
- 1.814
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.811
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.811
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.811-1avx
- 1.811
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.810-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.810-2avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.810-1avx
- 1.810

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.808-3avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.808-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.808-1sls
- 1.808
- fix url

* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 1.806-6sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
