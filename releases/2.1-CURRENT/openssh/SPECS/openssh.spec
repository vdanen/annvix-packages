#
# spec file for package openssh
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		openssh
%define version		4.6p1
%define release 	%_revrel

Summary:	OpenSSH free Secure Shell (SSH) implementation
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Networking/Remote Access
URL:		http://www.openssh.com/
Source0: 	ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source1: 	ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz.asc
Source2:	sshd.pam
# ssh-copy-id taken from debian, with "usage" added
Source3:	ssh-copy-id
Source4:	denyusers.pam
Source5:	04_openssh.afterboot
Source6:	ssh-client.sh
Source8:	sshd.run
Source9:	sshd-log.run
Source10:	convert_known_hosts-4.0.pl
Patch1:		openssh-4.3p1-avx-annvixconf.patch
# authorized by Damien Miller <djm@openbsd.com>
Patch2:		openssh-3.1p1-mdk-check-only-ssl-version.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	groff-for-man
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pam-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	zlib-devel
BuildRequires:	krb5-devel

Obsoletes:	ssh
Provides:	ssh = %{version}
Requires:	filesystem >= 2.1.5

%description
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package includes the core files necessary for both the OpenSSH
client and server.  To make this package useful, you should also
install openssh-clients, openssh-server, or both.


%package clients
Summary:	OpenSSH Secure Shell protocol clients
Requires:	%{name} = %{version}-%{release}
Group:		Networking/Remote Access
Obsoletes:	ssh-clients
Obsoletes:	sftp
Provides:	ssh-clients = %{version}
Provides:	sftp = %{version}

%description clients
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package includes the clients necessary to make encrypted connections
to SSH servers.


%package server
Summary:	OpenSSH Secure Shell protocol server (sshd)
Group:		System/Servers
Obsoletes:	ssh-server
Provides:	ssh-server = %{version}
Requires(pre):	rpm-helper
Requires(pre):	%{name} = %{version}
Requires(pre):	pam >= 0.74
Requires(post):	rpm-helper
Requires(post):	afterboot
Requires(post):	ipsvd
Requires(post):	openssl
Requires(preun): rpm-helper
Requires(postun): rpm-helper
Requires(postun): afterboot

%description server
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package contains the secure shell daemon. The sshd is the server 
part of the secure shell protocol and allows ssh clients to connect to 
your host.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p0 -b .avx
%patch2 -p1 -b .ssl_ver


%build
%serverbuild
CFLAGS="%{optflags}" ./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir}/ssh \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir}/ssh \
    --datadir=%{_datadir}/ssh \
    --with-tcp-wrappers \
    --with-pam \
    --with-default-path=/usr/local/bin:/bin:/usr/bin \
    --with-xauth=/usr/X11R6/bin/xauth \
    --with-privsep-path=/var/empty \
    --with-kerberos5=%{_prefix} \
    --with-superuser-path=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/{ssh,pam.d,profile.d}
mkdir -p %{buildroot}%{_libdir}/ssh

install -m 0644 %{_sourcedir}/sshd.pam %{buildroot}%{_sysconfdir}/pam.d/sshd
install -m 0640 %{_sourcedir}/denyusers.pam %{buildroot}%{_sysconfdir}/ssh/denyusers.pam
install -m 0755 %{_sourcedir}/ssh-client.sh %{buildroot}%{_sysconfdir}/profile.d/

if [[ -f sshd_config.out ]]; then 
    install -m 0600 sshd_config.out %{buildroot}%{_sysconfdir}/ssh/sshd_config
else 
    install -m 0600 sshd_config %{buildroot}%{_sysconfdir}/ssh/sshd_config
fi

if [[ -f ssh_config.out ]]; then
    install -m 0644 ssh_config.out %{buildroot}%{_sysconfdir}/ssh/ssh_config
else
    install -m 0644 ssh_config %{buildroot}%{_sysconfdir}/ssh/ssh_config
fi

cp %{_sourcedir}/ssh-copy-id %{buildroot}%{_bindir}/ssh-copy-id
chmod a+x %{buildroot}%{_bindir}/ssh-copy-id
install -m 0644 contrib/ssh-copy-id.1 %{buildroot}/%{_mandir}/man1/

rm -f %{buildroot}%{_datadir}/ssh/Ssh.bin

mkdir -p %{buildroot}%{_srvdir}/sshd/{log,peers,env}
install -m 0740 %{_sourcedir}/sshd.run %{buildroot}%{_srvdir}/sshd/run
install -m 0740 %{_sourcedir}/sshd-log.run %{buildroot}%{_srvdir}/sshd/log/run
touch %{buildroot}%{_srvdir}/sshd/peers/0
chmod 0640 %{buildroot}%{_srvdir}/sshd/peers/0

