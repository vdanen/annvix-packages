#
# spec file for package makedev
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# synced with mdk 4.4-1mdk
#
# $Id$

%define revision	$Rev$
%define name		makedev
%define version		4.4
%define release 	%_revrel

%define devrootdir	/lib/root-mirror
%define dev_lock	/var/lock/subsys/dev
%define makedev_lock	/var/lock/subsys/makedev

Summary:	A program used for creating the device files in /dev
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/soft/makedev/
Source:		%{name}-%{version}.tar.bz2
Patch:		makedev-4.4-avx-config.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires(post):	shadow-utils
Requires(post):	sed
Requires(post):	coreutils
Requires(post):	mktemp
Requires:	bash
Requires:	perl-base
Provides:	dev
Provides:	MAKEDEV
Obsoletes:	dev
Obsoletes:	MAKEDEV
# coreutils => /bin/mkdir

%description
This package contains the makedev program, which makes it easier to create
and maintain the files in the /dev directory.  /dev directory files
correspond to a particular device supported by Linux (serial or printer
ports, scanners, sound cards, tape drives, CD-ROM drives, hard drives,
etc.) and interface with the drivers in the kernel.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch -p0


%build
# Generate the config scripts
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{devrootdir}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
/usr/sbin/useradd -c "virtual console memory owner" -u 69 \
    -s /sbin/nologin -r -d /dev vcsa 2> /dev/null || :

#- when devfs or udev is used, upgrade and install can be done easily :)
if [[ -e /dev/.devfsd ]] || [[ -e /dev/.udev.tdb ]] || [[ -d /dev/.udevdb/ ]]; then
    [[ -d %{devrootdir} ]] || mkdir %{devrootdir}
    mount --bind / %{devrootdir}
    DEV_DIR=%{devrootdir}/dev
     
    [[ -L $DEV_DIR/snd ]] && rm -f $DEV_DIR/snd
    mkdir -p $DEV_DIR/{pts,shm}
    /sbin/makedev $DEV_DIR

    # race 
    while [[ ! -c $DEV_DIR/null ]]; do
        rm -f $DEV_DIR/null
        mknod -m 0666 $DEV_DIR/null c 1 3
        chown root:root $DEV_DIR/null
    done

    umount -f %{devrootdir} 2> /dev/null
#- case when makedev is being installed, not upgraded
else
    DEV_DIR=/dev
    mkdir -p $DEV_DIR/{pts,shm}
    [[ -L $DEV_DIR/snd ]] && rm -f $DEV_DIR/snd
    /sbin/makedev $DEV_DIR

    # race 
    while [[ ! -c $DEV_DIR/null ]]; do
        rm -f $DEV_DIR/null
        mknod -m 0666 $DEV_DIR/null c 1 3
        chown root:root $DEV_DIR/null
    done

    [[ -x /sbin/pam_console_apply ]] && /sbin/pam_console_apply
fi
:


%files
%defattr(-,root,root)
%{_mandir}/*/*
/sbin/makedev
%dir %{_sysconfdir}/makedev.d/
%config(noreplace) %{_sysconfdir}/makedev.d/*
%dir /dev
%dir %{devrootdir}

%files doc
%defattr(-,root,root)
%doc COPYING devices.txt README


%changelog
* Thu Aug 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4
- make the serial perms owned root:admin since we don't have group uucp
- spec cleanups

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4
- add -doc subpackage
- rebuild with gcc4
- some spec cleanups

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4-1avx
- 4.4
- sync with mandrake 4.4-1mdk (tvignaud):
  - add cloop, DVB nodes
  - enable extra makedev parameter to be regexp
  - udev support
  - enable to create onle one device rather than all devices

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1-8avx
- correct the buildroot

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1-7avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1-6avx
- bootstrap build

* Fri Feb 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1-5avx
- s/SLS/Annvix/
- add the erandom and frandom device nodes

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.1-4avx
- require packages not files
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 4.1-3sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 4.1-2sls
- OpenSLS build
- tidy spec

* Wed Sep 17 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1-1mdk
- smoother update
- fix rare "empty /dev/ on update" bug
- provide alsa devices (which is needed since /proc/asound/dev/
  entries are no more populated by alsa drivers) for users that do not
  want to use devfs
- add nosst devices for OnStream SC-x0 tape

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.0.1-2mdk
- rebuild

* Mon Dec 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0.1-1mdk
- enforce "having at least one argument and only one argument" policy

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0-2mdk
- fix url: use cvsweb url rather than just main mdk web site url

* Mon Nov 04 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0-1mdk
- simplify requires (through coreutils)
- generator scripts :
  o move them into scripts/
  o normalise "#!"
  o document them
  o set vim settings for editing
  o genida : don't generate spurious "1" base argument
- makedev.d/* :
  o remove all aliases that're of no use since we used to just skip them
    in makedev
  o reorganize files
- makedev :
  o move it from /usr/sbin to /sbin
  o rename :
    * mdk_makedev script as makedev
    * makedev() function into make_dev_t()
  o remove support for :
    * socket/fifo since we don't use it
      (this can be added back through patches/add_fifo_socket_support.diff)
    * alias skiping since we remove all aliases from configuration files
  o factorise node creation code in make_dev()
- man pages :
  o add makedev(5) : describe /etc/makedev.d/* format
  o add makedev(8) : explain what is makedev

* Fri Sep 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.3.1-10mdk
- add lirc device

* Thu Aug 29 2002 Pixel <pixel@mandrakesoft.com> 3.3.1-9mdk
- special case for /dev/null is nice to have even when installing

* Wed Aug 28 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.3.1-8mdk
- add sheep_net, mga_vid and radeon_vid
- add missing mandrake to /etc/makedev.d

* Mon Aug 26 2002 Pixel <pixel@mandrakesoft.com> 3.3.1-7mdk
- hum, dispatch the various cases between %%post and %%triggerpostun

* Mon Aug 26 2002 Pixel <pixel@mandrakesoft.com> 3.3.1-6mdk
- %%post is too soon for calling mdk_makedev, move it to %%triggerpostun

* Tue Aug 20 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.3.1-5mdk
- remove debugging print

* Tue Aug 20 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.3.1-4mdk
- add a special case for /dev/null since there's a race window when
  updating from <3.3.1-1mdk

* Mon Aug 19 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.3.1-3mdk
- requires: perl-base (for mdk_makedev)
- clean scripts:
	o merge %%pre and %%post
	o dev %%post: /dev/{pts,shm}'re managed by drakx
	o MAKEDEV is in %%{_sbindir}, link in dev and not the reverse
- add back kernel-2.2.x support (aka devfs isn't mounted)
- enforce pts,shm location

* Mon Aug 19 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.3.1-2mdk
- add missing mkdir

* Mon Aug 19 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.3.1-1mdk
- add audio group
- source 1 : mdk_makedev: new perl script from pixel patched to work
  in this context; this script does the MAKEDEV job (aka creating the
  whole /dev entries, not the MAKEDEV /dev/hda job).
  how a wonderful 69 lines perl script takes 9 seconds to do what the
  911 lines C programm did in several minutes :-)
  see README for further informations
- patch 0: comment all uneeded entries which are useless to parse
  (pixel/me)
- patch 1: alter ida/ccis/dac960/ataraid generators so that they
  build tables faster to parse and interpret
- kill mkdev(), makedev()
- add new entries:
	o cfs device (coda)
	o kpoll
	o scramdisk
	o tunnelling (/dev/net/tun)
	o video1394 (for libraw1394)
	o sr devices (scd ones're still there though)
	o cpu/*/{msr,cpuid,microcode} (perms 0600)
	o various char devices: nvram, intel_rng
	o increase v4l and i2c entries number from 4 to 8 (vtx, vbi,
	  radio, video, i2c)
	o 4 dri/cards
	o watchdogs
	o mwave ACP Modem
	o firewire (raw1394, video1394)
