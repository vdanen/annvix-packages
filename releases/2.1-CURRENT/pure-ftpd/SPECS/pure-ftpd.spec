#
# spec file for package pure-ftpd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		pure-ftpd
%define	version 	1.0.21
%define release 	%_revrel

Summary:	Lightweight, fast and secure FTP server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.pureftpd.org
Source:		http://download.pureftpd.org/pub/pure-ftpd/releases/%{name}-%{version}.tar.bz2
Source2:	pure-ftpd.logrotate
Source4:	pureftpd.run
Source5:	pureftpd-log.run
Source6:	pure-ftpd.pam
Patch0:		pure-ftpd-1.0.16b-slsconf.patch
Patch1:		pure-ftpd-1.0.16b-pureconfig.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	pam-devel
BuildRequires:	openldap-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	openssl-devel

Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	rpm-helper
Requires(preun): rpm-helper
Provides:	ftp-server
Provides:	ftpserver
Obsoletes:	pure-ftpd-anonymous
Obsoletes:	pure-ftpd-anon-upload

%description
Pure-FTPd is a fast, production-quality, standard-conformant FTP server,
that focuses on security.

It is really trivial to set up and it is especially designed for modern
Linux and FreeBSD kernels (setfsuid, sendfile, capabilities).  Features
include chroot()ed and/or virtual chroot()ed home directories, virtual
domains, built-in 'ls', anti-warez system, bounded ports for passive
downloads, FXP protocol, bandwidth throttling, ratios, LDAP / MySQL /
PostgreSQL-based authentication, fortune files, Apache-like log files, fast
standalone mode, text / HTML / XML real-time status report, virtual users,
virtual quotas, privilege separation and more.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%setup -q -D -T -a 2

%patch0 -p1 -b .mdkconf
%patch1 -p1 -b .pureconfig

# fix the path for docs
perl -pi -e 's|/etc/ssl/private/pure-ftpd.pem|/etc/pure-ftpd/pure-ftpd.pem|g' README.TLS


%build
%configure2_5x \
    --with-paranoidmsg \
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
    --with-largefile \
    --with-privsep \
    --with-tls \
    --with-certfile=/etc/pure-ftpd/pure-ftpd.pem \
    --sysconfdir=%{_sysconfdir}/%{name}

%make


%install 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install-strip DESTDIR=%{buildroot}

mkdir -p %{buildroot}{%{_mandir}/man8,%{_sbindir},%{_sysconfdir}/{%{name},pam.d,logrotate.d}}

install -m 0755 configuration-file/pure-config.pl %{buildroot}%{_sbindir}
install -m 0644 configuration-file/pure-ftpd.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 0755 configuration-file/pure-config.py %{buildroot}%{_sbindir}
install -m 0644 pureftpd-ldap.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 pureftpd-mysql.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 pureftpd-pgsql.conf %{buildroot}%{_sysconfdir}/%{name}

install -m 0644 man/pure-ftpd.8 %{buildroot}%{_mandir}/man8
install -m 0644 man/pure-ftpwho.8 %{buildroot}%{_mandir}/man8
install -m 0644 man/pure-mrtginfo.8 %{buildroot}%{_mandir}/man8
install -m 0644 man/pure-uploadscript.8 %{buildroot}%{_mandir}/man8
install -m 0644 man/pure-pw.8 %{buildroot}%{_mandir}/man8
install -m 0644 man/pure-pwconvert.8 %{buildroot}%{_mandir}/man8
install -m 0644 man/pure-statsdecode.8 %{buildroot}%{_mandir}/man8
install -m 0644 man/pure-quotacheck.8 %{buildroot}%{_mandir}/man8
install -m 0644 man/pure-authd.8 %{buildroot}%{_mandir}/man8

mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
install -m 0644 %{_sourcedir}/pure-ftpd.pam %{buildroot}%{_sysconfdir}/pam.d/pure-ftpd

install -m 0644 %{_sourcedir}/pure-ftpd.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

mkdir -p %{buildroot}%{_srvdir}/pureftpd/log
install -m 0740 %{_sourcedir}/pureftpd.run %{buildroot}%{_srvdir}/pureftpd/run
install -m 0740 %{_sourcedir}/pureftpd-log.run %{buildroot}%{_srvdir}/pureftpd/log/run


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
# ftpusers creation
if [ ! -f %{_sysconfdir}/ftpusers ]; then
    touch %{_sysconfdir}/ftpusers
