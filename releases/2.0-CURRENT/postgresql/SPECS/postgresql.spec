#
# spec file for package postgresql
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		postgresql
%define version		8.1.4
%define release		%_revrel

%define _requires_exceptions devel(libtcl8.4)\\|devel(libtcl8.4(64bit))

%define pyver		%(python -c 'import sys;print(sys.version[0:3])')
%define perl_version	%(rpm -q --qf "%{VERSION}" perl)
%define perl_epoch	%(rpm -q --qf "%{EPOCH}" perl)

%define pgdata		/var/lib/pgsql
%define logrotatedir	%{_sysconfdir}/logrotate.d

%define major		4
%define major_ecpg	5
%define jdbc		312

%define current_major_version 8.1

%define libname		%mklibname pq %{major}
%define libecpg		%mklibname ecpg %{major_ecpg}

Summary: 	PostgreSQL client programs and libraries
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Databases
URL:		http://www.postgresql.org/ 

Source0:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source5:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2.md5
Source8:	logrotate.postgresql
Source10:	postgresql-mdk_update.tar.bz2
Source14:	mdk-pgdump.sh
Source20:	postgresql.run
Source21:	postgresql-log.run
Source22:	postgresql.sysconfig
Source23:	01_postgresql.afterboot
Source24:	postgresql.finish
Source53:	CAN-2005-1409-1410-update-dbs.sh
Patch0:		postgresql-7.4.1-mdk-pkglibdir.patch
Patch1:		postgresql-7.4.5-CAN-2005-0227.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	termcap-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	python-devel
BuildRequires:	readline-devel >= 4.3
BuildRequires:	zlib-devel, tcl

Requires:	perl
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Provides:	postgresql-clients
Obsoletes:	postgresql-clients

%description
PostgreSQL is an advanced Object-Relational database management system
(DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). The
postgresql package includes the client programs and libraries that
you'll need to access a PostgreSQL DBMS server.  These PostgreSQL
client programs are programs that directly manipulate the internal
structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL
server, or may be on a remote machine which accesses a PostgreSQL
server over a network connection. This package contains the client
libraries for C and C++, as well as command-line utilities for
managing PostgreSQL databases on a PostgreSQL server. 

If you want to manipulate a PostgreSQL database on a remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql-server package.


%package -n %{libname}
Summary:	The shared libraries required for any PostgreSQL clients
Group:		System/Libraries
Obsoletes:	postgresql-libs
Provides:	postgresql-libs = %{version}-%{release}
Provides:	libpq = %{version}-%{release}
Conflicts:	%{_lib}pq3 = 8.0.1

%description -n %{libname}
C and C++ libraries to enable user programs to communicate with the
PostgreSQL database backend. The backend can be on another machine and
accessed through TCP/IP.


%package -n %{libname}-devel
Summary:	Development library for libpq
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	postgresql-libs-devel = %{version}-%{release}
Provides:	libpq-devel = %{version}-%{release}
Conflicts:	%{_lib}pg3-devel = 8.0.1

%description -n %{libname}-devel
Development libraries for libpq


%package -n %{libecpg}
Summary:	Shared library libecpg for PostgreSQL
Group:		System/Libraries
Requires:	postgresql = %{version}-%{release}
Provides:	libecpg = %{version}-%{release}

%description -n %{libecpg}
Libecpg is used by programs built with ecpg (Embedded PostgreSQL for C)
Use postgresql-dev to develop such programs.


%package -n %{libecpg}-devel
Summary:	Development library to libecpg
Group:		Development/C
Requires:	%{libecpg} = %{version}-%{release}
Provides:	libecpg-devel = %{version}-%{release} 

%description -n %{libecpg}-devel
Development library to libecpg.


