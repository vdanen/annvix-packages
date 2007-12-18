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
Requires:	perl(MDK::Common)
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
* Mon Dec 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.4
- don't add the user vcsa; we dropped that pre-2.0-RELEASE

* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.4
- add requires on perl(MDK::Common)

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
