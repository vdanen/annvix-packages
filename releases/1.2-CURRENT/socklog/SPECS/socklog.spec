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
Source1:	socklog-unix.run
Source2:	socklog-unix-log.run
Source3:	socklog-klog.run
Source4:	socklog-klog-log.run
Source5:	socklog-config.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  dietlibc-devel >= 0.28

Requires:       execline
Requires:       runit
Requires(post):	rpm-helper
Requires(preun): rpm-helper
#Conflicts:      syslog

%description
socklog cooperates with the runit package to create a small and secure 
replacement for syslogd. socklog supports system logging through Unix 
domain sockets (/dev/log) and UDP sockets (0.0.0.0:514) with the help of 
runit's runsvdir, runsv, and svlogd. socklog provides a different network 
logging concept, and also does log event notification. svlogd has built in 
log file rotation based on file size, so there is no need for any cron 
jobs to rotate the logs. socklog is small, secure, and reliable.


%prep
%setup -q -n admin -a 5


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

mkdir -p %{buildroot}%{_srvdir}/{socklog-unix,socklog-klog}/log

pushd %{name}-%{version}
    for i in `cat package/commands` ;  do
        install -m 0755 command/$i %{buildroot}/bin/
    done

    install -m 0644 man/*.1 %{buildroot}%{_mandir}/man1/
    install -m 0644 man/*.8 %{buildroot}%{_mandir}/man8/
popd

install -m 0740 %{SOURCE1} %{buildroot}%{_srvdir}/socklog-unix/run 
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/socklog-unix/log/run 
install -m 0740 %{SOURCE3} %{buildroot}%{_srvdir}/socklog-klog/run 
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/socklog-klog/log/run 

# install our default config files
mkdir -p %{buildroot}/var/log/socklog
pushd socklog-config
    cp -av * %{buildroot}/var/log/socklog/
    find %{buildroot}/var/log/socklog -name config -exec chmod 0640 {} \;
    chmod 0750 %{buildroot}/var/log/socklog/*
popd


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ -d /var/log/supervise/socklog-unix -a ! -d /var/log/service/socklog-unix ]; then
    mv /var/log/supervise/socklog-unix /var/log/service/
fi

if [ -d /var/log/supervise/socklog-klog -a ! -d /var/log/service/socklog-klog ]; then
    mv /var/log/supervise/socklog-klog /var/log/service/
fi


%_post_srv socklog-unix
%_post_srv socklog-klog

%preun
%_preun_srv socklog-unix
%_preun_srv socklog-klog


%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
/bin/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-unix/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-unix/log/run
%dir %attr(0750,root,admin) %{_srvdir}/socklog-klog
%dir %attr(0750,root,admin) %{_srvdir}/socklog-klog/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-klog/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/socklog-klog/log/run
# config files
%attr(0750,root,syslogd) %dir /var/log/socklog
%attr(0770,root,syslogd) %dir /var/log/socklog/all
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/all/config
%attr(0770,root,syslogd) %dir /var/log/socklog/auth
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/auth/config
%attr(0770,root,syslogd) %dir /var/log/socklog/boot
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/boot/config
%attr(0770,root,syslogd) %dir /var/log/socklog/cron
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/cron/config
%attr(0770,root,syslogd) %dir /var/log/socklog/daemon
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/daemon/config
%attr(0770,root,syslogd) %dir /var/log/socklog/debug
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/debug/config
%attr(0770,root,syslogd) %dir /var/log/socklog/ftp
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/ftp/config
%attr(0770,root,syslogd) %dir /var/log/socklog/kern
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/kern/config
%attr(0770,root,syslogd) %dir /var/log/socklog/local
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/local/config
%attr(0770,root,syslogd) %dir /var/log/socklog/mail
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/mail/config
%attr(0770,root,syslogd) %dir /var/log/socklog/messages
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/messages/config
%attr(0770,root,syslogd) %dir /var/log/socklog/news
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/news/config
%attr(0770,root,syslogd) %dir /var/log/socklog/syslog
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/syslog/config
%attr(0770,root,syslogd) %dir /var/log/socklog/user
%attr(0640,root,syslogd) %config(noreplace) /var/log/socklog/user/config


%changelog
* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
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
