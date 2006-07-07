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
Patch5:		shadow-4.0.12-avx-owl-configure_passwd.patch
Patch6:		shadow-4.0.12-avx-owl-crypt_gensalt.patch
Patch7:		shadow-4.0.12-avx-owl-usergroupname_max.patch
Patch8:		shadow-4.0.12-avx-owl-tcb.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext-devel, pam-devel, tcb-devel, glibc-crypt_blowfish-devel, pam_userpass-devel
BuildRequires:  automake1.7

Requires:	pam, tcb, pam_userpass
Requires(pre):	setup >= 2.5-5735avx
Obsoletes:	adduser, newgrp
Provides: 	adduser, newgrp

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
#%patch5 -p1 -b .passwd
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
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/login.defs
install -m 0600 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/useradd
install -m 0644 man/shadow.3 %{buildroot}%{_mandir}/man3/shadow.3
install -m 0644 man/adduser.8 %{buildroot}%{_mandir}/man8/

ln -s useradd %{buildroot}%{_sbindir}/adduser
perl -pi -e "s/encrpted/encrypted/g" %{buildroot}%{_mandir}/man8/newusers.8

mkdir -p %{buildroot}/etc/pam.d/
pushd %{buildroot}/etc/pam.d
    install -m 0600 %{SOURCE3} chpasswd-newusers
    ln -s chpasswd-newusers chpasswd
    ln -s chpasswd-newusers newusers
    install -m 0600 %{SOURCE4} chage-chfn-chsh
    ln -s chage-chfn-chsh chage
    ln -s chage-chfn-chsh chfn
    ln -s chage-chfn-chsh chsh
    install -m 0600 %{SOURCE5} user-group-mod
    ln -s user-group-mod groupadd
    ln -s user-group-mod groupdel
    ln -s user-group-mod groupmod
    ln -s user-group-mod useradd
    ln -s user-group-mod userdel
    ln -s user-group-mod usermod
popd

# remove unwanted files
rm -rf %{buildroot}%{_mandir}/{cs,cu,de,es,fr,hu,id,it,ja,ko,pl,pt_BR,ru,zh_CN,zh_TW}
rm -rf %{buildroot}%{_libdir}

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
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/chage
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/chfn
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/chsh
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/chpasswd-newusers
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/chpasswd
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/newusers
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/user-group-mod
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/useradd
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/userdel
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/usermod
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/groupadd
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/groupdel
%attr(640,root,shadow) %config(noreplace) /etc/pam.d/groupmod

%files doc
%defattr(-,root,root)
%doc doc/HOWTO NEWS doc/LICENSE doc/README doc/README.linux


%changelog
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

* Mon Apr 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.3-5mdk
- Patch500: Handle biarch struct utmp
- BuildRequires: automake1.7, until both are independently executable

* Mon Feb 24 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.0.3-4mdk
- fix the mailspool patch (make mail spools owned by mail, not user)

* Wed Nov 20 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-3mdk
- added a Conflicts with msec < 0.37

* Mon Nov 18 2002  Warly <warly@mandrakesoft.com> 4.0.3-2mdk
- fix useradd -r -M problem

* Fri Nov 15 2002  <warly@mandrakesoft.com> 4.0.3-1mdk
- new version

* Tue Oct 29 2002 Stefan van der Eijk <stefan@eijk.nu> 20000902-9mdk
- BuildRequires: gettext-devel

* Sun Sep  8 2002 Frederic Lepied <flepied@mandrakesoft.com> 20000902-8mdk
- create home dir in 755 mode by default in useradd.

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 20000902-7mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Tue Jul 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 20000902-6mdk
- s/Copyright/License/
- resync with rh 20000902-10:
	o update patch0
	o patch 3 -> 2,  5 -> 3,  8 -> 4,  9 ->5
	o patch 6: remove USG (Unix Systems Group?) behavior support
	  (newer autoheader complains about missing defaults)
	o patch 7: remove nonexistent directory reference so that newer autoconf
	  doesn't complains about
	o patch 8: SUBDIRS is defined further below, and includes this value.
	  (newer automake complains about the duplicate)
	o patch 9: fix conflict between lseek() declaration and the glibc one when
	  building with support for Large files
	o build in source directory
	o always build with -D_BSD_SOURCE=1 -D_FILE_OFFSET_BITS=6
	o use %%configure
