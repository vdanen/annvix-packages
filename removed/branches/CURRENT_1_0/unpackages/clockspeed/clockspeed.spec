%define name	clockspeed
%define version	0.62
%define release	6avx

Summary:	Clock speed measurement and manipulation
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	D. J. Bernstein
Group:		System/Servers
URL:		http://cr.yp.to/clockspeed.html
Source0:	%{name}-%{version}.tar.gz
Source1:	clockspeed.run
Source3:	taiclockd.run
Source4:	taiclockd-log.run
Source5:	98_clockspeed.afterboot
Source6:	clockspeed.cron
Source7:	clockspeed.sysconfig
Patch0:		clockspeed-0.62-errno.patch.bz2
Patch1:		clockspeed-0.62-path.patch.bz2

Buildroot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.20

Requires:	daemontools, afterboot
Provides:	ntp
ExclusiveArch:	%{ix86}

%description
clockspeed uses a hardware tick counter to compensate for a
persistently fast or slow system clock. Given a few time
measurements from a reliable source, it computes and then
eliminates the clock skew. 

sntpclock checks another system's NTP clock, and prints the
results in a format suitable for input to clockspeed. sntpclock
is the simplest available NTP/SNTP client. 

taiclock and taiclockd form an even simpler alternative to SNTP.
They are suitable for precise time synchronization over a local
area network, without the hassles and potential security
problems of an NTP server. 

This version of clockspeed can use the Pentium RDTSC tick counter
or the Solaris gethrtime() nanosecond counter. 

%package devel
Summary:	The static library and headers for %{name}.
Group:		Development/Libraries

%description devel
The static library and headers for %{name}.

%prep

%setup -q
%patch0 -p1
%patch1 -p1 -b .path

%build
echo "diet gcc -Os -pipe" > conf-cc
echo "diet gcc -Os -static -s" > conf-ld
echo "%{_prefix}" >conf-home
make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man3

install -m0644 leapsecs.dat %{buildroot}%{_sysconfdir}/
install -m0755 clockspeed %{buildroot}%{_bindir}/
install -m0755 clockadd %{buildroot}%{_bindir}/
install -m0755 clockview %{buildroot}%{_bindir}/
install -m0755 sntpclock %{buildroot}%{_bindir}/
install -m0755 taiclock %{buildroot}%{_bindir}/
install -m0755 taiclockd %{buildroot}%{_bindir}/
install -m0644 *.1 %{buildroot}%{_mandir}/man1/

install -m0644 leapsecs.h %{buildroot}%{_includedir}/
install -m0644 tai.h %{buildroot}%{_includedir}/
install -m0644 taia.h %{buildroot}%{_includedir}/
install -m0644 libtai.a %{buildroot}%{_libdir}/
install -m0644 *.3 %{buildroot}%{_mandir}/man3/

mkdir -p %{buildroot}%{_srvdir}/{clockspeed,taiclockd/log}
mkdir -p %{buildroot}%{_srvlogdir}/taiclockd
install -m 0755 %{SOURCE1} %{buildroot}%{_srvdir}/clockspeed/run
install -m 0755 %{SOURCE3} %{buildroot}%{_srvdir}/taiclockd/run
install -m 0755 %{SOURCE4} %{buildroot}%{_srvdir}/taiclockd/log/run

mkdir -p %{buildroot}/var/lib/clockspeed
mkfifo -m 0600 %{buildroot}/var/lib/clockspeed/adjust
touch %{buildroot}/var/lib/clockspeed/atto

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE5} %{buildroot}%{_datadir}/afterboot/98_clockspeed

mkdir -p %{buildroot}%{_sysconfdir}/{cron.monthly,sysconfig}
install -m 0750 %{SOURCE6} %{buildroot}%{_sysconfdir}/cron.monthly/clockspeed
install -m 0640 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/clockspeed

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_mkafterboot
%_post_srv clockspeed
%_post_srv taiclockd

%preun
%_preun_srv clockspeed
%_preun_srv taiclockd

%postun
%_mkafterboot

%files
%defattr (-,root,root)
%doc BLURB CHANGES README TODO INSTALL THANKS
%{_sysconfdir}/leapsecs.dat
%config(noreplace) %{_sysconfdir}/cron.monthly/clockspeed
%config(noreplace) %{_sysconfdir}/sysconfig/clockspeed
%{_bindir}/clockspeed
%{_bindir}/clockadd
%{_bindir}/clockview
%{_bindir}/sntpclock
%{_bindir}/taiclock
%{_bindir}/taiclockd
%{_mandir}/man1/clockadd.1*
%{_mandir}/man1/clockspeed.1*
%{_mandir}/man1/clockview.1*
%{_mandir}/man1/sntpclock.1*
%{_mandir}/man1/taiclock.1*
%{_mandir}/man1/taiclockd.1*
%dir %{_srvdir}/clockspeed
%{_srvdir}/clockspeed/run
%dir %{_srvdir}/taiclockd
%dir %{_srvdir}/taiclockd/log
%{_srvdir}/taiclockd/run
%{_srvdir}/taiclockd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/taiclockd
%dir /var/lib/clockspeed
/var/lib/clockspeed/adjust
%attr(0600,root,root) /var/lib/clockspeed/atto
%{_datadir}/afterboot/98_clockspeed

%files devel
%defattr(-,root,root)
%{_includedir}/leapsecs.h
%{_includedir}/tai.h
%{_includedir}/taia.h
%{_libdir}/libtai.a
%{_mandir}/man3/leapsecs.3*
%{_mandir}/man3/tai.3*
%{_mandir}/man3/tai_pack.3*
%{_mandir}/man3/taia.3*
%{_mandir}/man3/taia_now.3*
%{_mandir}/man3/taia_pack.3*

%changelog
* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 0.62-6avx
- %%_post_srv and %%_preun_srv macros

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 0.62-5avx
- Annvix build

* Tue Jun 15 2004 Vincent Danen <vdanen@opensls.org> 0.62-4sls
- cron file needs to be executable
- make exclusive to x86; on amd64 it doesn't work very well

* Tue May 11 2004 Vincent Danen <vdanen@opensls.org> 0.62-3sls
- P1: put adjustment fifo in /var/lib/clockspeed
- include the adjustment fifo
- /etc/cron.monthly/clockspeed adjusts the clock if
  /etc/sysconfig/clockspeed is configured with an NTP server
- include afterboot man snippet
- atto file in /var/lib/clockspeed as well
- clockspeed doesn't log anything so don't need a log service

* Mon Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.62-2sls
- macros

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 0.62-1sls
- rebuild for OpenSLS
- tidy spec
- provides ntp
- added service files for clockspeed and taiclockd

* Thu Aug 28 2003 Oden Eriksson <oden.eriksson@deserve-it.com> 0.62-1mdk
- initial package
