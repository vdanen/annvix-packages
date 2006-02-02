#
# spec file for package mkinitrd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mkinitrd
%define version 	3.4.43
%define release 	%_revrel
%define epoch		1

%define use_dietlibc 	0
%ifarch %{ix86} x86_64 amd64
%define use_dietlibc 	1
%endif

Summary:	Creates an initial ramdisk image for preloading modules
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.redhat.com/
Source:		ftp://ftp.redhat.com/mkinitrd-%{version}.tar.bz2
Source1:	mkinitrd_helper-3.5.15.1.tar.bz2
Source2:	nash-4.1.18.tar.bz2
Patch0:		mkinitrd-3.4.43-avx-mdkize.patch
Patch1:		mkinitrd-3.1.6-shutup-insmod-busybox.patch
Patch2:		mkinitrd-3.4.43-mdk-kernel-2.5.patch
Patch3:		mkinitrd-3.4.43-avx-mkdevices.patch
Patch4:		mkinitrd-4.1.12-mdk-nash.patch
Patch5:		mkinitrd-3.4.43-avx-nodietinsmod.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl
%if %{use_dietlibc}
BuildRequires:	dietlibc-devel
%else
BuildRequires:	glibc-static-devel
Requires:	/sbin/insmod.static
%endif

Requires:	mktemp >= 1.5-9mdk e2fsprogs /bin/sh coreutils grep mount gzip tar findutils >= 4.1.7-3mdk gawk
Requires:	modutils >= 2.4.26-5187avx

%description
Mkinitrd creates filesystem images for use as initial ramdisk (initrd)
images.  These ramdisk images are often used to preload the block
device modules (SCSI or RAID) needed to access the root filesystem.

In other words, generic kernels can be built without drivers for any
SCSI adapters which load the SCSI driver as a module.  Since the
kernel needs to read those modules, but in this case it isn't able to
address the SCSI adapter, an initial ramdisk is used.  The initial
ramdisk is loaded by the operating system loader (normally LILO) and
is available to the kernel as soon as the ramdisk is loaded.  The
ramdisk image loads the proper SCSI adapter and allows the kernel to
mount the root filesystem.  The mkinitrd program creates such a
ramdisk using information found in the /etc/modules.conf file.


%prep
%setup -q -a 1
rm -rf nash
tar xvjf %{SOURCE2}
%patch0 -p0 -b .mdk
%patch1 -p0
%patch2 -p0 -b .kernel25
%patch3 -p0 -b .mkdevices
%patch4 -p1 -b .mdk-nash
%patch5 -p0 -b .nodietinsmod
perl -pi -e 's/grubby//' Makefile


%build
%if %{use_dietlibc}
%ifarch x86_64
perl -pi -e 's| gcc | x86_64-annvix-linux-gnu-gcc |g' mkinitrd_helper-subdir/insmod-busybox/Makefile
perl -pi -e 's| gcc | x86_64-annvix-linux-gnu-gcc |g' mkinitrd_helper-subdir/insmod-module-init-tools/Makefile
%endif
make -C mkinitrd_helper-subdir
%endif
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make BUILDROOT=%{buildroot} mandir=%{_mandir} install
%if %{use_dietlibc}
mkdir -p %{buildroot}/sbin
cp mkinitrd_helper-subdir/insmod-busybox/insmod %{buildroot}/sbin/insmod-DIET
cp mkinitrd_helper-subdir/insmod-module-init-tools/insmod %{buildroot}/sbin/insmod-25-DIET
%endif
rm -f %{buildroot}/sbin/{grubby,installkernel,new-kernel-pkg}
rm -f %{buildroot}%{_mandir}/*/grubby*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-, root, root)
/sbin/*
%{_mandir}/*/*


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.43
- P5: don't use the insmod-DIET binary for now due to problems with it
  loading the libata driver (use insmod.static instead); increases the
  size somewhat but at least it will work
- Require modutils >= 2.4.26-5187avx as that contains our insmod.static
  that we need to work with P5 (this really is a bit of an ugly hack, there
  has to be a better way to fix this since this only seems to affect booting
  off of SATA hardware and we now by default explode the size of our ramdisk)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.43
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.43
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.43
- Obfuscate email addresses and new tagging
- Uncompress patches
- dietlibc fixes

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4.43-22avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4.43-21avx
- bootstrap build

