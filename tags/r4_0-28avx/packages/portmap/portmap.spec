%define name	portmap
%define version	4.0
%define release	28avx
%define ver	4

Summary:	A program which manages RPC connections
Name:		portmap
Version:	%{version}
Release:	%{release}
Group:		System/Servers
License:	BSD
URL:		ftp://ftp.porcupine.org/pub/security/index.html
Source0:	ftp://coast.cs.purdue.edu:/pub/tools/unix/netutils/portmap/portmap_%{ver}.tar.bz2
Source1:	portmap.sysconfig
Source2:	pmap_set.8.bz2
Source3:	pmap_dump.8.bz2
Source4:	portmap.8.bz2
Source5:	portmap.run
Source6:	portmap-log.run
Patch0:		portmap-4.0-linux.patch.bz2
Patch1:		portmap-malloc.patch.bz2
Patch2:		portmap-4.0-cleanup.patch.bz2
Patch3:		portmap-4.0-rpc_user.patch.bz2
Patch4:		portmap-4.0-sigpipe.patch.bz2
Patch5:		portmap-4.0-errno.patch.bz2
Patch6:		portmap-4.0-pie.diff.bz2
Patch7:		portmap_4-bind_to_ip_or_host_address.diff.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	tcp_wrappers-devel

Prereq:		rpm-helper
Requires:	setup >= 2.4-16avx

%description
The portmapper program is a security tool which prevents theft of NIS
(YP), NFS and other sensitive information via the portmapper.  A
portmapper manages RPC connections, which are used by protocols like
NFS and NIS.

The portmap package should be installed on any machine which acts as
a server for protocols using RPC.

%prep 
%setup -q -n portmap_%{ver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p0

%build
%serverbuild
make FACILITY=LOG_AUTH ZOMBIES='-DIGNORE_SIGCHLD -Dlint' LIBS="-lnsl" RPM_OPT_FLAGS="%{optflags}" \
	WRAP_DIR=%{_libdir}

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/{sbin,%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/sysconfig}

install -m 0755 -s portmap $RPM_BUILD_ROOT/sbin
install -m 0755 -s pmap_set $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 -s pmap_dump $RPM_BUILD_ROOT%{_sbindir}

install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/portmap
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man8
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/man8
install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man8

mkdir -p %{buildroot}%{_srvdir}/portmap/log
mkdir -p %{buildroot}%{_srvlogdir}/portmap
install -m 0755 %{SOURCE5} %{buildroot}%{_srvdir}/portmap/run
install -m 0755 %{SOURCE6} %{buildroot}%{_srvdir}/portmap/log/run

strip %{buildroot}/sbin/portmap

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%pre
%_pre_useradd rpc / /bin/false 72

%post
%_post_srv portmap

%triggerpostun -- portmap <= portmap-4.0-9
/sbin/chkconfig --add portmap

%preun
%_preun_srv portmap

%postun
%_postun_userdel rpc

%files
%defattr(-,root,root)
%doc README CHANGES BLURB
%config(noreplace) %{_sysconfdir}/sysconfig/portmap
%dir %{_srvdir}/portmap
%dir %{_srvdir}/portmap/log
%dir %attr(0750,logger,logger) %{_srvlogdir}/portmap
%{_srvdir}/portmap/run
%{_srvdir}/portmap/log/run
/sbin/portmap
%{_sbindir}/pmap_dump
%{_sbindir}/pmap_set
%{_mandir}/*/*


%changelog
* Thu Mar 03 2005 Vincent Danen <vdanen@annvix.org> 4.0-28avx
- use logger for logging
- P7: allow portmapper to listen to only one hostname or IP and
  a sysconfig file to define it
- P3: updated from fedora
- P6: from mdk, originally from fedora
- add url
- drop initscript

* Mon Sep 20 2004 Vincent Danen <vdanen@annvix.org> 4.0-27avx
- update run scripts

* Tue Jun 22 2004 Vincent Danen <vdanen@annvix.org> 4.0-26avx
- remove req on chkconfig
- Annvix build

* Tue Feb 03 2004 Vincent Danen <vdanen@opensls.org> 4.0-25sls
- minor spec cleanups
- srv macros

* Tue Feb 03 2004 Vincent Danen <vdanen@opensls.org> 4.0-24sls
- remove initscript
- give rpc static uid/gid 72
- use srv macros

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 4.0-23sls
- supervise files

* Mon Dec 02 2003 Vincent Danen <vdanen@opensls.org> 4.0-22sls
- OpenSLS build
- tidy spec

* Mon Apr 28 2003 Warly <warly@mandrakesoft.com> 4.0-21mdk
- fix rebuild

* Wed Jul 31 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0-20mdk
- lib64 fixes

* Thu Jul 18 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0-19mdk
- add rpc user

* Wed Feb 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0-18mdk
- applied patch from rh to not die on sigpipe

* Fri Mar 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-17mdk
- use new server macros

* Mon Mar 26 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-16mdk
- initscript installed as no replace.
- depends on setup-2.1.9-38mdk for user rpc.

* Wed Mar 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0-15mdk
- We have a rpc user we can apply the rpc user patch.
- Requires last setup.

* Mon Feb 26 2001 Francis Galiegue <fg@mandrakesoft.com> 4.0-14mdk
- Don't apply patch3, unless we decide one day to have a rpc user...

* Sat Feb 24 2001 Francis Galiegue <fg@mandrakesoft.com> 4.0-13mdk
- Patch merge from RH

* Fri Nov 10 2000 David BAUDENS <baudens@mandrakesoft.com> 4.0-12mdk
- BuildRequires: tcp_wrappers-devel

* Thu Aug 31 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 4.0-11mdk
- slight specfile cleanup
- use %{_initrddir}
- don't link portmap init script in runlevel dir, chkconfig do it for us

* Thu Jul 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>  4.0-10mdk
- BM, macros

* Wed Mar 22 2000 Pixel <pixel@mandrakesoft.com> 4.0-9mdk
- fix version (is 4.0, not 4)

* Tue Mar 21 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 4-9mdk
- Fix group tag.
- Use version tag.

* Fri Nov  5 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- checkconfig --del in %preun.

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Tue Mar 23 1999 Preston Brown <pbrown@redhat.com>
- added man pages.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul  7 1998 Jeff Johnson <jbj@redhat.com>
- start/stop portmap at levels 11/89

* Mon May 04 1998 Cristian Gafton <gafton@redhat.com>
- fixed the trigger script

* Fri May 01 1998 Jeff Johnson <jbj@redhat.com>
- added triggerpostun

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- added %trigger to fix a previously broken package

* Thu Apr 23 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscripts

* Thu Jan 08 1998 Erik Troan <ewt@redhat.com>
- rebuilt against glibc 2.0.6

* Tue Oct 28 1997 Erik Troan <ewt@redhat.com>
- fixed service name in stop section of init script

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- fixed chkconfig support

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- added restart, status commands to init script
- added chkconfig support
- uses a buildroot and %attr tags

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
