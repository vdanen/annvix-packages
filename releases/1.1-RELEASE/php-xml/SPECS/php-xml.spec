#
# spec file for package php-xml
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		php-%{modname}
%define version		%{phpversion}
%define release		1avx

%define phpversion	4.4.1
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define realname	XML
%define modname		xml
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		52_%{modname}.ini
%define mod_src		xml.c
%define mod_lib		"-lexpat"
%define mod_def		"-DCOMPILE_DL_XML -DHAVE_LIBEXPAT -DHAVE_DLFCN_H"

Summary:	The %{realname} module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php4-devel
BuildRequires:	expat-devel

Requires:	php4

%description
The %{name} package is a dynamic shared object (DSO) that adds
%{realname} support to PHP. PHP is an HTML-embedded scripting language. 
If you need %{realname} support for PHP applications, you will need to 
install this package in addition to the php package.


%prep
%setup -c -T
cp -dpR %{phpsource}/extensions/%{dirname}/* .


%build
phpize
export XML_SHARED_LIBADD="$XML_SHARED_LIBADD -lexpat"
export CPPFLAGS="$CPPFLAGS -DHAVE_LIBXML -DHAVE_XML -DHAVE_LIBEXPAT"
%configure2_5x \
  --with-expat-dir=%{_prefix}

%make
mv modules/*.so .


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
* Wed Nov 02 2005 Vincent Danen <vdanen@annvix.org> 4.4.1-1avx
- php 4.4.1

* Sat Oct 29 2005 Vincent Danen <vdanen@annvix.org> 4.4.0-3avx
- fix linking to libxml and libexpat

* Fri Sep 16 2005 Vincent Danen <vdanen@annvix.org> 4.4.0-2avx
- rebuild against new expat

* Wed Sep 14 2005 Vincent Danen <vdanen@annvix.org> 4.4.0-1avx
- php 4.4.0

* Fri Aug 19 2005 Vincent Danen <vdanen@annvix.org> 4.3.11-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 4.3.11-2avx
- rebuild

* Sat May 14 2005 Vincent Danen <vdanen@annvix.org> 4.3.11-1avx
- php 4.3.11

* Sat Mar 05 2005 Vincent Danen <vdanen@annvix.org> 4.3.10-3avx
- rebuild for new libxml2 and libxslt

* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 4.3.10-2avx
- spec cleanups

* Fri Dec 17 2004 Vincent Danen <vdanen@annvix.org> 4.3.10-1avx
- php 4.3.10

* Thu Sep 30 2004 Vincent Danen <vdanen@annvix.org> 4.3.9-1avx
- php 4.3.9

* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
- use phpize (oden)
- use the %%configure2_5x macro (oden)
- move scandir to /etc/php.d
- own docdir

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- php 4.3.7

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- php 4.3.6

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-3sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Mon Oct 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- 4.3.3

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-3mdk
- built for 4.3.3
- fix explicit-lib-dependency
- misc spec file fixes

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 4.3.2-2mdk
- Rebuild to fix bad signature

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-2mdk
- rebuild

* Sun Jan  5 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-1mdk
- New 4.3.0 release
- Totally macroize based on suggestions from Alexander Skwar
- New method of installing extensions thanks to Oden Eriksson
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3 maintenance release
- Do not reload apache

* Thu Aug 22 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.2-1mdk
- Rebuild for 4.2.2
- Macroize a bit more, make version depend on "php -v"

* Sun May 26 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-2mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.1

* Mon Apr 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- misc spec file fixes
	- PHP 4.2.0

* Mon Mar 02 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-1mdk
- Moved the XML functionnality into this php-xml package to get rid of
  segfault problems with different expat libraries statically linked into
  different parts of Apache.
