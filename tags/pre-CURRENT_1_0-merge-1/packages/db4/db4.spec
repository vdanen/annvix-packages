# compatibility with legacy rpm
%{!?_lib:%define _lib	lib}

%define	__soversion	4.1
%define	_libdb_a	libdb-%{__soversion}.a
%define	_libcxx_a	libdb_cxx-%{__soversion}.a

%define libname_orig	%mklibname db
%define libname		%{libname_orig}%{__soversion}
%define libnamedev	%{libname}-devel
%define libnamestatic	%{libname}-static-devel

%define libdbcxx	%{libname_orig}cxx%{__soversion}
%define libdbtcl	%{libname_orig}tcl%{__soversion}
%define libdbjava	%{libname_orig}java%{__soversion}

# Define Mandrake Linux version we are building for
%define mdkversion	%(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandrake-release)

# Define to build Java bindings (default)
%define build_java	1

# Allow --with[out] JAVA rpm command line buil
%{?_with_JAVA: %{expand: %%define build_java 1}}
%{?_without_JAVA: %{expand: %%define build_java 0}}

# Don't build Java bindings for any MDK release < 9.0
%if %{mdkversion} < 900
%define build_java	0
%endif

Summary: The Berkeley DB database library for C.
Name: db4
Version: 4.1.25
Release: 3mdk
Source: http://www.sleepycat.com/update/%{version}/db-%{version}.tar.bz2
URL: http://www.sleepycat.com
License: BSD
Group: System/Libraries
PreReq: /sbin/ldconfig
BuildRequires: tcl, db1-devel
%if %{mdkversion} >= 900
BuildRequires: glibc-static-devel	
%endif
%if %{build_java}
BuildRequires: gcc-java >= 3.1.1-0.8mdk
%endif

# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=70362
#Patch0: db-4.0.14-recover.patch.bz2

#http://www.sleepycat.com/update/4.1.25/patch.4.1.25.html
Patch1: http://www.sleepycat.com/update/4.1.25/patch.4.1.25.1

# Add fast AMD64 mutexes
Patch2: db-4.1.25-amd64-mutexes.patch.bz2

BuildRoot: %{_tmppath}/%{name}-root
Prefix: %{_prefix}

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n %{libname}
Summary: The Berkeley DB database library for C.
Group: System/Libraries
PreReq: /sbin/ldconfig

%description -n %{libname}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n %{libdbcxx}
Summary: The Berkeley DB database library for C++.
Group: System/Libraries
PreReq: /sbin/ldconfig
Provides: libdbcxx = %{version}-%{release}

%description -n %{libdbcxx}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build C++ programs which use
Berkeley DB.

%package -n %{libdbjava}
Summary: The Berkeley DB database library for C++.
Group: System/Libraries
PreReq: /sbin/ldconfig
Provides: libdbjava = %{version}-%{release}

%description -n %{libdbjava}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build Java programs which use
Berkeley DB.

%package -n %{libdbtcl}
Summary: The Berkeley DB database library for TCL.
Group: System/Libraries
PreReq: /sbin/ldconfig
Provides: libdbtcl = %{version}-%{release}

%description -n %{libdbtcl}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the header files, libraries, and documentation for
building tcl programs which use Berkeley DB.

%package utils
Summary: Command line tools for managing Berkeley DB databases.
Group: Databases
Prefix: %{_prefix}

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains command line tools for managing Berkeley DB databases.

%package -n %{libnamedev}
Summary: Development libraries/header files for the Berkeley DB library.
Group: Development/Databases
Prefix: %{_prefix}
Requires: %{libname} = %{version}-%{release}
Requires: %{libdbtcl} = %{version}-%{release}
Requires: %{libdbcxx} = %{version}-%{release}
Provides: db-devel = %{version}-%{release}
Provides: db4-devel = %{version}-%{release}
Provides: libdb-devel = %{version}-%{release}
Conflicts: %{libname_orig}3.3-devel, %{libname_orig}4.0-devel

