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
%define version		1.39
%define release		%_revrel

%define	_root_sbindir	/sbin
%define	_root_libdir	/%{_lib}
%define libname		%mklibname ext2fs 2

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
Patch3:		e2fsprogs-1.39-ubu-CVE-2007-5497.patch

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


%package -n %{libname}-devel
Summary:	The libraries for Ext2fs
Group:		Development/C
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel
Provides:	libext2fs-devel
Provides:	libe2fsprogs-devel

%description -n %{libname}-devel
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
%patch3 -p1 -b .cve-2007-5497
rm -f configure
autoconf

# Fix build:
chmod 0644 po/*.po


%build
autoconf
OPT_FLAGS=`echo %{optflags} | sed -e "s/-fomit-frame-pointer//g"`
# (gb) 1.23-3mdk: e2fsck may work will full optimizations but without strict-aliasing
CFLAGS="%{optflags} -fno-omit-frame-pointer -O1 -fno-strict-aliasing"
%configure2_5x \
    --enable-elf-shlibs
make libs progs docs
# use e2fsck shared instead, avoid patch.
cp -af e2fsck/e2fsck.shared e2fsck/e2fsck
# all tests must pass
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
export PATH=/sbin:$PATH

make install install-libs \
    DESTDIR="%{buildroot}" \
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


%post -n %{libname}-devel
%_install_info libext2fs.info


%postun -n %{libname}-devel
%_remove_install_info libext2fs.info


%files -f %{name}.lang
%defattr(-,root,root)
%{_sysconfdir}/mke2fs.conf
%{_root_sbindir}/badblocks
%{_root_sbindir}/debugfs
%{_root_sbindir}/dumpe2fs
%{_root_sbindir}/e2fsck
%{_root_sbindir}/e2label
%{_root_sbindir}/fsck
%{_root_sbindir}/fsck.ext2
%{_root_sbindir}/fsck.ext3
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
%{_mandir}/man8/debugfs.8*
%{_mandir}/man8/dumpe2fs.8*
%{_mandir}/man8/e2fsck.8*
%{_mandir}/man8/e2image.8.bz2
%{_mandir}/man8/e2label.8*
%{_mandir}/man8/filefrag.8*
%{_mandir}/man8/findfs.8.bz2
%{_mandir}/man8/fsck.8*
%{_mandir}/man8/fsck.ext2.8.bz2
%{_mandir}/man8/fsck.ext3.8.bz2
%{_mandir}/man8/mke2fs.8*
%{_mandir}/man8/mkfs.ext2.8.bz2
%{_mandir}/man8/mkfs.ext3.8.bz2
%{_mandir}/man8/mklost+found.8*
%{_mandir}/man8/resize2fs.8*
%{_mandir}/man8/tune2fs.8*

%{_root_sbindir}/blkid
%{_mandir}/man8/blkid.8.bz2
%{_root_sbindir}/logsave
%{_mandir}/man8/logsave.8.bz2


%files -n %{libname}
%defattr(-,root,root)
%{_root_libdir}/libcom_err.so.*
%{_root_libdir}/libe2p.so.*
%{_root_libdir}/libext2fs.so.*
%{_root_libdir}/libss.so.*
%{_root_libdir}/libuuid.so.*

%{_root_libdir}/libblkid.so.*
%{_mandir}/man3/libblkid.3.bz2
%{_libdir}/e2initrd_helper

%files -n %{libname}-devel
%defattr(-,root,root,755)
%{_infodir}/libext2fs.info*
%{_bindir}/compile_et
%{_mandir}/man1/compile_et.1*
%{_bindir}/mk_cmds
%{_mandir}/man1/mk_cmds.1.bz2
%{_libdir}/pkgconfig/*

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

%_datadir/et
%_datadir/ss
%{_includedir}/et
%{_includedir}/ext2fs
%multiarch %dir %{multiarch_includedir}/ext2fs
%multiarch %{multiarch_includedir}/ext2fs/ext2_types.h
%{_includedir}/ss
%{_includedir}/uuid
%{_includedir}/e2p/e2p.h
%{_mandir}/man3/com_err.3*

%{_includedir}/blkid/blkid.h
%{_includedir}/blkid/blkid_types.h
%multiarch %dir %multiarch_includedir/blkid
%multiarch %multiarch_includedir/blkid/blkid_types.h
%{_libdir}/libblkid.a

%files doc
%defattr(-,root,root)
%doc README RELEASE-NOTES


%changelog
* Mon Dec 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.39
- P3: security fix for CVE-2007-5497

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
