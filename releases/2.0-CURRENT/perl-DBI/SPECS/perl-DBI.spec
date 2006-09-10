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
%define version 	1.50
%define release 	%_revrel

Summary:	The Perl Database Interface
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://dbi.perl.org
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/DBI/%{module}-%{version}.tar.bz2

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
rm -f %{buildroot}%{_mandir}/man3pm/Win32::DBIODBC.3pm*
rm -f %{buildroot}%{_mandir}/man3pm/DBI::W32ODBC.3pm*
rm -f %{buildroot}%{_mandir}/man3pm/Roadmap.3pm*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/dbiprof
%{_mandir}/*/*
%exclude %{_mandir}/man1/dbiproxy.1*
%exclude %{_mandir}/man3*/DBD::Proxy.3pm*
%exclude %{_mandir}/man3*/DBI::ProxyServer.3pm*
%exclude %{_mandir}/man3*/DBI::ProfileDumper::Apache.3pm*
%{perl_vendorarch}/Bundle
%{perl_vendorarch}/DBD
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
%doc Changes README ToDo 


%changelog
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

* Sat Aug 23 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 1.38-1mdk
- 1.38
- dropped patch

* Fri Aug  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.37-3mdk
- Remove flawed (arch-)dependent test fixed in DBI 1.38

* Fri May 16 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.37-2mdk
- splitted proxy and ProfileDumper subpackage for dependencies
- removed useless Win32 code

* Fri May 16 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.37-1mdk
- 1.37

* Tue Apr 01 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.35-1mdk
- 1.35

* Mon Dec 02 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.32-1mdk
- 1.32

* Sat Nov 30 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.31-1mdk
- 1.31
- added forgottent binaries

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 1.30-2mdk
- rebuild for perl thread-multi

* Fri Jul 19 2002 François Pons <fpons@mandrakesoft.com> 1.30-1mdk
- 1.30.

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.25-2mdk
- rebuild for perl 5.8.0

* Mon Jun 10 2002 François Pons <fpons@mandrakesoft.com> 1.25-1mdk
- 1.25.

* Tue May 28 2002 François Pons <fpons@mandrakesoft.com> 1.23-1mdk
- 1.23.

* Tue Mar 26 2002 François Pons <fpons@mandrakesoft.com> 1.21-1mdk
- 1.21.

* Wed Nov 07 2001 François Pons <fpons@mandrakesoft.com> 1.20-3mdk
- added url tag.

* Tue Oct 16 2001 Stefan van der Eijk <stefan@eijk.nu> 1.20-2mdk
- BuildRequires: perl-devel

* Fri Aug 31 2001 François Pons <fpons@mandrakesoft.com> 1.20-1mdk
- 1.20.

* Fri Aug 24 2001 François Pons <fpons@mandrakesoft.com> 1.19-1mdk
- 1.19.

* Tue Jul 03 2001 François Pons <fpons@mandrakesoft.com> 1.18-1mdk
- 1.18.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.14-6mdk
- Rebuild against the latest perl.

* Tue Nov 14 2000 François Pons <fpons@mandrakesoft.com> 1.14-5mdk
- description typo fix.

* Tue Aug 29 2000 François Pons <fpons@mandrakesoft.com> 1.14-4mdk
- removed make macro (-j x gets mad with x > 1).
- simplification of files.

* Thu Aug 03 2000 François Pons <fpons@mandrakesoft.com> 1.14-3mdk
- macroszifications.
- add doc.

* Tue Jul 18 2000 François Pons <fpons@mandrakesoft.com> 1.14-2mdk
- forgot dbipport.h in files.

* Tue Jul 18 2000 François Pons <fpons@mandrakesoft.com> 1.14-1mdk
- added requires.
- 1.14.

* Fri Jul 07 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.13-4mdk
- FIx build as user.

* Wed May 17 2000 David BAUDENS <baudens@mandrakesoft.com> 1.13-3mdk
- Fix build for i486

* Mon Apr  3 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.13-2mdk
- fixed group
- rebuild with new perl
- fixed location

* Sun Dec 05 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- First specfile

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