%description -n %{libnamedev}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%package -n %{libnamestatic}
Summary: Development static libraries files for the Berkeley DB library.
Group: Development/Databases
Prefix: %{_prefix}
Requires: db4-devel = %{version}-%{release}
Provides: db-static-devel = %{version}-%{release}
Provides: db4-static-devel = %{version}-%{release}
Provides: libdb-static-devel = %{version}-%{release}
Conflicts: %{libname_orig}3.3-static-devel, %{libname_orig}4.0-static-devel

%description -n %{libnamestatic}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the static libraries for building programs which
use Berkeley DB.


%prep
%setup -q -n db-%{version}
#%patch0 -p1 -b .recover
%patch1
%patch2 -p1 -b .amd64-mutexes

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
CFLAGS="$RPM_OPT_FLAGS"
%ifarch ppc
CFLAGS="$CFLAGS -D_GNU_SOURCE -D_REENTRANT"
%endif
export CFLAGS

%if %{build_java}
# Use javac trampoline from gcj
mkdir -p build_unix/gcj
pushd build_unix/gcj;
cat > javac << EOF
#!/bin/sh
exec /usr/bin/gcj-javac-`gcj -dumpversion` "\$@"
EOF
chmod +x javac
export PATH=$PWD:$PATH
# Kludge lookup of <jni.h> and make configure grab the right one from gcj
ln -s `gcj -print-file-name=include`/libgcj include
popd
%endif

%if %{build_java}
ENABLE_JAVA="--enable-java"
%endif

pushd build_unix
CONFIGURE_TOP="../dist" %configure2_5x \
	--enable-compat185 --enable-dump185 \
	--enable-shared --enable-static --enable-rpc \
	--enable-tcl --with-tcl=%{_libdir} \
	--enable-cxx $ENABLE_JAVA --enable-test  \
	# --enable-diagnostic \
	# --enable-debug --enable-debug_rop --enable-debug_wop \
	# --enable-posixmutexes

%make libdb=%{_libdb_a} %{_libdb_a}
%make libcxx=%{_libcxx_a} %{_libcxx_a}

# Static link with old db-185 libraries.
/bin/sh ./libtool --mode=compile cc -c -O2 -g -g -I/usr/include/db1 -I../dist/../include -D_REENTRANT  ../dist/../db_dump185/db_dump185.c
cc -s -static -o db_dump185 db_dump185.lo -L%{_libdir} -ldb1

