%define name	shadow-utils
%define version	4.0.3
%define release	7sls

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
Source7:	pwdutils-2.4.tar.bz2
Source8:	pwdutils-2.4.tar.bz2.sign
Source9:	shadow.pamd
Source10:	pam_login-3.14.tar.bz2
Source11:	login.pamd
Source12:	chfn.pamd
Source13:	chsh.pamd
Patch1000:	shadow-20000902-mdk.patch.bz2
Patch0:		shadow-4.0.3-mdk.patch.bz2
Patch1001:	shadow-20000902-nscd.patch.bz2
Patch1:		shadow-4.0.3-nscd.patch.bz2
Patch2:		shadow-19990827-group.patch.bz2
Patch1003:	shadow-20000902-vipw.patch.bz2
Patch3:		shadow-4.0.3-vipw.patch.bz2
Patch1004:	shadow-20000826-preserve.patch.bz2
Patch4:		shadow-4.0.3-preserve.patch.bz2
Patch5:		shadow-4.0.3-mailspool.patch.bz2
Patch6:		shadow-20000902-usg.patch.bz2
Patch7:		shadow-20000902-old.patch.bz2
Patch8:		shadow-20000902-man.patch.bz2
Patch9:		shadow-20000902-64.patch.bz2
Patch100:	shadow-20000826-no-syslog-setlocale.patch.bz2
Patch101:	shadow-20000902-useradd-LSB-compliance.patch.bz2
Patch1102:	shadow-20000902-useradd-umask.patch.bz2
Patch102:	shadow-4.0.3-useradd-umask.patch.bz2
patch200:	shadow-000_manpages.diff.bz2
patch201:	shadow-001_src_Makefile.am.diff.bz2
patch202:	shadow-002_src_login.c.diff.bz2
patch203:	shadow-003_src_newgrp.c.diff.bz2
patch204:	shadow-004_src_su.c.diff.bz2
patch205:	shadow-005_src_lastlogin.c.diff.bz2
patch206:	shadow-006_src_useradd.c.diff.bz2
patch207:	shadow-007_cppw.diff.bz2
patch208:	shadow-008_readonly_root.diff.bz2
patch209:	shadow-009_logoutd.diff.bz2
patch210:	shadow-010_src_passwd.c.diff.bz2
patch211:	shadow-011_doc_README.debian.diff.bz2
patch212:	shadow-012_libmisc_sulog.c.diff.bz2
patch213:	shadow-013_fix_shadowconfig.bz2
patch214:	shadow-014_libmisc_xmalloc.c.diff.bz2
# patch215 is ia64 support in *generated* files
patch216:	shadow-016_subsystem_shell_fix.diff.bz2
patch217:	shadow-017_su_root_hack.diff.bz2
patch218:	shadow-018_expiry_man_page.diff.bz2
# patch219 contains *generated* files
patch220:	shadow-020_silence_alarm.diff.bz2
patch221:	shadow-021_man_shadowconfig_usr_doc.diff.bz2
patch222:	shadow-022_su_user.diff.bz2
patch223:	shadow-023_group_shadow_cleanup.diff.bz2
patch224:	shadow-024_shadowconfig_grpck_prune.diff.bz2
patch225:	shadow-025_note_chage_lossage.diff.bz2
# patch226 is bullshit
patch227:	shadow-027_commonio_fix.diff.bz2
# patch228 add /var/mail which we don't want
# patch229 is bullshit
patch230:	shadow-030_less_rabid_argument_checking.diff.bz2
patch231:	shadow-031_passwd_5_no_aging.diff.bz2
patch232:	shadow-032_login.defs_maildir.diff.bz2
# patch233 add /var/mail which we don't want
patch234:	shadow-034_login_1_file_locations.diff.bz2
# patch235 contains *generated* files
# this may depend on previous patches
Patch500:	shadow-4.0.3-biarch-utmp.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gettext-devel
BuildRequires:  automake1.7

