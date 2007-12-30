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
%define	version		3.9p1
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
Source0:	ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.gz
Source1:	openntpd.run
Source2:	openntpd-log.run
Source3:	usr.sbin.ntpd.profile
Patch0:		openntpd-20040824p-avx-ntpuser.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-static-devel
BuildRequires:	autoconf2.5
BuildRequires:	bison
BuildRequires:	byacc
BuildRequires:	groff-for-man

Requires:	openssl
Requires:	execline
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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


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
install -m 0740 %{_sourcedir}/openntpd.run %{buildroot}%{_srvdir}/ntpd/run
install -m 0740 %{_sourcedir}/openntpd-log.run %{buildroot}%{_srvdir}/ntpd/log/run

mkdir -p %{buildroot}%{_profiledir}
install -m 0640 %{_sourcedir}/usr.sbin.ntpd.profile %{buildroot}%{_profiledir}/usr.sbin.ntpd


%pre
%_pre_useradd ntp /var/empty /sbin/nologin 87


%post
%_post_srv ntpd


%preun
%_preun_srv ntpd


%postun
%_postun_userdel ntp


%posttrans
%_aa_reload


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/ntpd.conf
%{_sbindir}/ntpd
%{_mandir}/man5/ntpd.conf.5*
%{_mandir}/man8/ntpd.8*
%dir %attr(0750,root,admin) %{_srvdir}/ntpd
%dir %attr(0750,root,admin) %{_srvdir}/ntpd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/ntpd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/ntpd/log/run
%config(noreplace) %attr(0640,root,root) %{_profiledir}/usr.sbin.ntpd

%files doc
%defattr(-,root,root)
%doc README ChangeLog


%changelog
* Sat Dec 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1
- rebuild with new %%_aa_reload macro definition

* Tue Dec 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1
- fix buildrequires

* Tue Jun 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1
- drop %%_touch_aa_reload; no longer needed

* Mon Jun 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1
- use %%posttrans to execute the apparmor reload, and use
  %%_touch_aa_reload to signal we want the profile reloaded

* Mon Jun 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1
- add a default AppArmor profile

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1
- rebuild against new openssl
- spec cleanups

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1
- 3.9p1
- add "-s" to ntpd call so that it sets the clock immediate on start
  if the skew is greater than 180s
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7p1
- Clean rebuild

* Sun Jan 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7p1
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
