#rh-7.0-2
Summary: The skeleton package which defines a simple Mandrake Linux system.
Name: basesystem
Version: 9.2
Release: 1mdk
License: GPL
Group: System/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

Requires: setup filesystem sed initscripts console-tools utempter
Requires: chkconfig coreutils SysVinit bdflush crontabs dev
Requires: e2fsprogs etcskel findutils grep gzip kernel less 
Requires: logrotate losetup mingetty modutils mount net-tools passwd procps
Requires: psmisc mandrake-release rootfiles rpm sash shadow-utils 
Requires: stat sysklogd tar termcap time util-linux vim
Requires: vixie-cron which perl-base common-licenses
Requires: ldconfig

# (gb) Add timezone database here for now before moving it to DrakX
Requires: timezone

# MDK 9.0 requires a working libgcc
# Note: gcc3.2 is the system compiler there
Requires: libgcc >= 3.2-1mdk

%ifarch %ix86
Requires: lilo mkbootdisk
%endif
%ifarch alpha
Requires: aboot
%endif
%ifarch sparc sparc64
Requires: silo mkbootdisk
%endif
# (sb) need pdisk hfsutils ybin mktemp to setup bootloader PPC
%ifarch ppc
Requires: pdisk hfsutils ybin mktemp mkinitrd pmac-utils
%endif
# (fg) 20001027 ia64 uses eli as a bootloader
%ifarch ia64
Requires: elilo mkinitrd
%endif
%ifarch x86_64
Requires: lilo mkbootdisk
%endif

%description
Basesystem defines the components of a basic Mandrake Linux system (for
example, the package installation order to use during bootstrapping).
Basesystem should be the first package installed on a system, and it
should never be removed.
%files

%changelog
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

