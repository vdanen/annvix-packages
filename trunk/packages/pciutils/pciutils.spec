Name:		pciutils
Version:	2.1.11
Release:	4mdk
Source0:	ftp://atrey.karlin.mff.cuni.cz/pub/linux/pci/%{name}-%{version}.tar.bz2
URL:		http://atrey.karlin.mff.cuni.cz/~mj/pciutils.html
Patch1:		pciutils-bufsiz.patch.bz2
Patch10:	pciutils-2.1.11-pcimodules.patch.bz2
Patch11:	pciutils-2.1.6-cardbusonlywhenroot.patch.bz2
Patch12:	pciutils-2.1.9-unused.patch.bz2
Patch13:	pciutils-2.1.10-x86_64.patch.bz2
License:	GPL
Buildroot:	%{_tmppath}/%{name}-%{version}-root
Requires:	kernel >= 2.1.82
BuildRequires:	wget
Summary:	PCI bus related utilities.
Group:		System/Kernel and hardware

%description
This package contains various utilities for inspecting and setting
devices connected to the PCI bus. The utilities provided require
kernel version 2.1.82 or newer (supporting the /proc/bus/pci
interface).

%package devel
Summary: Linux PCI development library
Group: Development/C
Requires: %{name} = %{version}

%description devel
This package contains a library for inspecting and setting
devices connected to the PCI bus.

%prep
%setup -q
%patch11 -p1
%patch1 -p1 -b .bufsiz
%patch10 -p1
%patch12 -p1 -b .unused
%patch13 -p1 -b .x86_64

./update-pciids.sh

%build
make PREFIX=/usr OPT="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%_bindir,%_mandir/man8,%_datadir,%_libdir,%_includedir/pci}

install -s pcimodules lspci setpci $RPM_BUILD_ROOT%_bindir
install -m 644 pcimodules.man lspci.8 setpci.8 $RPM_BUILD_ROOT%_mandir/man8
install -m 644 pci.ids $RPM_BUILD_ROOT%_datadir
install -m 644 lib/libpci.a $RPM_BUILD_ROOT%_libdir
install -m 644 lib/{pci.h,header.h,config.h} $RPM_BUILD_ROOT%_includedir/pci

%files
%defattr(-, root, root)
%doc README ChangeLog pciutils.lsm
%{_mandir}/man8/*
%{_bindir}/*
%{_datadir}/pci.ids

%files devel
%defattr(-, root, root)
%doc TODO
%_libdir/*.a
%_includedir/pci

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
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
- removed %config for pci.ids (someone was zealous here?)
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
