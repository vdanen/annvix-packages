#
# spec file for package xinitrc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name    	xinitrc
%define version 	2.4.4
%define release 	%_revrel

Summary:	The default startup script for the X Window System
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/XFree86
URL:		http://www.mandrakelinux.com/
# get the source from our cvs repository (see
# http://www.linuxmandrake.com/en/cvs.php3)
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	XFree86 >= 3.3.5-12mdk, bash, grep
Conflicts:	initscripts < 6.87-2mdk

%description
The xinitrc package contains the xinitrc file, a script which is used
to configure your X Window System session or to start a window manager.


%prep
%setup -q


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install R=%{buildroot}/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) /etc/X11/Xmodmap
%config(noreplace) /etc/X11/xinit/Xclients
%config(noreplace) /etc/X11/xinit/xinitrc
%config(noreplace) /etc/X11/xinit/fixkeyboard
%config(noreplace) /etc/X11/xinit/XIM
%config(noreplace) /etc/X11/xdm/*
%config(noreplace) /etc/X11/Xsession
%config(noreplace) /etc/X11/Xresources
/usr/X11R6/bin/*
%dir /etc/X11/xinit.d
%dir /etc/X11/wmsession.d
%config(noreplace) /etc/X11/xinit.d/Mod_Meta_L_Disable


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4-81avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4-80avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4-79avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 2.4.4-78sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.4.4-77sls
- OpenSLS build
- tidy spec

* Thu Sep  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-76mdk
- enable to source /etc/X11/xinit.d scripts if they contain the special
comment "# to be sourced" (bug #2493)

* Mon Aug 25 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-75mdk
- Xsession doesn't handle anymore .xsession-errors with gdm

* Mon Mar 24 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-74mdk
- Xsession: add a fix for qtrc in Japanese

* Mon Mar  3 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-73mdk
- pass right session type to xinit.d scripts in default mode

* Tue Feb 25 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-72mdk
- pass $DESKTOP to xinit.d scripts

* Mon Feb 24 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-71mdk
- Xsetup_0: call numlock if present (bug #2301)

* Wed Feb 12 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-70mdk
- Xsetup_0: don't use kdmdesktop as it doesn't exist anymore

* Tue Sep 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-69mdk
- Xsession: do not change the background for non root users when called
from [gkx]dm. Put a watch cursor before launching the desktop.

* Fri Sep  6 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-68mdk
- Xsession: make the tests silent and back to a terminal in failsafe

* Tue Aug 27 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-67mdk
- fixkeyboard: set PATH before using xdpyinfo.

* Fri Aug 23 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-66mdk
- Xft.dpi resource to 90 and removed Xft.hinting resource (not used)

* Wed Aug 21 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-65mdk
- added resources for Xft to correct tiny and huge fonts rendering

* Fri Aug  9 2002 Pixel <pixel@mandrakesoft.com> 2.4.4-64mdk
- use /etc/profile.d/10lang.sh instead of lang.sh (and Conflicts: initscripts < 6.87-2mdk)

* Wed May 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-63mdk
- Xsession: launch twm in failsafe mode

* Tue Apr  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-62mdk
- corrected resources for tk packages (David Walser)

* Tue Mar 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-61mdk
- don't launch drakfw if $HOME doesn't exist
- don't set SSH_AGENT if already running under an ssh-agent.

* Wed Feb 27 2002 Pixel <pixel@mandrakesoft.com> 2.4.4-60mdk
- removed delay before loading xim; new XFree86 doesn't like it

* Wed Feb 20 2002 Pixel <pixel@mandrakesoft.com> 2.4.4-59mdk
- Xservers: raise the priority of the X server (Martin Maèok)

* Sat Sep 22 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.4.4-58mdk
- xinitrc-XIM,Xsession: included patches from Jaegum that improves
 behaviour of XIMs in general and Korean one in particular
- xinitrc-XIM: added an entry for Chinput XIM
- Xsession: made XIM launched before first time Wizard (so if the
 wizard asks to type something you can use your language)

* Wed Sep 19 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-57mdk
- Xsetup_0: display the good color when KDE isn't installed (David).

* Wed Sep 19 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-56mdk
- Xsession: added ssh v2 identification files check (Stefan Siegel).

* Mon Sep 17 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-55mdk
- launch drakfw with an exec.

* Mon Sep 17 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-54mdk
- fix First Time wizard call (aka Daouda sux).
- fix the sync for root color.

* Mon Sep 17 2001 Daouda LO <daouda@mandrakesoft.com> 2.4.4-53mdk
- add First Time wizard for first login
- resync the cvs spec file!!

* Sat Sep 16 2001 David BAUDENS <baudens@mandrakesoft.com> 2.4.4-52mdk
- Fix color for root interface

* Fri Sep  7 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-51mdk
- configure xdm in local mode only (Pixel's request)

* Tue Sep  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-50mdk
- don't execute empty scripts in /etc/X11/xinit.d (Beat Kappert)

* Tue Aug 21 2001 David BAUDENS <baudens@mandrakesoft.com> 2.4.4-49mdk
- Change xsetroot colors according to new graphical charter

* Mon Aug 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-48mdk
- lookup mozilla before netscape (fcrozat)

* Tue Aug  7 2001 Stew Benedict <sbenedict@mandrakesoft.com> 2.4.4-47mdk
- move Xmodmap.{DISPLAY} to /etc/X11 like Xmodmap for FHS
- added keycode "115 = F13" and "117 = Menu" for KDE. (Stefan Siegel)

* Thu Aug  2 2001 Stew Benedict <sbenedict@mandrakesoft.com> 2.4.4-46mdk
- move Xmodmap to /etc/X11 and edit fixkeyboard for FHS

* Sat May  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-45mdk
- use the right session launcher to use bash -login.

* Mon Apr  9 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-44mdk
- allow restart of X server in kdm/xdm more than once

* Fri Apr  6 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-43mdk
- Xsession uses /etc/sysconfig/desktop to gather default

* Mon Apr  2 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-42mdk
- Xservers launch X with -deferplyphs 16 (Andrew Lee).

* Wed Mar 21 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-41mdk
- Xsession: fixed typo for commecial ssh (#2581).

* Sun Mar  4 2001 Pixel <pixel@mandrakesoft.com> 2.4.4-40mdk
- replaced a few "xterm" with "xvt"

* Fri Mar  2 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-39mdk
- in failsafe mode try xvt before xterm.

* Wed Jan 31 2001 Pablo Saratxaga <pablo@manderakesoft.com> 2.4.4-38mdk
- xinitrc-fixkeyboard: added a possibility to disable XKB use by the user

* Wed Jan 17 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-37mdk
- put Daouda changes in the xinitrc cvs module.
- /etc/X11/Xresources includes the old Xdefaults resources.

* Wed Jan 10 2001  Daouda Lo <daouda@mandrakesoft.com> 2.4.4-36mdk
- use kdmdesktop to set background (fixed )

* Thu Dec 28 2000 Pablo Saratxaga <pablo@manderakesoft.com> 2.4.4-35mdk
- xinitrc-fixkeyboard: added support of per-DISPLAY keyboard definitions

* Tue Dec 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.4-34mdk
- xinitrc-Mod_Meta_L_Disable: Add this ugly script, when a
  REMOVE_MOD_META_L=yes remove the MOD_META_L to make some
  applications happy (ie:xemacs).

* Tue Nov 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-33mdk
- added support for ssh2 (bug #871).
- use bash -login only on Xsession for xdm (bug #1505).

* Fri Oct 13 2000 Pablo Saratxaga <pablo@manderakesoft.com> 2.4.4-32mdk
- added auto-launching of XIM servers.

* Fri Oct 06 2000 David BAUDENS <baudens@mandrakesoft.com> 2.4.4-31mdk
- Set HELP_BROWSER

* Mon Oct  2 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-30mdk
- removed ^@ in /etc/X11/Xsession.

* Mon Oct  2 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-29mdk
- remove xhost+ in /etc/X11/Xsession (let msec do this job).

* Tue Sep 12 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-28mdk
- fix resources to make xdm starts the X server only once and let init do its job.

* Fri Sep 01 2000 David BAUDENS <baudens@mandrakesoft.com> 2.4.4-27mdk
- Use Linux-Mandrake colors for xsetroot

* Wed Aug 30 2000 Christopher Molnar <molnarc@mandrakesoft.com> 2.4.4-26mdk
- Xsetup_0: commented out the kdmdesktop and added line to fix background colors

* Tue Jun  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.4-25mdk
- Xsession: Resinsert /bin/bash -login.

* Mon Jun  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.4-24mdk
- Xsession: use /bin/sh instead of /bin/bash -login.

* Thu May  4 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-23mdk
- fix path of WindowMaker in RunWM.

* Thu Apr 27 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-22mdk
- added a fallback /etc/X11/xdm/Xsession.

* Thu Apr 20 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-21mdk
- Xsession: merge ~/.Xdefaults too.

* Thu Apr 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.4-20mdk
- xinitrc-RunWM: set wmaker to the right path (thanks
  john.cavan@sympatico.ca).

* Tue Apr 11 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-18mdk
- launch scripts in /etc/X11/xinit.d
- removed imwheel stuff.

* Fri Apr  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.4-18mdk
- Cvs import clean up spec file.

* Thu Apr  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.4-17mdk
- Another fix of Xsession.

* Thu Apr  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.4-16mdk
- Try to get chksession feature when launching with startx (aka:
  fix merge of flepied).

* Thu Apr  6 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.4.4-15mdk
- smaller xterm in Xsession for failsafe setting, in order
  to stay in screen when having 800x600

* Thu Mar 30 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-14mdk
- activate imwheel only if WHEEL is yes in /etc/sysconfig/mouse.
- end the merge of xinit and xdm startup.

* Thu Mar 09 2000 Francis Galiegue <francis@mandrakesoft.com> 2.4.4-13mdk
- imwheel -k added to Xsession

* Wed Mar  1 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-12mdk
- make Xsession ssh aware.

* Mon Feb  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-11mdk

- unified xdm and startx init sequences.

* Thu Jan  6 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-10mdk

- load xmodmaps the same way in xinit and xdm modes.

* Wed Dec 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Do an exec for chksession. (c) Chmouel.

* Wed Dec 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Do an exec (flepied).

* Wed Dec 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Xsession and Xclients for new chksession.

* Tue Dec 21 1999 Frederic Lepied <flepied@mandrakesoft.com> 2.4.4-5mdk

- fix RunWM for WindowMaker.
- fix Xclients to be able to launch something else than KDE, GNOME or AnotherLevel.

* Thu Dec 16 1999 Frederic Lepied <flepied@mandrakesoft.com>

- fixed a typo in /etc/X11/xinit/xinitrc.

* Wed Nov 24 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- By default if there is no windows manager launch icewm-light no fvwm.
- Put a midnight color by default.

* Wed Nov  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add xmodmap files.
- 2.4.4.

* Thu Jul 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add Xsession files.
- Oups typo :-((

* Sun May 09 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- By default we run kde (again 8-)

* Mon May 03 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adpatations.
- By default Mandrake launch KDE.

* Mon Apr 19 1999 Preston Brown <pbrown@redhat.com>
- argh, fixed my changes from yesterday

* Sun Apr 18 1999 Preston Brown <pbrown@redhat.com>
- added /etc/sysconfig/desktop support

* Mon Mar 22 1999 Bill Nottingham <notting@redhat.com>
- make /etc/X11/xinit/* %config (bug #1051)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Tue Feb 02 1999 Preston Brown <pbrown@redhat.com>
- added ability to have KDE recognized if it is all that is installed

* Wed Jan 27 1999 Preston Brown <pbrown@redhat.com>
- updated so that GNOME is the default, and a few other cleanups

* Fri Sep 18 1998 Cristian Gafton <gafton@redhat.com>
- added the RunWM script and modified Xclients to use this new script

* Sun Sep 13 1998 Cristian Gafton <gafton@redhat.com>
- included WindowMaker hints

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 22 1998 Cristian Gafton <gafton@redhat.com>
- handle AfterStep (and possibly other window managers)

* Tue Nov 11 1997 Michael K. Johnson <johnsonm@redhat.com>
- export the BROWSER variable.

* Fri Nov 08 1997 Cristian Gafton <gafton@redhat.com>
- added handling for the BROWSER variable

* Wed Oct 15 1997 Cristian Gaftin <gafton@redhat.com>
- updated for AnotherLevel

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built for glibc, added dependencies

* Thu Mar 20 1997 Erik Troan <ewt@redhat.com>
- Added /etc/X11/xinitrc/Xclients to this file and removed it from rootfiles
  and etcskel.

