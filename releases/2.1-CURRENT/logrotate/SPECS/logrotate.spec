#
# spec file for package logrotate
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		logrotate
%define version		3.7.5
%define release		%_revrel

Summary:	Rotates, compresses, and mails system logs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		http://download.fedora.redhat.com/pub/fedora/linux/core/development/source/SRPMS/
Source0:	ftp://ftp.redhat.com/pub/redhat/code/logrotate/%{name}-%{version}.tar.gz
Source1:	logrotate.conf.annvix
Patch0:		logrotate-3.7.5-mdv-run_scripts_with_arg0.patch
Patch1:		logrotate-3.7.5-mdv-stop_on_script_errors.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	popt-devel

%description
The logrotate utility is designed to simplify the administration of log
files on a system which generates a lot of log files.  Logrotate allows for
the automatic rotation compression, removal and mailing of log files.
Logrotate can be set to handle a log file daily, weekly,monthly or when the
log file gets to a certain size.  Normally, logrotate runs as a daily cron
job.


%prep
%setup -q
%patch0 -p1 -b .run_scripts_with_arg0
%patch1 -p1 -b .stop_on_script_errors


%build
%make RPM_OPT_FLAGS="%{optflags}" WITH_SELINUX=no


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make PREFIX=%{buildroot} MANDIR=%{_mandir} install
mkdir -p %{buildroot}%{_sysconfdir}/%{name}.d
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
mkdir -p %{buildroot}/var/lib

cat %{_sourcedir}/logrotate.conf.annvix > %{buildroot}%{_sysconfdir}/%{name}.conf
chmod 0644 %{buildroot}%{_sysconfdir}/%{name}.conf

install -m 0755 examples/%{name}.cron %{buildroot}%{_sysconfdir}/cron.daily/%{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ "${1}" == "1" ]; then
    /bin/touch %{_var}/lib/logrotate.staus
fi


%files
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/logrotate
%attr(0644,root,root) %{_mandir}/man8/logrotate.8*
%attr(0755,root,root) %{_sysconfdir}/cron.daily/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}.d


%changelog
* Sun Nov 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.7.5
- 3.7.5
- don't ship status files, create it in %%post
- don't rotate lastlog
- drop old P0; no longer required
- P0: run scripts passing a simple fixed $0 for error messages and such
- P1: stop processing logs when scripts exit with error

* Mon Aug 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7.3
- 3.7.3
- drop P1, P2
- updated P3 and renamed to P0
- spec cleanups
- do the make test

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7.1
- drop the docs (CHANGES)
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7.1
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.7.1-4avx
- sync with mdk 3.7.1-2mdk (sync with 3.7.1-7)
- fix S1 to set better perms for btmp

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.7.1-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.7.1-2avx
- bootstrap build

* Fri Dec 03 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.7.1-1avx
- 3.7.1

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.7-2avx
- Annvix build

* Tue May 11 2004 Vincent Danen <vdanen@opensls.org> 3.7-1sls
- 3.7 (grabbed from a Fedora SRPM since there doesn't seem to be a home for
  logrotate anywhere)
- include rotate support for /var/log/btmp
- NOTE: this version has hooks for SELinux, but we'll disable it until we
  get SELinux support all figured out

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 3.6.6-4sls
- minor spec cleanups

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 3.6.6-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
