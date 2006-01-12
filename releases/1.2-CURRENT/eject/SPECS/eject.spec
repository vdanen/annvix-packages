#
# spec file for package eject
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		eject
%define version 	2.0.13
%define release		%_revrel

Summary:	A program that ejects removable media using software control
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://metalab.unc.edu/pub/Linux/utils/disk-management/
Source:		http://metalab.unc.edu/pub/Linux/utils/disk-management/eject-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext

%description
The eject program allows the user to eject removable media
(typically CD-ROMs, floppy disks or Iomega Jaz or Zip disks)
using software control. Eject can also control some multi-
disk CD changers and even some devices' auto-eject features.


%prep
%setup -q


%build
%configure
%make DEFAULTDEVICE="/dev/cdrom"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

%makeinstall ROOTDIR=%{buildroot} PREFIX=%{buildroot}/%{_prefix}

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO COPYING ChangeLog
%{_bindir}/eject
%{_bindir}/volname
%{_mandir}/man1/eject.1*
%{_mandir}/man1/volname.1*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13-9avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13-8avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13-7avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.0.13-6sls
- minor spec cleanups
- remove the supermount patch

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.0.13-5sls
- OpenSLS build
- tidy spec

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.0.13-4mdk
- adjust macro during since we dropped the prefix tag

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.0.13-3mdk
- rebuild
- drop prefix tag

* Tue Jan  7 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.13-2mdk
- Fix locales installation.

* Fri Dec 27 2002 Warly <warly@mandrakesoft.com> 2.0.13-1mdk
- new version

* Mon Jun  3 2002 Stefan van der Eijk <stefan@eijk.nu> 2.0.12-5mdk
- BuildRequires

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.12-4mdk
- Automated rebuild in gcc3.1 environment

* Mon Jan 28 2002 François Pons <fpons@mandrakesoft.com> 2.0.12-3mdk
- supermount patches from Andrej Borsenkow.

* Fri Jan 18 2002 Warly <warly@mandrakesoft.com> 2.0.12-2mdk
- rpmlint fixes

* Mon Oct 29 2001 Warly <warly@mandrakesoft.com> 2.0.12-1mdk
- new version

* Mon Sep 17 2001 Warly <warly@mandrakesoft.com> 2.0.10-2mdk
- added new fr_FR contributed by Christophe Combelles <combech@gemse.fr>

* Wed Jul 04 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0.10-1mdk
- New and shiny source which supports localizd strings (kewl).
- s/Copyright/License/, finally.

* Mon Jul 02 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0.7-2mdk
- Include the manual page for volname.

* Wed May 16 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0.7-1mdk
- Version 2.0.7 out for general consumption.

* Mon May 14 2001  Daouda Lo<daouda@mandrakesoft.com> 2.0.6-2mdk
- Resync rpm/srpm (happy nono? ) 

* Fri May 11 2001 Geoffrey Lee <snaitalk@mandrakesoft.com> 2.0.6-1mdk
- 2.0.6.
- Run ./configure.

* Sat May 05 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0.5-2mdk
- Include volname binary.

* Thu May 03 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.5-1mdk
- new release

* Tue May 01 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.4-1mdk
- new version

* Wed Apr 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0.3-1mdk
- A new and shiny source for folks on Anzac Day, and general cleanups.

* Thu Jul 20 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.2-8mdk
- BM
- specfile cleanup
- macrozashions

* Wed Mar 22 2000 Daouda Lo <daouda@mandrakesoft.com> 2.0.2-7mdk
- fix group

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Build Release.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Tue Feb 16 1999 Preston Brown <pbrown@redhat.com>
- solved a lot of problems by finding eject 2.0.2. :)

* Tue Feb 09 1999 Preston Brown <pbrown@redhat.com>
- patch to improve symlink handling folded into linux-2.2 patch

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Wed Jul 15 1998 Donnie Barnes <djb@redhat.com>
- added small patch to 1.5 for longer device names

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 15 1997 Donnie Barnes <djb@redhat.com>
- upgraded to 1.5
- various spec file clean ups
- eject rocks!

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
