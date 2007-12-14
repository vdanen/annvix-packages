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
%define version		3.2.7
%define release		%_revrel

Summary:	Utilities for monitoring your system and processes on your system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://procps.sf.net/
Source:		http://procps.sourceforge.net/%{name}-%{version}.tar.gz
Patch0:		procps-3.2.3-sysctlshutup.patch
Patch1:		procps-3.2.7-mdv-fix-buffer-overflow.patch
Patch2:		procps-3.2.7-mdv-dont-strip.patch
Patch3:		procps-3.2.5-fdr-top-rc.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel

Provides:	procps3
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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0 -b .sysctl
%patch1 -p1 -b .fix-buffer-overflow
%patch2 -p1 -b .dont-strip
%patch3 -p1 -b .top-rc


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

%files doc
%defattr(-,root,root)
%doc NEWS BUGS TODO


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.2.7
- rebuild against new ncurses

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.2.7
- 3.2.7
- drop P1, P2: no longer required
- P1: fix a buffer overflow in sysctl
- P2: don't strip binaries
- P3: fix bad saving of .toprc files
- drop the provides on libproc.so.3.1 as I have no idea why it's there

* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2.6
- rebuild against new ncurses
- clean spec

* Thu Jun 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2.6
- 3.2.6
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2.5
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2.5
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
