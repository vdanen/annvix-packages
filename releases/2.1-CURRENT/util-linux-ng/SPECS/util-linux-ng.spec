#
# spec file for package util-linux
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		util-linux-ng
%define version		2.13.0.1
%define release		%_revrel

Summary:	A collection of basic system utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		http://userweb.kernel.org/~kzak/util-linux-ng/
Source0:	ftp://ftp.kernel.org/pub/linux/utils/%{name}/v2.13/%{name}-%{version}.tar.bz2
Source1:	login.pamd
Source2:	remote.pamd
Source8:	nologin.c
Source9:	nologin.8
#
# 0-29 RedHat/Fedora
#
# 91174 - Patch to enabled remote service for login/pam
Patch0:		util-linux-ng-2.13-login-pamstart.patch
# RHEL/Fedora specific mount options
Patch1:		util-linux-ng-2.13-mount-managed.patch
Patch2:		util-linux-ng-2.13-mount-pamconsole.patch
# add note about ATAPI IDE floppy to fdformat.8
Patch3:		util-linux-ng-2.13-fdformat-man-ide.patch
# 151635 - makeing /var/log/lastlog
Patch4:		util-linux-ng-2.13-login-lastlog.patch
# 199745 - Non-existant simpleinit(8) mentioned in ctrlaltdel(8)
Patch5:		util-linux-ng-2.13-ctrlaltdel-man.patch
# 218915 - fdisk -b 4K (move to upstream?)
Patch6:		util-linux-ng-2.13-fdisk-b-4096.patch
# 231192 - ipcs is not printing correct values on pLinux
Patch7:		util-linux-ng-2.13-ipcs-32bit.patch
# 174111 - mount allows loopback devices to be mounted more than once to the
#	same mount point (move to upstream?)
Patch8:		util-linux-ng-2.13-mount-twiceloop.patch
# 165863 - swsusp swaps should be reinitialized
Patch9:		util-linux-ng-2.13-swapon-swsuspend.patch
# remove partitions
Patch10:	util-linux-ng-2.13-blockdev-rmpart.patch
#
# 30-49 Mandriva
#
# misc documentation fixes for man pages
Patch30:	util-linux-2.12q-miscfixes.patch
Patch31:	util-linux-2.11t-mkfsman.patch
Patch32:	util-linux-2.11t-dumboctal.patch
Patch33:	util-linux-2.12q-fix-ioctl.patch
Patch34:	util-linux-2.12q-autodav.patch
# Added r & w options to chfn (lsb mandate)
Patch35:	util-linux-2.11o-chfn-lsb-usergroups.patch
# handle biarch struct ll_time
Patch36:	util-linux-2.13-pre7-biarch-ll_time.patch
# do not hide users option in mtab
Patch37:	util-linux-2.13-pre7-users.patch
# fdisk: reread partition table on block devices only
Patch38:	util-linux-2.12r-rereadpt.patch
# remove mode= from udf mounts (architecture done so that more may come)
Patch39:	util-linux-ng-2.13-mount-remove-silly-options-in-auto.patch
#
# 50-59 crypto patches
# loop-AES patch rediffed from Debian port to util-linux-ng
# (conflicts with mount-twiceloop and swapon-swsuspend)
# svn://svn.debian.org/pkg-loop-aes/trunk/loop-aes-utils/debian/patches/20loop-AES.dpatch
Patch50:	util-linux-ng-2.13-loopAES.patch
Patch51:	util-linux-2.12q-swapon-skip-encrypted.patch
Patch52:	util-linux-2.12-lower-LOOP_PASSWORD_MIN_LENGTH-for-AES.patch
# load cryptoloop and cypher modules when use cryptoapi
Patch53:	util-linux-2.12a-cryptoapi-load-module.patch
Patch54:	util-linux-ng-2.13-rc3-set-as-encrypted.patch
#
# 60+ submitted upstream
#
Patch60:	util-linux-ng-2.13-locale.patch
Patch61:	util-linux-ng-2.13-mount-no-canonicalize-remote-fs.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gcc
BuildRequires:	sed
BuildRequires:	ncurses-devel
BuildRequires:	termcap-devel
BuildRequires:	texinfo
BuildRequires:	slang-devel
BuildRequires:	zlib-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	gettext-devel
BuildRequires:	audit-devel

