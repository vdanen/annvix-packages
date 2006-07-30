#
# spec file for package httpd-mod_auth_pgsql
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		httpd-%{mod_name}
%define version 	%{apache_version}_%{mod_version}
%define release 	%_revrel

# Module-Specific definitions
%define apache_version	2.2.3
%define mod_version	2.0.3
%define mod_name	mod_auth_pgsql
%define mod_conf	13_%{mod_name}.conf
%define mod_so		%{mod_name}.so

Summary:	Basic authentication for the Apache web server using a PostgreSQL database
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://www.giuseppetanzilli.it/mod_auth_pgsql2/
Source0:	http://www.giuseppetanzilli.it/mod_auth_pgsql2/dist/%{mod_name}-%{mod_version}.tar.bz2
Source1:	%{mod_conf}
Patch0:		mod_auth_pgsql-2.0.3-nonpgsql.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  httpd-devel >= %{apache_version}
BuildRequires:	postgresql-devel
BuildRequires:	postgresql-libs-devel
BuildRequires:	openssl-devel

Requires(pre):	httpd = %{apache_version}
Requires(pre):	httpd-conf >= 2.2.0
Provides:	apache2-mod_auth_pgsql
Obsoletes:	apache2-mod_auth_pgsql

%description
mod_auth_pgsql can be used to limit access to documents served by
a web server by checking fields in a table in a PostgresQL
database.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{mod_name}-%{mod_version}
%patch0 -p0 -b .nonpgsql


%build
%{_sbindir}/apxs -I%{_includedir}/pgsql -L%{_libdir} \
    "-lpq -lcrypto -lssl" -c mod_auth_pgsql.c -n mod_auth_pgsql.so


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/httpd-extramodules/
cat %{_sourcedir}/%{mod_conf} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_so}

%files doc
%defattr(-,root,root)
%doc README INSTALL *.html


%changelog
* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_2.0.3
- apache 2.2.3
- spec cleanups

* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_2.0.3
- rebuild against new postgresql

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_2.0.3
- apache 2.2.2
- mod_auth_pgsql 2.0.3
- remove unneeded patches and rediff P0
- add -doc subpackage
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_2.0.2b1
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_2.0.2b1
- build against new postgresql

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_2.0.2b1
- apache 2.0.55
- P2: security fix for CVE-2005-3656

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.0.2b1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.0.2b1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.0.2b1
- Clean rebuild

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.0.2b1-1avx
- apache 2.0.54
- s/conf.d/modules.d/
- s/apache2/httpd/

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.0.2b1-3avx
- bootstrap build (new gcc, new glibc)
- don't include the symlinks to docs in /var/www/html/addon-modules

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.0.2b1-2avx
- rebuild

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.0.2b1-1avx
- 2.0.2b1
- apache 2.0.53
- P0, P1: from Fedora
- get rid of ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_2.0.1-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_2.0.1-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_2.0.1-1sls
- apache 2.0.49

* Wed Feb 18 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_2.0.1-3sls
- small cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_2.0.1-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_2.0.1-1mdk
- built for apache 2.0.48

* Fri Sep 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.47_2.0.1-4mdk
- fix deps

* Thu Sep 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_2.0.1-3mdk
- fix requires and buildrequires

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47_2.0.1-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_2.0.1-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_2.0.1-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_2.0.1-1mdk
- cosmetic rebuild for apache v2.0.45

* Sun Apr 06 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_2.0.1-1mdk
- 2.0.1

* Thu Jan 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_2.0.0-1mdk
- 2.0.0

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_2.0b6-1mdk
- rebuilt for apache v2.0.44

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.0b6-10mdk
- fix buildrequires apache2-devel >= 2.0.43-5mdk, as 
  pointed out by Olivier Thauvin

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.0b6-9mdk
- rebuilt against rebuilt buildrequires

* Tue Jan 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.0b6-8mdk
- fix BuildPrereq
- build against latest BuildRequires

* Tue Jan 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.0b6-7mdk
- fix BuildPrereq, Requires and build string

* Mon Jan 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.0b6-6mdk
- Rebuilt with the new apache-devel that uses /usr/sbin/apxs2 and
  /usr/include/apache2

* Sat Nov 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.0b6-5mdk
- rebuilt for/against apache2 where dependencies has changed in apr

* Tue Oct 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.0b6-4mdk
- extra modules needs to be loaded _before_ mod_ssl, mod_php and mod_perl
  in order to show up in the server string...

* Mon Oct  7 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.0b6-3mdk
- use the right version in the d*mn changelog... (gotta sleep now...)

* Mon Oct  7 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.0b6-3mdk
- use the right apache version in the d*mn changelog...

* Mon Oct  7 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42_2.0b6-1mdk
- new version

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.0b5-1mdk
- rebuilt for/against new apache2 version 2.0.43 (even though 2.0.42 and 
  2.0.43 are binary compatible, we have to consider rpm dependencies)
- sanitize rpm package versioning

* Thu Sep 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42_2.0b5-1mdk
- new version
- drop the apache2 patch, it's merged upstream
- update url
- requires libpgsql2

* Thu Sep 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42_0.9.12-5mdk
- rebuilt against new apache v2.0.42

* Wed Sep  3 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX_0.9.12-4mdk
- Comply with ADVX policy at http://advx.org/devel/policy.php

* Sun Sep  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.9.12-3mdk
- use examples in S1 from RH Rawhide

* Sun Aug 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.9.12-2mdk
- revert macro changes in %%post and %%preun (what was I thinking...)

* Sat Aug 17 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.9.12-1mdk
- initial cooker contrib, ripped from RH, adapted for ML
- use macros in %%post and %%preun
- fix requires
