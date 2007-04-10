#
# spec file for package perl-DBD-mysql
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		DBD-mysql
%define	revision	$Rev$
%define	name		perl-%{module}
%define version 	3.0006
%define release 	%_revrel

Summary:	MySQL Perl bindings
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Databases
URL:		http://search.cpan.org/dist/%{module}
Source:		http://www.cpan.org/modules/by-module/DBD/%{module}-%{version}.tar.gz

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	mysql-devel
BuildRequires:	perl(DBI)
BuildRequires:	perl-devel

Provides:	perl-Mysql
Obsoletes:	perl-Mysql

%description
DBD::mysql is an interface driver for connecting the DBMS independent
Perl API DBI to the MySQL DBMS. When you want to use MySQL from
within perl, DBI and DBD::mysql are your best choice: Unlike "mysqlperl",
another option, this is based on a common standard, so your sources
will easily be portable to other DBMS's.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="%{optflags}"


%check
# make test requires a running mysql server
#make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorarch}/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README ChangeLog


%changelog
* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0006
- 3.0006
- rebuild against new mysql

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0002
- rebuild against new mysql
- spec cleanups

* Thu May 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0002
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0002
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0002
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0002-1avx
- 3.0002
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9004-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9004-2avx
- bootstrap build

* Fri Feb 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9004-1avx
- first annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
