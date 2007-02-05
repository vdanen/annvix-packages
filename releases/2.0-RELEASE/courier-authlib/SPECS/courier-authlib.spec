#
# spec file for package courier-authlib
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		courier-authlib
%define version		0.59
%define release		%_revrel

Summary:	Courier authentication library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.courier-mta.org
Source0:	http://prdownloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2
Source1:	courier-authlib.sysconftool.m4
Source2:	authdaemond.run
Source3:	authdaemond-log.run
Patch0:		courier-authlib-0.58.sysconftool.patch
Patch1:		courier-authlib-0.58.automake.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	automake1.9
BuildRequires:	expect
BuildRequires:	libltdl-devel
BuildRequires:	gdbm-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel

Obsoletes:	courier-imap-utils
Conflicts:	courier-imap <= 3.0.8

%description
The Courier authentication library provides authentication
services for other Courier applications.

This package contains the Courier authentication daemon and common
authentication modules:

 o authcustom
 o authpam
 o authpwd
 o authshadow
 o courierauthsaslclient
 o courierauthsasl


%package -n courier-authdaemon
Summary:	Courier authentication daemon
Group:		System/Servers
Requires:	%{name} = %{version}
Requires:	expect
Requires:	libltdl
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description -n courier-authdaemon
This package contains the Courier authentication daemon.


%package userdb
Summary:	Userdb support for the Courier authentication library
Group:		System/Servers
Requires(pre):	%{name} = %{version}
Requires(post):	rpm-helper
Requires(postun): rpm-helper

%description userdb
This package installs the userdb support for the Courier
authentication library.  Userdb is a simple way to manage virtual
mail accounts using a GDBM-based database file.

Install this package in order to be able to authenticate with
userdb.


%package ldap
Summary:	LDAP support for the Courier authentication library
Group:		System/Servers
Requires(pre):	%{name} = %{version}
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Obsoletes:	courier-imap-ldap

%description ldap
This package installs LDAP support for the Courier authentication
library. Install this package in order to be able to authenticate
using LDAP.


%package mysql
Summary:	MySQL support for the Courier authentication library
Group:		System/Servers
Requires(pre):	%{name} = %{version}
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Obsoletes:	courier-imap-mysql

%description mysql
This package installs MySQL support for the Courier authentication
library. Install this package in order to be able to authenticate
using MySQL.


%package pgsql
Summary:	MySQL support for the Courier authentication library
Group:		System/Servers
Requires(pre):	%{name} = %{version}
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Obsoletes:	courier-imap-pgsql

%description pgsql
This package installs PostgreSQL support for the Courier
authentication library. Install this package in order to be able
to authenticate using PostgreSQL.


%package devel
Summary:	Development libraries for the Courier authentication library
Group:		Development/C
Requires:	%{name} = %{version}

%description devel
This package contains the development libraries and files needed
to compile Courier packages that use this authentication library.
Install this package in order to build the rest of the Courier
packages. After they are built and installed this package can be
removed. Files in this package are not needed at runtime.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p 0 -b .sysconftool
%patch1 -p 0 -b .automake

cp %{_sourcedir}/courier-authlib.sysconftool.m4 .


%build
aclocal-1.9 -I .
automake-1.9
%configure \
    --with-syslog=MAIL \
    --disable-ltdl-install \
    --with-db=gdbm \
    --with-random=/dev/urandom \
    --with-mailuser=daemon \
    --with-mailgroup=daemon \
    --with-authdaemonrc=%{_sysconfdir}/courier/authdaemonrc \
    --with-authdaemonvar=%{_localstatedir}/authdaemon \
    --with-makedatprog=%{_sbindir}/makedatprog \
    --with-userdb=%{_sysconfdir}/userdb \
    --with-pkgconfdir=%{_sysconfdir}/courier \
    --with-authuserdb \
    --with-authpam \
    --with-authldap \
    --with-authldaprc=%{_sysconfdir}/courier/authldaprc \
    --with-authpwd \
    --with-authshadow \
    --without-authvchkpw \
    --with-authpgsqlrc=%{_sysconfdir}/courier/authpgsqlrc \
    --with-authpgsql \
    --with-pgsql-libs=%{_libdir} \
    --with-pgsql-includes=%{_includedir}/pgsql \
    --with-authmysqlrc=%{_sysconfdir}/courier/authmysqlrc \
    --with-authmysql \
    --with-mysql-libs=%{_libdir} \
    --with-mysql-includes=%{_includedir}/mysql \
    --with-authcustom
