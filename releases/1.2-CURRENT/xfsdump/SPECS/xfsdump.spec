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
%define	version		2.2.30
%define	release		%_revrel

Summary:	Administrative utilities for the XFS filesystem
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	%{name}-%{version}.src.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	attr-devel, libext2fs-devel, xfs-devel >= 2.6.0, dm-devel
BuildRequires:	ncurses-devel

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


%prep
%setup -q

# make it lib64 aware, better make a patch?
perl -pi -e "/(libuuid|pkg_s?lib_dir)=/ and s|/lib\b|/%{_lib}|;" configure


%build
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
%doc doc/CHANGES.gz doc/COPYING doc/INSTALL doc/PORTING doc/README.xfsdump
/sbin/*
%{_sbindir}/*
%{_mandir}/*/*


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Thu Feb 26 2004 Thomas Backlund <tmb@mandrake.org> 2.2.16-1mdk
- done by Per Øyvind Karlsen
  * 2.2.16
  * cosmetics
  * drop prefix tag

* Mon Oct 13 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.13-2mdk
- lib64 fixes

* Fri Aug  8 2003 Juan Quintela <quintela@mandrakesoft.com> 2.2.13-1mdk
- 2.2.13.

* Wed Jul 30 2003 Götz Waschk <waschk@linux-mandrake.com> 2.2.12-2mdk
- fix buildrequires

* Fri Jul 18 2003 Juan Quintela <quintela@mandrakesoft.com> 2.2.12-1mdk
- 2.2.12.

* Wed Jun 18 2003 Juan Quintela <quintela@trasno.org> 2.2.6-1mdk
- 2.2.6

* Wed Jul 24 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.3-1mdk
- 2.0.3

* Wed Jul 10 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.1-1mdk
- 2.0.1

* Thu Mar  7 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.0.0-1mdk
- 2.0.0

* Tue Nov 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.7-1mdk
- 1.1.7.

* Fri Sep 28 2001 Stefan van der Eijk <stefan@eijk.nu> 1.1.3-2mdk
- BuildRequires: libext2fs-devel
- Copyright --> License

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.3-1mdk
- 1.1.3.
- rework spec files and adjust requires.

* Wed May  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.5-1mdk
- Fist attempt based on the SGI spec.


# end of file
