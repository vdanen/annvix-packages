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
%define version		2.2.9
%define release		%_revrel

Summary:	PCI bus related utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://atrey.karlin.mff.cuni.cz/~mj/pciutils.html
Source0:	ftp://atrey.karlin.mff.cuni.cz/pub/linux/pci/%{name}-%{version}.tar.gz
Patch0: 	pciutils-2.2.1-mdv-use-stdint.patch
Patch1:		pciutils-2.2.4-mdv-pcimodules.patch
Patch2:		pciutils-2.2.1-mdv-cardbus-only-when-root.patch
# allow build with dietlibc, using sycall() and sys/io.h
Patch3:		pciutils-2.2.6-mdv-noglibc.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	dietlibc-devel

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%make PREFIX=%{_prefix} ZLIB=no OPT="-Os" CC="diet gcc" lib/libpci.a
cp lib/libpci.a libpci.a.diet
make clean

%make PREFIX=%{_prefix} OPT="$RPM_OPT_FLAGS -fPIC" ZLIB=no


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}{%{_bindir},%{_mandir}/man8,%{_libdir},%{_includedir}/pci}

install -m 0755 pcimodules lspci setpci %{buildroot}%{_bindir}
install -m 0644 pcimodules.man lspci.8 setpci.8 %{buildroot}%{_mandir}/man8
install -m 0644 lib/libpci.a %{buildroot}%{_libdir}
install -m 0644 lib/{pci.h,header.h,config.h,types.h} %{buildroot}%{_includedir}/pci

install -d %{buildroot}%{_prefix}/lib/dietlibc/lib-%{_arch}
install libpci.a.diet %{buildroot}%{_prefix}/lib/dietlibc/lib-%{_arch}/libpci.a

%multiarch_includes %{buildroot}%{_includedir}/pci/config.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/man8/*
%{_bindir}/lspci
%{_bindir}/pcimodules
%{_bindir}/setpci


%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_prefix}/lib/dietlibc/lib-%{_arch}/libpci.a
%{_includedir}/pci
%{_includedir}/*/pci
%multiarch %{_includedir}/multiarch-*/pci/config.h


%files doc
%defattr(-,root,root)
%doc README ChangeLog pciutils.lsm TODO 


%changelog
* Wed Mar 05 2008 Vincent Danen <vdanen-at-build.annvix.org> 2.2.9
- 2.2.9

* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.6
- 2.2.6
- updated patches from Mandriva 2.2.6-3mdv
- always build with dietlibc
- relocate binaries from /sbin to /usr/bin

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
