#
# spec file for package etcskel
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		etcskel
%define version 	1.63
%define release 	%_revrel

Summary:	Annvix default files for new users' home directories
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Base
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	bash

%description
The etcskel package is part of the basic Annvix system.

Etcskel provides the /etc/skel directory's files. These files are then placed
in every new user's home directory when new accounts are created.


%prep
%setup -q


%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install RPM_BUILD_ROOT=%{buildroot}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc ChangeLog
%dir /etc/skel
%config(noreplace) /etc/skel/.??*
%config(noreplace) /etc/skel/tmp


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.63-20avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.63-19avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.63-18avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 1.63-17sls
- DIRM: /etc/skel

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 1.63-17sls
- more OpenSLS specific

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 1.63-16sls
- OpenSLS build

* Mon Sep 08 2003 David Baudens <baudens@mandrakesoft.com> 1.63-15mdk
- Rebuild

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.63-14mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon Oct 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.63-13mdk
- s!Linux Mandrake!Mandrake Linux!g

* Tue May 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.63-12mdk
- Remove .bash* (provided by bash).

* Thu Apr 12 2001 David BAUDENS <baudens@mandrakesoft.com> 1.63-11mdk
- Remove /etc/skel/kderc (provided by kdebase)
- Remove /etc/skel/netscape/* (created by Netscape)

* Thu Jan  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.63-10mdk
- remove all commands except source /etc/bashrc from .bashrc and .bash_profile
to allow upgrade.
- removed Xdefaults (all is in Xresources now).

* Thu Oct 05 2000 David BAUDENS <baudens@mandrakesoft.com> 1.63-9mdk
- Really fix xterm font problem with KDE 2

* Wed Oct 04 2000 Francis Galiegue <fg@mandrakesoft.com> 1.63-8mdk
- Fix xterm font problem with KDE2, hopefully
  [ NOTE: not merged with CVS, right now this is a patch ]

* Sun Sep 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.63-7mdk
- Rebuild to remove the CVS files.

* Thu Aug 31 2000 David BAUDENS <baudens@mandrakesoft.com> 1.63-6mdk
- Update kderc to KDE 2

* Thu Aug  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.63-5mdk
- Increase release since titi won't follow rules like normal.

* Thu Aug  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.63-4mdk
- mailcap: s|mswordview|wvHtml|;

* Tue Apr 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.63-3mdk
- remove vimrc.

* Thu Apr 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.63-2mdk
- bash_profile: add export HISTIGNORE="[   ]*:&:bg:fg" (dindin).

* Wed Mar 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.63-1mdk
- etcskel.spec: Adjust groups.
- Makefile: remove zshrc (moved to his own package).
- Makefile: remove emacs (moved to his own package).

* Wed Feb 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.62-35mdk
- zshrc: define function dir to /usr/share/zsh/$ZSH_VERSION/

* Mon Dec 27 1999 Pixel <pixel@mandrakesoft.com>
- remove the df alias from bashrc and zshrc (moved to /etc/profile.d/alias.sh)
- Real Makefile and cvs add (chmou).

* Wed Dec 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- fix vimrc with vim-minimal.

* Sat Dec 18 1999 Pixel <pixel@mandrakesoft.com>
- added .netscape/(cache|archive)

* Wed Dec 15 1999 Pixel <pixel@mandrakesoft.com>
- fixed home/end in .emacs

* Thu Dec 02 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- alias df to -x supermount.

* Wed Dec  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Make screen happy, chmod 700 ~/tmp/.

* Wed Dec 01 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- fix color ls in X_Windows.

* Fri Nov 26 1999 Pixel <pixel@linux-mandrake.com>
- fix .vimrc for vim-minimal without vim-common

* Tue Nov  9 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- fix .emacs typo (again).

* Thu Oct  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix .emacs for xemacs and (string-match).
- Fix .emacs for Xemacs to handle bzip2.

* Fri Aug 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix typo.

* Fri Aug 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Bind Window key to (K)Menu.

* Sun Aug  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- zshrc: by defaut we launch the completion machine.

* Thu Aug 05 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix typo in .vimrc (statusline).

* Mon Aug  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Syn on only with enhanced vim.
- Add statusbar for vim
- New alias in bashrc.

* Fri Jul 16 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Removing the statusbar by default in vim (awfull).

* Mon Jun 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Adding a Xauthoriy varibale to allow connection from localhost with another
  use (even if we make xhost -).

* Mon Jun 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Removing the if &term=xterm in .vimrc.

* Tue May 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Accents for Gnu-Emacs.

* Tue May 18 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fixing a [ -n $INPUTRC ] || { STUFF }
- add a mime type for mswordview.

* Mon May 17 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix locales with kde bug.

* Fri May 14 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix bug with alias on xtem (need -ls to display .bashrc)

* Tue May 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fixing typo in .vimrc.
- Reinserting alias -i to .bash_profile.
- tmp directory in $HOME/.

* Wed May 05 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add modifications to .Xdefauts and emacs to get to emacs some 
  new colors.

* Tue Apr 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- New files like .vimrc .zshrc
- Modification of .emacs to handle all keys.
- Modifications of .Xdefault to handle suppr/backspace.

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- upgarde to 1.61

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- glibc 2.1

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- clean out more stuff from the default .Xdefaults

* Sat Aug 22 1998 Jeff Johnson <jbj@redhat.com>
- use BASH_ENV=~/.bashrc -- leave ENV for ksh (change #459)

* Fri Nov 08 1997 Cristian Gafton <gafton@redhat.com>
- .Xdefaults file was broken; it is not processed by any macro thing.

* Tue Sep 09 1997 Erik Troan <ewt@redhat.com>
- converted to a noarch package

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- added bash dependencie 

* Thu Mar 20 1997 Erik Troan <ewt@redhat.com>
- Moved .Xclients and .xsession to xinitrc package
