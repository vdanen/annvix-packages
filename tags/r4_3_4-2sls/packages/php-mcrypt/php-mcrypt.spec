%define name	php-%{modname}
%define version	%{phpversion}
%define release	2sls

%define phpsource	%{_prefix}/src/php-devel
%define _docdir		%{_datadir}/doc/%{name}-%{version}
%{expand:%(cat /usr/src/php-devel/PHP_BUILD||(echo -e "error: failed build dependencies:\n        php-devel >= 430 (4.3.0) is needed by this package." >/dev/stderr;kill -2 $PPID))}

%define realname	MCRYPT
%define modname		mcrypt
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		29_%{modname}.ini
%define mod_src		%{modname}.c
%define rlibs		libmcrypt4 libltdl3
%define blibs		libmcrypt4-devel libltdl3-devel

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

# version hack :)
if [[ -x %{_bindir}/libmcrypt-config ]]; then
    MCRYPT_VERSION=`%{_bindir}/libmcrypt-config --version`
    perl -p -i -e "s|\"version\", \">= 2.4.x\"|\"Version\", \"$MCRYPT_VERSION\"|g" %{mod_src}
else
    echo "%{_bindir}/libmcrypt-config not found, version hack not possible..."
fi

phpize
%configure --with-mcrypt
%make
mv modules/*.so .

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

[mcrypt]
;mcrypt.algorithms_dir = 
;mcrypt.modes_dir = 
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ -e ./%{dirname} ] && rm -fr ./%{dirname}

%files 
%defattr(-,root,root)
%doc %{_docdir}
%{phpdir}/extensions/%{soname}
%config(noreplace) %{_sysconfdir}/php/%{inifile}

%changelog
* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Wed Aug 27 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- built for php 4.3.3
- misc spec file fixes

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Wed Feb 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- rebuilt against php-4.3.1

* Sun Jan 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-3mdk
- really rebuilt against rebuilt buildrequires

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-2mdk
- rebuilt against rebuilt buildrequires

* Fri Jan 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-1mdk
- built against php-4.3.0
- built against new libmcrypt
- follow the spec file design as in main

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.3-2mdk
- rebuilt against latest BuildRequires

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3 maintenance release
- Do not reload apache

* Thu Aug 22 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.2-1mdk
- Rebuild for 4.2.2
- Macroize a bit more, make version depend on "php -v"

* Sat Jun  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.1-4mdk
- rebuilt against latest BuildRequires

* Mon May 27 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.1-3mdk
- rebuilt against php-4.2.1 this time (klama is wierd...)
- added Requires: php-common

* Mon May 27 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.1-2mdk
- misc spec file fixes

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.1

* Sun May 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.0-3mdk
- rebuilt with gcc3.1
- misc spec file fixes

* Tue May  7 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.0-2mdk
- misc spec file fixes

* Mon Apr 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- misc spec file fixes
	- added my version hack :)
	- initial cooker contrib
	- PHP 4.2.0
