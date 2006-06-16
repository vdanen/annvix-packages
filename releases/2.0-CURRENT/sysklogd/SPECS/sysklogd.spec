#
# spec file for package sysklogd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		sysklogd
%define version		1.4.1
%define release		%_revrel

Summary:	System logging and kernel message trapping daemons
Name:		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Kernel and hardware 
Source:		ftp://sunsite.unc.edu/pub/Linux/system/daemons/%{name}-%{version}rh.tar.bz2
Source1:	syslogd.run
Source2:	klogd.run
Source3:	syslog.logrotate
Source4:	syslog.conf
Source5:	syslog.sysconfig
Patch0:		sysklogd-1.4.1-avx-conf.patch
Patch1: 	sysklogd-1.4rh-do_not_use_initlog_when_restarting.patch
Patch2:		sysklogd-1.4.1-owl-longjmp.diff
Patch3:		sysklogd-1.4.1-owl-syslogd-create-mode.patch
Patch4:		sysklogd-1.4.1-alt-owl-syslogd-killing.diff
Patch5:		sysklogd-1.4.1-caen-owl-klogd-drop-root.diff
Patch6:		sysklogd-1.4.1-caen-owl-syslogd-bind.patch
Patch7:		sysklogd-1.4.1-caen-owl-syslogd-drop-root.patch
Patch8:		sysklogd-1.4.1-owl-syslogd-crunch_list.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	logrotate >= 3.3-8mdk, bash >= 2.0
Requires(pre):	rpm-helper
Requires(preun): rpm-helper
Requires(post):	rpm-helper
Provides:	syslog

%description
The sysklogd package contains two system utilities (syslogd and klogd)
which provide support for system logging.  Syslogd and klogd run as
daemons (background processes) and log system messages to different
places, like sendmail logs, security logs, error logs, etc.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}rh
%patch0 -p1 -b .slsconf
%patch1 -p1 -b .initlog
%patch2 -p1 -b .longjmp
%patch3 -p1 -b .createmode
%patch4 -p1 -b .killing
%patch5 -p1 -b .klogddroproot
%patch6 -p1 -b .syslogdbind
%patch7 -p1 -b .syslogddroproot
%patch8 -p1 -b .crunch_list


%build
%serverbuild
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_sysconfdir},%{_bindir},%{_mandir}/man{5,8},%{_sbindir},/sbin}

make install TOPDIR=%{buildroot} MANDIR=%{buildroot}%{_mandir} \
    MAN_OWNER=`id -nu`

install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/syslog.conf

mkdir -p %{buildroot}%{_sysconfdir}/{logrotate.d,sysconfig}
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/syslog
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/syslog

chmod 0750 %{buildroot}/sbin/syslogd
chmod 0750 %{buildroot}/sbin/klogd

mkdir -p %{buildroot}%{_srvdir}/{syslogd,klogd}/env
install -m 0700 %{SOURCE1} %{buildroot}%{_srvdir}/syslogd/run
install -m 0700 %{SOURCE2} %{buildroot}%{_srvdir}/klogd/run

echo "-m 0" >%{buildroot}%{_srvdir}/syslogd/env/OPTIONS
echo "-2" >%{buildroot}%{_srvdir}/klogd/env/OPTIONS


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
%_pre_useradd syslogd /var/empty /bin/false 85
%_pre_useradd klogd /var/empty /bin/false 84


%post
# Create standard logfiles if they do not exist:
for file in \
    /var/log/{auth.log,syslog,user.log,messages,secure,mail.log,cron,kernel,daemons,boot.log};
do
    [ -f $file ] || touch $file && chmod 620 $file && chown root:syslogd $file
done

%_post_srv syslogd
%_post_srv klogd


%preun
%_preun_srv syslogd
%_preun_srv klogd


%postun
if [ "$1" -ge "1" ]; then
    /usr/sbin/srv --restart syslogd > /dev/null 2>&1
    /usr/sbin/srv --restart klogd > /dev/null 2>&1
