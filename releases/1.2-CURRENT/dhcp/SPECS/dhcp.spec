#
# spec file for package dhcp
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		dhcp
%define version		3.0.3
%define release		%_revrel
%define epoch		2

%define _catdir		/var/cache/man

%define _requires_exceptions perl(Win32API::Registry)

Summary:	The ISC DHCP (Dynamic Host Configuration Protocol) server/relay agent/client
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	Distributable
Group:		System/Servers
URL:		http://www.isc.org/dhcp.html
Source0:	ftp://ftp.isc.org/isc/%{name}/%{name}-%{version}.tar.gz
Source1:	dhcpd.conf.sample
Source3:	dhcp-dynamic-dns-examples.tar.bz2
Source5:	update_dhcp.pl
Source6:	dhcpreport.pl
Source7:	ftp://ftp.isc.org/isc/%{name}/%{name}-%{version}.tar.gz.asc
Source8:	dhcpd.run
Source9:	dhcpd-log.run
Source10:	dhcrelay.run
Source11:	dhcrelay-log.run
Source12:	CONFIGFILE.env
Source13:	INTERFACES.env
Source14:	LEASEFILE.env
Source15:	OPTIONS.env
Source16:	OPTIONS-dhcrelay.env
Source17:	SERVERS-dhcrelay.env
Patch0:		dhcp-3.0.1-ifup.patch
# http://www.episec.com/people/edelkind/patches/
Patch1:		dhcp-3.0.1-paranoia.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl groff-for-man

Requires:	bash
Obsoletes:	dhcpd

%description 
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows 
individual devices on an IP network to get their own network configuration
information (IP address, subnetmask, broadcast address, etc.) from a DHCP
server. The overall purpose of DHCP is to make it easier to administer a 
large network. The dhcp package includes the DHCP server and a DHCP relay
agent. You will also need to install the dhcp-client or dhcpcd package,
or pump or dhcpxd, which provides the DHCP client daemon, on client machines.

If you want the DHCP server and/or relay, you will also need to install the
dhcp-server and/or dhcp-relay packages.


%package common
Summary:	The ISC DHCP (Dynamic Host Configuration Protocol) server
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(postun): rpm-helper

%description common
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows 
individual devices on an IP network to get their own network 
configuration information (IP address, subnetmask, broadcast address, 
etc.) from a DHCP server.  The overall purpose of DHCP is to make it 
easier to administer a large network.  The dhcp package includes the 
DHCP server and a DHCP relay agent.

You will also need to install the dhcp-client or dhcpcd package, or pump or
dhcpxd, which provides the DHCP client daemon, on  client machines. If you
want the DHCP server and/or relay, you will also need to install the
dhcp-server and/or dhcp-relay packages.


%package server
Summary:	The ISC DHCP (Dynamic Host Configuration Protocol) server
Group:		System/Servers
Requires:	dhcp-common = %{epoch}:%{version}, bash
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Obsoletes:	dhcp
Provides:	dhcp

%description server
DHCP server is the Internet Software Consortium (ISC) DHCP server for various
UNIX operating systems. It allows a UNIX mac hine to serve DHCP requests from
the network.


%package client
Summary:	The ISC DHCP (Dynamic Host Configuration Protocol) client
Group:		System/Servers
Requires:	dhcp-common = %{epoch}:%{version}, bash

%description client
DHCP client is the Internet Software Consortium (ISC) DHCP client for various
UNIX operating systems.  It allows a UNIX mac hine to obtain it's networking
parameters from a DHCP server.


%package relay
Summary:	The ISC DHCP (Dynamic Host Configuration Protocol) relay
Group:		System/Servers
Requires:	dhcp-common = %{epoch}:%{version}-%{release} /bin/sh
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description relay
DHCP relay is the Internet Software Consortium (ISC) relay agent for DHCP
packets. It is used on a subnet with DHCP clients to "relay" their requests
to a subnet that has a DHCP server on it. Because DHCP packets can be
broadcast, they will not be routed off of the local subnet. The DHCP relay
takes care of this for the client. You will need to set the environment
variable SERVERS and optionally OPTIONS in /etc/sysconfig/dhcrelay before
starting the server.


