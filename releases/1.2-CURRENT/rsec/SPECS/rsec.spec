#
# spec file for package rsec
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rsec
%define version		0.62
%define release		%_revrel

Summary:	Security Reporting tool for Annvix
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		http://annvix.org/cgi-bin/viewcvs.cgi/tools/rsec/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	bash coreutils perl-base diffutils shadow-utils gawk mailx
Requires:	setup >= 2.2.0-21mdk, coreutils, iproute2
Conflicts:	passwd < 0.67, msec

%description
The Annvix Security Reporting tool (rsec) is largely based on the
Mandrakelinux msec program.  rsec produces the same reports as msec, but
does not manage permission issues or system configuration changes.  It is
nothing more than a reporting tool to advise you of changes to your system
and potential problem areas.  Any changes or fixes are entirely up to the
user to correct.


%prep


%setup -q


%build
make CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_sysconfdir}/{security,logrotate.d,cron.daily,cron.hourly}}
mkdir -p %{buildroot}{%{_datadir}/rsec,%{_bindir},/var/log/security,%{_mandir}/man8}

install -m 0640 cron-sh/{security,diff}_check.sh %{buildroot}%{_datadir}/rsec
install -m 0750 cron-sh/{promisc_check,security,urpmicheck}.sh %{buildroot}%{_datadir}/rsec
install -m 0750 src/promisc_check/promisc_check src/rsec_find/rsec_find %{buildroot}%{_bindir}
install -m 0644 rsec.logrotate %{buildroot}/etc/logrotate.d/rsec
install -m 0644 *.8 %{buildroot}%{_mandir}/man8/
install -m 0640 rsec.conf %{buildroot}%{_sysconfdir}/security
install -m 0750 rsec.crondaily %{buildroot}%{_sysconfdir}/cron.daily/rsec
install -m 0750 rsec.cronhourly %{buildroot}%{_sysconfdir}/cron.hourly/rsec
pushd %{buildroot}%{_sysconfdir}/cron.daily
    ln -s ../..%{_datadir}/rsec/urpmicheck.sh urpmicheck
popd

touch %{buildroot}/var/log/security.log


%post
touch /var/log/security.log && chmod 0640 /var/log/security.log


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog
%{_bindir}/promisc_check
%{_bindir}/rsec_find
%dir %_datadir/rsec
%{_datadir}/rsec/*
%{_mandir}/man8/rsec.8*
%dir %attr(0750,root,root) /var/log/security
%config(noreplace) %{_sysconfdir}/security/rsec.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsec
%config(noreplace) %{_sysconfdir}/cron.daily/rsec
%config(noreplace) %{_sysconfdir}/cron.hourly/rsec
%{_sysconfdir}/cron.daily/urpmicheck
%ghost %attr(0640,root,root) /var/log/security.log


%changelog
* Sun Jan 15 2006 Vincent Danen <vdanen-at-build.annvix.org>
- 0.62:
  - don't change ownership of unowned files

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Oct 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.61-2avx
- update the docs/configs to explain EXCLUDE_REGEXP better

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.61-1avx
- 0.61
  - don't check sysfs, usbfs, or hfs filesystems
  - fix user or homedir with spaces
  - new option to rsec.conf: EXCLUDE_REGEXP; used to exclude directories from
    the various reports
  - use getent rather than /etc/passwd for lookups (due to LDAP/NIS users)
  - allow % in filenames
  - removed xfs from remote filesystems
  - updated manpage and moved it from .3 to .8

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.60-1avx
- 0.60: uses rkhunter rather than chkrootkit

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51-2avx
- rebuild

* Sun Feb 13 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51-1avx
- 0.51: new option to exclude certain directories from the world-writeable file check

* Wed Jul 07 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.50-4avx
- Requires: mailx (for /bin/mail)

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.50-3avx
- Requires: packages, not files
- Annvix build

* Fri Apr 23 2004 Vincent Danen <vdanen@opensls.org> 0.50-2sls
- make urpmicheck.sh a bit more robust

* Wed Mar 10 2004 Vincent Danen <vdanen@opensls.org> 0.50-1sls
- first OpenSLS package based on msec-0.42-1mdk
