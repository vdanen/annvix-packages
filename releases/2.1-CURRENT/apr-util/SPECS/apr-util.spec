#
# spec file for package apr-util
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		apr-util
%define version		1.2.12
%define release		%_revrel

%define apuver		1
%define libname		%mklibname %{name} %{apuver}
%define devname		%mklibname %{name} -d

Summary:	Apache Portable Runtime Utility library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Libraries
URL:		http://apr.apache.org/
Source0:	http://www.apache.org/dist/apr/%{name}-%{version}.tar.gz
Source1:	http://www.apache.org/dist/apr/%{name}-%{version}.tar.gz.asc
# http://apache.webthing.com/database/apr_dbd_mysql.c
# http://apache.webthing.com/svn/apache/apr/apr_dbd_mysql.c
Source2:	apr_dbd_mysql.c
Patch0:		apr-util-1.2.2-config.diff
Patch2:		apr-util-1.2.8-postgresql.patch
Patch3:		apr-util-1.2.12-mdv-no_linkage.patch
Patch4:		apr-util-1.2.7-dso.diff
Patch5:		apr-util-1.2.7-link.diff
Patch6:		apr-util-1.2.7-apr_dbd_mysql_headers.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	libtool
BuildRequires:	doxygen
BuildRequires:	apr-devel >= 1:1.2.12
BuildRequires:	openldap-devel
BuildRequires:	db4-devel
BuildRequires:	gdbm-devel
BuildRequires:	expat-devel
BuildRequires:	openssl-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	sqlite-devel
BuildRequires:	python
BuildRequires:	multiarch-utils >= 1.0.3

%description
The purpose of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.


%package -n %{libname}
Summary:	Apache Portable Runtime Utility library
Group: 		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}

%description -n	%{libname}
The purpose of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

This package includes the DBD drivers for MySQL, PostgreSQL, and
SQLite3.


%package -n %{devname}
Group:		Development/C
Summary:	APR utility library development kit
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Requires:	apr-devel
Requires:	openldap-devel
Requires:	expat-devel
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 -d

%description -n	%{devname}
This package provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0 -b .config
%patch2 -p1 -b .postgresql
%patch3 -p0 -b .exports
%patch4 -p0 -b .dso
%patch5 -p0 -b .link

cp %{_sourcedir}/apr_dbd_mysql.c dbd/apr_dbd_mysql.c

%build
cat >> config.layout << EOF
<Layout AVX>
    prefix:        %{_prefix}
    exec_prefix:   %{_prefix}
    bindir:        %{_bindir}
    sbindir:       %{_sbindir}
    libdir:        %{_libdir}
    libexecdir:    %{_libexecdir}
    mandir:        %{_mandir}
    infodir:       %{_infodir}
    includedir:    %{_includedir}/apr-%{apuver}
    sysconfdir:    %{_sysconfdir}
    datadir:       %{_datadir}
    installbuilddir: %{_libdir}/apr-%{aprver}/build
    localstatedir: /var
    runtimedir:    /var/run
    libsuffix:     -\${APRUTIL_MAJOR_VERSION}
</Layout>
EOF

# We need to re-run ./buildconf because of any applied patch(es)
#./buildconf --with-apr=%{_prefix}

# buildconf is borked...
cp %{_libdir}/apr-%{apuver}/build/apr_common.m4 %{_libdir}/apr-%{apuver}/build/find_apr.m4 %{_libdir}/apr-%{apuver}/build/gen-build.py build/

