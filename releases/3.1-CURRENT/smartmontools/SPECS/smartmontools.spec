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
%define version 	5.36
%define release 	%_revrel

Summary:	SMARTmontools - for monitoring S.M.A.R.T. disks and devices
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:	GPL
Group:		System/Kernel and hardware
URL:            http://smartmontools.sourceforge.net/
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}.tar.gz.asc
Source2:	smartd.run
Source3:	smartd-log.run

BuildRoot:      %{_buildroot}/%{name}-%{version}

Obsoletes:	smartsuite
Provides:	smartsuite
Requires(pre):	setup
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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%serverbuild
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_srvdir}/smartd/log
install -m 0740 %{_sourcedir}/smartd.run %{buildroot}%{_srvdir}/smartd/run
install -m 0740 %{_sourcedir}/smartd-log.run %{buildroot}%{_srvdir}/smartd/log/run
rm -rf %{buildroot}%{_sysconfdir}/rc.d

mkdir -p %{buildroot}%{_srvdir}/smartd/env
echo "1800" > %{buildroot}%{_srvdir}/smartd/env/INTERVAL


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_srv smartd

%preun
%_preun_srv smartd


%files
%defattr(-,root,root)
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

%files doc
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}


%changelog
* Thu Nov 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.36
- rebuild

* Tue Dec 26 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.36
- use %%serverbuild

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.36
- requires setup (for group admin)
- spec cleanups

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.36
- 5.36
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.33
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.33
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
