#
# spec file for package dcron
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	revision	$Rev$
%define	name		dcron
%define	version		2.9
%define	release		%_revrel

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
Patch0:		http://www.ogris.de/diet/dcron29-dietlibc-patch.diff
Patch1:		dcron29-avx-paths.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires(post):	rpm-helper, setup
Requires(preun): rpm-helper
Requires:	srv, runit
Conflicts:	vixie-cron
Obsoletes:	crontabs
Provides:	crond, crontabs

%description
A multiuser cron written from scratch, dcron is follows concepts
of vixie-cron but has significant differences. Less attention is
paid to feature development in favor of usability and reliability.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


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

install -m 0755 crontab %{buildroot}%{_bindir}/
install -m 0750 crond %{buildroot}%{_sbindir}/
install -m 0644 crontab.1 %{buildroot}%{_mandir}/man1/
install -m 0644 crond.8 %{buildroot}%{_mandir}/man8/

install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/crontab

install -d %{buildroot}%{_srvdir}/crond/log
install -m 0740 %{SOURCE1} %{buildroot}%{_srvdir}/crond/run
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/crond/log/run


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [[ -z `crontab -l | grep run-parts` ]]; then
    echo "Adding the \"system crontab\" to emulate vixie-cron"
    /bin/grep "^[0-9]" %{_sysconfdir}/crontab | %{_bindir}/crontab -
fi
%_post_srv crond


%preun
%_preun_srv crond


%files
%defattr(-,root,root)
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/crontab
%dir %attr(0750,root,root) %{_sysconfdir}/cron.hourly
%dir %attr(0750,root,root) %{_sysconfdir}/cron.daily
%dir %attr(0750,root,root) %{_sysconfdir}/cron.weekly
%dir %attr(0750,root,root) %{_sysconfdir}/cron.monthly
# OE: only root should be allowed to add cronjobs!
%attr(4750,root,cron) %{_bindir}/crontab
%attr(0750,root,root)%{_sbindir}/crond
%{_mandir}/man1/crontab.1*
%{_mandir}/man8/crond.8*
%dir %attr(0755,root,root) /var/spool/dcron/crontabs
%dir %attr(0750,root,admin) %{_srvdir}/crond
%dir %attr(0750,root,admin) %{_srvdir}/crond/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/crond/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/crond/log/run

%files doc
%defattr(-,root,root)
%doc CHANGELOG README


%changelog
* Thu Jun 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.9
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.9
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.9
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix requires
- remove the moving of the logging directory

* Sun Sep 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9-15avx
- adjust some permissions on crond
- execlineb for run script (spt)

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9-14avx
- use execlineb for run scripts
- move logdir to /var/log/service/crond
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9-13avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9-12avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9-11avx
- bootstrap build

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9-10avx
- user logger for logging

* Tue Jan 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9-9avx
- drop the buildreq on dietlibc since we don't actually compile with it

* Tue Sep 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.9-8avx
- use the original dietlibc patch
- P1 for path customizations and chown fixes
- clean up run scripts

* Sat Sep 11 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.9-7avx
- Requires: s/daemontools/runit/
- update run scripts

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.9-6avx
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
