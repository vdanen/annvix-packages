#
# spec file for package man
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		man
%define version		1.5m2
%define release		%_revrel

Summary:	A set of documentation tools:  man, apropos and whatis
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		ftp://ftp.win.tue.nl:/pub/linux-local/utils/man
Source0:	ftp://ftp.win.tue.nl/pub/linux-local/utils/man/man-%{version}.tar.bz2
Source1:	makewhatis.cronweekly
Source2:	makewhatis.crondaily
Source3:	man.config.5
# changed 'groff -Tlatin' to 'nroff' (no -T option); that makes auto-detect
# the charset to use for the output -- pablo
Patch1:		man-1.5k-confpath.patch
Patch4:		man-1.5h1-make.patch
Patch5:		man-1.5k-nonascii.patch
Patch6:		man-1.5m2-security.patch
Patch7:		man-1.5k-mandirs.patch
Patch8:		man-1.5m2-bug11621.patch
Patch9:		man-1.5k-sofix.patch
Patch10:	man-1.5m2-buildroot.patch
Patch12:	man-1.5m2-ro-usr.patch
Patch14:	man-1.5i2-newline.patch
Patch15:	man-1.5k-lookon.patch
Patch17:	man-1.5j-utf8.patch
# comment out the NJROFF line of man.conf, so that the nroff script
# can take care of japanese -- pablo
Patch18:	man-1.5k-nroff.patch
Patch19:	man-1.5i2-overflow.patch
Patch22:	man-1.5j-nocache.patch
Patch24:	man-1.5i2-initial.patch
# Japanese patches
Patch51:	man-1.5h1-gencat.patch
Patch101:	man-1.5m2-lang-aware_whatis.patch
Patch102:	man-1.5g-nonrootbuild.patch
Patch104:	man-1.5m2-tv_fhs.patch
Patch105:	man-1.5j-i18n.patch
Patch106:	man-1.5j-perlman.patch
Patch107:	man-1.5j-whatis2.patch
Patch200:	man-1.5m2-colored_groff.patch
Patch201:	man-1.5m2-l10ned-whatis.patch

Patch300:	man-1.5m2-new-sections.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	groff-for-man
Prereq:		setup

%description
The man package includes three tools for finding information and/or
documentation about your Linux system: man, apropos and whatis. The man
system formats and displays on-line manual pages about commands or
functions on your system. Apropos searches the whatis database
(containing short descriptions of system commands) for a string. Whatis
searches its own database for a complete word.


%prep
%setup -q
%patch1 -p0 -b .confpath
%patch4 -p1 -b .make
%patch5 -p1 -b .nonascii
%patch6 -p1 -b .security
%patch7 -p1 -b .mandirs
%patch8 -p1 -b .ad
%patch9 -p1 -b .sofix
%patch10 -p1 -b .less
%patch12 -p1 -b .usr
%patch14 -p1 -b .newline
%patch15 -p1 -b .lookon
%patch51 -p1 -b .jp2
%patch17 -p1 -b .utf8
%patch18 -p1 -b ._nroff
%patch19 -p1 -b .overflow
%patch22 -p1 -b .nocache
%patch24 -p1 -b .initial

%patch101 -p1 -b .whatbz2
%patch102 -p1
%patch104 -p1 -b .tv_fhs
%patch105 -p1 -b .i18n
%patch106 -p0 -b .perl
%patch107 -p0
%patch200 -p0 -b .color
%patch201 -p0 -b .l10n
%patch300 -p1 -b .sec

/bin/rm -f %{_builddir}/man-%{version}/man/en/man.conf.man


%build
(cd man; for i in `find -name man.conf.man`; do mv $i `echo $i|sed -e 's/conf.man/config.man/g'`;done)
install -m 0644 %{SOURCE3} man/en/
./configure -default -confdir /etc +fsstnd +sgid +fhs +lang all \
    -compatibility_mode_for_colored_groff
make CC="gcc -g %{optflags} -D_GNU_SOURCE"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p  %{buildroot}%{_bindir}
mkdir -p  %{buildroot}%{_sbindir}
mkdir -p  %{buildroot}%{_mandir}
mkdir -p  %{buildroot}%{_sysconfdir}/cron.{daily,weekly}
perl -pi -e 's!/usr/man!/usr/share/man!g' conf_script
perl -pi -e 's!mandir = .*$!mandir ='"%{_mandir}"'!g' man2html/Makefile
make install PREFIX=%{buildroot}/  mandir=%{buildroot}/%{_mandir}

install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis.cron
install -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.daily/makewhatis.cron

mkdir -p %{buildroot}/var/catman{local,X11}
for i in 1 2 3 4 5 6 7 8 9 n; do
    mkdir -p %{buildroot}/var/catman/cat$i
    mkdir -p %{buildroot}/var/catman/local/cat$i
    mkdir -p %{buildroot}/var/catman/X11R6/cat$i
done


# symlinks for manpath
pushd %{buildroot}
    ln -s man .%{_bindir}/manpath
    ln -s man.1.bz2 .%{_mandir}/man1/manpath.1.bz2
    #perl -pi -e 's!nippon!latin1!g;s!-mandocj!-mandoc!g' etc/man.config