# conditional lib64 hack
%if "%{_lib}" != "lib"
perl -pi -e "s|/lib\b|/%{_lib}|g" build/*.m4
%endif

export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal-1.7; autoconf --force

python build/gen-build.py make

sed -i -e '/OBJECTS_all/s, dbd/apr_dbd_[^ ]*\.lo,,g' build-outputs.mk

# use sqlite3 only
export apu_have_sqlite2='0'
cat >> config.cache << EOF
ac_cv_header_sqlite_h=no
ac_cv_lib_sqlite_sqlite_open=no
EOF


%configure2_5x \
    --cache-file=config.cache \
    --with-apr=%{_prefix} \
    --includedir=%{_includedir}/apr-%{apuver} \
    --with-installbuilddir=%{_libdir}/apr-%{aprver}/build \
    --enable-layout=AVX \
    --with-ldap \
    --with-mysql=%{_prefix} \
    --with-pgsql=%{_prefix} \
    --without-sqlite2 \
    --with-sqlite3=%{_prefix} \
    --with-berkeley-db \
    --without-gdbm

%make
make dox

make dbd/apr_dbd_mysql.lo
libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -avoid-version -module dbd/apr_dbd_mysql.lo -lmysqlclient_r -o dbd/apr_dbd_mysql.la

make dbd/apr_dbd_pgsql.lo
libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -avoid-version -module dbd/apr_dbd_pgsql.lo -lpq -o dbd/apr_dbd_pgsql.la

make dbd/apr_dbd_sqlite3.lo
libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -avoid-version -module dbd/apr_dbd_sqlite3.lo -lsqlite3 -o dbd/apr_dbd_sqlite3.la


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

libtool --mode=install %{_bindir}/install -c -m 755 dbd/apr_dbd_mysql.la %{buildroot}%{_libdir}
libtool --mode=install %{_bindir}/install -c -m 755 dbd/apr_dbd_pgsql.la %{buildroot}%{_libdir}
libtool --mode=install %{_bindir}/install -c -m 755 dbd/apr_dbd_sqlite3.la %{buildroot}%{_libdir}

# Documentation
rm -rf html
mv docs/dox/html html

# Remove unnecessary exports from dependency_libs
sed -ri '/^dependency_libs/{s,-l(pq|sqlite[0-9]|mysqlclient_r|rt|dl|uuid) ,,g}' \
    %{buildroot}%{_libdir}/libapr*.la
# here as well
sed -ri '/^dependency_libs/{s,%{_libdir}/lib(sqlite[0-9]|mysqlclient_r)\.la ,,g}' \
    %{buildroot}%{_libdir}/libapr*.la

# clean apu-1-config (multiarch, includes)
perl -pi -e "s|^LDFLAGS=.*|LDFLAGS=\"\"|g" %{buildroot}%{_bindir}/apu-%{apuver}-config
perl -pi -e "s|-I%{_includedir}/mysql||g" %{buildroot}%{_bindir}/apu-%{apuver}-config

# Unpackaged files
rm -f %{buildroot}%{_libdir}/aprutil.exp


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libaprutil-%{apuver}.so.*
%attr(755,root,root) %{_libdir}/apr_dbd_mysql.so
%attr(755,root,root) %{_libdir}/apr_dbd_pgsql.so
%attr(755,root,root) %{_libdir}/apr_dbd_sqlite3.so

%files -n %{devname}
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/apu-%{apuver}-config
%{_libdir}/libaprutil-%{apuver}.*a
%{_libdir}/libaprutil-%{apuver}.so
%{_libdir}/apr_dbd_mysql.*a
%{_libdir}/apr_dbd_pgsql.*a
%{_libdir}/apr_dbd_sqlite3.*a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/apr-%{apuver}/*.h

%files doc
%defattr(-,root,root)
%doc CHANGES LICENSE
%doc --parents html


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.12
- rebuild against new mysql

* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.12
- 1.2.12
- rebuild against new apr
- buildrequires apr >= 1.2.12
- updated P3 from Mandriva

* Fri Sep 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.10
- rebuild against new postgresql, openldap, apr
- drop P1; no longer required
- updated apr_dbd_mysql.c

* Tue Jul 24 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.8
- rebuild against new mysql
- updated apr_dbd_mysql.c with a clarified license

* Sat Jun 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.8
- rebuild against new expat
- implement devel naming policy
- implement library provides policy
- cleanup obsoletes/provides

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.8
- rebuild against new postgresql

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.8
- 1.2.8
- new S2 with better mysql 5.x support
- updated patches from Mandriva
- rebuilt against new apr

* Sat Dec 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- rebuild against new mysql, new postgresql, and new openldap

* Tue Nov 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- rebuild against new sqlite

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- rebuild against new mysql

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- rebuild against new openssl
- spec cleanups

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- rebuild against new db4

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- rebuild against new sqlite3

* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- rebuild against new postgresql

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- 1.2.7
- merge patches from mandriva
- updated dependencies
- build dbd for mysql, postgresql, and sqlite3
- add -doc subpackage
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7
- 0.9.7
- drop P8; merged upstream

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6
- Clean rebuild

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-4avx
- sync with mandriva 0.9.6-8mdk:
  - enable gdbm linkage (oden)
  - P8: apr_memcache (oden)

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-2avx
- rebuild

* Fri Feb 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-1avx
- 0.9.6
- P0: lib64 fixes (oden)
- run tests in %%build
- remove db4-devel requires from -devel pkg (mdk bug #13906) (stefan)
- remove debug build support

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.5-1avx
- first Annvix package for the new-style apache2

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
