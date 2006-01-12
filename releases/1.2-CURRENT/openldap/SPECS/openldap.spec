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
%define version		2.3.9
%define release		%_revrel

%define major 		2.3_0
%define migtools_ver	45
%define fname		ldap
%define libname		%mklibname %{fname} %{major}

%global db4_internal	1
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
%{!?_with_cyrussasl:	%{!?_without_cyrussasl: %define _with_cyrussasl --with-cyrus-sasl}}
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
Source0: 	ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{name}-%{version}.tar.bz2
# Specific source
Source2: 	%{name}.sysconfig
Source5:	DB_CONFIG
Source6:	ldap.conf
Source7:	slapd.access.conf
Source8:	ldap-hot-db-backup
Source9:	ldap-reinitialise-slave
Source10:	ldap-common
Source12:	10_openldap.afterboot
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
%if %db4_internal
Source30:	http://www.sleepycat.com/update/snapshot/db-%{dbver}.tar.bz2
%endif
# Extended Schema 
Source50: 	rfc822-MailMember.schema
Source51: 	autofs.schema
Source52: 	kerberosobject.schema
# Get from qmail-ldap patch (http://www.nrg4u.com/qmail/)
Source53: 	qmail.schema
Source54: 	mull.schema
# Get from samba source, examples/LDAP/samba.schema
Source55: 	samba.schema
Source56: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/netscape-profile.schema
Source57: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/trust.schema
Source58: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/dns.schema
Source59: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/cron.schema
Source60:	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/qmailControl.schema
Source61:	krb5-kdc.schema
Source62:	kolab.schema
# from evolution package
Source63:	evolutionperson.schema
# from rfc2739, updated schema for correctness, used by evo for calendar attrs
Source64:	calendar.schema
# from README.LDAP in sudo (pre-1.6.8) CVS:
Source65:	sudo.schema
# from bind sdb_ldap page: http://www.venaas.no/ldap/bind-sdb/dnszone-schema.txt
Source66:	dnszone.schema
# from http://cvs.pld.org.pl/SOURCES/openldap-dhcp.schema
Source67:	dhcp.schema
# Chris Patches
Patch0: 	%{name}-2.3.4-config.patch
Patch1:		%{name}-2.0.7-module.patch
#
# For now only build support for SMB (no krb5) changing support in smbk5passwd overlay:
Patch2:		openldap-2.3.4-smbk5passwd-only-smb.patch
# RH + PLD Patches
Patch6: 	%{name}-2.0.3-krb5-1.1.patch
Patch8:		%{name}-conffile.patch
Patch10:	%{name}-sql.patch
Patch12:	%{name}-syslog.patch
Patch15:	%{name}-cldap.patch
# additional modules
Patch20:	openldap-2.2.23-smbk5passwd-cvs-20050314.patch
Patch21:	openldap-2.2.23-smbk5passwd-cvs-20050314-upcasehash.patch
# Migration tools Patch
Patch40: 	MigrationTools-34-instdir.patch
Patch41: 	MigrationTools-36-mktemp.patch
Patch42: 	MigrationTools-27-simple.patch
Patch43: 	MigrationTools-26-suffix.patch
Patch45:	MigrationTools-45-i18n.patch
# schema patch
Patch46: 	openldap-2.0.21-schema.patch
# maildrop schema
Patch47:	openldap-2.0.27-maildrop.schema.patch
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
Patch100:	openldap-2.3.9-its4035.patch


BuildRoot: 	%{_buildroot}/%{name}-%{version}-root
%{?_with_cyrussasl:BuildRequires: 	libsasl-devel}
%{?_with_kerberos:BuildRequires:	krb5-devel}
BuildRequires:	openssl-devel, perl, autoconf2.5, ed
#BuildRequires: libgdbm1-devel
%if %sql
BuildRequires: 	unixODBC-devel
%endif
%if %back_perl
BuildRequires:	perl-devel
%endif
%if !%db4_internal
BuildRequires: 	db%{dbname}-devel >= %{dbver}
%endif
BuildRequires:  ncurses-devel >= 5.0, tcp_wrappers-devel, libtool-devel
# for make test:
BuildRequires:	diffutils

Requires: 	%{libname} = %{version}-%{release}
Requires:	shadow-utils, setup >= 2.2.0-6mdk


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
Requires(pre): 	/usr/sbin/useradd
Requires(pre):	rpm-helper
Requires(post):	afterboot, rpm-helper
Requires(postun): mkafterboot, rpm-helper
%if !%db4_internal
Requires(pre):	db4-utils
Requires(post):	db4-utils
Requires:	db4-utils
%endif
Provides:	%{name}-back_dnssrv = %{version}-%{release}
Provides:	%{name}-back_ldap = %{version}-%{release}
Provides:	%{name}-back_passwd = %{version}-%{release}
Provides:	%{name}-back_sql = %{version}-%{release}
Obsoletes:	%{name}-back_dnssrv < %{version}-%{release}
Obsoletes:	%{name}-back_ldap < %{version}-%{release}
Obsoletes:	%{name}-back_passwd < %{version}-%{release}
Obsoletes:	%{name}-back_sql < %{version}-%{release}

Requires: 	%{libname} = %{version}-%{release}

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
Group: 		System/Configuration/Other
Requires: 	%{name}-servers = %{version}-%{release}
Requires: 	%{name}-clients = %{version}-%{release}
Requires: 	perl-MIME-Base64

%description migration
This package contains a set of scripts for migrating data from local files
(ie /etc/passwd) or a nis domain to an ldap directory.


%package -n %{libname}
Summary: 	OpenLDAP libraries
Group: 		System/Libraries
Provides:       lib%{fname} = %{version}-%{release}
# This is needed so all libldap2 applications get /etc/openldap/ldap.conf
# which was moved from openldap-clients to openldap in 2.1.29-1avx
Requires:	openldap >= 2.1.29-1avx

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


