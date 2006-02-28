#
# spec file for package devfsd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		devfsd
%define version		1.3.25
%define release		%_revrel
%define rname		devfsd

%define state_dir	/lib/dev-state
%define build_static	0

%if %{build_static}
# $Id$

%define revision	$Rev$
%define name		devfsd-static
%endif

Summary:	Daemon for providing old entries in /dev with devfs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.atnf.csiro.au/~rgooch/linux/docs/devfs.html
Source:		ftp://ftp.atnf.csiro.au/pub/people/rgooch/linux/daemons/devfsd/%{rname}-v%{version}.tar.bz2
Source1:	devfs_fs.h
Source2:	devfs_fs_kernel.h
Source3:	%{rname}
Source4:	devfs-add-mouse-entry
#
# Compatibility names
#
# old /dev/cdrom
Patch0:		devfsd-1.3.25-cdrom.patch
# add back tun handling
Patch1:		devfsd-1.3.25-tun.patch
# Compacq smart array support
Patch2:		devfsd-1.3.25-ida.patch
# Compacq smart array support
Patch3:		devfsd-1.3.25-cciss.patch
# Mylex support
Patch4:		devfsd-1.3.25-rd.patch
# Support ide devices while using IDE-SCSI
Patch6:		devfsd-1.3.25-idescsi.patch
# Support scd devices as well as sd ones
Patch7:		devfsd-1.3.25-sr_to_scd.patch
# USB serial driver
Patch8:		devfsd-1.3.25-usb-serial.patch
# add back /dev/hd* handling
Patch9:		devfsd-1.3.25-hd.patch
#
# Compilation
#
# Fix compilation with glibc-2.2.x 's libnsl
Patch10:	devfsd-1.3.25-glibc22.patch
#
# Devices support
#
# enable defaults that're disabled
Patch20:	devfsd-1.3.25-enable.patch
# disable alsa support
Patch21:	devfsd-1.3.25-disable-alsa.patch
# nvidia driver
Patch22:	devfsd-1.3.25-nvidia.patch
# fix usb mice support: input/mouse0 and input/mice race for usbmouse link
# what's more, mice multiplex mouse0 and wacom tablets
Patch23:	devfsd-1.3.25-usbmouse.patch
# DVB (tv through satelite) driver
Patch24:	devfsd-1.3.25-dvb.patch
# prevent minilogd/initlog deadlock because of /dev/log
Patch25:	devfsd-1.3.25-log-fix.patch
# IPMI support
Patch26:	devfsd-1.3.25-ipmi.patch
#
# Add support for /etc/devfs/conf.d/
#
# include conf.d directory
Patch31:	devfsd-1.3.25-conf_d.patch
# only read .conf files
Patch32: 	devfsd-1.3.24-conf-files.patch
#
# Add support for /etc/devfs/conf.d/
#
# prevent lsb warnings
Patch50:	devfsd-1.3.25-lsb_vs_ptsfs.patch
#
# run-time kernel 2.5 detection
Patch100:	devfsd-1.3.25-kernel-2.5.patch
Patch101:	devfsd-1.3.25-pts.patch

BuildRoot:	%{_buildroot}/%{rname}-%{version}

Exclusiveos:	Linux
Requires:	initscripts >= 6.40.2-21mdk, pam
Requires:	modutils >= 2.4.13-3mdk
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Prefix:		/


%description
The devfsd programme is a daemon, run by the system boot
scripts which can provide for intelligent management of
device entries in the Device Filesystem (devfs).

As part of its setup phase devfsd creates certain symbolic
links which are compiled into the code. These links are
required by /usr/src/linux/Documentation/devices.txt. This
behaviour may change in future revisions.

devfsd will read the special control file .devfsd in a
mounted devfs, listening for the creation and removal of
device entries (this is termed a change operation). For
each change operation, devfsd can take many actions. The
daemon will normally run itself in the background and send
messages to syslog.

The opening of the syslog service is automatically delayed
until /dev/log is created.

At startup, before switching to daemon mode, devfsd will
scan the mounted device tree and will generate synthetic
REGISTER events for each leaf node.


