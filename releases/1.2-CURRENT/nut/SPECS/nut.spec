#
# spec file for package nut
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id: httpd.spec 5157 2006-01-19 20:27:35Z vdanen $

%define revision        $Rev: 5159 $
%define name            nut
%define version         2.0.1
%define release         %_revrel

%define nutuser		ups

Summary:	Network UPS Tools Client Utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Hardware
URL:		http://random.networkupstools.org
Source0:	%{name}-%{version}.tar.bz2
Source1:	upsd.run
Source2:	upsd.finish
Source3:	upsd-log.run
Source4:	upsmon.run
Source5:	upsmon.finish
Source6:	upsmon-log.run
Source7:	ups_command
#Source1:	upsd
#Source2:	upsmon
Patch0:		nut-2.0.1-lib64.patch.bz2
Patch1:		bouissou2.patch.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5 libusb-devel

Requires(pre):	rpm-helper >= 0.8
Requires(preun): rpm-helper >= 0.8
Requires(post):	rpm-helper >= 0.8
Requires(postun): rpm-helper >= 0.8

%description
These programs are part of a developing project to monitor the assortment 
of UPSes that are found out there in the field. Many models have serial 
ports of some kind that allow some form of state checking. This
capability has been harnessed where possible to allow for safe shutdowns, 
live status tracking on web pages, and more.

This package includes the client utilities that are required to monitor a
UPS that the client host is powered from - either connected directly via
a serial port (in which case the nut-server package needs to be installed on
this machine) or across the network (where another host on the network
monitors the UPS via serial cable and runs the main nut package to allow
clients to see the information).


%package server
Summary:	Network UPS Tools server
Group:		System/Servers
Requires:	nut = %{version}-%{release}
Requires(pre):	nut = %{version}-%{release}
Requires(preun): rpm-helper >= 0.8
Requires(post):	rpm-helper >= 0.8

%description server
These programs are part of a developing project to monitor the assortment 
of UPSes that are found out there in the field. Many models have serial 
serial ports of some kind that allow some form of state checking. This
capability has been harnessed where possible to allow for safe shutdowns, 
live status tracking on web pages, and more.

This package is the main NUT upsd daemon and the associated per-UPS-model
drivers which talk to the UPSes.  You also need to install the base NUT
package.


%package devel
Summary:	Development for NUT Client
Group:		Monitoring
Prereq:		rpm-helper >= 0.8

%description devel
This package contains the development header files and libraries
necessary to develop NUT client applications.


%prep
%setup -q
%patch0 -p1 -b .lib64
env WANT_AUTOCONF_2_5=1 autoconf
%patch1 -p1


%build
%serverbuild
%configure2_5x \
    --without-cgi \
    --with-statepath=/var/run/ups \
    --with-drvpath=/sbin \
    --with-user=%{nutuser} \
    --with-group=%{nutuser} \
    --enable-shared \
    --sysconfdir=%{_sysconfdir}/ups

# workaround buggy parrallel build:
make all usb snmp


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/ups
mkdir -p %{buildroot}/var/run/ups
mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install-conf
#make DESTDIR=%{buildroot} install-all-drivers
make DESTDIR=%{buildroot} install-lib
make DESTDIR=%{buildroot} install-usb

mkdir -p %{buildroot}%{_srvdir}/{upsmon,upsd}/log
install -m 0740 %{SOURCE1} %{buildroot}%{_srvdir}/upsd/run
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/upsd/finish
install -m 0740 %{SOURCE3} %{buildroot}%{_srvdir}/upsd/log/run
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/upsmon/run
install -m 0740 %{SOURCE5} %{buildroot}%{_srvdir}/upsmon/finish
install -m 0740 %{SOURCE6} %{buildroot}%{_srvdir}/upsmon/log/run

install -m 0750 %{SOURCE7} %{buildroot}%{_sysconfdir}/ups/ups_command

