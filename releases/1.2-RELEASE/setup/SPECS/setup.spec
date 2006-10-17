#
# spec file for package setup
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		setup
%define version 	2.5
%define release 	%_revrel

Summary:	A set of system configuration and setup files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Configuration/Other
URL:		http://annvix.org/cgi-bin/viewcvs.cgi/tools/setup
Source:		setup-%{version}.tar.bz2
Patch0:		setup-2.5-avx-motd.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	shadow-utils

%description
The setup package contains a set of very important system
configuration and setup files, such as passwd, group,
profile and more.


%prep
%setup -q
%patch0 -p0


%build
%make CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install RPM_BUILD_ROOT=%{buildroot} mandir=%{_mandir}

rm -rf %{buildroot}%{_datadir}/base-passwd %{buildroot}%{_sbindir}
rm -f  `find %{buildroot}%{_mandir} -name 'update-passwd*'`
mkdir -p %{buildroot}/var/lib/rsbac


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post 
pwconv 2>/dev/null >/dev/null  || :
grpconv 2>/dev/null >/dev/null  || :

if [ -x /usr/sbin/nscd ]; then
    nscd -i passwd -i group || :
fi


%files
%defattr(-,root,root)
%doc ChangeLog
%verify(not md5 size mtime) %config(noreplace) /etc/passwd
%verify(not md5 size mtime) %config(noreplace) /etc/group
%verify(not md5 size mtime) %attr(0400,root,root) %config(noreplace) /etc/shadow
%{_mandir}/man8/*8*
# find_lang can't find man pages yet :-(
%lang(cs) %{_mandir}/cs/man8/*8*
%lang(et) %{_mandir}/et/man8/*8*
%lang(eu) %{_mandir}/eu/man8/*8*
%lang(fr) %{_mandir}/fr/man8/*8*
%lang(it) %{_mandir}/it/man8/*8*
%lang(nl) %{_mandir}/nl/man8/*8*
#%lang(ru) %{_mandir}/ru/man8/*8*
%lang(uk) %{_mandir}/uk/man8/*8*
/usr/bin/run-parts
%config(noreplace) /etc/services
%config(noreplace) /etc/exports
%config(noreplace) /etc/inputrc
%config(noreplace) /etc/filesystems
%config(noreplace) /etc/host.conf
%config(noreplace) /etc/hosts.allow
%config(noreplace) /etc/hosts.deny
%config(noreplace) /etc/motd
%config(noreplace) /etc/printcap
%config(noreplace) /etc/profile
%config(noreplace) /etc/bashrc
%config(noreplace) /etc/shells
%config(noreplace) /etc/protocols
%attr(0644,root,root) %config(missingok,noreplace) /etc/securetty
%config(noreplace) /etc/csh.login
%config(noreplace) /etc/csh.cshrc
%config(noreplace) /etc/sysconfig/ulimits
%dir /etc/profile.d
%config(noreplace) /etc/profile.d/*
%verify(not md5 size mtime) /var/log/lastlog
%attr(0700,rsbadmin,rsbadmin) %dir /var/lib/rsbac


%changelog
* Tue Oct 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- fix url links in the motd (as per ying)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- make /var/lib/rsbac owned by rsbadmin:rsbadmin and mode 0700

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-7avx
- bump the dataseg size ulimit from 6144 to 12288

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-6avx
- varargs fixes to run-parts (gbeauchesne)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-4avx
- bootstrap build

* Sat Mar 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-3avx
- add /etc/sysconfig/ulimits to determine defaults for max number of user procs,
  max number of open files, and max data segment size

* Fri Mar 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-2avx
- set some limits via limit/ulimit in /etc/profile and /etc/csh.cshrc
  as right now all resources are pretty much unlimited

* Fri Mar 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-1avx
- csh.cshrc: fix some csh code in csh.cshrc
- inputrc: redefine PgUp/PgDn so that instead of just cycling through
  history (like Up/Down arrows), it is possible to type the beginning
  of a previous command, then cycle through matching history entries
  (pablo)
- services: add missing entries and cleanups
- updated manpages (pablo); dutch translation updated by Richard Rasker
- requires on shadow-utils for %%post scripts
- securetty: root can only login on tty1 now

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4-17avx
- bad cut-n-paste job on passwd

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4-16avx
- add uid/gid 67 for supervise logging (dedicated user is safer than
  using nobody/nogroup)

* Fri Nov 12 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4-15avx
- ouch... make sure /etc/shadow is mode 0400

* Thu Aug 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4-14avx
- fix homedir for RSBAC users

* Wed Aug 11 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4-13avx
- add uid/gid 400, 401, and 402 for RSBAC

* Mon Jun 28 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4-12avx
- fix the motd

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4-11avx
- Annvix build

* Tue Jun 15 2004 Vincent Danen <vdanen@opensls.org> 2.4-10sls
- include rpm in the default group/passwd/shadow files since on install
  for some reason the rpm user doesn't get created

* Sat Jun 12 2004 Vincent Danen <vdanen@opensls.org> 2.4-9sls
- revert umask changes; 077 and 027 are too strict (even OpenBSD uses
  022 across the board), so we use 022 for all users

* Fri Jun  6 2004 Vincent Danen <vdanen@opensls.org> 2.4-8sls
- umask 077 for users and 027 for daemons
- make csh.login better match bashrc for more consistency

* Sat Apr 24 2004 Vincent Danen <vdanen@opensls.org> 2.4-7sls
- add shadow file because our installer doesn't create one and everyone
  should be using shadow password anyways

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.4-6sls
- minor spec cleanups

* Wed Feb 04 2004 Vincent Danen <vdanen@opensls.org> 2.4-5sls
- cdwriter is gid 23, video is gid 25, usb is gid 20

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 2.4-4sls
- remove conflicts because none of them are applicable
- remove groups: uucp, audio, games
- add groups: admin, cron
- remove users: uucp, games
- use a standard motd

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 2.4-3sls
- OpenSLS build
- tidy spec

* Wed Aug 27 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.4-2mdk
- removed prereq on rpm-helper

* Tue Aug 26 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.4-1mdk
- added video group

* Tue Aug  5 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-1mdk
- gcc3.3 fixes

* Wed Feb 12 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.3.0-1mdk
- Add sane-port (#873).
- Updates po files (pablo).
- services: change ipp from ucp to udp (warly).

* Wed Nov 27 2002 Warly <warly@mandrakesoft.com> 2.2.0-35mdk
- Apply patch from Buchan Milne to allow user name with space in it
- deactivate ru building as subdir is empty
- add update-passwd into package
- clean unpackaged files

* Thu Sep  5 2002 Pixel <pixel@mandrakesoft.com> 2.2.0-34mdk
- apply patch from Konrad Bernloehr on csh.cshrc to allow error detection when
using files in /etc/profile.d/*.csh and ignore non-readable files (bug #135)

* Mon Aug 26 2002 Warly <warly@mandrakesoft.com> 2.2.0-33mdk
- set page-completions to off in inputrc so that bash completions
does not use a pager

* Wed Aug 21 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0-32mdk
- added usb and floppy

* Sun Aug 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0-31mdk
- added utmp group for initscripts package

* Tue Aug  6 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0-30mdk
- added cdwriter and audio groups for the dev package.

* Tue Jul 16 2002 Warly <warly@mandrakesoft.com> 2.2.0-29mdk
- fix files sourced twice at login 

* Thu Jul 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0-28mdk
- no need for update-passwd any more.

* Thu Jul 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0-27mdk
- removed non essential users

* Thu Apr 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0-26mdk
- added the postdrop group for the new postfix package.

* Tue Feb 26 2002 Pixel <pixel@mandrakesoft.com> 2.2.0-25mdk
- "unhash" workaround for /usr/bin non-readable (msec 5) applied in csh.cshrc,
and after each modification of PATH (eurk!)

* Mon Feb 25 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0-24mdk
- add /usr/X11R6/bin and /usr/games to the PATH to allow to run correctly
without msec.

* Tue Feb  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0-23mdk
- add Conflict for version of packages using the nobody group.

* Tue Feb  5 2002 Pixel <pixel@mandrakesoft.com> 2.2.0-22mdk
- securetty: by default have standard console ttys

* Mon Feb  4 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0-21mdk
- renamed nobody group as nogroup
- nobody/nogroup at 65534/65534
- updated update-passwd to 3.4.0
- call nscd in %%post to update its content
- added missing floppy group
- added rpc user in daemon group

* Wed Jan 30 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-20mdk
- passgrp/: group, passwd: Add postfix/group user.
- profile: add missing "export HISTCONTROL" (siegel).

* Thu Jan 17 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-19mdk
- passgrp/group: Add xgrp (with xfs user as default), ntools, ctools.
- profile: add HISTCONTROL=ignoredups
- passgrp/syncforrpmlint.sh: corrected group regex to allow a x in the
  password field. (flepied).

* Thu Dec 27 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-18mdk
- passgrp/: group, passwd: Add gica (for commercial apps).

* Mon Dec 17 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-17mdk
- utils/run-parts.c: Skip rpm backup files.

* Thu Nov 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-15mdk
- passgrp/{group,passwd}: vpopmail UID 399 with vchkpw GID 399 (oden).

* Tue Nov 27 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-14mdk
- passgrp/group: Add utmp group as 24.

* Thu Nov 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-13mdk
- services: revert to the rh one (old services is buggy).
- passgrp/: group, passwd: Add snort group passwd (florin).
- passgrp/syncforrpmlint.pl: Sync group and passwd for rpmlint.
- setup.spec: set securetty as 644.
- setup.spec: fix an old changelog log (pixel).

* Thu Sep 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-12mdk
- passgrp/group: Fix syntax for postgres user (L.Borntreger).
- services: Fix ldap (thks: charles)
- Makefile, setup.spec: Added French man pages (pablo)

* Fri Aug 31 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-11mdk
- Rebuild to fix weird permissions.

* Mon Aug 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-10mdk
- passgrp/group: Add wine group.

* Thu Jun 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-9mdk
- passgrp/Makefile, utils/Makefile: Correct install file for the
  latest install of fileutils (mattias).

* Tue Jun 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-8mdk
- passgrp/: group, passwd: Add rpm group/passwd.

* Tue Jun  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-7mdk
- services: Add lisa service (Michael Brown <mandrake-cooker@fensystems.co.uk>).
- bashrc: Remove the tput stuff, it screwd up things.

* Mon May 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-6mdk
- utils/run-parts.c: A file with a . is a valid name (Sebastian
  Dransfeld <sebastid@stud.ntnu.no>)
- passgrp/: group, passwd: Add ldap user/group (vince).

* Wed May 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-5mdk
- profile: Cleanup.
- passgrp/: group, passwd: Add squid group.
- passgrp/group: added nofiles (gid 401) for qmail compat (vdanen).

* Tue May 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-4mdk
- Makefile, bashrc, setup.spec: Add bashrc make the package conflict
  with older bash.

* Mon May 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-3mdk
- utils/run-parts.c: Launch at the latest time with /bin/sh if failed
  (and a script with shbang).

* Thu May  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-2mdk
- Makefile, setup.spec, utils/.cvsignore, utils/Makefile,
  utils/run-parts.8, utils/run-parts.c: Add C program run-parts from
  Debian here.
- protocols: Merge with rh version.
- csh.login: Remove the source of profile.d. Add set of env INPUTRC
  if ~/.inputrc is here and binkey suppr under tcsh.

* Wed May  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0-1mdk
- Makefile: Make a CVS release each rpm.
- passgrp/update-passwd.[c8]: Merge with Debian 3.2.0.
- profile.d/: xhost.csh, xhost.sh: Check $SSH_TTY is not set before
  setting authority (#3052).
- csh.cshrc: Add suggetions from zijdenbos@videotron.ca (#3169)
- Bump to 2.2.0.

* Fri Apr 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-42mdk
- services: Don't do tcp/ with ntalk/talk since it break them.

* Tue Apr  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-41mdk
- services: 901 is swat.

* Mon Apr  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-40mdk
- passgrp/: group, passwd: Add postgres user/group (#2702)
- services: s|nic-name|whois|; like old day to make works fwhois

* Tue Mar 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.1.9-39mdk
- rpcuser is back for nfs-utils (kept rpc for portmap).

* Mon Mar 26 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.1.9-38mdk
- rpc user is called rpc and not rpcuser.

* Thu Mar 22 2001 Pixel <pixel@mandrakesoft.com> 2.1.9-37mdk
- /etc/filesystems: add reiserfs

* Mon Mar 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-36mdk
- services: Merge list from
  http://www.isi.edu/in-notes/iana/assignments/port-numbers.

* Sun Mar 18 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-35mdk
* passgrp/: group, passwd: Add rpcuser.

* Thu Feb 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-34mdk
- setup.spec: Relaunch pwconv and grpconv after update-passwd.

* Wed Feb 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-33mdk
- passgrp/: group, passwd: Add gdm group and user.  Add usb group.
- profile: added definition of NLSPATH variable (pablo).
- inputrc: fix for problems when bash is in vi mode set at login
  time (reported by Zot O'Connor) (pablo).

* Mon Feb 05 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-32mdk
- Add htdig user.

* Wed Jan  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-31mdk
- passgrp/: group, passwd: Add dhcp user and group for dark-florin,
  and sort the list BTW:.

* Wed Nov 29 2000 François Pons <fpons@mandrakesoft.com> 2.1.9-30mdk
- removed PreReq on /bin/sh.
- fixed building.

* Thu Nov 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-29mdk
- Set the /etc/profile.d/* scripts as no replace.

* Thu Nov 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-28mdk
- passgrp/update-passwd.8: Fixes documentation.

* Tue Nov 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-27mdk
- profile.d/xhost.csh: Fix forwarding with ssh (#1192).

* Fri Nov 10 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-26mdk
- services: Add talk as udp as well. 

* Wed Nov  8 2000 Pixel <pixel@mandrakesoft.com> 2.1.9-25mdk
- source /etc/profile.d/inputrc.csh in /etc/csh.cshrc, not only in
/etc/csh.login, that way key bindings work even you don't have a login shell
(4jl)

* Tue Oct 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-24mdk
- Add nscd user/group.

* Wed Oct 11 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-23mdk
- Remove the noarch.
- Integration of update-passwd from Debian.

* Wed Oct 11 2000 Pixel <pixel@mandrakesoft.com> 2.1.9-22mdk
- move the home directory of sympa to /var/lib/sympa

* Mon Oct  9 2000 Pixel <pixel@mandrakesoft.com> 2.1.9-21mdk
- /etc/csh.login: better fix for non-readable PATH dirs (unhash, thanks to
Christos Zoulas)
- /etc/group: fix syntax for wnn and named entries

* Mon Oct  9 2000 Pixel <pixel@mandrakesoft.com> 2.1.9-20mdk
- /etc/csh.login: better formatted warning (see 19mdk)

* Mon Oct  9 2000 Pixel <pixel@mandrakesoft.com> 2.1.9-19mdk
- /etc/csh.login: add a warning for high security level where /usr/bin is
non-user readable and tcsh doesn't handle it nicely

* Mon Oct  9 2000 Pixel <pixel@mandrakesoft.com> 2.1.9-18mdk
- /etc/group: fix syntax for the sympa entry

* Fri Oct  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-17mdk
- Add named user.

* Wed Sep  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-16mdk
- passwd: define home of ftp user to /var/ftp.

* Fri Aug  4 2000 Pixel <pixel@mandrakesoft.com> 2.1.9-15mdk
- add a lot of of noreplace's (eg: /etc/exports!)

* Mon Jul 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-14mdk
- BM.

* Sat Jul  1 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-13mdk
- group (slocate): Add slocate group.

* Thu Jun 15 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.9-12mdk
- added /etc/shells

* Mon May 15 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-11mdk
- services: Add jserver entrie.
- group (wnn): add wnn.

* Tue Apr 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-10mdk
- profile: fix LESSOPEN.

* Wed Apr 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-9mdk
- profile: export LESSOPEN variable if /usr/bin/lesspipe.sh is installed.

* Wed Apr  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-8mdk
- group (sympa): Add sympa as 89.
- passwd (sympa): Add sympa as 89.
- initscripts.spec: /etc/profile.d/ as config files.

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-7mdk
- initscripts.spec: adjust groups.

* Mon Mar 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-6mdk
- inputrc: revert pablo stuff to my stuff (until pablo come with a
  better fix :\).

* Thu Mar 23 2000 Pixel <pixel@mandrakesoft.com> 2.1.9-5mdk
- add swat entry for samba

* Sun Mar 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-4mdk
- inputrc: fix backspace bug (until pablo got a better fix).

* Thu Mar 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-3mdk
- setup.spec. Really insert inputrc.

* Sun Mar 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-2mdk
- inputrc: Reinsert Pablo file (was not included).

* Sun Feb 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.9-1mdk
- Makefile: 2.1.9.
- ChangeLog: create it.
- profile.d/xhost*: check if the XAUTHORITY variable is not defined.
- etcskel.spec: addd some files in noreplace.
- filesystems: move it here and add defaults sane.
- profile: don't define the PATH here.
- profile: HISTFILESIZE is obsoletes, don't export it.
- profile: Check before if INPUTRC variable is not defined and ~/.inputrc
	is not present.
- services: Add LDAP services.
- services: fix mailq lines (udp & tcp).

* Thu Jan  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.6-15mdk
- cdrom groups == 22.

* Thu Dec 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Don't request /bin/csh or /bin/sh

* Mon Dec 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- in CVS  and real Makefile.

* Mon Dec 20 1999 Frederic Lepied <flepied@mandrakesoft.com> 2.0.6-11mdk
- set the variable PROFILE_LOADED in /etc/setup

* Mon Dec 13 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- fix typos in group
- add x10 and radio groups here (so the gid do not change)

* Thu Dec  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- make empty the securetty for security.

* Wed Dec 01 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Oups take the wrong version :\.

* Wed Dec 01 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- export XAUTHORITY to permit root to launch X applications (but not others
  users !!!).

* Wed Nov 24 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Remove PATH of profile (handle by mandrake security).

* Sun Nov 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add cdrecord::80 and audio::81 in group.
- Remove default umask (handle by mdk security).
- Set core files only for root.

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.0.6.
- split csh.login into csh.login and csh.cshrc (r)
- fix pop service names (r)
- fix ipv6 protocols entries (r)

* Fri Sep 24 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Really fix limit coredump problem (cant believe i forgot this)

* Fri Sep 24 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- use tcp not udp for talk in /etc/services

* Tue Sep 14 1999 Pixel <pixel@mandrakesoft.com>
- added group postgres to fix the bogus useradd of install2 

* Fri Aug 13 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- fix bogus permissions

* Wed Jul 28 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- added the following default groups to /etc/group:
   smb:		for allwoing mounting/unmounting of SMB shares
   floppy:	for allowing raw acces to the floppies (eg with mtools)
   cdrom:	for allowing raw access to CDs (eg for music)
   pppusers:	for users allowed to launch pppd
   cdwriters:	for users allowed to roast CDs
   audio:	for users allowed to open /dev/dsp etc.
   dos:		for r/w access to mounted FAT partitions.
 (reminder: other interesting groups are 'lp' for access to the printer(s))

* Wed May 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- ulimit -c 0 for user.

* Tue May 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Bash2 can't handle ulimit for a user :-(

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages

* Thu Feb 18 1999 Jeff Johnson <jbj@redhat.com>
- unset variables used in /etc/csh.cshrc (#1212)

* Mon Jan 18 1999 Jeff Johnson <jbj@redhat.com>
- compile for Raw Hide.

* Tue Oct 13 1998 Cristian Gafton <gafton@redhat.com>
- fix the csh.cshrc re: ${PATH} undefined

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Dec 05 1997 Erik Troan <ewt@redhat.com>
- /etc/profile uses $i, which needs to be unset

* Mon Nov 03 1997 Donnie Barnes <djb@redhat.com>
- made /etc/passwd and /etc/group %config(noreplace)

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- removed /etc/inetd.conf, /etc/rpc
- flagged /etc/securetty as missingok
- fixed buildroot stuff in spec file

* Thu Jul 31 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

* Wed Apr 16 1997 Erik Troan <ewt@redhat.com>
- Don't verify md5sum, size, or timestamp of /var/log/lastlog, /etc/passwd,
  or /etc/group.

