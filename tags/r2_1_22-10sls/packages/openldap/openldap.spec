%define name	openldap
%define version	2.1.22
%define release	10sls

%define major 		2
%define migtools_ver	40
%define fname		ldap
%define libname		%mklibname %fname %major

#localstatedir is passed directly to configure, and we want it to be /var/lib
#define _localstatedir	%{_var}/run
%define	_libexecdir	%{_sbindir}

# Allow --with[out] SASL at rpm command line build
%{?_without_SASL: %{expand: %%define _without_cyrussasl --without-cyrus-sasl}}
%{?_with_SASL: %{expand: %%define _with_cyrussasl --with-cyrus-sasl}}
%{!?_with_cyrussasl: %{!?_without_cyrussasl: %define _with_cyrussasl --with-cyrus-sasl}}
%{?_with_cyrussasl: %define _with_cyrussasl --with-cyrus-sasl}
%{?_without_cyrussasl: %define _without_cyrussasl --without-cyrus-sasl}
%{?_with_gdbm: %global db_conv dbb}
%{!?_with_gdbm: %global db_conv gdbm}
%global sql 1
%{?_without_sql: %global sql 0}

Summary: 	LDAP servers and sample clients.
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	Artistic
Group: 		System/Servers
URL: 		http://www.openldap.org
# Openldap source
Source0: 	%{name}-%{version}.tar.bz2
# Specific source
Source1: 	ldap.init
Source2: 	%{name}.sysconfig
Source19:	gencert.sh
Source20:	ldap.logrotate
Source21:	slapd.conf
Source22:	slapd.run
Source23:	slapd-log.run
Source24:	slurpd.run
Source25:	slurpd-log.run
# Migration tools
Source11:	http://www.padl.com/download/MigrationTools-%{migtools_ver}.tar.bz2
Source3: 	migration-tools.txt
Source4: 	migrate_automount.pl
# Extended Schema 
Source50: 	rfc822-MailMember.schema
Source51: 	autofs.schema
Source52: 	kerberosobject.schema
Source53: 	qmail.schema
Source54: 	mull.schema
Source55: 	samba.schema
Source56: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/netscape-profile.schema
Source57: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/trust.schema
Source58: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/dns.schema
Source59: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/cron.schema
Source60:	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/qmailControl.schema
Source61:	krb5-kdc.schema
# Chris Patches
Patch0: 	%{name}-2.0.7-config.patch.bz2
Patch1:		%{name}-2.0.7-module.patch.bz2
Patch2:		%{name}-2.0.7-schema.patch.bz2
Patch3: 	%{name}-2.0.9-slapd.conf.patch.bz2
Patch4: 	%{name}-2.0.7-db3.patch.bz2
Patch22:	%{name}-libtool.patch.bz2
Patch24:	%{name}-2.0.18-libtool.patch.bz2
Patch25:	%{name}-2.0.25-liblber.patch.bz2
# RH + PLD Patches
Patch6: 	%{name}-2.0.3-krb5-1.1.patch.bz2
Patch8:		%{name}-conffile.patch.bz2
Patch10:	%{name}-sql.patch.bz2
Patch12:	%{name}-syslog.patch.bz2
Patch15:	%{name}-cldap.patch.bz2
# Migration tools Patch
Patch40: 	MigrationTools-34-instdir.patch.bz2
Patch41: 	MigrationTools-36-mktemp.patch.bz2
Patch42: 	MigrationTools-27-simple.patch.bz2
Patch43: 	MigrationTools-26-suffix.patch.bz2
Patch44: 	MigrationTools-24-schema.patch.bz2
Patch45:	MigrationTools-38-i18n.patch.bz2
# schema patch
Patch46: 	openldap-2.0.21-schema.patch.bz2
# maildrop schema
Patch47:	openldap-2.0.27-maildrop.schema.patch.bz2
# md5 hash fix patch
Patch48:	openldap-2.0.27-slapd-Makefile.patch.bz2
Patch49:	openldap-2.1.22-libtool.patch.bz2

BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
%{?_with_cyrussasl:BuildRequires: 	libsasl-devel}
%{?_with_kerberos:BuildRequires:	krb5-devel}
BuildRequires:	openssl-devel, perl, autoconf
#BuildRequires: libgdbm1-devel
%if %sql
BuildRequires: 	libunixODBC-devel
%endif
BuildRequires: 	db4-devel >= 4.1.25, libtool-devel
BuildRequires:  ncurses-devel >= 5.0, tcp_wrappers-devel

Requires: 	%libname = %{version}-%{release}
Requires:	shadow-utils, setup >= 2.2.0-6mdk


%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools.  The suite includes a
stand-alone LDAP server (slapd), a stand-alone LDAP replication server
(slurpd), libraries for implementing the LDAP protocol, and utilities,
tools, and sample clients.
Install openldap if you need LDAP applications and tools.

