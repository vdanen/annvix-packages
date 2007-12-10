#
# spec file for package courier-imap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		courier-imap
%define version		4.2.1
%define release		%_revrel

Summary:	Courier-IMAP is an IMAP server that uses Maildirs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.courier-mta.org
Source0:	http://prdownloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2
Source1:	courier-imapd.run
Source2:	courier-imapd-log.run
Source3:	courier-imapds.run
Source4:	courier-imapds-log.run
Source5:	courier-pop3d.run
Source6:	courier-pop3d-log.run
Source7:	courier-pop3ds.run
Source8:	courier-pop3ds-log.run
Source9:	09_courier-imap.afterboot
Source10:	courier.pam
Source11:	MAX_MEM.env
Source12:	MAX_CONN.env
Source13:	MAX_PER_HOST.env
Source14:	IP.env
Patch0: 	courier-imap-4.1.1-pam_service_name.diff
Patch1:		courier-imap-4.2.1-avx-cert_location.patch
Patch2:		courier-imap-4.1.1-avx-tcpsvd_configs.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel
BuildRequires:	gdbm-devel
BuildRequires:	courier-authlib-devel
BuildRequires:	courier-authdaemon

Requires:	ipsvd
Requires:	courier-base = %{version}
Requires:	courier-authdaemon
Requires(post):	afterboot
Requires(post):	rpm-helper >= 0.20
Requires(postun): afterboot
Requires(preun): rpm-helper >= 0.20
Conflicts:	uw-imap
Conflicts:	bincimap
Provides:	imap = %{version}
Provides:	imap-server = %{version}

%description
Courier-IMAP is an IMAP server for Maildir mailboxes.  This package contains
the standalone version of the IMAP server that's included in the Courier
mail server package.  This package is a standalone version for use with
other mail servers.


%package -n courier-base
Summary:	Contains base files for POP and IMAP servers
Group:		System/Servers
Provides:	maildirmake++ = %{version}
Obsoletes:	maildirmake++

%description -n courier-base
This package contains the base files for POP and IMAP servers.


%package -n courier-pop
Summary:	Courier-IMAP POP servers
Group:		System/Servers
Requires:	courier-base = %{version}
Requires:	courier-authdaemon
Requires:	ipsvd
Requires(post):	rpm-helper >= 0.20
Requires(preun): rpm-helper >= 0.20
Provides:	pop = %{version}
Provides:	pop-server = %{version}
Provides:	%{name}-pop = %{version}
Conflicts:	uw-imap-pop
Obsoletes:	%{name}-pop

%description -n courier-pop
This package contains the POP servers of the Courier-IMAP
server suite.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .avx
%patch2 -p1 -b .tcpsvd

# fix docs
cp imap/README imap/README.imap
cp rfc822/ChangeLog rfc822/ChangeLog.rfc822
cp unicode/README unicode/README.unicode
chmod 0644 maildir/README.sharedfolders.html imap/README.html


%build
%configure2_5x \
    --enable-unicode \
    --libexec=%{_libdir}/%{name} \
    --datadir=%{_datadir}/%{name} \
    --sysconfdir=%{_sysconfdir}/courier

%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/pam.d

%makeinstall_std