%prep
%setup -q -n %{rname}
# Compatibility names
%patch0 -p1 -b .cdrom
%patch1 -p1 -b .tun
%patch2 -p1 -b .ida
%patch3 -p1 -b .cciss
%patch4 -p1 -b .rd
%patch6 -p1 -b .idescsi
%patch7 -p1 -b .scd
%patch8 -p1 -b .usb_serial
%patch9 -p1 -b .hd

# Compilation
%patch10 -p1 -b .glibc22

# Devices support
%patch20 -p1 -b .enable
%patch21 -p1 -b .alsa
%patch22 -p1 -b .nv
%patch23 -p1 -b .usb
%patch24 -p1 -b .dvb
%patch25 -p1 -b .log
%patch26 -p0 -b .log

# Add support for /etc/devfs/conf.d/
%patch31 -p1 -b .conf_d
%patch32 -p1 -b .conf_files

# kernel 2.5
%patch100 -p1 -b .kernel25
%patch101 -p1 -b .slowps

%patch50 -p1 -b .lsb_vs_pts

# Make devfsd.conf lib64 aware, notably of pam modules location
perl -pi -e "s|/lib(/security)|/%{_lib}\1|g" devfsd.conf


%build
%serverbuild
%if %{build_static}
make all CEXTRAS="-pg -fpic -static -I."
%else
make all CEXTRAS="-pg -fpic -I."
%endif


%install
export DONT_STRIP=1
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/{sbin,%{_sysconfdir},/%{_mandir}/man{5,8},etc,%{state_dir}}
install -m 0755 -s devfsd %{buildroot}/sbin/devfsd
install -m 0644 devfsd.8 %{buildroot}/%{_mandir}/man8
install -m 0644 devfsd.conf.5 %{buildroot}/%{_mandir}/man5
install -m 0644 devfsd.conf %{buildroot}%{_sysconfdir}
install -m 0644 modules.devfs %{buildroot}%{_sysconfdir}
# service and mouse entry script
mkdir -p  %{buildroot}{%_initrddir,/etc/devfs/conf.d} || :
install -m 0755 %SOURCE3 %{buildroot}%_initrddir/%{rname}
install -m 0755 %SOURCE4 %{buildroot}/sbin/devfs-add-mouse-entry


%pre
[ -d /var/dev-state/ -a ! -e %{state_dir} ] && /bin/mv /var/dev-state %{state_dir}
[ -d /var/lib/dev-state/ -a ! -e %{state_dir} ] && /bin/mv /var/lib/dev-state %{state_dir} || :


%post
%_post_service %{rname}

# prevent minilogd/initlog deadlock because of /dev/log:
rm -f %{state_dir}/log

[[ "$1" -gt 1 ]] && exit 0
[ -f /etc/sysconfig/mouse -a ! -e /etc/devfs/conf.d/mouse.conf ] || exit 0
/sbin/devfs-add-mouse-entry


%preun
if [ "$1" = 0 ]; then
    for i in /etc/lilo.conf /boot/grub/menu.lst; do
        [[ -e $i ]] && perl -pi -e 's/(\s*)devfs=mount(\s*)/$1 || $2/e' $i
    done
  
    [[ $(/usr/sbin/detectloader -q) = "LILO" ]] && /sbin/lilo > /dev/null
fi
%_preun_service %{rname}
:


%postun
if [[ "$1" = 0 ]]; then
    killall -TERM devfsd 2>/dev/null || :
fi


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/man8/devfsd.8*
%{_mandir}/man5/devfsd.conf.5*
%dir /etc/devfs/
%dir /etc/devfs/conf.d/
/sbin/devfsd
/sbin/devfs-add-mouse-entry
%dir %{state_dir}
%config(noreplace) %{_sysconfdir}/devfsd.conf
%config(noreplace) %{_sysconfdir}/modules.devfs
%config(noreplace) %_initrddir/%{rname}


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25-41avx
- P7: fix missing srX links
- P26: IPMI support

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25-40avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25-39avx
- rebuild

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25-38avx
- Annvix build

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> 1.3.25-37sls
- OpenSLS build (necessary evil)
- Remove Requirement: dynamic
- new macro %%build_static to allow us to make devfsd static for installer

