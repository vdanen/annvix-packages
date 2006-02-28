#
# spec file for package psmisc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		psmisc
%define version		21.3
%define release		%_revrel

Summary:	Utilities for managing processes on your system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://psmisc.sourceforge.net
Source:		http://download.sourceforge.net/psmisc/psmisc-%{version}.tar.bz2
Patch1:		psmisc-20.2-libsafe.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtermcap-devel

%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs
of processes that are using specified files or filesystems.


%prep
%setup -q 
%patch1 -p1


%build
%configure


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
mkdir %{buildroot}/sbin
mv %{buildroot}%{_bindir}/fuser %{buildroot}/sbin/

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
/sbin/fuser
%{_bindir}/killall
%{_bindir}/pstree
%{_mandir}/man1/fuser.1*
%{_mandir}/man1/killall.1*
%{_mandir}/man1/pstree.1*


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 21.3-7avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 21.3-6avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 21.3-5avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 21.3-4sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 21.3-3sls
- OpenSLS build

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 21.3-2mdk
- rebuild

* Thu Jun 05 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 21.3-1mdk
- new release
- added locale files

* Tue Oct 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 21.2-1mdk
- new release :
	* bug fixes in pstree:
	  o pstree -a would often fail badly (swapped variable  not set)
	  o fix pstree -a extra bracket problem
	* removed pidof.1 and a variable not used.
	* SELINUX/hurd/lfs support
	* changed killall.1 to be less ambigous
	* fix UTF8 problem
	* return for fuser -k will mean no.

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 21-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Tue May 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 21-1mdk
- new release
- remove patch0 (merged upstream)

* Tue May 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 20.2-3mdk
- gcc-3.1 build
- fix "fails to show process tree" problem with libsafe [Patch1]:
  the source string for comm is too short for "%15c" wich potentially allow the
  code to read beyond the end of the source string.
  The new format '%[^)]' will never read beyond the end of the source string,
  which keeps libsafe happy. (It appears that glibc doesn't "sniff" the stack
  in this way, so the authors of libsafe may be overly cautious.)

* Mon Jan 14 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 20.2-2mdk
- hum, try to use the same signal numbers as the kernel... 15 signals
  names were wrong!

* Thu Jan 10 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 20.2-1mdk
- this is gpl, not distributable
- sanitize
- new version

* Sun Apr 08 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 20.1-1mdk
- Bump up to 20.1.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 19-4mdk
- automatically added BuildRequires


* Thu Jul 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 19-3mdk
- macros, BM, spechelper ( :-( )

* Thu Apr 13 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 19-2mdk
- Fix bad tag value.

* Tue Mar 21 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 19-1mdk
- Version update (19)
- Use default Mandrake Optimisations.
- Patch the Makefile for psmisc rpm to be compiled by non root user.
- bziped psmisc-17-buildroot.patch

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Move fuser to /sbin(r).

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Sat Mar 13 1999 Michael Maher <mike@redhat.com>
- updated package

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- renamed the patch file .patch instead of .spec

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- updated to psmisc version 17
- buildrooted

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from version 11 to version 16
- spec file cleanups

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
