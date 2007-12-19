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
%define version 	2.9.2
%define release 	%_revrel

Summary:	A set of system configuration and setup files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Configuration
URL:		http://svn.annvix.org/cgi-bin/viewvc.cgi/tools/setup/trunk/
Source:		setup-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	shadow-utils

%description
The setup package contains a set of very important system
configuration and setup files, such as passwd, group,
profile and more.


%prep
%setup -q


%build
%make CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install RPM_BUILD_ROOT=%{buildroot} mandir=%{_mandir}

rm -rf %{buildroot}%{_datadir}/base-passwd %{buildroot}%{_sbindir}
rm -f  `find %{buildroot}%{_mandir} -name 'update-passwd*'`

# remove unwanted locale files
rm -rf %{buildroot}%{_mandir}/{cs,et,eu,fr,uk}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
# due to important new group additions, we need to add them manually here if they
# don't already exist because rpm will create group.rpmnew instead
if [ -f /etc/group ]; then
    grep -q '^auth:' /etc/group || groupadd -g 27 auth
    # be a little fancy here in case this is an upgrade and the user hasn't migrated to tcb yet
    if [ "`grep -q '^shadow:' /etc/group; echo $?`" == 1 ]; then
        groupadd -g 28 shadow 
        if [ -f /etc/shadow ]; then
            chmod 0440 /etc/shadow && chgrp shadow /etc/shadow
        fi
    fi
    grep -q '^chkpwd:' /etc/group || groupadd -g 29 chkpwd
    grep -q '^ctools:' /etc/group || groupadd -g 18 ctools
fi


%posttrans
if [ -x /usr/sbin/nscd ]; then
    nscd -i passwd || :
    nscd -i group || :
fi


%files
%defattr(-,root,root)
%verify(not md5 size mtime) %config(noreplace) /etc/passwd
%verify(not md5 size mtime) %config(noreplace) /etc/group
%{_mandir}/man8/*8*
/usr/bin/run-parts
%config(noreplace) /etc/services
%config(noreplace) /etc/inputrc
%config(noreplace) /etc/filesystems
%config(noreplace) /etc/host.conf
%config(noreplace) /etc/hosts.allow
%config(noreplace) /etc/hosts.deny
%config(noreplace) /etc/motd
%config(noreplace) /etc/printcap
%config(noreplace) /etc/profile
%config(noreplace) /etc/shells
%config(noreplace) /etc/protocols
%attr(0644,root,root) %config(missingok,noreplace) /etc/securetty
%config(noreplace) /etc/csh.login
%config(noreplace) /etc/csh.cshrc
%dir /etc/sysconfig/env/ulimits
%attr(0644,root,admin) %config(noreplace) /etc/sysconfig/env/ulimits/MAX_DATASEG_SIZE
%attr(0644,root,admin) %config(noreplace) /etc/sysconfig/env/ulimits/MAX_OPEN_FILES
%attr(0644,root,admin) %config(noreplace) /etc/sysconfig/env/ulimits/MAX_USER_PROCS
%verify(not md5 size mtime) /var/log/lastlog


%changelog
* Tue Dec 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.9.2
- don't call pwconv and grpconv; they don't seem to play too well without
  /etc/shadow
- call nscd twice as it doesn't seem we can invalidate two caches with
  a single call

* Sun Dec 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.9.2
- 2.9.2: don't provide the xhost.* profile.d scripts; we don't need to
  set ssh X support when we don't have X
- don't own /etc/profile.d; filesystem already does that

* Sat Oct 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.9.1
- 2.9.1: don't provide bashrc anymore, bash does

* Mon Sep 24 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.9
- 2.9
- /etc/exports is no longer provided (in nfs-utils instead)
- drop the rsbac stuff too

* Sat Jan 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.8
- change the urls in motd

* Mon Nov 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8
- move %%post stuff to %%posttrans to run after the install transaction
  (should ease chroot installs a bit)

* Mon Nov 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8
- 2.8

* Sat Nov 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.7
- don't include /etc/shadow at all; if you migrate to tcb then /etc/shadow should
  be deleted so let's not put it back
- handle the existance of /etc/shadow more gracefully (in case the user hasn't moved
  to tcb yet)

* Sat Nov 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.7
- 2.7 (support for env/ulimits/* files)

* Sat Nov 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- remove /usr/X11R6/bin from PATH
- change URL

* Tue Oct 31 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- 2.6
- add ctools group (gid 18)
- fix URL

* Thu Oct 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- updated tarball to add svnserve alias to svn (/etc/services)

* Tue Oct 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- updated tarball to fix motd

* Sun Oct 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- fix pre-reqs

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- move adding new groups to %%pre

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- requires libtcb (for groupadd)
- remove non-english manpages
- spec cleanups

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- make syslogd (uid/gid 85) here instead of relying on the rpm-helper
  scripts to add the user (for some reason it's not working as it
  should) -- anyways, we will always need this user
- add post-requires on grep

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- drop the doc (Changelog)

* Sat Jul 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- /etc/passwd is now owned root:shadow
- new groups: auth (gid 27), shadow (gid 28), chkpwd (gid 29)
- these groups are pretty important, so if they don't exist, add
  them instead of waiting for an admin to merge the changes from
  group.rpmnew
- also, we have to change the ownership of /etc/shadow if we setup
  the new shadow group

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- fix group

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