echo "22" >%{buildroot}%{_srvdir}/sshd/env/PORT
>%{buildroot}%{_srvdir}/sshd/env/OPTIONS


mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/04_openssh.afterboot %{buildroot}%{_datadir}/afterboot/04_openssh

install -m 0644 %{_sourcedir}/convert_known_hosts-4.0.pl .


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre server
%_pre_useradd sshd /var/empty /bin/true 71

%post server
# do some key management; taken from the initscript

KEYGEN=/usr/bin/ssh-keygen
RSA1_KEY=/etc/ssh/ssh_host_key
RSA_KEY=/etc/ssh/ssh_host_rsa_key
DSA_KEY=/etc/ssh/ssh_host_dsa_key

do_rsa1_keygen() {
	if [ ! -s $RSA1_KEY ]; then
		echo -n "Generating SSH1 RSA host key... "
		if $KEYGEN -q -t rsa1 -f $RSA1_KEY -C '' -N '' >&/dev/null; then
			chmod 600 $RSA1_KEY
			chmod 644 $RSA1_KEY.pub
			echo "done"
			echo
		else
			echo "failed"
			echo
			exit 1
		fi
	fi
}

do_rsa_keygen() {
	if [ ! -s $RSA_KEY ]; then
		echo "Generating SSH2 RSA host key... "
		if $KEYGEN -q -t rsa -f $RSA_KEY -C '' -N '' >&/dev/null; then
			chmod 600 $RSA_KEY
			chmod 644 $RSA_KEY.pub
			echo "done"
			echo
		else
			echo "failed"
			echo
			exit 1
		fi
	fi
}

do_dsa_keygen() {
	if [ ! -s $DSA_KEY ]; then
		echo "Generating SSH2 DSA host key... "
		if $KEYGEN -q -t dsa -f $DSA_KEY -C '' -N '' >&/dev/null; then
			chmod 600 $DSA_KEY
			chmod 644 $DSA_KEY.pub
			echo "done"
			echo
		else
			echo "failed"
			echo
			exit 1
		fi
	fi
}

do_rsa1_keygen
do_rsa_keygen
do_dsa_keygen

%_post_srv sshd
%_mkafterboot
pushd %{_srvdir}/sshd >/dev/null 2>&1
    ipsvd-cdb peers.cdb peers.cdb.tmp peers/
popd >/dev/null 2>&1


%preun server
%_preun_srv sshd

%postun server
%_mkafterboot
%_postun_userdel sshd


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/ssh
%{_bindir}/ssh-keygen
%{_bindir}/ssh-keyscan
%{_bindir}/scp
%{_libdir}/ssh/ssh-keysign
%{_mandir}/man1/ssh-keygen.1*
%{_mandir}/man1/ssh-keyscan.1*
%{_mandir}/man8/ssh-keysign.8*
%{_mandir}/man1/scp.1*

%files clients
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/profile.d/ssh-client.sh
%{_bindir}/ssh
%{_bindir}/ssh-agent
%{_bindir}/ssh-add
%{_bindir}/ssh-copy-id
%{_bindir}/slogin
%{_bindir}/sftp
%{_mandir}/man1/ssh-copy-id.1*
%{_mandir}/man1/slogin.1*
%{_mandir}/man1/ssh.1*
%{_mandir}/man1/ssh-agent.1*
%{_mandir}/man1/ssh-add.1*
%{_mandir}/man1/sftp.1*
%{_mandir}/man5/ssh_config.5*

%files server
%defattr(-,root,root)
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/denyusers.pam
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/pam.d/sshd
%config(noreplace) %{_sysconfdir}/ssh/moduli
%{_sbindir}/sshd
%dir %{_libdir}/ssh
%{_libdir}/ssh/sftp-server
%{_mandir}/man5/sshd_config.5*
%{_mandir}/man8/sshd.8*
%{_mandir}/man8/sftp-server.8*
%dir %attr(0750,root,admin) %{_srvdir}/sshd
%dir %attr(0750,root,admin) %{_srvdir}/sshd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/sshd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/sshd/log/run
%dir %attr(0750,root,admin) %{_srvdir}/sshd/peers
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/sshd/peers/0
%attr(0640,root,admin) %{_srvdir}/sshd/env/PORT
%attr(0640,root,admin) %{_srvdir}/sshd/env/OPTIONS
%{_datadir}/afterboot/04_openssh

%files doc
%defattr(-,root,root)
%doc ChangeLog OVERVIEW README* INSTALL CREDITS LICENCE TODO
%doc convert_known_hosts-4.0.pl


