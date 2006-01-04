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
%define version		4.1.25
%define release		%_revrel

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

Summary:	The Berkeley DB database library for C
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://www.sleepycat.com
Source:		http://www.sleepycat.com/update/%{version}/db-%{version}.tar.bz2
#http://www.sleepycat.com/update/4.1.25/patch.4.1.25.html
Patch1:		http://www.sleepycat.com/update/4.1.25/patch.4.1.25.1
# Add fast AMD64 mutexes
Patch2:		db-4.1.25-mdk-amd64-mutexes.patch
# NPTL pthreads mutexes are evil
Patch3:		db-4.2.52-mdk-disable-pthreadsmutexes.patch
Patch4:		db-4.2.52-mdk-db185.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	tcl, db1-devel, glibc-static-devel	

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


%package -n %{libnamedev}
Summary:	Development libraries/header files for the Berkeley DB library
Group:		Development/Databases
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libdbtcl} = %{version}-%{release}
Requires:	%{libdbcxx} = %{version}-%{release}
Provides:	db-devel = %{version}-%{release}
Provides:	db4-devel = %{version}-%{release}
Provides:	libdb-devel = %{version}-%{release}
Conflicts:	%{libname_orig}3.3-devel, %{libname_orig}4.0-devel

%description -n %{libnamedev}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.


%package -n %{libnamestatic}
Summary:	Development static libraries files for the Berkeley DB library
Group:		Development/Databases
Requires:	db4-devel = %{version}-%{release}
Provides:	db-static-devel = %{version}-%{release}
Provides:	db4-static-devel = %{version}-%{release}
Provides:	libdb-static-devel = %{version}-%{release}
Conflicts:	%{libname_orig}3.3-static-devel, %{libname_orig}4.0-static-devel

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
%patch3 -p1 -b .pthreadsmutexes
%patch4 -p1 -b .db185

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

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make -C build_unix install_setup install_include install_lib install_utilities \
    includedir=%{buildroot}%{_includedir}/db4 \
    libdir=%{buildroot}%{_libdir} \
    bindir=%{buildroot}%{_bindir} \
    emode=755

ln -sf db4/db.h %{buildroot}%{_includedir}/db.h

# we don't ship db4.2 (yet)
## XXX This is needed for parallel install with db4.2
#for F in %{buildroot}%{_bindir}/*db_* ; do
#   mv $F `echo $F | sed -e 's,db_,db41_,'`
#done


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libdbcxx} -p /sbin/ldconfig
%postun -n %{libdbcxx} -p /sbin/ldconfig

%post -n %{libdbtcl} -p /sbin/ldconfig
%postun -n %{libdbtcl} -p /sbin/ldconfig


%files -n %{libname}
%defattr(0644,root,root,0755)
%doc LICENSE README
%attr(0755,root,root) %{_libdir}/libdb-%{__soversion}.so

%files -n %{libdbcxx}
%defattr(0755,root,root) 
%{_libdir}/libdb_cxx-%{__soversion}.so

%files -n %{libdbtcl}
%defattr(0755,root,root)
%{_libdir}/libdb_tcl-%{__soversion}.so

%files utils
%defattr(0644,root,root,0755)
%doc docs/utility/*
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

%files -n %{libnamedev}
%defattr(0644,root,root,0755)
%doc docs/api_c docs/api_cxx docs/api_tcl docs/index.html
%doc docs/ref docs/sleepycat docs/images
%doc examples_c examples_cxx
%dir %{_includedir}/db4
%{_includedir}/db4/db.h
%{_includedir}/db4/db_185.h
%{_includedir}/db4/db_cxx.h
%{_includedir}/db4/cxx_common.h
%{_includedir}/db4/cxx_except.h
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

%files -n %{libnamestatic}
%defattr(0644,root,root,0755)
%{_libdir}/*.a

%changelog
* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org>
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
