%define name	sysklogd
%define version	1.4.1
%define release	8sls

# rh 1.4.1-5

Summary:	System logging and kernel message trapping daemons.
Name:		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Kernel and hardware 
Source:		ftp://sunsite.unc.edu/pub/Linux/system/daemons/%{name}-%{version}rh.tar.bz2
Source1:	syslogd.run
Source2:	syslogd-log.run
Source3:	klogd.run
Source4:	klogd-log.run
Patch0:		sysklogd-1.4.1rh-opensls.patch.bz2
Patch1: 	sysklogd-1.4rh-do_not_use_initlog_when_restarting.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root

Requires:	logrotate >= 3.3-8mdk, bash >= 2.0
PreReq:		fileutils, initscripts >= 5.60, rpm-helper

%description
The sysklogd package contains two system utilities (syslogd and klogd)
which provide support for system logging.  Syslogd and klogd run as
daemons (background processes) and log system messages to different
places, like sendmail logs, security logs, error logs, etc.

%prep

%setup -q -n %{name}-%{version}rh
%patch0 -p1 -b .slsconf
%patch1 -p1 -b .initlog

%build
%serverbuild
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_mandir}/man{5,8},%{_sbindir},/sbin}

make install TOPDIR=$RPM_BUILD_ROOT MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	MAN_OWNER=`id -nu`

install -m644 redhat/syslog.conf.rhs $RPM_BUILD_ROOT/etc/syslog.conf

mkdir -p $RPM_BUILD_ROOT/etc/{rc.d/init.d,logrotate.d,sysconfig}
install -m644 redhat/syslog.log $RPM_BUILD_ROOT/etc/logrotate.d/syslog
install -m644 redhat/syslog $RPM_BUILD_ROOT/etc/sysconfig/syslog

chmod 755 $RPM_BUILD_ROOT/sbin/syslogd
chmod 755 $RPM_BUILD_ROOT/sbin/klogd

mkdir -p %{buildroot}%{_srvdir}/{syslogd,klogd}/log
mkdir -p %{buildroot}%{_srvlogdir}/{syslogd,klogd}
install -m 0750 %{SOURCE1} %{buildroot}%{_srvdir}/syslogd/run
install -m 0750 %{SOURCE2} %{buildroot}%{_srvdir}/syslogd/log/run
install -m 0750 %{SOURCE3} %{buildroot}%{_srvdir}/klogd/run
install -m 0750 %{SOURCE4} %{buildroot}%{_srvdir}/klogd/log/run

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%pre
# Because RPM do not know the difference about a file or a directory,
# We need to verify if there is no file with the same name as the directory
# we want to create for the new logdir architecture.
# If the name is the same and it is a file, rename it to name.old
for file in mail cron kernel lpr news daemons; do
	if [ -f /var/log/$file ]; then 
		mv -f /var/log/$file /var/log/$file.old \
		&& mkdir /var/log/$file && mv /var/log/$file.old /var/log/$file/$file.old  
	fi
done

%post
# Create each log directory with logfiles : info, warnings, errors :
for dir in /var/log/{mail,cron,kernel,lpr,news,daemons}; do
    [ -d $dir ] || mkdir ${dir}
    for file in $dir/{info,warnings,errors}; do
        [ -f $file ] || touch $file && chmod 600 $file
    done
done

# Create standard logfiles if they do not exist:
for file in \
 /var/log/{auth.log,syslog,user.log,messages,secure,spooler,boot.log,explanations};
do
    [ -f $file ] || touch $file && chmod 600 $file
done

%_post_srv syslogd
%_post_srv klogd

%preun
%_preun_srv syslogd
%_preun_srv klogd

%postun
if [ "$1" -ge "1" ]; then
	/usr/sbin/srv restart klogd > /dev/null 2>&1
	/usr/sbin/srv restart syslogd > /dev/null 2>&1
fi	


%files
%defattr(-,root,root)
%doc ANNOUNCE README* NEWS INSTALL 
%config(noreplace) %{_sysconfdir}/syslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/syslog
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
/sbin/*
%{_mandir}/*/*
%dir %{_srvdir}/syslogd
%dir %{_srvdir}/syslogd/log
%{_srvdir}/syslogd/run
%{_srvdir}/syslogd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/syslogd
%dir %{_srvdir}/klogd
%dir %{_srvdir}/klogd/log
%{_srvdir}/klogd/run
%{_srvdir}/klogd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/klogd


%changelog
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
