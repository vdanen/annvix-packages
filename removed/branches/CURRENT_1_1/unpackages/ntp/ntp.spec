%define name	ntp 
%define version 4.2.0
%define release 1avx

Summary:	Synchronizes system time using the Network Time Protocol (NTP)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-Style
Group:		System/Servers
URL:		http://www.ntp.org/
Source0:	http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/%{name}-%{version}.tar.bz2
Source1:	ntp.conf
Source2:	ntp.keys
Source3:	ntpstat-0.2.tar.bz2
Source4:	ntp-4.1.2-rh-manpages.tar.bz2
Source5:	ntpd.run
Source6:	ntpd-log.run
Patch0:		ntp-4.1.1-biarch-utmp.patch.bz2
Patch1:		ntp-4.2.0-fdr-genkey3.patch.bz2
Patch2:		ntp-4.2.0-fdr-md5.patch.bz2
Patch3:		ntp-4.2.0-mdk-libtool.diff.bz2
Patch4:		ntp-4.2.0-fdr-droproot.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	openssl-static-devel, ncurses-devel, elfutils-devel, libcap-devel
BuildRequires:	autoconf2.5, automake1.7

PreReq:		rpm-helper, %{name}-client = %{version}
Requires:	libcap


%description
The Network Time Protocol (NTP) is used to synchronize a computer's time
with another reference time source.  The ntp package contains utilities
and daemons which will synchronize your computer's time to Coordinated
Universal Time (UTC) via the NTP protocol and NTP servers.  Ntp includes
ntpdate (a program for retrieving the date and time from remote machines
via a network) and ntpd (a daemon which continuously adjusts system time).

Install the ntp package if you need tools for keeping your system's
time synchronized via the NTP protocol.


%package client
Summary:	The ntpdate client for setting system time from NTP servers
Group:		System/Servers
Conflicts:	ntp < 4.2.0-1avx

%description client
The Network Time Protocol (NTP) is used to synchronize a computer's time
with another reference time source.  The ntp package contains utilities
and daemons which will synchronize your computer's time to Coordinated
Universal Time (UTC) via the NTP protocol and NTP servers.  Ntp includes
ntpdate (a program for retrieving the date and time from remote machines
via a network) and ntpd (a daemon which continuously adjusts system time).

ntpdate is a simple NTP client which allows a system's clock to be set
to match the time obtained by communicating with one or more servers.

ntpdate is optional (but recommended) if you're running an NTP server,
because initially setting the system clock to an almost-correct time
will help the NTP server synchronize faster.

The ntpdate client by itself is useful for occasionally setting the time on
machines that are not on the net full-time, such as laptops.


%prep 
%setup -q -n ntp-%{version} -a3 -a4

%patch0 -p1 -b .biarch-utmp
%patch1 -p1 -b .genkey3
%patch2 -p1 -b .md5
%patch3 -p1 -b .libtool
%patch4 -p1 -b .droproot

# fix strange perms
find html -type f | xargs chmod 644
find html -type d | xargs chmod 755

%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal-1.7; autoconf; automake-1.7 --add-missing

%serverbuild
%ifarch x86_64 amd64
# cheap hack to fix detection of openssl libs
perl -pi -e 's#ans="/usr/lib#ans="/usr/lib64#g' configure
%endif
%configure2_5x --libdir=%{_libdir} --with-crypto=openssl

%make CFLAGS="%{optflags}" 
mv html/hints .

make -C ntpstat-0.2 CFLAGS="%{optflags}"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_sysconfdir},%{_mandir}/man1}
%makeinstall bindir=$RPM_BUILD_ROOT%{_sbindir}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ntp
mkdir -p %{buildroot}{%{_srvdir}/ntpd/log,%{_srvlogdir}/ntpd}

install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/ntp.conf
install -m600 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/ntp/keys
touch $RPM_BUILD_ROOT%{_sysconfdir}/ntp/step-tickers