fi

USERS="root bin daemon adm lp sync shutdown halt mail news uucp operator games nobody"
for i in $USERS ;do
    cat %{_sysconfdir}/ftpusers | grep -q "^$i$" || echo $i >> %{_sysconfdir}/ftpusers
done

%_post_srv pureftpd


%pre
%_pre_useradd ftp /var/ftp /bin/false 81


%postun
%_postun_userdel ftp


%preun
%_preun_srv pureftpd


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/pure-ftpd.conf
%config(noreplace) %{_sysconfdir}/%{name}/pureftpd-ldap.conf
%config(noreplace) %{_sysconfdir}/%{name}/pureftpd-mysql.conf
%config(noreplace) %{_sysconfdir}/%{name}/pureftpd-pgsql.conf
%config(noreplace) %{_sysconfdir}/pam.d/pure-ftpd
%config(noreplace) %{_sysconfdir}/logrotate.d/pure-ftpd
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
%dir %attr(0750,root,admin) %{_srvdir}/pureftpd
%dir %attr(0750,root,admin) %{_srvdir}/pureftpd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/pureftpd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/pureftpd/log/run

%files doc
%defattr(-,root,root)
%doc FAQ THANKS README.Authentication-Modules README.Windows README.Virtual-Users README.TLS
%doc README.Debian README README.Contrib README.Configuration-File AUTHORS CONTACT
%doc HISTORY NEWS README.LDAP README.PGSQL README.MySQL README.Netfilter
%doc pure-ftpd.png  contrib/pure-vpopauth.pl contrib/pure-stat.pl pureftpd.schema


%changelog
* Tue Jul 24 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.21
- rebuild against new mysql

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.21
- rebuild against new postgresql

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.21
- rebuild against new pam

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.21
- rebuild against new mysql, postgresql, openldap

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.21
- rebuild against new mysql
- rebuild against new openssl
- rebuild against new openldap
- spec cleanups

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.21
- build with privsep and TLS support
- buildrequires: openssl-devel
- remove conflicts
- update description

* Fri Jun 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.21
- rebuild against new pam
- install S6 for new pam

* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.21
- 1.0.21
- add -doc subpackage
- rebuild with gcc4
- rebuild against new postgresql
- drop the -anonymous and -anon-upload packages since all they contain
  are directories... i suppose the end-user may be intelligent enough
  to create these directories themself if required <sheesh>
- S6: pam file for new pam (coming soon)

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.20
- build against new postgresql

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.20
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.20
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.20
- Obfuscate email addresses and new tagging
- Uncompress patches
- drop S1 (initscript) and S3 (xinetd support)
- fix prereq

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.20-5avx
- use execlineb for run scripts
- move logdir to /var/log/service/pureftpd
- run scripts are now considered config files and are not replaceable

* Sat Aug 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.20-4avx
- fix perms on run scripts

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.20-3avx
- rebuild

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.20-1avx
- 1.0.20
- enable largefile support
- user logger for logging

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.19-2avx
- update run scripts

* Mon Jul 05 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.19-1avx
- fix source url
- 1.0.19 (fix possible DoS)
- fix service name in %%_preun_srv and %%_post_srv

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.18-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 1.0.18-1sls
- 1.0.18

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 1.0.16b-5sls
- pure-config.pl now prints the pure-ftpd commandline instead of executing
  pure-ftpd (better for supervise) (P2)
- by default Daemonize==no in config

* Wed Feb 04 2004 Vincent Danen <vdanen@opensls.org> 1.0.16b-4sls
- remove %%build_opensls macro
- remove xinetd stuff
- srv macros
- remove initscript
- /var/service not /var/supervise
- ftp has static uid/gid 81

* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 1.0.16b-3sls
- BuildRequires: openldap-devel, not libldap2-devel (for amd64)

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 1.0.16b-2sls
- OpenSLS build
- tidy spec
- remove README.RPM
- if %%build_opensls add stuff for supervise, remove stuff for xinetd

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
