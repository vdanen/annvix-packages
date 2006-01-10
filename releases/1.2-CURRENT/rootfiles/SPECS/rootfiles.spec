#
# spec file for package rootfiles
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rootfiles
%define version		10.2
%define	release		%_revrel

Summary:	The basic required files for the root user's directory
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Base
Source:		%{name}-%{version}.tar.bz2
Patch0:		rootfiles-9.1-avx-rootwarning.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

%description
The rootfiles package contains basic required files that are placed
in the root user's account.


%prep


%setup -q
%patch0 -p0 -b .warn


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}/root
make install RPM_BUILD_ROOT=%{buildroot}

rm -f %{buildroot}/root/.bash_completion


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) /root/.Xdefaults
%config(noreplace) /root/.bash_logout
%config(noreplace) /root/.bash_profile
%config(noreplace) /root/.bashrc
%config(noreplace) /root/.cshrc
%config(noreplace) /root/.tcshrc
%config(noreplace) /root/.vimrc
%attr(0700,root,root) /root/tmp/


%changelog
* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 10.2-1avx
- mandriva 10.2-2mdk:
  - modernize root's .vimrc
  - clean description
- get rid of bash completion junk

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.1-6avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.1-5avx
- bootstrap build

* Mon Jul 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.1-4avx
- update P0 so that if one connects via rsync (where logname is undefined)
  the error doesn't go to STDOUT
- patch policy

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.1-3avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 9.1-2sls
- minor spec cleanups
- remove the %%pre backup of Xclients files
- add warning about logging in as root
- remove Changelog doc (no one cares)

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 9.1-1sls
- OpenSLS build
- tidy spec

* Sat Nov 30 2002 Yves Duret <yves@zarb.org> 9.1-0.1mdk
- bashrc: source /etc/bashrc after PATH redefinition (for bash_completion)
  thanks Guillaume Rousse.
- added clean, changelog rules in Makefile. enhanced version detection
  (with rpm -q) and toto rules.
- ChangeLog is now always uptodate.
- resync spec file with CVS one.

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 8.2-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Feb 15 2002 David BAUDENS <baudens@mandrakesoft.com> 8.2-1mdk
- Update version to 8.2

* Mon Oct 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 8.0-5mdk
- bashrc: remove obsoletes stuff.

* Thu Apr 12 2001 David BAUDENS <baudens@mandrakesoft.com> 8.0-4mdk
- Remove KDE stuff (provided by kdebase)
- Remove Netscape stuff (provided by netscape)

* Tue Mar 20 2001 Daouda Lo <daouda@mandrakesoft.com> 8.0-3mdk
- remove Drakconf workaround

* Tue Mar 20 2001 Daouda Lo <daouda@mandrakesoft.com> 8.0-2mdk
- workaround for DrakConf crash.

* Tue Mar 13 2001 Pixel <pixel@mandrakesoft.com> 8.0-1mdk
- vimrc: remove "Default tab for 4" (set ts=4)

* Thu Jan 18 2001 David BAUDENS <baudens@mandrakesoft.com> 7.3-1mdk
- Fix build on PPC
- Spec clean up

* Wed Nov 08 2000 David BAUDENS <baudens@mandrakesoft.com> 7.2-2mdk
- Use config(noreplace)

* Mon Oct  9 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 7.2-1mdk
- rebuild for 7.2

* Mon Jul 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 7.1-9mdk
- rootfiles.spec: BM.

* Wed May 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 7.1-8mdk
- Desktop/DrakConf.kdelnk: Don't launch with kdesu for root.

* Mon May 08 2000 dam's <damien@mandrakesoft.com> 7.1-7mdk
- corrected vimrc

* Mon May 08 2000 dam's <damien@mandrakesoft.com> 7.1-6mdk
- added no wrap in vimrc

* Sun Apr 30 2000 dam's <damien@mandrakesoft.com> 7.1-5mdk
- re-added XKill in Desktop

* Thu Apr 27 2000 dam's <damien@mandrakesoft.com> 7.1-4mdk
- kde/share/config/kpanelrc :removed DesktopButton section to fix empty panel in root session

* Wed Apr 26 2000 dam's <damien@mandrakesoft.com> 7.1-3mdk
- Desktop : cleaned up kdelnk files.

* Thu Mar 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 7.1-2mdk
- tcshrc: define hard PATH.
- cshrc: define hard PATH.
- rootfiles.spec: adjust groups.
- rootfiles.spec: Add ChangeLog in %doc
- bashrc: cleanup.

* Wed Mar 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 7.1-1mdk
- Remove .emacs (moved to his package).
- Remove .zshrc (moved to his package).

* Mon Jan 10 2000 Pixel <pixel@mandrakesoft.com>
- added a kfmrc (for Templates directory)

* Tue Jan 04 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Sync .kdelnk.

* Tue Dec 28 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- add kppp icons for kde.
- True makefile and cvs.

* Wed Dec 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- fix vimrc with vim-minimal.

* Tue Dec 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- put ~/tmp as 700.

* Sat Dec 18 1999 Pixel <pixel@mandrakesoft.com>
- added .netscape/(cache|archive)

* Thu Dec 16 1999 François PONS <fpons@mandrakesoft.com>
- removed Cd-Rom.kdelnk and floppy.kdelnk, since handled by DrakX.

* Thu Dec 16 1999 Pixel <pixel@mandrakesoft.com>
- moved Templates from Desktop to .kde
- better .emacs (especially gnu-emacs)

* Fri Dec 10 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Syn Desktop.

* Thu Dec 02 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Alias df to -x supermount.

* Wed Dec 01 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Remove the export XAUTHORITY for root.

* Sat Nov 27 1999 Pixel <pixel@linux-mandrake.com>
- .vimrc: `syntax on' only if vim-common is there

* Mon Nov 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add hwiz.kdelnk in Autostart of kde package.

* Wed Nov 10 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix .emacs (<c> Chmouel All right reserved).

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- fix stupid path in .bashrc (thanks john).

* Tue Sep 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add Desktop directory.
- Kde in English.

* Tue Sep 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Insert kde configuration and Desktop of kde directly here.

* Fri Aug 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix typo.

* Fri Aug 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Bind Windows key to (K)menu.

* Sun Aug  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- zshrc: by defaut we launch the completion machine.

* Thu Aug 05 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix typo in .vimrc.

* Mon Aug  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Syn on only with enhanced vim.
- Add statusbar for vim
- New alias in bashrc.

* Tue Jun 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Tmp for root.

* Tue May 18 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix locales bug rapport by Jean Michel <jmdault@netrevolution.com>


* Wed May 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Security path for root.
- Suppr work now for root.

* Tue May 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- a /sbin and /usr/sbin for root even for telnet.

* Sun May 09 1999 Gaël Duval <gael@linux-mandrake.com>

- Added .kderc for root 
- changed the version number (5.2->6.0)

* Sun May 09 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Mandrake adaptations.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- add %clean (#719)

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Wed Oct  9 1998 Bill Nottingham <notting@redhat.com>
- remove /root from %files (it's in filesystem)

* Sun Aug 23 1998 Jeff Johnson <jbj@redhat.com>
- portability fix for .cshrc (problem #235)
- change version to be same as release.

* Tue Sep 09 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

* Thu Mar 20 1997 Erik Troan <ewt@redhat.com>
- Removed .Xclients and .Xsession from package, added %pre to back up old
  .Xclients if necessary.