install -m 0755 ntpstat-0.2/ntpstat %{buildroot}%{_sbindir}/
install -m 0644 ntpstat-0.2/ntpstat.1 %{buildroot}%{_mandir}/man1/
install -m 0644 man/*.1 %{buildroot}%{_mandir}/man1/

install -m 0755 %{SOURCE5} %{buildroot}%{_srvdir}/ntpd/run
install -m 0755 %{SOURCE6} %{buildroot}%{_srvdir}/ntpd/log/run

mkdir -p %{buildroot}/var/lib/ntp
echo "0.0" >%{buildroot}/var/lib/ntp/drift


%pre
%_pre_useradd ntp /var/lib/ntp /sbin/nologin 87

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
%doc html NEWS TODO README* ChangeLog
%dir %{_sysconfdir}/ntp
%config(noreplace) %{_sysconfdir}/ntp.conf
%config(noreplace) %{_sysconfdir}/ntp/keys
%ghost %config(missingok) %{_sysconfdir}/ntp/step-tickers
%{_sbindir}/ntp-keygen
%{_sbindir}/ntp-wait
%{_sbindir}/ntpd
%{_sbindir}/ntpdc
%{_sbindir}/ntpq
%{_sbindir}/ntpstat
%{_sbindir}/ntptime
%{_sbindir}/ntptrace
%{_sbindir}/tickadj
%{_mandir}/man1/ntpd.1*
%{_mandir}/man1/ntpdc.1*
%{_mandir}/man1/ntpq.1*
%{_mandir}/man1/ntpstat.1*
%{_mandir}/man1/ntptime.1*
%{_mandir}/man1/ntptrace.1*
%{_mandir}/man1/tickadj.1*
%dir %{_srvdir}/ntpd
%dir %{_srvdir}/ntpd/log
%{_srvdir}/ntpd/run
%{_srvdir}/ntpd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/ntpd
%dir %attr(-,ntp,ntp) /var/lib/ntp
%config(noreplace) %attr(0644,ntp,ntp) %verify(not md5 size mtime) /var/lib/ntp/drift

%files client
%defattr(-,root,root)
%{_sbindir}/ntpdate
%{_mandir}/man1/ntpdate.1*

%changelog
* Sat Sep 11 2004 Vincent Danen <vdanen@annvix.org> 4.2.0-1avx
- 4.2.0
- Annvix build (re-introduce); use this rather than clockspeed
  since clockspeed has issues on x86_64
- major spec cleanups
- run scripts
- P4: from Fedora - drop root privs after binding
- static uid/gid 87 for ntp
- set the drift file to /var/lib/ntp/drift from /etc/ntp/drift
- BuildRequires: libcap-devel
- Requires: libcap
- cheap fix to build ntp-keygen on x86_64
- sync with cooker 4.2.0-8mdk:
  - S3, S4 from Fedora (oden)
  - broke out ntpdate as that's the only one needed if using an external
    clock source (description stolen from debian) (oden)
  - P1, P2: from Fedora (fix #10159) (oden)
  - P3: libtool stuff (oden)
  - added more pool.ntp.org entries in ntpd.conf (warly)

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.1.2-2sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Warly <warly@mandrakesoft.com> 4.1.2-1mdk
- new version
- add pool.ntp.org as default server

* Tue Apr 15 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1.1-4mdk
- Fix mess introduced in previous release

* Tue Apr  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1.1-3mdk
- Patch1: Handle biarch struct utmp
- rpmlint fixes: rpm-helper, use %%configure

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1.1-2mdk
- Automated rebuild in gcc3.1 environment

* Wed Feb 27 2002 Warly <warly@mandrakesoft.com> 4.1.1-1mdk
- final 4.1.1 version

* Tue Dec 11 2001 Warly <warly@mandrakesoft.com> 4.1.0b-0.rc1.1mdk
- new version

* Fri Aug 24 2001 Warly <warly@mandrakesoft.com> 4.1.0-1mdk
- new version

* Tue Jul  3 2001 Pixel <pixel@mandrakesoft.com> 4.0.99k-8mdk
- add a commented - line "server clock.via.net" (will be replaced by DrakX)

* Fri May 11 2001 Warly <warly@mandrakesoft.com> 4.0.99k-7mdk
- remove restrict default ignore from config file

* Sat Apr  7 2001 Warly <warly@mandrakesoft.com> 4.0.99k-6mdk
- s/fopen/fdopen/ in patch tmp
- add restrict default ignore to answer only known server

* Fri Apr 06 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.99k-5mdk
- include patches to fix buffer overflows (MDKSA-2001:036)

* Thu Mar 29 2001 Warly <warly@mandrakesoft.com> 4.0.99k-4mdk
- use %%serverbuild and co macro

* Wed Mar 14 2001 Warly <warly@mandrakesoft.com> 4.0.99k-3mdk
- fix build

* Thu Aug 31 2000 Warly <warly@mandrakesoft.com> 4.0.99k-2mdk
- add condrestart

* Mon Jul 24 2000 Warly <warly@mandrakesoft.com> 4.0.99k-1mdk
- new release
- BM

* Wed Apr 05 2000 Daouda Lo <daouda@mandrakesoft.com> 4.0.99g-3mdk
- fix the conf files permissions
- bunzip'ed conf files

* Fri Mar 31 2000 Warly <warly@mandrakesoft.com> 4.0.99g-2mdk
- New group: System/Configuration/Other

* Tue Mar 07 2000 Daouda LO <daouda@mandrakesoft.com>
- Mandrakised (relocatable + %%define )

* Sun May 23 1999 David E. Myers <dem@skyline.rtp.nc.us>
- Changes for submission to Red Hat Contrib|Net.

* Wed Apr 14 1999 Cristian Gafton <gafton@redhat.com>
- disallow remote updates by default in ntp.conf (#2170)

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- use %configure
- fix initscript not to sit out the output of ntpdate (use syslog instead)
- eliminate subshell from the install stage

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)

* Sun Nov 22 1998 Jeff Johnson <jbj@redhat.com>
- ntp.conf: default local clock stratum to 10.

* Wed Oct 21 1998 Jeff Johnson <jbj@redhat.com>
- update to 5.93e.

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries

* Thu Aug  6 1998 Jeff Johnson <jbj@redhat.com>
- update to 5.93c.
- implement suggestions from James Youngman <JYoungman@vggas.com>:
-   correct default /etc/ntp/keys 
-   use /etc/ntp/step-tickers for ntpdate hosts

* Sun May 10 1998 Cristian Gafton <gafton@redhat.com>
- start it after named

* Mon May 04 1998 Jeff Johnson <jbj@redhat.com>
- Update to 5.93.

* Mon Feb  2 1998 Jeff Johnson <jbj@jbj.org>
- Fiddles for RH-5.0. Update to xntp3-5.92.

* Mon Feb  2 1998 Jeff Johnson <jbj@jbj.org>
- Fiddles for RH-5.0. Update to xntp3-5.92.

* Sat Oct 18 1997 Manoj Kasichainula <manojk@io.com>
- Initial release for 5.91
