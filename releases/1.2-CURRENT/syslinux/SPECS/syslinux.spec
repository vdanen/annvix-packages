#
# spec file for package syslinux
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		syslinux
%define version 	1.76
%define release 	%_revrel

%define old_version	1.67
%define pxelinux_ver	2.13

Summary:	A bootloader for linux using floppies, CD or PXE
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://ftp.kernel.org/pub/linux/utils/boot/syslinux/

Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-%{old_version}.tar.bz2
Source2:	%{name}-%{pxelinux_ver}.tar.bz2
Patch0:         syslinux-1.67-use-vfat-instead-of-msdos.patch
Patch1:		syslinux-1.75-graphic.patch
Patch2:		syslinux-1.76-gcc-3.3.patch
Patch3:		syslinux-1.67-gcc-3.3.patch
Patch5:		syslinux-1.76-mdk-kernel-length.patch
Patch6:		syslinux-1.76-avx-nostack.patch
Patch7:		syslinux-2.13-avx-nostack.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	nasm >= 0.97, netpbm

ExclusiveArch:	%{ix86}
Obsoletes:	isolinux < %{version}
Provides:	isolinux = %{version}

%description
SYSLINUX is a boot loader for the Linux operating system which
operates off an MS-DOS/Windows FAT filesystem.  It is intended to
simplify first-time installation of Linux, and for creation of rescue-
and other special-purpose boot disks.

This version include a patched SYSLINUX for handling VESA graphic mode.


%package devel
Summary:	Development environment for SYSLINUX add-on modules
Group:		Development/Other

%description devel
The SYSLINUX boot loader contains an API, called COM32, for writing
sophisticated add-on modules.  This package contains the libraries
necessary to compile such modules.


%prep
%setup -q
%setup -q -b 2 -n %{name}-%{pxelinux_ver}
#%patch7 -p1 -b .nostack
%setup -q -a 1 -n %{name}-%{version}
%patch0 -p0
%patch1 -p1
%patch2 -p1 -b .gcc3.3
%patch3 -p1 -b .gcc3.3
%patch5 -p1 -b .klen
#%patch6 -p1 -b .nostack


%build
make clean
make DATE="Annvix"

cd %{name}-%{old_version}
make clean
make DATE="Annvix"

cd ../../%{name}-%{pxelinux_ver}
make clean
make pxelinux.0 DATE="Annvix"
make memdisk DATE="Annvix"
make gethostip DATE="Annvix"
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}

install -p syslinux-graphic %{buildroot}%{_bindir}
install -p syslinux %{buildroot}%{_bindir}/syslinux-original
install -p %{name}-%{old_version}/syslinux %{buildroot}%{_bindir}/syslinux-old
ln -s syslinux-graphic %{buildroot}%{_bindir}/syslinux
install -m 0755 ppmtolss16 %{buildroot}%{_bindir}/ppmtolss16
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_libdir}/syslinux

#ISOLINUX PART
install -m 0644 isolinux-graphic.bin %{buildroot}%{_libdir}/syslinux
install -m 0644 isolinux.bin %{buildroot}%{_libdir}/syslinux/isolinux-original.bin
install -m 0644 %{name}-%{old_version}/isolinux.bin %{buildroot}%{_libdir}/syslinux/isolinux-old.bin
ln -s isolinux-graphic.bin %{buildroot}%{_libdir}/syslinux/isolinux.bin
install -m 0644 isolinux-debug-graphic.bin %{buildroot}%{_libdir}/syslinux
install -m 0644 isolinux-debug.bin %{buildroot}%{_libdir}/syslinux/isolinux-debug-original.bin
install -m 0644 %{name}-%{old_version}/isolinux-debug.bin %{buildroot}%{_libdir}/syslinux/isolinux-debug-old.bin
ln -s isolinux-debug-graphic.bin %{buildroot}%{_libdir}/syslinux/isolinux-debug.bin

