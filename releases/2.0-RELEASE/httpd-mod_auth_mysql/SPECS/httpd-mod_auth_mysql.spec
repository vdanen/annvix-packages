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
%define apache_version	2.2.4
%define mod_version	3.0.0
%define mod_name	mod_auth_mysql
%define mod_conf	12_%{mod_name}.conf
%define mod_so		%{mod_name}.so

Summary:	Basic authentication for the Apache web server using a MySQL database
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://sourceforge.net/projects/modauthmysql/
Source0:	http://prdownloads.sourceforge.net/modauthmysql/%{mod_name}-%{mod_version}.tar.bz2
Source1:	%{mod_conf}
Patch0:		mod_auth_mysql-3.0.0-apr1x.patch
Patch1:		mod_auth_mysql-3.0.0-htpasswd-style.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  httpd-devel >= %{apache_version}
BuildRequires:	mysql-devel

Requires(pre):	httpd = %{apache_version}
Requires(pre):	httpd-conf >= 2.2.0

%description
mod_auth_mysql is an Apache module to authenticate users and
authorize access through a MySQL database.  It is flexible and
support several encryption methods.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{mod_name}-%{mod_version}
%patch0 -p1 -b .apr1x
%patch1 -p0 -b .htpasswd-style


%build
%{_sbindir}/apxs -L%{_libdir}/mysql -I%{_includedir}/mysql -Wl,-lmysqlclient -c mod_auth_mysql.c


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
%doc README CHANGES BUILD CONFIGURE


%changelog
* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.4_3.0.0
- apache 2.2.4

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_3.0.0
- rebuild against new mysql

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_3.0.0
- rebuild against new mysql
- spec cleanups

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_3.0.0
- apache 2.2.3
- spec cleanups

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_3.0.0
- apache 2.2.2
- mod_auth_mysql 3.0.0
- P0: apr1 fixes from fedora
- P1: htpasswd-style encryption
- add -doc subpackage
- rebuild with gcc4

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
