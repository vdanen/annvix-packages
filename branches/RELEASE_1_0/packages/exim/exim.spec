%define name	exim
%define version 4.50
%define release 1avx

%define build_mysql 0
%define build_pgsql 0
%define saversion   4.1

%define alternatives 1
%define altpriority  40
%define alternatives_install_cmd update-alternatives --install %{_sbindir}/sendmail mta %{_sbindir}/sendmail.exim %{altpriority} --slave %{_libdir}/sendmail mta-in_libdir %{_sbindir}/sendmail.exim --slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.exim --slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.exim --slave %{_bindir}/rmail mta-rmail %{_bindir}/rmail.exim --slave %{_sysconfdir}/aliases mta-etc_aliases %{_sysconfdir}/exim/aliases

# commandline overrides:
# rpm -ba|--rebuild --define 'with_xxx'
%{?_with_mysql: %{expand: %%define build_mysql 1}}
%{?_with_pgsql: %{expand: %%define build_pgsql 1}}

Name:		%{name}
Summary:	The exim mail transfer agent
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.exim.org
Source:		ftp://ftp.exim.org/pub/exim/exim4/%{name}-%{version}.tar.bz2
Source1:	exim.aliases
Source2:	exim.init
Source3:	exim.sysconfig
Source4:	exim.logrotate
Source5:	exim.8
Source8:	eximconfig
Source9:	exim.pam
Source10:	ftp://ftp.exim.org/pub/exim/exim4/%{name}-%{version}.tar.bz2.sig
Source11:	http://www.exim.org/ftp/exim4/config.samples.tar.bz2
# http://sa-exim.sourceforge.net/
Source12:	sa-exim-%{saversion}.tar.gz
Source13:	exim.run
Source14:	exim-log.run
Patch0:		exim-4.50-avx-config.patch.bz2
Patch2:		exim-4.22-install.patch.bz2
Patch3:		exim-4.43-debian-system_pcre.diff.bz2
Patch4:		exim-4.43-debian-dontoverridecflags.diff.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	tcp_wrappers-devel, pam-devel, openssl, openssl-devel, openldap-devel, lynx
BuildRequires:	db4-devel >= 4.1, pcre-devel, perl-devel
%if %{build_mysql}
BuildRequires:	libmysql-devel
%endif
%if %{build_pgsql}
BuildRequires: postgresql-devel
%endif

PreReq:		rpm-helper
%if %{alternatives}
PreReq:		rpm
%else
Obsoletes:	sendmail postfix qmail smail
%endif
Requires:	chkconfig, initscripts, sh-utils, openssl, pam
Requires:	openldap >= 2.0.11
%ifarch amd64 x86_64
Requires:	lib64db4.1
%else
Requires:	libdb4.1
%endif
Provides:	smtpdaemon MTA

%description
Exim is a mail transport agent (MTA) developed at the University of
Cambridge for use on Unix systems connected to the Internet. In style
it is similar to Smail 3, but its facilities are more extensive, and
in particular it has options for verifying incoming sender and
recipient addresses, for refusing mail from specified hosts, networks,
or senders, and for controlling mail relaying. Exim is in production
use at quite a few sites, some of which move hundreds of thousands of
messages per day.

A utility, eximconfig, is included to simplify exim configuration.

%package saexim
Summary:	Exim SpamAssassin at SMTP time plugin
Group:		System/Servers
Requires:	%{name}

%description saexim
Allows running SpamAssassin on incoming mail and rejection
at SMTP time as well as other nasty things like teergrubbing.


%prep
%setup -q
%setup -q -T -D -a 11
%setup -q -T -D -a 12
%patch0 -p1 -b .config
%patch2 -p1 -b .install
%patch3 -p1 -b .pcre
%patch4 -p0 -b .cflags

# apply the SA-exim dlopen patch
cat sa-exim*/localscan_dlopen_exim_4.20_or_better.patch | patch -p1

%build
# pre-build setup
cp src/EDITME Local/Makefile

# modify Local/Makefile for our builds
%if !%{build_mysql}
  perl -pi -e 's|LOOKUP_MYSQL=yes|#LOOKUP_MYSQL=yes|g' Local/Makefile
  perl -pi -e 's|-lmysqlclient||g' Local/Makefile
  perl -pi -e 's|-I /usr/include/mysql||g' Local/Makefile
%endif
%if !%{build_pgsql}
  perl -pi -e 's|LOOKUP_PGSQL=yes|#LOOKUP_PGSQL=yes|g' Local/Makefile
  perl -pi -e 's|-lpq||g' Local/Makefile
  perl -pi -e 's|-I /usr/include/pgsql||g' Local/Makefile
