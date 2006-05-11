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
%define version 	3.0002
%define release 	%_revrel

Summary:	MySQL Perl bindings
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Databases
URL:		http://search.cpan.org/dist/%{module}
Source:		http://www.cpan.org/modules/by-module/DBD/%{module}-%{version}.tar.bz2

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	MySQL-devel
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

* Wed Jan 26 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.9004-6mdk
- Add perl-DBI in the BuildRequires (Marc Koschewski)

* Mon Jan 24 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9004-5mdk
- rebuild

* Sat Jan 22 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.9004-4mdk
- rebuilt against MySQL-4.1.x system libs

* Fri Jan 21 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.9004-3mdk
- Fix URL and source
- Replaces perl-Mysql

* Mon Nov 15 2004 Michael Scherer <misc@mandrake.org> 2.9004-2mdk
- Rebuild for new perl

* Sat Jul 17 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.9004-1mdk
- 2.9004

* Wed Jun 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.9003-1mdk
- 2.9003
- drop distribution tag
- cosmetics

* Mon Nov 24 2003 Michael Scherer <misc@mandrake.org> 2.9002-2mdk 
- BuildRequires perl-devel

* Tue Oct 21 2003 Warly <warly@mandrakesoft.com> 2.9002-1mdk
- new version
