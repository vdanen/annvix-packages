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
%define version		2.1.99.test8
%define release		%_revrel

%define rver		2.1.99-test8

Summary:	PCI bus related utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://atrey.karlin.mff.cuni.cz/~mj/pciutils.html
Source0:	ftp://atrey.karlin.mff.cuni.cz/pub/linux/pci/alpha/%{name}-%{rver}.tar.gz
Patch0:		pciutils-strip.patch
Patch1:		pciutils-pciids.patch
Patch2:		pciutils-2.1.10-scan.patch
Patch3: 	pciutils-havepread.patch
Patch4:		pciutils-2.1.99-test3-amd64.patch
Patch5:		pciutils-typo.patch
Patch6:		pciutils-devicetype.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
%ifarch %{ix86}
BuildRequires:	dietlibc-devel
%endif

Requires:	kernel >= 2.1.82, hwdata

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
%setup -q -n %{name}-%{rver}
%patch0 -p1 -b .strip
%patch1 -p1 -b .pciids
%patch2 -p1 -b .scan
%patch3 -p1 -b .pread
#%patch4 -p1 -b .amd64
%patch5 -p1 -b .typo
%patch6 -p1 -b .devicetype


%build
%ifarch %{ix86}
#make OPT="%{optflags} -fno-stack-protector -D_GNU_SOURCE=1" CC="diet gcc" PREFIX="/usr"
make OPT="%{optflags} -D_GNU_SOURCE=1" CC="diet gcc" PREFIX="/usr"
mv lib/libpci.a lib/libpci_loader_a
make clean
%endif

make OPT="%{optflags} -D_GNU_SOURCE=1" PREFIX="/usr"


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

* Thu Aug 14 2003 Pixel <pixel@mandrakesoft.com> 2.1.11-4mdk
- distlint DIRM fix: own /usr/include/pci
- get latest pci.ids

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.1.11-3mdk
- buildrequires

* Thu Feb 27 2003 Pixel <pixel@mandrakesoft.com> 2.1.11-2mdk
- get latest pci.ids

* Sat Jan  4 2003 Pixel <pixel@mandrakesoft.com> 2.1.11-1mdk
- new release
- replace "make update-ids" with "./update-pciids.sh"

* Wed Jun 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.10-2mdk
- rebuild with latest gcc, get latest pci.ids

* Fri Apr 26 2002 Pixel <pixel@mandrakesoft.com> 2.1.10-1mdk
- new release
- use "make update-ids" to get latest pci.ids
- update patch10, drop patch2 (included upstream)

* Thu Apr 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.9-4mdk
- Patch12: apply "unused" attribute to the parameter, not to its type

* Tue Apr 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.1.9-3mdk
- resync with rh-2.1.9-3
- in order to ease comparison with rh:
  patch1 -> patch11, patch2 -> patch1, patch5 -> patch2
- remove old commented refererences to merged patches
- removing -Werror is needed only for alpha, it seems
- better description
- add -b flags to patches
- remove uneeded Prefix:

* Sun Feb 10 2002 Pixel <pixel@mandrakesoft.com> 2.1.9-2mdk
- removing patch 3 & 4 which *are* merged upstream

* Fri Feb  8 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 2.1.9-1mdk
- Version 2.1.9.
- Removed Patch 6, 7, 8 and 9, merged upstream.
- Commented out Patch 3 and 4, likely merged upstream.

* Thu Oct 11 2001 Pixel <pixel@mandrakesoft.com> 2.1.8-8mdk
- make rpmlint happy

* Tue Jun 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.8-7mdk
- Add pcimodules.

* Tue Nov  7 2000 Pixel <pixel@mandrakesoft.com> 2.1.8-6mdk
- add require for -devel

* Mon Sep 25 2000 Pixel <pixel@mandrakesoft.com> 2.1.8-5mdk
- include pci.ids patch from redhat

* Sun Sep  3 2000 Pixel <pixel@mandrakesoft.com> 2.1.8-4mdk
- fix the license

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 2.1.8-3mdk
- BM

* Wed Jun 28 2000 Pixel <pixel@mandrakesoft.com> 2.1.8-2mdk
- cleanup
- add redhat's patch

* Tue Jun  6 2000 Pixel <pixel@mandrakesoft.com> 2.1.8-1mdk
- new version

* Tue Apr 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.6-2mdk
- move lspci to /usr/bin since it's userspace.
- Read Cardbus info only when we are root.
- Clean-up specs.

* Mon Apr 17 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 2.1.6-1mdk
- 2.1.6
- new BuildRoot
- remove ExcludeArch armv4l
- add TODO as pciutils-devel documentation

* Sat Mar 25 2000 Pixel <pixel@mandrakesoft.com> 2.1.5-2mdk
- new group

* Wed Feb 16 2000 Pixel <pixel@mandrakesoft.com> 2.1.5-1mdk
- new version

* Sun Nov 21 1999 Pixel <pixel@mandrakesoft.com>
- removed %%config for pci.ids (someone was zealous here?)
- changed 0711 to 0755 for lspci (makes rpmlint happy :)

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- s/=>/>=//g in Requires:.

* Sun Oct 31 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 2.1 final.

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.1-pre8.

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- NMU: Build release.

* Fri Oct  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add pciutils-devel package.

* Fri Aug 13 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 2.1pre5
- cleaning spec

* Thu Jul 15 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- update to 2.1-pre4.tar.bz2

* Wed May 19 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- 2.0

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Mon Apr 19 1999 Jakub Jelinek  <jj@ultra.linux.cz>
- update to 1.99.5
- fix sparc64 operation

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Thu Feb  4 1999 Bill Nottingham <notting@redhat.com>
- initial build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
