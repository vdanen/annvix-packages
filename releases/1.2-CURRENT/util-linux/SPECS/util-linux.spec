#
# spec file for package util-linux
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		util-linux
%define version		2.12q
%define release		%_revrel

Summary:	A collection of basic system utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		ftp://ftp.win.tue.nl/pub/linux-local/utils/util-linux/
# Alternative => ftp.kernel.org:/pub/linux/utils/util-linux/
Source0:	ftp://ftp.win.tue.nl/pub/linux-local/utils/util-linux/%{name}-%{version}.tar.bz2
Source1:	util-linux-2.7-login.pamd
Source2:	util-linux-2.7-chfn.pamd
Source3:	util-linux-2.7-chsh.pamd
Source6:	mkcramfs.c
Source7:	cramfs.h
Source8:	nologin.c
Source9:	nologin.8
Source10:	kbdrate.tar.bz2
# Change default config to switch mandrake config
Patch0:		util-linux-2.12q-mdkconf.patch
# We don't want to compile chkdupexe
Patch1:		util-linux-2.11o-nochkdupexe.patch
# limit the length of gecos size (security problem)
Patch2:		util-linux-2.11a-gecossize.patch
# the group of the tty program is root (instead of tty)
Patch21:	util-linux-2.9v-nonroot.patch
# Make more use xstrncpy and be build always (we have TERMCAP)
Patch27:	util-linux-2.11t-moretc.patch
# s390 patches (only applied for s390)
Patch60:	util-linux-2.10s-s390x.patch
Patch61:	util-linux-2.11b-s390x.patch
# fdisk: use 16 partitions as maximun
# misc documentation fixes for man pages
Patch70:	util-linux-2.12q-miscfixes.patch
# lot of cleanups for mkcramfs
Patch100:	mkcramfs.patch
# Make mkcramfs quieter, use --verbose for old behaviour
Patch101:	mkcramfs-quiet.patch
#
########### START UNSUBMITTED
#
Patch105:	util-linux-2.12q-varargs.patch
Patch106:	util-linux-2.12q-swaponsymlink-57301.patch
Patch107:	util-linux-2.11x-procpartitions-37436.patch
Patch109:	util-linux-2.11f-rawman.patch 
Patch111:	util-linux-2.11t-mkfsman.patch
Patch114:	util-linux-2.11t-dumboctal.patch
Patch115:	util-linux-2.12q-fix-ioctl.patch
Patch116:	util-linux-2.12q-autodav.patch
Patch117:	util-linux-2.12-kbdrate-period-fix.patch
Patch120:	util-linux-2.12q-compilation.patch
########### END UNSUBMITTED.
########
# Allow raw(8) to bind raw devices whose device nodes do not yet exist
Patch160:	raw-handle-nonpresent-devs.patch
# Mount patches
Patch201:	util-linux-2.11m-nolock-docs.patch
Patch204:	util-linux-2.12q-2gb.patch
Patch206:	util-linux-2.11m-kudzu.patch
Patch207:	util-linux-2.12q-swapon.patch
Patch209:	util-linux-2.12q-swapoff.patch
Patch210:	util-linux-2.12-largefile.patch
Patch211:	util-linux-2.12q-user_label_umount.patch
Patch213:	util-linux-2.12q-loop-AES-v3.0c.patch
Patch214:	util-linux-2.12q-set-as-encrypted.patch
Patch215:	util-linux-2.12q-swapon-skip-encrypted.patch
Patch216:	util-linux-2.12q-nfsmount.patch
# remove mode= from udf mounts (architecture done so that more may come)
Patch218:	util-linux-2.12q-mount-remove-silly-options-in-auto.patch
Patch219:	util-linux-2.12-lower-LOOP_PASSWORD_MIN_LENGTH-for-AES.patch
# load cryptoloop and cypher modules when use cryptoapi
Patch220:	util-linux-2.12a-cryptoapi-load-module.patch
# (fc) 2.12a-11mdk add support for pamconsole mount option (fedora)
Patch221:	util-linux-2.12q-pamconsole.patch
# (fc) 2.12a-11mdk add support for pamconsole mount option (fedora)
Patch222:	util-linux-2.12a-managed.patch
# nfs4 support (http://www.citi.umich.edu/projects/nfsv4/linux/util-linux-patches/2.12-3/)
Patch223:	util-linux-2.12q-nfs4.patch
# fortify fixes
Patch224:	util-linux-2.12q-fortify.patch
# honor "mode=" for devpts filesystem
Patch225:	util-linux-2.12q-devpts-mode.patch
#
# Mandrake Specific patches
# fix compilation related with miscfixes
Patch1000:	util-linux-2.11h-fix-compilation.patch
# clock program for ppc
Patch1200:	util-linux-2.10r-clock-1.1-ppc.patch
# leng options for clock-ppc
Patch1201:	util-linux-2.10s-clock-syntax-ppc.patch
# Added r & w options to chfn (lsb mandate)
Patch1202:	util-linux-2.11o-chfn-lsb-usergroups.patch
# fix build on alpha with newer kernel-headers
Patch1203:	util-linux-2.11m-cmos-alpha.patch
# handle biarch struct utmp[x]
Patch1206:	util-linux-2.12a-biarch-utmp.patch
# do not hide users option in mtab
Patch1207:	util-linux-2.12a-users.patch
# use glibc syscall() to use syscalls, ban use of <asm/unistd.h>
Patch1208:	util-linux-2.12q-llseek-syscall.patch
# Try to detect if the cdrom we have is a cd-extra (track audio and later track data) not
Patch1210:	util-linux-2.12q-mount_guess_fs_cdextra.patch

