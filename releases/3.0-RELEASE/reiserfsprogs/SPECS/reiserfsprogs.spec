#
# spec file for package reiserfsprogs
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		reiserfsprogs
%define version		3.6.19
%define release		%_revrel
%define epoch		1

Summary:	The utilities to manage Reiserfs volumes
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPLv2-like
Group:		System/Kernel and hardware
URL:		http://www.namesys.com/
Source0:	ftp://ftp.namesys.com/pub/reiserfsprogs/%{name}-%{version}.tar.bz2
Patch1:		reiserfsprogs-3.6.2-make-the-force-option-works-in-resize_reiserfs.patch
Patch2:		reiserfsprogs-3.6.19-mdv-ubu-unaligned.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	e2fsprogs-devel

Obsoletes:	reiserfs-utils
Provides:	reiserfs-utils

%description
Reiserfs is a file system using a plug-in based object oriented variant
on classical balanced tree algorithms. The results when compared to the
ext2fs conventional block allocation based file system running under
the same operating system and employing the same buffering code suggest
that these algorithms are overall more efficient.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1
%patch2 -p1


%build
%configure2_5x
%make OPTFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8
%makeinstall

mv %{buildroot}/{usr/,}sbin
ln -s mkreiserfs %{buildroot}/sbin/mkfs.reiserfs
ln -s reiserfsck %{buildroot}/sbin/fsck.reiserfs
ln -s mkreiserfs.8 %{buildroot}%{_mandir}/man8/mkfs.reiserfs.8
ln -s reiserfsck.8 %{buildroot}%{_mandir}/man8/fsck.reiserfs.8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README ChangeLog


%changelog
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19
- rebuild against new e2fsprogs
- P2 was 0 bytes before; really apply the patch and commit it

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19
- update the description
- update the license
- P2: patch to avoid use of unaligned.h which no longer exists
- buildrequires e2fsprogs to get uuid generation support

* Sat Jun 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19-2avx
- rebuild

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19-1avx
- 3.6.19

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.6.11-3avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.6.11-2sls
- minor spec cleanups

* Fri Jan 09 2004 Vincent Danen <vdanen@opensls.org> 3.6.11-1sls
- 3.6.11

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 3.6.10-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
