# RH 2.14.90.0.4-19, SuSE 2.13.90.0.18-6
%define name		%{package_prefix}binutils
%define version		2.14.90.0.7
%define release		2sls

%define lib_major	2
%define lib_name_orig	%{package_prefix}%mklibname binutils
%define lib_name	%{lib_name_orig}%{lib_major}

# Define if building a cross-binutils
%define package_prefix	%{nil}
%{expand: %{?cross:	%%define target_cpu %{cross}}}
%{expand: %{?cross:	%%define package_prefix cross-%{target_cpu}-}}

Summary:	GNU Binary Utility Development Utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://sources.redhat.com/binutils/
Source0:	http://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
Patch0:		binutils-2.13.90.0.10-x86_64-testsuite.patch.bz2
Patch1:		binutils-2.13.90.0.10-x86_64-gotpcrel.patch.bz2
Patch2:		binutils-2.14.90.0.5-testsuite-Wall-fixes.patch.bz2
Patch3:		binutils-2.14.90.0.7-eh-frame-ro.patch.bz2
Patch4:		binutils-2.14.90.0.5-lt-relink.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	autoconf automake bison flex gcc gettext texinfo
BuildRequires:	dejagnu

Requires:	%{lib_name} = %{version}-%{release}
Conflicts:	gcc-c++ < 3.2.3-1mdk

%description
Binutils is a collection of binary utilities, including:

   * ar: creating modifying and extracting from archives
   * nm: for listing symbols from object files
   * objcopy: for copying and translating object files
   * objdump: for displaying information from object files
   * ranlib: for generating an index for the contents of an archive
   * size: for listing the section sizes of an object or archive file
   * strings: for listing printable strings from files
   * strip: for discarding symbols (a filter for demangling encoded C++ symbols
   * addr2line: for converting addresses to file and line
   * nlmconv: for converting object code into an NLM

Install binutils if you need to perform any of these types of actions on
binary files.  Most programmers will want to install binutils.

%package -n %{lib_name}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{lib_name_orig}

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with binutils.

%package -n %{lib_name}-devel
Summary:	Main library for %{name}
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{lib_name_orig}-devel, %{name}-devel

%description -n %{lib_name}-devel
This package contains the library needed to run programs dynamically
linked with binutils.

This is the development headers for %{lib_name}

%prep
%setup -q -n binutils-%{version}
%patch0 -p1 -b .x86_64-testsuite
%patch1 -p1 -b .x86_64-gotpcrel
%patch2 -p1 -b .testsuite-Wall-fixes
%patch3 -p1 -b .eh-frame-ro
%patch4 -p1 -b .lt-relink

%build
# Additional targets
ADDITIONAL_TARGETS=
%ifarch ia64
ADDITIONAL_TARGETS="--enable-targets=i586-opensls-linux"
%endif
%ifarch %{ix86}
ADDITIONAL_TARGETS="--enable-targets=amd64-opensls-linux"
%endif
%if "%{name}" != "binutils"
ADDITIONAL_TARGETS="--target=%{target_cpu}-linux"
%endif
# Binutils comes with its own custom libtool
# [gb] FIXME: but system libtool also works and has relink fix
%define __libtoolize /bin/true
%configure --enable-shared $ADDITIONAL_TARGETS
%make tooldir=%{_prefix} all info
%if "%{name}" != "binutils"
exit 0
%endif

# Disable gasp tests since the tool is deprecated henceforth neither
# built nor already installed
(cd gas/testsuite/gasp/; mv gasp.exp gasp.exp.disabled)

# All Tests must pass on x86 and x86_64/amd64
echo ====================TESTING=========================
%ifarch %{ix86} x86_64 amd64 ppc
# because the S-records tests always fail for some reason (bi must be a
# magic machine)
rm -rf ld/testsuite/ld-srec
%make check
%else
%make -k check || echo make check failed
%endif
echo ====================TESTING END=====================

logfile="%{name}-%{version}-%{release}.log"
rm -f $logfile; find . -name "*.sum" | xargs cat >> $logfile

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_prefix}
%makeinstall_std