# Annvix patches
Patch1250:	util-linux-2.12a-avx-noselinux.patch
Patch1252:	util-linux-2.12a-can-2005-2876.patch

Obsoletes:	fdisk tunelp
provides:	fdisk, tunelp
%ifarch alpha sparc sparc64 ppc
Obsoletes:	clock
%endif
# (Dadou) Stupid, noarch is specified. Uncomment if you put something
#%ifarch
Conflicts:	initscripts <= 4.58, timeconfig <= 3.0.1
#%endif

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gcc, sed, pam-devel, ncurses-devel, termcap-devel, texinfo, slang-devel, zlib-devel

Requires:	pam >= 0.66-4, shadow-utils >= 20000902-5
Prereq:		mktemp, gawk, diffutils, coreutils

%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function.  Among
others, Util-linux contains the fdisk configuration tool and the
login program.

%package -n mount
Summary:	Programs for mounting and unmounting filesystems
Group:		System/Base

%description -n mount
The mount package contains the mount, umount, swapon and swapoff
programs.  Accessible files on your system are arranged in one big
tree or hierarchy.  These files can be spread out over several
devices. The mount command attaches a filesystem on some device to
your system's file tree.  The umount command detaches a filesystem
from the tree.  Swapon and swapoff, respectively, specify and disable
devices and files for paging and swapping.

%package -n losetup
Summary:	Programs for setting up and configuring loopback devices
Group:		System/Configuration/Networking

%description -n losetup
Linux supports a special block device called the loop device, which
maps a normal file onto a virtual block device.  This allows for the
file to be used as a "virtual file system" inside another file.
Losetup is used to associate loop devices with regular files or block
devices, to detach loop devices and to query the status of a loop
device.

%prep

%setup -q -a 10 0n %{name}-%{version}

%patch0 -p1 -b .rhconfig
%patch1 -p1 -b .nochkdupexe
%patch2 -p1 -b .gecos

%patch21 -p1 -b .nonroot

%patch27 -p1 -b .moretc

%ifarch s390 s390x
%patch60 -p1 -b .s390x2
%patch61 -p1 -b .s390x
%endif
%patch70 -p1 -b .miscfixes
#%patch81 -p1 -b .fdisk

# mkcramfs
cp %{SOURCE7} %{SOURCE6} .
%patch100 -p1 -b .mkcramfs
%patch101 -p1 -b .quiet

# nologin
cp %{SOURCE8} %{SOURCE9} .
 
%ifarch ppc
%patch1200 -p0
%patch1201 -p1
%endif

%patch1000 -p1 -b .fixes

#LSB (sb)
%patch1202 -p1

#fix build on alpha with newer kernel-headers
%ifarch alpha
%patch1203 -p1
%endif

%patch1206 -p1 -b .biarch-utmp
%patch1207 -p1 -b .users
%patch1208 -p1 -b .llseek-syscall

%patch160 -p1

# mount patches
%patch201 -p1 -b .docbug
%patch204 -p1 -b .2gb
%patch206 -p1 -b .kudzu
%patch207 -p1 -b .swapon
%patch209 -p1 -b .swapoff
%patch210 -p1 -b .largefile
%patch211 -p1 -b .userumount
%patch213 -p1 -b .loopAES
%patch214 -p1 -b .encrypted
%patch215 -p1 -b .swapon-encrypted
%patch223 -p1 -b .nfs4
%patch216 -p1 -b .nfsmount
%patch218 -p1 -b .silly
%patch219 -p1 -b .loopAES-password
%patch220 -p1 -b .load-module

%patch221 -p1 -b .pamconsole
%patch222 -p1 -b .managed
%patch224 -p1 -b .fortify
%patch225 -p1 -b .devfs-mode

%patch105 -p1 -b .varargs
%patch106 -p1 -b .swaponsymlink
%patch107 -p1 -b .procpartitions
%patch109 -p1 -b .rawman
%patch111 -p1 -b .mkfsman
                                                               
# Third time's the charm
%patch114 -p1 -b .dumboctal
%patch115 -p1 -b .fix-ioctl
%patch116 -p1 -b .autodav
%patch117 -p1 -b .kbdrate
%patch120 -p1 -b .comp
%patch1210 -p1 -b .cdextra

%patch1250 -p0 -b .noselinux
%patch1252 -p1 -b .can-2005-2876

# USRLIB_DIR is %{_libdir}
perl -pi -e "s|(USRLIB_DIR)\s*=\s*(.*)|\1=%{_libdir}|" ./MCONFIG

%build
unset LINGUAS || :

%configure
make "OPT=%{optflags} -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE" \
	HAVE_PIVOT_ROOT=yes %{?_smp_mflags}
make CFLAGS="%{optflags}" -C partx %{?_smp_mflags}

pushd rescuept
    cc %{optflags} -o rescuept rescuept.c
popd

#%ifnarch s390 s390x
#pushd kbdrate
#    cc %{optflags} -o kbdrate kbdrate.c
#popd
#%endif

gcc %{optflags} -o mkcramfs mkcramfs.c -I. -lz

gcc %{optflags} -o nologin nologin.c

%ifarch ppc
gcc clock-ppc.c -o clock-ppc
%endif

pushd sys-utils
    makeinfo --number-sections ipc.texi