%package devel
Summary:	Development headers and libraries for the dhcpctl API
Group:		Development/Other
Requires:	dhcp-common = %{epoch}:%{version}

%description devel
DHCP devel contains all of the libraries and headers for developing with the
Internet Software Consortium (ISC) dhcpctl API.


%prep
%setup -q -a 3 -n %{name}-%{version}
%patch0 -p1 -b .ifup
%patch1 -p1 -b .paranoia

cat << EOF >site.conf
VARDB=%{_localstatedir}/dhcp
LIBDIR=%{_libdir}
INCDIR=%{_includedir}
ADMMANDIR=%{_mandir}/man8
FFMANDIR=%{_mandir}/man5
LIBMANDIR=%{_mandir}/man3
USRMANDIR=%{_mandir}/man1
EOF
cat << EOF >>includes/site.h
#define _PATH_DHCPD_PID		"%{_localstatedir}/dhcp/dhcpd.pid"
#define _PATH_DHCPD_DB		"%{_localstatedir}/dhcp/dhcpd.leases"
#define _PATH_DHCLIENT_DB	"%{_localstatedir}/dhcp/dhclient.leases"
EOF


%build
echo 'int main() { return sizeof(void *) != 8; }' | gcc -xc - -o is_ptr64
./is_ptr64 && PTR64_FLAGS="-DPTRSIZE_64BIT"

./configure --copts "%{optflags} $PTR64_FLAGS -DPARANOIA"

#-DEARLY_CHROOT

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_localstatedir}/dhcp
mkdir -p %{buildroot}/var/run/dhcpd

%makeinstall_std

touch %{buildroot}%{_localstatedir}/dhcp/dhcpd.leases
touch %{buildroot}%{_localstatedir}/dhcp/dhclient.leases

install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}
install -m 0755 %{SOURCE5} %{buildroot}%{_sbindir}/
install -m 0755 %{SOURCE6} %{buildroot}%{_sbindir}/

find . -type d -exec chmod 0755 {} \;
find . -type f -exec chmod 0644 {} \;

rm -rf doc/ja_JP.eucJP

mkdir -p %{buildroot}%{_srvdir}/{dhcpd,dhcrelay}/{log,env}

install -m 0740 %{SOURCE8} %{buildroot}%{_srvdir}/dhcpd/run
install -m 0740 %{SOURCE9} %{buildroot}%{_srvdir}/dhcpd/log/run

install -m 0640 %{SOURCE12} %{buildroot}%{_srvdir}/dhcpd/env/CONFIGFILE
install -m 0640 %{SOURCE13} %{buildroot}%{_srvdir}/dhcpd/env/INTERFACES
install -m 0640 %{SOURCE14} %{buildroot}%{_srvdir}/dhcpd/env/LEASEFILE
install -m 0640 %{SOURCE15} %{buildroot}%{_srvdir}/dhcpd/env/OPTIONS

install -m 0740 %{SOURCE10} %{buildroot}%{_srvdir}/dhcrelay/run
install -m 0740 %{SOURCE11} %{buildroot}%{_srvdir}/dhcrelay/log/run
install -m 0640 %{SOURCE16} %{buildroot}%{_srvdir}/dhcrelay/env/OPTIONS
install -m 0640 %{SOURCE17} %{buildroot}%{_srvdir}/dhcrelay/env/SERVERS


%pre common
%_pre_useradd dhcp %{_localstatedir}/dhcp /bin/false 89

%post server
if [ -d /var/log/supervise/dhcpd -a ! -d /var/log/service/dhcpd ]; then
    mv /var/log/supervise/dhcpd /var/log/service/
fi
%_post_srv dhcpd
# New dhcpd lease file
if [ ! -f %{_localstatedir}/dhcp/dhcpd.leases ]; then
    touch %{_localstatedir}/dhcp/dhcpd.leases && chown dhcp:dhcp %{_localstatedir}/dhcp/dhcpd.leases
fi

%preun server
%_preun_srv dhcpd

%postun common
%_postun_userdel dhcp

%post relay
if [ -d /var/log/supervise/dhcrelay -a ! -d /var/log/service/dhcrelay ]; then
    mv /var/log/supervise/dhcrelay /var/log/service/
fi
%_post_srv dhcrelay

%preun relay
%_preun_srv dhcrelay

