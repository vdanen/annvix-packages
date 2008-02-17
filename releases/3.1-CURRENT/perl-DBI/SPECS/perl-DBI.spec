#
# spec file for package perl-DBI
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		DBI

%define revision	$Rev$
%define name		perl-%{module}
%define version 	1.602
%define release 	%_revrel

Summary:	The Perl Database Interface
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://dbi.perl.org
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/DBI/DBI-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(Storable) >= 1
BuildRequires:	perl(Test::Simple) >= 0.4
BuildConflicts:	perl-PlRPC

Requires:	perl

%description
The Perl Database Interface (DBI) is a database access Application Programming
Interface (API) for the Perl Language. The Perl DBI API specification defines a
set of functions, variables and conventions that provide a consistent database
interface independent of the actual database being used.


%package proxy
Group:		Development/Perl
Summary: 	DBI proxy server and client
Requires:	%{name} = %{version}

%description proxy
DBI::ProxyServer is a module for implementing a proxy for the DBI
proxy driver, DBD::Proxy.
DBD::Proxy is a Perl module for connecting to a database via a remote
DBI driver.


%package ProfileDumper-Apache
Group:		Development/Perl
Summary: 	DBI profiling data for mod_perl
Requires:	%{name} = %{version}

%description ProfileDumper-Apache
This module interfaces DBI::ProfileDumper to Apache/mod_perl. Using this
module you can collect profiling data from mod_perl applications. It
works by creating a DBI::ProfileDumper data file for each Apache
process. These files are created in your Apache log directory. You can
then use dbiprof to analyze the profile files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make CFLAGS="%{optflags}"


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

# remove Win32 stuff
rm -rf %{buildroot}%{perl_vendorarch}/Win32
rm -f %{buildroot}%{perl_vendorarch}/DBI/W32ODBC.pm
rm -f %{buildroot}%{perl_vendorarch}/Roadmap.pod
rm -f %{buildroot}%{perl_vendorarch}/DBI/Roadmap.pm
rm -f %{buildroot}%{perl_vendorarch}/TASKS.pod
rm -f %{buildroot}%{perl_vendorarch}/DBI/TASKS.pm
rm -f %{buildroot}%{_mandir}/man3pm/Win32::DBIODBC.3pm*
rm -f %{buildroot}%{_mandir}/man3pm/DBI::W32ODBC.3pm*
rm -f %{buildroot}%{_mandir}/man3pm/Roadmap.3pm*
rm -f %{buildroot}%{_mandir}/man3pm/TASKS.3pm*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/dbilogstrip
%{_bindir}/dbiprof
%{_mandir}/*/*
%exclude %{_mandir}/man1/dbiproxy.1*
%exclude %{_mandir}/man3*/DBD::Proxy.3pm*
%exclude %{_mandir}/man3*/DBI::ProxyServer.3pm*
%exclude %{_mandir}/man3*/DBI::ProfileDumper::Apache.3pm*
%{perl_vendorarch}/Bundle
%{perl_vendorarch}/DBD
%{perl_vendorarch}/dbixs_rev.pl
%exclude %{perl_vendorarch}/DBD/Proxy.pm
%{perl_vendorarch}/DBI.pm
%{perl_vendorarch}/DBI
%exclude %{perl_vendorarch}/DBI/ProfileDumper
%exclude %{perl_vendorarch}/DBI/ProxyServer.pm
%{perl_vendorarch}/auto/DBI

%files proxy
%defattr(-,root,root)
%{_bindir}/dbiproxy
%{perl_vendorarch}/DBD/Proxy.pm
%{perl_vendorarch}/DBI/ProxyServer.pm
%{_mandir}/man1/dbiproxy.1.*
%{_mandir}/man3*/DBI::ProxyServer.3pm.*
%{_mandir}/man3*/DBD::Proxy.3pm.*

%files ProfileDumper-Apache
%defattr(-,root,root)
%{perl_vendorarch}/DBI/ProfileDumper
%{_mandir}/man3*/DBI::ProfileDumper::Apache.3pm.*

%files doc
%doc Changes README TODO_2005.txt Roadmap.pod TASKS.pod


%changelog
* Sun Feb 17 2008 Vincent Danen <vdanen-at-build.annvix.org> 1.602
- 1.602

* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.601
- 1.601

* Mon Jul 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.54
- 1.54

* Fri Dec 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.53
- 1.53

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.52
- 1.52

* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.50
- 1.50
- build against perl 5.8.8
- update BuildRequires according to new perl policy
- add -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.48
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.48
- add BuildRequires: perl-Net-Daemon
- add BuildConflicts: perl-PlRPC (or the tests fail on the proxy test)

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.48
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.48-1avx
- 1.48
- remove requires on release for sub-packages
- rebuild against perl 2.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.47-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.47-2avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.47-1avx
- 1.47
- use %%make and %%makeinstall_std macros (peroyvind)
- remove manpages of Windows-specific modules (rgarciasuarez)

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.38-6avx
- rebuild against new perl

* Fri Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.38-5avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.38-4sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 1.38-3sls
- rebuild for new perl
- minor spec cleanups
- remove Prefix

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.38-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
