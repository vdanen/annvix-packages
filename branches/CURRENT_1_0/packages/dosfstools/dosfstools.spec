%define name	dosfstools
%define version 2.9
%define release 2sls

Summary:	Utilities to create and check MS-DOS FAT filesystems.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File tools
URL:		ftp://ftp.uni-erlangen.de/pub/Linux/LOCAL/dosfstools
Source:		ftp://ftp.uni-erlangen.de/pub/Linux/LOCAL/dosfstools/%{name}-%{version}.src.tar.bz2
Patch0:		dosfstools-2.8-x86_64.patch.bz2
Patch1:		mkdosfs.errno.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot

Obsoletes:	mkdosfs-ygg
Provides:	mkdosfs-ygg = %{version}

%description
Inside of this package there are two utilities to create and to
check MS-DOS FAT filesystems on either harddisks or floppies under
Linux.  This version uses the enhanced boot sector/superblock
format of DOS 3.3+ as well as provides a default dummy boot sector
code.

%prep
%setup -q
%patch0 -p1 -b .x86_64
%patch1 -p0 -b .errno

%build
%make PREFIX=/%{_prefix} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
cp dosfsck/README README.fsck
cp mkdosfs/README README.mkdosfs
%makeinstall PREFIX=$RPM_BUILD_ROOT MANDIR=$RPM_BUILD_ROOT%{_mandir}/man8

# as stated below, /sbin/fsck.* are not included in %files.
#
# Remove this link because for initscripts to don't have a fsck in a vfat
# -- Use dosfsck luke --

%clean
rm -r $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES TODO README.fsck README.mkdosfs dosfsck/COPYING
/sbin/mkdosfs
/sbin/mkfs.msdos
/sbin/mkfs.vfat
/sbin/dosfsck
%{_mandir}/man8/*

%changelog
* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.9-2sls
- OpenSLS build
- tidy spec
- remove Prefix

* Tue Jul 08 2003 Fran�ois Pons <fpons@mandrakesoft.com> 2.9-1mdk
- 2.9.

* Mon Jul 07 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.8-4mdk
- Patch1: fix build, errno

* Tue Nov 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.8-3mdk
- Patch0: Fix build on x86-64

* Wed Nov 07 2001 Fran�ois Pons <fpons@mandrakesoft.com> 2.8-2mdk
- add url tag.

* Wed Sep 05 2001 Fran�ois Pons <fpons@mandrakesoft.com> 2.8-1mdk
- update provides tag.
- 2.8.

* Tue Jul 03 2001 Fran�ois Pons <fpons@mandrakesoft.com> 2.7-2mdk
- build release, update distribution tag.

* Thu Feb 15 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.7-1mdk
- 2.7.

* Wed Nov 29 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.6-1mdk
- remove ExclusiveArch tag.
- new and shiny source.
- put in correct optimizations.

* Thu Jul 20 2000 Fran�ois Pons <fpons@mandrakesoft.com> 2.4-3mdk
- further spec cleaning.

* Mon Jul 17 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4-2mdk
- remove man-pages compression and let spec-helper do the job
- Stefan van der Eijk <s.vandereijk@chello.nl>
	* makeinstall macro
	* macroszifications
	* added %clean

* Fri Mar 31 2000 Fran�ois Pons <fpons@mandrakesoft.com> 2.4-1mdk
- updated Group.
- 2.4.

* Sun Mar 19 2000 John Buswell <johnb@mandrakesoft.com> 2.2-7mdk
- Added PPC support

* Mon Jan 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-6mdk
- ExclusiveArch x86.

* Wed Dec 01 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Thu Aug 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Stripping again (#60).
- Fix defatttr root,root.

* Mon Aug  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Remove fsck.* to don't have a fsck on vfat on boot (Maybe we can
  do a port of scandisk on linux ;) )
 
* Thu Jul  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Rewriting the .spec files to obsoletes mkdosfs-ygg for new dosfstools.
- initialization of spec file.
- 2.2 :
 - Added dosfsck/COPYING, putting dosfsck officially under GPL (Werner
   and I agree that it should be GPL).
 - mkdosfs: Allow creation of a 16 bit FAT on filesystems that are too
   small for it if the user explicitly selected FAT16 (but a warning
   is printed). Formerly, you got the misleading error message "make
   the fs a bit smaller".
 - dosfsck: new option -y as synonym for -y; for compability with
   other fs checkers, which also accept this option.
 - dosfsck: Now prints messages similar to e2fsck: at start version
   and feature list; at end number of files (and directories) and
   number of used/total clusters. This makes the printouts of *fsck at
   boot time nicer.
 - dosfsck: -a (auto repair) now turns on -f (salvage files), too. -a
   should act as non-destructive as possible, so lost clusters should
   be assigned to files. Otherwise the data in them might be
   overwritten later.
 - dosfsck: Don't drop a directory with lots of bad entries in
   auto-repair mode for the same reason as above.
 - dosfsck: avoid deleting the whole FAT32 root dir if something is
   wrong with it (bad start cluster or the like).
 - general: also create symlinks {mkfs,fsck}.vfat.8 to the respective
   real man pages.

# end of file
