#
# spec file for package mkbootdisk
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mkbootdisk
%define version 	1.5.1
%define release 	%_revrel

Summary: 	Creates an initial ramdisk image for preloading modules
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Kernel and hardware
URL:		http://www.redhat.com/swr/src/mkbootdisk-1.4.2-1.src.html
Source: 	%{name}-%{version}.tar.bz2
Patch0: 	mkbootdisk-1.5.1-mdk.patch
Patch1: 	mkbootdisk-1.5.1-devfs-compliant.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}

ExclusiveArch: 	sparc sparc64 %{ix86} x86_64 amd64
ExclusiveOs: 	Linux
Requires: 	mkinitrd
Requires:	gawk
Requires:	dosfstools
Requires:	mktemp
Conflicts:	modutils < 2.3.11-5
%ifarch %ix86 x86_64 amd64
Requires:	syslinux >= 1.76-2mdk
%endif
%ifarch sparc sparc64
Requires: 	silo
Requires:	genromfs
%endif

%description
The mkbootdisk program creates a standalone boot floppy disk for booting
the running system.  The created boot disk will look for the root
filesystem on the device mentioned in /etc/fstab and includes an
initial ramdisk image which will load any necessary SCSI modules for
the system.


%prep
%setup -q
%patch0 -p1 -b .mdk
%patch1 -p1 -b .devfs


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%make BUILDROOT=%{buildroot} mandir=%{_mandir} install


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(755,root,root) /sbin/mkbootdisk
%attr(644,root,root) %{_mandir}/man8/mkbootdisk.8*


%changelog
* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- rebuild with gcc4
- remove pre-Annvix changelog

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1-3avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1-2avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 1.5.1-1sls
- 1.5.1
- Requires: gawk rather than /bin/awk
- rediff P0, P1 (tvignaud)
- drop P2, P3 (tvignaud)

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.4.5-9sls
- minor spec cleanups

* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 1.4.5-8sls
- OpenSLS build
- tidy spec
