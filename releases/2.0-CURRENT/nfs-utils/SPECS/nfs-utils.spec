#
# spec file for package nfs-utils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		nfs-utils
%define	version		1.0.10
%define release		%_revrel
%define epoch		1

Summary:	The utilities for Linux NFS server
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Networking/Other
URL:		http://sourceforge.net/projects/nfs/
Source0:	http://prdownloads.sourceforge.net/nfs/%{name}-%{version}.tar.gz
Source1:	ftp://nfs.sourceforge.net/pub/nfs/nfs.doc.tar.bz2
Source3:	nfs.statd.run
Source4:	nfs.statd-log.run
Source5:	nfs.statd.finish
Source6:	nfs.mountd.run
Source7:	nfs.mountd-log.run
Source8:	nfs.mountd.finish
Source9:	rpc.idmapd.run
Source10:	rpc.idmapd-log.run
Source11:	rpc.gssd.run
Source12:	rpc.gssd-log.run
Source13:	rpc.svcgssd.run
Source14:	rpc.svcgssd-log.run
Source15:	nfsv4.schema
Source16:	gssapi_mech.conf
Source17:	idmapd.conf

Patch1:		eepro-support.patch
Patch3:		nfs-utils-1.0.7-binary-or-shlib-defines-rpath.diff
# (oe) boldly stolen from gentoo
Patch40:	nfs-utils-1.0.7-gcc4.patch
#
# Local Patches (FC)
#
Patch50:	nfs-utils-1.0.5-statdpath.patch
Patch51:	nfs-utils-1.0.6-mountd.patch
Patch52:	nfs-utils-1.0.6-idmap.conf.patch
Patch54:	nfs-utils-1.0.7-mountd-stat64.patch
Patch100:	nfs-utils-1.0.8-compile.diff
Patch150:	nfs-utils-1.0.6-pie.patch
Patch151:	nfs-utils-1.0.7-strip.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	tcp_wrappers-devel
BuildRequires:	nfsidmap-devel >= 0.16
BuildRequires:	krb5-devel >= 1.3
BuildRequires:	libevent-devel
BuildRequires:	rpcsecgss-devel >= 0.12
BuildRequires:	gssapi-devel >= 0.9

ExcludeArch:	armv4l
Obsoletes:	nfs-server
Obsoletes:	knfsd
Obsoletes:	nfs-server-clients
Provides:	nfs-server = %{version}
Provides:	knfsd = %{version}
Provides:	nfs-server-clients = %{version}
Requires:	nfs-utils-clients
Requires:	kernel >= 2.2.5
Requires:	portmap >= 4.0
Requires:	setup >= 2.1.9-35mdk
Requires:	tcp_wrappers
Requires:	kernel >= 2.6.0
Requires:	module-init-tools >= 3.0-5mdk
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
The nfs-utils package provides a daemon for the kernel NFS server and
related tools, which provides a much higher level of performance than the
traditional Linux NFS server used by most users.

This package also contains the showmount program.  Showmount queries the
mount daemon on a remote host for information about the NFS (Network File
System) server on the remote host.  For example, showmount can display the
clients which are mounted on that host.


%package clients
Summary:	The utilities for Linux NFS client
Group:		Networking/Other
Obsoletes:	knfsd-clients
Obsoletes:	knfsd-lock
Provides:	knfsd-clients
Provides:	knfsd-lock = %{version}
Requires:	kernel >= 2.6
Requires:	module-init-tools >= 3.0-5mdk
Requires:	portmap >= 4.0
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	rpm-helper
Requires(preun): rpm-helper

%description clients
The nfs-utils package provides a daemon for the kernel NFS server and
related tools, which provides a much higher level of performance than the
traditional Linux NFS server used by most users.

This package also contains the showmount program.  Showmount queries the
mount daemon on a remote host for information about the NFS (Network File
System) server on the remote host.  For example, showmount can display the
clients which are mounted on that host.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 1
cp %{_sourcedir}/nfsv4.schema .

# fix strange perms
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%patch1 -p1 -b .eepro-support
#patch3 -p1 -b .binary-or-shlib-defines-rpath
# (oe) boldly stolen from gentoo
#patch40 -p1 -b .gcc4
%patch50 -p1 -b .statdpath
%patch51 -p1 -b .mountd
%patch52 -p1 -b .conf
%patch54 -p1 -b .stat64
%patch100 -p1 -b .compile
#patch150 -p1 -b .pie
#patch151 -p1 -b .strip

