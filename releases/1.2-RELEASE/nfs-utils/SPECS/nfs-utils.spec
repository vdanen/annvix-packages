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
%define	version		1.0.7
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
Source0:	http://prdownloads.sourceforge.net/nfs/%{name}-%{version}.tar.bz2
Source1:	nfs.doc.tar.bz2
Source10:	nfs.init
Source11:	nfslock.init
Source12:	nfs.sysconfig
Source13:	nfs.statd.run
Source14:	nfs.statd-log.run
Source15:	nfs.mountd.run
Source16:	nfs.mountd-log.run
Source17:	nfs.mountd.finish
Source18:	nfsv4.schema
Source19:	rpcgssd.init
Source20:	rpcidmapd.init
Source21:	rpcsvcgssd.init
Source22:	gssapi_mech.conf
Source23:	idmapd.conf

Patch0:		nfs-utils-0.3.3-statd-manpage.patch
Patch1:		eepro-support.patch
Patch2:		nfs-utils-1.0.4-no-chown.patch
Patch3:		nfs-utils-1.0.7-binary-or-shlib-defines-rpath.diff
# (oe) stolen from fedora
Patch20:	nfs-utils-1.0.6-citi-mountd_flavors.patch
Patch21:	nfs-utils-1.0.6-zerostats.patch
Patch22:	nfs-utils-1.0.6-mountd.patch
Patch23:	nfs-utils-1.0.6-expwarn.patch
Patch24:	nfs-utils-1.0.6-fd-sig-cleanup.patch
Patch25:	nfs-utils-1.0.6-statd-notify-hostname.patch
Patch26:	nfs-utils-1.0.7-rpcsecgss-debug.patch
Patch27:	nfs-utils-1.0.7-xlog-loginfo.patch
Patch28:	nfs-utils-1.0.7-svcgssd-bufover.patch
# (oe) stolen from gentoo
Patch50:	nfs-utils-1.0.7-gcc4.patch
# security fixes
Patch200:	nfs-utils-1.0.7-CAN-2004-1014.diff
Patch201:	nfs-utils-1.0.7-CAN-2004-0946.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	tcp_wrappers-devel
# 2.6:
#BuildRequires:	nfsidmap-devel, krb5-devel >= 1.3, libevent-devel

ExcludeArch:	armv4l
Obsoletes:	nfs-server knfsd nfs-server-clients
Provides:	nfs-server knfsd nfs-server-clients
Requires:	nfs-utils-clients, kernel >= 2.2.5, portmap >= 4.0, setup >= 2.1.9-35mdk, tcp_wrappers
#Requires:	kernel >= 2.6.0, module-init-tools >=3.0-5mdk
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
Obsoletes:	knfsd-clients knfsd-lock
Provides:	knfsd-clients knfsd-lock
Requires:	kernel >= 2.2.5, portmap >= 4.0
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


%prep
%setup -q -a 1

mkdir -p Annvix
cat %{SOURCE10} > Annvix/nfs.init
cat %{SOURCE12} > Annvix/nfs.sysconfig
cat %{SOURCE11} > Annvix/nfslock.init
cat %{SOURCE18} > Annvix/nfsv4.schema
cat %{SOURCE19} > Annvix/rpcgssd.init
cat %{SOURCE20} > Annvix/rpcidmapd.init
cat %{SOURCE21} > Annvix/rpcsvcgssd.init
cat %{SOURCE22} > Annvix/gssapi_mech.conf
cat %{SOURCE23} > Annvix/idmapd.conf

# fix strange perms
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%patch0 -p1 -b .statd-manpage
%patch1 -p1 -b .eepro-support
%patch2 -p1 -b .no-chown
%patch3 -p1 -b .binary-or-shlib-defines-rpath
%patch20 -p1 -b .mountd_flavors
%patch21 -p1 -b .zerostats
%patch22 -p1 -b .mountd
%patch23 -p1 -b .expwarn
%patch24 -p1 -b .cleanup
%patch25 -p1 -b .notify
%patch26 -p1 -b .rpcsecgss
%patch27 -p1 -b .xlog
%patch28 -p1 -b .svcgssd-bufover
%patch50 -p1 -b .gcc4
%patch200 -p1 -b .CAN-2004-1014
%patch201 -p0 -b .CAN-2004-0946

