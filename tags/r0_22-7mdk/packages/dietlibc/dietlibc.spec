%define name	dietlibc
%define version 0.22
%define release 7mdk

Summary:	C library optimized for size
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Url:		http://www.fefe.de/dietlibc/
Source0:	http://www.fefe.de/dietlibc/%{name}-%{version}.tar.bz2
Patch0:		dietlibc-0.21-features.patch.bz2
Patch1:		dietlibc-0.21-config.patch.bz2
Patch2:		dietlibc-0.21-ppc64asppc.patch.bz2
Patch3:		dietlibc-0.22-x86_64-sigaction.patch.bz2
Patch4:		dietlibc-0.22-x86_64-elf.patch.bz2
Patch5:		dietlibc-0.22-tests.patch.bz2
Patch6:		dietlibc-0.22-fix-tests-warnings.patch.bz2
Patch7:		dietlibc-0.22-lib64.patch.bz2
Patch8:		dietlibc-0.22-net-ethernet.patch.bz2
Patch9:		dietlibc-0.22-rpc-types.patch.bz2
Patch10:	dietlibc-0.22-x86_64-syscall-retval.patch.bz2
Patch11:	dietlibc-0.22-assert-fix.patch.bz2
Patch12:	dietlibc-0.22-resolv.patch.bz2
Patch13:	dietlibc-0.22-CAN-2003-0028.patch.bz2
Patch14:	dietlibc-0.22-biarch-utmp.patch.bz2
Patch15:	dietlibc-0.22-64bit-fixes.patch.bz2
Patch16:	dietlibc-0.22-pmgetport-IPPROTO_TCP.patch.bz2
Patch17:	dietlibc-0.22-rpc64.patch.bz2
Patch18:	dietlibc-0.22-amd64-ioport.patch.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Small libc for building embedded applications.

%package devel
Group:          Development/C
Summary:        Development files for dietlibc
Obsoletes:	%name
Provides:	%name

%description devel
Small libc for building embedded applications.

%prep
%setup -q 
%patch0 -p1 -b .features
%patch1 -p1 -b .config
%patch2 -p1 -b .ppc
%patch3 -p1 -b .x86_64-sigaction
%patch4 -p1 -b .x86_64-elf
%patch5 -p1 -b .tests
%patch6 -p1 -b .fix-tests-warnings
%patch7 -p1 -b .lib64
%patch8 -p1 -b .net-ethernet
%patch9 -p1 -b .rpc-types
%patch10 -p1 -b .x86_64-syscall-retval
%patch11 -p1 -b .assert-fix
%patch12 -p1 -b .resolv
%patch13 -p1 -b .CAN-2003-0028
%patch14 -p1 -b .biarch-utmp
%patch15 -p1 -b .64bit-fixes
%patch16 -p1 -b .pmgetport-IPPROTO_TCP
%patch17 -p1 -b .rpc64
%patch18 -p1 -b .amd64-ioport

%build
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files devel
%defattr(-,root,root)
%doc AUTHOR BUGS CAVEAT CHANGES README THANKS TODO
%{_bindir}/diet
%{_libdir}/dietlibc
%{_mandir}/man*/*

%changelog
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