# lib64 fixes
perl -pi -e "s|\\$dir/lib/|\\$dir/%{_lib}/|g" configure


%build
sh autogen.sh

%serverbuild
%configure2_5x \
    --with-statedir=%{_localstatedir}/nfs \
    --with-statduser=rpcuser \
    --enable-nfsv3 \
    --disable-rquotad \
    --enable-nfsv4 \
    --enable-gss \
    --enable-secure-statd \
    --with-krb5=%{_prefix}

make all


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{/sbin,%{_sbindir}}
mkdir -p %{buildroot}%{_mandir}/{man5,man8}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/env/nfs
mkdir -p %{buildroot}%{_localstatedir}/nfs/{statd,v4recovery}

%make \
    DESTDIR=%{buildroot} \
    MANDIR=%{buildroot}%{_mandir} \
    SBINDIR=%{buildroot}%{_sbindir} \
    install

install -m 0755 tools/rpcdebug/rpcdebug %{buildroot}/sbin/
ln -snf rpcdebug %{buildroot}/sbin/nfsdebug
ln -snf rpcdebug %{buildroot}/sbin/nfsddebug

touch %{buildroot}%{_localstatedir}/nfs/rmtab
mv %{buildroot}%{_sbindir}/{rpc.lockd,rpc.statd} %{buildroot}/sbin

install -m 0644 %{_sourcedir}/idmapd.conf %{buildroot}%{_sysconfdir}/idmapd.conf
install -m 0644 %{_sourcedir}/gssapi_mech.conf %{buildroot}%{_sysconfdir}/gssapi_mech.conf
perl -pi -e "s|/usr/lib|%{_libdir}|g" %{buildroot}%{_sysconfdir}/gssapi_mech.conf
mkdir -p %{buildroot}%{_localstatedir}/nfs/rpc_pipefs


mkdir -p %{buildroot}%{_srvdir}/{nfs.statd,nfs.mountd,rpc.idmapd,rpc.gssd,rpc.svcgssd}/log
install -m 0740 %{_sourcedir}/nfs.statd.run %{buildroot}%{_srvdir}/nfs.statd/run
install -m 0740 %{_sourcedir}/nfs.statd-log.run %{buildroot}%{_srvdir}/nfs.statd/log/run
install -m 0740 %{_sourcedir}/nfs.statd.finish %{buildroot}%{_srvdir}/nfs.statd/finish
install -m 0740 %{_sourcedir}/nfs.mountd.run %{buildroot}%{_srvdir}/nfs.mountd/run
install -m 0740 %{_sourcedir}/nfs.mountd-log.run %{buildroot}%{_srvdir}/nfs.mountd/log/run
install -m 0740 %{_sourcedir}/nfs.mountd.finish %{buildroot}%{_srvdir}/nfs.mountd/finish
install -m 0740 %{_sourcedir}/rpc.idmapd.run %{buildroot}%{_srvdir}/rpc.idmapd/run
install -m 0740 %{_sourcedir}/rpc.idmapd-log.run %{buildroot}%{_srvdir}/rpc.idmapd/log/run
install -m 0740 %{_sourcedir}/rpc.gssd.run %{buildroot}%{_srvdir}/rpc.gssd/run
install -m 0740 %{_sourcedir}/rpc.gssd-log.run %{buildroot}%{_srvdir}/rpc.gssd/log/run
install -m 0740 %{_sourcedir}/rpc.svcgssd.run %{buildroot}%{_srvdir}/rpc.svcgssd/run
install -m 0740 %{_sourcedir}/rpc.svcgssd-log.run %{buildroot}%{_srvdir}/rpc.svcgssd/log/run

mkdir -p %{buildroot}%{_srvdir}/{nfs.mountd,nfs.statd,rpc.svcgssd,rpc.idmapd}/depends
%_mkdepends nfs.statd portmap
%_mkdepends nfs.mountd nfs.statd
%_mkdepends rpc.svcgssd rpc.gssd
%_mkdepends rpc.idmapd nfs.mountd

rm -f %{buildroot}%{_sbindir}/rpcdebug
rm -f %{buildroot}%{_mandir}/man8/rpcdebug.8

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_srv nfs.statd
%_post_srv nfs.mountd
%_post_srv rpc.gssd
%_post_srv rpc.svcgssd
%_post_srv rpc.idmapd