* Sun Feb 27 2005 Vincent Danen <vdanen@annvix.rg> 3.4.43-20avx
- remove calls to handledevfs

* Fri Feb 04 2005 Vincent Danen <vdanen@annvix.rg> 3.4.43-19avx
- rebuild against new dietlibc

* Wed Jan 19 2005 Vincent Danen <vdanen@annvix.rg> 3.4.43-18avx
- pull nash out of mkinitrd-4.1.18 (fedora)
- P4: mdk patches against this version of nash
- regen P1 and remove all splash* stuff
- regen P2
- mkinitrd_helper 3.5.15.1
- regen P3; add mountdev call - also make it valid for all archs

* Tue Jan 18 2005 Vincent Danen <vdanen@annvix.rg> 3.4.43-17avx
- macros

* Sun Dec 19 2004 Vincent Danen <vdanen@annvix.rg> 3.4.43-16avx
- s/%%{x86}/%%{ix86}/ so we actually apply the patch where needed

* Sat Dec 18 2004 Vincent Danen <vdanen@annvix.rg> 3.4.43-15avx
- only apply P3 on x86; x86_64 doesn't need it and hangs with it enabled

* Fri Dec 17 2004 Vincent Danen <vdanen@annvix.rg> 3.4.43-14avx
- P3: put back "mkdevices /dev" call which was preventing our kernels
  from booting properly (the removal is in the mdk patch)

* Tue Jun 22 2004 Vincent Danen <vdanen@annvix.rg> 3.4.43-13avx
- Annvix build

* Tue Jun 15 2004 Vincent Danen <vdanen@opensls.rg> 3.4.43-12sls
- revert to 3.4.43 because 3.5.18 is not playing nice with our kernels at all
- Epoch: 1

* Tue May 25 2004 Vincent Danen <vdanen@opensls.rg> 3.5.18-1sls
- P4: fix "unknown module [x]" error when having more than one scsi_hostadapter
  entry (ie. scsi_hostadapter[x])
- 3.5.18 (merged with cooker 3.5.18-11mdk):
  - (far too many things to mention)

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.rg> 3.4.43-11sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.rg> 3.4.43-10sls
- OpenSLS build
- tidy spec

* Sat Sep 13 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.4.43-9mdk
- fix error messages when creating initrd for root-on-lvm in devfs mode

* Mon Aug 25 2003 Nicolas Planel <nplanel@mandrakesoft.com> 3.4.43-8mdk
- add dsdt option in mdkize patch, now you can use your own 
  tweaked/fixed dsdt acpi table. (default file /boot/dsdt.aml)

* Mon Aug 11 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.4.43-7mdk
- mkinitrd -h moves, suggested by houpla:
         (ex: mkinitrd /boot/initrd-2.4.21-6mdk 2.4.21-6mdk)
  ->
         (ex: mkinitrd /boot/initrd-2.4.21-6mdk.img 2.4.21-6mdk)

* Fri Aug  1 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.4.43-6mdk
- support 2.5 thx to Andrey Borzenkov <arvidjaar@mail.ru>:
  - check for kernel version. It is needed to enable build under different
    kernel (where modprobe -c cannot be used). Use either /etc/modules.conf
    or /etc/modprobe.conf
  - parse module-init-tools "install ... /sbin/modprobe ..."; it is not
    foolproof but should do as long as modprobe.conf is kept consistent
  - add insmod-25-DIET directly based on insmod from module-init-tools;
    install it as insmod on non-dietlibc archs if version >= 2.5