Obsoletes:	adduser, newgrp, passwd
Provides: 	adduser, newgrp, shadow-utils > 20000902-5, passwd
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
%setup -q -n shadow-%{version} -a 7 -a 10
%patch0 -p1 -b .mdk
%patch1 -p1 -b .nscd
%patch2 -p1 -b .group
%patch3 -p1 -b .vipw
%patch4 -p1 -b .preserve
%patch5 -p1 -b .mailspool
%patch6 -p1 -b .usg

# warly 20021114 integrated in default branch
# %patch7 -p1 -b .old

# warly 20021114 seems not useful anymore
# %patch8 -p1 -b .man

# warly 20021114 seems not useful anymore
# %patch9 -p1 -b .64

# MDK patches
%patch100 -p1 -b .chmou
%patch101 -p1 -b .lsb
%patch102 -p1 -b .useradd-umask

# Debian fixes 
# %patch200 -p1
# %patch201 -p1
# %patch202 -p1
# %patch203 -p1
# %patch204 -p1
# %patch205 -p1
# %patch206 -p1
# %patch207 -p1
# %patch208 -p1
# %patch209 -p1
# %patch210 -p1
# %patch211 -p1
# %patch212 -p1
# %patch213 -p1
%patch214 -p1
%patch216 -p1
# %patch217 -p1
# %patch218 -p1
# %patch220 -p1
# %patch221 -p1
# %patch222 -p1
# %patch223 -p1
# %patch224 -p1
# %patch225 -p1
# %patch227 -p1
# %patch230 -p1
%patch231 -p1
%patch232 -p1
#%patch234 -p1
%patch500 -p1 -b .biarch-utmp

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

cd pam_login-*
CFLAGS="$RPM_OPT_FLAGS -Wall" %configure2_5x

cd ../pwdutils-*
CFLAGS="$RPM_OPT_FLAGS -Wall" %configure2_5x \
  --with-ldap-conf-file=/etc/ldap.conf
make
# make check needs to be done as root
if [ "`whoami`" == "root" ]; then
  make check
fi

cd ..

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale

install -d -m 750 $RPM_BUILD_ROOT%{_sysconfdir}/default
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/login.defs
install -m 0600 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/default/useradd

cd pam_login-*
make install DESTDIR=%{buildroot}

