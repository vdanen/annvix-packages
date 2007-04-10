#
# spec file for package shadow-utils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		shadow-utils
%define version		4.0.12
%define release		%_revrel
%define epoch		1

#rh-20000902-10
%define _unpackaged_files_terminate_build 0

Summary:	Utilities for managing shadow password files and user/group accounts
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	BSD
Group:		System/Base
URL:		http://shadow.pld.org.pl/
Source0:	ftp://ftp.pld.org.pl/software/shadow/shadow-%{version}.tar.bz2
Source1:	login.defs
Source2:	useradd.default
Source3:	chpasswd-newusers.pamd
Source4:	chage-chfn-chsh.pamd
Source5:	user-group-mod.pamd
Patch0:		shadow-4.0.12-mdk.patch
Patch1:		shadow-4.0.12-nscd.patch
Patch2:		shadow-4.0.3-rpmsave.patch
Patch3:		shadow-4.0.11.1-no-syslog-setlocale.patch
Patch4:		shadow-4.0.12-avx-alt-man.patch
Patch6:		shadow-4.0.12-avx-owl-crypt_gensalt.patch
Patch7:		shadow-4.0.12-avx-owl-usergroupname_max.patch
Patch8:		shadow-4.0.12-avx-owl-tcb.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	tcb-devel
BuildRequires:	glibc-crypt_blowfish-devel
BuildRequires:	pam_userpass-devel
BuildRequires:  automake1.7

Requires:	pam
Requires:	tcb
Requires:	pam_userpass
Requires(pre):	setup >= 2.5-5873avx
Obsoletes:	adduser
Obsoletes:	newgrp
Provides: 	adduser
Provides:	newgrp

%description
The shadow-utils package includes the necessary programs for
converting UNIX password files to the shadow password format, plus
programs for managing user and group accounts.  The pwconv command
converts passwords to the shadow password format.  The pwunconv command
unconverts shadow passwords and generates an npasswd file (a standard
UNIX password file).  The pwck command checks the integrity of
password and shadow files.  The lastlog command prints out the last
login times for all users.  The useradd, userdel and usermod commands
are used for managing user accounts.  The groupadd, groupdel and
groupmod commands are used for managing group accounts.

This package contains support for both traditional shadow and tcb
password files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n shadow-%{version}
%patch0 -p1 -b .mdk
%patch1 -p1 -b .nscd
%patch2 -p1 -b .rpmsave
%patch3 -p1 -b .chmou
%patch4 -p1 -b .man
%patch6 -p1 -b .crypt_gensalt
%patch7 -p1 -b .usergroupname_max
%patch8 -p1 -b .tcb

echo ".so man8/useradd.8" >man/adduser.8


%build
libtoolize --copy --force; aclocal; autoconf; automake
CFLAGS="%{optflags} -DSHADOWTCB -DEXTRA_CHECK_HOME_DIR" \
%configure \
    --disable-shared \
    --disable-desrpc \
    --with-libcrypt \
    --with-libpam \
    --without-libcrack
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std gnulocaledir=%{buildroot}%{_datadir}/locale MKINSTALLDIRS=`pwd`/mkinstalldirs

mkdir -p %{buildroot}%{_sysconfdir}/default
mkdir -p %{buildroot}%{_mandir}/man3
install -m 0644 %{_sourcedir}/login.defs %{buildroot}%{_sysconfdir}/login.defs
install -m 0600 %{_sourcedir}/useradd.default %{buildroot}%{_sysconfdir}/default/useradd
install -m 0644 man/shadow.3 %{buildroot}%{_mandir}/man3/shadow.3
install -m 0644 man/adduser.8 %{buildroot}%{_mandir}/man8/

ln -s useradd %{buildroot}%{_sbindir}/adduser
perl -pi -e "s/encrpted/encrypted/g" %{buildroot}%{_mandir}/man8/newusers.8

mkdir -p %{buildroot}/etc/pam.d/
pushd %{buildroot}/etc/pam.d
    install -m 0600 %{_sourcedir}/chpasswd-newusers.pamd chpasswd-newusers
    ln -s chpasswd-newusers chpasswd
    ln -s chpasswd-newusers newusers
    install -m 0600 %{_sourcedir}/chage-chfn-chsh.pamd chage-chfn-chsh
    ln -s chage-chfn-chsh chage
    ln -s chage-chfn-chsh chfn
    ln -s chage-chfn-chsh chsh
    install -m 0600 %{_sourcedir}/user-group-mod.pamd  user-group-mod
    ln -s user-group-mod groupadd
    ln -s user-group-mod groupdel
    ln -s user-group-mod groupmod
    ln -s user-group-mod useradd
    ln -s user-group-mod userdel
    ln -s user-group-mod usermod
popd

# remove unwanted files
rm -rf %{buildroot}%{_libdir}
%kill_lang shadow
%find_lang shadow

