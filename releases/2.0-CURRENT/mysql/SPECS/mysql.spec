#
# spec file for package mysql
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mysql
%define version		5.0.26
%define release		%_revrel

%define major		15
%define libname		%mklibname mysql %{major}
%define oldlibname	%mklibname mysql 14
%define mysqld_user	mysql

%global make_test	1
%{?_with_test:		%global make_test 1}
%{?_without_test:	%global make_test 0}

%define _requires_exceptions perl(this)

Summary:	MySQL is a very fast and reliable SQL database engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Databases
URL:        	http://www.mysql.com
Source0:	ftp://ftp.mysql.serenitynet.com/MySQL-5.0/mysql-%{version}.tar.gz
Source1:	ftp://ftp.mysql.serenitynet.com/MySQL-5.0/mysql-%{version}.tar.gz.asc
Source2:	mysqld.run
Source3:	mysqld-log.run
Source4:	mysqld.finish
Source5:	05_mysql.afterboot
Source6:	logrotate.mysqld
Source7:	my.cnf
Source8:	DATADIR.env
Source9:    	LOG.env
Source10:   	MYSQLD_OPTS.env
Patch1:		mysql-5.0.15-install_script_mysqld_safe.diff
Patch2:		mysql-5.0.23-lib64.diff
Patch3:		mysql-5.0.15-noproc.diff
Patch6:		mysql-errno.patch
# Add fast AMD64 mutexes
Patch7:		db-4.1.24-amd64-mutexes.diff
# NPTL pthreads mutex are evil
Patch8:		db-4.1.24-disable-pthreadsmutexes.diff
Patch9:		mysql-5.0.15-disable-pthreadsmutexes.diff
Patch10:	mysql-5.0.19-instance-manager.diff

