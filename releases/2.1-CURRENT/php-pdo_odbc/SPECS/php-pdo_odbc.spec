#
# spec file for package php-pdo_odbc
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

%define phpversion	5.2.1
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		pdo_odbc
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		75_%{modname}.ini

Summary:	ODBC Interface driver for PDO
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= %{phpversion}
BuildRequires:	unixODBC-devel

Requires:	php-pdo

%description
PDO_ODBC is a driver that implements the PHP Data Objects (PDO) interface to
enable access from PHP to databases through ODBC drivers or through the IBM DB2
Call Level Interface (DB2 CLI) library. PDO_ODBC currently supports three
different "flavours" of database drivers:

 o ibm-db2  - Supports access to IBM DB2 Universal Database, Cloudscape, and
              Apache Derby servers through the free DB2 client. ibm-db2 is not
              supported in Mandriva.

 o unixODBC - Supports access to database servers through the unixODBC driver
              manager and the database's own ODBC drivers.

 o generic  - Offers a compile option for ODBC driver managers that are not
              explicitly supported by PDO_ODBC.


%prep
%setup -c -T -q
cp -dpR %{phpsource}/extensions/%{dirname}/* .
ln -s %{_usrsrc}/php-devel/ext .


%build
phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-pdo-odbc=unixODBC,%{_prefix}


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
* Wed Feb 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- php 5.2.1

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0 
- php 5.2.0

* Tue Nov 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
