%define name 	db2
%define version 2.4.14
%define release 10sls

Summary:	The BSD database library for C (version 2).
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://www.sleepycat.com
#Source:	http://www.sleepycat.com/update/2.7.7/db-2.7.7.tar.gz
# Taken from glibc 2.1.3
Source:		%{name}-glibc-2.1.3.tar.bz2
# Patch to make it standalone
Patch0:		db2-glibc-2.1.3.patch.bz2
Patch1:		db2-2.4.14-db2.patch.bz2
Patch2:		db2-2.4.14-db_fileid-64bit-fix.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root

PreReq:		/sbin/ldconfig
%ifnarch ia64
Conflicts:	glibc < 2.1.90
%endif

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This library used to be part of the glibc package.

%package devel
Summary:	Development libs/header files for Berkeley DB (version 2) library.
Group:		Development/C
Requires:	%{name} = %{version}
%ifnarch ia64
Conflicts:	glibc-devel < 2.1.90
%endif

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B tree, Hashing, Fixed and Variable-length
record access methods.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%prep
%setup -q -n db2
%patch0 -p1
%patch1 -p1 -b .db2
%patch2 -p1 -b .db_fileid-64bit-fix

%build
CFLAGS="$RPM_OPT_FLAGS" %make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/db2
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}

# XXX this causes all symbols to be deleted from the shared library
#strip -R .comment libdb2.so.3
install -m644 libdb2.a			$RPM_BUILD_ROOT/%{_libdir}/libdb2.a
install -m755 libdb2.so.3		$RPM_BUILD_ROOT/%{_libdir}/libdb2.so.3
ln -sf libdb2.so.3 			$RPM_BUILD_ROOT/%{_libdir}/libdb2.so
ln -sf libdb2.a				$RPM_BUILD_ROOT/%{_libdir}/libndbm.a
ln -sf libdb2.so.3			$RPM_BUILD_ROOT/%{_libdir}/libndbm.so

install -m644 db.h			$RPM_BUILD_ROOT/%{_includedir}/db2
install -m644 db_185.h			$RPM_BUILD_ROOT/%{_includedir}/db2
for p in db_archive db_checkpoint db_deadlock db_dump db_load \
	 db_printlog db_recover db_stat; do
	q="`echo $p | sed -e 's,^db_,db2_,'`"
	install -s -m755 $p		$RPM_BUILD_ROOT/%{_bindir}/$q
done

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README LICENSE
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/db2/db.h
%{_includedir}/db2/db_185.h
%{_libdir}/libdb2.a
%{_libdir}/libdb2.so
%{_libdir}/libndbm.a
%{_libdir}/libndbm.so
%{_bindir}/db2_archive
%{_bindir}/db2_checkpoint
%{_bindir}/db2_deadlock
%{_bindir}/db2_dump
%{_bindir}/db2_load
%{_bindir}/db2_printlog
%{_bindir}/db2_recover
%{_bindir}/db2_stat

%changelog
* Tue Mar 03 2004 Vincent Danen <vdanen@opensls.org> 2.4.14-10sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.4.14-9sls
- OpenSLS build
- tidy spec

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.4.14-8mdk
- rebuild
- drop Prefix tag
- use %%make macro

* Sat Nov 23 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.14-7mdk
- Patch2: os/os_fid.c (__db_fileid): Use implementation from db3, this
  fixes Python test_dbm on x86-64. Debian people use a similar patch
  because this works better under 64-bit architectures. Indeed.
  (Basically, we were getting an EINVAL resulting from a check for the
  "unthinkable". Sure, in the old days we hadn't had any 64-bit arch
  where we now have sizeof(<stat>.st_ino) + sizeof(<stat>.st_dev) +
  sizeof(time_t) > DB_FILE_ID_LEN with DB_FILE_ID_LEN == 20).

* Mon Jun 24 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.14-6mdk
- rpmlint fixes: hardcoded-library-path

* Tue Nov 06 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.4.14-5mdk
- Rebuild (to fix invalid-packager in rpmlint).

* Wed Oct 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.4.14-4mdk
- Make rpmlint a little happier.

* Tue Sep 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.4.14-3mdk
- s/Copyright/License.
- rebuild.

* Thu Dec  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.14-2mdk
- corrected missing ldconfig symlink.

* Tue Oct 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.14-1mdk
- First mandrake release.

* Thu Aug 17 2000 Bill Nottingham <notting@redhat.com>
- fix ia64 conflicts

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.

* Fri Jul 14 2000 Jeff Johnson <jbj@redhat.com>
- remove "strip -R comment" from spec file, rely on brp-* instead.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 28 2000 Matt Wilson <msw@redhat.com>
- regenerated the db2.patch to link against -ldb2, not -ldb

* Mon May  8 2000 Jeff Johnson <jbj@redhat.com>
- Rename files (like db1) to prepare for db3 deployment.
- Change version to reflect Berkeley db rather than glibc distribution.

* Thu Apr 27 2000 Jakub Jelinek <jakub@redhat.com>
- Don't provide makedb, it is provided by glibc.

* Wed Apr 20 2000 Jakub Jelinek <jakub@redhat.com>
- Create.
