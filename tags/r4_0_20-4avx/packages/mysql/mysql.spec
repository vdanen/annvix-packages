%define name	MySQL
%define version	4.0.20
%define release	4avx

%define major		12
%define libname_orig	mysql
%define libname		%mklibname %{libname_orig} %{major}

%define shared_lib_version	12:0:0
%define mysqld_user		mysql
%define var			/var

%define _requires_exceptions perl(this)

%define see_base For a description of MySQL see the base MySQL RPM or http://www.mysql.com

Summary:	MySQL: a very fast and reliable SQL database engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Databases
URL:            http://www.mysql.com
Source:		ftp.free.fr:/pub/MySQL/Downloads/MySQL-4.0/mysql-%{version}.tar.bz2
Source1:	ftp://ftp.free.fr:/pub/MySQL/Downloads/Manual/manual-split.tar.bz2
Source2:	mysqld.run
Source3:	mysqld-log.run
Source4:	mysqld.sysconfig
Source5:	mysqld.finish
Source6:	05_mysql.afterboot
Source7:	logrotate.mysqld
Patch1:		MySQL-4.0.16-mdk-fix_install_scripts.patch.bz2
Patch2:		mysql-mdk-all_charset.patch.bz2
Patch3:		mysql-4.0.17-mdk-lib64.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	bison, db4-devel, glibc-static-devel, libstdc++-static-devel, automake1.7
BuildRequires:	termcap-devel
BuildRequires:	ncurses-devel, python, openssl-static-devel, tetex, texinfo, zlib-devel

Provides:       msqlormysql MySQL-server mysqlserver mysql
PreReq:		MySQL-common = %{version}-%{release} rpm-helper runit
Obsoletes:      mysql MySQL-devel <= 3.23.39
Conflicts:      MySQL-Max > 4.0.11

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

%package common
Summary:	MySQL: common files
Group:          Databases
Prereq:  	rpm-helper
Requires:       MySQL-client

%description common
Common files for the MySQL(TM) database server.

%{see_base}

%package client
Summary:        MySQL - Client
Group:          Databases
Obsoletes:      mysql-client
Provides:       mysql-client 
Requires:       %{libname} = %{version}-%{release}

%description client
This package contains the standard MySQL clients.

%{see_base}

%package bench
Summary:        MySQL - Benchmarks and test system
Group:          Databases
Obsoletes:      mysql-bench
Provides:       mysql-bench
Requires:       MySQL-client = %{version}-%{release} perl

%description bench
This package contains MySQL benchmark scripts and data.

%{see_base}

%package -n %{libname}-devel
Summary:        MySQL - Development header files and libraries
Group:          Development/Other
Obsoletes:      MySQL-devel mysql-devel
Provides:       MySQL-devel = %{version}-%{release} mysql-devel = %{version}-%{release} %{libname_orig}-devel = %{version}-%{release}
Requires:       %{libname} = %{version} MySQL-common = %{version}-%{release} MySQL-client = %{version}-%{release}
Provides:	libmysql-devel

%description -n %{libname}-devel
This package contains the development header files and libraries
necessary to develop MySQL client applications.

%{see_base}

%package -n %{libname}
Summary:        MySQL - Shared libraries
Group:          System/Libraries
Obsoletes:      MySQL-shared-libs MySQL-shared
Provides:       MySQL-shared-libs = %{version}-%{release} MySQL-shared = %{version}-%{release}

%description -n %{libname}
This package contains the shared libraries (*.so*) which certain
languages and applications need to dynamically load and use MySQL.

%package Max
Release:	%{release}
Summary:	MySQL - server with Berkeley DB and Innodb support
Group:		Databases
Provides:	mysql-Max = %{version}-%{release}
Provides:	msqlormysql MySQL-server mysqlserver mysql
Obsoletes:	mysql-Max
PreReq:		MySQL-common = %{version}-%{release} rpm-helper runit
Conflicts:	MySQL > 4.0.11