%post client
touch %{_localstatedir}/dhcp/dhclient.leases

%postun client
rm -rf %{_localstatedir}/dhcp/dhclient.leases


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files common
%defattr(-,root,root)
%doc README RELNOTES doc contrib
%attr(0750,dhcp,dhcp) %dir %{_localstatedir}/dhcp
%{_mandir}/man5/dhcp-options.5*

%files server
%defattr(-,root,root)
%doc server/dhcpd.conf tests/failover
%config(noreplace) %ghost %{_localstatedir}/dhcp/dhcpd.leases
%{_sysconfdir}/dhcpd.conf.sample
%{_sbindir}/dhcpd
%{_sbindir}/update_dhcp.pl
%{_sbindir}/dhcpreport.pl
%{_bindir}/omshell
%{_mandir}/man1/omshell.1*
%{_mandir}/man3/omapi.3*
%{_mandir}/man5/dhcpd.conf.5*
%{_mandir}/man5/dhcpd.leases.5*
%{_mandir}/man5/dhcp-eval.5*
%{_mandir}/man8/dhcpd.8*
%dir %attr(0750,root,admin) %{_srvdir}/dhcpd
%dir %attr(0750,root,admin) %{_srvdir}/dhcpd/log
%dir %attr(0750,root,admin) %{_srvdir}/dhcpd/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/dhcpd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/dhcpd/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/dhcpd/env/CONFIGFILE
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/dhcpd/env/INTERFACES
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/dhcpd/env/LEASEFILE
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/dhcpd/env/OPTIONS

%files relay
%defattr(-,root,root)
%{_sbindir}/dhcrelay
%{_mandir}/man8/dhcrelay.8*
%dir %attr(0750,root,admin) %{_srvdir}/dhcrelay
%dir %attr(0750,root,admin) %{_srvdir}/dhcrelay/log
%dir %attr(0750,root,admin) %{_srvdir}/dhcrelay/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/dhcrelay/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/dhcrelay/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/dhcrelay/env/OPTIONS
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/dhcrelay/env/SERVERS

%files client
%defattr(-,root,root)
%doc client/dhclient.conf
%config(noreplace) %ghost %{_localstatedir}/dhcp/dhclient.leases
%attr (0755,root,root) /sbin/dhclient-script
/sbin/dhclient
%{_mandir}/man5/dhclient.conf.5*
%{_mandir}/man5/dhclient.leases.5*
%{_mandir}/man8/dhclient.8*
%{_mandir}/man8/dhclient-script.8*