cd ../pwdutils-*
make install DESTDIR=%{buildroot}
install -m 0755 etc/*.local %{buildroot}%{_sbindir}

rm -f %{buildroot}%{_initrddir}/rpasswdd
install -m 0600 %{SOURCE9} %{buildroot}%{_sysconfdir}/pam.d/shadow
install -m 0600 %{SOURCE9} %{buildroot}%{_sysconfdir}/pam.d/chage
install -m 0600 %{SOURCE9} %{buildroot}%{_sysconfdir}/pam.d/useradd
install -m 0600 %{SOURCE11} %{buildroot}%{_sysconfdir}/pam.d/login
install -m 0600 %{SOURCE12} %{buildroot}%{_sysconfdir}/pam.d/chfn
install -m 0600 %{SOURCE13} %{buildroot}%{_sysconfdir}/pam.d/chsh

cd ..

ln -s useradd $RPM_BUILD_ROOT%_sbindir/adduser
install -m644 %SOURCE3 $RPM_BUILD_ROOT%_mandir/man8/
install -m644 %SOURCE4 $RPM_BUILD_ROOT%_mandir/man8/
install -m644 %SOURCE5 $RPM_BUILD_ROOT%_mandir/man8/
install -m644 %SOURCE6 $RPM_BUILD_ROOT%_mandir/man8/
perl -pi -e "s/encrpted/encrypted/g" $RPM_BUILD_ROOT%{_mandir}/man8/newusers.8

# remove unwanted files
rm -rf %{buildroot}%{_mandir}/{pt_BR,pl,ja,it,id,hu,fr,cs,de,ko}

cd ../shadow-*
%find_lang shadow
%find_lang pam_login
%find_lang pwdutils
cat shadow.lang pam_login.lang pwdutils.lang >shadow.lang.tmp
mv -f shadow.lang.tmp shadow.lang

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf build-$RPM_ARCH

%files -f shadow.lang
%defattr(-,root,root)
%doc ChangeLog doc/ANNOUNCE doc/HOWTO doc/LICENSE doc/README doc/README.linux
%dir %{_sysconfdir}/default
%attr(0644,root,root)	%config(noreplace) %{_sysconfdir}/login.defs
%attr(0600,root,root)	%config(noreplace) %{_sysconfdir}/default/useradd
%attr(0600,root,root)	%config(noreplace) %{_sysconfdir}/pam.d/shadow
%attr(0600,root,root)	%config(noreplace) %{_sysconfdir}/pam.d/useradd
%attr(0600,root,root)	%config(noreplace) %{_sysconfdir}/pam.d/chage
%attr(0600,root,root)	%config(noreplace) %{_sysconfdir}/pam.d/login
%attr(0600,root,root)	%config(noreplace) %{_sysconfdir}/pam.d/chfn
%attr(0600,root,root)	%config(noreplace) %{_sysconfdir}/pam.d/chsh
%attr(0600,root,root)	%config(noreplace) %{_sysconfdir}/pam.d/passwd
/bin/login
%{_bindir}/sg
%{_bindir}/chage
%attr(4711,root,root)	%{_bindir}/chfn
%attr(4711,root,root)	%{_bindir}/chsh
%attr(4511,root,root)	%{_bindir}/passwd
%{_bindir}/faillog
%{_bindir}/gpasswd
%{_bindir}/expiry
%{_bindir}/login
%{_bindir}/lastlog
%attr(4711,root,root)   %{_bindir}/newgrp
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
%{_sbindir}/vigr
%{_sbindir}/vipw
%{_sbindir}/useradd.local
%{_sbindir}/userdel-pre.local
%{_sbindir}/userdel-post.local
%{_mandir}/man1/chage.1*
%{_mandir}/man1/chfn.1*
%{_mandir}/man1/chsh.1*
%{_mandir}/man1/expiry.1*
%{_mandir}/man1/login.1*
%{_mandir}/man1/passwd.1*
%{_mandir}/man1/sg.1*
%{_mandir}/man1/newgrp.1*
%{_mandir}/man1/gpasswd.1*
%{_mandir}/man5/shadow.5*
%{_mandir}/man5/faillog.5*
%{_mandir}/man5/limits.5*
%{_mandir}/man5/login.defs.5*
%{_mandir}/man8/adduser.8*
%{_mandir}/man8/group*.8*
%{_mandir}/man8/user*.8*
%{_mandir}/man8/pwck.8*
%{_mandir}/man8/grpck.8*
%{_mandir}/man8/chpasswd.8*
%{_mandir}/man8/newusers.8*
%{_mandir}/man8/*conv.8*
%{_mandir}/man8/lastlog.8*
%{_mandir}/man8/faillog.8*
%{_mandir}/man8/vipw.8*
%{_mandir}/man8/vigr.8*

%changelog
* Tue Dec 16 2003 Vincent Danen <vdanen@opensls.org> 4.0.3-7sls
- Obsoletes/Provides: passwd
- use pwdutils 2.4 (http://www.thkukuk.de/pam/pwdutils/) as it eliminates
  the need for passwd, which in turn eliminates useradd, which eliminates alot
  of unnecessary BuildReqs (18MB of sgml junk) and glib2
- use pam_login 3.14 (http://www.thkukuk.de/pam/pam_login/)
- provide /etc/pam.d/{shadow,chage,useradd,login}
- add missing manpages
- make all of the pam files not use paths to modules
- include user{add,del}*.local files

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