popd

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/{bin,sbin}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_infodir}
mkdir -p %{buildroot}%{_mandir}/man{1,6,8,5}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/{pam.d,security/console.apps}

make install DESTDIR=%{buildroot} MANDIR=%{buildroot}/%{_mandir} INFODIR=%{buildroot}/%{_infodir}

install -m 0755 mount/pivot_root %{buildroot}/sbin
install -m 0644 mount/pivot_root.8 %{buildroot}%{_mandir}/man8
install -m 0755 rescuept/rescuept %{buildroot}/sbin
ln -f rescuept/README rescuept/README.rescuept
install -m 0755 mkcramfs %{buildroot}/usr/bin
install -m 0755 nologin %{buildroot}/sbin
install -m 0644 nologin.8 %{buildroot}%{_mandir}/man8
#%ifnarch s390 s390x
#install -m 0755 kbdrate/kbdrate %{buildroot}/sbin
#install -m 0644 kbdrate/kbdrate.8 nologin.8 %{buildroot}%{_mandir}/man8
#%endif
echo '.so man8/raw.8' > %{buildroot}%{_mandir}/man8/rawdevices.8

install -m 0755 partx/{addpart,delpart,partx} %{buildroot}/sbin

# Correct mail spool path.
perl -pi -e 's,/usr/spool/mail,/var/spool/mail,' %{buildroot}%{_mandir}/man1/login.1

