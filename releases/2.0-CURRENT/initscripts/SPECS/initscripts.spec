#
# spec file for package initscripts
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		initscripts
%define version		8.34
%define release		%_revrel

Summary:	The inittab file and the /etc/init.d scripts
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		http://svn.annvix.org/cgi-bin/viewvc.cgi/initscripts/?root=tools
Source0:	initscripts-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	glib2-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	python

Requires:	mingetty
Requires:	sed
Requires:	mktemp
Requires:	e2fsprogs
Requires:	gettext-base
Requires:	procps
Requires:	modutils
Requires:	psmisc
Requires:	which
Requires:	setup
Requires:	iproute2
Requires:	iputils
Requires:	util-linux >= 2.10s
Requires:	mount >= 2.11l
Requires:	SysVinit
Requires:	bootloader-utils
Requires:	srv
Requires:	ethtool
Requires(pre):	runit >= 1.7.0
Requires(pre):	sed
Requires(pre):	mktemp
Requires(pre):	fileutils
Requires(pre):	grep
Requires(pre):	rpm-helper
Requires(post):	runit >= 1.7.0
Requires(post):	fileutils
Requires(post):	grep

%description
The initscripts package contains the basic system scripts used to boot
your Annvix system, change run levels, and shut the system down cleanly.
Initscripts also contains the scripts that activate and deactivate most
network interfaces.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

gzip -9 ChangeLog

%build
make
make -C annvix/ CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/etc
make ROOT=%{buildroot} SUPERUSER=`id -un` SUPERGROUP=`id -gn` mandir=%{_mandir} install 
mkdir -p %{buildroot}/var/run/netreport
chmod u=rwx,g=rwx,o=rx %{buildroot}/var/run/netreport

#MDK
make -C annvix/ install ROOT=%{buildroot} mandir=%{_mandir}

python annvix/gprintify.py `find %{buildroot}/etc/init.d -type f` `find %{buildroot}/sysconfig/network-scripts -type f`

touch %{buildroot}/var/log/btmp

%kill_lang %{name}
%find_lang %{name}

# remove S390 and isdn stuff
rm -f %{buildroot}/etc/sysconfig/init.s390 %{buildroot}/etc/sysconfig/network-scripts/{ifdown-ippp,ifup-ctc,ifup-escon,ifup-ippp,ifup-iucv,ifup-ipsec,ifdown-ipsec}

# we have our own copy of gprintify
export DONT_GPRINTIFY=1


%post
touch /var/log/wtmp
touch /var/log/btmp
touch /var/run/utmp
chown root:utmp /var/log/wtmp /var/run/utmp /var/log/btmp
chmod 0664 /var/log/wtmp /var/run/utmp
chmod 0600 /var/log/btmp

# handle serial installs semi gracefully
if [ $1 = 0 ]; then
    if [ "$TERM" = "vt100" ]; then
        tmpfile=`mktemp /etc/sysconfig/tmp.XXXXXX`
        sed -e '/BOOTUP=color/BOOTUP=serial/' /etc/sysconfig/init > $tmpfile
        mv -f $tmpfile /etc/sysconfig/init
    fi
fi


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %verify(not md5 mtime size) /etc/adjtime
%config(noreplace) /etc/initlog.conf
%config(noreplace) /etc/modules
/etc/rc.modules
%dir /etc/modprobe.preload.d
/etc/rwtab
%dir /etc/rwtab.d
%config(noreplace) /etc/sysctl.conf
%dir /etc/sysconfig
%config(noreplace) /etc/sysconfig/init
%config(noreplace) /etc/sysconfig/autofsck
%config(noreplace) /etc/sysconfig/i18n
%config(noreplace) /etc/sysconfig/readonly-root
%config(noreplace) /etc/sysconfig/networking/ifcfg-lo
%dir /etc/sysconfig/console
%dir /etc/sysconfig/console/consoletrans
%dir /etc/sysconfig/console/consolefonts
%dir /etc/sysconfig/modules
%dir /etc/sysconfig/networking
%dir /etc/sysconfig/networking/tmp
%dir /etc/sysconfig/networking/devices
%dir /etc/sysconfig/networking/profiles
%dir /etc/sysconfig/networking/profiles/default

%dir /etc/sysconfig/network-scripts
%dir /etc/sysconfig/network-scripts/ifup.d
%dir /etc/sysconfig/network-scripts/ifdown.d
/etc/sysconfig/network-scripts/ifdown
/etc/sysconfig/network-scripts/ifdown-post
/etc/sysconfig/network-scripts/ifup
%config(noreplace) /etc/sysconfig/network-scripts/network-functions
%config(noreplace) /etc/sysconfig/network-scripts/network-functions-ipv6
/etc/sysconfig/network-scripts/init.ipv6-global
%config(noreplace) /etc/sysconfig/network-scripts/ifcfg-lo
/etc/sysconfig/network-scripts/ifup-ipx
/etc/sysconfig/network-scripts/ifup-post
/etc/sysconfig/network-scripts/ifdown-ppp
/etc/sysconfig/network-scripts/ifdown-sl
/etc/sysconfig/network-scripts/ifup-ppp
/etc/sysconfig/network-scripts/ifup-sl
/etc/sysconfig/network-scripts/ifup-routes
/etc/sysconfig/network-scripts/ifup-plip
/etc/sysconfig/network-scripts/ifup-plusb
/etc/sysconfig/network-scripts/ifup-bnep
/etc/sysconfig/network-scripts/ifdown-bnep
/etc/sysconfig/network-scripts/ifup-eth
/etc/sysconfig/network-scripts/ifdown-eth
/etc/sysconfig/network-scripts/ifup-ipv6
/etc/sysconfig/network-scripts/ifdown-ipv6
/etc/sysconfig/network-scripts/ifup-sit
/etc/sysconfig/network-scripts/ifdown-sit
/etc/sysconfig/network-scripts/ifup-aliases
%dir /etc/sysconfig/network-scripts/hostname.d

%dir /etc/ppp
%dir /etc/ppp/ip-down.d
%dir /etc/ppp/ip-up.d
%dir /etc/ppp/peers
/etc/ppp/ip-up
/etc/ppp/ip-down
/etc/ppp/ip-up.ipv6to4
/etc/ppp/ip-down.ipv6to4
/etc/ppp/ipv6-up
/etc/ppp/ipv6-down

/etc/init.d/*

/etc/profile.d/10lang.sh
/etc/profile.d/10lang.csh
/etc/profile.d/inputrc.sh
/etc/profile.d/inputrc.csh
/etc/profile.d/tmpdir.sh
/etc/profile.d/tmpdir.csh

/bin/doexec
/bin/ipcalc
/bin/usleep
/sbin/consoletype
/sbin/fstab-decode
/sbin/genhostid
/sbin/getkey
/sbin/ifdown
/sbin/ifup
/sbin/initlog
%attr(0700,root,root) /sbin/netreport
/sbin/ppp-watch
/sbin/service
/sbin/setsysfont
/usr/bin/*
/usr/sbin/sys-unconfig
%attr(0700,root,root) /usr/sbin/usernetctl

%dir %attr(775,root,root) /var/run/netreport
/var/lib/stateless
%ghost %attr(0664,root,utmp) /var/log/wtmp
%ghost %attr(0600,root,utmp) /var/log/btmp
%ghost %attr(0664,root,utmp) /var/run/utmp

%{_mandir}/man*/*

%files doc
%defattr(-,root,root)
%doc sysconfig.txt sysvinitfiles ChangeLog.gz static-routes-ipv6 ipv6-tunnel.howto ipv6-6to4.howto


%changelog
* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.34
- 8.34
- remove scripts that are now being provided by runit
- remove requires on chkconfig
- requires recent runit which owns /etc/init.d

* Mon Oct 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.33
- remove requires on perl-MDK-Common
- remove some locale'd manpages

* Sat Sep 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.33
- fix URL

* Thu Jul 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.33
- r353:
  - comment out 2.4-related usb module loading; our 2.4 kernel has usb builtin
  - remove dm service support
  - remove prcsys and support for parallel init
  - remove udev stuff

* Tue Jul 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.33
- this is the first 100% Annvix-driven initscripts package, so this
  is a new tarball (8.33) that we'll backport and work with out of
  svn as this needs a *lot* of work
- 8.33 (sync with Mandriva 8.34-3mdv)
- lots of cleanups in the spec to remove old and useless stuff
- install a default sysconfig/i18n file defaulting to en_US
- use /etc instead of %%{_sysconfdir}; this package is *never* relocatable
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.61.1
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.61.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.61.1-5avx
- rebuild against new glib2.0

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.61.1-4avx
- mark /etc/rc.d/rc.local and /etc/rc.local as %%config(noreplace)
- compress the ChangeLog
- remove the X11 config files
- /sbin/netreport and /usr/sbin/usernetctl are not s*id anymore
- make tmpdir.sh not require an msec SECURE_* setting to use ~/tmp for
  TMP and TMPDIR
- rc.d/rc.sysinit: don't deal with anything sound-related
- rc.d/rc.sysinit: get rid of raidtools support; we've never shipped it
- rc.d/rc.sysinit: get rid of /.unconfigured support; this must come from
  DrakX
