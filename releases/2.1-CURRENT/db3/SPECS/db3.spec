#
# spec file for package db3
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		db3
%define version		3.3.11
%define release		%_revrel

%define	__soversion	3.3
%define	_libdb_a	libdb-%{__soversion}.a
%define	_libcxx_a	libdb_cxx-%{__soversion}.a

%define libdb		%mklibname db %{__soversion}
%define libdbdevel	%{libdb}-devel
%define libdbcxx	%mklibname dbcxx %{__soversion}
%define libdbtcl	%mklibname dbtcl %{__soversion}
%define liborig		%mklibname db

Summary:	The Berkeley DB database library for C
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://www.sleepycat.com
Source:		http://www.sleepycat.com/update/%{version}/db-%{version}.tar.bz2
Patch1:		db3.3-3.3.11.patch
Patch2:		db3.3-compile-with-bash31.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	db1-devel
BuildRequires:	glibc-static-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel

Requires(post):	ldconfig
Requires(postun): ldconfig

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.


%package -n %{libdb}
Summary:	The Berkeley DB database library for C
Group:		System/Libraries
Requires(post):	ldconfig
Requires(postun): ldconfig

%description -n %{libdb}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.


%package -n %{libdbcxx}
Summary:	The Berkeley DB database library for C++
Group:		System/Libraries
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


%package -n %{libdbdevel}
Summary:	Development libraries/header files for the Berkeley DB library
Group:		Development/Databases
Requires:	%{libdb} = %{version}-%{release}
Requires:	%{libdbtcl} = %{version}-%{release}
Provides:	db3-devel = %{version}-%{release}
Provides:	libdb3.3-devel = %{version}-%{release}
Conflicts:	%{liborig}4.0-devel
Conflicts:	%{liborig}4.1-devel
Conflicts:	%{liborig}4.2-devel
Conflicts:	%{liborig}4.3-devel
Conflicts:	%{liborig}4.4-devel

%description -n %{libdbdevel}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n db-%{version}
%patch1 -p0 -b .org
%patch2 -p0 -b .bash

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


%build
CFLAGS="%{optflags}"; export CFLAGS
%ifarch ppc
CFLAGS="-D_GNU_SOURCE -D_REENTRANT %{optflags}"; export CFLAGS
%endif

# XXX --enable-posixmutexes is useful for threads but useless for interprocess locking.
# XXX --enable-diagnostic should be disabled for production (but is useful).
# XXX --enable-debug_{r,w}op should be disabled for production.

pushd build_unix
    CONFIGURE_TOP="../dist" %configure \
        --enable-compat185 \
        --enable-dump185 \
        --enable-shared \
        --enable-static \
        --enable-rpc \
        --enable-tcl \
        --with-tcl=%{_libdir} \
        --enable-cxx \
        --enable-test \
        # --enable-diagnostic \
        # --enable-debug --enable-debug_rop --enable-debug_wop \
        # --enable-posixmutexes

    make libdb=%{_libdb_a} %{_libdb_a}
    make libcxx=%{_libcxx_a} %{_libcxx_a}

    # Static link with old db-185 libraries.
    /bin/sh ./libtool --mode=compile cc -c -O2 -g -g -I/usr/include/db1 -I../dist/../include -D_REENTRANT  ../dist/../db_dump185/db_dump185.c
    cc -s -static -o db_dump185 db_dump185.o -L%{_libdir} -ldb1

    # Compile rest normally.
    make libdb=%{_libdb_a} libcxx=%{_libcxx_a} TCFLAGS='-I$(builddir)'
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_includedir},%{_libdir}}

%makeinstall -C build_unix libdb=%{_libdb_a} libcxx=%{_libcxx_a}

