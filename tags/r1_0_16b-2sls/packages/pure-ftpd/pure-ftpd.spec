%define name	pure-ftpd
%define	version 1.0.16b
%define release 2sls

%{!?build_opensls:%global build_opensls 0}

Summary:	Lightweight, fast and secure FTP server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.pureftpd.org
Source:		ftp://download.sourceforge.net/pub/sourceforge/pureftpd/%{name}-%{version}.tar.bz2
Source1:	pure-ftpd.init 
Source2:	pure-ftpd.logrotate
Source3:	pure-ftpd-xinetd.bz2
Source4:	pureftpd.run
Source5:	pureftpd-log.run
Patch0:		pure-ftpd.mdkconf.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	pam-devel, libldap2-devel, MySQL-devel, postgresql-devel

PreReq:		rpm-helper
Provides:	ftp-server ftpserver pure-ftpd
Conflicts:	wu-ftpd, ncftpd, proftpd, anonftp, vsftpd

%description
Pure-FTPd is a fast, production-quality, standard-comformant FTP server,
based upon Troll-FTPd. Unlike other popular FTP servers, it has no known
security flaw, it is really trivial to set up and it is especially designed
for modern Linux and FreeBSD kernels (setfsuid, sendfile, capabilities) .
Features include PAM support, IPv6, chroot()ed home directories, virtual
domains, built-in LS, anti-warez system, bandwidth throttling, FXP, bounded
ports for passive downloads, UL/DL ratios, native LDAP and SQL support,
Apache log files and more.

%package anonymous
Summary:	Anonymous support for pure-ftpd
Group:		System/Servers
Requires:	pure-ftpd

%description anonymous
This package provides anonymous support for pure-ftpd. 

%package anon-upload
Summary:	Anonymous upload support for pure-ftpd
Group:		System/Servers
Requires:	pure-ftpd

%description anon-upload
This package provides anonymous upload support for pure-ftpd. 

%prep
%setup -q -n %{name}-%{version}
%setup -q -D -T -a 2

%patch -p1 -b .mdkconf

%build
%configure2_5x	--with-paranoidmsg \
		--without-capabilities \
		--with-pam \
		--with-ldap \
		--with-mysql \
		--with-pgsql \
		--with-puredb \
		--without-sendfile \
		--with-altlog \
		--with-cookie \
		--with-diraliases \
		--with-throttling \
		--with-ratios \
		--with-quotas \
		--with-ftpwho \
		--with-welcomemsg \
		--with-uploadscript \
		--with-peruserlimits \
		--with-virtualhosts \
		--with-virtualchroot \
		--with-extauth \
		--sysconfdir=%{_sysconfdir}/%{name}
		

%make

%install 
make install-strip DESTDIR=%{buildroot}

install -d -m 755 %{buildroot}%{_mandir}/man8/
install -d -m 755 %{buildroot}%{_sbindir}
install -d -m 755 %{buildroot}%{_sysconfdir}/rc.d/init.d/
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}

# Conf 

install -m 755 configuration-file/pure-config.pl %{buildroot}%{_sbindir}
install -m 644 configuration-file/pure-ftpd.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 755 configuration-file/pure-config.py %{buildroot}%{_sbindir}
install -m 644 pureftpd-ldap.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 644 pureftpd-mysql.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 644 pureftpd-pgsql.conf %{buildroot}%{_sysconfdir}/%{name}

# Man

install -m 644 man/pure-ftpd.8 %{buildroot}%{_mandir}/man8
install -m 644 man/pure-ftpwho.8 %{buildroot}%{_mandir}/man8
install -m 644 man/pure-mrtginfo.8 %{buildroot}%{_mandir}/man8
install -m 644 man/pure-uploadscript.8 %{buildroot}%{_mandir}/man8
install -m 644 man/pure-pw.8 %{buildroot}%{_mandir}/man8
install -m 644 man/pure-pwconvert.8 %{buildroot}%{_mandir}/man8
install -m 644 man/pure-statsdecode.8 %{buildroot}%{_mandir}/man8
install -m 644 man/pure-quotacheck.8 %{buildroot}%{_mandir}/man8
install -m 644 man/pure-authd.8 %{buildroot}%{_mandir}/man8

install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/pure-ftpd

