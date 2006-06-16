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
%define version		1.2.7
%define release		%_revrel

%define apuver		1
%define libname		%mklibname %{name} %{apuver}

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
Patch1:		apr-util-0.9.5-lib64.diff
Patch2:		apr-util-1.2.2-postgresql.diff
Patch3:		apr-util-1.2.7-exports.diff
Patch4:		apr-util-1.2.7-dso.diff
Patch5:		apr-util-1.2.7-link.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, automake1.7, libtool, doxygen
BuildRequires:	apr-devel >= 1:1.2.7
BuildRequires:	openldap-devel, db4-devel, gdbm-devel, expat-devel
BuildRequires:	openssl-devel, mysql-devel, postgresql-devel, sqlite3-devel
BuildRequires:	python, multiarch-utils >= 1.0.3

%description
The purpose of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.


%package -n %{libname}
Summary:	Apache Portable Runtime Utility library
Group: 		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} %{name} = %{version}-%{release}
Obsoletes:	lib%{name} %{name}

%description -n	%{libname}
The purpose of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

This package includes the DBD drivers for MySQL, PostgreSQL, and
SQLite3.


%package -n %{libname}-devel
Group:		Development/C
Summary:	APR utility library development kit
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}-%{release}
Requires:	apr-util = %{version}
Requires:	apr-devel
Requires:	openldap-devel
Requires:	expat-devel
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	lib%{name}-devel %{name}-devel

%description -n	%{libname}-devel
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
%patch1 -p0 -b .lib64
%patch2 -p0 -b .postgresql
%patch3 -p0 -b .exports
%patch4 -p0 -b .dso
%patch5 -p0 -b .link

cat %{SOURCE2} >dbd/apr_dbd_mysql.c

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
libtoolize --copy --force && aclocal-1.7 && autoconf --force

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
libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -avoid-version -module dbd/apr_dbd_pgsql.lo -lpq  -o dbd/apr_dbd_pgsql.la

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

# multiacrh anti-borker
perl -pi -e "s|^LDFLAGS=.*|LDFLAGS=\"\"|g" %{buildroot}%{_bindir}/apu-%{apuver}-config

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

%files -n %{libname}-devel
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

* Wed Sep 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-8mdk
- security fix (P100) for CAN-2004-0786

* Tue Aug 10 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-7mdk
- rebuilt against db4.2

* Wed Jun 30 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-6mdk
- new P0
- drop P3,P4,P6 and P8 the fix is implemented upstream
- drop P5, another fix is implemented upstream
- fix P7, it's partially implemented upstream

* Thu Jun 17 2004 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.5-5mdk
- rebuild with new openssl 

* Thu Jun 17 2004 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.5-4mdk
- rebuild

* Tue May 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-2mdk
- rebuild

* Fri May 07 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-1mdk
- initial fedora import and mandrake adaptions

* Thu Apr  1 2004 Joe Orton <jorton@redhat.com> 0.9.4-14
- fix use of SHA1 passwords (#119651)

* Tue Mar 30 2004 Joe Orton <jorton@redhat.com> 0.9.4-13
- remove fundamentally broken check_sbcs() from xlate code

* Fri Mar 19 2004 Joe Orton <jorton@redhat.com> 0.9.4-12
- tweak xlate fix

* Fri Mar 19 2004 Joe Orton <jorton@redhat.com> 0.9.4-11
- rebuild with xlate fixes and tests enabled

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 0.9.4-10.1
- rebuilt

* Tue Mar  2 2004 Joe Orton <jorton@redhat.com> 0.9.4-10
- rename sdbm_* symbols to apu__sdbm_*

* Mon Feb 16 2004 Joe Orton <jorton@redhat.com> 0.9.4-9
- fix sdbm apr_dbm_exists() on s390x/ppc64

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 0.9.4-8
- rebuilt

* Thu Feb  5 2004 Joe Orton <jorton@redhat.com> 0.9.4-7
- fix warnings from use of apr_optional*.h with gcc 3.4

* Thu Jan 29 2004 Joe Orton <jorton@redhat.com> 0.9.4-6
- drop gdbm support

* Thu Jan  8 2004 Joe Orton <jorton@redhat.com> 0.9.4-5
- fix DB library detection

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 0.9.4-4
- rebuild against db-4.2.52.

* Mon Oct 13 2003 Jeff Johnson <jbj@jbj.org> 0.9.4-3
- rebuild against db-4.2.42.

* Mon Oct  6 2003 Joe Orton <jorton@redhat.com> 0.9.4-2
- fix 'apu-config --apu-la-file' output

* Mon Oct  6 2003 Joe Orton <jorton@redhat.com> 0.9.4-1
- update to 0.9.4.

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.3-10
- rebuild

* Mon Jul  7 2003 Joe Orton <jorton@redhat.com> 0.9.3-9
- rebuild
- don't run testuuid test because of #98677

* Thu Jul  3 2003 Joe Orton <jorton@redhat.com> 0.9.3-8
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 20 2003 Joe Orton <jorton@redhat.com> 0.9.3-6
- fix to detect crypt_r correctly (CAN-2003-0195)

* Thu May 15 2003 Joe Orton <jorton@redhat.com> 0.9.3-5
- fix to try linking against -ldb first (#90917)
- depend on openldap, gdbm, db4, expat appropriately.

* Tue May 13 2003 Joe Orton <jorton@redhat.com> 0.9.3-4
- rebuild

* Wed May  7 2003 Joe Orton <jorton@redhat.com> 0.9.3-3
- make devel package conflict with old subversion-devel
- run the less crufty parts of the test suite

* Tue Apr 29 2003 Joe Orton <jorton@redhat.com> 0.9.3-2
- run ldconfig in post/postun

* Mon Apr 28 2003 Joe Orton <jorton@redhat.com> 0.9.3-1
- initial build

