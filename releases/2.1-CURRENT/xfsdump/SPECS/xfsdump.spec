#
# spec file for package xfsdump
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	revision	$Rev$
%define	name		xfsdump
%define	version		2.2.46
%define	release		%_revrel

Summary:	Administrative utilities for the XFS filesystem
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-1.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	attr-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	xfs-devel >= 2.6.0
BuildRequires:	dm-devel
BuildRequires:	ncurses-devel
BuildRequires:	libtool

%description
The xfsdump package contains xfsdump, xfsrestore and a number of
other utilities for administering XFS filesystems.

xfsdump examines files in a filesystem, determines which need to be
backed up, and copies those files to a specified disk, tape or other
storage medium.  It uses XFS-specific directives for optimizing the
dump of an XFS filesystem, and also knows how to backup XFS extended
attributes.  Backups created with xfsdump are "endian safe" and can
thus be transfered between Linux machines of different architectures
and also between IRIX machines.

xfsrestore performs the inverse function of xfsdump; it can restore a
full backup of a filesystem.  Subsequent incremental backups can then
be layered on top of the full backup.  Single files and directory
subtrees may be restored from full or partial backups.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

# make it lib64 aware, better make a patch?
#perl -pi -e "/(libuuid|pkg_s?lib_dir)=/ and s|/lib\b|/%{_lib}|;" configure


%build
aclocal && autoconf
%configure2_5x \
    --libdir=/%{_lib} \
    --sbindir=/sbin \
    --bindir=%{_sbindir}

%make DEBUG=-DNDEBUG OPTIMIZER="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DIST_ROOT=%{buildroot}/

# nuke files already packaged as %doc
rm -rf %{buildroot}%{_datadir}/doc/xfsdump/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/*
%{_sbindir}/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/COPYING doc/INSTALL doc/PORTING doc/README.xfsdump


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.46
- rebuild against new attr

* Sat Dec 1 2007 Ying-Hung Chen <ying-at-yingternet.com> 2.2.46
- 2.2.46

* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.42
- P0: fix for CVE-2007-2654
- rebuild against new e2fsprogs
- remove the perl call as configure isn't even created at this point

* Mon Jun 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.42
- build against new attr
- fixed buildreqs as per new devel naming policy

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.42
- rebuild against new xfs-devel

* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.42
- 2.2.42
- rebuild against new ncurses

* Mon Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.38
- 2.2.38
- spec cleanups
- rebuild against new e2fsprogs, new xfsprogs, new attr, and new dmapi

* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.30
- add -doc subpackage
- rebuild with gcc4
- buildrequires: libtool

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.30
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.30
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.30-1avx
- 2.2.30

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.21-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.21-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.21-2avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.2.21-1avx
- 2.2.21
- Annvix build

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 2.2.16-1sls
- OpenSLS build
- tidy spec
- BuildRequires: xfs-devel >= 2.6.0

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
