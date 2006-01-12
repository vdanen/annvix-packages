#
# spec file for package mc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mc
%define version		4.6.1
%define release		%_revrel

Summary:	A user-friendly file manager and visual shell
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File tools
URL:		http://www.ibiblio.org/mc/
Source0:	ftp://ftp.gnome.org:/pub/GNOME/stable/sources/mc/%{name}-%{version}.tar.bz2
Patch0:		mc-4.6.1-fdr-utf8.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libext2fs-devel pam-devel
BuildRequires:	slang-devel glib2-devel

Requires:	groff

%description
Midnight Commander is a visual shell much like a file manager, only with way
more features.  It is text mode, but also includes mouse support if you are
running GPM.  With mc you are able to ftp as well as view tar, zip, and rpm
files.


%prep
%setup -q
%patch0 -p1 -b .utf8


%build
%serverbuild
# libcom_err of e2fsprogs and krb5 conflict. Watch this hack. -- Geoff.
# <hack>
mkdir -p %{_lib}
ln -sf /%{_lib}/libcom_err.so.2 %{_lib}/libcom_err.so
export LDFLAGS="-L`pwd`/%{_lib}"
# </hack>


%configure2_5x \
    --with-debug \
    --without-included-gettext \
    --without-included-slang \
    --with-screen=slang \
    --enable-nls \
    --enable-charset \
    --enable-largefile \
    --without-x \
    --without-gpm-mouse

# don't use make macro, mc doesn't support parallel compilation
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/{pam.d,profile.d,X11/wmconfig}

#fix mc-wrapper.sh
perl -p -i -e 's/rm -f \"/rm -rf \"/g' lib/mc-wrapper.sh

%makeinstall

