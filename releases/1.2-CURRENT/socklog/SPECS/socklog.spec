#
# spec file for package socklog
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		socklog
%define version		2.0.2
%define release		%_revrel

Summary:	Small and secure replacement for syslogd
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System
URL:		http://smarden.org/%{name}/
Source0:	http://smarden.org/%{name}/%{name}-%{version}.tar.gz
Source1:	socklog-config.tar.bz2
Source2:	socklog-unix.run
Source3:	socklog-unix-log.run
Source4:	socklog-klog.run
Source5:	socklog-klog-log.run
Source6:	socklog-rklog.run
Source7:	socklog-rklog-log.run

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  dietlibc-devel >= 0.28

Requires:       execline
Requires:       runit
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Conflicts:      sysklogd
Provides:	syslog

%description
socklog cooperates with the runit package to create a small and secure 
replacement for syslogd. socklog supports system logging through Unix 
domain sockets (/dev/log) and UDP sockets (0.0.0.0:514) with the help of 
runit's runsvdir, runsv, and svlogd. socklog provides a different network 
logging concept, and also does log event notification. svlogd has built in 
log file rotation based on file size, so there is no need for any cron 
jobs to rotate the logs. socklog is small, secure, and reliable.


%package remote
Summary:        Scripts to receive remote logs
Group:          System
Requires:       %{name} = %{version}
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description remote
This package contains the run scripts used to receive remote TCP and UDP
log messages.


%prep
%setup -q -n admin -a 1


%build
%ifarch x86_64
COMP="diet x86_64-annvix-linux-gnu-gcc"
%else
COMP="diet gcc"
%endif

pushd %{name}-%{version}
    echo "$COMP -O2 -W -Wall -fomit-frame-pointer -pipe" > src/conf-cc
    echo "$COMP -Os -static -s" > src/conf-ld

    package/compile
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}/bin
install -d %{buildroot}%{_mandir}/{man1,man8}

mkdir -p %{buildroot}%{_srvdir}/socklog-{unix,klog,rklog,tcp,udp}/log

