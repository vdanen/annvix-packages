%define name	usbutils
%define version 0.11
%define release 5sls

Summary:	Linux USB utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://usb.in.tum.de/download/usbutils
Source0:	http://usb.in.tum.de/download/usbutils/usbutils-%{version}.tar.bz2
# 1.95 2002/01/13 (with 2 fixes + PHY below)
Source1:	http://www.linux-usb.org/usb.ids
Patch0:		usbutils-0.11-fix-classes.patch.bz2 

BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
usbutils contains a utility for inspecting devices connected to the USB bus.
It requires a Linux kernel version 2.3.15 or newer (supporting the
'/proc/bus/usb' interface).

%prep
%setup -q
perl -pe 's/^PHY.*//' %SOURCE1 > usb.ids
%patch0 -p0 -b .classes

%build
%configure
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

# the latest usb.ids contain entries that usbutils doesn't handle
rm -f $RPM_BUILD_ROOT{%_includedir/libusb.h,%_libdir/libusb*}
#perl -pe 's/^PHY.*//' %{SOURCE1} > $RPM_BUILD_ROOT%{_datadir}/usb.ids

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_mandir}/*/*
%{_datadir}/usb.ids
%{_sbindir}/*


%changelog
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