Requires:	pam >= 0.66-4
Requires:	shadow-utils >= 20000902-5
Requires(pre):	mktemp
Requires(pre):	gawk
Requires(pre):	diffutils
Requires(pre):	coreutils
Requires(post):	info-install
Requires(preun): info-install
Obsoletes:	mount < 2.13
Obsoletes:	losetup < 2.13
Obsoletes:	linux32
Obsoletes:	setarch <= 2.0
Obsoletes:	util-linux < 2.13
Provides:	mount = %{version}-%{release}
Provides:	losetup = %{version}-%{release}
Provides:	linux32 = %{version}-%{release}
Provides:	setarch = %{version}-%{release}
Provides:	util-linux = %{version}-%{release}


%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function.  Among
others, Util-linux contains the fdisk configuration tool and the
login program.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

# nologin
cp %{_sourcedir}/nologin.c %{_sourcedir}/nologin.8 .
 
#
# RedHat/Fedora
#
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
#
# Mandriva 
#
%patch30 -p1 -b .miscfixes
%patch31 -p1 -b .mkfsman                                                      
%patch32 -p1 -b .dumboctal
%patch33 -p1 -b .fix-ioctl
%patch34 -p1 -b .autodav
%patch35 -p1 -b .lsb
%patch36 -p1 -b .biarch-ll_time
%patch37 -p1 -b .users
%patch38 -p1 -b .rereadpt
%patch39 -p1 -b .silly
#
# crypto support
#
%patch50 -p1 -b .loopAES
%patch51 -p1 -b .swapon-encrypted
%patch52 -p1 -b .loopAES-password
%patch53 -p1 -b .load-module
%patch54 -p1 -b .set-as-encrypted
#
# submitted upstream
#
%patch60 -p1 -b .locale
%patch61 -p1 -b .no-canonicalize-remote-fs


%build
%serverbuild
unset LINGUAS || :

# rebuild build system for loop-AES patch
./autogen.sh

# CFLAGS
%define make_cflags -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64

# (blino) build with -fno-ivopts to workaround a gcc 4.2 optimization bug:
#         when mount/mount.c is optimized, guess_fstype_and_mount()
#         is passed a char *types instead of char **types
export CFLAGS="%{make_cflags} %{optflags} -fno-ivopts"
%configure \
    --bindir=/bin \
    --sbindir=/sbin \
    --disable-wall \
    --enable-partx \
    --enable-login-utils \
    --enable-kill \
    --enable-write \
    --enable-arch \
    --enable-raw \
    --disable-makeinstall-chown

make %{?_smp_mflags}

gcc %{optflags} -o nologin nologin.c

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

install -m 0755 nologin %{buildroot}/sbin
install -m 0644 nologin.8 %{buildroot}%{_mandir}/man8

echo '.so man8/raw.8' > %{buildroot}%{_mandir}/man8/rawdevices.8

# Correct mail spool path.
perl -pi -e 's,/usr/spool/mail,/var/spool/mail,' %{buildroot}%{_mandir}/man1/login.1

pushd %{buildroot}%{_sysconfdir}/pam.d
    install -m 0644 %{_sourcedir}/login.pamd login
    install -m 0644 %{_sourcedir}/remote.pamd remote
popd

# this has dependencies on stuff in /usr
mv %{buildroot}{/sbin/,/usr/sbin}/cfdisk

ln -sf ../../sbin/hwclock %{buildroot}/usr/sbin/hwclock
ln -sf ../../sbin/clock %{buildroot}/usr/sbin/clock
ln -sf hwclock %{buildroot}/sbin/clock

# move flock and logger in /bin, so they can be used if /usr isn't mounted
for p in flock logger; do
    mv %{buildroot}{%{_bindir},/bin}/${p}
    ln -sf ../../bin/${p} %{buildroot}%{_bindir}/${p}
done