%changelog
* Tue May 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.6p1
- 4.6p1
- versioned provides
- don't need /usr/X11R6/bin in the path
- drop the buildreq on db1-devel

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.5p1
- rebuild against new pam
- fix build with kerberos

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.5p1
- rebuild against new krb5

* Wed Nov 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.5p1
- 4.5p1 (privsep vuln fixed)

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.3p2
- rebuild against new openssl
- remove skey conditional build options
- spec cleanups

* Fri Jun 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.3p2
- add -doc subpackage
- rebuild againt new pam
- S2: use our own pam config
- remove hashed format note from %%post in -client package
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.3p2
- 4.3p2 (minor portability fixes)

* Wed Feb 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.3p1
- 4.3p1
- rediff P1

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2p1
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2p1
- Clean rebuild

* Sun Jan 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2p1
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Sep 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2p1-7avx
- revert the quotes change in the runscript as it then runs sshd without
  any args (bad)

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2p1-6avx
- quotes and braces in runscript

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2p1-5avx
- only include PORT and OPTIONS env files; defaults will come from
  the tcpsvd env dir (update run script too)

* Sun Sep 25 2005 Sean P. Thomas <spt-at-build.annvix.org> 4.2p1-4avx
- Converted run script to execlineb.
- fix requires (vdanen)
- add default env file (vdanen)
- precompile peers.cdb in %%post (vdanen)
- change sshd_config/ssh_config to not permit X11 fwding by default (vdanen)

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2p1-3avx
- s/supervise/service/ in log/run

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2p1-2avx
- really update the log/run script
- run sshd from ipsvd so we can use it's ACLs and peers support
- update the afterboot manpage to reflect this change

* Fri Sep 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2p1-1avx
- 4.2p1
- use execlineb for run scripts
- move logdir to /var/log/service/sshd
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1p1-5avx
- fix perms on run scripts

* Tue Aug 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1p1-4avx
- enable HashKnownHosts by default [ssh_config]
- include convert_known_hosts-4.0pl script from nms.lcs.mit.edu
  to convert existing known_hosts files to the hashed format
- update afterboot snippet to note the HashKnownHosts change

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1p1-3avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1p1-2avx
- rebuild for new gcc and openssl

* Thu Jul 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1p1-1avx
- 4.1p1
- fix ssh-client.sh so it doesn't assume that all non-zsh or ksh
  shells are bourne shells (re: Claudio)
- always build with kerberos support

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0p1-2avx
- rebuild

* Wed Mar 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0p1-1avx
- 4.0p1
- rediff P1

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1-7avx
- use logger for logging
- spec cleanups

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1-6avx
- rebuild against new openssl

* Tue Sep 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1-5avx
- don't own /var/empty; filesystem does (thus filesystem Requires)

* Sat Sep 11 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1-4avx
- fix bad paths in sshd/log/run

* Sat Sep 11 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1-3avx
- update run scripts

* Thu Sep  2 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1-2avx
- turn AllowTcpForwarding off by default

* Thu Aug 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.9p1-1avx
- 3.9p1
- rediff P1
- set MaxAuthTries to 4 by default, rather than 6
- set Protocol to "2" rather than "2,1" by default (it's time people
  stop using RSA1 or even allowing a fallback)

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.8.1p1-1avx
- 3.8.1p1
- patch policy

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.8p1-3avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 3.8p1-2sls
- modify /etc/pam.d/sshd to use pam_listfile.so first on the auth stack so
  even if UsePAM is enabled, we can still securely use PermitRootLogin
  without-password without having to worry about it dropping down to a
  password auth
- new config file: /etc/ssh/denyusers.pam which contains root by default (S4)
- include afterboot man-snippet

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 3.8p1-1sls
- 3.8p1
- rediff P1
- drop P5 (no initscripts)
- drop P6 (merged upstream)
- rename P3 to P2
- remove smartcard and watchdog build options
- NOTE: Use the UsePAM option with caution!

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.6.1p2-13sls
- minor spec cleanups
- remove all gui stuff completely
- remove P7; we don't need to patch the initscript anymore
- StricHostKeyChecking is ask by default
- build kerberos support by default
- remove ssh-askpass symlink

* Tue Jan 27 2004 Vincent Danen <vdanen@opensls.org> 3.6.1p2-12sls
- srv macros
- sshd has static uid/gid 71

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 3.6.1p2-11sls
- remove S7
- no conditional %%build_opensls anymore
- service macros
- remove the initscript

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 3.6.1p2-10sls
- include supervise files, remove xinetd files

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 3.6.1p2-9sls
- OpenSLS build
- tidy spec
- use %%build_opensls macros to prevent x11-ish stuff from being built
- patch initscript to work with supervise

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