%clean
#[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f shadow.lang
%defattr(-,root,root)
%dir %{_sysconfdir}/default
%attr(0640,root,shadow)	%config(noreplace) %{_sysconfdir}/login.defs
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/default/useradd
%{_bindir}/sg
%attr(2711,root,shadow) %{_bindir}/chage
%attr(0700,root,root) %{_bindir}/chfn
%attr(0700,root,root) %{_bindir}/chsh
%{_bindir}/faillog
%attr(0700,root,root) %{_bindir}/gpasswd
%{_bindir}/expiry
%{_bindir}/login
%attr(0700,root,root) %{_bindir}/newgrp
%{_bindir}/lastlog
%{_sbindir}/logoutd
%{_sbindir}/adduser
%{_sbindir}/user*
%{_sbindir}/group*
%{_sbindir}/grpck
%{_sbindir}/pwck
%{_sbindir}/*conv
%{_sbindir}/chpasswd
%{_sbindir}/newusers
%{_sbindir}/vipw
%{_sbindir}/vigr
#%{_sbindir}/mkpasswd
%{_mandir}/man1/chage.1*
%{_mandir}/man1/chfn.1*
%{_mandir}/man1/chsh.1*
%{_mandir}/man1/expiry.1*
%{_mandir}/man1/newgrp.1*
%{_mandir}/man1/gpasswd.1*
%{_mandir}/man3/shadow.3*
%{_mandir}/man3/getspnam.3*
%{_mandir}/man5/shadow.5*
%{_mandir}/man5/faillog.5*
%{_mandir}/man5/login.access.5*
%{_mandir}/man5/login.defs.5*
%{_mandir}/man8/adduser.8*
%{_mandir}/man8/group*.8*
%{_mandir}/man8/user*.8*
%{_mandir}/man8/pwck.8*
%{_mandir}/man8/grpck.8*
%{_mandir}/man8/chpasswd.8*
%{_mandir}/man8/newusers.8*
#%{_mandir}/man8/mkpasswd.8*
%{_mandir}/man8/*conv.8*
%{_mandir}/man8/lastlog.8*
%{_mandir}/man8/faillog.8*
%{_mandir}/man8/vigr.8*
%{_mandir}/man8/vipw.8*
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/chage-chfn-chsh
/etc/pam.d/chage
/etc/pam.d/chfn
/etc/pam.d/chsh
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/chpasswd-newusers
/etc/pam.d/chpasswd
/etc/pam.d/newusers
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/user-group-mod
/etc/pam.d/useradd
/etc/pam.d/userdel
/etc/pam.d/usermod
/etc/pam.d/groupadd
/etc/pam.d/groupdel
/etc/pam.d/groupmod

%files doc
%defattr(-,root,root)
%doc doc/HOWTO NEWS doc/LICENSE doc/README doc/README.linux


%changelog
* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.12
- rebuild against new pam

* Sat Dec 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.12
- rebuild against new gettext

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.12
- use %%kill_lang

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.12
- spec cleanups
- update the prereq on setup to ensure we get the proper groups setup
  first
- no locale files
- drop P5; it's not applied and not needed

* Fri Jul 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.12
- rebuild with new spec-helper so can revert the last unwanted workaround

* Fri Jul 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.12
- stupid rpm-helper is removing the symlinks for the pam.d files which
  is making them have incorrect ownership and permissions

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.12
- sync with openwall 4.0.4.1 (yes, we're syncing patches with an older
  version of shadow-utils, but we're updating each and every patch to
  work with 4.0.12, thus them being tagged -avx-):
  - P4: update manpages wrt LDAP and valid names
  - P5: make sure configure always puts passwd in /usr/bin
  - P6: add CRYPT_PREFIX/CRYPT_ROUNDS support
  - P7: add USERNAME_MAX and GROUPNAME_MAX support
  - P8: tcb support
- drop S3, S4, S5, S6; all but adduser.8 are included upstream
- S3: pam info for chpasswd/newuser
- S4: pam info for chage
- S6: pam info for usermod/groupmod
- requires: pam, tcb, pam_userpass
- requires setup >= 2.5-5735avx
- update S1 to handle tcb
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.12
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.12
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.12-1avx
- 4.0.12

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.11.1-2avx
- strip the suid bit from newgrp

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.11.1-1avx
- 4.0.11.1
- drop all unrequired patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3-14avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3-13avx
- rebuild for new gcc
- P13: fix gcc-3.4 build (peroyvind)
- use %%make and %%makeinstall_std
- fix the nscd patch to refer to the right pid file (mdk bug #14840) (warly)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3-12avx
- bootstrap build

* Tue Jun 29 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3-11avx
- P12 (from Owl): Properly check the return value from pam_chauthtok()
  in libmisc/pwdcheck.c: passwd_check() that is used by chfn and chsh
  commands.  Thanks to Steve Grubb and Martin Schulze.

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3-10avx
- Annvix build

* Fri Jun 04 2004 Vincent Danen <vdanen@opensls.org> 4.0.3-9sls
- make umask for useradd 0066 rather than 0022

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.0.3-8sls
- do not copy rpmsave, rpmorig, and .rpmnew files from /etc/skel (warly)
- major patch cleanup, remove all unapplied patches: P7, P8, P9, P200, P201,
  P202, P203, P204, P205, P206, P207, P208, P209, P210, P211, P212, P213,
  P217, P218, P220, P221, P222, P223, P224, PP25, P227, P230, P234, P1000,
  P1001, P1003, P1004, P1102
- renumber patches
- P11: fix Makefile in po/

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.0.3-7sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 4.0.3-6sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