* Fri Feb 27 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-36mdk
- fix error on uninstalling (#8265)

* Thu Jan 22 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-35mdk
- patch 1 : fix tun support

* Tue Jan 13 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-34mdk
- patch 101: fix spurious lookups on pts devices (the usual suspect:
  Andrey Borzenkov)

* Wed Jan  7 2004 Andrey Borzenkov <arvidjaar@mail.ru> 1.3.25-33mdk
- update patch100 - pass "-q" to modprobe. It prevents flooding syslog
  with errors on 2.6 and should not change anything on 2.4 (exit code
  of modprobe was never checked)

* Thu Aug  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.25-32mdk
- Remerge from amd64-branch:
  - Make devfsd.conf lib64 aware, notably of pam modules location

* Wed Jul 09 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-31mdk
- fix hang on bootstrapping by really remove log copy entry after installation
  (and not when package is definitively removed)

* Tue Jul 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-30mdk
- patch 100: run-time kernel 2.5 detection for MODLOAD action (Andrey Borzenkov)
  (replace source 5 and patch 40)
- init script: only delete files created by dynamic on desktop

* Tue Jul 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-29mdk
- really package /sbin/devfsd-try-modload

* Mon May 19 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-28mdk
- source 5: introduce devfsd-try-modload (wrapper because of devfsd
  braindamage)
- patch 40: devfsd.conf (use newly added wrapper instead of builtin MODLOAD in
  order to better support kernels 2.5.x)
- patch 50: remove 4 of 5 lsb tests faillures (stew)

* Wed Apr 30 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-27mdk
- patch 25: prevent minilogd/initlog deadlock because of /dev/log (andrey)
- patch 9: rediff and really apply

* Thu Apr 24 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-26mdk
- patch 4: fix rd/discX links

* Thu Apr 10 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-25mdk
- source 3 : fix #3259

* Tue Apr 08 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-24mdk
- patch 9 : add back /dev/hd* handling (Andrey Borzenkov)
  (side effect is that root can access IDE cdrom when logging in on the console
  immediately after startup (whereas pam_console_appy triggered ide-cd loading
  for normal users

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-23mdk
- build release

* Wed Oct 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-22mdk
- patch 3 -> 4
- patch 3 : support cciss compatibility links

* Fri Oct 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-21mdk
- fix ida devices managment (aka spurious ida/)

* Tue Oct 08 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-20mdk
- init script : conditionally start devfsd if devfs is mountedr
  (Borzenkov Andrey)

* Wed Sep 18 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-19mdk
- devfsd service:
  o restart works (and really restart)
  o reload always works, not only the first time
  o list reload target in help
  o add a working stop target
  o rename s/start()/reload()/ since it better describe the function goal

* Thu Sep 12 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-18mdk
- service scrip: restart(): do a real restart instead of just signaling
  devfsd to reread its config files (ease mdk8.2 update)

* Tue Sep 03 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-17mdk
- remove patch11, useless once we use s/CFLAGS/CEXTRAS/
- patch29 -> 23
- patch24 : add support for dvb cards (juan)

* Thu Aug 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-16mdk
- kill obsolete patch1

* Mon Aug 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-15mdk
- patch22: add support for nvidia driver

* Wed Aug 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-14mdk
- "still cleaner" release
- no need to redifine _sysconfdir
- simplify patch 29 (usb mouse support); default to input/mice rather
  to usbmouse; this has a nice side effect, since mice multiplex usb
  mouse graphic tables, ...
- kill ppc usb mouse patch since it's obviously wrong and because
  of new patch29 behavior
- nls::yp_all() support:
	o kill patch13 (explicit linkage with libnsl)
	o [Patch 10] right fix is to use the same prototype as in
	  glibc-2.2.x::rpcsvc/ypclnt.h thus dynamic support is back
	o [Patch 11] fix "make CFLAGS=..." by splitting CFLAGS into CFLAGS
	  and CPPFLAGS so that we don't overwite "-DLIBNSL=..."
- various spec cleaning

* Wed Aug 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-13mdk
- move part of %%post to /sbin/devfs-add-mouse-entry
- Prereq: rpm-helper
- gq pixel's changelog

* Mon Aug 19 2002 Pixel <pixel@mandrakesoft.com> 1.3.25-12mdk
- fix the condition for doing the "fix on upgrade for doing what was done in
  rc.sysinit (the symlink /dev/mouse)"

* Sat Aug 17 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-11mdk
- "much more clean" release
- scripts simplifications
- split up the 10 patches in 14 small ones, thus enabling to:
	o see that USB serial device was include two times in compat_names table
	o cancel patches doing something reversed by another one
	o group all scd/sr related patches into one
- join them in 4 sections: Compatibility names, Compilation fixes,
  Devices support, and /etc/devfs/conf.d/ support
- shrink compacq smart array and mylex patches
- document all patches

* Sat Aug 17 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-10mdk
- patch2, %%post: kill devfsd warnings

* Sat Aug 17 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-9mdk
- patch9: fix usb mouse managment
- remove all dynamic stuff (dynamic'll put them in /etc/devfs/conf.d/)

* Fri Aug  9 2002 Pixel <pixel@mandrakesoft.com> 1.3.25-8mdk
- patch2: adding symlink radio -> radio0

* Mon Aug 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-7mdk
- own /etc/devfs/conf.d/ too

* Fri Aug  2 2002 Pixel <pixel@mandrakesoft.com> 1.3.25-6mdk
- oops, only create symlink /dev/mouse on the running system if devfs is mounted in /dev

* Fri Aug  2 2002 Pixel <pixel@mandrakesoft.com> 1.3.25-5mdk
- fix on upgrade for doing what was done in rc.sysinit (the symlink /dev/mouse)

* Tue May 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-4mdk
- fix serial devices on usb (eg Handspring Visor and co)
  [already merged upstream but not yet released]

* Wed Mar 27 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-3mdk
- be sure to use /lib/dev-state

* Tue Mar 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-2mdk
- use sr for autoloading stuff so that "new compatibility" names (i.e.
  /dev/sr/c0b0t6u0) that devfsd creates still autoload (obscure case)
- fix mylex problem
- drop patches part that get merged upstream:
	- Parrallel port devices handling
	- raw I/O driver managment
	- misc/agpgart handling

* Tue Mar 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-2mdk

* Tue Mar 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.25-1mdk
- new release
- ide-scsi patch from andrej that enable /dev/hd? even for ide-scsi devices
- scd fix from andrej
- fix agp loading (andrej) if one manually create devices or link in a
  devfsd mounted /dev

* Wed Mar 13 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-17mdk
- fix scsi cdroms
- fix rd

* Tue Mar 12 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-16mdk
- rollback pixel patch because of usb problem

* Mon Mar 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-15mdk
- fix pp devices handling via scsi emulation

* Thu Mar 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-14mdk
- Requires: modutils >= 2.4.13-3mdk for pixel hack
- fix pixel mess (above => preinstall)

* Wed Mar 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-13mdk
- fix ida

* Wed Mar 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-12mdk
- fix printers rules

* Wed Mar 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-11mdk
- fix printers permission (frederic l***** doesn't know how to write
  regexps or what means testing ?)

* Tue Mar 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-10mdk
- fix common probeall

* Mon Mar 04 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-9mdk
- fix /dev/pg managment

* Wed Feb 27 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-8mdk
- fix the ppc patch to use $devname

* Wed Feb 27 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.3.24-7mdk
- rework PPC usbmouse patch

* Tue Feb 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-6mdk
- move drakx directory for lord pixel

* Tue Feb 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-5mdk
- devfsd service: if no deamon to kill, don't output kill error message

* Tue Feb 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-4mdk
- only read .conf files when optionnaly including a directory

* Tue Feb 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-3mdk
- add rawctl link
- replace a symlink by a mksymlink

* Mon Feb 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-2mdk
- move the OPTIONAL_INCLUDE

* Mon Feb 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.24-1mdk
- set group to "tty" for the pseudo-tty devices so that mesg(1) can
  later be used to enable/disable talk requests and wall(1) messages.
- new release (bug fix)
- re-add pg aliases (was lost when merging with ppc changes)
- add /etc/devfsd/
- read/include all config files added to /etc/devfsd/

* Wed Feb 13 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.23-7mdk
- add pg aliases (pixel)
- requires recent enough initscripts (Andrej)

* Mon Feb 11 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.3.23-6mdk
- change usbmouse symlink for PPC to input/mice

* Fri Feb  8 2002 Warly <warly@mandrakesoft.com> 1.3.23-5mdk
- killall -HUP devfsd kill ALSO the initscripts, change that.

* Thu Feb 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.23-4mdk
- move rc.sysinit stuff related to running actions in a separate service

* Tue Feb 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.23-3mdk
- fix my stupid patch

* Tue Feb 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.23-2mdk
- disable richard gooch stuff for sound, uneeded (Borsenkow Andrej)
- enable amovible media 

* Mon Feb 04 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.23-1mdk
- new version
- enhancements from richard
- alias scd & sr
- irda stuff
- fix alsa

* Fri Jan 25 2002 Pixel <pixel@mandrakesoft.com> 1.3.22-3mdk
- remove devfs=mount from lilo and grub when removing devfsd

* Thu Jan 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.22-2mdk
- enhancements from richard gooch

* Thu Jan 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.22-1mdk
- restore RESTORE
- new release

* Tue Jan 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.21-3mdk
- reput back the /lib/dev-state managment that disappear while updating to
  1.3.21

* Wed Jan 16 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.3.21-2mdk
- add agpgart to modules.devfs

* Tue Jan 15 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.21-1mdk
- Add fixes from Andrej.
- 1.3.21.

* Fri Dec 14 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.20-1mdk
- new release
- merge my cdrom fix in conf patch

* Thu Oct 11 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.18-17mdk
- fix cdrom link (fergal)

* Sun Sep 23 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-16mdk
- fixed sound devices permissions by calling pam_console_apply for them.

* Fri Sep 21 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-15mdk
- fix names of printers devices.

* Thu Sep 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-14mdk
- make_symlink: remove unlink before symlink but no message when the symlink
fail when it's the good file that's already pointed.
- GLOBAL symlink is rerouted to make_symlink

* Thu Sep 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-13mdk
- comment call to part.script (too buggy)
- add the /dev/video symlink

* Wed Sep 19 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-12mdk
- symlink <==> ln -sf.
- devfsd.conf unlink on UNREGISTER not to create devices on next boot.

* Wed Sep 19 2001 Pixel <pixel@mandrakesoft.com> 1.3.18-11mdk
- make rd/discX/* (DAC960) works

* Sat Sep 15 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-10mdk
- fix devfsd.conf for part regexp and visor regexp.

* Thu Sep 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-9mdk
- launch part.script when a new partition is detected.

* Tue Sep 11 2001 Pixel <pixel@mandrakesoft.com> 1.3.18-8mdk
- nicer handling of in directories symlinks (function make_symlink)
- make ida/ and rd/ works (cpqarray, cciss and DAC960)
    [updated patch0]

* Sun Sep  9 2001 Pixel <pixel@mandrakesoft.com> 1.3.18-7mdk
- modules.devfs: replace scsi-hosts with scsi_hostadapter

* Sat Sep  8 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-6mdk
- don't mess up /lib/dev-state with REGISTER and UNREGISTER [updated patch2]

* Wed Sep  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-5mdk
- added compatibility for cpqarray and DAC960 devices (not tested) [updated patch0].
- remove /lib/dev-state entry on UNREGISTER (Andrej Borsenkow) [updated patch2].

* Tue Sep  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-4mdk
- added compatibility entry for Parallel port ATAPI generic devices (updated patch0).

* Tue Aug 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-3mdk
- changed sr => scd for compatibility symlinks (updated patch0).
- removed autoloading of bttv and autoload sound-slot-0 instead of sound.

* Tue Aug 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-2mdk
- reworked patch3 to handle DELETE events to clean /lib/dev-state entries.

* Fri Aug 24 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.18-1mdk
- 1.3.18

* Fri Aug 24 2001 Pixel <pixel@mandrakesoft.com> 1.3.17-4mdk
- shut up the killall

* Thu Aug 23 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.17-3mdk
- manage the usbmouse symlinks

* Wed Aug 22 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.17-2mdk
- removed call to pam_console_apply to speed up boot in the meantime.

* Tue Aug 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.17-1mdk
- Fix build.
- 1.3.17.

* Mon Aug 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.16-2mdk
- call pam_console_apply on device creation/removal.

* Thu Aug 16 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.16-1mdk
- new release

* Tue Aug 14 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.15-1mdk
- new release

* Wed Aug  8 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.12-3mdk
- use dynamic scripts

* Tue Aug 07 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.12-2mdk
- remove warning on ia64
- fake rpmlint

* Wed Aug  1 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.12-1mdk
- moved devices saving dir to /lib/dev-state to allow a separate /var partition.
- 1.3.12 (merged patches 3 and 5, updated source2)

* Wed Jul 11 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.11-4mdk
- typo fixes

* Tue Jul 10 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.11-3mdk
- use %%serverbuild
- nicely reload devfsd on update
- nicely stop it on uninstall
- move /var/dev-state to /var/lib/dev-state in order to be FHS complient
  [on update, move existing perms]
  add a macro for it
- add %%dir /var/lib/dev-state
- no more need to link /dev/video0 on /dev/video for xawtv
  (need to be tested with zapping)

* Tue Jun 19 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.11-2mdk
- minor spec fixes
- build release

* Tue Feb 06 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.11-1mdk
- new release
- remove glibc-2.2 hack as this release fix it

* Tue Jan 09 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.10-7mdk
- more ALSA stuff
- prevent devfsd to auto{save,load} permissions & ownerships
  on Unix98 ptys (/dev/pts)
- handle CD burners too

* Thu Jan 04 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.10-6mdk
- more stuff for videtext support
- comment my previous changes

* Thu Nov 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.10-5mdk
- enable devfs to save and restore /dev/ state in /var/dev-state
- document devfsd.conf to show how to force default permissions
  out of the kernel
- remove empty %%post

* Fri Nov 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.10-4mdk
- fix glibc22 compilation.

* Wed Jul 19 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.10-3mdk
- BM

* Mon Jul 17 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.10-2mdk
- fix from Stefan van der Eijk <s.vandereijk@chello.nl>
- make devfsd LM-update comliant (aka pixelization)


* Tue Jul 04 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.10-1mdk
- new release (argh ... why do he fix in a new release what i've just fixed
  !!! => suppres my previous patch as it is now in)
- let spec-helper compress man-page
- guillomization

* Tue Jul 04 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.9-2mdk
- automatically load modules when a process lookup a /dev entry (part1)
	(part2 is copying richard' aliases in /etc/conf.modules)
  

* Tue Jun 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.9-1mdk
- New release
- Add old cdrom entries (i'll remove those from /etc/rc.d/rc.sysinit which is
  eventually not their place)
- Use mandir macros for FHS compatibilty.
- Add URL

* Wed Apr 19 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.5-1mdk
- version 1.3.5
- ditch mdk fixes patch

* Tue Apr 18 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.4-1mdk
- version 1.3.4
- fix spec permissions

* Mon Apr 17 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.3-1mdk
- version 1.3.3
- new BuildRoot

* Thu Mar 30 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.31-2mdk
- fix a typo in the release number :-(
- compiled against 2.3.99pre4-1
- patches for DrakX had been submited and integrated. Patches for rc.sysinit
  are currently tested.

* Thu Mar 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.31-1mdk
- fist mandrake spec: use spechelper
- by default, we provide compatiblity entries in /dev
  (DiskDrake won't like /dev/ide/host0/bus0/target0/lun0/part1 instead of
  /dev/hda1 ...)
- fix bad code compilation
- add loading of sound module when /dev/{mixer,dsp,...} is lookuped

