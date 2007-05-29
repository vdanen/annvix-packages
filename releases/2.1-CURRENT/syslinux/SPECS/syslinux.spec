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
%define version 	3.35
%define release 	%_revrel

%define pxebase		/var/lib/tftpboot/X86PC/linux

Summary:	A bootloader for linux using floppies, CD or PXE
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://syslinux.zytor.com/

Source0:	http://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{version}.tar.bz2
Source1:	pxelinux-help.txt
Source2:	pxelinux-messages
Source3:	pxelinux-default
Patch0:         syslinux-3.11-mdv-vfat.patch
Patch1:		syslinux-3.35-opensuse-pre.patch
Patch2:		syslinux-3.20-mdv-date.patch
Patch3:		syslinux-3.31-mdv-system_png.patch
Patch4:		syslinux-3.20-mdv-png_com32.patch
# no idea if these need to be rediffed or not; they're currently not applied
Patch6:		syslinux-1.76-avx-nostack.patch
Patch7:		syslinux-2.13-avx-nostack.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	nasm >= 0.97
BuildRequires:	netpbm
BuildRequires:	png-static-devel

ExclusiveArch:	%{ix86}
Obsoletes:	isolinux < %{version}
Provides:	isolinux = %{version}

%description
SYSLINUX is a boot loader for the Linux operating system which
operates off an MS-DOS/Windows FAT filesystem.  It is intended to
simplify first-time installation of Linux, and for creation of rescue-
and other special-purpose boot disks.


%package -n pxelinux
Summary:	A PXE bootloader
Group:		System/Kernel and hardware
Requires:	syslinux

%description -n pxelinux
PXELINUX is a PXE bootloader.


%package devel
Summary:	Development environment for SYSLINUX add-on modules
Group:		Development/Other
Requires:	syslinux

%description devel
The SYSLINUX boot loader contains an API, called COM32, for writing
sophisticated add-on modules.  This package contains the libraries
necessary to compile such modules.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
#%patch7 -p1 -b .nostack
%patch0 -p1 -b .vfat
%patch1 -p1 -b .gfx
%patch2 -p1 -b .bootdir
%patch3 -p1 -b .syspng
install %{_includedir}/png.h %{_includedir}/pngconf.h com32/include
%patch4 -p1
#%patch6 -p1 -b .nostack


%build
chmod +x add_crc
%make DATE="Annvix"
mv isolinux.bin isolinux.bin.normal

perl -pi -e 's,^(isolinux_dir.*)/isolinux,$1/x86_64/isolinux,' isolinux.asm
%make DATE="Mandriva Linux" isolinux.bin
mv isolinux.bin isolinux-x86_64.bin

perl -pi -e 's,^(isolinux_dir.*)/x86_64/isolinux,$1/i586/isolinux,' isolinux.asm
%make DATE="Annvix" isolinux.bin
mv isolinux.bin isolinux-i586.bin

mv isolinux.bin.normal isolinux.bin


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%make install \
    INSTALLROOT=%{buildroot} \
    BINDIR=%{_bindir} \
    SBINDIR=%{_sbindir} \
    LIBDIR=%{_libdir} \
    INCDIR=%{_includedir}

mkdir -p %{buildroot}%{_libdir}/%{name}/menu
cp -av menu/* %{buildroot}%{_libdir}/%{name}/menu/

cp gethostip sha1pass mkdiskimage sys2ansi.pl keytab-lilo.pl %{buildroot}%{_libdir}/syslinux

mkdir -p %{buildroot}%{pxebase}/pxelinux.cfg
install -m 0644 %{_sourcedir}/pxelinux-help.txt %{buildroot}%{pxebase}/help.txt
install -m 0644 %{_sourcedir}/pxelinux-messages %{buildroot}%{pxebase}/messages
install -m 0644 %{_sourcedir}/pxelinux-default %{buildroot}%{pxebase}/pxelinux.cfg/default
perl -pi -e "s|VERSION|%version|g" %{buildroot}%{pxebase}/messages
install -m 0644 pxelinux.0 %{buildroot}%{pxebase}/linux.0
install -m 0644 memdisk/memdisk %{buildroot}%{pxebase}/memdisk
install -m 0644 isolinux-i586.bin %{buildroot}%{_libdir}/syslinux/
install -m 0644 isolinux-x86_64.bin %{buildroot}%{_libdir}/syslinux/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%exclude %{_libdir}/%{name}/com32
%exclude %{_libdir}/%{name}/menu
%{_libdir}/%{name}/*

%files -n pxelinux
%{pxebase}/*.0
%{pxebase}/memdisk
%config(noreplace) %{pxebase}/messages
%config(noreplace) %{pxebase}/help.txt
%config(noreplace) %{pxebase}/pxelinux.cfg/default

%files devel
%defattr(-,root,root)
%{_libdir}/syslinux/com32
%{_libdir}/%{name}/menu

%files doc
%defattr(-,root,root)
%doc COPYING NEWS README TODO
%doc syslinux.doc isolinux.doc pxelinux.doc


%changelog
* Mon May 28 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.35
- 3.35
- drop P1 (ASM graphic patch); no longer maintained
- drop P4; no longer required
- updated P0 from Mandriva
- P1: GFX support and build fixes (CLT_TCK); from OpenSUSE
- P2: correctly pass DATE when running make in subdirs; from Mandriva
- P3, P4: use the system libpng; from Mandriva
- package mkdiskimage, gethostip, and sha1pass
- split pxelinux into it's own package
- add isolinux-x86_64

* Thu Apr 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.76
- rebuild against rebuilt netpbm

* Fri Jun 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.76
- rebuild against new netpbm

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.76
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.76
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.76
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