%description Max 
Optional MySQL server binary that supports features
like transactional tables. You can use it as an alternate
to MySQL basic server.

%prep
%setup -q -n mysql-%{version}

%patch1 -p0 -b .max
%patch2 -p1 -b .charset
%patch3 -p0 -b .lib64

# 20021227 warly manual include files not in the archives
# perl -pi -e 's/\@include reservedwords.texi//' ./Docs/manual.texi
# perl -pi -e 's/..\/MIRRORS INSTALL-BINARY/INSTALL-BINARY/' ./Docs/Makefile.am

# Run aclocal in order to get an updated libtool.m4 in generated
# configure script for "new" architectures (aka. x86_64, mips)
export WANT_AUTOCONF_2_5=1
aclocal-1.7
autoconf
automake-1.7

%build
%serverbuild

FollowLink() {
  perl -e '{my $f = shift; $f = readlink $f while (-l $f); print $f, "\n"}' $0
}

# (gb) We shall always have the fully versioned binary
# FIXME: Please, please, do tell why you need fully qualified version
GCC_VERSION=`gcc -dumpversion`
CFLAGS="$CFLAGS -DHAVE_ERRNO_AS_DEFINE"
%ifarch alpha
CXXFLAGS="$CXXFLAGS -DHAVE_ERRNO_AS_DEFINE -fPIC"
%else
CXXFLAGS="$CXXFLAGS -DHAVE_ERRNO_AS_DEFINE"
%endif
export MYSQL_BUILD_CC="gcc-$GCC_VERSION"
export MYSQL_BUILD_CXX="g++-$GCC_VERSION"

export MYSQL_BUILD_CFLAGS="$CFLAGS"
export MYSQL_BUILD_CXXFLAGS="$CXXFLAGS"
	
