#
# spec file for package mkbootdisk
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mkbootdisk
%define version 	1.5.1
%define release 	%_revrel

Summary: 	Creates an initial ramdisk image for preloading modules
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Kernel and hardware
URL:		http://www.redhat.com/swr/src/mkbootdisk-1.4.2-1.src.html
Source: 	%{name}-%{version}.tar.bz2
Patch0: 	mkbootdisk-1.5.1-mdk.patch
Patch1: 	mkbootdisk-1.5.1-devfs-compliant.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}

ExclusiveArch: 	sparc sparc64 %{ix86} x86_64 amd64
ExclusiveOs: 	Linux
Requires: 	mkinitrd, gawk, dosfstools, mktemp
Conflicts:	modutils < 2.3.11-5
%ifarch %ix86 x86_64 amd64
Requires:	syslinux >= 1.76-2mdk
%endif
%ifarch sparc sparc64
Requires: 	silo genromfs
%endif

%description
The mkbootdisk program creates a standalone boot floppy disk for booting
the running system.  The created boot disk will look for the root
filesystem on the device mentioned in /etc/fstab and includes an
initial ramdisk image which will load any necessary SCSI modules for
the system.


%prep
%setup -q
%patch0 -p1 -b .mdk
%patch1 -p1 -b .devfs


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%make BUILDROOT=%{buildroot} mandir=%{_mandir} install


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(755,root,root) /sbin/mkbootdisk
%attr(644,root,root) %{_mandir}/man8/mkbootdisk.8*

%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1-3avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1-2avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 1.5.1-1sls
- 1.5.1
- Requires: gawk rather than /bin/awk
- rediff P0, P1 (tvignaud)
- drop P2, P3 (tvignaud)

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.4.5-9sls
- minor spec cleanups

* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 1.4.5-8sls
- OpenSLS build
- tidy spec

* Tue Aug  5 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.5-7mdk
- amd64 rebuild

* Sun Jul 06 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.4.5-6mdk
- Requires syslinux only on x86/x86_64

* Wed Apr 16 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.5-5mdk
- Add x86-64

* Thu Sep 12 2002 François Pons <fpons@mandrakesoft.com> 1.4.5-4mdk
- fix bad requires listed.

* Wed Sep 11 2002 François Pons <fpons@mandrakesoft.com> 1.4.5-3mdk
- fix to use syslinux-old instead of syslinux in order to run with
  cooker version of kernel (patch3).

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.5-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Jul 26 2002 Damien Chaumette <dchaumette@mandrakesoft.com> 1.4.5-1mdk
- version 1.4.5
- little patchs fix due to changes

* Tue Nov 20 2001 Yves Duret <yduret@mandrakesoft.com> 1.4.2-8mdk
- changed Summary:, it's no longer a bad copy and paste job from the
  mkinitrd spec file (MF #50193) (rh)
- added Url: tag

* Sun Sep 23 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4.2-7mdk
- really fix No space left on device since very surprinsingly, a command
  may fail at a moment and a following command may succeed, so testing
  errorcode of last copy command is not enough :-(

* Fri Sep 21 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4.2-6mdk
- when No space left on device, exitcode-1

* Thu Aug 30 2001 Pixel <pixel@mandrakesoft.com> 1.4.2-5mdk
- remove fd0[uH]1440 special code

* Wed Aug 29 2001 Pixel <pixel@mandrakesoft.com> 1.4.2-4mdk
- devfs compliant
- use fd0u1440 instead of fd0H1440 (devfs prefer this)

* Mon Jul 16 2001 Yves Duret <yduret@mandrakesoft.com> 1.4.2-3mdk
- rebuild
- spec clean up

* Tue May 29 2001 Yves Duret <yduret@mandrakesoft.com> 1.4.2-2mdk
- corrected Requires and Conflicts tags.

* Mon May 28 2001 Yves Duret <yduret@mandrakesoft.com> 1.4.2-1mdk
- bumped into version 1.4.2 thx to gc and his rubish bot
- rewrite all patches : geoffreyleeisation risk :)
- warning : now uses syslinux instead of lilo

* Tue Mar 13 2001 Pixel <pixel@mandrakesoft.com> 1.2.8-3mdk
- as "Paul Giordano" <gio2000@mindspring.com> says, it works much better when
the device given to lilo is the same as the one which is mounted under devfs
(otherwise you get a device busy). So give boot=$rdevice to lilo

* Sat Feb 24 2001 Pixel <pixel@mandrakesoft.com> 1.2.8-2mdk
- workaround for bad floppy drives which can't correctly give their size (fix is
to use fd0H1440), see civileme for more

* Thu Dec 21 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.8-1mdk
- new and shiny source.

* Thu Aug 24 2000 Pixel <pixel@mandrakesoft.com> 1.2.7-2mdk
- fix for /boot/boot.b now being a symlink (cp -a is stupid for boot.b)

* Thu Jul 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.7-1mdk
- Clean-up  patches (aka: i am sure i have break something)
- 1.2.7.
- BM.

* Wed Apr 19 2000 Pixel <pixel@mandrakesoft.com> 1.2.4-8mdk
- patch for ls120 (add ability to precise bios number for device)

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.4-7mdk
- Spec-helper clean-up.
- Adjust groups.

* Sun Mar 19 2000 John Buswell <johnb@mandrakesoft.com> 1.2.4-6mdk
- Added PPC support
- Added k7 arch

* Mon Mar 13 2000 Pixel <pixel@mandrakesoft.com> 1.2.4-5mdk
- patch for loopback

* Sun Jan  2 2000 Pixel <pixel@mandrakesoft.com>
- add ability to handle options given to kernel (via append=...)

* Tue Dec 21 1999 Pixel <pixel@mandrakesoft.com>
- added requires /bin/awk and cpio

* Fri Nov 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.2.4.

* Fri Oct 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.2.3.
- Remove cpio deps.

* Tue Sep 28 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Requires cpio (#41).

* Wed Jun 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add patch to be sure to copy all devices (using cpio) from
  H.J. <hjl@varesearch.com>.

* Fri May 14 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- We boot on Mandrake no RedHat.

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Update to 1.2.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- fix Summary line (RH apparently took the same as mkinitrd has)

* Thu Feb 25 1999 Matt Wilson <msw@redhat.com>
- updated the description

* Thu Nov  5 1998 Jeff Johnson <jbj@redhat.com>
- import from ultrapenguin 1.1.

* Fri Oct 30 1998 Jakub Jelinek <jj@ultra.linux.cz>
- support for SPARC

* Sat Aug 29 1998 Erik Troan <ewt@redhat.com>
- wasn't including nfs, isofs, or fat modules properly
- mkinitrd args weren't passed right due to a typo