popd

/bin/rm -fr %{buildroot}/%{_mandir}/{de,fr,it,pl}
perl -pi -e 's!less -is!less -isr!g' %{buildroot}%{_sysconfdir}/man.config
#perl -pi -e 's!/usr/man!/usr/share/man!g' %{buildroot}%{_sbindir}/makewhatis

# Fix makewhatis perms
chmod 0755 %{buildroot}%{_sbindir}/makewhatis


%clean
#[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sysconfdir}/cron.weekly/makewhatis.cron
%{_sysconfdir}/cron.daily/makewhatis.cron
%attr(2755,root,man)	%{_bindir}/man
%{_bindir}/manpath
%{_bindir}/apropos
%{_bindir}/whatis
%{_bindir}/man2dvi
%{_sbindir}/makewhatis
%config(noreplace) %{_sysconfdir}/man.config
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_mandir}/man1/*

%{_mandir}/*/man?/*
%{_bindir}/man2html

%attr(0775,root,man)	%dir /var/catman
%attr(0775,root,man)	%dir /var/catman/cat[123456789n]
%attr(0775,root,man)	%dir /var/catman/local
%attr(0775,root,man)	%dir /var/catman/local/cat[123456789n]
%attr(0775,root,man)	%dir /var/catman/X11R6
%attr(0775,root,man)	%dir /var/catman/X11R6/cat[123456789n]

# translation of man program. It doesn't use gettext formatr, so
# find_lang doesn't find them... manual setting is needed
%lang(bg) %{_datadir}/locale/bg/man
%lang(cs) %{_datadir}/locale/cs/man
%lang(da) %{_datadir}/locale/da/man
%lang(de) %{_datadir}/locale/de/man
%lang(el) %{_datadir}/locale/el/man
%lang(en) %{_datadir}/locale/en/man
%lang(es) %{_datadir}/locale/es/man
%lang(fi) %{_datadir}/locale/fi/man
%lang(fr) %{_datadir}/locale/fr/man
%lang(hr) %{_datadir}/locale/hr/man
%lang(it) %{_datadir}/locale/it/man
%lang(ja) %{_datadir}/locale/ja/man
%lang(ko) %{_datadir}/locale/ko/man
%lang(nl) %{_datadir}/locale/nl/man
%lang(pl) %{_datadir}/locale/pl/man
%lang(pt) %{_datadir}/locale/pt/man
%lang(ro) %{_datadir}/locale/ro/man
%lang(ru) %{_datadir}/locale/ru/man
%lang(sl) %{_datadir}/locale/sl/man


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2-4avx
- P300: add new POSIX sections (tvignaud)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2-2avx
- bootstrap build

* Thu Mar 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2-1avx
- 1.5m2
- rediff P6, P8, P10,P104,  P201, P300 (tvignaud)
- rediff and rename P101: bzip2 whatis part was meged upstream, only keep
  LANG management part (tvignaud)
- drop P3, P11, P16, P26, and P108 (merged upstream) (tvignaud)
- spec cleanups

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.5k-16avx
- Annvix build

* Tue Jun 15 2004 Vincent Danen <vdanen@opensls.org> 1.5k-15sls
- include /usr/local/share/man in search path (modified P7)

* Sat Mar 06 2004 Vincent Danen <vdanen@mandrakesoft.com> 1.5k-14sls
- minor spec cleanups

* Mon Dec 02 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.5k-13sls
- OpenSLS build
- tidy spec

* Wed Jul 23 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5k-12mdk
- fix patch 107

* Tue Jul 22 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5k-11mdk
- patch 107 : fix #3968

* Mon Jun 16 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.5k-10mdk
- patch26 fix gcc 3.3 build

* Tue May 13 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5k-9mdk
- really remove network man pages (should never have been there)

* Thu Mar 13 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5k-8mdk
- patch 300: prevent possible of executing unsafe command with sgid man

* Mon Mar 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5k-7mdk
- remove network man pages (should never have been there)

* Thu Feb 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5k-6mdk
- add ifcfg.5, ifdown.8 and ifup.8 man pages

* Thu Feb 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5k-5mdk
- patch 201: fix #1599

* Wed Jan 08 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 1.5k-4mdk
- commented out the NJROFF lien of man.conf file

* Thu Dec 19 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5k-3mdk
- added man2dvi, makewhatis manpage & russian locale (Han Boetes)

* Tue Aug 27 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5k-2mdk
- patch8: s/less -isr/less -isR/
- patch106: simplify
- patch200: fix man rendering, aka make {g,n,t}roff use compatibility mode

  alternative fix is to disable the new groff ANSI colour/bold/underline
  escapes in nroff mode, since most pagers either fail to cope with it
  or need special options to do so.
  (put the following in /usr/share/groff/site-tmac/{mdoc.local,man.local}
    .if n \{\
    .  \" Disable the use of SGR (ANSI colour) escape sequences by grotty.
    .  if '\V[GROFF_SGR]'' \
    .    output x X tty: sgr 0
    \}

  right fix is to fix bogus pagers (either missing options or they should
  tell groff (GROFF_SGR and co) to not use ansi sequences)

* Tue Aug 13 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5k-1mdk
- new release
- patch 1: drop bits in favor of configure -confdir
- drop merged upstream patch 2, 7 (bits)
- rediff patches 1, 5, 6, 7, 9, 15, 101
- remove nippon hack in favor of new groff
- remove hack for man.config since its location is fixed

* Thu Jul 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5j-9mdk
- rediff patch106 : remove old perl manpath, add 3pm section

* Thu May 30 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5j-8mdk
- new man-pages-framework
- add chinese, hungarian, indonesian, japanese, korean, polish, russian
  support into makewhatis [Patch108]
  new scheme is completed (i18n/l10n, DESTDIR support, ...)
- fix makewhatis permissions

* Mon May 27 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5j-7mdk
- remove useless cp
- patch makewhatis so that it can be used for generic spec works:
	- add support for /var/cache/man/LANG/
	- add support for DESTDIR
	- factorize reference to the same directory
	- create directory if necessary

* Mon Apr 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5j-5mdk
- look to perl man pages too

* Fri Mar 08 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5j-4mdk
- resync with rh
- fix japanese man pages viewing

* Tue Feb 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5j-3mdk
- fix apropos (Ralf Ahlbrink)

* Tue Jan 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5j-2mdk
- rpmlint fixes

* Sat Jan 19 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5j-1mdk
- new release

* Tue Oct 30 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5i2-8mdk
- add %%url

* Thu Oct 18 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5i2-7mdk
- don't rease catman anymore
- fix description-use-invalid-word Mandrake-Linux

* Tue Oct 09 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5i2-6mdk
- qaize()
- bzip2 source patches for lorq qa

* Mon Oct 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5i2-5mdk
- s!Linux-Mandrake!Mandrake-Linux!g

* Mon Sep 03 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.5i2-4mdk
- put back the interface messages translations

* Wed Aug 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.5i2-3mdk
- Fix silly warning in makewhatis that make cron fu** up.

* Mon Jul 23 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.5i2-2mdk
- remove stale "read" command (Titi sux)

* Fri Jul 13 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5i2-1mdk
- fix url
- new version
- merge in rh patches

* Thu May 03 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.5h1-10mdk
- changed config file s/groff -Tlatin1/nroff/ that allows for auto-detection
  of charset to use in output with recent GNU roff (utf-8 output is possible)

* Thu Mar 01 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5h1-9mdk
- fix makewhatis for fhs

* Tue Oct 24 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5h1-8mdk
- prereq on setup

* Wed Oct 11 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5h1-7mdk
- uses less -r by default which enables to read man pages which are
  not in ascii even when the locales are set as EN.

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 1.5h1-6mdk
- some noreplace added
- requires groff-for-man instead of groff

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5h1-5mdk
- remove {de,fr,it,pl} man-pages which conflicts

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5h1-4mdk
- build release for BM
- use new macros
- add all translated man-pages (how can the author be so silly??)

* Sun Jul 09 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.5h1-3mdk
- Fix typo.

* Thu Jun 29 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5h-2mdk
- security fix for makewhatis

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5h-1mdk
- new release
- remove useless loop & manpath patch
- remove a chunk of make patch which is now usefull

* Mon May 15 2000 Pixel <pixel@mandrakesoft.com> 1.5g-15mdk
- build as non root fix

* Thu Mar 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>
- build for new environnment (new group naming)
- heavy use of spechelper

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with rh patchs.

* Thu Jul 08 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- By default in latin1.

* Tue May 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Makewhatis make the database with $LANG.
- Fix bug, if parsing files with -0 size.

* Mon May 24 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Fix up makewhatis bzip2/$LANG support
- 1.5g

* Tue Apr 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add patch to makewhatis support bzip2 pages.
- Add patch to makewhatis to $LANG pages.

* Sun Apr 11 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- Mandrake adaptions
- restore de, fr, tr locales from 5.2
- Add support for {bzip2|bzip|tzip} compressed manpages
- bzip2 man pages

* Thu Feb 18 1999 Jeff Johnson <jbj@redhat.com>
- add manpath symlinks (#1138).

* Fri Feb 12 1999 Michael Maher <mike@redhat.com>
- fixed bug #792
- added man2html files

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0
- upgraded to 1.5e
- properly buildrooted

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- enable fsstnd organization
- change /var/catman/X11 to X11R6
- %post/%preun to clean up cat litter

* Tue Jun 02 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Tue Jun 02 1998 Erik Troan <ewt@redhat.com>
- you can't do free(malloc(10) + 4) <sigh>

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.5d

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.5a

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- uses a build root

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- updated to man-1.4j, which fixes some security problems; release 1 is
  for RH 4.2, release 2 is for glibc
 
* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Mar 25 1997 Erik Troan <ewt@redhat.com>
- Added /usr/lib/perl5/man to default manpath
