%define name	courier-imap
%define version	2.1.2
%define release	2sls

%define _localstatedir	/var/run
%define	authdaemondir	%{_localstatedir}/authdaemon.courier-imap
%define	courierdatadir	%{_datadir}/courier
%define	courierlibdir	%{_libdir}/courier
%define	couriersysconfdir %{_sysconfdir}/courier

%define	courier_patch_version 0.42.0

Summary:	Courier-IMAP is an IMAP server that uses Maildirs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.courier-mta.org
Source0:	%{name}-%{version}.tar.bz2
Source1:	courier-imap-sysconftool-rpmupgrade.bz2
# S4 & S5  originates from the works of Carlo Contavalli and can be found here:
# http://www.commedia.it/ccontavalli/
Source2:	courier_patch.tar.gz
Source3:	courier_patch.tar.gz.asc
Source4:	auto_maildir_creator.bz2
# (fc) 1.4.2-2mdk fix missing command in initrd
Patch0: 	courier-imap-1.6.1-initrd.patch.bz2
Patch1:		courier-imap-2.1.2-auto_maildir_creator.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildPreReq:	autoconf2.5, coreutils, libtool, perl, sed
BuildRequires:	openssl-devel, pam-devel, fam-devel, gdbm-devel
# ldap subpackage:
BuildRequires:	openldap-devel
# mysql subpackage:
BuildRequires:	MySQL-devel 
# postgresql subpackage:
BuildRequires:	postgresql-devel

Requires:	chkconfig, coreutils, fam, gdbm, sed
#Requires:	libopenssl0.9.7
PreReq:		maildirmake++, rpm-helper
Conflicts:	uw-imap, bincimap
Provides:	imap, imap-server

%description
Courier-IMAP is an IMAP server for Maildir mailboxes.  This package contains
the standalone version of the IMAP server that's included in the Courier
mail server package.  This package is a standalone version for use with
other mail servers.  Do not install this package if you intend to install
the full Courier mail server.  Install the Courier package instead.

%package pop
Summary:	Courier-IMAP POP servers
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
Provides:	pop, pop-server
Conflicts:	uw-imap-pop

%description pop
This package contains the POP servers of the Courier-IMAP
server suite.

%package ldap
Summary:	Courier-IMAP LDAP authentication driver.
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
#Requires:	libldap2
Conflicts:	%{name}-mysql %{name}-pgsql

%description ldap
This package contains the necessary files to allow Courier-IMAP to
authenticate from an LDAP directory.  Install this package if you need the
ability to use an LDAP directory for authentication.

%package mysql
Summary:	Courier-IMAP MySQL authentication driver.
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}, MySQL-shared
Conflicts:	%{name}-ldap %{name}-pgsql

%description mysql
This package contains the necessary files to allow Courier-IMAP to
authenticate using a MySQL database table.  Install this package if you need
the ability to use a MySQL database table for authentication.

%package pgsql
Summary:	Courier-IMAP PostgreSQL authentication driver.
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}, postgresql-libs
Conflicts:	%{name}-ldap %{name}-mysql

%description pgsql
This package contains the necessary files to allow Courier-IMAP to
authenticate using a PostgreSQL database table.  Install this package if you
need the ability to use a PostgreSQL database table for authentication.

%package utils
Summary:	Courier-IMAP debugging utils.
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}

%description utils
This package contains the necessary files to debug the authentication
modules for Courier-IMAP.

You may also as of v1.6.0 use DEBUG_LOGIN.

%package -n maildirmake++
Summary:	The maildirmake application by Mr. Sam
Group:		System/Servers
Provides:	maildirmake
Obsoletes:	maildirmake

%description -n	maildirmake++
This package contains the maildirmake command.

You can create either standard Maildir or Maildir++ with the
maildirmake command.

%prep
%setup -q -a2
%patch0 -p0 -b .initrd
%patch1 -p1 -b .auto_maildir_creator

%build

%configure2_5x \
    --enable-unicode \
    --enable-workarounds-for-imap-client-bugs \
    --disable-root-check \
    --localstatedir=%{_localstatedir} \
    --with-authdaemonvar=%{authdaemondir} \
    --libexec=%{courierlibdir} \
    --datadir=%{courierdatadir} \
    --sysconfdir=%{couriersysconfdir} \
    --with-db=gdbm \
    --with-dirsync \
    --without-authvchkpw

%make

# don't run that if using --enable-workarounds-for-imap-client-bugs
#make check

