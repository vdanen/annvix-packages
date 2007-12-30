#
# spec file for package httpd-mod_auth_radius
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
%define apache_version	2.2.6
%define mod_version	1.5.7
%define mod_name	mod_auth_radius
%define mod_conf	14_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}

Summary:	Mod_radius is a DSO module for the Apache Web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	Apache License
Group:		System/Servers
URL:		https://www.gnarst.net/authradius/
Source0:	%{mod_name}.tar.bz2
Source1:	%{mod_conf}
Patch0:		mod_auth_radius-1.5.7-CAN2005-0108.diff
Patch1:		mod_auth_radius-2.0.c.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  httpd-devel >= %{apache_version}

Requires(pre):	httpd >= %{apache_version}
Requires(pre):	httpd-conf >= 2.2.0

%description
Make Apache a RADIUS client for authentication and accounting requests.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n mod_auth_radius-%{mod_version}
%patch0 -p0
%patch1 -p0

mv mod_auth_radius-2.0.c mod_auth_radius.c


%build
%{_sbindir}/apxs -c mod_auth_radius.c -Wl,-lresolv


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
%doc README htaccess httpd.conf index.html


%changelog
* Sat Sep 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.6_1.5.7
- apache 2.2.6

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.4_1.5.7
- apache 2.2.4

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_1.5.7
- apache 2.2.3
- spec cleanups

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_1.5.7
- apache 2.2.2
- add -doc subpackage
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_1.5.7
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_1.5.7
- apache 2.0.55

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_1.5.7
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_1.5.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_1.5.7
- Clean rebuild

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_1.5.7-1avx
- apache 2.0.54
- mod_auth_radius 1.5.7
- s/conf.d/modules.d/
- s/apache2/httpd/
- epoch: 1
- update patches, including a fix for CAN-2005-0108


* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_1.7PR1-3avx
- bootstrap build (new gcc, new glibc)
- don't include the symlinks to docs in /var/www/html/addon-modules

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_1.7PR1-2avx
- rebuild

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_1.7PR1-1avx
- apache 2.0.53
- remove ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_1.7PR1-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_1.7PR1-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_1.7PR1-1sls
- apache 2.0.49

* Wed Feb 18 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_1.7PR1-3sls
- small cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_1.7PR1-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