fi	


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/syslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/syslog
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
%attr(0700,root,root) /sbin/klogd
%attr(0700,root,root) /sbin/syslogd
%{_mandir}/*/*
%attr(0750,root,admin) %dir %{_srvdir}/syslogd
%attr(0750,root,admin) %dir %{_srvdir}/syslogd/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/syslogd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/syslogd/env/OPTIONS
%attr(0750,root,admin) %dir %{_srvdir}/klogd
%attr(0750,root,admin) %dir %{_srvdir}/klogd/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/klogd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/klogd/env/OPTIONS

%files doc
%defattr(-,root,root)
%doc ANNOUNCE README* NEWS INSTALL 


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1
- add -doc subpackage
- rebuild with gcc4

* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1
- Provides: syslog

* Wed Jan 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1
- revert run scripts back to sh scripts so that ./env/OPTIONS is properly
  parsed (fixing bug #18)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sun Oct 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1-18avx
- fix calls to srv

* Wed Sep 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1-17avx
- execline run scripts
- add env directory

* Thu Sep 08 2005 Sean P. Thomas <spt-at-build.annvix.org> 1.4.1-16avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1-15avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1-14avx
- bootstrap build

* Sun Oct 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1-13avx
- s/OpenSLS/Annvix/ in syslog.conf (re: Jean-Pierre Denis)
- remove cron.* entries from syslog.conf because dcron logs to svlogd,
  thus logs are in /var/log/supervise/crond (in other words, get rid of
  useless empty 0 byte cron logs)

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1-12avx
- updated run scripts
- minor spec cleanups
- remove the trigger
- bzip patches

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1-11avx
- Annvix build

* Sat May 08 2004 Vincent Danen <vdanen@opensls.org> 1.4.1-10sls
- make klogd run as root again until we can make the kernel give mode 440
  perms to /proc/kmsg (and owned root:klogd) so that klogd can actually read
  from it (otherwise klogd and syslogd consume all the CPU)

* Thu Apr 22 2004 Vincent Danen <vdanen@opensls.org> 1.4.1-9sls
- merge patches from 1.4.1-owl8 (openwall) (P2-P8)
  - fix buffer overflows (re: Steve Grubb) and other issues in
    crunch_list()
  - klogd and syslogd both run as user klogd/syslogd respectively; be
    warned!  All syslog files should be owned by syslogd.syslogd now
  - logfiles are created mode 0600 rather than 0644
  - klogd is chrooted to /var/empty
  - syslogd can be told to bind to a specific interface
  - numerous other small bugfixes/stability fixes
- add user/group pairs for syslogd/klogd (85/84)
- update runscripts
- change perms of sysklogd and klogd to be 0700
- include our own logrotate file
- we don't need logging services for these services so remove them
- syslog.conf and sysconfig/syslog are source files now, so we can remove P1
- seriously cleanup syslog.conf; instead of logging to
  /var/log/[fac]/{info,warning,errors} log to /var/log/[fac] (one
  file to rule them all, one file to find them... bla)
- we no longer include facilities for lpr, news, uucp, or mdk config tools
- trigger script to move dir to dir.old and create our new files to move
  away from the logdir mechanism 

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.4.1-8sls
- minor spec cleanups

* Wed Feb 04 2004 Vincent Danen <vdanen@opensls.org> 1.4.1-7sls
- remove initscripts
- supervise scripts
- rediff/rename P0; we're using svc to restart syslogd for log rotation

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 1.4.1-6sls
- OpenSLS build
- tidy spec

* Wed Apr  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.1-5mdk
- Revert s/fileutils/coreutils/ the latter should provide the former

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.4.1-4mdk
- prereq: rpm-helper
- rpmlint fixes
- requires s/fileutils/coreutils/

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.1-3mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon Mar  4 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.4.1-2mdk
- merged with rh

* Wed Nov 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.4.1-1mdk
- 1.4.1
- add the explanations log file for local1.

* Mon Sep 10 2001 Pixel <pixel@mandrakesoft.com> 1.4-12mdk
- sysklogd-1.4rh-do_not_use_initlog_when_restarting:
  why doing this: the pb of initlog being called when syslog is being
  restarted is that minilogd is started to keep the logs waiting for syslog to
  really treat them. Alas with devfs mounted (with or without devfsd),
  minilogd do not exit as it should. I don't know why.
  
  minilogd keeping the logs means its memory usage grows a lot as time goes.
  Restarting syslog mainly happens when upgrading glibc.

* Fri Jun 15 2001 Philippe Libat <philippe@mandrakesoft.com> 1.4-11mdk
- fix news entry

* Thu Mar 29 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.4-10mdk
- recompiled without omit-frame-pointer and ease upgrades (new macros)

* Mon Feb 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.4-9mdk
- Add /etc/sysconfig/syslog configuration files.
- Upgrade initscripts (which now get work condrestart).
- Merge with rh package.

* Wed Feb 07 2001 Francis Galiegue <fg@mandrakesoft.com> 1.4-8mdk
- Apply patch1 and patch5 even if non alpha - type enforcing and foolproof
  checks never hurt

* Tue Jan 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.4-7mdk
- Don't do busy loop when encounter two zero bytes (Troels Walsted
  Hansen (troels@thule.no)).

* Wed Dec 20 2000 David BAUDENS <baudens@mandrakesoft.com> 1.4-6mdk
- Build on Cooker (sorry... :()

* Wed Dec 20 2000 David BAUDENS <baudens@mandrakesoft.com> 1.4-5mdk
- Fix build for PPC (aka, don't apply sparc & alpha patches on non sparc &
  alpha archs)

* Mon Sep 25 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.4-4mdk
- readded requirement for initscripts (but removed sysklogd 
  requirement in initscripts, see initscripts-5.27-27mdk) to 
  ease install.

* Mon Sep 25 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.4-3mdk
- added postun to restart syslog when upgrading
- sylog script relies on /etc/rc.d/init.d/functions so depends from 
  initscripts; starting and stopping syslog relies also on initscripts.
  But /sbin/initlog called by rc.sysinit from initscripts relies on 
  sysklogd... So for now I remove the initscripts requirement here.

* Fri Sep 22 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.4-2mdk
- added prereq on initscripts
- some cleanup

* Fri Sep 22 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.4-1mdk
- new version with several fixes

* Tue Sep 19 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.3.33-8mdk
- removed news.xxx entries also, they're added by inn package

* Tue Sep 19 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.3.33-7mdk
- removed mail.xxx entries in logrotate conf file

* Tue Sep 19 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.3.33-6mdk
- applied "format bug" patch to correct vulnerability (thanks to V.Danen)

* Thu Sep 14 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 1.3.33-5mdk
- modified logrotate.d conf file to avoid using * (see logrotate 3.3-9)

* Wed Sep 13 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 1.3.33-4mdk
- applied patch from Grzegorz Nosek <blackfire@go2.pl>,
  pass the system.map for our kernel version as argument to klogd if possible.

* Tue Sep 05 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 1.3.33-3mdk
- create all log file to avoid syslog warning.

- I was knowing that rpm sucked... Now I know that it suck hard.

  %ghost tag isn't able to create a directory, nor to touch file
  in a newly created by the %dir tag directory.
  So I'm creating all file in %post which is dirty.

  The conclusion of all this is that :
  It is good to make good package, but it's even better if you do it without rpm.
  (Thanks to Frederic Lepied who was as frightened as me when he saw that).

- Due to the new logdir architecture, 
  and that RPM can not distinguish a file and a directory :
    - Search for a file of the same name as the directory we wish to create,
      if such file exist, rename it to file.old and put it in the created
      directory in order for it to be rotated.

- In syslog initscript, created separate start and stop function
  (instead of having them in the case), and added a condrestart case which use them.
  This avoid having to re execute the syslog init script.

* Mon Sep 04 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 1.3.33-2mdk
- Completly rewritten syslog configuration
- Updated logrotate configuration file for new syslog config
  (log rotation recurssion is now avoided by logrotate itself, not
   configuration tweak)
- do not create init script link manually

* Fri Aug 25 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.33-1mdk
- update to 1.3-33
- Use new initrddir macro 
- Correct logrotate config script to prevent rotating previous files

* Thu Aug 10 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.31-15mdk
- add noreplace to make rpmlint happy

* Fri Jul 28 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.31-14mdk
- BM + macroszification
- bzipped config files

* Tue May 17 2000 Yoann Vandoorselaere <yoann@mandrakeosft.com> 1.3.31-13mdk
- correct path to killall in syslog.log

* Thu May 04 2000 Yoann Vandoorselaere <yoann@mandrakeosft.com> 1.3.31-12mdk
- create the mail & news log directory.
- update syslog.log

* Tue May 02 2000 Yoann Vandoorselaere <yoann@mandrakeosft.com> 1.3.31-11mdk
- kern.* is now logged to kern.log
- much more logfile now (cron, syslog, kernel, mail.log, mail.warn, 
  mail.err, mail.info, auth.log, user.log, lpr.log, daemon.log ).
- do not sync() not important logfile everytime an entry is added.
- syslog.conf.rhs -> syslog.conf.mdk
- mail & news log are in their own directory.
- again a little config change.

* Thu Mar 23 2000 Daouda Lo <daouda@mandrakesoft.com> 1.3.31-8mdk
- fix group for the next release 7.1
* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with rh changes.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- fix handling of RPM_OPT_FLAGS

* Wed Feb 24 1999 Bill Nottingham <notting@redhat.com>
- update to sysklogd-1.3-31
- stop klogd *before* syslogd

* Tue Feb  9 1999 Jeff Johnson <jbj@redhat.com>
- escape naked percent chars in kernel messages (#1088).

* Thu Dec 17 1998 Jeff Johnson <jbj@redhat.com>
- rework last-gasp address-in-module oops trace for both 2.0.x/2.1.x modules.

* Mon Dec  7 1998 Jakub Jelinek <jj@ultra.linux.cz>
- make klogd translate SPARC register dumps and oopses.

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- add %clean

* Tue Aug  4 1998 Chris Adams <cadams@ro.com>
- only log to entries that are USER_PROCESS (fix #822)

* Mon Jul 27 1998 Jeff Johnson <jbj@redhat.com>
- remove RPM_BUILD_ROOT from %post

* Wed Apr 29 1998 Cristian Gafton <gafton@redhat.com>
- patch to support Buildroot
- package is now buildrooted

* Wed Apr 29 1998 Michael K. Johnson <johnsonm@redhat.com>
- Added exit patch so that a normal daemon exit is not flagged as an error.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added (missingok) to init symlinks

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- added status|restart support to syslog.init
- added chkconfig support
- various spec file cleanups

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
