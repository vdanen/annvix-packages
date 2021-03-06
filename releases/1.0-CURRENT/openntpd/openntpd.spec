%define	name	openntpd
%define	version	3.6.1p1
%define	release	1avx
%define epoch	1

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
Patch0:		openntpd-20040824p-avx-ntpuser.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	openssl-static-devel, autoconf2.5

Requires:	openssl
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

mkdir -p %{buildroot}{%{_srvdir}/ntpd/log,%{_srvlogdir}/ntpd}
install -m 0750 %{SOURCE1} %{buildroot}%{_srvdir}/ntpd/run
install -m 0750 %{SOURCE2} %{buildroot}%{_srvdir}/ntpd/log/run

%pre
%_pre_useradd ntp /var/empty /sbin/nologin 87

%post
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
%dir %attr(0750,logger,logger) %dir %{_srvlogdir}/ntpd
%dir %{_srvdir}/ntpd
%{_srvdir}/ntpd/run
%dir %{_srvdir}/ntpd/log
%{_srvdir}/ntpd/log/run


%changelog
* Fri Mar 04 2005 Vincent Danen <vdanen@annvix.org> 3.6.1p1-1avx
- 3.6.1p1
- user logger for logging
- drop P1; specify privsep user and path instead

* Wed Nov  3 2004 Vincent Danen <vdanen@annvix.org> 3.6p1-1avx
- 3.6p1
- Epoch: 1

* Mon Sep 13 2004 Vincent Danen <vdanen@annvix.org> 20040824p-1avx
- initial Annvix package
- P0: set ntp user to ntp, not _ntp
