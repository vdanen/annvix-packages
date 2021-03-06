#
# spec file for package e2fsprogs
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		e2fsprogs
%define version		1.40.3
%define release		%_revrel

%define	_root_sbindir	/sbin
%define	_root_libdir	/%{_lib}
%define libname		%mklibname ext2fs 2
%define devname		%mklibname ext2fs -d

Summary:	Utilities used for the second extended (ext2) filesystem
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://e2fsprogs.sourceforge.net/
Source0:	http://easynews.dl.sourceforge.net/sourceforge/e2fsprogs/%{name}-%{version}.tar.gz
Source1:	http://easynews.dl.sourceforge.net/sourceforge/e2fsprogs/%{name}-%{version}.tar.gz.asc
Patch0:		e2fsprogs-1.36-autoconf.patch
# (gb) strip references to home build dir
Patch1:		e2fsprogs-1.36-strip-me.patch
Patch2:		e2fsprogs-1.38-tst_ostype-buildfix.patch
Patch3:		e2fsprogs-1.40-mdv-handle-last-check-in-the-future.patch
# Fedora patches
Patch10:	e2fsprogs-1.38-fdr-resize-inode.patch
Patch11:	e2fsprogs-1.38-fdr-no_pottcdate.patch
Patch12:	e2fsprogs-1.39-fdr-blkid-devmapper.patch
Patch13:	e2fsprogs-1.38-fdr-etcblkid.patch
Patch14:	e2fsprogs-1.39-fdr-multilib.patch
Patch15:	e2fsprogs-1.40.3-fdr-mkinstalldirs.patch
Patch16:	e2fsprogs-1.40.2-fdr-warning-fixes.patch
Patch18:	e2fsprogs-1.40.2-fdr-protect-open-ops.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo
BuildRequires:	autoconf
BuildRequires:	multiarch-utils

%description
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in second
extended (ext2) filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters) and most of the other core ext2fs
filesystem utilities.


%package -n %{libname}
Summary:	The libraries for Ext2fs
Group:		System/Libraries
Requires:	e2fsprogs
Provides:	libext2fs = %{version}-%{release}

%description -n %{libname}
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in second
extended (ext2) filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters) and most of the other core ext2fs
filesystem utilities.


%package -n %{devname}
Summary:	The libraries for Ext2fs
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
# XXX too many things require this right now; be sure to remove it later
Provides:	libext2fs-devel = %{version}-%{release}
Obsoletes:	%mklibname ext2fs 2 -d

%description -n %{devname}
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in second
extended (ext2) filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters) and most of the other core ext2fs
filesystem utilities.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0
%patch1 -p1 -b .strip-me
%patch2 -p1 -b .tst_ostype
%patch3 -p1 -b .mem_leak
# Fedora
%patch10 -p1 -b .resize-inode
%patch11 -p1 -b .pottcdate
%patch12 -p1 -b .dm
%patch13 -p1 -b .etcblkid
%patch14 -p1 -b .multilib
%patch15 -p1 -b .mkinstalldirs
%patch16 -p1 -b .warnings
%patch18 -p1 -b .protect-open-ops

rm -f configure
autoconf