%if "%{name}" == "binutils"
make prefix=$RPM_BUILD_ROOT%{_prefix} infodir=$RPM_BUILD_ROOT%{_infodir} install-info
install -m 644 include/libiberty.h $RPM_BUILD_ROOT%{_includedir}/
# Ship with the PIC libiberty
install -m 644 libiberty/pic/libiberty.a $RPM_BUILD_ROOT%{_libdir}/
rm -rf $RPM_BUILD_ROOT%{_prefix}/%{_target_platform}/
%else
rm -f  $RPM_BUILD_ROOT%{_libdir}/libiberty.a
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -rf $RPM_BUILD_ROOT%{_prefix}/%{target_cpu}-linux/lib/ldscripts/
rm -f  $RPM_BUILD_ROOT%{_prefix}/%{_target_platform}/%{target_cpu}-linux/%{_lib}/*.la
%endif

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{dlltool,nlmconv,windres}*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%if "%{name}" == "binutils"
%post
%_install_info as.info
%_install_info bfd.info
%_install_info binutils.info
%_install_info gasp.info
%_install_info gprof.info
%_install_info ld.info
%_install_info standards.info
%endif

%if "%{name}" == "binutils"
%preun
%_remove_install_info as.info
%_remove_install_info bfd.info
%_remove_install_info binutils.info
%_remove_install_info gasp.info
%_remove_install_info gprof.info
%_remove_install_info ld.info
%_remove_install_info standards.info
%endif

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_mandir}/man1/*
%if "%{name}" == "binutils"
%{_infodir}/*info*
%else
%{_prefix}/%{target_cpu}-linux/bin/*
%endif

%files -n %{lib_name}
%defattr(-,root,root)
%doc README
%if "%{name}" == "binutils"
%{_libdir}/libbfd-%{version}.so
%{_libdir}/libopcodes-%{version}.so
%else
%{_prefix}/%{_target_platform}/%{target_cpu}-linux/%{_lib}/libbfd-%{version}.so
%{_prefix}/%{_target_platform}/%{target_cpu}-linux/%{_lib}/libopcodes-%{version}.so
%endif

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc README
%if "%{name}" == "binutils"
%{_includedir}/*
%{_libdir}/libbfd.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.a
%{_libdir}/libopcodes.so
%{_libdir}/libiberty.a
%else
%{_prefix}/%{_target_platform}/%{target_cpu}-linux/include/*
%{_prefix}/%{_target_platform}/%{target_cpu}-linux/%{_lib}/libbfd.a
%{_prefix}/%{_target_platform}/%{target_cpu}-linux/%{_lib}/libbfd.so
%{_prefix}/%{_target_platform}/%{target_cpu}-linux/%{_lib}/libopcodes.a
%{_prefix}/%{_target_platform}/%{target_cpu}-linux/%{_lib}/libopcodes.so
%endif

%changelog
* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 2.14.90.0.7-2sls
- minor spec cleanups
- %%ifarch amd64 as well as x86_64
- use opensls tagging for %%_target_platform

* Tue Dec 23 2003 Vincent Danen <vdanen@opensls.org> 2.14.90.0.7-1sls
- 2.14.90.0.7
- new P3 for this version (gbeauchesne)
- remove the ld/testsuite/ld-screc test since it never wants to pass (bi
  must be a magic machine)

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 2.14.90.0.5-3sls
- OpenSLS build
- tidy spec

* Wed Aug  6 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.14.90.0.5-2mdk
- better relink fix

* Wed Aug  6 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.14.90.0.5-1mdk
- 2.14.90.0.5

* Wed Jul 16 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.14.90.0.4-2mdk
- Merge with RH 2.14.90.0.4-19:
  - fix -pie support on amd64, s390, s390x and ppc64
  - issue relocation overflow errors for s390/s390x -fpic code when
    accessing .got slots above 4096 bytes from .got start

* Tue Jul  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.14.90.0.4-1mdk
- Patch17: Fix embedded libtool relink
- Merge with RH 2.14.90.0.4-18:
  - CFI updates
  - Rename ld --dynamic option to --pic-executable or --pie
  - Add PT_GNU_STACK support
  - Handle as --execstack and --noexec stack
  - Fix readelf -d on IA-64
  - Add new Intel Prescott instructions
  - Fix shared libraries with >= 8192 .plt slots on ppc32

* Fri May  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.20-1mdk
- 2.13.90.0.20
- Ship with c++filt here since it's no longer available in gcc3.3
- Patch4: Fix TLS on IA-64 with ld relaxation (Jakub Jelinek)
- Patch5: Fix ppc32 PLT reference counting (Alan Modra)
- Patch6: optimize DW_CFA_advance_loc4 in gas even if there is 'z'
  augmentation with size 0 in FDE (Jakub Jelinek)

* Wed Apr  2 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.18-5mdk
- Enable Patch0 (CVS 2003/02/06)
- Patch5: Don't optimize .eh_frame during ld -r (RH 2.13.90.0.18-7)

* Sat Mar 15 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.18-4mdk
- Enable build of cross binutils
- Move includes to -devel package

* Sat Feb 15 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.18-3mdk
- Tighten lib requirements
- Patch11: Handle # <linenum> "<filename>" directives, though this is
  a deprecated feature (Nick Clifton)

* Sat Feb 15 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.18-2mdk
- Remove glibc21 compat patch
- Enable more targets: X86-64 on IA-32, IA-32 on IA-64
- Patch1: Handle .symver x, x@FOO in ld such that relocs against x
  become dynamic relocations against x@FOO (Jakub Jelinek)
- Patch9: Fix ld-shared testsuite if building with -Wall since
  ld-lib.exp (prune_warnings) doesn't prune gcc warnings

* Sat Feb  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.18-1mdk
- All tests should pass on PPC by now
- Patch6: Fix ld on lib64 systems (CVS)
- Patch7: Fix SEARCH_DIR statements on multi-abi arches (CVS)
- Patch8: Fix .eh_frame_hdr sign extension bug (CVS)
- Update to 2.13.90.0.18:
  - Fix an ia64 gas bug
  - Fix some TLS bugs
  - Fix some ELF/ppc bugs

* Wed Feb  5 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.16-6mdk
- Rewrite Patch7 (x86_64-disasm-movd) to introduce new dq_mode instead

* Mon Feb  3 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.16-5mdk
- Patch7: Fix x86-64 disassembly of MOVD with REX prefix

* Mon Jan 20 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.16-4mdk
- Patch6: Fix ld invocation flags in ld-srec testsuite (Alan Modra)

* Fri Jan 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.16-3mdk
- Move linker name libraries to -devel package
- Add Provides: binutils-devel, libbinutils accordingly

* Fri Jan 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.16-2mdk
- Rebuild, use %%mklibname

* Tue Dec 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.16-1mdk
- Update to 2.13.90.0.16
- Merge with Red Hat release 2.13.90.0.16-3:
  - pad .rodata.cstNN sections at the end if they aren't sized to
    multiple of sh_entsize
  - temporary patch to make .eh_frame and .gcc_except_table sections
    readonly if possible (should be removed when AUTO_PLACE is implemented)
  - fix .PPC.EMB.apuinfo section flags
  - STT_TLS SHN_UNDEF fix
  - fix IA-64 ld bootstrap
  - fix strip on TLS binaries and libraries

* Fri Nov 15 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13.90.0.10-1mdk
- Update to 2.13.90.0.10
- Ship with the PIC libiberty

* Mon Nov  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.15-4mdk
- Patch6: USE_BRL optimization for Itanium2

* Mon Nov 04 2002 Ha Quôc-Viêt <viet@mandrakesoft.com> 2.12.90.0.15-3mdk
-Patch20: corrects missing include in budemang.c, memcpy should be linked now

* Fri Sep 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.15-2mdk
- Patch3: Fix reference counting on various platforms (Alan Modra)
- Patch4: Fix problem with absolute section (Alan Modra)
- Patch5: Fix counting of definitions in shared objects (H.J. Lu)
- Patch12: Fix x86-64 gotpcrel generation (Jan Hubicka, SuSE 2.12.90.0.15-37)
- Patch13: Fix LIB_PATH for x86_64 (SuSE 2.12.90.0.15-37)

* Mon Aug 12 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.15-1mdk
- Update to 2.12.90.0.15
- Patch2: Fix IA-32 gas _GLOBAL_OFFSET_TABLE_ handling bugs (Jakub Jelinek)

* Thu Jul 18 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.14-3mdk
- Patch16: Fix generation of nops for x86-64 (SuSE 2.12.90.0.14-8)

* Mon Jul 15 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.14-2mdk
- Add BuildRequires: for make check'ing
- Don't forcibly redefine CFLAGS
- Patch3: Fix -ffunction-sections
- Patch2: Performance bug fix on Itanium 2 concerning an encoding
  table bug for the indirect call instruction (br.call b1=b2)

* Fri Jun 28 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.14-1mdk
- Update to 2.12.90.0.14
- Merge with SuSE release 2.12.90.0.11-4:
  - Revert ld -Y patch
  - Try to error out if shared libs are built without -fPIC on x86-64

* Sun Jun 23 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.7-6mdk
- Merge with SuSE release 2.12.90.0.11-1:
  - Update Patch2 (x86_64-biarch)
  - Better handling of ld -Y with multilibs

* Tue Jun 18 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.7-5mdk
- Make check in %%build stage, shall all pass on x86 and x86_64
- Patch2: Select the correct library for the target
  architecture. Aka. Fix biarch support for x86-64 (H.J. Lu)

* Mon Jun 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.7-4mdk
- Rebuild, use %%makeinstall

* Mon Jun 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.7-3mdk
- Merge with SuSE release 2.12.90.0.7-10 (4 new patches):
  - Fix pcrel relocations for x86-64
  - Add PIC configuration for x86-64
  - x86-64 relocations conversion should not just convert to 64-bit
    relocations since there are sometimes 32-bit ones
  - Make selective[1245] xfail on x86-64

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.7-2mdk
- Automated rebuild in gcc3.1 environment

* Tue Apr 30 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.7-1mdk
- Fix URL and Source0 links
- Update to 2.12.90.0.7, which fixes an .eh_frame optimization
- Drop Patch2 (DATA_SEGMENT_ALIGN) since integrated in upstream sources
- Disable "gasp" regression testsuite since that tool is deprecated
  henceforth neither built nor already installed, thus always failing

* Thu Apr  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.90.0.3-1mdk
- Regenerate Patch1 (elf_i386_glibc21)
- Regenerate Patch12 as Patch2 (DATA_SEGMENT_ALIGN)
- Update to 2.12.90.0.3 which obsoletes Patch2 up to Patch11
- Also note that "gasp" is deprecated henceforth not packaged

* Tue Mar 19 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11.93.0.2-1mdk
- Remove Patch50 now included in sources
- Merge with RH release 2.11.93.0.2-9:
  - fix DATA_SEGMENT_ALIGN on ia64/alpha/sparc/sparc64
  - don't crash on SHN_UNDEF local dynsyms (Andrew MacLeod)
  - fix bfd configury bug (Alan Modra)
  - don't copy visibility when equating symbols
  - fix alpha .text/.data with .previous directive bug
  - fix SHF_MERGE crash with --gc-sections (#60369)
  - C++ symbol versioning patch
  - add DW_EH_PE_absptr -> DW_EH_PE_pcrel optimization for shared libs,
    if DW_EH_PE_absptr cannot be converted that way, don't build the
    .eh_frame_hdr search table
  - trade one saved runtime page for data segment (=almost always not shared)
    for up to one page of disk space where possible

* Wed Feb  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11.92.0.12-6mdk
- Rename Patch19 (Fix handling of Alpha plt entries) to Patch50.
- Merge with RH release 2.11.92.0.12-10:
  - Patch19: Don't create SHN_UNDEF STB_WEAK symbols unless there are
    any relocations against them.

* Fri Jan 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11.92.0.12-5mdk
- Temporarily disable all .shf-merge patches for Alpha since they
  break glibc build. That's a solution to fix glibc build on Alpha but
  it breaks other application builds with SHF_MERGE support.
- Patch19: elf64-alpha.c (elf64_alpha_adjust_dynamic_symbol): Don't
  suppress plt entries for undefweak symbols. This should fix
  glibc-2.2.5 build on Alpha. (Richard Henderson, CVS HEAD 2002/01/23)
- Remove all .eh-frame patches (P9, P12, P13, P14, P17, P18)
  concerning the PT_GNU_EH_FRAME optimization that appears to break
  other arches (ppc, alpha). It's probably not stable enough for IA-32
  as well.

* Mon Jan 21 2002 Stefan van der Eijk <stefan@eijk.nu> 2.11.92.0.12-4mdk
- eh-frame patches cause segfaults with ld on certain c++ builds - alpha
- BuildRequires

* Tue Jan 15 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.11.92.0.12-3mdk
- eh-frame patches cause segfaults with ld on certain c++ builds - PPC
 
* Wed Jan  2 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11.92.0.12-2mdk
- Merge up to RH release 2.11.92.0.12-8

* Wed Dec 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11.92.0.12-1mdk
- Merge with rh patches.
- 2.11.92.0.12.

* Fri Dec  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11.92.0.7-4mdk
- Disable patch2 break kernel build.

* Wed Dec  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11.92.0.7-3mdk
- Upgrade strings64 patch to fix strings on ia32 :p.

* Mon Nov 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11.92.0.7-2mdk
- Use oldmakeinstall instead of makeinstall (too tricky to do proper support of DESTDIR).

* Wed Oct 31 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11.92.0.7-1mdk
- Merge up to RH-2.11.92.0.7

* Fri Oct  5 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.11.90.0.8-6mdk
- Patch9: add IA-64 @iplt reloc
- Really enable -z combreloc by default

* Fri Sep 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11.90.0.8-5mdk
- put RELATIVE relocs first, not last (rh).
- enable -z combreloc by default on IA-{32,64}, Alpha, Sparc* (rh).

* Tue Jul 31 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11.90.0.8-4mdk
- Merge with rh patches.

* Tue Jun 26 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11.90.0.8-3mdk
- Make hard-links as true files.

* Tue Jun 26 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11.90.0.8-2mdk
- Workaround libtool/rpm weirdness.

* Mon Jun 25 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.11.90.0.8-1mdk
- Various spec fixes and rh merges.
- 2.11.90.

* Sat May 26 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10.91.0.2-1mdk
- Merge RH patches.
- 2.10.91.0.2.

* Sun May 20 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.10.1.0.2-5mdk
- BuildRequires bison, flex

* Thu Apr 12 2001 Francis Galiegue <fg@mandrakesoft.com> 2.10.1.0.2-4mdk
- No longer excludearch ia64

* Mon Jan 22 2001 Stefan van der Eijk <s.vandereijk@chello.nl> 2.10.1.0.2-3mdk
- rebuild to fix broken src.rpm on mirrors

* Fri Jan 05 2001 David BAUDENS <baudens@mandrakesoft.com> 2.10.1.0.2-2mdk
- BuildRequires: texinfo

* Tue Nov 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10.1.0.2-1mdk
- Split libs(and devel) of binaries.
- 2.10.1.0.2.

* Thu Nov 09 2000 François Pons <fpons@mandrakesoft.com> 2.10.1-1mdk
- new release

* Tue Oct 10 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10.0.24-5mdk
- Really remove c++filt this one come from gcc2.96 package.

* Sun Aug 27 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.10.0.24-4mdk
- add back c++filt (chmouscks)

* Sun Aug 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10.0.24-3mdk
- Fix %post script.

* Sat Aug 26 2000 David BAUDENS <baudens@mandrakesoft.com> 2.10.0.24-2mdk
- Fix build for i486 (and other x86 archs)
- Human readable Description

* Thu Aug 24 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.10.0.24-1mdk
- new release
- fix tmppath

* Fri Jul 28 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.10.0.18-1mdk
- BM
- new release
- real macroszification.

* Wed Jul 12 2000 Warly <warly@mandrakesoft.com> 2.10.0.12-1mdk
- 2.10.0.12

* Thu Jun 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.10.0.9-2mdk
- Macroszification.
- Remove c++-filt since the one from gcc2.96 is more recent.

* Mon Jun 26 2000 Warly <warly@mandrakesoft.com> 2.10.0.9-1mdk
- 2.10.0.9

* Thu Mar 23 2000 Florent Villard <warly@mandrakesoft.com> 2.9.5.0.31-1mdk
- group update
- mandrake adaptation
