#
# spec file for package openntpd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	revision	$Rev$
%define	name		openntpd
%define	version		3.7p1
%define	release		%_revrel
%define epoch		1

Summary:	OpenNTPD is a secure implementation of the Network Time Protocol
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	BSD
Group:		System/Servers
URL:		http://www.openntpd.org/
Source0:	%{name}-%{version}.tar.gz
Source1:	openntpd.run
Source2:	openntpd-log.run
Patch0:		openntpd-20040824p-avx-ntpuser.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-static-devel, autoconf2.5

Requires:	openssl, execline
Requires(pre):	rpm-helper
Requires(preun): rpm-helper
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Provides:	ntp
Obsoletes:	ntp

%description
OpenNTPD is a FREE implementation of the Network Time Protocol. It
provides the ability to sync the local clock to remote NTP servers
and can act as NTP server itself, redistributing the local clock.


%prep
%setup -q


%build
%configure2_5x \
    --with-privsep-user=ntp \
    --with-privsep-path=/var/empty
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

mkdir -p %{buildroot}%{_srvdir}/ntpd/log
install -m 0740 %{SOURCE1} %{buildroot}%{_srvdir}/ntpd/run
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/ntpd/log/run


%pre
%_pre_useradd ntp /var/empty /sbin/nologin 87

%post
if [ -d /var/log/supervise/ntpd -a ! -d /var/log/service/ntpd ]; then
    mv /var/log/supervise/ntpd /var/log/service/
fi
%_post_srv ntpd

%preun
%_preun_srv ntpd

%postun
%_postun_userdel ntp


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README ChangeLog
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/ntpd.conf
%{_sbindir}/ntpd
%{_mandir}/man5/ntpd.conf.5*
%{_mandir}/man8/ntpd.8*
%dir %attr(0750,root,admin) %{_srvdir}/ntpd
%dir %attr(0750,root,admin) %{_srvdir}/ntpd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/ntpd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/ntpd/log/run


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sun Jan 08 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Tue Aug 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.7p1-2avx
- don't include the logdir

* Tue Aug 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.7p1-1avx
- 3.7p1
- use execlineb for run scripts
- move logdir to /var/log/service/ntpd
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.1p1-4avx
- fix perms on run scripts

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.1p1-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.1p1-2avx
- rebuild

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.1p1-1avx
- 3.6.1p1
- user logger for logging
- drop P1; specify privsep user and path instead

* Wed Nov  3 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.6p1-1avx
- 3.6p1
- Epoch: 1

* Mon Sep 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 20040824p-1avx
- initial Annvix package
- P0: set ntp user to ntp, not _ntp