BuildMySQL() {
# The --enable-assembler simply does nothing on systems that does not
# support assembler speedups.

%configure2_5x \
 	    $* \
	    --enable-assembler \
	    --enable-local-infile \
            --with-mysqld-user=%{mysqld_user} \
	    --with-openssl \
            --with-unix-socket-path=/var/lib/mysql/mysql.sock \
            --prefix=/ \
	    --with-extra-charsets=complex \
            --exec-prefix=%{_prefix} \
            --libexecdir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --localstatedir=%{_localstatedir}/mysql \
            --infodir=%{_infodir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
            --program-prefix= ;
#	    --with-comment=\"%{distribution} MySQL RPM\";
	    # Add this for more debugging support
	    # --with-debug
	    # Add this for MyISAM RAID support:
	    # --with-raid

 # benchdir does not fit in above model. Maybe a separate bench distribution
 %make benchdir_root=$RPM_BUILD_ROOT%{_datadir}
}

# Use our own copy of glibc
OTHER_LIBC_DIR=/%{_lib}
USE_OTHER_LIBC_DIR=""
if test -d "$OTHER_LIBC_DIR"
then
  USE_OTHER_LIBC_DIR="--with-other-libc=$OTHER_LIBC_DIR"
fi

# Use the build root for temporary storage of the shared libraries.

RBR=$RPM_BUILD_ROOT
MBD=$RPM_BUILD_DIR/mysql-%{version}

#
# Use MYSQL_BUILD_PATH so that we can use a dedicated version of gcc
#
PATH=${MYSQL_BUILD_PATH:-/bin:/usr/bin}
export PATH

# We need to build shared libraries separate from mysqld-max because we
# are using --with-other-libc

# BuildMySQL "--disable-shared $USE_OTHER_LIBC_DIR --with-berkeley-db --with-innodb --with-mysqld-ldflags='-all-static' --with-server-suffix='-Max'"
BuildMySQL "--enable-shared --with-berkeley-db --with-innodb --with-server-suffix='-Max'"

# Save mysqld-max
mv sql/mysqld sql/mysqld-max
nm --numeric-sort sql/mysqld-max > sql/mysqld-max.sym

# Save manual to avoid rebuilding
mv Docs/manual.ps Docs/manual.ps.save
make distclean
mv Docs/manual.ps.save Docs/manual.ps

#now build and save shared libraries

#  BuildMySQL "--enable-shared --enable-thread-safe-client --without-server "
#  (cd libmysql/.libs; tar cf $MBD/shared-libs.tar *.so*)
#  (cd libmysql_r/.libs; tar rf $MBD/shared-libs.tar *.so*)

#  # Save manual to avoid rebuilding
#  mv Docs/manual.ps Docs/manual.ps.save
#  make distclean
#  mv Docs/manual.ps.save Docs/manual.ps

# RPM:s destroys Makefile.in files, so we generate them here
automake-1.7

# BuildMySQL "--enable-shared " \
# 	   "--with-mysqld-ldflags='-all-static'" \
# 	   "--with-client-ldflags='-all-static'" \
#  	   "$USE_OTHER_LIBC_DIR" \
# 	   "--without-berkeley-db --without-innodb"

BuildMySQL "--enable-shared" \
           "--enable-thread-safe-client" \
	   "--without-berkeley-db --with-innodb"

nm --numeric-sort sql/mysqld > sql/mysqld.sym

%install 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
RBR=$RPM_BUILD_ROOT
MBD=$RPM_BUILD_DIR/mysql-%{version}
# Ensure that needed directories exists
install -d $RBR%{_sysconfdir}/logrotate.d
install -d $RBR%{_localstatedir}/mysql/mysql
install -d $RBR%{_datadir}/sql-bench
install -d $RBR%{_datadir}/mysql-test
install -d $RBR%{_sbindir}
install -d $RBR%{_datadir}
install -d $RBR%{_mandir}
install -d $RBR%{_includedir}
install -d $RBR%{_infodir}
install -d $RBR%{_docdir}/%{name}-%{version}
install -d $RBR%{_docdir}/%{name}-%{version}/chapter
install -d $RBR%{_libdir}

make install DESTDIR=$RBR benchdir_root=%{_datadir}

# Install shared libraries (Disable for architectures that don't support it)
# (cd $RBR%{_libdir}; tar xf $MBD/shared-libs.tar)

# install saved mysqld-max
install -m755 $MBD/sql/mysqld-max $RBR/usr/sbin/mysqld-max

# install symbol files ( for stack trace resolution)
install -m644 $MBD/sql/mysqld-max.sym $RBR%{_libdir}/mysql/mysqld-max.sym
install -m644 $MBD/sql/mysqld.sym $RBR%{_libdir}/mysql/mysqld.sym

install -m 0644 %{SOURCE7} $RBR%{_sysconfdir}/logrotate.d/mysql

mkdir -p %{buildroot}%{_srvdir}/mysqld/log
mkdir -p %{buildroot}%{_srvlogdir}/mysqld
install -m 0750 %{SOURCE2} %{buildroot}%{_srvdir}/mysqld/run
install -m 0750 %{SOURCE5} %{buildroot}%{_srvdir}/mysqld/finish
install -m 0750 %{SOURCE3} %{buildroot}%{_srvdir}/mysqld/log/run

# Install docs
install -m644 $MBD/Docs/mysql.info \
 $RBR%{_infodir}/mysql.info

for file in README COPYING Docs/manual_toc.html Docs/manual.html \
    Docs/manual.txt Docs/manual.texi Docs/manual.ps \
    support-files/my-huge.cnf support-files/my-large.cnf \
    support-files/my-medium.cnf support-files/my-small.cnf
do
    b=`basename $file`
    install -m644 $MBD/$file $RBR%{_docdir}/MySQL-%{version}/$b
done

pushd $RBR%{_docdir}/MySQL-%{version}/chapter
tar tjvf %{SOURCE1}
popd

#Fix libraries
mv $RBR%{_libdir}/mysql/libmysqlclient.* ${RBR}%{_libdir}/
mv $RBR%{_libdir}/mysql/libmysqlclient_r.* ${RBR}%{_libdir}/
perl -pi -e "s|%{_libdir}/mysql|%{_libdir}|" \
	${RBR}%{_libdir}/libmysqlclient.la  ${RBR}%{_libdir}/libmysqlclient_r.la

pushd $RBR%{_bindir}
ln -sf mysqlcheck mysqlrepair
ln -sf mysqlcheck mysqlanalyze
ln -sf mysqlcheck mysqloptimize
popd

mysql_datadir=$RPM_BUILD_ROOT/%{_localstatedir}/mysql
# Create data directory if needed
if test ! -d $mysql_datadir;		then mkdir -p $mysql_datadir; fi
if test ! -d $mysql_datadir/mysql;	then mkdir $mysql_datadir/mysql; fi
if test ! -d $mysql_datadir/test;	then mkdir $mysql_datadir/test; fi
chmod -R og-rw $mysql_datadir/mysql

rm -rf $RPM_BUILD_ROOT%{_datadir}/info/dir $RPM_BUILD_ROOT/shared-libs.tar
rm -rf $RPM_BUILD_ROOT%{_datadir}/info/dir $RPM_BUILD_ROOT/shared-libs.tar
rm -rf $RPM_BUILD_ROOT%{_bindir}/make_win_src_distribution
rm -rf $RPM_BUILD_ROOT%{_bindir}/make_win_binary_distribution

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/mysqld

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE6} %{buildroot}%{_datadir}/afterboot/05_mysql

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
EOF

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%pre common
%_pre_useradd mysql %{_localstatedir}/mysql /bin/bash 82