%files devel
%defattr(-,root,root)
%{_mandir}/man3/*
%{_libdir}/*
%{_includedir}/*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Sep 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.3-4avx
- revert the quoting in the runscript; doesn't work

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.3-3avx
- quote the args in the runscripts

* Sun Sep 25 2005 Sean P. Thomas <spt-at-build.annvix.org> 3.0.3-2avx
- use execlineb for run scripts and used envdirs.
- pass -d to dhcpd in run script to log to stderr (vdanen)

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.3-1avx
- 3.0.3
- drop P2; fixed upstream
- create a default dhcrelay config file instead of an empty one
- use execlineb for run scripts
- move logdir to /var/log/service/sshd
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.2-4avx
- fix perms on run scripts

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.2-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.2-2avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.2-1avx
- 3.0.2
- require setup >= 2.4-16avx
- P1: this is a chroot patch, but I don't see the point of chrooting
  dhcpd although making it drop privs is useful
- S13: makes it easier to chroot the server
- fixed pid file location for dhcpd
- P2: allows build against gcc-3.4.3
- spec cleanups
- update runscripts for logger
- drop initscripts
- dhcpd runs as static uid/gid user dhcp (89)

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0.1-1avx
- 3.0.1
- update run scripts
- updated P1 from mdk (flepied): only change the hostname if
  NEEDHOSTNAME=yes; assign default gateway by interface

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0-1.rc14.1avx
- 3.0-1.rc14 (security fixes for CAN-2004-0460, CAN-2004-0461)
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 3.0-1.rc13.1sls
- 3.0-1.rc13
- S12 is the default sysconfig file
- add -q to OPTIONS in the run file
- sync with 3.0-1.rc13.4mdk:
  - beautify dhcpd.conf.sample (olivier)


* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 3.0-1.rc12.6sls
- minor spec cleanups
- some syncs with 3.0-1.rc13.3mdk:
  - remove the ja_JP.eucJP redundant directory (florin)
  - move the dhcp-options manpage to the common package
  - remove the no longer existing ANONCVS, CHANGES, COPYRIGHT files
  - add epoch to requires

* Wed Feb 04 2004 Vincent Danen <vdanen@opensls.org> 3.0-1.rc12.5sls
- remove initscripts
- supervise scripts
- remove PreReq on chkconfig, service

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 3.0-1.rc12.4sls
- real RC12

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 3.0-1.rc12.3sls
- OpenSLS build
- tidy spec

* Thu Sep 04 2003 Florin <florin@mandrakesoft.com> 3.0-1.rc12.2mdk
- fix the postun script

* Mon Sep 01 2003 Florin <florin@mandrakesoft.com> 3.0-1.rc12.1mdk
- 3.0.1rc12

* Thu Aug 21 2003 Florin <florin@mandrakesoft.com> 3.0-1rc11.1mdk
- 3.0.1rc11 instead of 3.0-2pl2 fixes some pxe related prbs

* Wed Aug 20 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.0-2pl2.7mdk
- 64-bit & lib64 fixes

* Thu Jul 31 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.0-2pl2.6mdk
- rebuild

* Fri Mar  7 2003 Frederic Lepied <flepied@mandrakesoft.com> 3.0-2pl2.5mdk
- corrected creation of resolv.conf when there is only a nameserver
without a domainname.

* Mon Mar  3 2003 Frederic Lepied <flepied@mandrakesoft.com> 3.0-2pl2.4mdk
- corrected NEEDHOSTNAME test

* Mon Jan 20 2003 Frederic Lepied <flepied@mandrakesoft.com> 3.0-2pl2.3mdk
- apply patch2 on the right file and merge it in patch1

* Mon Jan 20 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0-2pl2.2mdk
- Call /sbin/update-resolvrd if present.

* Fri Jan 17 2003 Florin <florin@mandrakesoft.com> 3.0-2pl2.1mdk
- 3.0pl2
- remove the cat files
- silly version name, if you ask me ;o) (an ancient typo)
- better use of macros names

* Thu Jan 16 2003 Frederic Lepied <flepied@mandrakesoft.com> 3.0-1rc10.4mdk
- handle NEEDHOSTNAME in dhclient-script 

* Tue Nov 19 2002 Frederic Lepied <flepied@mandrakesoft.com> 3.0-1rc10.3mdk
- make dhclient-script silent when pinging (when dhcp server is down)

* Tue Nov 19 2002 Frederic Lepied <flepied@mandrakesoft.com> 3.0.1rc10.2mdk
- corrected dhclient-script to conform to the initscripts

* Fri Nov 08 2002 Florin <florin@mandrakesoft.com> 3.0.1rc10.1mdk
- 3.0.1rc10
- add the asc file and keep the sources in gz format

* Wed Nov 06 2002 Florin <florin@mandrakesoft.com> 3.01rc9.3mdk
- fix the leases path (thx to A.Duclos)

* Wed Sep 18 2002 Florin <florin@mandrakesoft.com> 3.01rc9.2mdk
- update the dhcpd.conf.sample (thx to a. delorbeau)

* Sun Jun 09 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 3.01rc9.1mdk
- 3.0.1rc9

* Fri Mar 08 2002 Florin <florin@mandrakesoft.com> 3.01rc8.1mdkmdk
- 3.0.1rc8

* Wed Feb 20 2002 Florin <florin@mandrakesoft.com> 3.01rc7.1mdk
- 3.0.1rc7

* Sat Jan 19 2002 Davud BAUDENS <bauudens@mandrakesoft.com> 3.0.1rc6.2mdk
- Fix Group: for devel package
- Use human readable descriptions
- Requires: %%{version}-%%{release} and not only %%{version}

* Fri Jan 18 2002 Florin <florin@mandrakesoft.com> 3.0.1rc6.1mdk
- 3.0.1rc6
- add the omapi man pages
- remove the laziness weird line

* Tue Jan 15 2002 Florin <florin@mandrakesoft.com> 3.0.1rc5.1mdk
- 3.0.1rc5

* Tue Nov 06 2001 Florin <florin@mandrakesoft.com> 3.0-1rc4.1mdk
- 3.0.1rc4

* Mon Nov 05 2001 Florin <florin@mandrakesoft.com> 3.0-1rc3.1mdk
- 3.0.1rc3

* Wed Oct 31 2001 Florin <florin@mandrakesoft.com> 3.0-1rc2.1mdk
- 3.0.1rc2

* Thu Oct 25 2001 Florin <florin@mandrakesoft.com> 3.0-1.rc1.2mdk
- add the dhcpreport.pl script

* Wed Oct 17 2001 Florin <florin@mandrakesoft.com> 3.0-1.rc1.1mdk
- 3.0.1rc1
- fix the doc permissions
- add the %_preun/post_service macros

* Fri Oct 05 2001 Florin <florin@mandrakesoft.com> 3.0-1mdk
- 3.0
- add the cat pages 
- add the touch command in post section of dhcp-client

* Fri Aug 24 2001 Florin <florin@mandrakesoft.com> 3.0-0.rc12.1mdk
- 3.0rc12

* Thu Aug 16 2001 Florin <florin@mandrakesoft.com> 3.0-0.rc11.1mdk
- 3.0rc11

* Fri Aug 10 2001 Florin <florin@mandrakesoft.com> 3.0-0.rc10.3mdk
- requires /bin/sh

* Tue Jul 17 2001 Florin <florin@mandrakesoft.com> 3.0-0.rc10.2mdk
- test if /etc/dhcpd.conf exists before the update_dhcp script in post

* Mon Jul 02 2001 Florin <florin@mandrakesoft.com> 3.0-0.rc10.1mdk
- 3.0rc10

* Wed Jun 27 2001 Florin <florin@mandrakesoft.com> 3.0-0.rc8pl2.1mdk
- real working example files (the same ones from the bind package)
- 3.0rc8pl2

* Tue Jun 26 2001 Florin Grad <florin@mandrakesoft.com> 3.0-0.rc8pl1.1mdk
- 3.0.rc8pl1
- update the examples files in relation with bind 

* Wed Jun 13 2001 Florin Grad <florin@mandrakesoft.com> 3.0-0.rc8.2mdk
- a better update_dhcp.pl script

* Mon Jun 11 2001 Florin Grad <florin@mandrakesoft.com> 3.0-0.rc8.1mdk
- 3.0rc8
- modify patches
- put dhclient-script in /sbin
- add the update_dhcp.pl script

* Thu May 31 2001 Florin Grad <florin@mandrakesoft.com> 3.0rc7-2mdk
- merge with redhat packages recommended by isc
- so we now have 5 packages: dhcp, dhcp-server, dhcp-relay, dhcp-client, dhcp-devel

* Sun May 27 2001 Stefan van der Eijk <stefan@eijk.nu> 3.0rc7-1mdk
- 3.0rc7

* Tue Mar 27 2001 Florin Grad <florin@mandrakesoft.com> 3.0b2pl23-1mdk
- pl23

* Wed Feb 28 2001 Florin Grad <florin@mandrakesoft.com> 3.0b2pl18-1mdk
- pl18
- update the mdkpathcorrect patch

* Mon Dec 04 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl11-1mdk
- pl11

* Fri Nov 17 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl9-6mdk
- chkconfig is now set to 345

* Fri Nov 17 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl9-5mdk
- add dynamic dns config file example

* Mon Nov 06 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl9-4mdk
- minor fixes in the spec files

* Mon Nov 06 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl9-3mdk
- fix some errors in the initscripts

* Tue Oct 17 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl9-2mdk
- modify the init script not to depend on linuxconf (thanks to A.Skwar) 

* Tue Oct 17 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl9-1mdk
- 3.0b2pl9

* Sun Oct 15 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.0b2pl8-1mdk
- new patch level version.

* Thu Oct  5 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0b2pl2-7mdk
- fixes initscript (s/return/exit)

* Thu Sep 28 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl2-6mdk
- /etc/dhcpd.conf.sample instead of /etc/dhcpd.conf

* Wed Sep 27 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl2-5mdk
- modify dhcpd.init

* Wed Sep 27 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl2-4mdk
- make a copy of the *doc*/dhcpd.conf.sample file to /etc/dhcpd.conf