%package server
Summary:	The programs needed to create and run a PostgreSQL server
Group:		Databases
Provides:	sqlserver
Provides:	%{name}-server-ABI = %{current_major_version}
Requires(post):	rpm-helper
Requires(post):	afterboot
Requires(post):	%{libname} > %{version}-%{release}
Requires(post):	postgresql = %{version}-%{release}
Requires(postun): rpm-helper
Requires(postun): afterboot
Requires(pre):	rpm-helper
Requires(pre):	postgresql = %{version}-%{release}
Requires(preun): rpm-helper
Conflicts:	postgresql < 7.3

%description server
The postgresql-server package includes the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.  PostgreSQL is an advanced
Object-Relational database management system (DBMS) that supports
almost all SQL constructs (including transactions, subselects and
user-defined types and functions). You should install
postgresql-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need
to install the postgresql and postgresql-devel packages.


%package contrib
Summary:	Contributed binaries distributed with PostgreSQL
Group:		Databases
Requires:	postgresql = %{version}-%{release}
Requires:	perl(Pg)

%description contrib
The postgresql-contrib package includes the contrib tree distributed with
the PostgreSQL tarball.  Selected contrib modules are prebuilt.


%package devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Databases
Requires:	postgresql = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libecpg} = %{version}-%{release}

%description devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server. If
you're installing postgresql-server, you need to install this
package.


%package pl
Summary:	The PL/Perl procedural language for PostgreSQL
Group:		Databases
Obsoletes:	libpgsql2
Requires:	postgresql = %{version}
Requires:	perl-base = %{perl_epoch}:%{perl_version}

%description pl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pl package contains the the PL/Perl, PL/Tcl,
and PL/Python procedural languages for the backend.  PL/Pgsql is part
of the core server package.


%package test
Summary:	The test suite distributed with PostgreSQL
Group:		Databases
Requires:	postgresql >= %{version}-%{release}
Requires:	postgresql-pl = %{version}-%{release}

%description test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 10
%patch0 -p0 -b .pkglibdir
%patch1 -p1 -b .can-2005-0227


%build
pushd src
    #(deush) if libtool exist, copy some files 
    if [ -d %{_datadir}/libtool ]; then
        cp %{_datadir}/libtool/config.* .
    fi

    # doesn't build on PPC with full optimization (sb)
    %ifnarch ppc
        CFLAGS="${CFLAGS:-%{optflags}}" ; export CFLAGS
        CXXFLAGS="${CXXFLAGS:-%{optflags}}" ; export CXXFLAGS
    %endif

    #fix -ffast-math problem (deush)
    %ifnarch ppc
        %serverbuild
        CFLAGS=`echo %{optflags}|xargs -n 1|grep -v ffast-math|xargs -n 100`
    %endif
popd

%configure --disable-rpath \
            --enable-hba \
	    --enable-locale \
	    --enable-multibyte \
	    --enable-syslog\
	    --with-CXX \
	    --enable-odbc \
	    --with-perl \
	    --with-python \
	    --without-tcl \
            --without-tk \
            --with-openssl \
            --with-pam \
            --libdir=%{_libdir} \
	    --datadir=%{_datadir}/pgsql \
	    --with-docdir=%{_docdir} \
	    --includedir=%{_includedir}/pgsql \
	    --mandir=%{_mandir} \
	    --prefix=%{_prefix} \
	    --sysconfdir=%{_sysconfdir}/pgsql \
            --enable-nls

# $(rpathdir) come from Makefile
perl -pi -e 's|^all:|LINK.shared=\$(COMPILER) -shared -Wl,-rpath,\$(rpathdir),-soname,\$(soname)\nall:|' src/pl/plperl/GNUmakefile

%make pkglibdir=%{_libdir}/pgsql all
%make -C contrib pkglibdir=%{_libdir}/pgsql all

pushd src/test
    make all
popd


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make DESTDIR=%{buildroot} pkglibdir=%{_libdir}/pgsql install 
make -C contrib DESTDIR=%{buildroot} pkglibdir=%{_libdir}/pgsql install

# install odbcinst.ini
mkdir -p %{buildroot}%{_sysconfdir}/pgsql

