%define name	nfs-utils
%define	version	1.0.5
%define release	5sls

%define	url	ftp://ftp.kernel.org:/pub/linux/utils/nfs

Summary:	The utilities for Linux NFS server.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	GPL
Group:		Networking/Other
URL:		%{url}
Source0:	%{url}/%{name}-%{version}.tar.bz2
Source1:	ftp://nfs.sourceforge.net/pub/nfs/nfs.doc.tar.bz2
Source10:	nfs.init
Source11:	nfslock.init
Source12:	nfs.sysconfig
Source13:	rpc.statd.run
Source14:	rpc.statd-log.run
Source15:	rpc.nfsd.run
Source16:	rpc.nfsd-log.run
Source17:	rpc.mountd.run
Source18:	rpc.mountd-log.run
Source19:	rpc.mountd.stop
Source20:	rpc.nfsd.stop
Patch1:		nfs-utils-0.2beta-nowrap.patch.bz2
Patch3:		nfs-utils-0.3.3-statd-manpage.patch.bz2
Patch4:		eepro-support.patch.bz2
Patch5:		nfs-utils-1.0.4-no-chown.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root

ExcludeArch:	armv4l
Obsoletes:	nfs-server knfsd nfs-server-clients
Provides:	nfs-server knfsd nfs-server-clients
Requires:	nfs-utils-clients, kernel >= 2.2.5, portmap >= 4.0, setup >= 2.1.9-35mdk
PreReq:		rpm-helper

%description
The nfs-utils package provides a daemon for the kernel NFS server and
related tools, which provides a much higher level of performance than the
traditional Linux NFS server used by most users.

This package also contains the showmount program.  Showmount queries the
mount daemon on a remote host for information about the NFS (Network File
System) server on the remote host.  For example, showmount can display the
clients which are mounted on that host.

%package clients
Summary:	The utilities for Linux NFS client.
Group:		Networking/Other
Obsoletes:	knfsd-clients knfsd-lock
Provides:	knfsd-clients knfsd-lock
Requires:	kernel >= 2.2.5, portmap >= 4.0
PreReq:		rpm-helper

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
%patch1 -p0
%patch3 -p1 -b .statd-manpage
%patch4 -p1 -b .eepro-support
%patch5 -p1 -b .no-chown

%build
#
# Hack to enable netgroups.  If anybody knows the right way to do
# this, please help yourself.
#
%serverbuild
%configure --disable-rquotad
make all

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT{/sbin,/usr/sbin}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/{man5,man8}
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
mkdir -p $RPM_BUILD_ROOT/var/lib/nfs
make install_prefix=$RPM_BUILD_ROOT MANDIR=$RPM_BUILD_ROOT%{_mandir} SBINDIR=$RPM_BUILD_ROOT%{_prefix}/sbin install
install -s -m 755 tools/rpcdebug/rpcdebug $RPM_BUILD_ROOT/sbin
install -m 755 %{SOURCE12} $RPM_BUILD_ROOT/etc/sysconfig/nfs
touch $RPM_BUILD_ROOT/var/lib/nfs/rmtab
mv $RPM_BUILD_ROOT/usr/sbin/{rpc.lockd,rpc.statd} $RPM_BUILD_ROOT/sbin

mkdir -p $RPM_BUILD_ROOT/var/lib/nfs/statd

mkdir -p %{buildroot}%{_srvdir}/rpc.{statd,nfsd,mountd}/log
mkdir -p %{buildroot}%{_srvlogdir}/rpc.{statd,nfsd,mountd}
install -m 0755 %{SOURCE13} %{buildroot}%{_srvdir}/rpc.statd/run
install -m 0755 %{SOURCE14} %{buildroot}%{_srvdir}/rpc.statd/log/run
install -m 0755 %{SOURCE15} %{buildroot}%{_srvdir}/rpc.nfsd/run
install -m 0755 %{SOURCE16} %{buildroot}%{_srvdir}/rpc.nfsd/log/run
install -m 0755 %{SOURCE17} %{buildroot}%{_srvdir}/rpc.mountd/run
install -m 0755 %{SOURCE18} %{buildroot}%{_srvdir}/rpc.mountd/log/run
install -m 0755 %{SOURCE19} %{buildroot}%{_srvdir}/rpc.mountd/stop
install -m 0755 %{SOURCE20} %{buildroot}%{_srvdir}/rpc.nfsd/stop

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_post_srv rpc.mountd
%_post_srv rpc.nfsd

