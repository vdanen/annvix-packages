#
# spec file for package apr
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		apr
%define version		1.2.7
%define release		%_revrel
%define epoch		1

%define aprver		1
%define libname		%mklibname %{name} %{aprver}

Summary:	Apache Portable Runtime library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Libraries
URL:		http://apr.apache.org/
Source0:	http://www.apache.org/dist/apr/apr-%{version}.tar.gz
Source1:	http://www.apache.org/dist/apr/apr-%{version}.tar.gz.asc
Patch0:		apr-0.9.3-deplibs.patch
Patch1:		apr-1.1.0-config.diff
Patch2:		apr-1.0.0-mutextype_reorder.diff
Patch3:		apr-0.9.6-readdir64.patch
Patch4:		apr-0.9.6-fdr-procexit.patch
Patch5:		apr-1.2.2-locktimeout.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, automake1.7, libtool
BuildRequires:	doxygen, openssl-devel, python, e2fsprogs-devel

%description
The purpose of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.


%package -n %{libname}
Summary:	Apache Portable Runtime library
Group: 		System/Libraries
#Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	lib%{name}
Epoch:		%{epoch}

%description -n %{libname}
The purpose of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.


%package -n %{libname}-devel
Summary:	APR library development kit
Group:		Development/C
#Requires:	%{name} = %{version}
Requires:	%{libname} = 1:%{version}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	lib%{name}-devel %{name}-devel
Epoch:		%{epoch}

%description -n	%{libname}-devel
This package provides the support files which can be used to 
build applications using the APR library.  The mission of the
Apache Portable Runtime (APR) is to provide a free library of 
C data structures and routines.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .deplibs
%patch1 -p0 -b .config
%patch2 -p0 -b .mutextype_reorder
%patch3 -p1 -b .readdir64
%patch4 -p1 -b .procexit
%patch5 -p1 -b .locktimeout

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
    includedir:    %{_includedir}/apr-%{aprver}
    sysconfdir:    %{_sysconfdir}
    datadir:       %{_datadir}
    installbuilddir: %{_libdir}/apr-%{aprver}/build
    localstatedir: /var
    runtimedir:    /var/run
    libsuffix:     -\${APR_MAJOR_VERSION}
</Layout>
EOF


%build
# We need to re-run ./buildconf because of any applied patch(es)
rm -f configure
./buildconf

# hack to enable LFS on x86_64
%ifarch x86_64
perl -pi -e "s|4yes|8yes|g" configure*
cat > config.cache << EOF
apr_cv_use_lfs64=yes
EOF
%endif

# Forcibly prevent detection of shm_open (which then picks up but
# does not use -lrt).
cat >> config.cache << EOF
ac_cv_search_shm_open=no
EOF


%configure2_5x \
    --cache-file=config.cache \
    --includedir=%{_includedir}/apr-%{aprver} \
    --with-installbuilddir=%{_libdir}/apr-%{aprver}/build \
    --enable-layout=AVX \
%ifarch %ix86
%ifnarch i386 i486
    --enable-nonportable-atomics=yes \
%endif
%endif
    --enable-lfs \
    --enable-threads \
    --with-sendfile \
    --with-devrandom=/dev/urandom

%make
make dox

# Run non-interactive tests
%ifarch x86_64
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=97611
excludes=testlock
%endif
pushd test
    %make testall CFLAGS="-fno-strict-aliasing"
    TZ=PST8PDT ./testall -v ${excludes+-x $excludes} || exit 1
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

# These are referenced by apr_rules.mk
for f in make_exports.awk make_var_export.awk; do
    install -m 0644 build/${f} %{buildroot}%{_libdir}/apr-%{aprver}/build/${f}
done

install -m 0755 build/mkdir.sh %{buildroot}%{_libdir}/apr-%{aprver}/build/mkdir.sh

