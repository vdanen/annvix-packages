%define name	openssh
%define version	3.6.1p2
%define release 12sls

## Do not apply any unauthorized patches to this package!
## - vdanen 05/18/01
##

# Version of ssh-askpass
%define aversion 1.2.4.1
# Version of watchdog patch
%define wversion 3.6p1

# overrides
%global build_skey	 0
%global build_krb5	 0
%global build_scard	 0
%global build_watchdog   0
%global no_x11_askpass	 1
%global no_gnome_askpass 1
%{?_with_skey: %{expand: %%global build_skey 1}}
%{?_with_krb5: %{expand: %%global build_krb5 1}}
%{?_with_watchdog: %{expand: %%global build_watchdog 1}}
%{?_with_smartcard: %{expand: %%global build_scard 1}}
%{?_with_nox11askpass: %{expand: %%global no_x11_askpass 1}}
%{?_with_nognomeaskpass: %{expand: %%global no_gnome_askpass 1}}

Summary:	OpenSSH free Secure Shell (SSH) implementation
Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://www.openssh.com/
Source: 	ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source1:	http://www.ntrnet.net/~jmknoble/software/x11-ssh-askpass/x11-ssh-askpass-%{aversion}.tar.bz2
Source2: 	ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz.sig
# ssh-copy-id taken from debian, with "usage" added
Source3:	ssh-copy-id.bz2 
Source4: 	gnome-ssh-askpass.sh
Source5: 	gnome-ssh-askpass.csh
Source6:	ssh-client.sh
Source8:	sshd.run
Source9:	sshd-log.run
# this is never to be applied by default
Source10:	openssh-%{wversion}-watchdog.patch.tar.bz2
Patch1:		openssh-3.6.1p2-mdkconf.patch.bz2
# authorized by Damien Miller <djm@openbsd.com>
Patch3:		openssh-3.1p1-check-only-ssl-version.patch.bz2
# (flepied) don't use killproc to avoid killing running sessions in some cases
Patch5:		openssh-3.6.1p1-initscript.patch.bz2
Patch6:		openssh-3.6.1p2-bufferfix.patch.bz2
Patch7:		openssh-3.6.1p2-supervise.patch.bz2
License:	BSD
Group:		Networking/Remote access

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	groff-for-man, openssl-devel >= 0.9.7, pam-devel, tcp_wrappers-devel, zlib-devel
BuildRequires:	db1-devel
%if %{build_skey}
BuildRequires:	skey-devel, skey-static-devel
%endif
%if %{build_krb5}
BuildRequires:	krb5-devel
%endif
%if !%{no_x11_askpass}
BuildRequires:  XFree86-devel
%endif
%if !%{no_gnome_askpass}
BuildRequires:	gtk+2-devel
%endif

Obsoletes:	ssh
Provides:	ssh
PreReq:		openssl >= 0.9.7

%package clients
Summary:	OpenSSH Secure Shell protocol clients
Requires:	%{name} = %{version}-%{release}
Group:		Networking/Remote access
Obsoletes:	ssh-clients, sftp
Provides:	ssh-clients, sftp

%package server
Summary:	OpenSSH Secure Shell protocol server (sshd)
PreReq:		%{name} = %{version}-%{release} chkconfig >= 0.9 
PreReq:		pam >= 0.74
PreReq:		rpm-helper
%if %{build_skey}
Requires:	skey
%endif
Group:		System/Servers
Obsoletes:	ssh-server
Provides:	ssh-server

%if !%{no_x11_askpass}
%package askpass
Summary:	OpenSSH X11 passphrase dialog
Group:		Networking/Remote access
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ssh-extras, ssh-askpass
Provides:	%{name}-askpass, ssh-extras, ssh-askpass
PreReq:		/usr/sbin/update-alternatives
%endif

