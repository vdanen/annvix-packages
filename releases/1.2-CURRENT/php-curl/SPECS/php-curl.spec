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

%define phpversion      4.4.1
%define phpsource       %{_prefix}/src/php-devel
%define phpdir          %{_libdir}/php

%define realname	Curl
%define modname		curl
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		14_%{modname}.ini
%define mod_src		php_mysql.c
%define mod_lib		"-lcurl -lssl -lcrypto -ldl"
%define mod_def		"-DCOMPILE_DL_CURL -DHAVE_CURL"

Summary:	The %{realname} module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php4-devel
BuildRequires:	curl-devel >= 7.9.8, openssl-devel

Requires:	php4


%description
The %{name} package is a dynamic shared object (DSO) that adds
%{realname} support to PHP. PHP is an HTML-embedded scripting language. 
If you need %{realname} support for PHP applications, you will need to 
install this package in addition to the php package.


%prep
%setup -c -T
cp -dpR %{_usrsrc}/php-devel/extensions/%{dirname}/* .


%build
phpize
%configure2_5x \
  --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .
chrpath -d %{soname}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/

cat > README.%{modname} <<EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
To activate it, make sure a file /etc/php.d/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%doc README*
%config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%{phpdir}/extensions/%{soname}


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Nov 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-1avx
- first Annvix build to support the curl extensions in php
