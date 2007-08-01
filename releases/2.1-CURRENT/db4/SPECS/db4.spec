#
# spec file for package db4
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		db4
%define version		4.2.52
%define release		%_revrel

# compatibility with legacy rpm
%{!?_lib:%define _lib	lib}

%define	__soversion	4.2
%define	_libdb_a	libdb-%{__soversion}.a
%define	_libcxx_a	libdb_cxx-%{__soversion}.a

%define libname_orig	%mklibname db
%define libname		%{libname_orig}%{__soversion}
%define devname	%{libname}-devel
%define staticdevname	%{libname}-static-devel

%define libdbcxx	%{libname_orig}cxx%{__soversion}
%define libdbtcl	%{libname_orig}tcl%{__soversion}

%define libdbnss	%{libname_orig}nss%{__soversion}
%define libdbnssdev	%{libdbnss}-devel

Summary:	The Berkeley DB database library for C
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://www.oracle.com/technology/software/products/berkeley-db/db/
Source:		http://download.oracle.com/berkeley-db/db-%{version}.tar.bz2
Patch0:		http://www.sleepycat.com/update/4.2.52/patch.4.2.52.1
Patch1:		http://www.sleepycat.com/update/4.2.52/patch.4.2.52.2
# Add fast AMD64 mutexes
Patch2:		db-4.2.52-mdk-disable-pthreadsmutexes.patch
# NPTL pthreads mutex are evil
Patch3:		db-4.1.25-mdk-amd64-mutexes.patch
Patch4:		db-4.2.52-mdk-db185.patch
# Fix broken built-in libtool 1.5
Patch5:		db-4.2.52-mdk-libtool-fixes.patch
Patch6:		http://www.sleepycat.com/update/4.2.52/patch.4.2.52.3
Patch7:		http://www.sleepycat.com/update/4.2.52/patch.4.2.52.4
# no transaction patch from OpenLDAP 2.3 CVS pre-2.3.5, allows transactions
# to be disabled for operations that specify it (TXN_NOLOG)
Patch8:		BerkeleyDB42.patch
Patch9:		http://www.oracle.com/technology/products/berkeley-db/db/update/4.2.52/patch.4.2.52.5
Patch10:	http://www.stanford.edu/services/directory/openldap/configuration/patches/db/4252-region-fix.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	tcl
BuildRequires:	db1-devel
BuildRequires:	glibc-static-devel
BuildRequires:	ed

Requires(post):	ldconfig
Requires(postun): ldconfig

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.


%package -n %{libname}
Summary:	The Berkeley DB database library for C
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}
Requires(post):	ldconfig
Requires(postun): ldconfig

%description -n %{libname}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.


%package -n %{libdbcxx}
Summary:	The Berkeley DB database library for C++
Group:		System/Libraries
Provides:	libdbcxx = %{version}-%{release}
Requires(post):	ldconfig
Requires(postun): ldconfig

%description -n %{libdbcxx}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build C++ programs which use
Berkeley DB.


%package -n %{libdbtcl}
Summary:	The Berkeley DB database library for TCL
Group:		System/Libraries
Provides:	libdbtcl = %{version}-%{release}
Requires(post):	ldconfig
Requires(postun): ldconfig

%description -n %{libdbtcl}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the header files, libraries, and documentation for
building tcl programs which use Berkeley DB.


%package utils
Summary:	Command line tools for managing Berkeley DB databases
Group:		Databases

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains command line tools for managing Berkeley DB databases.


%package -n %{devname}
Summary:	Development libraries/header files for the Berkeley DB library
Group:		Development/Databases
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libdbtcl} = %{version}-%{release}
Requires:	%{libdbcxx} = %{version}-%{release}
Provides:	db-devel = %{version}-%{release}
Provides:	db4-devel = %{version}-%{release}
Provides:	libdb-devel = %{version}-%{release}
Provides:	%{_lib}db-devel = %{version}-%{release}
Conflicts:	%{libname_orig}3.3-devel
Conflicts:	%{libname_orig}4.0-devel

%description -n %{devname}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.


%package -n %{staticdevname}
Summary:	Development static libraries files for the Berkeley DB library
Group:		Development/Databases
Requires:	db4-devel = %{version}-%{release}
Provides:	db-static-devel = %{version}-%{release}
Provides:	db4-static-devel = %{version}-%{release}
Provides:	libdb-static-devel = %{version}-%{release}
Provides:	%{_lib}db-static-devel = %{version}-%{release}
Conflicts:	%{libname_orig}3.3-static-devel
Conflicts:	%{libname_orig}4.0-static-devel

%description -n %{staticdevname}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the static libraries for building programs which
use Berkeley DB.


%package -n %{libdbnss}
Summary:	The Berkeley DB database library for NSS modules
Group:		System/Libraries
Requires(post):	/sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n %{libdbnss}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the shared library required by some nss modules
that use Berkeley DB.


