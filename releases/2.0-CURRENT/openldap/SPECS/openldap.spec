#
# spec file for package openldap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		openldap
%define version		2.3.30
%define release		%_revrel

%define major 		2.3_0
%define migtools_ver	45
%define fname		ldap
%define libname		%mklibname %{fname} %{major}

%global db4_internal	0
%define dbver		4.2.52
%define dbname		%(a=%dbver;echo ${a%.*})

%global sql		1
%global back_perl	0

#localstatedir is passed directly to configure, and we want it to be /var/lib
#define _localstatedir	%{_var}/run
%define	_libexecdir	%{_sbindir}

# Allow --with[out] SASL at rpm command line build
%{?_without_SASL:	%{expand: %%define _without_cyrussasl --without-cyrus-sasl}}
%{?_with_SASL:		%{expand: %%define _with_cyrussasl --with-cyrus-sasl}}
%{!?_with_cyrussasl:	%{!?_without_cyrussasl: %global _with_cyrussasl --with-cyrus-sasl}}
%{?_with_cyrussasl:	%define _with_cyrussasl --with-cyrus-sasl}
%{?_without_cyrussasl:	%define _without_cyrussasl --without-cyrus-sasl}
%{?_with_gdbm:		%global db_conv dbb}
%{!?_with_gdbm:		%global db_conv gdbm}
%{?_without_sql:	%global sql 0}

Summary: 	LDAP servers and sample clients
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	Artistic
Group: 		System/Servers
URL: 		http://www.openldap.org
# Openldap source
Source0: 	ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{name}-%{version}.tgz
# Specific source (S1-S19)
Source1: 	openldap.sysconfig
Source2:	DB_CONFIG
Source3:	ldap.conf
Source4:	slapd.access.conf
Source5:	ldap-hot-db-backup
Source6:	ldap-reinitialise-slave
Source7:	ldap-common
Source8:	10_openldap.afterboot
Source9:	gencert.sh
Source10:	ldap.logrotate
Source11:	slapd.conf
Source12:	slapd.run
Source13:	slapd-log.run
Source14:	slurpd.run
Source15:	slurpd-log.run
# Migration tools (S20-24)
Source20:	http://www.padl.com/download/MigrationTools-%{migtools_ver}.tar.bz2
Source21: 	migration-tools.txt
Source22: 	migrate_automount.pl
%if %{db4_internal}
Source25:	http://www.sleepycat.com/update/snapshot/db-%{dbver}.tar.bz2
%endif
# Extended Schema (S30+)
Source30: 	rfc822-MailMember.schema
Source31: 	autofs.schema
Source32: 	kerberosobject.schema
# Get from qmail-ldap patch (http://www.nrg4u.com/qmail/)
Source33: 	qmail.schema
Source34: 	mull.schema
# Get from samba source, examples/LDAP/samba.schema
Source35: 	samba.schema
Source36: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/netscape-profile.schema
Source37: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/trust.schema
Source38: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/dns.schema
Source39: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/cron.schema
Source40:	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/qmailControl.schema
Source41:	krb5-kdc.schema
Source42:	kolab.schema
# from evolution package
Source43:	evolutionperson.schema
# from rfc2739, updated schema for correctness, used by evo for calendar attrs
Source44:	calendar.schema
# from README.LDAP in sudo (pre-1.6.8) CVS:
Source45:	sudo.schema
# from bind sdb_ldap page: http://www.venaas.no/ldap/bind-sdb/dnszone-schema.txt
Source46:	dnszone.schema
# from http://cvs.pld.org.pl/SOURCES/openldap-dhcp.schema
Source47:	dhcp.schema
# Chris Patches
Patch0: 	%{name}-2.3.4-config.patch
Patch1:		%{name}-2.0.7-module.patch
#
# For now only build support for SMB (no krb5) changing support in smbk5passwd overlay:
Patch2:		openldap-2.3.4-smbk5passwd-only-smb.patch
# RH + PLD Patches
Patch15:	%{name}-cldap.patch
# Migration tools Patch
Patch40: 	MigrationTools-34-instdir.patch
Patch41: 	MigrationTools-36-mktemp.patch
Patch42: 	MigrationTools-27-simple.patch
Patch43: 	MigrationTools-26-suffix.patch
Patch45:	MigrationTools-45-i18n.patch
# schema patch
Patch46: 	openldap-2.0.21-schema.patch
# http://qa.mandriva.com/show_bug.cgi?id=15499
Patch48:	MigrationTools-45-structural.patch
Patch50:	http://www.sleepycat.com/update/4.2.52/patch.4.2.52.1
Patch51:	http://www.sleepycat.com/update/4.2.52/patch.4.2.52.2
Patch55:	http://www.sleepycat.com/update/4.2.52/patch.4.2.52.3
Patch56:	http://www.sleepycat.com/update/4.2.52/patch.4.2.52.4
Patch52:	db-4.2.52-amd64-mutexes.patch
Patch53:	openldap-2.2.19-ntlm.patch
# preserves the temp file used to import data if an error occured
Patch54:	MigrationTools-40-preserveldif.patch