#PXE PART
install -m 0644 pxelinux-graphic.0 %{buildroot}%{_libdir}/syslinux
install -m 0644 pxelinux.0 %{buildroot}%{_libdir}/syslinux/pxelinux-old.0
install -m 0644 ../%{name}-%{pxelinux_ver}/pxelinux.0 %{buildroot}%{_libdir}/syslinux/pxelinux.0
install -m 0755 ../%{name}-%{pxelinux_ver}/gethostip %{buildroot}%{_bindir}/gethostip
install -m 0644 ../%{name}-%{pxelinux_ver}/memdisk/memdisk %{buildroot}%{_libdir}/syslinux/memdisk
install -m 0755 ../%{name}-%{pxelinux_ver}/mkdiskimage %{buildroot}%{_bindir}

pushd ../%{name}-%{pxelinux_ver}/
    cp mkdiskimage sys2ansi.pl keytab-lilo.pl %{buildroot}%{_libdir}/syslinux
    cd com32
    make install BINDIR=%{buildroot}%{_bindir} LIBDIR=%{buildroot}%{_libdir} INCLUDEDIR=%{buildroot}%{_includedir}
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc COPYING NEWS README README.graphic TODO
%doc syslinux.doc isolinux.doc pxelinux.doc
%{_bindir}/*
%{_libdir}/syslinux/*.c32
%{_libdir}/syslinux/*.bin
%{_libdir}/syslinux/*.0
%{_libdir}/syslinux/memdisk
%{_libdir}/syslinux/*.pl
%{_libdir}/syslinux/mkdiskimage

%files devel
%defattr(-,root,root)
%{_libdir}/syslinux/com32


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- re-enable the disabling of SSP

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.76-17avx
- correct the buildroot

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.76-16avx
- bootstrap build (new gcc, new glibc)
- disable P6 and P7 for now

* Fri Jun 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.76-15avx
- rebuild
- P6, P7: build without stack protection
- add mkdiskimage
- pxelinux 2.13
- P5: for syslinux-1.76 (backport from 2.06-pre1): fix problem that
  would occassionally cause a boot failure, depending on the length
  of the kernel (blino)

* Sun Aug 01 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.76-14avx
- s/OpenSLS/Annvix/

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.76-13avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.76-12sls
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.76-11sls
- OpenSLS build
- tidy spec

* Mon Aug 25 2003 Erwan Velu <erwan@mandrakesoft.com> 1.76-10mdk
- New pxelinux 2.06 
-- Fix problem that would occationally cause a boot failure, depending on the length of the kernel
* Tue Aug 12 2003 Erwan Velu <erwan@mandrakesoft.com> 1.76-9mdk
- New pxelinux 2.05
* Mon Jul 14 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.76-8mdk
- rebuild
- quiet setup
- fix gcc-3.3 build (P2, P3 & P4)

* Thu Apr 24 2003  <erwan@ke.mandrakesoft.com> 1.76-7mdk
- Fixing buildrequires (thx to Stefan van der Eijk )

* Thu Apr 17 2003 <erwan@mandrakesoft.com> 1.76-7mdk
- New version of pxelinux & memdisk (2.04)

* Mon Apr 14 2003  <erwan@ke.mandrakesoft.com> 1.76-6mdk
- New version of pxelinux & memdisk (2.03)
-- Actually support comment lines in the configuration file.
-- PXELINUX: Try to resolve some problems with stack switches.
-- PXELINUX: Handle PXE stacks with broken routing.
      With these workarounds, the remote install PXE boot floppy
      (rbfg.exe) from Argon Technologies should work correctly.
-- Fix problems with Perl scripts in UTF-8 locales.
-- MEMDISK: Now supports gzip compressed images.

* Fri Feb 28 2003 Erwan Velu <erwan@mandrakesoft.com> 1.76-5mdk
- New version of pxelinux (2.02)

* Thu Jan 16 2003 Erwan Velu <erwan@mandrakesoft.com> 1.76-4mdk
- Including new version of pxelinux, memdisk and gethostip (2.00)
- Adding subversion %%{pxelinux_version}

* Fri Sep 20 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.76-3mdk
- fix double fponsux (combo)
  - patch -p1 for the patch changing msdos with vfat will not
    work for 1.67 since syslinux-1.67 is in a subdir!
  - do rebuild syslinux-1.67 as well, not only the main version

* Wed Sep 11 2002 François Pons <fpons@mandrakesoft.com> 1.76-2mdk
- added syslinux 1.67 as old version (for mkbootdisk).

* Tue Sep 03 2002 François Pons <fpons@mandrakesoft.com> 1.76-1mdk
- 1.76.

* Thu Jul 18 2002 François Pons <fpons@mandrakesoft.com> 1.75-2mdk
- fix for isolinux and pxelinux (still display prompt) in
  VESA graphic mode.

* Wed Jul 17 2002 François Pons <fpons@mandrakesoft.com> 1.75-1mdk
- ported graphic patch to syslinux, isolinux and pxelinux.
- 1.75.

* Fri Jun 28 2002 Erwan Velu <erwan@mandrakesoft.com> 1.67-6mdk
- new release of pxelinux (1.75).
- unloading memory bug fix for pxelinux (big images could be
  pxe loaded !).

* Thu May 23 2002 Erwan Velu <erwan@mandrakesoft.com> 1.67-5mdk
- including new release of pxelinux, memdisk and gethostip
  (usefull for pxe service).

* Tue Feb 26 2002 François Pons <fpons@mandrakesoft.com> 1.67-4mdk
- moved arch dependant files into /usr/lib/syslinux instead of
  /usr/lib only.

* Mon Feb 25 2002 François Pons <fpons@mandrakesoft.com> 1.67-3mdk
- fixed possible extended register corruption.
- fixed cursor displayed on some hardware.

* Mon Feb 18 2002 François Pons <fpons@mandrakesoft.com> 1.67-2mdk
- added missing gethostip and memdisk for Erwan.

* Thu Feb 05 2002 François Pons <fpons@mandrakesoft.com> 1.67-1mdk
- updated graphic patch for 1.67 release of syslinux.
- updated use vfat patch for 1.67 release of syslinux.
- merge isolinux.
- add pxelinux.
- 1.67.

* Thu Aug 30 2001 François Pons <fpons@mandrakesoft.com> 1.48-10mdk
- use syslinux-graphic by default for syslinux.

* Thu Aug 30 2001 Pixel <pixel@mandrakesoft.com> 1.48-9mdk
- use vfat instead of msdos

* Tue Jul 31 2001 Pixel <pixel@mandrakesoft.com> 1.48-8mdk
- ugly fix to ensure syslinux is rebuild (the default syslinux binary in the
  package is broken)

* Tue Jul 10 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.48-7mdk
- exclusivearch: x86
- remove translations that kill rpm build

* Tue Jul 03 2001 François Pons <fpons@mandrakesoft.com> 1.48-6mdk
- build release, update distribution tag.

* Thu May 31 2001 François Pons <fpons@mandrakesoft.com> 1.48-5mdk
- make sure msg file are interchangeable with lilo-graphic.

* Thu Aug 31 2000 François Pons <fpons@mandrakesoft.com> 1.48-4mdk
- macroszifications.
- changed the date string to "Linux-Mandrake" for syslinux-graphic.

* Mon Apr 03 2000 François Pons <fpons@mandrakesoft.com> 1.48-3mdk
- new version of graphic patch for avoiding BIOS text output when using
  graphic mode, this make things much better on screen and much more
  card are supported.
- added a small documention on graphic patch in README.graphic.
- Updated spec file and Group.

* Thu Dec 23 1999 François PONS <fpons@mandrakesoft.com> 1.48-2mdk
- corrected for unsunported TTY output in graphic mode.
- take care of ATI* and Intel* cards.

* Thu Dec 23 1999 François PONS <fpons@mandrakesoft.com> 1.48-1mdk
- first version with graphic patch.

