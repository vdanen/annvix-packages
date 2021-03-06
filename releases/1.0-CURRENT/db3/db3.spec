%define name	db3
%define version	3.3.11
%define release	19avx

%define	__soversion	3.3
%define	_libdb_a	libdb-%{__soversion}.a
%define	_libcxx_a	libdb_cxx-%{__soversion}.a

# Define to build Java bindings (default)
%define build_java	0

# Allow --with[out] JAVA rpm command line build
%{?_with_JAVA: %{expand: %%define build_java 1}}
%{?_without_JAVA: %{expand: %%define build_java 0}}

%define libdb		%mklibname db %{__soversion}
%define libdbdevel	%libdb-devel
%define libdbcxx	%mklibname dbcxx %{__soversion}
%define libdbjava	%mklibname dbjava %{__soversion}
%define libdbtcl	%mklibname dbtcl %{__soversion}

Summary:	The Berkeley DB database library for C.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://www.sleepycat.com
Source:		http://www.sleepycat.com/update/%{version}/db-%{version}.tar.bz2
Patch1:		db3.3-3.3.11.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	db1-devel, gcc-c++, glibc-static-devel, tcl
%if %{build_java}
BuildRequires:	gcc-java >= 3.1.1-0.8mdk
BuildRequires:	gcj-tools >= 3.1.1-0.8mdk
%endif

PreReq:		ldconfig

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n %libdb
Summary:	The Berkeley DB database library for C.
Group:		System/Libraries
PreReq:		ldconfig
Provides:	db3 = %{version}-%{release}

%description -n %libdb
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n %libdbcxx
Summary:	The Berkeley DB database library for C++.
Group:		System/Libraries
PreReq:		ldconfig
Provides:	db3 = %{version}-%{release}

%description -n %libdbcxx
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build C++ programs which use
Berkeley DB.

%if %{build_java}
%package -n %libdbjava
Summary:	The Berkeley DB database library for C++.
Group:		System/Libraries
PreReq:		ldconfig
Provides:	db3 = %{version}-%{release}

%description -n %libdbjava
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build Java programs which use
Berkeley DB.
%endif

%package -n %libdbtcl
Summary:	The Berkeley DB database library for TCL.
Group:		System/Libraries
PreReq:		ldconfig
Provides:	db3 = %{version}-%{release}

%description -n %libdbtcl
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the header files, libraries, and documentation for
building tcl programs which use Berkeley DB.

%package utils
Summary:	Command line tools for managing Berkeley DB databases.
Group:		Databases

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains command line tools for managing Berkeley DB databases.

%package -n %libdbdevel
Summary:	Development libraries/header files for the Berkeley DB library.
Group:		Development/Databases
Requires:	%libdb = %{version}-%{release}, %libdbtcl = %{version}-%{release}
Provides:	db3-devel = %{version}-%{release} libdb-devel = %{version}-%{release}
Conflicts:	libdb4.0-devel

%description -n %libdbdevel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%prep
%setup -q -n db-%{version}
%patch1 -p0

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
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS
%ifarch ppc
CFLAGS="-D_GNU_SOURCE -D_REENTRANT $RPM_OPT_FLAGS"; export CFLAGS
%endif

%if %{build_java}
# Use javac trampoline from gcj
mkdir -p build_unix/gcj
pushd build_unix/gcj;
cat > javac << EOF
#!/bin/sh
exec /usr/bin/gcj-javac-`gcj -dumpversion` "\$@"
EOF
chmod +x javac
export JAVAC=$PWD/javac
export JAVACABS=$JAVAC
# Kludge lookup of <jni.h> and make configure grab the right one from gcj
ln -s `gcj -print-file-name=include`/libgcj include
popd
%endif

# XXX --enable-posixmutexes is useful for threads but useless for interprocess locking.
# XXX --enable-diagnostic should be disabled for production (but is useful).
# XXX --enable-debug_{r,w}op should be disabled for production.
# XXX --enable-java

%if %{build_java}
ENABLE_JAVA="--enable-java"
%endif

pushd build_unix
CONFIGURE_TOP="../dist" %configure \
	--enable-compat185 --enable-dump185 \
	--enable-shared --enable-static --enable-rpc \
	--enable-tcl --with-tcl=%{_libdir} \
	--enable-cxx $ENABLE_JAVA --enable-test \
	# --enable-diagnostic \
	# --enable-debug --enable-debug_rop --enable-debug_wop \
	# --enable-posixmutexes

make libdb=%{_libdb_a} %{_libdb_a}
make libcxx=%{_libcxx_a} %{_libcxx_a}

# Static link with old db-185 libraries.
/bin/sh ./libtool --mode=compile cc -c -O2 -g -g -I/usr/include/db1 -I../dist/../include -D_REENTRANT  ../dist/../db_dump185/db_dump185.c
cc -s -static -o db_dump185 db_dump185.lo -L%{_libdir} -ldb1

