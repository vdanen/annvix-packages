# $Id: srv.spec,v 1.11 2004/08/19 16:34:10 vdanen Exp $

%define name	srv
%define version 0.7
%define release 2avx

Summary:	Tool to manage supervise-controlled services.
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Servers
URL:		http://annvix.org/cgi-bin/viewcvs.cgi/tools/srv/
Source:		%{name}-%{version}.tar.bz2
Source1:	http://em.ca/~bruceg/supervise-scripts/supervise-scripts-3.3.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-root

Requires:	daemontools >= 0.70, initscripts >= 7.06-41avx
Obsoletes:	supervise-scripts
Provides:	supervise-scripts
PreReq:		rpm-helper

%description
A tool to manage supervise-controlled services.


%prep
%setup -q
%setup -q -n %{name}-%{version} -D -T -a1

%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}
gcc nothing.c -o nothing

%install
mkdir -p %{buildroot}{/sbin,%{_bindir},%{_sbindir},%{_mandir}/man8,%{_datadir}/srv}
install -m 0755 srv %{buildroot}%{_sbindir}
install -m 0755 srv-start %{buildroot}/sbin
install -m 0755 srv-stop %{buildroot}/sbin
install -m 0644 srv.8 %{buildroot}%{_mandir}/man8
install -m 0755 nothing %{buildroot}%{_bindir}
install -m 0644 functions %{buildroot}%{_datadir}/srv

# supervise scripts
pushd supervise-scripts-3.3
make prefix=%{buildroot}%{_prefix} install
popd

# move manpages to appropriate location
mkdir -p %{buildroot}%{_mandir}/man1
mv -f %{buildroot}%{_prefix}/man/man1/* %{buildroot}%{_mandir}/man1

# remove unwanted files and move stuff around
rm -f %{buildroot}%{_bindir}/svscan*
mv %{buildroot}%{_bindir}/svc* %{buildroot}%{_sbindir}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
/sbin/srv-start
/sbin/srv-stop
%{_sbindir}/srv
%{_sbindir}/svc-add
%{_sbindir}/svc-isdown
%{_sbindir}/svc-isup
%{_sbindir}/svc-remove
%{_sbindir}/svc-start
%{_sbindir}/svc-status
%{_sbindir}/svc-stop
%{_sbindir}/svc-waitdown
%{_sbindir}/svc-waitup
%{_bindir}/nothing
%{_datadir}/srv/functions
%{_mandir}/man8/srv.8*
%{_mandir}/man1/svc-add.1*
%{_mandir}/man1/svc-remove.1*
%{_mandir}/man1/svc-start.1*
%{_mandir}/man1/svc-stop.1*

%changelog
* Thu Aug 19 2004 Vincent Danen <vdanen@annvix.org> 0.7-2avx
- make srv *not* kill "rogue" sshd processes as that makes remote
  upgrades of sshd impossible

* Tue Jul 27 2004 Vincent Danen <vdanen@annvix.org> 0.7-1avx
- remove srv-addinit and %%post scriptlet to add it to inittab; it's now
  done in initscripts
- add logging support to srv (logs to daemon.info)
- add external functions for run scripts to use (logging and to check
  for dependencies)
- add a final "super kill" for processes that fork and supervise can't
  kill (ie. smbd)

* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 0.6-2avx
- fix really bad and stupid typeo in srv-stop
- give some feedback on starting and stopping supervise

* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 0.6-1avx
- numerous fixes; there was some bad bash going on (this solves
  the problem with every service taking 15s to shutdown, they should
  be instant now)
- it is prefered to run svscan from init so that it can be restarted
  should something happen, so the initscript is gone
- don't remove the build directory by default
- move most of the files in %%{_bindir} to %%{_sbindir} because only
  root can really do anything with services

* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 0.5-2avx
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
