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
Group:		System/Configuration
URL:		http://annvix.org/cgi-bin/viewcvs.cgi/tools/setup
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
mkdir -p %{buildroot}/var/lib/rsbac

# remove unwanted locale files
rm -rf %{buildroot}%{_mandir}/{cs,et,eu,fr,uk}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
# due to important new group additions, we need to add them manually here if they
# don't already exist because rpm will create group.rpmnew instead
if [ -f /etc/group ]; then
    grep -q '^auth:' /etc/group || groupadd -g 27 auth
    grep -q '^shadow:' /etc/group || groupadd -g 28 shadow && chmod 0440 /etc/shadow && chgrp shadow /etc/shadow
    grep -q '^chkpwd:' /etc/group || groupadd -g 29 chkpwd
fi


%post
pwconv 2>/dev/null >/dev/null  || :
grpconv 2>/dev/null >/dev/null  || :

if [ -x /usr/sbin/nscd ]; then
    nscd -i passwd -i group || :
fi


%files
%defattr(-,root,root)
%verify(not md5 size mtime) %config(noreplace) /etc/passwd
%verify(not md5 size mtime) %config(noreplace) /etc/group
%verify(not md5 size mtime) %attr(0440,root,shadow) %config(noreplace) /etc/shadow
%{_mandir}/man8/*8*
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