%if !%{no_gnome_askpass}
%package askpass-gnome
Summary:	OpenSSH GNOME passphrase dialog
Group:		Networking/Remote access
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ssh-extras
PreReq:		/usr/sbin/update-alternatives
Provides:	%{name}-askpass, ssh-askpass, ssh-extras
%endif

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

%if !%{no_x11_askpass}
%description askpass
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package contains Jim Knoble's <jmknoble@pobox.com> X11 passphrase 
dialog.
%endif

%if !%{no_gnome_askpass}
%description askpass-gnome
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine.  It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network.  X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing it
up to date in terms of security and features, as well as removing all 
patented algorithms to separate libraries (OpenSSL).

This package contains the GNOME passphrase dialog.
%endif

%prep
%if %{no_x11_askpass}
echo "Building without x11 askpass..."
%endif
%if %{no_gnome_askpass}
echo "Building without GNOME askpass..."
%endif
%if %{build_krb5}
echo "Building with Kerberos5 support..."
%endif
%if %{build_skey}
echo "Building with S/KEY support..."
%endif
%if %{build_scard}
echo "Building with smartcard support..."
%endif
%if %{build_watchdog}
echo "Building with watchdog support..."
%endif

%if %{no_x11_askpass}
%setup -q
%else
%setup -q -a 1
%endif
%if %{build_watchdog}
%setup -q -n %{name}-%{version} -D -T -a10
%endif

%patch1 -p1 -b .mdkconf
%patch3 -p1 -b .ssl_ver
%patch5 -p1 -b .initscript
%patch6 -p0 -b .secfix
%if %{build_watchdog}
patch -p0 -b --suffix .wdog <%{name}-%{wversion}-watchdog.patch
%endif

%build

%serverbuild

CFLAGS="$RPM_OPT_FLAGS" ./configure \
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
%if %{build_krb5}
  --with-kerberos5 \
%endif
%if %{build_skey}
  --with-skey \
%endif
%if %{build_scard}
  --with-smartcard \
%endif
  --with-superuser-path=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
make

%if !%{no_x11_askpass}
pushd x11-ssh-askpass-%{aversion}
CFLAGS="$RPM_OPT_FLAGS" ./configure \
  --prefix=%{_prefix} --libdir=%{_libdir} \
  --mandir=%{_mandir} --libexecdir=%{_libdir}/ssh \
  --with-app-defaults-dir=%{_libdir}/X11/app-defaults
xmkmf -a
make
popd
%endif

%if !%{no_gnome_askpass}
pushd contrib
make gnome-ssh-askpass2
mv gnome-ssh-askpass2 gnome-ssh-askpass
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ssh
install -d $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
install -m644 contrib/redhat/sshd.pam $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/sshd

if [[ -f sshd_config.out ]]; then 
	install -m600 sshd_config.out $RPM_BUILD_ROOT%{_sysconfdir}/ssh/sshd_config
else 
	install -m600 sshd_config $RPM_BUILD_ROOT%{_sysconfdir}/ssh/sshd_config
fi

if [[ -f ssh_config.out ]]; then
    install -m644 ssh_config.out $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ssh_config
else
    install -m644 ssh_config $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ssh_config
fi
echo "    StrictHostKeyChecking no" >> $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ssh_config

mkdir -p $RPM_BUILD_ROOT%{_libdir}/ssh
%if !%{no_x11_askpass}
pushd x11-ssh-askpass-%{aversion}
make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT install.man
popd
# fix x11-ssh-askpass manpage
(cd $RPM_BUILD_ROOT%{_mandir}/man1; mv x11-ssh-askpass.1x x11-ssh-askpass.1)
%endif

(cd $RPM_BUILD_ROOT%{_bindir}; ln -s ../../%{_libdir}/ssh/ssh-askpass)

install -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
%if !%{no_gnome_askpass}
install -m 755 contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libdir}/ssh/gnome-ssh-askpass
install -m 755 %{SOURCE4} %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
%endif

install -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

