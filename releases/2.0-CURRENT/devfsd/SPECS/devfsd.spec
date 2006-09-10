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
* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org>
- rebuild with gcc4
- remove pre-Annvix changelog

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
