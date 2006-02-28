#
# spec file for package mktemp
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mktemp
%define version		1.6
%define release		%_revrel

Summary:	A small utility for safely making /tmp files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		File tools
URL:		ftp://ftp.openbsd.org/pub/OpenBSD/src/usr.bin/mktemp/
Source:		mktemp-%{version}.tar.bz2
Patch0:		mktemp-1.6-avx-makefile.patch
Patch1:		mktemp-1.6-avx-linux.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The mktemp utility takes a given file name template and overwrites
a portion of it to create a unique file name.  This allows shell
scripts and other programs to safely create and use /tmp files.


%prep
%setup -q
%patch0 -p0 -b .makefile
%patch1 -p0 -b .linux


%build
CFLAGS="%{optflags}" make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
perl -pi -e "s!/usr/man!%{_mandir}!g" Makefile
%makeinstall ROOT="%{buildroot}"


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/bin/mktemp
%{_mandir}/man1/mktemp.1*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-2avx
- bootstrap build

* Thu Sep 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.6-1avx
- OpenBSD CVS rev 1.13 (we'll call this 1.6)
- rework patches and drop those no longer needed

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.5-14avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.5-13sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 1.5-12sls
- OpenSLS build
- tidy spec
- pass CFLAGS on to make

* Sun May 25 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.5-11mdk
- rebuild for rpm 4.2

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 1.5-10mdk
- Remove unneeded step in %%install section

* Wed Nov 29 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.5-9mdk
- resync with rh patches (enabled -d for mkinitrd).

* Thu Jul 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5-8mdk
- macros, BM
- let spechelper do the man-pages compression job ...

* Fri Mar 31 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.5-7mdk
- group fix

* Tue Jan 11 2000 Pixel <pixel@linux-mandrake.com>
- fix build as non-root

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Upgrade of man-pages(r).

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Upgarde to 1.5.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 01 1997 Erik Troan <ewt@redhat.com>
- moved to /bin

