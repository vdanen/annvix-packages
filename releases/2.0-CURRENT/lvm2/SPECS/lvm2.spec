#
# spec file for package lvm2
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision        $Rev$
%define name            lvm2
%define version         2.02.09
%define release         %_revrel

Summary:	Logical Volume Manager administration tools
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://sources.redhat.com/lvm2/
Source0:	ftp://sources.redhat.com/pub/lvm2/LVM2.%{version}.tar.bz2

Patch0:		lvm2-alternatives.patch
Patch1:		lvm2-2.02.09-diet.patch
Patch2:		lvm2-2.01.15-stdint.patch
Patch3:		lvm2-termcap.patch
Patch4:		lvm2-ignorelock.patch
Patch5:		lvm2-fdlog.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	device-mapper-devel >= 1.02
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
BuildRequires:	dietlibc-devel

Conflicts:	lvm
Conflicts:	lvm1

%description
LVM includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadm(8) or even loop devices, see losetup(8)),
creating volume groups (kind of virtual disks) from one or more physical
volumes and creating one or more logical volumes (kind of logical partitions)
in volume groups.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n LVM2.%{version}
%patch0 -p1 -b .alternatives
%patch1 -p1 -b .diet
%patch2 -p1 -b .stdint
%patch3 -p1 -b .termcap
%patch4 -p1 -b .ignorelock
%patch5 -p1 -b .fdlog


%build
autoconf # required by termcap patch

export ac_cv_lib_dl_dlopen=no
%configure \
    --with-user=`id -un` \
    --with-group=`id -gn` \
    --enable-static_link \
    --disable-readline \
    --disable-selinux \
    --with-cluster=none \
    --with-pool=none

unset ac_cv_lib_dl_dlopen
CFEXTRA="-DWRAPPER -D_BSD_SOURCE"
%ifarch x86_64
export CC="diet x86_64-annvix-linux-gnu-gcc $CFEXTRA"
%else
export CC="diet gcc $CFEXTRA"
%endif
LVMLIBS="-llvm -ldevmapper-diet"

%make CC="$CC" LVMLIBS="$LVMLIBS"

pushd tools
    $CC -o lvm-static lvm.o lvmcmdline.o vgchange.o vgscan.o toollib.o vgmknodes.o pvmove.o polldaemon.o -L ../lib $LVMLIBS
popd

%make clean

unset CC
%configure \
    --with-user=`id -un` \
    --with-group=`id -gn` \
    --disable-static_link \
    --enable-readline \
    --disable-selinux \
    --enable-fsadm \
    --enable-nls \
    --with-pool=internal

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall sbindir=%{buildroot}/sbin confdir=%{buildroot}%{_sysconfdir}/lvm

install -m 0755 tools/lvm-static %{buildroot}/sbin/lvm.static
install -m 0755 tools/fsadm/fsadm %{buildroot}/sbin
chmod 0755 %{buildroot}/sbin/lvm

# compatibility links
ln %{buildroot}/sbin/lvm %{buildroot}/sbin/lvm2
ln %{buildroot}/sbin/lvm.static %{buildroot}/sbin/lvm2-static

%find_lang %{name}
%kill_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
if [ -L /sbin/lvm -a -L /etc/alternatives/lvm ]; then
    update-alternatives --remove lvm /sbin/lvm2
fi


%files
%defattr(-,root,root)
%attr(0755,root,root) /sbin/*
%dir %{_sysconfdir}/lvm
%config(noreplace) %{_sysconfdir}/lvm/lvm.conf
%{_mandir}/man5/*
%{_mandir}/man8/*

%files doc
%defattr(-,root,root)
%doc INSTALL README VERSION WHATS_NEW


%changelog
* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.02.09
- 2.02.09 (lvm2)
- chmod lvm so we have perms to strip it

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8
- Obfuscate email addresses and new tagging
- Uncompress patches
- dietlibc fixes

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8-5avx
- bootstrap build (new gcc, new glibc)
- merge with lvm1-1.0.8-5mdk:
  - make it build with recent gcc and glibc (bluca)
  - do not use getgrnam when statically built against glibc (bluca)
  - use dietlibc

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8-4avx
- rebuild

* Wed Nov 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8-3avx
- P3: security fix for CAN-2004-0972

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8-2avx
- Annvix build

* Fri Mar  5 2004 Thomas Backlund <tmb@mandrake.org> 1.0.8-1sls
- update to 1.0.8 to match 2.4.25 kernel and support
  future move to lvm2
  
* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 1.0.7-3sls
- OpenSLS build
- tidy spec
- remove %%{_prefix}

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
