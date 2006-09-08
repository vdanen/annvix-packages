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
%define version		9.3.1
%define release		%_revrel

%define their_version	9.3.1
%define build_daemon	1

Summary:	A DNS (Domain Name System) server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Distributable
Group:		System/Servers
URL:		http://www.isc.org/products/BIND/
Source0:	ftp://ftp.isc.org/isc/%{name}9/%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}-manpages.tar.bz2
Source2:	named.init
Source3:	named.logrotate
Source4:	named.sysconfig
Source5:	keygen.c
Source6:	new_key.pl
Source7:	dhcp-dynamic-dns-examples.tar.bz2
Source8:	update_bind.pl
Source9:	ftp://ftp.isc.org/isc/%{name}9/%{version}/%{name}-%{version}.tar.gz.asc
Source10:	bind-chroot.sh
Source11:	ftp://FTP.RS.INTERNIC.NET/domain/named.root
Source12:	named.run
Source13:	named.stop
Source14:	named-log.run
Patch1:		bind-9.3.0rc2-fallback-to-second-server.patch
Patch2:		bind-9.3.0-mdk-libresolv.patch
Patch4:		bind-9.2.3-bsdcompat.patch
Patch5:		bind-9.3.0beta2-libtool.diff
Patch6:		libbind-9.3.1rc1-fix_h_errno.patch
Patch7:		bind-9.3.1-reject_resolv_conf_errors.patch
Patch8:		cert.v9_3_1.diff

BuildRoot:	%{_buildroot}/%{name}-root
BuildRequires:	openssl-devel
BuildRequires:	autoconf, autoconf2.5, automake1.7, multiarch-utils >= 1.0.3

%if %{build_daemon}
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


%prep
%setup -q  -n %{name}-%{version} -a1
%patch1 -p1 -b .fallback-to-second-server
#%patch -p1 -b .overflow
%patch2 -p1 -b .libresolv
%patch4 -p1 -b .bsdcompat
%patch5 -p1 -b .libtool
%patch6 -p1 -b .fix_h_errno
%patch7 -p1 -b .reject_resolv_conf_errors
%patch8 -p0 -b .cve-2006-409_56

#(cd contrib/queryperf && autoconf-2.13)
tar -xjf %{SOURCE7}


%build
# (oe) make queryperf from the contrib before bind, makes it easier
# to determine if it builds or not
#cd contrib/queryperf
#mv README README.queryperf
#sh configure
#make CFLAGS="%{optflags}"
#cd -

%configure \
    --localstatedir=/var \
    --enable-ipv6 \
    --with-openssl=%{_includedir}/openssl

# override CFLAGS for better security.  Ask Jay...
make "CFLAGS=-O2 -Wall -pipe"

gcc %{optflags} -o dns-keygen %{SOURCE5}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
pushd doc
    rm -rf html
popd
%if %{build_daemon}
    mkdir -p %{buildroot}%{_sysconfdir}/{logrotate.d,sysconfig}
    mkdir -p %{buildroot}%{_sbindir}
    mkdir -p %{buildroot}%{_var}/{run/named,named}
    mkdir -p %{buildroot}%{_mandir}/man3
%endif

mkdir -p %{buildroot}{%{_bindir},%{_includedir},%{_libdir}}
mkdir -p %{buildroot}%{_mandir}/{man1,man5,man8}
mkdir -p %{buildroot}%{_docdir}/

%makeinstall_std
#tar -xjf %{SOURCE1} -C %{buildroot}%{_mandir}
# fix man pages
install -m 0644 man5/resolver.5 %{buildroot}%{_mandir}/man5/
ln -s resolver.5.bz2 %{buildroot}%{_mandir}/man5/resolv.5.bz2

