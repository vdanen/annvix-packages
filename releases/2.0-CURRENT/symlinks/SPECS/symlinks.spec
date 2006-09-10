#
# spec file for package symlinks
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	revision	$Rev$
%define	name		symlinks
%define	version		1.2
%define release		%_revrel

Summary:	A utility which maintains a system's symbolic links
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		File tools
License:	BSD-style
URL:		http://www.ibiblio.org/pub/Linux/utils/file/
Source0:	ftp://sunsite.unc.edu/pub/Linux/utils/file/%{name}-%{version}.tar.bz2
Patch0:		symlinks-1.2-mdk-noroot.patch
Patch1:		symlinks-1.2-mdk-static.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glibc-static-devel

%description
The symlinks utility performs maintenance on symbolic links.  Symlinks
checks for symlink problems, including dangling symlinks which point to
nonexistent files.  Symlinks can also automatically convert absolute
symlinks to relative symlinks.


%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .static


%build
%make CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -s -m 0755 %{name} -D %{buildroot}%{_bindir}/%{name}
install -m 0644 %{name}.8 -D %{buildroot}%{_mandir}/man8/%{name}.8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org>
- rebuild with gcc4
- pass %%optflags directly to make rather than mess with the Makefile

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2-21avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2-20avx
- rebuild for new gcc
- P1: fix static build (gbeauchesne)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2-19avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2-18avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.2-17sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 1.2-16sls
- OpenSLS build
- tidy spec

* Thu Jul 24 2003 Götz Waschk <waschk@linux-mandrake.com> 1.2-15mdk
- fix buildrequires

* Mon Jul 14 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.2-14mdk
- quiet setup
- macroize
- cosmetics
- rm -rf %{buildroot} in %%install

* Tue Apr 29 2003 Daouda LO <daouda@mandrakesoft.com> 1.2-13mdk
- Buildrequires
- add URL

* Thu Oct 18 2001 Daouda LO <daouda@mandrakesoft.com> 1.2-12mdk
- rpmlint compliant

* Mon Jul 30 2001 Daouda LO <daouda@mandrakesoft.com> 1.2-11mdk
- rebuild (not done since Jul 26 2000!) 
- spec cleanups

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2-10mdk
- use tmppath

* Thu Jul 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2-9mdk
- let spec-helper compress, strip and the like
- BM, macros

* Thu Mar 23 2000 Daouda Lo <daouda@mandrakesoft.com> 1.2-8mdk
- fix group for 7.1

* Tue Nov 30 1999 Florent Villard <warly@mandrakesoft.com>
- built in new environment
- clean Makefile

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 20 1997 Otto Hammersmith <otto@redhat.com>
- changed build root to /var/tmp, not /var/lib
- updated to version 1.2

* Wed Jul 09 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- build-rooted

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