pushd %{buildroot}
#    mkdir -p ./%{_lib}
#    mv .%{_libdir}/libdb-%{__soversion}.so ./%{_lib}
#    # XXX Rather than hack *.la (see below), create /usr/lib/libdb-3.1.so symlink.
#    ln -sf ../../%{_lib}/libdb-%{__soversion}.so .%{_libdir}/libdb-%{__soversion}.so

    mkdir -p .%{_includedir}/db3
    mv .%{_prefix}/include/*.h .%{_includedir}/db3
    ln -sf db3/db.h .%{_includedir}/db.h
    # XXX This is needed for a parallel install with db4-utils
    #for F in .%{_prefix}/bin/db_* ; do
    #    mv $F `echo $F | sed -e 's,/db_,/db3_,'`
    #done
popd

# XXX libdb-3.1.so is in /lib teach libtool as well
#perl -pi -e 's,/usr,,' %{buildroot}%{_libdir}/libdb-%{__soversion}.la

# Remove unpackaged files
rm -rf	%{buildroot}/usr/docs \
    %{buildroot}%{_libdir}/libdb_tcl-3.so	\
    %{buildroot}%{_libdir}/libdb_cxx-3.so	\
    %{buildroot}%{_libdir}/libdb-3.so \
    %{buildroot}/%{_lib}/libdb-${__soversion}.so


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libdb} -p /sbin/ldconfig
%postun -n %{libdb} -p /sbin/ldconfig

%post -n %{libdbcxx} -p /sbin/ldconfig
%postun -n %{libdbcxx} -p /sbin/ldconfig

%post -n %{libdbtcl} -p /sbin/ldconfig
%postun -n %{libdbtcl} -p /sbin/ldconfig


%files -n %{libdb}
%defattr(0644,root,root)
#/%{_lib}/libdb-%{__soversion}.so
%attr(0755,root,root) %{_libdir}/libdb-%{__soversion}.so

%files -n %{libdbcxx}
%defattr(0755,root,root) 
%{_libdir}/libdb_cxx-%{__soversion}.so

%files -n %{libdbtcl}
%defattr(0755,root,root)
%{_libdir}/libdb_tcl-%{__soversion}.so

%files utils
%defattr(0755,root,root)
%{_bindir}/berkeley_db_svc
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

%files -n %{libdbdevel}
%defattr(0644,root,root,0755)
%{_includedir}/*
%{_libdir}/libdb.so
%{_libdir}/libdb-%{__soversion}.la
%{_libdir}/%{_libdb_a}
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_cxx-%{__soversion}.la
%{_libdir}/%{_libcxx_a}
%{_libdir}/libdb_tcl.so
%{_libdir}/libdb_tcl-%{__soversion}.a
%{_libdir}/libdb_tcl-%{__soversion}.la

%files doc
%doc LICENSE README
%doc docs/utility
%doc docs/api_c docs/api_cxx docs/api_tcl docs/index.html
%doc docs/ref docs/sleepycat docs/images
%doc examples_c examples_cxx


%changelog
* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.3.11
- rebuild against new tcl and adjust buildrequires

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.3.11
- provide libdb3.3-devel even on biarches
- devel conflicts for all libdb4.x-devel packages
- force permissions on pacakged files
- don't install libdb*.so into /lib (that should only be done for the
  preferred/main dbX package, and for us that's db4)
- P1: fix compilation when using newer bash (from Mandriva)
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.3.11
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.3.11
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.3.11-22avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.3.11-21avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.3.11-20avx
- bootstrap build
- drop buildreq on gcc-c++
- sync with cooker 3.3.11-19mdk:
  - fix build of db_dump185 with current libtool (cjw)
  - only C binding provides db3 (deaddog)
  - include static lib and .la files for other bindings (deaddog)
  - critical stuff moved over to db4, so don't place db3 library under
    /lib (deaddog)
- completely remove java stuff
- spec cleanups

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.3.11-19avx
- Annvix build
- require packages not files

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 3.3.11-18sls
- remove %%build_opensls macro
- minor spec cleanups
- remove %%prefix
- include libdb-3.so and libdb_{cxx,tcl}-3.so symlinks

* Sat Jan 04 2004 Vincent Danen <vdanen@opensls.org> 3.3.11-17sls
- OpenSLS build
- tidy spec
- use %%build_opensls to prevent building java stuff
- remove %%build_mdk90 conditional macro

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
