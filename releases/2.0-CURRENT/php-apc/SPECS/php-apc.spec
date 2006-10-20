#
# spec file for package php-apc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		php-%{modname}
%define version		3.0.10
%define release		%_revrel
%define epoch		1

%define phpversion	5.1.6
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		apc
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		99_%{modname}.ini

%define _requires_exceptions	pear(

Summary:	The apc (Alternative PHP Cache) module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	PHP License
Group:		Development/PHP
URL:		http://pecl.php.net/package/APC
Source0:	APC-%{version}.tgz
Source1:	apc.ini

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= 5.1.4

Requires:	php
Conflicts:	php-afterburner php-mmcache

%description
APC was conceived of to provide a way of boosting the performance
of PHP on heavily loaded sites by providing a way for scripts to
be cached in a compiled state, so that the overhead of parsing and
compiling can be almost completely eliminated. There are
commercial products which provide this functionality, but they are
neither open-source nor free. Our goal was to level the playing
field by providing an implementation that allows greater
flexibility and is universally accessible. 

We also wanted the cache to provide visibility into it's own
workings and those of PHP, so time was invested in providing
internal diagnostic tools which allow for cache diagnostics and
maintenance. 

Thus arrived APC. Since we were committed to developing a product
which can easily grow with new version of PHP, we implemented it
as a zend extension, allowing it to either be compiled into PHP or
added post facto as a drop in module. As with PHP, it is available
completely free for commercial and non-commercial use, under the
same terms as PHP itself. 

NOTE!: %{name} has to be loaded last, very important!


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n APC-%{version}


%build
phpize
%configure2_5x \
    --enable-%{modname}=shared,%{_prefix} \
    --enable-apc-mmap

%make
mv modules/*.so .


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat %{SOURCE1} > %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml


%files 
%defattr(-,root,root)
%attr(0755,root,root) %{phpdir}/extensions/%{soname}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}

%files doc
%defattr(-,root,root)
%doc CHANGELOG INSTALL NOTICE TODO apc.php


%changelog
* Fri Oct 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.10
- php 5.1.6+suhosin
- revert previous change

* Fri Oct 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.10
- move the apc ini position from 99 to 98

* Tue Jul 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.10
- set apc.user_ttl to 7200
- set apc.mmap_file_mask to /tmp/apc.XXXXXX
- include apc.php in the doc package

* Sun Jun 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.10
- add -doc subpackage
- fix changelog versioning

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.10
- php 5.1.4
- cleanup config

* Wed Apr 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.10
- php 5.1.2
- APC 3.0.10
- stricter permissions and spec cleanups
- group is now Development/PHP

* Mon Feb 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8
- APC 3.0.8
- fix versioning and give it an epoch

* Wed Jan 18 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2_2.0.4
- php 4.4.2

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1_2.0.4
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1_2.0.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Nov 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1_2.0.4-1avx
- php 4.4.1

* Wed Sep 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0_2.0.4-1avx
- php 4.4.0

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11_2.0.4-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11_2.0.4-2avx
- rebuild

* Sat May 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11_2.0.4-1avx
- php 4.3.11

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10_2.0.4-2avx
- rebuild and cleanups

* Thu Dec 16 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10_2.0.4-1avx
- php 4.3.10

* Thu Sep 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.9_2.0.4-1avx
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
