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
%define version		4.1.14
%define release		%_revrel

%define major		14
%define libname		%mklibname mysql %{major}
%define oldlibname	%mklibname mysql 12
%define mysqld_user	mysql

%global mk_test		0
%{?_with_test: %global mk_test 1}
%{?_without_test: %global mk_test 0}

%define _requires_exceptions perl(this)

Summary:	MySQL is a very fast and reliable SQL database engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Databases
URL:        	http://www.mysql.com
Source:		ftp://ftp.mysql.serenitynet.com/MySQL-4.1/mysql-%{version}.tar.gz
Source1:	ftp://ftp.mysql.serenitynet.com/MySQL-4.1/mysql-%{version}.tar.gz.asc
Source2:	mysqld.run
Source3:	mysqld-log.run
Source4:	mysqld.finish
Source5:	05_mysql.afterboot
Source6:	logrotate.mysqld
Source7:	my.cnf
Source8:	DATADIR.env
Source9:    	LOG.env
Source10:   	MYSQLD_OPTS.env
Patch0:		mysql-4.1.10-install_script_mysqld_safe.diff
Patch1:		mysql-4.1.3-lib64.diff
Patch3:		mysql-errno.patch
Patch4:		mysql-libdir.patch
Patch5:		mysql-4.1.10-libtool.diff
Patch6:		mysql-4.1.11-rh-testing.patch
# Add fast AMD64 mutexes
Patch7:		db-4.1.24-amd64-mutexes.diff
# NPTL pthreads mutexes are evil
Patch8:		db-4.1.24-disable-pthreadsmutexes.diff
Patch9:		mysql-4.1.9-disable-pthreadsmutexes.diff
Patch10:	mysql-4.1.12-mdk-noproc.patch
Patch11:	mysql-4.1.19-CVE-2006-1516-1517.patch
Patch12:	mysql-4.1.12-CVE-2006-2753.patch

BuildRoot:      %{_buildroot}/%{name}-%{version}
BuildRequires:	bison, glibc-static-devel, libstdc++-static-devel, autoconf2.5, automake1.7
BuildRequires:	termcap-devel, multiarch-utils 
BuildRequires:	ncurses-devel, python, openssl-static-devel, zlib-devel, readline-devel

Provides:       mysql-server MySQL-server
PreReq:         rpm-helper, runit
Obsoletes:      MySQL, MySQL-devel <= 3.23.39, MySQL-common, MySQL-Max

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
Requires:       %{libname} = %{version}-%{release}
Obsoletes:	MySQL-client

%description client
This package contains the standard MySQL clients.


%package bench
Summary:        MySQL benchmarks and test system
Group:          Databases
Requires:       mysql-client = %{version}-%{release} perl
Obsoletes:	MySQL-bench

%description bench
This package contains MySQL benchmark scripts and data.


%package -n %{libname}
Summary:        MySQL shared libraries
Group:          System/Libraries

%description -n %{libname}
This package contains the shared libraries (*.so*) which certain
languages and applications need to dynamically load and use MySQL.


%package -n %{libname}-devel
Summary:        MySQL development header files and libraries
Group:          Development/Other
Obsoletes:      MySQL-devel
Provides:       mysql-devel = %{version}-%{release}
Provides:       MySQL-devel = %{version}-%{release}
Requires:       %{libname} = %{version} mysql = %{version}-%{release} mysql-client = %{version}-%{release}
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


%prep
%setup -q

%patch0 -p1 -b .install_script_mysqld_safe
%patch1 -p1 -b .lib64
%patch3 -p1 -b .errno_as_defines
%patch4 -p1 -b .libdir
%patch5 -p0 -b .libtool
%patch6 -p1 -b .testing
%patch7 -p1 -b .amd64-mutexes
%patch8 -p1 -b .pthreadsmutexes
%patch9 -p0 -b .disable-pthreadsmutexes
%patch10 -p1 -b .noproc
%patch11 -p1 -b .cve-2006-1516-1517
%patch12 -p1 -b .cve-2006-2753