%create_ghostfile %{_localstatedir}/nfs/xtab root root 644
%create_ghostfile %{_localstatedir}/nfs/etab root root 644
%create_ghostfile %{_localstatedir}/nfs/rmtab root root 644

%preun
# create a bare-bones /etc/exports
if [ ! -s /etc/exports ]; then
  echo "#" >/etc/exports
  chmod 644 /etc/exports
fi
%_preun_srv rpc.mountd
%_preun_srv rpc.nfsd

%pre clients
%_pre_useradd rpcuser /var/lib/nfs /bin/false 73

%post clients
%_post_srv rpc.statd

%preun clients
%_preun_srv rpc.statd

%postun clients
%_postun_userdel rpcuser

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/nfs
%config(noreplace) %ghost  %{_localstatedir}/nfs/xtab
%config(noreplace) %ghost  %{_localstatedir}/nfs/etab
%config(noreplace) %ghost  %{_localstatedir}/nfs/rmtab
/sbin/rpcdebug
%{_sbindir}/exportfs
%{_sbindir}/nfsstat
%{_sbindir}/nhfsgraph
%{_sbindir}/nhfsnums
%{_sbindir}/nhfsrun
%{_sbindir}/nhfsstone
%{_sbindir}/rpc.mountd
%{_sbindir}/rpc.nfsd
%{_mandir}/man5/exports.5.bz2
%{_mandir}/man7/nfsd.7.bz2
%{_mandir}/man8/exportfs.8.bz2
%{_mandir}/man8/mountd.8.bz2
%{_mandir}/man8/nfsd.8.bz2
%{_mandir}/man8/nfsstat.8.bz2
%{_mandir}/man8/nhfsgraph.8.bz2
%{_mandir}/man8/nhfsnums.8.bz2
%{_mandir}/man8/nhfsrun.8.bz2
%{_mandir}/man8/nhfsstone.8.bz2
%{_mandir}/man8/rpc.mountd.8.bz2
%{_mandir}/man8/rpc.nfsd.8.bz2
%dir %{_srvdir}/rpc.nfsd
%dir %{_srvdir}/rpc.nfsd/log
%{_srvdir}/rpc.nfsd/run
%{_srvdir}/rpc.nfsd/stop
%{_srvdir}/rpc.nfsd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/rpc.nfsd
%dir %{_srvdir}/rpc.mountd
%dir %{_srvdir}/rpc.mountd/log
%{_srvdir}/rpc.mountd/run
%{_srvdir}/rpc.mountd/stop
%{_srvdir}/rpc.mountd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/rpc.mountd

%doc README ChangeLog COPYING
%doc nfs/*.html nfs/*.ps linux-nfs/*

%files clients
%defattr(-,root,root)
%doc README
/sbin/rpc.lockd
/sbin/rpc.statd
%{_sbindir}/showmount
%{_mandir}/man8/lockd.8.bz2
%{_mandir}/man8/rpc.lockd.8.bz2
%{_mandir}/man8/rpc.statd.8.bz2
%{_mandir}/man8/statd.8.bz2
%{_mandir}/man8/showmount.8.bz2
%dir %{_localstatedir}/nfs
%dir %{_localstatedir}/nfs/state
%dir %attr(700,rpcuser,rpcuser) /var/lib/nfs/statd
%dir %{_srvdir}/rpc.statd
%dir %{_srvdir}/rpc.statd/log
%{_srvdir}/rpc.statd/run
%{_srvdir}/rpc.statd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/rpc.statd

%changelog
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
