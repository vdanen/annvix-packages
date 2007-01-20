#
# spec file for package httpd-mod_auth_remote
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
%define epoch		1

# Module-Specific definitions
%define apache_version	2.2.4
%define mod_version	0.1
%define mod_name	mod_auth_remote
%define mod_conf	82_%{mod_name}.conf
%define mod_so		%{mod_name}.so

Summary:	Mod_auth_remote is a DSO module for the Apache Web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		System/Servers
URL:		http://puggy.symonds.net/~srp/stuff/mod_auth_remote/
Source0:	%{mod_name}-%{mod_version}.tar.bz2
Source1:	%{mod_conf}
Patch0:		mod_auth_remote-0.1-register.patch
Patch1:		mod_auth_remote-0.1-apr1_1.diff
Patch2:		mod_auth_remote-0.1-apr1_2.diff


BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  httpd-devel >= %{apache_version}

Requires(pre):	httpd >= %{apache_version}
Requires(pre):	httpd-conf >= 2.2.0
Provides:	apache2-mod_auth_remote
Obsoletes:	apache2-mod_auth_remote


%description
This module is a very simple, lightweight method of setting up a
single signon system across multiple web-applicaitions hosted on
different servers.

The actual authentication & authorization system is deployed on a
single server instead of each individual server. All other servers
are built with mod_auth_remote enabled. When a request comes in,
mod_auth_remote obtains the client username & password from the
client via basic authentication scheme.

It then builds a HTTP header with authorization header built from
the client's userid:passwd. mod_auth_remote then makes a HEAD
request to the authentication server. On reciept of a 2XX
response, the client is validated; for all other responses the
client is not validated.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -c -n %{mod_name}-%{mod_version} -a0
%patch0 -p0
%patch1 -p0
%patch2 -p0


%build
%{_sbindir}/apxs -c %{mod_name}.c


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
%doc readme.txt


%changelog
* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.4_0.1
- apache 2.2.4

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_0.1
- apache 2.2.3
- spec cleanups

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_0.1
- apache 2.2.2
- P0, P1: apr1 fixes from mandriva
- add -doc subpackage
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_0.1
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_0.1
- apache 2.0.55

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_0.1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_0.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_0.1
- Clean rebuild

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_0.1-1avx
- apache 2.0.54
- s/conf.d/modules.d/
- s/apache2/httpd/

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_0.1-3avx
- bootstrap build (new gcc, new glibc)
- don't include the symlinks to docs in /var/www/html/addon-modules

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_0.1-2avx
- rebuild

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_0.1-1avx
- apache 2.0.53
- remove ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_0.1-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_0.1-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_0.1-1sls
- apache 2.0.49

* Wed Feb 18 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_0.1-4sls
- small tidy

* Tue Dec 23 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_0.1-3sls
- new version from author (bugfixes)
- fix url
- this is actually 0.1 so bump up the epoch and make the version right
- rename P0

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_1.0-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