# remove stuff we don't want; vipw/vigr/chfn/chsh are in shadow-utils
# and need to stay there due to tcb integration
rm -f %{buildroot}%{_mandir}/man1/{line,newgrp,pg,chfn,chsh}.1*
rm -f %{buildroot}%{_mandir}/man8/{vipw,vigr}.8*
rm -f %{buildroot}%{_bindir}/{line,newgrp,pg,chfn,chsh}
rm -f %{buildroot}%{_sbindir}/{vipw,vigr}


# deprecated commands
for p in /sbin/fsck.minix /sbin/mkfs.{bfs,minix} /usr/bin/chkdupexe %{_bindir}/scriptreplay; do
    rm -f %{buildroot}${p}
done

# deprecated man pages
for p in man1/chkdupexe.1 man8/fsck.minix.8 man8/mkfs.minix.8 man8/mkfs.bfs.8 man1/scriptreplay.1; do
    rm -rf %{buildroot}%{_mandir}/${p}*
done

# we install getopt/getopt-*.{bash,tcsh} as doc files
# note: versions <=2.12 use path "%{_datadir}/misc/getopt/*"
chmod 644 getopt/getopt-*.{bash,tcsh}
rm -f %{buildroot}%{_datadir}/getopt/*
rmdir %{buildroot}%{_datadir}/getopt

# /usr/sbin -> /sbin
for p in addpart delpart partx; do
    if [ -e %{buildroot}/usr/sbin/${p} ]; then
        mv %{buildroot}/usr/sbin/${p} %{buildroot}/sbin/${p}
    fi
done

# /usr/bin -> /bin
for p in taskset; do
    if [ -e %{buildroot}/usr/bin/${p} ]; then
        mv %{buildroot}/usr/bin/${p} %{buildroot}/bin/${p}
    fi
done

# /sbin -> /bin
for p in raw; do
    if [ -e %{buildroot}/sbin/${p} ]; then
        mv %{buildroot}/sbin/${p} %{buildroot}/bin/${p}
    fi
done

%kill_lang %{name}
%find_lang %{name}

mv -f %{name}.lang %{name}.files

# create list of setarch(8) symlinks
find  %{buildroot}%{_bindir}/ -regextype posix-egrep -type l \
    -regex ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64)$" \
    -printf "%{_bindir}/%f\n" >> %{name}.files


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info ipc.info


%postun
%_remove_install_info ipc.info


%files -f %{name}.files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/login
%config(noreplace) %{_sysconfdir}/pam.d/remote
/bin/arch
/bin/dmesg
/bin/flock
/bin/kill
/bin/logger
%attr(0755,root,root) /bin/login
/bin/more
%attr(0700,root,root) /bin/mount
/bin/raw
/bin/taskset
%attr(0700,root,root) /bin/umount
%{_bindir}/cal
%{_bindir}/chrt
%{_bindir}/col
%{_bindir}/colcrt
%{_bindir}/colrm
%{_bindir}/column
%{_bindir}/cytune
%{_bindir}/ddate
%{_bindir}/fdformat
%{_bindir}/flock
%{_bindir}/getopt
%{_bindir}/hexdump
%{_bindir}/ionice
%{_bindir}/ipcrm
%{_bindir}/ipcs
%{_bindir}/isosize
%{_bindir}/logger
%{_bindir}/look
%{_bindir}/mcookie
%{_bindir}/namei
%{_bindir}/rename
%{_bindir}/renice
%{_bindir}/rev
%{_bindir}/script
%{_bindir}/setarch
%{_bindir}/setsid
%{_bindir}/setterm
%{_bindir}/tailf
%{_bindir}/ul
%{_bindir}/whereis
%attr(0755,root,tty) %{_bindir}/write
/sbin/addpart
/sbin/agetty
/sbin/blockdev
/sbin/clock
/sbin/ctrlaltdel
/sbin/delpart
/sbin/fdisk
/sbin/fsck.cramfs
/sbin/hwclock
/sbin/losetup
/sbin/mkfs
/sbin/mkfs.cramfs
/sbin/mkswap
/sbin/nologin
/sbin/partx
/sbin/pivot_root
/sbin/sfdisk
/sbin/swapoff
/sbin/swapon
%{_sbindir}/cfdisk
%{_sbindir}/clock
%{_sbindir}/hwclock
%{_sbindir}/readprofile
%{_sbindir}/rtcwake
%{_sbindir}/tunelp
%{_mandir}/man1/arch.1*
%{_mandir}/man1/cal.1*
%{_mandir}/man1/chrt.1*
%{_mandir}/man1/col.1*
%{_mandir}/man1/colcrt.1*
%{_mandir}/man1/colrm.1*
%{_mandir}/man1/column.1*
%{_mandir}/man1/ddate.1*
%{_mandir}/man1/dmesg.1*
%{_mandir}/man1/flock.1*
%{_mandir}/man1/getopt.1*
%{_mandir}/man1/hexdump.1*
%{_mandir}/man1/ionice.1*
%{_mandir}/man1/ipcrm.1*
%{_mandir}/man1/ipcs.1*
%{_mandir}/man1/kill.1*
%{_mandir}/man1/logger.1*
%{_mandir}/man1/login.1*
%{_mandir}/man1/look.1*
%{_mandir}/man1/mcookie.1*
%{_mandir}/man1/more.1*
%{_mandir}/man1/namei.1*
%{_mandir}/man1/readprofile.1*
%{_mandir}/man1/rename.1*
%{_mandir}/man1/renice.1*
%{_mandir}/man1/rev.1*
%{_mandir}/man1/script.1*
%{_mandir}/man1/setsid.1*
%{_mandir}/man1/setterm.1*
%{_mandir}/man1/tailf.1*
%{_mandir}/man1/taskset.1*
%{_mandir}/man1/ul.1*
%{_mandir}/man1/whereis.1*
%{_mandir}/man1/write.1*
%{_mandir}/man5/fstab.5*
%{_mandir}/man8/addpart.8*
%{_mandir}/man8/agetty.8*
%{_mandir}/man8/blockdev.8*
%{_mandir}/man8/cfdisk.8*
%{_mandir}/man8/ctrlaltdel.8*
%{_mandir}/man8/cytune.8*
%{_mandir}/man8/delpart.8*
%{_mandir}/man8/fdformat.8*
%{_mandir}/man8/fdisk.8*
%{_mandir}/man8/hwclock.8*
%{_mandir}/man8/isosize.8*
%{_mandir}/man8/losetup.8*
%{_mandir}/man8/mkfs.8*
%{_mandir}/man8/mkswap.8*
%{_mandir}/man8/mount.8*
%{_mandir}/man8/nologin.8*
%{_mandir}/man8/partx.8*
%{_mandir}/man8/pivot_root.8*
%{_mandir}/man8/raw.8*
%{_mandir}/man8/rawdevices.8*
%{_mandir}/man8/rtcwake.8*
%{_mandir}/man8/setarch.8*
%{_mandir}/man8/sfdisk.8*
%{_mandir}/man8/swapoff.8*
%{_mandir}/man8/swapon.8*
%{_mandir}/man8/tunelp.8*
%{_mandir}/man8/umount.8*
%{_infodir}/ipc.info*

%files doc
%defattr(-,root,root)
%doc */README.* NEWS AUTHORS
%doc getopt/getopt-*.{bash,tcsh}


%changelog
* Wed Dec 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.13.0.1
- 2.13.0.1 (the new util-linux-ng)
- obsoletes/provides mount, losetup, linux32, setarch
- drop the separate mount, losetup packages
- sync patches with Mandriva's 2.13-2mdv
- add remote.pamd
- use pam_loginuid in login/remote pam configs

* Sat Nov 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- P1213: security fix for CVE-2007-5191

* Sun Sep 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- rebuild against new slang

* Mon Jun 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- P1212: security fix for CVE-2006-7108

* Tue May 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.12r
- clean obsoletes/provides
- remove all support for non-x86/x86_64 archs (dropping P60, P61,
  P1200, P1202, P1203 as a result)
- major cleanup of %%files

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
