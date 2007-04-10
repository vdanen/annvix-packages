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
%define version		3.7.3
%define release		%_revrel

Summary:	Rotates, compresses, and mails system logs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		http://download.fedora.redhat.com/pub/fedora/linux/core/1/i386/os/SRPMS
Source0:	ftp://ftp.redhat.com/pub/redhat/code/logrotate/%{name}-%{version}.tar.bz2
Source1:	logrotate.conf.annvix
Patch0:		logrotate-3.7.3-mdv-glob.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	popt-devel

%description
Logrotate is designed to ease administration of systems that generate
large numbers of log files. It allows automatic rotation, compression,
removal, and mailing of log files. Each log file may be handled daily,
weekly, monthly, or when it grows too large.


%prep
%setup -q
%patch0 -p0 -b .glob


%build
%make RPM_OPT_FLAGS="%{optflags}"


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

touch %{buildroot}/var/lib/logrotate.status


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/logrotate
%attr(0644,root,root) %{_mandir}/man8/logrotate.8*
%attr(0755,root,root) %{_sysconfdir}/cron.daily/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}.d
%attr(0644,root,root) %verify(not size md5 mtime) %config(noreplace) /var/lib/logrotate.status


%changelog
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
