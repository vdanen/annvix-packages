#
# spec file for package socklog
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name 		socklog
%define version		2.0.2
%define release		1avx

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

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  dietlibc-devel >= 0.28

Requires:       execline
Requires:       runit
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
%setup -q -n admin


%build
pushd %{name}-%{version}
    echo "diet gcc -O2 -W -Wall -fomit-frame-pointer -pipe" > src/conf-cc
    echo "diet gcc -Os -static -s" > src/conf-ld

    package/compile
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}/bin
install -d %{buildroot}%{_mandir}/{man1,man8}

mkdir -p %{buildroot}%{_srvdir}/{socklog-unix,socklog-klog}/log
mkdir -p %{buildroot}%{_srvlogdir}/{socklog-unix,socklog-klog}

pushd %{name}-%{version}
    for i in `cat package/commands` ;  do
        install -m 0755 command/$i %{buildroot}/bin/
    done

    install -m 0644 man/*.1 %{buildroot}%{_mandir}/man1/
    install -m 0644 man/*.8 %{buildroot}%{_mandir}/man8/
popd

install -m 0750 %{SOURCE1} %{buildroot}%{_srvdir}/socklog-unix/run 
install -m 0750 %{SOURCE2} %{buildroot}%{_srvdir}/socklog-unix/log/run 
install -m 0750 %{SOURCE3} %{buildroot}%{_srvdir}/socklog-klog/run 
install -m 0750 %{SOURCE4} %{buildroot}%{_srvdir}/socklog-klog/log/run 


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
/bin/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%dir %attr(0750,logger,logger) %{_srvlogdir}/socklog-unix
%attr(0755,root,admin) %dir %{_srvdir}/socklog-unix
%attr(0755,root,admin) %dir %{_srvdir}/socklog-unix/log
%attr(0750,root,admin) %{_srvdir}/socklog-unix/run
%attr(0750,root,admin) %{_srvdir}/socklog-unix/log/run
%dir %attr(0750,logger,logger) %{_srvlogdir}/socklog-klog
%attr(0755,root,admin) %dir %{_srvdir}/socklog-klog
%attr(0755,root,admin) %dir %{_srvdir}/socklog-klog/log
%attr(0750,root,admin) %{_srvdir}/socklog-klog/run
%attr(0750,root,admin) %{_srvdir}/socklog-klog/log/run


%changelog
* Tue Aug 23 2005 Sean P. Thomas <spt@annvix.org> 2.0.2-1avx
- initial Annvix build
