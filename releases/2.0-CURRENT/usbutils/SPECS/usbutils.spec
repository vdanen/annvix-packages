#
# spec file for package usbutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		usbutils
%define version 	0.72
%define release		%_revrel

Summary:	Linux USB utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://sourceforge.net/project/showfiles.php?group_id=3581&package_id=142529
Source0:	http://prownloads.sourceforge.net/linux-usb/usbutils-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libusb-devel

%description
usbutils contains a utility for inspecting devices connected to the USB bus.
It requires a Linux kernel version 2.3.15 or newer (supporting the
'/proc/bus/usb' interface).


%prep
%setup -q


%build
%configure \
    --enable-usbmodules
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -f %{buildroot}{%{_includedir}/libusb.h,%{_libdir}/libusb*}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{_datadir}/usb.ids
%{_sbindir}/*


%changelog
* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.72
- rebuild against new libusb

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.72
- 0.72
- use the usb.ids provided in the package rather than an external source
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.70
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.70
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.70-1avx
- 0.70
- BuildRequires: libusb-devel

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11-8avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11-7avx
- rebuild

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.11-6avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 0.11-5sls
- minor spec cleanups
- remove %%prefix

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 0.11-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
