%define	name	dcron
%define	version	2.9
%define	release	8avx

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
Source3:	etc-crontab
Patch0:		http://www.ogris.de/diet/dcron29-dietlibc-patch.diff.bz2
Patch1:		dcron29-avx-paths.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	dietlibc-devel >= 0.20-1mdk

PreReq:		rpm-helper, srv, runit, setup
Conflicts:	vixie-cron
Obsoletes:	crontabs
Provides:	crond, crontabs

%description
A multiuser cron written from scratch, dcron is follows concepts
of vixie-cron but has significant differences. Less attention is
paid to feature development in favor of usability and reliability.

%prep

%setup -q -n dcron
%patch0 -p1
%patch1 -p1 -b .avx
perl -pi -e "s|VISUAL|EDITOR|g" crontab.*

%build
make CC="gcc" CFLAGS="%{optflags}"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/cron.{hourly,daily,weekly,monthly}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man{1,8}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}/var/spool/dcron/crontabs

install -m0755 crontab %{buildroot}%{_bindir}/
install -m0755 crond %{buildroot}%{_sbindir}/
install -m0644 crontab.1 %{buildroot}%{_mandir}/man1/
install -m0644 crond.8 %{buildroot}%{_mandir}/man8/

install -m0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/crontab

install -d %{buildroot}%{_srvdir}/crond/log
install -d %{buildroot}%{_srvlogdir}/crond
install -m0755 %{SOURCE1} %{buildroot}%{_srvdir}/crond/run
install -m0755 %{SOURCE2} %{buildroot}%{_srvdir}/crond/log/run

%post
if [[ -z `crontab -l | grep run-parts` ]]; then
    echo "Adding the \"system crontab\" to emulate vixie-cron"
    /bin/grep "^[0-9]" %{_sysconfdir}/crontab | %{_bindir}/crontab -
fi
%_post_srv crond

%preun
%_preun_srv crond

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG README
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/crontab
%dir %attr(0750,root,root) %{_sysconfdir}/cron.hourly
%dir %attr(0750,root,root) %{_sysconfdir}/cron.daily
%dir %attr(0750,root,root) %{_sysconfdir}/cron.weekly
%dir %attr(0750,root,root) %{_sysconfdir}/cron.monthly
# OE: only root should be allowed to add cronjobs!
%attr(4750,root,cron) %{_bindir}/crontab
%attr(0755,root,wheel)%{_sbindir}/crond
%{_mandir}/man1/crontab.1*
%{_mandir}/man8/crond.8*
%dir %attr(0755,root,root) /var/spool/dcron/crontabs
%dir %{_srvdir}/crond
%dir %{_srvdir}/crond/log
%{_srvdir}/crond/run
%{_srvdir}/crond/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/crond

%changelog
* Tue Sep 21 2004 Vincent Danen <vdanen@annvix.org> 2.9-8avx
- use the original dietlibc patch
- P1 for path customizations and chown fixes
- clean up run scripts

* Sat Sep 11 2004 Vincent Danen <vdanen@annvix.org> 2.9-7avx
- Requires: s/daemontools/runit/
- update run scripts

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 2.9-6avx
- Annvix build

* Tue Mar 23 2004 Vincent Danen <vdanen@opensls.org> 2.9-5sls
- default root crontab can't start with "root" because dcron handles things
  differently than vixie-cron

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.9-4sls
- supervise macros

* Sun Feb 01 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9-3sls
- added S3, obsolete and mimic the crontabs package, but with tighter file
  and directory attributes
- fixed the %%post stuff (update safe, doesn't nuke root's cronjobs, if any)
- use the EDITOR env to get the preferred editor (vi, e3, nano, etc.)
- Conflicts: vixie-cron
- Obsoletes: crontabs
- Provides: crontabs
- PreReq: setup (for run-parts)

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 2.9-2sls
- can't build with dietlibc because we lose the ability to do lookups via
  NSS which causes problems with LDAP-based users
- Provides: crond
- move the %%pre stuff to %%post since crontab doesn't exist before it's
  installed

* Sat Jan 31 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9-1sls
- initial package
- added P0, S1 & S2
