%define name	clockspeed
%define version	0.62
%define release	1sls

Summary:	Clock speed measurement and manipulation
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	D. J. Bernstein
Group:		System/Servers
URL:		http://cr.yp.to/clockspeed.html
Source0:	%{name}-%{version}.tar.gz
Source1:	clockspeed.run
Source2:	clockspeed-log.run
Source3:	taiclockd.run
Source4:	taiclockd-log.run
Patch0:		clockspeed-0.62-errno.patch.bz2

Buildroot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.20

Requires:	daemontools
Provides:	ntp

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

mkdir -p %{buildroot}/var/service/{clockspeed,taiclockd}/log
mkdir -p %{buildroot}/var/log/supervise/{clockspeed,taiclockd}
install -m 0755 %{SOURCE1} %{buildroot}/var/service/clockspeed/run
install -m 0755 %{SOURCE2} %{buildroot}/var/service/clockspeed/log/run
install -m 0755 %{SOURCE3} %{buildroot}/var/service/taiclockd/run
install -m 0755 %{SOURCE4} %{buildroot}/var/service/taiclockd/log/run

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc BLURB CHANGES README TODO INSTALL THANKS
%{_sysconfdir}/leapsecs.dat
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
%dir /var/service/clockspeed
%dir /var/service/clockspeed/log
/var/service/clockspeed/run
/var/service/clockspeed/log/run
%dir /var/service/taiclockd
%dir /var/service/taiclockd/log
/var/service/taiclockd/run
/var/service/taiclockd/log/run
%dir %attr(0750,nobody,nogroup) /var/log/supervise/clockspeed
%dir %attr(0750,nobody,nogroup) /var/log/supervise/taiclockd

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
* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 0.62-1sls
- rebuild for OpenSLS
- tidy spec
- provides ntp
- added service files for clockspeed and taiclockd

* Thu Aug 28 2003 Oden Eriksson <oden.eriksson@deserve-it.com> 0.62-1mdk
- initial package