# remove unwanted files
rm -f %{buildroot}%{_libdir}/%{name}/*.rc
rm -rf %{buildroot}%{_sysconfdir}/profile.d

# Fix configurations
perl -p -i -e 's|^IMAPDSTART=.*|IMAPDSTART=YES|' %{buildroot}%{_sysconfdir}/courier/imapd.dist
perl -p -i -e 's|^IMAPDSSLSTART=.*|IMAPDSSLSTART=YES|' %{buildroot}%{_sysconfdir}/courier/imapd-ssl.dist
perl -p -i -e 's|^POP3DSTART=.*|POP3DSTART=YES|' %{buildroot}%{_sysconfdir}/courier/pop3d.dist
perl -p -i -e 's|^POP3DSSLSTART=.*|POP3DSSLSTART=YES|' %{buildroot}%{_sysconfdir}/courier/pop3d-ssl.dist
for file in %{buildroot}%{_sysconfdir}/courier/*.dist; do
    mv $file  %{buildroot}%{_sysconfdir}/courier/`basename $file .dist`
done
chmod 0644 %{buildroot}%{_sysconfdir}/courier/imapd*
chmod 0644 %{buildroot}%{_sysconfdir}/courier/pop3d*

mkdir -p %{buildroot}%{_sysconfdir}/skel
pushd %{buildroot}%{_sysconfdir}/skel
    %{buildroot}%{_bindir}/maildirmake Maildir
popd

mkdir -p %{buildroot}%{_srvdir}/{courier-imapd,courier-imapds,courier-pop3d,courier-pop3ds}/{env,log}
mkdir -p %{buildroot}%{_srvdir}/{courier-imapd,courier-imapds,courier-pop3d,courier-pop3ds}/peers
install -m 0740 %{_sourcedir}/courier-imapd.run %{buildroot}%{_srvdir}/courier-imapd/run
install -m 0740 %{_sourcedir}/courier-imapd-log.run %{buildroot}%{_srvdir}/courier-imapd/log/run
install -m 0740 %{_sourcedir}/courier-imapds.run %{buildroot}%{_srvdir}/courier-imapds/run
install -m 0740 %{_sourcedir}/courier-imapds-log.run %{buildroot}%{_srvdir}/courier-imapds/log/run
install -m 0740 %{_sourcedir}/courier-pop3d.run %{buildroot}%{_srvdir}/courier-pop3d/run
install -m 0740 %{_sourcedir}/courier-pop3d-log.run %{buildroot}%{_srvdir}/courier-pop3d/log/run
install -m 0740 %{_sourcedir}/courier-pop3ds.run %{buildroot}%{_srvdir}/courier-pop3ds/run
install -m 0740 %{_sourcedir}/courier-pop3ds-log.run %{buildroot}%{_srvdir}/courier-pop3ds/log/run

for service in courier-imapd courier-imapds courier-pop3d courier-pop3ds; do
    install -m 0640 %{_sourcedir}/MAX_MEM.env %{buildroot}%{_srvdir}/${service}/env/MAX_MEM
    install -m 0640 %{_sourcedir}/MAX_CONN.env %{buildroot}%{_srvdir}/${service}/env/MAX_CONN
    install -m 0640 %{_sourcedir}/MAX_PER_HOST.env %{buildroot}%{_srvdir}/${service}/env/MAX_PER_HOST
    install -m 0640 %{_sourcedir}/IP.env %{buildroot}%{_srvdir}/${service}/env/IP
done
echo "143" >%{buildroot}%{_srvdir}/courier-imapd/env/PORT
echo "993" >%{buildroot}%{_srvdir}/courier-imapds/env/PORT
echo "110" >%{buildroot}%{_srvdir}/courier-pop3d/env/PORT
echo "995" >%{buildroot}%{_srvdir}/courier-pop3ds/env/PORT

touch %{buildroot}%{_srvdir}/{courier-imapd,courier-imapds,courier-pop3d,courier-pop3ds}/peers/0
chmod 0640  %{buildroot}%{_srvdir}/{courier-imapd,courier-imapds,courier-pop3d,courier-pop3ds}/peers/0

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/09_courier-imap.afterboot %{buildroot}%{_datadir}/afterboot/09_courier-imap

# fix location of authlib stuff on x86_64
%ifarch x86_64 amd64
find %{buildroot}%{_srvdir} -name run -exec perl -pi -e 's|/usr/lib/courier|/usr/lib64/courier|g' {} \;
%endif

# fix pam
rm -f %{buildroot}%{_sysconfdir}/pam.d/*
cp -f %{_sourcedir}/courier.pam %{buildroot}%{_sysconfdir}/pam.d/courier-imap
cp -f %{_sourcedir}/courier.pam %{buildroot}%{_sysconfdir}/pam.d/courier-pop3
chmod 0644 %{buildroot}%{_sysconfdir}/pam.d/*

rm -f %{buildroot}%{_sysconfdir}/courier/*.cnf

perl -pi -e 's|TLS_CERTFILE=.*|TLS_CERTFILE=%{_sysconfdir}/pki/tls/private/courier-imap.pem|'\
    %{buildroot}%{_sysconfdir}/courier/imapd-ssl
perl -pi -e 's|TLS_CERTFILE=.*|TLS_CERTFILE=%{_sysconfdir}/pki/tls/private/courier-pop.pem|'\
    %{buildroot}%{_sysconfdir}/courier/pop3d-ssl


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
for cert in %{_datadir}/courier/imapd.pem %{_sysconfdir}/ssl/courier/courier-imapd.pem
do
    if [ -f $cert ]; then
        mv $cert %{_sysconfdir}/pki/tls/private/courier-imap.pem
        echo "Found and relocated imapd SSL cert to %{_sysconfdir}/pki/tls/private/"
    fi
done
test -f %{_sysconfdir}/courier/imapd.rpmnew && %{_libdir}/courier-authlib/sysconftool %{_sysconfdir}/courier/imapd.rpmnew >/dev/null
test -f %{_sysconfdir}/courier/imapd-ssl.rpmnew && %{_libdir}/courier-authlib/sysconftool %{_sysconfdir}/courier/imapd-ssl.rpmnew >/dev/null

%_post_srv courier-imapd
%_post_srv courier-imapds
%create_ssl_certificate courier-imap true
%_mkafterboot

for i in courier-imapd courier-imapds
do
    pushd %{_srvdir}/$i >/dev/null 2>&1
        ipsvd-cdb peers.cdb peers.cdb.tmp peers/
    popd >/dev/null 2>&1
done


%preun 
%_preun_srv courier-imapd
%_preun_srv courier-imapds
%_preun_srv authdaemond


%postun
%_mkafterboot



%post -n courier-pop
for cert in %{_datadir}/courier/pop3d.pem %{_sysconfdir}/ssl/courier/pop3d.pem
do
    if [ -f $cert ]; then
        mv $cert %{_sysconfdir}/pki/tls/private/courier-pop.pem
        echo "Found and relocated pop3d SSL cert to %{_sysconfdir}/pki/tls/private/"
    fi
done
test -f %{_sysconfdir}/courier/pop3d.rpmnew && %{_libdir}/courier-authlib/sysconftool %{_sysconfdir}/courier/pop3d.rpmnew >/dev/null
test -f %{_sysconfdir}/courier/pop3d-ssl.rpmnew && %{_libdir}/courier-authlib/sysconftool %{_sysconfdir}/courier/pop3d-ssl.rpmnew >/dev/null

%_post_srv courier-pop3d
%_post_srv courier-pop3ds
%create_ssl_certificate courier-pop true

for i in courier-pop3d courier-pop3ds
do
    pushd %{_srvdir}/$i >/dev/null 2>&1
        ipsvd-cdb peers.cdb peers.cdb.tmp peers/
    popd >/dev/null 2>&1
done


%preun -n courier-pop
%_preun_srv courier-pop3d
%_preun_srv courier-pop3ds


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/courier-imap
%config(noreplace) %{_sysconfdir}/courier/imapd
%config(noreplace) %{_sysconfdir}/courier/imapd-ssl
%{_bindir}/imapd
%{_sbindir}/imaplogin
%{_sbindir}/mkimapdcert
%{_mandir}/man8/imapd.8*
%{_mandir}/man8/mkimapdcert.8*
%{_datadir}/%{name}/mkimapdcert
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapd
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapd/log
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapd/peers
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-imapd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-imapd/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapd/peers/0
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapd/env/MAX_CONN
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapd/env/MAX_MEM
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapd/env/MAX_PER_HOST
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapd/env/IP
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapd/env/PORT
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapds
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapds/log
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapds/peers
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-imapds/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-imapds/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapds/peers/0
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapds/env/MAX_CONN
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapds/env/MAX_MEM
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapds/env/MAX_PER_HOST
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapds/env/IP
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapds/env/PORT
%{_datadir}/afterboot/09_courier-imap

%files -n courier-pop
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/courier-pop3
%config(noreplace) %{_sysconfdir}/courier/pop3d
%config(noreplace) %{_sysconfdir}/courier/pop3d-ssl
%{_bindir}/pop3d
%{_sbindir}/pop3login
%{_sbindir}/mkpop3dcert
%{_mandir}/man8/mkpop3dcert.8*
%{_datadir}/%{name}/mkpop3dcert
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3d
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3d/log
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3d/peers
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-pop3d/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-pop3d/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3d/peers/0
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3d/env/MAX_CONN
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3d/env/MAX_MEM
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3d/env/MAX_PER_HOST
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3d/env/IP
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3d/env/PORT
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3ds
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3ds/log
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3ds/peers
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-pop3ds/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-pop3ds/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3ds/peers/0
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3ds/env/MAX_CONN
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3ds/env/MAX_MEM
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3ds/env/MAX_PER_HOST
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3ds/env/IP
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3ds/env/PORT

%files -n courier-base
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/courier/quotawarnmsg.example
%config(noreplace) %{_sysconfdir}/courier/shared
%config(noreplace) %{_sysconfdir}/courier/shared.tmp
%config(noreplace) %{_sysconfdir}/skel/Maildir
%{_bindir}/maildirmake
%{_bindir}/deliverquota
%{_bindir}/couriertls
%{_bindir}/maildirkw
%{_bindir}/maildiracl
%{_sbindir}/sharedindexinstall
%{_sbindir}/sharedindexsplit
%{_mandir}/man1/maildirmake.1*
%{_mandir}/man1/couriertcpd.1*
%{_mandir}/man1/maildiracl.1*
%{_mandir}/man1/maildirkw.1*
%{_mandir}/man8/deliverquota.8*
%{_libdir}/%{name}

%files doc
%defattr(-,root,root)
%doc imap/BUGS imap/ChangeLog imap/README.* imap/*.html
%doc INSTALL INSTALL.html NEWS README
%doc liblock/*.html
%doc maildir/README.* maildir/*.html
%doc rfc2045/*.html
%doc rfc822/ChangeLog.rfc822 rfc822/rfc822.html
%doc tcpd/README.* tcpd/*.html
%doc unicode/README.*
%doc maildir/maildirmake.html


%changelog
* Sun Dec 09 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1
- use the rpm-helper ssl certificate scriptlets

* Wed Oct 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1
- 4.2.1
- build against new courier-authlib
- rediff P1

* Thu Apr 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.1.3
- 4.1.3
- rediff P1
- fix the obsoletes/provides

* Sat Jan 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.1.2
- 4.1.2

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.1
- 4.1.1
- complete overhaul due to the break-out of courier-authlib
- merge maildirmake++ into courier-base
- SSL certs are now in /etc/ssl/courier rather than the default of
  /usr/share/courier (moved the ssl config files there too)
- P0: fix the pam.d/ filenames
- P1: fix the SSL cert location in mkimapdcert and mkpop3dcert
- use environment directories
- update runscripts to use envdirs (MAX_CONN, MAX_MEM, IP, PORT,
  MAX_PER_HOST); NOTE: the ./env/IP and ./env/PORT settings override
  the courier-imap configuration files' PORT/SSLPORT, ADDRESS, MAXPERIP,
  and MAXDAEMONS settings
- move the SSL certs from the old location to the new if they're found
- P2: heavy patch to remove all couriertcpd-related options from the
  config files

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8
- rebuild against new openldap, mysql, postgresql

* Sun Aug 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8
- rebuild against new mysql
- rebuild against new openssl
- rebuild against new openldap 
- spec cleanups

* Fri Jun 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8
- rebuild against new pam
- fix pam config files
- fix the spec a bit to make it more --short-circuit friendly

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8
- rebuild against new postgresql
- add -doc subpackage
- rebuild with gcc4

* Tue Feb 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8
- fix requirements (thanks Ying); should by mysql not MySQL-shared

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8
- build against new postgresql

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8-2avx
- make the imapd/pop3d daemons use peers.cdb rather than ./peers; no
  execline yet as these scripts are way too complex
- make all sub-packages require courier-imap (Requires(post)) due to
  the sysconftool-rpmupgrade script

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8-1avx
- 3.0.8
- P4: overflow patch (andreas)
- work around authmksock bug during %%install with long paths (andreas)
- minor spec cleanups
- drop P3; merged upstream

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-22avx
- use execlineb for run scripts
- move logdir to /var/log/service/courier*
- run scripts are now considered config files and are not replaceable

* Sat Aug 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-21avx
- fix perms on run scripts

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-20avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-19avx
- rebuild

* Sat Apr 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-18avx
- set AUTHDIR in runscriptappropriate on x86_64

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-17avx
- use logger for logging

* Thu Feb 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-16avx
- rebuild against new gdbm

* Wed Jan 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-15avx
- rebuild against new openssl

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-14avx
- fix typeo in courier-pop3ds run script

* Wed Oct 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-13avx
- use tcpsvd rather than tcpserver
- Requires: ipsvd
- PreReq: afterboot
- add afterboot snippet

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-12avx
- update run scripts

* Thu Aug 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-11avx
- authdaemond needs to restart on upgrades and such also

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-10avx
- rebuild against new openssl

* Sat Jul 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-9avx
- fix all of the run scripts; the imap services are reading the config
  options as env vars so we need to do some monkeying around; also
  updated them to better match courier-imap's rc scripts (aka everything
  should work properly now)

* Sat Jul 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-8avx
- fix *ssl runscripts as they need to source the non-ssl configs
  and then the *ssl configs to work properly
- respect the PORT and SSLPORT settings in the config files

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.2-7avx
- Annvix build

* Fri Apr 23 2004 Vincent Danen <vdanen@opensls.org> 2.1.2-6sls
- P3 makes authdaemond no longer daemonize itself so we can run under
  supervise (thanks Brian Candler)
- run scripts for authdaemond
- remove initscript

* Thu Mar 11 2004 Vincent Danen <vdanen@opensls.org> 2.1.2-5sls
- supervise scripts
- make all plugins %%postun rather than %%preun and use srv macros to
  restart services (the previous method was flawed in that it just stopped
  the service without restarting)
- default sysconfig files for tuning tcpserver performance

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 2.1.2-4sls
- patch authlib/configure so that builds on amd64 (ignore failed res_query
  error, only shows up on amd64)
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 2.1.2-3sls
- remove deps on fam

* Thu Dec 04 2003 Vincent Danen <vdanen@opensls.org> 2.1.2-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