%if %{build_daemon}
    install -m0600 bin/rndc/rndc.conf %{buildroot}%{_sysconfdir}
    touch %{buildroot}%{_sysconfdir}/rndc.key
    install -m0755 contrib/named-bootconf/named-bootconf.sh %{buildroot}%{_sbindir}/named-bootconf
    #install -m0755 contrib/queryperf/queryperf %{buildroot}%{_sbindir}/
    install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/named

    install -m0755 dns-keygen -D %{buildroot}%{_sbindir}/dns-keygen
    cp %{SOURCE6} %{buildroot}%{_sbindir}
    cp %{SOURCE8} %{buildroot}%{_sbindir}
    cp %{SOURCE10} %{buildroot}%{_sbindir}

    echo "; Use \"dig @A.ROOT-SERVERS.NET . ns\" to update this file if it's outdated." >named.cache
    cat %{SOURCE11} >>named.cache
    install -m 644 named.cache %{buildroot}%{_var}/named/named.ca
    install -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/named

    mkdir -p %{buildroot}%{_srvdir}/named/log
    install -m 0740 %{SOURCE12} %{buildroot}%{_srvdir}/named/run
    install -m 0640 %{SOURCE13} %{buildroot}%{_srvdir}/named/finish
    install -m 0740 %{SOURCE14} %{buildroot}%{_srvdir}/named/log/run
%else
    rm -rf %{buildroot}%{_sbindir}
    rm -rf %{buildroot}%{_mandir}/man3
    rm -rf %{buildroot}%{_mandir}/man5/{named.conf,rndc.conf}*
    rm -rf %{buildroot}%{_mandir}/man8/{dnssec-keygen,dnssec-signzone,lwresd,named-checkconf,named-checkzone,named.8,rndc-confgen,rndc.8}*
%endif

# the following 3 lines is needed to make it short-circuit compliant.
pushd doc
    rm -rf html
popd

mkdir -p doc/html
cp -f `find . -type f |grep html |sed -e 's#\/%{name}-%{version}##'|grep -v contrib` %{_builddir}/%{name}-%{version}/doc/html 

%multiarch_binaries %{buildroot}%{_bindir}/isc-config.sh

%if %{build_daemon}
%pre
%_pre_useradd named /var/named /bin/false 80

%post
if [ -d /var/log/supervise/named -a ! -d /var/log/service/named ]; then
    mv /var/log/supervise/named /var/log/service/
fi
%_post_srv named

echo "You can use the sample named.conf file from the %{_docdir}/%{name}-%{version} directory"

if [ -e %{_sysconfdir}/rndc.conf.rpmnew ]; then
    /usr/sbin/new_key.pl
fi


%preun
%_preun_srv named

%postun
%_postun_userdel named
%endif


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%if %{build_daemon}
%files
%defattr(-,root,root)
%doc CHANGES README FAQ COPYRIGHT
#%doc contrib/queryperf/README.queryperf
%doc doc/draft doc/html doc/rfc doc/misc/
%doc doc/dhcp-dynamic-dns-examples doc/chroot doc/trustix
%config(noreplace) %{_sysconfdir}/sysconfig/named
%config(noreplace) %{_sysconfdir}/logrotate.d/named
%config(noreplace) %attr(0600,named,named) %{_sysconfdir}/rndc.conf
%config(noreplace) %attr(0600,named,named) %{_sysconfdir}/rndc.key
%dir %attr(0750,root,admin) %{_srvdir}/named
%dir %attr(0750,root,admin) %{_srvdir}/named/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/named/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/named/finish
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
%attr(-,named,named) %dir /var/named
%attr(-,named,named) %config(noreplace) %{_var}/named/named.ca
%attr(-,named,named) %dir /var/run/named
%endif