- apply debian patches:
	o patch 200 : add expiry.1 man page, various man pages updates
	o patch 201 : shadow makefile fix
	o patch 202 : login update
	o patch 203 : don't sanitize env when locales under use in newgrp
	o patch 204 : su: add long options
	o patch 205 : lastlog: add long options
	o patch 206 : useradd: secure temp file, 
	o patch 207 : add cppw
	o patch 208 : chowntty: handle ro /
	o patch 209 : pam use /etc/security/time.conf
	o patch 210 : passwd messages cleanups
	o patch 211 : README.debian update, don't really care ...
	o patch 212 : printf format fix
	o patch 213 : don't alter permissions of packaged programs
	o patch 214 : malloc is already defined
	o patch 216 : shell fix
	o patch 217 : su: use uid 0, not "root"
	o patch 218 : expiry man page fix
	o patch 220 : reset SIGALRM signals
	o patch 221 : fhs fix in man pages
	o patch 222 : su: handle USER variable
	o patch 223 : grpck: more checks, prune option
	o patch 224 : shadowconfig: use grpck prune option
	o patch 225 : chage man page: add warnings regarding shadow passwords
	o patch 227 : stricter check for buffer overflow
	o patch 230 : login: stop looking for options after "--"
	o patch 231 : shadow is default for now
	o patch 233 : warn for invalid strings in shadow
	o patch 234 : login man page: current login sessions are loged in
	  /var/log/{u,w}tmp
- rename patch0 as shadow-mdk and drop parts splitted in previous patches
- rpmlint fixes
- get rid of RPM_SOURCE_DIR

* Wed Dec 26 2001 Stew Benedict <sbenedict@mandraksoft.com> 20000902-5mdk
- replace newgrp from util-linux with this version for LSB compliance

* Sat Sep 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20000902-4mdk
- rpmlint correction.

* Fri Sep 28 2001 Stew Benedict <sbenedict@mandrakesoft.com> 20000902-3mdk
- patch useradd to allow blindly adding user when group of same name 
- exists - LSB requirement

* Fri Sep 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20000902-2mdk
- Rebuild.

* Wed Jun  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20000902-1mdk
- Update descriptions.
- Merge rh patch.
- 20000902.

* Sun May 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 20000826-6mdk
- Fix po install oddity (No Makefile created).

* Tue Mar 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20000826-5mdk
- truncate new files when moving overwriting files with the contents of other
  files while moving directories (keeps files from looking weird later on)(rh).
- don't overwrite user dot files in useradd (rh).

* Wed Jan 10 2001 Vincent Danen <vdanen@mandrakesoft.com> 20000826-4mdk
- security fix for insecure creation of tmpfiles

* Fri Dec 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20000826-3mdk
- Really segfault of adduser, don't setlocale when doing a SYSLOG
  since the last SYSLOG check already for DOS attack.

* Tue Nov 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20000826-2mdk
- Fix segfault of adduser.

* Tue Nov 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20000826-1mdk
- Adjust file list.
- 20000826.

* Sun Sep 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 19990827-8mdk
- Fix manpages.
- Merge with rh patches.

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 19990827-7mdk
- add noreplace
- use find_lang

* Thu Jul 20 2000 David BAUDENS <baudens@mandrakesoft.com> 19990827-6mdk
- Human readble description

* Thu Jul 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 19990827-5mdk
- BM.
- Merge rh patches.

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 19990827-4mdk
- Upgrade groups.
- Spec-helper clean-up.

* Fri Dec 3 1999 Florent Villard <warly@mandrakesoft.com>
- correct a segfault problem with NIS

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with rh patchs.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Wed Jan 13 1999 Bill Nottingham <notting@redhat.com>
- configure fix for arm

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Fri Aug 21 1998 Jeff Johnson <jbj@redhat.com>
- Note that %{_sbindir}/mkpasswd conflicts with %{_bindir}/mkpasswd;
  one of these (I think %{_sbindir}/mkpasswd but other opinions are valid)
  should probably be renamed.  In any case, mkpasswd.8 from this package
  needs to be installed. (problem #823)

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to 980403
- redid the patches

* Tue Dec 30 1997 Cristian Gafton <gafton@redhat.com>
- updated the spec file
- updated the patch so that new accounts created on shadowed system won't
  confuse pam_pwdb anymore ('!!' default password instead on '!')
- fixed a bug that made useradd -G segfault
- the check for the ut_user is now patched into configure

* Thu Nov 13 1997 Erik Troan <ewt@redhat.com>
- added patch for XOPEN oddities in glibc headers
- check for ut_user before checking for ut_name -- this works around some
  confusion on glibc 2.1 due to the utmpx header not defining the ut_name
  compatibility stuff. I used a gross sed hack here because I couldn't make
  automake work properly on the sparc (this could be a glibc 2.0.99 problem
  though). The utuser patch works fine, but I don't apply it.
- sleep after running autoconf

* Thu Nov 06 1997 Cristian Gafton <gafton@redhat.com>
- added forgot lastlog command to the spec file

* Mon Oct 26 1997 Cristian Gafton <gafton@redhat.com>
- obsoletes adduser

* Thu Oct 23 1997 Cristian Gafton <gafton@redhat.com>
- modified groupadd; updated the patch

* Fri Sep 12 1997 Cristian Gafton <gafton@redhat.com>
- updated to 970616
- changed useradd to meet RH specs
- fixed some bugs

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
