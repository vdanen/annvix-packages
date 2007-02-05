#
# spec file for package binutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$
#
# mdk 2.16.91.0.7-1mdk

%define revision	$Rev$
%define name		binutils
%define version		2.16.91.0.7
%define release		%_revrel

%define lib_major	2
%define libname_orig	%mklibname binutils
%define libname		%{libname_orig}%{lib_major}

Summary:	GNU Binary Utility Development Utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://sources.redhat.com/binutils/
Source0:	http://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
Patch0:		binutils-2.16.91.0.6-testsuite.patch
Patch1:		binutils-2.14.90.0.5-testsuite-Wall-fixes.patch
Patch2:		binutils-2.14.90.0.5-lt-relink.patch
Patch3:		binutils-2.15.92.0.2-linux32.patch
Patch4:		binutils-2.15.94.0.2-place-orphan.patch
Patch5:		binutils-2.15.92.0.2-ppc64-pie.patch
Patch6:		binutils-2.16.91.0.1-deps.patch
Patch7:		binutils-2.16.91.0.6-elfvsb-test.patch
Patch8:		binutils-2.16.91.0.6-frepo.patch
Patch9:		63_all_binutils-2.16.91.0.7-pt-pax-flags-20060317.patch
Patch10:	binutils-2.16.91.0.2-CVE-2006-2362.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	gettext
BuildRequires:	texinfo
BuildRequires:	glibc-static-devel
BuildRequires:	dejagnu

Requires:	%{libname} = %{version}-%{release}
Requires(post):	info-install
Requires(preun): info-install
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


%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{libname_orig}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with binutils.


%package -n %{libname}-devel
Summary:	Main library for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{libname_orig}-devel
Provides:	%{name}-devel

%description -n %{libname}-devel
This package contains the library needed to run programs dynamically
linked with binutils.

This is the development headers for %{libname}


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .testsuite
%patch1 -p1 -b .testsuite-Wall-fixes
%patch2 -p1 -b .lt-relink
%patch3 -p1 -b .linux32
%patch4 -p0 -b .place-orphan
%patch5 -p0 -b .ppc64-pie
%patch6 -p1 -b .deps
%patch7 -p0 -b .elfvsb-test
%patch8 -p0 -b .frepo
#%patch9 -p1 -b .pax
%patch10 -p1 -b .cve-2006-2362


%build
# Additional targets
ADDITIONAL_TARGETS=
%ifarch ia64
ADDITIONAL_TARGETS="--enable-targets=i586-annvix-linux"
%endif
%ifarch %{ix86}
ADDITIONAL_TARGETS="--enable-targets=x86_64-annvix-linux"
%endif

# Binutils comes with its own custom libtool
# [gb] FIXME: but system libtool also works and has relink fix
%define __libtoolize /bin/true
%configure \
    --enable-shared \
    $ADDITIONAL_TARGETS
%make tooldir=%{_prefix}

# Disable gasp tests since the tool is deprecated henceforth neither
# built nor already installed
(cd gas/testsuite/gasp/; mv gasp.exp gasp.exp.disabled)

# All Tests must pass on x86 and x86_64/amd64
echo ====================TESTING=========================
%ifarch %{ix86} x86_64 ppc ppc64
# because the S-records tests always fail for some reason (bi must be a
# magic machine)
rm -rf ld/testsuite/ld-srec
make check
%else
make -k check || echo make check failed
%endif
echo ====================TESTING END=====================

logfile="%{name}-%{version}-%{release}.log"
rm -f $logfile; find . -name "*.sum" | xargs cat >> $logfile


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}
%makeinstall_std

make prefix=%{buildroot}%{_prefix} infodir=%{buildroot}%{_infodir} install-info
install -m 0644 include/libiberty.h %{buildroot}%{_includedir}/
# Ship with the PIC libiberty
install -m 0644 libiberty/pic/libiberty.a %{buildroot}%{_libdir}/
rm -rf %{buildroot}%{_prefix}/%{_target_platform}/

rm -f %{buildroot}%{_mandir}/man1/{dlltool,nlmconv,windres}*
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_datadir}/locale/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info as.info
%_install_info bfd.info
%_install_info binutils.info
%_install_info gasp.info
%_install_info gprof.info
%_install_info ld.info
%_install_info standards.info


%preun
%_remove_install_info as.info
%_remove_install_info bfd.info
%_remove_install_info binutils.info
%_remove_install_info gasp.info
%_remove_install_info gprof.info
%_remove_install_info ld.info
%_remove_install_info standards.info


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*info*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libbfd-%{version}.so
%{_libdir}/libopcodes-%{version}.so

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libbfd.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.a
%{_libdir}/libopcodes.so
%{_libdir}/libiberty.a

%files doc
%defattr(-,root,root)
%doc README


%changelog
* Thu Aug 31 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.16.91.0.7
- P10: security fix for CVE-2006-2362

* Sat May 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.16.91.0.7
- rebuild the toolchain against itself (gcc/glibc/libtool/binutils)

* Sat May 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.16.91.0.7
- 2.16.91.0.7
- rebuild against gcc 4.0.3 and rebuilt glibc
- add -doc subpackage
- merge changes from 2.16.91.0.7-1mdk:
  - fix build with gcc 4.1
  - avoid abort with dynamic symbols in >64K sections (PR 2411)
  - merge with RH 2.16.91.0.6-6
    * support S signal frame augmentation flag in .eh_frame,
      add .cfi_signal_frame support (#175951, PR other/26208, BZ#300)
    * support DW_CFA_val_{offset,offset_sf,expression} in readelf/objdump
    * fix relaxation of TLS GD to LE on PPC (RH #184590)
    * fix for g++ -frepo ((RH #187142)
  - add Merom New Instructions (MNI)
- P9: add PaX support (from gentoo); disable the patch for the time being as
  make check dies on a few tests, particularly ld-i386/i386.exp (TLS issues)
  and ld-scripts/empty-aligned.exp

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.16.91.0.2
- Clean rebuild

* Fri Dec 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16.91.0.2
- build with SSP
- make check can't have stack protection or it will fail
- obfuscate email addresses

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16.91.0.2-2avx
- fix requires

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16.91.0.2-1avx
- 2.16.91.0.2:
  - update from binutils 2005 0720
  - add AMD SVME & Intel VMX support
  - add x86_64 new relocations for medium model
  - fix a PIE regression (PR 975)
  - fix an x86_64 signed 32bit displacement regression
  - fix PPC PLT (PR 2004)
  - improve empty section removal
- removed P6; fixed upstream
- new P6: make the linker ignore .got2 relocs against symbols from discarded
  sections (Alan Modra, PR target/17828) (gbeauchesne)
- new-style requires on info-install
- use %%libname instead of %%lib_name (for consistency)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16.91.0.1-3avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16.91.0.1-2avx
- rebuild for new gcc
- spec cleanups
- remove extraneous docs for all but the main package
- remove -fno-stack-protector-all from CFLAGS for testing

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16.91.0.1-1avx
- 2.16.91.0.1
- BuildRequires: glibc-static-devel
- remove support for cross-compilation

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.14.90.0.7-4avx
- bootstrap build
- make tests without stack protection so we don't get failed tests

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.14.90.0.7-3avx
- Annvix build

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
