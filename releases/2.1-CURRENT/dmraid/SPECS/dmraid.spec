#
# spec file for package dmraid
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		dmraid
%define version		1.0.0.rc14
%define release		%_revrel
#%define epoch		0

%ifarch %{ix86} x86_64
%define use_dietlibc	1
%else
%define use_dietlibc	0
%endif

%{?_with_dietlibc: %{expand: %%global use_dietlibc 1}}
%{?_without_dietlibc: %{expand: %%global use_dietlibc 0}}

Summary:	Device-mapper ATARAID tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
#Epoch:		%{epoch}
Group:		System/Kernel and hardware
License:	GPL
URL:		http://people.redhat.com/~heinzm
Source0:	http://people.redhat.com/~heinzm/sw/dmraid/src/dmraid-%{version}.tar.bz2
Patch0:		dmraid-mdk.patch
Patch1:		dmraid-isw_raid10.patch
Patch2:		dmraid-isw_raid10_1.patch
Patch3:		dmraid-isw_segfault.patch
Patch4:		dmraid-pdc_max_sectors.patch
Patch5:		dmraid-pdc_configoffsets.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	device-mapper-devel >= 1.00.09
%if %{use_dietlibc}
BuildRequires:	dietlibc-devel >= 0.29
%else
BuildRequires:	glibc-static-devel
%endif

%description
dmraid (Device-Mapper Raid tool) discovers, [de]activates and displays
properties of software RAID sets (i.e. ATARAID) and contained DOS
partitions using the device-mapper runtime of the 2.6 kernel.

The following ATARAID types are supported on Linux 2.6:

Adaptec HostRAID ASR
Highpoint HPT37X
Highpoint HPT45X
Intel Software RAID
JMicron JMB36X
LSI Logic MegaRAID
NVidia NForce
Promise FastTrack
Silicon Image Medley
VIA Software RAID


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}/%{version}
%patch0 -p2 -b .mdk
%patch1 -p1 -b .isw_raid10
%patch2 -p0 -b .isw_raid101
%patch3 -p0 -b .isw_segfault
%patch4 -p1 -b .pdc_max_sectors
%patch5 -p0 -b .pdc_configoffsets


%build
%if %{use_dietlibc}
%ifarch x86_64
COMP="diet x86_64-annvix-linux-gnu-gcc"
%else
COMP="diet gcc"
%endif
%endif

%if %{use_dietlibc}
%configure2_5x \
    --enable-dietlibc \
    --disable-libselinux
%else
%configure2_5x \
    --enable-static_link \
    --disable-libselinux
%endif

%if %{use_dietlibc}
make CC="${COMP}"
%else
make
%endif

mv tools/dmraid tools/dmraid-static
make clean

%configure \
    --with-user=`id -un` \
    --with-group=`id -gn`
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir} %{buildroot}/sbin
%makeinstall -s sbindir=%{buildroot}/sbin
install tools/dmraid-static %{buildroot}/sbin
rm -rf %{buildroot}%{_includedir}/dmraid


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0755,root,root) /sbin/dmraid
%attr(0755,root,root) /sbin/dmraid-static
%{_mandir}/man8/dmraid.8*
%exclude %{_libdir}

%files doc
%defattr(-,root,root)
%doc CHANGELOG KNOWN_BUGS README TODO doc/dmraid_design.txt


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.0.rc14
- 1.0.0.rc14
- drop fedora patches, merged upstream
- P1, P2: add raid10 support for isw format
- P3: fix a segfault issue with dmraid -r -E with isw
- P4, P5: improve Promise FastTrack metadata detection

* Fri Dec 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.0.rc11
- rebuild against new device-mapper

* Wed Aug 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.0.rc11
- dietlibc fixes for x86_64

* Wed Aug 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.0.rc11
- first Annvix build based on Mandriva's 1.0.0-0.rc11.1mdv
- there's no help for it, comment out to remind we need to use epoch once
  the final (assuming 1.0.0) is released due to RH's idiot versioning

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