# Compile rest normally.
%make libdb=%{_libdb_a} libcxx=%{_libcxx_a} TCFLAGS='-I$(builddir)'
popd

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
%makeinstall -C build_unix libdb=%{_libdb_a} libcxx=%{_libcxx_a}
chmod +x %{buildroot}/%{_libdir}/*.so*

# XXX annoying
set -x
cd %{buildroot}

# XXX This was the /lib handling code for db3. Keep it in case db4
# will be installed in /lib
#  mkdir -p ./%{_lib}
#  mv .%{_libdir}/libdb[-.]*so* ./%{_lib}

mkdir -p .%{_includedir}/db4
mv .%{_prefix}/include/*.h .%{_includedir}/db4
ln -sf db4/db.h .%{_includedir}/db.h
# XXX This was the /lib handling code for db3. Keep it in case db4
# will be installed in /lib
# XXX Rather than hack *.la (see below), create /usr/lib/libdb-4.0.so symlink.
#  ln -sf ../../%{_lib}/libdb-%{__soversion}.so .%{_libdir}/libdb-%{__soversion}.so
# XXX This is needed for packaging db4 for Red Hat 6.x
#  for F in .%{_prefix}/bin/db_* ; do
#    mv $F `echo $F | sed -e 's,/db_,/db4_,'`
#  done
cd -
set +x

# XXX libdb-3.1.so is in /lib teach libtool as well
#perl -pi -e 's,/usr,,' %{buildroot}%{_libdir}/libdb-%{__soversion}.la

# Move db.jar file to the correct place, and version it
%if %{build_java}
mkdir -p %{buildroot}%{_datadir}/java
mv %{buildroot}%{_libdir}/db.jar %{buildroot}%{_datadir}/java/db-%{__soversion}.jar
%endif

# remove this because of new rpm build install check policy
rm -rf %{buildroot}/usr/docs
#rm -f  %{buildroot}/%{_libdir}/libdb_java-%{__soversion}.la

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libdbcxx} -p /sbin/ldconfig
%postun -n %{libdbcxx} -p /sbin/ldconfig

%if %{build_java}
%post -n %{libdbjava} -p /sbin/ldconfig
%postun -n %{libdbjava} -p /sbin/ldconfig
%endif
 
%post -n %{libdbtcl} -p /sbin/ldconfig
%postun -n %{libdbtcl} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/libdb-%{__soversion}.so

%files -n %{libdbcxx}
%defattr(-,root,root) 
%{_libdir}/libdb_cxx-%{__soversion}.so

%if %{build_java}
%files -n %{libdbjava}
%defattr(-,root,root) 
%doc docs/api_java
%{_libdir}/libdb_java-%{__soversion}.so
%{_libdir}/libdb_java-%{__soversion}.la
%{_datadir}/java/db-%{__soversion}.jar
%endif

%files -n %{libdbtcl}
%defattr(-,root,root)
%{_libdir}/libdb_tcl-%{__soversion}.la
%{_libdir}/libdb_tcl-%{__soversion}.so

%files utils
%defattr(-,root,root)
%doc docs/utility
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

%files -n %{libnamedev}
%defattr(-,root,root)
%doc docs/api_c docs/api_cxx docs/api_java docs/api_tcl docs/index.html
%doc docs/ref docs/sleepycat docs/images
%doc examples_c examples_cxx
%{_libdir}/libdb-%{__soversion}.la
%{_libdir}/libdb_cxx-%{__soversion}.la
%{_libdir}/%{_libdb_a}
%{_libdir}/%{_libcxx_a}
%{_includedir}/db4/db.h
%{_includedir}/db4/db_185.h
%{_includedir}/db4/db_cxx.h
%{_includedir}/db4/cxx_common.h
%{_includedir}/db4/cxx_except.h
%{_includedir}/db.h
%{_libdir}/libdb_cxx-4.so
%{_libdir}/libdb-4.so
%{_libdir}/libdb.so
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_tcl.so

%files -n %{libnamestatic}
%defattr(-,root,root)
%{_libdir}/*.a

%changelog
* Fri Aug 22 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1.25-3mdk
- Add some provides & conflicts to ease installations

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1.25-2mdk
- Patch2: Add fast mutexes for AMD64
- %%configure2_5x, fix mklibnamification

* Thu Jun 26 2003 Stefan van der Eijk <stefan@eijk.nu> 4.1.25-1mdk
- Buchan's package
  * Sun May 18 2003 Buchan Milne <bgmilne@linux-mandrake.com> 4.1.25-1mdk
  - 4.1.25 (see if we can get openldap-2.1 to build with bdb support)
  - Remove db_recover patch(0), add official patch(1)
  - Maybe someone needs libdb_java-4.1.la, and if no-one does, at least
   use the macro so it doesn't have to be changed every time ...

* Wed Feb 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.14-6mdk
- Only package libdbcxx*.so.* into dedicated package
- Remove extra Provides: db4, since they are bindings in different languages

* Wed Feb 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.14-5mdk
- Patch0: SleepyCat patch for db_recover
- When moving a package from contribs to main, especially if it now
  the default, maintainer is expected to check that contributor hasn't
  nuked away changes that were made to initial package!
  - Add -D_GNU_SOURCE -D_REENTRANT to CFLAGS for PPC - fix crazy 2GB .db files
  - Conditionalize build of Java bindings --with[out] JAVA
  - Sanitize specfile (use %%configure, %%makeinstall, etc.)
  - Enable Java bindings, disable debug
  - Rpmlint fixes: strange-permission, hardcoded-library-path
  - Move docs images to devel package.
  - Make a new libdbcxx package.
  - Remove duplicate BuildPrereq, fix BuildRequires
  - Add missing files

* Mon Feb 17 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.14-4mdk
- use %%mklibname and other rpmlint stuff

* Mon Feb 17 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.14-3mdk
- remove libdb-4.0.so from -devel package
- fix BuildRequires

* Wed Jan 01 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0.14-2mdk
- add missing files
- remove unwanted but elswhere installed doc files
- add a static-devel sub package
- misc spec file fixes

* Tue Apr 02 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.14-1mdk
- 4.0.14.
- Don't install libdb-4.0.so in /lib.
- Spec cleanup.

* Thu Oct 25 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.3.11-5mdk
- Add missing files.

* Thu Oct 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.3.11-4mdk
- Add a description to the main package.
- Applied db 3.3.11.1 patch.

* Thu Oct 11 2001 Frederic Lepied <flepied@mandrakesoft.com> 3.3.11-3mdk
- don't obsolete libdb3.2

* Thu Oct 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.3.11-2mdk
- rebuild.

* Wed Oct 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.3.11-1mdk
- 3.3.11.

* Fri Oct 05 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.2.9-3mdk
- Change License for BSD (thanks to Geoffrey).
- devel package provide libdb-devel.

* Tue Sep 04 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.2.9-2mdk
- rebuild.
- s/Copyright/License.

* Tue Jul  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 3.2.9-1mdk
- 3.2.9

* Mon Mar 12 2001 Frederic Lepied <flepied@mandrakesoft.com> 3.1.17-1mdk
- 3.1.17

* Thu Dec  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.1.14-2mdk
- new lib policy.

* Mon Oct 16 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.1.14-1mdk
- first mandrake version.

* Wed Aug 30 2000 Matt Wilson <msw@redhat.com>
- rebuild to cope with glibc locale binary incompatibility, again

* Wed Aug 23 2000 Jeff Johnson <jbj@redhat.com>
- remove redundant strip of libnss_db* that is nuking symbols.
- change location in /usr/lib/libdb-3.1.la to point to /lib (#16776).

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.
- all of libdb_tcl* (including symlinks) in db3-utils, should be db3->tcl?

* Wed Aug 16 2000 Jakub Jelinek <jakub@redhat.com>
- temporarily build nss_db in this package, should be moved
  into separate nss_db package soon

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 11 2000 Jeff Johnson <jbj@redhat.com>
- upgrade to 3.1.14.
- create db3-utils sub-package to hide tcl dependency, enable tcl Yet Again.
- FHS packaging.

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- disable tcl Yet Again, base packages cannot depend on libtcl.so.

* Sat Jun  3 2000 Jeff Johnson <jbj@redhat.com>
- enable tcl, rebuild against tcltk 8.3.1 (w/o pthreads).

* Tue May 30 2000 Matt Wilson <msw@redhat.com>
- include /lib/libdb.so in the devel package

* Wed May 10 2000 Jeff Johnson <jbj@redhat.com>
- put in "System Environment/Libraries" per msw instructions.

* Tue May  9 2000 Jeff Johnson <jbj@redhat.com>
- install shared library in /lib, not /usr/lib.
- move API docs to db3-devel.

* Mon May  8 2000 Jeff Johnson <jbj@redhat.com>
- don't rename db_* to db3_*.

* Tue May  2 2000 Jeff Johnson <jbj@redhat.com>
- disable --enable-test --enable-debug_rop --enable-debug_wop.
- disable --enable-posixmutexes --enable-tcl as well, to avoid glibc-2.1.3
  problems.

* Mon Apr 24 2000 Jeff Johnson <jbj@redhat.com>
- add 3.0.55.1 alignment patch.
- add --enable-posixmutexes (linux threads has not pthread_*attr_setpshared).
- add --enable-tcl (needed -lpthreads).

* Sat Apr  1 2000 Jeff Johnson <jbj@redhat.com>
- add --enable-debug_{r,w}op for now.
- add variable to set shm perms.

* Sat Mar 25 2000 Jeff Johnson <jbj@redhat.com>
- update to 3.0.55

* Tue Dec 29 1998 Jeff Johnson <jbj@redhat.com>
- Add --enable-cxx to configure.

* Thu Jun 18 1998 Jeff Johnson <jbj@redhat.com>
- Create.