* Thu Sep 21 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0b2pl2-3mdk
- chkconfig --del has to be done in %preun not %postun !!

* Tue Sep 07 2000 Florin Grad <florin@mandrakesoft.com> 3.0b2pl2-2mdk
- adding noreplace in the config section 

* Thu Sep 07 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.0b2pl2-1mdk
- new and shiny dhcp.

* Tue Aug 30 2000 Florin Grad <florin@mandrakesoft.com> 3.0b1pl17-6mdk
- recompile because of some modif on rpm

* Tue Aug 29 2000 Florin Grad <florin@mandrakesoft.com> 3.0b1pl17-5mdk
- updating the macros

* Mon Jul 24 2000 Vincent Saugey <vince@mandrakesoft.com> 3.0b1pl17-4mdk
- Really fixed this update script

* Mon Jul 24 2000 Vincent Saugey <vince@mandrakesoft.com> 3.0b1pl17-3mdk
- Fix a little typo error in upgrade script

* Fri Jul 21 2000 Vincent Saugey <vince@mandrakesoft.com> 3.0b1pl17-2mdk
- Remove older patch remade clean one
- corrected init file (no more error for config without linux-conf)
- Now, full FHS compliant, with leases in /var/lib/dhcpd

* Fri Jul 21 2000 Vincent Saugey <vince@mandrakesoft.com> 3.0b1pl17-1mdk
- Up to 3.0b1pl17
- Slipt in 3 packages, new one for relay.
- Correct man file path
- Clean spec file (use macro)