%package -n %{libdbnssdev}
Summary:	Development libraries/header files for building nss modules with Berkeley DB
Group:		Development/Databases
Requires:	%{libdbnss} = %{version}-%{release}
Provides:	libdbnss-devel = %{version}-%{release}
Provides:	%{_lib}dbnss-devel = %{version}-%{release}
Provides:	db_nss-devel = %{version}-%{release}
Provides:	libdb_nss-devel = %{version}-%{release}

%description -n %{libdbnssdev}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files and libraries for building nss
modules which use Berkeley DB.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n db-%{version}
#upstream patches
%patch0
%patch1
%patch6
%patch7

%patch2 -p1 -b .amd64-mutexes
%patch3 -p1 -b .pthreadsmutexes
%patch4 -p1 -b .db185
%patch5 -p1 -b .libtool-fixes
%patch8 -b .txn_nolog
%patch9
%patch10 -p1


# Remove tags files which we don't need.
find . -name tags | xargs rm -f
# Define a shell function for fixing HREF references in the docs, which
# would otherwise break when we split the docs up into subpackages.
fixup_href() {
    for doc in $@ ; do
        chmod u+w ${doc}
        sed -e 's,="../api_c/,="../../%{name}-devel-%{version}/api_c/,g' \
            -e 's,="api_c/,="../%{name}-devel-%{version}/api_c/,g' \
            -e 's,="../api_cxx/,="../../%{name}-devel-%{version}/api_cxx/,g' \
            -e 's,="api_cxx/,="../%{name}-devel-%{version}/api_cxx/,g' \
            -e 's,="../api_java/,="../../%{name}-devel-%{version}/api_java/,g' \
            -e 's,="api_java/,="../%{name}-devel-%{version}/api_java/,g' \
            -e 's,="../api_tcl/,="../../%{name}-devel-%{version}/api_tcl/,g' \
            -e 's,="api_tcl/,="../%{name}-devel-%{version}/api_tcl/,g' \
            -e 's,="../examples_c/,="../../%{name}-devel-%{version}/examples_c/,g' \
            -e 's,="examples_c/,="../%{name}-devel-%{version}/examples_c/,g' \
            -e 's,="../examples_cxx/,="../../%{name}-devel-%{version}/examples_cxx/,g' \
            -e 's,="examples_cxx/,="../%{name}-devel-%{version}/examples_cxx/,g' \
            -e 's,="../ref/,="../../%{name}-devel-%{version}/ref/,g' \
            -e 's,="ref/,="../%{name}-devel-%{version}/ref/,g' \
            -e 's,="../sleepycat/,="../../%{name}-devel-%{version}/sleepycat/,g' \
            -e 's,="sleepycat/,="../%{name}-devel-%{version}/sleepycat/,g' \
            -e 's,="../images/,="../../%{name}-%{version}/images/,g' \
            -e 's,="images/,="../%{name}-%{version}/images/,g' \
            -e 's,="../utility/,="../../%{name}-%{version}/utility/,g' \
            -e 's,="utility/,="../%{name}-%{version}/utility/,g' ${doc} > ${doc}.new
        touch -r ${doc} ${doc}.new
        cat ${doc}.new > ${doc}
        touch -r ${doc}.new ${doc}
        rm -f ${doc}.new
    done
}

set +x	# XXX painful to watch
# Fix all of the HTML files.
fixup_href `find . -name "*.html"`
set -x	# XXX painful to watch
 
chmod -R u+w dist
(cd dist && ./s_config)


%build
CFLAGS="%{optflags}"
%ifarch ppc
CFLAGS="$CFLAGS -D_GNU_SOURCE -D_REENTRANT"
%endif
export CFLAGS

pushd build_unix
    export CC=%{__cc}
    CONFIGURE_TOP="../dist" %configure2_5x \
        --enable-compat185 \
        --enable-dump185 \
        --enable-shared \
        --enable-static \
        --enable-rpc \
        --enable-tcl \
        --with-tcl=%{_libdir} \
        --enable-cxx \
        --enable-test  \
        --disable-pthreadsmutexes \
        # --enable-diagnostic \
        # --enable-debug \
        # --enable-debug_rop \
        # --enable-debug_wop \
        # --enable-posixmutexes

    %make
popd

mkdir build_nss
pushd build_nss
    CONFIGURE_TOP="../dist" %configure2_5x \
        --enable-shared \
        --disable-static \
        --disable-tcl \
        --disable-cxx \
        --disable-java \
        --disable-pthreadsmutexes \
        --with-uniquename \
        --enable-compat185 \
        --disable-cryptography \
        --disable-queue \
        --disable-replication \
        --disable-verify \
	#--disable-hash  \
	#--enable-smallbuild \
	# END

    %make libdb_base=libdb_nss libso_target=libdb_nss-%{__soversion}.la libdir=/%{_lib}
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make -C build_unix install_setup install_include install_lib install_utilities \
    DESTDIR=%{buildroot} \
    includedir=%{_includedir}/db4 \
    emode=755