#patches in CVS


BuildRoot: 	%{_buildroot}/%{name}-%{version}
%{?_with_cyrussasl:BuildRequires: 	libsasl-devel}
%{?_with_kerberos:BuildRequires:	krb5-devel}
%if %sql
BuildRequires: 	unixODBC-devel
%endif
%if %back_perl
BuildRequires:	perl-devel
%endif
%if !%db4_internal
BuildRequires: 	db4-devel >= %{dbver}
%endif
BuildRequires:	openssl-devel
BuildRequires:	perl
BuildRequires:	autoconf2.5
BuildRequires:	ed
BuildRequires:  ncurses-devel >= 5.0
BuildRequires:	tcp_wrappers-devel
BuildRequires:	libtool-devel
# for make test:
BuildRequires:	diffutils

Requires: 	%{libname} = %{version}-%{release}
Requires:	shadow-utils
Requires:	setup >= 2.2.0-6mdk


%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools.  The suite includes a
stand-alone LDAP server (slapd) and stand-alone LDAP replication server
(slurpd) which are in the -servers package, libraries for implementing the 
LDAP protocol (in the lib packages), and utilities, tools, and sample clients 
(in the -clients package). The openldap binary package includes configuration
files used by the libraries.


%package servers
Summary: 	OpenLDAP servers and related files
Group: 		System/Servers
Requires(pre): 	shadow-utils
Requires(pre):	rpm-helper
Requires(post):	afterboot
Requires(post):	rpm-helper
Requires(postun): afterboot
Requires(postun): rpm-helper
%if !%db4_internal
Requires(pre):	db4-utils
Requires(post):	db4-utils
Requires:	db4-utils
Requires: 	%{libname} = %{version}-%{release}
%endif
Provides:	%{name}-back_dnssrv = %{version}-%{release}
Provides:	%{name}-back_ldap = %{version}-%{release}
Provides:	%{name}-back_passwd = %{version}-%{release}
Provides:	%{name}-back_sql = %{version}-%{release}
Obsoletes:	%{name}-back_dnssrv < %{version}-%{release}
Obsoletes:	%{name}-back_ldap < %{version}-%{release}
Obsoletes:	%{name}-back_passwd < %{version}-%{release}
Obsoletes:	%{name}-back_sql < %{version}-%{release}

%description servers
This package contains the OpenLDAP servers, slapd (LDAP server) and slurpd
(replication daemon), additional backends, configuration files, schema 
definitions required for operation, and database maintenance tools.

This server package was compiled with support for the %{?_with_gdbm:gdbm}%{!?_with_gdbm:berkeley}
database library.


%package clients
Summary: 	OpenLDAP clients and related files
Group: 		System/Servers
Requires: 	%{libname} = %{version}-%{release}

%description clients
This package contains command-line ldap clients (ldapsearch, ldapadd etc).


%package migration
Summary: 	Set of scripts for migration of a nis domain to a ldap directory
Group: 		System/Configuration
Requires: 	%{name}-servers = %{version}-%{release}
Requires: 	%{name}-clients = %{version}-%{release}
Requires: 	perl(MIME::Base64)

%description migration
This package contains a set of scripts for migrating data from local files
(ie /etc/passwd) or a nis domain to an ldap directory.


%package -n %{libname}
Summary: 	OpenLDAP libraries
Group: 		System/Libraries
Provides:       lib%{fname} = %{version}-%{release}
# This is needed so all libldap2 applications get /etc/openldap/ldap.conf
# which was moved from openldap-clients to openldap in 2.1.29-1avx
Requires:	%{name} >= 2.1.29-1avx

%description -n %{libname}
This package includes the libraries needed by ldap applications.


%package -n %{libname}-devel
Summary: 	OpenLDAP development libraries and header files
Group: 		Development/C
Provides: 	lib%{fname}-devel = %{version}-%{release}
Provides:       openldap-devel = %{version}-%{release}
Provides:	openldap2-devel = %{version}-%{release}
Requires: 	%{libname} = %{version}-%{release}
Obsoletes: 	openldap-devel
Conflicts:	libldap1-devel
Conflicts:	%mklibname -d ldap 2
Conflicts:	%mklibname -d ldap 2.2_7

%description -n %{libname}-devel
This package includes the development libraries and header files
needed for compiling applications that use LDAP internals.  Install
this package only if you plan to develop or will need to compile
LDAP clients.


%package -n %{libname}-static-devel
Summary: 	OpenLDAP development static libraries
Group: 		Development/C
Provides: 	lib%{fname}-devel-static = %{version}-%{release}
Provides: 	lib%{fname}-static-devel = %{version}-%{release}
Provides:	openldap-devel-static = %{version}-%{release}
Provides:	openldap-static-devel = %{version}-%{release}
Requires: 	%{libname}-devel = %{version}-%{release}
Obsoletes: 	openldap-devel-static
Conflicts:	libldap1-devel