%package servers
Summary: 	OpenLDAP servers and related files.
Group: 		System/Servers
Prereq: 	fileutils,  /usr/sbin/useradd
PreReq:		rpm-helper
Requires: 	%libname = %{version}-%{release}

%description servers
OpenLDAP Servers

This server package was compiled with support for the %{?_with_gdbm:gdbm}%{!?_with_gdbm:berkeley}
database backend.

%package clients
Summary: 	OpenLDAP clients and related files.
Group: 		System/Servers
Requires: 	%libname = %{version}-%{release}

%description clients
OpenLDAP clients

%package migration
Summary: 	Set of scripts for migration of a nis domain to a ldap annuary.
Group: 		System/Configuration/Other
Requires: 	openldap-servers = %{version}-%{release}
Requires: 	openldap-clients = %{version}-%{release}
Requires: 	perl-MIME-Base64

%description migration
Set of scripts for migration of a nis domain to a ldap annuary.

%package -n %libname
Summary: 	OpenLDAP libraries.
Group: 		System/Libraries
Provides:       lib%fname = %version-%release

%description -n %libname
This package includes thelibraries needed for make works ldap applications.


%package -n %libname-devel
Summary: 	OpenLDAP development libraries and header files.
Group: 		Development/C
Provides: 	lib%fname-devel = %version-%release
Provides:       openldap-devel
Requires: 	%libname = %{version}-%release
Obsoletes: 	openldap-devel
Conflicts:	libldap1-devel

%description -n %libname-devel
This package includes the development libraries and header files
needed for compiling applications that use LDAP internals.  Install
this package only if you plan to develop or will need to compile
customized LDAP clients.


%package -n %libname-devel-static
Summary: 	OpenLDAP development static libraries
Group: 		Development/C
Provides: 	lib%fname-devel-static = %version-%release
provides:	openldap-devel-static
Requires: 	%libname-devel = %{version}-%release
Obsoletes: 	openldap-devel-static
Conflicts:	libldap1-devel


%description -n %libname-devel-static
OpenLDAP development static libraries


%package back_dnssrv
Summary: 	Module dnssrv for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%{release}
Requires: 	openldap-servers = %{version}-%{release}

%description back_dnssrv
Module dnssrv for OpenLDAP daemon


%package back_ldap
Summary: 	Module ldap for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%{release}
Requires: 	openldap-servers = %{version}-%{release}

%description back_ldap
Module ldap for OpenLDAP daemon


%package back_passwd
Summary: 	Module passwd for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%release
Requires: 	openldap-servers = %{version}-%release

%description back_passwd
Module passwd for OpenLDAP daemon

%if %sql
%package back_sql
Summary: 	Module sql for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%{release}
Requires: 	openldap-servers = %{version}-%{release}

%description back_sql
Module sql for OpenLDAP daemon
%endif


%prep
%setup -q -a 11

# Chris patches
#bgmilne %patch0 -p1 -b .config
%patch1 -p1 -b .module
#bgmilne %patch2 -p1 -b .schema
#%patch3 -p1 
#%patch4 -p1 
#bgmilne %patch24 -p1 -b .libtool
#bgmilne %patch25 -p1 -b .liblber

# RH patches
#%patch6 -p1 
%patch8 -p1 -b .conffile
#bgmilne %patch10 -p1 -b .sql
#bgmilne %patch12 -p1 -b .syslog
%patch15 -p1 -b .cldap 

pushd MigrationTools-%{migtools_ver}
%patch40 -p1 -b .instdir
%patch41 -p1 -b .mktemp
%patch42 -p1 -b .simple
%patch43 -p1 -b .suffix
%patch44 -p2 -b .schema
%patch45 -p2 -b .i18n
popd

%patch46 -p1 -b .mdk
#bgmilne %patch47 -p1 -b .maildropschema
#bgmilne %patch48 -p1 -b .md5
%patch49 -p1 -b .libtool
autoconf
# FIXME: copy from automake dir
cp -p contrib/ldapc++/install-sh build/

%build
%serverbuild

#
# dont't run libtoolize because openldap use custom libtool 1.3
%define __libtoolize  /bin/true

#if %{build_sasl}
#WITH_CYRUS_SASL="--with-cyrus-sasl --enable-spasswd"
#else
#WITH_CYRUS_SASL="--without-cyrus-sasl"
#endif

%configure2_5x \
	--localstatedir=/var/run/ldap \
	--enable-syslog \
	--enable-proctitle \
	--enable-cache \
	--enable-referrals \
	--enable-ipv6 \
	--enable-local \
	%{?_with_cyrussasl} %{?_without_cyrussasl} \
	%{?_with_kerberos} %{?_without_kerberos} \
	--with-readline \
	--with-threads \
	--with-tls \
	--with-yielding-select \
	--enable-slapd \
	--enable-cleartext \
	--enable-crypt \
	%{?_with_kerberos:--enable-kpasswd} \
	%{?_with_cyrussasl:--enable-spasswd} \
	--enable-modules \
	--enable-phonetic \
	--enable-rlookups \
	--enable-aci \
	--enable-wrappers \
	--enable-dynamic \
	--enable-dnssrv \
	--with-dnssrv-module=dynamic \
	--enable-ldap \
	--with-ldap-module=dynamic \
	--enable-ldbm \
	--with-ldbm-api=%{?_with_gdbm:gdbm}%{!?_with_gdbm:berkeley}  \
	--with-ldbm-module=static \
	--enable-passwd \
	--with-passwd-module=dynamic \
	--enable-shell \
	--with-shell-module=static \
