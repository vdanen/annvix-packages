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
%define apache_version	2.2.8
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

%description
mod_auth_pgsql can be used to limit access to documents served by a web
server by checking fields in a table in a PostgresQL database.


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
install -m 0644 %{_sourcedir}/%{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}


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
* Sat Jan 26 2008 Vincent Danen <vdanen-at-build.annivix.org> 2.2.8_2.0.3
- apache 2.2.8

* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.6_2.0.3
- rebuild against new openssl

* Sat Sep 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.6_2.0.3
- apache 2.2.6
- rebuild against new postgresql

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.4_2.0.3
- apache 2.2.4
- rebuild against new postgresql

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_2.0.3
- rebuild against new postgresql

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_2.0.3
- rebuild against new openssl
- spec cleanups

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
