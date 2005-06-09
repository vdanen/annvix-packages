%define	module	DBD-mysql
%define	name	perl-%{module}
%define version 2.9004
%define release 2avx

Summary:	DBD MySQL Perl Emulation Layer
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Databases
URL:		http://search.cpan.org/dist/%{module}
Source:		http://www.cpan.org/modules/by-module/DBD/%{module}-%{version}.tar.bz2

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	MySQL-devel perl-DBI
BuildRequires:	perl-devel

Requires:	perl
Provides:	perl-Mysql
Obsoletes:	perl-Mysql

%description
DBD::mysql is an interface driver for connecting the DBMS independent
Perl API DBI to the MySQL DBMS. When you want to use MySQL from
within perl, DBI and DBD::mysql are your best choice: Unlike "mysqlperl",
another option, this is based on a common standard, so your sources
will easily be portable to other DBMS's.


%prep
%setup -q -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="$RPM_OPT_FLAGS"

# make test requires a running mysql server
#make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%{makeinstall_std}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ChangeLog
%{perl_vendorarch}/*
%{_mandir}/*/*

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 2.9004-2avx
- bootstrap build

* Fri Feb 25 2005 Vincent Danen <vdanen@annvix.org> 2.9004-1avx
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
