%define	name	device-mapper
%define	version	1.00.19
%define	release	3avx

#%ifarch %{ix86} x86_64 ppc
#%define	use_dietlibc	1
#%else
%define	use_dietlibc	0
#%endif

%define	_sbindir	/sbin
%define	major		1.00
# Macro: %%{mklibname <name> [<major> [<minor>]] [-s] [-d]}
%define	libname		%{mklibname devmapper 1.00}
%define	dlibname	%{mklibname devmapper 1.00 -d}

Summary:	Device mapper
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://sources.redhat.com/dm/
Source0:	ftp://sources.redhat.com/pub/dm/%{name}.%{version}.tar.bz2
Patch0:		device-mapper-1.00.19-diet.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	glibc-static-devel
%if %{use_dietlibc}
BuildRequires:	dietlibc-devel
%endif

%description
The goal of this driver is to support volume management.  
The driver enables the definition of new block devices composed of
ranges of sectors of existing devices.  This can be used to define
disk partitions - or logical volumes.  This light-weight kernel
component can support user-space tools for logical volume management.

%package -n dmsetup
Summary:	Device mapper setup tool
Group:		System/Kernel and hardware
Provides:	device-mapper = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n dmsetup
The goal of this driver is to support volume management.  
The driver enables the definition of new block devices composed of
ranges of sectors of existing devices.  This can be used to define
disk partitions - or logical volumes.  This light-weight kernel
component can support user-space tools for logical volume management.

%package -n %{libname}
Summary:	Device mapper library
Group:		System/Kernel and hardware

%description -n	%{libname}
The goal of this driver is to support volume management.  
The driver enables the definition of new block devices composed of
ranges of sectors of existing devices.  This can be used to define
disk partitions - or logical volumes.  This light-weight kernel
component can support user-space tools for logical volume management.

%package -n %{dlibname}
Summary:	Device mapper development library
Group:		Development/C
Provides:	device-mapper-devel = %{version}-%{release}
Provides:	libdevmapper-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{dlibname}
The goal of this driver is to support volume management.  
The driver enables the definition of new block devices composed of
ranges of sectors of existing devices.  This can be used to define
disk partitions - or logical volumes.  This light-weight kernel
component can support user-space tools for logical volume management.

%prep
%setup -q -n %{name}.%{version}
%if %{use_dietlibc}
%patch0 -p1 -b .diet
%endif
bzip2 patches/*.patch

%build
%configure --with-user=`id -un` --with-group=`id -gn` --enable-static_link --disable-selinux

%if %{use_dietlibc}
%make CC="diet gcc" PIC=
mv lib/ioctl/libdevmapper.a lib/ioctl/libdevmapper-diet.a
mv dmsetup/dmsetup-static dmsetup/dmsetup-diet
%make clean
%endif

OPTFLAGS="%{optflags} -fno-stack-protector" %make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libdevmapper.so.* %{buildroot}/%{_lib}
ln -sf /%{_lib}/libdevmapper.so.%{major} %{buildroot}%{_libdir}/libdevmapper.so

%if %{use_dietlibc}
cp lib/ioctl/libdevmapper-diet.a %{buildroot}%{_libdir}
install dmsetup/dmsetup-diet %{buildroot}%{_sbindir}/dmsetup-static
%endif

chmod -R u+w %{buildroot} #else brp_mandrake won't strip binaries

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files -n dmsetup
%defattr(644,root,root,755)
%doc INSTALL INTRO README VERSION WHATS_NEW
%doc scripts/*
%attr(755,root,root) %{_sbindir}/dmsetup
%if %{use_dietlibc}
%attr(755,root,root) %{_sbindir}/dmsetup-static
%else
%attr(755,root,root) %{_sbindir}/dmsetup.static
%endif
%{_mandir}/man8/dmsetup.8*

%files -n %{libname}
%defattr(755,root,root)
/%{_lib}/libdevmapper.so.*

%files -n %{dlibname}
%defattr(644,root,root,755)
%{_libdir}/libdevmapper.*
%{_includedir}/libdevmapper.h
%if %{use_dietlibc}
%{_libdir}/libdevmapper-diet.*
%endif

%changelog
* Fri Sep 24 2004 Vincent Danen <vdanen@annvix.org> 1.00.19-3avx
- initial Annvix build (for lilo)
- spec cleanups / make proper use of %%use_dietlibc
- don't include patches in docs (huh?)
- don't build with dietlibc as it doesn't like our SSP system for some
  reason (and I have no time to debug right now)

* Sun Aug 01 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.00.19-2mdk
- enable dietlibc version on ppc

* Mon Jul 26 2004 Luca Berra <bluca@vodka.it> 1.00.19-1mdk 
- 1.00.19
- rediffed p0
- disable selinux build

* Tue Jun 29 2004 Luca Berra <bluca@vodka.it> 1.00.18-1mdk 
- 1.00.18
- rediffed p0
- fix unstripped binaries

* Mon Apr 19 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.00.16-2mdk
- fix buildrequires
- spec cosmetics

* Sat Apr 17 2004 Luca Berra <bluca@vodka.it> 1.00.16-1mdk 
- 1.00.16
- rediffed p0
- added dmsetup-static

* Fri Dec 19 2003 Luca Berra <bluca@vodka.it> 1.00.07-2mdk
- i discovered --disable-compat to configure actually enables it
- put library in %%{_lib}
- fix permissions

* Sat Nov 22 2003 Luca Berra <bluca@vodka.it> 1.00.07-1mdk
- 1.00.07
- dmsetup requires same version of library
- correct provides for development library

* Thu Nov 20 2003 Luca Berra <bluca@vodka.it> 1.00.05-2mdk
- provide dietlibc version for building lvm2 tools

* Sat Sep 06 2003 Luca Berra <bluca@vodka.it> 1.00.05-1mdk
- 1.00.05

* Wed Aug 27 2003 Luca Berra <bluca@vodka.it> 1.00.01-0.rc2.1mdk
- 1.00.04
- mdk uses bz2

* Wed Jul 16 2003 Luca Berra <bluca@vodka.it> 1.00.01-0.rc2.1mdk
- 1.00.01-rc2

* Sun Dec  1 2002 Luca Berra <bluca@vodka.it> 0.96.07-1mdk
- 0.96.07

* Sat Jun  1 2002 Luca Berra <bluca@vodka.it> 0.95.11-1mdk
- 0.95.11
