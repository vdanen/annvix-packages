#
# spec file for package db1
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		db1
%define version 	1.85
%define release 	%_revrel

Summary:	The BSD database library for C (version 1)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://www.sleepycat.com
Source:		http://www.sleepycat.com/update/%{version}/db.%{version}.tar.bz2
Patch0:		db.%{version}.patch
Patch1:		db.%{version}-include.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires(post):	ldconfig
Requires(postun): ldconfig
# this is a symlink not a real soname, so it has to be explicitely put
# in a provides line -- pablo
Provides:	libdb1.so.2
%ifnarch ia64
Conflicts:	glibc < 2.1.90
%endif

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
It should be installed if compatibility is needed with databases created
with db1.
This library used to be part of the glibc package.


%package devel
Summary:	Development libs/header files for Berkeley DB (version 1) library
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


%package tools
Summary:	Tools for Berkeley DB (version 1) library
Group:		Databases

%description tools
Tools to manipulate Berkeley Databases (Berkeley DB).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n db.%{version}
%patch0 -p1
%patch1 -p1 -b .old


%build
gzip -9 docs/*.ps
pushd PORT/linux
    # otherwise "db1/db.h" not found
    ln -s include db1
    %make OORG="%{optflags}" 
popd

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_includedir}/db1,%{_bindir},%{_libdir}}

sed -n '/^\/\*-/,/^ \*\//s/^.\*.\?//p' include/db.h | grep -v '^@.*db\.h' > LICENSE

pushd PORT/linux
    sover=`echo libdb.so.* | sed 's/libdb.so.//'`
    install -m 0644 libdb.a %{buildroot}%{_libdir}/libdb1.a
    install -m 0755 libdb.so.$sover %{buildroot}%{_libdir}/libdb1.so.$sover
    ln -sf libdb1.so.$sover %{buildroot}%{_libdir}/libdb1.so
    ln -sf libdb1.so.$sover %{buildroot}%{_libdir}/libdb.so.$sover
    install -m 0644 ../include/ndbm.h %{buildroot}%{_includedir}/db1/
    install -m 0644 ../../include/db.h %{buildroot}%{_includedir}/db1/
    install -m 0644 ../../include/mpool.h %{buildroot}%{_includedir}/db1/
    install -s -m 0755 db_dump185 %{buildroot}%{_bindir}/db1_dump185
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_libdir}/libdb1.so.*
%{_libdir}/libdb.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/db1
%{_libdir}/libdb1.a
%{_libdir}/libdb1.so

%files tools
%defattr(-,root,root)
%{_bindir}/db1_dump185

%files doc
%defattr(-,root,root)
%doc README LICENSE changelog docs/*.ps.gz


%changelog
* Thu Jun 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.85
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.85
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.85
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.85-15avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.85-14avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.85-13avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.85-12avx
- Annvix build

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 1.85-11sls
- remove %%prefix
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 1.85-10sls
- OpenSLS build
- tidy spec

* Thu Jul 10 2003 Götz Waschk <waschk@linux-mandrake.com> 1.85-9mdk
- rebuild for new rpm

* Fri Jun  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.85-8mdk
- rpmlint fixes: hardcoded-library-path

* Tue Nov 06 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.85-7mdk
- Rebuild (to fix invalid-packager from rpmlint).

* Tue Sep 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.85-6mdk
- s/Copyright/License.
- rebuild

* Wed May 09 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.85-5mdk
- tell to provide 'libdb1.so.2' (it has to be expliciteltold, as it
  is a symlink and not a real soname; so it is not automatically found)
  this allows proper install on some systems having old compiled binaries

* Thu Apr 12 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.85-4mdk
- Fix chicken and egg problem: Be able to compile this even with no db1 
  previously installed (Abel Cheung maddog@linuxhall.org).

* Thu Dec  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.85-3mdk
- new lib policy.

* Tue Nov 28 2000 dam's <damien@mandrakesoft.com> 1.85-2mdk
- fixed bad db.h include (patch 1 : db.1.85-include)

* Mon Oct 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.85-1mdk
- First mandrake package.

* Thu Aug 17 2000 Bill Nottingham <notting@redhat.com>
- fix ia64 conflicts

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.

* Sun Aug  6 2000 Jeff Johnson <jbj@redhat.com>
- remove "strip -R comment" from spec file, rely on brp-* instead.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun May 28 2000 Jeff Johnson <jbj@redhat.com>
- rename db_dump185 to db1_dump185 to avoid file conflict with db3.

* Thu Apr 20 2000 Jakub Jelinek <jakub@redhat.com>
- Include db_dump185 program from db2 here (as it is linked
  against this shared library).

* Wed Apr 19 2000 Jakub Jelinek <jakub@redhat.com>
- Create.

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
