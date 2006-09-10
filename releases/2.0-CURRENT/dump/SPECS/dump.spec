#
# spec file for package dump
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		dump
%define version 	0.4b40
%define release 	%_revrel

%define rmtrealname	rmt-dump

Summary:	Programs for backing up and restoring filesystems
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Archiving
URL:		http://sourceforge.net/projects/dump/
Source: 	http://osdn.dl.sourceforge.net/pub/sourceforge/d/du/%{name}/%{name}-%{version}.tar.bz2
Patch0:		dump-mdk-nonroot.patch
Patch2:		dump-0.4b34-mdk-check-systypes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	e2fsprogs-devel >= 1.15
BuildRequires:	openssl-devel >= 0.9.7a
BuildRequires:	termcap-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	autoconf2.5

Requires:	rmt = %{version}-%{release}

%description
The dump package contains both dump and restore.  Dump examines files in
a filesystem, determines which ones need to be backed up, and copies
those files to a specified disk, tape or other storage medium.  The
restore command performs the inverse function of dump; it can restore a
full backup of a filesystem.  Subsequent incremental backups can then be
layered on top of the full backup.  Single files and directory subtrees
may also be restored from full or partial backups.


%package -n rmt
Summary:	Provides certain programs with access to remote tape devices
Group:		Archiving
Provides:	/sbin/rmt

%description -n rmt
The rmt utility provides remote access to tape devices for programs
like dump (a filesystem backup program), restore (a program for
restoring files from a backup) and tar (an archiving program).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0
%patch2 -p1 -b .sys-types


%build
%configure2_5x \
    --with-manowner=root \
    --with-mangrp=root \
    --with-manmode=644 \
    --enable-ermt \
    --disable-kerberos

%make OPT="%{optflags} -Wall -Wpointer-arith -Wstrict-prototypes -Wmissing-prototypes -Wno-char-subscripts"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make install SBINDIR=%{buildroot}/sbin BINDIR=%{buildroot}/sbin MANDIR=%{buildroot}%{_mandir}/man8

pushd %{buildroot}
    mkdir .%{_sysconfdir}
    > .%{_sysconfdir}/dumpdates
    ln -s ../sbin/smt .%{_sysconfdir}/rmt
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0664,root,disk) %config(noreplace) %{_sysconfdir}/dumpdates
/sbin/dump
/sbin/restore
/sbin/rdump
/sbin/rrestore
%{_mandir}/man8/dump.8*
%{_mandir}/man8/rdump.8*
%{_mandir}/man8/restore.8*
%{_mandir}/man8/rrestore.8*

%files -n rmt
%defattr(-,root,root)
/sbin/rmt
%{_sysconfdir}/rmt
%{_mandir}/man8/rmt.8*

%files doc
%defattr(-,root,root)
%doc CHANGES COPYRIGHT KNOWNBUGS README THANKS TODO MAINTAINERS dump.lsm


%changelog
* Mon Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.4b40
- rebuild against new e2fsprogs

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.4b40
- rebuild against new openssl
- spec cleanups

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.4b40
- rebuild against new readline
- drop P1; wasn't being applied so don't keep it
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.4b40
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.4b40
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.4b40
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.4b40-2avx
- rebuild for new readline

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.4b40-1avx
- 0.4b40
- no more alternatives

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.4b37-3avx
- rebuild

* Wed Jan 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.4b37-2avx
- rebuild against new openssl

* Thu Aug 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.4b37-1avx
- 0.4b37
- drop P1, krb5 doesn't bundle libcom_err now (deaddog)
- use alternative for rmt (tar now provides rmt also) (deaddog)
- new P1: fix build (peroyvind)
- patch policy

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.4b34-5avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 0.4b34-4sls
- minor spec cleanups

* Mon Jan 05 2004 Vincent Danen <vdanen@opensls.org> 0.4b34-3sls
- sync with 2mdk (gbeauchesne): make sure to check for <sys/types.h> prior
  to actual types like quad_t
- BuildPreReq: autoconf2.5

* Mon Dec 02 2003 Vincent Danen <vdanen@opensls.org> 0.4b34-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