%if %sql
	--enable-sql \
	--with-sql-module=dynamic \
%endif
	--enable-slurpd \
	--enable-static \
	--enable-shared

# These options are no longer available
#	--enable-cldap \
#	--enable-multimaster \

#configure --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin \
#	--sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share \
#	--includedir=/usr/include --libdir=/usr/lib --libexecdir=/usr/sbin \
#	--localstatedir=/var/run --sharedstatedir=/usr/com \
#	--mandir=/usr/share/man --infodir=/usr/share/info \
#   --with-ldbm-api=gdbm \
#	--with-ldbm-api=berkeley \
#	--with-ldbm-type=%{?ldbm_type:%{ldbm_type}}%{?!ldbm_type:btree} \

#patch -p1 < %{PATCH22}

%make depend 

%make 

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


#	sysconfdir=%{_sysconfdir}/openldap \
#	datadir=%{buildroot}/%{_datadir}/openldap 
#
### install slapcat-gdbm
#install -m 755 slapcat-gdbm %{buildroot}%{_sbindir}


### some hack
#perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_sysconfdir}/openldap/slapd.conf
#perl -pi -e "s|^#! /bin/sh|#!/bin/sh|g" %{buildroot}%{_bindir}/xrpcomp 
perl -pi -e "s| -L../liblber/.libs||g" %{buildroot}%{_libdir}/libldap.la

mkdir -p %{buildroot}%{_srvdir}/{slapd,slurpd}/log
mkdir -p %{buildroot}%{_srvlogdir}/{slapd,slurpd}
install -m 0755 %{SOURCE22} %{buildroot}%{_srvdir}/slapd/run
install -m 0755 %{SOURCE23} %{buildroot}%{_srvdir}/slapd/log/run
install -m 0755 %{SOURCE24} %{buildroot}%{_srvdir}/slurpd/run
install -m 0755 %{SOURCE25} %{buildroot}%{_srvdir}/slurpd/log/run

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/ldap

install -m 755 %{SOURCE21} %{buildroot}%{_sysconfdir}/openldap

### repository dir
install -d %{buildroot}%{_localstatedir}/ldap

### run dir
install -d %{buildroot}%{_var}/run/ldap

### Server defaults
echo "localhost" > %{buildroot}%{_sysconfdir}/openldap/ldapserver

