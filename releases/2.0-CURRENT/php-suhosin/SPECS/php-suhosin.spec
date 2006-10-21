#
# spec file for package php-suhosin
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id: php-apc.spec 6207 2006-10-20 14:47:07Z vdanen $

%define revision	$Rev: 6207 $
%define name		php-%{modname}
%define version		0.9.8
%define release		%_revrel
%define epoch		1

%define phpversion	5.1.6
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
Source0:	%{modname}-%{version}.tgz
Source1:	%{modname}-%{version}.tgz.sig
Source2:	suhosin.ini

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

install -m 0644 %{_sourcedir}/suhosin.ini %{buildroot}%{_sysconfdir}/php.d/%{inifile}
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
* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
- first Annvix build of the suhosin extension (replaces the hardening patch)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
