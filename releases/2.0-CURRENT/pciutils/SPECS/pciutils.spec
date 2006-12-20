#
# spec file for package pciutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		pciutils
%define version		2.2.3
%define release		%_revrel

Summary:	PCI bus related utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://atrey.karlin.mff.cuni.cz/~mj/pciutils.html
Source0:	ftp://atrey.karlin.mff.cuni.cz/pub/linux/pci/%{name}-%{version}.tar.gz
Patch0:		pciutils-strip.patch
Patch2:		pciutils-2.1.10-scan.patch
Patch3:		pciutils-havepread.patch
Patch5:		pciutils-devicetype.patch
Patch6:		pciutils-2.2.1-idpath.patch
Patch7:		pciutils-2.1.99-gcc4.patch
Patch8:		pciutils-2.2.3-multilib.patch
Patch9:		pciutils-2.2.3-sata.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
%ifarch %{ix86}
BuildRequires:	dietlibc-devel
%endif

Requires:	kernel >= 2.1.82
Requires:	hwdata

%description
This package contains various utilities for inspecting and setting
devices connected to the PCI bus. The utilities provided require
kernel version 2.1.82 or newer (supporting the /proc/bus/pci
interface).


%package devel
Summary:	Linux PCI development library
Group:		Development/C
Requires:	%{name} = %{version}

%description devel
This package contains a library for inspecting and setting
devices connected to the PCI bus.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .strip
%patch2 -p1 -b .scan
%patch3 -p1 -b .pread
%patch5 -p1 -b .devicetype
%patch6 -p1 -b .idpath
%patch7 -p1 -b .glibcmacros
%patch8 -p1 -b .multilib
%patch9 -p1 -b .sata


%build
%ifarch %{ix86}
make OPT="%{optflags} -D_GNU_SOURCE=1" CC="diet gcc" PREFIX="/usr"  IDSDIR="/usr/share/hwdata"
mv lib/libpci.a lib/libpci_loader_a
make clean
%endif

make OPT="%{optflags} -D_GNU_SOURCE=1" PREFIX="/usr" IDSDIR="/usr/share/hwdata"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}{/sbin,%{_mandir}/man8,%{_libdir},%{_includedir}/pci}

install -s lspci setpci %{buildroot}/sbin
install -m 0644 lspci.8 setpci.8 %{buildroot}%{_mandir}/man8
install -m 0644 lib/libpci.a %{buildroot}%{_libdir}
install -m 0644 lib/{pci.h,header.h,config.h,types.h} %{buildroot}%{_includedir}/pci

%ifarch %{ix86}
install lib/libpci_loader_a %{buildroot}%{_libdir}/libpci_loader.a
%endif


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(0644,root,root,0755)
%{_mandir}/man8/*
%attr(0755,root,root) /sbin/*

%files devel
%defattr(0644,root,root,0755)
%{_libdir}/libpci.a
%ifarch %{ix86}
%{_libdir}/libpci_loader.a
%endif
%{_includedir}/pci

%files doc
%defattr(-,root,root)
%doc README ChangeLog pciutils.lsm


%changelog
* Tue Dec 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- spec cleanups

* Sat Nov 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- 2.2.3
- refresh patches from Fedora

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.99.test8
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.99.test8
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.99.test8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.99.test8-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.99.test8-3avx
- rebuild

* Fri Feb 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.99-test8-2avx
- rebuild against new dietlibc

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.99-test8-1avx
- 2.1.99-test8
- sync patches with Fedora (P5, P6)
- drop P4, fixed upstream
- spec cleanups
- relocate binaries to /sbin
- drop BuildRequires: wget

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.99-test3-2avx
- Annvix build

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> 2.1.99-test3-1sls
- 2.1.99-test3
- sync patches with Fedora (support for dietlibc)

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.1.11-6sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.1.11-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
