#
# spec file for package grub
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# fdr: 0.97-5
#
# $Id$

%define revision	$Rev$
%define name		grub
%define version 	0.97
%define release 	%_revrel

Summary:	GRand Unified Bootloader
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.gnu.org/software/grub/
Source0:	ftp://alpha.gnu.org/gnu/grub/%{name}-%{version}.tar.gz
Source1:	annvix-splash.xpm.gz

# Follow Fedora patching convention... this is 100% FDR patching

# let's have some sort of organization for the patches
# patches 0-19 are for config file related changes (menu.lst->grub.conf)
#
Patch0:		grub-0.93-configfile.patch
Patch1:		grub-0.90-symlinkmenulst.patch
#
# patches 20-39 are for grub-install bits
#
Patch20:	grub-0.97-install.in.patch
Patch21:	grub-0.94-installcopyonly.patch
Patch22:	grub-0.94-addsyncs.patch
#
# patches 40-59 are for miscellaneous build related patches
#
# link against curses statically
Patch40:	grub-0.95-staticcurses.patch
# patches submitted upstream and pending approval
# change the message so that how to accept changes is clearer (#53846)
Patch81:	grub-0.93-endedit.patch
#
# patches 100-199 are for features proposed but not accepted upstream
#
# add support for appending kernel arguments
Patch100:	grub-0.90-append.patch
# add support for lilo -R-esque select a new os to boot into
Patch101:	grub-0.97-once.patch
#
# patches 200-299 are for graphics mode related patches
#
Patch200:	grub-0.95-graphics.patch
Patch201:	grub-0.91-splashimagehelp.patch
Patch202:	grub-0.93-graphics-bootterm.patch
Patch203:	grub-0.95-hiddenmenu-tweak.patch
#
# patches 300-399 are for things already upstream
#
#
# patches 500+ are for miscellaneous little things
#
# support for non-std devs (eg cciss, etc)
Patch500:	grub-0.93-special-device-names.patch
# i2o device support
Patch501:	grub-0.94-i2o.patch
# detect cciss/ida/i2o
Patch502:	grub-0.95-moreraid.patch
# for some reason, using the initrd max part of the setup.S structure
# causes problems on x86_64 and with 4G/4G
Patch505:	grub-0.94-initrdmax.patch
# we need to use O_DIRECT to avoid hitting oddities with caching
Patch800:	grub-0.95-odirect.patch
# the 2.6 kernel no longer does geometry fixups.  so now I get to do it
# instead in userspace everywhere.
Patch1000:	grub-0.95-geometry-26kernel.patch
# Support for booting from a RAID1 device
Patch1100:	grub-0.95-md.patch
Patch1101:	grub-0.95-md-rework.patch
# Ignore everything before the XPM header in the bootsplash
Patch1102:	grub-0.95-xpmjunk.patch
# Don't go to "graphics" mode unless we find the bootsplash and it's an xpm,
# and don't print any errors about the missing file while current_term is
# "graphics".
Patch1103:	grub-0.95-splash-error-term.patch
# Mark the simulation stack executable
Patch1104:	grub-0.97-nxstack.patch
Patch1105:	grub-0.97-nx-multiinstall.patch
# always use a full path for mdadm.
Patch1110:	grub-0.97-mdadm-path.patch
# always install into the mbr if we're on a raid1 /boot.
Patch1111:	grub-0.95-md-mbr.patch
# gcc4 fixes.
Patch1115:	grub-0.97-gcc4.patch
# Make non-MBR installs work again on non-raid1.
Patch1120:	grub-0.95-nonmbr.patch
# Make "grub-install --recheck" look like the menace it is.
Patch1130:	grub-0.95-recheck-bad.patch
# Fix missing prototypes, since grub nicely sets -Wmissing-prototypes and
# then tries to build conftests without them.
Patch1135:	grub-0.97-prototypes.patch
# put /usr/lib/grub back in /usr/share/grub like it was before, so other
# scripts don't screw up.
Patch1140:	grub-0.97-datadir.patch
# install correctly on dmraid devices
Patch1145:	grub-0.97-dmraid.patch
Patch1146:	grub-0.97-dmraid-recheck-bad.patch
Patch1147:	grub-0.97-dmraid-partition-names.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel
BuildRequires:	texinfo
BuildRequires:	binutils
BuildRequires:	automake1.7
BuildRequires:	autoconf2.5

