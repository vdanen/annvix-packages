#
# spec file for package php-mbstring
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		php-%{modname}
%define version		%{phpversion}
%define release		%_revrel

%define phpversion	5.1.4
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		mbstring
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		29_%{modname}.ini

Summary:	The mbstring module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net
Source0:	php-mbstring.ini

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= 5.1.4

Requires:	php

%description
This is a dynamic shared object (DSO) for PHP that will add multibyte
string support.


%prep
%setup -c -T
cp -dpR %{phpsource}/extensions/%{dirname}/* .


%build
phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix} \
    --enable-mbregex

%make
mv modules/*.so .


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/

install -m 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/php.d/%{inifile}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{phpdir}/extensions/%{soname}


%changelog
* Sun Jun 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- remove docs

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- php 5.1.4
- update config with mbstring.stric_encoding setting

* Mon Apr 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- fix summary

* Sun Apr 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
