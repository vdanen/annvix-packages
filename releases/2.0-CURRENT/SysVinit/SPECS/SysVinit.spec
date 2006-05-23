#
# spec file for package SysVinit
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		SysVinit
%define version 	2.86
%define release 	%_revrel

Summary:	Programs which control basic system processes
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		ftp://ftp.cistron.nl/pub/people/miquels/software
Source:		ftp://ftp.cistron.nl/pub/people/miquels/software/sysvinit-%{version}.tar.bz2
Source1:	reboot.avx
Source2:	halt.avx
Patch0:		sysvinit-2.77-md5-be.patch
Patch1:		sysvinit-2.78-halt.patch
Patch2:		sysvinit-2.86-mdk-autofsck.patch
Patch4:		sysvinit-2.85-walltty.patch
Patch5:		sysvinit-2.86-fdr-chroot.patch
Patch8:		sysvinit-2.86-mdk-shutdown.patch
Patch9:		sysvinit-2.86-mdk-libcrypt.patch
Patch10:	sysvinit-2.83-biarch-utmp.patch
Patch11:	sysvinit-disable-respawn-more-quickly.patch
Patch12:	sysvinit-2.85-avx-silent_no_runlevel.patch
Patch13:	sysvinit-2.86-mdk-varargs.patch
Patch14:	sysvinit-avx-silentcontrolchannel.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glibc-static-devel

Requires:	pam >= 0.66-5

%description
The SysVinit package contains a group of processes that control 
the very basic functions of your system. SysVinit includes the init 
program, the first program started by the Linux kernel when the 
system boots.  Init then controls the startup, running and shutdown
of all other programs.

NOTE: Annvix uses runit to handle init's duties, but this package still
contains some useful utilities to manage the running of the system.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n sysvinit-%{version}
%patch0 -p1 -b .be
%patch1 -p1 -b .halt
%patch2 -p1 -b .autofsck
%patch4 -p1 -b .wall
%patch5 -p1 -b .chroot
%patch11 -p0 -b .disable-respawn-more-quickly
%patch8 -p1 -b .shutdown
%patch9 -p1 -b .libcrypt
%patch10 -p1 -b .biarch-utmp
%patch12 -p1 -b .silent_no_runlevel
%patch13 -p1 -b .varargs
%patch14 -p1 -b .silent_controlchannel


%build
# cpp hack workaround
pushd src
    perl -pi -e "s,\"paths.h\",\"pathsfoo.h\",g" *
    mv paths.h pathsfoo.h
popd

make CFLAGS="%{optflags} -D_GNU_SOURCE" -C src


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
for i in bin sbin usr/bin usr/include %{_mandir}/man{1,3,5,8} etc var/run dev; do
    mkdir -p %{buildroot}/$i
done

make -C src ROOT=%{buildroot} MANDIR=%{_mandir} \
    BIN_OWNER=`id -nu` BIN_GROUP=`id -ng` install

# If this already exists, just do nothing (the ||: part)
mknod --mode=0600 %{buildroot}/dev/initctl p ||:
ln -snf killall5 %{buildroot}/sbin/pidof

chmod 0755 %{buildroot}/usr/bin/utmpdump

# move around files for runit
rm -rf	%{buildroot}/usr/include
mv %{buildroot}/sbin/init %{buildroot}/sbin/init.sysv
mv %{buildroot}%{_mandir}/man8/init.8 %{buildroot}%{_mandir}/man8/init.sysv.8
rm -f %{buildroot}%{_mandir}/man8/telinit.8
#rm -f %{buildroot}/sbin/{halt,reboot,poweroff}
#rm -f %{buildroot}%{_mandir}/man8/{halt,reboot,poweroff}.8*
#install -m 0750 %{SOURCE1} %{buildroot}/sbin/reboot
#install -m 0750 %{SOURCE2} %{buildroot}/sbin/halt

