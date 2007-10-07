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
%define version		8.37.1
%define release		%_revrel

Summary:	The inittab file and the /etc/init.d scripts
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		http://svn.annvix.org/cgi-bin/viewvc.cgi/tools/initscripts/
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
Requires:	module-init-tools
Requires:	psmisc
Requires:	which
Requires:	setup
Requires:	iproute2
Requires:	iputils
Requires:	util-linux >= 2.10s
Requires:	mount >= 2.11l
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
rm -f %{buildroot}/etc/sysconfig/network-scripts/{ifdown-ippp,ifup-ctc,ifup-escon,ifup-ippp,ifup-iucv,ifup-ipsec,ifdown-ipsec}

# we have our own copy of gprintify
export DONT_GPRINTIFY=1


%post
touch /var/log/wtmp
touch /var/log/btmp
touch /var/run/utmp
chown root:utmp /var/log/wtmp /var/run/utmp /var/log/btmp
chmod 0664 /var/log/wtmp /var/run/utmp
chmod 0600 /var/log/btmp


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %verify(not md5 mtime size) /etc/adjtime
%config(noreplace) /etc/initlog.conf
%config(noreplace) /etc/modules
/etc/rc.modules
%dir /etc/modprobe.preload.d
%config(noreplace) /etc/sysctl.conf
%dir /etc/sysconfig
%config(noreplace) /etc/sysconfig/i18n
%config(noreplace) /etc/sysconfig/networking/ifcfg-lo
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
%attr(0700,root,root) /usr/sbin/usernetctl

%dir %attr(775,root,root) /var/run/netreport
%ghost %attr(0664,root,utmp) /var/log/wtmp
%ghost %attr(0600,root,utmp) /var/log/btmp
%ghost %attr(0664,root,utmp) /var/run/utmp

%{_mandir}/man*/*

%files doc
%defattr(-,root,root)
%doc sysconfig.txt sysvinitfiles ChangeLog.gz static-routes-ipv6 ipv6-tunnel.howto ipv6-6to4.howto


%changelog
* Sun Oct 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 8.37.1
- requires module-init-tools, not modutils

* Sat Sep 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 8.37.1
- fix url
- build against new glib2

* Fri Feb 09 2007 Vincent Danen <vdanen-at-build.annvix.org> 8.37.1
- 8.37.1; lots of cleanups

* Sat Jan 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 8.37
- 8.37; more minor modifications

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.36
- 8.36; more minor fixes

* Wed Nov 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.35
- remove requires on SysVinit

* Sat Oct 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.35
- update sysctl.conf to note the kernel.modprobe option

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.35
- 8.35; some minor fixes

* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.34
- fix the "ok" message placement when scripts include the functions file

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