%description -n %{libname}-static-devel
OpenLDAP development static libraries.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%if %{db4_internal}
%setup -q -a 20 -a 25
pushd db-%{dbver} >/dev/null
# upstream patches
%patch50
%patch51
%patch55
%patch56

%ifnarch %ix86
%patch52 -p1 -b .amd64-mutexes
(cd dist && ./s_config)
%endif
popd >/dev/null
%else
%setup -q -a 20
%endif

# Chris patches
%patch0 -p1 -b .config
perl -pi -e 's/LDAP_DIRSEP "run" //g' include/ldap_defaults.h
%patch1 -p1 -b .module
%patch2 -p1 -b .only-smb

%patch15 -p1 -b .cldap 

pushd MigrationTools-%{migtools_ver}
%patch40 -p1 -b .instdir
%patch41 -p1 -b .mktemp
%patch42 -p1 -b .simple
%patch43 -p1 -b .suffix
%patch45 -p2 -b .i18n
%patch48 -p2 -b .account
%patch54 -p1 -b .preserve
popd

%patch46 -p1 -b .mdk
#bgmilne %patch47 -p1 -b .maildropschema
%patch53 -p1 -b .ntlm

# patches from CVS

# test 036, 041 seems broken (036 is an experimental test)
rm -f tests/scripts/test036*
rm -f tests/scripts/test041*
# test 018 fails on x86_64 for some reason
#%ifarch x86_64
#rm -f tests/scripts/test018*
#%endif


%build
%serverbuild

%if %db4_internal
dbdir=`pwd`/db-instroot
pushd db-%{dbver}/build_unix >/dev/null
CONFIGURE_TOP="../dist" \
    %configure2_5x \
    --enable-shared \
    --disable-static \
    --with-uniquename=_openldap_slapd_avx \
    --program-prefix=slapd_ \
%ifarch %{ix86}
    --disable-posixmutexes \
    --with-mutex=x86/gcc-assembly
%endif
%ifarch alpha
    --disable-posixmutexes \
    --with-mutex=ALPHA/gcc-assembly
%endif
%ifarch ia64
    --disable-posixmutexes \
    --with-mutex=ia64/gcc-assembly
%endif
%ifarch ppc
    --disable-posixmutexes \
    --with-mutex=PPC/gcc-assembly
%endif
%ifarch sparc
    --disable-posixmutexes \
    --with-mutex=Sparc/gcc-assembly
%endif

#--with-mutex=POSIX/pthreads/library
# JMD: use --disable-posixmutexes so it works on a non-NPTL kernel, and use
# assembler mutexes since they're *way* faster and correctly implemented.

perl -pi -e 's/^(libdb_base=\s+)\w+/\1libslapd_db/g' Makefile
#Fix soname and libname in libtool:
perl -pi -e 's/shared_ext/shrext/g' libtool
make
rm -Rf $dbdir
mkdir -p $dbdir
make DESTDIR=$dbdir install
ln -sf ${dbdir}/%{_libdir}/libslapd_db-%{dbname}.so ${dbdir}/%{_libdir}/libdb-%{dbname}.so
popd >/dev/null
export CPPFLAGS="-I${dbdir}/%{_includedir} $CPPFLAGS"
export LDFLAGS="-L${dbdir}/%{_libdir} $LDFLAGS"
export LD_LIBRARY_PATH="${dbdir}/%{_libdir}"
%endif

unset CONFIGURE_TOP

#FIXME: Some script backends should not be used with threads, mostly shell/perl

# don't choose db4.3 even if it is available
export ol_cv_db_db_4_dot_3=no

# XXX: this is for when we move to glibc 2.4:
## try and miss linuxthreads, so we get a threading lib on glibc2.4:
#export ol_cv_header_linux_threads=no

#rh only:
export CPPFLAGS="-I%{_prefix}/kerberos/include $CPPFLAGS"
%if %{?openldap_fd_setsize:1}%{!?openldap_fd_setsize:0}
CPPFLAGS="$CPPFLAGS -DOPENLDAP_FD_SETSIZE=%{openldap_fd_setsize}"
%endif
export LDFLAGS="-L%{_prefix}/kerberos/%{_lib} $LDFLAGS"


%configure2_5x \
    --with-subdir=%{name} \
    --localstatedir=/var/run/ldap \
    --enable-dynamic \
    --enable-syslog \
    --enable-proctitle \
    --enable-ipv6 \
    --enable-local \
    %{?_with_cyrussasl} %{?_without_cyrussasl} \
    %{?_with_kerberos} %{?_without_kerberos} \
    --with-threads \
    --with-tls \
    --enable-slapd \
    --enable-aci \
    --enable-cleartext \
    --enable-crypt \
    --enable-lmpasswd \
    %{?_with_kerberos:--enable-kpasswd} \
    %{?_with_cyrussasl:--enable-spasswd} \
    --enable-modules \
    --enable-rewrite \
    --enable-rlookups \
    --enable-wrappers \
    --enable-bdb=yes \
    --enable-dnssrv=mod \
    --enable-hdb=yes \
    --enable-ldap=mod \
    --enable-ldbm=yes \
    --enable-meta=mod \
    --enable-monitor=mod \
    --enable-passwd=mod \