- replace core link on /proc/kcore by a device
- from now, we can do easy updates, wheter devfs is mountaed or not
  problem is: live update from <3.3-1mdk will fail on old package removal
  which need 'rpm -e --justdb --noscripts dev'
- resync with rh-3.3.1-1
- set the /dev/vcs* devices to be owned by the vcsa user, and create the
  vcsa user
- Prereq: groupadd, useradd, sed, textutils, fileutils, mktemp
- clean scripts
- fix "unable to install while devfs is mounted" by creating dynamically
  the devices in %%post
- requires MAKEDEV for the above
- s/dac960/rd/
- MAKEDEV: take ownership on /etc/makedev.d

* Thu Mar 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.2-4mdk
- add %%doc devices.txt
- rpmlint fixes
- resync with rh

* Thu Aug 30 2001 Pixel <pixel@mandrakesoft.com> 3.2-3mdk
- move MAKEDEV to /sbin (symlink kept for compatibility)

* Tue Aug  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.2-2mdk
- Rebuild as root or rpm screwd up.
- Fix file lists.

* Mon Aug  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.2-1mdk
- Add hiddev.
- 3.2.

* Mon Jun 25 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.1-1mdk
- 3.1.1 (big upgrade may screw up thing).

* Mon Apr 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 3.0.6-10mdk
- call pam_console_apply in %%post to restore the owner of the devices
after an upgrade.

* Sat Apr 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.6-9mdk
- Add nvidia.

* Thu Mar  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.6-8mdk
- For ppc create adb devices (stew).

* Tue Mar  6 2001 Pixel <pixel@mandrakesoft.com> 3.0.6-7mdk
- fix for /dev/rd/c*d*p8 which doesn't exist
- add cciss

* Thu Feb 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.6-6mdk
- add sheep_net entry.

* Wed Jan 17 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.6-5mdk
- Add shm directorie.
- Add more generated device.
- Upgrade to -8 release of rh.

* Tue Nov 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.6-4mdk
- Put config files as noreplace.

* Wed Nov 15 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.6-3mdk
- Add toshiba devices.
- Upgrade to -7 release of rh.

* Wed Sep 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.6-2mdk
- Make pg* as cdwriter group (thanks till).

* Wed Aug 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.6-1mdk
- add an rm -f $TMP in %%post (pixel).
- Correct alsa link.
- Merge with RH 3.0.6

* Mon Jul 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.2-5mdk
- Correct usbmouse link to input/mouse0.

* Wed Jul 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.2-4mdk
- Create ppp devices.

* Tue Jul 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.2-3mdk
- Don't remove isdnctl (remove it from the isdn package instead).
- Correct micrcode in the right way (titi sucks).

* Tue Jul 25 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.2-2mdk
- remove RH microcode entry and reput the entires i add to dev before
  lord chmoue destroy it : cpu/{mircrocode,?/{cpuid,msr} for 2cpuid,msr} for
  2.4.x
- remove also conflicting /dev/isdnctrl

* Mon Jul 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.2-1mdk
- Mandrake adaptation of the new dev system.
- Merge dev system of Red Hat.
- Merge MAKEDEV and dev package.