bzcat %{SOURCE3} > $RPM_BUILD_ROOT/%{_bindir}/ssh-copy-id
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/ssh-copy-id
install -m 644 contrib/ssh-copy-id.1 $RPM_BUILD_ROOT/%{_mandir}/man1/

# create pre-authentication directory
mkdir -p %{buildroot}/var/empty

%if !%{build_scard}
rm -f %{buildroot}%{_datadir}/ssh/Ssh.bin
%endif

mkdir -p %{buildroot}%{_srvdir}/sshd/log
mkdir -p %{buildroot}%{_srvlogdir}/sshd
install -m 0755 %{SOURCE8} %{buildroot}%{_srvdir}/sshd/run
install -m 0755 %{SOURCE9} %{buildroot}%{_srvdir}/sshd/log/run


%clean
rm -rf $RPM_BUILD_ROOT

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

%preun server
%_preun_srv sshd

%postun server
%_postun_userdel sshd

%if !%{no_x11_askpass}
%post askpass
update-alternatives --install %{_libdir}/ssh/ssh-askpass ssh-askpass %{_libdir}/ssh/x11-ssh-askpass 10

%postun askpass
[ $1 = 0 ] || exit 0
update-alternatives --remove ssh-askpass %{_libdir}/ssh/x11-ssh-askpass
%endif

%if !%{no_gnome_askpass}
%post askpass-gnome
update-alternatives --install %{_libdir}/ssh/ssh-askpass ssh-askpass %{_libdir}/ssh/gnome-ssh-askpass 20

%postun askpass-gnome
[ $1 = 0 ] || exit 0
update-alternatives --remove ssh-askpass %{_libdir}/ssh/gnome-ssh-askpass
%endif

%files
%defattr(-,root,root)
%doc ChangeLog OVERVIEW README* INSTALL CREDITS LICENCE TODO
%if %{build_watchdog}
%doc CHANGES-openssh-watchdog openssh-watchdog.html
%endif
%{_bindir}/ssh-keygen
%dir %{_sysconfdir}/ssh
%{_bindir}/ssh-keyscan
%{_mandir}/man1/ssh-keygen.1*
%{_mandir}/man1/ssh-keyscan.1*
%{_mandir}/man8/ssh-keysign.8*
%{_libdir}/ssh/ssh-keysign
%{_bindir}/scp
%{_mandir}/man1/scp.1*

%if %{build_scard}
%dir %{_datadir}/ssh
%{_datadir}/ssh/Ssh.bin
%endif

%files clients
%defattr(-,root,root)
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
%config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/profile.d/ssh-client.sh
%{_bindir}/ssh-askpass

%files server
%defattr(-,root,root)
%{_sbindir}/sshd
%dir %{_libdir}/ssh
%{_libdir}/ssh/sftp-server
%{_mandir}/man5/sshd_config.5*
%{_mandir}/man8/sshd.8*
%{_mandir}/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/pam.d/sshd
%dir %{_srvdir}/sshd
%dir %{_srvdir}/sshd/log
%{_srvdir}/sshd/run
%{_srvdir}/sshd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/sshd


%config(noreplace) %{_sysconfdir}/ssh/moduli
%dir %attr(0755,root,root) /var/empty

%if !%{no_x11_askpass}
%files askpass
%defattr(-,root,root)
%doc x11-ssh-askpass-%{aversion}/README
%doc x11-ssh-askpass-%{aversion}/ChangeLog
%doc x11-ssh-askpass-%{aversion}/SshAskpass*.ad
%{_libdir}/ssh/x11-ssh-askpass
%{_libdir}/X11/app-defaults/SshAskpass
%{_mandir}/man1/x11-ssh-askpass.1*
%endif

%if !%{no_gnome_askpass}
%files askpass-gnome
%defattr(-,root,root)
%{_libdir}/ssh/gnome-ssh-askpass
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%endif

%changelog
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