%post common
%_install_info mysql.info
%_mkafterboot

%post
# Initiate databases
/sbin/chpst -u mysql mysql_install_db -IN-RPM >/dev/null

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
    pid_file=$datadir/mysql.pid
    if %{_bindir}/mysqld_safe --skip-grant-tables --skip-networking --pid-file=$pid_file &> /dev/null & then  
        pid=$!
        i=1
        while [ $i -lt 10 -a ! -f $pid_file ]; do 
            i=$(($i+1))
            sleep 1
        done
        if [ -f $datadir/mysql.pid ]; then
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

if [ "x`runsvstat /service/mysqld|grep down >/dev/null 2>&1; echo $?`" = "x0" ]; then
    fix_privileges
else
    /usr/sbin/srv stop mysqld &> /dev/null
    fix_privileges
    /usr/sbin/srv start mysqld &> /dev/null 
fi

%post Max
/sbin/chpst -u mysql mysql_install_db -IN-RPM >/dev/null

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
    pid_file=$datadir/mysql.pid
    if %{_bindir}/mysqld_safe --skip-grant-tables --skip-networking --pid-file=$pid_file &> /dev/null & then  
        pid=$!
        i=1
        while [ $i -lt 10 -a ! -f $pid_file ]; do 
            i=$(($i+1))
            sleep 1
        done
        if [ -f $datadir/mysql.pid ]; then
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

if [ "x`runsvstat /service/mysqld|grep down >/dev/null 2>&1; echo $?`" = "x0" ]; then
    fix_privileges
else
    /usr/sbin/srv stop mysqld &> /dev/null
    fix_privileges
    /usr/sbin/srv start mysqld &> /dev/null 
fi

%preun
%_preun_srv mysqld
# We do not remove the mysql user since it may still own a lot of
# database files.

%preun common
%_remove_install_info mysql.info

%postun common
%_mkafterboot

