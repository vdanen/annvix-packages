%define name	shadow-utils
%define version	4.0.3
%define release	11avx

#rh-20000902-10
#%define url	ftp://ftp.ists.pwr.wroc.pl/pub/linux/shadow/beta
%define url     ftp.pld.org.pl:/software/shadow
%define _unpackaged_files_terminate_build 0

Summary:	Utilities for managing shadow password files and user/group accounts
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	BSD
Group:		System/Base
URL:		%{url}
Source0:	%{url}/shadow-%{version}.tar.bz2
Source1:	shadow-970616.login.defs
Source2:	shadow-970616.useradd
Source3:	adduser.8
Source4:	pwunconv.8
Source5:	grpconv.8
Source6:	grpunconv.8
Patch0:		shadow-4.0.3-mdk.patch.bz2
Patch1:		shadow-4.0.3-nscd.patch.bz2
Patch2:		shadow-19990827-group.patch.bz2
Patch3:		shadow-4.0.3-vipw.patch.bz2
Patch4:		shadow-4.0.3-preserve.patch.bz2
Patch5:		shadow-4.0.3-mailspool.patch.bz2
Patch6:		shadow-20000902-usg.patch.bz2
Patch7:		shadow-4.0.3-rpmsave.patch.bz2
Patch8:		shadow-20000826-no-syslog-setlocale.patch.bz2
Patch9:		shadow-20000902-useradd-LSB-compliance.patch.bz2
Patch10:	shadow-4.0.3-useradd-umask.patch.bz2
Patch11:	shadow-4.0.3-Makefile.po.patch.bz2
Patch12:	shadow-4.0.0-owl-pam_chauthtok.diff.bz2
# Debian fixes
patch200:	shadow-014_libmisc_xmalloc.c.diff.bz2
patch201:	shadow-016_subsystem_shell_fix.diff.bz2
patch202:	shadow-031_passwd_5_no_aging.diff.bz2
patch203:	shadow-032_login.defs_maildir.diff.bz2
Patch204:	shadow-4.0.3-biarch-utmp.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gettext-devel
BuildRequires:  automake1.7

Obsoletes:	adduser, newgrp
Provides: 	adduser, newgrp, shadow-utils > 20000902-5
Prefix:		%{_prefix}
Conflicts:	msec < 0.37

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

%prep
%setup -q -n shadow-%{version}
%patch0 -p1 -b .mdk
%patch1 -p1 -b .nscd
%patch2 -p1 -b .group
%patch3 -p1 -b .vipw
%patch4 -p1 -b .preserve
%patch5 -p1 -b .mailspool
%patch6 -p1 -b .usg
%patch7 -p1 -b .rpmsave

# MDK patches
%patch8 -p1 -b .chmou
%patch9 -p1 -b .lsb
%patch10 -p1 -b .useradd-umask
%patch11 -p1 -b .makefilepo
%patch12 -p1 -b .chauthtok_fix

# Debian fixes 
%patch200 -p1
%patch201 -p1
%patch202 -p1
%patch203 -p1
%patch204 -p1 -b .biarch-utmp

%build
unset LINGUAS || :
libtoolize --copy --force
aclocal-1.7
automake-1.7
autoheader
autoconf
export CFLAGS="$RPM_OPT_FLAGS -D_BSD_SOURCE=1 -D_FILE_OFFSET_BITS=64"
%configure2_5x --disable-desrpc --with-libcrypt --disable-shared
make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale

install -d -m 750 $RPM_BUILD_ROOT%{_sysconfdir}/default
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/login.defs
install -m 0600 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/default/useradd


ln -s useradd $RPM_BUILD_ROOT%_sbindir/adduser
install -m644 %SOURCE3 $RPM_BUILD_ROOT%_mandir/man8/
install -m644 %SOURCE4 $RPM_BUILD_ROOT%_mandir/man8/
install -m644 %SOURCE5 $RPM_BUILD_ROOT%_mandir/man8/
install -m644 %SOURCE6 $RPM_BUILD_ROOT%_mandir/man8/
perl -pi -e "s/encrpted/encrypted/g" $RPM_BUILD_ROOT%{_mandir}/man8/newusers.8

%find_lang shadow

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -rf build-$RPM_ARCH

%files -f shadow.lang
%defattr(-,root,root)
%doc ChangeLog doc/ANNOUNCE doc/HOWTO
%doc doc/LICENSE doc/README doc/README.linux
%dir %{_sysconfdir}/default
%attr(0644,root,root)	%config(noreplace) %{_sysconfdir}/login.defs
%attr(0600,root,root)	%config(noreplace) %{_sysconfdir}/default/useradd
%{_bindir}/sg
%{_bindir}/chage
%{_bindir}/faillog
%{_bindir}/gpasswd
%{_bindir}/expiry
%{_bindir}/login
%attr(4711,root,root)   %{_bindir}/newgrp
%{_bindir}/lastlog
%{_sbindir}/dpasswd
%{_sbindir}/logoutd
%{_sbindir}/adduser
%{_sbindir}/user*
%{_sbindir}/group*
%{_sbindir}/grpck
%{_sbindir}/pwck
%{_sbindir}/*conv
%{_sbindir}/chpasswd
%{_sbindir}/newusers
#%{_sbindir}/mkpasswd
%{_mandir}/man1/chage.1*
%{_mandir}/man1/newgrp.1*
%{_mandir}/man1/gpasswd.1*
#%{_mandir}/man3/shadow.3*
%{_mandir}/man5/shadow.5*
%{_mandir}/man5/faillog.5*
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

%changelog
* Tue Jun 29 2004 Vincent Danen <vdanen@annvix.org> 4.0.3-11avx
- P12 (from Owl): Properly check the return value from pam_chauthtok()
  in libmisc/pwdcheck.c: passwd_check() that is used by chfn and chsh
  commands.  Thanks to Steve Grubb and Martin Schulze.

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 4.0.3-10avx
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