* Tue Jul  8 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.4.43-5mdk
- ignore modules before processing dependencies, to not end up with
  loading usbcore when probeall contains usb-storage (#4160)

* Wed Apr 16 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.4.43-4mdk
- use system dietlibc, insmod busybox 0.60.5 on x86-64 too

* Tue Apr 15 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.4.43-3mdk
- add some buildrequires
- don't build unneeded grubby

* Thu Apr 10 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.4.43-2mdk
- fix broken error handling when "mount -o loop" fails (via side-effect,
  this lead to breaking mkinitrd generation during install)

* Thu Apr  3 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.4.43-1mdk
- merge RH version
- add automatic modules deps handling (#3614 and so many more..)
- this makes two good reasons to plank the children

* Tue Feb 18 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-37mdk
- add dependance info on mptscsih (Patch11)

* Sat Feb 15 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-36mdk
- taking patch from jose_urena at hotmail.com to fix #1654 (Patch9)
- following suggestion by Fabio Stumbo <f.stumbo at unife.it>, force use
  of /bin/ls to circumvent problems with people aliasing ls with more
  options

* Mon Jan 20 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-35mdk
- support generation of initrd suitable for a raid system on a non raid
  system thx to Christopher Samuel <chris@csamuel.org>

* Thu Dec 19 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-34mdk
- ignore failures when looking for xfs support modules, some recent
  kernels don't have them
- still compile minilibc with glibc-2.3

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.6-33mdk
- remove useless prefix
- requires s/fileutils/coreutils/

* Sun Oct  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.6-32mdk
- fix x86-64 support

* Fri Sep 13 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-31mdk
- workaround kmod suckiness (kmod failed to exec modprobe
  scsi_hostadapter) by loading sd_mod right after the scsi hostadapter

* Thu Aug  8 2002 Warly <warly@mandrakesoft.com> 3.1.6-30mdk
- add exit 0 at the end not to make make-boot-splash set the exit value

* Tue Jul 30 2002 Pixel <pixel@mandrakesoft.com> 3.1.6-29mdk
- integrate patch from Brian J. Murrell to allow LVM on /

* Fri Mar  1 2002 Warly <warly@mandrakesoft.com> 3.1.6-28mdk
- fix error when SPLASH=no

* Mon Feb 18 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6-27mdk
- Remove the echo 0 of splash screen from here.

* Fri Feb  8 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6-26mdk
- Add themes support to splash.

* Thu Feb  7 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-25mdk
- change splash patch (chmou)

* Wed Feb  6 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-24mdk
- xfs now requires xfs_dmapi instead of pagebuf, so try to find both
  modules (for juan new kernel)

* Tue Feb  5 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-23mdk
- update splash patch from chmouel

* Wed Jan 30 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-22mdk
- use mkinitrd-boot-splash.diff from chmouel

* Mon Jan 28 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-21mdk
- as suggested by Borsenkow Andrej <Andrej.Borsenkow@mow.siemens.ru>,
  mount devfs with device "none" for consistency

* Fri Jan 25 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-20mdk
- use relative symlinks in the initrd, because ls from new fileutils
  produced "No such file or directory" on broken symlinks

* Thu Jan 17 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-19mdk
- now that find has been moved to /bin we use find again (speed)
- as suggested on cooker, cleanup even in failure case (using trap)

* Wed Jan 16 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-18mdk
- exclude modules found with "build" in the path so that we don't end
  up with modules from /lib/modules/*/build/../../../usr/src/*/...

* Wed Jan  9 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-17mdk
- two small fixes pointed by Reinhard Katzmann <suamor@gmx.net>
  - overriden rootdev definition
  - broken symlink bin -> bin in /sbin of initrd

* Wed Dec 19 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-16mdk
- small patch from chmouel on chmouel's patch
- really can work without /usr by removing one remaining "find" and by
  emulating "wc -w" with a for

* Wed Dec 19 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-15mdk
- replace `find' (which is in /usr/bin) by a shell-based equivalent
  => mkinitrd should be usable without /usr mounted, now, hopefully
- fix no-url-tag

* Mon Dec 17 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-14mdk
- integrate Chmouel's patch [to check that the tmpdir underlying fs is not
  tmpfs nor nfs (since we need lomount capability)]

* Tue Dec 11 2001 Stew Benedict <sbenedict@mandrakesoft.com> 3.1.6-13mdk
- kernel 2.4.16 brings PPC behavior of real-root-device inline with x86
- reverse patches for 2.4

* Tue Nov 27 2001 Stew Benedict <sbenedict@mandrakesoft.com> 3.1.6-12mdk
- merge patches to correct endian problem with real-root-dev mounts at boot

* Wed Nov 14 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-11mdk
- use Greg Edwards <gedwards@fireweed.org> patch to fix problem where SCSI
  modules were not loaded in the correct order (I suck)

* Tue Oct 16 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-10mdk
- fix obsolete-tag Copyright
- fix strange-permission

* Sat Sep 22 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-9mdk
- parses mount options to correctly feed the mount flags and the mount
  options

* Fri Sep 14 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-8mdk
- integrate gb's patch to support ia64
- back to the use of insmod-from-busybox on ix86 arch, the 2.4 kernel
  is so large "mkbootdisk" fails in almost all situations now :-(
- refine Requires:

* Fri Sep 14 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-7mdk
- argh, rootflags broke root on loopback, fix
- safety: when a mount with flags fails, try to mount without the flags

* Thu Sep 13 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-6mdk
- remove duplicate scsi modules for safety

* Thu Sep 13 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-5mdk
- use mount opts from /etc/fstab for root fs
- ifneeded -> force need when / is ext3 (for cases when ext3 would be non
  modular); and when / has mount opts
- try to sync man pages with actual code

* Sun Sep  9 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-4mdk
- don't keep old bug of using 'ide-cd' module (juan)
- support new form of "probeall scsi_hostadapter" in modules.conf (pixel)
- don't load sd_mod and scsi_mod when not really needed (ide-scsi,
  usb-storage, etc) (pixel)
- support compressed modules with simpler stuff than ZMODULES
- when / is ext3 and we're on a 2.2 kernel, fallback to ext2
- don't use pivot_root with a 2.2 kernel, it's not implemented ;p

* Fri Sep  7 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-3mdk
- support XFS (chmouel)
- say that our version is "3.1.6-mdk" to tell that it's patched for mdk

* Fri Sep  7 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-2mdk
- honours quiet mode (again) (needed to fix a RH bug, ouch)

* Wed Sep  5 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.6-1mdk
- synchronize with redhat stuff (for their way of mounting root fs)
- try to keep all (good) our patches, hope not too much is broken...

* Mon Aug 20 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0.1-1mdk
- because of devfs, I need to have my special dev files in another
  directory than /dev, because devfs will shadow my dev files :-(
  (applies to loopback-on-/ and raid-on-/)
- use IS_IX86 instead of the is_ix86 function

* Fri Aug  3 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0-1mdk
- we had a very large and silly patch on official 2.7 (385 lines of
  patch on a 450 lines original file), fork to ease maintainance
- merge RH interesting changes (mkinitrd-3.1.5 from RH)
  - added checks to load the modules i2o_block needs
  - skip errors finding jbd as a module if we're skipping them trying to find
  ext3 so that you can build a kernel with ext3 built-in and still use an
  initrd (MDK: we don't have ext3 yet, but we'll have it soon)
- prepend /(I|W|E):/ in front of all messages
- don't let "cat" fail on empty files in verbose mode

* Tue Apr 10 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.7-11mdk
- initrd_helper honours quiet mode
- rip rh idea to have a fake modprobe in order to remove kmod problems

* Fri Apr  6 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.7-10mdk
- import rh raid autorun stuff in mkinitrd_helper and mkinitrd
- grab a small rh raid fix (raid5 -> xor)
- use only one patch

* Fri Mar 23 2001 Pixel <pixel@mandrakesoft.com> 2.7-9mdk
- auto-adjust the number of inodes

* Sat Mar 17 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.7-8mdk
- use fix for insmod-busybox-dietlibc

* Fri Mar 16 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.7-7mdk
- use my own smaller code rather than sash+insmod.static for ix86

* Mon Mar  5 2001 Pixel <pixel@mandrakesoft.com> 2.7-6mdk
- compute the size really needed for initrd

* Sun Mar  4 2001 Pixel <pixel@mandrakesoft.com> 2.7-5mdk
- fix always making an initrd (ifneeded broken)

* Thu Mar  1 2001 Pixel <pixel@mandrakesoft.com> 2.7-4mdk
- fix last patch

* Tue Feb 27 2001 Pixel <pixel@mandrakesoft.com> 2.7-3mdk
- enable-use-of-gziped-modules.patch

* Sun Feb 11 2001 Pixel <pixel@mandrakesoft.com> 2.7-2mdk
- add require mktemp >= 1.5-9mdk (for option -d)

* Thu Dec 21 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.7-1mdk
- new and shiny source.

* Tue Nov 28 2000 Pixel <pixel@mandrakesoft.com> 2.6-2mdk
- fix typo patch. Still need a new mktemp that handles -d

* Sat Nov 25 2000 Pixel <pixel@mandrakesoft.com> 2.6-1mdk
- new version
- patch for case of no scsi needed and scsi_mod is in module

* Wed Aug 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5-2mdk
- bug fix

* Mon Aug 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5-1mdk
- update for hackkernel (new modules layout)
- remove exclusiveos:linux (rms'll be happy)
- make it noarch

* Fri Jul 28 2000 Pixel <pixel@mandrakesoft.com> 2.4.3-3mdk
- modified the mdk patch: don't do "insmod the.o || insmod -f the.o" because
sash doesn't handle it :(

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 2.4.3-2mdk
- BM

* Sun Jun 25 2000 Pixel <pixel@mandrakesoft.com> 2.4.3-1mdk
- merge with redhat (mainly modules.conf by default)

* Thu Jun  1 2000 Bill Nottingham <notting@redhat.com>
- build on ia64
- bump up initrd size on ia64
- modules.confiscation, /usr/man -> /usr/share/man

* Thu May 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.3.2-16mdk
- Thanks my god initrd work on alpha !!!.

* Tue May  9 2000 Pixel <pixel@mandrakesoft.com> 2.3.2-15mdk
- add possibility to modules to ignore via env var IGNOREMODS

* Wed May  3 2000 Pixel <pixel@mandrakesoft.com> 2.3.2-14mdk
- patch for skipping usb-storage

* Tue Apr 18 2000 Pixel <pixel@mandrakesoft.com> 2.3.2-13mdk
- add handling of non-ext2 root filesytems (again :()

* Mon Apr 17 2000 Pixel <pixel@mandrakesoft.com> 2.3.2-12mdk
- insmod -f instead of insmod

* Sat Mar 25 2000 Pixel <pixel@mandrakesoft.com> 2.3.2-11mdk
- new group

* Sun Mar 19 2000 John Buswell <johnb@mandrakesoft.com> 2.3.2-10mdk
- Added ppc and k7 arch
- Fixed bzipping of man pages

* Mon Mar 13 2000 Pixel <pixel@mandrakesoft.com> 2.3.2-9mdk
- do not require ash.static but sash
- add requires sash >= 3.4

* Mon Mar 13 2000 Pixel <pixel@mandrakesoft.com> 2.3.2-8mdk
- add loopback handling

* Thu Jan  6 2000 Pixel <pixel@mandrakesoft.com>
- fix *buggy* grep scsi_hostadapter on conf.modules

* Mon Jan  3 2000 Pixel <pixel@mandrakesoft.com>
- fix to skip ide-scsi.o (overkill :)

* Tue Dec 28 1999 Pixel <pixel@mandrakesoft.com>
- fix to skip ppa.o and imm.o
- fix a typo

* Tue Oct 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.3.2.

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Upgrade to 2.0.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Thu Feb 25 1999 Matt Wilson <msw@redhat.com>
- updated description

* Mon Jan 11 1999 Matt Wilson <msw@redhat.com>
- Ignore the absence of scsi modules, include them if they are there, but
  don't complain if they are not.
- changed --no-scsi-modules to --omit-scsi-modules (as it should have been)

* Thu Nov  5 1998 Jeff Johnson <jbj@redhat.com>
- import from ultrapenguin 1.1.

* Tue Oct 20 1998 Jakub Jelinek <jj@ultra.linux.cz>
- fix for combined sparc/sparc64 insmod, also pluto module is really
  fc4:soc:pluto and we don't look at deps, so special case it.

* Sat Aug 29 1998 Erik Troan <ewt@redhat.com>
- replaced --needs-scsi-mods (which is now the default) with
  --omit-scsi-mods

* Fri Aug  7 1998 Jeff Johnson <jbj@redhat.com>
- correct obscure regex/shell interaction (hardwires tabs on line 232)

* Mon Jan 12 1998 Erik Troan <ewt@redhat.com>
- added 'make archive' rule to Makefile
- rewrote install procedure for more robust version handling
- be smarter about grabbing options from /etc/conf.modules

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- made it use /bin/ash.static

* Wed Apr 16 1997 Erik Troan <ewt@redhat.com>
- Only use '-s' to install binaries if /usr/bin/strip is present.
- Use an image size of 2500 if binaries can't be stripped (1500 otherwise)
- Don't use "mount -o loop" anymore -- losetup the proper devices manually
- Requires losetup, e2fsprogs

* Wed Mar 12 1997 Michael K. Johnson <johnsonm@redhat.com>
- Fixed a bug in parsing options.
- Changed to use a build tree, then copy the finished tree into the
  image after it is built.
- Added patches derived from ones written by Christian Hechelmann which
  add an option to put the kernel version number at the end of the module
  name and use install -s to strip binaries on the fly.
