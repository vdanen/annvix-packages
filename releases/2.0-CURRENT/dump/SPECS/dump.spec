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
BuildRequires:	e2fsprogs-devel >= 1.15, openssl-devel >= 0.9.7a
BuildRequires:	termcap-devel, readline-devel, zlib-devel, bzip2-devel, autoconf2.5

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
Group:		Archiving/Backup
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

* Mon Dec 01 2003 Vincent Danen <vdanen@mandrakesoft.com> 0.4b34-1.1.92mdk
- bugfix update for 9.2

* Fri Nov 28 2003 Nicolas Planel <nplanel@mandrakesoft.com> 0.4b34-1mdk
- 0.4b34 (#147)

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.4b32-2mdk
- rebuild
- use %%make macro

* Wed Jan 15 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.4b32-1mdk
- Bump to version 0.4b32.

* Wed Jun 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.4b28-2mdk
- rpmlint fixes: hardcoded-library-path

* Mon Jun 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b28-1mdk
- Build a 0.4b28 for cooker users.

* Mon Apr 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b27-1mdk
- Build a dump 0.4b27.

* Sun Nov 18 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b25-1mdk
- Build a 0.4b25.

* Sun Oct 28 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b24-2mdk
- Work around when krb5-devel is not installed.

* Sun Sep 30 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b24-1mdk
- Dump 0.4b24.
- Work around libcom_err conflict of e2fsprogs / krb5 with a genius hack.

* Sun Sep 30 2001 Stefan van der Eijk <stefan@eijk.nu> 0.4b23-3mdk
- BuildRequires: krb5-devel (-lcom_err is no longer provided with
  e2fsprogs-devel)

* Sat Aug 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b23-2mdk
- Sanity build for 8.1.

* Fri Jul 20 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b23-1mdk
- Newest, shiniest, best-thing-ever-since-sliced-bread release.

* Sat Jun 16 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b22-2mdk
- s/Copyright/License/;
- Finally remember to bring my brain to work and so this time the Source
  URL should be correct.
  
* Sun May 13 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b22-1mdk
- Remove the glibc 2.2.2 patch from the last release.
- New and shiny dump 0.4b22.

* Wed Mar 14 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b21-2mdk
- Include time.h in optr.c.

* Sun Jan 14 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b21-1mdk
- new and shiny source.

* Sun Nov 12 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b20-1mdk
- new and shiny version to avoid potential security hole.

* Wed Nov 08 2000 Geoffrey Lee <snailtalk@mandrkaesoft.com> 0.4b19-3mdk
- don't pass suid permissions to %%configure.

* Tue Aug 22 2000 Vincent Saugey <vince@mandrakesoft.com> 0.4b19-2mdk
- Corrected licence
- Adding url

* Mon Aug 21 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b19-1mdk
- s|0.4b18|0.4b19|.

* Fri Jul 28 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4b18-2mdk
- rebuild for the BM
- use more new macros (titiscks)

* Wed Jul 05 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4b18-1mdk
- new release (potential SECURITY FIX)
- use new macros

* Wed Apr 19 2000 Vincent Saugey <vince@mandrakesoft.com> 0.4b16-3mdk
- Remove the sgid (tty) on binaries files.

* Fri Mar 31 2000 Vincent Saugey <vince@mandrakesoft.com> 0.4b16-2mdk
- Update to 4b16

* Mon Mar 13 2000 David BAUDNS <baudens@mandrakesoft.com> - 0.4b10-2mdk
- Fix %%{doc}
- Use new Groups
- Use %%{_buildroot} for BuildRoot  

* Mon Nov 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.4b10.

* Mon Nov  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.4b9.

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix danglings symlinks.

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge rh patchs.

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add modification from RedHat 6.0.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man pages
- add de locale

* Fri Feb 19 1999 Preston Brown <pbrown@redhat.com>
- upgraded to dump 0.4b4, massaged patches.

* Tue Feb 02 1999 Ian A Cameron <I.A.Cameron@open.ac.uk>
- added patch from Derrick J Brashear for traverse.c to stop bread errors

* Wed Jan 20 1999 Jeff Johnson <jbj@redhat.com>
- restore original 6755 root.tty to dump/restore, defattr did tty->root (#684).
- mark /etc/dumpdates as noreplace.

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- add build root.

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- added a patch for resolving linux/types.h and sys/types.h conflicts

* Wed Dec 31 1997 Erik Troan <ewt@redhat.com>
- added prototype of llseek() so dump would work on large partitions

* Thu Oct 30 1997 Donnie Barnes <djb@redhat.com>
- made all symlinks relative instead of absolute

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 06 1997 Michael K. Johnson <johnsonm@redhat.com>
- Moved rmt to its own package.

* Tue Feb 11 1997 Michael Fulbright <msf@redhat.com>
- Added endian cleanups for SPARC

* Fri Feb 07 1997 Michael K. Johnson <johnsonm@redhat.com> 
- Made /etc/dumpdates writeable by group disk.
