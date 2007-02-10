#
# spec file for package portmap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		portmap
%define version		4.0
%define release		%_revrel
%define ver		4

Summary:	A program which manages RPC connections
Name:		portmap
Version:	%{version}
Release:	%{release}
Group:		System/Servers
License:	BSD
URL:		ftp://ftp.porcupine.org/pub/security/index.html
Source0:	ftp://coast.cs.purdue.edu:/pub/tools/unix/netutils/portmap/portmap_%{ver}.tar.bz2
Source2:	pmap_set.8
Source3:	pmap_dump.8
Source4:	portmap.8
Source5:	portmap.run
Source6:	portmap-log.run
Patch0:		portmap-4.0-linux.patch
Patch1:		portmap-malloc.patch
Patch2:		portmap-4.0-cleanup.patch
Patch3:		portmap-4.0-rpc_user.patch
Patch4:		portmap-4.0-sigpipe.patch
Patch5:		portmap-4.0-errno.patch
Patch6:		portmap-4.0-pie.diff
Patch7:		portmap_4-bind_to_ip_or_host_address.diff
Patch8:		portmap-4.0-mdk-typo.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	tcp_wrappers-devel

Requires(pre):	rpm-helper
Requires(preun): rpm-helper
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires:	setup >= 2.4-16avx

%description
The portmapper program is a security tool which prevents theft of NIS
(YP), NFS and other sensitive information via the portmapper.  A
portmapper manages RPC connections, which are used by protocols like
NFS and NIS.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


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
%patch8 -p1 -b .typo


%build
%serverbuild
make FACILITY=LOG_AUTH ZOMBIES='-DIGNORE_SIGCHLD -Dlint' LIBS="-lnsl" RPM_OPT_FLAGS="%{optflags}" \
    WRAP_DIR=%{_libdir}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/{sbin,%{_sbindir},%{_mandir}/man8}

install -m 0755 -s portmap %{buildroot}/sbin
install -m 0755 -s pmap_set %{buildroot}%{_sbindir}
install -m 0755 -s pmap_dump %{buildroot}%{_sbindir}

install -m 0644 %{_sourcedir}/pmap_set.8 %{buildroot}%{_mandir}/man8
install -m 0644 %{_sourcedir}/pmap_dump.8 %{buildroot}%{_mandir}/man8
install -m 0644 %{_sourcedir}/portmap.8 %{buildroot}%{_mandir}/man8

mkdir -p %{buildroot}%{_srvdir}/portmap/{log,env}
install -m 0740 %{_sourcedir}/portmap.run %{buildroot}%{_srvdir}/portmap/run
install -m 0740 %{_sourcedir}/portmap-log.run %{buildroot}%{_srvdir}/portmap/log/run

strip %{buildroot}/sbin/portmap


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
%_pre_useradd rpc / /bin/false 72

%post
%_post_srv portmap

%preun
%_preun_srv portmap

%postun
%_postun_userdel rpc


%files
%defattr(-,root,root)
%dir %attr(0750,root,admin) %{_srvdir}/portmap
%dir %attr(0750,root,admin) %{_srvdir}/portmap/log
%dir %attr(0750,root,admin) %{_srvdir}/portmap/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/portmap/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/portmap/log/run
/sbin/portmap
%{_sbindir}/pmap_dump
%{_sbindir}/pmap_set
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README CHANGES BLURB


%changelog
* Fri Feb 09 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.0
- drop the sysconfig file; it's not used (envdir instead)

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0
- remove the docs from the main package
- remove checks for old service log dir

* Thu Jun 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Oct 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0-33avx
- execline the main runscript (spt)
- include env dir but make it empty by default

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0-32avx
- use execlineb for run scripts
- move logdir to /var/log/service/portmap
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0-31avx
- fix perms on run scripts
- P8: fix typo in tcp bind error message (oblin)

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0-30avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0-29avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0-28avx
- use logger for logging
- P7: allow portmapper to listen to only one hostname or IP and
  a sysconfig file to define it
- P3: updated from fedora
- P6: from mdk, originally from fedora
- add url
- drop initscript

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0-27avx
- update run scripts

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0-26avx
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
