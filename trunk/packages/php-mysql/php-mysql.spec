%define phpsource       %{_prefix}/src/php-devel
%define _docdir %{_datadir}/doc/%{name}-%{version}
%{expand:%(cat /usr/src/php-devel/PHP_BUILD||(echo -e "error: failed build dependencies:\n        php-devel >= 430 (4.3.0) is needed by this package." >/dev/stderr;kill -2 $PPID))}

%define release 1mdk

%define realname MySQL
%define modname mysql
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 34_%{modname}.ini
%define mod_src php_mysql.c
%define mod_lib "-lmysqlclient -lpthread -lcrypt -lz -lnsl -lm"
%define mod_def "-DCOMPILE_DL_MYSQL -DHAVE_MYSQL -DMYSQL_SOCK=\"/var/lib/mysql/mysql.sock\""
%define rlibs libmysql12 >= 4.0.10
%define blibs MySQL-devel >= 4.0.10

#########################################################
## Nothing to be changed after this, except changelog! ##
#########################################################

Summary:	The %{realname} module for PHP
Name:		php-%{modname}
Version:	%{phpversion}
Release:	%{release}
Group:		System/Servers
URL:		http://www.php.net
License:	PHP License
#Requires:	libphp_common%{libversion}
#Requires:	%{rlibs}
Requires:	php%{libversion}
BuildRequires:  php%{libversion}-devel
BuildRequires:	%{blibs}
BuildRoot:	%{_tmppath}/%{name}-root
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

cat > %{buildroot}%{_sysconfdir}/php/%{inifile} << EOF
extension = %{soname}
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ -e ./%{dirname} ] && rm -fr ./%{dirname}

%files 
%defattr(-,root,root)
%doc %{_docdir}/README
%{phpdir}/extensions/%{soname}
%config(noreplace) %{_sysconfdir}/php/%{inifile}

%changelog
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

* Wed Jun 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2
- misc spec file fixes

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-2mdk
- rebuild with new MySQL 4.0.10

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

* Tue Mar 05 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-2mdk
- Fixed error in description (it said pgsql). The module was built using
  php-pgsql as a template, and for all that time, nobody found the error.
  Congrats to Levi Ramsey <levi@haml-169.res.umass.edu> for pointing it out!

* Mon Mar 04 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-1mdk
- PHP 4.1.2

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-1mdk
- PHP 4.1.1.
- MySQL 3.23.47.

* Tue Dec 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-1mdk
- PHP 4.1.0.
- Updated MySQL name and version in Requires.

* Thu Nov 15 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-4mdk
- Fix no-url and invalid-packager warnings in rpmlint.
- Update MySQL version to 3.23.44.

* Mon Sep 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-3mdk
- s/Copyright/License/.
- Provides the Obsoletes for compatibility.

* Wed Jul 25 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-2mdk
- rebuild

* Fri Jun 29 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-1mdk
- 4.0.6

* Thu Apr 12 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-6mdk
- fix requires

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-5mdk
- fix post scripts for good 

* Mon Apr  2 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-4mdk
- Split mysql package from php package so that when a new mysql 
  package comes out, we don't have to recompile php, only this module