ExclusiveArch:	%{ix86} x86_64
Requires:	diffutils
Requires:	mktemp
Requires(post):	info-install
Requires(preun): info-install
Conflicts:	initscripts <= 6.40.2-15mdk
Provides:	bootloader

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems.  In addition to loading the Linux and *BSD kernels,
it implements the Multiboot standard, which allows for flexible loading
of multiple boot images (needed for modular kernels such as the GNU
Hurd).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .config
%patch1 -p1 -b .menulst
%patch20 -p1 -b .install
%patch21 -p1 -b .copyonly
%patch22 -p1 -b .addsync
%patch40 -p1 -b .static
%patch81 -p0 -b .endedit
%patch100 -p1 -b .append
%patch101 -p1 -b .bootonce
%patch200 -p1 -b .graphics
%patch201 -p1 -b .splashhelp
%patch202 -p1 -b .bootterm
%patch203 -p1 -b .hidden
%patch500 -p1 -b .raid
%patch501 -p1 -b .i2o
%patch502 -p1 -b .moreraid
%patch505 -p1 -b .initrdmax
%patch800 -p1 -b .odirect
%patch1000 -p1 -b .26geom
%patch1100 -p1 -b .md
%patch1101 -p1 -b .md-rework
%patch1102 -p1 -b .xpmjunk
%patch1103 -p1 -b .splash-error-term
%patch1104 -p1 -b .nxstack
%patch1105 -p1 -b .nx-multiinstall
%patch1110 -p1 -b .mdadm-path
%patch1111 -p1 -b .md-mbr
%patch1115 -p1 -b .gcc4
%patch1120 -p1 -b .nonmbr
%patch1130 -p1 -b .recheck-bad
%patch1135 -p1 -b .prototypes
%patch1140 -p1 -b .datadir
%patch1145 -p1 -b .dmraid
%patch1146 -p1 -b .dmraid-recheck-bad
%patch1147 -p1 -b .dmraid-partition-names


%build
#WANT_AUTOCONF_2_5=1 autoreconf --install --force
aclocal-1.7
WANT_AUTOCONF_2_5=1 autoconf
automake-1.7 --force-missing

#CFLAGS="-Os -g" ; export CFLAGS
#%ifarch x86_64
#CFLAGS="$CFLAGS -static" ; export CFLAGS
#%endif

./configure \
    --prefix=%{_prefix} \
    --sbindir=/sbin \
    --disable-auto-linux-mem-opt
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall sbindir=%{buildroot}/sbin
mkdir -p %{buildroot}{/boot/grub,%{_sysconfdir}}

rm -f %{buildroot}%{_infodir}/dir

install -m 0644 %{SOURCE1} %{buildroot}/boot/grub/
ln -s ../boot/grub/grub.conf %{buildroot}%{_sysconfdir}/grub.conf


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info
%_install_info multiboot.info


%triggerun -- grub < 0.97-7235avx
if [ -e /boot/grub/grub.conf ]; then
    perl -pi -e 's|background 000000|background 34d1c0|' /boot/grub/grub.conf
    perl -pi -e 's|foreground 34d1c0|foreground 000000|' /boot/grub/grub.conf
fi


%preun
%_remove_install_info %{name}.info
%_remove_install_info multiboot.info


%files
%defattr(-,root,root)
/boot/grub
/sbin/grub
/sbin/grub-install
/sbin/grub-terminfo
/sbin/grub-md5-crypt
%{_bindir}/mbchk
%{_infodir}/grub*
%{_infodir}/multiboot*
%{_mandir}/man*/*
%dir %{_datadir}/grub
%{_datadir}/grub/*
%config(noreplace) %{_sysconfdir}/grub.conf

%files doc
%defattr(-,root,root)
%doc README TODO BUGS NEWS ChangeLog docs/menu.lst


%changelog
* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.97
- rebuild with new binutils

* Mon Apr 02 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.97
- new grub splash image
- add a trigger to change the foreground/background colors on update

* Sat Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.97
- rebuild againt new ncurses

* Sun Aug 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.97
- updated P501 so it actually compiles

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.97
- 0.97
- sync with fedora 0.97-5:
  - updated P20, P101, P500, P1000
  - dropped P300
  - new P1104, P1105, P1110, P1111, P1115, P1120, P1130, P1135, P1140,
    P1145, P1146, P1147
- add -doc subpackage
- rebuild with gcc4

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.95
- use --prefix with configure or else grub-install looks for files
  in /usr/local/share

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.95
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.95
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.95
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq
- let grub set it's own CFLAGS without our tampering otherwise we get
  undefined reference stuff for __guard and __stack_smash_handler

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.95-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.95-2avx
- bootstrap build
- build without stack protection

* Fri Feb 04 2005 Vincent Danen <vdanen@opensls.org> 0.95-1avx
- 0.95
- remodel to follow the FDR spec completely (only use FDR patches)
  in an attempt to make graphical splash screens work
- sync with fedora 0.95-7
- grub goes graphic... install a graphical bootloader screen
- add a symlink to grub.conf in /etc
- don't apply P800 because it seems to make grub not detect devices
  properly and breaks grub-install

* Thu Jun 24 2004 Vincent Danen <vdanen@opensls.org> 0.93-7avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.93-6sls
- Provides: bootloader

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 0.93-5sls
- remove docs package
- don't use %%build_opensls
- docs in main package
- amd64 support
- don't remove mbchk files
- files are in /sbin not /usr/sbin
- get rid of the /boot/grub/install.sh stuff in %%post since we haven't had
  that there in forever
- sync some patches with fedora 0.93-7:
  - P10/P11: grub.conf default, not menu.lst
  - P12: link against curses statically
  - P13: support large disks
  - P14/P15/P16: graphics mode support
  - P17: support to build on amd64
- this gives us preliminary splash support but there are a lot of issues
  with it to resolve

* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 0.93-4sls
- OpenSLS build
- tidy spec
- don't build doc with %%build_opensls

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
