#
# spec file for package udev
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		udev
%define version 	114
%define release 	%_revrel

%define major		0
%define libname		%mklibname volume_id %{major}
%define devname		%mklibname volume_id -d

%define EXTRAS		"extras/ata_id extras/cdrom_id extras/edd_id extras/firmware extras/path_id/ extras/scsi_id extras/usb_id extras/volume_id/"

Summary:	A userspace implementation of devfs
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group:		System/Configuration/Hardware
URL:		ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
Patch0:		udev-114-libudevdir.patch

BuildRequires:  kernel-source
BuildRequires:	dietlibc
BuildRequires:	glibc-static-devel
BuildRoot: 	%{_buildroot}/%{name}-%{version}

%description
Udev is an implementation of devfs/devfsd in userspace using sysfs and
/sbin/hotplug. It requires a 2.6 kernel to run properly.

Like devfs, udev dynamically creates and removes device nodes from /dev/.
It responds to /sbin/hotplug device events.

This package only exists to build the volume_id libraries and development
files.  Annvix does not provide udev support.


%package -n %{libname}
Group:		System/Libraries
Summary:	Library for volume_id

%description -n %{libname}
Library for volume_id.


%package -n %{devname}
Group:		Development/C
Summary:	Devel library for volume_id
Provides:	volume_id-devel = %{version}-%{release}
Provides:	libvolume_id-devel = %{version}-%{release}
Requires:	%{libname} = %{version}

%description -n %{devname}
Devel library for volume_id.


%prep
%setup -q
find -type f | xargs chmod u+rw
%patch0 -p1 -b .libudevdir


%build
%serverbuild

%ifarch x86_64
COMP="diet x86_64-annvix-linux-gnu-gcc"
%else
COMP="diet gcc"
%endif
make E=@\# CC="$COMP" CFLAGS="-Os" RANLIB="ranlib" -C extras/volume_id/lib libvolume_id.a
mv extras/volume_id/lib/libvolume_id.a libvolume_id.a.diet
%make clean

make libudevdir=/%{_lib}/udev EXTRAS=%{EXTRAS} USE_LOG=true


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%make \
    EXTRAS=%{EXTRAS} \
    DESTDIR=%{buildroot} \
    install \
    libudevdir=/%{_lib}/udev \
    libdir=/%{_lib} \
    usrlibdir=%{_libdir}

install -d %{buildroot}%{_prefix}/lib/dietlibc/lib-%{_arch}
install libvolume_id.a.diet %{buildroot}%{_prefix}/lib/dietlibc/lib-%{_arch}/libvolume_id.a

# delete udev and it's files, we only want the libs
rm -rf %{buildroot}{%{_sysconfdir},/sbin,%{_bindir},%{_sbindir},%{_datadir},/%{_lib}/udev}


%check
%if %{_lib} != lib
find %{buildroot} \
    -not -wholename '*/usr/*/debug/*' -a \
    -not -wholename '*/usr/share/doc/*' -a \
    -not -wholename '*/usr/share/man/*' \
    -print0 \
    | xargs -0 grep /lib/udev && exit 1
%endif


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
/%{_lib}/libvolume_id.so.*

%files -n %{devname}
%{_libdir}/libvolume_id.*
%{_prefix}/lib/dietlibc/lib-%{_arch}/libvolume_id.a
%{_libdir}/pkgconfig/libvolume_id.pc
%{_includedir}/libvolume_id.h


%changelog
* Sun Oct 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 114
- first Annvix build; don't package udev, just the volume_id libs
  and development files (needed by new mkinitrd)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
