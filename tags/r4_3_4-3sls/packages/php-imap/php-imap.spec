%define name	php-%{modname}
%define version	%{phpversion}
%define release	3sls

%define phpsource	%{_prefix}/src/php-devel
%define _docdir		%{_datadir}/doc/%{name}-%{version}
%{expand:%(cat /usr/src/php-devel/PHP_BUILD||(echo -e "error: failed build dependencies:\n        php-devel >= 430 (4.3.0) is needed by this package." >/dev/stderr;kill -2 $PPID))}

%define realname	IMAP
%define modname		imap
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		26_%{modname}.ini
%define mod_src		php_imap.c

Summary:	The %{realname} module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net
Source0:	ftp://ftp.cac.washington.edu/mail/imap-2002d.tar.bz2
Source7:	flock.c
Source8:	Makefile.imap.bz2
Patch0: 	imap-2001a-ssl.patch.bz2
Patch1: 	imap-2000-linux.patch.bz2
Patch3:		imap-2001a-disable-mbox.patch.bz2
Patch4:		imap-2001a-redhat.patch.bz2
Patch5: 	imap-2000c-flock.patch.bz2
Patch7: 	imap-2002d-version.patch.bz2
Patch9:		imap-2000-glibc-2.2.2.patch.bz2
Patch10:	imap-2002a-ssldocs.patch.bz2
Patch11:	imap-2002-krbpath.patch.bz2
Patch12:	imap-2001a-overflow.patch.bz2
Patch14:	imap-2002a-ansi.patch.bz2
Patch15:	imap-2002a-noprompt-makefile.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:  php%{libversion}-devel
BuildRequires:	pam-devel >= 0.75
BuildRequires:	openssl-devel

Requires:	php%{libversion}
Provides: 	ADVXpackage

%description
The %{name} package is a dynamic shared object (DSO) that adds
%{realname} support to PHP. PHP is an HTML-embedded scripting language. 
If you need %{realname} support for PHP applications, you will need to 
install this package in addition to the php package.

%prep

%setup -q -n imap-2002d

rm -rf RCS

%patch0 -p1 -b .ssl
%patch1 -p1 -b .linxu
%patch3 -p1 -b .mbox
%patch4 -p1 -b .redhat
%patch5 -p1 -b .flock
%patch7 -p1 -b .version
cp %{SOURCE7} src/osdep/unix/
%patch9 -p1 -b .glibc
%patch10 -p1
%patch12 -p1 -b .overflow
%patch14 -p1 -b .ansi
%patch15 -p1 -b .noprompt

%build

# first build the static imap lib

EXTRACFLAGS="$EXTRACFLAGS -DDISABLE_POP_PROXY=1"
EXTRACFLAGS="$EXTRACFLAGS -I%{_includedir}/openssl"
EXTRALDFLAGS="$EXTRALDFLAGS -L%{_libdir}"

%make RPM_OPT_FLAGS="%{optflags} -fPIC -fno-omit-frame-pointer" lnp \
	EXTRACFLAGS="$EXTRACFLAGS" \
	EXTRALDFLAGS="$EXTRALDFLAGS" \
	SSLTYPE=unix \
	c-client

# then the php-imap stuff

cp -dpR %{phpsource}/extensions/%{dirname}/* .

%{phpsource}/buildext %{modname} %{mod_src} \
    "./c-client/c-client.a -lpam -lcrypto -lssl" \
    "-DCOMPILE_DL_IMAP -DHAVE_IMAP2001 -DHAVE_IMAP_SSL -I%{_includedir}/openssl -I./src/c-client -I./c-client"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_docdir}
install -d %{buildroot}%{_sysconfdir}/php

install -m755 %{soname} %{buildroot}%{phpdir}/extensions/

cat > %{buildroot}%{_docdir}/README <<EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
To activate it, make sure a file /etc/php/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php/%{inifile} << EOF
extension = %{soname}
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc %{_docdir}/README
%{phpdir}/extensions/%{soname}
%config(noreplace) %{_sysconfdir}/php/%{inifile}

%changelog
* Wed Dec 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-3sls
- built against provided c-client

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Mon Oct 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- 4.3.3

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-3mdk
- built for 4.3.3
- misc spec file fixes
- fix explicit-lib-dependency

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 4.3.2-2mdk
- Rebuild to fix bad signature

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild
- misc spec file fixes

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-3mdk
- rebuild

* Sat Jan 18 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-2mdk
- rebuilt with new openssl

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

* Thu May 02 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- misc spec file fixes
	- PHP 4.2.0

* Mon Mar 04 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-1mdk
- PHP 4.1.2

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-1mdk
- PHP 4.1.1.

* Mon Dec 17 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-2mdk
- Removed IMAP from Requires.

* Tue Dec 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-1mdk
- PHP 4.1.0.
- Added version check for pam in Requires.

* Fri Nov 16 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-3mdk
- Fix invalid-packager and no-url-tag warnings in rpmlint.

* Mon Sep 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-2mdk
- Provides the Obsoletes for compatibility.

* Wed Jul  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-1mdk
- 4.0.6
- s/Copyright/License/

* Thu Apr 12 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-6mdk
- fix requires

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-5mdk
- fix post scripts for good 

* Mon Apr  2 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-4mdk
- Split imap package from php package so that when a new imap 
  package comes out, we don't have to recompile php, only this module