pushd %{name}-%{version}
    for i in `cat package/commands` ;  do
        install -m 0755 command/$i %{buildroot}/bin/
    done

    install -m 0644 man/*.1 %{buildroot}%{_mandir}/man1/
    install -m 0644 man/*.8 %{buildroot}%{_mandir}/man8/
popd

install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/socklog-unix/run 
install -m 0740 %{SOURCE3} %{buildroot}%{_srvdir}/socklog-unix/log/run 
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/socklog-klog/run 
install -m 0740 %{SOURCE5} %{buildroot}%{_srvdir}/socklog-klog/log/run 
install -m 0740 %{SOURCE6} %{buildroot}%{_srvdir}/socklog-rklog/run 
install -m 0740 %{SOURCE7} %{buildroot}%{_srvdir}/socklog-rklog/log/run

mkdir -p %{buildroot}%{_srvdir}/socklog-{tcp,udp}/env
mkdir -p %{buildroot}%{_srvdir}/socklog-tcp/peers
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/socklog-tcp/run 
install -m 0740 %{SOURCE3} %{buildroot}%{_srvdir}/socklog-tcp/log/run  
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/socklog-udp/run 
install -m 0740 %{SOURCE3} %{buildroot}%{_srvdir}/socklog-udp/log/run  

touch %{buildroot}%{_srvdir}/socklog-tcp/peers/0
chmod 0640 %{buildroot}%{_srvdir}/socklog-tcp/peers/0

echo "5140" >%{buildroot}%{_srvdir}/socklog-tcp/env/PORT
echo "514" >%{buildroot}%{_srvdir}/socklog-udp/env/PORT

# install our default config files
mkdir -p %{buildroot}/var/log/system
pushd socklog-config
    cp -av * %{buildroot}/var/log/system/
    find %{buildroot}/var/log/system -name config -exec chmod 0640 {} \;
    chmod 0750 %{buildroot}/var/log/system/*
popd



%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_srv socklog-unix
%_post_srv socklog-klog
%_post_srv socklog-rklog


%preun
%_preun_srv socklog-unix
%_preun_srv socklog-klog
%_preun_srv socklog-rklog


%post remote
%_post_srv socklog-tcp
%_post_srv socklog-udp
if [ -L %{_srvdir}/socklog-tcp ]; then
    pushd %{_srvdir}/socklog-tcp >/dev/null 2>&1
        ipsvd-cdb peers.cdb peers.cdb.tmp peers/
    popd >/dev/null 2>&1
fi


%preun remote
%_preun_srv socklog-tcp
%_preun_srv socklog-udp


%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
/bin/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%dir %attr(0750,root,admin) %{_srvdir}/socklog-unix
%dir %attr(0750,root,admin) %{_srvdir}/socklog-unix/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-unix/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-unix/log/run
%dir %attr(0750,root,admin) %{_srvdir}/socklog-klog
%dir %attr(0750,root,admin) %{_srvdir}/socklog-klog/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-klog/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-klog/log/run
%dir %attr(0750,root,admin) %{_srvdir}/socklog-rklog
%dir %attr(0750,root,admin) %{_srvdir}/socklog-rklog/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-rklog/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-rklog/log/run
# config files
%attr(0750,root,syslogd) %dir /var/log/system
%attr(0770,root,syslogd) %dir /var/log/system/all
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/all/config
%attr(0770,root,syslogd) %dir /var/log/system/auth
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/auth/config
%attr(0770,root,syslogd) %dir /var/log/system/boot
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/boot/config
%attr(0770,root,syslogd) %dir /var/log/system/cron
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/cron/config
%attr(0770,root,syslogd) %dir /var/log/system/daemon
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/daemon/config
%attr(0770,root,syslogd) %dir /var/log/system/debug
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/debug/config
%attr(0770,root,syslogd) %dir /var/log/system/ftp
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/ftp/config
%attr(0770,root,syslogd) %dir /var/log/system/kern
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/kern/config
%attr(0770,root,syslogd) %dir /var/log/system/local
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/local/config
%attr(0770,root,syslogd) %dir /var/log/system/mail
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/mail/config
%attr(0770,root,syslogd) %dir /var/log/system/messages
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/messages/config
%attr(0770,root,syslogd) %dir /var/log/system/news
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/news/config
%attr(0770,root,syslogd) %dir /var/log/system/syslog
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/syslog/config
%attr(0770,root,syslogd) %dir /var/log/system/user
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/user/config

%files remote
%defattr(-,root,root)
%dir %attr(0750,root,admin) %{_srvdir}/socklog-tcp
%dir %attr(0750,root,admin) %{_srvdir}/socklog-tcp/log
%dir %attr(0750,root,admin) %{_srvdir}/socklog-tcp/env
%dir %attr(0750,root,admin) %{_srvdir}/socklog-tcp/peers
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-tcp/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-tcp/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/socklog-tcp/peers/0
%attr(0640,root,admin) %{_srvdir}/socklog-tcp/env/PORT
%dir %attr(0750,root,admin) %{_srvdir}/socklog-udp
%dir %attr(0750,root,admin) %{_srvdir}/socklog-udp/log
%dir %attr(0750,root,admin) %{_srvdir}/socklog-udp/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-udp/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-udp/log/run
%attr(0640,root,admin) %{_srvdir}/socklog-udp/env/PORT
%attr(0750,root,syslogd) %dir /var/log/system/remote
%attr(0770,root,syslogd) %dir /var/log/system/remote/all-tcp
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/remote/all-tcp/config
%attr(0770,root,syslogd) %dir /var/log/system/remote/all-udp
%attr(0640,root,syslogd) %config(noreplace) /var/log/system/remote/all-udp/config


%changelog
* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- add peers support for socklog-tcp and add ./env support for both
  socklog-tcp and socklog-udp (to set PORT and IP)

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- add a -remote subpackage with scripts to receive TCP/UDP logs from
  remote systems (services socklog-tcp and socklog-udp)

* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- fix perms of the created log dirs for rklog and klog

* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- Provides: syslog

* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- make klog/rklog log as syslogd rather than logger to match everything
  else put into /var/log/system

* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- put logs in /var/log/system rather than /var/log/socklog
- conflict with sysklogd
- add socklog-rklog to log rsbac kernel messages (NOTE: this uses setuidgid
  to become rsbadmin in order to open /proc/rsbac-info/rmsg and probably
  isn't the best way to do this, but we can put ACLs in place once we setup
  RSBAC with proper ACL support)
- own /var/service/socklog-unix(/log)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq
- dietlibc fixes

* Sun Sep 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2-4avx
- added config files to mirror the setup in /etc/syslog.conf
- modified the logging daemon to accomodate the configs

* Thu Sep 08 2005 Sean P. Thomas <spt-at-build.annvix.org> 2.0.2-3avx
- fix up log run script, moved logs, and some perms.

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2-2avx
- fix perms on run scripts
- add %%post and %%preun scriptlets

* Tue Aug 23 2005 Sean P. Thomas <spt-at-build.annvix.org> 2.0.2-1avx
- initial Annvix build
