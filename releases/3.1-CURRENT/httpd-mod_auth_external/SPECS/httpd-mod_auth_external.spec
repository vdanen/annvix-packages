#
# spec file for package httpd-mod_auth_external
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		httpd-%{mod_name}
%define version		%{apache_version}_%{mod_version}
%define release		%_revrel

# Module-Specific definitions
%define apache_version	2.2.8
%define mod_version	3.1.0
%define mod_name	mod_authnz_external
%define mod_conf	10_%{mod_name}.conf
%define mod_so		%{mod_name}.so

Summary:	An Apache authentication DSO using external programs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://www.unixpapa.com/mod_auth_external.html
Source0:	http://www.unixpapa.com/software/%{mod_name}-%{mod_version}.tar.gz
Source1:	%{mod_conf}

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  httpd-devel >= %{apache_version}

Requires(pre):	rpm-helper
Requires(pre):	httpd >= %{apache_version}
Requires(pre):	httpd-conf >= 2.2.0
Requires(postun): rpm-helper
Requires:	pwauth
Provides:	httpd-mod_auth_external = %{version}-%{release}
Obsoletes:	httpd-mod_auth_external

%description
An Apache external authentication module - uses PAM.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{mod_name}-%{mod_version}


%build
%{_sbindir}/apxs -c %{mod_name}.c


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/httpd-extramodules/
install -m 0644 %{_sourcedir}/%{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

chmod 0644 AUTHENTICATORS CHANGES INSTALL* README* TODO


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_so}

%files doc
%defattr(-,root,root)
%doc AUTHENTICATORS CHANGES INSTALL* README* TODO


%changelog
* Sat Jan 26 2008 Vincent Danen <vdanen-at-build.annivix.org> 2.2.8_3.1.0
- apache 2.2.8

* Sat Sep 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.6_3.1.0
- apache 2.2.6

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.4_3.1.0
- apache 2.2.4

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_3.1.0
- apache 2.2.3
- spec cleanups

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_3.1.0
- 3.1.0 (new name is httpd-mod_authnz_external)
- apache 2.2.2
- drop P1
- add -doc subpackage
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_2.2.9
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_2.2.9
- apache 2.0.55

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.2.9
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.2.9
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.2.9
- Clean rebuild

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.2.9-1avx
- apache 2.0.54
- s/conf.d/modules.d/
- s/apache2/httpd/

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.2.9-3avx
- bootstrap build (new gcc, new glibc)
- don't include the symlinks to docs in /var/www/html/addon-modules

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.2.9-2avx
- rebuild

* Fri Feb 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.2.9-1avx
- apache 2.0.53
- mod_auth_external 2.2.9
- pwauth is an external package
- get rid of ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_2.2.7-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_2.2.7-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_2.2.7-1sls
- apache 2.0.49

* Wed Feb 11 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_2.2.7-3sls
- more spec cleanups
- remove paths from pam.d file

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_2.2.7-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
