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
%define version		2.12r
%define release		%_revrel

Summary:	A collection of basic system utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		ftp://ftp.kernel.org/pub/linux/utils/util-linux/
Source0:	ftp://ftp.kernel.org/pub/linux/utils/util-linux/%{name}-%{version}.tar.bz2
Source1:	login.pamd
Source2:	chfn.pamd
Source3:	chsh.pamd
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
#
# Mandriva Specific patches
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
# (blino) don't fail when using labels and -e option
Patch1211:	util-linux-2.12r-mdk-label.patch

# Annvix patches
Patch1250:	util-linux-2.12a-avx-noselinux.patch

Obsoletes:	fdisk
Obsoletes:	tunelp
Provides:	fdisk
Provides:	tunelp
%ifarch alpha sparc sparc64 ppc
Obsoletes:	clock
%endif
# (Dadou) Stupid, noarch is specified. Uncomment if you put something
#%ifarch
Conflicts:	initscripts <= 4.58
Conflicts:	timeconfig <= 3.0.1
#%endif

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gcc
BuildRequires:	sed
BuildRequires:	pam-devel
BuildRequires:	ncurses-devel
BuildRequires:	termcap-devel
BuildRequires:	texinfo
BuildRequires:	slang-devel
BuildRequires:	zlib-devel

Requires:	pam >= 0.66-4
Requires:	shadow-utils >= 20000902-5
Requires(pre):	mktemp
Requires(pre):	gawk
Requires(pre):	diffutils
Requires(pre):	coreutils
Requires(post):	info-install
Requires(preun): info-install

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
Group:		System/Configuration

%description -n losetup
Linux supports a special block device called the loop device, which
maps a normal file onto a virtual block device.  This allows for the
file to be used as a "virtual file system" inside another file.
Losetup is used to associate loop devices with regular files or block
devices, to detach loop devices and to query the status of a loop
device.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


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
cp %{_sourcedir}/cramfs.h %{_sourcedir}/mkcramfs.c .
%patch100 -p1 -b .mkcramfs
%patch101 -p1 -b .quiet

# nologin
cp %{_sourcedir}/nologin.c %{_sourcedir}/nologin.8 .
 
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
%patch1211 -p1 -b .label

%patch1250 -p0 -b .noselinux

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
    install -m 0644 %{_sourcedir}/login.pamd login
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

# move flock and logger in /bin, so they can be used if /usr isn't mounted
for p in flock logger; do
	mv %{buildroot}{%{_bindir},/bin}/$p
	ln -sf ../../bin/$p %{buildroot}%{_bindir}/$p
done

# remove stuff we don't want
rm -f %{buildroot}%{_mandir}/man1/{line,newgrp,pg,chfn,chsh}.1*
rm -f %{buildroot}%{_mandir}/man8/{vipw,vigr}.8*
rm -f %{buildroot}%{_bindir}/{line,newgrp,pg,chfn,chsh}
rm -f %{buildroot}%{_sbindir}/{vipw,vigr}
rm -f %{buildroot}/sbin/sln

%kill_lang %{name}
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
%config(noreplace) %{_sysconfdir}/fdprm
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
/bin/flock
%{_bindir}/flock
%{_bindir}/getopt
%{_bindir}/hexdump
%{_bindir}/ipcrm
%{_bindir}/ipcs
%{_bindir}/isosize
%{_mandir}/man8/isosize.8*
/bin/logger
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

%{_infodir}/ipc.info*

%{_mandir}/man1/arch.1*
%{_mandir}/man1/cal.1*
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

%{_datadir}/misc/getopt

%files -n mount
%defattr(-,root,root)
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

%files doc
%defattr(-,root,root)
%doc */README.* HISTORY mount/README.mount
%ifarch %ix86 alpha ia64 x86_64 s390 s390x ppc sparc sparc64 sparcv9
%doc fdisk/sfdisk.examples
%endif


%changelog
* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- rebuild against new pam

* Sat Dec 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- rebuild against new ncurses

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- spec cleanups
- remove locales

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- really add -doc subpackage
- fix requires

* Sat Jul 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- drop chfn, chsh, vipw, vigr; these are provided by shadow-utils now

* Wed Jun 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- move flock and logger into /bin
- updated P218 from Mandriva to refresh non-handled options list for
  various fs
- removed P225; merged into P218
- update URLs
- fix pam config files
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- fix group

* Wed Jan 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- 2.12r
- drop P1252; merged upstream
- P1211: don't fail in "swapon -a" when using labels and -e option (blino)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12q
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12q
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.12q
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
