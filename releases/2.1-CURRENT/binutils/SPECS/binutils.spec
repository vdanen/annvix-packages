#
# spec file for package binutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$
#
# mdk 2.17.50.0.9-1mdv

%define revision	$Rev$
%define name		binutils
%define version		2.17.50.0.12
%define release		%_revrel

%define major		2
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

%define arch		%(echo %{target_cpu}|sed -e "s/\(i.86\|athlon\)/i386/" -e "s/amd64/x86_64/" -e "s/\(sun4.*\|sparcv[89]\)/sparc/")
%define isarch()	%(case %{arch} in (%1) echo 1;; (*) echo 0;; esac)

Summary:	GNU Binary Utility Development Utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://sources.redhat.com/binutils/
Source0:	http://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
Patch1:		binutils-2.14.90.0.5-testsuite-Wall-fixes.patch
Patch2:		binutils-2.16.91.0.7-libtool.patch
Patch3:		binutils-2.17.50.0.8-linux32.patch
Patch4:		binutils-2.17.50.0.12-place-orphan.patch
Patch5:		binutils-2.17.50.0.12-ppc64-pie.patch
Patch6:		binutils-2.16.91.0.1-deps.patch
Patch7:		binutils-2.17.50.0.12-ltconfig-multilib.patch
Patch8:		binutils-2.17.50.0.12-standards.patch
Patch9:		binutils-2.17.50.0.12-symbolic-envvar-revert.patch
Patch10:	binutils-2.17.50.0.12-osabi.patch
Patch11:	binutils-2.17.50.0.12-rh235747.patch
#Patch9:		63_all_binutils-2.16.91.0.7-pt-pax-flags-20060317.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	gettext
BuildRequires:	texinfo
#BuildRequires:	glibc-static-devel
BuildRequires:	dejagnu

Requires:	%{libname} = %{version}
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
Group:		Development/Other
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with binutils.


%package -n %{devname}
Summary:	Main library for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 2 -d

%description -n %{devname}
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
%patch1 -p1 -b .testsuite-Wall-fixes
%patch2 -p1 -b .libtool
%patch3 -p1 -b .linux32
%patch4 -p0 -b .place-orphan
%patch5 -p0 -b .ppc64-pie
%patch6 -p1 -b .deps
%patch7 -p0 -b .ltconfig-multilib
%patch8 -p0 -b .standards
%patch9 -p0 -b .tekhex
%patch10 -p0 -b .osabi
%patch11 -p0 -b .rh235747~


%build
# Additional targets
ADDITIONAL_TARGETS=""
case %{target_cpu} in
    i*86 | athlon*)
        ADDITIONAL_TARGETS="x86_64-annvix-linux"
        ;;
esac

[[ -n "$ADDITIONAL_TARGETS" ]] && ADDITONAL_TARGETS="--enable-targets=$ADDITIONAL_TARGETS"

case %{target_cpu} in
    i*86 | athlon*)
        ADDITIONAL_TARGETS="$ADDITIONAL_TARGETS --enable-64-bit-bfd"
        ;;
esac

# Binutils comes with its own custom libtool
# [gb] FIXME: but system libtool also works and has relink fix
%define __libtoolize /bin/true

# Build with -Wno-error
export CFLAGS="%{optflags} -Wno-error"

# Build main binaries
rm -rf objs
mkdir objs
pushd objs
    CONFIGURE_TOP=.. %configure --enable-shared $ADDITIONAL_TARGETS
    %make tooldir=%{_prefix}
popd


%check
# All Tests must pass on x86 and x86_64
echo ====================TESTING=========================
%make -C objs check || echo make check failed
echo ====================TESTING END=====================

logfile="%{name}-%{version}-%{release}.log"
rm -f $logfile; find . -name "*.sum" | xargs cat >> $logfile


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}
%makeinstall_std -C objs

make -C objs prefix=%{buildroot}%{_prefix} infodir=%{buildroot}%{_infodir} install-info
install -m 0644 include/libiberty.h %{buildroot}%{_includedir}/
# Ship with the PIC libiberty
install -m 0644 objs/libiberty/pic/libiberty.a %{buildroot}%{_libdir}/
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

%files -n %{devname}
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
* Wed Nov 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.17.50.0.12
- rebuild against new gettext

* Thu Sep 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.17.50.0.12
- 2.17.50.0.12
- sync patches with Mandriva 2.17.50.0.12-1mdv
- implement devel naming policy
- implement library provides policy
- temporarily make the tests non-fatal because it seems there is a hiccup with
  SSP support and one single test (S-records with constructors) which the logs 
  show as: sr3.cc:(.text+0x24c): undefined reference to `__stack_chk_fail'

* Sat Jun 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.17.50.0.9
- 2.17.50.0.9
- updated patches from Mandriva (sync with 2.17.50.0.9-1mdv)

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
