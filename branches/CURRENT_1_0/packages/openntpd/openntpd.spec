%define	name	openntpd
%define	version	20040824p
%define	release	1avx

Summary:	OpenNTPD is a secure implementation of the Network Time Protocol
Name:		%{name}
Version:	%{version}
Release:	%{release}
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
%patch0 -p0 -b .ntpuser

%build
%configure2_5x
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
%dir %attr(0750,nobody,nogroup) %dir %{_srvlogdir}/ntpd
%dir %{_srvdir}/ntpd
%{_srvdir}/ntpd/run
%dir %{_srvdir}/ntpd/log
%{_srvdir}/ntpd/log/run


%changelog
* Mon Sep 13 2004 Vincent Danen <vdanen@annvix.org> 20040824p-1avx
- initial Annvix package
- P0: set ntp user to ntp, not _ntp
