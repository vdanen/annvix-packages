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
%define	version		1.02.07
%define	extraversion	%{nil}
%define	release		%_revrel

%ifarch %{ix86} x86_64 ppc ppc64
%define	use_dietlibc	1
%else
%define	use_dietlibc	0
%endif

%define	build_dmeventd	1

%{?_with_dmeventd: %{expand: %%global build_dmeventd 1}}
%{?_without_dmeventd: %{expand: %%global build_dmeventd 0}}
%{?_with_dietlibc: %{expand: %%global use_dietlibc 1}}
%{?_without_dietlibc: %{expand: %%global use_dietlibc 0}}

%define	_sbindir	/sbin
%define	major		1.02

# Macro: %%{mklibname <name> [<major> [<minor>]] [-s] [-d]}
%define	libname		%mklibname devmapper %major
%define	dlibname	%mklibname devmapper %major -d
%define	pdlibname	%mklibname devmapper -d
%define	elibname	%mklibname devmapper-event %major
%define	delibname	%mklibname devmapper-event %major -d
%define	pdelibname	%mklibname devmapper-event -d

Summary:	Device mapper
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://sources.redhat.com/dm/
Source0:	ftp://sources.redhat.com/pub/dm/%{name}.%{version}%{extraversion}.tar.bz2
Patch0:		device-mapper.1.02.07-build.patch
Patch2:		device-mapper.1.02.07-pk.patch
Patch3:		device-mapper.1.02.07-misc.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5 >= 2.53
%if %{use_dietlibc}
BuildRequires:	dietlibc-devel
%else
BuildRequires:	glibc-static-devel
%endif

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
Requires(post):	ldconfig
Requires(postun): ldconfig

%description -n %{libname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the shared libraries required for running
programs which use device-mapper.


%package -n %{dlibname}
Summary:	Device mapper development library
Group:		Development/C
Provides:	device-mapper-devel = %{version}-%{release}
Provides:	libdevmapper-devel = %{version}-%{release}
Provides:	%{pdlibname} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	pkgconfig
Conflicts:	device-mapper-devel < %{version}-%{release}

%description -n %{dlibname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the header files and development libraries
for building programs which use device-mapper.


%if %{build_dmeventd}
%package -n %{elibname}
Summary:	Device mapper event library
Group:		System/Kernel and hardware
Requires(post):	ldconfig
Requires(postun): ldconfig

%description -n %{elibname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the shared libraries required for running
programs which use device-mapper-event.


%package -n %{delibname}
Summary:	Device mapper event development library
Group:		Development/C
Provides:	device-mapper-event-devel = %{version}-%{release}
Provides:	libdevmapper-event-devel = %{version}-%{release}
Provides:	%{pdelibname} = %{version}-%{release}
Requires:	%{elibname} = %{version}-%{release}
Requires:	%{dlibname} = %{version}-%{release}
Requires:	pkgconfig
Conflicts:	device-mapper-event-devel < %{version}-%{release}

%description -n %{delibname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the header files and development libraries
for building programs which use device-mapper-event.
%endif


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}.%{version}%{extraversion}
%patch0 -p1 -b .build
%patch2 -p1 -b .pkg
%patch3 -p1 -b .misc
autoconf


%build
%configure2_5x \
    --with-user=`id -un` \
    --with-group=`id -gn` \
%if %{use_dietlibc}
    --enable-static_link_dietlibc \
%else
    --enable-static_link \
%endif
    --disable-selinux \
%if %{build_dmeventd}
    --enable-dmeventd \
%endif
    --enable-pkgconfig \

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libdevmapper.so.* %{buildroot}/%{_lib}
ln -sf /%{_lib}/libdevmapper.so.%{major} %{buildroot}%{_libdir}/libdevmapper.so
%if %{use_dietlibc}
mv %{buildroot}%{_sbindir}/dmsetup-static{-diet,}
%endif
chmod -R u+w %{buildroot} #else brp won't strip binaries


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%if %{build_dmeventd}
%post -n %{elibname} -p /sbin/ldconfig
%postun -n %{elibname} -p /sbin/ldconfig
%endif


%files -n dmsetup
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dmsetup
%attr(755,root,root) %{_sbindir}/dmsetup-static
%{_mandir}/man8/dmsetup.8*

%files -n %{libname}
%defattr(755,root,root)
/%{_lib}/libdevmapper.so.*

%files -n %{dlibname}
%defattr(644,root,root,755)
%{_libdir}/libdevmapper.so
%{_libdir}/libdevmapper.a*
%{_includedir}/libdevmapper.h
%if %{use_dietlibc}
%{_libdir}/libdevmapper-diet.a*
%endif
%{_libdir}/pkgconfig/devmapper.pc

%if %{build_dmeventd}
%defattr(755,root,root)
%files -n %{elibname}
%{_libdir}/libdevmapper-event.so.*

%files -n %{delibname}
%defattr(644,root,root,755)
%{_includedir}/libdevmapper-event.h
%{_libdir}/libdevmapper-event.so
%{_libdir}/libdevmapper-event.a*
%{_libdir}/pkgconfig/devmapper-event.pc
%endif

%files doc
%defattr(-,root,root)
%doc INSTALL INTRO README VERSION WHATS_NEW
#doc patches/*.patch.bz2
%doc scripts/*
%doc contrib/*


%changelog
* Wed Aug 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.02.07
- first Annvix build based on Mandriva's 1.02.07-4mdv
