%define	name	symlinks
%define	version	1.2
%define release	15mdk

Summary:	A utility which maintains a system's symbolic links.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		File tools
License:	BSD-style
Source0:	ftp://sunsite.unc.edu/pub/Linux/utils/file/%{name}-%{version}.tar.bz2
URL:		http://www.ibiblio.org/pub/Linux/utils/file/
Patch0:		%{name}-1.2-noroot.patch.bz2
Buildrequires:	glibc-static-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The symlinks utility performs maintenance on symbolic links.  Symlinks
checks for symlink problems, including dangling symlinks which point to
nonexistent files.  Symlinks can also automatically convert absolute
symlinks to relative symlinks.

Install the symlinks package if you need a program for maintaining
symlinks on your system.

%prep
%setup -q
%patch0 -p1

%build
perl -p -i -e "s/-O2/$RPM_OPT_FLAGS/" Makefile
%make

%install
rm -rf $RPM_BUILD_ROOT
install -s -m 755 %{name} -D $RPM_BUILD_ROOT%{_bindir}/%{name}
install -m 644 %{name}.8 -D $RPM_BUILD_ROOT%{_mandir}/man8/%{name}.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*

%changelog
* Thu Jul 24 2003 Götz Waschk <waschk@linux-mandrake.com> 1.2-15mdk
- fix buildrequires

* Mon Jul 14 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.2-14mdk
- quiet setup
- macroize
- cosmetics
- rm -rf $RPM_BUILD_ROOT in %%install

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