# Compile rest normally.
make libdb=%{_libdb_a} libcxx=%{_libcxx_a} TCFLAGS='-I$(builddir)'
popd

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
%makeinstall -C build_unix libdb=%{_libdb_a} libcxx=%{_libcxx_a}
chmod +x $RPM_BUILD_ROOT/%{_libdir}/*.so*

# XXX annoying
set -x
cd $RPM_BUILD_ROOT

%ifos linux
  mkdir -p ./%{_lib}
  mv .%{_libdir}/libdb[-.]*so* ./%{_lib}
%endif

  mkdir -p .%{_includedir}/db3
  mv .%{_prefix}/include/*.h .%{_includedir}/db3
  ln -sf db3/db.h .%{_includedir}/db.h
# XXX Rather than hack *.la (see below), create /usr/lib/libdb-3.1.so symlink.
  ln -sf ../../%{_lib}/libdb-%{__soversion}.so .%{_libdir}/libdb-%{__soversion}.so
# XXX This is needed for packaging db3 for Red Hat 6.x
#  for F in .%{_prefix}/bin/db_* ; do
#    mv $F `echo $F | sed -e 's,/db_,/db3_,'`
#  done
cd -
set +x

# XXX libdb-3.1.so is in /lib teach libtool as well
#perl -pi -e 's,/usr,,' $RPM_BUILD_ROOT%{_libdir}/libdb-%{__soversion}.la

# Move db.jar file to the correct place, and version it
%if %{build_java}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/java
mv $RPM_BUILD_ROOT%{_libdir}/db.jar $RPM_BUILD_ROOT%{_datadir}/java/db-%{__soversion}.jar
%endif

# Remove unpackaged files
rm -rf	$RPM_BUILD_ROOT/usr/docs \
	$RPM_BUILD_ROOT/%{_libdir}/libdb_java-3.3.a \
	$RPM_BUILD_ROOT/%{_libdir}/libdb_java-3.3.la \
	$RPM_BUILD_ROOT/%{_libdir}/libdb_tcl-3.3.a

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %libdb -p /sbin/ldconfig
%postun -n %libdb -p /sbin/ldconfig

%post -n %libdbcxx -p /sbin/ldconfig
%postun -n %libdbcxx -p /sbin/ldconfig

%if %{build_java}
%post -n %libdbjava -p /sbin/ldconfig
%postun -n %libdbjava -p /sbin/ldconfig
%endif

%post -n %libdbtcl -p /sbin/ldconfig
%postun -n %libdbtcl -p /sbin/ldconfig

%files -n %libdb
%defattr(-,root,root)
%doc LICENSE README
/%{_lib}/libdb-%{__soversion}.so

%files -n %libdbcxx
%defattr(-,root,root) 
%{_libdir}/libdb_cxx-%{__soversion}.so

%if %{build_java}
%files -n %libdbjava
%defattr(-,root,root) 
%doc docs/api_java
%{_libdir}/libdb_java-%{__soversion}.so
%{_datadir}/java/db-%{__soversion}.jar
%endif

%files -n %libdbtcl
%defattr(-,root,root)
%{_libdir}/libdb_tcl-%{__soversion}.la
%{_libdir}/libdb_tcl-%{__soversion}.so

%files utils
%defattr(-,root,root)
%doc	docs/utility
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

%files -n %libdbdevel
%defattr(-,root,root)
%doc	docs/api_c docs/api_cxx docs/api_java docs/api_tcl docs/index.html
%doc	docs/ref docs/sleepycat docs/images
%doc	examples_c examples_cxx
%{_libdir}/libdb-%{__soversion}.la
%{_libdir}/libdb_cxx-%{__soversion}.la
%{_libdir}/%{_libdb_a}
%{_libdir}/%{_libcxx_a}
%{_includedir}/db3/db.h
%{_includedir}/db3/db_185.h
%{_includedir}/db3/db_cxx.h
%{_includedir}/db3/cxx_common.h
%{_includedir}/db3/cxx_except.h
%{_includedir}/db.h
%ifos linux
/%{_lib}/libdb.so
/%{_lib}/libdb-3.so
/%{_libdir}/libdb-%{__soversion}.so
%else
%{_libdir}/libdb.so
%endif
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_cxx-3.so
%{_libdir}/libdb_tcl.so
%{_libdir}/libdb_tcl-3.so

%changelog
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 3.3.11-19avx
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

* Sat Jul 05 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 3.3.11-15mdk
- use %%mklibname
- libdb3-devel conflict libdb4-devel

* Fri Jun 06 2003 Per ?yvind Karlsen <peroyvind@sintrax.net> 3.3.11-14mdk
- rebuild against tcl 8.4

* Sun Jan 19 2003 Stefan van der Eijk <stefan@eijk.nu> 3.3.11-13mdk
- remove unpackaged files

* Sat Oct 26 2002 Stew Benedict <sbenedict@mandrakesoft.com> 3.3.11-12mdk
- add -D_GNU_SOURCE -D_REENTRANT to CFLAGS for PPC - fix crazy 2GB .db files

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.11-11mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Tue Aug 06 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.3.11-10mdk
- glibc-static-devel BuildRequires for Mandrake 9.

* Fri Jul 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.11-9mdk
- Rebuild with gcc3.2
- Conditionalize build of Java bindings --with[out] JAVA

* Wed Jun 19 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.11-8mdk
- Sanitize specfile (use %%configure, %%makeinstall, etc.)
- Enable Java bindings, disable debug
- Rpmlint fixes: strange-permission, hardcoded-library-path

* Tue Feb 19 2002 Christian Belisle <cbelisle@mandrakesoft.com> 3.3.11-7mdk
- Move docs images to devel package.
- Make a new libdbcxx package.

* Sat Feb 16 2002 Stefan van der Eijk <stefan@eijk.nu> 3.3.11-6mdk
- Remove duplicate Buildprereq
- BuildRequires

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