%if %{back_perl}
    --enable-perl=mod \
%endif
    --enable-relay=mod \
%if %sql
    --enable-sql=mod \
%endif
    --enable-overlays=mod \
    --enable-shared

# These options are no longer available
#	--enable-cldap \
#	--enable-multimaster \

# (oe) amd64 fix
perl -pi -e "s|^AC_CFLAGS.*|AC_CFLAGS = $CFLAGS -fPIC|g" libraries/librewrite/Makefile

make depend 

make 
make -C contrib/slapd-modules/smbk5pwd


%check
%if %{!?_without_test:1}%{?_without_test:0}
dbdir=`pwd`/db-instroot
export LD_LIBRARY_PATH="${dbdir}/%{_libdir}"
make test
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
cp -af contrib/slapd-modules/smbk5pwd/README{,.smbk5passwd}

%if %{db4_internal}
pushd db-%{dbver}/build_unix >/dev/null
%makeinstall_std
for i in %{buildroot}%{_bindir}/db_*; do mv $i ${i/db_/slapd_db_}; done
popd >/dev/null
%endif
%makeinstall_std

cp contrib/slapd-modules/smbk5pwd/.libs/smbk5pwd.so* %{buildroot}/%{_libdir}/%{name}

### some hack
perl -pi -e "s| -L../liblber/.libs||g" %{buildroot}%{_libdir}/libldap.la

#sed -i -e "s|-L%{_builddir}/%{name}-%{version}/db-instroot/%{_libdir}||g" %{buildroot}/%{_libdir}/%{name}/*.la %{buildroot}/%{_libdir}/*la
perl -pi -e  "s,-L%{_builddir}\S+%{_libdir},,g" %{buildroot}/%{_libdir}/lib*.la

