%define	name	php-%{modname}
%define version	%{phpversion}
%define release	2avx

%define phpsource	%{_prefix}/src/php-devel
%define _docdir		%{_datadir}/doc/%{name}-%{version}
%{expand:%(cat /usr/src/php-devel/PHP_BUILD||(echo -e "error: failed build dependencies:\n        php-devel >= 430 (4.3.0) is needed by this package." >/dev/stderr;kill -2 $PPID))}

%define libxslt	%mklibname xslt 1
%define libxml2 %mklibname xml 2

%define realname	DOMXML
%define modname		domxml
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		19_%{modname}.ini
%define mod_src		php_domxml.c
%define mod_lib		"-lxml2 -lz -lm -lc -lexslt -lxslt -I%{_includedir}/libexslt -I%{_includedir}/libxml2"
%define mod_def		"-DCOMPILE_DL_DOMXML -DLIBXML_HTML_ENABLED -DLIBXML_XPATH_ENABLED -DLIBXML_XPTR_ENABLED -DHAVE_DOMEXSLT -DHAVE_DOMXML -DHAVE_DOMXSLT -DXML_GLOBAL_NAMESPACE"
%define rlibs		%{libxslt} >= 1.0.16, %{libxml2} >= 2.4.21
%define blibs		%{libxslt}-devel >= 1.0.16, %{libxml2}-devel >= 2.4.21

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

Requires:	%{rlibs}
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

perl -p -i -e "s|#include <libxml/|#include <libxml2/libxml/|g" php_domxml.*

#########################################################
## Nothing to be changed after this, except changelog! ##
#########################################################

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
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- php 4.3.7

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- php 4.3.6

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-4sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-3sls
- OpenSLS build
- tidy spec

* Mon Nov 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-2mdk
- remove deprecated "-lxsltbreakpoint"
- rebuilt against new xslt and xml2 libs

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- fix versioning

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Fri Sep 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3.2-4mdk
- fix deps

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-3mdk
- built for 4.3.3
- misc spec file fixes
- fix explicit-lib-dependency

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 4.3.2-2mdk
- Rebuild to fix bad signature

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-2mdk
- rebuild

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

* Mon May 27 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.1-3mdk
- rebuilt against php-4.2.1 this time (klama is wierd...)
- added Requires: php-common

* Mon May 27 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.1-2mdk
- misc spec file fixes

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- build against latest libxml2
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.1

* Mon Apr 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- Updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.0
	- initial cooker contrib
