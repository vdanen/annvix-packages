#
# spec file for package php-imap
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

%define phpversion	5.2.0
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		imap
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		26_%{modname}.ini
%define mod_src		php_imap.c

Summary:	The IMAP module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net
Source0:	ftp://ftp.cac.washington.edu/mail/imap-2002d.tar.bz2
Source1:	flock.c
Patch0: 	imap-2001a-ssl.patch
Patch1: 	imap-2000-linux.patch
Patch2:		imap-2001a-disable-mbox.patch
Patch3:		imap-2001a-redhat.patch
Patch4: 	imap-2000c-flock.patch
Patch5: 	imap-2002d-version.patch
Patch6:		imap-2000-glibc-2.2.2.patch
Patch7:		imap-2002a-ssldocs.patch
Patch8:		imap-2001a-overflow.patch
Patch9:		imap-2002a-ansi.patch
Patch10:	imap-2002a-noprompt-makefile.patch
Patch11:	imap-2002d-CAN-2005-2933.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= %{phpversion}
BuildRequires:	pam-devel >= 0.75
BuildRequires:	openssl-devel

Requires:	php >= %{phpversion}

%description
This is a dynamic shared object (DSO) for PHP that will add IMAP
support.


%prep
%setup -q -n imap-2002d

rm -rf RCS

%patch0 -p1 -b .ssl
%patch1 -p1 -b .linxu
%patch2 -p1 -b .mbox
%patch3 -p1 -b .redhat
%patch4 -p1 -b .flock
%patch5 -p1 -b .version
cp %{_sourcedir}/flock.c src/osdep/unix/
%patch6 -p1 -b .glibc
%patch7 -p1
%patch8 -p1 -b .overflow
%patch9 -p1 -b .ansi
%patch10 -p1 -b .noprompt
%patch11 -p1 -b .can-2005-2933


%build
# first build the static imap lib

EXTRACFLAGS="$EXTRACFLAGS -DDISABLE_POP_PROXY=1"
EXTRACFLAGS="$EXTRACFLAGS -I%{_includedir}/openssl"
EXTRALDFLAGS="$EXTRALDFLAGS -L%{_libdir}"

%make RPM_OPT_FLAGS="%{optflags} -fPIC -fno-omit-frame-pointer" \
    EXTRACFLAGS="$EXTRACFLAGS" \
    EXTRALDFLAGS="$EXTRALDFLAGS" \
    SSLTYPE=unix.nopwd \
    lnp

# then the php-imap stuff

cp -dpR %{phpsource}/extensions/%{dirname}/* .

%{phpsource}/buildext %{modname} %{mod_src} \
    "./c-client/c-client.a -lpam -lcrypto -lssl" \
    "-DCOMPILE_DL_IMAP -DHAVE_IMAP2001 -DHAVE_IMAP_SSL -I%{_includedir}/openssl -I./src/c-client -I./c-client"


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
* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0 
- php 5.2.0

* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- php 5.1.6+suhosin
- drop S2 (unused)
- drop P11 (unapplied)
- renumber patches

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new openssl
- spec cleanups

* Sun Jun 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new pam

* Sun Jun 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- remove docs

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- php 5.1.4

* Thu Mar 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- php 5.1.2
- stricter permissions and spec cleanups
- group is now Development/PHP

* Wed Jan 18 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- php 4.4.2

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Nov 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-1avx
- php 4.4.1

* Mon Oct 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-2avx
- P16: patch the c-client libs to fix CAN-2005-2933

* Wed Sep 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-1avx
- php 4.4.0

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-2avx
- rebuild

* Sat May 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-1avx
- php 4.3.11

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-3avx
- spec cleanups

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-2avx
- rebuild against latest openssl

* Fri Dec 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-1avx
- php 4.3.10

* Thu Sep 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.9-1avx
- php 4.3.9

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-2avx
- rebuild against new openssl

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
- move scandir to /etc/php.d
- own docdir

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- php 4.3.7

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- php 4.3.6

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-4sls
- minor spec cleanups
- fixes to make imap compile properly

* Wed Dec 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-3sls
- built against provided c-client

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
