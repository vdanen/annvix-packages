%define name	php-%{modname}
%define version	%{phpversion}
%define release	1sls

%define phpsource	%{_prefix}/src/php-devel
%define _docdir		%{_datadir}/doc/%{name}-%{version}
%{expand:%(cat /usr/src/php-devel/PHP_BUILD||(echo -e "error: failed build dependencies:\n        php-devel >= 430 (4.3.0) is needed by this package." >/dev/stderr;kill -2 $PPID))}

%define realname	LDAP
%define modname		ldap
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		27_%{modname}.ini
%define mod_src		ldap.c
%define mod_lib		"-lldap -llber"
%define mod_def		"-DCOMPILE_DL_LDAP -DHAVE_LDAP_START_TLS_S"
%define rlibs		libldap2 libsasl2 libopenssl0.9.7
%define blibs		libldap-devel pam-devel libsasl-devel openssl-devel

Summary:	The %{realname} module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:  php%{libversion}-devel
BuildRequires:	%{blibs}

Requires:	php%{libversion}
Provides: 	ADVXpackage

%description
The %{name} package is a dynamic shared object (DSO) that adds
%{realname} support to PHP. PHP is an HTML-embedded scripting language. 
If you need %{realname} support for PHP applications, you will need to 
install this package in addition to the php package.

%build
[ -e ./%{dirname} ] && rm -fr ./%{dirname}
cp -dpR %{phpsource}/extensions/%{dirname} .
cd %{dirname}

%{phpsource}/buildext %{modname} %{mod_src} %{mod_lib} %{mod_def}

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
cd %{dirname}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_docdir}
install -d %{buildroot}%{_sysconfdir}/php

install -m755 %{soname} %{buildroot}%{phpdir}/extensions/

cat > %{buildroot}%{_docdir}/README <<EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
To activate it, make sure a file /etc/php/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php/%{inifile} << EOF
extension = %{soname}
EOF

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -e ./%{dirname} ] && rm -fr ./%{dirname}

%files 
%defattr(-,root,root)
%doc %{_docdir}/README
%{phpdir}/extensions/%{soname}
%config(noreplace) %{_sysconfdir}/php/%{inifile}

%changelog
* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- php 4.3.7

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- php 4.3.6

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-3sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Mon Oct 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- 4.3.3

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-3mdk
- built for 4.3.3
- added start tls (buchan?)
- fix explicit-lib-dependency
- misc spec file fixes

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 4.3.2-2mdk
- Rebuild to fix bad signature

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild
- misc spec file fixes

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-3mdk
- rebuild

* Sun Jan 19 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-2mdk
- rebuilt with new openssl

* Sun Jan  5 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-1mdk
- New 4.3.0 release
- Totally macroize based on suggestions from Alexander Skwar
- New method of installing extensions thanks to Oden Eriksson
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3 maintenance release
- Do not reload apache

* Thu Aug 22 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.2-1mdk
- Rebuild for 4.2.2
- Macroize a bit more, make version depend on "php -v"

* Sun May 26 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-2mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.1

* Mon Apr 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- misc spec file fixes
	- PHP 4.2.0

* Mon Mar 04 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-1mdk
- PHP 4.1.2

* Thu Jan 24 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-2mdk
- Rebuild against openldap 2.0.21.

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-1mdk
- PHP 4.1.1.
- openldap 2.0.19.

* Tue Dec 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-1mdk
- PHP 4.1.0.

* Mon Nov 16 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-7mdk
- Added an URL to fix no-url-tag warning in rpmlint.
- OpenLDAP 2.0.18.

* Mon Nov 12 2001 Philippe Libat <philippe@mandrakesoft.com> 4.0.6-6mdk
- fix summary

* Thu Oct 18 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-5mdk
- new openldap.

* Thu Oct 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-4mdk
- Rebuilt against latest openldap against latest db3.

* Mon Sep 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-3mdk
- Provides the Obsoletes for compatibility.

* Fri Jul 13 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-2mdk
- rebuild against libdb3.2

* Wed Jul  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-1mdk
- 4.0.6
- s/Copyright/License/

* Thu Apr 12 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-6mdk
- fix requires

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-5mdk
- fix post scripts for good 

* Mon Apr  2 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-4mdk
- Split ldap package from php package so that when a new ldap 
  package comes out, we don't have to recompile php, only this module
