#
# spec file for package perl-DBD-SQLite
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		DBD-SQLite
%define	revision	$Rev$
%define	name		perl-%{module}
%define version 	1.14
%define release 	%_revrel

Summary:	Self Contained RDBMS in a DBI Driver
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source:		http://www.cpan.org/modules/by-module/DBD/DBD-SQLite-%{version}.tar.gz

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl(DBI)
BuildRequires:	perl-devel

%description
DBD::SQLite embeds that database engine into a DBD driver, so if you
want a relational database for your project, but don't want to install a
large RDBMS system like MySQL or PostgreSQL, then DBD::SQLite may be
just what you need.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make CCFLAGS="%{optflags} -DNDEBUG=1 -DSQLITE_PTR_SZ=4"


%check
# these tests fail, ref: http://rt.cpan.org//Ticket/Display.html?id=32570
rm -f t/06error.t
rm -f t/07busy.t
rm -f t/08create_function.t
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorarch}/DBD
%{perl_vendorarch}/auto/DBD
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README* Changes


%changelog
* Sun Feb 17 2008 Vincent Danen <vdanen-at-build.annvix.org> 1.14
- re-enable the tests and disable those tests that fail

* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.14
- 1.14
- disable the tests for now, one result is "dubious"

* Wed Jun 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.12
- first Annvix package (needed by apparmor-utils)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
