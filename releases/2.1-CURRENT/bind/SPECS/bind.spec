#
# spec file for package bind
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		bind
%define version		9.4.2
%define release		%_revrel

%define their_version	9.4.2

Summary:	A DNS (Domain Name System) server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Distributable
Group:		System/Servers
URL:		http://www.isc.org/products/BIND/
Source0:	ftp://ftp.isc.org/isc/%{name}9/%{their_version}/%{name}-%{their_version}.tar.gz
Source1:	ftp://ftp.isc.org/isc/%{name}9/%{their_version}/%{name}-%{their_version}.tar.gz.asc
Source2:	bind-manpages.tar.bz2
Source3:	caching-nameserver.tar.bz2
Source4:	bind-9.3.1-missing_tools.tar.gz
Source5:	dhcp-dynamic-dns-examples.tar.bz2
Source6:	named.init
Source7:	OPTIONS.env
Source8:	keygen.c
Source9:	ftp://FTP.RS.INTERNIC.NET/domain/named.root
Source10:	named.run
Source11:	named.finish
Source12:	named-log.run
#Source13:       rndc.key
Patch1:		bind-9.4.1-fallback-to-second-server.diff
Patch5:		bind-9.3.0beta2-libtool.diff
Patch6:		libbind-9.3.1rc1-fix_h_errno.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel
BuildRequires:	autoconf
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	multiarch-utils >= 1.0.3

Requires(post):	rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(postun): rpm-helper
Requires:	bind-utils >= %{version}-%{release}
Obsoletes:	libdns0
Provides:	libdns0

%description
BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(domain Name System) protocols. BIND includes a DNS server (named), 
which resolves host names to IP addresses, and a resolver library 
(routines for applications to use when interfacing with DNS).  A DNS 
server allows clients to name resources or objects and share the 
information with other network machines.  The named DNS server can be 
used on workstations as a caching name server, but is generally only 
needed on one machine for an entire network.  Note that the 
configuration files for making BIND act as a simple caching nameserver 
are included in the caching-nameserver package.  

Install the bind package if you need a DNS server for your network.  If
you want bind to act a caching name server, you will also need to install
the caching-nameserver package.

Many BIND 8 features previously unimplemented in BIND 9, including 
domain-specific forwarding, the $GENERATE master file directive, and
the "blackhole", "dialup", and "sortlist" options Forwarding of dynamic
update requests; this is enabled by the "allow-update-forwarding" option 
A new, simplified database interface and a number of sample drivers based
on it; see doc/dev/sdb for details 
Support for building single-threaded servers for environments that do not 
supply POSIX threads 
New configuration options: "min-refresh-time", "max-refresh-time", 
"min-retry-time", "max-retry-time", "additional-from-auth",
"additional-from-cache", "notify explicit" 
Faster lookups, particularly in large zones. 


%package utils
Summary:	Utilities for querying DNS name servers
Group:		Networking/Other

%description utils
Bind-utils contains a collection of utilities for querying DNS (Domain
Name Service) name servers to find out information about Internet hosts.
These tools will provide you with the IP addresses for given host names,
as well as other information about registered domains and network 
addresses.


%package devel
Summary:	Include files and libraries needed for bind DNS development
Group:		Development/C

%description devel
The bind-devel package contains all the include files and the
library required for DNS (Domain Name Service) development for
BIND versions 9.x.x.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q  -n %{name}-%{their_version} -a2 -a3 -a4 -a5
%patch1 -p1 -b .fallback-to-second-server
#%patch -p1 -b .overflow
%patch5 -p1 -b .libtool
%patch6 -p1 -b .fix_h_errno

#(cd contrib/queryperf && autoconf-2.13)
tar -xjf %{_sourcedir}/dhcp-dynamic-dns-examples.tar.bz2


%build
%serverbuild
%configure \
    --localstatedir=/var \
    --enable-ipv6 \
    --disable-threads \
    --with-openssl=%{_includedir}/openssl

# override CFLAGS for better security
make CFLAGS="-O2 -Wall -pipe"

gcc %{optflags} -o dns-keygen %{_sourcedir}/keygen.c


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
pushd doc
    rm -rf html
popd
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_var}/{run/named,named}
mkdir -p %{buildroot}%{_mandir}/man3