%preun Max
%_preun_srv mysqld

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files common -f mysql.lang
%defattr(-, root, root) 
%doc %{_docdir}/MySQL-%{version}/
%{_bindir}/isamchk
%{_bindir}/isamlog
%{_bindir}/pack_isam
%{_bindir}/myisamchk
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_fix_privilege_tables
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_install_db
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_explain_log 
%{_bindir}/mysql_fix_extensions 
%{_bindir}/mysql_install 
%{_bindir}/mysql_secure_installation 
%{_bindir}/mysql_tableinfo 
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
%config(noreplace) %{_sysconfdir}/logrotate.d/mysql
%dir %attr(-,mysql,mysql) %{_localstatedir}/mysql
%dir %attr(-,mysql,mysql) %{_localstatedir}/mysql/mysql
%dir %attr(-,mysql,mysql) %{_localstatedir}/mysql/test
%dir %{_datadir}/mysql
%{_datadir}/mysql/binary-configure
%{_datadir}/mysql/make_binary_distribution
%{_datadir}/mysql/make_sharedlib_distribution
%{_datadir}/mysql/mi_test_all
%{_datadir}/mysql/mi_test_all.res
%{_datadir}/mysql/my-huge.cnf
%{_datadir}/mysql/my-large.cnf
%{_datadir}/mysql/my-medium.cnf
%{_datadir}/mysql/my-small.cnf
%{_datadir}/mysql/mysql-*.spec
%{_datadir}/mysql/mysql-log-rotate
%{_datadir}/mysql/charsets
%{_datadir}/mysql/mysql.server
%{_datadir}/mysql/english
%{_datadir}/mysql/Description.plist
%{_datadir}/mysql/Info.plist
%{_datadir}/mysql/StartupParameters.plist
%{_datadir}/mysql/postinstall
%{_datadir}/mysql/preinstall
%{_datadir}/mysql/MySQL-shared-compat.spec
%{_datadir}/afterboot/05_mysql

%files
%defattr(-, root, root) 
%{_sbindir}/mysqld
%dir %{_libdir}/mysql
%{_libdir}/mysql/mysqld.sym
%dir %{_srvdir}/mysqld
%dir %{_srvdir}/mysqld/log
%{_srvdir}/mysqld/run
%{_srvdir}/mysqld/finish
%{_srvdir}/mysqld/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/mysqld
%config(noreplace) %{_sysconfdir}/sysconfig/mysqld

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

%files -n %{libname}-devel
%defattr(-, root, root)
%doc INSTALL-SOURCE
%{_bindir}/comp_err
%{_includedir}/mysql/
%dir %{_libdir}/mysql
%{_libdir}/mysql/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.a
%{_bindir}/mysql_config

%files -n %{libname}
%defattr(-, root, root)
# Shared olibraries (omit for architectures that don't support them)
%{_libdir}/*.so.*

%files bench
%defattr(-, root, root)
%doc sql-bench/README
%{_datadir}/sql-bench
%{_datadir}/mysql-test

%files Max
%defattr(-, root, root)
%{_sbindir}/mysqld-max
%dir %{_libdir}/mysql
%{_libdir}/mysql/mysqld-max.sym
%dir %{_srvdir}/mysqld
%dir %{_srvdir}/mysqld/log
%{_srvdir}/mysqld/run
%{_srvdir}/mysqld/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/mysqld
%config(noreplace) %{_sysconfdir}/sysconfig/mysqld

%changelog
* Mon Oct 04 2004 Vincent Danen <vdanen@annvix.org> 4.0.20-4avx
- add a finish script
- add an afterboot snippet
- add our own logrotate script which has everything commented out
  by default

* Mon Sep 20 2004 Vincent Danen <vdanen@annvix.org> 4.0.20-3avx
- s/setuidgid/chpst in spec
- Prereq: runit

* Sun Sep 19 2004 Vincent Danen <vdanen@annvix.org> 4.0.20-2avx
- updated runscripts

* Fri Aug 13 2004 Vincent Danen <vdanen@annvix.org> 4.0.20-1avx
- 4.0.20
- remove P4: security fixes included upstream
- own directories
- correct call to tar
- build both MySQL and MySQL-Max with openssl, rather than just MySQL-Max
- fix buildrequires for libstdc++-static-devel (gbeauchesne)
- patch policy

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 4.0.18-2avx
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