# fix annoyances
perl -pi -e "s|AC_PROG_RANLIB|AC_PROG_LIBTOOL|g" configure*
perl -pi -e "s|^MAX_C_OPTIMIZE.*|MAX_C_OPTIMIZE=\"\"|g" configure*
perl -pi -e "s|^MAX_CXX_OPTIMIZE.*|MAX_CXX_OPTIMIZE=\"\"|g" configure*


%build
# Run aclocal in order to get an updated libtool.m4 in generated
# configure script for "new" architectures (aka. x86_64, mips)
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal-1.7; autoconf; automake-1.7

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
    --with-extra-charsets=complex \
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

%if %{mk_test}
make check
make test
%endif

nm --numeric-sort sql/mysqld >mysqld.sym


%install 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/chapter
mkdir -p %{buildroot}%{_var}/run/mysqld
mkdir -p %{buildroot}%{_var}/log/mysqld
mkdir -p %{buildroot}%{_localstatedir}/mysql/{mysql,test,.tmp}

%makeinstall_std benchdir_root=%{_datadir} testdir=%{_datadir}/mysql-test

install -m 0644 mysqld.sym %{buildroot}%{_libdir}/mysql/mysqld.sym

install -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/mysql
install -m 0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/my.cnf

mkdir -p %{buildroot}%{_srvdir}/mysqld/{log,env}
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/mysqld/run
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/mysqld/finish
install -m 0740 %{SOURCE3} %{buildroot}%{_srvdir}/mysqld/log/run

install -m 0640 %{SOURCE8} %{buildroot}%{_srvdir}/mysqld/env/DATADIR
install -m 0640 %{SOURCE9} %{buildroot}%{_srvdir}/mysqld/env/LOG
install -m 0640 %{SOURCE10} %{buildroot}%{_srvdir}/mysqld/env/MYSQLD_OPTS


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
rm -f %{buildroot}%{_datadir}/mysql/{postinstall,preinstall,mysql-log-rotate,mysql.server}
rm -f %{buildroot}%{_bindir}/client_test
rm -f %{buildroot}%{_bindir}/mysql_client_test

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE5} %{buildroot}%{_datadir}/afterboot/05_mysql

%find_lang mysql

cat >> mysql.lang << EOF 
%lang(cz) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(nl) %{_datadir}/mysql/dutch
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
%lang(sl) %{_datadir}/mysql/slovak
%lang(es) %{_datadir}/mysql/spanish
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian
%lang(sr) %{_datadir}/mysql/serbian
EOF

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
# Initialize database
export TMPDIR="%{_localstatedir}/mysql/.tmp"
export TMP="${TMPDIR}"
/sbin/chpst -u %{mysqld_user} %{_bindir}/mysql_install_db --rpm --user=%{mysqld_user}

if [ -d /var/log/supervise/mysqld -a ! -d /var/log/service/mysqld ]; then
    mv /var/log/supervise/mysqld /var/log/service/
fi
%_post_srv mysqld

# Allow mysqld_safe to start mysqld and print a message before we exit
sleep 2

# try to fix privileges table, use a no password user table for that
fix_privileges() 
{
    datadir=`my_print_defaults mysqld | grep '^--datadir=' | cut -d= -f2`
    if [ -z $datadir ]; then
        datadir=%{_localstatedir}/mysql/
    fi
    cd $datadir/mysql
    pid_file=$datadir/mysqld-fix_privileges.pid
    if %{_bindir}/mysqld_safe --skip-grant-tables --skip-networking --pid-file=$pid_file &> /dev/null & then  
        pid=$!
        i=1
        while [ $i -lt 10 -a ! -f $pid_file ]; do 
            i=$(($i+1))
            sleep 1
        done
        if [ -f $datadir/mysqld-fix_privileges.pid ]; then
            %{_bindir}/mysql_fix_privilege_tables &> /dev/null 
            kill `cat $pid_file` &> /dev/null
            rm -f $pid_file
        else 
            # just in case
            kill $pid &> /dev/null
        fi
        sleep 2
    fi
}

