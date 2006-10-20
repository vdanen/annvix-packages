#
# spec file for package php-bz2
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

%define phpversion	5.1.6
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		bz2
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		10_%{modname}.ini

Summary:	The bzip2 module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= 5.1.4
BuildRequires:	bzip2-devel

Requires:	php

%description
This is a dynamic shared object (DSO) for PHP that will add bzip2
compression support.


%prep
%setup -c -T
cp -dpR %{phpsource}/extensions/%{dirname}/* .


%build
export CPPFLAGS="-DCOMPILE_DL_BZ2 -DHAVE_BZ2"

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
* Fri Oct 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- php 5.1.6+suhosin

* Sun Jun 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- remove docs

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- php 5.1.4

* Sun Apr 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