* Sat Jul  1 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0b1pl15-1mdk
- Fix %doc.
- 3.0b1pl15.

* Wed Jun 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0b1pl12-6mdk
- Correct patches.

* Wed Jun 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0b1pl12-5mdk
- Add security patch.
- Clan upmacros spec file.

* Thu Apr 13 2000 Vincent Saugey <vince@mandrakesoft.com> 3.0b1pl12-4mdk
- Made init script at config file

* Fri Mar 24 2000 - Jean-Michel Dault <jmdault@mandrakesoft.com> 3.0b1pl12-3mdk
- modified init script so it binds to the correct interface. It reads
  /etc/conf.linuxconf to do it.

* Tue Mar 21 2000 - Vincent Saugey <vince@mandrakesoft.com> 3.0b1pl12-2mdk
- correct group

* Mon Dec 06 1999 - David BAUDENS <baudens@mandrakesoft.com>
- Fix build as user
- Add "%%define prefix /usr"
- Replace /%%{prefix} by  %%{prefix}

* Mon Dec 01 1999 Philippe Libat <philippe@mandrakesoft.com>
- Subpackages dhcp-client
- Upgrade of patch.
- Change dhcpd.leases directory

* Mon Jul 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Prefixing the package.
- Upgrade of patch.
- 3.0b1pl0.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- copy the source file in %prep, not move

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Mon Jan 11 1999 Erik Troan <ewt@redhat.com>
- added a sample dhcpd.conf file
- we don't need to dump rfc's in /usr/doc

* Sun Sep 13 1998 Cristian Gafton <gafton@redhat.com>
- modify dhcpd.init to exit if /etc/dhcpd.conf is not present

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- Upgraded to 2.0b1pl6 (patch1 no longer needed).

* Thu Jun 11 1998 Erik Troan <ewt@redhat.com>
- applied patch from Chris Evans which makes the server a bit more paranoid
  about dhcp requests coming in from the wire

* Mon Jun 01 1998 Erik Troan <ewt@redhat.com>
- updated to dhcp 2.0b1pl1
- got proper man pages in the package

* Tue Mar 31 1998 Erik Troan <ewt@redhat.com>
- updated to build in a buildroot properly
- don't package up the client, as it doens't work very well <sigh>

* Tue Mar 17 1998 Bryan C. Andregg <bandregg@redhat.com>
- Build rooted and corrected file listing.

* Mon Mar 16 1998 Mike Wangsmo <wanger@redhat.com>
- removed the actual inet.d links (chkconfig takes care of this for us)
  and made the %postun section handle upgrades.

* Mon Mar 16 1998 Bryan C. Andregg <bandregg@redhat.com>
- First package.