if [ "x`runsvstat /service/mysqld 2>&1|grep -q ": run"; echo $?`" == "x1" ]; then
    fix_privileges
else
    /usr/sbin/srv --down mysqld >/dev/null 2>&1
    fix_privileges
    /usr/sbin/srv --up mysqld >/dev/null 2>&1
fi


%preun
%_remove_install_info mysql.info
%_preun_srv mysqld
# We do not remove the mysql user since it may still own a lot of
# database files.


%postun
%_mkafterboot


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -f mysql.lang
%defattr(-, root, root) 
%doc README COPYING
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
%config(noreplace) %{_sysconfdir}/logrotate.d/mysql
%config(noreplace) %{_sysconfdir}/my.cnf
%{_bindir}/isamchk
%{_bindir}/isamlog
%{_bindir}/pack_isam
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
%{_bindir}/mysql_waitpid 
%{_bindir}/mysqlmanager-pwgen 
%{_bindir}/mysqlmanager
%{_bindir}/mysqlmanagerc 
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
%{_infodir}/mysql.info*
%dir %attr(0711,mysql,mysql) %{_localstatedir}/mysql
%dir %attr(0711,mysql,mysql) %{_localstatedir}/mysql/mysql
%dir %attr(0711,mysql,mysql) %{_localstatedir}/mysql/test
%dir %attr(0711,mysql,mysql) %{_localstatedir}/mysql/.tmp
%dir %attr(0755,mysql,mysql) %{_var}/run/mysqld
%dir %attr(0755,mysql,mysql) %{_var}/log/mysqld
%dir %{_datadir}/mysql
%{_datadir}/mysql/binary-configure
%{_datadir}/mysql/mi_test_all
%{_datadir}/mysql/mi_test_all.res
%{_datadir}/mysql/my-huge.cnf
%{_datadir}/mysql/my-large.cnf
%{_datadir}/mysql/my-medium.cnf
%{_datadir}/mysql/my-small.cnf
%{_datadir}/mysql/my-innodb-heavy-4G.cnf
%{_datadir}/mysql/charsets
%{_datadir}/mysql/english
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_fix_privilege_tables.sql
%{_datadir}/mysql/japanese-sjis
%{_datadir}/mysql/*.ini
%{_datadir}/afterboot/05_mysql
%dir %{_libdir}/mysql


%files bench
%defattr(-, root, root)
%doc sql-bench/README
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
%{_mandir}/man1/*.1*


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*


%files -n %{libname}-devel
%defattr(-,root,root)
%doc INSTALL-SOURCE
%{_bindir}/comp_err
%multiarch %{multiarch_bindir}/mysql_config
%{_bindir}/mysql_config
%{_includedir}/mysql
%multiarch %{multiarch_includedir}/mysql/my_config.h
%dir %{_libdir}/mysql
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/mysql/*.a


%changelog
* Wed Jun 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14
- P12: security fix for CVE-2006-2753

* Fri May 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.14
- P11: security fixes for CVE-2006-1516, CVE-2006-1517

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

* Sun Sep 14 2003 Warly <warly@mandrakesoft.com> 4.0.15-1mdk
- Security update

* Fri Aug  8 2003 Warly <warly@mandrakesoft.com> 4.0.14-1mdk
- new version (main changes):
   * Enabled `INSERT' from `SELECT' when the table into which the records are inserted is also a table listed in the `SELECT'.
   * Added `--nice' option to `mysqld_safe' to allow setting the  niceness of the `mysqld' process.
   * `RESET SLAVE' now clears the `Last_errno' and `Last_error' fields in the output of `SHOW SLAVE STATUS'.
   * Added `max_relay_log_size' variable; the relay log will be rotated
     automatically when its size exceeds `max_relay_log_size'. But if
     `max_relay_log_size' is 0 (the default), `max_binlog_size' will be
     used (as in older versions). `max_binlog_size' still applies to
     binary logs in any case.

* Fri Aug  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.13-4mdk
- lib64 fixes, quotes test fixes
- BuildRequires: termcap-devel for MDK 9.2

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 4.0.13-3mdk
- Rebuild

* Wed Jun 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0.13-2mdk
- brute fix the offending "perl(the)" stuff, remove this when perl.req is fixed.
- fix "no-prereq-on rpm-helper" for MySQL-common
- fix "no-provides libmysql-devel" for libmysql12-devel
- activated %%clean

* Fri May 30 2003 Warly <warly@mandrakesoft.com> 4.0.13-1mdk
- new version (main changes):
Functionality added or changed:
 - `PRIMARY KEY' now implies `NOT NULL'.
 - `SHOW MASTER STATUS' and `SHOW SLAVE STATUS' required the `SUPER'  privilege; now they accept `REPLICATION CLIENT' as well.
 - MySQL now issues a warning when it opens a table that was created with MySQL 4.1.
 - Option `--new' now changes binary items (`0xFFDF') to be treated
   as binary strings instead of numbers by default. This fixes some
   problems with character sets where it's convenient to input the
   string as a binary item.  After this change you have to convert
   the binary string to `INTEGER' with a `CAST' if you want to
   compare two binary items with each other and know which one is
   bigger than the other.  `SELECT CAST(0xfeff AS UNSIGNED) <
   CAST(0xff AS UNSIGNED)'.  This will be the default behaviour in
   MySQL 4.1. (Bug #152)
 - Fixed bug with `NATURAL LEFT JOIN', `NATURAL RIGHT JOIN' and
   `RIGHT JOIN' when using many joined tables.  The problem was that
   the `JOIN' method was not always associated with the tables
   surrounding the `JOIN' method.  If you have a query that uses many
   `RIGHT JOIN' or `NATURAL ... JOINS' you should check that they
   work as you expected after upgrading MySQL to this version.
 - Tuned optimizer to favour clustered index over table scan.
 - `BIT_AND()' and `BIT_OR()' now return an unsigned 64 bit value.
Bugs fixed:
 - Fixed `Unknown error' when using `UPDATE ... LIMIT'.
 - Fixed problem with ansi mode and `GROUP BY' with constants.
 - Fixed bug if one used a multi-table `UPDATE' and the query required a temporary table bigger than `tmp_table_size'.
 - `LOAD DATA INFILE' will now read `000000' as a zero date instead as `"2000-00-00"'.
 - Fixed bug that caused `DELETE FROM table WHERE const_expression' always to delete the whole table.
 - Fixed core dump bug when using `FORMAT('nan',#)'.
 - Fixed wrong result from truncation operator (`*') in `MATCH ... AGAINST()' in some complex joins.
 - Fixed a crash in `REPAIR ... USE_FRM' command, when used on read-only, nonexisting table or a table with a crashed index file.
 - Fixed bug in `LEFT', `RIGHT' and `MID' when used with multi-byte character sets and some `GROUP BY' queries.
 - Fix problem with `ORDER BY' being discarded for some `DISTINCT' queries.
 - Fixed that `SET SQL_BIG_SELECTS=1' works as documented (New bug in 4.0)
 - Fixed some serious bugs in `UPDATE ... ORDER BY'.
 - Fixed that `SET SQL_BIG_SELECTS=1' works again.
 - `FULLTEXT' index stopped working after `ALTER TABLE' that converts `TEXT' field to `CHAR'. 
 - Fixed a security problem with `SELECT' and wildcarded select list, when user only had partial column `SELECT' privileges on the table.
 - Only ignore world-writeable `my.cnf' files that are regular files (and not e.g. named pipes or character devices).
 - `SUM()' didn't return `NULL' when there was no rows in result or  when all values was `NULL'.
 - On Unix symbolic links handling was not enabled by default and there was no way to turn this on.
 - Fixed a bug with `NAN' in `FORMAT(...)' function ...
 - Fixed a bug with improperly cached database privileges.
 - Fixed a bug in `ALTER TABLE ENABLE / DISABLE KEYS' which failed to force a refresh of table data in the cache.
 - Fixed bugs in replication of `LOAD DATA INFILE' for custom parameters (`ENCLOSED',  `TERMINATED' and so on) and temporary tables.
 - Fixed a replication bug when the master is 3.23 and the slave 4.0:  the slave lost the replicated temporary tables if `FLUSH LOGS' was issued on the master.

* Sun May 11 2003 Stefan van der Eijk <stefan@eijk.nu> 4.0.12-3mdk
- BuildRequires openssl-static-devel
- removed redeundant BuildRequires
- fix build on alpha: add -fPIC to CXXFLAGS (thanks glee)

* Fri May  2 2003 Warly <warly@mandrakesoft.com> 4.0.12-2mdk
- buildrequires openssl-devel
- add splitted manual in 'chapter' subdir in doc dir (Steve White)

* Wed Apr  9 2003 Warly <warly@mandrakesoft.com> 4.0.12-1mdk
- new version (main changes):
 * `mysqld' no longer reads options from world-writeable config files.
 * Fixed `mysqld' crash on extremely small values of `sort_buffer' variable.
 * Fixed checking of random part of `WHERE' clause.
 * Don't allow `BACKUP TABLE' to overwrite existing files.
 * Fixed a bug with multi-table `UPDATE's when user had all privileges
   on the database where tables are located and there were any
   entries in `tables_priv' table, i.e. `grant_option' was true.
 * Fixed a bug that allowed a user with table or column grants on
   some table, `TRUNCATE' any table in the same database.
 * Fixed deadlock when doing `LOCK TABLE' followed by `DROP TABLE' in
   the same thread.  In this case one could still kill the thread
   with `KILL'.
 * Fixed query cache invalidation on `LOAD DATA'.
 * Fixed memory leak on `ANALYZE' procedure with error.
 * Fixed a bug in handling `CHAR(0)' columns that could cause wrong results from the query.
 * Fixed a crash when no database was selected and `LOAD DATA' command
   was issued with full table name specified, including database
   prefix.
- add Zdenek Mazanec patch for charset conversion fix

* Wed Mar 12 2003 Warly <warly@mandrakesoft.com> 4.0.11a-5mdk
- Apply Benjamin Pflugmann patch to mysql_install_db

* Sun Mar  9 2003 Warly <warly@mandrakesoft.com> - 4.0.11a-4mdk
- Correct post install scripts and requires

* Thu Mar  6 2003 Warly <warly@mandrakesoft.com> 4.0.11a-3mdk
- MySQL and MySQL-Max conflicts between each others
- include a separate service for mysql and mysql-max in respective server to have clean uninstall
- fix requires in MySQL MySQL-common and MySQL-max
- Try to correct post install script to fix privileges.
- fix initscripts problem with chkconfig --add

* Mon Mar  3 2003 Warly <warly@mandrakesoft.com> 4.0.11a-2mdk
- use --skip-grant-tables --skip-networking for the update process (Benjamin Pflugmann)

* Sat Mar  1 2003  <warly@ke.mandrakesoft.com> 4.0.11a-1mdk
- new version
- new MySQL-common package
- call mysql_fix_privilege_tables in post (but this will fail if
root access need a password)
- add openssl support in MySQL-Max

* Fri Feb  7 2003 Warly <warly@mandrakesoft.com> 4.0.10-1mdk
- new version
- fix initscript

* Thu Feb  6 2003 Warly <warly@mandrakesoft.com> 4.0.9-1mdk
- new version
- do not compile in static anymore
- check mysqld-max on status

* Tue Jan 28 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.23.55-1mdk
- 3.23.55; fixes a double free() in COM_CHANGE_USER
- comment out --with-comment for %%configure as it doesn't seem to like us
  anymore

* Tue Dec 24 2002 Warly <warly@mandrakesoft.com> 3.23.54a-1mdk
- new version

* Wed Nov 20 2002 Warly <warly@mandrakesoft.com> 3.23.53-5mdk
- fix /var/lib/lib/ home dir typo
- remove lang tag to english

* Tue Nov 19 2002 Warly <warly@mandrakesoft.com> 3.23.53-4mdk
- add glibc-static-devel buildrequires

* Tue Nov 19 2002 Warly <warly@mandrakesoft.com> 3.23.53-3mdk
- fix file ownership problems in /var/lib/mysql
- put lang files in %%lang

* Sat Nov  9 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.23.53-2mdk
- Patch3: Fix build on x86-64

* Wed Oct 23 2002 Warly <warly@mandrakesoft.com> 3.23.53-1mdk
- new version
 
* Sun Aug 18 2002 Christian Belisle <cbelisle@mandrakesoft.com> 3.23.52-1mdk
- update from Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- new stable version

* Sat Aug 10 2002 Christian Belisle <cbelisle@mandrakesoft.com> 3.23.51-4mdk
- fix initscript.

* Wed Jul 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.23.51-3mdk
- Patch2: Fix --with-other-libc support
- Take care of new CFLAGS from %%serverbuild
- rpmlint fixes: configure-without-libdir-spec, hardcoded-library-path
- Stop hardcoding compiler versions. Why so? and why parts of the
  %%changelog were nuked away??

* Sat Jul  6 2002 Stefan van der Eijk <stefan@eijk.nu> 3.23.51-2mdk
- BuildRequires

* Fri Jun 14 2002 Christian Belisle <cbelisle@mandrakesoft.com> 3.23.51-1mdk
- New version.

* Thu Apr 25 2002 Christian Belisle <cbelisle@mandrakesoft.com> 3.23.50-1mdk
- Synchronize with MySQL official SPEC
- Add InnoDB support
- Build against gcc 3.

* Fri Feb 15 2002 Sasha

- changed build to use --with-other-libc

* Fri Apr 13 2001 Monty

- Added mysqld-max to the distribution

* Tue Jan 2  2001  Monty

- Added mysql-test to the bench package

* Fri Aug 18 2000 Tim Smith <tim@mysql.com>

- Added separate libmysql_r directory; now both a threaded
  and non-threaded library is shipped.

* Wed Sep 28 1999 David Axmark <davida@mysql.com>

- Added the support-files/my-example.cnf to the docs directory.

- Removed devel dependency on base since it is about client
  development.

* Wed Sep 8 1999 David Axmark <davida@mysql.com>

- Cleaned up some for 3.23.

* Thu Jul 1 1999 David Axmark <davida@mysql.com>

- Added support for shared libraries in a separate sub
  package. Original fix by David Fox (dsfox@cogsci.ucsd.edu)

- The --enable-assembler switch is now automatically disables on
  platforms there assembler code is unavailable. This should allow
  building this RPM on non i386 systems.

* Mon Feb 22 1999 David Axmark <david@detron.se>

- Removed unportable cc switches from the spec file. The defaults can
  now be overridden with environment variables. This feature is used
  to compile the official RPM with optimal (but compiler version
  specific) switches.

- Removed the repetitive description parts for the sub rpms. Maybe add
  again if RPM gets a multiline macro capability.

- Added support for a pt_BR translation. Translation contributed by
  Jorge Godoy <jorge@bestway.com.br>.

* Wed Nov 4 1998 David Axmark <david@detron.se>

- A lot of changes in all the rpm and install scripts. This may even
  be a working RPM :-)

* Sun Aug 16 1998 David Axmark <david@detron.se>

- A developers changelog for MySQL is available in the source RPM. And
  there is a history of major user visible changed in the Reference
  Manual.  Only RPM specific changes will be documented here.

