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
%define version		0.9.6
%define release		%_revrel
%define epoch		1

%define aprver		0
%define libname		%mklibname %{name} %{aprver}

Summary:	Apache Portable Runtime library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Libraries
URL:		http://apr.apache.org/
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}.tar.gz.asc
Patch0:		apr-0.9.3-deplibs.patch
Patch1:		apr-0.9.5-config.diff
Patch2:		apr-0.9.3-noipv6.patch
Patch3:		apr-0.9.4-trimlibs.patch
Patch4:		apr-0.9.4-tests.patch
Patch5:		apr-0.9.5-mutextype_reorder.diff
Patch6:		apr-0.9.6-guardsize.diff
Patch7:		apr-0.9.4-cleanups.patch
Patch8:		apr-0.9.4-cflags.patch
Patch9:		apr-0.9.4-lp64psem.patch
Patch10:	apr-0.9.4-attrerror.patch
Patch11:	apr-0.9.6-readdir64.patch
Patch12:	apr-0.9.6-uidgid.patch
Patch13:	apr-0.9.6-flushbufs.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildPrereq:	autoconf2.5
BuildPrereq:	automake1.7
BuildPrereq:	libtool
BuildPrereq:	doxygen

%description
The purpose of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.


%package -n %{libname}
Summary:	Apache Portable Runtime library
Group: 		System/Libraries
#Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name}
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
Provides:	lib%{name}-devel %{name}-devel
Obsoletes:	lib%{name}-devel %{name}-devel
Epoch:		%{epoch}

%description -n	%{libname}-devel
This package provides the support files which can be used to 
build applications using the APR library.  The mission of the
Apache Portable Runtime (APR) is to provide a free library of 
C data structures and routines.


%prep
%setup -q
%patch0 -p1 -b .deplibs
%patch1 -p0 -b .config
%patch2 -p1 -b .noipv6
%patch3 -p1 -b .trimlibs
%patch4 -p1 -b .tests
%patch5 -p0 -b .mutextype_reorder
%patch6 -p1 -b .guardsize
%patch7 -p1 -b .cleanups
%patch8 -p1 -b .cflags
%patch9 -p1 -b .lp64psem
%patch10 -p1 -b .attrerror
%patch11 -p1 -b .readdir64
%patch12 -p1 -b .uidgid
%patch13 -p1 -b .flushbufs


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
    includedir:    %{_includedir}/apr-%{aprver}
    sysconfdir:    %{_sysconfdir}
    datadir:       %{_datadir}
    installbuilddir: %{_libdir}/apr/build
    localstatedir: /var
    runtimedir:    /var/run
    libsuffix:     -\${APR_MAJOR_VERSION}
</Layout>
EOF

# We need to re-run ./buildconf because of any applied patch(es)
./buildconf

%configure2_5x \
    --cache-file=config.cache \
    --includedir=%{_includedir}/apr-%{aprver} \
    --with-installbuilddir=%{_libdir}/apr/build \
    --enable-layout=AVX \
%ifarch %ix86
%ifnarch i386 i486
    --enable-nonportable-atomics=yes \
%endif
%endif
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
    install -m 0644 build/${f} %{buildroot}%{_libdir}/apr/build/${f}
done

install -m 0755 build/mkdir.sh %{buildroot}%{_libdir}/apr/build/mkdir.sh

# Sanitize apr_rules.mk
sed -e "/^apr_build/d" \
    -e 's|$(apr_builders)|%{_libdir}/apr/build|g' \
    -e 's|$(apr_builddir)|%{_libdir}/apr/build|g' \
    < build/apr_rules.mk > %{buildroot}%{_libdir}/apr/build/apr_rules.mk

# Move docs to more convenient location
rm -rf html; mv docs/dox/html html

# Unpackaged files:
rm -f %{buildroot}%{_libdir}/apr.exp


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root,-)
%doc CHANGES README*
%{_libdir}/libapr-%{aprver}.so.*

%files -n %{libname}-devel
%defattr(-,root,root,-)
%doc docs/APRDesign.html docs/canonical_filenames.html
%doc docs/incomplete_types docs/non_apr_programs
%doc --parents html
%{_bindir}/apr-config
%{_libdir}/libapr-%{aprver}.*a
%{_libdir}/libapr-%{aprver}.so
%dir %{_libdir}/apr
%dir %{_libdir}/apr/build
%{_libdir}/apr/build/*
%dir %{_includedir}/apr-%{aprver}
%{_includedir}/apr-%{aprver}/*.h


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org>
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
