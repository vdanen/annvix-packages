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
%define version		0.9.6
%define release		%_revrel

%define apuver		0
%define libname		%mklibname %{name} %{apuver}

Summary:	Apache Portable Runtime Utility library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Libraries
URL:		http://apr.apache.org/
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}.tar.gz.asc

Patch0:		apr-util-0.9.5-lib64.diff
# OE: these are from fedora
Patch1:		%{name}-0.9.3-deplibs.patch
Patch2:		%{name}-0.9.5-config.diff
Patch7:         %{name}-0.9.4-xlate.patch
# http://www.outoforder.cc/projects/libs/apr_memcache/apr_reslist_invalidate.patch
Patch8:		apr_reslist_invalidate.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildPrereq:	doxygen
BuildPrereq:	apr-devel >= 0.9.5
BuildPrereq:	openldap-devel db4-devel expat-devel gdbm-devel

%description
The purpose of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.


%package -n %{libname}
Summary:	Apache Portable Runtime Utility library
Group: 		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} %{name}
Obsoletes:	lib%{name} %{name}

%description -n	%{libname}
The purpose of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.


%package -n %{libname}-devel
Group:		Development/C
Summary:	APR utility library development kit
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Requires:	apr-util = %{version}
Requires:	apr-devel
Requires:	openldap-devel
Requires:	expat-devel
Provides:	lib%{name}-devel %{name}-devel
Obsoletes:	lib%{name}-devel %{name}-devel

%description -n	%{libname}-devel
This package provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.


%prep
%setup -q
%patch0 -p0 -b .lib64
%patch1 -p1 -b .deplibs
%patch2 -p0 -b .config
%patch7 -p1 -b .xlate
%patch8 -p0 -b .apr_reslist_invalidate


%build
%{__cat} >> config.layout << EOF
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
    installbuilddir: %{_libdir}/apr/build
    localstatedir: /var
    runtimedir:    /var/run
    libsuffix:     -\${APRUTIL_MAJOR_VERSION}
</Layout>
EOF

# We need to re-run ./buildconf because of any applied patch(es)
#./buildconf --with-apr=%{_prefix}
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force && aclocal-1.7 && autoconf --force

%configure2_5x \
    --with-apr=%{_prefix} \
    --includedir=%{_includedir}/apr-%{apuver} \
    --with-installbuilddir=%{_libdir}/apr/build \
    --enable-layout=AVX \
    --with-ldap \
    --with-gdbm

%make
make dox

# Run the less verbose tests
%define tests testmd5 testrmm teststrmatch testuri testxlate
pushd test
    make %{tests} testdbm
    for t in %{tests}; do ./${t} || exit 1; done
    ./testdbm auto tsdbm
    ./testdbm -tDB auto tbdb.db
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

# Documentation
rm -rf html; mv docs/dox/html html

# Unpackaged files
rm -f %{buildroot}%{_libdir}/aprutil.exp


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root,-)
%doc CHANGES LICENSE
%{_libdir}/libaprutil-%{apuver}.so.*

%files -n %{libname}-devel
%defattr(-,root,root,-)
%doc --parents html
%{_bindir}/apu-config
%{_libdir}/libaprutil-%{apuver}.*a
%{_libdir}/libaprutil-%{apuver}.so
%{_includedir}/apr-%{apuver}/*.h


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org>
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

