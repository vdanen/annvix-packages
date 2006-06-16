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

* Sun Apr  6 2003 Pixel <pixel@mandrakesoft.com> 0.11-3mdk
- update ids list
- fix patch 0 (otherwise, one gets "Invalid product/subclass spec", bug #3654)

* Mon Jan 06 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.11-2mdk
- update ids list
- patch 0 : let ldetect fill its class field for hub & interface classes
- fix build with new rpm

* Tue Oct 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.11-1mdk
- new release
- updated usb.ids

* Thu Jun 27 2002 Pixel <pixel@mandrakesoft.com> 0.10-1mdk
- updated usb.ids
- new release

* Fri Jan 25 2002 Pixel <pixel@mandrakesoft.com> 0.9-1mdk
- updated usb.ids
- new version

* Thu Oct 11 2001 Pixel <pixel@mandrakesoft.com> 0.8-3mdk
- s/Copyright/License/

* Mon Sep 10 2001 Pixel <pixel@mandrakesoft.com> 0.8-2mdk
- the latest usb.ids contain entries that usbutils doesn't handle (PHY lines),
  remove them

* Mon Aug 13 2001 Pixel <pixel@mandrakesoft.com> 0.8-1mdk
- new version
- get the latest usb.ids from http://www.linux-usb.org/usb.ids
- remove the hotplug patch which is included by default

* Mon Jul  2 2001 Pixel <pixel@mandrakesoft.com> 0.7-3mdk
- fix description

* Tue Jun 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.7-2mdk
- Add hotplug patch.

* Sat Dec 16 2000 Pixel <pixel@mandrakesoft.com> 0.7-1mdk
- initial spec


# end of file
