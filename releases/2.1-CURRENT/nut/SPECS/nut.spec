#
# spec file for package nut
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision        $Rev$
%define name            nut
%define version         2.2.0
%define release         %_revrel

%define nutuser		ups

Summary:	Network UPS Tools Client Utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://random.networkupstools.org
Source0:	http://random.networkupstools.org/source/2.2/%{name}-%{version}.tar.gz
Source1:	http://random.networkupstools.org/source/2.2/%{name}-%{version}.tar.gz.sig
Source2:	upsd.run
Source3:	upsd.finish
Source4:	upsd-log.run
Source5:	upsmon.run
Source6:	upsmon.finish
Source7:	upsmon-log.run
Source8:	ups_command

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	libusb-devel
BuildRequires:	net-snmp-devel

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
Requires:	nut = %{version}
Requires(pre):	nut = %{version}
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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
env WANT_AUTOCONF_2_5=1 autoconf


%build
%serverbuild
%configure2_5x \
    --without-cgi \
    --with-snmp \
    --with-usb \
    --without-lib \
    --with-statepath=/var/run/ups \
    --with-drvpath=/sbin \
    --with-user=%{nutuser} \
    --with-group=%{nutuser} \
    --enable-shared \
    --sysconfdir=%{_sysconfdir}/ups \
    --with-pkgconfig-dir=%{_libdir}/pkgconfig

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/ups
mkdir -p %{buildroot}/var/run/ups
mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_srvdir}/{upsmon,upsd}/log
install -m 0740 %{_sourcedir}/upsd.run %{buildroot}%{_srvdir}/upsd/run
install -m 0740 %{_sourcedir}/upsd.finish %{buildroot}%{_srvdir}/upsd/finish
install -m 0740 %{_sourcedir}/upsd-log.run %{buildroot}%{_srvdir}/upsd/log/run
install -m 0740 %{_sourcedir}/upsmon.run %{buildroot}%{_srvdir}/upsmon/run
install -m 0740 %{_sourcedir}/upsmon.finish %{buildroot}%{_srvdir}/upsmon/finish
install -m 0740 %{_sourcedir}/upsmon-log.run %{buildroot}%{_srvdir}/upsmon/log/run

install -m 0750 %{_sourcedir}/ups_command %{buildroot}%{_sysconfdir}/ups/ups_command

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
%{_bindir}/upssched-cmd
%{_sbindir}/upsmon
%{_sbindir}/upssched
%{_mandir}/man5/upsmon.conf.5*
%{_mandir}/man5/upssched.conf.5*
%{_mandir}/man8/upsc.8*
%{_mandir}/man8/upscmd.8*
%{_mandir}/man8/upsrw.8*
%{_mandir}/man8/upslog.8*
%{_mandir}/man8/upsmon.8*
%{_mandir}/man8/upssched.8*

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
%{_datadir}/cmdvartab
%{_datadir}/driver.list
%{_mandir}/man5/ups.conf.5*
%{_mandir}/man5/upsd.conf.5*
%{_mandir}/man5/upsd.users.5*
%{_mandir}/man8/*.8*
%exclude %{_mandir}/man8/upsc.8*
%exclude %{_mandir}/man8/upscmd.8*
%exclude %{_mandir}/man8/upsrw.8*
%exclude %{_mandir}/man8/upslog.8*
%exclude %{_mandir}/man8/upsmon.8*
%exclude %{_mandir}/man8/upssched.8*

%files doc
%defattr(-,root,root)
%doc ChangeLog COPYING INSTALL MAINTAINERS NEWS README UPGRADING docs


%changelog
* Wed Sep 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.0
- 2.2.0
- add package sig and renumber sources
- rebuild against new net-snmp
- don't build the libs; nothing builds against nut or libupsclient
  (no more -devel package either)

* Sat Jan 27 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.5
- 2.0.5
- go back to using "make all usb snmp" or the usb drivers don't get built

* Mon Dec 18 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.4
- 2.0.4
- rebuild against new net-snmp

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.3
- 2.0.3
- drop P1
- fully include snmp support
- add -doc subpackage
- rebuild with gcc4
- rebuild against new libusb
- fix source url
- simplify manpage listing
- use %%_sourcedir/file instead of %%{SOURCEx}
- drop useless prereq on rpm-helper (for -devel)

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.1
- fix group

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
