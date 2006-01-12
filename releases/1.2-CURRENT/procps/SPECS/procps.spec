#
# spec file for package procps
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		procps
%define version		3.2.5
%define release		%_revrel

Summary:	Utilities for monitoring your system and processes on your system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://procps.sf.net/
Source:		http://procps.sourceforge.net/%{name}-%{version}.tar.bz2
Patch0:		procps-3.2.3-sysctlshutup.patch
Patch1:		procps-3.2.3-perm-top.patch
Patch2:		procps-3.2.3-perror.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel

Provides:	libproc.so.3.1 procps3
Obsoletes:	procps3
Requires(post):	coreutils

%description
The procps package contains a set of system utilities which provide system
information.

Procps includes ps, free, skill, snice, tload, top, uptime, vmstat, w
and watch.

  * The ps command displays a snapshot of running processes.
  * The top command provides a repetitive update of the statuses of running
    processes.
  * The free command displays the amounts of free and used memory on your
    system.
  * The skill command sends a terminate command (or another specified signal)
    to a specified set of processes.
  * The snice command is used to change the scheduling priority of specified
    processes.
  * The tload command prints a graph of the current system load average to a
    specified tty.
  * The uptime command displays the current time, how long the system has been
    running, how many users are logged on and system load averages for the past
    one, five and fifteen minutes. 
  * The w command displays a list of the users who are currently logged on and
    what they're running.
  * The watch program watches a running program.
  * The vmstat command displays virtual memory statistics about processes,
    memory, paging, block I/O, traps and CPU activity.


%package devel
Group:		Development/C
Summary:	Development and headers files for the proc library
Requires:	%{name} = %{version}

%description devel
Development headers and library for the proc library.


%prep
%setup -q
%patch0 -p0 -b .sysctl
%patch1 -p1 -b .perm-top
%patch2 -p1 -b .perror


%build
make CC="gcc %{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
PATH=/sbin:$PATH
mkdir -p %{buildroot}{{/usr,}/bin,/sbin,%{_mandir}/man{1,5,8},%{_lib}}

%makeinstall_std ldconfig=/bin/true install="install -D" lib="%{buildroot}/%{_lib}/"

rm -f %{buildroot}%{_mandir}/man1/kill.1*

