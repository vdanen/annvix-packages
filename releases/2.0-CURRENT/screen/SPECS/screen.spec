#
# spec file for package screen
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		screen
%define version		4.0.3
%define release		%_revrel

Summary:	A screen manager that supports multiple logins on one terminal
Name:		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		Terminals
URL:		http://www.gnu.org/software/screen
Source0:	ftp://ftp.uni-erlangen.de/pub/utilities/screen/%{name}-%{version}.tar.gz
Patch0:		screen-3.7.6-compat21.patch
Patch1: 	screen-ia64.patch
Patch3:		screen-makefile-ppc.patch
Patch4:		screen-3.9.11-fix-utmp.diff
Patch6:		screen-3.9.13-no-libelf.patch
Patch7:		screen-3.9.11-biarch-utmp.patch
Patch8:		screen-3.9.15-overflow.patch
Patch9:		screen-4.0.2-screenrc-utf8-switch.patch
Patch10:	screen-4.0.2-varargs.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel
BuildRequires:	utempter-devel
BuildRequires:	texinfo

Requires(post):	info-install
Requires(preun): info-install

%description
The screen utility allows you to have multiple logins on just one
terminal.  Screen is useful for users who telnet into a machine or
are connected via a dumb terminal, but want to use more than just
one login.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
# (sb) seems to be needed on x86 now too 
%patch3 -p1
%patch4 -p1
%patch6 -p1 -b .no-libelf
%patch7 -p1 -b .biarch-utmp
%patch8 -p1 -b .overflow
%patch9 -p0 -b .utf8
%patch10 -p1 -b .varargs


%build
%configure
perl -pi -e 's|.*#.*PTYMODE.*|#define PTYMODE 0620|' config.h
perl -pi -e 's|.*#.*PTYGROUP.*|#define PTYGROUP 5|' config.h

perl -pi -e 's|.*#undef HAVE_BRAILLE.*|#define HAVE_BRAILLE 1|' config.h
perl -pi -e 's|.*#undef BUILTIN_TELNET.*|#define BUILTIN_TELNET 1|' config.h