mkdir -p %{buildroot}%{_srvdir}/{slapd,slurpd}/log
install -m 0740 %{_sourcedir}/slapd.run %{buildroot}%{_srvdir}/slapd/run
install -m 0740 %{_sourcedir}/slapd-log.run %{buildroot}%{_srvdir}/slapd/log/run
install -m 0740 %{_sourcedir}/slurpd.run %{buildroot}%{_srvdir}/slurpd/run
install -m 0740 %{_sourcedir}/slurpd-log.run %{buildroot}%{_srvdir}/slurpd/log/run

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 %{_sourcedir}/%{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/ldap

for i in slapd.conf ldap.conf slapd.access.conf; do
    install -m 0640 %{_sourcedir}/${i} %{buildroot}%{_sysconfdir}/openldap
done

### repository dir
install -d %{buildroot}%{_var}/lib/ldap

### DB_CONFIG for bdb backend
install -m 0644 %{_sourcedir}/DB_CONFIG %{buildroot}%{_var}/lib/ldap

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
for i in rfc822-MailMember.schema \
    autofs.schema \
    kerberosobject.schema \
    qmail.schema \
    mull.schema \
    samba.schema \
    netscape-profile.schema \
    trust.schema \
    dns.schema \
    cron.schema \
    qmailControl.schema \
    krb5-kdc.schema \
    kolab.schema \
    evolutionperson.schema \
    calendar.schema \
    sudo.schema \
    dnszone.schema \
    dhcp.schema ; do
        install -m 0644 %{_sourcedir}/${i} %{buildroot}%{_datadir}/openldap/schema/
done

mkdir -p %{buildroot}%{_datadir}/openldap/scripts
install -m 0755 %{_sourcedir}/{ldap-hot-db-backup,ldap-reinitialise-slave} %{buildroot}%{_datadir}/openldap/scripts/

mkdir -p %{buildroot}/%{_sysconfdir}/cron.daily
ln -s %{_datadir}/%{name}/scripts/ldap-hot-db-backup %{buildroot}/%{_sysconfdir}/cron.daily/ldap-hot-db-backup

### create local.schema
echo "# This is a good place to put your schema definitions " > %{buildroot}%{_sysconfdir}/openldap/schema/local.schema
chmod 0644 %{buildroot}%{_sysconfdir}/openldap/schema/local.schema

### deal with the migration tools
install -d %{buildroot}%{_datadir}/openldap/migration
install -m 0755 MigrationTools-%{migtools_ver}/{*.pl,*.sh,*.txt,*.ph} %{buildroot}%{_datadir}/openldap/migration
install -m 0644 MigrationTools-%{migtools_ver}/README %{_sourcedir}/migration-tools.txt %{buildroot}%{_datadir}/openldap/migration
install -m 0755 %{_sourcedir}/migrate_automount.pl %{buildroot}%{_datadir}/openldap/migration

cp MigrationTools-%{migtools_ver}/README README.migration
cp %{_sourcedir}/migration-tools.txt TOOLS.migration


### gencert.sh
install -m 0755 %{_sourcedir}/gencert.sh %{buildroot}/%{_datadir}/openldap

### log repository
install -m 0700 -d %{buildroot}/var/log/ldap
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 %{_sourcedir}/ldap.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/ldap


# get the buildroot out of the man pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

mkdir -p %{buildroot}%{_sysconfdir}/ssl/openldap

mv %{buildroot}/var/run/ldap/openldap-data/DB_CONFIG.example %{buildroot}/%{_var}/lib/ldap/

# afterboot snippet
mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/10_openldap.afterboot %{buildroot}%{_datadir}/afterboot/10_openldap


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre servers
%_pre_useradd ldap %{_var}/lib/ldap /bin/false 76
# allowing slapd to read hosts.allow and hosts.deny
%{_bindir}/gpasswd -a ldap adm 1>&2 > /dev/null || :

LDAPUSER=ldap
LDAPGROUP=ldap
[ -e "/etc/sysconfig/%{name}" ] && . "/etc/sysconfig/%{name}"
SLAPDCONF=${SLAPDCONF:-/etc/%{name}/slapd.conf}

#decide whether we need to migrate at all:
MIGRATE=`%{_sbindir}/slapd -VV 2>&1|while read a b c d e;do case $d in (2.3.*) echo nomigrate;;(2.*) echo migrate;;esac;done`

if [ "$1" -ne 1 -a -e "$SLAPDCONF" -a "$MIGRATE" != "nomigrate" ]; then
    SLAPD_STATUS=`/sbin/sv status /service/slapd 2>/dev/null | cut -d ';' -f 1 | egrep -q '^run: ' ; echo $?`
    [ $SLAPD_STATUS -eq 0 ] && srv --down slapd
    #`awk '/^[:space:]*directory[:space:]*\w*/ {print $2}' /etc/%{name}/slapd.conf`
    dbs=`awk 'BEGIN {OFS=":"} /[:space:]*^database[:space:]*\w*/ {db=$2;suf="";dir=""}; /^[:space:]*suffix[:space:]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm"||db=="hdb")&&(suf!=""&&dir!="")) print dir,suf};/^[:space:]*directory[:space:]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm"||db="hdb")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g'`
    # " (for syntax highlighting)
    for db in $dbs
    do
        dbdir=${db/:*/}
        dbsuffix=${db/*:/}
        [ -e /etc/sysconfig/ldap ] && . /etc/sysconfig/ldap
        # data migration between incompatible versions
        # openldap >= 2.2.x have slapcat as a link to slapd, older releases do not
        if [ "${AUTOMIGRATE:-yes}" == "yes" -a -f %{_sbindir}/slapcat ]; then
            ldiffile="rpm-migrate-to-%{major}.ldif"
            # dont do backups more than once
            if [ ! -e "${dbdir}/${ldiffile}-imported" -a ! -e "${dbdir}/${ldiffile}-import-failed" ];then
                echo "Migrating pre-OpenLDAP-%{major} data"
                echo "Making a backup of $dbsuffix to ldif file ${dbdir}/$ldiffile"
                # For some reason, slapcat works in the shell when slapd is running but not via rpm ...
                slapcat -b "$dbsuffix" -l ${dbdir}/${ldiffile} ||:
            fi
        fi
    done
fi


%post servers
/sbin/ldconfig
SLAPD_STATUS=`srv --list slapd|grep -e '^slapd '|grep -q -v 'up'; echo $?`
[ $SLAPD_STATUS -eq 1 ] && srv --down slapd
# bgmilne: part 2 of gdbm->dbb conversion for data created with 
# original package for 9.1:
dbnum=1
LDAPUSER=ldap
LDAPGROUP=ldap
[ -e "/etc/sysconfig/%{name}" ] && . "/etc/sysconfig/%{name}"
SLAPDCONF=${SLAPDCONF:-/etc/%{name}/slapd.conf}
if [ -e "$SLAPDCONF" ]; then
    dbs=`awk 'BEGIN {OFS=":"} /[:space:]*^database[:space:]*\w*/ {db=$2;suf="";dir=""}; /^[:space:]*suffix[:space:]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm")&&(suf!=""&&dir!="")) print dir,suf};/^[:space:]*directory[:space:]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g'`
    # " (for syntax highlighting)
    for db in $dbs
    do	
        dbdir=${db/:*/}
        dbsuffix=${db/*:/}
        ldiffile="rpm-migrate-to-%{major}.ldif"
        if [ -e "${dbdir}/${ldiffile}" ]; then
            echo -e "\n\nImporting $dbsuffix"
            if [ -e ${dbdir}/ldap-rpm-backup ]; then 
                echo "Warning: Old ldap backup data in ${dbdir}/ldap-rpm-backup"
                echo "These files will be removed"
                rm -f ${dbdir}/ldap-rpm-backup/*
            fi

            echo "Moving the database files fom ${dbdir} to ${dbdir}/ldap-rpm-backup"
            mkdir -p ${dbdir}/ldap-rpm-backup
            mv -f ${dbdir}/{*.bdb,*.gdbm,*.dbb,log.*,__db*} ${dbdir}/ldap-rpm-backup 2>/dev/null
            echo "Importing $dbsuffix from ${dbdir}/${ldiffile}"
            if slapadd -q -cv -b "$dbsuffix" -l ${dbdir}/${ldiffile} > \
                ${dbdir}/rpm-ldif-import.log 2>&1
                then
                mv -f ${dbdir}/${ldiffile} ${dbdir}/${ldiffile}-imported
                echo "Import complete, see log ${dbdir}/rpm-ldif-import.log"
                echo "If any entries were not migrated, see ${dbdir}/${ldiffile}-imported"
            else
                mv -f ${dbdir}/${ldiffile} ${dbdir}/${ldiffile}-import-failed
                echo "Import failed on ${dbdir}/${ldifffile}, see ${dbdir}/rpm-ldif-import.log"
                echo "An ldif dump of $dbsuffix has been saved as ${dbdir}/${ldiffile}-import-failed"
                echo -e "\nYou can import it manually by running (as root):"
                echo "# srv --down slapd"
                echo "# slapadd -c -l ${dbdir}/${ldiffile}-import-failed"
                echo "# chown $LDAPUSER:$LDAPGROUP ${dbdir}/*"
                echo "# srv --up slapd"

            fi
	fi
	chown ${LDAPUSER}:${LDAPGROUP} -R ${dbdir}
	# openldap-2.0.x->2.1.x on ldbm/dbb backend seems to need reindex regardless:
	#slapindex -n $dbnum
	#dbnum=$[dbnum+1]
    done
fi
[ $SLAPD_STATUS -eq 1 ] && srv --up  slapd

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

    if [ ${cntlog} -le 9 ]; then
        echo "# added by %{name}-%{version} r""pm $(date)" >> %{_sysconfdir}/syslog.conf
#   modified by Oden Eriksson
#		echo "local${cntlog}.*       /var/log/ldap/ldap.log" >> %{_sysconfdir}/syslog.conf
        echo -e "local${cntlog}.*\t\t\t\t\t\t\t-/var/log/ldap/ldap.log" >> %{_sysconfdir}/syslog.conf

        # reset syslog daemon
        if [ "`/sbin/sv status /service/syslogd 2>/dev/null | cut -d ';' -f 1 | egrep -q '^run: ' ; echo $?`" == "0" ]; then
            /sbin/sv hup /service/syslogd  > /dev/null 2>/dev/null || : 
        fi
    else
        echo "I can't set syslog local-user!"
    fi
		
    # set syslog local-user in /etc/sysconfig/ldap
    perl -pi -e "s|^.*SLAPDSYSLOGLOCALUSER.*|SLAPDSYSLOGLOCALUSER=\"LOCAL${cntlog}\"|g" %{_sysconfdir}/sysconfig/ldap 
fi

# generate the ldap.pem cert here instead of the initscript
if [ ! -e %{_sysconfdir}/ssl/openldap/ldap.pem ] ; then
    if [ -x %{_datadir}/openldap/gencert.sh ] ; then
        echo "Generating self-signed certificate..."
        pushd %{_sysconfdir}/ssl/openldap/ > /dev/null
            yes ""|%{_datadir}/openldap/gencert.sh >/dev/null 2>&1
            chmod 0640 ldap.pem
            chown root:${LDAPGROUP} ldap.pem
        popd > /dev/null
    fi
    echo "To generate a self-signed certificate, you can use the utility"
    echo "%{_datadir}/openldap/gencert.sh..."
fi

pushd %{_sysconfdir}/openldap/ > /dev/null
    for i in slapd.conf slapd.access.conf ; do
        if [ -f $i ]; then
            chmod 0640 $i
            chown root:${LDAPGROUP} $i
	fi
    done
popd > /dev/null

%_post_srv slapd
%_post_srv slurpd
%_mkafterboot

# nscd reset
if [ "`/sbin/sv status /service/nscd 2>/dev/null | cut -d ';' -f 1 | egrep -q '^run: ' ; echo $?`" == "0" ]; then
    /sbin/sv hup /service/nscd  > /dev/null 2>/dev/null || : 
fi


%preun servers
%_preun_srv slapd


%postun servers
/sbin/ldconfig
if [ $1 = 0 ]; then 
    # remove ldap entry 
    perl -pi -e "s|^.*ldap.*\n||g" %{_sysconfdir}/syslog.conf 

    # reset syslog daemon
    if [ "`/sbin/sv status /service/syslogd 2>/dev/null | cut -d ';' -f 1 | egrep -q '^run: ' ; echo $?`" == "0" ]; then
        /sbin/sv hup /service/syslogd  > /dev/null 2>/dev/null || : 
    fi
fi
%_postun_userdel ldap
%_mkafterboot

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%triggerpostun -- openldap-clients < 2.1.29-1avx
# We may have openldap client configuration in /etc/ldap.conf
# which now needs to be in /etc/openldap/ldap.conf
if [ -f /etc/ldap.conf ]; then
    mv -f /etc/openldap/ldap.conf /etc/openldap/ldap.conf.rpmfix
    cp -af /etc/ldap.conf /etc/openldap/ldap.conf
fi


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/openldap
%dir %{_sysconfdir}/openldap/schema
#%config(noreplace) %{_sysconfdir}/openldap/ldapfilter.conf
#%config(noreplace) %{_sysconfdir}/openldap/ldapsearchprefs.conf
#%config(noreplace) %{_sysconfdir}/openldap/ldaptemplates.conf
%config(noreplace) %{_sysconfdir}/openldap/ldapserver
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/openldap/ldap.conf
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
%dir %{_sysconfdir}/openldap
%dir %{_sysconfdir}/openldap/schema
#%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/ssl/openldap/ldap.pem
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/openldap/slapd.conf
%attr(0640,root,ldap) %{_sysconfdir}/openldap/DB_CONFIG.example
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/openldap/slapd.access.conf

%dir %{_sysconfdir}/ssl/openldap
%config(noreplace) %{_sysconfdir}/openldap/schema/*.schema
%{_sysconfdir}/cron.daily/ldap-hot-db-backup
%dir %{_datadir}/openldap
%dir %{_datadir}/openldap/schema
%{_datadir}/openldap/schema/*.schema
%{_datadir}/openldap/schema/*.ldif
%{_datadir}/openldap/schema/README
#%dir %{_datadir}/openldap/ucdata
#%{_datadir}/openldap/ucdata/*.dat
%{_datadir}/openldap/scripts


%config(noreplace) %{_sysconfdir}/sysconfig/ldap
%attr(750,ldap,ldap) %dir %{_var}/lib/ldap
%config(noreplace) %{_var}/lib/ldap/DB_CONFIG
%{_var}/lib/ldap/DB_CONFIG.example
%attr(755,ldap,ldap) %dir /var/run/ldap
#%{_datadir}/openldap/*.help
%{_datadir}/openldap/gencert.sh
%{_sbindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.la
%{_libdir}/%{name}/*.so*
%{_mandir}/man5/slap*.5*
%{_mandir}/man8/*
%dir %attr(0750,root,admin) %{_srvdir}/slapd
%dir %attr(0750,root,admin) %{_srvdir}/slapd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/slapd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/slapd/log/run
%dir %attr(0750,root,admin) %{_srvdir}/slurpd
%dir %attr(0750,root,admin) %{_srvdir}/slurpd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/slurpd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/slurpd/log/run
%{_datadir}/afterboot/10_openldap

%attr(750,ldap,ldap) %dir /var/log/ldap
%config(noreplace) %{_sysconfdir}/logrotate.d/ldap


%files clients
%defattr(-,root,root)
%{_bindir}/ldap*
%{_mandir}/man1/ldap*
#%{_mandir}/man5/ud.conf.5*


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*
%if %db4_internal
# internal version of db4
%{_libdir}/libslapd_db*
%attr(755,root,root) %{_bindir}/slapd_db*
%exclude %{_prefix}/docs
%exclude %{_includedir}/db*.h
%endif

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libl*.so
%{_libdir}/libl*.la
%{_includedir}/l*.h
%{_includedir}/s*.h
%{_mandir}/man3/*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/lib*.a

%files doc
%defattr(-,root,root)
%doc ANNOUNCEMENT CHANGES COPYRIGHT LICENSE README 
%doc doc/rfc doc/drafts
%doc README.migration TOOLS.migration
%doc contrib/slapd-modules/smbk5pwd/README.smbk5passwd


# TODO:
# - add cron-job to remove transaction logs (bdb)


%changelog
* Fri Dec 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.30
- 2.3.30
- don't use the internal db4 anymore
- P101 dropped; fixed upstream

* Mon Sep 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.24
- don't package /usr/bin/slapd_db* twice (doesn't belong in openldap-clients)

* Sun Sep 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.24
- reversed the sv logic so it actually will work properly

* Sun Sep 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.24
- change runsvctrl calls to /sbin/sv calls

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.24
- 2.3.24
- install the ldap hot-copy backup script to run daily
- use slapd -VV, not -V, for version check otherwise slapd gets
  started (bgmilne)
- allow for the setting of the maximum file descriptor limit at compile
  time (ie. --define 'openldap_fd_setsize 8192)
- P101: fix ppolicy issues (ITS4576)
- drop unapplied patches: P6, P8, P10, P12, P20, P21, P47
- drop P100; fixed upstream
- update samba.schema (bgmilne)
- updated some options for logrotate (daily rotation, etc.)
- updated ldap-common to only consider bdb and hdb (not ldbm)
- updated slapd.conf
- spec cleanups
- rebuild against new openssl

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9
- add -doc subpackage

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9
- rebuild against perl 5.8.8
- perl policy

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9
- fix group

* Mon Feb 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9
- fix requires

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9
- Clean rebuild

* Sun Jan 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Oct 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9-4avx
- move the internal db slapd_db stuff to the lib package otherwise we
  always get openldap-server installed whether we want it or not
- fix bug #13 (unused options in /etc/sysconfig/ldap)

* Thu Oct 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9-3avx
- fix the test for slapd running in the logrotate script

* Sun Oct 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9-2avx
- make runsvstat quieter if /service/slapd doesn't exist

* Mon Oct 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.9-1avx
- 2.3.9
- test041 is disabled upstream too
- P100: fix ITS 4035 - rootdn incorrect in cn=config backend/database
  (andreas)
- disable (experimental) test036
- add afterboot snippet

* Sat Oct 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.8-1avx
- 2.3.8
- drop P100, P101 (fixed upstream)
- test041 seems broken; don't run it
- spec fixes (srv, unused macros)

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6-5avx
- fix dumb typeo in %%pre script

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6-4avx
- fix the slapd run script; -d by itself is no longer sufficient, a
  loglevel needs to be passed so it if isn't defined in slapd.conf, use
  256 per default
- fix the slurpd run script; -d there also needs a loglevel
- remove some crap that made slurpd's run script totally not work
- check slapd version to avoid unnecessary export/import (bgmilne)
- fix test for db4 internal case (bgmilne)
- P100, P101: fixes from cvs

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6-3avx
- rebuild against new unixODBC

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6-2avx
- drop S1
- put back out ldap.logrotate

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6-1avx
- 2.3.6
- use execlineb for run scripts
- move logdir to /var/log/service/{slapd,slurpd}
- run scripts are now considered config files and are not replaceable
- update migration/upgrade stuff from mandriva spec (2.3.6-1mdk)

* Sat Aug 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-16avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-15avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-14avx
- bootstrap build

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-13avx
- really use logger in the run scripts (have I done a few too many
  of these today?)

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-12avx
- use logger for logging

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-11avx
- rebuild against new perl

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-10avx
- rebuild against new openssl

* Thu Sep 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-9avx
- make runsvstat a little quieter

* Tue Sep 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-8avx
- grep for "run" with runsvstat rather than "up"

* Sun Sep 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-7avx
- missed one call to svstat

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-6avx
- update run scripts
- s/svc/runsvctrl/ in spec
- update logrotate script

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-5avx
- rebuild against latest openssl

* Wed Jun 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-4avx
- fix slapd's run file; we need to give the loglevel to slapd's "-d"
  parameter in order for logging to work
- P2: bring back re-ordered XXLIBS in slapd/Makefile to ensure we use the
  right md5 for passwords (otherwise if one changes a password with
  passwd, it's stored in crypt format rather than crypt's md5 format)

* Tue Jun 29 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-3avx
- force ldap.conf to be mode 0644
- BuildRequires: autoconf2.5, ed (jmdault)
- disable posix mutexes, this breaks setups with non-NPTL kernels,
  low-end processors (VIA, K6, P1) and UML (jmdault)
- use assembler mutexes whenever possible, since they're the fastest
  on Linux (jmdault)
- change the internal db4 unique name

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-2avx
- fix requires
- fix logrotate script (again) to call srv not service

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.29-1avx
- Annvix build
- 2.1.29
- fix spec scriptlets to use supervise tools rather than initscripts (for
  syslog, nscd, and slapd)
- update slapd.run script to do the bdb recovery stuff
- sync with cooker 2.1.29-4mdk:
  - Migration-tools 0.45 (bgmilne)
  - removed P44; fixed upstream (bgmilne)
  - updated P45 - including fix for schema compliance (bgmilne)
  - slapd.conf: default to bdb backend, add examples for monitor backend
    (bgmilne)
  - updated samba (for samba-3.0.x with legacy entries uncommented) and qmail
    (fixes syntax numbers) schemas (bgmilne)
  - return of P0 - place ldap data and slurpd replog in /var/lib/ldap (bgmilne)
  - drop unapplied patches P2, P3, P4, P24, P25, P48 (bgmilne)
  - build against internal version of db4 (so we can use db-4.2.52.2) (bgmilne)
  - fix hot-dump/restore pre/post scripts to handle multiple dbs (bgmilne)
  - include a sane copy of kolab.schema, and enable it and samba.schema in
    default config (bgmilne)
  - add example DB_CONFIG file (bgmilne)
  - revert to using /etc/openldap/ldap.conf instead of /etc/ldap.conf
    (#4462) (bgmilne)
  - merge fixes from amd64 branch (gbeauchesne)
  - better default slapd.access.conf and ldap.conf (don't require CA-signed
    certs) (bgmilne)
  - comment out the TLS_CACERT line in ldap.conf since /etc/ssl/cacert.pem
    doesn't exist anyway and it breaks non-TLS behaviour (florin)
  - add some excample scripts for hot database backups/removal of old
    transaction logs (bgmilne)
  - add schema for evolution, dnszone, sudo, dhcp, drop dns, cron (not
    valid, and never implemented) (bgmilne)
  - update ACLs to allow users to add contacts (ie. via Evolution) (bgmilne)
  - add the ntlm.patch (florin)


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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