%install
if [ -d %{buildroot} ]; then rm -rf %{buildroot}; fi

mkdir -p %{buildroot}%{_sysconfdir}/pam.d

%makeinstall_std

mkdir -p %{buildroot}%{_initrddir}
install -m755 courier-imap.sysvinit %{buildroot}%{_initrddir}/courier-imap

# Fix imapd.dist
perl -p -i -e 's|^IMAPDSTART=.*|IMAPDSTART=YES|' %{buildroot}%{couriersysconfdir}/imapd.dist
perl -p -i -e 's|^IMAPDSSLSTART=.*|IMAPDSSLSTART=YES|' %{buildroot}%{couriersysconfdir}/imapd-ssl.dist
perl -p -i -e 's|^POP3DSTART=.*|POP3DSTART=YES|' %{buildroot}%{couriersysconfdir}/pop3d.dist
perl -p -i -e 's|^POP3DSSLSTART=.*|POP3DSSLSTART=YES|' %{buildroot}%{couriersysconfdir}/pop3d-ssl.dist

# nuke this...
rm -rf %{buildroot}%{_sysconfdir}/profile.d

# fix this...
cp imap/README imap/README.imap
cp rfc822/ChangeLog rfc822/ChangeLog.rfc822
cp unicode/README unicode/README.unicode

# Create config files for sysconftool-rpmupgrade (see below)
mkdir -p %{buildroot}%{courierdatadir}
cat sysconftool > %{buildroot}%{courierdatadir}/sysconftool
cat << EOF > %{buildroot}%{courierdatadir}/configlist
%{couriersysconfdir}/imapd.dist
%{couriersysconfdir}/imapd-ssl.dist
EOF

cat << EOF > %{buildroot}%{courierdatadir}/configlist.pop
%{couriersysconfdir}/pop3d.dist
%{couriersysconfdir}/pop3d-ssl.dist
EOF

touch %{buildroot}%{courierdatadir}/configlist.ldap
touch %{buildroot}%{courierdatadir}/configlist.mysql
touch %{buildroot}%{courierdatadir}/configlist.pgsql

# Backwards compatability for older versions of courier-imap.  Run the
# sysconftool-rpmupgrade script if you are upgrading from an older
# courier-imap RPM
bzip2 -cd %{SOURCE1} > %{buildroot}%{courierdatadir}/sysconftool-rpmupgrade

# Check if authdaemond was installed, make sure to include authdaemon
# directory
touch authdaemon.files

. authlib/authdaemonrc

if [ "x$authdaemonvar" != "x" ]; then
	echo "%{couriersysconfdir}/authdaemonrc.dist" >> %{buildroot}%{courierdatadir}/configlist
	echo '%dir %attr(700, root, root) ' $authdaemonvar		>  authdaemon.files
	touch %{buildroot}/${authdaemonvar}/lock		|| exit 1
	touch %{buildroot}/${authdaemonvar}/pid			|| exit 1
	authlib/authmksock %{buildroot}/${authdaemonvar}/socket	|| exit 1
	echo '%ghost %attr(600, root, root) ' ${authdaemonvar}/lock	>> authdaemon.files
	echo '%ghost %attr(644, root, root) ' ${authdaemonvar}/pid	>> authdaemon.files
	echo '%ghost %attr(777, root, root) ' ${authdaemonvar}/socket	>> authdaemon.files
fi

(cd %{buildroot} ; find .%{courierlibdir} -type f ! -name authdaemond.ldap ! -name authdaemond.mysql ! -name authdaemond.pgsql -print ) | cut -c2- >> authdaemon.files

touch authdaemon.files.ldap
touch authdaemon.files.mysql
touch authdaemon.files.pgsql

test ! -f %{buildroot}%{courierlibdir}/authlib/authdaemond.mysql ||
        echo %{courierlibdir}/authlib/authdaemond.mysql >>authdaemon.files.mysql

test ! -f %{buildroot}%{courierlibdir}/authlib/authdaemond.pgsql ||
        echo %{courierlibdir}/authlib/authdaemond.pgsql >>authdaemon.files.pgsql

test ! -f %{buildroot}%{courierlibdir}/authlib/authdaemond.ldap || \
        echo %{courierlibdir}/authlib/authdaemond.ldap >>authdaemon.files.ldap

if test -f %{buildroot}%{courierlibdir}/authlib/authdaemond.mysql
then
        echo '%{couriersysconfdir}/authmysqlrc.dist' >>%{buildroot}%{courierdatadir}/configlist.mysql
        echo '%attr(-, root, root) %config(noreplace) %{couriersysconfdir}/authmysqlrc.dist' >>authdaemon.files.mysql
