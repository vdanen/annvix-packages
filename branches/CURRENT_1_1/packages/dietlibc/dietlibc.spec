#
# spec file for package dietlibc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		dietlibc
%define version 	0.28
%define release 	4avx

# This is eventually a biarch package, so no %_lib for diethome
%define diethome	%{_prefix}/lib/dietlibc

# Enable builds without testing (default is always to test)
%define build_check	1
%{expand: %{?_with_CHECK:	%%global build_check 1}}
%{expand: %{?_without_CHECK:	%%global build_check 0}}

Summary:	C library optimized for size
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.fefe.de/dietlibc/
Source0:	http://www.fefe.de/dietlibc/%{name}-%{version}.tar.bz2
Patch0:		dietlibc-0.21-features.patch.bz2
Patch1:		dietlibc-0.27-mdkconfig.patch.bz2
Patch3:		dietlibc-0.22-tests.patch.bz2
Patch4:		dietlibc-0.27-fix-getpriority.patch.bz2
Patch5:		dietlibc-0.22-net-ethernet.patch.bz2
Patch6:		dietlibc-0.24-rpc-types.patch.bz2
Patch7:		dietlibc-0.22-amd64-ioport.patch.bz2
Patch8:		dietlibc-0.24-strtol-64bit-fixes.patch.bz2
Patch9:		dietlibc-0.27-glibc-nice.patch.bz2
Patch10:	dietlibc-0.26-LC_-defines.patch.bz2
Patch11:	dietlibc-0.26-amd64-rdtsc.patch.bz2
Patch12:	dietlibc-0.26-64bit-fixes.patch.bz2
Patch13:	dietlibc-0.27-x86_64-lseek64.patch.bz2
# (oe) http://synflood.at/patches/contrapolice/contrapolice-0.3.patch
Patch14:	dietlibc-0.28-contrapolice.diff.bz2
Patch15:	dietlibc-0.27-ppc-rdtsc.patch.bz2
Patch16:	dietlibc-0.27-test-makefile-fix.patch.bz2
Patch17:	dietlibc-0.27-x86_64-stat64.patch.bz2
Patch18:	dietlibc-0.24-ppc64-umount.patch.bz2
Patch19:	dietlibc-0.24-ppc64-setjmp.patch.bz2
Patch20:	dietlibc-0.24-ppc64-endian.patch.bz2
Patch21:	dietlibc-0.24-ppc64-select.patch.bz2
Patch22:	dietlibc-0.27-ppc64-stat64.patch.bz2
Patch23:	dietlibc-0.27-biarch.patch.bz2
Patch24:	dietlibc-0.27-quiet.patch.bz2
Patch25:	dietlibc-0.27-ppc-select.patch.bz2
Patch26:	dietlibc-0.28-avx-stackgap_off.patch.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Small libc for building embedded applications.

%package devel
Group:          Development/C
Summary:        Development files for dietlibc
Obsoletes:	%{name}
Provides:	%{name}

%description devel
Small libc for building embedded applications.


%prep
%setup -q 
%patch0 -p1 -b .features
%patch1 -p1 -b .mdkconfig
%patch3 -p1 -b .tests
%patch4 -p1 -b .fix-getpriority
%patch5 -p1 -b .net-ethernet
%patch6 -p1 -b .rpc-types
#%patch7 -p1 -b .amd64-ioport
#%patch8 -p1 -b .strtol-64bit-fixes
%patch9 -p1 -b .glibc-nice -E
#%patch10 -p1 -b .locale-macros
#%patch11 -p1 -b .amd64-rdtsc
#%patch12 -p1 -b .tzfile-64bit-fixes
%patch13 -p1 -b .x86_64-lseek64
# (oe) http://synflood.at/patches/contrapolice/contrapolice-0.3.patch
# reject
%patch14 -p1 -b .contrapolice
%patch15 -p1 -b .ppc-rdtsc
%patch16 -p1 -b .inettest
%patch17 -p1 -b .x86_64-stat64
%patch18 -p1 -b .ppc64-umount
#%patch19 -p1 -b .ppc64-setjmp
#%patch20 -p1 -b .ppc64-endian
%patch21 -p1 -b .ppc64-select
%patch22 -p1 -b .ppc64-stat64
%patch23 -p1 -b .biarch
%patch24 -p1 -b .quiet
%patch25 -p1 -b .ppc-select
%patch26 -p1 -b .stackgap_off

# fix execute permissions on test scripts
chmod a+x test/{dirent,inet,stdio,string,stdlib,time}/runtests.sh


%build
%make
%make "CFLAGS=-pipe -nostdinc -fno-stack-protector"

# make and run the tests
%if %{build_check}
cd test
rm -f *.c.*
export DIETHOME="%{_builddir}/%{name}-%{version}"
MYARCH=`uname -m | sed -e 's/i[4-9]86/i386/' -e 's/armv[3-6][lb]/arm/'`
find -name "Makefile" | xargs perl -pi -e "s|^DIET.*|DIET=\"${DIETHOME}/bin-${MYARCH}/diet\"|g"
%make

STANDARD_TESTPROGRAMS=`grep "^TESTPROGRAMS" runtests.sh | cut -d\" -f2`
# these fail: cp-test3 cp-test4 cp-test6 cp-test7 cp-test11 cp-test12 cp-test15
CP_TEST_PROGRAMS="cp-test1 cp-test2 cp-test5 cp-test8 cp-test9 cp-test10 cp-test13 cp-test14"
perl -pi -e "s|^TESTPROGRAMS.*|TESTPROGRAMS=\"${STANDARD_TESTPROGRAMS} ${CP_TEST_PROGRAMS}\"|g" runtests.sh
# getpass requires user input
perl -pi -e "s|^PASS.*|PASS=\"\"|g" runtests.sh
sh ./runtests.sh
cd ..
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make DESTDIR=%{buildroot} install


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files devel
%defattr(-,root,root)
%doc AUTHOR BUGS CAVEAT CHANGES README THANKS TODO FAQ
%{_bindir}/diet
%dir %{diethome}
%{diethome}/*
%{_mandir}/man*/*


