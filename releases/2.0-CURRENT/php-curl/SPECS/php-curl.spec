#
# spec file for package php-curl
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

%define phpversion      5.1.2
%define phpsource       %{_prefix}/src/php-devel
%define phpdir          %{_libdir}/php

%define modname		curl
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		14_%{modname}.ini

Summary:	The Curl module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= 5.1.4
BuildRequires:	curl-devel >= 7.9.8

Requires:	php >= 5.1.2


%description
This is a dynamic shared object (DSO) for PHP that will add curl
support.

%prep
%setup -c -T
cp -dpR %{_usrsrc}/php-devel/extensions/%{dirname}/* .


%build
phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .
chrpath -d %{soname}


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
%doc CREDITS package.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{phpdir}/extensions/%{soname}


%changelog
* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- php 5.1.4

* Thu Mar 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- php 5.1.2
- stricter permissions and spec cleanups
- group is now Development/PHP

* Tue Mar 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- rebuild againt curl 7.15.3

* Wed Jan 18 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- php 4.4.2

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Nov 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-1avx
- first Annvix build to support the curl extensions in php
