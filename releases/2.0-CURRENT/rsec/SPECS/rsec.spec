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
%define version		0.66
%define release		%_revrel

Summary:	Security Reporting tool for Annvix
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		http://svn.annvix.org/cgi-bin/viewvc.cgi/rsec/?root=tools
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	bash
Requires:	coreutils
Requires:	perl-base
Requires:	diffutils
Requires:	shadow-utils
Requires:	gawk
Requires:	mailx
Requires:	setup >= 2.2.0-21mdk
Requires:	iproute2
Conflicts:	passwd < 0.67
Conflicts:	msec

%description
The Annvix Security Reporting tool (rsec) is largely based on the
Mandriva Linux msec program.  rsec produces the same reports as msec, but
does not manage permission issues or system configuration changes.  It is
nothing more than a reporting tool to advise you of changes to your system
and potential problem areas.  Any changes or fixes are entirely up to the
user to correct.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


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

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog

%changelog
* Sat Sep 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.66
- fix URL

* Wed Jul 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.66
- 0.66:
  - fix call to logger

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.65
- 0.65:
  - security_check.sh: don't check /etc/shadow if it doesn't exist
  - rsec.conf: turn off CHECK_SHADOW by default since we use tcb instead
  - urpmicheck.sh: also check update/check apt if it's available
- fix URL
- add -doc subpackage

* Mon Mar 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.63
-0.63:
  - change reporting of unowned user/group files since we don't chown
    them anymore
  - document the EXCLUDEDIR option and include it in the default rsec.conf
    with a default entry of "/var/lib/rsbac"
  - set EXCLUDE_REGEXP to exclude /override and /var/tmp/php_sessions by
    default

* Sun Jan 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.62
- 0.62:
  - don't change ownership of unowned files

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.61
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.61
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.61
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