%files devel
%defattr(-,root,root)
%doc CHANGES README
%multiarch %{multiarch_bindir}/isc-config.sh
%attr(0755,root,root) %{_bindir}/isc-config.sh
%{_includedir}/*
%{_libdir}/*.a

%files utils
%defattr(-,root,root)
%doc README COPYRIGHT
%{_bindir}/*
%{_mandir}/man1/host.1*
%{_mandir}/man1/dig.1*
%{_mandir}/man1/nslookup.1*
%{_mandir}/man8/nsupdate.8*
%{_mandir}/man5/resolver.5*
%{_mandir}/man5/resolv.5*


%changelog
* Fri Sep 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 9.3.1
- P8: security fix for CVE-2006-4095 and CVE-2006-4096

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Sun Nov 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 9.2.3-3mdk
- rebuilt for reupload

* Mon Oct 27 2003 Florin <florin@mandrakesoft.com> 9.2.3-2mdk
- add sleep 2 in the restart function of the initscript

* Fri Oct 24 2003 Florin <florin@mandrakesoft.com> 9.2.3-1mdk
- 9.2.3

* Thu Oct 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 9.2.3-0.rc4.3mdk
- added IDN support (P4, rediffed from the patch for bind-9.2.2)
- buildrequires idnkit-devel

* Wed Sep 24 2003 Florin <florin@mandrakesoft.com> 9.2.3-2mdk
- fix the stop in the initscript

* Mon Sep 22 2003 Florin <florin@mandrakesoft.com> 9.2.3-0.rc4.1mdk
- rc4 (fixes bugs 1511, 1512)

* Sat Sep 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 9.2.3-0.rc3.1mdk
- 9.2.3rc3 (fixes bind bugs 1509, 1508, 1507 and 1506)
- added P3 to make nslookup shut up about possible deprecation, i think
  we will notice this ourselves eventually anyhow...

* Wed Sep 17 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 9.2.3-0.rc2.1mdk
- 9.2.3rc2 (support for "delegation-only" zones)
- updated S7 to reflect the support for "delegation-only" zones

* Tue Aug 26 2003 Florin <florin@mandrakesoft.com> 9.2.3-0.rc1.1mdk
- 9.2.3rc1
- update the callback patch

* Fri Aug  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.2.2-3mdk
- Reenable libresolv patch, it's always nice to see useful patches
  silently removed...

* Mon Jun 02 2003 Florin <florin@mandrakesoft.com> 9.2.2-2mdk
- better help message for the chroot script (thx Charles Davant)

* Wed Mar 05 2003 Florin <florin@mandrakesoft.com> 9.2.2-1mdk
- 9.2.2

* Wed Feb 26 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 9.2.2-0.rc1.4mdk
- Change the default semantic by default it go on the second server
  when get a SERVFAIL, specify +fail to dig or -fail to nslookup or -F
  to host if you really want this option.

* Wed Feb 26 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 9.2.2-0.rc1.3mdk
- Add option -f to host to don't fail when the firstserv and fallback
  on the second server when the first one return SERVFAIL (same for
  nslookup and option -nofail)(and use +nofail with dig) usefull with
  zeroconf dns.

* Mon Feb 10 2003 Florin <florin@mandrakesoft.com> 9.2.2-0.rc1.2mdk
- update the named.root (thx to Ben Reser)

* Wed Oct 16 2002 Florin <florin@mandrakesoft.com> 9.2.2-0.rc1.1mdk
-  9.2.2-0.rc1.1mdk

* Fri Sep 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.2.1-5mdk
- Patch1: Fix lookup of res_mkquery() in libresolv

* Tue Aug 13 2002 Vincent Danen <vdanen@mandrakesoft.com> 9.2.1-4mdk
- fix buffer overflow for dns resolver libs
- put named.ca in bind proper (not in caching-nameserver anymore)

* Fri Jul 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 9.2.1-3mdk
- add named user

* Thu Jul 11 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 9.2.1-2mdk
- Really 9.2.1 (Florin forgot to remove the rc1 tag).
- Don't bzip2, use pristine .tar.gz source, otherwise there is no point in 
  shipping the .asc file.
- Short Circuit Compliant (tm).

* Thu May 02 2002 Florin <florin@mandrakesoft.com> 9.2.1-1mdk
- 9.2.1
- rename the chroot script : bind-chroot.sh is the new name

* Thu Mar 21 2002 Florin <florin@mandrakesoft.com> 9.2.1-0.rc1.1mdk
- 9.2.1rc1
- some minor fixes for chroot_bind.sh

* Mon Mar 11 2002 Florin <florin@mandrakesoft.com> 9.2.0-5mdk
- chroot_bind.sh final fixes (thx to Scott Wunsch ideas)

* Fri Mar 08 2002 Florin <florin@mandrakesoft.com> 9.2.0-4mdk
- new chroot_bind.sh script (supports interactive, undo, status)

* Fri Feb 15 2002 Florin <florin@mandrakesoft.com> 9.2.0-3mdk
- fix the sed line (thx to Bryan Paxton for letting me know)
- add a userfriendly chroot configuration chroot_bind.sh script
- add a sample chroot configuration in %{_docdir}/%{name}-%{version}

* Sun Jan 13 2002 Geoffrey Lee <snailtalk@mandrkaesoft.com> 9.2.0-2mdk
- Don't require bind for the -devel package. The development package only
  contain C header files and static libraries.
  
* Tue Nov 27 2001 Florin <florin@mandrakesoft.com> 9.2.0-1mdk
- 9.2.0 ... at last

* Wed Nov 21 2001 Florin <florin@mandrakesoft.com> 9.2.0-0.rc10.1mdk
- 9.2.0rc10
- add a whole bunch of html files

* Thu Nov 08 2001 Florin <florin@mandrakesoft.com> 9.2.0-0.rc9.1mdk
- 9.2.0rc9

* Thu Oct 25 2001 Florin <florin@mandrakesoft.com> 9.2.0-0.rc8.1mdk
- 9.2.0rc8

* Wed Oct 17 2001 Florin <florin@mandrakesoft.com> 9.2.0-0.rc7.1mdk
- 9.2.0rc7

* Wed Oct 10 2001 Florin <florin@mandrakesoft.com> 9.2.0-0.rc6.2mdk
- remove the named.conf file as it  conflicts with ch-nm-server

* Tue Oct 09 2001 Florin <florin@mandrakesoft.com> 9.2.0-0.rc6.1mdk
- 9.2.0rc6
- add a silly named.conf file

* Wed Oct 03 2001 Florin <florin@mandrakesoft.com>  9.2.0-0.rc5.1mdk
-  9.2.0rc5

* Wed Sep 26 2001 Florin <florin@mandrakesoft.com> 9.2.0-0.rc4.1mdk
- 9.2.0rc4

* Wed Sep 12 2001 Florin <florin@mandrkaesoft.com> 9.2.0-0.rc2.3mdk
- 9.2.0rc3
- remove the rndc-confgen.8 part as it is copied by the Makefile now

* Wed Sep 12 2001 Florin <florin@mandrkaesoft.com> 9.2.0-0.rc2.3mdk
- add the rndc-confgen.8 man page
- update the config in the examples from doc (rndc status, etc, works now)

* Mon Sep 10 2001 Florin <florin@mandrkaesoft.com> 9.2.0-0.rc2.2mdk
- bind-utils doesn't have to require bind (my mistake)
- remove the useless patches

* Fri Sep 07 2001 Florin <florin@mandrkaesoft.com> 9.2.0-0.rc2.1mdk
- 9.2.0rc2
- fix some doc permissions
- remove the requires on libs in the bind-utils package
- bind-utils requires bind >= %{version} now
- add the /et/rndc.key file
- compile with static libs and remove the libs package 
- slightly modify the named.ca file in the docs
- add Epoch 1

* Fri Aug 10 2001 Florin <florin@mandrkaesoft.com> 9.2.0-0.rc1.1mdk
- 9.2.0rc1
- add the kerberos sections in the examples files
- add /bin/sh in requires 

* Tue Jul 31 2001 Florin <florin@mandrkaesoft.com> 9.2.0-0.b2.1mdk
- 9.2.0b2

* Wed Jul 18 2001 Florin <florin@mandrkaesoft.com> 9.2.0-0.b1.1mdk
- 9.2.0b1

* Tue Jul 17 2001 Florin <florin@mandrkaesoft.com> 9.2.0-0.a3.2mdk
- use the new_key.pl silly script only if /etc/rndc.conf.rpmnew exists
- add the named.pid line in /etc/named.conf file, if the later exists
  using the new update_bind.pl silly script

* Mon Jul 16 2001 Florin Grad <florin@mandrkaesoft.com> 9.2.0-0.a3.1mdk
- 9.2.0a3
- add the nanny.pl, rndc-confgen, queryperf scripts
- add the FAQ, COPYRIGHT, README.queryperf text files


* Tue Jun 26 2001 Florin Grad <florin@mandrkaesoft.com> 9.2.0-0.a2.2mdk
- fix a small typo on the silly new_key.pl script
- add really working examples
- add /etc/sysconfig/named file

* Fri Jun 22 2001 Florin Grad <florin@mandrkaesoft.com> 9.2.0-0.a2.1mdk
- correct naming (add the their_version macro). Thx G. Lee

* Thu Jun 21 2001 Florin Grad <florin@mandrkaesoft.com> 9.2.0a2-1mdk
- 9.2.0a2
- extract the bind-utils libraries to a libdns package
- add the keygen.c and the sysconfig file sources
- fix the /etc/rndc.conf permission (thx to Michael Brown)
- add the sample configuration files in relation with the dhcpd server
- add the named.conf, named-* and all the lwres* man pages
- add the %{_sbindir}/new_key.pl script that generates a key and updates the 
  /etc/named.conf and /etc/rndc.conf files

* Sun Jun 10 2001 Stefan van der Eijk <stefan@eijk.nu> 9.1.2-2mdk
- BuildRequires: openssl-devel

* Sat May 05 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 9.1.2-1mdk
- Version 9.1.2.

* Thu Mar 29 2001 Florin Grad <florin@mandrkaesoft.com> 9.1.1-1mdk
- 9.1.1

* Wed Mar 28 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 9.1.1-0.rc7.2mdk
- use post_service and preun_service scripts

* Tue Mar 27 2001 Florin Grad <florin@mandrkaesoft.com> 9.1.1-0.rc7.1mdk
- rc7

* Thu Mar 01 2001 Geoffrey Lee <snailtalk@mandrkaesoft.com> 9.1.1-0.rc3.1mdk
- New and shiny 9.1.1rc3.

* Tue Feb 27 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 9.1.1-0.rc2.2mdk
- Fix build on glibc.
- Explicitly enable IPv6.
- Override CFLAGS with conservative ones for better security.

* Tue Feb 13 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 9.1.1-0.rc2.1mdk
- Put 9.1.1rc2 out for everyone to use.
- Use system openssl libraries.
- Enable threading.
- Use -j, not -I when using the bzip2 filter through tar.

* Mon Jan 22 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 9.1.0-3mdk
- fix the nslookup issue.
- merge in the other redhat patch (.reverse).

* Sun Jan 21 2001 Stefan van der Eijk <s.vandereijk@chello.nl> 9.1.0-2mdk
- fix /var/run issue (thanks redhat)

* Fri Jan 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 9.1.0-1mdk
- really 9.1.0.

* Sat Jan 13 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 9.1.0-0.rc1.1mdk
- make a new and shiny binary from a new and shiny source.

* Tue Jan 09 2001 Geoff <snailtalk@mandrakesoft.com> 9.1.0-0.b3.1mdk
- Change how the release is handled to avoid potential Serial: problem.
  Well, you might still have to use --force now, but better early than
  late.
- new and shiny source.

* Wed Jan 03 2001 Florin Grad <florin@mandrakesoft.com> 9.1.0b2-1mdk
- 9.1.0b2

* Wed Dec 06 2000 Florin Grad <florin@mandrakesoft.com> 9.1.0b1-1mdk
- 9.1.0b1 

* Tue Nov 07 2000 Florin Grad <florin@mandrakesoft.com> 9.0.1rc2-1mdk
- 9.0.1rc2

* Mon Nov 06 2000 Florin Grad <florin@mandrakesoft.com> 9.0.1rc1-1mdk
- 9.0.1rc1 wich contains alot of fixes for 9.0.0
- fix the spec file
- dig manpage is provided now by the bind package (removed from the bind-manpages)

* Thu Nov 02 2000 Florin Grad <florin@mandrakesoft.com> 9.0.0-1mdk
- Mandrake adaptations

* Tue Oct 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add some missing man pages (taken from bind8) (Bug #18794)

* Sun Sep 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 9.0.0 final
