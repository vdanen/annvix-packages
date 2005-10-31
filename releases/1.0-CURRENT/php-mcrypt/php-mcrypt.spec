%define name	php-%{modname}
%define version	%{phpversion}
%define release	2avx

%define phpversion	4.3.10
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define realname	MCRYPT
%define modname		mcrypt
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		29_%{modname}.ini
%define mod_src		%{modname}.c

Summary:	The %{realname} module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:  php4-devel
BuildRequires:	libmcrypt-devel, libtool-devel

Requires:	php4

%description
The %{name} package is a dynamic shared object (DSO) that adds
%{realname} support to PHP. PHP is an HTML-embedded scripting language. 
If you need %{realname} support for PHP applications, you will need to 
install this package in addition to the php package.


%prep
%setup -c -T
cp -dpR %{phpsource}/extensions/%{dirname}/* .

%build

# version hack :)
if [[ -x %{_bindir}/libmcrypt-config ]]; then
    MCRYPT_VERSION=`%{_bindir}/libmcrypt-config --version`
    perl -p -i -e "s|\"version\", \">= 2.4.x\"|\"Version\", \"$MCRYPT_VERSION\"|g" %{mod_src}
else
    echo "%{_bindir}/libmcrypt-config not found, version hack not possible..."
fi

phpize
%configure2_5x \
  --with-mcrypt

%make
mv modules/*.so .

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{phpdir}/extensions/

cat > README.%{modname} <<EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
To activate it, make sure a file /etc/php.d/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[mcrypt]
;mcrypt.algorithms_dir = 
;mcrypt.modes_dir = 
EOF

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README*
%config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%{phpdir}/extensions/%{soname}

%changelog
* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 4.3.10-2avx
- spec cleanups

* Fri Dec 17 2004 Vincent Danen <vdanen@annvix.org> 4.3.10-1avx
- php 4.3.10

* Thu Sep 30 2004 Vincent Danen <vdanen@annvix.org> 4.3.9-1avx
- php 4.3.9

* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
- use %%configure2_5x macro (oden)
- fix invalid BuildRequires (oden)
- move scandir to /etc/php.d
- own docdir

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- php 4.3.7

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- php 4.3.6

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-4sls
- minor spec cleanups

* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-3sls
- change requires from libmcrypt4(-devel) to libmcrypt(-devel) and
  libltdl3(-devel) to libltdl(-devel) to be amd64 nice

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