%endif
%ifarch amd64 x86_64
  perl -pi -e 's|X11\)/lib|X11\)/lib64|g' OS/Makefile-Linux
%endif

make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

# build SA-exim
cd sa-exim*
perl -pi -e 's|/usr/lib/exim4/local_scan|%{_libdir}/exim|g' INSTALL
make clean
make SACONF=/etc/exim/sa-exim.conf CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-shared -fPIC"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_sbindir},%{_bindir},%{_libdir},%{_sysconfdir}/{pam.d,exim}}

make DESTDIR=%{buildroot} install

pushd %{buildroot}%{_bindir}
mv exim-%{version}-1 exim
popd

install -m 0775 build-`scripts/os-type`-`scripts/arch-type`/convert4r3 %{buildroot}%{_bindir}
install -m 0775 build-`scripts/os-type`-`scripts/arch-type`/convert4r4 %{buildroot}%{_bindir}

install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/exim/aliases
install -m 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/pam.d/exim

pushd %{buildroot}%{_sbindir}/
ln -sf ../bin/exim sendmail.exim
ln -sf ../bin/exim exim
popd

pushd %{buildroot}%{_bindir}/
ln -sf exim runq
ln -sf exim rsmtp
ln -sf exim mailq.exim
ln -sf exim rmail.exim
ln -sf exim newaliases.exim
popd

install -d -m 0750 %{buildroot}/var/spool/exim
install -d -m 0750 %{buildroot}/var/spool/exim/db
install -d -m 0750 %{buildroot}/var/spool/exim/input
install -d -m 0750 %{buildroot}/var/spool/exim/msglog
install -d -m 0750 %{buildroot}/var/log/exim

mkdir -p %{buildroot}{%{_mandir}/man8,%{_sysconfdir}/{sysconfig,cron.weekly}}
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/exim
install -m 0755 %{SOURCE4} %{buildroot}%{_sysconfdir}/cron.weekly/exim.logrotate
install -m 0644 %{SOURCE5} %{buildroot}%{_mandir}/man8/exim.8
install -m 0755 %{SOURCE8} %{buildroot}%{_sbindir}

mkdir -p %{buildroot}{%{_srvdir}/exim/log,%{_srvlogdir}/exim}
install -m 0755 %{SOURCE13} %{buildroot}%{_srvdir}/exim/run
install -m 0755 %{SOURCE14} %{buildroot}%{_srvdir}/exim/log/run

# install SA-exim
cd sa-exim*
mkdir -p %{buildroot}%{_libdir}/exim
install -m 0644 *.so %{buildroot}%{_libdir}/exim
install -m 0644 *.conf %{buildroot}%{_sysconfdir}/exim
pushd %{buildroot}%{_libdir}/exim
ln -s sa-exim*.so sa-exim.so
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_post_srv exim
%if %{alternatives}
%{alternatives_install_cmd}
%endif

