%define name ntp 
%define version 4.1.2
%define release 1mdk
%define realversion 4.1.2

Summary:	Synchronizes system time using the Network Time Protocol (NTP).
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-Style
Group:		System/Configuration/Other
Source0:	http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/%{name}-%{realversion}.tar.bz2
Source1:	ntp.conf
Source2:	ntp.keys
Source3:	ntpd.rc
Patch0:		ntp-4.0.99k-add_time_h.patch.bz2
Patch1:		ntp-4.1.1-biarch-utmp.patch.bz2
URL:		http://www.cis.udel.edu/~ntp
PreReq:		rpm-helper
Buildroot:	%{_tmppath}/%{name}-root

%description
The Network Time Protocol (NTP) is used to synchronize a computer's time
with another reference time source.  The ntp package contains utilities
and daemons which will synchronize your computer's time to Coordinated
Universal Time (UTC) via the NTP protocol and NTP servers.  Ntp includes
ntpdate (a program for retrieving the date and time from remote machines
via a network) and ntpd (a daemon which continuously adjusts system time).

Install the ntp package if you need tools for keeping your system's
time synchronized via the NTP protocol.

%prep 
%setup -q -n ntp-%{realversion}
%patch0 -p1 -b .add_time
%patch1 -p1 -b .biarch-utmp

%build
#CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr \
#        --sysconfdir=/etc --bindir='${prefix}/sbin'
#

%serverbuild
%configure2_5x
%make CFLAGS="$RPM_OPT_FLAGS" 
mv html/hints .

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall bindir=$RPM_BUILD_ROOT/usr/sbin

mkdir -p $RPM_BUILD_ROOT/etc/{ntp,rc.d/init.d}

install -m644 %{SOURCE1} $RPM_BUILD_ROOT/etc/ntp.conf
install -m600 %{SOURCE2} $RPM_BUILD_ROOT/etc/ntp/keys
touch $RPM_BUILD_ROOT/etc/ntp/step-tickers
install -m755 %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntpd

%post
%_post_service ntpd

%preun
%_preun_service ntpd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) /etc/ntp.conf
%config(noreplace) /etc/ntp/keys
%ghost %config(missingok) /etc/ntp/step-tickers
%doc html/* NEWS TODO 
/usr/sbin/ntp*
/usr/sbin/tickadj
%config(noreplace) /etc/rc.d/init.d/ntpd

%changelog
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
