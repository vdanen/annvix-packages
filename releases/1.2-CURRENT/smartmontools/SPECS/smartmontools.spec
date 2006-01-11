#
# spec file for package smartmontools
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		smartmontools
%define version 	5.33
%define release 	%_revrel

Summary:	SMARTmontools - for monitoring S.M.A.R.T. disks and devices
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:	GPL
Group:		System/Kernel and hardware
URL:            http://smartmontools.sourceforge.net/
Source0:	%{name}-%{version}.tar.gz
Source1:	smartd.run
Source2:	smartd-log.run
Source3:	%{name}-%{version}.tar.gz.asc

BuildRoot:      %{_buildroot}/%{name}-%{version}

Obsoletes:	smartsuite
Provides:	smartsuite
Requires(post):	rpm-helper
Requires(preun): rpm-helper


%description 
SMARTmontools controls and monitors storage devices using the
Self-Monitoring, Analysis and Reporting Technology System (S.M.A.R.T.)
build into ATA and SCSI Hard Drives. This is used to check the
reliability of the hard drive and predict drive failures. The suite
contains two utilities.  The first, smartctl, is a command line
utility designed to perform simple S.M.A.R.T. tasks. The second,
smartd, is a daemon that periodically monitors smart status and
reports errors to syslog.  The package is compatible with the
ATA/ATAPI-5 specification.  Future releases will be compatible with
the ATA/ATAPI-6 and ATA/ATAPI-7 specifications.  The package is
intended to incorporate as much "vendor specific" and "reserved"
information as possible about disk drives.  man smartctl and man
smartd will provide more information.


%prep
%setup -q


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_srvdir}/smartd/log
install -m 0740 %{SOURCE1} %{buildroot}%{_srvdir}/smartd/run
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/smartd/log/run
rm -rf %{buildroot}%{_initrddir}

mkdir -p %{buildroot}%{_srvdir}/smartd/env
echo "1800" > %{buildroot}%{_srvdir}/smartd/env/INTERVAL


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ -d /var/log/supervise/smartd -a ! -d /var/log/service/smartd ]; then
    mv /var/log/supervise/smartd /var/log/service/
fi
%_post_srv smartd

%preun
%_preun_srv smartd


%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}
%config(noreplace) %{_sysconfdir}/smartd.conf
%{_sbindir}/smartd
%{_sbindir}/smartctl
%{_mandir}/man5/smartd.conf.5*
%{_mandir}/man8/smartd.8*
%{_mandir}/man8/smartctl.8*
%dir %attr(0750,root,admin) %{_srvdir}/smartd
%dir %attr(0750,root,admin) %{_srvdir}/smartd/log
%dir %attr(0750,root,admin) %{_srvdir}/smartd/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/smartd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/smartd/log/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/smartd/env/INTERVAL


%changelog
* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.33-7avx
- execline runscript
- created env directory
- drop the sysconfig file

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.33-6avx
- s/supervise/service/ in log/run

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.33-5avx
- use execlineb for run scripts
- move logdir to /var/log/service/smartd
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.33-4avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.33-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.33-2avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.33-1avx
- 5.33
- use logger for logging

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.26-6avx
- update run scripts

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.26-5avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 5.26-4sls
- minor spec cleanups
- srv macros

* Mon Dec 29 2003 Vincent Danen <vdanen@opensls.org> 5.26-3sls
- supervise scripts
- remove initscript
- create /etc/sysconfig/smartd to configure polling interval
- don't be lazy in the %%files listing

* Mon Dec 29 2003 Vincent Danen <vdanen@opensls.org> 5.26-2sls
- OpenSLS build
- tidy spec

* Thu Dec 4 2003 Erwan Velu <erwan@mandrakesoft.com> 5.26-1mdk
- New release
- Release are too fast theses days :)

* Thu Nov 27 2003 Erwan Velu <erwan@mandrakesoft.com> 5.25-1mdk
- New release
- Fixing changelog entries :)
- Removing Patch1 (merged upstream)

* Mon Nov 1 2003 Erwan Velu <erwan@mandrakesoft.com> 5.1-23mdk
- New release

* Sat Nov 01 2003 Abel Cheung <deaddog@deaddog.org> 5.22-2mdk
- don't restart smartd multiple times

* Thu Oct 30 2003 Erwan Velu <erwan@mandrakesoft.com> 5.1-22.1mdk
- Jump to Release 22 (release are quick theses days :) )
- Removing patch1 (Mandrake is redhat compliant for initscripts)
- Adding autorestart on updates

* Sat Oct 04 2003 Abel Cheung <deaddog@deaddog.org> 5.19-1mdk
- 5.19 (no subrelease version number now)
- When upgrading, solely use rpm-helper scripts to start/stop service.
  It will be effective after next rpm update. (#5996)
- Obsoletes UCSC smartsuite instead of conflicts, looks like smartsuite
  is no longer maintained
- Rediff patch1

* Tue Sep 23 2003 Erwan Velu <erwan@mandrakesoft.com> 5.1-18.1mdk
- New release
* Tue Aug 12 2003 Lenny Cartier <lenny@mandrakesoft.com> 5.1-14.2mdk
- rebuild

* Wed Jun 18 2003 Erwan Velu <erwan@mandrakesoft.com> 5.1-14.1mdk
- Subrelease 14

* Wed May 07 2003 Lenny Cartier <lenny@mandrakesoft.com> 5.1-10.1mdk
- subrelease 10

* Fri Mar 28 2003 Erwan Velu <erwan@mandrakesoft.com> 5.1-9.2mdk
- Adding examplescript dir in /usr/share/doc/ (Thx to Bruce Allen)

* Mon Mar 24 2003 Erwan Velu <erwan@mandrakesoft.com> 5.1-9.1mdk
- New version
- Removing patch0
- Including missing files

* Thu Jan 16 2003 Erwan Velu <erwan@mandrakesoft.com> 5.0-8.2mdk
- Rebuild for new glibc

* Tue Oct 15 2002 Erwan Velu <erwan@mandrakesoft.com> 5.0-8.1mdk
- First mdk release

* Mon Oct 14 2002  Bruce Allen smartmontools-support@lists.sourceforge.net
Initial release.  Code is derived from smartsuite, and is
   intended to be compatible with the ATA/ATAPI-5 specifications.