# scrub hints files - db files change format between builds so
# killing the hints can save an MTA crash later
[ -d /var/spool/exim/db ] && rm -f /var/spool/exim/db/*

# alternatives changes the mode of /usr/bin/exim so we have to chmod
chmod 4755 %{_bindir}/exim

if [ $1 = 1 ]; then
  echo "Run %{_sbindir}/eximconfig to interactively configure exim"
fi


# necessary when we upgrade from a non-alternatives package
%triggerpostun -- exim
%if %{alternatives}
[ -e %{_sbindir}/sendmail.exim ] && %{alternatives_install_cmd} || :
%endif

%preun
%_preun_srv exim
if [ $1 = 0 ]; then
  %if %{alternatives}
    update-alternatives --remove mta %{_sbindir}/sendmail.exim
  %endif
fi


%files
%defattr(755,root,root)
%doc doc/ChangeLog LICENCE NOTICE README.UPDATING README
%doc doc util/unknownuser.sh build-Linux-*/transport-filter.pl
%doc util/cramtest.pl util/logargs.sh
%doc doc/NewStuff doc/Exim4.upgrade doc/*.txt doc/README.SIEVE
%attr(4755,root,root) %{_bindir}/exim
%{_bindir}/exim_checkaccess
%{_bindir}/exim_dumpdb
%{_bindir}/exim_fixdb
%{_bindir}/exim_tidydb
%{_bindir}/exinext
%{_bindir}/exipick
%{_bindir}/exiwhat
%{_bindir}/exim_dbmbuild
%{_bindir}/exicyclog
%{_bindir}/exigrep
%{_bindir}/eximstats
%{_bindir}/exiqgrep
%{_bindir}/exiqsumm
%{_bindir}/exim_lock
%{_bindir}/convert4r3
%{_bindir}/convert4r4
%{_sbindir}/exim
%{_sbindir}/eximconfig
%{_bindir}/runq
%{_bindir}/rsmtp
# alternatives
%{_sbindir}/sendmail.exim
%{_bindir}/mailq.exim
%{_bindir}/rmail.exim
%{_bindir}/newaliases.exim
%{_mandir}/man8/exim.8*

%defattr(-,mail,mail)
%dir /var/spool/exim
%dir /var/spool/exim/db
%dir /var/spool/exim/input
%dir /var/spool/exim/msglog
%dir /var/log/exim

%defattr(-,root,mail)
%dir %{_sysconfdir}/exim
%config(noreplace) %{_sysconfdir}/exim/exim.conf
%config(noreplace) %{_sysconfdir}/exim/aliases

%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/exim
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cron.weekly/exim.logrotate
%config(noreplace) %{_sysconfdir}/pam.d/exim
%dir %{_srvdir}/exim
%dir %{_srvdir}/exim/log
%{_srvdir}/exim/run
%{_srvdir}/exim/log/run
%dir %attr(0750,logger,logger) %{_srvlogdir}/exim

%files saexim
%defattr(-,root,root)
%doc sa-exim*/*.html sa-exim*/{ACKNOWLEDGEMENTS,INSTALL,LICENSE,TODO}
%dir %{_libdir}/exim
%{_libdir}/exim/*
%config(noreplace) %{_sysconfdir}/exim/sa-exim.conf
%config(noreplace) %{_sysconfdir}/exim/sa-exim_short.conf

%changelog
* Wed Mar 16 2005 Vincent Danen <vdanen@annvix.org> 4.50-1avx
- 4.50
- exiscan is now integrated in exim, so drop P1
- enable support for old demime ACL's but this is deprecated for the
  mime ACLs so this will be removed in the very near future (keep it
  for migratory purposes and backwards compatibility) by updating P0
- add some more docs

* Thu Mar 03 2005 Vincent Danen <vdanen@annvix.org> 4.44-3avx
- use logger for logging

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 4.44-2avx
- rebuild against new perl

* Fri Jan 21 2005 Vincent Danen <vdanen@annvix.org> 4.44-1avx
- 4.44
- exiscan-acl 4.44-28
- drop P5

* Wed Jan 05 2005 Vincent Danen <vdanen@annvix.org> 4.43-2avx
- actually apply P3 and P4
- P5: minor security fixes posted to exim ml by Philip

* Mon Dec 20 2004 Vincent Danen <vdanen@annvix.org> 4.43-1avx
- 4.43
- exiscan-acl 4.43-28
- P3: use system pcre libs
- P4: don't override cflags
- remove exim-mon completely
- BuildRequires: pcre-devel, perl-devel
- enable IPv6 support
- enable cyrus-sasl support

* Mon Sep 20 2004 Vincent Danen <vdanen@annvix.org> 4.42-1avx
- 4.42
- exiscan-acl 4.42-27
- update run scripts

* Thu Aug 19 2004 Vincent Danen <vdanen@annvix.org> 4.41-1avx
- 4.41
- exiscan-acl 4.41-25
- sa-exim 4.1
- move saexim libs from /usr/libexec/exim to %%{_libdir}/exim
- update the patch location in the sa-exim INSTALL doc

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 4.34-2avx
- Annvix build
- don't build the X11 monitor (%%build_mon macro)

* Mon May 10 2004 Vincent Danen <vdanen@opensls.org> 4.34-1sls
- 4.34
- exiscan-acl 4.34-21
- remove P3; integrated upstream

* Sat May 08 2004 Vincent Danen <vdanen@opensls.org> 4.33-1sls
- 4.33
- exiscan-acl 4.33-20
- sa-exim 4.0
- fix source url
- include doc/ChangeLog instead of CHANGES
- patch to fix CAN-2004-0400
- rediff P0; default delivery is now to /var/mail rather than
  /var/spool/mail

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.30-7sls
- remove mangling of msec

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 4.30-6sls
- tidy spec
- remove docs

* Tue Jan 27 2004 Vincent Danen <vdanen@opensls.org> 4.30-5sls
- use %%_post_srv and %%_preun_srv

* Mon Jan 26 2004 Vincent Danen <vdanen@opensls.org> 4.30-4sls
- remove initscript
- use %%_srvdir and %%_srvlogdir macros

* Sat Jan 10 2004 Vincent Danen <vdanen@opensls.org> 4.30-3sls
- Requires lib64db4.1 if amd64

* Mon Jan 05 2004 Vincent Danen <vdanen@opensls.org> 4.30-2sls
- BuildRequires: openldap-devel not libldap2-devel (amd64)
- if amd64, make eximon libs look in /usr/X11R6/lib64
- pass -fPIC and -Wall to sa-exim build
- supervise scripts

* Sat Dec 06 2003 Vincent Danen <vdanen@opensls.org> 4.30-1sls
- 4.30
- exiscan-acl 4.30-14
- 4.30 docs
- sa-exim 3.1
- rediff P0

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 4.24-3sls
- strip support for old mdk releases
- exiscan-acl 4.24-13

* Fri Oct 26 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.24-2mdk
- build for Corp3
- BuildRequires: lynx
- fix config to allow delivery to @localhost by default (for fetchmail, etc.)

* Mon Sep 29 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.24-1rph
- 4.24
- exiscan 4.24-12
- rediff P0

* Fri Sep 19 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.22-6rph
- fix the default config file so mail deliveries are made with egid mail
  (otherwise msgs are unable to be written to the spool)
- change /var/mail/$localpart to /var/spool/mail/$localpart

* Fri Sep 19 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.22-5rph
- build for 9.2
- if build_92; requires libdb4.1-devel
- add -lpam to our libs so it builds under 9.2
- add reload to initscript

* Sat Aug 23 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.22-4rph
- include sa-exim
- scrub db hints file (ala RH spec) which can cause db version mismatch
  problems
- include config samples

* Fri Aug 22 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.22-3rph
- force exim to read configs in /etc/exim so a) we don't have to worry about
  alternatives and b) exim doesn't complain about being unable to read the
  aliases file
- fix some of our msec-tampering logic
- throw in an extra echo at the end of %%post to make rpm not think we
  exited with errors if we're upgrading
- some spec cleanups
- patch scripts/exim_install so we don't need to run it as root
- remove logrotate entry for exim, add a cron.weekly entry to call exicyclog
- include exiqgrep (previously was missing)

* Thu Aug 21 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.22-2rph
- start using the exiscan-acl patches by default (4.22-10)
- add queue and doqueue commands to initscript
- use alternatives; give exim priority 40 so it is higher than 
  postfix (since postfix will likely be default)
- exim configs now go in /etc/exim
- use Obsoletes instead of Conflicts for qmail/postfix/sendmail/smail
- some hacks for dealing with msec

* Mon Aug 18 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.22-1rph
- 4.22; includes security fixes
- rediff P0
- include doc/NewStuff

* Thu May 15 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.20-1rph
- 4.20
- updated html docs and FAQ

* Thu May 7 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.14-3rph
- better build macro for CS2.1
- fix requirements for 9.1 (use libdb4.0, not db4 since nothing provides
  db4)

* Wed Apr 16 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.14-2rph
- enable dsearch (directory search)
- enable wildcard lsearch (linear search)
- enable dnsdb lookups

* Mon Apr 14 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.14-1rph
- 4.14

* Wed Apr 2 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.12-1rph
- 4.12
- conditional build macros for 9.0, 9.1 (9.0 uses db3, 9.1 uses db4)
- rediff P0
- PreReq: rpm-helper

* Mon Nov 25 2002 Vincent Danen <vdanen@mandrakesoft.com> 4.10-2rph
- put exim in %%{_bindir} and a symlink in %%{_sbindir}
- fix other symlinks

* Fri Nov 22 2002 Vincent Danen <vdanen@mandrakesoft.com> 4.10-1rph
- 4.10
- new patches for config; this time we build with postgres and mysql support
- lots of spec cleanups
- move all binaries except exim from %%{_sbindir} to %%{_bindir}
- some build macros: --with mysql, --with pgsql for MySQL, and PostgreSQL
  support respectively (not built by default)

* Thu Oct 10 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.36-1rph
- 3.36

* Mon Apr 15 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.33-5rph
- rebuild with rph extension

* Sun Nov 25 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.33-4mdk
- BuildRequires: XFree86-devel, openssl-devel

* Mon Nov 19 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.33-3mdk
- fix builds under 8.1
- don't remove log files on uninstall
- make more configs noreplace
- use %%_post_service and %%_preun_service macros
- use build macros: (ie. "rpm -ba --with 80 exim.spec" to build for 8.0)

* Fri Sep 21 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.33-2mdk
- remove dependency on openldap for 8.0 builds

* Fri Sep 21 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.33-1mdk
- first Mandrake build based on RPM from Mark Bergsma <mark@nedworks.org>
- Mandrake adaptations
- include support for TLS and LDAP (LDAP only in 8.1 package)
- use db3
