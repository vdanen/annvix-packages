%define name	php-%{modname}
%define version	%{phpversion}
%define release	2sls

%define phpsource	%{_prefix}/src/php-devel
%define _docdir		%{_datadir}/doc/%{name}-%{version}
%{expand:%(cat /usr/src/php-devel/PHP_BUILD||(echo -e "error: failed build dependencies:\n        php-devel >= 430 (4.3.0) is needed by this package." >/dev/stderr;kill -2 $PPID))}

%define realname	XSLT
%define modname		xslt
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		52_%{modname}.ini
%define mod_src		"xslt.c sablot.c" 
%define mod_lib		"-lsablot -lexpat -ljs -lstdc++ -lgcc"
%define mod_def		"-DCOMPILE_DL_XSLT -DHAVE_XSLT -DHAVE_SABLOT_BACKEND -DHAVE_DLFCN_H -DHAVE_LIBEXPAT2 -DHAVE_SABLOT_SET_ENCODING"
%define rlibs		libexpat0 libsablotron0 >= 0.90 libjs1 >= 1.5 libstdc++5 libgcc1
%define blibs		expat-devel libsablotron-devel js-devel >= 1.5 libstdc++-devel libgcc1

Summary:	The %{realname} module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net
Source0:	foo.xml
Source1:	foo.xsl
Source2:	run.php

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
cd %{dirname}
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_docdir}
install -d %{buildroot}%{_sysconfdir}/php

install -m755 %{soname} %{buildroot}%{phpdir}/extensions/

cat > %{buildroot}%{_docdir}/README <<EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
To activate it, make sure a file /etc/php/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

install -m644 %{SOURCE0} %{buildroot}%{_docdir}/
install -m644 %{SOURCE1} %{buildroot}%{_docdir}/
install -m644 %{SOURCE2} %{buildroot}%{_docdir}/
install -m644 README.XSLT-BACKENDS %{buildroot}%{_docdir}/

cat > %{buildroot}%{_sysconfdir}/php/%{inifile} << EOF
extension = %{soname}
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ -e ./%{dirname} ] && rm -fr ./%{dirname}

%files 
%defattr(-,root,root)
%doc %{_docdir}/README
%doc %{_docdir}/README.XSLT-BACKENDS
%doc %{_docdir}/foo.x*
%doc %{_docdir}/run.php
%{phpdir}/extensions/%{soname}
%config(noreplace) %{_sysconfdir}/php/%{inifile}

%changelog
* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Mon Oct 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- 4.3.3

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-3mdk
- built for 4.3.3
- fix explicit-lib-dependency
- misc spec file fixes

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 4.3.2-2mdk
- Rebuild to fix bad signature

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-3mdk
- rebuild

* Sun Jan 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-2mdk
- enable JavaScript support

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

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.1-4mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Jul 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.1-3mdk
- Automated rebuild with gcc3.2

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

* Thu Jan 17 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-2mdk
- Rebuild against sablotron 0.81.

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-1mdk
- PHP 4.1.1.

* Tue Dec 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-1mdk
- PHP 4.1.0.
- Added version check for libsablotron0.

* Tue Nov 13 2001 Stefan van der Eijk <stefan@eijk.nu> 4.0.6-7mdk
- BuildRequires: libexpat-devel

* Mon Nov 12 2001 Philippe Libat <philippe@mandrakesoft.com> 4.0.6-6mdk
- link with expat

* Mon Nov 12 2001 Philippe Libat <philippe@mandrakesoft.com> 4.0.6-5mdk
- new module XSLT integration
