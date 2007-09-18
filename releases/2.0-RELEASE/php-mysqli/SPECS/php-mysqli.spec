#
# spec file for package php-mysqli
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

%define phpversion	5.2.4
%define phpsource       %{_prefix}/src/php-devel
%define phpdir          %{_libdir}/php

%define modname		mysqli
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		37_%{modname}.ini

Summary:	The MySQL 4.1+ module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net
Source0:	php-mysqli.ini

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= %{phpversion}
BuildRequires:	mysql-devel >= 4.1.14

Requires:	php


%description
This is a dynamic shared object (DSO) for PHP that will add improved
MySQL 4.1.x (and higher) database support.  For older versions of
MySQL, use php-mysql instead.


%prep
%setup -c -T -q
cp -dpR %{_usrsrc}/php-devel/extensions/%{dirname}/* .


%build
phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-mysqli=%{_bindir}/mysql_config

%make
mv modules/*.so .


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/
install -m 0644 %{_sourcedir}/php-mysqli.ini %{buildroot}%{_sysconfdir}/php.d/%{inifile}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{phpdir}/extensions/%{soname}


%changelog
* Tue Sep 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.4
- php 5.2.4

* Sun Jun 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.3
- php 5.2.3

* Fri May 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.2
- php 5.2.2

* Tue Feb 27 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- don't provide/obsolete php-mysql; we added it back

* Wed Feb 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- php 5.2.1

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0 
- php 5.2.0
- provide and obsolete php-mysql (to ease upgrades from 1.2)

* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- php 5.1.6+suhosin

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new mysql
- spec cleanups

* Sun Jun 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- remove docs

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- php 5.1.4

* Sun Apr 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
