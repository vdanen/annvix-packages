#
# spec file for package mdadm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mdadm
%define version		2.5.2
%define release		%_revrel

%define use_dietlibc 	0
%ifarch %{ix86} x86_64 ppc
%define use_dietlibc 	1
%endif

%define mdassemble_auto	%{nil}
#define mdassemble_auto	MDASSEMBLE_AUTO=1

# we want to install in /sbin, not /usr/sbin...
%define _exec_prefix	%{nil}

Summary:	A tool for managing Soft RAID under Linux
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.cse.unsw.edu.au/~neilb/source/mdadm/
Source:		http://www.kernel.org/pub/linux/utils/raid/mdadm/%{name}-%{version}.tar.bz2
Source2:	mdadm.run
Source3:	mdadm-log.run
Patch2:		mdadm-2.3.1-kernel-byteswap-include-fix.patch
Patch4:		mdadm-2.5-rand.patch


BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	man groff groff-for-man
%if %{use_dietlibc}
BuildRequires:	dietlibc-devel >= 0.29-5662avx
%endif

Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description 
mdadm is a program that can be used to create, manage, and monitor
Linux MD (Software RAID) devices.

As such is provides similar functionality to the raidtools packages.
The particular differences to raidtools is that mdadm is a single
program, and it can perform (almost) all functions without a
configuration file (that a config file can be used to help with
some common tasks).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
#%patch2 -p1 -b .asm-byteorder_h
%patch4 -p1 -b .rand

chmod 0644 ChangeLog


%build
%ifarch x86_64
COMP="diet x86_64-annvix-linux-gnu-gcc"
%else
COMP="diet gcc"
%endif

%if %{use_dietlibc}
make mdassemble CXFLAGS="%{optflags}" %{mdassemble_auto} SYSCONFDIR="%{_sysconfdir}" DIET_GCC="$COMP"
%endif
make CXFLAGS="%{optflags}" SYSCONFDIR="%{_sysconfdir}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make DESTDIR=%{buildroot} MANDIR=%{_mandir} BINDIR=%{_sbindir} install
install -D -m 0644 mdadm.conf-example %{buildroot}%{_sysconfdir}/mdadm.conf

%if %{use_dietlibc}
install mdassemble %{buildroot}%{_sbindir}/mdassemble
install -D -m 0644 mdassemble.8 %{buildroot}%{_mandir}/man8/mdassemble.8
%endif

mkdir -p %{buildroot}%{_srvdir}/mdadm/log
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/mdadm/run
install -m 0740 %{SOURCE3} %{buildroot}%{_srvdir}/mdadm/log/run


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%preun
%_preun_srv mdadm

%post
if [ -d /var/log/supervise/mdadm -a ! -d /var/log/service/mdadm ]; then
    mv /var/log/supervise/mdadm /var/log/service/
fi
%_post_srv mdadm


%files
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/mdadm
%if %{use_dietlibc}
%attr(0755,root,root) %{_sbindir}/mdassemble
%endif
%config(noreplace,missingok)/%{_sysconfdir}/mdadm.conf
%{_mandir}/man*/md*
%dir %attr(0750,root,admin) %{_srvdir}/mdadm
%dir %attr(0750,root,admin) %{_srvdir}/mdadm/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/mdadm/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/mdadm/log/run

%files doc
%defattr(-,root,root)
%doc TODO ChangeLog mdadm.conf-example ANNOUNCE* README.initramfs


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.2
- remove the docs from the main package

* Thu Jun 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.2
- 2.5.2 (fixes a bad memory leak in 2.5's --monitor mode)
- drop P0, P1, P3, P5, P6; fixed upstream
- don't apply P2 for now... its for handling big endian systems like
  ppc which we don't support, but the surrounding code changes are
  too heavy for me to easily port (if it's even required)

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- rebuild against and require dietlibc >= 0.29-5662avx

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- 2.5
- sync patches from Mandriva:
  - P0: snprintf fix (bluca)
  - P1: strict aliasing fix (bluca)
  - P2: fix #include for kernel byteswap function (cjw)
  - P3: check return status of all write/fwrite functions (bluca)
  - P4: use posix rand() instead of BSD random() (bluca)
  - P5: fix some issues with mdassemble (bluca)
  - P6: use provided SHA1 and don't like against openssl (oden)
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.12.0
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.12.0
- Obfuscate email addresses and new tagging
- Uncompress patches
- drop unused S1
- fix prereq
- dietlibc fixes

* Sat Oct 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.12.0-4avx
- the run script needs to look for mdadm.conf rather than amd.conf

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.12.0-3avx
- execline the runscript

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.12.0-2avx
- s/supervise/service/ in log/run

* Fri Sep 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.12.0-1avx
- 1.12.0
- use execlineb for run scripts
- move logdir to /var/log/service/mdadm
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9.0-5avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9.0-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9.0-3avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9.0-2avx
- use logger for logging

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9.0-1avx
- 1.9.0

* Fri Feb 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6.0-5avx
- rebuild against new dietlibc

* Tue Oct 05 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.6.0-4avx
- rebuild with updated scripts; seems I forgot to increment the revision

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.6.0-3avx
- update run scripts

* Mon Jun 14 2004 Thomas Backlund <tmb@annvix.org> 1.6.0-2avx
- swith to new name Annvix / avx

* Mon Jun 14 2004 Thomas Backlund <tmb@iki.fi> 1.6.0-1sls
- 1.6.0

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.5.0-2sls
- minor spec cleanups

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 1.5.0-1sls
- 1.5.0
- drop all upstream-applied patches
- supervise scripts

* Wed Jan 21 2004 Vincent Danen <vdanen@opensls.org> 1.4.0-6sls
- sync with 5mdk (Luca Berra):
  - added raid6 patches from hpa

* Sun Jan 11 2004 Vincent Danen <vdanen@opensls.org> 1.4.0-5sls
- OpenSLS build
- tidy spec
- don't use dietlibc if building for amd64

* Sun Dec 21 2003 Luca Berra <bluca@vodka.it> 1.4.0-4mdk
- service name is mdadm

* Sat Dec 20 2003 Luca Berra <bluca@vodka.it> 1.4.0-3mdk
- updated with more patches from Neil, mdassemble is going to be integrated upstream
- added mdmonitor (from rh)

* Sun Nov 02 2003 Luca Berra <bluca@vodka.it> 1.4.0-2mdk
- added mdassemble built with dietlibc

* Fri Oct 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.4.0-1mdk
- 1.4.0
- drop patches included in the upstream source

* Mon Sep 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 1.3.0-2mdk
- updated by Luca Berra <bluca@vodka.it>
 - added patches from upstream maintainer
- fix perms on doc file

* Tue Jul 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.0-1mdk
- 1.3.0

* Fri Apr 25 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.2.0-2mdk
- fix buildrequires, thanks to Stefan van der Eijks robot

* Sun Mar 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.2.0-1mdk
- 1.2.0

* Mon Mar 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.1.0-1mdk
- 1.1.0
- misc spec file fixes

* Thu Jan 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.0.1-3mdk
- build release

* Sun Aug  4 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.0.1-2mdk
- rebuilt with gcc-3.2

* Mon Jun 10 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.0.1-1mdk
- 1.0.1
- capitalized summary to please rpmlint

* Mon May 20 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.0.0-2mdk
- rebuilt with gcc3.1

* Sat May 11 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.0.0-1mdk
- new version

* Sat May 11 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.2-1mdk
- initial cooker contrib
- used provided spec file
