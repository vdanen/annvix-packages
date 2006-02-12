#
# spec file for package httpd-mod_auth_mysql
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
%define apache_version	2.0.55
%define mod_version	2.9.0
%define mod_name	mod_auth_mysql
%define mod_conf	12_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

Summary:	Basic authentication for the Apache web server using a MySQL database
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://sourceforge.net/projects/modauthmysql/
Source0:	mod_auth_mysql-%{mod_version}.tar.bz2
Source1:	%{mod_conf}

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  httpd-devel >= %{apache_version}, MySQL-devel

Prereq:		httpd = %{apache_version}
Prereq:		httpd-conf
Provides:	apache2-mod_auth_mysql
Obsoletes:	apache2-mod_auth_mysql

%description
mod_auth_mysql is an Apache module to authenticate users and
authorize access through a MySQL database.  It is flexible and
support several encryption methods.


%prep
%setup -q -n %{mod_name}-%{mod_version}


%build
%{_sbindir}/apxs -L%{_libdir}/mysql -I%{_includedir}/mysql -Wl,-lmysqlclient -c mod_auth_mysql.c


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/httpd-extramodules/
cat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README CHANGES BUILD CONFIGURE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_2.9.0
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_2.9.0
- apache 2.0.55

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.9.0
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.9.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.9.0
- Clean rebuild

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.9.0-1avx
- apache 2.0.54
- mod_auth_mysql 2.9.0
- s/conf.d/modules.d/
- s/apache2/httpd/
- P0: fixes from 2.9.0 to make it work with MySQL-4.1.x password hashing

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.8.1-3avx
- bootstrap build (new gcc, new glibc)
- don't include the symlinks to docs in /var/www/html/addon-modules

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.8.1-2avx
- rebuild

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.8.1-1avx
- 2.8.1
- apache 2.0.53
- get rid of ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_1.11-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_1.11-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_1.11-1sls
- apache 2.0.49

* Wed Feb 18 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_1.11-3sls
- little cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_1.11-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_1.11-1mdk
- built for apache 2.0.48

* Fri Sep 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.47_1.11-4mdk
- nuke implicit requires

* Thu Sep 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.11-3mdk
- fix buildrequires

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47_1.11-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.11-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_1.11-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_1.11-1mdk
- cosmetic rebuild for apache v2.0.45

* Sat Feb 22 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_1.11-2mdk
- link with libmysql12

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_1.11-1mdk
- rebuilt for apache v2.0.44

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-7mdk
- fix buildrequires apache2-devel >= 2.0.43-5mdk, as 
  pointed out by Olivier Thauvin

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-6mdk
- rebuilt against rebuilt buildrequires

* Tue Jan 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-5mdk
- build against latest BuildRequires

* Mon Jan 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-4mdk
- Rebuilt with the new apache-devel that uses /usr/sbin/apxs2 and
  /usr/include/apache2

* Sat Nov 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-3mdk
- rebuilt for/against apache2 where dependencies has changed in apr

* Tue Oct 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-2mdk
- extra modules needs to be loaded _before_ mod_ssl, mod_php and mod_perl
  in order to show up in the server string...

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-1mdk
- rebuilt for/against new apache2 version 2.0.43 (even though 2.0.42 and 
  2.0.43 are binary compatible, we have to consider rpm dependencies)
- sanitize rpm package versioning

* Thu Sep 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42_1.11-6mdk
- rebuilt against new apache v2.0.42

* Wed Sep  3 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX_1.11-5mdk
- Comply with ADVX policy at http://advx.org/devel/policy.php
- link with dynamic libmysqlclient.so instead of the static .a (really
  important when used with PHP)

* Sat Aug 31 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.11-4mdk
- use examples in S2 from RH Rawhide

* Sun Aug 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.11-3mdk
- revert macro changes in %%post and %%preun (what was I thinking...)

* Sat Aug 17 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.11-2mdk
- use macros in %%post and %%preun
- fix requires

* Tue Aug 13 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.11-1mdk
- initial cooker contrib, ripped from RH, adapted for ML

