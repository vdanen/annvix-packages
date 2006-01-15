#
# spec file for package srv
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		srv
%define version 	0.21
%define release 	%_revrel

Summary:	Tool to manage runsv-controlled services
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Servers
URL:		http://annvix.org/cgi-bin/viewcvs.cgi/tools/srv/
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	dietlibc-devel

Requires:	runit >= 1.0.4, initscripts >= 7.06-41avx
Obsoletes:	supervise-scripts
Provides:	supervise-scripts

%description
A tool to manage runsv-controlled services.


%prep
%setup -q
%setup -q -n %{name}-%{version}


%build
diet gcc -Os -pipe nothing.c -o nothing


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{/sbin,%{_bindir},%{_sbindir},%{_mandir}/man8,%{_datadir}/srv}
install -m 0700 srv %{buildroot}%{_sbindir}
install -m 0644 srv.8 %{buildroot}%{_mandir}/man8
install -m 0755 nothing %{buildroot}%{_bindir}
install -m 0644 functions %{buildroot}%{_datadir}/srv


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sbindir}/srv
%{_bindir}/nothing
%{_datadir}/srv/functions
%{_mandir}/man8/srv.8*


%changelog
* Sun Jan 15 2006 Vincent Danen <vdanen-at-build.annvix.org>
- 0.21: properly manage the down file to save state across reboots

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Fri Oct 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.20-3avx
- don't display rpm package info if the run file doesn't belong to an rpm
- some --info tidying

* Sat Oct 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.20-2avx
- cosmetics and change the timeouts from 15s to 10s

* Mon Oct 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.20-1avx
- 0.20

* Fri Aug 26 2005 Sean P. Thomas <spt-at-build.annvix.org> 0.10-1avx
- 0.10

* Mon Aug 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9-5avx
- remove the srv-start and srv-stop scripts; they should never be used
- srv should be mode 0700 not 0755
- use dietlibc to compile nothing

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9-4avx
- bootstrap build

* Wed Oct 06 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9-3avx
- add %{_datadir}/srv/exceptions so we can have more services for
  process killing exceptions than just sshd; so far we have both
  sshd and mysqld here

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9-2avx
- add godown() function for a service to shut itself down if certain
  requirements (usually configuration-related) are not met

* Sat Sep 11 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9-1avx
- 0.9
- overhaul srv to work with runit (runsv) rather than daemontools (supervise);
  this can use more work but this should be a sufficient transition for now

* Thu Aug 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.7-2avx
- make srv *not* kill "rogue" sshd processes as that makes remote
  upgrades of sshd impossible

* Tue Jul 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.7-1avx
- remove srv-addinit and %%post scriptlet to add it to inittab; it's now
  done in initscripts
- add logging support to srv (logs to daemon.info)
- add external functions for run scripts to use (logging and to check
  for dependencies)
- add a final "super kill" for processes that fork and supervise can't
  kill (ie. smbd)

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.6-2avx
- fix really bad and stupid typeo in srv-stop
- give some feedback on starting and stopping supervise

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.6-1avx
- numerous fixes; there was some bad bash going on (this solves
  the problem with every service taking 15s to shutdown, they should
  be instant now)
- it is prefered to run svscan from init so that it can be restarted
  should something happen, so the initscript is gone
- don't remove the build directory by default
- move most of the files in %%{_bindir} to %%{_sbindir} because only
  root can really do anything with services

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.5-2avx
- Annvix build

* Tue May 11 2004 Vincent Danen <vdanen@opensls.org> 0.5-1sls
- 0.5:
  - nice overall status summary
  - fixed the handling of services that don't come with a log service

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 0.4-2sls
- fix from Oden to handle restarts better

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.4-1sls
- 0.4
- include Bruce's supervise-scripts (3.3)

* Mon Jan 26 2004 Vincent Danen <vdanen@opensls.org> 0.3-2sls
- include nothing

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 0.3-1sls
- 0.3

* Tue Jan 13 2004 Vincent Danen <vdanen@opensls.org> 0.2-1sls
- 0.2

* Sun Jan 11 2004 Vincent Danen <vdanen@opensls.org> 0.1-2sls
- PreReq: rpm-helper
- add %%post and %%preun service stuff

* Fri Jan 02 2004 Vincent Danen <vdanen@opensls.org> 0.1-1sls
- 0.1
