%define	name	dcron
%define	version	2.9
%define	release	1sls

Summary:	Dillon's Cron Daemon
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://apollo.backplane.com/FreeSrc/
Source0:	dcron29.tar.bz2
Source1:	dcron.run
Source2:	dcron-log.run

# OE: P0 originates from patches I found here:
# http://www.ogris.de/diet/
# ftp://ftp.icm.edu.pl/vol/rzm3/openpkg/current/SRC/dcron-2.9-20031020.src.rpm
Patch0:		dcron29-dietlibc-patch.diff.bz2

#PreReq:		MTA vim
PreReq:		rpm-helper
PreReq:		srv
PreReq:		daemontools
PreReq:		crontabs
Conflicts:	vixie-cron
BuildRequires:	dietlibc-devel >= 0.20-1mdk
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
A multiuser cron written from scratch, dcron is follows concepts
of vixie-cron but has significant differences. Less attention is
paid to feature development in favor of usability and reliability.

%prep

%setup -q -n dcron
%patch -p1

%build
make CC="diet gcc" CFLAGS="-Os -wall"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man{1,8}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}/var/spool/dcron/crontabs

install -m0755 crontab %{buildroot}%{_bindir}/
install -m0755 crond %{buildroot}%{_sbindir}/
install -m0644 crontab.1 %{buildroot}%{_mandir}/man1/
install -m0644 crond.8 %{buildroot}%{_mandir}/man8/

install -d %{buildroot}/var/service/crond/log
install -d %{buildroot}/var/log/supervise/crond
install -m0755 %{SOURCE1} %{buildroot}/var/service/crond/run
install -m0755 %{SOURCE2} %{buildroot}/var/service/crond/log/run

%pre
echo "Adding the system crontab to emulate vixie-cron"
%{_bindir}/crontab %{_sysconfdir}/crontab

%post
%_post_srv crond

%preun
%_preun_srv crond

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG README
# OE: only root should be allowed to add cronjobs!
%attr(4750,root,cron) %{_bindir}/crontab
%attr(0755,root,wheel)%{_sbindir}/crond
%{_mandir}/man1/crontab.1*
%{_mandir}/man8/crond.8*
%dir %attr(0755,root,root) /var/spool/dcron/crontabs
%dir /var/service/crond
%dir /var/service/crond/log
/var/service/crond/run
/var/service/crond/log/run
%dir %attr(0750,nobody,nogroup) /var/log/supervise/crond

%changelog
* Sat Jan 31 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9-1sls
- initial package
- added P0, S1 & S2
