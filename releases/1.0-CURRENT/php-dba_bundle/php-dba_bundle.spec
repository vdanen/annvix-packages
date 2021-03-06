%define name	php-%{modname}_bundle
%define version	%{phpversion}
%define release	3avx

%define phpversion	4.3.10
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define realname	dba (with cdb, gdbm and db4)
%define modname		dba
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		16_%{modname}.ini


Summary:	The %{realname} module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:  php4-devel
BuildRequires:	gdbm-devel db4-devel

Requires:	php4
Provides:       php-dba_gdbm_db2 php-cdb php-db2 php-db3 php-db3 php-db4
Obsoletes:      php-dba_gdbm_db2 php-cdb php-db2 php-db3 php-db3 php-db4

%description
The %{name} package is a dynamic shared object (DSO) that adds
%{realname} support to PHP. 
PHP is an HTML-embedded scripting language. 
If you need %{realname} support for PHP applications, 
you will need to install this package in addition to the php package.


%prep
%setup -c -T
cp -dpR %{_usrsrc}/php-devel/extensions/%{dirname}/* .

%build

#Keep this just in case phpize breaks sometime
#perl -pi -e 's|#include DB3_INCLUDE_FILE$|#include \"db.h"|g;' *db3.c
#perl -pi -e 's|#if ([A-Z_])|#ifdef \1|' *.{c,h}
#
#%{phpsource}/buildext db3 "dba.c dba_gdbm.c dba_db3.c dba_cdb.c" \
#	"-lm -lc -lgdbm -ldb-3.3 -lcdb" "-DHAVE_DBA -DCOMPILE_DL_DBA \
#	-DDBA_GDBM -DDBA_DB3 -DDB3_INCLUDE_FILE -DDBA_CDB"

phpize
%configure2_5x \
    --with-gdbm \
    --with-db4 \
    --with-cdb \
    --with-flatfile \
    --with-inifile \

%make
mv modules/*.so .

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{phpdir}/extensions/

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
* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 4.3.10-3avx
- spec cleanups

* Thu Feb 03 2005 Vincent Danen <vdanen@annvix.org> 4.3.10-2avx
- rebuild against new gdbm

* Thu Dec 16 2004 Vincent Danen <vdanen@annvix.org> 4.3.10-1avx
- php 4.3.10

* Wed Sep 29 2004 Vincent Danen <vdanen@annvix.org> 4.3.9-1avx
- php 4.3.9

* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
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

* Fri Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Mon Oct 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- 4.3.3

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-4mdk
- built for 4.3.3
- misc spec file fixes
- fix explicit-lib-dependency

* Sun Aug 24 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-3mdk
- rebuild against libdb4.1

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 4.3.2-2mdk
- Rebuild to fix bad signature

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild

* Thu Feb 20 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-4mdk
- fix requires

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-3mdk
- rebuild

* Thu Jan 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.0-2mdk
- added db4 support

* Sun Jan  5 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-1mdk
- New 4.3.0 release
- Totally macroize based on suggestions from Alexander Skwar
- New method of installing extensions thanks to Oden Eriksson
- Use phpize since it now works with this module
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3 maintenance release
- Do not reload apache

* Thu Aug 22 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.2-1mdk
- Rebuild for 4.2.2
- Macroize a bit more, make version depend on "php -v"

* Fri May 31 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-2mdk
- rebuild.

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.1

* Thu May 02 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-2mdk
- fix error in Prereq (thanks to Oden).

* Wed May 01 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- renamed the php-dba_gdbm_db3 package to php-dba_bundle
	- added cdb support
	- PHP 4.2.0

* Mon Mar 04 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-1mdk
- PHP 4.1.2

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-1mdk
- PHP 4.1.1.

* Tue Dec 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-1mdk
- PHP 4.1.0.

* Thu Oct 18 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-5mdk
- new db3

* Mon Sep 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-4mdk
- Provides the Obsoletes for compatibility.

* Tue Aug 28 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-3mdk
- s/libgdbm1/libgdbm2

* Fri Jul 13 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-2mdk
- rebuild against db3.2

* Wed Jul  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-1mdk
- 4.0.6
- s/Copyright/License/

* Thu Apr 12 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-6mdk
- fix requires

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-5mdk
- fix post scripts for good 

* Mon Apr  2 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-4mdk
- Split dba_gdbm_db3 package from php package so that when a new gdbm, db2
  or db3 package comes out, we don't have to recompile php, only this module


