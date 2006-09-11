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

Requires:	logrotate >= 3.3-8mdk
Requires:	bash >= 2.0
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

install -m 0644 %{_sourcedir}/syslog.conf %{buildroot}%{_sysconfdir}/syslog.conf

mkdir -p %{buildroot}%{_sysconfdir}/{logrotate.d,sysconfig}
install -m 0644 %{_sourcedir}/syslog.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/syslog
install -m 0644 %{_sourcedir}/syslog.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/syslog

chmod 0750 %{buildroot}/sbin/syslogd
chmod 0750 %{buildroot}/sbin/klogd

mkdir -p %{buildroot}%{_srvdir}/{syslogd,klogd}/env
install -m 0700 %{_sourcedir}/syslogd.run %{buildroot}%{_srvdir}/syslogd/run
install -m 0700 %{_sourcedir}/klogd.run %{buildroot}%{_srvdir}/klogd/run

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
* Sun Sep 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1
- change runsvctrl calls to /sbin/sv calls

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