%create_ghostfile %{_localstatedir}/nfs/xtab root root 644
%create_ghostfile %{_localstatedir}/nfs/etab root root 644
%create_ghostfile %{_localstatedir}/nfs/rmtab root root 644


%preun
# create a bare-bones /etc/exports
if [ ! -s %{_sysconfdir}/exports ]; then
    echo "#" >%{_sysconfdir}/exports
    chmod 0644 %{_sysconfdir}/exports
fi
%_preun_srv nfs.statd
%_preun_srv nfs.mountd
%_preun_srv rpc.gssd
%_preun_srv rpc.svcgssd
%_preun_srv rpc.idmapd


%pre clients
%_pre_useradd rpcuser %{_localstatedir}/nfs /bin/false 73


%post clients
%_post_srv rpc.statd


%preun clients
%_preun_srv rpc.statd


%postun clients
%_postun_userdel rpcuser


%files
%defattr(-,root,root)
%dir %attr(0750,root,admin) %{_sysconfdir}/sysconfig/env/nfs
%config(noreplace) %ghost  %{_localstatedir}/nfs/xtab
%config(noreplace) %ghost  %{_localstatedir}/nfs/etab
%config(noreplace) %ghost  %{_localstatedir}/nfs/rmtab
%config(noreplace) %{_sysconfdir}/idmapd.conf
%config(noreplace) %{_sysconfdir}/gssapi_mech.conf
/sbin/rpcdebug
/sbin/nfsdebug
/sbin/nfsddebug
%{_sbindir}/exportfs
%{_sbindir}/nfsstat
%{_sbindir}/nhfsgraph
%{_sbindir}/nhfsnums
%{_sbindir}/nhfsrun
%{_sbindir}/nhfsstone
%{_sbindir}/rpc.mountd
%{_sbindir}/rpc.nfsd
%{_sbindir}/rpc.idmapd
%{_sbindir}/rpc.gssd
%{_sbindir}/rpc.svcgssd
%{_sbindir}/gss_clnt_send_err
%{_sbindir}/gss_destroy_creds
%{_mandir}/man5/idmapd.conf.5*
%{_mandir}/man5/exports.5*
%{_mandir}/man7/nfsd.7*
%{_mandir}/man8/exportfs.8*
%{_mandir}/man8/mountd.8*
%{_mandir}/man8/nfsd.8*
%{_mandir}/man8/nfsstat.8*
%{_mandir}/man8/nhfsgraph.8*
%{_mandir}/man8/nhfsnums.8*
%{_mandir}/man8/nhfsrun.8*
%{_mandir}/man8/nhfsstone.8*
%{_mandir}/man8/rpc.mountd.8*
%{_mandir}/man8/rpc.nfsd.8*
%{_mandir}/man8/gssd.8*
%{_mandir}/man8/idmapd.8*
%{_mandir}/man8/rpc.gssd.8*
%{_mandir}/man8/rpc.idmapd.8*
%{_mandir}/man8/rpc.svcgssd.8*
%{_mandir}/man8/svcgssd.8*
%dir %{_localstatedir}/nfs/rpc_pipefs
%dir %attr(0750,root,admin) %{_srvdir}/nfs.mountd
%dir %attr(0750,root,admin) %{_srvdir}/nfs.mountd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.mountd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.mountd/finish
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.mountd/log/run
%dir %attr(0750,root,admin) %{_srvdir}/nfs.mountd/depends
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.mountd/depends/nfs.statd
%dir %attr(0750,root,admin) %{_srvdir}/rpc.idmapd
%dir %attr(0750,root,admin) %{_srvdir}/rpc.idmapd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rpc.idmapd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rpc.idmapd/log/run
%dir %attr(0750,root,admin) %{_srvdir}/rpc.idmapd/depends
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rpc.idmapd/depends/nfs.mountd
%dir %attr(0750,root,admin) %{_srvdir}/rpc.gssd
%dir %attr(0750,root,admin) %{_srvdir}/rpc.gssd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rpc.gssd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rpc.gssd/log/run
%dir %attr(0750,root,admin) %{_srvdir}/rpc.svcgssd
%dir %attr(0750,root,admin) %{_srvdir}/rpc.svcgssd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rpc.svcgssd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rpc.svcgssd/log/run
%dir %attr(0750,root,admin) %{_srvdir}/rpc.svcgssd/depends
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rpc.svcgssd/depends/rpc.gssd