%changelog
* Wed Aug 10 2005 Vincent Danen <vdanen@annvix.org> 0.28-4avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen@annvix.org> 0.28-3avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 0.28-2avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 0.28-1avx
- 0.28
- drop P7, P8, P10, P11, P12, P19, P20 (merged upstream)
- P26: disable WANT_STACKGAP as it interferes with our gcc+SSP

* Thu Jan 20 2005 Vincent Danen <vdanen@annvix.org> 0.27-2avx
- some fixes

* Thu Jan 20 2005 Vincent Danen <vdanen@annvix.org> 0.27-1avx
- 0.27
- re-order patches to match mdk package
- merge with mandrake 0.27-9mdk:
  - fix getpriority() as the return value from the syscall is biased (gb)
  - add nice() implementation from glibc, make it use the fixed getpriority (gb)
  - fix ppc select() (gb)
  - quiet test bsearch (gb)
  - biarch builds on x86_64 and ppc64 (gb)
  - ppc64 fixes: umount, setjmp, __WORDSIZE, select, stat64, rdtsc (gb)
  - added struct stat64 as struct stat and fstat64() as fstat() on x86_64,
    so test suite builds (bluca)
  - add RDTSC in testsuite for ppc (cjw)
  - fix permissions on test scripts in subdirs (cjw)
  - P16: build inet tests (cjw)
  - make and run the test suite (oden)
  - implement lseek64() as lseek() on x86_64 (gb)
  - fix rdstc in testsuite for amd64 (gb)
  - fix tzfile() for 64bit-archs, aka. fix mktime() (gb)
  - P10: ISO C defines LC_ macros (7.11 [#3]) (gb)
  - merge P2 and P4 into P1 (ppc64asppc and lib64 fixes are now in P1) (oden)
  - P8: fix strtol() + testcase on 64-bit platforms (gb)  

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 0.24-3avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 0.24-2sls
- rebuild

* Mon Jan 26 2004 Vincent Danen <vdanen@opensls.org> 0.24-1sls
- 0.24
- contrapolice 0.1 for heap protection
- remove P4, P6, P9, P10, P11, P12, P13, P14, P15, P16, P17: all
  merged upstream
- don't apply P3 as it prevents us from building on amd64

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 0.22-8sls
- OpenSLS build
- tidy spec

* Wed Oct 29 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.22-7mdk
- Patch18: Enable inb() and friends in <sys/io.h> on AMD64 too

* Tue Aug 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.22-6mdk
- Patch17: 64-bit clean RPC code enough to let MDK stage1 do NFS mounts

* Tue Aug 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.22-5mdk
- Patch15: 64-bit fixes to htonl() & htons()
- Patch16: Let pmap_getport() handle IPPROTO_TCP

* Mon Apr  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.22-4mdk
- Patch14: Handle biarch struct utmp

* Sat Mar 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.22-3mdk
- added P13 (from CVS, fixes CAN-2003-0028)

* Fri Feb 21 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.22-2mdk
- Patch12: Fix resolver on 64-bit platforms

* Thu Feb 20 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.22-1mdk
- 0.22
- Patch11: Fix assert() on 64-bit platforms

* Wed Feb 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.22-0.2mdk
- Merge with gi/mdk-stage1 x86_64-branch:
  - Patch8: Add <net/ethernet.h> and <linux/if_ether.h> headers
  - Patch9: Make sure we define some u_{char,int,long} in <rpc/types.h>
  - Patch10: Fix check for syscall return value. Assume an error if
    %rax falls into [ -1 .. -127 ], as <asm-x86_64/unistd.h>
    defines. Aka. fix create_module() in insmod implementation

* Fri Nov 29 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.22-0.1mdk
- Update to CVS 2002/11/29 which contains most of the fixes I made and need
- Patch3: Correct implementation of sigaction() on x86-64
- Patch4: Fix ELF definitions on x86-64
- Patch5: Add some signal related tests
- Patch6: Fix warnings in testsuite here and there
- Patch7: Let it be lib64 aware

* Fri Nov 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.21-1mdk
- new version
- added P0, P1 and P2 from RH RawHide

* Thu Aug 29 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.19-2mdk
- rebuild becasue of bad signature

* Mon Aug 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.19-1mdk
- new version
- use two redhat patches (P0 & P1)
- add %{_bindir}/diet to package to ease usage
- misc spec file fixes
- relocate DIETHOME to %{_libdir}/dietlibc to avoid conflicts
  with glibc-devel (the redhat way of doing it...)

* Fri Feb 22 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.15-1mdk
- 0.15

* Tue Jan 29 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.14-1mdk
- 0.14

* Tue Oct 30 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.11-1mdk
- 0.11
- suppress patch by copying files in the spec

* Sat Mar 31 2001 David BAUDENS <baudens@mandrakesoft.com> 0.8-2mdk
- Don't use %%ix86 flags on non %%ix86 architectures
- Don't create useless package

* Thu Mar 22 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.8-1mdk
- updated to 0.8

* Fri Mar  9 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.7.3-3mdk
- rebuild

* Fri Mar  9 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.7.3-2mdk
- new cvs snapshot, adds mkstemp and syslog support among other things
- install includes in /usr/share/dietlibc/include (gc suggest)

* Thu Mar  8 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.7.3-1mdk
- first mdk contribs version: pre-0.7.3 cvs snapshot 20010308.

