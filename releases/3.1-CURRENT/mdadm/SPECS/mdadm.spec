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
%define version		2.6.4
%define release		%_revrel

%define use_dietlibc 	0
%ifarch %{ix86} x86_64 ppc
%define use_dietlibc 	1
%endif

# cannot build with SSP
%define _ssp_cflags	%nil

%define mdassemble_auto	"MDASSEMBLE_AUTO=1"

# we want to install in /sbin, not /usr/sbin...
%define _exec_prefix	%{nil}

Summary:	A tool for managing Soft RAID under Linux
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.cse.unsw.edu.au/~neilb/source/mdadm/
Source0:	http://www.kernel.org/pub/linux/utils/raid/mdadm/%{name}-%{version}.tar.bz2
Source1:	mdadm.run
Source2:	mdadm-log.run
Patch0:		mdadm-2.6.2-mdv-werror.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	man
BuildRequires:	groff
BuildRequires:	groff-for-man
%if %{use_dietlibc}
BuildRequires:	dietlibc-devel >= 0.29-5662avx
%endif

Requires(pre):	setup
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
%patch0 -p1 -b .werror

perl -pi -e 's|-Werror||' Makefile

chmod 0644 ChangeLog


%build
%ifarch x86_64
COMP="diet x86_64-annvix-linux-gnu-gcc"
%else
COMP="diet gcc"
%endif

%if %{use_dietlibc}
make CXFLAGS="%{optflags}" %{mdassemble_auto} SYSCONFDIR="%{_sysconfdir}" DIET_GCC="$COMP" mdassemble
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
install -m 0740 %{_sourcedir}/mdadm.run %{buildroot}%{_srvdir}/mdadm/run
install -m 0740 %{_sourcedir}/mdadm-log.run %{buildroot}%{_srvdir}/mdadm/log/run


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%preun
%_preun_srv mdadm

%post
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
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4
- remove -Werror to fix the build

* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4
- 2.6.4

* Mon Jun 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2
- 2.6.2
- drop P0
- P0: fix -Werror

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.6
- really fix auto-assembly

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.6
- 2.5.6
- re-enable auto-assembly and fix bug#35
- drop P2; it was unapplied and doesn't apply to either x86 or x86_64

* Thu Oct 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4
- disable MDASSEMBLE_AUTO again; it was due to dietlibc that it
  was disabled in the first place (see bug #35)

* Thu Oct 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4
- 2.5.4
- re-enable auto-assembly (not sure when this was removed, but re-enable
  it even if it doesn't seem to work properly)

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.2
- requires setup (for group admin)
- spec cleanups

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
