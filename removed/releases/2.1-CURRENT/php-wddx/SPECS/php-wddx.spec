#
# spec file for package php-wddx
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

%define phpversion	5.2.2
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		wddx
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		63_%{modname}.ini

Summary:	The WDDX module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net
Requires:	php-xml

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= %{phpversion}
BuildRequires:	expat-devel

Requires:	php

%description
This is a dynamic shared object (DSO) for PHP that will add wddx
support.


%prep
%setup -c -T -q
cp -dpR %{phpsource}/extensions/%{dirname}/* .
ln -s %{phpsource}/extensions ext


%build
%{phpsource}/buildext \
    %{modname} \
    %{modname}.c \
    "-L%{_libdir} -lexpat" \
    "-DCOMPILE_DL_WDDX -DHAVE_WDDX -DHAVE_PHP_SESSION -I%{_includedir}/php/ext/date/lib"


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
* Fri May 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.2
- php 5.2.2

* Wed Feb 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- php 5.2.1

* Sat Feb 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0 
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