# fix telinit symlink
ln -sf init.sysv %{buildroot}/sbin/telinit


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
[ ! -p /dev/initctl ] && rm -f /dev/initctl && mknod --mode=0600 /dev/initctl p || :
[ -e /var/run/initrunlvl ] && ln -s ../var/run/initrunlvl /etc/initrunlvl || :
exit 0


%files
%defattr(-,root,root)
/sbin/bootlogd
/sbin/halt
/sbin/init.sysv
/sbin/killall5
/sbin/pidof
/sbin/reboot
/sbin/poweroff
/sbin/runlevel
/sbin/shutdown
/sbin/sulogin
/sbin/telinit
/bin/pidof
/bin/mountpoint
/usr/bin/last
/usr/bin/lastb
/usr/bin/mesg
/usr/bin/utmpdump
%attr(2555,root,tty)  /usr/bin/wall
%{_mandir}/*/*
%ghost /dev/initctl

%files doc
%doc doc/Propaganda doc/Changelog doc/Install
%doc doc/sysvinit-%{version}.lsm contrib/start-stop-daemon.* 


%changelog
* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.86
- add -doc subpackage
- rebuild with gcc4
- P5: add -c option to only match processes with the same root (from fedora)
- fix the telinit symlink

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.86
- fix group

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.86
- P14: silence the failure to communicate with init through /dev/initctl

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.86
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.86
- Clean rebuild

* Wed Dec 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.86
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.86-1avx
- 2.86
- sync P2, P8, and P9 with mdk 2.86-3mdk
- new P13 from mdk; varargs fixes (gbeauchesne)
- dropped P3, P5, P6, and P7

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.85-11avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.85-10avx
- bootstrap build

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.85-9avx
- put back halt/reboot/poweroff and use P12 to silence warnings
- renumber patches

* Sat Feb 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.85-8avx
- provide new halt/reboot scripts that are wrappers to shutdown
  (get rid of errors about not knowing the current runlevel due to runit)

* Sat Sep 11 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.85-7avx
- move /sbin/init to /sbin/init.sysv

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.85-6avx
- Annvix release

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.85-5sls
- minor spec cleanups

* Fri Feb 06 2004 Vincent Danen <vdanen@opensls.org> 2.85-4sls
- backout dietlibc support as it seems to cause INIT segfaults every second
  boot (reproducable on 3 different systems)

* Fri Jan 30 2004 Vincent Danen <vdanen@opensls.org> 2.85-3sls
- P106: dietlibc support (re: oden)

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 2.85-2sls
- remove conditionals
- OpenSLS build
- tidy spec

* Tue Jul 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.85-1mdk
- new release
- rediff patch 7

* Mon Apr  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.84-3mdk
- Patch102: Handle biarch struct utmp

* Sun Jan 19 2003 Stefan van der Eijk <stefan@eijk.nu> 2.84-2mdk
- Remove unpackaged file(s)

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.84-1mdk
- new release
- patch 4 -> 3
- reenable patch 3 (unlink /.autofsck on shutdown -f)
- patch 5 -> 105
- patch 5 : log halt/shutdown
- patch 7 : prevent wall to write to regular (aka non-ttys) files
- patch 8 : display a real help on halt/reboot --help
- patch 9 : allow '-t' argument to last{,b} for checking state at certain times
- patch 10 : (security) make pidof don't strip the path of binary to get the
  pid of; else one can fool "service XXX <cmd>" by running a process named XXX

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.83-5mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Aug  2 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.83-4mdk
- Patch101: statically link to system libcrypt

* Thu Jan 24 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.83-3mdk
- move automatic disabling of entries respawning too fast from
  10 times in 2 minutes to 3 times in 20 seconds [patch #5]

* Fri Nov  9 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.83-2mdk
- make /dev/initctl a ghost file

* Fri Nov  2 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.83-1mdk
- new version.
- remove patch1 (manpatch), integrated upstream
- remove patch3 (sigint), better patch integrated upstream
- remove patch5 (md5), integrated upstream
- remove patch6 (nologin), better patch integrated upstream
- remove patch7 (notty), better patch integrated upstream
- remove patch8 (wall-n), better patch integrated upstream
- remove patch9 (umask), integrated upstream
- remove patch10 (lastgone), better patch integrated upstream
- remove patch11 (cread), better patch integrated upstream
- Add -D_GNU_SOURCE to CFLAGS, required for build.

* Wed Aug 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-11mdk
- Disable again patch4.

* Mon Aug  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-10mdk
- update 'no logout' patch (rh).
- fix setting of CREAD to work with 2.4.3+ kernels (rh)

* Mon Jun 25 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-9mdk
- show users with no login pid but no logout record as gone (rh,
  <cwolf@starclass.com>)
- fix sulogin to *always* work without a tty (rh)

* Fri Jun  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-8mdk
- run telinit u on upgrade if we are in root fs (rh).
- set umask 022 on startup (rh).

* Thu Mar  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-7mdk
- document '-n' option to wall, make it root-only (rh)
- don't open files in sulogin unless they're really ttys (rh)

* Sun Sep 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-6mdk
- set SHLVL in sulogin so /etc/profile.d stuff isn't run by default (rh).

* Wed Sep 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-5mdk
- Add optimisations when compiling.
- Remove halt patch, by default halt = halt.

* Thu Jul 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-4mdk
- BM.

* Thu Jun 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-3mdk
- Merge with rh patches.
- macroszification.

* Wed Mar 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-2mdk
- Fix group.

* Mon Mar 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.78-1mdk
- 2.78.
- fix spec installation.
- Adjust groups.

* Tue Jan 04 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com>
- Clean up... All appear to work fine. 
- Oups, dumb little fix (but important)

* Mon Jan 03 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com>
- Patch : take care of the -a options even if shutdown.allow doesn't exist.

* Tue Oct 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with redhat changes.

* Tue Sep 28 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- nologin patch isn't needed

* Tue Sep 14 1999 Daouda LO <daouda@mandrakesoft.com>
- 2.77

* Wed May 19 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- We can't hardlink /bin/pidof anywhere, because it's a symlink itself.
  Fix...

* Tue May 18 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Linking /bin/pidof to /sbin/pidof for RH compatibilities.

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- The normal source doen't work, we need to remove the orphan link to rebuild.

* Fri Apr  9 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- update to 2.76
- bzip2 man pages
- handle RPM_OPT_FLAGS
- remove some RH patches because they're not required with 2.76
- add de, fr, tr locales
- Move pidof from /sbin to /bin - can't hurt.

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- glibc 2.1

* Sun Aug 23 1998 Jeff Johnson <jbj@redhat.com>
- poweroff symlink not included (problem #762)

* Thu Jul 09 1998 Chris Evans <chris@ferret.lmh.ox.ac.uk>
- Fix a securelevel releated security hole. Go on, try and break append
  only files + securelevel now ;-)

* Wed Jul  8 1998 Jeff Johnson <jbj@redhat.com>
- remove /etc/nologin at end of shutdown.
- compile around missing SIGPWR on sparc

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.74
- fixed the package source url... (yeah, it was wrong !)

* Wed Oct 1 1997 Cristian Gafton <gafton@redhat.com>
- fixed the MD5 check in sulogin (128 hash bits encoded with base64 gives
  22 bytes, not 24...). Fix in -md5.patch

* Thu Sep 11 1997 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- /etc/initrunlvl gets linked to /tmp/init-root/var/run/initrunlvl which is
  just plain wrong..
- /usr/bin/utmpdump was missing in the files section, although it was
  explicitly patched into PROGS.
- added attr's to the files section.
- various small fixes.

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- updated to 2.71
- built against glibc 2.0.4

* Fri Feb 07 1997 Michael K. Johnson <johnsonm@redhat.com>
- Added sulogin.8 man page to file list.