- rc.d/rc.sysinit: clean up some GUI stuff we don't need
- rc.d/rc.sysinit: clean up some GUI/ICE-related stuff in /tmp
- rc.d/rc.sysinit: remove more SELINUX bits
- remove /etc/sysconfig/network-scripts/ifup-wireless
- sysconfig/network-scripts/{ifup,network-functions}: remove wireless bits
- sync with mandriva 7.61.1-47mdk
  - ifup: don't try to rename device according to HWADDR if no device
    exists, or else ifup will loop endlessly and block boot
  - tmpdir.sh (Frederic Lepied): bourne shell compatible fix
  - adapt inputrc.csh to new tcsh (bugzilla #17999)
  - do not keep initrd's /dev (thus fixing cciss support)
  - rc.sysinit, netfs: added suport for shfs (bug #15964)
  - halt: fixed random-seed file name (bug #15889).
  - don't delete route for interfaces related to an alias interface
    being shut down
  - skip metric setting for alias interface
  - translation updates
  - netfs: fixed NFS shares are not mounted at boot (bug #16531).
  - rc.d/init.d/network: fix net-pf-10 alias being rewritten at each
    boot (#16045) (Olivier Blin)
  - network-functions, ifup: fixed ethtool path
  - sysconfig/network-scripts/ifup: DVB support (Olivier Blin).
  - rc.d/rc.sysinit: fix syntax error when nousb is used on the
    command line (David Faure).
  - do not write empty net-pf-10 aliases
  - rc.sysinit: check that /usr/bin/consolechars is available before 
    calling setsysfonts (bug #11054)
  - rc.d/init.d/network: fix duplicate addition of aliases in modprobe.conf
    and correct a potential bug when NETWORKING_IPV6 is not set (blino)
  - netfs, network: fixed nfs unmounting (Oden, bug #13677)
  - rc.sysinit: o don't enable process accounting here (bug #13672).
                o removed duplicated code for setting hdparm options (bug #13677).
  - setsysfont, rc.d/rc.sysinit, rc.d/init.d/functions: added a
    get_locale_encoding function to rc.d/init.d/functions so that
    detection of locale encoding from init scripts is easier;
    simplified the font loading. rewrite setsysfont script to better
    detect the locale, and to look first at /etc/sysconfig/console in
    all cases. (Pablo)
  - rc.d/init.d/network: handle net-pf-10 alias for respecting
    NETWORKING_IPV6 (Warly, bug #11896).
  - do not try to restart the no more existing random service (Thierry, #13426)

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.61.1-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.61.1-2avx
- bootstrap build

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.61.1-1avx
- rediff our patch
- drop SELinux stuff
- try to cleanup some USB stuff since we compile USB HID/keyboard/mouse
  support directly into our kernel
- cleanup some devfsd and udev junk
- sync with mandrake 7.61-22mdk:
  - (too much to note, so note the important stuff; all flepied unless
    otherwise noted):
  - rc.d/init.d/halt: remove sleep and exit in case of powerfail (apcupsd)
  - rc.sysinit fixes from Luca Bera:
    - rework creation of device mapper control node so we don't depend on nash
    - mdadm is preferred over raidtools now, and empty config files are ignored
    - correctly activate lvm after raid
    - mount other filesystems once, not twice
  - modprobe ide-cd and scsi_hostadapter
  - set TMP and TMPDIR to /tmp to have the same behaviour during and after boot
  - don't try to mount /dev/pts twice
  - rc.sysinit: modprobe scsi_hostadapter earleir to be able to use lvm on a
    second scsi controller
  - rc.sysinit: fix init of /dev/tty[1-8]
  - rc.sysinit: fix mount of /dev/pts and /dev/shm
  - rc.sysinit: avoid activating encrypted swap partitions directly handled by swapon.
    work with static crypto modules, keep the swap signature (4096 firs bytes) when
    mounting an encrypted swap
  - rc.sysinit: don't apply hdparm on software RAID arrays that are in process of
    background resyncing
  - don't mark initscripts as config files anymore

* Tue Jul 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.06-41avx
- rediffed P2: call supervise directly from init
- Requires: srv

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.06-40avx
- patch naming convention policy
- don't clear tty1 so we can see what happens

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.06-39avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 7.06-38sls
- all Requires/PreReq require packages, not files
- s/fileutils/coreutils/
- clean all the obsoletes/provides/requires/etc.

* Tue Jun  1 2004 Vincent Danen <vdanen@opensls.org> 7.06-37sls
- I never did like OK/PASSED/FAILED/etc. in all caps so change that
- change some colors
- on bootup have it say "[ver]-[tag]" rather than just "[ver]"
- get rid of some msec stuff in rc.local
- make initscripts own /etc/sysconfig/system to control issue rewrite's
  and such since the mdk installer seems to make this file

* Tue May 11 2004 Vincent Danen <vdanen@opensls.org> 7.06-36sls
- add /var/log/btmp by default
- rediff P2
- sync with cooker 7.06-49mdk (only pertinent entries noted):
  - network service: check actual value of MII_NOT_SUPPORTED instead of only
    testing if the variable exists (tvignaud)
  - add Han Boetes patch to set font on every text console, not only the
    first one (tvignaud)
  - rc.sysinit: added support for mdadm and lvm2 (bluca)
  - rc.sysinit: fixed loading of st module (bluca)
  - rc.local: option not to muck with /etc/issue (this is needed for sites
    where policy, or law, enforce use of banners before login) (bluca)
  - init.d/network: reload restarts active interfaces, restarts set boot
    behaviour (bug #6112) (bluca)
  - init.d/functions: fix print of multiple pid in status() (bug #6334)
    (bluca)
  - halt: added support for lvm2 (found by Navindra Umanee) (flepied)
  - fix /sbin/setsysfont to work only on current console (Andrey Borzenkov)
    (flepied)
  - fix /sbin/setsysfont regarding compressed fonts (Luca Berra) (flepied)
  - use fixed /sbin/setsysfont in rc (bug #6185) (Andrey Borzenkov)
    (flepied)
  - rc.d/rc.sysinit: no more depmod at boot (Nicolas) (flepied)
  - move proc mounting after font initialization (warly)
  - do not lock cdrom drive when mounted (warly)
  - mandrake/usb: mount /proc/bus/usb as usbdevfs for all kernel 2.4/2.6
    needed by speedtouch alcatel modem in user-mode/kernel-mode (Nicolas)
    (flepied)
  - rc.d/rc.sysinit: lookup device-mapper in /proc/misc too (bug #8398)
    (flepied)
  - call upsd earlier in halt script (warly)
- NOTE: this package needs some serious cleaning and should likely be fully
  branched away from the Mandrake patch (so a single OpenSLS-specific patch)

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 7.06-35sls
- remove supermount
- minor spec cleanups
- remove ifplugd requirement
- more OpenSLS branding
- s/mandrake_{everytime,firstime,consmap}/opensls_{everytime,firstime,consmap}/

* Tue Jan 27 2004 Vincent Danen <vdanen@opensls.org> 7.06-34sls
- remove P1 (supervise functions)
- remove dm, alsa, sound, partmon initscripts

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 7.06-33.1sls
- more OpenSLS branding
- tidy spec somewhat

* Fri Nov 07 2003 Vincent Danen <vdanen@opensls.org> 7.06-33sls
- patch functions to support supervise

* Wed Sep 24 2003 Warly <warly@mandrakesoft.com> 7.06-32mdk
- fix stupid error in setsysfont

* Mon Sep 22 2003 Warly <warly@mandrakesoft.com> 7.06-31mdk
- fix countdown for fsck in rc.sysinit

* Mon Sep 22 2003 Warly <warly@mandrakesoft.com> 7.06-30mdk
- add rc_splash verbose for fsck

* Mon Sep 22 2003 Warly <warly@mandrakesoft.com> 7.06-29mdk
- uniformize path between rc.sysinit and setsysfonts (use console/consoletrans 
  and console/consolefonts)
- initsripts owns console/consoletrans and console/consoletools
  
* Mon Sep 22 2003 Warly <warly@mandrakesoft.com> 7.06-28mdk
- rc.sysinit check also for uncompressed fonts for SYSFONT

* Thu Sep 18 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-27mdk
- rc.sysinit: fix fsck -y by removing -a option (Pixel)
- rc: fix reboot/halt problem in utf8 mode (bug #3020)
- po updates (Pablo)
- fr po fix (Thierry) (bug #5675)
- rc.sysinit: output translated messages in getkey (bug #5189)
- fix #3739: use alsactl to restore alsa specific mixer elements since
  alsa service won't do it if sound service is enabled (and thus has
  already load the sound module) (Thierry)
- support for non compressed fonts, as consolechars doesn't support
  them currently (Pablo)

* Thu Sep 11 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 7.06-26mdk
- rc.sysinit: remove scrollkeeper temp files at startup

* Wed Sep 10 2003 Warly <warly@mandrakesoft.com> 7.06-25mdk
- move initsplash to have progress bar update in rc.sysnit

* Fri Sep 05 2003 Warly <warly@mandrakesoft.com> 7.06-24mdk
- rc.sysinit: add rc_spalsh "name" value to have progress bar updated.
- rc: replace /dev/vc1 or /dev/tty1 by /dev/console
- rc.d/functions: replace splash by rc_splash, fix splash command call

* Thu Sep  4 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 7.06-23mdk
- mandrake_firstime, sound/sound.init: move alsa unmute code from
mandrakefirst time to sound service.  rationale: mandrake first time
is called way too early, before the sound module is loaded. so the
proper place really is while initialization sound.  now oss & alsa are
defaulted to the same place.  oss default to 80% and alsa to 66%.


* Thu Sep  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-22mdk
- don't remove the symlinks in /etc otherwise the upgrade will fail
- avoid the infamous TMOUT error
- use LC_ALL instead of LANG for gprintf (Pablo)

* Tue Sep  2 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-21mdk
- set TMPDIR to ~/tmp for the security levels >= 2 (bug #2337)
- launch dm at the end of the sequence in confirmation mode (bug #3164)
- removed kheader. It belongs to bootloader-utils now.
- run scripts in /etc/ppp/ip-up.d and /etc/ppp/ip-down.d in ip-up and ip-down (bug #4881)
- call ifup-post with the right device name (bug #3832)
- po updates (Pablo)

* Tue Aug 26 2003 Warly <warly@mandrakesoft.com> 7.06-20mdk
- switch to verbose mode in fsck and encrypted filesystem mount
- always redirect output to console 1
- do not do start bootsplash in rc when booting

* Sat Aug 23 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-19mdk
- requires bootloader-utils instead of kernel-utils
- po updates (Pablo)

* Mon Aug  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-18mdk
- fix bug #4491 (belle_eden)
- rc.modules: don't use head as /usr can be unmounted at this stage (Dirk O. Siebnich)
- fix bug #4230 with a modified version of Ben Reser's patch.
- head -1 => head -n 1
- fixed i18n

* Mon Aug  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-17mdk
- split loader into kernel-utils package.

Integrated Andrey Borzenkov's fixes (forgotten in 15mdk):

- workaround for boot hanging on "finding module dependencies".
  Due to wrong devfsd config /dev/log timestamp has been updated which
  resulted in minilogd attempting to exit and flush buffers. It tried to
  connect to itself and hung if too many connection requests were pending.
  The patch sets connection timeout to 30 seconds (it was 2**31-1 before).
- kernel 2.5 support including:
  + mount sysfs on /sys 
  + handle both usbdevfs and usbfs in rc.sysinit
  + use modprobe -c | grep  instead of gre[ /etc/modules.conf everywhere
- use /etc/modprobe.preload instead of /etc/modules on 2.5.
  Suggested by David Walser (name mine :)

* Fri Aug 01 2003 Warly <warly@mandrakesoft.com> 7.06-16mdk
- pass LANG to splash to be able to i18n the boot message

* Thu Jul 31 2003 Warly <warly@mandrakesoft.com> 7.06-15mdk
- new bootsplash changes (need some more tweaks, but enough to have some tests)

* Fri Jul 11 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-14mdk
- mandrake_everytime: corrected hotplug restoring (Andrey Borzenkov)
                      use modprobe -c instead of modules.conf (Andrey Borzenkov)
- rc.d/rc.sysinit: check 2.2 kernel correctly (Andrey Borzenkov)
- po/pt_BR.po: updated po file (Pablo)
- rc.d/init.d/functions: use LC_MESSAGE instead of LANGUAGE for gettext use

* Mon May 26 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-13mdk
- call the netprofile service from mandrake_everytime service to be able
to switch services before running /etc/rc.d/rc
- allow minilogd to open /dev/log as a STREAM (Andrey Borzenkov)
- when fsck return 2 or 3, reboot without asking question.
- updated po files for de and fi (Pablo)
- sp.po, sr.po, sr@Latn.po: renamed Serbian files (Pablo)
- Added	Finnish man pages (Pablo)
- fix detectloader behavior on non-lilo systems (Ben Reser)

* Wed Apr 23 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-12mdk
- fix minilog race condition (Andrey Borzenkov)

* Wed Mar 12 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-11mdk
- po updates
- don't add a zeroconf route (bug #2265)

* Tue Mar 11 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-10mdk
- po updates
- fix for non localized consoles (Pablo)

* Wed Mar  5 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-9mdk
- po updates
- prefdm: don't write to sysconfig/desktop

* Wed Feb 26 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-8mdk
- corrected BuildRequires (Stefan)
- po updates
- rc.d/rc.sysinit: fix of the long standing "unicode doesn't
 display correctly at boot time" bug (Pablo)

* Mon Feb 24 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-7mdk
- change owner of /tmp/.ICE-unix to root at boot time (bug #1280)
- po updates

* Tue Feb 18 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-5mdk
- po updates
- don't start ifplugd for non eth interfaces (bug #1717)

* Fri Feb 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-4mdk
- po updates

* Mon Feb 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-3mdk
- wait for ifplugd completion in network service
- add IFPLUGD_ARGS variable in sysconfig/network
to be able to change args passed to ifplugd
- mandrake/mandrake_consmap: Make launch of unicode_start only if
the console isn't yet in unicode mode (to avoid the "Already in
UTF8 mode" messages that are perturbing for some users) (Pablo)
- po updates

* Sat Feb  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-2mdk
- corrected network script to not bug on alias range (bug #1134)

* Sat Feb  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.06-1mdk
- 7.06

* Mon Feb  3 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 7.04-3mdk
- mandrake/loader/rebootin: Add list option (needed for new kdm).

* Mon Feb  3 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.04-2mdk
- mandrake/loader/common.pm: Support of latest kernel naming scheme (Chmouel)
- po updates (Pablo)
- typo fixes (bug #1206)
- prefdm: support mdkkdm
- rc.sysinit: don't display an error when /usr isn't mounted at the beginning of
the boot sequence (bug #1214)

* Wed Jan 29 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.04-1mdk
- merged rh 7.04
- Added Ukrainian man pages (Pablo)

* Mon Jan 20 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.02-3mdk
- handle correctly the return code of ifstatus
- updated fi locale (Pablo)

* Sat Jan 18 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.02-2mdk
- added /etc/sysconfig/network-scripts/{ifup,ifdown}.d to store scripts
- corrected MII_NOT_SUPPORTED management in network-functions
- ifup: always create a zeroconf IP address on dynamic config

* Tue Jan 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 7.02-1mdk
- use ifplugd
- merged 7.02

* Mon Dec 30 2002 Warly <warly@mandrakesoft.com> 6.91-19mdk
- fix ipv6 sit device functions
- network: don't call sysctl twice (bug #514) (flepied)
- halt: corrected HALTARGS handling (bug #633) (flepied)
- add detectloader to all the file lists (no more %%ifnarch).

* Tue Dec 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.91-18mdk
- exclude service dm & harddrake from restarting on glibc update

* Tue Nov 19 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-17mdk
- use zcip if dhcp client failed to configure the network
- use dhclient as the prefered dhcp client
- configure dhclient with more possibilities used in ifcfg
- removed output from sysctl

* Mon Nov 18 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-16mdk
- revert change for wireless device up in ifup

* Thu Nov  7 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.91-15mdk
- requires s/fileutils/coreutils/

* Tue Nov  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-14mdk
- like ethernet, bring up wireless devices before checking
their state (Dirk O. Siebnich)

* Fri Oct 18 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-13mdk
- corrcted the detection of wireless link down

* Thu Oct 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.91-12mdk
- detectloader also works on x86-64, so ship it there too

* Mon Oct  7 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-11mdk
- init.ipv6-global: reverted to 1.1.1.1
- usb: don't try to detect the usb chipset.
- rc: source mandrake_consmap when shutting down or rebooting to be sure to
have the console in a correct state. (Andrey Borzenkov)
- mandrake_everytime: do the right thing(tm) regarding network interfaces.
- corrected Danish translation encoding (Pablo)
- po corrections: pl, sq, fi, lv, ru and sk.
- ifup: use MII_NOT_SUPPORTED to be able to avoid the check for link up and
try to detect wireless link down.

* Thu Sep 19 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-10mdk
- usb: don't use expr because /usr ins't always mounted at this point

* Wed Sep 18 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-9mdk
- corrected message in usb to have translations.

* Wed Sep 18 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-8mdk
- corrected usb startup

* Tue Sep 17 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-7mdk
- mandrake_firstime: remove the MNF update entries as this
is done otherwise (Florin)
- po updates (Pablo)

* Sat Sep 14 2002 Warly <warly@mandrakesoft.com> 6.91-6mdk
- switch to console 1 when rebooting/halting

* Thu Sep 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-5mdk
- rc.sysinit: corrected rootfs type detection
- po updates (Pablo)

* Tue Sep 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-4mdk
- po updates (Pablo)
- quiet=no to avoid dm crash

* Fri Sep  6 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-3mdk
- po updates (Pablo)

* Wed Sep  4 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-2mdk
- po updates (Pablo)
- mandrake_firstime is called from rc.sysinit
- gprintify network-scripts
- NUT client check in halt
- mandrake_firstime doesn't call makewhatis anymore
- usb: Fix usb module loading with probeall in modules.conf : Fix pb
of usb keyboard at startup (usefull on legacyfree machines) (Nicolas)

* Tue Aug 27 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.91-1mdk
- add hook for nut in halt script
- alsa, sound and partmon are started earlier in the boot sequence
- dm is stopped at level 09
- 10lang.{sh,csh} fixed to handle GDM_LANG
- po updates: hu, no

* Wed Aug 21 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.90-1mdk
- po update: bs, hu, mt, ar
- merged rh 6.90

* Fri Aug 16 2002 Stew Benedict <sbenedict@mandrakesoft.com> 6.88-4mdk
- rework installkernel to not complain about userbuilt mdkcustom
- kernels and trigger fan mail to Chmouel

* Wed Aug 14 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.88-3mdk
- cosmetic change in boot: colors and welcome message in boot splash mode.

* Wed Aug 14 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.88-2mdk
- po updates: af, el, id, tr, vi (Pablo).
- display manager is now a separate service called dm

* Sun Aug 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.88-1mdk
- 6.88
- po updates (Pablo and Stefan Siegel)

* Fri Aug 09 2002 Warly <warly@mandrakesoft.com> 6.87-3mdk
- update prefdm to use 10lang.sh instead of lang.sh

* Thu Aug 08 2002 Warly <warly@mandrakesoft.com> 6.87-2mdk
- renamed lang.sh and lang.csh 10lang.c?sh
- readd bootsplash in rc (broken by the redhat merge)
- replace check_down_link with J.A. Magallon version in network-functions

* Fri Aug  2 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.87-1mdk
- merge with rh 6.87

* Wed Jul 31 2002 Warly <warly@mandrakesoft.com> 6.40.2-46mdk
- add optional option for initrd (Oden Eriksson)
- remove aurora (Borsenkow Andrej)
- rc.sysinit: remove ugly/unneeded setting of symlink /dev/mouse (Pixel)

* Wed Jul 17 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 6.40.2-45mdk
- Fix path for Mozilla database rebuild script (fcrozat)
- mandrake/loader/grub: handle fstab devices using devfs names 
  (fix problem reported by Alexander Skwar)

* Wed May 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.40.2-44mdk
- alsa service:
	- support new alsa driver naming scheme
	- remove all sequencer connections if any
	- remove old 2.2 gameport
	- some tests simplifications
- andrej: ignore backup files in service
- alus: update polish translation

* Wed May  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.40.2-43mdk
- corrected bad gprintify

* Wed May  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 6.40.2-42mdk
- corrected encrypted swap activation (Michel Bouissou)

* Fri Mar 15 2002 Warly <warly@mandrakesoft.com> 6.40.2-41mdk
- add a noquiet parsing in /proc/cmdline to easily remove quiet mode

* Wed Mar 13 2002 Warly <warly@mandrakesoft.com> 6.40.2-40mdk
- safer to have press I in console 1

* Wed Mar 13 2002 Warly <warly@mandrakesoft.com> 6.40.2-39mdk
- some fsck case were still appearing in console 11

* Tue Mar 12 2002 Warly <warly@mandrakesoft.com> 6.40.2-38mdk
- fsck must appear in console 1
- remove interactive mode from console 1

* Mon Mar 11 2002 Warly <warly@mandrakesoft.com> 6.40.2-37mdk
- reput kudzu in non quiet mode
- only redirect stdin not stderr

* Fri Mar 08 2002 Warly <warly@mandrakesoft.com> 6.40.2-36mdk
- rc.d/rc.sysinit: do not echo proc mounting
- rc.d/rc.sysinit: do not echo welcome to Mandrake-Linux when quiet
- rc.d/rc: put a black progress bar at the end of boot when LOGO_CONSOLE is no
- rc.d/rc.sysinit: remove fsck from console 1 in quiet mode
- rc.d/init.d/functions: add quiet function
- rc.d/rc.sysinit: add text to signify booting/rebooting/halting
- rc.d/init.d/functions: also redirect stdrr
- rc.d/init.d/functions: set runlevel=5 in rc.sysinit for initsplash
- rc.d/init.d/halt: add quiet mode in halt

* Sun Mar 03 2002 Warly <warly@mandrakesoft.com> 6.40.2-35mdk
- devnullize locale copying pushd output

* Sat Mar 02 2002 Warly <warly@mandrakesoft.com> 6.40.2-34mdk
- fix typo in post for copying locale to /etc/
- remove chvt and exec 1> in rc that prevent / umounting
- copy $LANG and co locale to /etc to have first initscript message 
  i18ned even with a separate /usr
- increase encrypted password timeout to 15s

* Fri Mar 01 2002 Warly <warly@mandrakesoft.com> 6.40.2-33mdk
- let locale in /usr, gettext need /usr/share/locale anyway
- add progress bar in rc.sysinit
- add initsplash in functions

* Thu Feb 28 2002 Warly <warly@mandrakesoft.com> 6.40.2-32mdk
- place proc mounting after setfont not to break i18n

* Thu Feb 28 2002 Warly <warly@mandrakesoft.com> 6.40.2-31mdk
- new progress bar with number of services
- redisplay bootsplash when rebooting
- disable bootsplash in init 1
- clear the splash in rc not rc.local
- change QUIET to quiet not to conflict with bootsplash config one
- check if /dev/fb0 exist not to have error message in non framebuffer

* Tue Feb 26 2002 Pixel <pixel@mandrakesoft.com> 6.40.2-30mdk
- nicer output for rawdevices (still not nice in case of errors, but...)

* Tue Feb 26 2002 Warly <warly@mandrakesoft.com> 6.40.2-29mdk
- add progress bar
- make kudzu always appear on console 1

* Fri Feb 22 2002 Warly <warly@mandrakesoft.com> 6.40.2-28mdk
- first real quiet mode to use bootsplash

* Fri Feb 22 2002 Warly <warly@mandrakesoft.com> 6.40.2-27mdk
- update $out variable in quiet mode

* Fri Feb 22 2002 Warly <warly@mandrakesoft.com> 6.40.2-26mdk
- mandrake/mandrake_everytime: move the bootlogo disable to rc.local
- mandrake/rc.local: add disable boot logo
- rc.d/rc, rc.d/rc.sysinit, rc.d/init.d/functions: add quiet mode

* Mon Feb 18 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-25mdk
- mandrake/inputrc.csh: fix "Couldnt get a file descriptor..." when launching tcsh (Olivier Dormond)
- mandrake/mandrake_everytime: Move the bootlogo disable here.

* Sat Feb 16 2002 Pixel <pixel@mandrakesoft.com> 6.40.2-24mdk
- move swapon after vgchange so that swap on LVM works

* Fri Feb 15 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-23mdk
- sysconfig/network-scripts/ifup: really clear bad pid of dhcp.

* Thu Feb 14 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-22mdk
- mandrake/loader/detectloader: Return always aboot on alpha.
- sysconfig/network-scripts/ifup: Cleanup bad pid of dhcp before
  ifup.
- po/fr.po: updated French file (pablo).

* Wed Feb 13 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-21mdk
- rc.d/rc.sysinit: Improve harddisk optimations setting (see:
  http://marc.theaimsgroup.com/?l=mandrake-cooker&m=101327129014413&w
  =2) (andrej).
- rc.d/init.d/functions: fixes small output bug in init.d/functions
  (success and pass) (andrej).
- po/*: updates (titi/pablo).

* Tue Feb 12 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-20mdk
- mandrake/loader/common.pm: Don't add quiet to options when the
  bootsplash theme say no.
- mandrake/loader/installkernel.sysconfig: Bootsplash things are moved
  to his config files.
- rc.d/rc.sysinit: Fix path: /var/lock/console => /var/run/console (andrej).
- mandrake/kheader: Remove obsoletes config- System.map-* and do
  not recreate kernel.h every time (andrej)
- po/*: updates (pablo).
- rc.d/rc.sysinit: Add a stanza to allow ext3 partitions to mount
  as ext2 for kernel22 (stew).

* Fri Feb  8 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-19mdk
- rc.d/rc.sysinit: Remove some devfsd stuff that make minilogd
  crazy (titi/andrej).

* Wed Feb  6 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-18mdk
- rc.d/rc.sysinit: devfs fixes from Andrej.
- mandrake/loader/installkernel.sysconfig: Add option
  LOGO_CONSOLE=no Say yes here if you want to leave the logo on the
  console.
- rc.d/init.d/functions: fixed reference to doc directory (pablo).
- po/*: updates (pablo).
- lang.sh: Fixed sourcing of i18n files (the user specific must have
  priority, and if it exists the system wide one must not be
  sourced; otherwise we end up with mixed locale settings and
  umpredicatable behaviour) (pablo).

* Wed Jan 30 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-17mdk
- mandrake/loader/installkernel.sysconfig: Add option SPLASH= for boot
  splash image.
- rc.d/rc.sysinit: Mount virtual's fs as none (andrej).
- sysconfig.txt, sysconfig/network-scripts/ifup: Add NO_ARPING option
  to skip arping (andrej).
- po/*: po updates (pablo).
- mandrake/loader/detectloader: duplicate signatures for grub
  unecessary (gc).

* Thu Jan 24 2002 Pixel <pixel@mandrakesoft.com> 6.40.2-16mdk
- mandrake/loader/installkernel: detect the now-nice-magic of grub

* Tue Jan 22 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-15mdk
- mandrake/loader/installkernel: Remove the DURING_INSTALL check it
  breaks rpmdrake instead checking menu.lst, lilo.conf before
  generating.

* Thu Jan 17 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-14mdk
- mandrake/kheader: Fix remove_orphaned() (andrej).
- mandrake/loader/common.pm: Don't exist when kernel_version_of_entry
  don't follow initrd_version_of_entry just warning.
- rc.d/rc.sysinit: Make the Timeout of Crypto configurable via
  /etc/sysconfig/autofsck.
- mandrake/: Makefile, autofsck: Add autofsck default sysconfig.
- rc.d/rc.sysinit: If noauto in encrypted swap skip it also.

* Tue Jan 15 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-13mdk
- rc.d/rc.sysinit: Fix getkey to display seconds.
- rc.d/rc.sysinit: Add encrypted swap support.
- rc.d/rc.sysinit: Fix my removing :p

* Tue Jan 15 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-12mdk
- rc.d/: rc.sysinit, init.d/netfs: Add support for encrypted
  filesystems.

* Tue Jan 15 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-11mdk
- rc.d/rc.sysinit: Add andrej changes don't restore /lib/dev-state/
  from here and erase /var/lock/console* before pam_console_apply.

* Tue Jan 15 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-10mdk
- mandrake/kheader: Remove orphaned kernel.h-${version} when
  /boot/vmlinuz-${version} not here.
- mandrake/kheader: Force ln when linking.
- mandrake/partmon/partmon: chmou sucks and changed filename of
  backend ;p (gc).

* Tue Jan 15 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-9mdk
* initscripts.spec, mandrake/: Makefile, partmon/Makefile,
  partmon/partmon, partmon/partmon.pl: Add partition monitor from GC

* Mon Jan 14 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-8mdk
- initscripts.spec: removed damn *ippp* files (dam's).

* Mon Jan 14 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-7mdk
- service: If no action is specified print the help of service not
  of $0 himself.
- mandrake/*/*: Upgrade copyright.
- service: Add fullrestartall option.
- rc.d/init.d/network: store arp mapping fron /etc/ethers. (fredl).
- po/*.po: po updates (pablo).

* Thu Dec 27 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-6mdk
- mandrake/loader/: common.pm, installkernel, make-initrd: Add
  linus and mosix to valid mdk kernels.  Check if it is a valid
  mdk kernels even when no initrd.  installkernel different
  links for different vmlinuz version.
- service: If it is a xinetd service then restart xinetd.

* Mon Dec 10 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-5mdk
- service: Add new rewrite of /sbin/service.
- mandrake/loader/make-initrd: Rewrite it in shell no need to do
  perl when we launch only shell command.
- mandrake/loader/installkernel: Do something smarter with arg
  parsing.
- po/*, rc.d/init.d/functions: Changed the space padding of
  OK/PASSED/FAILED from functions file to the translations; so each
  language can custom it as needed. (pablo).
- rc.d/rc.local: handle /etc/issue and /etc/issue.net the same way
  as msec. (flepied).

* Tue Dec  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-4mdk
- mandrake/loader/: common.pm, grub, lilo, yaboot: New function
  sanitize_ver to detect all kind of kernels naming and sanitize
  (new_mdk, old_mdk, linus-vanilla, linus-pre) like the old one to
  still have backward compatibility with old config files. Make the
  loader using it.
- mandrake/loader/installkernel: Make the copy to vmlinuz.old more
  robust check if it is a link before and try to copy the vmlinuz.old
  only if the one installed != the one already installed (guess
  nobody will understand that but yes this is smarter things update
  ;)).
- po/sv.po: made Swedish file fulle 8bit (pablo).

* Thu Nov 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-3mdk
- initscripts.spec: Remove groupadd wtmp put it in setup package
  and require this package.
- initscripts.spec: Add cvs repository as URL.
- mandrake/usb: Remove the removal of module when stoping, don't
  ask me why is it broken in kernel.
- initscripts.spec: We have our own copy of gprintify so we don't
  want to call the one from spec-helper. (flepied).
- mandrake/loader/installkernel: When NOLINK=yes set the right
  options (andrej).

* Mon Nov 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.40.2-2mdk
- mandrake/kheader: Fix kheader with multiple kernel
  (relson@osagesoftware.com).
- mandrake/loader/installkernel: Call with perl the configurator.
- mandrake/loader/lilo: Remove memtest crunch from here
- sysconfig/network-scripts/ifup: Remove -d to dhcpcd.
- initscripts.spec: Mandrake-Linux => Mandrake Linux (flepied).
- po/hu.po: Upgrade po files (pablo).

* Wed Nov 14 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.40.2-1mdk
- merge with rh 6.40.2
- prefdm: Fix detection of GNOME in prefdm. (Fred Crozat)
- rc.d/init.d/halt: Recreate /initrd if needed.
- po/hu.po: updated Hungarian file. (Pablo)
- mandrake/loader/yaboot: another yaboot mod for PPC, eliminate	root=root=/dev/hdX. (Stew)
- ifup: correctly launch dhcpcd to avoid updating ntp.conf and yp.conf.
- rc.local: escape the backspaces given by linux_logo, so that
 mingetty will show our new MandrakeLinux logo correctly (Stefan Siegel).

* Thu Oct 18 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-21mdk
- mandrake/loader/lilo: Close file after open it before moving.
- mandrake/loader/lilo: Die instead of print STDERR if we have in
  unknow option.
- mandrake/loader/installkernel: Don't make-initrd when we are in
  REMOVE mode.
- mandrake/loader/make-initrd: Fix stupid bug in make-initrd when
  -L is used in argument parsing.
- sysconfig/network-scripts/ifup: By default add the --wait option
  to dhcpxd (erwan).
- mandrake/supermount: Cosmectic changes to usage (Andrej).
- mandrake/loader/common.pm: s/Look/Looks/ s/unknow/unknown/ (stefan).
- mandrake/supermount: Add support when fs=auto (Andrej).

* Tue Oct 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-20mdk
- mandrake/loader/common.pm: Fix another bug in kernel/initrd
  comparaisons.

* Mon Oct 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-19mdk
- mandrake/loader/common.pm: Really check comparaision of kernel
  between initrd and vmlinuz among with others cleanup/fixes.
- mandrake/loader/make-initrd: Add check if there is a
  /lib/modules/$kernel_version before launching mkinitrd.
- initscripts.spec: Fixes descriptions lenght.
- mandrake/Makefile: chmod 644 the tarball when uncompressing it.

* Mon Oct 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-18mdk
- mandrake/loader/common.pm: Fix check_default_entry() cleanup the
  code there also...

* Thu Oct 11 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-17mdk
- rc.d/rc.sysinit: really fix loop fsck & mount (i'm really ashamed)
  (pixel).

* Thu Oct 11 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-16mdk
- mandrake/mandrake_everytime: s|echo_failed|echo_failure| if tmp
  removal fail.
- mandrake/mandrake_everytime: Remove unneded commented action.
- rc.d/rc.sysinit: fixes non rootfs filesystems that are never checked
  (gc)

* Wed Oct 10 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-15mdk
- sysconfig.txt, sysconfig/network-scripts/ifup: Add DHCP_TIMEOUT=
  option fo dhcpcd client (#5690).
- mandrake/supermount: Don't process entry that are comment (#5684).

* Tue Oct  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-14mdk
- sysctl.conf: Add net.ipv4.ip_dynaddr rules, by default disable.
- mandrake/loader/: common.pm, grub, lilo: Rework the root
  detection to make sure to include the sysconfig options, use the
  same root strategey for lilo and grub. Make sure to don't add too
  much \n in the config files and nasty it.
- mandrake/loader/installkernel.sysconfig: fixed a typo ("yo" instead
  of "you") (siegle)
- mandrake/inputrc.csh: invert up-history and down-history (key
  behavior was wrong) (siegle).

* Fri Oct  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-13mdk
- mandrake/loader/make-initrd: Make relative symlinks.
- mandrake/loader/: installkernel, installkernel.sysconfig: Ignore
  the Autoremove=yes we use it only when install rpm kernel.

* Sat Sep 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-12mdk
- service: Fix typo :p.
- prefdm: Make prefdm compatible with old behavior (mr@uue.org).

* Fri Sep 28 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.27-11mdk
- mandrake/: supermount.8, loader/detectloader loader/detectloader.8,
  loader/rebootin, sound/alsa.utils: Upgrade copyright.
- mandrake/supermount: set device to none for first entry to don't
  confuse some tools that want to be smarter.
- mandrake/supermount.8: Upgrade documentation with latest.
- mandrake/supermount: Add patch from Andrej, correct detection by
  fallback on mountpoint when $good_device (aka: ability to fallback
  on mountpoint when the cdrom floppy or zip are not a link).
- service: Add mandrake_consmap to service to don't restart
  (Borsenkow Andrej <Andrej.Borsenkow@mow.siemens.ru>).
- mandrake/supermount: Make backup before doing infile, correct
  long bug with /dev/cdrom device.
- mandrake/loader/installkernel.sysconfig: Fix wrong comment.
- po/*.po: updated po files (pablo).
- rc.d/init.d/functions: Added a check for LANGUAGE before sourcing
  i18n file; otherwise program "services" don't display in the user's
  language. (pablo).
- mandrake/Makefile, mandrake/mandrake_consmap,
  rc.d/init.d/mandrake_consmap: moved mandrake specific file to
  mandrake/ directory; adapted Makefile to install it (pablo)
- prefdm: Patches from Jaegum that allows to use different xdm and
  desktop (eg: Gnome adnd kdm, or gdm and xfce, etc) (pablo)
- sysconfig/network-scripts/ifup: applyed john allen patch (dams).

* Mon Sep 17 2001 Warly <warly@mandrakesoft.com> 6.27-10mdk
- mandrake/mandrake_everytime: temporary patch to prevent boot error
message on cdrom and floppy due to supermount

* Mon Sep 17 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.27-9mdk
- rc.d/rc: add chvt 11 to rc instead of 12 (Warly)
- lang.sh: If RPM_INSTALL_LANG is not defined, don't try to guess
it; it will mess what is in /etc/rpm/macros (Pablo).
- lang.sh, rc.d/rc, rc.d/rc.sysinit, rc.d/init.d/mandrake_consmap:
Added console font patch from Borsenkow Andrej (Pablo).
- po/: hr.po, uk.po: updated Ukrainian and Croatian files (Pablo).
- installkernel: If NOLINK then even for initrd don't do a link (Chmouel).

* Sun Sep 16 2001 Pixel <pixel@mandrakesoft.com> 6.27-8mdk
- rc.d/init.d/functions: fix rc return of function daemon

* Sun Sep 16 2001 Warly <warly@mandrakesoft.com> 6.27-7mdk
- rc.d/rc.sysinit: change aurora vt from 12 to 11

* Sat Sep 15 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.27-6mdk
- init.d/functions: added libsafe support.

* Thu Sep 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.27-5mdk
- added fr man pages in package (tvignaud).
- ifown: don't use HWADDR as we don't rely anymore on config file to shutdown
the interface.
- halt: use the right path for powerfail (Juergen Holm).

* Tue Sep 11 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.27-4mdk
- ifdown: shutdown ip adresses according to the kernel and running dhcp client and not from what is configured.
- rc.sysinit: do not unmount /initrd if /initrd/loopfs is mounted (happens for root loopback) (Pixel)
- init.d/netfs: remove unmounting loopback (Pixel)
  (cuz it's redhat specific, don't go along with mdk loopback, and has nothing to do in netfs)

* Sun Sep  9 2001 Pixel <pixel@mandrakesoft.com> 6.27-3mdk
- rc.sysinit: fix&update loopback special code

* Sat Sep  8 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.27-2mdk
- rc.sysinit: restore from /lib/dev-state before starting devfsd (Andrej Borsenkow).
- rc.sysinit: clean dynamic desktop directories on startup.
- po: updated Bosnian, Norwegian, Swedish and Turkish files (Pablo)
- po: Added Irish file (Pablo)

* Sat Sep  1 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.27-1mdk
- 6.27

* Thu Aug 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.17-7mdk
- Added French man pages (Pablo)
- ifup ifdown: completed HWADDR support.

* Wed Aug 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.17-6mdk
- force the copy of /lib/dev-state files.
- po updates (Pablo, Fabman)
- send HUP signal to devfsd when the filesystems are mounted.
- lang.csh: don't have any error when LANG is unset (Pixel)

* Sat Aug 25 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.17-5mdk
- fixed locales lookup

* Fri Aug 24 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.17-4mdk
- mandrake/loader/common.pm: Use fstab to get the root filesystem if
  we fail in /proc/cmdline (aka: not for grub).
- rc.d/rc.sysinit: restore saved permissions and links on boot (flepied).
- po/*: replaced »Linux-Mandrake« by »Mandrake Linux« (siegle).
- po/lt.po: updated Lithuanian file (pablo).

* Tue Aug 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.17-3mdk
- rc.d/rc.sysinit: Move the devfsd initialisation at the early process
  before aurora.
- sysconfig/network-scripts/ifup: Fix ifup with dhcp.
- initscripts.spec: make ifcfg-lo as noreplace.

* Mon Aug 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.17-2mdk
- rc.d/rc.sysinit: Remove RH sound and usb stuff, move our usb
  stuff at the early beginning process.
- sysconfig/network-scripts/ifdown: Remove unneeded check_device_down
  and make ifdown work again.

* Mon Aug 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.17-1mdk
- merge 6.17

* Mon Aug 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.11-3mdk
- mandrake/usb: Fix USB loading.
- mandrake/loader/grub: Fix grub removal.
- rc.d/rc.sysinit: don't check /proc/lvm because it's created by the
  lvm module (pixel).
- po/*: Po upgrades (pablo).
- mandrake/Makefile: corrected rdiff target (flepied).

* Wed Aug 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.11-2mdk
- Fix halt.

* Sat Aug 11 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.11-1mdk
- merge with rh 6.11

* Mon Aug  6 2001 dam's <damien@mandrakesoft.com> 5.96-8mdk
- removed *ippp* from specfile.

* Mon Aug  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.96-7mdk
- rc.d/rc.sysinit: Fix checking filesystems to display a \n.
- rc.d/init.d/halt: Add devfs to force unmounting.
- rc.d/rc.sysinit: no more need to do the /dev/cdrom link (tvignaud).

* Sat Aug  4 2001 Pixel <pixel@mandrakesoft.com> 5.96-6mdk
- make detectloader works with devfs device naming (even when devfs is not mounted :)
- detectloader now requires perl-MDK-Common, adding it to Requires (i wonder why perl-base was not required yet!)

* Fri Jul 20 2001 dam's <damien@mandrakesoft.com> 5.96-5mdk
- corrected bad package( not cvs synchronised)

* Fri Jul 20 2001 dam's <damien@mandrakesoft.com> 5.96-4mdk
- typo

* Fri Jul 20 2001 dam's <damien@mandrakesoft.com> 5.96-3mdk
- removed if{up|down}-ippp, it's provided by isdn4net or isdn-light.

* Fri Jul  6 2001 Stefan van der Eijk <stefan@eijk.nu> 5.96-2mdk
- BuildRequires:	popt-devel

* Thu Jul  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 5.96-1mdk
- 5.96

* Mon Jun 25 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.87-3mdk
- service: If the user specify -d then launch the script (only for
  bash-shell one) in debug mode.
- po/eo.po: updated Esperanto file (pablo).

* Mon Jun 18 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.87-2mdk
- mandrake/mandrake_everytime: setup eth* (without configuring it)
 interfaces before the hotplug/pcmcia started so we are sure that what
 we have configured in /etc/modules.conf get the device we have
 affected.  NB: We assume max 10 interfaces for speed reason.

* Thu Jun 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.87-1mdk
- Merge with rh587.
- mandrake/kheader: Add restart target and update help.
- mandrake/usb: Add fully usb stop function to completely stop the
  usb system.
- mandrake/usb: add identifier codes to ohci_t for Apple USB
  controllers (stew).
- mandrake/usb: fix usb probe (gc).
- po/: hu.po, ru.po: updated Russian and Hungarian files (pablo).
- rc.d/rc.sysinit: allow to enable/disable DMA for IDE cdroms/dvdroms
  (stefan).
- mandrake/kheader: [I think I have found a problem in the kheader
  script, when you press F1 it doesn't show a complete description in
  ntsysv, you need to escape the description] (geofrrey).

* Wed May 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.83-6mdk
- mandrake/Makefile: too much cleanup is not good :p
- mandrake/loader/yaboot: Set the name of Stew instead of my (aka:
	bug him for yaboot ;)).
- mandrake/loader/Makefile: Install yaboot file on ppc.
- mandrake/loader/: Makefile, detectloader, detectloader.8,
  installkernel, rebootin, yaboot: Add yaboot support from Stew
  Benedict <sbenedict@mandrakesoft.com>.
- po/tr.po: updated Turkish file (pablo)
- rc.d/rc.sysinit: umount /dev if devfs mounted but devfsd isn't
  availlable (tvignaud).
- po/de.po: fixed typo (siegle).

* Fri May  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.83-5mdk
- sysconfig/network-scripts/ifup: Set also the MTU for dhcp device
	if specified.
- sysconfig/network-scripts/ifup: Don't do another check for MTU
  (thnks Oded Arbel <oded@geek.co.il>)
- rc.d/init.d/network: Fix FORWARD_IPV4 check #3468
- rc.d/rc.sysinit: Add -e to sysctl call.
- rc.d/rc.sysinit: Print Checking root filesystem with a \n and
  gprintf.
- mandrake/mandrake_firstime: Export the
  LD_LIBRARY_PATH=/usr/lib/mozilla before rebuild Mozilla registry.
- rc.d/rc.sysinit: If user has specified KEYBOARD_AT_BOOT="YES" in
  /etc/sysconfig/usb then force the load (like rh does).
- mandrake/usb.conf: add KEYBOARD_AT_BOOT variable to be set if we
  want to load the keyboard at the early process (in case of broken
  BIOS for example), add some comment also.
- mandrake/usb: If the interface is already loaded don't load it.
- sysconfig/network-scripts/ifup: Fix MTU setting (#2958).

* Wed May  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.83-4mdk
- rc.d/init.d/: network, netfs: Set quote when calling
  ${NETWORKING}. (#380)
- rc.d/rc.sysinit: Fix regexp of profile (#2028).
- mandrake/loader/detectloader: If user has specified a variable
  DEFAULT_LOADER="lilo" or grub then print it and exist (aka: don't
  detect).
- sysctl.conf: Disable ECN by default.
- po/: id.po, sv.po: Updated Swedish file, added indonesian file. (pablo)

* Mon Apr 30 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.83-3mdk
- initscripts.spec: fix modutils requires :-(.
- mandrake/loader/lilo: Detect which vga we running by the BOOT_IMAGE=
  we have booted (via cmdline) and what it set lilo.conf.
- mandrak
  Changed lang.sh so $X11_NOT_LOCALIZED don't apply when launching
  xdm-like changed the po/Makefile and *.spec so the translation
  filesgo to /usr/share/locale and only one is copied to /etc/locale
  (as /etc is small when in a separate partition) when
  /usr/share/locale is visible it is used.(pablo).
- rc.d/rc.sysinit: fixed problem of "stair effect" on some
  framebuffer displays. (pablo).

* Mon Mar 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.61.1-6mdk
- rc.d/rc.sysinit: Don't do any translation for the PS1 login or
  it break sulogin and break the rescue file system.

* Mon Mar 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.61.1-5mdk
- mandrake/loader/: grub, lilo: Backup config files before doing
  anything.

* Fri Mar 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.61.1-4mdk
- mandrake/loader/common.pm: Add debug. Don't get_the_first_kernel
  get the kernel we going to uninstall. Don't detect only mdk kernel
  in get_the_first_kernel. Reactive generation of mkinitrd.
- mandrake/loader/installkernel: Add remove options.
- mandrake/loader/lilo: Fix regexp when doing remove.
- mandrake/loader/grub: Add remove options for grub.

* Tue Mar 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.61.1-3mdk
- mandrake/loader/lilo: set $debug to 0.
- mandrake/loader/installkernel: copy image with -$version and create
  link from vmlinuz-$version to vmlinuz (also for system.map)
  Autodetect by default.
- sysconfig/network-scripts/ifdown: make sure to kill dhcpcd while
  is running (gc).
- sysconfig/network-scripts/ifup-ppp: Add changes from
  daniel@format-software.com (#2312)

* Sun Mar 11 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.61.1-2mdk
- Improve installkernel (add remove to lilo and bugs fixes).

* Sun Mar 11 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.61.1-1mdk
- Add new installkernel.
- Merge with rh 5.61.1 (flepied).

* Wed Mar  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.60-10mdk
- mandrake/usb: Make USB as 8 to be before sound.
- *.po/: pablo update po files.

* Sun Mar  4 2001 Pixel <pixel@mandrakesoft.com> 5.60-9mdk
- flepied: don't check /proc/lvm because it's created by the lvm module.

* Sat Mar 3 2001 RedHog <redhog@mandrakesoft.com> 5.60-8mdk
- Fix to work with non-framebuffer-based Aurora Monitors.

* Tue Feb 27 2001 Pixel <pixel@mandrakesoft.com> 5.60-7mdk
- ugly fix for ia64 (see fg)
- fix detectloader for new grub

* Thu Feb 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.60-6mdk
- mandrake/mandrake_everytime: Improve detection of supermount as
  advised by Stefan and Andrej.

* Tue Feb 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.60-5mdk
- mandrake/gprintify.py: Remove the workaround code.
- rc.d/rc.sysinit: Change the Setting Clock string as advised by pablo
	to don't need to workaround it for i18n.

* Mon Feb 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.60-4mdk
- mandrake/gprintify.py: Don't do translation of "Setting clock" since
	it segfault initlog at boot.
- rc.d/init.d/halt: Remove aumix stuff we do that in the sound script.

* Mon Feb 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.60-3mdk
- rc.d/rc.sysinit: Start keyboard after mounting filesystem.
- rc.d/init.d/halt: Unmount usb filesystem if exist before unmounting
  /proc

* Mon Feb 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.60-2mdk
- initscripts.spec: Check po files who are empty and rm -f it.
- rc.d/init.d/halt: Remount also read only the reiserfs fs.
- mandrake/usb: Don't make /etc/sysconfig/usb necessary Use depmod -A
  instead of touch modules.dep Mount USB filesystem with the right gid
  and devmod (fcrozat).  Don't exit if no usb is detected in
  /proc/devices Don't unload the module let the autoclean of modutils
  do it.
- mandrake/usb.conf: First version dropped from the install moved
  here.
- mandrake/Makefile: Add installation of usb.conf to /etc/sysconfig/usb
- initscripts.spec: Add /etc/sysconfig/usb.
- mandrake/usb: Add new ids of kind of usb host.
- rc.d/init.d/functions: Add patch from Stefan Siegel
	<siegel@informatik.uni-kl.de> to search LANG with ^LANG to don't
	have also KDE_LANG variable.
- mandrake/sound: Add patches from David Faure : A wrong regexp leads
	to the alsa module not being loaded.
- mandrake/mandrake_everytime: Erase with rm -rf not with rm -f.
- mandrake/mandrake_everytime: remove also the ksocket- files.
- mandrake/mandrake_everytime: rm -f /tmp/.esd* rm -f /tmp/orbit-* rm
  -f /tmp/ssh-* in TMP_CLEAN
- po/: az.po, cs.po, da.po, de.po, es.po, eu_ES.po, fi.po, fr.po,
	gl.po, hr.po, hu.po, id.po, initscripts.pot, is.po, it.po, ja.po,
	ko.po, no.po, pl.po, pt.po, pt_BR.po, ro.po, ru.po, sk.po, sl.po,
	sr.po, sv.po, tr.po, uk.po, wa.po, zh.po, zh_CN.GB2312.po: removed
	empty files updated po files with the strings of our scripts added
	Azeri file (pablo).
- po/de.po: new german version (siegel).
- po/de.po: new german version (siegel).
- rc.d/init.d/halt: fixed stop when in aurora mode (flepied).
- mandrake/gprintify.py: allow VAR=<value> cmd syntax (flepied).
- rc.d/rc.sysinit: set NIS domain name (flepied).
- src/initlog.c: declare basename to be able to work on ia64 (fg).
- rc.d/rc.sysinit: allow colored Mandrake (flepied).
- mandrake/gprintify.py: handle array vars (flepied).
- mandrake/gprintify.py: handle one or two i18n strings on the same
  line (flepied).
- rc.d/init.d/functions: export TEXTDOMAINDIR for gettext (flepied).
- po/Makefile: replace $var with %s when building .mo (flepied).
- mandrake/Makefile: don't remove source and spec when building the
  rpm (flepied).
- rc.d/rc.sysinit: i18n for booting aurora string (flepied).
- rc.d/rc.sysinit: removed USB stuff (flepied).
- mandrake/Makefile: corrected lookup of tar when building a rpm
  (flepied).
- sysconfig/network-scripts/ifup: removed merge mark (flepied).
- initscripts.spec: added BuildRequires python and findutils
  (flpeied).
- added ipv6 scripts (flepied).
- mandrake/gprintify.py: corrected rewrite of normal i18n strings
  (flepied).

* Wed Feb  7 2001 Frederic Lepied <flepied@mandrakesoft.com> 5.60-1mdk
- merge with rh 5.60

* Fri Feb  2 2001 Pixel <pixel@mandrakesoft.com> 5.54-3mdk
- do not disable sysreq by default!

* Fri Jan 26 2001 Frederic Lepied <flepied@mandrakesoft.com> 5.54-2mdk
- initial german translation (Stefan Siegel)
- corrected translation script. Now it uses the LANGUAGE variable, and checks for empty string (Pablo)
- corrected supermount detection (Chmouel)
- put usb at level 09 to have it before network and get usb-network loaded (Chmouel)
- corrected Aurora stuff
- added WIRELESS_ prefix to all wireless variables

* Wed Jan 24 2001 Frederic Lepied <flepied@mandrakesoft.com> 5.54-1mdk
- merge with rh 5.54

* Mon Jan 22 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 5.27-44mdk
- fixed the console font loading stuff (better checkings for availability
  of all needed files)

* Fri Jan 12 2001 Frederic Lepied <flepied@mandrakesoft.com> 5.27-43mdk
- sysconfig/network-scripts/ifup added wireless stuff.

* Wed Dec 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-42mdk
- mandrake/usb: Remove USB autoload stuff (for usbd), clean up the
  stop) section.

* Thu Dec 21 2000 Pixel <pixel@mandrakesoft.com> 5.27-41mdk
- s/source/./ in mandrake/tmpdir.sh (beware of `source' which is allowed in
bash, but not in standard bourne shell or compatible, like ksh)

* Wed Dec  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-40mdk
- lang.sh: Add more i18n variables exported.

* Mon Dec  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-39mdk
- mandrake/installkernel: Only don't update the link to /boot/vmlinuz
  when the link egal at the what we want to install.

* Fri Nov 10 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-38mdk
- lang.csh, setsysfont: Stefan Siegel patches (pablo).
- lang.csh, lang.sh, mandrake/listhome: modified lang.sh to read
  the i18n in the right order (user one first) (pablo).
- rc.d/init.d/network: Remove the egrep -v 'ifcfg-ippp[0-9]+$' like
  DarkDam's.

* Fri Oct  6 2000 Frederic Lepied <flepied@mandrakesoft.com> 5.27-37mdk
- set HOME to /root in prefdm for kdm.

* Fri Oct 6 2000 RedHog <redhog@mandrakesoft.com> 5.27-36mdk
- Chvt 1 instaed of displaying a message throygh Aurora, that is, the
  last messages are in TEXT, but they are at least
  displayed. Previously, a user might have turned the computer off
  before filesystems where unmounted...

* Wed Oct  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-35mdk
- Add Prereq: fileutils.

* Wed Oct  4 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 5.27-34mdk
- remove webmin-postinstall script from mandrake_firsttime because it
  is now called AFTER the initscripts :-(

* Wed Oct  4 2000 Pixel <pixel@mandrakesoft.com> 5.27-33mdk
- rc.modules: don't try insmod -p before modprobe as insmod doesn't know about
aliases and i wanna use aliases!

* Tue Oct 3 2000 RedHog <redhog@mandrakesoft.com> 5.27-32mdk
- Fix to differentiate between reboot and halt in init.d/halt under
  Aurora...

* Fri Sep 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-31mdk
- mandrake/tmpdir.sh: Set a return instead of an exist (thanks
  cooker people).

* Thu Sep 28 2000 RedHog <redhog@mandrakesoft.com> 5.27-30mdk
- Fix not to do chvt when starting Aurora. Why was this ever done??

* Wed Sep 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-29mdk
- Makefile: Call make changelog of mandrake/Makefile
- rc.d/init.d/halt: Call /sbin/Monitor only if Aurora is installed.
- rc.d/rc.sysinit: Wonder where this bug come from but remove \t
  before display 'Press I to enter interactive startup'.
- rc.d/init.d/netfs: s|nonfs|nfs|; in mount -a.
- rc.d/init.d/functions: add a usleep 100000 in killproc functions.
  use builtins shell to read the pid and not calling head.
- mandrake/usb: Mount usb interface only when usb interface is not
  already mounted (or in builtins).
- rc.d/rc.sysinit: Use grep -i everywhere we grep in /proc/cmdline.
- src/: initlog.c, netreport.c: Sync with redhat version.
- sysconfig/network-scripts/ifup-ppp: Add IDLETIMEOUT before
  DEMAND=yes.
- mandrake/mandrake_firstime: Remove the call to sound start since
  now mandrake_firstime is called in rc.local and not rc.sysinit
  (sound is already started).
- rc.d/rc.local: Move the call to mandrake_firstime here.
- rc.d/rc.sysinit: don't call mandrake_firstime here, since when
  for example we put the mixer we need to launch which hangup the
  sound.
- rc.d/rc.sysinit: Don't load Aurora if we are in failsafe mode.

* Wed Sep 27 2000 Frederic Lepied <flepied@mandrakesoft.com> 5.27-28mdk
- (functions): use -s /bin/sh for startup via su.

* Mon Sep 25 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 5.27-27mdk
- removed requirement of sysklogd to avoid inter-dependence

* Mon Sep 25 2000 RedHog <redhog@mandrakesoft.com> 5.27-26mdk
- Fix for interactive bootup under Aurora and addition of a nice
  "system succesfully taken down - it is now safe to turn it off" -
  message to Auroraish shutdown.

* Mon Sep 25 2000 dam's <damien@mandrakesoft.com> 5.27-25mdk
- ppp/ip-up : add adsl temp dns handling.

* Fri Sep 22 2000 Frederic Lepied <flepied@mandrakesoft.com> 5.27-24mdk
- prefdm: kill autologin on SIGTERM.

* Wed Sep 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-23mdk
- mandrake/detectloader: patch detectloader to skip cdroms (otherwise
  stops cd-audios) (pixel).
- rc.d/rc: Export the aurora variable.
- rc.d/init.d/halt: halt should halt when poweroff poweroff.

* Mon Sep 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-22mdk
- mandrake/installkernel: link for FB and smp to /boot/vmlinuz-$_.

* Sun Sep 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-21mdk
- rc.d/init.d/halt: Fix halt to poweroff.
- rc.d/rc.sysinit: Fix load of rc.modules.

* Wed Sep 13 2000 RedHog <redhog@mandrakesoft.com> 5.27-20mdk
- Fix for Aurora-disabling for fb-kernels with fb currently disabled

* Tue Sep 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-19mdk
- mandrake/usb: Rewrote usb devices detection and add the usb
  printer in the train.
- rc.d/init.d/halt: By default set halt with the poweroff option
  and if /halt exist halt witout poweroffing.

* Mon Sep 11 2000 Pixel <pixel@mandrakesoft.com> 5.27-18mdk
- remove unneeded is_depmod_necessary

* Fri Sep  8 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-17mdk
- mandrake/usb: Be quiet when grepping. Detect USB
  Storage. s|ZIP|Storage|;.

* Tue Sep  5 2000 Pixel <pixel@mandrakesoft.com> 5.27-16mdk
- modify detectloader for new grub

* Sun Sep 3 2000 RedHog <redhog@mandrakesoft.com> 5.27-15mdk
- setscreenchars is broken, so my last patch didn't help much :(

* Sat Sep  2 2000 RedHog <redhog@mandrakesoft.com> 5.27-14mdk
- fixes to setsysfont to be able to work without switching active vt
  to a non-graphical one (This was done to make it work nicely with
  Aurora)

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 5.27-13mdk
- add some checking about aurora

* Fri Sep  1 2000 Pixel <pixel@mandrakesoft.com> 5.27-12mdk
- make the initscripts aurora aware

* Wed Aug 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-11mdk
- lang.sh: added support for variables allowing different
	localization in console and in X11 (pablo).
- rc.d/rc: Fix typo check for /etc/rc.d/rc* not /etc/rc*.
- mandrake/tmpdir.sh: Only set to TMPDIR when SECURE_TMP = yes in
  /etc/sysconfig/system.
- mandrake/Makefile: Put rc.modules in /etc/rc.d/
- mandrake/installkernel: Add config file parser of
  /etc/sysconfig/kernel (not really using it yet)
- rc.d/init.d/rawdevices, sysconfig/rawdevices: A new greatest hit.
- rc.d/init.d/halt: Remove USB Red Hat stuff (we have our own
  initscripts stuff).

* Tue Aug 29 2000 Frederic Lepied <flepied@mandrakesoft.com> 5.27-10mdk
- prefdm: don't exit after autologin.
- do the right thing (tm) in /etc/rc.d/init.d scripts
- use (noreplace) for config files.

* Tue Aug 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-9mdk
- Move to /etc/init.d/ with symlinks.
- Upgrade to the last 5.44.

* Sat Aug  5 2000 Pixel <pixel@mandrakesoft.com> 5.27-8mdk
- mandrake/detectloader (detect): signature for grub updated for grub new
  version (recognizes both)

* Mon Jul 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-7mdk
- mandrake/installkernel: Rename some functions to avoid conflicts
  with drakxtool functions.  Correct initrd= (it's on a different
  line not on the same of kernel).
- sysconfig/network-scripts/ifup: Don't add a -i to DHCPCD for
   $DEVICE.
- sysconfig/network-scripts/ifup: Fix dhcp (s|DHCP|DYNCONFIG|) set
  DYNCONFIG when detecting BOOTPROT=DHCP
- sysconfig/network-scripts/ifup: Set pump as second preferred dhcp
  client after dhcpcd.
- sysconfig.txt, rc.d/init.d/network: Upgrade doc about depreciated
  option FORWARD_IPV4=.

* Mon Jul 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-6mdk
- mandrake/installkernel: Only import libDrakX when using with grub.  
- mandrake/installkernel: Detect where is the /boot partition when
  using grub (if not use the /)

* Mon Jul 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-5mdk
- mandrake/installkernel: correct the symlink for the current initrd.
- mandrake/usb: Still try to see if MOUSE|KEYBOARD=yes if auto
  detecting fails.
- mandrake/usb: Check if we have /proc/bus/usb/devices first and if
  we detect check if $VARIABLE != no.
- mandrake/usb: Mount /proc/bus/usb/ interfaces before detecting
  devices.

* Sun Jul 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-4mdk
- mandrake/installkernel: Add initrd support.
- mandrake/installkernel: Grub != Lilo, grub don't have a = for default.

* Sun Jul 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-3mdk
- mandrake/installkernel: Ask for boot image and System.map only on
  copy mode.
- mandrake/installkernel: Fix very stupid typo when checking if we
  are root.
 
* Sun Jul 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-2mdk
- Merge with rh5_35.
- mandrake/usb: If nousb on the command line exit 0;

* Sun Jul 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.27-1mdk
- mandrake/usb: Don't use USB mouse and keyboard anymore, try to
  detect them like RH does.
- mandrake/installkernel: complete rewrite in perl.
- 5.27 (major changes, i guess i'll have some bugs report).
- BM.

* Thu Jul  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-50mdk
- mandrake/detectloader: Add denis modifications (#350).
- lang.sh: special hack so that right-to-left translations are only
  used in the console and not on X11 (no support yet). (pablo)
- mandrake/mandrake_firstime: fixed the making of whatis index to
  also be done for non English pages.
  Execute the "mdk_convert_translations" scripts if any (pablo)

* Fri Jun 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-49mdk
- mandrake/Makefile: add make test.
- mandrake/usb: try to use /etc/modules.conf or /etc/conf.modules
- mandrake/sound: try to use /etc/modules.conf or /etc/conf.modules

* Wed Jun 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-48mdk
- mandrake/mandrake_everytime: if user specify HDPARM_OPT use this
  options to optimize.

* Tue Jun  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-47mdk
- mandrake/installkernel: don't try to rdev on another arch than x86.

* Tue Jun  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-46mdk
- mandrake/installkernel: fix another typo.

* Mon Jun  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-45mdk
- sysctl.conf: timestamps with a 's'.
- rc.d/rc.sysinit: Set hwclock on alpha only when modules.dep is
  present.

* Sun Jun  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-44mdk
- mandrake/installkernel: use $(uname -m) not $(uname -r) (thnks:
  guisseppe)..

* Fri Jun  2 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-43mdk
- mandrake/inputrc.csh: tcsh handles its command line itself;
  added the needed lines to have it recognize Home/End and arrow keys(pablo)
- ppp/ip-up: added support for dynamic DNS.(pablo).
- sysconfig/network-scripts/ifdown-ppp: fix CONFIG file sourcing.
- mandrake/installkernel: Fix chmou stupudity (again).

* Tue May 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-42mdk
- mandrake/installkernel: fix typo.

* Mon May 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-41mdk
- mandrake/usb: Don't load/unload keyboard on alpha (usb keyboard
  are builtins in alpha).
- mandrake/tmpdir.csh: Remove the /bin/csh to don't depend of csh.
- rc.d/rc.sysinit: Better devfs support (titi).
- mandrake/inputrc.csh: Remove = (not needed).

* Sun May 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-40mdk
- mandrake/Makefile: Include usb for alpha. 
- initscripts.spec: Include usb for alpha.

* Sun May 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-39mdk
- mandrake/mandrake_everytime: Always clean /tmp/esrv* and
  /tmp/kio* files when CLEAN_TMP is set.
- mandrake/mandrake_everytime: Don't disable supermount	 on sparc
  (not even present).
- mandrake/usb: if USB=no in /etc/sysconfig/usb return 0
- mandrake/rc.modules: Fix typo.
- mandrake/installkernel: remove the \. from the label for lilo to
  minimize the chars.
- mandrake/installkernel: don't try to do something with lilo or
  grub when we are not on a x86 machines.
- mandrake/installkernel: Add --quiet options.
- mandrake/installkernel: remove the mdk for secure for lilo to minimize
  the chars.
- mandrake/Makefile: Add binfmt_aout to /etc/modules on alpha for netscape.
- rc.d/rc.sysinit: Merge Adam Lesback <adam@mandrakesoft.com> ppc change.

* Fri May 26 2000 Adam Lebsack <adam@mandrakesoft.com> 4.97-38mdk
- Patch for rc.sysinit for Powermac clock

* Tue May 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-37mdk
- mandrake/Makefile: Add various if{,n}eq $(ARCH) for alpha and sparc.
- mandrake/initscripts.spec: Add various %%ifarch for alpha and sparc.

* Tue May 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-36mdk
- mandrake/kheader: exit 0 when no mdk kernel.

* Wed May 10 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-35mdk
-  mandrake/inputrc.csh: Fix typo (jerome).

* Mon May  8 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-34mdk
- mandrake/usb: set sleep between loading interfaces.

* Sun May  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-33mdk
- mandrake/mandrake_firstime: fix when setting mixer and there is
 no mixer.

* Sat May  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-32mdk
- sysconfig/network-scripts/(ifup|ifdown): Set by default dhcpcd not dhcpxd.
- rc.d/init.d/network: Set ipv4 forwarding when  FORWARD_IPV4=(yes|true).

* Fri May  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-31mdk
- mandrake/usb: Add printer support.

* Fri May  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-30mdk
- mandrake/mandrake_firstime: set the mixer to 80% by default.
- mandrake/sound: use of aumix even for alsa.  printk=0 when loading
  modules.

* Tue May  2 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-29mdk
- rc.d/init.d/netfs: starting and stopping netfs properly.
- sysconfig/network-scripts/ifup{-aliases,plip}: remove old kernel
  compatibilities.

* Fri Apr 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-28mdk
- sysconfig/network-scripts/ifup (DHCP_ARGS): fix ugly ''basename
  command not found''
- sysconfig/network-scripts/ifdown (CONFIG): fix support for
  multiple dhcp client.

* Wed Apr 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-27mdk
- mandrake/usb: fix mounting proc usb and umount usbdevfs when stoping.
- mandrake/kheader: exit 0 when no mdk kernel.

* Mon Apr 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-26mdk
- mandrake/installkernel (grub_device): root=$root_device not $kversion.

* Mon Apr 24 2000 Pixel <pixel@mandrakesoft.com> 4.97-25mdk
- mandrake/usb: fix missing 'fi'

* Sun Apr 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-24mdk
- mandrake/sound: Add alsa support.

* Sun Apr 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-23mdk
- mandrake/installkernel: move from kernel to here.
- mandrake/usb: Mount usbdevfs if present.
- mandrake/detectloader: Don't detect cdrom.

* Wed Apr 19 2000 Pixel <pixel@mandrakesoft.com> 4.97-22mdk
- mandrake/mandrake_firstime: call postinstall.sh for webmin if there

* Tue Apr 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-21mdk
- mandrake/detectloader.8: man pages of detectloader.
- mandrake/detectloader: A new greatest hit.

* Mon Apr 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-20mdk
- rc.d/rc: if no askrunlevel installed jump directly to runlevel 1.
- rc.d/rc: s|ASKRUNLEVEL|failsafe|;
- rc.d/rc.sysinit: s|ASKRUNLEVEL|failsafe|;

* Sun Apr 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-19mdk
- rc.d/rc.sysinit: check if ASKRUNLEVEL arg.
- rc.d/rc: if specify ASKRUNLEVEL on commandline then run
askrunlevel interactively.
- rc.d/rc: if we found the tag "halt: yes" then stop the script even
if no subsytem is touched.
- sysconfig/network-scripts/network-functions: /dev/null some
error message.
- sysconfig/network-scripts/ifdown: Check to make sure the device
is actually up
- src/netreport.c (main): if no args then show usage.
- src/minilogd.c: stat the PATH_LOG better.
- service: add --full-restart options.
- rc.d/rc.sysinit (CLOCKFLAGS): if no UTC then set up as localtime.
- rc.d/init.d/network: If this is a final shutdown/halt, check for
network FS, and unmount them even if the user didn't turn on netfs
- rc.d/init.d/network: setting syscontrol network here.
- rc.d/init.d/network: fix typos.
- rc.d/init.d/halt: specify when retrying to umount devices.
- ppp/ip-up: using "$@" instead of "$*"
- ppp/ip-down: using "$@" instead of "$*"
- mandrake/sound: Add level 6 in chkconfig.

* Thu Apr 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-18mdk
- initscripts.spec: Conflicts: linuxconf <= 1.17r9 (for askrunlevel).
- mandrake/sound: new script.
- rc.d/rc.sysinit: check for executable when launching rc.modules.
- rc.d/rc.sysinit: remove sound stuff.
- rc.d/init.d/halt: remove sound stuff.
- rc.d/rc: if user ask for interactive setup, launch askrunlevel
  to change runlevel on the fly and (re)configure system before
  booting.

* Wed Apr 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-17mdk
- mandrake/usb: Try to find a usb adaptator.
- mandrake/usb: zip support.
- mandrake/supermount: lots of supermount fix from <denis@mandrakesoft.com>.

* Thu Apr  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-16mdk
- sysconfig.txt: Upgrade doc.
- mandrake/mandrake_everytime: Clean up /tmp if it choose at
  install.
- rc.d/init.d/halt: don't umount /var/shm do this from
  /etc/fstab.
- rc.d/rc.sysinit: don't mount /var/shm do this from
  /etc/fstab.

* Wed Apr  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-15mdk
- mandrake/supermount: add a chmod 0644 after writing the file
  (don't be nazi, let's permit the simple user to read the
  /etc/fstab file :\).

* Wed Apr  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-14mdk
- mandrake/supermount: fix multiple bugs (multiple cdrom, handle options).
- mandrake/mandrake_everytime: don't use insmod -p to detect is supermount 
  module is here.

* Mon Apr  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-13mdk
- rc.d/init.d/network: don't exclude ipp[0-9] from interfaces.

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-12mdk
- rc.d/rc.sysinit:  devfsd, shm support (titi).
- rc.d/init.d/halt: shm support (titi).

* Tue Mar 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-11mdk
- initscripts.spec: Add sysctl.conf in %%files.

* Sat Mar 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-10mdk
- rc.d/rc.sysinit: ignore failure of symlinking System.map (aka	stderr to dave null)(pixel).
- mandrake/modules: new file kernel modules to load at boot time (btw: add vfat).
- mandrake/rc.modules: new file to load modules of /etc/modules.
- mandrake/supermount: Fix typo and chmou stupidity.
- mandrake/Makefile: Add kheader/rc.modules/modules.
- mandrake/mandrake_everytime: use better approach to detect if	
  supermount modules is not present.
- mandrake/mandrake_everytime: Remove the modprobe vfat.
- mandrake/mandrake_firstime: erase first logfile if the file is empty.
- initscripts.spec: Add kheader in %%post %%preun.
- initscripts.spec: Add rc.modules and modules in %%files.
- initscripts.spec: chkconfig --del usb in %%preun.
- initscripts.spec: Add changeLog in %%doc.
- rc.d/rc.sysinit: remove generation of /boot/kernel.h (moved to
	kheader script).
- mandrake/kheader: new file
- mandrake/usb: fix description.
- sysconfig.txt: upgrade documentation.
- sysconfig/network-scripts/ifup: if BOOTPROTO=bootp launch them
  via pump.
- sysconfig/network-scripts/ifup: by default launch dhcpxd for
  DHCP if is not installed launch dhclient || dhcpcd || pump. If
  the variable DHCP_CLIENT= is specified in ifcfg-$device configure
  this one.

* Wed Mar 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-9mdk
- rc.d/rc.sysinit: fix buggy call in linuxconf stuff.
- mandrake/Makefile: include is_depmod_necessary
- mandrake/is_depmod_necessary.c: move it here from modutils package.

* Tue Mar 21 2000 Pixel <pixel@mandrakesoft.com> 4.97-8mdk
- rc.d/init.d/halt: added removing of entry /initrd/loopfs in
/etc/mtab. removed unused lnx4win stuff

- rc.d/rc.sysinit: added adding of entry /initrd/loopfs in
/etc/mtab

- rc.d/rc.sysinit: move the chmou linuxconf stuff (buggy by the
way, sed doesn't exit code depending on succeeding subst)

* Sun Mar 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-7mdk
- mandrake/Makefile: fix typo.
- initscripts.spec: Conflicts with linuxconf <= 1.17r5
- rc.d/rc.sysinit: preliminary linuxconf profile support.
- rc.d/rc.local: don't display too much information in issue.net
  if SECURITY_LEVEL => 4.
- mandrake/supermount.8: minor modifications.
- mandrake/usb: remove unused sleep
- initscripts.spec: add inputrc.csh in %%files.

* Sat Mar 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-6mdk
- initscripts.spec: add inputrc.csh in %%files.

* Thu Mar 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-5mdk
- initscripts.spec: requires setup >= 2.1.9-3mdk (for inputrc).

* Mon Mar 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-4mdk
- initscripts.spec: Adjust groups. 

* Mon Mar 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-3mdk
- rc.d/rc.sysinit: Remove nasty mount /boot stuff (pixel)
- mandrake/usb: Get working with the new configuration scheme for usb.
- mandrake/usb: Preferring to use usb-interface to usb-mouse-interface.

* Sun Mar 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.97-2mdk
- *: upgrade to 4.97.
- ChangeLog: new one.
- initscripts.spec: clean-up spec.
- sysconfig/network-scripts/ifup: fix typo.
- sysctl.conf: sysrq = 1 on mandrake.
- service: Exclude mandrake_firstime | mandrake_everytime.
- mandrake/usb: make compatible with usb backport.

* Sun Feb  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.72-14mdk
- Don't optimize for DVD-ROM(#740).

* Wed Jan 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.72-13mdk
- Fix wrong supermount man pages.

* Fri Jan  7 2000 Pixel <pixel@mandrakesoft.com> 4.72-12mdk
- more intelligent prefdm (in case of bad sysconfig/desktop)

* Thu Jan  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.72-11mdk
- remove the -i switch to dhcpd (thanks Gary Simmons <darshu@sympatico.ca).

* Thu Dec 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add supermount manpages (camille).

* Wed Dec 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add a supermount script to disable or enable supermount.
- fix typos.

* Wed Dec 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add makewhatis on first boot.

* Fri Dec 24 1999 Frederic Lepied <flepied@mandrakesoft.com> 4.72-4mdk
- fix halt not to call umount /proc.

* Tue Dec 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 4.72.
- Fix a lot of bugs.

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