mkdir -p %{buildroot}{%{_bindir},%{_includedir},%{_libdir}}
mkdir -p %{buildroot}%{_mandir}/{man1,man5,man8}
mkdir -p %{buildroot}%{_docdir}/

%makeinstall_std
#tar -xjf %{_sourcedir}/%{name}-manpages.tar.bz2 -C %{buildroot}%{_mandir}
# fix man pages
install -m 0644 man5/resolver.5 %{buildroot}%{_mandir}/man5/
ln -s resolver.5.bz2 %{buildroot}%{_mandir}/man5/resolv.5.bz2

install -m 0755 contrib/named-bootconf/named-bootconf.sh %{buildroot}%{_sbindir}/named-bootconf

install -m 0755 dns-keygen -D %{buildroot}%{_sbindir}/dns-keygen

# make the chroot
install -d %{buildroot}%{_localstatedir}/named/{dev,etc}
install -d %{buildroot}%{_localstatedir}/named/var/{log,run,tmp}
install -d %{buildroot}%{_localstatedir}/named/var/named/{master,slaves,reverse}

install -m 0644 caching-nameserver/named.conf %{buildroot}%{_localstatedir}/named/etc/named.conf
install -m 0644 caching-nameserver/rndc.conf %{buildroot}%{_localstatedir}/named/etc/rndc.conf
install -m 0644 caching-nameserver/rndc.key %{buildroot}%{_localstatedir}/named/etc/rndc.key
#install -m 0644 %{_sourcedir}/rndc.key %{buildroot}%{_localstatedir}/named/etc/rndc.key
install -m 0644 caching-nameserver/logging.conf %{buildroot}%{_localstatedir}/named/etc/logging.conf
install -m 0644 caching-nameserver/trusted_networks_acl.conf %{buildroot}%{_localstatedir}/named/etc/trusted_networks_acl.conf
install -m 0644 caching-nameserver/bogon_acl.conf %{buildroot}%{_localstatedir}/named/etc/bogon_acl.conf
install -m 0644 caching-nameserver/localdomain.zone %{buildroot}%{_localstatedir}/named/var/named/master/localdomain.zone
install -m 0644 caching-nameserver/localhost.zone %{buildroot}%{_localstatedir}/named/var/named/master/localhost.zone
install -m 0644 caching-nameserver/named.broadcast %{buildroot}%{_localstatedir}/named/var/named/reverse/named.broadcast
install -m 0644 caching-nameserver/named.ip6.local %{buildroot}%{_localstatedir}/named/var/named/reverse/named.ip6.local
install -m 0644 caching-nameserver/named.local %{buildroot}%{_localstatedir}/named/var/named/reverse/named.local
install -m 0644 caching-nameserver/named.zero %{buildroot}%{_localstatedir}/named/var/named/reverse/named.zero
install -m 0644 caching-nameserver/hosts %{buildroot}%{_localstatedir}/named/etc/hosts

# fix some compat symlinks
ln -s %{_localstatedir}/named/etc/named.conf %{buildroot}%{_sysconfdir}/named.conf
ln -s %{_localstatedir}/named/etc/rndc.conf %{buildroot}%{_sysconfdir}/rndc.conf
ln -s %{_localstatedir}/named/etc/rndc.key %{buildroot}%{_sysconfdir}/rndc.key

echo "; Use \"dig @A.ROOT-SERVERS.NET . ns\" to update this file if it's outdated." >named.cache
cat %{_sourcedir}/named.root >>named.cache
install -m 0644 named.cache %{buildroot}%{_localstatedir}/named/var/named/named.ca

mkdir -p %{buildroot}%{_srvdir}/named/{env,log}
install -m 0740 %{_sourcedir}/named.run %{buildroot}%{_srvdir}/named/run
install -m 0740 %{_sourcedir}/named.finish %{buildroot}%{_srvdir}/named/finish
install -m 0740 %{_sourcedir}/named-log.run %{buildroot}%{_srvdir}/named/log/run
install -m 0640 %{_sourcedir}/OPTIONS.env %{buildroot}%{_srvdir}/named/env/OPTIONS



# the following 3 lines is needed to make it short-circuit compliant.
pushd doc
    rm -rf html
popd

