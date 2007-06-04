#
# spec file for package php-pdo
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

%define phpversion	5.2.3
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		pdo
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		70_%{modname}.ini

Summary:	PHP Data Objects Interface
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= %{phpversion}

Requires:	php

%description
PDO provides a uniform data access interface, sporting advanced features such
as prepared statements and bound parameters. PDO drivers are dynamically
loadable and may be developed independently from the core, but still accessed
using the same API.

Read the documentation at http://www.php.net/pdo for more information.


%prep
%setup -c -T -q
cp -dpR %{phpsource}/extensions/%{dirname}/* .

# anti pdo hack
mkdir -p ext
cp -rp %{_usrsrc}/php-devel/ext/session ext/


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
