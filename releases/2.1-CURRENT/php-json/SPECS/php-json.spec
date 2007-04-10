#
# spec file for package php-json
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		php-%{modname}
%define version		1.2.1
%define release		%_revrel

%define phpversion	5.2.1
%define phpsource       %{_prefix}/src/php-devel
%define phpdir          %{_libdir}/php

%define modname		json
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		82_%{modname}.ini

Summary:	JavaScript Object Notation module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://pecl.php.net/package/%{modname}/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= %{phpversion}


%description
Support for JSON (JavaScript Object Notation) serialization.


%prep
%setup -q -n %{modname}-%{version}
[ "../package.xml" != "/" ] && mv ../package.xml .


%build
phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so %{soname}


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

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