make -C build_nss install_include install_lib libdb_base=libdb_nss \
    DESTDIR=%{buildroot} \
    includedir=%{_includedir}/db_nss \
    LIB_INSTALL_FILE_LIST=""

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}/%{_libdir}/libdb_nss-%{__soversion}.so %{buildroot}/%{_lib}
ln -s  /%{_lib}/libdb_nss-%{__soversion}.so %{buildroot}%{_libdir}

ln -sf db4/db.h %{buildroot}%{_includedir}/db.h

# symlink the short libdb???.a name
ln -sf %{_libdb_a} %{buildroot}%{_libdir}/libdb.a
ln -sf %{_libcxx_a} %{buildroot}%{_libdir}/libdb_cxx.a
ln -sf libdb_tcl-%{__soversion}.a %{buildroot}%{_libdir}/libdb_tcl.a
ln -sf %{_libdb_a} %{buildroot}%{_libdir}/libdb-4.a
ln -sf %{_libcxx_a} %{buildroot}%{_libdir}/libdb_cxx-4.a
ln -sf libdb_tcl-%{__soversion}.a %{buildroot}%{_libdir}/libdb_tcl-4.a


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libdbcxx} -p /sbin/ldconfig
%postun -n %{libdbcxx} -p /sbin/ldconfig

%post -n %{libdbtcl} -p /sbin/ldconfig
%postun -n %{libdbtcl} -p /sbin/ldconfig

%post -n %{libdbnss} -p /sbin/ldconfig
%postun -n %{libdbnss} -p /sbin/ldconfig


%files -n %{libname}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/libdb-%{__soversion}.so

%files -n %{libdbcxx}
%defattr(0755,root,root) 
%{_libdir}/libdb_cxx-%{__soversion}.so

%files -n %{libdbtcl}
%defattr(0755,root,root)
%{_libdir}/libdb_tcl-%{__soversion}.so

%files utils
%defattr(0755,root,root)
%{_bindir}/berkeley_db*_svc
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump
%{_bindir}/db*_dump185
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify

%files -n %{devname}
%defattr(0644,root,root,0755)
%dir %{_includedir}/db4
%{_includedir}/db4/db.h
%{_includedir}/db4/db_185.h
%{_includedir}/db4/db_cxx.h
%{_includedir}/db.h
%{_libdir}/libdb.so
%{_libdir}/libdb-4.so
%{_libdir}/libdb-%{__soversion}.la
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_cxx-4.so
%{_libdir}/libdb_cxx-%{__soversion}.la
%{_libdir}/libdb_tcl.so
%{_libdir}/libdb_tcl-4.so
%{_libdir}/libdb_tcl-%{__soversion}.la

%files -n %{staticdevname}
%defattr(0644,root,root,0755)
%{_libdir}/*.a

%files -n %{libdbnss}
%defattr(0755,root,root) 
/%{_lib}/libdb_nss-%{__soversion}.so

%files -n %{libdbnssdev}
%defattr(0644,root,root,0755)
%dir %{_includedir}/db_nss
%{_includedir}/db_nss/db.h
%{_includedir}/db_nss/db_185.h
%exclude %{_includedir}/db_nss/db_cxx.h
%{_libdir}/libdb_nss.so
%{_libdir}/libdb_nss-4.so
%{_libdir}/libdb_nss-%{__soversion}.la
%{_libdir}/libdb_nss-%{__soversion}.so

%files doc
%doc LICENSE README
%doc docs/utility
%doc docs/api_c docs/api_cxx docs/api_tcl docs/index.html
%doc docs/ref docs/sleepycat docs/images
%doc examples_c examples_cxx


%changelog
* Tue Jul 31 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.2.52
- P9: 4.2.52.5 patch
- P10: Howards cache memory leak fix
- updates URLs
- this one is too messy to apply the devel naming policy to
- implement library provides policy

* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.52
- rebuild against new tcl and adjust buildrequires

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.52
- 4.2.52
- build the nss modules
- BuildRequires: ed
- sync patches with Mandriva 4.2.52-10mdv2007.0
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.25
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.25
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.25-9avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.25-8avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.25-7avx
- bootstrap build
- remove java support entirely
- sync with mdk 4.1.25-8mdk:
  - P4: fix x86_64 mutexes from previous merge (gb)
  - P3: disable pthreads mutexes (bluca)
  - own %%_includedir/db4 (thauvin)
- get (silently) updated P2 from mdk srpm

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.1.25-6avx
- Annvix build
- require packages not files

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 4.1.25-5sls
- remove %%build_opensls macro
- remove %%prefix
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 4.1.25-4sls
- OpenSLS build
- tidy spec
- remove support for mdk < 9.0
- use %%build_opensls to disable java builds

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
