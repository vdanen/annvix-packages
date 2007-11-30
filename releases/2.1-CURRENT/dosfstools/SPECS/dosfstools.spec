#
# spec file for package dosfstools
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		dosfstools
%define version 	2.11
%define release 	%_revrel

Summary:	Utilities to create and check MS-DOS FAT filesystems
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		ftp://ftp.uni-erlangen.de/pub/Linux/LOCAL/dosfstools
Source:		ftp://ftp.uni-erlangen.de/pub/Linux/LOCAL/dosfstools/%{name}-%{version}.src.tar.bz2
Patch0:		dosfstools-2.7-argfix.patch
Patch1:		dosfstools-2.11-assumeKernel26.patch
Patch2:		dosfstools-2.11-lseek.patch
Patch3:		dosfstools-2.11-fortify.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Obsoletes:	mkdosfs-ygg
Provides:	mkdosfs-ygg = %{version}

%description
Inside of this package there are two utilities to create and to
check MS-DOS FAT filesystems on either harddisks or floppies under
Linux.  This version uses the enhanced boot sector/superblock
format of DOS 3.3+ as well as provides a default dummy boot sector
code.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .argfix
%patch1 -p1 -b .assumeKernel26
%patch2 -p1 -b .lseek
%patch3 -p1 -b .fortify


%build
%make PREFIX=%{_prefix} CFLAGS="%{optflags} -Dllseek=lseek64 -D_LARGEFILE64_SOURCE"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
cp dosfsck/README README.fsck
cp mkdosfs/README README.mkdosfs
%makeinstall PREFIX=%{buildroot} MANDIR=%{buildroot}%{_mandir}/man8

rm -f %{buildroot}/sbin/fsck.*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/mkdosfs
/sbin/mkfs.msdos
/sbin/mkfs.vfat
/sbin/dosfsck
%{_mandir}/man8/*

%files doc
%defattr(-,root,root)
%doc CHANGES TODO README.fsck README.mkdosfs dosfsck/COPYING


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.11
- rebuild

* Tue Jul 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.11
- 2.11
- sync patches with Mandriva
- drop S1; building against 2.6 headers
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.10
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.10
- Obfuscate email addresses and new tagging
- Uncompress patches
- drop P1: it breaks the build

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.10-4avx
- bootstrap build (new gcc, new glibc)
- P3: fix build

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.10-3avx
- rebuild

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.10-2avx
- Annvix build

* Fri Apr 30 2004 Vincent Danen <vdanen@opensls.org> 2.10-1sls
- 2.10
- ship with 2.4 kernel header (S1) and compile against it (P0) (peroyvind)
- drop unapplied previous P0 and P1

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.9-3sls
- minor spec cleanups
- remove /sbin/fsck.*

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.9-2sls
- OpenSLS build
- tidy spec
- remove Prefix

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