%files clients
%defattr(-,root,root)
/sbin/rpc.lockd
/sbin/rpc.statd
%{_sbindir}/showmount
%{_mandir}/man8/lockd.8*
%{_mandir}/man8/rpc.lockd.8*
%{_mandir}/man8/rpc.statd.8*
%{_mandir}/man8/statd.8*
%{_mandir}/man8/showmount.8*
%dir %{_localstatedir}/nfs
%dir %{_localstatedir}/nfs/state
%dir %{_localstatedir}/nfs/v4recovery
%dir %attr(0700,rpcuser,rpcuser) %{_localstatedir}/nfs/statd
%dir %attr(0750,root,admin) %{_srvdir}/nfs.statd
%dir %attr(0750,root,admin) %{_srvdir}/nfs.statd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.statd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.statd/finish
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.statd/log/run
%dir %attr(0750,root,admin) %{_srvdir}/nfs.statd/depends
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.statd/depends/portmap

%files doc
%defattr(-,root,root)
%doc README ChangeLog COPYING
%doc nfs/*.html linux-nfs/*
%doc nfsv4.schema


%changelog
* Sat Dec 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.10
- rpc.gssd needs to check for the existance (and configuration of)
  /etc/krb5/keytab before launching
- nfs.mountd doesn't start (or kill) rpc.rquotad anymore since that
  file is in the quota package and is entirely optional so don't
  bother looking for it; let it run as it's own service

* Sat Dec 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.10
- fix the runscripts regarding some of the envdir options

* Thu Dec 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.10
- 1.0.10
- enable all the stuff we couldn't use before without a 2.6 kernel (gssapi,
  kerberos, nfsv4)
- use the ./depends directory and let srv handle dependencies
- add /var/lib/nfs/v4recovery
- write run scripts for rpc.idmapd, rpc.gssd, and rpc.svcgssd and rework
  the other runscripts
- add a finish script for rpc.statd
- try to sanely handle dependencies
- NOTE: i'm comitting this but have no idea how well it will work.. the changeset
  will already be huge so it'll be easier to work from the comitted version

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.7
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.7
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.7
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.7-2avx
- rebuild

* Sat Aug 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.7-1avx
- 1.0.7
- don't package postscript docs
- prepare spec for nfsv4/kernel 2.6
- Requires: tcp_wrappers
- BuildRequires: tcp_wrappers-devel
- sync with mandrake 1.0.7-6mdk:
  - P20, P21, P22, P23, P24, P25, P26, P27, P28: from fedora
  - P50: gcc4 patch from gentoo
  - rediffed P200; parts were applied (CAN-2004-1014)
- use execlineb for run scripts
- move logdir to /var/log/service/nfs.{statd,mountd}
- run scripts are now considered config files and are not replaceable

* Sat Aug 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.6-9avx
- fix perms on run scripts

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.6-8avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.6-7avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.6-6avx
- use logger for logging

* Sat Jan 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.6-5avx
- fix run scripts so the properly stop the services
- enable checkdepends on nfs.statd

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.6-4avx
- P7: patch to fix CAN-2004-0946

* Sat Dec 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.6-3avx
- signal nfsd with signal 9 rather than 2

* Sat Dec 04 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.6-2avx
- P6: patch to fix CAN-2004-1014
- completely rework runscripts: remove rpc.statd, rpc.mountd, and
  rpc.nfsd services; we now have nfs.mountd and nfs.statd -- this
  should solve bug #3
- spec cleanups

* Wed Sep 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.6-1avx
- 1.0.6

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.5-7avx
- update run scripts
- stop scripts are now finish scripts

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.5-6avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 1.0.5-5sls
- minor spec cleanups

* Tue Jan 27 2004 Vincent Danen <vdanen@opensls.org> 1.0.5-4sls
- make the supervise scripts more robust

* Tue Jan 27 2004 Vincent Danen <vdanen@opensls.org> 1.0.5-3sls
- supervise scripts
- create barebones /etc/exports in %%post rather than the initscript
- do some fancy tricking to have supervise think it's running rpc.nfsd
- use %%_post_srv and %%_preun_srv macros
- rpcuser is uid/gid 73

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 1.0.5-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