# these are needed if apr-util is ./buildconf'ed
for f in apr_common.m4 apr_hints.m4 apr_network.m4 apr_threads.m4 find_apr.m4; do
    install -m 0644 build/${f} %{buildroot}%{_libdir}/apr-%{aprver}/build/${f}
done
install -m 0755 build/gen-build.py %{buildroot}%{_libdir}/apr-%{aprver}/build/

# Sanitize apr_rules.mk
sed -e "/^apr_build/d" \
    -e 's|$(apr_builders)|%{_libdir}/apr-%{aprver}/build|g' \
    -e 's|$(apr_builddir)|%{_libdir}/apr-%{aprver}/build|g' \
    < build/apr_rules.mk > %{buildroot}%{_libdir}/apr-%{aprver}/build/apr_rules.mk

# Move docs to more convenient location
rm -rf html
mv docs/dox/html html

# Trim exported dependecies
sed -ri '/^dependency_libs/{s,-l(uuid|crypt) ,,g}' \
    %{buildroot}%{_libdir}/libapr*.la
perl -pi -e "s|-luuid -lcrypt||g" \
    %{buildroot}%{_bindir}/apr-%{aprver}-config \
    %{buildroot}%{_libdir}/pkgconfig/*.pc

# Unpackaged files:
rm -f %{buildroot}%{_libdir}/apr.exp


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libapr-%{aprver}.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/apr-%{aprver}-config
%{_libdir}/libapr-%{aprver}.*a
%{_libdir}/libapr-%{aprver}.so
%dir %{_libdir}/apr-%{aprver}
%dir %{_libdir}/apr-%{aprver}/build
%{_libdir}/apr-%{aprver}/build/*
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/apr-%{aprver}
%{_includedir}/apr-%{aprver}/*.h

%files doc
%defattr(-,root,root)
%doc CHANGES README*
%doc docs/APRDesign.html docs/canonical_filenames.html
%doc docs/incomplete_types docs/non_apr_programs
%doc --parents html


%changelog
* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- rebuild against new db4

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- 1.2.7 (needed by apache 2.2)
- new patches from mandriva; drop old unneeded patches
- updated deps
- add -doc subpackage
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7
- 0.9.7 (needed by apache 2.0.55)
- drop P10, P12, P13; merged upstream
- new P12 from fedora (0.9.6-6)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6
- Clean rebuild

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-5avx
- sync more patches with fedora

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-4avx
- sync with mandrake 0.9.6-4mdk:
  - sync with fedora (oden)
  - fix requires-on-release (oden)
  - drop the metux patch (P30)

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-2avx
- rebuild

* Fri Feb 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-1avx
- 0.9.6
- drop P3 merged upstream
- P19: rediffed; partially merged upstream (oden)
- disable debug build support

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.5-1avx
- first Annvix build for new-style apache2

* Tue Aug 10 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-11mdk
- rebuilt

* Tue Aug 03 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-10mdk
- sync with fedora (0.9.4-17)

* Wed Jun 30 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-9mdk
- new P0
- remove one hunk from P1, partially implemented upstream
- drop P6,P9,P10,P11,P12,P13,P14,P15,P16 and P18,
  the fix is implemented upstream
- drop P8, similar fix is implemented upstream

* Fri Jun 18 2004 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.5-8mdk
- rebuild with new openssl

* Thu Jun 17 2004 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.5-7mdk
- use fcntl for mutexes instead of posix mutexes (which won't work on
  non-NPTL kernels and some older processors), or sysvsem which are not
  resistand under high load.

* Wed Jun 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-6mdk
- sync with fedora

* Thu Jun 10 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-5mdk
- sync with fedora

* Tue May 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-4mdk
- sync with fedora

* Tue May 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-3mdk
- add the metux mpm hooks (P30)

* Sun May 09 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-2mdk
- oops!, forgot to pass "--cache-file=config.cache" to configure

* Fri May 07 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.5-1mdk
- initial fedora import and mandrake adaptions

* Wed Mar 24 2004 Joe Orton <jorton@redhat.com> 0.9.4-11
- add APR_LARGEFILE flag

* Mon Mar 15 2004 Joe Orton <jorton@redhat.com> 0.9.4-10
- fix configure check for mmap of /dev/zero
- just put -D_GNU_SOURCE in CPPFLAGS not _{BSD,SVID,XOPEN}_SOURCE

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 0.9.4-9.1
- rebuilt

* Thu Feb 19 2004 Joe Orton <jorton@redhat.com> 0.9.4-9
- undocument apr_dir_read() ordering constraint and fix tests

* Sun Feb 15 2004 Joe Orton <jorton@redhat.com> 0.9.4-8
- rebuilt without -Wall -Werror

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 0.9.4-7
- rebuilt

* Tue Feb  3 2004 Joe Orton <jorton@redhat.com> 0.9.4-6
- define apr_off_t as int/long/... to prevent it changing
  with _FILE_OFFSET_BITS on 32-bit platforms

* Mon Jan 12 2004 Joe Orton <jorton@redhat.com> 0.9.4-5
- add apr_temp_dir_get fixes from HEAD

* Thu Jan  8 2004 Joe Orton <jorton@redhat.com> 0.9.4-4
- ensure that libapr is linked against libpthread
- don't link libapr against -lnsl

* Thu Nov 13 2003 Joe Orton <jorton@redhat.com> 0.9.4-3
- -devel package no longer requires libtool

* Fri Oct  3 2003 Joe Orton <jorton@redhat.com> 0.9.4-2
- disable tests on x86_64 (#97611)

* Fri Oct  3 2003 Joe Orton <jorton@redhat.com> 0.9.4-1
- update to 0.9.4, enable tests
- ensure that libresolv is not used

* Sun Sep  7 2003 Joe Orton <jorton@redhat.com> 0.9.3-14
- use /dev/urandom (#103049)

* Thu Jul 24 2003 Joe Orton <jorton@redhat.com> 0.9.3-13
- add back CC=gcc, CXX=g++

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.3-12
- rebuild

* Mon Jul 14 2003 Joe Orton <jorton@redhat.com> 0.9.3-11
- work round useless autoconf 2.57 AC_DECL_SYS_SIGLIST

* Thu Jul 10 2003 Joe Orton <jorton@redhat.com> 0.9.3-10
- support --cc and --cpp arguments in apr-config

* Thu Jul  3 2003 Joe Orton <jorton@redhat.com> 0.9.3-9
- force libtool to use CC=gcc, CXX=g++

* Thu Jul  3 2003 Joe Orton <jorton@redhat.com> 0.9.3-8
- fix libtool location in apr_rules.mk

* Mon Jun 30 2003 Joe Orton <jorton@redhat.com> 0.9.3-7
- use AI_ADDRCONFIG in getaddrinfo() support (#73350)
- include a working libtool script rather than relying on
 /usr/bin/libtool (#97695)

* Wed Jun 18 2003 Joe Orton <jorton@redhat.com> 0.9.3-6
- don't use /usr/bin/libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 20 2003 Joe Orton <jorton@redhat.com> 0.9.3-5
- add fix for psprintf memory corruption (CAN-2003-0245)
- remove executable bit from apr_poll.h

* Thu May  1 2003 Joe Orton <jorton@redhat.com> 0.9.3-4
- link libapr against libpthread
- make apr-devel conflict with old subversion-devel
- fix License

* Tue Apr 29 2003 Joe Orton <jorton@redhat.com> 0.9.3-3
- run ldconfig in post/postun

* Tue Apr 29 2003 Joe Orton <jorton@redhat.com> 0.9.3-2
- patch test suite to not care if IPv6 is disabled

* Mon Apr 28 2003 Joe Orton <jorton@redhat.com> 0.9.3-1
- initial build
