#
# spec file for package device-mapper
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define	name		device-mapper
%define	version		1.02.22
%define	release		%_revrel

%define	_sbindir	/sbin
%define	major		1.02

# cannot build with SSP
%define _ssp_cflags	%nil

%define	libname		%mklibname devmapper %{major}
%define	devname		%mklibname devmapper -d
%define	elibname	%mklibname devmapper-event %{major}
%define	edevname	%mklibname devmapper-event -d

Summary:	Device mapper
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2 or LGPLv2
Group:		System/Kernel and hardware
URL:		http://sources.redhat.com/dm/
Source0:	ftp://sources.redhat.com/pub/dm/%{name}.%{version}.tgz
Source1:	ftp://sources.redhat.com/pub/dm/%{name}.%{version}.tgz.asc
Patch0:		device-mapper.1.02.22-mdv-build.patch
Patch2:		device-mapper.1.02.22-mdv-pkgconfig.patch
Patch3:		device-mapper.1.02.22-mdv-canonicalize.patch
Patch4:		device-mapper.1.02.22-mdv-uint64.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf
BuildRequires:	dietlibc-devel

%description
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.


%package -n dmsetup
Summary:	Device mapper setup tool
Group:		System/Kernel and hardware
Provides:	device-mapper = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n dmsetup
Dmsetup manages logical devices that use the device-mapper driver.  
Devices are created by loading a table that specifies a target for
each sector (512 bytes) in the logical device.


%package -n %{libname}
Summary:	Device mapper library
Group:		System/Kernel and hardware
Provides:	libdevmapper = %{version}-%{release}
Requires(post):	ldconfig
Requires(postun): ldconfig

%description -n %{libname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the shared libraries required for running
programs which use device-mapper.


%package -n %{devname}
Summary:	Device mapper development library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libdevmapper-devel = %{version}-%{release}
Obsoletes:	%mklibname devmapper -d 1.02
Requires:	%{libname} = %{version}-%{release}
Requires:	pkgconfig
Conflicts:	device-mapper-devel < %{version}-%{release}

%description -n %{devname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the header files and development libraries
for building programs which use device-mapper.


%package -n %{elibname}
Summary:	Device mapper event library
Group:		System/Kernel and hardware
Provides:	libdevmapper-event = %{version}-%{release}
Requires(post):	ldconfig
Requires(postun): ldconfig

%description -n %{elibname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the shared libraries required for running
programs which use device-mapper-event.


%package -n %{edevname}
Summary:	Device mapper event development library
Group:		Development/C
Provides:	%{name}-event-devel = %{version}-%{release}
Provides:	libdevmapper-event-devel = %{version}-%{release}
Obsoletes:	%mklibname devmapper-event -d 1.02
Requires:	%{elibname} = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}
Requires:	pkgconfig
Conflicts:	device-mapper-event-devel < %{version}-%{release}

%description -n %{edevname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the header files and development libraries
for building programs which use device-mapper-event.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}.%{version}
%patch0 -p1 -b .build
%patch2 -p1 -b .pkgconfig
%patch3 -p1 -b .canonicalize
%patch4 -p1 -b .uint64
autoconf


%build
%ifarch x86_64
CC="x86_64-annvix-linux-gnu-gcc"
%else
CC="gcc"
%endif

%configure2_5x \
    --with-user=`id -un` \
    --with-group=`id -gn` \
    --enable-static_link_dietlibc \
    --disable-selinux \
    --enable-dmeventd \
    --enable-pkgconfig

%make CC="${CC}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libdevmapper.so.* %{buildroot}/%{_lib}
ln -sf /%{_lib}/libdevmapper.so.%{major} %{buildroot}%{_libdir}/libdevmapper.so
mv %{buildroot}%{_sbindir}/dmsetup-static{-diet,}
chmod -R u+w %{buildroot} #else brp won't strip binaries


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post -n %{elibname} -p /sbin/ldconfig
%postun -n %{elibname} -p /sbin/ldconfig


%files -n dmsetup
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dmsetup
%attr(755,root,root) %{_sbindir}/dmsetup-static
%attr(755,root,root) %{_sbindir}/dmeventd
%{_mandir}/man8/dmsetup.8*

%files -n %{libname}
%defattr(755,root,root)
/%{_lib}/libdevmapper.so.*

%files -n %{devname}
%defattr(644,root,root,755)
%{_libdir}/libdevmapper.so
%{_libdir}/libdevmapper.a*
%{_includedir}/libdevmapper.h
%{_libdir}/libdevmapper-diet.a*
%{_libdir}/pkgconfig/devmapper.pc

%defattr(755,root,root)
%files -n %{elibname}
%{_libdir}/libdevmapper-event.so.*

%files -n %{edevname}
%defattr(644,root,root,755)
%{_includedir}/libdevmapper-event.h
%{_libdir}/libdevmapper-event.so
%{_libdir}/libdevmapper-event.a*
%{_libdir}/pkgconfig/devmapper-event.pc

%files doc
%defattr(-,root,root)
%doc INSTALL INTRO README VERSION WHATS_NEW
#doc patches/*.patch.bz2
%doc scripts/*
%doc contrib/*


%changelog
* Wed Nov 28 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.02.22
- 1.02.22
- rediff P0, P2 from Mandriva
- drop P3
- new P3, P4 to fix build issues with dietlibc
- add dmeventd to dmsetup package
- S1: add the gpg signature

* Sat Aug 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.02.09
- implement devel naming policy
- implement library provides policy
- always use dietlibc
- always build the eventd
- update P2 to fix DM_LIB_VERSION for pkgconfig dependencies

* Thu Dec 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.02.09
- 1.02.09
- updated P3 from Mandriva

* Wed Aug 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.02.07
- dietlibc fixes for x86_64

* Wed Aug 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.02.07
- first Annvix build based on Mandriva's 1.02.07-4mdv

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
