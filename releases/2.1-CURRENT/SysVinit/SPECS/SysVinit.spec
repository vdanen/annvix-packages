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
Requires(pre):	setup
Requires(post):	coreutils

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
#install -m 0750 %{_sourcedir}/reboot.avx %{buildroot}/sbin/reboot
#install -m 0750 %{_sourcedir}/halt.avx %{buildroot}/sbin/halt

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
* Mon Jun 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.86
- rebuild with SSP

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.86
- fix some requires
- spec cleanups

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