fi

if test -f %{buildroot}%{courierlibdir}/authlib/authdaemond.pgsql
then
        echo '%{couriersysconfdir}/authpgsqlrc.dist' >>%{buildroot}%{courierdatadir}/configlist.pgsql
        echo '%attr(-, root, root) %config(noreplace) %{couriersysconfdir}/authpgsqlrc.dist' >>authdaemon.files.pgsql
fi

if test -f %{buildroot}%{courierlibdir}/authlib/authdaemond.ldap
then
        echo %{couriersysconfdir}/authldaprc.dist >> %{buildroot}%{courierdatadir}/configlist.ldap
        echo '%attr(-, root, root) %config(noreplace) %{couriersysconfdir}/authldaprc.dist' >> authdaemon.files.ldap

        if test -d /etc/openldap/schema
        then
                mkdir -p %{buildroot}/etc/openldap/schema
                cp authlib/authldap.schema %{buildroot}/etc/openldap/schema/courier.schema
                echo '%config(noreplace) %attr(444, root, root) /etc/openldap/schema/courier.schema' >>authdaemon.files.ldap
        fi
fi

mkdir -p %{buildroot}%{_localstatedir}
touch %{buildroot}%{_localstatedir}/imapd.pid
touch %{buildroot}%{_localstatedir}/imapd-ssl.pid
touch %{buildroot}%{_localstatedir}/imapd.pid.lock
touch %{buildroot}%{_localstatedir}/imapd-ssl.pid.lock

touch %{buildroot}%{_localstatedir}/pop3d.pid
touch %{buildroot}%{_localstatedir}/pop3d-ssl.pid
touch %{buildroot}%{_localstatedir}/pop3d.pid.lock
touch %{buildroot}%{_localstatedir}/pop3d-ssl.pid.lock

find %{buildroot} -type f -print | sed "s@^%{buildroot}@@g" | grep -v perllocal.pod > $RPM_BUILD_DIR/tmp-filelist

# some utils...
install -m755 authlib/authinfo %{buildroot}%{_bindir}/courier-imap-authinfo
install -m755 authlib/authtest %{buildroot}%{_bindir}/courier-imap-authtest
install -m755 authlib/authdaemontest %{buildroot}%{_bindir}/courier-imap-authdaemontest

# fix the maildirmake command so it won't conflict with vdanens qmail package?
mv %{buildroot}%{_bindir}/maildirmake %{buildroot}%{_bindir}/maildirmake++
mv %{buildroot}%{_mandir}/man1/maildirmake.1 %{buildroot}%{_mandir}/man1/maildirmake++.1