mkdir -p %{buildroot}%{_includedir}/procps
install -m 0644 proc/*.h %{buildroot}%{_includedir}/procps

# This would conflict with util-linux:
mv %{buildroot}/bin/{,procps3-}kill

ln -s libproc-%version.so $RPM_BUILD_ROOT/%_lib/libproc.so

# quiet spec-helper:
chmod +w $RPM_BUILD_ROOT/{bin,sbin,usr/bin,%_lib}/*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post 
/sbin/ldconfig
# remove obsolete files
rm -f /etc/psdevtab /etc/psdatabase

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc NEWS BUGS TODO
/%{_lib}/libproc-*.so
/bin/procps3-kill
/bin/ps
/sbin/sysctl
%{_bindir}/free
%{_bindir}/pgrep
%{_bindir}/pmap
%{_bindir}/pwdx
%{_bindir}/pkill
%{_bindir}/skill
%{_bindir}/slabtop
%{_bindir}/snice
%{_bindir}/tload
%{_bindir}/top
%{_bindir}/uptime
%{_bindir}/vmstat
%{_bindir}/w
%{_bindir}/watch
%{_mandir}/man1/free.1*
%{_mandir}/man1/pgrep.1*
%{_mandir}/man1/pkill.1*
%{_mandir}/man1/pmap.1*
%{_mandir}/man1/pwdx.1*
%{_mandir}/man1/ps.1*
%{_mandir}/man1/skill.1*
%{_mandir}/man1/slabtop.1*
%{_mandir}/man1/snice.1*
%{_mandir}/man1/tload.1*
%{_mandir}/man1/top.1*
%{_mandir}/man1/uptime.1*
%{_mandir}/man1/w.1*
%{_mandir}/man1/watch.1*
%{_mandir}/man5/sysctl.conf.5*
%{_mandir}/man8/sysctl.8*
%{_mandir}/man8/vmstat.8*

%files devel
%defattr(-,root,root)
%{_includedir}/procps/*
/%{_lib}/libproc.so


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.2.5-1avx
- 3.2.5
- update patches from mandriva:
  - P0: fix -f option; manpage merge back bits lost for 2 years
  - P1: pgrep, pmap, w, top: fix segfault in msec 5
  - P2: display a better message for other apps when proc isn't accessible
- rename spec file

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.2.1-5avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.2.1-4avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.2.1-3avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.2.1-2avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 3.2.1-1sls
- PreReq: coreutils, not /bin/rm
- 3.2.1
- rediff P0

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.1.11-4sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 3.1.11-3sls
- OpenSLS build
- tidy spec

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 11-2mdk
- lib64 fixes

* Mon Jul 14 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.11-1mdk
- new release

* Thu Jun 26 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.9-4mdk
- further cleanups

* Tue Jun 24 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.9-3mdk
- spec cleanups from Albert Cahalan

* Sun Jun 15 2003 Stefan van der Eijk <stefan@eijk.nu> 3.1.9-2mdk
- BuildRequires

* Thu Jun 05 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.9-1mdk
- new release
- remove patch 1 (merged upstream)

* Mon Mar 31 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.8-1mdk
- new release
- patch 1 : fix suspending (c-z) that got broken between 3.1.6 and 3.1.8

* Tue Mar  4 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 3.1.6-2mdk
- Rebuild
- Seems there was a problem uploading this package, the -devel package is
  still at version 3.1.5!!!

* Mon Feb 17 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.6-1mdk
- new release

* Tue Jan 21 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.5-3mdk
- procps3 is dead, viva el procps3

* Wed Jan 15 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.5-2mdk
- patch 0 : shut up sysctl

* Wed Jan 08 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.5-1mdk
- new release

* Wed Dec 18 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.4-1mdk
- new release

* Wed Dec 18 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.1-2mdk
- new release : switch to debian fork (conflict with std procps for now)
- patch 50 : don't run ldconfig in %%install
- cleanups
- add pmap
- prevent conflicting with util-linux

* Wed Oct 09 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.10-2mdk
- patch50: top fix (J.A. Magallon)

* Wed Oct 09 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.10-1mdk
- new release
- fix url

* Wed Aug 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.7-14mdk
- add url (Yura Gusev)
- rpmlint fixes

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2-13mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Wed Jul 31 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.7-12mdk
- rpmlint fixes: strange-permission, hardcoded-library-path

* Mon Mar 18 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.0.7-11mdk
- patch from OpenWall to have a working w with the secure kernel. (Martin Maèok)

* Wed Feb 27 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.7-10mdk
- Make uptime report more than 200 days (Caleb Crome <ccrome@yahoo.com>).

* Mon Apr  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.7-9mdk
- Readapt my shutupmsg patch of the last year ago ;p.

* Mon Apr  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.7-8mdk
- Merge rh patches.

* Thu Nov 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.7-7mdk
- Prereq: /bin/rm (Pedro Rosa <prosa@ksu.ru>)

* Tue Sep 05 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.0.7-6mdk
- Added a patch for the bug when locale aren't set to 'en' and top kill
  terminal.
- bzip all patch.

* Wed Aug  9 2000 Alexandre Dussart <adussart@mandrakesoft.com> 2.0.7-5mdk
- Headers go to /usr/include/procps now.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2-4mdk
- automatically added BuildRequires

* Tue Aug  1 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.7-3mdk
- Remove kill manpage to avoid conflicts with util-linux.

* Fri Jul 21 2000 David BAUDENS <baudens@mandrakesoft.com> 2.0.7-2mdk
- Human readble description
- Use %%{_buildroot} for BuildRoot

* Fri Jul 21 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.0.7-1mdk
- updated.
- removed not needed anymore patch : 
	- procps-proto-fix.patch.bz2 
	- procps-2.0.6-sysmap.patch.bz2
	- procps-2.0.6-include.patch.bz2
	- procps-2.0.6-Makefile.patch.bz2
- added patch procps-2.0.7-makefile.patch
- install new manpages / binary.
- create man5 directory.
- pass mandir as a make argument.

* Wed May 17 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.0.6-13mdk
- added devel package.

* Wed May 17 2000 Frederic Lepied <flepied@mandrakesoft.com> %{major_version}.%{minor_version}.%{revision}-13mdk
- added 

* Thu Apr 13 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> %{version}-12mdk
- fix postin / postun.
- .so in devel package

* Tue Mar 28 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.0.6-11mdk
- Added a patch to fix an include compile time problem with new glibc.
- Fix group.
- Url wasn't pointing to the main procps site.

* Mon Mar 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.6-9mdk
- Fix sysctly_shut_your_mouth patch.

* Sun Mar 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.6-8mdk
- By default shut up the mouth of sysctl (and add the -v option to verbose it).

* Sat Mar 11 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.6-7mdk
- Add /sbin/sysctl in %files.

* Tue Jan 18 2000 Francis Galiegue <francis@mandrakesoft.com>
- Fixed a wrong function prototype which made sparc's ps try to divide by zero

* Mon Jan 3 2000 Florent Villard <warly@mandrakesoft.com> 2.0.6-5mdk
- fix libproc.so problem

* Fri Dec 31 1999 Florent Villard <warly@mandrakesoft.com> 2.0.6-4mdk
- add link /lib/libproc.so to /lib/libproc.so.2.0.6

* Thu Dec 30 1999 Florent Villard <warly@mandrakesoft.com> 2.0.6-3mdk
- correct path permissions

* Sun Nov 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Provides: libproc.so.2.0

* Thu Nov  4 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.0.6.

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.0.5.
- include more manpages.

* Fri Aug 13 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- fix bogus permissions on doc (it was only availlable to root)

* Tue Jul  6 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Rebuild w/ prereq dev

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- FIx small bug with the /usr/X11R6/bin/

* Sun Apr 11 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- bzip2 man pages
- update to 2.0.2
- add de locale
- Mandrake adaptions
