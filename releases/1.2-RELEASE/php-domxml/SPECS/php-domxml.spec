#
# spec file for package php-domxml
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	revision	$Rev$
%define	name		php-%{modname}
%define version		%{phpversion}
%define release		%_revrel

%define phpversion	4.4.4
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define libxslt		%mklibname xslt 1
%define libxml2		%mklibname xml 2

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

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php4-devel
BuildRequires:	%{blibs}

Requires:	%{rlibs}
Requires:	php4

%description
The %{name} package is a dynamic shared object (DSO) that adds
%{realname} support to PHP. PHP is an HTML-embedded scripting language. 
If you need %{realname} support for PHP applications, you will need to 
install this package in addition to the php package.


%prep
%setup -c -T
cp -dpR %{_usrsrc}/php-devel/extensions/%{dirname}/* .


%build
perl -p -i -e "s|#include <libxml/|#include <libxml2/libxml/|g" php_domxml.*

phpize
%configure2_5x \
  --with-dom=shared,%{_prefix} \
  --with-zlib-dir=%{_prefix} \
  --with-dom-xslt=%{_prefix} \
  --with-dom-exslt=%{_prefix}

%make
mv modules/*.so .


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/

cat > README.%{modname} <<EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
To activate it, make sure a file /etc/php.d/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%doc README*
%config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%{phpdir}/extensions/%{soname}


%changelog
* Thu Aug 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.4
- php 4.4.4

* Wed Aug 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.3
- php 4.4.3

* Wed Jan 18 2006 Vincent Danen <vdanen-at-build.annvix.org>
- php 4.4.2

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Nov 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-1avx
- php 4.4.1

* Wed Sep 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-1avx
- php 4.4.0

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-2avx
- rebuild

* Sat May 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-1avx
- php 4.3.11

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-3avx
- rebuild for new libxml2 and libxslt

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-2avx
- spec cleanups

* Fri Dec 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-1avx
- php 4.3.10

* Wed Sep 29 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.9-1avx
- php 4.3.9

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
- use phpize and %%configure2_5x macro (oden)
- move scandir to /etc/php.d
- own docdir

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.7-2avx
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
