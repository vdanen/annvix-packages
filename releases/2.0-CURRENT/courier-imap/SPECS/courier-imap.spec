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
%define version		3.0.8
%define release		%_revrel

%define _localstatedir	/var/run
%define	authdaemondir	%{_localstatedir}/authdaemon.courier-imap
%define	courierdatadir	%{_datadir}/courier
%define	courierlibdir	%{_libdir}/courier
%define	couriersysconfdir %{_sysconfdir}/courier

%define	courier_patch_version 0.42.2

Summary:	Courier-IMAP is an IMAP server that uses Maildirs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.courier-mta.org
Source0:	%{name}-%{version}.tar.bz2
Source1:	courier-imap-sysconftool-rpmupgrade
# S4 & S5  originates from the works of Carlo Contavalli and can be found here:
# http://www.commedia.it/ccontavalli/
Source2:	courier_patch.tar.gz
Source3:	courier_patch.tar.gz.asc
Source4:	auto_maildir_creator
Source5:	courier-imapd.run
Source6:	courier-imapd-log.run
Source7:	courier-imapds.run
Source8:	courier-imapds-log.run
Source9:	courier-pop3d.run
Source10:	courier-pop3d-log.run
Source11:	courier-pop3ds.run
Source12:	courier-pop3ds-log.run
Source13:	courier-imap.sysconfig
Source14:	authdaemond.run
Source15:	authdaemond-log.run
Source16:	09_courier-imap.afterboot
Source17:	courier.pam
# (fc) 1.4.2-2mdk fix missing command in initrd
Patch0: 	courier-imap-1.6.1-initrd.patch
Patch1:		courier-imap-3.0.8-auto_maildir_creator.diff
Patch2:		courier-imap-2.1.1-configure.patch
Patch3:		courier-imap-2.1.2-authnodaemon.patch
Patch4:		courier-imap-3.0.8-overflow.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	gdbm-devel
BuildRequires:	openldap-devel
BuildRequires:	mysql-devel 
BuildRequires:	postgresql-devel

Requires:	gdbm
Requires:	ipsvd
Requires(post):	afterboot
Requires(post):	rpm-helper
Requires(postun): afterboot
Requires(preun): rpm-helper
Conflicts:	uw-imap
Conflicts:	bincimap
Provides:	imap
Provides:	imap-server

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
Requires:	ipsvd
Requires(post):	rpm-helper
Requires(post):	%{name}
Requires(preun): rpm-helper
Provides:	pop
Provides:	pop-server
Conflicts:	uw-imap-pop

%description pop
This package contains the POP servers of the Courier-IMAP
server suite.


%package ldap
Summary:	Courier-IMAP LDAP authentication driver
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
#Requires:	libldap2
Requires(post):	rpm-helper
Requires(post):	%{name}
Requires(postun): rpm-helper
Conflicts:	%{name}-mysql
Conflicts:	%{name}-pgsql

%description ldap
This package contains the necessary files to allow Courier-IMAP to
authenticate from an LDAP directory.  Install this package if you need the
ability to use an LDAP directory for authentication.


%package mysql
Summary:	Courier-IMAP MySQL authentication driver
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
Requires:	mysql
Requires(post):	rpm-helper
Requires(post):	%{name}
Requires(postun): rpm-helper
Conflicts:	%{name}-ldap
Conflicts:	%{name}-pgsql

%description mysql
This package contains the necessary files to allow Courier-IMAP to
authenticate using a MySQL database table.  Install this package if you need
the ability to use a MySQL database table for authentication.


%package pgsql
Summary:	Courier-IMAP PostgreSQL authentication driver
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
Requires:	postgresql-libs
Requires(post):	rpm-helper
Requires(post):	%{name}
Requires(postun): rpm-helper
Conflicts:	%{name}-ldap
Conflicts:	%{name}-mysql

%description pgsql
This package contains the necessary files to allow Courier-IMAP to
authenticate using a PostgreSQL database table.  Install this package if you
need the ability to use a PostgreSQL database table for authentication.


%package utils
Summary:	Courier-IMAP debugging utils
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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a2
%patch0 -p0 -b .initrd
%patch1 -p1 -b .auto_maildir_creator
%ifarch amd64 x86_64
%patch2 -p0 -b .config
%endif
#%patch3 -p1 -b .nodaemon
%patch4 -p1 -b .overflow

