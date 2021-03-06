#
# spec file for package php-pdo_sqlite
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
%define phpdir		%{_libdir}/php

%define modname		pdo_sqlite
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		77_%{modname}.ini

Summary:	SQLite v3 Interface driver for PDO
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= %{phpversion}
BuildRequires:	sqlite3-devel

Requires:	php-pdo

%description
PDO_SQLITE is a driver that implements the PHP Data Objects (PDO) interface to
enable access to SQLite 3 databases.

This extension provides an SQLite v3 driver for PDO. SQLite V3 is NOT
compatible with the bundled SQLite 2 in PHP 5, but is a significant step
forwards, featuring complete utf-8 support, native support for blobs, native
support for prepared statements with bound parameters and improved concurrency.
This is an extension for the SQLite Embeddable SQL Database Engine. SQLite is a
C library that implements an embeddable SQL database engine. Programs that link
with the SQLite library can have SQL database access without running a separate
RDBMS process.


%prep
%setup -c -T -q
cp -dpR %{phpsource}/extensions/%{dirname}/* .
ln -s %{_usrsrc}/php-devel/ext .


%build
phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}


%make
mv modules/*.so .


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF


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

* Wed Feb 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- php 5.2.1

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0 
- php 5.2.0

* Tue Nov 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