# Pam 
install -d -m 755 %{buildroot}%{_sysconfdir}/pam.d/
install -m 644 pam/pure-ftpd %{buildroot}%{_sysconfdir}/pam.d/

# Logrotate
install -d %{buildroot}%{_sysconfdir}/logrotate.d/
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

#anonymous ftp
mkdir -p $RPM_BUILD_ROOT/var/ftp/pub/
mkdir -p $RPM_BUILD_ROOT/var/ftp/incoming/

%if !%{build_opensls}
# xinetd support (tv)
mkdir -p $RPM_BUILD_ROOT%_sysconfdir/xinetd.d/
bzcat %SOURCE3 > $RPM_BUILD_ROOT%_sysconfdir/xinetd.d/pure-ftpd-xinetd
%endif

%if %{build_opensls}
mkdir -p %{buildroot}/var/supervise/pureftpd/log
mkdir -p %{buildroot}/var/log/supervise/pureftpd
install -m 0755 %{SOURCE4} %{buildroot}/var/supervise/pureftpd/run
install -m 0755 %{SOURCE5} %{buildroot}/var/supervise/pureftpd/log/run
%endif

%clean
rm -rf "%{buildroot}"

%files
%defattr(-, root, root)
%doc FAQ THANKS README.Authentication-Modules README.Windows README.Virtual-Users
%doc README.Debian README README.Contrib README.Configuration-File AUTHORS CONTACT
%doc HISTORY NEWS README.LDAP README.PGSQL README.MySQL README.Netfilter
%doc pure-ftpd.png  contrib/pure-vpopauth.pl pureftpd.schema
%config(noreplace) %{_sysconfdir}/rc.d/init.d/pure-ftpd
%config(noreplace) %{_sysconfdir}/%{name}/pure-ftpd.conf
%config(noreplace) %{_sysconfdir}/%{name}/pureftpd-ldap.conf
%config(noreplace) %{_sysconfdir}/%{name}/pureftpd-mysql.conf
%config(noreplace) %{_sysconfdir}/%{name}/pureftpd-pgsql.conf
%config(noreplace) %{_sysconfdir}/pam.d/pure-ftpd
%config(noreplace) %{_sysconfdir}/logrotate.d/pure-ftpd
%if !%{build_opensls}
%config(noreplace) %_sysconfdir/xinetd.d/pure-ftpd-xinetd
%endif
%{_bindir}/pure-pw
%{_bindir}/pure-pwconvert
%{_bindir}/pure-statsdecode
%{_sbindir}/pure-config.pl
%{_sbindir}/pure-config.py
%{_sbindir}/pure-ftpd
%{_sbindir}/pure-ftpwho
%{_sbindir}/pure-uploadscript
%{_sbindir}/pure-mrtginfo
%{_sbindir}/pure-quotacheck
%{_sbindir}/pure-authd
%attr(644,root,root)%{_mandir}/man8/*
%if %{build_opensls}
%dir %attr(0750,nobody,nogroup) /var/log/supervise/pureftpd
%dir /var/supervise/pureftpd
%dir /var/supervise/pureftpd/log
/var/supervise/pureftpd/run
/var/supervise/pureftpd/log/run
%endif

%files anonymous
%defattr(-, root, root)
%dir /var/ftp/pub/

%files anon-upload
%defattr(777, root, root)
%dir /var/ftp/incoming/

%post
# ftpusers creation
if [ ! -f %{_sysconfdir}/ftpusers ]; then
	touch %{_sysconfdir}/ftpusers
fi

USERS="root bin daemon adm lp sync shutdown halt mail news uucp operator games nobody"
for i in $USERS ;do
        cat %{_sysconfdir}/ftpusers | grep -q "^$i$" || echo $i >> %{_sysconfdir}/ftpusers
done

%_post_service pure-ftpd

%pre
%_pre_useradd ftp /var/ftp /bin/false

%postun
%_postun_userdel ftp

%preun
%_preun_service pure-ftpd

%changelog
* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 1.0.16b-2sls
- OpenSLS build
- tidy spec
- remove README.RPM
- if %%build_opensls add stuff for supervise, remove stuff for xinetd

* Mon Oct 20 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.0.16b-1mdk
- 1.0.16

* Wed Aug 13 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.0.16-1mdk
- 1.0.16

* Sat Jul 19 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.14-6mdk
- rebuild

* Sat Apr 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.14-5mdk
- use configure2_5x macro
- remove anonftp provides

* Wed Apr 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.14-4mdk
- rebuild against libmysql12

* Mon Feb 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.14-3mdk
- disable xinetd server by default, using the standalone one

* Mon Feb 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.14-2mdk
- source 3 : add xinetd support

* Mon Feb  3 2003 Laurent Culioli <laurent@pschit.net> 1.0.14-1mdk
- 1.0.14

* Tue Jan 16 2003 Laurent Culioli <laurent@pschit.net> 1.0.13a-1mdk
- 1.0.13a
- remove hardcoded packager tag

* Tue Dec 31 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.0.12-6mdk
- from Brook Humphrey <bah@webmedic.net> :
	- fixed anonymous users
	- fixed ftp user not being added to ftp groups

* Mon Sep  9 2002 Arnaud Desmons <adesmons@mandrakesoft.com> 1.0.12-5mdk
- fixed invalid-packager Laurent Culioli

* Fri Aug 23 2002 Laurent Culioli <laurent@pschit.net> 1.0.12-4mdk
- fix logrotate
- add --with-diraliases options

* Tue Aug 13 2002 Laurent Culioli <laurent@pschit.net> 1.0.12-3mdk
- add logrotate support

* Tue Jun 18 2002 Laurent Culioli <laurent@mandrakesoft.com> 1.0.12-2mdk
- add user-limit support
- add pure-ftpd.png

* Tue Jun 11 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.0.12-1mdk
- 1.0.12

* Fri Mar  8 2002 Laurent Culioli <laurent@mandrakesoft.com> 1.0.10-1mdk
- 1.0.10

* Fri Feb 22 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.0.9-1mdk
- 1.0.9

* Fri Jan 25 2002 Laurent Culioli <laurent@mandrakesoft.com> 1.0.8-3mdk
- really add postgresql support
- add extauth support
- add conflict with vsftpd

* Fri Jan 25 2002 Laurent Culioli <laurent@mandrakesoft.com> 1.0.8-2mdk
- add support for pgsql and virtual-chroot
- add mdkconf patch ( change _sysconfigdir from /etc to /etc/pure-ftpd )

* Fri Jan 25 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.0.8-1mdk
- 1.0.8

* Sun Dec 30 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.0.7-1mdk
- 1.0.7
- remove now integrated patch

* Tue Nov 13 2001 Laurent Culioli <laurent@mandrakesoft.com> 1.0.1-2mdk
- add BuildRequires

* Thu Nov  8 2001 Laurent Culioli <laurent@mandrakesoft.com> 1.0.1-1mdk
- updated to 1.0.1
- pam-support is back
- enabling virtual-user ( with puredb )
- patch config.pl to use the maxdiskusagepct option ( thanks to thomas.mangin@free.fr )
- update pure-ftpd.init
- clean specfile

* Wed Sep 19 2001 Laurent Culioli <laurent@mandrakesoft.com> 0.99.2a-1mdk
- updated to 0.99.2.a 

* Mon Sep 17 2001 Laurent Culioli <laurent@mandrakesoft.com> 0.99.2-2mdk
- fix files section

* Mon Sep 17 2001 Laurent Culioli <laurent@mandrakesoft.com> 0.99.2-1mdk
- updated to 0.99.2

* Sun Sep 02 2001 Laurent Culioli <laurent@mandrakesoft.com> 0.99.1b-5mdk
- fix

* Thu Aug 30 2001 Laurent Culioli <laurent@mandrakesoft.com> 0.99.1b-4mdk
- aarggh...fix changelog ( i'm jeune , i'm naif )

* Thu Aug 30 2001 Laurent Culioli <laurent@mandrakesoft.com> 0.99.1b-3mdk
- use pure-config.pl for pure-ftpd.init
- dont use -with-pam in configure

* Thu Aug 30 2001 Laurent Culioli <laurent@mandrakesoft.com> 0.99.1b-2mdk
- fix pure-ftpd.init

* Wed Aug 29 2001 Laurent Culioli <laurent@mandrakesoft.com> 0.99.1b-1mdk
- first mandrake package
