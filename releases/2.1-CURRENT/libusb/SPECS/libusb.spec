#
# spec file for package libusb
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libusb
%define	version		0.1.12
%define	release		%_revrel

%define api		0.1
%define major		4
%define libname		%mklibname usb %{api} %{major}
%define devname		%mklibname usb %{api} -d
%define staticdevname	%mklibname usb %{api} -d -s
%define basiclibname	%{name}%{api}

Summary:	Libusb is a library which allows userspace access to USB devices
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://libusb.sf.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/libusb/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Libusb is a library which allows userspace access to USB devices.


%package -n %{libname}
Summary:        Libusb is a library which allows userspace access to USB devices
Group:          System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	%{basiclibname} = %{version}-%{release}

%description -n	%{libname}
Libusb is a library which allows userspace access to USB devices.


%package -n %{devname}
Summary:        Libusb is a library which allows userspace access to USB devices
Group:          Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{basiclibname}-devel = %{version}-%{release}
Obsoletes:	%mklibname usb %{api} 4 -d
Requires:	%{libname} = %{version}

%description -n	%{devname}
This package includes the header files and shared libraries
necessary for developing programs which will access USB devices using
the %{name} library.


%package -n %{staticdevname}
Summary:        Static libraries for libusb
Group:          Development/C
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	%{basiclibname}-static-devel = %{version}-%{release}
Obsoletes:	%mklibname usb %{api} 4 -d -s
Requires:	%{devname} = %{version}

%description -n	%{staticdevname}
This package includes the static libraries necessary for developing
programs which will access USB devices using the %{name} library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x --disable-build-docs
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/libusb-config

# move libs to /%{_lib} for UPS shutdown
mkdir -p %{buildroot}/%{_lib}
pushd %{buildroot}%{_libdir}
    mv *.so.* ../../%{_lib}/
    # run lib_symlinks here so that we can remove what we want afterwards
    %{_datadir}/spec-helper/lib_symlinks
    rm -f libusb*.so.*
    export DONT_SYMLINK_LIBS=1
    # XXX: fix libusb.la if it's used with ltdlopen, i.e. current usage
    # only works to build stuff, aka .so symlink is not dispatched and.
    ln -sf ../../%{_lib}/libusb-%{api}.so.%{major} libusb.so
    ln -sf ../../%{_lib}/libusbpp-%{api}.so.%{major} libusbpp.so
popd
ln -s ../usr/lib/libusb.la %{buildroot}/%{_lib}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -p /sbin/ldconfig -n %{libname}
%postun -p /sbin/ldconfig -n %{libname}


%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_bindir}/libusb-config
%multiarch %{multiarch_bindir}/libusb-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
/%{_lib}/*.la

%files -n %{staticdevname}
%defattr(-,root,root)
%{_libdir}/*.a

%files doc
%defattr(-,root,root)
%doc AUTHORS README INSTALL.libusb NEWS ChangeLog


%changelog
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.1.12
- get rid of %%odevname

* Fri Sep 7 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.1.12
- implement devel naming policy
- implement library provides policy
- fix libusbpp symlink

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.1.12
- 0.1.12
- move *.la into the -devel package
- fix source url
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.1.8
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.1.8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.1.8-1avx
- first Annvix build (required by usbutils)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