mkdir -p doc/html
cp -f `find . -type f |grep html |sed -e 's#\/%{name}-%{version}##'|grep -v contrib` %{_builddir}/%{name}-%{their_version}/doc/html 

%multiarch_binaries %{buildroot}%{_bindir}/isc-config.sh

%pre
%_pre_useradd named %{_localstatedir}/named /bin/false 80

%post
#if grep -q "_MY_KEY_" %{_localstatedir}/named/etc/rndc.conf %{_localstatedir}/named/etc/rndc.key; then
#    MYKEY="%{_sbindir}/dns-keygen"
#    perl -pi -e "s|_MY_KEY_|$MYKEY|g" %{_localstatedir}/named/etc/rndc.conf %{_localstatedir}/named/etc/rndc.key
#fi

%_post_srv named

if [ -e %{_sysconfdir}/rndc.conf.rpmnew ]; then
    /usr/sbin/new_key.pl
fi


%preun
%_preun_srv named


%postun
%_postun_userdel named


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %attr(0750,root,admin) %{_srvdir}/named
%dir %attr(0750,root,admin) %{_srvdir}/named/env
%dir %attr(0750,root,admin) %{_srvdir}/named/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/named/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/named/finish
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/named/env/OPTIONS
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/named/log/run
%attr(0755,root,root) %{_sbindir}/*
%{_mandir}/man3/lwres*.3*
%{_mandir}/man5/named.conf.5*
%{_mandir}/man5/rndc.conf.5*
%{_mandir}/man8/rndc.8*
%{_mandir}/man8/rndc-confgen.8*
%{_mandir}/man8/named.8*
%{_mandir}/man8/dnssec-*.8*
%{_mandir}/man8/lwresd.8*
%{_mandir}/man8/named-*.8*
# the chroot
%attr(0711,named,named) %dir %{_localstatedir}/named
%attr(0711,named,named) %dir %{_localstatedir}/named/dev
%attr(0711,named,named) %dir %{_localstatedir}/named/etc
%attr(0711,named,named) %dir %{_localstatedir}/named/var
%attr(0711,named,named) %dir %{_localstatedir}/named/var/run
%attr(0711,named,named) %dir %{_localstatedir}/named/var/tmp
%attr(0711,named,named) %dir %{_localstatedir}/named/var/named
%attr(0711,named,named) %dir %{_localstatedir}/named/var/named/master
%attr(0711,named,named) %dir %{_localstatedir}/named/var/named/slaves
%attr(0711,named,named) %dir %{_localstatedir}/named/var/named/reverse
%attr(0711,named,named) %dir /var/run/named
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/etc/named.conf
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/etc/rndc.conf
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/etc/rndc.key
%attr(-,root,named) %{_sysconfdir}/named.conf
%attr(-,root,named) %{_sysconfdir}/rndc.conf
%attr(-,root,named) %{_sysconfdir}/rndc.key
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/etc/bogon_acl.conf
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/etc/logging.conf
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/etc/trusted_networks_acl.conf
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/var/named/master/localdomain.zone
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/var/named/master/localhost.zone
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/var/named/reverse/named.broadcast
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/var/named/reverse/named.ip6.local
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/var/named/reverse/named.local
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/var/named/reverse/named.zero
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/var/named/named.ca
%attr(0640,root,named) %config(noreplace) %{_localstatedir}/named/etc/hosts

%files devel
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/isc-config.sh
%attr(0755,root,root) %{_bindir}/isc-config.sh
%{_includedir}/*
%{_libdir}/*.a

%files utils
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/host.1*
%{_mandir}/man1/dig.1*
%{_mandir}/man1/nslookup.1*
%{_mandir}/man8/nsupdate.8*
%{_mandir}/man5/resolver.5*
%{_mandir}/man5/resolv.5*

%files doc
%defattr(-,root,root)
%doc CHANGES README FAQ COPYRIGHT
%doc doc/draft doc/html doc/rfc doc/misc/
%doc doc/dhcp-dynamic-dns-examples doc/chroot doc/trustix


%changelog
* Sat Dec 08 2007 Vincent Danen <vdanen-at-build.annvix.org> 9.4.2
- 9.4.2
- use %%serverbuild
- updated L.ROOT-SERVERS.NET IP address
- drop P2, P4: obsolete

* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 9.4.1-P1
- fix source urls
- this is actually 9.4.1-P1 which fixes CVE-2007-2925 and CVE-2007-2926

* Tue Sep 04 2007 Ying-Hung Chen <ying-at-yingternet.com> 9.4.1
- 9.4.1
- Updated Patch1, Patch4

* Tue Sep 04 2007 Ying-Hung Chen <ying-at-yingternet.com> 9.3.4
- Update rndc.key, rndc.conf to ensure named is runnable by default
- Fix named.finish script to make sure named will be restart
  correctly after reboot

* Thu Feb 08 2007 Ying-Hung Chen <ying-at-yingternet.com> 9.3.4
- empty /etc/rndc.key file to make named runnable by default

* Fri Feb 02 2007 Vincent Danen <vdanen-at-build.annvix.org> 9.3.4
- 9.3.4; fixes CVE-2007-0493, CVE-2007-0494

* Fri Sep 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 9.3.2-P1
- fix some permissions

* Fri Sep 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 9.3.2-P1
- 9.3.2-P1 (fixes CVE-2006-4095, CVE-2006-4096)
- drop the %%build_daemon macro
- updated P1
- drop P7
- drop S6, S8, S10
- new S6 from Fedora for caching-nameserver
- new S8 to bring back some missing tools
- chroot by default (/var/lib/named)
- this one acts as a caching-only resolver by default; IP addresses that should
  be allowed to use recursive lookups must be defined in
  /var/lib/named/etc/trusted_networks_acl.conf
- explicitly disable threading support
- drop the sysconfig file and use ./env/OPTIONS instead
- since we pass "-g" to named rather than "-f", there are no logs other than svlogd's
  stuff so drop the logrotate file

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 9.3.1
- rebuild against new openssl
- spec cleanups

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 9.3.1
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 9.3.1
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 9.3.1
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.3.1-1avx
- 9.3.1
- use execlineb for run scripts
- move logdir to /var/log/service/sshd
- run scripts are now considered config files and are not replaceable
- P6, P7: from fedora

* Mon Aug 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.3.0-8avx
- fix perms on run scripts
- make the finish script mode 640 so it's not executed; need to evaluate
  whether it's still needed

* Mon Aug 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.3.0-7avx
- disable threads support to enable switching user with -u
  (thanks Ying)
- re-enable linux caps
- build the daemon by default
- by default, log to svlogd rather than syslog (use -g rather than -f
  in the runscript)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.3.0-6avx
- rebuild

* Sat Apr 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.3.0-5avx
- add %%build_daemon macro so we can build bind-{utils,devel} but not
  named itself (since we want things like dig, host, etc.); by default
  we do not build the daemon

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.3.0-4avx
- use logger for logging

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.3.0-3avx
- rebuild against latest openssl

* Tue Dec 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.3.0-2avx
- merge with mdk:
  - fix detection of res_mkquery(), aka file build on e.g. x86_64 (gbeauchesne)
  - touched S7 and added stuff from trustix to it
- disable linux capabilities as bind is currently dying with "capset failed";
  NOTE: this means we can't run bind as an unprivileged user (named) which is not
  good at all, nor can we chroot it -- hopefully someone smarter than I can configure
  out how to fix this

* Fri Sep 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.3.0-1avx
- 9.3.0
- drop P3; fixed upstream
- fix manpage mess (oden)
- don't build queryperf from contribs right not as it's broken

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.2.3-9avx
- update run scripts

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.2.3-8avx
- lots of spec cleanups
- add the bsdcompat patch - bug #8840 (florin)
- add note to S11 (named.ca) (oden)
- use more aclocal and autoconf magic, including P5 (oden)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.2.3-7avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 9.2.3-6sls
- minor spec cleanups
- logrotate uses svc

* Wed Feb 04 2004 Vincent Danen <vdanen@opensls.org> 9.2.3-5sls
- remove %%build_opensls macro
- remove initscript
- supervise scripts
- give named static uid/gid 80
- more cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 9.2.3-4sls
- OpenSLS build
- use %%build_opensls macro to turn off IDN support
- explicitly provide -fstack-protector with %%build_opensls since we don't
  use standard %%{optflags}

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