%make
%make authinfo


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_var}/run/authdaemon
# fix perms
chmod 0755 %{buildroot}%{_localstatedir}/authdaemon

install -m 0755 sysconftool %{buildroot}%{_libdir}/courier-authlib/
install -m 0755 authmigrate %{buildroot}%{_libdir}/courier-authlib/

mv %{buildroot}%{_libdir}/courier-authlib/authdaemond %{buildroot}%{_sbindir}/authdaemond
mv %{buildroot}%{_libdir}/courier-authlib/makedatprog %{buildroot}%{_sbindir}/makedatprog

# some utils...
install -m 0755 authinfo %{buildroot}%{_sbindir}/
install -m 0755 authdaemontest %{buildroot}%{_sbindir}/
install -m 0755 liblock/lockmail %{buildroot}%{_sbindir}/
install -m 0644 liblock/lockmail.1 %{buildroot}%{_mandir}/man1/

# fix configuration
for file in %{buildroot}%{_sysconfdir}/courier/*.dist; do
    mv $file  %{buildroot}%{_sysconfdir}/courier/`basename $file .dist`
done

chmod 0644 %{buildroot}%{_sysconfdir}/courier/*

perl -pi \
    -e "s|^authmodulelist=.*|authmodulelist=\"authpam authpwd authshadow\"|g;" \
    -e "s|^authmodulelistorig=.*|authmodulelistorig=\"authpam authpwd authshadow\"|g;" \
    %{buildroot}%{_sysconfdir}/courier/authdaemonrc

mkdir -p %{buildroot}%{_srvdir}/authdaemond/log
install -m 0740 %{_sourcedir}/authdaemond.run %{buildroot}%{_srvdir}/authdaemond/run
install -m 0740 %{_sourcedir}/authdaemond-log.run %{buildroot}%{_srvdir}/authdaemond/log/run


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n courier-authdaemon
%{_libdir}/courier-authlib/authmigrate >/dev/null
test -f %{_sysconfdir}/courier/authdaemonrc.rpmnew && %{_libdir}/courier-authlib/sysconftool %{_sysconfdir}/courier/authdaemonrc.rpmnew >/dev/null
%_post_srv authdaemond


%preun -n courier-authdaemon
%_preun_srv authdaemond


%post userdb
%_preun_srv authdaemond


%postun userdb
%_preun_srv authdaemond


%post ldap
%{_libdir}/courier-authlib/authmigrate >/dev/null
test -f %{_sysconfdir}/courier/authldaprc.rpmnew && %{_libdir}/courier-authlib/sysconftool %{_sysconfdir}/courier/authldaprc.rpmnew >/dev/null
%_preun_srv authdaemond

    
%postun ldap
%_preun_srv authdaemond


%post mysql
%{_libdir}/courier-authlib/authmigrate >/dev/null
test -f %{_sysconfdir}/courier/authmysqlrc.rpmnew && %{_libdir}/courier-authlib/sysconftool %{_sysconfdir}/courier/authmysqlrc.rpmnew >/dev/null
%_preun_srv authdaemond

    
%postun mysql
%_preun_srv authdaemond


%post pgsql
%{_libdir}/courier-authlib/authmigrate >/dev/null
test -f %{_sysconfdir}/courier/authpgsqlrc.rpmnew && %{_libdir}/courier-authlib/sysconftool %{_sysconfdir}/courier/authpgsqlrc.rpmnew >/dev/null
%_preun_srv authdaemond

    
%postun pgsql
%_preun_srv authdaemond


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/courier
%dir %{_libdir}/courier-authlib
%{_libdir}/courier-authlib/authmigrate
%{_libdir}/courier-authlib/authsystem.passwd
%{_libdir}/courier-authlib/sysconftool
%{_libdir}/courier-authlib/libcourierauthsaslclient.so.*
%{_libdir}/courier-authlib/libcourierauthsasl.so.*
%{_libdir}/courier-authlib/libcourierauthcommon.so.*
%{_libdir}/courier-authlib/libcourierauth.so.*
%{_libdir}/courier-authlib/libauthcustom.so
%{_libdir}/courier-authlib/libauthpam.so
%{_libdir}/courier-authlib/libauthpwd.so
%{_libdir}/courier-authlib/libauthshadow.so
%{_libdir}/courier-authlib/libauthpipe.so
%{_mandir}/man1/*

%files -n courier-authdaemon
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/courier/authdaemonrc
%{_sbindir}/authdaemond
%{_sbindir}/authdaemontest
%{_sbindir}/authenumerate
%{_sbindir}/authinfo
%{_sbindir}/authtest
%{_sbindir}/courierlogger
%{_sbindir}/lockmail
%{_sbindir}/authpasswd
%{_sbindir}/makedatprog
%{_localstatedir}/authdaemon
%{_var}/run/authdaemon
%dir %attr(0750,root,admin) %{_srvdir}/authdaemond
%dir %attr(0750,root,admin) %{_srvdir}/authdaemond/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/authdaemond/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/authdaemond/log/run

%files userdb
%defattr(-,root,root)
%{_sbindir}/makeuserdb
%{_sbindir}/pw2userdb
%{_sbindir}/userdb
%{_sbindir}/userdb-test-cram-md5
%{_sbindir}/userdbpw
%{_sbindir}/vchkpw2userdb
%{_libdir}/courier-authlib/libauthuserdb.so
%{_mandir}/man8/*userdb*

%files ldap
%defattr(-,root,root)
%doc README.ldap authldap.schema
%config(noreplace) %{_sysconfdir}/courier/authldaprc
%{_libdir}/courier-authlib/libauthldap.so

%files mysql
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/courier/authmysqlrc
%{_libdir}/courier-authlib/libauthmysql.so

%files pgsql
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/courier/authpgsqlrc
%{_libdir}/courier-authlib/libauthpgsql.so

%files devel
%defattr(-,root,root)
%{_bindir}/courierauthconfig
%{_libdir}/courier-authlib/*.la
%{_libdir}/courier-authlib/*.a
%{_libdir}/courier-authlib/*.so
%{_includedir}/*
%{_mandir}/man3/*
%exclude %{_libdir}/courier-authlib/libauthpgsql.so
%exclude %{_libdir}/courier-authlib/libauthmysql.so
%exclude %{_libdir}/courier-authlib/libauthuserdb.so
%exclude %{_libdir}/courier-authlib/libauthldap.so
%exclude %{_libdir}/courier-authlib/libauthcustom.so
%exclude %{_libdir}/courier-authlib/libauthpam.so
%exclude %{_libdir}/courier-authlib/libauthpwd.so
%exclude %{_libdir}/courier-authlib/libauthshadow.so
%exclude %{_libdir}/courier-authlib/libauthpipe.so

%files doc
%defattr(-,root,root)
%doc README README.authdebug.html README.html README_authlib.html
%doc NEWS COPYING* AUTHORS ChangeLog liblock/lockmail.html liblog/courierlogger.html
%doc authlib.html auth_*.html
%doc README.authpostgres.html
%doc README.authmysql.html README.authmysql.myownquery
%doc userdb/makeuserdb.html userdb/userdb.html userdb/userdbpw.html


%changelog
* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.59
- rebuild against new postgresql

* Sat Jan 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.59
- 0.59

* Sat Jan 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.58
- fix the authdaemond runscript; it's handled quite differently than it
  was before

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.58
- add a requires on libltdl and fix changelog

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.58
- first Annvix build (for new courier-imap)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
