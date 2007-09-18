#
# spec file for package php-odbc
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

%define modname		odbc
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		39_%{modname}.ini

Summary:	The ODBC module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net
Source0:	odbc.ini

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= %{phpversion}
BuildRequires:	unixODBC-devel

Requires:	php

%description
This is a dynamic shared object (DSO) for PHP that will add ODBC
support.

In addition to normal ODBC support, the Unified ODBC functions in PHP allow you
to access several databases that have borrowed the semantics of the ODBC API to
implement their own API. Instead of maintaining multiple database drivers that
were all nearly identical, these drivers have been unified into a single set of
ODBC functions.


%prep
%setup -c -T -q
cp -dpR %{phpsource}/extensions/%{dirname}/* .


%build
phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-unixODBC=shared,%{_prefix}

%make
mv modules/*.so .
chrpath -d %{modname}.so


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/

install -m 0644 %{_sourcedir}/odbc.ini %{buildroot}%{_sysconfdir}/php.d/%{inifile}


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

* Sat Feb 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0 
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