# lib64 fixes
perl -pi -e "s|/usr/lib|%{_libdir}|g" Annvix/*
perl -pi -e "s|\\$dir/lib/|\\$dir/%{_lib}/|g" configure


%build
%serverbuild
%configure \
    --with-statedir=%{_localstatedir}/nfs \
    --with-statduser=rpcuser \
    --enable-nfsv3 \
    --disable-rquotad \
    --disable-nfsv4 --disable-gss --disable-secure-statd --without-krb5
# once we have a 2.6 kernel, we can enable all of the above
make all


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{/sbin,%{_sbindir}}
mkdir -p %{buildroot}%{_mandir}/{man5,man8}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_localstatedir}/nfs/statd

make \
    install_prefix=%{buildroot} \
    MANDIR=%{buildroot}%{_mandir} \
    SBINDIR=%{buildroot}%{_sbindir} \
    install
install -m 0755 tools/rpcdebug/rpcdebug %{buildroot}/sbin/
ln -snf rpcdebug %{buildroot}/sbin/nfsdebug
ln -snf rpcdebug %{buildroot}/sbin/nfsddebug

install -m 0755 Annvix/nfs.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/nfs

touch %{buildroot}%{_localstatedir}/nfs/rmtab
mv %{buildroot}%{_sbindir}/{rpc.lockd,rpc.statd} %{buildroot}/sbin

## when we're ready for 2.6 and nfsv4:
#install -m 0755 Annvix/rpcidmapd.init %{buildroot}%{_initrddir}/rpcidmapd
#install -m 0755 Annvix/rpcgssd.init %{buildroot}%{_initrddir}/rpcgssd
#install -m 0755 Annvix/rpcsvcgssd.init %{buildroot}%{_initrddir}/rpcsvcgssd
#install -m 0644 Annvix/idmapd.conf %{buildroot}%{_sysconfdir}/idmapd.conf
#install -m 0644 Annvix/gssapi_mech.conf %{buildroot}%{_sysconfdir}/gssapi_mech.conf
#mkdir -p %{buildroot}%{_localstatedir}/nfs/rpc_pipefs


mkdir -p %{buildroot}%{_srvdir}/nfs.{statd,mountd}/log
install -m 0740 %{SOURCE13} %{buildroot}%{_srvdir}/nfs.statd/run
install -m 0740 %{SOURCE14} %{buildroot}%{_srvdir}/nfs.statd/log/run
install -m 0740 %{SOURCE15} %{buildroot}%{_srvdir}/nfs.mountd/run
install -m 0740 %{SOURCE16} %{buildroot}%{_srvdir}/nfs.mountd/log/run
install -m 0740 %{SOURCE17} %{buildroot}%{_srvdir}/nfs.mountd/finish

# with 2.6/nfsv4 we'll need additional services: rpcdimap, rpcgssd, rpcsvcgssd
# refer to mdk nfs-utils.spec: 
# http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/SPECS/nfs-utils/nfs-utils.spec.diff?r1=1.34&r2=1.43

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
for i in nfs.statd nfs.mountd
do
    if [ -d /var/log/supervise/$i -a ! -d /var/log/service/$i ]; then
        mv /var/log/supervise/$i /var/log/service/
    fi
done
%_post_srv nfs.statd
%_post_srv nfs.mountd

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
%doc README ChangeLog COPYING
%doc nfs/*.html linux-nfs/*
#%doc Annvix/nfsv4.schema
%config(noreplace) %{_sysconfdir}/sysconfig/nfs
%config(noreplace) %ghost  %{_localstatedir}/nfs/xtab
%config(noreplace) %ghost  %{_localstatedir}/nfs/etab
%config(noreplace) %ghost  %{_localstatedir}/nfs/rmtab
# 2.6:
#%config(noreplace) %{_sysconfdir}/idmapd.conf
#%config(noreplace) %{_sysconfdir}/gssapi_mech.conf
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
# 2.6:
#%{_sbindir}/rpc.idmapd
#%{_sbindir}/rpc.gssd
#%{_sbindir}/rpc.svcgssd
#%{_mandir}/man5/idmapd.conf.5*
#%{_mandir}/man5/rpc.idmapd.conf.5*
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
#%{_mandir}/man8/gssd.8*
#%{_mandir}/man8/idmapd.8*
#%{_mandir}/man8/rpc.gssd.8*
#%{_mandir}/man8/rpc.idmapd.8*
#%{_mandir}/man8/rpc.svcgssd.8*
#%{_mandir}/man8/svcgssd.8*
#%dir %{_localstatedir}/nfs/rpc_pipefs
%dir %attr(0750,root,admin) %{_srvdir}/nfs.mountd
%dir %attr(0750,root,admin) %{_srvdir}/nfs.mountd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.mountd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.mountd/finish
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.mountd/log/run

%files clients
%defattr(-,root,root)
%doc README
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
%dir %attr(0700,rpcuser,rpcuser) %{_localstatedir}/nfs/statd
%dir %attr(0750,root,admin) %{_srvdir}/nfs.statd
%dir %attr(0750,root,admin) %{_srvdir}/nfs.statd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.statd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nfs.statd/log/run


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Tue Jul 22 2003 Juan Quintela <quintela@mandrakesoft.com> 1.0.5-1mdk
- included the rest of created programs & manpages.
  Inquiring minds need nhfsgraph, nfgsnums and nhfsrun.
- brown paper bug upstream, I tested it and it worked, problem is that
  it just worked once :(.
- 1.0.5.

* Wed Jul 16 2003 Juan Quintela <quintela@mandrakesoft.com> 1.0.4-1mdk
- remove patch5 (time.h) already included upstream.
- remove patch2 no-chroot (not needed after removing patch0).
- remove patch0 (drop privs) included better patch upstream.
- 1.0.4.

* Tue Jul 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.3-1mdk
- new release (kernel-2.5.x support)
- rediff patch 0

* Wed Jun 04 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0.1-2mdk
- remove unpackaged files
- fix E: nfs-utils-clients no-prereq-on rpm-helper
- drop obsolete Prefix tag

* Tue Jul 23 2002 Juan Quintela <quintela@mandrakesoft.com> 1.0.1-1mdk
- then merge them with nfs-1.0.1 ones.
- merged nfs.init & nfslock.init with rh ones.
- merge with rh 1.0.1.pre7-1.
- use %configure.
- 1.0.1.

* Thu Jul 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.3.3-4mdk
- add rpcuser

* Tue Jan 15 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3.3-3mdk
- Make some files as %ghost.

* Fri Dec  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3.3-2mdk
- Fix some rpmlints.

* Fri Sep 28 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3.3-1mdk
- 0.3.3.

* Sat Sep  1 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3.1-7mdk
- Merge rh scripts.
- Remove quota from here it's provided by quota.

* Sun Apr  1 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3.1-6mdk
- Move dir /var/lib/nfs/statd to clients packge or rpc.statd wouldn't
  work.

* Thu Mar 28 2001 Florin Grad <florin@mandrakesoft.com> 0.3.1-5mdk
- -fno-omit-frame-pointer

* Sun Mar 18 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3.1-4mdk
- Requires last setup package for rpcuser.
- Make /var/lib/nfs/statd as rpcuser,rpcuser.

* Thu Mar 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3.1-3mdk
- Fix incorrect file specifications in statd manpage. (rh).
- disable tcp_wrapper support (rh).
- Don't do a chroot(2) after dropping privs, in statd (rh).
- #include <time.h> patch.

* Fri Mar 02 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3.1-2mdk
- Fix chkconfig entry in initscripts.

* Mon Feb 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3.1-1mdk
- Move rpc.lockd and rpc.statd to /sbin
- Merge with rh changes.
- 0.3.1.

* Thu Dec  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2.1-3mdk
- Nfslock only when we have a lockd into the kernel.

* Mon Oct 09 2000 Florin Grad <florin@mandrakesoft.com> 0.2.1-2mdk
- chkconfig is now 345 ... instead of - 60 ...

* Fri Sep 29 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.2.1-1mdk
- 0.2.1 bug fix release.

* Thu Sep 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-5mdk
- Florin or chmou sucks, pidofproc come from the
  /etc/init.d/functions.

* Wed Sep 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-4mdk
- nfslock: where pidofproc come from ? use pidof instead (florin).

* Thu Sep 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-3mdk
- nfslock: don't kill lockd processes that do not have an executable
  (i.e. kernel threads).

* Thu Sep 07 2000 Florin Grad <florin@mandrakesoft.com> 0.2-2mdk
- added noreplace for %{_inirddir}/(nfs|nfslock)

* Thu Sep 07 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.2-1mdk
- s/0.1.9.1/0.2/;

* Wed Aug 30 2000 Florin Grad <florin@mandrakesoft.com> 0.1.9.1-4mdk
- changing some macros

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9.1-3mdk
- BM
- more macros

* Mon Jul 10 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9.1-2mdk
- fix build with latest rpm macros

* Wed Jul 05 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.9.1-1mdk
- new release (mainly turning gcc warnings off)
- fix build as non root with tmpdir

* Mon Jul  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1.9-1mdk
- 0.1.9.

* Tue Jun 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1.8-1mdk
- 0.1.8.
- Macrozifications.

* Sun May 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1.7-3mdk
- Fix path call (/usr/sbin !> /sbin/).
- Launch always rpc.statd.

* Wed Apr 06 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 0.1.7-2mdk
- Renamed linusinit patch to mdkinit.
- Do not grep for linus in /proc/version, but for mdk 
  (Thanks to Jürgen Zimmermann)

* Wed Mar 22 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 0.1.7-1mdk
- Update to 0.1.7.
- Fix group.

* Tue Jan 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1.6-1mdk
- 0.1.6.

* Tue Dec 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.1.5.
- Fix init script with kernel-linus.

* Mon Dec 06 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.1.4.

* Tue Nov 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.1.3.

* Thu Nov 25 1999 Pixel <pixel@linux-mandrake.com>
- fixed %defattr
- split in 2 packages: nfs-utils-clients & nfs-utils (for server)

* Fri Nov 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Last cvs version.

* Wed Oct 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 0.1.2

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.1.1.

* Tue Oct 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- First Spec files based on original version of H.J Lu.
