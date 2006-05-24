#
# spec file for package basesystem
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		basesystem
%define version 	2.0
%define release 	%_revrel
%define epoch		1

Summary:	The skeleton package which defines a simple Annvix system
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		System/Base
URL:		http://annvix.org/

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	setup filesystem sed initscripts console-tools utempter
Requires:	chkconfig coreutils SysVinit crontabs dev
Requires:	e2fsprogs etcskel findutils grep gzip kernel less 
Requires:	logrotate losetup mingetty modutils mount net-tools passwd procps
Requires:	psmisc annvix-release rootfiles rpm sash shadow-utils 
Requires:	stat syslog tar termcap time util-linux vim
Requires:	crond which perl-base common-licenses srv runit afterboot
Requires:	bootloader, mkinitrd
Requires:	ldconfig
Requires:	libgcc >= 3.2-1mdk
Requires:	timezone
# (sb) need pdisk hfsutils mktemp to setup bootloader PPC
%ifarch ppc
Requires:	pdisk hfsutils mktemp pmac-utils
%endif

%description
Basesystem defines the components of a basic Annvix system (for
example, the package installation order to use during bootstrapping).
Basesystem should be the first package installed on a system, and it
should never be removed.


%files


%changelog
* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- 2.0
- make mkinitrd required by every arch

* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- 1.2
- Requires: s/sysklogd/syslog/

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-1avx
- 1.1
- drop bdflush from requires

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0-9avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0-8avx
- bootstrap build

* Tue Sep 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0-7avx
- Requires: runit
- remove Requires: daemontools, ucspi-tcp, mkbootdisk

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0-6avx
- Annvix build
- Requires: s/opensls-release/annvix-release/

* Sat Mar 13 2004 Vincent Danen <vdanen@opensls.org> 1.0-5sls
- Requires: s/mandrake-release/opensls-release/

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.0-4sls
- Requires: afterboot
- remove specific requires for bootloaders for multiple archs, instead make
  sure they all provide "bootloader" and Requires: bootloader

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 1.0-3sls
- Requires: crond, not dcron or any specific flavour of cron

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 1.0-2sls
- Requires: dcron, srv, daemontools, ucspi-tcp
- remove Requires: vixie-cron

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.0-1sls
- change for OpenSLS
- tidy spec
- Epoch: 1

* Thu Apr 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.2-1mdk
- add mkbootdisk for x86-64

* Fri Oct 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 9.0-3mdk
- Requires: s/fileutils, sh-utils, textutils/coreutils/

* Sun Oct  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.0-2mdk
- Requires: lilo on x86-64 too

* Tue Sep 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.0-1mdk
- Requires: libgcc >= 3.2-1mdk

* Sat Jun 15 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 8.2-3mdk
- Requires: timezone here for now until DrakX deals with it directly
- Requires: ldconfig on IA-64 too

* Tue Apr  2 2002 Pixel <pixel@mandrakesoft.com> 8.2-2mdk
- don't require tmpwatch (not mandatory)

* Fri Feb 22 2002 Pixel <pixel@mandrakesoft.com> 8.2-1mdk
- next version is... 8.2 :)

* Fri Feb 22 2002 Pixel <pixel@mandrakesoft.com> 8.1-5mdk
- add BuildRoot to please rpmlint
- remove requires
  * ntsysv (replaced by drakxservices)
  * procmail (not needed)
  * libtermcap2 (no need to require libraries)
  * basesystem (why was it there?)

* Thu Jan 24 2002 Pixel <pixel@mandrakesoft.com> 8.1-4mdk
- remove requires
  * hdparm setserial (not needed by many hardware)
  * info man (not needed with excludedocs)
  * getty_ps
  * ash (there's sash which is much more useful)

* Thu Jan 24 2002 Pixel <pixel@mandrakesoft.com> 8.1-3mdk
- remove requires 
  * isapnptools (now required by sndconfig)
  * grub (lilo *is* needed, but not grub)
  * msec (DrakX will ensure it is installed in 99% of installs)

* Tue Dec  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 8.1-2mdk
- s|Copyright|Licenses|;

* Fri Sep 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 8.1-1mdk
- Rebuild.

* Wed Jul 11 2001 Matthias Badaire <mbadaire@mandrakesoft.com> 8.0-5mdk
- add mkinitrd for ia64

* Fri Jul  6 2001 Matthias Badaire <mbadaire@mandrakesoft.com> 8.0-4mdk
- change eli to elilo

* Fri May 11 2001 Stew Benedict <sebedict@mandrakesoft.com> 8.0-3mdk
- remove kernel-pmac, add pmac-utils to requires - PPC

* Thu Mar 22 2001 Stew Benedict <sbenedict@mandrakesoft.com> 8.0-2mdk
- add mkinitrd to requires - PPC

* Tue Mar 20 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 8.0-1mdk
- following lib policy, add libtermcap2 to basesystem
- bomb version to ``8.0''

* Wed Mar 7 2001 Stew Benedict <sbenedict@mandrakesoft.com> 7.2-5mdk
- ppc add mktemp to requires

* Fri Feb 13 2001 Stew Benedict <sbenedict@mandrakesoft.com> 7.2-4mdk
- ppc: requires ybin

* Fri Oct 27 2000 Francis Galiegue <fg@mandrakesoft.com> 7.2-2mdk

- ia64: does not require ldconfig nor procmail for now - KLUDGE - see spec file
  for details
- ia64: requires eli

* Mon Oct  9 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 7.2-1mdk
- 7.2

* Fri Mar 24 2000 Pixel <pixel@mandrakesoft.com> 7.1-4mdk
- remove the BuildArchitectures: noarch
(otherwise can't have arch dependent Requires, silly me)

* Wed Mar 22 2000 Pixel <pixel@mandrakesoft.com> 7.1-3mdk
- changed require vim-minimal to vim (thanks Quel Qun)

* Tue Mar 21 2000 Pixel <pixel@mandrakesoft.com> 7.1-2mdk
- added a *lot* of requires. Now *is* the base

* Mon Mar 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 7.1-1mdk
- Upgrade version.
- Update groups.

* Thu Dec  2 1999 Pixel <pixel@linux-mandrake.com>
- changed back Requires to preReq :(

* Wed Dec  1 1999 Pixel <pixel@linux-mandrake.com>
- changed preReq to Requires

* Tue Oct 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build Release.

* Tue Jul 06 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build in the new environement (VER: 6mdk).

* Fri Apr  9 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- add de locale

* Tue Mar 16 1999 Cristian Gafton <gafton@redhat.com>
- don't require rpm (breaks dependency chain)

* Tue Mar 16 1999 Erik Troan <ewt@redhat.com>
- require rpm

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Sep 23 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