perl -pi -e 's|%{_prefix}/etc/screenrc|%{_sysconfdir}/screenrc|' config.h
perl -pi -e 's|/usr/local/etc/screenrc|%{_sysconfdir}/screenrc|' etc/etcscreenrc doc/*
perl -pi -e 's|/local/etc/screenrc|%{_sysconfdir}/screenrc|' doc/*
rm doc/screen.info*

%make CFLAGS="%{optflags} -DETCSCREENRC=\\\"%{_sysconfdir}/screenrc\\\""


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/skel

%makeinstall SCREENENCODINGS=%{buildroot}%{_datadir}/screen/utf8encodings/

pushd %{buildroot}%{_bindir}
    rm -f screen.old screen
    mv screen-%{version} screen
popd

install -c -m 0644 etc/etcscreenrc %{buildroot}%{_sysconfdir}/screenrc
install -c -m 0644 etc/screenrc %{buildroot}%{_sysconfdir}/skel/.screenrc

mkdir -p %{buildroot}%{_sysconfdir}/profile.d

cat > %{buildroot}%{_sysconfdir}/profile.d/screen.sh <<EOF
#!/bin/sh
# %{_sysconfdir}/profile.d/screen.sh

if [ -z "\$SCREENDIR" ]; then
    export SCREENDIR=\$HOME/tmp
fi
EOF


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}


%preun
%_remove_install_info %{name}


%files
%defattr(-,root,root)
%{_bindir}/screen
%{_mandir}/man1/screen.1.bz2
%{_infodir}/screen.info*
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/profile.d/screen.sh
%config(noreplace) %{_sysconfdir}/screenrc
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/skel/.screenrc
%{_datadir}/screen/

%files doc
%defattr(-,root,root)
%doc NEWS README doc/FAQ doc/README.DOTSCREEN ChangeLog


%changelog
* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3
- drop P5; it's not used anywhere
- rebuild against new ncurses

* Thu Oct 26 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3
- 4.0.3 (fixes CVE-2006-4573)

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2
- rebuild against new libutempter

* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2-5avx
- P9: add 'C-a U' binding to /etc/skel/.screenrc (rgarciasuarez)
- P10: varargs fixes (gbeauchesne)
- fix the screen profile.d script (rgarciasuarez)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2-3avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2-2avx
- requires info-install rather than /sbin/install-info
- Annvix build

* Mon May 10 2004 Vincent Danen <vdanen@opensls.org> 4.0.2-1sls
- 4.0.2
- linked against new libutempter

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.9.15-4sls
- minor spec cleanups
- remove %%prefix

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 3.9.15-3sls
- OpenSLS build
- tidy spec

* Fri Nov 28 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.9.15-2.1.92mdk
- security fix

* Sun Jun 15 2003 Stefan van der Eijk <stefan@eijk.nu> 3.9.15-2mdk
- BuildRequires

* Tue Jun 03 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.9.15-1mdk
- new version

* Tue Apr  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.9.13-3mdk
- Patch7: Handle biarch struct utmp

* Mon Jan 20 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.9.13-2mdk
- Patch6: Don't link against libelf

* Fri Oct 25 2002 Warly <warly@mandrakesoft.com> 3.9.13-1mdk
- new version

* Tue Jun 18 2002 Stefan van der Eijk <stefan@eijk.nu> 3.9.11-3mdk
- BuildRequires

* Fri Apr 12 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.9.11-2mdk
- fix stupid usage of info macros
- nonreplace config files
- add japanese support
- utmp is in /var/run/utmp, screenrc is in /etc, remove {/usr,}/local
  references [Patch4]
- s!bew!new!g in warly description
- bump up max window title length to 60 [Patch5]

* Thu Mar 28 2002 Warly <warly@mandrakesoft.com> 3.9.11-1mdk
- new version

* Mon Mar 04 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.9.10-2mdk
- update info fix patch (Goetz Waschk)
  aka fix browsing with gnome-help-browser)

* Thu Nov 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.9.10-1mdk
- new release

* Wed Jul 18 2001 Francis Galiegue <fg@mandrakesoft.com> 3.9.9-1mdk
- 3.9.9
- patch cleanup
- s,Copyright,License,

* Sun Jul 15 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 3.9.8-5mdk
- BuildRequires s/utempter-devel/libutempter-devel/

* Thu May 10 2001 Stew Benedict <sbenedict@mandrakesoft.com> 3.9.8-4mdk
- sed script doubles up entries in term.h on PPC use term.h.dist

* Sun Jan 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.9.8-3mdk
- Rebuild with last ncurses.

* Sat Nov 25 2000 Warly <warly@mandrakesoft.com> 3.9.8-2mdk
- fix bugged displaying when scrolling

* Mon Nov 13 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.9.8-1mdk
- new and shiny version.

* Mon Sep 18 2000 Francis Galiegue <fg@mandrakesoft.com> 3.9.5-9mdk

- Fix info file


* Fri Sep 15 2000 Francis Galiegue <fg@mandrakesoft.com> 3.9.5-8mdk

- Security fix, adapted patch from RH

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.9.5-7mdk
- automatically added BuildRequires


* Fri Jul 28 2000 Francis Galiegue <fg@mandrakesoft.com> 3.9.5-6mdk

- Oops... Fixed *info macros...

* Fri Jul 28 2000 Francis Galiegue <fg@mandrakesoft.com> 3.9.5-5mdk

- BMacros
- Some spec file changes

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.9.5-4mdk
- fix wrong URL
- use %%{_mandir} & %%{_infodir} to prepare FHS compliancy
- merge in RH patches

* Sun Jun 04 2000 David BAUDENS <baudens@mandrakesoft.com> 3.9.5-3mdk
- Fix build

* Fri Mar 17 2000 Francis Galiegue <francis@mandrakesoft.com>
- Let spec helper handle stripping and compressed manpages
- Changed group to match 7.1 specs

* Tue Dec 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 3.9.5 (fix a lot of know bugs).

* Wed Nov 10 1999 Francis Galiegue <francis@mandrakesoft.com>
- Really fixed /etc/skel/.screenrc permissions
- Fixed /etc/screenrc permissions
- spawn ptys are no more world writable

* Tue Nov 09 1999 John Buswell <johnb@mandrakesoft.com>
- Fixed /etc/skel/.screenrc permissions
- Enabled Unix98 ptys

* Tue Nov 02 1999 John Buswell <johnb@mandrakesoft.com>
- Build Release

* Thu Oct 21 1999 Francis Galiegue <francis@mandrakesoft.com>
- Merged patch from RedHat: screen now uses /dev/pts/*
- made /etc/profile.d/screen.sh sh-compatible (use test -z $SCREENDIR)

* Tue Sep 21 1999 Francis Galiegue <francis@mandrakesoft.com>
- fixed bug in /etc/profile.d/screen.sh (credits go to Axalon for this one)

* Mon Aug 23 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 3.9.4

* Sun Jul 25 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- set SCREENDIR=$HOME/tmp

* Tue May 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adaptations.

* Wed Apr 07 1999 Bill Nottingham <notting@redhat.com>
- take out warning of directory ownership so root can still use screen

* Wed Apr 07 1999 Erik Troan <ewt@redhat.com>
- patched in utempter support, turned off setuid bit

* Fri Mar 26 1999 Erik Troan <ewt@redhat.com>
- fixed unix98 pty support

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Mar 11 1999 Bill Nottingham <notting@redhat.com>
- add patch for Unix98 pty support

* Mon Dec 28 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.7.6.

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- upgraded to 3.7.4

* Wed Oct 08 1997 Erik Troan <ewt@redhat.com>
- removed glibc 1.99 specific patch

* Tue Sep 23 1997 Erik Troan <ewt@redhat.com>
- added install-info support

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
