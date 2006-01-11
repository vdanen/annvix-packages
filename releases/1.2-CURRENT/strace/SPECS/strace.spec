#
# spec file for package strace
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		strace
%define version		4.5.13
%define release		%_revrel

%{expand:%%define optflags %{optflags} -Wall}

Summary:	Tracks and displays system calls associated with a running process
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Development/Kernel
URL:		http://sourceforge.net/projects/strace/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		strace-4.5.13-alt-quotactl.diff
Patch1:		strace-4.5.13-alt-mount.diff
Patch2:		strace-4.5.13-owl-man.diff
Patch3:		strace-4.5.13-alt-keep_status.diff
Patch4:		strace-4.5.13-drepper-x86_64-ipc.diff
Patch5:		strace-4.5.13-drepper-msgrcv.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, automake1.7

%description
The strace program intercepts and records the system calls called
and received by a running process.  Strace can print a record of
each system call, its arguments and its return value.  Strace is useful
for diagnosing problems and debugging, as well as for instructional
purposes.


%prep
%setup -q
#%patch0 -p1 -b .quotactl
%patch1 -p1 -b .mount
%patch2 -p1 -b .man
%patch3 -p1 -b .keep_status
%patch4 -p1 -b .x86_64-ipc
%patch5 -p1 -b .msgrcv


%build
#autoreconf -fisv

export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force && aclocal-1.7 && autoheader && automake-1.7 --add-missing && autoconf --force

%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

# remove unpackaged files
rm -f %{buildroot}%{_bindir}/strace-graph


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc COPYRIGHT README* CREDITS ChangeLog INSTALL NEWS PORTING TODO
%{_bindir}/strace
%{_mandir}/man1/strace.1*


%changelog
* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.5.13-1avx
- 4.5.13
- sync with ALT/Openwall patches
- redefine %%optflags to add -Wall

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.98-6avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.98-5avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.4.98-4avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.4.98-3sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 4.4.98-2sls
- OpenSLS build

* Thu Jul 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.4.98-1mdk
- 4.4.98

* Tue Apr 15 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.4.96-1mdk
- 4.4.96 + CVS (2003/04/10)

* Sat Apr  5 2003 Stefan van der Eijk <stefan@eijk.nu> 4.4.94-1mdk
- 4.4.94

* Sun Feb  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.4.93-1mdk
- 4.4.93

* Thu Jan 16 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.4.92-1mdk
- 4.4.92

* Thu Sep  5 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.4-4mdk
- Merge with Red Hat releases (7 new patches):
  - eliminate hang tracing threads (Jeff Law)
  - handle modify_ldt (#66894)
  - handle futexes, *xattr, sendfile64, etc. (Ulrich Drepper)
  - handle ?et_thread_area, SA_RESTORER (Ulrich Drepper)
  - fix strace -f (Roland McGrath, #68994)

* Fri Aug  9 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.4-3mdk
- Patch3: Add x86-64 support from Andi Kleen (SuSE)

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.4-2mdk
- Automated rebuild in gcc3.1 environment

* Wed Oct 10 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.4-1mdk
- Release 4.4
- Drop Patch2 (merged upstream)
- Drop Patch4 in favor of a new Patch2 for IA-64 based upon latest
  changes in CVS

* Thu Aug  2 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3-2mdk
- version.c (version): bump to 4.3

* Wed Aug  1 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3-1mdk
- release 4.3
- fix license (BSD)
- Patch0, Patch3: removed since merged upstream
- Patch2: reworked
- Patch4: some ia64 fixes

* Mon Mar 12 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 4.2-7mdk
- fix build broken due to glibc 2.2.2's more strict headers

* Mon Feb 05 2001 Francis Galiegue <fg@mandrakesoft.com> 4.2-6mdk
- ExcludeArch ia64 until sources are merged

* Tue Jan 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.2-5mdk
- Fix k2.4 compilation.

* Thu Nov 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.2-4mdk
- fix glibc22 compilation.

* Fri Sep 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.2-3mdk
- Big Move.
- Fix compilation (include a timex.h who don't include time.h).

* Sun Jun 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.2-2mdk
- Use makeinstall macros.

* Mon Apr 17 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 4.2-1mdk
- version 4.2 (fixes Y2K bug, adds 64-bit LFS and S/390 support)
- added documentation to package

* Mon Apr 10 2000 Christopher Molnar <molnarc@mandrakesoft.com> 4.1-4mdk
- Fixed group

* Sun Mar 19 2000 John Buswell <johnb@mandrakesoft.com> 4.1-3mdk
- Removed redundent arch define
- PPC fixes
- PPC build

* Thu Jan 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.1-2mdk
- Use %configure_

* Fri Nov 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 4.1.

* Mon Nov 08 1999 John Buswell <johnb@mandrakesoft.com>
- Commented out KERN_SECURELVL from system.c (this is not in sysctl.h in 
  2.2.13 kernel)
- Build Release

* Mon Jul 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 4.00.

* Wed Apr 28 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Update to 3.99.

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binary

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 16)

* Tue Feb  9 1999 Jeff Johnson <jbj@redhat.com>
- vfork est arrive!

* Tue Feb  9 1999 Christopher Blizzard <blizzard@redhat.com>
- Add patch to follow clone() syscalls, too.

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- patch to build alpha/sparc with glibc 2.1.

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to build on ARM

* Wed Sep 30 1998 Jeff Johnson <jbj@redhat.com>
- fix typo (printf, not tprintf).

* Sat Sep 19 1998 Jeff Johnson <jbj@redhat.com>
- fix compile problem on sparc.

* Tue Aug 18 1998 Cristian Gafton <gafton@redhat.com>
- buildroot

* Mon Jul 20 1998 Cristian Gafton <gafton@redhat.com>
- added the umoven patch from James Youngman <jay@gnu.org>
- fixed build problems on newer glibc releases

* Mon Jun 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr
