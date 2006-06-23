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
%define version		4.3p2
%define release 	%_revrel

# overrides
%global build_skey	0
%{?_with_skey: %{expand: %%global build_skey 1}}

Summary:	OpenSSH free Secure Shell (SSH) implementation
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Networking/Remote access
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
BuildRequires:	groff-for-man, openssl-devel >= 0.9.7, pam-devel, tcp_wrappers-devel, zlib-devel
BuildRequires:	db1-devel
BuildRequires:	krb5-devel
%if %{build_skey}
BuildRequires:	skey-devel, skey-static-devel
%endif

Obsoletes:	ssh
Provides:	ssh
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
Group:		Networking/Remote access
Obsoletes:	ssh-clients, sftp
Provides:	ssh-clients, sftp

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
%if %{build_skey}
Requires:	skey
%endif
Group:		System/Servers
Obsoletes:	ssh-server
Provides:	ssh-server
Requires(pre):	rpm-helper, %{name} = %{version}, pam >= 0.74
Requires(post):	rpm-helper, afterboot, ipsvd, openssl
Requires(preun): rpm-helper
Requires(postun): rpm-helper, afterboot

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
%if %{build_skey}
echo "Building with S/KEY support..."
%endif

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
    --with-default-path=/usr/local/bin:/bin:/usr/bin:/usr/X11R6/bin \
    --with-xauth=/usr/X11R6/bin/xauth \
    --with-privsep-path=/var/empty \
    --with-kerberos5 \
%if %{build_skey}
    --with-skey \
%endif
    --with-superuser-path=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot}/

mkdir -p %{buildroot}%{_sysconfdir}/{ssh,pam.d,profile.d}
mkdir -p %{buildroot}%{_libdir}/ssh

install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/sshd
install -m 0640 %{SOURCE4} %{buildroot}%{_sysconfdir}/ssh/denyusers.pam
install -m 0755 %{SOURCE6} %{buildroot}%{_sysconfdir}/profile.d/

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

cat %{SOURCE3} > %{buildroot}%{_bindir}/ssh-copy-id
chmod a+x %{buildroot}%{_bindir}/ssh-copy-id
install -m 0644 contrib/ssh-copy-id.1 %{buildroot}/%{_mandir}/man1/

rm -f %{buildroot}%{_datadir}/ssh/Ssh.bin

mkdir -p %{buildroot}%{_srvdir}/sshd/{log,peers,env}
install -m 0740 %{SOURCE8} %{buildroot}%{_srvdir}/sshd/run
install -m 0740 %{SOURCE9} %{buildroot}%{_srvdir}/sshd/log/run
touch %{buildroot}%{_srvdir}/sshd/peers/0
chmod 0640 %{buildroot}%{_srvdir}/sshd/peers/0

echo "22" >%{buildroot}%{_srvdir}/sshd/env/PORT
>%{buildroot}%{_srvdir}/sshd/env/OPTIONS


mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE5} %{buildroot}%{_datadir}/afterboot/04_openssh

install -m 0644 %{SOURCE10} .


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

* Tue Sep 16 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.6.1p2-8mdk
- revised patch for security fix

* Tue Sep 16 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.6.1p2-7mdk
- security fix 

* Mon Aug 25 2003 Frederic Lepied <flepied@mandrakesoft.com> 3.6.1p2-6mdk
- don't put pam_console and pam_limits in pam config file

* Sat Aug 23 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.6.1p2-5mdk
- make openssh-server own /usr/lib/ssh (re: distlint)
- spec cleanups (no more 7.2 support)

* Wed May 14 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.6.1p2-4mdk
- use %%global, not %%define and all the --with stuff works (thanks Buchan)

* Tue May 13 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.6.1p2-3mdk
- only build for 8.2 or 7.2 (no 8.1/8.0 checking); keep 7.2 because we still
  support SNF (you can still build for 8.[01] but have to edit the spec
  manually)
- remove P2; it's sorely out of date and not used
- remove P4; we don't need it anymore
- new macros:
  --with nox11askpass - doesn't build openssh-askpass
  --with nognomeaskpass - doesn't build openssh-askpass-gnome
  --with smartcard - builds with smartcard support
  --with watchdog - apply the watchdog/heartbeat patch
- set %%{_datadir} so Ssh.bin doesn't install in /usr/share
- NOTE: for some reason, the --with stuff doesn't seem to be working
  properly for stuff that modifies in places other than build or install
  (ie. files, post, etc.) and I'm not sure why, so to rebuild this properly
  with those options, you need to manually modify the spec (ie. for
  watchdog, smartcard, etc.)


* Wed May  7 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.6.1p2-2mdk
- --rebuild --with skey will now build with skey support
- --rebuild --with krb5 will now build with krb5 support (unsure as to
  whether we should do this by default as we would then require krb5-libs)

* Thu May  1 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.6.1p2-1mdk
- 3.6.1p2

* Fri Apr  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 3.6.1p1-2mdk
- don't use killproc in the stop target of the initscript to avoid
killing running sessions (patch5).

* Tue Apr 1 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.6.1p1-1mdk
- 3.6.1p1
- create keys in %%post instead of relying on the initscript (which is never
  called if someone uses xinetd)
- auto-detection for old hosts (build macros)
- rediff P1
- PermitRootLogin disabled by default

* Mon Feb 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.5p1-7mdk
- disable xinetd server by default

* Mon Feb 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.5p1-6mdk
- source 7 : add xinetd support

* Tue Jan 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 3.5p1-5mdk
- move scp to the openssh package as it's needed by the server and the clients

* Tue Jan 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 3.5p1-4mdk
- rebuilt for new openssl

* Tue Dec 31 2002 Stefan van der Eijk <stefan@eijk.nu> 3.5p1-3mdk
- BuildRequires

* Mon Dec 30 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.5p1-2mdk
- rebuild for glibc, etc.

* Mon Oct 15 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.5p1-1mdk
- 3.5p1
- rediff P1

* Wed Sep 11 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.4p1-4mdk
- openssh-server: PreReq: rpm-helper
- fix builds for old distribs (remove support for 7.1)

* Wed Jul 17 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.4p1-3mdk
- make privsep home /var/empty, not /var/empty/sshd
- use %%_pre_useradd and %%_postun_userdel if building for cooker or higher
- add %%build_8x to support 8.x distros
- put scp into clients package

* Wed Jul 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.4p1-2mdk
- rpmlint fixes: strange-permission, configure-without-libdir-spec

* Wed Jun 26 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.4p1-1mdk
- 3.4p1
- regenerate mdkconf patch to include our defaults in /etc/ssh_config again
  (X forwarding = yes)
- From Oden Erikkson <oden.eriksson@kvikkjokk.net>:
  - misc spec fixes
  - include missing ssh-keysign file

* Mon Jun 24 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.3p1-3mdk
- missing manpages

* Mon Jun 24 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.3p1-2mdk
- more build macros for 7.x
- create user sshd, group sshd (uid/gid 94)
- create pre-auth directory: /var/empty/sshd

* Mon Jun 24 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.3p1-1mdk
- 3.3p1
- build macro for 7.x systems so we can use the same spec

* Mon Jun 17 2002 Florin <florin@mandrakesoft.com> 3.2.3p1-1mdk
- 3.2.3p1

* Fri May 17 2002 Florin <florin@mandrakesoft.com> 3.2.2p1-1mdk
- 3.2.2p1
- update the mdk patch

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1p1-2mdk
- Automated rebuild in gcc3.1 environment

* Thu Mar 07 2002 Florin <florin@mandrakesoft.com> 3.1p1-1mdk
- 3.1p1
- update the mdkconf (1) and check (3) patches

* Mon Feb 25 2002 Frederic Lepied <flepied@mandrakesoft.com> 3.0.2p1-7mdk
- mention reload on argument error in initscript

* Mon Feb 25 2002 Frederic Lepied <flepied@mandrakesoft.com> 3.0.2p1-6mdk
- corrected init script to avoid a deadlock if the server dies (gc)
- added reload option to the init script

* Wed Feb 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 3.0.2p1-5mdk
- put scp on openssh package because it's needed for both the client and
server sides.

* Thu Feb  7 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.0.2p1-3mdk
- disable agent forwarding by default

* Wed Jan  2 2002 Frederic Lepied <flepied@mandrakesoft.com> 3.0.2p1-2mdk
- put back the init script patch to prevent killproc from killing all
the sshd instances.

* Tue Dec  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.0.2p1-1mdk
- 3.0.2p1
- remove init patch; the redhat initscript is identical to ours now     

* Thu Nov  8 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.0p1-1mdk
- 3.0p1
- x11-ssh-askpass 1.2.4.1
- fix rpmlint errors; we provide everything we obsolete

* Thu Oct  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.9.9p2-4mdk
- Fix ssh-client.sh with zsh (Andrej).

* Thu Oct  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.9.9p2-3mdk
- include fix from openssh.com for hung ssh clients on exit (thanks to Oden
  Eriksson <oden.eriksson@kvikkjokk.net> for pointing it out)

* Tue Oct  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.9.9p2-2mdk
- Fix xauth path for X11 forwarding.

* Mon Oct  1 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.9.9p2-1mdk
- 2.9.9p2 (security fix)
- regenerate patch 0 (initscript)
- regenerate patch 1 (configs)
- default to using Protocol 2,1 not Protocol 1,2
- /etc/ssh/primes is now called /etc/ssh/moduli

* Sat Sep 01 2001 Florin <florin@mandrakesoft.com> 2.9p2-4mdk
- fix the path in the profile.d files

* Fri Aug 31 2001 Florin <florin@mandrakesoft.com> 2.9p2-3mdk
- fix the reload in the initscript
- add the /etc/profile.d/gnome-ssh-askpass.* files

* Thu Jun 21 2001 Florin <florin@mandrakesoft.com> 2.9p2-2mdk
- move the sources back to the original gz state

* Wed Jun 20 2001 Florin <florin@mandrakesoft.com> 2.9p2-1mdk
- 2.9p2
- bzip2 the sources and the .sig file
- use %{version} for the patches names
- update the patches

