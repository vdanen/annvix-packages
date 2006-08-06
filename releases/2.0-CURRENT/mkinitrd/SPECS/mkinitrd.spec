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
%define version 	4.2.17
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
Source1:	mkinitrd-insmod-3.5.24.tar.bz2
Patch0:		mkinitrd-%{version}-mdk.patch
Patch1:		mkinitrd-4.2.17-label.patch
Patch2:		mkinitrd-4.2.17-cdrom.patch
Patch3:		mkinitrd-4.2.17-migrate-mptscsih.patch
Patch4:		mkinitrd-4.2.17-use-both-ahci-ata_piix.patch
Patch5:		mkinitrd-4.2.17-initramfs.patch
Patch6:		mkinitrd-4.2.17-resume.patch
Patch7:		mkinitrd-4.2.17-closedir.patch
Patch8:		mkinitrd-4.2.17-dmraid.patch
Patch9:		mkinitrd-4.2.17-evms.patch
Patch10:	mkinitrd-4.2.17-scsidriver.patch
Patch11:	mkinitrd-4.2.17-initramfs-dsdt.patch
Patch12:	mkinitrd-4.2.17-ide.patch
Patch13:	mkinitrd-4.2.17-avx-fix_switchroot.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl
%if %{use_dietlibc}
BuildRequires:	dietlibc-devel
%else
BuildRequires:	glibc-static-devel
Requires:	/sbin/insmod.static
%endif

Requires:	mktemp >= 1.5-9mdk
Requires:	e2fsprogs
Requires:	/bin/sh
Requires:	coreutils
Requires:	grep
Requires:	mount
Requires:	gzip
Requires:	tar
Requires:	findutils >= 4.1.7-3mdk
Requires:	gawk
Requires:	cpio
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
%patch0 -p1 -b .mdk
%patch1 -p1 -b .label
%patch2 -p1 -b .cdrom
%patch3 -p1 -b .migrate-mptscsih
%patch4 -p1 -b .use-both-ahci-ata_piix
%patch5 -p1 -b .initramfs
%patch6 -p1 -b .resume
%patch7 -p1 -b .closedir
%patch8 -p1 -b .dmraid
%patch9 -p1 -b .evms
%patch10 -p1 -b .scsidriver
%patch11 -p1 -b .initramfs-dsdt
%patch12 -p1 -b .ide
%patch13 -p1 -b .fix_switchroot


%build
%if %{use_dietlibc}
%ifarch x86_64
perl -pi -e 's| gcc | x86_64-annvix-linux-gnu-gcc |g' mkinitrd_helper-subdir/insmod-busybox/Makefile
perl -pi -e 's| gcc | x86_64-annvix-linux-gnu-gcc |g' mkinitrd_helper-subdir/insmod-module-init-tools/Makefile
%endif
make DIET=1
%else
make
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make BUILDROOT=%{buildroot} mandir=%{_mandir} install
%if %{use_dietlibc}
cp insmod/insmod %{buildroot}/sbin/insmod-DIET
%endif


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-, root, root)
/sbin/*
%{_mandir}/*/*


%changelog
* Sun Aug 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.17
- 4.2.17 (sync completely with mdv 4.2.17-20mdv)
- P13: make switchroot work properly (thanks Thomas)
- clean spec

* Mon Apr 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.43
- update P5 to test for insmod.static-25 before trying to install it in
  the initrd

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