install lib/{mc.sh,mc.csh} %{buildroot}%{_sysconfdir}/profile.d

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-, root, root)
%doc FAQ COPYING NEWS README
%{_bindir}/mc
%{_bindir}/mcedit
%{_bindir}/mcmfmt
%{_bindir}/mcview
%dir %{_libdir}/mc
%{_libdir}/mc/cons.saver
%_datadir/mc/cedit.menu
%_datadir/mc/edit.indent.rc
%_datadir/mc/edit.spell.rc
%{_datadir}/mc/mc.ext
%{_datadir}/mc/mc.hint
%_datadir/mc/mc.hint.*
%{_datadir}/mc/mc.hlp
%_datadir/mc/mc.hlp.*
%{_datadir}/mc/mc.lib
%{_datadir}/mc/mc.menu
%{_datadir}/mc/mc.menu.*
%{_datadir}/mc/mc.charsets
%{_datadir}/mc/extfs/*
%{_mandir}/man1/*
%dir %{_datadir}/mc
%dir %{_datadir}/mc/bin
%_datadir/mc/bin/*
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_datadir}/mc/syntax/
#%{_datadir}/mc/term/


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1-2avx
- rebuild against new glib2.0

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1-1avx
- 4.6.1
- drop all unrequired patches

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.0-12avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.0-11avx
- rebuild

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> - 4.6.0-10avx
- P16: make the wrapper script work (oden)

* Tue Sep 07 2004 Vincent Danen <vdanen-at-build.annvix.org> - 4.6.0-9avx
- renumber patches; patch policy
- update description
- sync with cooker 4.6.0-11mdk:
  - P5: image extension s/ee/gqview (bug #7907) (mpol)
  - [DIRM] (misc)
  - update P1, use gqview for images as upstream does (mpol)
  - add unzip vfs (mpol)
  - drop P2, merged in P6 to P10 (mpol)
  - P5: "secret" redhat cpio fix (mpol)
  - P7: build against slang-utf8 (mpol)
  - P8, P10, P11, P12: add utf8 patches from fedora/suse (mpol)
  - P9: (jumbo patch) several fixes, updates, etc. (mpol)
  - disable charset conversion (mpol)
  - security fix for vfs/extfs CAN-2004-0494 (mpol)
  - P14: add info/obsoletes, info/license to rpm extfs (mpol)
  - P15: fix crash on use of large syntax file (mpol)
  - P16: fix coloring of diffs of diffs (mpol)

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> - 4.6.0-8avx
- Annvix build

* Mon May 10 2004 Vincent Danen <vdanen@opensls.org> - 4.6.0-7sls
- P2 fixes CAN-2004-0226, CAN-2004-0231, CAN-2004-0232
- P3 don't build ta locale as it breaks build (sbenedict)

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> - 4.6.0-6sls
- minor spec cleanups

* Wed Jan 21 2004 Vincent Danen <vdanen@opensls.org> - 4.6.0-5sls
- OpenSLS build
- tidy spec
- security fix for CAN-2003-1023

* Wed Jul 16 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 4.6.0-4mdk
- Patch0: remove xpdf error from stdout (bug #4094)

* Fri Jun 06 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.6.0-3mdk
- don't rm -rf %{buildroot} in %%prep
- use double %%'s in changelog

* Wed Apr  2 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 4.6.0-2mdk
- from  Marcel Pol <mpol@gmx.net> 
 - avoid dependency on X11 libraries
 - make mcserv optional, disabled. ssh/fish is better anyway

* Mon Feb 10 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 4.6.0-1mdk
- from Douglas Wilkins <douglasw@mweb.co.za>:
- removed patch0: color_terminals no longer defined
- removed patch3 and patch16: gnome/mc.keys.in.in no longer exists
- removed patch4 and patch22: gnome/gscreen.c no longer exists and does not require translation
- removed patch20: gnome/gdesktoplnk.c no longer exists
- rediffed patch23 as mc-4.6.0-toolbar-po-mdk.path.bz2 (gnome/gscreen.c no longer exists)
- removed patch28: use_proxy no longer defined in xdirentry.h union u
- removed patch29: environment variable mc no longer used in mc.sh.in (see mc-wrapper.sh.in)
- rediffed patch31 as mc-4.6.0-init.patch.bz2
- removed patch32: gnome/gdesktop.c no longer exists
- removed patch33: merged upstream
- removed references to gmc in spec file (gmc no longer part of package)
- added '--with-mcfs' to compile options to enable building of mcserv
- edited perl script in specfile to modify mc-wrapper.sh rather than mc.sh
- removed install of mc.global (file is not in distribution)
- do not install ldp.xpm in desktoplinks (gmc no longer part of package)
- remove unused sources
- updated URL

* Tue Jul 16 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.5.55-10mdk
- rpmlint fixes: hardcoded-library-path. Should move arch-independent
  mc configs/helpers to %%{_datadir}/mc/ instead.

* Fri Apr 26 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 4.5.55-9mdk
- fixed largefiles size computation in "show directory size" menu.

* Tue Apr 16 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.55-8mdk
- GMC is dead now.. Long live to Nautilus for GNOME 2

* Mon Feb 18 2002 Pablo Saratxaga <pablo@@mandrakesoft.com> 4.5.55-7mdk
- merged with Basque translations

* Tue Nov 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.5.55-6mdk
- Redo bash export patch to detect bash by BASH_VERSION instead (andrej).

* Mon Oct 01 2001 Stefan van der Eijk <stefan@eijk.nu> 4.5.55-5mdk
- BuildRequires: e2fsprogs-devel gnome-libs-devel pam-devel slang-devel
- Removed redundant BuildRequires

* Mon Sep 17 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.55-4mdk
- Patch32: don't create ~/Desktop symlink

* Fri Sep 14 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 4.5.55-3mdk
- rebuild including latest translations

* Thu Aug 30 2001 David BAUDENS <baudens@mandrakesoft.com> 4.5.55-2mdk
- Use new icons
- Add missing files

* Mon Aug 27 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.55-1mdk
- Release 4.5.55
- Remove patche 2, 27, 30 (merged upstream)
- Regenerate patch 20
- bzip patch 31

* Mon Aug 06 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.54-4mdk
- add Requires: groff for viewing man-pages
- add runlevels to mcserv

* Thu Jul 26 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.54-3mdk
- Clean specfile
- Move provide gnome-desktop to gmc package

* Mon May 28 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.54-2mdk
- Patch30: fix rpm view (from GNOME CVS)
- fix BuildRequires and icons install (Thanks to Andre Duclos)

* Fri May  4 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.54-1mdk
- Release 4.5.54

* Mon Apr 30 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.5.52-6mdk
- Export only when bash.

* Tue Apr  3 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.52-5mdk
- Provides gnome-desktop virtual package

* Tue Apr 03 2001 David BAUDENS <baudens@mandrakesoft.com> 4.5.52-4mdk
- PPC: build with gcc

* Thu Mar 29 2001 dam's <damien@mandrakesoft.com> 4.5.52-3mdk
- new service policy.

* Thu Mar 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.5.52-2mdk
- Export quiet the function in mc.sh.

* Wed Mar 21 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.52-1mdk
- Release 4.5.52
- Regenerate and merge patch 20 and 21
- Regenerate patch 23
- Remove patches 25, 26 (merged upstream)

* Fri Jan 12 2001 David BAUDENS <baudens@mandrakesoft.com> 4.5.51-9mdk
- Fix build on PPC

* Wed Nov 15 2000 dam's <damien@mandrakesoft.com> 4.5.51-8mdk
- Corrected conffile & menu.

* Fri Sep 29 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.51-7mdk
- Correct proxy support (bug #443)

* Wed Sep 27 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.51-6mdk
- Patch to disable warning when running as root (from Redhat)

* Wed Sep 20 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 4.5.51-5mdk
- Use more macros
- Use find_lang macro

* Thu Aug 31 2000 David BAUDENS <baudens@mandrakesoft.com> 4.5.51-4mdk
- Fix gmc Group
- Remove french Descriptions
- Requires actual mandrake_desk

* Fri Jul 21 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 4.5.51-3mdk
- made 8bit clean the default for display and input (now mcedit is finally
  usable :) )

* Fri Jul 21 2000 dam's <damien@mandrakesoft.com> 4.5.51-2mdk
- BM + macrozification.
- added icons patch.

* Tue Jul  4 2000 dam's <damien@mandrakesoft.com> 4.5.51-1mdk
- new release.
- new BuidRequires.

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.50-1mdk
- new release

* Wed May 17 2000 Daouda Lo <daouda@mandrakesoft.com> 4.5.46-1mdk
- this upgrade fix lot of minor bugs.
- gmc-client in right place now

* Fri May 12 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 4.5.44-7mdk
- launch gmc with --nodesktop in menu entry, so that it does not
  pollute kde desktop icons with gnome desktop icons!

* Wed May 10 2000 dam's <damien@mandrakesoft.com> 4.5.44-6mdk
- corrected toolbar usize and translation.

* Tue May  9 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 4.5.44-5mdk
- remove /usr/lib/mc/desktop-scripts/startup.links in order
  to not have the link to slashdot.org

* Fri May 05 2000 Daouda Lo <daouda@mandrakesoft.com> 4.5.44-4mdk
- idl files are for gmc package ;-)

* Fri May 05 2000 Daouda Lo <daouda@mandrakesoft.com> 4.5.44-3mdk
- mc didn't open rpm files and list contains of this files. 
- missing .idl files added.

* Fri Apr 18 2000 Daouda Lo <daouda@mandrakesoft.com> 4.5.44-2mdk
- add icon to gmc

* Sun Apr 16 2000 Daouda Lo <daouda@mandrakesoft.com> 4.5.44-1mdk
- release from helix

* Wed Mar 22 2000 Lenny Cartier <lenny@mandrakesoft.com> 4.5.42-6mdk
- fix group
- add menu entry for package gmc

* Wed Jan 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix gdesktoplnk on alpha.

* Tue Jan 04 2000 Axalon Bloodstone <axalon@linux-mandrake.com>
- fix mc.* scripts (stupid rm -i)

* Sat Jan 01 2000 Axalon Bloodstone <axalon@linux-mandrake.com>
- Rely on mc's internal fixes for safe links in /tmp

* Thu Dec 23 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Move the mandrake files to mandrake_desk (hey what a concept)

* Tue Dec 07 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 4.5.42
	* Changes:
        - Important RFC-compliancy fix for ftpfs (Alexander).
        - Minor fixes to the desktop customization code (Miguel).
        - Cosmetic fixes to popup menus for devices (Jonathan).
        - File renaming fixes for the desktop and icon views (Federico).
        - Added a "--disablerootwarning" option (Vincent).
        - More sanity checks for the widget systems (Pavel).
        - Robustness fixes for desktop icon arranging (Federico).
        - Ability to free VFSes (Pavel).
        - Display fixes for ftpfs (Pavel).
        - Fishfs and general VFS fixes (Pavel).
        - Proofreading fixes of the user's guide (Kjartan, Dave).
        - Many updated translations (Ivan, David Sauer, David Martin,
          Kenneth, Marco, Sung-Hyun, Kjartan, Rodrigo, Evgeny,
          Richard, Lorint, Birger, Miroslav, Yuri).

* Mon Nov 08 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- added gdesktoplnk utility
- and scripts that us it to create default icons
- included the man.bz2 and lzh patches

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- enable SMP check/build
- redo ext patch
- redo user tmp patch in perl
- 4.5.40 : (if i find one more SOURCE_VER i'm hanging someone)

* Fri Sep 24 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 4.5.39

* Wed Sep 22 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- remove e keys patch, (keybindings per documentation)

* Sat Sep 04 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Merged :
	-- Sat Sep 04 1999 Giuseppe Ghibò <ghibo@linux-mandrake.com>
	 - Added support for bz2 man pages in mc.ext.
	 - Added support for TAR (uppercase) extension in mc.ext (it's often
	   used in ISO CDs).
	 - Changed lharc to lha in mc.ext.
	 - Fixed a problem with ls in vfs/ulha script.
- And :
	-- Fri Sep 03 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
	 - Upgraded to real 4.5.38; it should work much better with gnome-libs 1.0.16


* Thu Aug 19 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Opps, forgot to remove the bzip2 warning

* Thu Aug 19 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- update to bzip2 scripts for latest bzip2 
- update to the latest cvs version

* Wed Jul 21 1999 G.Colbert <gregus@etudiant.net>
- Oups, I forgot to translate some descriptions!
	* Wed Jul 21 1999 G.Colbert <gregus@etudiant.net>
	- fr locale

* Thu Jul 15 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- update to 4.5.37

* Wed Jul 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 4.5.36.

* Tue Jul 06 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Removing unused stuff.
- 4.5.35.
- Add patch compilation.

* Mon Jul 05 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add a missing icons from CVS.
- 4.5.34 :
   * Samba File System support.

     Wayne Roberts contributed the SMBfs virtual file system to the
     file manager, to use it just use the special path name "/#smb:", like this:
     "/#smb:thehost".

     It still needs username encoding, password encoding and that sort
     of thing, so if you want to help out in this area, contact Wayne
 
   * Many new localizations and updated localizations

   * Kjartan provided some GNOME documentation for the file manager.

   * GMC now loads pathnames specified on the command line.

   * Federico dropped some dead code from the code.

   * Viewer should paint colors correctly now.

   * Federico's changes to add the proper WMclass names to the desktop
     windows;  He also did some updates to the desktop handling code.

   * Starting terminals from the desktop starts them from the Home
     directory for the user, not the desktop directory.

   * Japaneese support by Akira.

   * Many compilation fixes, and many runtime fixes.  You need to try
     this out.

   * Updated documentation on the desktop.links startup option.

* Tue Jun 22 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- returned missing files into mc package (yes they just walked off by them selves)

* Sun Jun  6 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 4.5.33
- use DESTDIR=%{buildroot} solves bugs in help files
- never use /tmp, always use ~/tmp. cause I don't like it 

* Wed Jun 02 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Patched to co-exsist better with enlightenment default keys 
  right click now requires the shitkey to active the popup

* Tue May 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Compress manpages.
- Change links on the desktop (no ftp, use http mirrors)

* Wed May 12 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 4.5.31
- remove -g from CFLAGS - we don't need it

* Sat May 01 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adaptations.
- vanilla mc don't need icons.

* Mon Apr 19 1999 Michael Fulbright <drmike@redhat.com>
- removed rpm menu defs - we depend on gnorpm for these
- fixed bug that caused crash if group doesnt exist for file

* Thu Apr 15 1999 Michael Fulbright <drmike@redhat.com>
- cleanup several dialogs

* Mon Apr 12 1999 Michael Fulbright <drmike@redhat.com>
- true version 4.5.30

* Fri Apr 09 1999 Michael Fulbright <drmike@redhat.com>
- version pre-4.5.30 with patch to make this link on alpha properly
  Mark as version 0.7 to denote not the official 4.5.30 release

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Wed Mar 31 1999 Michael Fulbright <drmike@redhat.com>
- fixed errata support URL

* Tue Mar 25 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.29
- added default desktop icons for Red Hat desktop
- added redhat-logos to requirements
- added README.desktop to doc list for gmc
- added locale data

* Fri Mar 25 1999 Preston Brown <pbrown@redhat.com>
- patched so that TERM variable set to xterm produces color

* Mon Mar 22 1999 Michael Fulbright <drmike@redhat.com>
- made sure /etc/pam.d/mcserv has right permissions

* Thu Mar 18 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.27

* Tue Mar 16 1999 Michael Fulbright <drmike@redhat.com>
- fix'd icon display problem

* Sun Mar 14 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.25 AND 4.5.26

* Wed Mar 10 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.24

* Mon Feb 15 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.16
- removed mc.keys from mc file list

* Fri Feb 12 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.14
- fixed file list

* Sat Feb 06 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.11

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.10

* Fri Jan 22 1999 Michael Fulbright <drmike@redhat.com>
- added metadata to gmc file list

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.9

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.6

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- updated for GNOME freeze

* Thu Aug 20 1998 Michael Fulbright <msf@redhat.com>
- rebuilt against gnome-libs 0.27 and gtk+-1.1

* Thu Jul 09 1998 Michael Fulbright <msf@redhat.com>
- made cons.saver not setuid

* Sun Apr 19 1998 Marc Ewing <marc@redhat.com>
- removed tkmc

* Wed Apr 8 1998 Marc Ewing <marc@redhat.com>
- add %%{prefix}/lib/mc/layout to gmc

* Tue Dec 23 1997 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
- added --without-debug to configure,
- modification in %%build and %%install and cosmetic modification in packages
  headers,
- added %%{PACKAGE_VERSION} macro to Buildroot,
- removed "rm -rf %{buildroot}" from %%prep.
- removed Packager field.

* Thu Dec 18 1997 Michele Marziani <marziani@fe.infn.it>
- Merged spec file with that from RedHat-5.0 distribution
  (now a Hurricane-based distribution is needed)
- Added patch for RPM script (didn't always work with rpm-2.4.10)
- Corrected patch for mcserv init file (chkconfig init levels)
- Added more documentation files on termcap, terminfo, xterm

* Thu Oct 30 1997 Michael K. Johnson <johnsonm@redhat.com>

- Added dependency on portmap

* Wed Oct 29 1997 Michael K. Johnson <johnsonm@redhat.com>

- fixed spec file.
- Updated to 4.1.8

* Sun Oct 26 1997 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>

- updated to 4.1.6
- added %%attr macros in %%files,
- a few simplification in %%install,
- removed glibc patch,
- fixed installing /etc/X11/wmconfig/tkmc.

* Thu Oct 23 1997 Michael K. Johnson <johnsonm@redhat.com>

- updated to 4.1.5
- added wmconfig

* Wed Oct 15 1997 Erik Troan <ewt@redhat.com>

- chkconfig is for mcserv package, not mc one

* Tue Oct 14 1997 Erik Troan <ewt@redhat.com>

- patched init script for chkconfig
- don't turn on the service by default

* Fri Oct 10 1997 Michael K. Johnson <johnsonm@redhat.com>

- Converted to new PAM conventions.
- Updated to 4.1.3
- No longer needs glibc patch.

* Thu May 22 1997 Michele Marziani <marziani@fe.infn.it>

- added support for mc alias in /etc/profile.d/mc.csh (for csh and tcsh)
- lowered number of SysV init scripts in /etc/rc.d/rc[0,1,6].d
  (mcserv needs to be killed before inet)
- removed all references to RPM_SOURCE_DIR
- restored $RPM_OPT_FLAGS when compiling
- minor cleanup of spec file: redundant directives and comments removed

* Sun May 18 1997 Michele Marziani <marziani@fe.infn.it>

- removed all references to non-existent mc.rpmfs
- added mcedit.1 to the %%files section
- reverted to un-gzipped man pages (RedHat style)
- removed double install line for mcserv.pamd

* Tue May 13 1997 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>

- added new rpmfs script,
- removed mcfn_install from mc (adding mc() to bash enviroment is in
  /etc/profile.d/mc.sh),
- /etc/profile.d/mc.sh changed to %%config,
- removed %%{prefix}/lib/mc/bin/create_vcs,
- removed %%{prefix}/lib/mc/term.

* Wed May 9 1997 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>

- changed source url,
- fixed link mcedit to mc,

* Tue May 7 1997 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>

- new version 3.5.27,
- %%dir %%{prefix}/lib/mc/icons and icons removed from tkmc,
- added commented xmc part.

* Tue Apr 22 1997 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>

- FIX spec:
   - added URL field,
   - in mc added missing %%{prefix}/lib/mc/mc.ext, %%{prefix}/lib/mc/mc.hint,
     %%{prefix}/lib/mc/mc.hlp, %%{prefix}/lib/mc/mc.lib, %%{prefix}/lib/mc/mc.menu.

* Fri Apr 18 1997 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>

- added making packages: tkmc, mcserv (xmc not work yet),
- gziped man pages,
- added /etc/pamd.d/mcserv PAM config file.
- added instaling icons,
- added /etc/profile.d/mc.sh,
- in %%doc added NEWS README,
- removed %%{prefix}/lib/mc/FAQ,
- added mcserv.init script for mcserv (start/stop on level 86).
