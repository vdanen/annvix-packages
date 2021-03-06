%define name	apache2-%{mod_name}
%define version %{apache_version}_%{mod_version}
%define release 1avx

# Module-Specific definitions
%define apache_version	2.0.53
%define mod_version	2.0.2b1
%define mod_name	mod_auth_pgsql
%define mod_conf	13_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

Summary:	Basic authentication for the apache2 web server using a PostgreSQL database
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://www.giuseppetanzilli.it/mod_auth_pgsql2/
Source0:	http://www.giuseppetanzilli.it/mod_auth_pgsql2/dist/%{sourcename}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_auth_pgsql-2.0.1-fdr-nonpgsql.patch.bz2
Patch1:		mod_auth_pgsql-2.0.1-fdr-static.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:  apache2-devel >= %{apache_version}, postgresql-devel, postgresql-libs-devel, openssl-devel

# Standard ADVX requires
Prereq:		apache2 = %{apache_version}, apache2-conf

%description
mod_auth_pgsql can be used to limit access to documents served by
a web server by checking fields in a table in a PostgresQL
database.

%prep
%setup -q -n %{sourcename}
%patch0 -p1 -b .nonpgsql
%patch1 -p1 -b .static

%build

%{_sbindir}/apxs2 -I%{_includedir}/pgsql -L%{_libdir} \
    "-lpq -lcrypto -lssl" -c mod_auth_pgsql.c -n mod_auth_pgsql.so

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/apache2-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/apache2-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{mod_conf}

mkdir -p %{buildroot}/var/www/html/addon-modules
ln -s ../../../../%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README INSTALL *.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache2-extramodules/%{mod_so}
/var/www/html/addon-modules/*

%changelog
* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 2.0.53_2.0.2b1-2avx
- 2.0.2b1
- apache 2.0.53
- P0, P1: from Fedora
- get rid of ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52_2.0.1-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49_2.0.1-2avx
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
