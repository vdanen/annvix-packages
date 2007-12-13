#
# spec file for package php-suhosin
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		php-%{modname}
%define version		0.9.22
%define release		%_revrel
%define epoch		1

%define phpversion	5.2.5
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		suhosin
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		98_%{modname}.ini

Summary:	The Suhosin module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	PHP License
Group:		Development/PHP
URL:		http://www.hardened-php.net/suhosin/
Source0:	http://www.hardened-php.net/suhosin/_media/suhosin-%{version}.tgz
Source1:	http://www.hardened-php.net/suhosin/_media/suhosin-%{version}.tgz.sig

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= %{phpversion}

#Requires:	php-pdo >= %{phpversion}

%description
Suhosin is an advanced protection system for PHP installations. It was designed
to protect servers and users from known and unknown flaws in PHP applications
and the PHP core. Suhosin is binary compatible to normal PHP installation,
which means it is compatible to 3rd party binary extension like ZendOptimizer.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{modname}-%{version}


%build
%serverbuild

phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so %{modname}.so


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m 0644 suhosin.ini %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%attr(0755,root,root) %{phpdir}/extensions/%{soname}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}

%files doc
%defattr(-,root,root)
%doc CREDITS tests Changelog


%changelog
* Wed Dec 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.22
- 0.9.22
- php 5.2.5

* Wed Sep 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.20
- php 5.2.4
- use %%serverbuild

* Mon Jun 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.20
- rebuild with SSP

* Sun Jun 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.20
- php 5.2.3

* Mon May 28 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.20
- 0.9.20

* Fri May 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.19
- 0.9.19
- php 5.2.2
- use the bundled suhosin.ini instead of our own (essentially identical)

* Mon Mar 05 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.17
- 0.9.17

* Wed Feb 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.16
- php 5.2.1

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.16
- 0.9.16
- php 5.2.0
- documented suhosin.ini

* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
- first Annvix build of the suhosin extension (replaces the hardening patch)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