%prep
%if %db4_internal
%setup -q -a 11 -a 30
pushd db-%{dbver} >/dev/null
# upstream patches
%patch50
%patch51
%patch55
%patch56

#%patch57 -b .txn_nolog
patch -p0 -b -z .txn_nolog < ../build/BerkeleyDB42.patch

%patch52 -p1 -b .amd64-mutexes
(cd dist && ./s_config)
popd >/dev/null
%else
%setup -q -a 11
%endif

# Chris patches
%patch0 -p1 -b .config
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
%patch100 -p0 -b .its4035

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
#rh only:
export CPPFLAGS="-I%{_prefix}/kerberos/include $CPPFLAGS"
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

%if %db4_internal
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
install -m 0740 %{SOURCE22} %{buildroot}%{_srvdir}/slapd/run
install -m 0740 %{SOURCE23} %{buildroot}%{_srvdir}/slapd/log/run
install -m 0740 %{SOURCE24} %{buildroot}%{_srvdir}/slurpd/run
install -m 0740 %{SOURCE25} %{buildroot}%{_srvdir}/slurpd/log/run

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/ldap

install -m 640 %{SOURCE21} %{SOURCE6} %{SOURCE7} %{buildroot}%{_sysconfdir}/openldap

### repository dir
install -d %{buildroot}%{_var}/lib/ldap

### DB_CONFIG for bdb backend
install -m 644 %{SOURCE5} %{buildroot}%{_var}/lib/ldap

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
	%{SOURCE60} %{SOURCE61} %{SOURCE62} %{SOURCE63} %{SOURCE64} \
	%{SOURCE65} %{SOURCE66} %{SOURCE67} ; do
install -m 644 $i %{buildroot}%{_datadir}/openldap/schema/
done

mkdir -p %{buildroot}%{_datadir}/openldap/scripts
install -m 755 %{SOURCE8} %{SOURCE9} %{buildroot}%{_datadir}/openldap/scripts/

### create local.schema
echo "# This is a good place to put your schema definitions " > %{buildroot}%{_sysconfdir}/openldap/schema/local.schema
chmod 644 %{buildroot}%{_sysconfdir}/openldap/schema/local.schema

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

mkdir -p %{buildroot}%{_sysconfdir}/ssl/openldap

mv %{buildroot}/var/run/ldap/openldap-data/DB_CONFIG.example %{buildroot}/%{_var}/lib/ldap/

# afterboot snippet
mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE12} %{buildroot}%{_datadir}/afterboot/10_openldap


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
MIGRATE=`%{_sbindir}/slapd -V 2>&1|while read a b c d e;do case $d in (2.3.*) echo nomigrate;;(2.*) echo migrate;;esac;done`

if [ "$1" -ne 1 -a -e "$SLAPDCONF" -a "$MIGRATE" != "nomigrate" ]; then
    SLAPD_STATUS=`runsvstat /service/slapd 2>/dev/null|grep -q down;echo $?`
    [ $SLAPD_STATUS -eq 1 ] && srv --down slapd
    #`awk '/^[:space:]*directory[:space:]*\w*/ {print $2}' /etc/%{name}/slapd.conf`
    dbs=`awk 'BEGIN {OFS=":"} /[:space:]*^database[:space:]*\w*/ {db=$2;suf="";dir=""}; /^[:space:]*suffix[:space:]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm"||db=="hdb")&&(suf!=""&&dir!="")) print dir,suf};/^[:space:]*directory[:space:]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm"||db="hdb")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g'`
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
        if [ "`runsvstat /service/syslogd 2>/dev/null|grep -q run; echo $?`" == "0" ]; then
            runsvctrl h /service/syslogd  > /dev/null 2>/dev/null || : 
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

for i in slapd slurpd
do
    if [ -d /var/log/supervise/$i -a ! -d /var/log/service/$i ]; then
        mv /var/log/supervise/$i /var/log/service/
    fi
done
%_post_srv slapd
%_post_srv slurpd
%_mkafterboot

# nscd reset
if [ "`runsvstat /service/nscd 2>/dev/null|grep -q run; echo $?`" == "0" ]; then
    runsvctrl h /service/nscd  > /dev/null 2>/dev/null || : 
fi


%preun servers
%_preun_srv slapd


%postun servers
/sbin/ldconfig
if [ $1 = 0 ]; then 
    # remove ldap entry 
    perl -pi -e "s|^.*ldap.*\n||g" %{_sysconfdir}/syslog.conf 

    # reset syslog daemon
    if [ "`runsvstat /service/syslogd 2>/dev/null|grep -q run; echo $?`" == "0" ]; then
        runsvctrl h /service/syslogd  > /dev/null 2>/dev/null || : 
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
%doc ANNOUNCEMENT CHANGES COPYRIGHT LICENSE README 
%doc doc/rfc doc/drafts
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
%doc README.migration TOOLS.migration
%{_datadir}/openldap/migration


%files servers
%defattr(-,root,root)
%doc contrib/slapd-modules/smbk5pwd/README.smbk5passwd
%dir %{_sysconfdir}/openldap
%dir %{_sysconfdir}/openldap/schema
#%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/ssl/openldap/ldap.pem
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/openldap/slapd.conf
%attr(0640,root,ldap) %{_sysconfdir}/openldap/DB_CONFIG.example
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/openldap/slapd.access.conf

%dir %{_sysconfdir}/ssl/openldap
%config(noreplace) %{_sysconfdir}/openldap/schema/*.schema
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
%{_bindir}/*
%{_mandir}/man1/*
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


# TODO:
# - add cron-job to remove transaction logs (bdb)


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sun Jan 08 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