* Mon May 21 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.9p1-4mdk
- enable patch 3
- added zlib-devel to BuildRequires (Stephane Lentz).

* Fri May 18 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.9p1-3mdk
- remove transmit_interlude patch, ssl_version patch
- update x11-ssh-askpass to 1.2.2

* Mon May  7 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.9p1-2mdk
- only check version of openssl lib at runtime (and not patchlevel).

* Wed May  2 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.9p1-1mdk
- 2.9p1

* Fri Apr 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.2p2-3mdk
- put ssh-keyscan in main package
- put scp in client package

* Wed Mar 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.2p2-2mdk
- use new macros for %%preun et %%post of openssh-server

* Wed Mar 21 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.5.2p2-1mdk
- 2.5.2p2
- more macros
- removed -fomit-frame-pointer from compile flags

* Fri Mar 16 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.1p2-7mdk
- removed dependency on openssh-askpass to be able to install without X.

* Fri Mar 16 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.1p2-6mdk
- added missing /etc/ssh/primes

* Fri Mar 16 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.1p2-5mdk
- corrected trans_inter patch to avoid zero length malloc.

* Tue Mar  6 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.1p2-4mdk
- X11 forwarding by default.
- TransmitInterlude patch is back.

* Mon Mar  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.1p2-3mdk
- remove --with-ipv4-default from configure flag to work fine with ipv6.

* Mon Mar  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.1p2-2mdk
- pam is back.

* Sat Mar  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.1p2-1mdk
- Obsoletes/Provides sftp
- 2.5.1p2

* Tue Feb 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.1p1-1mdk
- correct init.d script to stop only the listening daemon.
- 2.5.1p1: added sftp client and ssh-keyscan.

* Tue Jan 16 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.3.0p1-8mdk
- applied patch for TransmitInterlude adapted by Troels Walsted Hansen.

* Fri Nov 10 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.3.0p1-7mdk
- 2.3.0p1

* Tue Oct 17 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0p1-7mdk
- ssh suid.

* Thu Oct  5 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0p1-6mdk
- don't try Protocol 2 first (chmou sucks).
- ssh not suid.

* Tue Sep 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.0p1-5mdk
- Pamstackizification.
- X11Forwarding = yes by defaut.

* Fri Sep 15 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0p1-4mdk
- fixed the init script to restart even if forked daemon are still present.

* Tue Sep 12 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0p1-3mdk
- put priority to 20 for gnome alternative of ssh-askpass.

* Mon Sep 11 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0p1-2mdk
- x11-ssh-askpass version 1.0.1
- new package askpass-gnome (use update-alternatives).

* Thu Sep  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.2.0p1-1mdk
- 2.2.0p1
- added copy-id man page
- make a symlink in libdir to ssh-askpass to allow ssh-add to find it.
- added reload and condrestart to init script.

* Tue Aug  8 2000 Pixel <pixel@mandrakesoft.com> 2.1.1p3-3mdk
- remove the BuildRequires gnome-libs-devel

* Thu Aug  3 2000 Pixel <pixel@mandrakesoft.com> 2.1.1p3-2mdk
- cleanup, macrozaition
- add script ssh-copy-id from debian's ssh (i just added a usage)
- StrictHostKeyChecking set to "no" in /etc/ssh/ssh_config (it was "ask"),
  so you won't get the following unless the identification changed
  "The authenticity of host 'linux-mandrake.com' can't be established.
   RSA key fingerprint is 9b:f4:10:21:d6:ff:b2:46:d6:86:b1:42:70:4e:5d:e3.
   Are you sure you want to continue connecting (yes/no)? "

* Thu Jul 13 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.1p3-1mdk
- 2.1.1p3

* Mon Jul  3 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.1p2-1mdk
- 2.1.1p2

* Wed Jun 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.1p1-2mdk
- Move all /usr/lib/ files to /usr/bin/.

* Tue Jun 13 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.1p1-1mdk
- move /usr/libexec => /usr/lib
- 2.1.1p1

* Thu Jun  8 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.0p3-2mdk
- removed unneeded BuildPreReq on gnome-libs-devel.

* Thu Jun  8 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.0p3-1mdk
- 2.1.0p3

* Fri May 26 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.0p2-1mdk
- 2.1.0p2

* Mon May 08 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.2.2-3mdk
- add Prereq openssl so the post script works.

* Tue Apr 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.2-2mdk
- Upgrade groups.
- Clean-up specs.

* Fri Feb  4 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com>
- openssh 1.2.2 release
- if it exist, install the .out version of ssh[d]_config.

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- final cleanup for Mandrake 7

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to 1.2.1pre24
- linked with openssl instead of ssleay

* Mon Jan  3 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com>
- Fix a problem with sshd not using the good path.
- Enable tcp wrapper support.

* Mon Dec 13 1999 Yoann Vandoorselaere <yoann@mandrakesoft.com>
- openssh-1.2pre17 released.

* Thu Dec  2 1999 Yoann Vandoorselaere <yoann@mandrakesoft.com>

- First Mandrake release.
