%define name	postgresql
%define version	7.3.4
%define release	8sls

%{expand:%%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{expand:%%define perl_version %(rpm -q --qf %{EPOCH}:%{VERSION} perl)}

%define pgdata		/var/lib/pgsql
%define logrotatedir	%{_sysconfdir}/logrotate.d

%define major		3
%define major_tcl	2
%define major_ecpg	3

%define current_major_version 7.3

%define libname		%mklibname pq %{major}
%define libpgtcl	%mklibname pgtcl %{major_tcl}
%define libecpg		%mklibname ecpg %{major_ecpg}

Summary: 	PostgreSQL client programs and libraries.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Databases
URL:		http://www.postgresql.org/ 
Source0:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz
Source1:	http://jdbc.postgresql.org/download/pg73jdbc1.jar 
Source2:	http://jdbc.postgresql.org/download/pg73jdbc2.jar 
Source3:	http://jdbc.postgresql.org/download/pg73jdbc3.jar
Source4:	http://www.rbt.ca/postgresql/upgrade/upgrade.pl
Source5:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz.md5
Source6:	ftp.postgresql.org:/pub/binary/v7.2/RPMS/README.rpm-dist.bz2
Source7:	migration-scripts.tar.gz
Source8:	logrotate.postgresql
Source9:	http://jdbc.postgresql.org/download/pg73jdbc2ee.jar
Source10:	README.postgresql.mdk
# Daouda : script for dumping database (from RedHat)
Source14:	mdk-pgdump.sh
Source15:	postgresql-bashprofile
Source20:	postgresql.run
Source21:	postgresql-log.run
Source22:	postgresql.sysconfig
Source23:	01_postgresql.afterboot
Source51:	README.v7.3
Source52:	upgrade_tips_7.3
Patch1:		rpm-pgsql-7.2.patch.bz2
Patch2:		postgresql-7.2rc2-betterquote.patch.bz2
Patch4:		postgresql-7.3-tighten.patch.bz2
Patch5:		pgaccess-7.2.patch.bz2
Patch6:		postgresql-7.2.1-perl-use-INSTALLDIRS-vendor.patch.bz2
Patch7:		postgresql-7.3.3-pythondir.patch.bz2
Patch8:		postgresql-7.3.4-amd64-testsuite.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	XFree86-devel bison flex gettext libtermcap-devel ncurses-devel openssl-devel pam-devel
BuildRequires:	perl-devel python-devel readline-devel >= 4.3 tk zlib-devel

Requires:	perl sfio
Prereq:		rpm-helper
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
Summary:	The shared libraries required for any PostgreSQL clients.
Group:		System/Libraries
Obsoletes:	postgresql-libs
Provides:	postgresql-libs = %{version}-%{release} libpq = %{version}-%{release}

%description -n %{libname}
C and C++ libraries to enable user programs to communicate with the
PostgreSQL database backend. The backend can be on another machine and
accessed through TCP/IP.

%package -n %{libname}-devel
Summary:	Development library for libpq2
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	postgresql-libs-devel = %{version}-%{release} libpq-devel = %{version}-%{release}

%description -n %{libname}-devel
Development libraries for libpq

%package -n %{libpgtcl}
Summary:	Tcl/Tk library and front-end for PostgreSQL.
Group:		System/Libraries
Requires:	tcl => 8.0
Provides:	libpgtcl = %{version}-%{release}

%description -n %{libpgtcl}
A library to enable Tcl/Tk scripts to communicate with the PostgreSQL
database backend.

%package -n %{libpgtcl}-devel
Summary:	Tcl/Tk development library and front-end for PostgreSQL.
Group:		Development/C
Requires:	%{libpgtcl} = %{version}-%{release}
Provides:	libpgtcl-devel = %{version}-%{release} 

%description -n %{libpgtcl}-devel
Development library to libpgtcl2.

%package -n %{libecpg}
Summary:	Shared library libecpg for PostgreSQL
Group:		System/Libraries
Requires:	postgresql = %{version}-%{release}
Provides:	libecpg = %{version}-%{release}

%description -n %{libecpg}
Libecpg is used by programs built with ecpg (Embedded PostgreSQL for C)
Use postgresql-dev to develop such programs.

%package -n %{libecpg}-devel
Summary:	Development library to libecpg.
Group:		Development/C
Requires:	%{libecpg} = %{version}-%{release}
Provides:	libecpg-devel = %{version}-%{release} 

%description -n %{libecpg}-devel
Development library to libecpg.

%package server
Summary:	The programs needed to create and run a PostgreSQL server.
Group:		Databases
Provides:	sqlserver
Prereq:		rpm-helper %{_sbindir}/useradd afterboot
Requires:	postgresql = %{version}-%{release}
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

If you never played with PostgreSQL before, please read README.mdk.

%package contrib
Summary:	Contributed binaries distributed with PostgreSQL
Group:		Databases
Requires:	libpq = %{version}-%{release} postgresql = %{version}-%{release}
Requires:	libpq = %{version}-%{release} 
Requires:	perl-Pg

%description contrib
The postgresql-contrib package includes the contrib tree distributed with
the PostgreSQL tarball.  Selected contrib modules are prebuilt.

%package devel
Summary:	PostgreSQL development header files and libraries.
Group:		Development/Databases
Requires:	postgresql = %{version}-%{release} libpq = %{version}-%{release}
Requires:	%{libpgtcl} = %{version}-%{release}
Requires:	%{libecpg} = %{version}-%{release}
# Requires:	libpgsqlodbc = %{version}-%{release}

%description devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server. If
you're installing postgresql-server, you need to install this
package.

%package pl
Summary:	The PL/Perl procedural language for PostgreSQL.
Group:		Databases
Obsoletes:	libpgsql2
Requires:	postgresql = %{version} perl-base = %{perl_version}

%description pl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pl package contains the the PL/Perl, PL/Tcl, and PL/Python
procedural languages for the backend.  PL/Pgsql is part of the core server package.

%package tcl
Summary:	A Tcl client library, and the PL/Tcl procedural language for PostgreSQL.
Group:		Databases
Requires:	tcl >= 8.0 postgresql = %{version}-%{release}
Requires:	%{libpgtcl} = %{version}-%{release}

%description tcl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-tcl package contains the pg-enhanced pgtclsh, 
and the PL/Tcl procedural language for the backend.

%package python
Summary:	Development module for Python code to access a PostgreSQL DB.
Group:		Databases
Requires:	python >= %{pyver} postgresql = %{version}-%{release}

%description python
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-python package includes a module for
developers to use when writing Python code for accessing a PostgreSQL
database.

%package jdbc
Summary:	Files needed for Java programs to access a PostgreSQL database.
Group:		Databases
Requires:	postgresql = %{version}-%{release}

%description jdbc
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar file needed for
Java programs to access a PostgreSQL database.

%package test
Summary:	The test suite distributed with PostgreSQL.
Group:		Databases
Requires:	postgresql = %{version}-%{release}

%description test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.

%prep
%setup -q

# 20021202 warly to be tested
#   %patch1 -p1

# 20021202 warly merged upstream
#   %patch2 -p1

# %patch3 -p1
%patch4 -p1 -z .pg_hba

# 20021202 warly this file does not exist any more
#   %patch5 -p0 -z .pgaccess

# 20021203 warly interface moved from postgresql packages
#    %patch6 -p1 -z .pix
%patch7 -p1 -b .pythondir

# amd64 has comparable math precision to alpha
%patch8 -p1 -b .amd64-testsuite

%build

pushd src
#(deush) if libtool exist, copy some files 
if [ -d %{_datadir}/libtool ]
then
   cp %{_datadir}/libtool/config.* .
fi

# doesn't build on PPC with full optimization (sb)
%ifnarch ppc
CFLAGS="${CFLAGS:-$RPM_OPT_FLAGS}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-$RPM_OPT_FLAGS}" ; export CXXFLAGS
%endif

#fix -ffast-math problem (deush)
%ifnarch ppc
%serverbuild
CFLAGS=`echo $RPM_OPT_FLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
%endif
popd

./configure --disable-rpath \
            --enable-hba \
	    --enable-locale \
	    --enable-multibyte \
	    --enable-syslog\
	    --with-CXX \
	    --enable-odbc \
	    --with-perl \
	    --with-python \
	    --with-tcl --with-tclconfig=%{_libdir} \
            --without-tk \
            --with-openssl \
            --with-pam \
            --libdir=%{_libdir} \
	    --datadir=%{_datadir}/pgsql \
	    --docdir=%{_docdir} \
	    --includedir=%{_includedir}/pgsql \
	    --mandir=%{_mandir} \
	    --prefix=%_prefix \
	    --sysconfdir=%{_sysconfdir}/pgsql \
            --enable-nls

#make COPT="$CFLAGS" all

perl -pi -e 's|^all:|LINK.shared=\$(COMPILER) -shared -Wl,-rpath,/usr/lib/perl5/%{perl_version}/i386-linux-thread-multi/CORE,-soname,\$(soname)\nall:|' src/pl/plperl/GNUmakefile

make pkglibdir=%{_libdir}/pgsql all
make -C contrib pkglibdir=%{_libdir}/pgsql all

pushd src/test
make all
popd

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make DESTDIR=$RPM_BUILD_ROOT pkglibdir=%{_libdir}/pgsql install 
make -C contrib DESTDIR=$RPM_BUILD_ROOT pkglibdir=%{_libdir}/pgsql install

make DESTDIR=$RPM_BUILD_ROOT install-all-headers

install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_datadir}/pgsql
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/pgsql
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT/%{_datadir}/pgsql
install -m 755 %{SOURCE9} $RPM_BUILD_ROOT/%{_datadir}/pgsql

install -m 755 %{SOURCE4} $RPM_BUILD_ROOT/%{_datadir}/pgsql/upgrade.pl

# install the dump script
install -m755 %{SOURCE14} $RPM_BUILD_ROOT%{_bindir}/

# install odbcinst.ini
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pgsql

# 20021223 warly removed 
#install -m755 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/pgsql

# copy over Makefile.global to the include dir....
install -m755 src/Makefile.global $RPM_BUILD_ROOT%{_includedir}/pgsql/

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/backups

# postgres' .bash_profile
install -m 644 %{SOURCE15} $RPM_BUILD_ROOT/var/lib/pgsql/.bash_profile

# tests. There are many files included here that are unnecessary, but include
# them anyway for completeness.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pgsql/test
cp -a src/test/regress $RPM_BUILD_ROOT%{_libdir}/pgsql/test
install -m 0755 contrib/spi/refint.so $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
install -m 0755 contrib/spi/autoinc.so $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
pushd  $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/
strip *.so
popd

cp %{SOURCE51} %{SOURCE52} .

bzip2 -cd %{SOURCE6} >  README.rpm-dist

cp %{SOURCE10} README.mdk
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/html $RPM_BUILD_ROOT%{_docdir}/%{name}-docs-%{version}

mkdir -p %{buildroot}%{_srvdir}/postgresql/log
mkdir -p %{buildroot}%{_srvlogdir}/postgresql
install -m 0755 %{SOURCE20} %{buildroot}%{_srvdir}/postgresql/run
install -m 0755 %{SOURCE21} %{buildroot}%{_srvdir}/postgresql/log/run

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 %{SOURCE22} %{buildroot}%{_sysconfdir}/sysconfig/postgresql

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE23} %{buildroot}%{_datadir}/afterboot/01_postgresql

%find_lang libpq
%find_lang libecpg
%find_lang libpgtcl
%find_lang pg_dump
%find_lang postgres
%find_lang psql
%find_lang pg_resetxlog
%find_lang pg_controldata

cat psql.lang pg_dump.lang > main.lst
cat postgres.lang pg_resetxlog.lang pg_controldata.lang > server.lst
# 20021226 warly waiting to be able to add a major in po name
cat libpq.lang libecpg.lang libpgtcl.lang >> main.lst

# taken directly in build dir.
rm -fr $RPM_BUILD_ROOT%{_datadir}/doc/postgresql/contrib/

make check

rm -rf %{buildroot}%{_docdir}/%{name}-docs-%{version}

%pre server
%_pre_useradd postgres /var/lib/pgsql /bin/bash 75
if [ ! -e /var/log/postgresql ]; then
    touch /var/log/postgresql
fi
chown postgres:postgres /var/log/postgresql
chmod 0700 /var/log/postgresql


%post server
/sbin/ldconfig
%_mkafterboot

PGDATA="%{pgdata}/data"
# create the database if it doesn't exist
if [ ! -f $PGDATA/PG_VERSION ] && [ ! -d $PGDATA/base ]; then
  if [ ! -d $PGDATA ]; then
    mkdir -p $PGDATA
    chown postgres:postgres $PGDATA
    chmod 700 $PGDATA
  fi
  # Make sure the locale from the initdb is preserved for later startups...
  [ -f %{_sysconfdir}/sysconfig/i18n ] && cp %{_sysconfdir}/sysconfig/i18n $PGDATA/../initdb.i18n
  # Just in case no locale was set, use en_US
  [ ! -f %{_sysconfdir}/sysconfig/i18n ] && echo "LANG=en_US" >$PGDATA/../initdb.i18n
  # Is expanded this early to be used in the command su runs
  echo "export LANG LC_ALL LC_CTYPE LC_COLLATE LC_NUMERIC LC_TIME" >> $PGDATA/../initdb.i18n
  # Initialize the database
  su -l postgres -s /bin/sh -c "/usr/bin/initdb --pgdata=$PGDATA >/dev/null 2>&1" </dev/null
  [ -f $PGDATA/PG_VERSION ] && echo "Database successfully initialized!"
  [ ! -f $PGDATA/PG_VERSION ] && echo "Database was NOT successfully initalized!"
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

%post -n %{libpgtcl} -p /sbin/ldconfig
%postun -n %{libpgtcl} -p /sbin/ldconfig

%post -n %{libecpg} -p /sbin/ldconfig
%postun -n %{libecpg} -p /sbin/ldconfig

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -f perlfiles.list

%files -f main.lst 
%defattr(-,root,root)
%doc doc/FAQ doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README HISTORY doc/bug.template
%doc README.rpm-dist README.v7.3
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createlang
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/droplang
%{_bindir}/dropuser
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_encoding
%{_bindir}/pg_id
%{_bindir}/pg_restore
%{_bindir}/psql
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
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man7/*

%files -n %{libname} 
%defattr(-,root,root)
%{_libdir}/libpq.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libpq.so

%files -n %{libecpg}
%defattr(-,root,root)
%{_libdir}/libecpg.so.*

%files -n %{libecpg}-devel
%defattr(-,root,root)
%{_libdir}/libecpg.so

%files contrib
%defattr(-,root,root)
%doc contrib/*/README.* contrib/spi/*.example
%{_libdir}/pgsql/_int.so
%{_libdir}/pgsql/array_iterator.so
%{_libdir}/pgsql/autoinc.so
%{_libdir}/pgsql/btree_gist.so
%{_libdir}/pgsql/chkpass.so
%{_libdir}/pgsql/cube.so
%{_libdir}/pgsql/dblink.so
%{_libdir}/pgsql/dbsize.so
%{_libdir}/pgsql/earthdistance.so
%{_libdir}/pgsql/fti.so
%{_libdir}/pgsql/fuzzystrmatch.so
%{_libdir}/pgsql/insert_username.so
%{_libdir}/pgsql/int_aggregate.so
%{_libdir}/pgsql/isbn_issn.so
%{_libdir}/pgsql/lo.so
%{_libdir}/pgsql/ltree.so
%{_libdir}/pgsql/misc_utils.so
%{_libdir}/pgsql/moddatetime.so
%{_libdir}/pgsql/noup.so
%{_libdir}/pgsql/pending.so
%{_libdir}/pgsql/pgcrypto.so
%{_libdir}/pgsql/pgstattuple.so
%{_libdir}/pgsql/refint.so
%{_libdir}/pgsql/rserv.so
%{_libdir}/pgsql/rtree_gist.so
%{_libdir}/pgsql/seg.so
%{_libdir}/pgsql/string_io.so
%{_libdir}/pgsql/tablefunc.so
%{_libdir}/pgsql/timetravel.so
%{_libdir}/pgsql/tsearch.so
%{_libdir}/pgsql/user_locks.so
%{_datadir}/pgsql/contrib/
%{_bindir}/dbf2pg
%{_bindir}/findoidjoins
%{_bindir}/make_oidjoins_check
%{_bindir}/fti.pl
%{_bindir}/oid2name
%{_bindir}/pg_dumplo
%{_bindir}/pg_logger
%{_bindir}/pg_encoding
%{_bindir}/pg_id
%{_bindir}/pgbench
%{_bindir}/RservTest
%{_bindir}/MasterInit
%{_bindir}/MasterAddTable
%{_bindir}/Replicate
%{_bindir}/MasterSync
%{_bindir}/CleanLog
%{_bindir}/SlaveInit
%{_bindir}/SlaveAddTable
%{_bindir}/GetSyncID
%{_bindir}/PrepareSnapshot
%{_bindir}/ApplySnapshot
%{_bindir}/InitRservTest
%{_bindir}/vacuumlo

%files server -f server.lst
%defattr(-,root,root)
%doc README.mdk README.v7.3 upgrade_tips_7.3
%{_bindir}/initdb
%{_bindir}/initlocation
%{_bindir}/ipcclean
%{_bindir}/pg_controldata 
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_bindir}/mdk-pgdump.sh
%{_mandir}/man1/initdb.1*
%{_mandir}/man1/initlocation.1*
%{_mandir}/man1/ipcclean.1*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.1*
%{_mandir}/man1/pg_resetxlog.*
%{_mandir}/man1/postgres.1*
%{_mandir}/man1/postmaster.1*
%{_datadir}/pgsql/postgres.bki
%{_datadir}/pgsql/postgres.description
%{_datadir}/pgsql/*.sample
%dir %{_libdir}/pgsql
%dir %{_datadir}/pgsql
%attr(700,postgres,postgres) %dir %{pgdata}
%attr(700,postgres,postgres) %dir %{pgdata}/data
%attr(700,postgres,postgres) %dir %{pgdata}/backups
%attr(644,postgres,postgres) %config(noreplace) %{_localstatedir}/pgsql/.bash_profile
%{_libdir}/pgsql/*_and_*.so
%{_datadir}/pgsql/conversion_create.sql
%{_datadir}/pgsql/upgrade.pl
%dir %{_srvdir}/postgresql
%dir %{_srvdir}/postgresql/log
%{_srvdir}/postgresql/run
%{_srvdir}/postgresql/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/postgresql
%config(noreplace) %{_sysconfdir}/sysconfig/postgresql
%{_datadir}/afterboot/01_postgresql

%files devel
%defattr(-,root,root)
%doc doc/TODO doc/TODO.detail
%{_includedir}/pgsql
%{_bindir}/ecpg
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_mandir}/man1/ecpg.1*
%{_bindir}/pg_config
%{_mandir}/man1/pg_config.1*

%files pl 
%defattr(-,root,root) 
%{_libdir}/pgsql/plperl.so 
%{_libdir}/pgsql/pltcl.so 
%{_bindir}/pltcl_delmod 
%{_bindir}/pltcl_listmod 
%{_bindir}/pltcl_loadmod 
%{_datadir}/pgsql/unknown.pltcl 
%{_libdir}/pgsql/plpython.so 
%{_libdir}/pgsql/plpgsql.so

%files tcl
%defattr(-,root,root)
%doc src/interfaces/libpgtcl/README
%{_bindir}/pgtclsh
%{_mandir}/man1/pgtclsh.*
%{_mandir}/man1/pgtksh.*

%files -n %{libpgtcl} 
%defattr(-,root,root) 
%doc src/interfaces/libpgtcl/README 
%attr(755,root,root) %{_libdir}/libpgtcl.so.* 

%files -n %{libpgtcl}-devel
%defattr(-,root,root)  
%doc src/interfaces/libpgtcl/README  
%{_libdir}/libpgtcl.so

%files python
%defattr(-,root,root)
%doc src/interfaces/python/README* src/interfaces/python/tutorial
%{_libdir}/python*/site-packages/_pgmodule.so
%{_libdir}/python*/site-packages/*.py

%files jdbc
%defattr(-,root,root)
%doc src/interfaces/jdbc/README
%{_datadir}/pgsql/pg73jdbc1.jar
%{_datadir}/pgsql/pg73jdbc2.jar
%{_datadir}/pgsql/pg73jdbc3.jar
%{_datadir}/pgsql/pg73jdbc2ee.jar

%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{_libdir}/pgsql/test/*
%attr(-,postgres,postgres) %dir %{_libdir}/pgsql/test

%changelog
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

* Sun Aug 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 7.3.4-2mdk
- Patch8: amd64 has comparable math precision to alpha

* Wed Aug  6 2003 Warly <warly@mandrakesoft.com> 7.3.4-1mdk
- new version.

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 7.3.3-4mdk
- Patch7: Fix pythondir detection

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 7.3.3-3mdk
- Rebuild

* Sun Jun 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 7.3.3-2mdk
- the contribs package requires the new perl-Pg package

* Thu Jun 26 2003 Warly <warly@mandrakesoft.com> 7.3.3-1mdk
- new version (Migration to version 7.3.3: A dump/restore is *not* 
required for those running 7.3.*.)

* Thu Jun 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 7.3.2-6mdk
- make it provide

* Tue Mar  4 2003 Warly <warly@mandrakesoft.com> - 7.3.2-5mdk
- move plpgsql.so in postgresql-pl
- postgresql-pl obsoletes libpgsql2 to have clean updates

* Mon Mar  3 2003 Warly <warly@mandrakesoft.com> 7.3.2-4mdk
- try to change pg_hba.conf to do the dump/restore even if the base access is restricted

* Fri Feb 21 2003 Warly <warly@mandrakesoft.com> 7.3.2-3mdk
- silly me

* Fri Feb 21 2003 Warly <warly@mandrakesoft.com> 7.3.2-2mdk
- fix empty dir in docs package (Guillaume Rousse)

* Fri Feb 14 2003 Warly <warly@mandrakesoft.com> 7.3.2-1mdk
- new version

* Mon Dec 30 2002 Warly <warly@mandrakesoft.com> 7.3.1-4mdk
- fix post script syntax
- change pg_hba.conf default permission setting

* Sun Dec 29 2002 Stefan van der Eijk <stefan@eijk.nu> 7.3.1-3mdk
- add %%defattr(-,root,root) to libecpg package
- removed some hardcoded /usr/lib/ entries in .spec file (rpmlint)
- comment out "Requires: libpgsqlodbc = %{version}-%{release}"

* Sun Dec 29 2002 Stefan van der Eijk <stefan@eijk.nu> 7.3.1-2mdk
- BuildRequires

* Tue Dec 24 2002 Warly <warly@mandrakesoft.com> 7.3.1-1mdk
- new version

* Mon Dec  2 2002 Warly <warly@mandrakesoft.com> 7.3-1mdk
- new version

* Wed Oct 30 2002 Warly <warly@mandrakesoft.com> 7.2.3-2mdk
- applied initscript fix from Guillaume Rousse <rousse@ccr.jussieu.fr>

* Mon Oct 28 2002 Warly <warly@mandrakesoft.com> 7.2.3-1mdk
- new version
- remove files.lst source
- remove postgresql-dump
- remove pg_options source

* Tue Sep  3 2002 Vincent Danen <vdanen@mandrakesoft.com> 7.2.2-1mdk
- 7.2.2 (security fixes)

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 7.2.1-11mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Thu Aug 08 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2.1-10mdk
- fix initscript.
- fix few rpmlint errors.

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 7.2.1-9mdk
- rebuild for perl thread-multi

* Thu Jul 25 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2.1-8mdk
- don't forget to upload all postgres libs.

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 7.2.1-7mdk
- Automated rebuild with gcc3.2

* Wed Jul 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 7.2.1-6mdk
- rebuild for new readline

* Mon Jul 15 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2.1-5mdk
- add postgres user

* Sun Jul 14 2002 Stefan van der Eijk <stefan@eijk.nu> 7.2.1-4mdk
- BuildRequires

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 7.2.1-3mdk
- add patch6 to use INSTALLDIRS=vendor
- rebuild for perl 5.8.0

* Tue May 28 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2.1-2mdk
- rebuild with gcc 3.1.
- update readline version in BuildRequires.

* Mon Apr 08 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2.1-1mdk
- Version 7.2.1.
- Remove Patch3 (applied)

* Tue Apr 02 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-13mdk
- Fix apostrophe insertion prob (thx to Digital Wokan).

* Mon Mar 11 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-12mdk
- Make sure that data directory is created.

* Sun Mar 10 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-11mdk
- Fix postgresql-tcl requires and description (thanks to Tanner).

* Mon Mar 04 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-10mdk
- Added few Requires in postgresql-devel (thx to Michael).
- Updated README.rpm-dist.
- Clean the configure options.
- s/pg_dumpall_new/pg_dumpall/ in mdk-pgdump.sh.
- Change backup rpm scripts to use mdk-pgdump.sh.

* Wed Feb 27 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-9mdk
- s/rh-dump/mdk-dump in README.rpm-dist (thx to Guillaume).

* Wed Feb 27 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-8mdk
- README.rpm -> README.rpm-dist (thx to Olivier).
- Remove find-lang handling.

* Wed Feb 27 2002 Stew Benedict <sbenedict@mandrakesoft.com> 7.2-7mdk
- relax CFLAGS for PPC build - were turned back on for all arch

* Mon Feb 25 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-6mdk
- Add default runlevel in initscript.
- Remove service startup in %%post.

* Fri Feb 22 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-5mdk
- Remove useless .bash_profile rewriting.

* Thu Feb 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-4mdk
- Fix typo in python tutorial folder name (postgresql-python).
- postgresql-tk require postgresql-devel.

* Wed Feb 13 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-3mdk
- More spec cleanup to fix db creation-upgrade problems.
- Update README.postgresql.mdk

* Mon Feb 11 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-2mdk
- Fix backups (make a %%pre for each package instead of one for all).
- Spec cleanup pt 1 (next cleanup will fix all the db creation-upgrade pb).
- Add patches and init script from redhat.

* Fri Feb 08 2002 Christian Belisle <cbelisle@mandrakesoft.com> 7.2-1mdk
- 7.2.
- Take patches and initscript from RH.

* Sat Dec 15 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.3-8mdk
- Really fix docs location.

* Sat Dec 15 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.3-7mdk
- Fix docs location.
- Fix bash_profile entries.
- Fix backup feature.

* Thu Dec 06 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.3-6mdk
- libification
- gzip the source (for security check)

* Wed Nov 21 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.3-5mdk
- Fix init script

* Mon Nov 19 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.3-4mdk
- Fix doc location (Guillaume Rousse)
- Remove doc source (Guillaume Rousse)
- Fix init script (Guillaume Rousse)

* Fri Nov 16 2001 Stew Benedict <sbenedict@mandrakesoft.com> 7.1.3-3mdk
- relax CFLAGS for PPC build, just use defaults

* Thu Nov 15 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.3-2mdk
- fix invalid-packager and strange-permissions warning in rpmlint.
- Added a reload entry.

* Mon Oct  1 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.3-1mdk
- 7.1.3.
- Fixed init.d script.

* Thu Sep 13 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-19mdk
- Fixed post-install procedure (initialize ok now).
- Modified README.mdk.

* Tue Sep 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-18mdk
- Fixed backup feature when upgrading.

* Tue Sep 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-17mdk
- Removed conflict with perl-ldap.

* Tue Sep 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-16mdk
- Fixed a library simlink

* Mon Sep 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-15mdk
- Added missing files

* Mon Sep 10 2001 David BAUDENS <baudens@mandrakesoft.com> 7.1.2-14mdk
- Fix menu entry for postgresql-tk
- Fix Requires (requires %%version-%%release and not only %%version)

* Sun Sep 09 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-13mdk
- Added documentation in each package.

* Fri Sep 07 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-12mdk
- postgresql-contrib: removed sources.
- added README.mdk for beginners.
- Fixed menu problem.

* Sat Aug  4 2001 Pixel <pixel@mandrakesoft.com> 7.1.2-11mdk
- postgresql-plperl: add require the perl-base used for building 
(the libperl.so auto-require is not enough)

* Thu Aug 02 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-10mdk
- Applied a patch to pgacess (thanks to Digital Wokan)

* Fri Jul 27 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-9mdk
- Restore the enhanced backup feature.

* Fri Jul 27 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-8mdk
- Remove the backup feature.

* Wed Jul 25 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-7mdk
- Backup the database when update.

* Mon Jul 16 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-6mdk
- Fixed the %post command.

* Mon Jul 16 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-5mdk
- Moved all libraries to %{_libdir}
- Fixed some typos in the Requires
- Added Prefix support.

* Mon Jul  9 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-4mdk
- s/Copyright/License
- Added the TODO as documentation for the -devel package.
- Removed commas in the Requires.

* Wed Jun 27 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-3mdk
- Fixed Distribution tag.

* Mon Jun 18 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-2mdk
- Fixed few BuildRequires (thanks to Stefan van der Eijk)

* Mon Jun 18 2001 Christian Belisle <cbelisle@mandrakesoft.com> 7.1.2-1mdk
- Updated to 7.1.2
- Removed --pglib to initdb, invalid option now

* Mon Jun 18 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 7.1.1-4mdk
- New office menu structure

* Sat May 19 2001  Daouda Lo <daouda@mandrakesoft.com> 7.1.1-3mdk
- fix files section typos (credits to Christian Zoffoli)

* Thu May 17 2001  Daouda Lo <daouda@mandrakesoft.com> 7.1.1-2mdk
- enhanced init script file. 
- fix buildequires + dependencies

* Mon May  7 2001  Stefan van der Eijk <stefan@eijk.nu> 7.1.1-1mdk
- removed old alpha stuff
- 7.1.1

* Tue May  1 2001  Daouda Lo <daouda@mandrakesoft.com> 7.1-2mdk
- fix typos in pgaccess and postgresql-tcl
- fix --prefix --datadir values.

* Mon Apr 30 2001 Daouda Lo <daouda@mandrakesoft.com> 7.1-1mdk
- release 7.1
- bug fixes, big spec cleanups and lot of enhancements
  o  NOTE: many files that used to be in %{_libdir}/pgsql are now in /usr/share/pgsql!
  o  fix buildrequires
  o  Split out the libs into the libs subpackage.
  o  added mdk-pgdump.sh script (adapted to Mandrake)
  o  Updated initscript to use pg_ctl to stop
  o  Updated initscript to initdb and start postmaster with LC_ALL=C to prevent index corruption.
  o  Packaging reorg: added contrib and docs subpackages.
  o  mark odbcinst.ini as a config file
  o  libpq.so changes for maximum compatiblity
  o  fix dangling symlimks (pg_crc.c)
  o  Merged with postgresql official modifications
  o  Fix docs mixup.
  o  rewrote postgresql init script ( use -i tcp/ip connections available -> Thanx to Jerome Martin)
  o  Removed broken and confusing logrotate script. 
  o  strip out -ffastmath -- Considered Harmful.
  o  README.rpm-dist updated.  
- need a dump/restore before upgrading 

* Sun Apr 6 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 7.0.3-12mdk
- added some BuildRequires and --with-readline so it picks everything up
  in the case the build machine does not have them installed

* Tue Apr 3 2001 Daouda Lo <daouda@mandrakesoft.com> 7.0.3-11mdk
- server build macro .

* Tue Apr 3 2001 Daouda Lo <daouda@mandrakesoft.com> 7.0.3-10mdk
- used server macros in post and preun 

* Tue Apr 3 2001 Daouda Lo <daouda@mandrakesoft.com> 7.0.3-9mdk
- macrozif of python version to allow build on 7.2 boxes (thanx Ian )

* Thu Dec  28 2000  Daouda Lo <daouda@mandrakesoft.com> 7.0.3-8mdk
- add missing include files (for GIST) .

* Wed Dec  6 2000  Daouda Lo <daouda@mandrakesoft.com> 7.0.3-7mdk
- fix PGACCESS_HOME variable (close #1463)
- add noreplace to conf files
- add longtitle to pgsql-tk menu

* Mon Dec  4 2000  Daouda Lo <daouda@mandrakesoft.com> 7.0.3-6mdk
- many changes from official spec
- patch for i64  
- add some missing include dir
- libtoolized


* Wed Nov 29 2000 Daouda Lo <daouda@mandrakesoft.com> 7.0.3-5mdk
- fix gcc flags (don't use both -ffast-math and Optmisations) 
  thx Ian C. Sison
- add perl-devel in Builrequires section.
- avoid building with hardcoded number version inside spec --> use 
  define tag .
 
* Wed Nov 15 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 7.0.3-4mdk
- fix dependency with /usr/local/bin/python.
- short-circuit compliant (tm.)

* Fri Nov 10 2000 David BAUDENS <baudens@mandrakesoft.com> 7.0.3-3mdk
- Fix build for PPC
- Use %%make macros

* Fri Nov 10 2000 Daouda Lo <daouda@mandrakesoft.com> 7.0.3-2mdk
- add %postun to package postgres-tk
- correct postgres-tk menu entry  
- added caution for upgrade from 7.0.2 to 7.0.3
- make /etc/logtrotate.d/postgres 0644 instead of 0700 

* Thu Nov 09 2000 Daouda Lo <daouda@mandrakesoft.com> 7.0.3-1mdk
- new release.
- more macros .
- regenerate patch1.
- upgrade source files to new version

* Sun Oct 22 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 7.0.2-6mdk
- create menu for pgaccess [Bug #425]
- modify pgaccess to it does not require libpgtcl.so, but libpgtcl.so.2
- remove postgres group when uninstalling [Bug 921]

* Sat Sep 16 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 7.0.2-5mdk
- Remove *.bs before creating filelist

* Sat Sep 02 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 7.0.2-4mdk
- create database "postgres" if it does not exist already
- if not during Drak install, start postgresql
- copied files from /etc/skel in /var/lib/pgsql
- add PGDATA in /etc/profile 

* Mon Aug 07 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 7.0.2-3mdk
- modified initscripts so that, at upgrade, the user is pointed at the
  right directory for a Howto on how to convert the database from the
  old format.

* Mon Aug 07 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 7.0.2-2mdk
- cleaned package for rpmlint

* Sun Aug 06 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 7.0.2-1mdk
- Merged with RPM from postgresql.com
- Macroized package

* Mon Jun 12 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0.2-2
- Corrected misreporting of version.
- Corrected for non-root build clean script.

* Mon Jun 05 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0.2 
- Postgresql-dump manpage to man1, and to separate source file to facilitate
-- _mandir macro expansion correctness.
- NOTE: The PostScript documentation is no longer being included in the
-- PostgreSQL tarball.  If demand is such, I will pull together a
-- postgresql-ps-docs subpackage or pull in the PostScript docs into the
-- main package.
- RPM patchset has release number, now, to prevent patchfile confusion :-(.


* Sat Jun 03 2000 Lamar Owen <lamar.owen@wgcr.org>
- Incorporate most of Trond's changes (reenabled the alpha
-- patches, as it was a packaging error on my part).
- Trimmed changelog history to Version 7.0beta1 on. To see the
-- previous changelog, grab the 6.5.3 RPM from RedHat 6.2 and pull the spec.
- Rev to 7.0.1 (which incorporates the syslog patch, which has
-- been removed from rpm-pgsql-7.0.1-1.patch)

* Fri May 26 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable the alpha patch, as it doesn't apply cleanly
- removed distribution, packager, vendor
- renamed spec file
- don't build pl-perl
- use %%{_mandir}
- now includes vacuumdb.1*

* Thu May 25 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0-3
- Incorporated Tatsuo's syslog segmentation patches
- Incorporated some of Trond's changes (see below)
-- Fixed some Perl 5.6 oddness in Rawhide
- Incorporated some of Karl's changes (see below)
-- PL/Perl should now work.
- Fixed missing /usr/bin/pg_passwd.

* Mon May 22 2000 Karl DeBisschop <kdebisschop@infoplease.com>
- 7.0-2.1
- make plperl module (works for linux i386, your guess for other platforms)
- use "make COPT=" because postgreSQL configusre script ignores CFLAGS

* Sat May 20 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0-2
- pg_options default values changed.
- SPI headers (again!) fixed in a permanent manner  -- hopefully!
- Alpha patches!

* Tue May 16 2000 Frederic Lepied <flepied@mandrakesoft.com> 6.5.3-2mdk
- fix build for perl 5.6.

* Tue May 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- changed buildroot, removed packager, vendor, distribution
-- [Left all but buildroot as-is for PostgreSQL.org RPMS. LRO]
- don't strip in package [strip in PostgreSQL.org RPMS]
- fix perl weirdnesses (man page in bad location, remove 
  perllocal.pod from file list)

* Mon May 15 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0 final -1
- Man pages restructured
- Changed README.rpm notices about BETA
- incorporated minor changes from testing
- still no 7.0 final alpha patches -- for -2 or -3, I guess.
- 7.0 JDBC jars!

* Sat May 06 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0RC5-0.5
- UserID of 26 to conform to RedHat Standard, instead of 40.  This only
-- is for new installs -- upgrades will use what was already there.
- Waiting on built jar's of JDBC.  If none are forthcoming by release,
-- I'm going to have to bite the bullet and install the jdk....

* Mon May 01 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0RC2-0.5
- Fixed /usr/src/redhat/BUILD path to $RPM_BUILD_DIR for portability
-- and so that RPM's can be built by non-root.
- Minor update to README.rpm

* Tue Apr 18 2000 Lamar Owen <lamar.owen@wgcr.org>
- 0.6
- Fixed patchset: wasn't patching pgaccess or -i in postmaster.opts.default
- minor update to README.rpm

* Mon Apr 17 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0RC1-0.5 (release candidate 1.)
- Fixed SPI header directories' permisssions.
- Removed packaging of Alpha patches until Ryan releases RC1-tested set.

* Mon Apr 10 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0beta5-0.1 (released instead of the release candidate)

* Sat Apr 08 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0beta4-0.2 (pre-release-candidate CVS checkout)
- Alpha patches!
- pg_options.sample

* Sun Apr 2 2000 John Buswell <johnb@mandrakesoft.com> 6.5.3-1mdk
- 6.5.3
- Sparc64 patch added
- spec-helper
- fixed groups

* Fri Mar 24 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0beta3-0.1

* Mon Feb 28 2000 Lamar Owen <lamar.owen@wgcr.org>
- Release 0.3
- Fixed stderr redir problem in init script
- Init script now uses pg_ctl to start postmaster
- Packaged inital pg_options for good logging
- built with timestamped logging.

* Tue Feb 22 2000 Lamar Owen <lamar.owen@wgcr.org>
- Initial 7.0beta1 build
- Moved PGDATA to /var/lib/pgsql/data
- First stab at logging and logrotate functionality -- test carefully!
- -tcl subpackage split -- tcl client and pltcl lang separated from
-- the Tk stuff.  PgAccess and the tk client are now in the -tk subpackage.
- No patches for Alpha as yet.