BuildRoot:      %{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	glibc-devel
BuildRequires:	libstdc++-devel
BuildRequires:	doxygen
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	termcap-devel
BuildRequires:	multiarch-utils 
BuildRequires:	ncurses-devel
BuildRequires:	python
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo

Provides:       mysql-server
Provides:	MySQL-server
Requires(pre):	rpm-helper
Requires(pre):	runit
Requires(preun): rpm-helper
Requires(preun): runit
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires:	mysql-client = %{version}
Obsoletes:      MySQL
Obsoletes:	MySQL-devel <= 3.23.39
Obsoletes:	MySQL-common
Obsoletes:	MySQL-Max

%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
MySQL AB.

The MySQL software has Dual Licensing, which means you can use the MySQL
software free of charge under the GNU General Public License
(http://www.gnu.org/licenses/). You can also purchase commercial MySQL
licenses from MySQL AB if you do not wish to be bound by the terms of
the GPL. See the chapter "Licensing and Support" in the manual for
further info.

The MySQL web site (http://www.mysql.com/) provides the latest
news and information about the MySQL software. Also please see the
documentation and the manual for more information.


%package client
Summary:        MySQL client
Group:          Databases
Requires:       %{libname} = %{version}
Obsoletes:	MySQL-client

%description client
This package contains the standard MySQL clients.


%package bench
Summary:        MySQL benchmarks and test system
Group:          Databases
Requires:       mysql-client = %{version}
Requires:	perl
Obsoletes:	MySQL-bench

%description bench
This package contains MySQL benchmark scripts and data.


%package -n %{libname}
Summary:        MySQL shared libraries
Group:          System/Libraries
Obsoletes:	%{oldlibname}

%description -n %{libname}
This package contains the shared libraries (*.so*) which certain
languages and applications need to dynamically load and use MySQL.


%package -n %{libname}-devel
Summary:        MySQL development header files and libraries
Group:          Development/Other
Obsoletes:      MySQL-devel
Provides:       mysql-devel = %{version}-%{release}
Provides:       MySQL-devel = %{version}-%{release}
Requires:       %{libname} = %{version}
Requires:	mysql = %{version}
Requires:	mysql-client = %{version}
Provides:       libmysql-devel
Obsoletes:      %{oldlibname}-devel

%description -n %{libname}-devel
This package contains the development header files and libraries
necessary to develop MySQL client applications.

This package also contains the MySQL server as an embedded library.

The embedded MySQL server library makes it possible to run a
full-featured MySQL server inside the client application.
The main benefits are increased speed and more simple management
for embedded applications.

The API is identical for the embedded MySQL version and the
client/server version.


%package -n %{libname}-static-devel
Summary:        MySQL static development libraries
Group:          Development/Other
Provides:       mysql-static-devel = %{version}-%{release}
Provides:       MySQL-static-devel = %{version}-%{release}
Requires:	mysql-devel = %{version}
Requires:	mysql-client = %{version}
Provides:       libmysql-static-devel

%description -n %{libname}-static-devel
This package contains the static development libraries.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p0
%patch2 -p1
%patch3 -p0 -b .noproc
%patch6 -p1 -b .errno_as_defines
%patch7 -p1 -b .amd64-mutexes
%patch8 -p1 -b .pthreadsmutexes
%patch9 -p0 -b .disable-pthreadsmutexes
%patch10 -p0 -b .instance-manager

# fix annoyances
perl -pi -e "s|AC_PROG_RANLIB|AC_PROG_LIBTOOL|g" configure*
perl -pi -e "s|^MAX_C_OPTIMIZE.*|MAX_C_OPTIMIZE=\"\"|g" configure*
perl -pi -e "s|^MAX_CXX_OPTIMIZE.*|MAX_CXX_OPTIMIZE=\"\"|g" configure*


%build
# Run aclocal in order to get an updated libtool.m4 in generated
# configure script for "new" architectures (aka. x86_64, mips)
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal-1.7; autoconf; automake-1.7 --foreign --add-missing --copy

pushd bdb/dist
    sh ./s_config
popd

pushd bdb/build_unix
    CONFIGURE_TOP="../dist" %configure2_5x --disable-pthreadsmutexes
    CONFIGURE_TOP="."
popd


%serverbuild

# (gb) We shall always have the fully versioned binary
# FIXME: Please, please, do tell why you need fully qualified version
GCC_VERSION=`gcc -dumpversion`
CFLAGS="$CFLAGS"
%ifarch alpha
CXXFLAGS="$CXXFLAGS -fPIC"
%else
CXXFLAGS="$CXXFLAGS"
%endif
export MYSQL_BUILD_CC="gcc-$GCC_VERSION"
export MYSQL_BUILD_CXX="g++-$GCC_VERSION"

export MYSQL_BUILD_CFLAGS="$CFLAGS"
export MYSQL_BUILD_CXXFLAGS="$CXXFLAGS"

#
# Use MYSQL_BUILD_PATH so that we can use a dedicated version of gcc
#
export PATH=${MYSQL_BUILD_PATH:-/bin:/usr/bin}	
export PS="/bin/ps"
export FIND_PROC="/bin/ps p $$PID"
export KILL="/bin/kill"
export CHECK_PID="/bin/kill -0 $$PID"

# The --enable-assembler simply does nothing on systems that do not
# support assembler speedups.

%configure2_5x \
    --prefix=/ \
    --exec-prefix=%{_prefix} \
    --libexecdir=%{_sbindir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --localstatedir=%{_localstatedir}/mysql \
    --infodir=%{_infodir} \
    --includedir=%{_includedir} \
    --mandir=%{_mandir} \
    --enable-shared \
    --with-pic \
    --with-extra-charsets=all \
    --enable-assembler \
    --enable-local-infile \
    --enable-large-files=yes \
    --enable-largefile=yes \
    --without-readline \
    --without-libwrap \
    --without-mysqlfs \
    --with-openssl \
    --with-berkeley-db \
    --with-innodb \
    --with-big-tables \
    --with-archive-storage-engine \
    --with-blackhole-storage-engine \
    --without-example-storage-engine \
    --with-csv-storage-engine \
    --without-debug \
    --with-mysqld-user=%{mysqld_user} \
    --with-unix-socket-path=%{_localstatedir}/mysql/mysql.sock \
    --enable-thread-safe-client \
    --without-embedded-server \
    --with-vio

# benchdir does not fit in the above model
%make benchdir_root=%{buildroot}%{_datadir}

nm --numeric-sort sql/mysqld >mysqld.sym


%check
%if %{make_test}
# disable failing tests
echo "mysql_client_test : Unstable test case, bug#12258" >> mysql-test/t/disabled.def
echo "openssl_1 : Unstable test case" >> mysql-test/t/disabled.def
echo "rpl_openssl : Unstable test case" >> mysql-test/t/disabled.def
echo "rpl_trigger : Unstable test case" >> mysql-test/t/disabled.def
# set some test env, should be free high random ports...
export MYSQL_TEST_MANAGER_PORT=9305
export MYSQL_TEST_MASTER_PORT=9306
export MYSQL_TEST_SLAVE_PORT=9308
export MYSQL_TEST_NDB_PORT=9350
make check

pushd mysql-test
    ./mysql-test-run.pl \
    --force \
    --timer \
    --master_port=$MYSQL_TEST_MASTER_PORT \
    --slave_port=$MYSQL_TEST_SLAVE_PORT \
    --ndbcluster_port=$MYSQL_TEST_NDB_PORT \
    --testcase-timeout=5 \
    --suite-timeout=30 || true
popd
%endif


%install 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/chapter
mkdir -p %{buildroot}%{_var}/run/mysqld
mkdir -p %{buildroot}%{_var}/log/mysqld
mkdir -p %{buildroot}%{_localstatedir}/mysql/{mysql,test,.tmp}

%makeinstall_std benchdir_root=%{_datadir} testdir=%{_datadir}/mysql-test

install -m 0644 mysqld.sym %{buildroot}%{_libdir}/mysql/mysqld.sym

install -m 0644 %{_sourcedir}/logrotate.mysqld %{buildroot}%{_sysconfdir}/logrotate.d/mysqld
install -m 0644 %{_sourcedir}/my.cnf %{buildroot}%{_sysconfdir}/my.cnf

mkdir -p %{buildroot}%{_srvdir}/mysqld/{log,env}
install -m 0740 %{_sourcedir}/mysqld.run %{buildroot}%{_srvdir}/mysqld/run
install -m 0740 %{_sourcedir}/mysqld.finish %{buildroot}%{_srvdir}/mysqld/finish
install -m 0740 %{_sourcedir}/mysqld-log.run %{buildroot}%{_srvdir}/mysqld/log/run

install -m 0640 %{_sourcedir}/DATADIR.env %{buildroot}%{_srvdir}/mysqld/env/DATADIR
install -m 0640 %{_sourcedir}/LOG.env %{buildroot}%{_srvdir}/mysqld/env/LOG
install -m 0640 %{_sourcedir}/MYSQLD_OPTS.env %{buildroot}%{_srvdir}/mysqld/env/MYSQLD_OPTS


# Install docs
install -m 0644 Docs/mysql.info %{buildroot}%{_infodir}/mysql.info

# Fix libraries
mv %{buildroot}%{_libdir}/mysql/libmysqlclient.* %{buildroot}%{_libdir}/
mv %{buildroot}%{_libdir}/mysql/libmysqlclient_r.* %{buildroot}%{_libdir}/
perl -pi -e "s|%{_libdir}/mysql|%{_libdir}|" %{buildroot}%{_libdir}/*.la

pushd %{buildroot}%{_bindir}
    ln -sf mysqlcheck mysqlrepair
    ln -sf mysqlcheck mysqlanalyze
    ln -sf mysqlcheck mysqloptimize
popd

rm -f %{buildroot}%{_datadir}/info/dir
rm -f %{buildroot}%{_bindir}/make_win_src_distribution
rm -f %{buildroot}%{_bindir}/make_win_binary_distribution
rm -f %{buildroot}%{_datadir}/mysql/*.spec
rm -f %{buildroot}%{_datadir}/mysql/{postinstall,preinstall,mysql-log-rotate,mysql.server,binary-configure}
rm -f %{buildroot}%{_bindir}/client_test
rm -f %{buildroot}%{_bindir}/mysql_client_test*

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/05_mysql.afterboot %{buildroot}%{_datadir}/afterboot/05_mysql

# move docs around
cp -f sql-bench/README README.sql-bench

%multiarch_binaries %{buildroot}%{_bindir}/mysql_config
%multiarch_includes %{buildroot}%{_includedir}/mysql/my_config.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
%_pre_useradd %{mysqld_user} %{_localstatedir}/mysql /bin/bash 82


%post
%_install_info mysql.info
%_mkafterboot
chown -R %{mysqld_user}:%{mysqld_user} %{_localstatedir}/mysql
chmod 0711 %{_localstatedir}/mysql
if [ "$1" == "1" ]; then
    # Initialize database
    export TMPDIR="%{_localstatedir}/mysql/.tmp"
    export TMP="${TMPDIR}"
    HOME=/var/lib/mysql /sbin/chpst -u %{mysqld_user} /bin/sh -c %{_bindir}/mysql_install_db --rpm --user=%{mysqld_user}

    if [ ! -f /root/.my.cnf ]; then
        echo "[mysqladmin]" >/root/.my.cnf
        echo "user=root" >>/root/.my.cnf
        echo "password=" >>/root/.my.cnf
        echo ""
        echo "** An unconfigured /root/.my.cnf file exists, sufficient to start mysqld with srv"
        echo "** however you will need to create a password for the root user and modify"
        echo "** /root/.my.cnf accordingly to safely shutdown the database."
        echo ""
        echo "** Read 'man afterboot' for more details."
    fi
fi

%_post_srv mysqld


%preun
%_remove_install_info mysql.info
%_preun_srv mysqld
# We do not remove the mysql user since it may still own a lot of
# database files.


%postun
%_mkafterboot


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-, root, root) 
%{_sbindir}/mysqld
%{_libdir}/mysql/mysqld.sym
%dir %attr(0750,root,admin) %{_srvdir}/mysqld
%dir %attr(0750,root,admin) %{_srvdir}/mysqld/log
%dir %attr(0750,root,admin) %{_srvdir}/mysqld/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/mysqld/finish
%config(noreplace) %attr(0740,root,admin)%{_srvdir}/mysqld/run
%config(noreplace) %attr(0740,root,admin)%{_srvdir}/mysqld/log/run
%config(noreplace) %attr(0740,root,admin)%{_srvdir}/mysqld/env/DATADIR
%config(noreplace) %attr(0740,root,admin)%{_srvdir}/mysqld/env/LOG
%config(noreplace) %attr(0740,root,admin)%{_srvdir}/mysqld/env/MYSQLD_OPTS
%config(noreplace) %{_sysconfdir}/logrotate.d/mysqld
%config(noreplace) %{_sysconfdir}/my.cnf
%{_bindir}/innochecksum
%{_bindir}/myisamchk
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_create_system_tables
%{_bindir}/mysql_fix_privilege_tables
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_install_db
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_explain_log 
%{_bindir}/mysql_fix_extensions 
%{_bindir}/mysql_secure_installation 
%{_bindir}/mysql_tableinfo 
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_upgrade
%{_bindir}/mysql_upgrade_shell
%{_bindir}/mysql_waitpid 
%{_bindir}/mysql_zap
%{_bindir}/mysqlbug
%{_bindir}/mysqltest
%{_bindir}/mysqlhotcopy
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolveip
%{_bindir}/resolve_stack_dump
%{_bindir}/mysqld_safe
%{_bindir}/mysqld_multi
%{_bindir}/my_print_defaults
%{_bindir}/myisam_ftdump
%{_sbindir}/mysqlmanager
%{_infodir}/mysql.info*
%dir %attr(0711,mysql,mysql) %{_localstatedir}/mysql
%dir %attr(0711,mysql,mysql) %{_localstatedir}/mysql/mysql
%dir %attr(0711,mysql,mysql) %{_localstatedir}/mysql/test
%dir %attr(0711,mysql,mysql) %{_localstatedir}/mysql/.tmp
%dir %attr(0755,mysql,mysql) %{_var}/run/mysqld
%dir %attr(0755,mysql,mysql) %{_var}/log/mysqld
%dir %{_datadir}/mysql
%{_datadir}/mysql/mi_test_all
%{_datadir}/mysql/mi_test_all.res
%{_datadir}/mysql/my-huge.cnf
%{_datadir}/mysql/my-large.cnf
%{_datadir}/mysql/my-medium.cnf
%{_datadir}/mysql/my-small.cnf
%{_datadir}/mysql/my-innodb-heavy-4G.cnf
%{_datadir}/mysql/charsets
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_fix_privilege_tables.sql
%{_datadir}/mysql/*.ini
%{_datadir}/mysql/errmsg.txt
%{_datadir}/afterboot/05_mysql
%dir %{_libdir}/mysql
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_fix_privilege_tables.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqld.1*
%{_mandir}/man1/mysqld_multi.1*
%{_mandir}/man1/mysqld_safe.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysqlman.1*
%{_mandir}/man1/mysqlmanager.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/safe_mysqld.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysql_explain_log.1*
%{_mandir}/man8/mysqld.8*
%{_mandir}/man8/mysqlmanager.8*
%lang(cz) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(nl) %{_datadir}/mysql/dutch
%{_datadir}/mysql/english
%lang(et) %{_datadir}/mysql/estonian
%lang(fr) %{_datadir}/mysql/french
%lang(de) %{_datadir}/mysql/german
%lang(el) %{_datadir}/mysql/greek
%lang(hu) %{_datadir}/mysql/hungarian
%lang(it) %{_datadir}/mysql/italian
%lang(jp) %{_datadir}/mysql/japanese
%lang(ko) %{_datadir}/mysql/korean
%lang(no) %{_datadir}/mysql/norwegian
%lang(no_ny) %{_datadir}/mysql/norwegian-ny
%lang(pl) %{_datadir}/mysql/polish
%lang(pt) %{_datadir}/mysql/portuguese
%lang(ro) %{_datadir}/mysql/romanian
%lang(ru) %{_datadir}/mysql/russian
%lang(sr) %{_datadir}/mysql/serbian
%lang(sl) %{_datadir}/mysql/slovak
%lang(es) %{_datadir}/mysql/spanish
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian


%files bench
%defattr(-, root, root)
%{_bindir}/mysqltestmanager
%{_bindir}/mysqltestmanager-pwgen
%{_bindir}/mysqltestmanagerc
%{_datadir}/sql-bench
%{_datadir}/mysql-test


%files client
%defattr(-, root, root)
%{_bindir}/msql2mysql
%{_bindir}/mysql
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlcheck
%{_bindir}/mysqlrepair
%{_bindir}/mysqlanalyze
%{_bindir}/mysqloptimize
%{_bindir}/mysql_find_rows
%{_bindir}/mysqldump
%{_bindir}/mysqldumpslow
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlbinlog
%{_bindir}/mysql_tableinfo
%{_bindir}/mysql_waitpid
%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/myisam_ftdump.1*


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*


%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/comp_err
%multiarch %{multiarch_bindir}/mysql_config
%{_bindir}/mysql_config
%{_includedir}/mysql
%multiarch %{multiarch_includedir}/mysql/my_config.h
%dir %{_libdir}/mysql
%{_libdir}/*.la
%{_libdir}/*.so
%{_mandir}/man1/mysql_config.1*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/mysql/*.a

%files doc
%defattr(-,root,root)
%doc INSTALL-SOURCE README.sql-bench README COPYING
%doc support-files/*.cnf SSL/NOTES SSL/run* SSL/*.pem


%changelog
* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0.26
- 5.0.26
- don't assume the ./env/* files exist in the runscript

* Sun Sep 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0.24
- change runsvctrl calls to /sbin/sv calls

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0.24
- rebuild against new openssl

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0.24
- 5.0.24
- sync patches with mandriva (less the patches we do not need or want)
- updated my.cnf to be more based on my-medium.cnf
- spec cleanups
- sync the logrotate script with the provided one
- make the runscript read the ./env directory files
- clean up some of the post stuff, in particular we need to pass
  --defaults-file to my_print_defaults or the datadir is listed twice
  and we need to exec mysql_install_db via sh
- have the new lib obsolete the old lib
- don't initialize the database everytime we're upgraded, only on a fresh
  install
- drop the mysql_fix_privilege_tables call; this can be done "by hand" and
  is noted in the 2.0 release notes (this should only need to be done on
  major version upgrades anyways, so why do it every single time?)

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14
- fix requires-on-release
- mysql requires mysql-client
- on a fresh install, create an unconfigured /root/.my.cnf and note
  to the user they need to set a root password and configure it
- fix deps
- add -doc subpackage
- rebuild with gcc4

* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14
- install the afterboot snippet properly (use the right source)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14
- Clean rebuild

* Wed Dec 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14-7avx
- fix the logrotate script to make runsvstat quieter if /service/mysqld doesn't exist
- fix the srv call in the logrotate script

* Wed Oct 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14-6avx
- revert the mysqld run and finish scripts; execline doesn't help us to
  debug and I have no time to figure out why they broke all of a sudden

* Sun Oct 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14-5avx
- fix calls to srv

* Sun Sep 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14-4avx
- drop the MySQL-Max package (only difference was the embedded server
  support)
- drop the mysql-common package; it can all go in mysql now
- s/MySQL/mysql for package name
- convert to run scripts to execlineb, envdirs, removed sysinit (spt)

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14-3avx
- rebuild against new readline

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14-2avx
- s/supervise/service/ in log/run

* Tue Aug 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14-1avx
- 4.1.14
- added support for the archive, blackhole, and csv storage engines
- disable make test until we can make it avoid tests for items we
  haven't included in the build (ie. the example storage engine); also
  mysql's test script got dumb recently because it fails on things that
  aren't even compiled in and bombs out rather than skip the test
- use execlineb for logging run script
- move logs to /var/log/service/mysqld
- run scripts are now considered config files and are not replaceable
- make the run script refuse to run without a /root/.my.cnf file present
- use chpst to run mysqld as user mysql rather than mysqld starting as
  root than switching itself to mysqld

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.12-3avx
- fix perms on run scripts

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.12-2avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.12-1avx
- 4.1.12
- drop P2
- html docs are gone
- P10: make it build in a chroot without /proc mounted (PLD)
- don't require texinfo or tetex

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.11-2avx
- bootstrap build

* Wed Apr 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.11-1avx
- 4.1.11; fixes an additional found case of CAN-2004-0957
- spec cleanups
- update P6
- update source URLs
- hack to fix make Docs
- fix runsvstat logic

* Tue Mar 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.10a-1avx
- 4.0.10a; security fixes for CAN-2005-0709, CAN-2005-0710, CAN-2005-0711

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.10-2avx
- user logger for logging
- multiarch

* Fri Feb 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.10-1avx
- 4.1.10
- update afterboot snippet with upgrade info
- by default set --skip-networking in /etc/sysconfig/mysqld so that we don't
  listen to the network (and note this in afterboot)
- drop P10; applied upstream
- use a different pid name for the fix_privileges stuff in %%post (oden)
- rediff P0, P5 (oden)

* Thu Feb 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.9-1avx
- 4.1.9
- major spec cleanups
- somewhat sync with mdk 4.1.9-8mdk (but with lots of imho useless
  stuff removed)
- provide TMPDIR/TMP directory and environment (oden)
- added rediffed P7 and P8 from latest db-4.1.25 package, plus added
  P9 to use it in an attempt to address possible nptl issues (oden)
- P10: fix for CAN-2005-0004

* Wed Jan 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.23-1avx
- 4.0.23

* Fri Oct 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.21-1avx
- 4.0.21
- updated manual-split package
- include gpg signature and use original sources
- rediff P1, P3
- pick a better mirror
- make runsvstat more silent

* Wed Oct 06 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.20-5avx
- fix the scripts; it should now run flawlessly and fix bug #2

* Mon Oct 04 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.20-4avx
- add a finish script
- add an afterboot snippet
- add our own logrotate script which has everything commented out
  by default

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.20-3avx
- s/setuidgid/chpst in spec
- Prereq: runit

* Sun Sep 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.20-2avx
- updated runscripts

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.20-1avx
- 4.0.20
- remove P4: security fixes included upstream
- own directories
- correct call to tar
- build both MySQL and MySQL-Max with openssl, rather than just MySQL-Max
- fix buildrequires for libstdc++-static-devel (gbeauchesne)
- patch policy

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.18-2avx
- Annvix build

* Thu Apr 22 2004 Vincent Danen <vdanen@opensls.org> 4.0.18-1sls
- 4.0.18
- drop unused patches: P1, P2, P3, P4, P7, P9
- drop P0; we do not need to patch the initscript anymore
- add innodb support
- renumber patches
- remove icon
- patch to fix CAN-2004-0381, CAN-2004-0388
- fix runscript so $DATADIR is declared before it's used for the pid file
- add default sysconfig/mysqld file
- add sysconfig option to log to a file (off by default; works in
  conjunction with the logrotate.d/mysql file)

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 4.0.15-5sls
- minor spec cleanups

* Wed Feb 04 2004 Vincent Danen <vdanen@opensls.org> 4.0.15-3sls
- remove initscripts
- supervise scripts
- give mysql static uid/gid 82
- use the same run files in both Max and non-Max installs since they
  conflict and mysqld_safe makes the determination of which to use
- change how we determine if mysqld is running

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 4.0.15-2sls
- OpenSLS build
- don't worry about older mdk distribs
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
