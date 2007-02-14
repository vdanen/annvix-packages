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
%define version		3.0.5
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
Patch0:		dhcp-3.0.4b2-ifup.patch
# http://www.episec.com/people/edelkind/patches/
Patch1:		dhcp-3.0.1-paranoia.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl
BuildRequires:	groff-for-man

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
Requires:	dhcp-common = %{epoch}:%{version}
Requires:	bash
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
Requires:	dhcp-common = %{epoch}:%{version}
Requires:	bash

%description client
DHCP client is the Internet Software Consortium (ISC) DHCP client for various
UNIX operating systems.  It allows a UNIX mac hine to obtain it's networking
parameters from a DHCP server.


%package relay
Summary:	The ISC DHCP (Dynamic Host Configuration Protocol) relay
Group:		System/Servers
Requires:	dhcp-common = %{epoch}:%{version}-%{release}
Requires:	bash
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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


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

./configure --copts "%{optflags} $PTR64_FLAGS -DPARANOIA -DLDAP_DEPRECATED"

#-DEARLY_CHROOT

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_sbindir}}
mkdir -p %{buildroot}%{_localstatedir}/dhcp
mkdir -p %{buildroot}/var/run/dhcpd

%makeinstall_std

touch %{buildroot}%{_localstatedir}/dhcp/dhcpd.leases
touch %{buildroot}%{_localstatedir}/dhcp/dhclient.leases

install -m 0644 %{_sourcedir}/dhcpd.conf.sample %{buildroot}%{_sysconfdir}
install -m 0755 %{_sourcedir}/update_dhcp.pl %{buildroot}%{_sbindir}/
install -m 0755 %{_sourcedir}/dhcpreport.pl %{buildroot}%{_sbindir}/

find . -type d -exec chmod 0755 {} \;
find . -type f -exec chmod 0644 {} \;

rm -rf doc/ja_JP.eucJP

mkdir -p %{buildroot}%{_srvdir}/{dhcpd,dhcrelay}/{log,env}

install -m 0740 %{_sourcedir}/dhcpd.run %{buildroot}%{_srvdir}/dhcpd/run
install -m 0740 %{_sourcedir}/dhcpd-log.run %{buildroot}%{_srvdir}/dhcpd/log/run

install -m 0640 %{_sourcedir}/CONFIGFILE.env %{buildroot}%{_srvdir}/dhcpd/env/CONFIGFILE
install -m 0640 %{_sourcedir}/INTERFACES.env %{buildroot}%{_srvdir}/dhcpd/env/INTERFACES
install -m 0640 %{_sourcedir}/LEASEFILE.env %{buildroot}%{_srvdir}/dhcpd/env/LEASEFILE
install -m 0640 %{_sourcedir}/OPTIONS.env %{buildroot}%{_srvdir}/dhcpd/env/OPTIONS

install -m 0740 %{_sourcedir}/dhcrelay.run %{buildroot}%{_srvdir}/dhcrelay/run
install -m 0740 %{_sourcedir}/dhcrelay-log.run %{buildroot}%{_srvdir}/dhcrelay/log/run
install -m 0640 %{_sourcedir}/OPTIONS-dhcrelay.env %{buildroot}%{_srvdir}/dhcrelay/env/OPTIONS
install -m 0640 %{_sourcedir}/SERVERS-dhcrelay.env %{buildroot}%{_srvdir}/dhcrelay/env/SERVERS


%pre common
%_pre_useradd dhcp %{_localstatedir}/dhcp /bin/false 89


%post server
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
%attr(0750,dhcp,dhcp) %dir %{_localstatedir}/dhcp
%{_mandir}/man5/dhcp-options.5*

%files server
%defattr(-,root,root)
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
%config(noreplace) %ghost %{_localstatedir}/dhcp/dhclient.leases
%attr (0755,root,root) /sbin/dhclient-script
/sbin/dhclient
%{_mandir}/man5/dhclient.conf.5*
%{_mandir}/man5/dhclient.leases.5*
%{_mandir}/man8/dhclient.8*
%{_mandir}/man8/dhclient-script.8*

%files devel
%defattr(-,root,root)
%{_libdir}/*
%{_includedir}/*
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc README RELNOTES doc contrib/3.0b1-lease-convert server/dhcpd.conf tests/failover
%doc client/dhclient.conf


%changelog
* Wed Feb 14 2007 Ying-Hung Chen <ying-at-yingternet.com> 3.0.5
- 3.0.5

* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.4
- 3.0.4
- updated P0
- drop S7; gpg can't verify any of their sha{1,512,256} sigs for some reason
  so no point in keeping it
- add -doc subpackage
- rebuild with gcc4
- use %%_sourcedir/file instead of %%{SOURCEx}

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.3
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.3
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
