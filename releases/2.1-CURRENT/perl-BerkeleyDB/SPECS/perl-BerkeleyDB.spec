#
# spec file for package perl-BerkeleyDB
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		BerkeleyDB
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.31
%define release		%_revrel

Summary:	Perl module for BerkeleyDB 2.x and greater
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://www.cpan.org/modules/by-module/BerkeleyDB/%{module}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	db4-devel
BuildRequires:	perl-devel

%description
BerkeleyDB is a module which allows Perl programs to make use of the
facilities provided by Berkeley DB version 2 or greater. (Note: if
you want to use version 1 of Berkeley DB with Perl you need the DB_File
module).

Berkeley DB is a C library which provides a consistent interface to a
number of database formats. BerkeleyDB provides an interface to all
four of the database types (hash, btree, queue and recno) currently
supported by Berkeley DB.

For further details see the documentation in the file BerkeleyDB.pod.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make CFLAGS="%{optflags}" 


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/*/BerkeleyDB*
%{perl_vendorlib}/*/auto/BerkeleyDB
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.26
- rebuild against new db4

* Wed May 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.26
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.26
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.26
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.26-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.26-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.26-2avx
- bootstrap build

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.26-1avx
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