# move the *.sample config files to their real locations
for file in %{buildroot}%{_sysconfdir}/ups/*.sample
do
    mv $file %{buildroot}%{_sysconfdir}/ups/`basename $file .sample`
done

mv %{buildroot}%{_sysconfdir}/ups/upsmon.conf %{buildroot}%{_sysconfdir}/ups/upsmon.conf.sample
perl -pi -e 's/# RUN_AS_USER nutmon/RUN_AS_USER ups/g' %{buildroot}%{_sysconfdir}/ups/upsmon.conf.sample
perl -pi -e 's|CMDSCRIPT /usr/local/ups/bin/upssched-cmd|CMDSCRIPT /etc/ups/ups_command|g' %{buildroot}%{_sysconfdir}/ups/upsmon.conf.sample

cp -af data/driver.list docs/


%pre
# Create an UPS user.
%_pre_useradd ups /var/run/ups /bin/false 93
%_pre_groupadd tty ups ups
%_pre_groupadd usb ups ups


%preun
# only do this if it is not an upgrade
%_preun_srv upsmon


%post
%_post_srv upsmon


%postun
%_postun_userdel ups


%preun server
%_preun_srv upsd


%post server
%_post_srv upsd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc CHANGES COPYING CREDITS INSTALL MAINTAINERS NEWS README UPGRADING docs
%dir %attr(750,ups,ups) /var/run/ups
%dir %attr(755,root,root) %{_sysconfdir}/ups
%config(noreplace) %attr(640,root,ups) %{_sysconfdir}/ups/upssched.conf
%attr(640,root,ups) %{_sysconfdir}/ups/upsmon.conf.sample
%config(noreplace) %attr(0750,root,ups) %{_sysconfdir}/ups/ups_command
%dir %attr(0750,root,admin) %{_srvdir}/upsmon
%dir %attr(0750,root,admin) %{_srvdir}/upsmon/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/upsmon/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/upsmon/finish
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/upsmon/log/run
%{_bindir}/upsc
%{_bindir}/upscmd
%{_bindir}/upsrw
%{_bindir}/upslog
%{_sbindir}/upsmon
%{_sbindir}/upssched
%{_mandir}/man5/upsmon.conf.5.bz2
%{_mandir}/man5/upssched.conf.5.bz2
%{_mandir}/man8/upsc.8.bz2
%{_mandir}/man8/upscmd.8.bz2
%{_mandir}/man8/upsrw.8.bz2
%{_mandir}/man8/upslog.8.bz2
%{_mandir}/man8/upsmon.8.bz2
%{_mandir}/man8/upssched.8.bz2

%files server
%defattr(-,root,root)
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/ups/ups.conf
%config(noreplace) %attr(640,root,ups) %{_sysconfdir}/ups/upsd.users
%config(noreplace) %attr(640,root,ups) %{_sysconfdir}/ups/upsd.conf
%dir %attr(0750,root,admin) %{_srvdir}/upsd
%dir %attr(0750,root,admin) %{_srvdir}/upsd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/upsd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/upsd/finish
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/upsd/log/run
/sbin/*
%{_sbindir}/upsd
%{_bindir}/libupsclient-config
%{_datadir}/cmdvartab
%{_datadir}/driver.list
%{_libdir}/pkgconfig/libupsclient.pc
%{_mandir}/man5/ups.conf.5.bz2
%{_mandir}/man5/upsd.conf.5.bz2
%{_mandir}/man5/upsd.users.5.bz2
%{_mandir}/man8/belkin.8.bz2
%{_mandir}/man8/belkinunv.8.bz2
%{_mandir}/man8/bestups.8.bz2
%{_mandir}/man8/bestuferrups.8.bz2
%{_mandir}/man8/cyberpower.8.bz2
%{_mandir}/man8/cpsups.8.bz2
%{_mandir}/man8/everups.8.bz2
%{_mandir}/man8/etapro.8.bz2
%{_mandir}/man8/fentonups.8.bz2
%{_mandir}/man8/genericups.8.bz2
%{_mandir}/man8/isbmex.8.bz2
%{_mandir}/man8/liebert.8.bz2
%{_mandir}/man8/masterguard.8.bz2
%{_mandir}/man8/mge-utalk.8.bz2
%{_mandir}/man8/apcsmart.8.bz2
%{_mandir}/man8/nutupsdrv.8.bz2
%{_mandir}/man8/oneac.8.bz2
%{_mandir}/man8/powercom.8.bz2
%{_mandir}/man8/sms.8.bz2
%{_mandir}/man8/snmp-ups.8.bz2
%{_mandir}/man8/tripplite.8.bz2
%{_mandir}/man8/tripplitesu.8.bz2
%{_mandir}/man8/victronups.8.bz2
%{_mandir}/man8/upsd.8.bz2
%{_mandir}/man8/upsdrvctl.8.bz2
%{_mandir}/man8/mge-shut.8.bz2
%{_mandir}/man8/energizerups.8.bz2
%{_mandir}/man8/safenet.8.bz2
%{_mandir}/man8/hidups.8.bz2
%{_mandir}/man8/newhidups.8.bz2
%{_mandir}/man8/ippon.8.bz2
%{_mandir}/man8/bestfcom.8.bz2
%{_mandir}/man8/metasys.8.bz2
%{_mandir}/man8/mustek.8.bz2
%{_mandir}/man8/powermust.8.bz2

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libupsclient.a
%{_mandir}/man3/upscli_*.3.bz2


%changelog
* Tue Jan 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.1
- first Annvix build
- change statepath from /var/state/ups to /var/run/ups (makes more sense as
  this removes the need for another single-use directory tree (/var/state is
  not used anywhere else))
- not everyone gets to own /etc/ups; now only nut owns it since everything else
  that would requires it anyways
- drop nut-cgi; it would require a lot of graphics libs, some we ship and some
  we don't
- drop buildreq on net-snmp; we don't ship that either
- make nut-server require nut in Requires(pre) so we don't have to useradd twice
- adjust %%_pre_groupadd call to our syntax
- run scripts
- add a ups_command script to handle AT events and toss it in /etc/ups marking it
  %%config(noreplace) so it can be easily customized

* Wed Jan 04 2006 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-5mdk
- rebuilt against new net-snmp with new major (10)

* Wed Dec 21 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-4mdk
- rebuilt against net-snmp that has new major (9)

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-3mdk
- rebuilt against openssl-0.9.8a

* Tue Mar 22 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.1-2mdk
- lib64 fixes (again)

* Mon Feb 28 2005 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1:2.0.1-1mdk
- 2.0.1
- adapt patchs from Michel Bouissou

* Thu Feb 10 2005 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1:2.0.0-4mdk
- upsd poweroff script clean: remove the sleep and let the halt script continue
- add upsd service status option
- add Michel Bouissou's patch

* Fri Oct 22 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.0-3mdk
- lib64 fixes

* Tue Oct 05 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.0-2mdk
- workaround buggy parrallel build
- package again driver list
- patch 2: fix compiling

* Fri Mar 26 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 2.0.0-1mdk
- 2.0.0

* Wed Mar 24 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.2-1mdk
- 1.4.2 final (with no changements from previous pre2 release)

* Tue Mar 16 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.2-0.pre2.1mdk
- New release with security and kernel 2.6 fixs
- Change URL

* Thu Mar  4 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-10mdk
- Clean remove (bis repetita)

* Wed Mar  3 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-9mdk
- Clean remove

* Wed Mar  3 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-8mdk
- Force remove old init scripts even if they have been customised

* Tue Feb 24 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-7mdk
- Add Epoch required by new rpm

* Fri Jan 23 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-6mdk
- Orthographical correction for i18n team

* Tue Jan 20 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-5mdk
- Fix initscripts (Bug report from Henning Kulander)

* Mon Jan 19 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-4mdk
- Fix upsd initscript

* Tue Jan  6 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-2mdk
- Add dummycons driver and correction in upsd script

* Tue Dec  9 2003 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-1mdk
- New release

* Mon Dec 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.4.1-0.7mdk
- buildrequires net-snmp-devel

* Tue Dec  5 2003 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-0.6mdk
- More clean

* Tue Dec  4 2003 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-0.5mdk
- Clean the init script upsd

* Tue Dec  2 2003 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-0.4mdk
- pre4 release
- The init scripts read now some parameters directly from upsmon.conf
- Remove patch0 and add the parameters snmp and hidups to make instead

* Wed Nov 26 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.4.1-0.3mdk
- fix packaging in order to enable update
- fix server update when service is down

* Thu Nov 20 2003 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.1-0.pre3.1mdk
- New release
- Remove bad require in devel package
- Adapt patch 0 to new release and add the snmp-ups driver
- patch 1 to add parseconf.h in the devel package

* Fri Oct 31 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.4.0-3mdk
- patch 0: support ups connected through usb

* Tue Oct 21 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.0-2mdk
- fix deps

* Wed Jul 30 2003 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.4.0-1mdk
- New stable tree: 1.4.0 released

* Tue Jul 29 2003 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.2.3-2mdk
- Add cgi conflict with apcupsd wich is using the same file name for its cgi

* Wed Jul 23 2003 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.2.3-1mdk
- New release
- Change gid of upssched.conf, upsd.conf & upsd.users

* Fri Jan 24 2003 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.2.1-4mdk
- Requires

* Sat Dec 28 2002 Stefan van der Eijk <stefan@eijk.nu> 1.2.1-2mdk
- BuildRequires

* Fri Dec 20 2002 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.2.1-1mdk
- New Release

* Thu Nov 14 2002 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.2.0-1mdk
- New Release
- Do not use the buggy macro %_pre_groupadd anymore
- Create the devel package

* Thu Aug 29 2002 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.0.0-4mdk
- TODO

* Mon Aug 26 2002 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.0.0-3mdk
- Change STATEPATH, change owner of upsd.* files and modify init scripts

* Mon Aug 26 2002 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.0.0-2mdk
- Add the user ups to the group tty and usb with rpmhelper.
- Add new runlevel scripts
- Remove upspowerdown: now supported in the Mandrake halt init script.

* Wed Aug 21 2002 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.0.0-1mdk
- New release
- Use rpm-helper
- Add some new manuals to %files

* Mon Jul 22 2002 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 0.50.0-1mdk
- New release
- Add upssched-cmd in the doc directory

* Wed Feb 07 2002 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 0.45.3-2mdk
- Specfile adaptations for Mandrake Linux.

* Wed Oct 24 2001 Peter Bieringer <pb@bieringer.de> (0.45.3pre1)
- Take man path given by rpm instead of hardwired
- Add some missing man pages to %files

* Wed Feb 07 2001 Karl O. Pinc <kop@meme.com> (0.44.3-pre2)
- Cgi package buildrequires gd >= 1.6
- Added man pages for apcsmart and powercom models

* Tue Dec 05 2000 <Nigel.Metheringham@InTechnology.co.uk> (0.44.2)
- Made cgi package standalone (needs no other parts of NUT)
- Moved some configs into cgi
- Shared hosts.conf between cgi & main

* Fri Nov 24 2000 <Nigel.Metheringham@InTechnology.co.uk> (0.44.2)
- Moved models to be more FHS compliant and make sure they are there
  if everything but root is unmounted
- Moved a few things around

* Mon Aug 21 2000 <Nigel.Metheringham@Vdata.co.uk> (0.44.1)
- Added new model drivers into rpm list
- Made it wildcard more stuff so this doesn't need to be
  maintained for every little change.
  ** NOTE this breaks things if modelpath isn't distinct **

* Mon Jul 17 2000 <Nigel.Metheringham@Vdata.co.uk> (0.44.0)
- Fixed some problems in the spec file
- Dropped the older changelog entries since there is some
  intermediate history thats been missed.
- Added new model drivers into rpm list
- Updated descriptions somewhat