### we don't need the default files 
rm -f %{buildroot}/etc/openldap/*.default 
rm -f %{buildroot}/etc/openldap/schema/*.default 


### Standard schemas should not be changed by users
install -d %{buildroot}%{_datadir}/openldap/schema
mv -f %{buildroot}%{_sysconfdir}/openldap/schema/* %{buildroot}%{_datadir}/openldap/schema/

### install additional schemas
for i in %{SOURCE50} %{SOURCE51} %{SOURCE52} %{SOURCE53} %{SOURCE54} \
	%{SOURCE55} %{SOURCE56} %{SOURCE57} %{SOURCE58} %{SOURCE59} \
	%{SOURCE60} %{SOURCE61}; do
install -m 644 $i %{buildroot}%{_datadir}/openldap/schema/
done

### create local.schema
echo "# This is a good place to put your schema definitions " > %{buildroot}%{_sysconfdir}/openldap/schema/local.schema
chmod 644 %{buildroot}%{_sysconfdir}/openldap/schema/local.schema

### create slapd.access.conf
echo "# This is a good place to put slapd access-control directives" > %{buildroot}%{_sysconfdir}/openldap/slapd.access.conf

### try to build saucer, but don't fret if we can't
if make -C contrib/saucer ; then
	install -m755 contrib/saucer/saucer %{buildroot}%{_bindir}/
	install -m644 contrib/saucer/saucer.1 %{buildroot}%{_mandir}/man1/
fi

### deal with the migration tools
install -d %{buildroot}%{_datadir}/openldap/migration
install -m 755 MigrationTools-%{migtools_ver}/{*.pl,*.sh,*.txt,*.ph} %{buildroot}%{_datadir}/openldap/migration
install -m 644 MigrationTools-%{migtools_ver}/README %{SOURCE3} %{buildroot}%{_datadir}/openldap/migration
install -m 755 %{SOURCE4} %{buildroot}%{_datadir}/openldap/migration

cp MigrationTools-%{migtools_ver}/README README.migration
cp %{SOURCE3} TOOLS.migration


### gencert.sh
install -m 755 %{SOURCE19} %{buildroot}/%{_datadir}/openldap

### log repository
install -m 700 -d %{buildroot}/var/log/ldap
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE20} %{buildroot}%{_sysconfdir}/logrotate.d/ldap


# get the buildroot out of the man pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

# if ldapadd and ldapmodify are the same, make them a hard link
if cmp %{buildroot}%{_bindir}/ldapadd %{buildroot}%{_bindir}/ldapmodify ; then
	ln -f %{buildroot}%{_bindir}/ldapadd %{buildroot}%{_bindir}/ldapmodify
fi

mkdir -p %{buildroot}%{_sysconfdir}/ssl/openldap


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre servers
%_pre_useradd ldap %{_localstatedir}/ldap /bin/false 76
# allowing slapd to read hosts.allow and hosts.deny
%{_bindir}/gpasswd -a ldap adm 1>&2 > /dev/null || :

# bgmilne: Fix dbb->gdbm stuffup:
#echo "Checking for incompatible db types"
if [ -n "`find %{_localstatedir}/ldap/*.%{db_conv} 2>&-`" ]
then
	echo "Found incompatible db type %{db_conv}"
	echo "Making a backup to ldif file %{_localstatedir}/ldap/rpm-db-backup-%{db_conv}.ldif"
	# For some reason, slapcat works in the shell when slapd is running
	# but not via rpm ...
	SLAPD_STATUS=`srv status slapd|grep -q -v up;echo $?`
	[ $SLAPD_STATUS -eq 1 ] && srv stop slapd
	slapcat > %{_localstatedir}/ldap/rpm-db-backup-%{db_conv}.ldif ||:
	[ $SLAPD_STATUS -eq 1 ] && srv start slapd
#else
#	echo "Found no incompatible db-type"
fi

%post servers
SLAPD_STATUS=`srv status slapd|grep -q -v up;echo $?`
[ $SLAPD_STATUS -eq 1 ] && srv stop slapd
# bgmilne: part 2 of gdbm->dbb conversion for data created with 
# original package for 9.1:
if [ -n "`find %{_localstatedir}/ldap/*.%{db_conv} 2>&-`" ]
then
	if [ -e %{_localstatedir}/ldap-rpm-backup -a -e %{_localstatedir}/ldap/rpm-db-backup-%{db_conv}.ldif ]
	then 
		echo "Warning: Old ldap backup data in %{_localstatedir}/ldap-rpm-backup"
		echo "If importing %{_localstatedir}/ldap/rpm-db-backup-%{db_conv}.ldif fails,"
		echo "please do it manually by running (as root):"
		echo "# srv stop slapd"
		echo "# slapadd -c -l %{_localstatedir}/ldap/rpm-db-backup-%{db_conv}.ldif"
		echo "# slapindex"
		echo "# chown ldap.ldap %{_localstatedir}/ldap/*"
		echo "# srv start slapd"
	fi
	if [ -e %{_localstatedir}/ldap/rpm-db-backup-%{db_conv}.ldif ]
	then
		mkdir -p %{_localstatedir}/ldap-rpm-backup
		mv -f %{_localstatedir}/ldap/*.%{db_conv} %{_localstatedir}/ldap-rpm-backup
		echo "Importing %{_localstatedir}/ldap/rpm-db-backup-%{db_conv}.ldif"
		slapadd -cv -l %{_localstatedir}/ldap/rpm-db-backup-%{db_conv}.ldif > \
		%{_localstatedir}/ldap/rpm-ldif-import.log 2>&1
		echo "Import complete, see log %{_localstatedir}/ldap/rpm-ldif-import.log"
	fi
fi
# openldap-2.0.x->2.1.x on ldbm/dbb backend seems to need reindex regardless:
slapindex
chown ldap.ldap -R %{_localstatedir}/ldap/
[ $SLAPD_STATUS -eq 1 ] && srv start slapd

# Setup log facility for OpenLDAP
if [ -f %{_sysconfdir}/syslog.conf ] ;then

	# clean syslog
	perl -pi -e "s|^.*ldap.*\n||g" %{_sysconfdir}/syslog.conf 

	typeset -i cntlog
	cntlog=0

	# probe free local-users
	while [ `grep -c local${cntlog} %{_sysconfdir}/syslog.conf` -gt 0 ]
	do 
		cntlog=${cntlog}+1
	done

	if [ ${cntlog} -le 9 ];then
		echo "# added by %{name}-%{version} r""pm $(date)" >> %{_sysconfdir}/syslog.conf
#   modified by Oden Eriksson
#		echo "local${cntlog}.*       /var/log/ldap/ldap.log" >> %{_sysconfdir}/syslog.conf
		echo -e "local${cntlog}.*\t\t\t\t\t\t\t-/var/log/ldap/ldap.log" >> %{_sysconfdir}/syslog.conf

		# reset syslog daemon
		if [ -f /var/lock/subsys/syslog ]; then
        		service syslog restart  > /dev/null 2>/dev/null || : 
		fi
	else
		echo "I can't set syslog local-user!"
	fi
		
	# set syslog local-user in /etc/sysconfig/ldap
	perl -pi -e "s|^.*SLAPDSYSLOGLOCALUSER.*|SLAPDSYSLOGLOCALUSER=\"LOCAL${cntlog}\"|g" %{_sysconfdir}/sysconfig/ldap 

fi

# Reset right permissions 
for i in %{_localstatedir}/ldap/* ; do
	if [ -f $i ]; then
		chmod 0600 $i
		chown ldap.ldap $i
	fi
done

# generate the ldap.pem cert here instead of the initscript
if [ ! -e %{_sysconfdir}/ssl/openldap/ldap.pem ] ; then
  if [ -x %{_datadir}/openldap/gencert.sh ] ; then
    echo "Generating self-signed certificate..."
    pushd %{_sysconfdir}/ssl/openldap/ > /dev/null
    yes ""|%{_datadir}/openldap/gencert.sh >/dev/null 2>&1
    chmod 640 ldap.pem
    chown root.ldap ldap.pem
    popd > /dev/null
  fi
  echo "To generate a self-signed certificate, you can use the utility"
  echo "%{_datadir}/openldap/gencert.sh..."
fi

pushd %{_sysconfdir}/openldap/ > /dev/null
for i in slapd.conf slapd.access.conf ; do
	if [ -f $i ]; then
		chmod 0640 $i
		chown root.ldap $i
	fi
done
popd > /dev/null


%_post_srv slapd
%_post_srv slurpd

# nscd reset
if [ -f /var/lock/subsys/nscd ]; then
        service nscd restart  > /dev/null 2>/dev/null || : 
fi


%preun servers
%_preun_srv slapd


%postun servers
if [ $1 = 0 ]; then 
	# remove ldap entry 
	perl -pi -e "s|^.*ldap.*\n||g" %{_sysconfdir}/syslog.conf 

	# reset syslog daemon
	if [ -f /var/lock/subsys/syslog ]; then
	        service syslog restart  > /dev/null 2>/dev/null || : 
	fi
fi
%_postun_userdel ldap


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig



%files
%defattr(-,root,root)
%doc ANNOUNCEMENT CHANGES COPYRIGHT LICENSE README 
%doc README.migration TOOLS.migration
%doc doc/rfc doc/drafts
%dir %{_sysconfdir}/openldap
%dir %{_sysconfdir}/openldap/schema
#%config(noreplace) %{_sysconfdir}/openldap/ldapfilter.conf
#%config(noreplace) %{_sysconfdir}/openldap/ldapsearchprefs.conf
#%config(noreplace) %{_sysconfdir}/openldap/ldaptemplates.conf
%config(noreplace) %{_sysconfdir}/openldap/ldapserver
%config(noreplace) %{_sysconfdir}/openldap/ldap.conf
%dir %{_datadir}/openldap
#%{_datadir}/openldap/ldapfriendly
%{_mandir}/man5/ldap.conf.5*
#%{_mandir}/man5/ldapfilter.conf.5*
#%{_mandir}/man5/ldapfriendly.5*
#%{_mandir}/man5/ldapsearchprefs.conf.5*
#%{_mandir}/man5/ldaptemplates.conf.5*
%{_mandir}/man5/ldif.5*

%files migration
%defattr(-,root,root)
%{_datadir}/openldap/migration


%files servers
%defattr(-,root,root)
#%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/ssl/openldap/ldap.pem
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/openldap/slapd.conf
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/openldap/slapd.access.conf

%dir %{_sysconfdir}/ssl/openldap
%config(noreplace) %{_sysconfdir}/openldap/schema/*.schema
%dir %{_datadir}/openldap/schema
%{_datadir}/openldap/schema/*.schema
%{_datadir}/openldap/schema/README
%dir %{_datadir}/openldap/ucdata
%{_datadir}/openldap/ucdata/*.dat

%config(noreplace) %{_sysconfdir}/sysconfig/ldap
%attr(750,ldap,ldap) %dir %{_localstatedir}/ldap
%attr(755,ldap,ldap) %dir /var/run/ldap
#%{_datadir}/openldap/*.help
%{_datadir}/openldap/gencert.sh
%{_sbindir}/*
%{_mandir}/man5/slapd.*.5*
%{_mandir}/man5/slapd-*.5*
%{_mandir}/man8/*
%dir %{_srvdir}/slapd
%dir %{_srvdir}/slapd/log
%{_srvdir}/slapd/run
%{_srvdir}/slapd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/slapd
%dir %{_srvdir}/slurpd
%dir %{_srvdir}/slurpd/log
%{_srvdir}/slurpd/run
%{_srvdir}/slurpd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/slurpd


%attr(750,ldap,ldap) %dir /var/log/ldap
%config(noreplace) %{_sysconfdir}/logrotate.d/ldap


%files clients
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
#%{_mandir}/man5/ud.conf.5*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/lib*.so.*


%files -n %libname-devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_mandir}/man3/*

%files -n %libname-devel-static
%defattr(-,root,root)
%{_libdir}/lib*.a

%files back_dnssrv
%defattr(-,root,root)
%{_libdir}/openldap/back_dnssrv.la
%{_libdir}/openldap/back_dnssrv.a
%{_libdir}/openldap/back_dnssrv*.so.*
%{_libdir}/openldap/back_dnssrv*.so

%files back_ldap
%defattr(-,root,root)
%{_libdir}/openldap/back_ldap.la
%{_libdir}/openldap/back_ldap.a
%{_libdir}/openldap/back_ldap*.so.*
%{_libdir}/openldap/back_ldap*.so

%if %sql
%files back_sql
%defattr(-,root,root)
%dir %{_libdir}/openldap
%{_libdir}/openldap/back_sql.la
%{_libdir}/openldap/back_sql.a
%{_libdir}/openldap/back_sql*.so.*
%{_libdir}/openldap/back_sql*.so
%endif

%files back_passwd
%defattr(-,root,root)
%{_libdir}/openldap/back_passwd.la
%{_libdir}/openldap/back_passwd.a
%{_libdir}/openldap/back_passwd*.so.*
%{_libdir}/openldap/back_passwd*.so


%changelog
* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 2.1.22-10sls
- minor spec cleanups

* Tue Feb 03 2004 Vincent Danen <vdanen@opensls.org> 2.1.22-9sls
- s/sldapd/slapd/

* Mon Feb 02 2004 Vincent Danen <vdanen@opensls.org> 2.1.22-8sls
- logrotate should call srv not service

* Tue Jan 27 2004 Vincent Danen <vdanen@opensls.org> 2.1.22-7sls
- supervise scripts (still some incomplete calls to old service command in
  the scriptlets; to be done when the others are converted (syslog, nscd))
- remove the guide package
- ldap has static uid/gid of 76

* Mon Dec 02 2003 Vincent Danen <vdanen@opensls.org> 2.1.22-6sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.22-5mdk
- Fix deps

* Mon Aug 11 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.22-4mdk
- Nuke rpath, make it know about -lssl

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.22-3mdk
- Fix mklibnamification

* Wed Jul 09 2003 Buchan Milne <bgmilne@linux-mandrake.com> 2.1.22-2mdk
- index on install/upgrade (should fix 2.0.x->2.1.x assuming no schema
  violations)
- TODO: test/patch migration tools, provide update default config 
  (bdb, better ACLs)

* Tue Jul 01 2003 Buchan Milne <bgmilne@linux-mandrake.com> 2.1.22-1mdk
- 2.1.22
- Merge changes from sparc team on 2.0.x (as below)

* Fri Jun 13 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.0.27-7mdk
- add --without-sql
- %%mklibname
- openldap-servers: add PreReq rpm-helper

* Fri May 23 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.1.20-1mdk
- 2.1.20

* Sun May 18 2003 Buchan Milne <bgmilne@linux-mandrake.com> 2.1.19-1mdk
- Openldap 2.1, with sasl2 and db4
- Update kerberosobject.schema (to include krbName atttribute removed from
  core.schema) and add krb5-kdc.schema (removed upstream).

* Tue Apr 29 2003 Vincent Danen <vdanen@linux-mandrake.com> 2.0.27-6mdk
- patch to fix library order for slapd so that unix crypt md5 hashes work
  properly

* Wed Apr 23 2003 Buchan Milne <bgmilne@linux-mandrake.com> 2.0.27-5mdk
- Specify the ldbm-api, so we don't get a random one ... and get the wrong
  one. Seems berkeley is better, and that's what 9.0 had.
- OK, maybe we should make it optional, for people who have had the
  misfortune of already "upgrading". Options are now:
  --with[out] cyrussasl (new) or --with[out] SASL (synonyms) (default: with)
  --with[out] kerberos (new) (default: without)
  --with gdbm (new) (defaults to berkeley without this option)
- Trash the message in post about a file that was removed a long time ago
  (with no changelog entry :-().
- configure options given in the same order as the --help (to easily read it)
- make --short-cricuit work to test scripts
  -DON'T CLEAN THE BUILDDIR!!! (that's what --clean is for)
  -clean the buildroot in install
- Provide automatic migration of ldap data from previous db format
  to current db format for a single database (multi-db installations
  are on your own). Any 9.1 installation with a single database should
  work after upgrading to this one, regardless of which db format
  is currently in use (gdbm as in the 9.1 packages or berkeley as in 9.0).

* Mon Jan 20 2003 Florin <florin@mandrakesoft.com> 2.0.27-4mdk
- rebuild and remove the schema dir ownership 

* Fri Jan 17 2003 Florin <florin@mandrakesoft.com> 2.0.27-3mdk
- add the maildrop schema (V. Guardiola's idea)

* Fri Jan 17 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.27-2mdk
- fix added syslog entry

* Mon Nov  4 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.0.27-1mdk
- 2.0.27
- start slurpd as user ldap, not root (re: bgmilne)

* Wed Sep 11 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.0.25-7mdk
- put /etc/ssl/openldap in openldap-server package since openldap-server
  does not specifically need the openldap package (re: Juhani Kurki)
- better cleanup
- fix libldap.la (re: Lonnie Borntreger)

* Thu Aug 01 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.0.25-6mdk
- really put ldap.pem into /etc/ssl/openldap
- use %%_{pre,postun}_user{add,del} macros for ldap user in servers

* Fri Jul 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.25-5mdk
- Enable build --with[out] SASL
- Patch25: Stop self-requiring when linking libldap.so. Aka. link with
  liblber that was just compiled

* Wed Jul 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.25-4mdk
- rebuild for new readline

* Thu Jul 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.0.25-3mdk
- rebuild to have the correct provides

* Wed Jul 10 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.25-2mdk
- sync samba.schema with samba-2.2.5

* Wed Jun 19 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.0.25-1mdk
- 2.0.25
- MigrationTools 40
- include a basic loglevel in slapd.conf so we can get some logging by
  default
- add qmailControl.schema
- take samba.schema from samba 2.2.3a
- remove references to patches no longer included
- spec cleanups
- since setup pkg contains ldap user, let's remove all {user,group}{del,add}
  stuff; still keep adding ldap user to adm group for the time being
- put /etc/openldap/ldap.conf back
- make ldap.pem in %%post instead of the initscript
- clean up the initscript so it's output is not so annoying
- put ldap.pem into /etc/ssl/openldap

* Tue Mar 12 2002 Daouda LO <daouda@mandrakesoft.com> 2.0.21-4mdk
- split the LANG variable to get correct country code.

* Thu Feb 14 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.0.21-3mdk
- fix typeo in misc.schema

* Tue Jan 28 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.0.21-2mdk
- fix typeo in schema patch
- fix some rpmlint warnings
- fix slapd.conf; remove missing nadf.schema reference
- fix logrotate entry so slapd is restarted only if it's already running
  (re: mr@uue.org)

* Wed Jan 22 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.0.21-1mdk
- 2.0.21 (security update)
- regenerate schema patch

* Tue Dec 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0.19-1mdk
- 2.0.19 for general usage.

* Thu Dec 06 2001 Philippe Libat <philippe@mandrakesoft.com> 2.0.18-3mdk
- fix static librairies (Patch24+libtool comment)

* Mon Nov 26 2001 Philippe Libat <philippe@mandrakesoft.com> 2.0.18-2mdk
- add new schema
- Migration Tools v39

* Fri Oct 26 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.18-1mdk
- Up to 2.0.18

* Tue Oct 16 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.17-1mdk
- Up to 2.0.17

* Thu Oct 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.0.15-2mdk
- new db3.

* Sat Sep 22 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.15-1mdk
- Up to 2.0.15, SSL fix

* Tue Sep 11 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.14-1mdk
- Up 2.0.14, Fixed slurpd millionth second bug.

* Mon Sep 10 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.13-1mdk
- Up to 2.0.13

* Fri Aug 31 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.12-1mdk
- Up to 2.0.12

* Fri Aug 24 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.11-6mdk
- Adding some directory in package (thanks to fcrozat)

* Thu Jul 05 2001 Philippe Libat <philippe@mandrakesoft.com> 2.0.11-6mdk
- new db3

* Mon Jul 02 2001 Philippe Libat <philippe@mandrakesoft.com> 2.0.11-5mdk
- fix requires on openldap-migration

* Wed Jun 27 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.11-4mdk
- Change typo fault in gencert script

* Mon Jun 11 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.11-3mdk
- Rebuild with some change
- Rebuild with cooker's libtool
- Remove slapcat because cooker broken libtool 
- Auto preset common name by hostname in gencert

* Mon May 28 2001 Christian Zoffoli <czoffoli@mandrakesoft.com> 2.0.11-2mdk
- added a statically compiled slapcat (named slapcat-gdbm) to dump gdbm DBs 
  to LDIF files also with an OpenLDAP compiled with Berkeley DB support
- added BuildRequires: db3-devel
- fixed certificate search in the init script
- added some conversion infos in the init script

* Mon May 28 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.11-1mdk
- Update to 2.0.11
- Build on 8.0, cooker devel environnement is broken

* Tue May 22 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.10-1mdk
- Adding default run level in init file
- Up to 2.0.10
- Don't get patched file in migration package
- Set default country in gencert.sh by default lang
- Now generate certificate at first start of server
- Correct strange space in sldap.conf patch (it made warning message on start
  of slapd)
- Using berkeley base for storing

* Mon May 21 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.9-2mdk
- Require setup with ldap user (remove user creation in few time, please ugrade).
- Adding i18n for migration tools patch.

* Sat May 19 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 2.0.9-1mdk
- 2.0.9
- removed no more needed openldap-2.0.8-ipv6-configure.patch (ITS#1146)
- new openldap-2.0.9-slapd.conf.patch (added basic ACL)

* Tue May 15 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 2.0.8-3mdk
- added Conflicts: openldap1-devel
- clean up in spec

* Mon May 14 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.8-2mdk
- Rebuild on cooker environnement (Thx to : Christian Zoffoli)

* Sat May 12 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 2.0.8-1mdk
- 2.0.8
- removed not needed openldap-norbert.patch
- updated openldap-2.0.8-slapd.conf.patch
- added openldap-2.0.8-ipv6-configure.patch

* Thu May 10 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.7-9mdk
- Really fall in love Christian's work !!!
- Removed not needen rh patch 
- Assembled html admin guide in one file
- Changed number of patch and source for easy maintenance
- Added migration package

* Tue May 08 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 2.0.7-8mdk
- added static libraries
- s!Copyright!License

* Mon May 07 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 2.0.7-7mdk
- added reset permissions on post macro
- merged with last RH patches
- removed ldap.conf
- improved post - postun - preun macros
- fixed tcp_wrapper support (allowing slapd to read hosts.*)
- fixed man pages (removed buildroot)

* Thu Apr 26 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 2.0.7-6mdk
- complete spec restyle
- Migration Tools v37
- merge with RH patches
- merge with PLD patches
- added SSL/TLS, unixODBC support
- added modules: dnssrv, sql, ldap, passwd
- added static modules: ldbm, shell
- changed default schema location
- added libldap2-static-devel package
- added openldap-servers package
- added openldap-clients package
- added openldap-guide package (added guide)
- added ldap user/group
- OpenLDAP executed as ldap  :O
- fixed slapd - slurpd DB paths
- fixed module path
- massive changes on default slapd.conf
- added Netscape Roaming profiles schema
- added QMAIL schema
- added kerberos schema
- added autofs schema
- added samba schema (MS AD)
- improved init script
- added certificate generation
- added syslog support (with autoprobe local-user) + logrotate 

* Mon Apr  9 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.7-5mdk
- Adaptation of default config file (bug#: 3044, by peter.boerner@lhsystems.com) 

* Mon Apr  2 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.7-4mdk
- Using build server macro

* Fri Mar  9 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.7-3mdk
- Rebuild with sasl support
- Correct bad link in man page

* Mon Feb 19 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.7-2mdk
- adding provide openldap-devel to libldap-devel package

* Tue Feb 13 2001 Vincent Saugey <vince@mandrakesoft.com> 2.0.7-1mdk
- Libificatizication
- Up to 2.0.7 (promize at French linux-expo, sorry for late)
- Update Migration tools to 2.0.7

* Tue Oct 17 2000 Vincent Saugey <vince@mandrakesoft.com> 2.0.6-1mdk
- Up to 2.0.6
- Macrozification

* Wed Aug 30 2000 Etienne Faure <etienne@mandrakesoft.com> 1.2.9-7mdk
- rebuilt with _mandir macro

* Fri Jul 07 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.9-6mdk.
- Remove make tests.

* Fri Apr 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.9-5mdk
- Move default databases to /var/lib/ldap and not /usr/tmp/
- Add redhat patch.
- Clean up.

* Tue Mar 21 2000 Jerome Dumonteil <jd@mandrakesoft.com>
- error in changelog

* Mon Mar 13 2000 Jerome Dumonteil <jd@mandrakesoft.com>
- Upgrade to versin 1.2.9
- use of _prefix

* Tue Nov 30 1999 Jerome Dumonteil <jd@mandrakesoft.com>
- Upgrade version of MigrationTools.
- use of _tmppath and prefix

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Get your life easy, patch the sources for bzman.

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- First mandrake release.

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip files

* Sat Sep 11 1999 Bill Nottingham <notting@redhat.com>
- update to 1.2.7
- fix some bugs from bugzilla (#4885, #4887, #4888, #4967)
- take include files out of base package

* Fri Aug 27 1999 Jeff Johnson <jbj@redhat.com>
- missing ;; in init script reload) (#4734).

* Tue Aug 24 1999 Cristian Gafton <gafton@redhat.com>
- move stuff from /usr/libexec to /usr/sbin
- relocate config dirs to /etc/openldap

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Wed Aug 11 1999 Cristian Gafton <gafton@redhat.com>
- add the migration tools to the package

* Fri Aug 06 1999 Cristian Gafton <gafton@redhat.com>
- upgrade to 1.2.6
- add rc.d script
- split -devel package

* Sun Feb 07 1999 Preston Brown <pbrown@redhat.com>
- upgrade to latest stable (1.1.4), it now uses configure macro.

* Fri Jan 15 1999 Bill Nottingham <notting@redhat.com>
- build on arm, glibc2.1

* Wed Oct 28 1998 Preston Brown <pbrown@redhat.com>
- initial cut.
- patches for signal handling on the alpha