# doc handling
mkdir automatic_maildir_creation_patch
cp -f courier_patch/html/*.html automatic_maildir_creation_patch/
cp -f courier_patch/README.txt automatic_maildir_creation_patch/
cp -f courier_patch/THANKS automatic_maildir_creation_patch/
cp -f courier_patch/README_%{courier_patch_version} automatic_maildir_creation_patch/

%build
#(cd authlib; autoreconf)
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
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/pam.d

%makeinstall_std

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
cp %{_sourcedir}/courier-imap-sysconftool-rpmupgrade %{buildroot}%{courierdatadir}/sysconftool-rpmupgrade

# Check if authdaemond was installed, make sure to include authdaemon
# directory
touch authdaemon.files

. authlib/authdaemonrc

if [ "x$authdaemonvar" != "x" ]; then
    echo "%{couriersysconfdir}/authdaemonrc.dist" >> %{buildroot}%{courierdatadir}/configlist
    echo '%dir %attr(700, root, root) ' $authdaemonvar >  authdaemon.files
    touch %{buildroot}/${authdaemonvar}/lock || exit 1
    touch %{buildroot}/${authdaemonvar}/pid || exit 1
    # authmksock can't deal with paths longer than 108 chars
    foo=$(pwd)
    pushd %{buildroot}/${authdaemonvar}
        $foo/authlib/authmksock socket || exit 1
    popd
    echo '%ghost %attr(600, root, root) ' ${authdaemonvar}/lock >> authdaemon.files
    echo '%ghost %attr(644, root, root) ' ${authdaemonvar}/pid >> authdaemon.files
    echo '%ghost %attr(777, root, root) ' ${authdaemonvar}/socket >> authdaemon.files
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

find %{buildroot} -type f -print | sed "s@^%{buildroot}@@g" | grep -v perllocal.pod > %{_builddir}/tmp-filelist

# some utils...
install -m 0755 authlib/authinfo %{buildroot}%{_bindir}/courier-imap-authinfo
install -m 0755 authlib/authtest %{buildroot}%{_bindir}/courier-imap-authtest
install -m 0755 authlib/authdaemontest %{buildroot}%{_bindir}/courier-imap-authdaemontest

# fix the maildirmake command so it won't conflict with vdanens qmail package?
mv %{buildroot}%{_bindir}/maildirmake %{buildroot}%{_bindir}/maildirmake++
mv %{buildroot}%{_mandir}/man1/maildirmake.1 %{buildroot}%{_mandir}/man1/maildirmake++.1

# fix the auto maildir creation stuff
cp %{_sourcedir}/auto_maildir_creator %{buildroot}%{courierdatadir}/auto_maildir_creator
chmod 0755 %{buildroot}%{courierdatadir}/auto_maildir_creator
chmod -R 0644 %{buildroot}%{courierdatadir}/auto_maildir_creator

echo "IMAP_MAILDIR_CREATOR=\"%{courierdatadir}/auto_maildir_creator\"" >> %{buildroot}%{couriersysconfdir}/imapd.dist
echo "IMAP_MAILDIR_CREATOR=\"%{courierdatadir}/auto_maildir_creator\"" >> %{buildroot}%{couriersysconfdir}/imapd-ssl.dist
echo "POP3_MAILDIR_CREATOR=\"%{courierdatadir}/auto_maildir_creator\"" >> %{buildroot}%{couriersysconfdir}/pop3d.dist
echo "POP3_MAILDIR_CREATOR=\"%{courierdatadir}/auto_maildir_creator\"" >> %{buildroot}%{couriersysconfdir}/pop3d-ssl.dist 
echo "MOD_MAILDIR_CREATOR=\"/bin/false\"" >> %{buildroot}%{couriersysconfdir}/imapd.dist
echo "MOD_MAILDIR_CREATOR=\"/bin/false\"" >> %{buildroot}%{couriersysconfdir}/imapd-ssl.dist
echo "MOD_MAILDIR_CREATOR=\"/bin/false\"" >> %{buildroot}%{couriersysconfdir}/pop3d.dist
echo "MOD_MAILDIR_CREATOR=\"/bin/false\"" >> %{buildroot}%{couriersysconfdir}/pop3d-ssl.dist 

mkdir -p %{buildroot}%{_srvdir}/{courier-imapd,courier-imapds,courier-pop3d,courier-pop3ds,authdaemond}/log
mkdir -p %{buildroot}%{_srvdir}/{courier-imapd,courier-imapds,courier-pop3d,courier-pop3ds}/peers
install -m 0740 %{_sourcedir}/courier-imapd.run %{buildroot}%{_srvdir}/courier-imapd/run
install -m 0740 %{_sourcedir}/courier-imapd-log.run %{buildroot}%{_srvdir}/courier-imapd/log/run
install -m 0740 %{_sourcedir}/courier-imapds.run %{buildroot}%{_srvdir}/courier-imapds/run
install -m 0740 %{_sourcedir}/courier-imapds-log.run %{buildroot}%{_srvdir}/courier-imapds/log/run
install -m 0740 %{_sourcedir}/courier-pop3d.run %{buildroot}%{_srvdir}/courier-pop3d/run
install -m 0740 %{_sourcedir}/courier-pop3d-log.run %{buildroot}%{_srvdir}/courier-pop3d/log/run
install -m 0740 %{_sourcedir}/courier-pop3ds.run %{buildroot}%{_srvdir}/courier-pop3ds/run
install -m 0740 %{_sourcedir}/courier-pop3ds-log.run %{buildroot}%{_srvdir}/courier-pop3ds/log/run
install -m 0740 %{_sourcedir}/authdaemond.run %{buildroot}%{_srvdir}/authdaemond/run
install -m 0740 %{_sourcedir}/authdaemond-log.run %{buildroot}%{_srvdir}/authdaemond/log/run

touch %{buildroot}%{_srvdir}/{courier-imapd,courier-imapds,courier-pop3d,courier-pop3ds}/peers/0
chmod 0640  %{buildroot}%{_srvdir}/{courier-imapd,courier-imapds,courier-pop3d,courier-pop3ds}/peers/0

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/09_courier-imap.afterboot %{buildroot}%{_datadir}/afterboot/09_courier-imap

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 %{_sourcedir}/courier-imap.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/imapd
install -m 0644 %{_sourcedir}/courier-imap.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/imapd-ssl
install -m 0644 %{_sourcedir}/courier-imap.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/pop3d
install -m 0644 %{_sourcedir}/courier-imap.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/pop3d-ssl

# fix location of authlib stuff on x86_64
%ifarch x86_64 amd64
find %{buildroot}%{_srvdir} -name run -exec perl -pi -e 's|/usr/lib/courier|/usr/lib64/courier|g' {} \;
%endif

# fix pam
cp -f %{_sourcedir}/courier.pam %{buildroot}%{_sysconfdir}/pam.d/imap
cp -f %{_sourcedir}/courier.pam %{buildroot}%{_sysconfdir}/pam.d/pop3
chmod 0644 %{buildroot}%{_sysconfdir}/pam.d/*


%post
%{courierdatadir}/sysconftool `cat %{courierdatadir}/configlist` >/dev/null
%_post_srv courier-imapd
%_post_srv courier-imapds
%_post_srv authdaemond
%_mkafterboot
for i in courier-imapd courier-imapds
do
    pushd %{_srvdir}/$i >/dev/null 2>&1
        ipsvd-cdb peers.cdb peers.cdb.tmp peers/
    popd >/dev/null 2>&1
done

%create_ghostfile %{_localstatedir}/imapd.pid root root 0600
%create_ghostfile %{_localstatedir}/imapd.pid.lock root root 0600
%create_ghostfile %{_localstatedir}/imapd-ssl.pid root root 0600
%create_ghostfile %{_localstatedir}/imapd-ssl.pid.lock root root 0600
%create_ghostfile %{_localstatedir}/authdaemon.courier-imap/lock root root 0600
%create_ghostfile %{_localstatedir}/authdaemon.courier-imap/pid	root root 0644
%create_ghostfile %{_localstatedir}/authdaemon.courier-imap/socket root root 0777


%post pop
%{courierdatadir}/sysconftool `cat %{courierdatadir}/configlist.pop` >/dev/null
%_post_srv courier-pop3d
%_post_srv courier-pop3ds
for i in courier-pop3d courier-pop3ds
do
    pushd %{_srvdir}/$i >/dev/null 2>&1
        ipsvd-cdb peers.cdb peers.cdb.tmp peers/
    popd >/dev/null 2>&1
done

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


%postun
%_mkafterboot


%postun ldap
%_preun_srv courier-imapd
%_preun_srv courier-imapds
%_preun_srv courier-pop3d
%_preun_srv courier-pop3ds
%_preun_srv authdaemond


%postun mysql
%_preun_srv courier-imapd
%_preun_srv courier-imapds
%_preun_srv courier-pop3d
%_preun_srv courier-pop3ds
%_preun_srv authdaemond


%postun pgsql
%_preun_srv courier-imapd
%_preun_srv courier-imapds
%_preun_srv courier-pop3d
%_preun_srv courier-pop3ds
%_preun_srv authdaemond


%preun 
%_preun_srv courier-imapd
%_preun_srv courier-imapds
%_preun_srv authdaemond


%preun pop
%_preun_srv courier-pop3d
%_preun_srv courier-pop3ds


%triggerpostun -- courier-imap
test ! -f %{courierdatadir}/configlist || %{courierdatadir}/sysconftool-rpmupgrade `cat %{courierdatadir}/configlist` >/dev/null


%triggerpostun pop -- courier-imap
test ! -f %{courierdatadir}/configlist.pop || %{courierdatadir}/sysconftool-rpmupgrade `cat %{courierdatadir}/configlist.pop` >/dev/null


%triggerpostun ldap -- courier-imap
test ! -f %{courierdatadir}/configlist.ldap || %{courierdatadir}/sysconftool-rpmupgrade `cat %{courierdatadir}/configlist.ldap` >/dev/null


%triggerpostun mysql -- courier-imap
test ! -f %{courierdatadir}/configlist.mysql || %{courierdatadir}/sysconftool-rpmupgrade `cat %{courierdatadir}/configlist.mysql` >/dev/null


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f authdaemon.files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/imap
%dir %{couriersysconfdir}
%attr(0600,root,root) %config(noreplace) %{couriersysconfdir}/imapd.dist
%attr(0600,root,root) %config(noreplace) %{couriersysconfdir}/imapd-ssl.dist
%config(noreplace) %{couriersysconfdir}/imapd.cnf
%config(noreplace) %{couriersysconfdir}/quotawarnmsg.example
%attr(0644,root,root) %config(noreplace) %{couriersysconfdir}/authdaemonrc.dist
%dir %{courierlibdir}
%dir %{courierlibdir}/authlib

%{_bindir}/deliverquota
%{_bindir}/imapd
%{_bindir}/couriertls
%{_bindir}/maildirkw
%{_bindir}/maildiracl

%{_sbindir}/imaplogin
%{_sbindir}/userdbpw
%{_sbindir}/makeuserdb
%{_sbindir}/mkimapdcert
%{_sbindir}/pw2userdb
%{_sbindir}/userdb
%{_sbindir}/vchkpw2userdb
%{_sbindir}/authenumerate
%{_sbindir}/courierlogger
%{_sbindir}/sharedindexinstall
%{_sbindir}/sharedindexsplit

%{_mandir}/man1/couriertcpd.1*
%{_mandir}/man1/courierlogger.1*
%{_mandir}/man1/maildiracl.1*
%{_mandir}/man1/maildirkw.1*
%{_mandir}/man7/auth*.7*
%{_mandir}/man8/deliverquota.8*
%{_mandir}/man8/imapd.8*
%{_mandir}/man8/makeuserdb.8*
%{_mandir}/man8/mkimapdcert.8*
%{_mandir}/man8/mkpop3dcert.8*
%{_mandir}/man8/pw2userdb.8*
%{_mandir}/man8/user*.8*
%{_mandir}/man8/vchkpw2userdb.8*

%{courierdatadir}/pw2userdb
%{courierdatadir}/makeuserdb
%{courierdatadir}/mkimapdcert
%{courierdatadir}/vchkpw2userdb
%{courierdatadir}/userdb
%attr(0755,root,root) %{courierdatadir}/auto_maildir_creator

%attr(0755,root,root) %{courierdatadir}/sysconftool
%attr(0755,root,root) %{courierdatadir}/sysconftool-rpmupgrade
%attr(0644,root,root) %{courierdatadir}/configlist

%ghost %attr(0600,root,root) %{_localstatedir}/imapd.pid
%ghost %attr(0600,root,root) %{_localstatedir}/imapd-ssl.pid
%ghost %attr(0600,root,root) %{_localstatedir}/imapd.pid.lock
%ghost %attr(0600,root,root) %{_localstatedir}/imapd-ssl.pid.lock

%dir %attr(0750,root,admin) %{_srvdir}/courier-imapd
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapd/log
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapd/peers
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-imapd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-imapd/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapd/peers/0
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapds
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapds/log
%dir %attr(0750,root,admin) %{_srvdir}/courier-imapds/peers
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-imapds/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-imapds/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-imapds/peers/0
%config(noreplace) %{_sysconfdir}/sysconfig/imapd
%config(noreplace) %{_sysconfdir}/sysconfig/imapd-ssl
%dir %attr(0750,root,admin) %{_srvdir}/authdaemond
%dir %attr(0750,root,admin) %{_srvdir}/authdaemond/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/authdaemond/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/authdaemond/log/run
%{_datadir}/afterboot/09_courier-imap


%files pop
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/pam.d/pop3
%attr(0600,root,root) %config(noreplace) %{couriersysconfdir}/pop3d.dist
%attr(0600,root,root) %config(noreplace) %{couriersysconfdir}/pop3d-ssl.dist
%config(noreplace) %{couriersysconfdir}/pop3d.cnf
%{_bindir}/pop3d
%{_sbindir}/pop3login
%{_sbindir}/mkpop3dcert
%{courierdatadir}/mkpop3dcert
%attr(0644,root,root) %{courierdatadir}/configlist.pop

%ghost %attr(0600,root,root) %{_localstatedir}/pop3d.pid
%ghost %attr(0600,root,root) %{_localstatedir}/pop3d-ssl.pid
%ghost %attr(0600,root,root) %{_localstatedir}/pop3d.pid.lock
%ghost %attr(0600,root,root) %{_localstatedir}/pop3d-ssl.pid.lock

%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3d
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3d/log
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3d/peers
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-pop3d/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-pop3d/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3d/peers/0
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3ds
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3ds/log
%dir %attr(0750,root,admin) %{_srvdir}/courier-pop3ds/peers
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-pop3ds/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/courier-pop3ds/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/courier-pop3ds/peers/0
%config(noreplace) %{_sysconfdir}/sysconfig/pop3d
%config(noreplace) %{_sysconfdir}/sysconfig/pop3d-ssl


%files ldap -f authdaemon.files.ldap
%defattr(-,root,root)
%attr(0644,root,root) %{courierdatadir}/configlist.ldap


%files mysql -f authdaemon.files.mysql
%defattr(-,root,root)
%attr(0644,root,root) %{courierdatadir}/configlist.mysql


%files pgsql -f authdaemon.files.pgsql
%defattr(-,root,root)
%attr(0644,root,root) %{courierdatadir}/configlist.pgsql


%files utils
%defattr(0755,root,root)
%{_bindir}/courier-imap-authinfo
%{_bindir}/courier-imap-authtest
%{_bindir}/courier-imap-authdaemontest


%files -n maildirmake++
%defattr(-, root, root)
%{_bindir}/maildirmake++
%{_mandir}/man1/maildirmake++.1*

%files doc
%defattr(-,root,root)
%doc 00README.NOW.OR.SUFFER INSTALL INSTALL.html NEWS README
%doc imap/README.html imap/courierpop3d.html imap/imapd.html imap/mkimapdcert.html imap/mkpop3dcert.html
%doc imap/BUGS imap/ChangeLog imap/README.imap
%doc liblock/lockmail.html
%doc maildir/README.maildirfilter.html maildir/README.maildirquota.html maildir/README.sharedfolders.html maildir/deliverquota.html
%doc maildir/maildirquota.html maildir/README.maildirquota.txt maildir/README.sharedfolders.txt
%doc rfc2045/makemime.html rfc2045/reformime.html rfc2045/rfc2045.html rfc822/ChangeLog.rfc822 rfc822/rfc822.html
%doc tcpd/README.couriertls tcpd/couriertcpd.html tcpd/couriertls.html
%doc unicode/README.unicode
%doc userdb/makeuserdb.html userdb/userdb.html userdb/userdbpw.html automatic_maildir_creation_patch
%doc authlib/README.ldap
%doc authlib/authldap.schema
%doc authlib/README.authmysql.html
%doc authlib/README.authmysql.myownquery
%doc authlib/README.authpostgres.html
%doc maildir/maildirmake.html


%changelog
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