%ifarch sparc sparc64 sparcv9
rm -rf %{buildroot}%{_bindir}/sunhostid
cat << E-O-F > %{buildroot}%{_bindir}/sunhostid
#!/bin/sh
# this should be %{_bindir}/sunhostid or somesuch.
# Copyright 1999 Peter Jones, <pjones@redhat.com> .  
# GPL and all that good stuff apply.
(
idprom=\`cat /proc/openprom/idprom\`
echo \$idprom|dd bs=1 skip=2 count=2
echo \$idprom|dd bs=1 skip=27 count=6
echo
) 2>/dev/null
E-O-F
chmod 0755 %{buildroot}%{_bindir}/sunhostid
%endif

#%ifnarch s390 s390x
#install -m 0644 kbdrate/kbdrate.apps %{buildroot}%{_sysconfdir}/security/console.apps/kbdrate
#install -m 0644 kbdrate/kbdrate.pam %{buildroot}%{_sysconfdir}/pam.d/kbdrate
#%endif
pushd %{buildroot}%{_sysconfdir}/pam.d
    install -m 0644 %{SOURCE1} login
    install -m 0644 %{SOURCE2} chfn
    install -m 0644 %{SOURCE3} chsh
popd

# We do not want dependencies on csh
chmod 0644 %{buildroot}%{_datadir}/misc/getopt/*

# This has dependencies on stuff in /usr
%ifnarch sparc sparc64 sparcv9
mv %{buildroot}{/sbin/,/usr/sbin}/cfdisk
%endif

%ifarch ppc
cp -f %{_builddir}/%{name}-%{version}/clock-ppc %{buildroot}/sbin/clock-ppc
mv %{buildroot}/sbin/hwclock %{buildroot}/sbin/clock-rs6k
ln -sf clock-rs6k %{buildroot}/sbin/hwclock
%endif
ln -sf ../../sbin/hwclock %{buildroot}/usr/sbin/hwclock
ln -sf ../../sbin/clock %{buildroot}/usr/sbin/clock
ln -sf hwclock %{buildroot}/sbin/clock

# remove stuff we don't want
rm -f %{buildroot}%{_mandir}/man1/{line,newgrp,pg}.1*
rm -f %{buildroot}%{_bindir}/{line,newgrp,pg}
rm -f %{buildroot}/sbin/sln

%find_lang %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_install_info ipc.info
%ifarch ppc
ISCHRP=`grep CHRP /proc/cpuinfo`
if [ -z "$ISCHRP" ]; then
    ln -sf /sbin/clock-ppc /sbin/hwclock
fi
%endif

%postun
%_remove_install_info ipc.info

%files -f %{name}.lang
%defattr(-,root,root)
%doc */README.* HISTORY
%config(noreplace) %{_sysconfdir}/fdprm
%config(noreplace) %{_sysconfdir}/pam.d/chfn
%config(noreplace) %{_sysconfdir}/pam.d/chsh
%config(noreplace) %{_sysconfdir}/pam.d/login
#%ifnarch s390 s390x
#%config(noreplace) %{_sysconfdir}/pam.d/kbdrate
#%config(noreplace) %{_sysconfdir}/security/console.apps/kbdrate
#%endif

/bin/arch
/bin/dmesg
/bin/kill
%attr(0755,root,root)	/bin/login
/bin/more

/sbin/agetty
/sbin/blockdev
/sbin/pivot_root
%ifnarch s390 s390x
/sbin/clock
%{_sbindir}/clock
%endif
/sbin/ctrlaltdel
/sbin/elvtune
/sbin/fdisk
/sbin/addpart
/sbin/delpart
/sbin/partx

%ifarch %ix86 alpha ia64 x86_64 s390 s390x ppc sparc sparc64 sparcv9
/sbin/fsck.minix
/sbin/mkfs.minix
/sbin/mkfs.bfs
/sbin/fsck.cramfs
/sbin/mkfs.cramfs
%{_mandir}/man8/fsck.minix.8*
%{_mandir}/man8/mkfs.minix.8*
%{_mandir}/man8/mkfs.bfs.8*
/sbin/sfdisk

%{_mandir}/man8/sfdisk.8*
%doc fdisk/sfdisk.examples
%endif

%ifnarch s390 s390x
/sbin/hwclock
/usr/sbin/hwclock
%endif
%ifarch ppc
/sbin/clock-ppc
/sbin/clock-rs6k
%endif
/sbin/mkfs
/sbin/mkswap
#/sbin/mkfs.bfs
/sbin/rescuept
#/sbin/sln
/sbin/nologin
%{_mandir}/man8/nologin.8*
# Begin kbdrate stuff
#%ifnarch s390 s390x
#/sbin/kbdrate
##/usr/bin/kbdrate
#%{_mandir}/man8/kbdrate.8*
#%endif

%{_bindir}/cal
%attr(0700,root,root)	%{_bindir}/chfn
%attr(0700,root,root)	%{_bindir}/chsh
%{_bindir}/col
%{_bindir}/colcrt
%{_bindir}/colrm
%{_bindir}/column
%ifarch %ix86 alpha armv4l ppc sparc sparc64 sparcv9 x86_64
%{_bindir}/cytune
%{_mandir}/man8/cytune.8*
%endif
%{_bindir}/ddate
%{_bindir}/fdformat
%{_bindir}/flock
%{_bindir}/getopt
%{_bindir}/hexdump
%{_bindir}/ipcrm
%{_bindir}/ipcs
%{_bindir}/isosize
%{_mandir}/man8/isosize.8*
%{_bindir}/logger
%{_bindir}/look
%{_bindir}/mcookie
%{_bindir}/mkcramfs
%{_bindir}/namei
%{_bindir}/raw
%{_bindir}/rename
%{_bindir}/renice
%{_bindir}/rev
%{_bindir}/script
%{_bindir}/setfdprm
%{_bindir}/setsid
%{_bindir}/setterm
%ifarch sparc sparc64 sparcv9
%{_bindir}/sunhostid
%endif
#%{_bindir}/tsort
%{_bindir}/tailf
%{_bindir}/ul
%{_bindir}/whereis
%attr(0755,root,tty)	%{_bindir}/write

%ifarch sparc sparc64 sparcv9
/sbin/cfdisk
%else
%{_sbindir}/cfdisk
%endif
%{_mandir}/man8/cfdisk.8*

%ifarch %ix86
%{_sbindir}/rdev
%{_sbindir}/ramsize
%{_sbindir}/rootflags
%{_sbindir}/vidmode
%{_mandir}/man8/rdev.8*
%{_mandir}/man8/ramsize.8*
%{_mandir}/man8/rootflags.8*
%{_mandir}/man8/vidmode.8*
%endif
%{_sbindir}/readprofile
%ifnarch s390
%{_sbindir}/tunelp
%endif
%{_sbindir}/vipw
%{_sbindir}/vigr

%{_infodir}/ipc.info*

%{_mandir}/man1/arch.1*
%{_mandir}/man1/cal.1*
%{_mandir}/man1/chfn.1*
%{_mandir}/man1/chsh.1*
%{_mandir}/man1/col.1*
%{_mandir}/man1/colcrt.1*
%{_mandir}/man1/colrm.1*
%{_mandir}/man1/column.1*
%{_mandir}/man1/ddate.1*
%{_mandir}/man1/flock.1*
%{_mandir}/man1/getopt.1*
%{_mandir}/man1/hexdump.1*
#%{_mandir}/man1/hostid.1*
%{_mandir}/man1/kill.1*
%{_mandir}/man1/logger.1*
%{_mandir}/man1/login.1*
%{_mandir}/man1/look.1*
%{_mandir}/man1/mcookie.1*
%{_mandir}/man1/more.1*
%{_mandir}/man1/namei.1*
%{_mandir}/man1/readprofile.1*
%{_mandir}/man1/rename.1*
%{_mandir}/man1/rev.1*
%{_mandir}/man1/script.1*
%{_mandir}/man1/setterm.1*
#%{_mandir}/man1/tsort.1*
%{_mandir}/man1/tailf.1*
%{_mandir}/man1/ul.1*
%{_mandir}/man1/whereis.1*
%{_mandir}/man1/write.1*

%{_mandir}/man8/agetty.8*
%{_mandir}/man8/blockdev.8*
%{_mandir}/man8/ctrlaltdel.8*
%{_mandir}/man8/dmesg.8*
%{_mandir}/man8/elvtune.8*
%{_mandir}/man8/fdformat.8*
%{_mandir}/man8/fdisk.8*
%ifnarch s390 s390x
%{_mandir}/man8/hwclock.8*
%endif
%{_mandir}/man8/ipcrm.8*
%{_mandir}/man8/ipcs.8*
%{_mandir}/man8/mkfs.8*
#%{_mandir}/man8/mkfs.bfs.8*
%{_mandir}/man8/mkswap.8*
%{_mandir}/man8/pivot_root.8*
%{_mandir}/man8/raw.8*
%{_mandir}/man8/rawdevices.8*
%{_mandir}/man8/renice.8*
%{_mandir}/man8/setfdprm.8*
%{_mandir}/man8/setsid.8*
# XXX this man page should be moved to glibc.
%{_mandir}/man8/sln.8*
%{_mandir}/man8/tunelp.8*
%{_mandir}/man8/vigr.8*
%{_mandir}/man8/vipw.8*

%{_datadir}/misc/getopt

%files -n mount
%defattr(-,root,root)
%doc mount/README.mount
%attr(0700,root,root)	/bin/mount
%attr(0700,root,root)	/bin/umount
/sbin/swapon
/sbin/swapoff
%{_mandir}/man5/fstab.5*
%{_mandir}/man5/nfs.5*
%{_mandir}/man8/mount.8*
%{_mandir}/man8/swapoff.8*
%{_mandir}/man8/swapon.8*
%{_mandir}/man8/umount.8*

%files -n losetup
%defattr(-,root,root)
%{_mandir}/man8/losetup.8*
/sbin/losetup


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- drop unapplied P1251 (sln builds fine with SSP anyways)

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.12q-5avx
- updated P218 (oblin):
  - really ignore utf8 if fs doesn't handle it
  - udf does support utf8
  - allow to remove conflicting options (for example utf8 if fs is
    udf and iocharset is specified)

* Tue Sep 20 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.12q-4avx
- P1252: patch to remove the -r flag from umount (CAN-2005-2876);
  NOTE: this doesn't affect Annvix by default since umount is not
  suid, but this is a precaution in case someone stupidly adds back
  the suid bit

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.12q-3avx
- strip suid bit from mount, umount, chfn, and chsh
- strip sgid bit from write (not required)
- don't build kdbrate at all; who needs it anyways
- sync with cooker 2.12q-5mdk:
  - P105: varargs fixes (gbeauchesne)
  - P224: fortify fixes (gbeauchesne)
  - P225: honor "mode=" for devpts filesystems (LSB, re: sbenedict)
    (gbeauchesne)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.12q-2avx
- bootstrap build (new gcc, new glibc)
- add missing P117 from mdk 2.12q-3mdk (without it kbdrate won't compile)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.12q-1avx
- 2.12q (sync with cooker 2.12q-3mdk):
  - updated P218: only keep utf8 option for iso9660, ntfs, and vfat (oblin)
  - rediff patches P0, P106, P115, P116, P121, P204, P207, P209, P211, P214,
    P215, P221, P1208 (apatard)
  - drop the limitation on partition numbers which was preventing having
    more than 16 partitions on an IDE device
  - P1210: patch for guessing if a CD is a cd-extra or not (apatard)
  - updated nfs mount version to the kernel version (apatard)
  - dropped the retryupd patch as the mount program relies now on the
    information provided by portmap (apatard)
- drop P121; applied upstream
- don't apply P1251 since we're not compiling with SSP

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.12a-2avx
- bootstrap build

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.12a-1avx
- 2.12a (sync with cooker 2.12a-11mdk):
  - P120: fix compilation issues (blino)
  - P160: fix raw devices with udev (mdk bug #11511) (tvignaud)
  - P128: fixes from blino, pixel
  - P220: load cryptoapi and cypher modules when using cryptoapi (nplanel)
  - P221: add support for "pamconsole" (fedora) (fcrozat)
  - P222: add support for "managed" (fedora) (fcrozat)
  - P1207: don't hide users option in mtab (blino)
  - P1208: use glibc syscall() to use syscalls, ban use of <asm/unistd.h> (gb)
  - fix unstripped-binary-or-object and non-standard-executable-perm for
    /sbin/{addpart,delpart,kbdrate,partx}
- spec cleanups
- P1250: don't build with SELinux support
- P1251: don't build sln with -fstack-protector because compiling static stuff
  right now gives us symbol issues

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.12-3avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 2.12-2sls
- fix PreReq to be dependant on packages, not files

* Thu Apr 22 2004 Vincent Danen <vdanen@opensls.org> 2.12-1sls
- 2.12
- sync with 2.12-2mdk:
  - rediff P210, P211, P116 (tvignaud)
  - rediff P215, P106 (nplanel)
  - remove P1205; merged upstream (tvignaud)
  - loop AES 2.0e (P213) (nplanel)
  - new patche: P115; ioctl fix (nplanel)
  - fix shadow-utils requires version (#284) (nplanel)
- P121: make sure return code from pam_chauthtok is being checked (re: Steve
  Grubb)
- drop all unapplied patches: P81, P113, P120, P1204

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 2.11z-9sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 2.11z-8sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.11z-7mdk
- fix segfault in my patch of 2.11z-6mdk, /me sux

* Tue Aug 12 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.11z-6mdk
- mount-remove-silly-options-in-auto, removes mode= from udf mounts in
  "auto" fstype, so that we can put mode=0644 in /etc/fstab for cd/dvd
  drives, and don't end up with a silly udf.c kernel driver bailing out
  because it doesn't know about this option

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11z-5mdk
- BuildRequires: termcap-devel

* Tue Jun 26 2003  <nplanel@mandrakesoft.com> 2.11z-4mdk
- fix x86_64 build: add "cytune" files (unpackaged files) (Stefan van der Eijk)
- include multi hostname and udp retry patch (David Black)

* Fri May 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.11z-3mdk
- fixed %%ifarch sparc sparc64 sparcv9 in %%files.

* Wed Apr 30 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.11z-2mdk
- fixed %%ifarch ppc in %%files.

* Mon Apr 14 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.11z-1mdk
- 2.11z.
- Remove locales_fr fixes (merged).
- Remove 216.

* Mon Apr  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11x-4mdk
- Patch1206: Handle biarch struct utmp[x]

* Tue Jan 28 2003 Vincent Danen <vdanen@mandrakesoft.com> 2.11x-3mdk
- don't apply P1204; we want mcookie to use /dev/random instead of
  /dev/urandom
- P216: fix errno handling in pivot_root (thanks Chmou)
- unpackaged files fixes... now we include isosize and cramfs stuff and
  remove some other useless crud (/Chmou salvation)

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11x-2mdk
- requires s/(file|text)utils/coreutils/

* Wed Nov 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11x-1mdk
- new release
- add HISTORY to doc
- rediff patches 1205, 214 & 107
- remove patches 212 & 220 (merged upstream)
- patch 207 : drop ifexist support (merged upstream)

* Wed Nov  6 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.11w-2mdk
- rs6000 uses normal x86 style hwclock, provide both, adapt in %%post

* Wed Oct 09 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11w-1mdk
- new release

* Wed Oct  9 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11u-2mdk
- Update Patch1205 (x86_64): Fix mcookie crash. Also, lseek() is
  64-bit and available there.

* Tue Sep 03 2002 François Pons <fpons@mandrakesoft.com> 2.11u-1mdk
- updated patch 212, removed patch 120.
- created patch 220 to fix --help and device on command line.
- 2.11u.

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11t-4mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Wed Jul 31 2002 Nicolas Planel <nplanel@mandrakesoft.com> 2.11t-3mdk
- Fix davfs detection
- Remove unapplied patches from SRPM: 35 (loginpath), 108 (autosmb)
  115 (fstabperm)

* Wed Jul 31 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 2.11t-2mdk
- Fix alpha hwclock build (patch 120)
- Remove unapplied patches from SRPM: 110 (skipraid), 202 (nfsman)

* Wed Jul 29 2002 Nicolas Planel <nplanel@mandrakesoft.com> 2.11t-1mdk
- new release
- add autodetection of davfs  
- remove P35 (loginpath), P202 (nfsman), P108 (autosmb), P110 (skipraid)
- remove P115 (fstabperm)
- rediff P207 (swapon), P209 (swapoff), P212 (netdev), P111 (mkfsman)
- rediff P114 (dumboctal)

* Wed Jul 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11r-3mdk
- USRLIB_DIR is %%{_libdir}

* Thu Jun 20 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.11r-2mdk
- patch213: allow -p as a legal option.

* Wed May 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11r-1mdk
- new release
- remove patches 104, 1205 (merged upstream)
- rediff patch 70
- gcc-3.1 build

* Thu Apr 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11q-2mdk
- make it --short-circuit aware
- remove useless use of subshells
- spec cleanups
- remove bogus bits from util-linux-2.11q-miscfixes.patch as recommended
  by Andries Brouwer (upstream maintainer)
- don't use install -s in order to strip binaries since spec-helper
  will do that very job
- resync with rh-2.11o-12 (patch115 from ejb@ql.org)

* Wed Apr 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11q-1mdk
- new release
- fix zoneinfo location in man page [Patch1205]
- regenerate patches 107, 110
- remove merged patches: 112
- remove patches when better fix merged upstream: 80
- disable 81 (conflicts with maintream changes for better geometry detection)

* Wed Apr 03 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11o-1mdk
- new release
- fix Url typo
- remove Patch1000 (merged upstream)
- add alternative url
- resync with rh; to ease future resync, keep the same patche numbers
  as rh, move mdk patches above 1000, ...
- add BuildRequires: sed
- add rawdevices(8) manpage
- add addpart, delpart, partx
- don't apply rh patch113
- pivot_root.8 doesn't need to be executable...
- remove uneeded mkdir

* Tue Feb 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11n-4mdk
- disk-utils/raw.c: if we cannot open /dev/rawctl, try /dev/raw/rawctl

* Thu Feb 14 2002 Stefan van der Eijk <stefan@eijk.nu> 2.11n-3mdk
- BuildRequires

* Sun Feb 10 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 2.11n-2mdk
- Drop Patch300 (alphahack)

* Fri Feb  8 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 2.11n-1mdk
- Version 2.11n.
- Update Patch70 (miscfixes), remove mount/pivot_root.c change,
  better change merged upstream.
- Make Patch300 (alphahack) alpha-only.  It's broken, deal with it later.

* Tue Jan 15 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11m-7mdk
- Make swapon -a skip encrypted.
- Make mcookie using /dev/urandom to generate random number.

* Tue Jan 15 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11m-6mdk
- Add encyrpted option for loop-AES.

* Wed Dec 26 2001 Stew Benedict <sbenedict@mandrakesoft.com> 2.11m-5mdk
- replace newgrp command with version from shadow package for LSB

* Fri Dec  7 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.11m-4mdk
- Patch203 (alpha only): fix build on alpha with newer kernel-headers

* Fri Nov 23 2001 Juan Quintela <quintela@mandrakesoft.com> 2.11m-3mdk
- added loopAES 1.4h support (P313).

* Sat Nov 17 2001 Juan Quintela <quintela@mandrakesoft.com> 2.11m-2mdk
- merge with mount-2.11g-5 redhat package.
- audited all the patches.
- merge mount & util-linux packages.
- clean install-info.
- removed unused test of the kind (if x != x) do at install time.
- merge with util-linux-2.11f-16 from rh.
- fix fdisk in not big disks (P81) from rh.
- fix pwent race in login (P80) from rh.
- removed p75. Included in P80.
- removed patch9 (integrated upstream).
- removed patch8 (nomount).
- remove patch3 (nomount unused anyways).
- add URL tag.

* Fri Nov 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11m-1mdk
- 2.11m.

* Thu Oct 04 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11j-2mdk
- readd cfdisk

* Sat Sep 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11j-1mdk
- Fix rpmlint's.
- Include arch manpages.
- 2.11j.
- Get the rh patch to don't setsid on login instead of my.
- Upgrade kbdrate to the one of kbd package.

* Thu Sep  6 2001 Stew Benedict <sbenedict@mandrakesoft.com> 2.11h-3mdk
- add additional switches to chfn for LSB usrgroups test
- /usr/sbin/hwclock link on PPC too

* Wed Aug 29 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.11h-2mdk
- put again the patch to fixed 'cal' program to properly display columns
  for i18n'ed names in multibyte locales (eg, in utf-8)

* Mon Aug  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11h-1mdk
- Add pivot_root.
- Silly compilation fixes with newer glibc.
- 2.11h.
- Merges rh patches.

* Wed Jul 18 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.11f-1mdk
- use fix vipw to not create world-readable shadow files from rh
- 2.11f

* Sat Jul 07 2001 Stefan van der Eijk <stefan@eijk.nu> 2.11e-2mdk
- BuildRequires:	zlib-devel

* Fri Jun  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11e-1mdk
- 2.11e.
- Really fix the login.c to don't do setsid (thanks dbg by Andrej
  Borsenkow <arvidjaar@mail.ru>).

* Wed Jun  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11d-2mdk
- Revert login.c to 2.10d version.

* Tue Jun  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11d-1mdk
- 2.11d.

* Mon May 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11c-2mdk
- Fix rpmlint errors.

* Mon May 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11c-1mdk
- Clean-Up specs.
- Merge with rh patches.
- 2.11c (add kbdrate from kbd pacakge here).

* Tue May 15 2001 Stew Benedict <sbenedict@mandrakesoft.com> 2.10s-4mdk
- Adapt clock-ppc syntax to accept hwclock parameters

* Mon Apr  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10s-3mdk
- Fix look to search words in /usr/share/dict (#2096).

* Tue Feb 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10s-2mdk
- Recompile again the last glibc-devel to have the PATH_VI defined to
  /bin/vi.

* Mon Feb  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10s-1mdk
- BuildRequires: slang-devel.
- 2.10s.

* Tue Jan 23 2001 Francis Galiegue <fg@mandrakesoft.com> 2.10r-5mdk
- Removed all that usermode crap - we don't want X in basesystem

* Tue Jan 16 2001 David BAUDENS <baudens@mandrakesoft.com> 2.10r-4mdk
- PPC: fix build with Linux 2.4

* Fri Jan 05 2001 David BAUDENS <baudens@mandrakesoft.com> 2.10r-3mdk
- BuildRequires: pam-devel
- Requires: usermode

* Wed Dec 13 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.10r-2mdk
- in french, "partition number" translation should be "numéro de partition" and
  not "nombre de partition" (Jacques Stephant)

* Tue Dec  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10r-1mdk
- Remove vipath patch since not really usefull for mandrake (we set always a /bin/vi).
- 2.10r.

* Thu Nov 29 2000 David BAUDENS <baudens@mandrakesoft.com> 2.10q-2mdk
- Fix build for PPC
- Fix %%doc

* Fri Nov 10 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.10q-1mdk
- new and shiny version.

* Tue Sep 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10o-6mdk
- Pamstackizification.

* Wed Sep 20 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.10o-5mdk
- added compat patch for ftp://nfs.sourceforge.net/pub/nfs.

* Sat Aug 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10o-4mdk
- Fix info file installation.

* Fri Aug 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10o-3mdk
- Change license to GPL.

* Wed Aug 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10o-2mdk
- Move getopt examples to /usr/share/misc/
- Set some noreplace for config files.
- Correct licens to OpensSource.

* Wed Aug 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10o-1mdk
- 2.10o.

* Wed Aug 16 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.10n-4mdk
- add elvtune (needed by recent kernels), blockdev, mkfs.bfs, agetty
- fix config files
- fix postun script

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.10n-3mdk
- automatically added BuildRequires

* Thu Aug  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10n-2mdk
- Add install-info for ipc.

* Thu Aug  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10n-1mdk
- Correct URL.
- 2.10n.

* Mon Jul 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10m-1mdk
- Add %{_mandir} to whereis.
- BM.
- Merge rh patches.
- 2.19m.

* Fri Jun 30 2000 Vincent Saugey <vince@mandrakesoft.com> 2.10h-6mdk
- Remove Requires: tcsh
- move exemple to doc

* Thu Jun 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10h-5mdk
- Remove Requires: kernel.

* Sun Jun 04 2000 David BAUDENS <baudens@mandrakesoft.com> 2.10h-4mdk
- Really use RPM_OPT_FLAGS
- Use %%{_buildroot} for BuildRoot
- Comment empty %%ifarch
- Remove duplicate k6 

* Fri May 26 2000 Adam Lebsack <adam@mandrakesoft.com> 2.10h-3mdk
- ppc clock patch fix

* Mon May 15 2000 Pixel <pixel@mandrakesoft.com> 2.10h-2mdk
- fix build (ugly)

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10h-1mdk
- 2.10h.
- Spec-helper cleanup.
- Adjust groups.

* Sun Mar 19 2000 John Buswell <johnb@mandrakesoft.com> 2.10f-2mdk
- Added PPC support
- Added fix for PowerMac/G3/G4 clock

* Wed Feb 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10f-1mdk
- 2.10f.

* Wed Jan 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10e-1mdk
- Fix multiple files inclusion for alpha and sparc{,64}.
- 2.10e.

* Tue Jan 18 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.10b-3mdk
- fixed build on sparc.

* Sun Nov 21 1999 Pixel <pixel@mandrakesoft.com>
- add rescuept in %files

* Mon Nov 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.2.10b.

* Wed Nov  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.2.10.

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix this fu**** %files, references to a archeologic arch(again).

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix this fu**** %files, references to a dinosaur arch.
- Merge with (Buggy) RH changes.
- 2.9z

* Tue Sep 28 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 2.9y

* Mon Sep 13 1999 Francis Galiègue <francis@mandrakesoft.com>
- Added file /etc/filesystems for i[3-6]86 archs with entry vfat,
  therefore obsoleting the need for modprobe vfat in rc.sysinit

* Sun Aug 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Insert rescuept.

* Tue Aug 24 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 2.9w

* Wed Jul 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.9v

* Mon Jul 11 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 2.9u
- Add french description from Thierry Vignaud <tvignaud@linux-mandrake.com>

* Fri Jul 09 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- update source url
- rebuild under cur env (13mdk)

* Mon Jul  5 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Update to 2.9t
- remove a series of patches - they finally made it to the base.

* Mon May 24 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- fix some %ifarch bugs
- Update to 2.9r

* Tue May 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add vigr to the file lists.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- enable building mount
- fix handling of RPM_OPT_FLAGS

* Mon Mar 15 1999 Michael Johnson <johnsonm@redhat.com>
- added pam_console.so to /etc/pam.d/login

* Thu Feb  4 1999 Michael K. Johnson <johnsonm@redhat.com>
- .perms patch to login to make it retain root in parent process
  for pam_close_session to work correctly

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- strip fdisk in buildroot correctly (#718)

* Mon Jan 11 1999 Cristian Gafton <gafton@redhat.com>
- have fdisk compiled on sparc and arm

* Mon Jan 11 1999 Erik Troan <ewt@redhat.com>
- added beos partition type to fdisk

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- incorporate fdisk on all arches

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- restore PAM functionality at end of login (Bug #201)

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch top build on the arm without PAM and related utilities, for now.
- build hwclock only on intel

* Wed Nov 18 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 2.9

* Thu Oct 29 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide (slang-1.2.2)
- patch kbdrate wackiness so it builds with egcs

* Tue Oct 13 1998 Erik Troan <ewt@redhat.com>
- patched more to use termcap

* Mon Oct 12 1998 Erik Troan <ewt@redhat.com>
- added warning about alpha/bsd label starting cylinder

* Mon Sep 21 1998 Erik Troan <ewt@redhat.com>
- use sigsetjmp/siglongjmp in more rather then sig'less versions

* Fri Sep 11 1998 Jeff Johnson <jbj@redhat.com>
- explicit attrs for setuid/setgid programs

* Thu Aug 27 1998 Cristian Gafton <gafton@redhat.com>
- sln is now included in glibc

* Sun Aug 23 1998 Jeff Johnson <jbj@redhat.com>
- add cbm1581 floppy definitions (problem #787)

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- remove /etc/nologin at end of shutdown/halt.

* Fri Jun 19 1998 Jeff Johnson <jbj@redhat.com>
- add mount/losetup.

* Thu Jun 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 2.8 with 2.8b clean up. hostid now defunct?

* Mon Jun 01 1998 David S. Miller <davem@dm.cobaltmicro.com>
- "more" now works properly on sparc

* Sat May 02 1998 Jeff Johnson <jbj@redhat.com>
- Fix "fdisk -l" fault on mounted cdrom. (prob #513)

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- manhattan rebuild

* Mon Dec 29 1997 Erik Troan <ewt@redhat.com>
- more didn't suspend properly on glibc
- use proper tc*() calls rather then ioctl's

* Sun Dec 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed a security problem in chfn and chsh accepting too 
  long gecos fields

* Fri Dec 19 1997 Mike Wangsmo <wanger@redhat.com>
- removed "." from default path

* Tue Dec 02 1997 Cristian Gafton <gafton@redhat.com>
- added (again) the vipw patch

* Wed Oct 22 1997 Michael Fulbright <msf@redhat.com>
- minor cleanups for glibc 2.1

* Fri Oct 17 1997 Michael Fulbright <msf@redhat.com>
- added vfat32 filesystem type to list recognized by fdisk

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- don't build clock on the alpha 
- don't install chkdupexe

* Thu Oct 02 1997 Michael K. Johnson <johnsonm@redhat.com>
- Update to new pam standard.
- BuildRoot.

* Thu Sep 25 1997 Cristian Gafton <gafton@redhat.com>
- added rootok and setproctitle patches
- updated pam config files for chfn and chsh

* Tue Sep 02 1997 Erik Troan <ewt@redhat.com>
- updated MCONFIG to automatically determine the architecture
- added glibc header hacks to fdisk code
- rdev is only available on the intel

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- update to util-linux 2.7, fixed login problems

* Wed Jun 25 1997 Erik Troan <ewt@redhat.com>
- Merged Red Hat changes into main util-linux source, updated package to
  development util-linux (nearly 2.7).

* Tue Apr 22 1997 Michael K. Johnson <johnsonm@redhat.com>
- LOG_AUTH --> LOG_AUTHPRIV in login and shutdown

* Mon Mar 03 1997 Michael K. Johnson <johnsonm@redhat.com>
- Moved to new pam and from pam.conf to pam.d

* Tue Feb 25 1997 Michael K. Johnson <johnsonm@redhat.com>
- pam.patch differentiated between different kinds of bad logins.
  In particular, "user does not exist" and "bad password" were treated
  differently.  This was a minor security hole.