# copy over Makefile.global to the include dir....
install -m 0755 src/Makefile.global %{buildroot}%{_includedir}/pgsql/

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 0700 %{buildroot}/var/lib/pgsql/data

# backups of data go here...
install -d -m 0700 %{buildroot}/var/lib/pgsql/backups

# tests. There are many files included here that are unnecessary, but include
# them anyway for completeness.
mkdir -p %{buildroot}%{_libdir}/pgsql/test
cp -a src/test/regress %{buildroot}%{_libdir}/pgsql/test
install -m 0755 contrib/spi/refint.so %{buildroot}%{_libdir}/pgsql/test/regress
install -m 0755 contrib/spi/autoinc.so %{buildroot}%{_libdir}/pgsql/test/regress
pushd  %{buildroot}%{_libdir}/pgsql/test/regress/
    strip *.so
popd

install -m 0755 %{_sourcedir}/mdk-pgdump.sh %{buildroot}%{_bindir}/avx-pgdump.sh
install -D -m 0755 mdk/mdk_update_dump.sh %{buildroot}%{_datadir}/pgsql/avx/avx_update_dump
install -m 0755 mdk/mdk_update_restore.sh %{buildroot}%{_datadir}/pgsql/avx/avx_update_restore

mv %{buildroot}%{_docdir}/%{name}/html %{buildroot}%{_docdir}/%{name}-docs-%{version}

mkdir -p %{buildroot}%{_srvdir}/postgresql/log
install -m 0740 %{_sourcedir}/postgresql.run %{buildroot}%{_srvdir}/postgresql/run
install -m 0740 %{_sourcedir}/postgresq-log.run %{buildroot}%{_srvdir}/postgresql/log/run
install -m 0740 %{_sourcedir}/postgresql.finish %{buildroot}%{_srvdir}/postgresql/finish

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 %{_sourcedir}/postgresql.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/postgresql

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/01_postgresql.afterboot %{buildroot}%{_datadir}/afterboot/01_postgresql

