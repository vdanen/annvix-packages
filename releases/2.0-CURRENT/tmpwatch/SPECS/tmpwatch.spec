#
# spec file for package tmpwatch
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		tmpwatch
%define version		2.9.6
%define release		%_revrel

# CVSROOT=':ext:user@devserv.devel.redhat.com:/home/devel/CVS'
Summary:	A utility for removing files based on when they were last accessed
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		ftp://ftp.redhat.com/pub/redhat/linux/rawhide/SRPMS/SRPMS/
Source0:	%{name}-%{version}.tar.bz2
Source1:	tmpwatch.cron

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	psmisc

%description
The tmpwatch utility recursively searches through specified
directories and removes files which have not been accessed in a
specified period of time.  Tmpwatch is normally used to clean up
directories which are used for temporarily holding files (for example,
/tmp).  Tmpwatch ignores symlinks, won't switch filesystems and only
removes empty directories and regular files.


%prep
%setup -q


%build
make RPM_OPT_FLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall ROOT=%{buildroot} MANDIR=%{_mandir} SBINDIR=%{_sbindir}

mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.daily/tmpwatch


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sbindir}/tmpwatch
%{_mandir}/man8/tmpwatch.8*
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/tmpwatch


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.9.6
- 2.9.6
- S1: make the cron script a source instead of echo'd in the spec
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.9.0
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.9.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9.0-6avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9.0-5avx
- bootstrap build

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.9.0-4avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.9.0-3sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 2.9.0-2sls
- OpenSLS build
- tidy spec

* Wed Jul 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.9.0-1mdk
- new release

* Thu Jan 23 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4-1mdk
- new release
- add cvs "url" too

* Fri Nov  2 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.8-1mdk
- new version
- add URL tag

* Thu Mar 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.7-1mdk
- 2.7 (allows concurrent usage of mtime, ctime, and atime checking).

* Sat Oct  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.6.2-1mdk
- Requires: psmisc.
- 2.6.2 security fixes.

* Wed Sep 20 2000 Francis Galiegue <fg@mandrakesoft.com> 2.0-16mdk
- /etc/cron.daily/tmpwatch is %%config(noreplace)

* Fri Jul 28 2000 Francis Galiegue <fg@mandrakesoft.com> 2.0-15mdk
- More macros
- Spec file cleanup

* Thu Jul 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0-14mdk
- BM

* Sun Apr 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0-13mdk
- check if /var/catman/$LANG is here before running it.

* Wed Apr 05 2000 John Buswell <johnb@mandrakesoft.com> 2.0-12mdk
- fix vendor tag

* Thu Mar 30 2000 John Buswell <johnb@mandrakesoft.com> 2.0-11mdk
- Fixed groups
- spec-helper

* Wed Dec 15 1999 Yoann Vandoorselaere <yoann@mandrakesoft.com>
- s/mtiem/mtime/
- tmpwatch --something shouldn't segfault 
  ( struct options should end with NULL ).

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.0

* Mon Jul 19 1999 Pawe³ Jab³oñski <pj@linux-mandrake.com>
- added pl locale
- added /var/catman/$LANG/cat?
- fixed build error - remove -s from Makefile (in install  tmpwatch.1)

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Wed Feb 10 1999 Preston Brown <pbrown@redhat.com>
- made tmpwatch clean up man pages formatted by root as well. Added missing
  formatted man page dirs (bugzilla #224)

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Jun 10 1998 Erik Troan <ewt@redhat.com>
- make /etc/cron.daily/tmpwatch executable

* Tue Jan 13 1998 Erik Troan <ewt@redhat.com>
- version 1.5
- fixed flags passing
- cleaned up message()

* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added man page to package
- uses a buildroot and %attr
- fixed error message generation for directories
- fixed flag propagation

* Mon Mar 24 1997 Erik Troan <ewt@redhat.com>
- Don't follow symlinks which are specified on the command line
- Added a man page

* Sun Mar 09 1997 Erik Troan <ewt@redhat.com>
- Rebuilt to get right permissions on the Alpha (though I have no idea
  how they ended up wrong).