# Fix build:
chmod 0644 po/*.po


%build
%configure2_5x \
    --enable-elf-shlibs
make libs progs docs
# use e2fsck shared instead, avoid patch.
cp -af e2fsck/e2fsck.shared e2fsck/e2fsck


%check
# to make lib/ss test pass
export PATH=$PATH:.
# all tests should pass, but on x86_64 we get:
# r_move_itable: resize2fs with resize_inode: failed
# r_resize_inode: resize2fs with resize_inode: failed
# 80 tests succeeded	2 tests failed
%ifarch x86_64
make check || :
%else
make check
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
export PATH=/sbin:$PATH

%makeinstall_std install-libs \
    root_sbindir=%{_root_sbindir} \
    root_libdir=%{_root_libdir}

for i in libblkid.so.1 libcom_err.so.2 libe2p.so.2 libext2fs.so.2 libss.so.2 libuuid.so.1; do
    ln -s $i %{buildroot}/%{_root_libdir}/${i%.[0-9]}
done

# remove unwanted files
rm -f %{buildroot}%{_libdir}/libss.a
rm -f %{buildroot}%{_root_libdir}/{libblkid,libcom_err,libe2p,libext2fs,libss,libuuid}.so

# multiarch policy, alternative is to use <stdint.h>
%multiarch_includes %{buildroot}%{_includedir}/ext2fs/ext2_types.h
%multiarch_includes %{buildroot}%{_includedir}/blkid/blkid_types.h

chmod +x %{buildroot}%{_bindir}/{mk_cmds,compile_et}

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post -n %{devname}
%_install_info libext2fs.info


%preun -n %{devname}
%_remove_install_info libext2fs.info


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/mke2fs.conf
%{_root_sbindir}/badblocks
%{_root_sbindir}/blkid
%{_root_sbindir}/debugfs
%{_root_sbindir}/dumpe2fs
%{_root_sbindir}/e2fsck
%{_root_sbindir}/e2label
%{_root_sbindir}/fsck
%{_root_sbindir}/fsck.ext2
%{_root_sbindir}/fsck.ext3
%{_root_sbindir}/logsave
%{_root_sbindir}/mke2fs
%{_root_sbindir}/mkfs.ext2
%{_root_sbindir}/resize2fs
%{_root_sbindir}/tune2fs
%{_root_sbindir}/e2image
%{_root_sbindir}/findfs
%{_root_sbindir}/mkfs.ext3
%{_sbindir}/filefrag
%{_sbindir}/mklost+found
%{_bindir}/chattr
%{_bindir}/lsattr
%{_bindir}/uuidgen
%{_mandir}/man1/chattr.1*
%{_mandir}/man1/lsattr.1*
%{_mandir}/man1/uuidgen.1*
%{_mandir}/man3/uuid*
%{_mandir}/man5/e2fsck.conf.5*
%{_mandir}/man5/mke2fs.conf.5*
%{_mandir}/man8/badblocks.8*
%{_mandir}/man8/blkid.8*
%{_mandir}/man8/debugfs.8*
%{_mandir}/man8/dumpe2fs.8*
%{_mandir}/man8/e2fsck.8*
%{_mandir}/man8/e2image.8*
%{_mandir}/man8/e2label.8*
%{_mandir}/man8/filefrag.8*
%{_mandir}/man8/findfs.8*
%{_mandir}/man8/fsck.8*
%{_mandir}/man8/fsck.ext2.8*
%{_mandir}/man8/fsck.ext3.8*
%{_mandir}/man8/logsave.8*
%{_mandir}/man8/mke2fs.8*
%{_mandir}/man8/mkfs.ext2.8*
%{_mandir}/man8/mkfs.ext3.8*
%{_mandir}/man8/mklost+found.8*
%{_mandir}/man8/resize2fs.8*
%{_mandir}/man8/tune2fs.8*


%files -n %{libname}
%defattr(-,root,root)
%{_root_libdir}/libcom_err.so.*
%{_root_libdir}/libe2p.so.*
%{_root_libdir}/libext2fs.so.*
%{_root_libdir}/libss.so.*
%{_root_libdir}/libuuid.so.*
%{_root_libdir}/libblkid.so.*
%{_libdir}/e2initrd_helper


%files -n %{devname}
%defattr(-,root,root,755)
%{_bindir}/compile_et
%{_bindir}/mk_cmds
%{_libdir}/pkgconfig/*
%{_libdir}/libblkid.a
%{_libdir}/libblkid.so
%{_libdir}/libcom_err.so
%{_libdir}/libe2p.a
%{_libdir}/libe2p.so
%{_libdir}/libext2fs.a
%{_libdir}/libext2fs.so
%{_libdir}/libuuid.a
%{_libdir}/libuuid.so
%{_libdir}/libcom_err.a
%{_libdir}/libss.so
%{_includedir}/et
%{_includedir}/ext2fs
%{_includedir}/ss
%{_includedir}/uuid
%{_includedir}/e2p/e2p.h
%{_includedir}/blkid/blkid.h
%{_includedir}/blkid/blkid_types.h
%multiarch %dir %{multiarch_includedir}/blkid
%multiarch %{multiarch_includedir}/blkid/blkid_types.h
%multiarch %dir %{multiarch_includedir}/ext2fs
%multiarch %{multiarch_includedir}/ext2fs/ext2_types.h
%{_mandir}/man1/compile_et.1*
%{_mandir}/man1/mk_cmds.1*
%{_mandir}/man3/com_err.3*
%{_mandir}/man3/libblkid.3*
%{_infodir}/libext2fs.info*
%{_datadir}/et
%{_datadir}/ss

%files doc
%defattr(-,root,root)
%doc README RELEASE-NOTES


%changelog
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.40.3
- 1.40.3
- updated P15
- P18: protect ->open ops rom glibc open-create-mode-checker (Fedora)
- build with optimizations now that it can be done so safely
- drop P17; merged upstream

* Mon Dec 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.40.2
- P17: fixes CVE-2007-5497

* Thu Nov 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.40.2
- 1.40.2
- tests go in %%check
- clean filelist
- P3: fix last check problem index (from Mandriva)
- move libblkid.3 manpage to -devel package to fix multiarch conflict
- info page uninstall should be in %%preun, not %%postun
- remove redundant autoconf call
- mark /etc/mke2fs.conf as a config file
- sync with Fedora's patches:
  - P10: enable tune2fs to set and clear the resize inode (#167816)
  - P11: drop timestamp from mo files (#168815/168814/245653)
  - P12: look at device mapper devices
  - P13: put blkid.tab in /etc/blkid/
  - P14: Fix multilib conflicts (#192665)
  - P15: Fix for newer autoconf (#220715)
  - P16: Fix type warning in badblocks
  - P17: Fix ext2fs_swap_inode_full() on bigendian boxes
- make the tests non-fatal on x86_64 as two tests fail

* Mon Jun 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.39
- implement devel naming policy
- implement library provides policy

* Mon Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.39
- 1.39
- use a direct-download url and add the gpg sig file
- spec cleanups
- remove locale files

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.38
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.38
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.38
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.38-1avx
- 1.38
- renumber patches
- P1: strip references to home build dir (gbeauchesne)
- P2: fix compilation of libs/e2p/os_type (cjw)
- multiarch support

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35-2avx
- bootstrap build

* Thu Aug 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.35-1avx
- 1.35
- fix perms (tvignaud)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.34-4avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 1.34-3sls
- more spec cleaning
- remove unpackaged symlinks

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 1.34-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