# fix the auto maildir creation stuff
bzip2 -cd %{SOURCE4} > %{buildroot}%{courierdatadir}/auto_maildir_creator
chmod 755 %{buildroot}%{courierdatadir}/auto_maildir_creator
mkdir automatic_maildir_creation_patch
cp -f courier_patch/html/*.html automatic_maildir_creation_patch/
cp -f courier_patch/README.txt automatic_maildir_creation_patch/
cp -f courier_patch/THANKS automatic_maildir_creation_patch/
cp -f courier_patch/README_%{courier_patch_version} automatic_maildir_creation_patch/

echo "IMAP_MAILDIR_CREATOR=\"%{courierdatadir}/auto_maildir_creator\"" >> %{buildroot}%{couriersysconfdir}/imapd.dist
echo "IMAP_MAILDIR_CREATOR=\"%{courierdatadir}/auto_maildir_creator\"" >> %{buildroot}%{couriersysconfdir}/imapd-ssl.dist
echo "POP3_MAILDIR_CREATOR=\"%{courierdatadir}/auto_maildir_creator\"" >> %{buildroot}%{couriersysconfdir}/pop3d.dist
echo "POP3_MAILDIR_CREATOR=\"%{courierdatadir}/auto_maildir_creator\"" >> %{buildroot}%{couriersysconfdir}/pop3d-ssl.dist 
echo "MOD_MAILDIR_CREATOR=\"/bin/false\"" >> %{buildroot}%{couriersysconfdir}/imapd.dist
echo "MOD_MAILDIR_CREATOR=\"/bin/false\"" >> %{buildroot}%{couriersysconfdir}/imapd-ssl.dist
echo "MOD_MAILDIR_CREATOR=\"/bin/false\"" >> %{buildroot}%{couriersysconfdir}/pop3d.dist
echo "MOD_MAILDIR_CREATOR=\"/bin/false\"" >> %{buildroot}%{couriersysconfdir}/pop3d-ssl.dist 

%post
%{courierdatadir}/sysconftool `cat %{courierdatadir}/configlist` >/dev/null
%_post_service courier-imap

%create_ghostfile %{_localstatedir}/imapd.pid root root 0600
%create_ghostfile %{_localstatedir}/imapd.pid.lock root root 0600
%create_ghostfile %{_localstatedir}/imapd-ssl.pid root root 0600
%create_ghostfile %{_localstatedir}/imapd-ssl.pid.lock root root 0600
%create_ghostfile %{_localstatedir}/authdaemon.courier-imap/lock root root 0600
%create_ghostfile %{_localstatedir}/authdaemon.courier-imap/pid	root root 0644
%create_ghostfile %{_localstatedir}/authdaemon.courier-imap/socket root root 0777

%post pop
%{courierdatadir}/sysconftool `cat %{courierdatadir}/configlist.pop` >/dev/null

%create_ghostfile %{_localstatedir}/pop3d.pid root root 0600
%create_ghostfile %{_localstatedir}/pop3d.pid.lock root root 0600
%create_ghostfile %{_localstatedir}/pop3d-ssl.pid root root 0600
%create_ghostfile %{_localstatedir}/pop3d-ssl.pid.lock root root 0600

%post ldap
%{courierdatadir}/sysconftool `cat %{courierdatadir}/configlist.ldap` >/dev/null

%post mysql
%{courierdatadir}/sysconftool `cat %{courierdatadir}/configlist.mysql` >/dev/null

%post pgsql
%{courierdatadir}/sysconftool `cat %{courierdatadir}/configlist.pgsql` >/dev/null

%preun ldap
for file in %{courierlibdir}/{imap,pop3d}{,-ssl}.rc ; do
	[ -x ${file} ] && ${file} stop
done

%preun mysql
for file in %{courierlibdir}/{imap,pop3d}{,-ssl}.rc ; do
	[ -x ${file} ] && ${file} stop
done

%preun pgsql
for file in %{courierlibdir}/{imap,pop3d}{,-ssl}.rc ; do
	[ -x ${file} ] && ${file} stop
done

%preun 
%_preun_service courier-imap

%triggerpostun -- courier-imap
test ! -f %{courierdatadir}/configlist || %{courierdatadir}/sysconftool-rpmupgrade `cat %{courierdatadir}/configlist` >/dev/null

%triggerpostun pop -- courier-imap
test ! -f %{courierdatadir}/configlist.pop || %{courierdatadir}/sysconftool-rpmupgrade `cat %{courierdatadir}/configlist.pop` >/dev/null

%triggerpostun ldap -- courier-imap
test ! -f %{courierdatadir}/configlist.ldap || %{courierdatadir}/sysconftool-rpmupgrade `cat %{courierdatadir}/configlist.ldap` >/dev/null

%triggerpostun mysql -- courier-imap
test ! -f %{courierdatadir}/configlist.mysql || %{courierdatadir}/sysconftool-rpmupgrade `cat %{courierdatadir}/configlist.mysql` >/dev/null

%clean
if [ -d %{buildroot} ]; then rm -rf %{buildroot}; fi

%files -f authdaemon.files
%defattr(-, root, root)
%doc 00README.NOW.OR.SUFFER INSTALL INSTALL.html NEWS README index.html
%doc imap/FAQ.html imap/README.html imap/courierpop3d.html imap/imapd.html imap/mkimapdcert.html imap/mkpop3dcert.html
%doc imap/BUGS imap/ChangeLog imap/FAQ imap/README.imap
%doc liblock/lockmail.html
%doc maildir/README.maildirfilter.html maildir/README.maildirquota.html maildir/README.sharedfolders.html maildir/deliverquota.html
%doc maildir/maildirquota.html maildir/README.maildirquota.txt maildir/README.sharedfolders.txt
%doc rfc2045/makemime.html rfc2045/reformime.html rfc2045/rfc2045.html rfc822/ChangeLog.rfc822 rfc822/rfc822.html
%doc tcpd/README.couriertls tcpd/couriertcpd.html tcpd/couriertls.html
%doc unicode/README.unicode
%doc userdb/makeuserdb.html userdb/userdb.html userdb/userdbpw.html automatic_maildir_creation_patch

%config(noreplace) %{_sysconfdir}/pam.d/imap
%dir %{couriersysconfdir}
%attr(600, root, root) %config(noreplace) %{couriersysconfdir}/imapd.dist
%attr(600, root, root) %config(noreplace) %{couriersysconfdir}/imapd-ssl.dist
%config(noreplace) %{couriersysconfdir}/imapd.cnf
%config(noreplace) %{couriersysconfdir}/quotawarnmsg.example
%attr(755, root, root) %config(noreplace) %{_initrddir}/courier-imap
%attr(644, root, root) %config(noreplace) %{couriersysconfdir}/authdaemonrc.dist
%dir %{courierlibdir}
%dir %{courierlibdir}/authlib

%{_bindir}/deliverquota
%{_bindir}/imapd
%{_bindir}/couriertls
%{_bindir}/maildirkw

%{_sbindir}/imaplogin
%{_sbindir}/userdbpw
%{_sbindir}/makeuserdb
%{_sbindir}/mkimapdcert
%{_sbindir}/pw2userdb
%{_sbindir}/userdb
%{_sbindir}/vchkpw2userdb

%{_mandir}/man1/couriertcpd.1*
%{_mandir}/man1/maildirkw.1*
%{_mandir}/man7/auth*.7*
%{_mandir}/man8/deliverquota.8*
%{_mandir}/man8/imapd.8*
%{_mandir}/man8/makeuserdb.8*
%{_mandir}/man8/mkimapdcert.8*
%{_mandir}/man8/mkpop3dcert.8*
%{_mandir}/man8/pw2userdb.8*
%{_mandir}/man8/user*.8*

%{courierdatadir}/pw2userdb
%{courierdatadir}/makeuserdb
%{courierdatadir}/mkimapdcert
%{courierdatadir}/vchkpw2userdb
%{courierdatadir}/userdb
%attr(755, root, root) %{courierdatadir}/auto_maildir_creator

%attr(755, root, root) %{courierdatadir}/sysconftool
%attr(755, root, root) %{courierdatadir}/sysconftool-rpmupgrade
%attr(644, root, root) %{courierdatadir}/configlist

%ghost %attr(600, root, root) %{_localstatedir}/imapd.pid
%ghost %attr(600, root, root) %{_localstatedir}/imapd-ssl.pid
%ghost %attr(600, root, root) %{_localstatedir}/imapd.pid.lock
%ghost %attr(600, root, root) %{_localstatedir}/imapd-ssl.pid.lock

%files pop
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/pam.d/pop3
%attr(600, root, root) %config(noreplace) %{couriersysconfdir}/pop3d.dist
%attr(600, root, root) %config(noreplace) %{couriersysconfdir}/pop3d-ssl.dist
%config(noreplace) %{couriersysconfdir}/pop3d.cnf
%{_bindir}/pop3d
%{_sbindir}/pop3login
%{_sbindir}/mkpop3dcert
%{courierdatadir}/mkpop3dcert
%attr(644, root, root) %{courierdatadir}/configlist.pop

%ghost %attr(600, root, root) %{_localstatedir}/pop3d.pid
%ghost %attr(600, root, root) %{_localstatedir}/pop3d-ssl.pid
%ghost %attr(600, root, root) %{_localstatedir}/pop3d.pid.lock
%ghost %attr(600, root, root) %{_localstatedir}/pop3d-ssl.pid.lock

%files ldap -f authdaemon.files.ldap
%defattr(-, root, root)
%doc authlib/README.ldap
%doc authlib/authldap.schema
%attr(644, root, root) %{courierdatadir}/configlist.ldap

%files mysql -f authdaemon.files.mysql
%defattr(-, root, root)
%doc authlib/README.authmysql.html
%doc authlib/README.authmysql.myownquery
%attr(644, root, root) %{courierdatadir}/configlist.mysql

%files pgsql -f authdaemon.files.pgsql
%defattr(-, root, root)
%doc authlib/README.authpostgres.html
%attr(644, root, root) %{courierdatadir}/configlist.pgsql

%files utils
%defattr(-, root, root)
%attr(755, root, root) %{_bindir}/courier-imap-authinfo
%attr(755, root, root) %{_bindir}/courier-imap-authtest
%attr(755, root, root) %{_bindir}/courier-imap-authdaemontest

%files -n maildirmake++
%defattr(-, root, root)
%doc maildir/maildirmake.html
%{_bindir}/maildirmake++
%{_mandir}/man1/maildirmake++.1*

%changelog
* Thu Dec 04 2003 Vincent Danen <vdanen@opensls.org> 2.1.2-2sls
- OpenSLS build
- tidy spec

* Sun Sep 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.1.2-1mdk
- 2.1.2
- fix invalid-build-requires
- fix explicit-lib-dependency
- rediffed the auto_maildir_creator patch

* Wed Aug 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.1.1-1mdk
- 2.1.1
- rediffed the auto_maildir_creator patch

* Mon Aug 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.1.0-1mdk
- 2.1.0
- rediffed the auto_maildir_creator patch
- added the new %{_bindir}/maildirkw command

* Wed Jul 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.0-1mdk
- 2.0.0
- rediffed the auto_maildir_creator patch

* Tue May 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.7.3-1mdk
- 1.7.3
- use the %%configure2_5x macro
- misc spec file fixes

* Mon Apr 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.7.1-1mdk
- 1.7.1
- added S2 & S3 from a mail from Carlo Contavalli
- feixed another way to apply the patch in S2
- misc spec file fixes

* Sun Feb 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.7.0-3mdk
- added P1 (obsoletes the requirement and should end the 
  thread about my controversial Maildir package (?))
- added S2 & S3

* Thu Feb 06 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.7.0-2mdk
- broke out the maildirmake command into a subpackage as maildirmake++
- require Maildir & maildirmake++

* Tue Jan 28 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.7.0-1mdk
- 1.7.0
- don´t ship unused files
- misc spec file fixes

* Sun Jan 26 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.6.2-2mdk
- build release

* Tue Dec 31 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.6.2-1mdk
- 1.6.2

* Mon Dec 30 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.6.1-2mdk
- make the rpm magic work (duh!)
- fix P0
- misc spec file fixes

* Mon Dec 30 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.6.1-1mdk
- new version
- fix P0
- misc spec file fixes

* Fri Oct 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.6.0-1mdk
- new version
- %{_bindir}/deliverquota was missing from package (why?)
- added %{_bindir}/courier-imap-authdaemontest to the utils sub package
- make sure you read the "REALTIME FOLDER STATUS UPDATES" section in
  the "INSTALL" file (buildrequires fam-devel).
- misc spec file fixes

* Wed Sep 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.5.3-1mdk
- new version

* Sat Aug  3 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.5.2-1mdk
- new version

* Sun Jul  7 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.5.1-1mdk
- new version

* Mon Jun 24 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.5.0-1mdk
- new version

* Sun May 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.4.6-1mdk
- new version
- build with gcc 3.1

* Mon May  6 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.4.5-1mdk
- new version
- added "--without-authvchkpw" for now

* Sun Mar 24 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.4.3-3mdk
- added the utils sub package.
- added "--disable-root-check"

* Thu Mar 21 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.4.3-2mdk
- Add --enable-workarounds-for-imap-client-bugs option (from Oden Eriksson)
- Remove make check as it won't work with option above

* Tue Mar 19 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.4.3-1mdk
- Release 1.4.3
- Fix start script to call functions file
- Clean specfile
- Move courier files in separate 
  directories (%{couriersysconf}, %{courierdatadir},  %{courierlibdir})
- Remove profiles.d scripts, they are not useful at all
- Remove some conflicts in -pop package, they prevent installing the package...

* Thu Jan 24 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 1.4.2-1mdk
- 1.4.2
- Make rpmlint a little happier by creating the ghost files in postins
  and by trimming the length of the lines in the description

* Thu Nov 29 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 1.3.12.20011123-3md
- Make it really conflict with uw-imap
- Just like uw-imap, have it also Provides: imap-server
- Split POP stuff into a -pop subpackage, which Provides: pop, pop-server
- Add the warning shown when installing the RPM also to the description
- FIXME: There are still some problems with the maildrop-man package; maybe a full
  blown courier package containg the IMAP server, maildrop and SqWebMail should be
  done to fix this

* Wed Nov 28 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 1.3.12.20011123-2mdk
- Make it conflict with imap (uw-imapd).  Todo: also have it conflict with cyrus
- Add a Provides: imap, so that other packages like php-imap can still be installed
  Hmm, this won't work.  uw-imapd needs to be renamed!
- Fix perms of %{datadir}/sysconftool
- Enable all unicode character sets
- Include pam files
- Make sure, that all (?) needed files are included
- Add a big, fat warning during post that ~/Maildir needs to be present for courier
  to work

* Tue Nov 27 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 1.3.12.20011123-1mdk
- Basically rewrote the complete SPEC
- New release

* Sun Jan 28 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.3.2-1mdk
- first Mandrake build