# contrib docs
# make this --short-circuit friendly
rm -rf contrib-docs && mkdir contrib-docs
cp -f contrib/*/README.* contrib-docs/
cp -f contrib/spi/*.example contrib-docs/

%find_lang libpq
%find_lang libecpg
%find_lang pg_dump
%find_lang postgres
%find_lang psql
%find_lang pg_resetxlog
%find_lang pg_controldata
%find_lang pgscripts
%find_lang initdb
%find_lang pg_config
%find_lang pg_ctl

cat pg_ctl.lang initdb.lang pg_config.lang psql.lang pg_dump.lang pgscripts.lang > main.lst
cat postgres.lang pg_resetxlog.lang pg_controldata.lang > server.lst
# 20021226 warly waiting to be able to add a major in po name
cat libpq.lang libecpg.lang >> main.lst

# taken directly in build dir.
rm -fr %{buildroot}%{_datadir}/doc/postgresql/contrib/

rm -rf %{buildroot}%{_docdir}/%{name}-docs-%{version}

# postgres' .bash_profile
cat > %{buildroot}/var/lib/pgsql/.bashrc <<EOF
# Default database location
PGDATA=%{pgdata}

# Setting up minimal envirronement
[ -f /etc/sysconfig/i18n ] && . /etc/sysconfig/i18n
[ -f /etc/sysconfig/postgresql ] && . /etc/sysconfig/postgresql

export LANG LC_ALL LC_CTYPE LC_COLLATE LC_NUMERIC LC_CTYPE LC_TIME
export PGDATA
PS1="[\u@\h \W]\\$ "
EOF



%pre server
%_pre_useradd postgres %{pgdata} /bin/bash 75


%post server
/sbin/ldconfig
%_mkafterboot

PGDATA="%{pgdata}/data"
# create the database if it doesn't exist
if [ ! -f $PGDATA/PG_VERSION ] && [ ! -d $PGDATA/base ]; then
    if [ ! -d $PGDATA ]; then
        mkdir -p $PGDATA
        chown postgres:postgres $PGDATA
        chmod 0700 $PGDATA
    fi
    # Make sure the locale from the initdb is preserved for later startups...
    [ -f %{_sysconfdir}/sysconfig/i18n ] && cp %{_sysconfdir}/sysconfig/i18n $PGDATA/../initdb.i18n
    # Just in case no locale was set, use en_US
    [ ! -f %{_sysconfdir}/sysconfig/i18n ] && echo "LANG=en_US" >$PGDATA/../initdb.i18n
    # Is expanded this early to be used in the command su runs
    echo "export LANG LC_ALL LC_CTYPE LC_COLLATE LC_NUMERIC LC_TIME" >> $PGDATA/../initdb.i18n
    # Initialize the database
    /sbin/chpst -u postgres /usr/bin/initdb --pgdata=$PGDATA >/dev/null 2>&1 </dev/null
    [ -f $PGDATA/PG_VERSION ] && echo "Database successfully initialized!"
    [ ! -f $PGDATA/PG_VERSION ] && echo "Database was NOT successfully initalized!"
fi

if [ $1 -gt 1 ]; then
    echo "" 
    echo "After install, you must run %{_docdir}/%{name}-doc-%{version}/CAN-2005-1409-1410-update-dbs.sh"
    echo "in order to upgrade your databases to protect against the vulnerabilities described in CAN-2005-1409"
    echo "and CAN-2005-1410.  PostgreSQL must be running when you run this script.  Note that this script is"
    echo "provided in the postgresql-doc package."
    echo "" 
fi
%_post_srv postgresql


%preun server
%_preun_srv postgersql


%postun server
/sbin/ldconfig
%_mkafterboot
%_postun_userdel postgres


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post -n %{libecpg} -p /sbin/ldconfig
%postun -n %{libecpg} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f main.lst 
%defattr(-,root,root)
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createlang
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/droplang
%{_bindir}/dropuser
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createlang.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/droplang.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/psql.*
%{_mandir}/man1/reindexdb.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man7/*
%{_datadir}/pgsql/avx/avx_update_dump
%{_datadir}/pgsql/avx/avx_update_restore

%files -n %{libname} 
%defattr(-,root,root)
%{_libdir}/libpq.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libpq.so

%files -n %{libecpg}
%defattr(-,root,root)
%{_libdir}/libecpg.so.*
%{_libdir}/libecpg_compat.so.*
%{_libdir}/libpgtypes.so.*

%files -n %{libecpg}-devel
%defattr(-,root,root)
%{_libdir}/libecpg.so

%files contrib
%defattr(-,root,root)
%{_libdir}/pgsql/_int.so
%{_libdir}/pgsql/btree_gist.so
%{_libdir}/pgsql/chkpass.so
%{_libdir}/pgsql/cube.so
%{_libdir}/pgsql/dblink.so
%{_libdir}/pgsql/earthdistance.so
%{_libdir}/pgsql/fti.so
%{_libdir}/pgsql/fuzzystrmatch.so
%{_libdir}/pgsql/insert_username.so
%{_libdir}/pgsql/int_aggregate.so
%{_libdir}/pgsql/isbn_issn.so
%{_libdir}/pgsql/lo.so
%{_libdir}/pgsql/ltree.so
%{_libdir}/pgsql/moddatetime.so
%{_libdir}/pgsql/pending.so
%{_libdir}/pgsql/pgcrypto.so
%{_libdir}/pgsql/pgstattuple.so
%{_libdir}/pgsql/refint.so
%{_libdir}/pgsql/seg.so
%{_libdir}/pgsql/tablefunc.so
%{_libdir}/pgsql/timetravel.so
%{_libdir}/pgsql/tsearch2.so
%{_libdir}/pgsql/user_locks.so
%{_libdir}/pgsql/pg_trgm.so
%{_libdir}/pgsql/autoinc.so
%{_libdir}/pgsql/pg_buffercache.so
%{_datadir}/pgsql/contrib/
%{_bindir}/dbf2pg
%{_bindir}/fti.pl
%{_bindir}/oid2name
%{_bindir}/pgbench
%{_bindir}/vacuumlo
%{_bindir}/DBMirror.pl
%{_bindir}/clean_pending.pl

%files server -f server.lst
%defattr(-,root,root)
%{_bindir}/initdb
%{_bindir}/ipcclean
%{_bindir}/pg_controldata 
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_bindir}/avx-pgdump.sh
%{_mandir}/man1/initdb.1*
%{_mandir}/man1/ipcclean.1*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.1*
%{_mandir}/man1/pg_resetxlog.*
%{_mandir}/man1/postgres.1*
%{_mandir}/man1/postmaster.1*
%{_datadir}/pgsql/postgres.bki
%{_datadir}/pgsql/postgres.description
%{_datadir}/pgsql/*.sample
%{_datadir}/pgsql/timezone
%{_datadir}/pgsql/system_views.sql
%dir %{_libdir}/pgsql
%dir %{_datadir}/pgsql
%attr(0700,postgres,postgres) %dir %{pgdata}
%attr(0700,postgres,postgres) %dir %{pgdata}/data
%attr(0700,postgres,postgres) %dir %{pgdata}/backups
%attr(0644,postgres,postgres) %config(noreplace) %{_localstatedir}/pgsql/.bashrc
%{_libdir}/pgsql/*_and_*.so
%{_datadir}/pgsql/conversion_create.sql
%{_datadir}/pgsql/information_schema.sql
%{_datadir}/pgsql/sql_features.txt
%dir %attr(0750,root,admin) %{_srvdir}/postgresql
%dir %attr(0750,root,admin) %{_srvdir}/postgresql/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/postgresql/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/postgresql/finish
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/postgresql/log/run
%config(noreplace) %{_sysconfdir}/sysconfig/postgresql
%{_datadir}/afterboot/01_postgresql

%files devel
%defattr(-,root,root)
%{_includedir}/pgsql
%{_bindir}/ecpg
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/pgsql/pgxs/
%{_mandir}/man1/ecpg.1*
%{_bindir}/pg_config
%{_mandir}/man1/pg_config.1*

%files pl 
%defattr(-,root,root) 
%{_libdir}/pgsql/plperl.so 
%{_libdir}/pgsql/plpython.so 
%{_libdir}/pgsql/plpgsql.so

%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{_libdir}/pgsql/test/*
%attr(-,postgres,postgres) %dir %{_libdir}/pgsql/test

%files doc
%defattr(-,root,root)
%doc doc/FAQ doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* doc/TODO doc/TODO.detail
%doc COPYRIGHT README HISTORY doc/bug.template
%doc contrib-docs


%changelog
* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.1.4
- rebuild against new openssl
- spec cleanups

* Sat Jun 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.1.4
- rebuild against new pam

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.1.4
- rebuild against new readline

* Sat Jun 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.1.4
- rebuild against new python

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.1.4
- drop the jdbc stuff
- drop P2; merged upstream
- dropped a bunch of no more needed sources
- remove the pg_autovacuum service
- update the login script for user postgres (nanardon)
- rebuild with gcc4

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.0.7
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Tue Feb 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.0.7
- 8.0.7 (minor bugfixes)

* Wed Feb 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.0.6
- 8.0.6

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.0.4
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.0.4
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.0.4
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Oct 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.4-1avx
- 8.0.4 (contains some pretty important bugfixes)
- updated jar files

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.3-5avx
- rebuild against new readline and new python

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.3-4avx
- s/supervise/service/ in log/run

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.3-3avx
- use execlineb for run scripts
- move logdir to /var/log/service/postgresql
- run scripts are now considered config files and are not replaceable
- add %%post/%%preun scripts for pg_autovacuum service

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.3-2avx
- fix perms on run scripts

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.3-1avx
- 8.0.3
- fix major lib number (nanardon)
- move pgxs files from contrib to devel; postgresql external
  contributions do not require -contrib to be built anymore (nanardon)
- drop P3 and P4; merged upstream
- rediff P2; partially merged upstream
- conflict with older lib packages with bad major

* Sat Jun 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.1-6avx
- P3: fix CAN-2005-1409
- P4: fix CAN-2005-1410
- S53: upgrade script to update databases
- spec cleanups

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.1-5avx
- bootstrap build

* Wed Mar 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.1-4avx
- fix plperl linkage over libperl.so for all archs (nanardon)
- patches to fix CAN-2005-0227, CAN-2005-0245, CAN-2005-0247
- fix requires on perl
- don't require sfio
- renumber patches

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.1-3avx
- use logger for logging

* Wed Feb 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.1-2avx
- update the afterboot snippet to mention upgrading tips
- s/su/chpst/ in the spec

* Tue Feb 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.0.1-1avx
- 8.0.1
- build without tcl support

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.4.3-8avx
- drop BuildRequires on XFree86-devel
- rebuild against new python and perl

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.4.3-7avx
- rebuild against latest openssl

* Tue Dec 07 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.4.3-6avx
- P4: patch to fix CAN-2004-0977

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.4.3-5avx
- update run scripts and afterboot manpages
- add a finish script

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.4.3-4avx
- rebuild against new openssl

* Mon Jul 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.4.3-3avx
- fix the requires exceptions

* Wed Jul 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.4.3-2avx
- remove unapplied patches; renumber remaining patches

* Mon Jul 05 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.4.3-1avx
- 7.4.3
- use bzip sources
- new jdbc jar files for 7.4 (build 214)
- include new mdk update scripts (re-branded to avx)
- BuildRequires: s/libtermcap-devel/termcap-devel, tcl
- P9: fixes location of pkglibdir in pg_regress test (mdk bug #9148)
- postgresql-test requires postgresql-pl (mdk bug #9149) so pg_regress
  test works properly
- update P4 and P7 from Mandrake (7.4.1-6mdk)
- put the .sample files back; they're needed for initdb otherwise
  we can't make a new database
- remove postgresql-python; according to the HISTORY file:
    "The Python language no longer supports a restricted execution
     environment, so the trusted version of PL/Python was removed. If
     this situation changes, a version of PL/Python that can be used by
     non-superusers will be readded."
- add a requires exception on devel(libtcl8.4)

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.3.4-10avx
- Annvix build

* Thu Apr 22 2004 Vincent Danen <vdanen@opensls.org> 7.3.4-9sls
- include default config files (not .sample) so we can run postgres "out of
  the box" and mark them as %%config
- don't create /var/log/postgresql if nothing is going to use it
- fix run script to trap on exit and remove $PGDATA/postmaster.pid otherwise
  we'll have a real hard time restarting the service next time
- also redirect stderr to stdout for logging in run script
- remove S10 (README.postgresql.mdk) as that data is in the afterboot man
  section now

* Mon Apr 12 2004 Vincent Danen <vdanen@opensls.org> 7.3.4-8sls
- include epoch in perl requirements for -pl

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 7.3.4-7sls
- minor spec cleanups

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 7.3.4-6sls
- add afterboot snippet
- use %%_mkafterboot macro
- Requires: afterboot

* Tue Jan 27 2004 Vincent Danen <vdanen@opensls.org> 7.3.4-5sls
- use srv macros
- postgres user has static uid/gid of 75

* Sun Jan 25 2004 Vincent Danen <vdanen@opensls.org> 7.3.4-4sls
- init the db in %%post
- don't try to do the admin's work for them; we don't want to be responsible
  for something going wrong so remove all stuff to automate dumps/restores
- remove %%build_opensls macros
- supervise scripts
- remove icons
- remove initscript
- make /etc/sysconfig/postgresql to hold some options for the supervise
  script

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 7.3.4-3sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to not build -doc package
