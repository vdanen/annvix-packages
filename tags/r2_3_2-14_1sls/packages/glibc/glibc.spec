# RH 2.2.4-20, SuSE 2.3.1-32
%define name		%{cross_prefix}glibc

# Define Mandrake Linux version we are building for
%define mdkversion	%(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandrake-release)

%{!?build_opensls:%global build_opensls 0}

# <version>-<release> tags for glibc main package
%define glibcversion	2.3.2
%define glibcrelease	14.1sls
# <version>-<release> tags from kernel package where headers were
# actually extracted from
%define kheaders_ver	2.4.22
%define kheaders_rel	0.3mdk
# Don't care about locales/* and pt_chown
%define _unpackaged_files_terminate_build 0
# Add errno compat hack for errata
%define build_errata	0

# CVS snapshots of glibc
%define RELEASE		0
%if %{RELEASE}
%define source_package	glibc-%{glibcversion}
%define source_dir	glibc-%{glibcversion}
%else
%define snapshot	20030704
%define source_package	glibc-%{glibcversion}-%{snapshot}
%define source_dir	glibc-%{glibcversion}
%endif

# Define "cross" to an architecture to which glibc is to be
# cross-compiled
%if %{?cross:1}%{!?cross:0}
%define target_cpu	%{cross}
%define cross_prefix	cross-%{target_cpu}-
%define _prefix		/usr/%{target_cpu}-linux
%define _slibdir	%{_libdir}
%define _ssbindir	%{_sbindir}
%else
%define target_cpu	%{_target_cpu}
%define cross_prefix	%{nil}
%define _slibdir	/%{_lib}
%define _ssbindir	/sbin
%endif

# Define target architecture
%define arch		%(echo %{target_cpu}|sed -e "s/i.86/i386/" -e "s/athlon/i386/" -e "s/amd64/x86_64/")

# Define prelinkarches
%define prelinkarches	%{nil}

# Flag for build_pdf_doc:
# 1	build glibc with PDF documentation
# 0	don't build PDF glibc documentation (e.g. for bootstrap build)
%define build_pdf_doc	1

# Enable checking by default for arches where we know tests all pass
%define build_check	1

# Define to build a biarch package
%define build_biarch	0
%ifarch x86_64
%define build_biarch	1
%endif

# Define to build glibc-debug package
%define build_debug	1
%if %{mdkversion} >= 920
%define _enable_debug_packages 1
%endif
%if "%{_enable_debug_packages}" == "1"
%define build_debug	0
%endif

# Define to bootstrap new glibc
%define build_bootstrap	0

%define build_profile	1
%define build_nscd	1
%define build_doc	1
%define build_utils	1
%define build_i18ndata	1
%define build_timezone	1

# Disable a few defaults when cross-compiling a glibc
%if "%{name}" != "glibc"
%define build_doc	0
%define build_pdf_doc	0
%define build_biarch	0
%define build_check	0
%define build_debug	0
%define build_nscd	0
%define build_profile	0
%define build_utils	0
%define build_i18ndata	0
%define build_timezone	0
%endif

# Allow --with[out] <feature> at rpm command line build
%{expand: %{?_without_PDF:	%%global build_pdf_doc 0}}
%{expand: %{?_without_CHECK:	%%global build_check 0}}
%{expand: %{?_without_UTILS:	%%global build_utils 0}}
%{expand: %{?_without_BOOTSTRAP:%%global build_bootstrap 0}}
%{expand: %{?_with_PDF:		%%global build_pdf_doc 1}}
%{expand: %{?_with_CHECK:	%%global build_check 1}}
%{expand: %{?_with_UTILS:	%%global build_utils 1}}
%{expand: %{?_with_BOOTSTRAP:	%%global build_bootstrap 1}}

Summary:	The GNU libc libraries
Name:		%{name}
Version:	%{glibcversion}
Release:	%{glibcrelease}
Epoch:		6
License:	LGPL
Group:		System/Libraries
Url:		http://www.gnu.org/software/glibc/

# Red Hat tarball
Source0:	%{source_package}.tar.bz2
Source1:	glibc-redhat.tar.bz2
Source2:	glibc-manpages.tar.bz2
Source3:	glibc-find-requires.sh

# Generated from Kernel-RPM
Source10:	kernel-headers-%{kheaders_ver}.%{kheaders_rel}.tar.bz2
Source11:	make_versionh.sh
Source12:	create_asm_headers.sh

# service --full-restart-all from initscripts 6.91-18mdk
Source13:	glibc-post-upgrade

Buildroot:	%{_tmppath}/glibc-%{PACKAGE_VERSION}-root
Obsoletes:	zoneinfo, libc-static, libc-devel, libc-profile, libc-headers,
Obsoletes: 	linuxthreads, gencat, locale, glibc-localedata
Provides:	glibc-localedata
Autoreq:	false
BuildRequires:	patch, gettext, perl
BuildRequires:	%{cross_prefix}binutils >= 2.13.90.0.18-2mdk
PreReq:         sash >= 3.4-6mdk /bin/sh
%if "%{name}" != "glibc"
ExclusiveArch:	%{ix86}
%endif
%ifarch %{prelinkarches}
BuildRequires:	prelink >= 0.2.0-16mdk
%endif
%if "%{name}" != "glibc"
BuildPreReq:	%{cross_prefix}gcc >= 3.2.2-4mdk
%endif
%ifarch %{ix86} alpha
BuildPreReq:	gcc >= 2.96-0.50mdk
%endif
%ifarch ia64
BuildPreReq:	gcc >= 3.2.3-1mdk
%endif
%ifarch x86_64
BuildPreReq:	gcc >= 3.1.1-0.5mdk
%endif
%ifarch alpha
Provides:	ld.so.2
%endif
%ifarch ppc
Provides:	ld.so.1
%endif
%ifarch sparc
Obsoletes:	libc
%endif

Conflicts:	rpm <= 4.0-0.65
Conflicts:	%{name}-devel < 2.2.3
# We need initscripts recent enough to not restart service dm
Conflicts:	initscripts < 6.91-18mdk

%if %{build_pdf_doc}
BuildRequires:	texinfo, tetex, tetex-latex
%endif
%if %{build_utils}
BuildRequires:	gd-devel
%endif

Patch0:		glibc-kernel-2.4.patch.bz2
Patch1:		glibc-2.2.2-fhs.patch.bz2
Patch2:		glibc-2.1.92-ldd-non-exec.patch.bz2
Patch3:		glibc-2.1.92-pthread_create-manpage.patch.bz2
Patch4:		glibc-2.1.95-string2-pointer-arith.patch.bz2
Patch5:		glibc-2.2-nss-upgrade.patch.bz2
Patch6:		glibc-2.2.5-ldconfig-exit-during-install.patch.bz2
Patch7:		glibc-2.2.5-share-locale.patch.bz2
Patch8:		glibc-2.2.3-samba-wins-hosts.patch.bz2
Patch9:		glibc-2.3.1-new-charsets.patch.bz2
Patch10:	glibc-2.2.4-xterm-xvt.patch.bz2
Patch11:	glibc-2.2.4-hack-includes.patch.bz2
Patch12:	glibc-2.2.5-compat-EUR-currencies.patch.bz2
Patch13:	glibc-2.2.5-ppc-build-lddlibc4-ld-linux.patch.bz2
# ThizLinux version for correct gb18030 support
Patch14:	glibc-2.2.5-gb18030-updates.patch.bz2
Patch15:	glibc-2.3.1-glibc22-compat.patch.bz2
Patch16:	glibc-2.2.5-hwcap-check-platform.patch.bz2
# http://sources.redhat.com/ml/libc-hacker/2001-01/msg00004.html
Patch17:	glibc-2.3.1-setlocale-ibm-jdk-compat.patch.bz2
Patch18:	glibc-2.3.1-i586-hptiming.patch.bz2
Patch19:	glibc-2.3.1-i386-fix-hwcaps.patch.bz2
Patch20:	glibc-2.3.2-config-amd64-alias.patch.bz2
Patch21:	glibc-2.2.5-nscd-no-host-cache.patch.bz2
Patch22:	glibc-2.3.1-quota.patch.bz2
Patch23:	glibc-2.3.1-x86_64-fpu_control.patch.bz2
Patch24:	glibc-2.3.1-x86_64-new-libm.patch.bz2
Patch25:	glibc-2.3.2-nscd-fixes.patch.bz2
Patch26:	glibc-2.3.1-nscd-HUP.patch.bz2
Patch27:	glibc-2.3.1-errno-compat.patch.bz2
Patch28:	glibc-2.3.2-tcsetattr-kernel-bug-workaround.patch.bz2
Patch29:	glibc-2.3.2-timezone.patch.bz2
Patch30:	glibc-2.3.2-libm-ulps.patch.bz2
Patch31:	glibc-2.3.2-sse-fixes.patch.bz2
Patch32:	glibc-2.3.2-rtld32-workaround.patch.bz2
Patch33:	glibc-2.3.2-amd64-ldconfig.patch.bz2
Patch34:	glibc-2.3.2-wcsmbs.patch.bz2
Patch35:	glibc-2.3.2-libio-compat.patch.bz2
Patch36:	glibc-2.3.2-_res-compat.patch.bz2
Patch37:	glibc-2.3.2-aliasing-fixes.patch.bz2
Patch38:	glibc-2.3.2-dlerror-fix.patch.bz2
Patch39:	glibc-2.3.2-iofwide.patch.bz2
Patch40:	glibc-2.3.2-i586-if-no-cmov.patch.bz2
Patch41:	glibc-2.3.2-propolice.patch.bz2

# Generated from Kernel RPM
Patch100:	kernel-headers-include-%{kheaders_ver}.%{kheaders_rel}.patch.bz2
Patch101:	kernel-headers-gnu-extensions.patch.bz2

# Determine minium kernel versions
%ifarch ia64 x86_64
Conflicts:		kernel < 2.4.0
%define enablemask	[01].*|2.[0-3]*
%else
%ifarch %{ix86}
%define enablemask	[01].*|2.[0-3]*|2.4.0*
%else
%define enablemask	[01].*|2.[0-1]*|2.2.[0-4]|2.2.[0-4][^0-9]*
%endif
%endif

# Don't try to explicitly provide GLIBC_PRIVATE versioned libraries
%define __find_provides	%{_builddir}/%{source_dir}/find_provides.sh
%define __find_requires %{_builddir}/%{source_dir}/find_requires.sh

Obsoletes:	ld.so
Provides:	ld.so

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.  The glibc package also contains
national language (locale) support.

%package -n ldconfig
Summary:	Creates a shared library cache and maintains symlinks for ld.so
Group:		System/Base

%description -n ldconfig
Ldconfig is a basic system program which determines run-time link
bindings between ld.so and shared libraries. Ldconfig scans a running
system and sets up the symbolic links that are used to load shared
libraries properly. It also creates a cache (/etc/ld.so.cache) which
speeds the loading of programs which use shared libraries.

%package devel
Summary:	Header and object files for development using standard C libraries
Group:		Development/C
Conflicts:	texinfo < 3.11
Prereq:		/sbin/install-info
Obsoletes:	libc-debug, libc-headers, libc-devel, linuxthreads-devel
%if !%{build_debug}
Obsoletes:	glibc-debug
%endif
Requires:	%{name} = %{glibcversion}-%{glibcrelease}
Obsoletes:	kernel-headers
Provides:	kernel-headers = 1:%{kheaders_ver}
%ifnarch ppc
Conflicts:	gcc < 2.96-0.50mdk
%endif
Autoreq:	true

%description devel
The glibc-devel package contains the header and object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header and object files available in order to create the
executables.

This package also includes the C header files for the Linux kernel.
The header files define structures and constants that are needed for
building most standard programs. The header files are also needed for
rebuilding the kernel.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

%package static-devel
Summary:	Static libraries for GNU C library
Group:		Development/C
Requires:	%{name}-devel = %{glibcversion}-%{glibcrelease}

%description static-devel
The glibc-static-devel package contains the static libraries necessary
for developing programs which use the standard C libraries. Install
glibc-static-devel if you need to statically link your program or
library.

%package profile
Summary:	The GNU libc libraries, including support for gprof profiling
Group:		Development/C
Obsoletes:	libc-profile
Provides:	libc-profile = %{glibcversion}-%{glibcrelease}
Autoreq:	true

%description profile
The glibc-profile package includes the GNU libc libraries and support
for profiling using the gprof program.  Profiling is analyzing a
program's functions to see how much CPU time they use and determining
which functions are calling other functions during execution.  To use
gprof to profile a program, your program needs to use the GNU libc
libraries included in glibc-profile (instead of the standard GNU libc
libraries included in the glibc package).

If you are going to use the gprof program to profile a program, you'll
need to install the glibc-profile program.

%package -n nscd
Summary:	A Name Service Caching Daemon (nscd)
Group:		System/Servers
Conflicts:	kernel < 2.2.0
PreReq:		/sbin/chkconfig
PreReq:		rpm-helper
Autoreq:	true

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS+, and may help with DNS as well. Note that you
can't use nscd with 2.0 kernels because of bugs in the kernel-side
thread support. Unfortunately, nscd happens to hit these bugs
particularly hard.

Install nscd if you need a name service lookup caching daemon, and
you're not using a version 2.0 kernel.

%if %{build_debug}
%package debug
Summary: Shared standard C libraries with debugging information
Group: System/Libraries
Requires: %{name} = %{glibcversion}-%{glibcrelease}
Autoreq: false

%description debug
The glibc-debug package contains shared standard C libraries with
debugging information. You need this only if you want to step into C
library routines during debugging.

To use these libraries, you need to add %{_libdir}/debug to your
LD_LIBRARY_PATH variable prior to starting the debugger.
%endif

%package utils
Summary:	Development utilities from GNU C library
Group:		Development/Other
Requires:	%{name} = %{glibcversion}-%{glibcrelease}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer which
can be helpful during program debugging.

If unsure if you need this, don't install this package.

%package i18ndata
Summary:	Database sources for 'locale'
Group:		System/Libraries

%description i18ndata
This package contains the data needed to build the locale data files
to use the internationalization features of the GNU libc.

%package -n timezone
Summary:	Time zone descriptions
Group:		System/Base
Conflicts:	glibc < 2.2.5-6mdk

%description -n timezone
These are configuration files that describe possible
time zones.

%package doc
Summary:	GNU C library documentation
Group:		Development/Other

%description doc
The glibc-doc package contains documentation for the GNU C library in
info format.

%if %{build_pdf_doc}
%package doc-pdf
Summary:	GNU C library documentation
Group:		Development/Other

%description doc-pdf
The glibc-doc-pdf package contains the printable documentation for the
GNU C library in PDF format.
%endif

%prep
%setup -q -n %{source_dir} -a 10 -a 2 -a 1
%patch1 -p1 -b .fhs
%patch2 -p1 -b .ldd-non-exec
%patch3 -p1 -b .pthread_create-manpage
%patch4 -p1 -b .string2-pointer-arith
%patch5 -p1 -b .nss-upgrade
%patch6 -p1 -b .ldconfig-exit-during-install
%patch7 -p1 -b .share-locale
%patch8 -p1 -b .samba-wins-hosts
%patch9 -p1 -b .new-charsets
%patch10 -p1 -b .xterm-xvt
%patch11 -p1 -b .hack-includes
%patch12 -p1 -b .compat-EUR-currencies
%patch13 -p1 -b .ppc-build
#%patch14 -p1 -b .gb18030-updates
%patch15 -p1 -b .glibc22-compat
%patch16 -p1 -b .hwcap-check-platform
%patch17 -p1 -b .setlocale-ibm-jdk-compat
%patch18 -p1 -b .i586-hptiming
%patch19 -p1 -b .i386-fix-hwcaps
%patch20 -p1 -b .config-amd64-alias
%patch21 -p1 -b .nscd-no-host-cache
%patch22 -p1 -b .quota
%patch23 -p1 -b .x86_64-fpu_control
%patch24 -p1 -b .x86_64-new-libm -E
%patch25 -p1 -b .nscd-fixes
%patch26 -p1 -b .nscd-HUP
%if %{build_errata}
%patch27 -p1 -b .errno-compat
%endif
%patch28 -p1 -b .tcsetattr-kernel-bug-workaround
%patch29 -p1 -b .timezone
%patch30 -p1 -b .libm-ulps
%patch31 -p1 -b .sse-fixes
%patch32 -p1 -b .rtld32-workaround
%patch33 -p1 -b .amd64-ldconfig
%patch34 -p1 -b .wcsmbs
%patch35 -p1 -b .libio-compat
%patch36 -p1 -b ._res-compat
%patch37 -p1 -b .aliasing-fixes
%patch38 -p1 -b .dlerror-fix
%patch39 -p1 -b .iofwide
%patch40 -p1 -b .i586-if-no-cmov
%if %build_opensls
%patch41 -p1 -b .propolice
%endif

# If we are building enablekernel 2.x.y glibc on older kernel,
# we have to make sure no binaries compiled against that glibc
# are ever run
case `uname -r` in
%enablemask)
%patch0 -p1
;; esac

%ifarch armv4l
rm -rf glibc-compat
%endif

pushd kernel-headers/
TARGET=%{target_cpu}
%patch100 -p1
%patch101 -p1
%{expand:%(%__cat %{SOURCE11})}
%{expand:%(%__cat %{SOURCE12})}
popd

find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

cat > find_provides.sh << EOF
#!/bin/sh
/usr/lib/rpm/find-provides | grep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_provides.sh

cat > find_requires.sh << EOF
%if %{build_bootstrap}
exec /bin/sh %{SOURCE3} %{buildroot} %{_target_cpu}
%else
/usr/lib/rpm/find-requires %{buildroot} %{_target_cpu} | grep -v GLIBC_PRIVATE
exit 0
%endif
EOF
chmod +x find_requires.sh

%build
#
# BuildGlibc <arch> [<extra_configure_options>+]
#
function BuildGlibc() {
  arch="$1"
  shift 1

  # Select minimal kernel version
  case $arch in
    ia64 | x86_64 | amd64)
      EnableKernel=2.4.0
      ;;
    i686 | athlon)
      EnableKernel=2.4.1
      ;;
    *)
      EnableKernel=2.2.5
      ;;
  esac

  # Select optimization flags and compiler to use
  BuildCC="gcc"
  case $arch in
    i[3456]86 | athlon)
      BuildFlags="-march=$arch"
      if [[ "`uname -m`" = "x86_64" ]]; then
        BuildCC="$BuildCC -m32"
      fi
      ;;
    alphaev6)
      BuildFlags="-mcpu=ev6"
      ;;
    sparc)
      BuildFlags="-fcall-used-g6"
      BuildCC="gcc -m32"
      ;;
    sparcv9)
      BuildFlags="-mcpu=ultrasparc -fcall-used-g6"
      BuildCC="gcc -m32"
      ;;
    sparc64)
      BuildFlags="-mcpu=ultrasparc -mvis -fcall-used-g6"
      BuildCC="gcc -m64"
      ;;
  esac
  # Temporarily don't do this on ia64, s390 and ppc
  case $arch in
    ia64 | s390 | s390x | ppc)
      ;;
    * )
      BuildFlags="$BuildFlags -freorder-blocks"
      ;;
  esac

  # Are we supposed to cross-compile?
  if [[ "%{target_cpu}" != "%{_target_cpu}" ]]; then
    BuildCC="%{target_cpu}-linux-$BuildCC"
    BuildCross="--build=%{_target_platform}"
  fi

  BuildFlags="$BuildFlags -DNDEBUG=1 -O2 -finline-functions -g"
  if $BuildCC -v 2>&1 | grep -q 'gcc version 3.0'; then
    # gcc3.0 had really poor inlining heuristics causing problems in
    # resulting ld.so
    BuildFlags="$BuildFlags -finline-limit=2000"
  fi

  # FIXME: m68k code has functions that should be __attribute__((used))
  if [[ "$arch" = "m68k" ]]; then
    BuildFlags="$BuildFlags -O2"
  fi

  # FIXME: don't use unit at time compilation
  if $BuildCC -funit-at-a-time -S -o /dev/null -xc /dev/null 2>&1; then
    BuildFlags="$BuildFlags -fno-unit-at-a-time"
  fi

  if [[ "%{build_profile}" = "0" ]]; then
    ExtraFlags="$ExtraFlags --disable-profile"
  fi

  # Kernel headers directory
  KernelHeaders=$PWD/kernel-headers

  # Determine library name
  glibc_cv_cc_64bit_output=no
  if echo ".text" | $BuildCC -c -o test.o -xassembler -; then
    case `/usr/bin/file test.o` in
    *"ELF 64"*)
      glibc_cv_cc_64bit_output=yes
      ;;
    esac
  fi
  rm -f test.o

  case $arch:$glibc_cv_cc_64bit_output in
  powerpc64:yes | s390x:yes | sparc64:yes | x86_64:yes | amd64:yes)
    glibc_libname="lib64"
    ;;
  *:*)
    glibc_libname="lib"
    ;;
  esac

  # Force a separate and clean object dir
  rm -rf build-$arch-linux
  mkdir  build-$arch-linux
  pushd  build-$arch-linux
  CC="$BuildCC" CFLAGS="$BuildFlags" ../configure \
    $arch-mandrake-linux-gnu $BuildCross \
    --prefix=%{_prefix} \
    --libexecdir="%{_prefix}/$glibc_libname" \
    --infodir=%{_infodir} \
    --enable-add-ons=yes --without-cvs \
    --without-tls --without-__thread $ExtraFlags \
    --enable-kernel=$EnableKernel --with-headers=$KernelHeaders ${1+"$@"}
%if %build_opensls
  %make -r CFLAGS="$BuildFlags" PARALLELMFLAGS=
%else
  %make -r CFLAGS="$BuildFlags" PARALLELMFLAGS=-s
%endif
  popd
}

# Build main glibc
BuildGlibc %{target_cpu}

%if %{build_biarch}
# Build i586 libraries, and preserve maximum compatibility
%ifarch x86_64
BuildGlibc i586
%endif
%endif

# Build i686 libraries if not already building for i686/athlon
case %{target_cpu} in
  i686 | athlon)
    ;;
  i[3-6]86)
    BuildGlibc i686 --disable-profile
    ;;
esac

BUILD_CHECK=
%if %{build_check}
BUILD_CHECK=yes
%endif
if [[ -n "$BUILD_CHECK" ]]; then
echo ====================TESTING=========================
# All tests must pass on x86, x86-64, ia64 and ppc
%ifarch %{ix86} x86_64 ia64 ppc
%make -C build-%{_target_cpu}-linux check PARALLELMFLAGS=-s
case `uname -m` in
  i686 | athlon) ALT_ARCH=i686;;
  x86_64)        ALT_ARCH=i586;;
esac
[[ -n "$ALT_ARCH" && -d "build-$ALT_ARCH-linux" ]] &&
%make -C build-$ALT_ARCH-linux check PARALLELMFLAGS=-s
%else
%make -C build-%{_target_cpu}-linux -k check PARALLELMFLAGS=-s \
|| echo make check failed
%endif
echo ====================TESTING END=====================
fi

%install
rm -rf $RPM_BUILD_ROOT

make install_root=$RPM_BUILD_ROOT install -C build-%{target_cpu}-linux
%if %{build_i18ndata}
(cd build-%{target_cpu}-linux; %make install_root=$RPM_BUILD_ROOT install-locales -C ../localedata objdir=`pwd`)
%endif
sh manpages/Script.sh

# Empty filelist for non i686/athlon targets
> optarch.filelist

# Install biarch libraries
%if %{build_biarch}
%ifarch x86_64
ALT_ARCH=i586-linux
%endif
mkdir -p $RPM_BUILD_ROOT/$ALT_ARCH
make install_root=$RPM_BUILD_ROOT/$ALT_ARCH install -C build-$ALT_ARCH
(cd build-$ALT_ARCH;
  %make -C ../localedata objdir=`pwd` \
	install_root=$RPM_BUILD_ROOT/$ALT_ARCH \
	install-locales
)
# Dispatch */lib only
mv $RPM_BUILD_ROOT/$ALT_ARCH/lib $RPM_BUILD_ROOT/
mv $RPM_BUILD_ROOT/$ALT_ARCH%{_prefix}/lib $RPM_BUILD_ROOT%{_prefix}/
rm -rf $RPM_BUILD_ROOT/$ALT_ARCH
%endif

# Install arch-specific optimized libraries
%ifarch %{ix86}
case %{target_cpu} in
i[3-5]86) SubDir=i686;;
esac

[[ -n "$SubDir" ]] && {
pushd build-i686-linux
  mkdir -p $RPM_BUILD_ROOT%{_slibdir}/$SubDir/
  cp -a libc.so $RPM_BUILD_ROOT%{_slibdir}/$SubDir/`basename $RPM_BUILD_ROOT%{_slibdir}/libc-*.so`
  ln -sf `basename $RPM_BUILD_ROOT%{_slibdir}/libc-*.so` $RPM_BUILD_ROOT%{_slibdir}/$SubDir/`basename $RPM_BUILD_ROOT%{_slibdir}/libc.so.*`
  cp -a math/libm.so $RPM_BUILD_ROOT%{_slibdir}/$SubDir/`basename $RPM_BUILD_ROOT%{_slibdir}/libm-*.so`
  ln -sf `basename $RPM_BUILD_ROOT%{_slibdir}/libm-*.so` $RPM_BUILD_ROOT%{_slibdir}/$SubDir/`basename $RPM_BUILD_ROOT%{_slibdir}/libm.so.*`
  cp -a linuxthreads/libpthread.so $RPM_BUILD_ROOT%{_slibdir}/$SubDir/`basename $RPM_BUILD_ROOT%{_slibdir}/libpthread-*.so`
  ln -sf `basename $RPM_BUILD_ROOT%{_slibdir}/libpthread-*.so` $RPM_BUILD_ROOT%{_slibdir}/$SubDir/`basename $RPM_BUILD_ROOT%{_slibdir}/libpthread.so.*`
  cp -a linuxthreads_db/libthread_db.so $RPM_BUILD_ROOT%{_slibdir}/$SubDir/`basename $RPM_BUILD_ROOT%{_slibdir}/libthread_db-*.so`
  ln -sf `basename $RPM_BUILD_ROOT%{_slibdir}/libthread_db-*.so` $RPM_BUILD_ROOT%{_slibdir}/$SubDir/`basename $RPM_BUILD_ROOT%{_slibdir}/libthread_db.so.*`
  cp -a rt/librt.so $RPM_BUILD_ROOT%{_slibdir}/$SubDir/`basename $RPM_BUILD_ROOT%{_slibdir}/librt-*.so`
  ln -sf `basename $RPM_BUILD_ROOT%{_slibdir}/librt-*.so` $RPM_BUILD_ROOT%{_slibdir}/$SubDir/`basename $RPM_BUILD_ROOT%{_slibdir}/librt.so.*`
  echo "%dir %{_slibdir}/$SubDir" >> ../optarch.filelist
  find $RPM_BUILD_ROOT%{_slibdir}/$SubDir -type f -o -type l | sed -e "s|$RPM_BUILD_ROOT||" >> ../optarch.filelist
popd
}
%endif

# Compatibility hack: this locale has vanished from glibc, but some other
# programs are still using it. Normally we would handle it in the %pre
# section but with glibc that is simply not an option
mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/ru_RU/LC_MESSAGES

# If librt.so is a symlink, change it into linker script
if [ -L $RPM_BUILD_ROOT%{_libdir}/librt.so ]; then
  rm -f $RPM_BUILD_ROOT%{_libdir}/librt.so
  LIBRTSO=`cd $RPM_BUILD_ROOT%{_slibdir}; echo librt.so.*`
  LIBPTHREADSO=`cd $RPM_BUILD_ROOT%{_slibdir}; echo libpthread.so.*`
  cat > $RPM_BUILD_ROOT%{_libdir}/librt.so <<EOF
/* GNU ld script
   librt.so.1 needs libpthread.so.0 to come before libc.so.6*
   in search scope.  */
GROUP ( %{_slibdir}/$LIBPTHREADSO %{_slibdir}/$LIBRTSO )
EOF
fi

# Remove the files we don't want to distribute
rm -f $RPM_BUILD_ROOT%{_libdir}/libNoVersion*
case %{arch} in
  sparc64 | ia64 | s390 | s390x )
    rm -f $RPM_BUILD_ROOT%{_slibdir}/libNoVersion*
    ;;
esac

# The man pages for the linuxthreads require special attention
make -C linuxthreads/man
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
install -m 0644 linuxthreads/man/*.3thr $RPM_BUILD_ROOT%{_mandir}/man3

ln -sf libbsd-compat.a $RPM_BUILD_ROOT%{_libdir}/libbsd.a
%if %{build_biarch}
ln -sf libbsd-compat.a $RPM_BUILD_ROOT%{_prefix}/lib/libbsd.a
%endif

%if "%{name}" == "glibc"
install -m 644 redhat/nsswitch.conf $RPM_BUILD_ROOT%{_sysconfdir}/nsswitch.conf
%endif

# Take care of setuids
# -- new security review sez that this shouldn't be needed anymore
#chmod 755 $RPM_BUILD_ROOT%{_libdir}/pt_chown

# This is for ncsd - in glibc 2.2
%if %{build_nscd}
install -m 644 nscd/nscd.conf $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m 755 nscd/nscd.init $RPM_BUILD_ROOT%{_initrddir}/nscd
%endif

# Useless and takes place
rm -rf %buildroot/%{_datadir}/zoneinfo/{posix,right}

# Don't include ld.so.cache
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.cache

# Include ld.so.conf
%if "%{name}" == "glibc"
> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
%endif

# Include %{_libdir}/gconv/gconv-modules.cache
> $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache
chmod 644 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache

# Add libraries to debug sub-package
%if %{build_debug}
mkdir $RPM_BUILD_ROOT%{_libdir}/debug
#cp -a $RPM_BUILD_ROOT%{_libdir}/*.a $RPM_BUILD_ROOT%{_libdir}/debug/
#rm -f $RPM_BUILD_ROOT%{_libdir}/debug/*_p.a
cp -a $RPM_BUILD_ROOT%{_slibdir}/lib*.so* $RPM_BUILD_ROOT%{_libdir}/debug/

pushd $RPM_BUILD_ROOT%{_libdir}/debug
for lib in *.so*; do
  [[ -f "$lib" ]] && DEBUG_LIBS="$DEBUG_LIBS %{_libdir}/debug/$lib"
done
popd
%endif

# Are we cross-compiling?
Strip="strip"
if [[ "%{_target_cpu}" != "%{target_cpu}" ]]; then
  Strip="%{target_cpu}-linux-$Strip"
fi

# Strip libpthread but keep some symbols
find $RPM_BUILD_ROOT%{_slibdir} -type f -name "libpthread-*.so" | \
     xargs $Strip -g -R .comment

%if %{build_biarch}
find $RPM_BUILD_ROOT/lib -type f -name "libpthread-*.so" | \
     xargs $Strip -g -R .comment
%endif

# Strip debugging info from all static libraries
pushd $RPM_BUILD_ROOT%{_libdir}
for i in *.a; do
  if [ -f "$i" ]; then
    case "$i" in
    *_p.a) ;;
    *) $Strip -g -R .comment $i ;;
    esac
  fi
done
popd

%ifarch %{prelinkarches}
# Prelink libc.so on supported arches
%ifarch %{ix86}
[[ -n "$SubDir" ]] && {
/usr/sbin/prelink --reloc-only=0x42000000 $RPM_BUILD_ROOT%{_slibdir}/$SubDir/libc-*.so
}
%endif
%endif

# post upgrade script
install -m 700 %{SOURCE13} $RPM_BUILD_ROOT%{_sbindir}/glibc-post-upgrade

# rquota.x and rquota.h are now provided by quota
rm -f $RPM_BUILD_ROOT%{_includedir}/rpcsvc/rquota.[hx]

# Hardlink identical locale files together
%if %{build_i18ndata}
gcc -O2 -o build-%{_target_cpu}-linux/hardlink redhat/hardlink.c
build-%{_target_cpu}-linux/hardlink -vc $RPM_BUILD_ROOT%{_datadir}/locale
%endif

rm -rf $RPM_BUILD_ROOT%{_includedir}/netatalk/

# (sb) PPC - built with ld-linux.so.2, but you get
# a nasty unusable system without retaining ld.so.1
%if "%{arch}" == "ppc"
pushd $RPM_BUILD_ROOT%{_slibdir}
ln -s ld-%{glibcversion}.so ld.so.1
popd
%endif

# Build file list for devel package
find $RPM_BUILD_ROOT%{_includedir} -type f -or -type l > devel.filelist
find $RPM_BUILD_ROOT%{_includedir} -type d  | sed "s/^/%dir /" | grep -v "%{_includedir}$" >> devel.filelist
find $RPM_BUILD_ROOT%{_libdir} -name "*.so" -o -name "*.o" -maxdepth 1 | egrep -v "(libmemusage.so|libpcprofile.so)" >> devel.filelist
# biarch libs
%if %{build_biarch}
find $RPM_BUILD_ROOT%{_prefix}/lib -name "*.so" -o -name "*.o" -maxdepth 1 | egrep -v "(libmemusage.so|libpcprofile.so)" >> devel.filelist
%endif
perl -pi -e "s|$RPM_BUILD_ROOT||" devel.filelist

%if %{build_utils}
if [[ "%{_slibdir}" != "%{_libdir}" ]]; then
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT%{_slibdir}/lib{pcprofile,memusage}.so $RPM_BUILD_ROOT%{_libdir}
for i in $RPM_BUILD_ROOT%{_prefix}/bin/{xtrace,memusage}; do
  cp -a $i $i.tmp
  sed -e 's~=%{_slibdir}/libpcprofile.so~=%{_libdir}/libpcprofile.so~' \
      -e 's~=%{_slibdir}/libmemusage.so~=%{_libdir}/libmemusage.so~' \
    $i.tmp > $i
  chmod 755 $i; rm -f $i.tmp
done
fi
%endif

# /etc/localtime - we're proud of our timezone #Well we(mdk) may put Paris
%if %{build_timezone}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/localtime
cp -f $RPM_BUILD_ROOT%{_datadir}/zoneinfo/US/Eastern $RPM_BUILD_ROOT%{_sysconfdir}/localtime
#ln -sf ..%{_datadir}/zoneinfo/US/Eastern $RPM_BUILD_ROOT%{_sysconfdir}/localtime
%endif

# [gg] build PDF documentation
%if %{build_pdf_doc}
(cd manual; texi2dvi -p -t @afourpaper -t @finalout libc.texinfo)
%endif

# Copy Kernel-Headers
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT/boot/
cp -avrf kernel-headers/* $RPM_BUILD_ROOT%{_includedir}
echo "#if 0" > $RPM_BUILD_ROOT/boot/kernel.h-%{kheaders_ver}

# the last bit: more documentation
rm -rf documentation
mkdir documentation
cp linuxthreads/ChangeLog  documentation/ChangeLog.threads
cp linuxthreads/Changes documentation/Changes.threads
cp linuxthreads/README documentation/README.threads
cp linuxthreads/FAQ.html documentation/FAQ-threads.html
cp -r linuxthreads/Examples documentation/examples.threads
cp crypt/README.ufc-crypt documentation/README.ufc-crypt
cp timezone/README documentation/README.timezone
cp ChangeLog* documentation
gzip -9 documentation/ChangeLog*

%find_lang libc

# In case we are cross-compiling, don't bother to remake symlinks and
# fool spec-helper when stripping files
%if "%{name}" != "glibc"
export DONT_SYMLINK_LIBS=1
export PATH=%{_bindir}:$PATH
%endif

EXCLUDE_FROM_STRIP="ld-%{glibcversion}.so libpthread $DEBUG_LIBS"
export EXCLUDE_FROM_STRIP

%if "%{name}" == "glibc"
%define upgradestamp %{_slibdir}/glibc.upgraded
%define broken_link %{_slibdir}/libnss_nis.so.1 %{_slibdir}/libnss_files.so.1 %{_slibdir}/libnss_dns.so.1 %{_slibdir}/libnss_compat.so.1

%pre -p /sbin/sash
if [ ! -f %{_slibdir}/libnss_files-%{glibcversion}.so ]; then echo > %{upgradestamp}; fi
%ifarch ppc
# FIXME: Get around intermediate breakage on upgrade
if [ -f %{_slibdir}/ld-2.2.4.so ]; then cp %{_slibdir}/ld-2.2.4.so %{_libdir};ln -s %{_libdir}/ld-2.2.4.so %{_libdir}/ld-linux.so.2; ln -sf %{_libdir}/ld-2.2.4.so %{_slibdir}/ld-linux.so.2; fi
%endif

%post
/sbin/ldconfig

%ifarch ppc
# FIXME: Get around intermediate breakage on upgrade
if [ -f %{_libdir}/ld-2.2.4.so ]; then
cat > /tmp/ppc-glibc-update.sh <<EOF
-rm %{_slibdir}/ld-linux.so.2
-ln -s %{_slibdir}/ld-2.2.5.so %{_slibdir}/ld-linux.so.2
-rm %{_libdir}/ld-2.2.4.so
-rm %{_libdir}/ld-linux.so.2
EOF
/sbin/sash /tmp/ppc-glibc-update.sh
rm -f /tmp/ppc-glibc-update.sh
fi
%endif

if [ "$1" -ge 1 ]; then
  # On upgrade the services doesn't work because libnss couldn't be
  # loaded anymore.
    if [ -f %{upgradestamp} ]; then
	# if X is running define the fontpath to something xfs-independent
	[[ -n "$DISPLAY" ]] && xset fp= /usr/X11R6/lib/X11/fonts/misc
	echo "Restarting all the services of this run level"
	%{_sbindir}/glibc-post-upgrade
	# if X is running, reset the fontpath to its default value
	[[ -n "$DISPLAY" ]] && xset fp default        
    fi
    if [ -f /bin/rm ]; then
      for i in %broken_link; do
        if [ -e $i ] && [ ! -L $i ]; then
          /bin/rm -f $i
	fi
      done
    fi
fi

rm -f %{upgradestamp}

%postun -p /sbin/ldconfig
%endif

%pre devel
if [ -L %{_includedir}/scsi ]; then
  rm -f %{_includedir}/scsi
fi
if [ -L %{_includedir}/sound ]; then
  rm -f %{_includedir}/sound
fi
if [ -L %{_includedir}/linux ]; then
  rm -f %{_includedir}/linux
fi
if [ -L %{_includedir}/asm ]; then
  rm -f %{_includedir}/asm
fi
if [ -L %{_includedir}/asm-generic ]; then
  rm -f %{_includedir}/asm-generic
fi
%ifarch x86_64
if [ -L %{_includedir}/asm-x86_64 ]; then
  rm -f %{_includedir}/asm-x86_64
fi
if [ -L %{_includedir}/asm-i386 ]; then
  rm -f %{_includedir}/asm-i386
fi
%endif
exit 0

%if "%{name}" == "glibc"
%post devel
cd /boot
rm -f kernel.h
ln -snf kernel.h-%{kheaders_ver} kernel.h
/sbin/service kheader start 2>/dev/null >/dev/null || :
exit 0

%postun devel
if [ $1 = 0 ];then
  if [ -L /boot/kernel.h -a `ls -l /boot/kernel.h 2>/dev/null| awk '{ print $11 }'` = "kernel.h-%{kheader}" ]; then
    rm -f /boot/kernel.h
  fi
fi
exit 0
%endif

%if %{build_doc}
%post doc
%_install_info libc.info

%preun doc
%_remove_install_info libc.info
%endif

%if %{build_utils}
%post utils -p /sbin/ldconfig
%postun utils -p /sbin/ldconfig
%endif

%if %{build_nscd}
%pre -n nscd
%_pre_useradd nscd / /bin/false

%post -n nscd
/sbin/chkconfig --add nscd

%preun -n nscd
if [ $1 = 0 ] ; then
  /sbin/chkconfig --del nscd
fi

%postun -n nscd
%_postun_userdel nscd

if [ "$1" -ge "1" ]; then
  /sbin/service nscd condrestart > /dev/null 2>&1 || :
fi
%endif

%clean
#rm -rf "$RPM_BUILD_ROOT"
#rm -f *.filelist*

#
# glibc
#
%files -f libc.lang -f optarch.filelist
%defattr(-,root,root)
%if "%{name}" == "glibc"
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/localtime
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/ld.so.conf
%config(noreplace) %{_sysconfdir}/rpc
%{_mandir}/man1/*
%{_mandir}/man8/rpcinfo.8*
%{_mandir}/man8/ld.so*
%{_datadir}/locale/locale.alias
/sbin/sln
%endif
%{_slibdir}/ld-%{glibcversion}.so
%if "%{arch}" == "i386"
%{_slibdir}/ld-linux.so.2
%endif
%if "%{arch}" == "alpha"
%{_slibdir}/ld-linux.so.2
%endif
%if "%{arch}" == "ppc"
%{_slibdir}/ld-linux.so.2
%{_slibdir}/ld.so.1
%endif
%if "%{arch}" == "ia64"
%{_slibdir}/ld-linux-ia64.so.2
%endif
%if "%{arch}" == "x86_64"
%{_slibdir}/ld-linux-x86-64.so.2
%endif
%if "%{arch}" == "m68k"
%{_slibdir}/ld.so.1
%endif
%{_slibdir}/lib*-[.0-9]*.so
%{_slibdir}/lib*.so.[0-9]*
%{_slibdir}/libSegFault.so
%dir %{_libdir}/gconv
%{_libdir}/gconv/*
# Don't package pt_chown. It is only needed if devpts is not used. But
# since we are running kernel 2.4+, that's fine without.
# (and it never actually worked, aka was not setuid, nor executable)
#%{_libdir}/pt_chown
%{_bindir}/catchsegv
%{_bindir}/gencat
%{_bindir}/getconf
%{_bindir}/getent
%{_bindir}/glibcbug
%{_bindir}/iconv
%{_bindir}/ldd
%if "%{arch}" == "i386"
%{_bindir}/lddlibc4
%endif
%{_bindir}/locale
%{_bindir}/localedef
%{_bindir}/rpcgen
%{_bindir}/sprof
%{_bindir}/tzselect
%{_sbindir}/rpcinfo
%{_sbindir}/iconvconfig
%{_sbindir}/glibc-post-upgrade

%if %{build_biarch}
/lib/ld-%{glibcversion}.so
/lib/ld-linux*.so.2
/lib/lib*-[.0-9]*.so
/lib/lib*.so.[0-9]*
/lib/libSegFault.so
%dir %{_prefix}/lib/gconv
%{_prefix}/lib/gconv/*
%endif

#
# ldconfig
#
%if "%{name}" == "glibc"
%files -n ldconfig
%defattr(-,root,root)
/sbin/ldconfig
%{_mandir}/man8/ldconfig*
%endif

#
# glibc-devel
#
%files devel -f devel.filelist
%defattr(-,root,root)
%doc README NEWS INSTALL FAQ BUGS NOTES PROJECTS CONFORMANCE
%doc COPYING COPYING.LIB
%doc documentation/* README.libm
%doc hesiod/README.hesiod
%if "%{name}" == "glibc"
%{_mandir}/man3/*
%endif
%{_libdir}/libbsd-compat.a
%{_libdir}/libbsd.a
%{_libdir}/libc_nonshared.a
%{_libdir}/libg.a
%{_libdir}/libieee.a
%{_libdir}/libmcheck.a
%{_libdir}/libpthread_nonshared.a
%if "%{name}" == "glibc"
%{_libdir}/librpcsvc.a
%endif

%{_includedir}/linux
%{_includedir}/asm
%{_includedir}/asm-generic
%{_includedir}/sound
%if "%{arch}" == "x86_64"
%dir %{_includedir}/asm-i386
%{_includedir}/asm-i386/*.h
%dir %{_includedir}/asm-x86_64
%{_includedir}/asm-x86_64/*.h
%endif
%if "%{name}" == "glibc"
/boot/kernel.h-%{kheaders_ver}
%endif

%if %{build_biarch}
%{_prefix}/lib/libbsd-compat.a
%{_prefix}/lib/libbsd.a
%{_prefix}/lib/libc_nonshared.a
%{_prefix}/lib/libg.a
%{_prefix}/lib/libieee.a
%{_prefix}/lib/libmcheck.a
%{_prefix}/lib/libpthread_nonshared.a
%{_prefix}/lib/librpcsvc.a
%endif

#
# glibc-static-devel
#
%files static-devel
%defattr(-,root,root)
%doc COPYING COPYING.LIB
%{_libdir}/libBrokenLocale.a
%{_libdir}/libanl.a
%{_libdir}/libc.a
%{_libdir}/libcrypt.a
%{_libdir}/libdl.a
%{_libdir}/libm.a
%{_libdir}/libnsl.a
%{_libdir}/libpthread.a
%{_libdir}/libresolv.a
%{_libdir}/librt.a
%{_libdir}/libutil.a

%if %{build_biarch}
%{_prefix}/lib/libBrokenLocale.a
%{_prefix}/lib/libanl.a
%{_prefix}/lib/libc.a
%{_prefix}/lib/libcrypt.a
%{_prefix}/lib/libdl.a
%{_prefix}/lib/libm.a
%{_prefix}/lib/libnsl.a
%{_prefix}/lib/libpthread.a
%{_prefix}/lib/libresolv.a
%{_prefix}/lib/librt.a
%{_prefix}/lib/libutil.a
%endif

#
# glibc-doc
#
%if %{build_doc}
%files doc
%defattr(-,root,root)
%{_infodir}/libc.info*
%endif

#
# glibc-doc-pdf
#
%if %{build_pdf_doc}
%files doc-pdf
%defattr(-,root,root)
%doc manual/libc.pdf
%endif

#
# glibc-debug
#
%if %{build_debug}
%files debug
%defattr(-,root,root)
%dir %{_libdir}/debug
%{_libdir}/debug/*.so
%{_libdir}/debug/*.so.*
%endif

#
# glibc-profile
#
%if %{build_profile}
%files profile
%defattr(-,root,root)
%{_libdir}/lib*_p.a
%endif

#
# glibc-utils
#
%if %{build_utils}
%files utils
%defattr(-,root,root)
%{_libdir}/libmemusage.so
%{_libdir}/libpcprofile.so
%{_bindir}/memusage
%{_bindir}/memusagestat
%{_bindir}/mtrace
%{_bindir}/pcprofiledump
%{_bindir}/xtrace
%endif

#
# nscd
#
%if %{build_nscd}
%files -n nscd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nscd.conf
%config(noreplace) %{_initrddir}/nscd
%{_sbindir}/nscd
%{_sbindir}/nscd_nischeck
%endif

#
# timezone
#
%if %{build_timezone}
%files -n timezone
%defattr(-,root,root)
%{_sbindir}/zdump
%{_sbindir}/zic
%{_mandir}/man1/zdump.1*
%dir %{_datadir}/zoneinfo
%{_datadir}/zoneinfo/*
%endif

#
# glibc-i18ndata
#
%if %{build_i18ndata}
%files i18ndata
%defattr(-,root,root)
%dir %{_datadir}/i18n
%dir %{_datadir}/i18n/charmaps
%{_datadir}/i18n/charmaps/*
%dir %{_datadir}/i18n/locales
%{_datadir}/i18n/locales/*
%endif

%changelog
* Sat Dec 06 2003 Vincent Danen <vdanen@opensls.org> 2.3.2-14.1sls
- OpenSLS build
- P41: propolice patch; use %%build_opensls macros

* Fri Aug 29 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-14mdk
- Patch40: Avoid */lib/i686 compiled libraries to be loaded if the
  host doesn't support CMOV instructions

* Tue Aug 26 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-13mdk
- Patch39: Fix _IO_fwide() for GLIBC_2.0 compatibility (Ulrich Drepper)

* Fri Aug 22 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-12mdk
- Fix <asm/types.h> to mark long long types as GNU __extension__
- Assorted fixes fro current CVS:
  - Patch35: Fix libio for arches without < GLIBC_2.2 compatibility
  - Patch36: Binary compatibility fix for _res@GLIBC_2.0
  - Patch37: Strict aliasing fixes in <ctype.h>
  - Patch38: Fix C++/dlerror/pthread problem

* Tue Aug 12 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-11mdk
- Update kernel-headers to 2.4.22-0.3mdk for new alsa
- Fix kernel-headers to not include <linux/ethtool.h> in <linux/wireless.h>
- Patch34: wcsmbs fixes from current CVS (Ulrich Drepper)

* Tue Jul 29 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-10mdk
- Fix nscd installation
- Patch32: Workaround i586 rtld regression from last release

* Mon Jul 28 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-9mdk
- Update Patch18 (i586-hptiming) to really initilize _dl_hwcap
- Patch32: Add -fno-reorder-block to build -m32 dl-load.c on AMD64
- Patch33: Fix amd64 ldconfig (Jakub Jelinek, CVS)

* Fri Jul 25 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-8mdk
- Update to 2.3.2-CVS (2003/07/04)
- Patch30: Update libm ULPs for cos() and 3.3-hammer branch
- Patch31: SSE fixes from newer CVS (fix i686 libm regression testing)

* Fri Jul 25 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-7mdk
- -fcall-used-g6 on sparc (Per Oyvind Karlsen)
- Patch20: Recognize amd64-*
- Patch24: Add new AMD64 math library
- Patch33: Fix linuxthreads32 tests on AMD64 (Jakub Jelinek, CVS)
- Patch102: Mark GNU extensions in <linux/byteorder/swab*.h>

* Fri Jul 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-6mdk
- Enable %%fs on AMD64, kernel contains necessary fixes
- Fix build on biarch platforms, -m32 is not cross-compiling

* Wed Jul  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-5mdk
- Don't use /bin/rm if it is not available on the system (1st time install)
- All tests now pass on PPC according to Olivier Thauvin
- Patch32: Add Asia/Beijing alias and other time zones requested by users

* Thu Jun  5 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-4mdk
- All tests should pass on ia64 nowadays too
- Patch31: Reintegrate workaround for kernel bug in tcsetattr. According
  to Stew, this fixes an LSB regression. However, the kernel bug remains...

* Mon May 12 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-3mdk
- Assorted fixes from CVS and RH glibc errata

* Thu Apr  3 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-2mdk
- Patch28: Fix get_proc_path(), aka getconf _NPROCESSORS_ONLN (Jakub Jelinek)

* Thu Apr  3 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-1mdk
- Update to 2.3.2-CVS (2003/04/01)

* Sat Mar 15 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-12mdk
- Enable cross-compilation

* Wed Mar  5 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-11mdk
- Remove useless Requires: libgd1 for glibc-utils
- Patch28: Make errno and _res re-available at link time (Daniel Jacobwitz)

* Mon Feb 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-10mdk
- Rebuild against latest binutils so that accesses to errno don't bind locally
- Patch25: Various nscd config & script fixlets (RH)
- Patch26: Really do handle HUP signal for nscd reload (RH)
- Patch27: Fix nextafterl() on x86 (CVS)

* Fri Feb 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-9mdk
- Update kernel headers to 2.4.21-0.pre4.6mdk

* Thu Feb 13 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-8mdk
- Ship with libpthread_nonshared.a
- Workaround build with gcc 3.3-hammer, i.e. disable -funit-at-time
- Patch22: Fix struct dqstats (<quota.h>) to match kernel headers
- Patch23: Implement x86-64 access to FPU control word bits (Olaf Flebbe)
- Patch101: Fix <unistd.h> ppc kernel header (Franz Sirl, SuSE 2.3.1-32)
- Update to 2.3.1-CVS (2003/02/12):
  - Add cancellation support
  - Add and fix support for AT_SYSINFO
  - Add nsec resolution for struct stat and struct stat64
  - Fix dlclose, _res, malloc, vfork in linuxthreads, regex once more
  - Fix handling of encodings with //TRANSLIT in bind_textdomain_codeset()

* Wed Jan 22 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-7mdk
- Remove obsolete Patch20 (x86_64-mathasm)
- Prelink -r i686 libc.so
- Patch20: Revert latest linuxthreads changes on x86-64 for now
- Patch22: Add yet more regex fixes from current CVS
- Patch24: Handle locale-archive in locale -a. Fix LC_MEASUREMENT
  locale bug (Jakub Jelinek, Andreas Schwab from current CVS)

* Mon Dec 23 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-6mdk
- Revert to glibc-2.3.1 sources as of 2002/12/10
- Patch22: Add regexp fixes from current CVS (2002/12/19)
- Patch23: Revert cancellation wrappers from libtphread.so.0(GLIBC_2.3.2)

* Mon Dec 23 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.3.1-5mdk
- Back to Conflicts: initscripts < 6.91-18mdk
- Source13: Inline upgrade script (Fred)

* Thu Dec 19 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-4mdk
- Yet another fix to <linux/videodev2.h>
- Update to 2.3.1-CVS (2002/12/19)
  - Regexp fixes
  - Add support for cancellation handling

* Wed Dec 18 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-3mdk
- Fix <linux/videodev2.h> yet again

* Tue Dec 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-2mdk
- PreReq: initscripts >= 6.91-18mdk instead of Conflicts the other way

* Tue Dec 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1-1mdk
- Move to 2.3.1-CVS (2002/12/10)
- Update new charsets from Pablo
- Nuke kernel-headers sub package, merge it into glibc-devel
- Patch15: Add glibc-2.2 compatibility to workaround broken programs for now
- Patch17: Enable compatibility with older IBM JDK (Jakub Jelinek)
- Really fix MDK 8.2 -> 9.1 ppc upgrade I messed up earlier (Stew)

* Tue Dec 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-22mdk
- Renew and factorize glibc build system
- Fix detection of gcc version for addition of -finline-limit=
- Update Patch6 (exit-during-install) to quit ldconfig only if we are
  installing within DrakX and no extra arguments are used (gc)
- Ship with i686 libthread_db.so.1 otherwise gdb is getting confused
  if i686 libpthread is loaded along with i586 libthread_db.so.1. It
  worked before because libpthread was fully stripped

* Fri Dec  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-21mdk
- Enable make check'ing on PPC, it reportedly no longer hangs
- Make a biarch package for x86-64. We do need 32-bit static libraries
  to build biarch gcc and I don't want to mess with a glibc32 package
- Update Patch25 (i386-fix-hwcaps) in order to better match output of
  /proc/cpuinfo concerning SSE and SSE2. In other words, do search in
  */lib/*/sse{,2} instead of */xmm{,2}

* Wed Nov 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-20mdk
- Workaround 8.2 -> 9.0 upgrade borkage on PPC (Stew)
- Update Patch21 (ia64-fix-strncpy) yet again with glic-2.3-branch
  implementation as rev 1.9 + Kenneth Chen new changes
- Patch102: Fix <linux/posix_acl.h> to include <asm/atomic.h>
- Patch25: Remove "amd3d" hwcap for now since kernel people decided to
  move it to second hwcap word which is not passed to glibc. Add SSE
  and SSE2 features to HWCAP_IMPORTANT. i.e. SSE2 optimized libraries
  can now be looked into */lib/*/xmm2

* Fri Nov  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-19mdk
- Update Patch21 (ia64-fix-strncpy). Also provide a testcase (Ken Chen)
- Really strip only debug symbols and .comment sections from libpthread

* Thu Nov  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-18mdk
- Patch21: Fix IA-64 strncpy() (Ken Chen)
- Patch22: Add Itanium2 optimized bzero(), memset(), memcpy()
  functions (Sverre Jarp, 2.3-branch). Also define __bzero().
- Patch23: Add IA-64 libgcc routines for binary compatibility when
  building with gcc 3.X (Jakub Jelinek, 2.3-branch)
- Patch24: Revert latest linuxthreads changes on x86-64 for now
- Rediff Patch16 (hwcap-check-platform), partly merged upstream
- Update to 2.2-branch (CVS snapshot 2002/09/30):
  - Fix ABI compatibility with libc compiled with old tools on powerpc
  - Fix arguments of shmat() in x86-64 syscall definitions
  - Really store errno as a 32-bit value on x86-64
  - Use __cache_line_size to select the correct stride for dcbz on memset/ppc

* Wed Nov  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-17mdk
- Add debug sub-package
- Conflicts: glibc < 2.2.5-6mdk for timezone package
- Update kernel headers to 2.4.19-18.2mdk

* Mon Aug 19 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-16mdk
- Patch20: revert additions of __nanosleep in 2.2.6 namespace
- Update Patch7 (share-locale) to fix location of locales on x86-64
- Update to 2.2-branch (CVS snapshot 2002/08/12):
  - Fix statvfs ST_NODIRATIME
  - Fix rewind() after first fwscanf() (PR libc/4070)
  - Fix semctl() on PPC (PR libc/3259)
  - Fix pread()/pwrite()
  - Check for overflow on multiplication in xdr_array() and calloc()
- Merge with SuSE releases:
  - Add x86-64 asm optimized string functions
  - Implement {get,set,make,swap}context on x86-64

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-15mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon Jul 22 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-14mdk
- Patch22: Don't segfault on empty charmap file (Bruno Haible)
- Patch23: Don't use __thread as identifier since it is now a gcc3.3+ keyword

* Sat Jul 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-13mdk
- Fix create_asm_headers.sh to correctly translate '-' to '_' as well
- Fix %%post buglets introduced in previous release

* Sat Jul 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-12mdk
- Add biarch headers, clean kernel-headers
- Strip libpthread, do ship with i686 librt
- Fix service restart in %%post when xfs is running (Pablo)
- Go back at using ../configure and pass correct host information
- Minimum kernel supported is back to 2.2.5 on ia32 for non-floating stacks
- Merge with SuSE releases:
  - Add some optimized x86-64 math routines
  - Fix lgammal_r implementation
  - Warn about using host caching with nscd, in the config file

* Tue Jul 16 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 2.2.5-11mdk
- Patch25: fix alpha asm for recent binutils (Roland McGrath, via Stefan)

* Tue Jul  9 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-10mdk
- Static-devel'ization
- Explicit Requires: version-release for glibc-devel
- Update kernel-headers to 2.4.18-21mdk for new alsa 0.9.0-rc2

* Fri Jul  5 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-9mdk
- Add nscd user
- Remove merged bits from Patch50 (x86_64-linuxthreads)
- Fix Patch19 (hwcap-check-platform) so that the platform check in
  HWCAP_CHECK is performed even if _dl_platform was NULL. This happens
  for example in a statically linked executable that uses dlopen().

* Wed Jul  3 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-8mdk
- Add %{_bindir}/sln, it's not useless for users
- Don't package pt_chown. It is only needed if devpts is not used. But
  since we are running kernel 2.4+, that's fine without
- Patch19: Skip library that is not of a subarch of running architecture
- Patch20: Define sqrtl() on PPC, should fix OOo link there
- Update to 2.2-branch (CVS snapshot 2002/07/02):
  - Fix libgcc compat on PPC
  - Fix getcontext() on IA-64 to really match David's change
  - Rewrite x86-64 elf_machine_load_address() to not use 32-bit pc
    relative relocations

* Fri Jun 21 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-7mdk
- Sanitize specfile (BuildRequires: perl, url tag, use %%configure)
- Add i686 optimized libraries in /%{_lib}/i686
- Disable tests on ppc for now

* Fri Jun 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-6mdk
- Remove -D__USE_STRING_INLINES
- Add Provides: ld.so.1 on PPC
- Remove BuildRequires: gcc = 2.95.3 on PPC
- Make check in %%build stage
- Patch15: Add changes from former Source12 (gb18030) but disable that
  in regression testing
- Patch16: Use old DE.po since the new one from 2002/05/14 is
  incomplete and results in failures for intl checks
- Patch17: Add i386 ULPs for cacosh() tests
- Major specfile reorganization, new subpackages (glibc-i18n,
  glibc-doc, glibc-doc-pdf, timezone)
- Update to 2.2-branch (CVS snapshot 2002/06/09):
  - X86-64 fixes and additions
  - Correct calls to __lseek() in the dynamic linker
  - Fix recovery code in strncpy() on IA-64
  - Correct check for size of alignment value in __posix_memalign()
  - Fix a typo causing only lower 4 bits of each ethernet address byte
    being assigned
- Merge with SuSE releases (2 new patches):
  - Fix linuxthreads for x86-64
  - Enable profiling on x86-64

* Tue May  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-5mdk
- Automated rebuild in gcc3.1 environment

* Wed May  1 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-4mdk
- Update kernel-headers to match 2.4.18-13mdk (alsa-headers 0.9.0rc1)
- Patch14: Create lddlibc4 and ld-linux.so.2 files on PPC (Stew)
- Also add lddlibc4 for other arches

* Mon Apr 15 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-3mdk
- Update to 2.2-branch (CVS snapshot 2002/04/14):
  - Fix mktime() again
  - Fix relocation dependency handling
  - Fix symbol lookup for most recent vs. earliest version of a symbol
    (aka. fix undefined atexit symbol problem with VisualWorks Smalltalk)
- Add Requires: libgd1 to glibc-utils
- Update kernel-headers to match 2.4.18-11mdk with alsa-headers
- Per Stew and Andrew Josey's recommendantions, don't obsolete old
  currencies from Euro countries. Aka. revert 2002-02-28 change.

* Thu Apr 11 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-2mdk
- Update to 2.2-branch (CVS snapshot 2002/04/08)
- Update kernel-headers to match 2.4.18-10mdk
- Strip debugging info from all static libraries
- Build with --enable-kernel=2.4.1 on all arches

* Thu Mar 21 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.5-1mdk
- Regenerate Patch9 for new charsets
- Remove ldd-rewrite Patch11 for IA-64 (merged upstream)
- Add glibc-utils package for memusage, mtrace and xtrace
- Update to 2.2-branch (CVS snapshot 2002/03/20):
  - Correctly close the UDP connection right away [PR libc/3120]
  - Fix daylight setting for tzset
  - Fix DST handling for southern hemisphere
  - Fix ftime, aka don't return 1000 in millitm
  - Fix nice return value
  - Provide libc's __{,u}{div,mod}di3 since it is not possible to grab
    it from libgcc.a anymore (gcc-3.1 libgcc.a has all its routines
    .hidden)
  - Store correct collation sequence values
  - Remove some string2.h optimizations for gcc-3.0+

* Thu Mar  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.4-25mdk
- 2.4.18-4mdk kernel headers
- Fixup Source11 (make_versionh.sh) for s/kheaders/kheaders_ver/

* Wed Feb  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.4-24mdk
- Spec cleanups.
- 3 new patches from glibc-2.2.5:
  - Patch60: Bugfix to pthread_key_delete. It was iterating over the
    thread manager's linked list of threads, behind the thread
    manager's back causing a race. The fix is to have the manager
    iterate over the threads instead, using a new request type for
    doing so. (Kaz Kylheku)
  - Patch61: specific.c (pthread_key_delete): Don't contact the thread
    manager if no threads have been created yet. (Andreas Schwab)
  - Patch62: When sigaction in libpthread is called the first time for
    a signal we don't know whether the old signal handler is SIG_DFL
    or SIG_IGN, so we must return the value that the kernel
    reports. (Andreas Schwab)

* Mon Jan 28 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.2.4-23mdk
- replaced the gb18030 support with the one from Thiz Laboratory as
  suggested by Geoffrey Lee

* Mon Jan 14 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-22mdk
- Conflicts with older initscripts (don't do Requires: to don't screwd
  up install requires and it's only needed when upgrade).
- Use /sbin/service --fullrestartall instead of doing in %post.

* Mon Jan 14 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-21mdk
- s|modversion|modversions|; (Thanks a lot Andrej).

* Thu Jan 10 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-20mdk
- Remove netatalk/at.h to avoid conflict with netatalk rpm's.

* Wed Jan  9 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-19mdk
- 2.4.17 kernel headers.

* Wed Dec 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-18mdk
- Add rh patch for gcc3 support.

* Wed Dec 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-17mdk
- Add rh patches (j.jelinek 2.2.4-19.3):
	- fix inttypes.h typo (#57268)
	- fix glob buffer overflow
- add selected changes from CVS
  - handle DT_RUNPATH properly
  - fix *scanf nan/inf handling
  - fix strndup
  - fix fnmatch - handling at end of bracket expr
  - allow dlfcn.h to be used in C++
  - fix IPv6 reverse lookups
  - avoid SPARC warnings in bits/mathinline.h
- Sync with latest kernel headers.

* Tue Dec  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-16mdk
- Fix upgrade to relaunch service only when upgrade between version.
- Rewrote the glibc upgrade %post to do a correct ordering of services.

* Mon Dec  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-15mdk
- sync with kernel-headers 2.4.16.

* Thu Nov 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-14mdk
- Fix stupidities in version.h generation.

* Thu Nov 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-13mdk
- Include more explicit #error in modversion.sh like the one of version.sh.
- Fix %post to restart the service only when is present.

* Wed Nov 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-12mdk
- Move the kernel-headers package here.
- Big specs changes to compile with the kernel-headers.

* Tue Nov 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-11mdk
- New charset patch from pablo.

* Mon Nov 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-10mdk
- Merge with latest rh.
- turn /usr/lib/librt.so into linker script.
- call xtrace with xvt not xterm (snailtalk).

* Wed Oct 31 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.4-9mdk
- Patch14: timer_delete, timer_settime.c: Thread may be NULL for SIGEV_NONE
- Patch13: Protect all communications from and to manager with
  TEMP_FAILURE_RETRY. aka. Fix bug in LinuxThreads where manager and
  threads could get out of synch due to an interrupted read call.

* Wed Oct  3 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.4-8mdk
- Add BuildRequires: tetex-latex
- Use /bin/rm in %%post scriptlet
- Patch11: Enable ldd to know about IA-32 binaries or libraries on IA-64
- Patch12: Define __gwchar_t to wchar_t for C++ in <inttypes.h>

* Tue Sep 18 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.4-7mdk
- Remove Patch200: strnlen() for IA-64 is now fixed upstream,
  and strncpy() has been improved

* Mon Sep 10 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.2.4-6mdk
- fix perror

* Tue Sep  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-5mdk
- Merge new_charsets patch with latest release.

* Mon Sep  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-4mdk
- Merge with 2.2.4-11 rh release.

* Mon Sep  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-3mdk
- Merge with latest rh release.

* Mon Aug 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-2mdk
- Add pablo new_charsets patch for 2.2.4.

* Mon Aug 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-1mdk
- 2.2.4.
- Spec cleanup.

* Tue Aug 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.3-8mdk
- Add /usr/lib/gconv to filelist (pixel).

* Tue Jul 31 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.3-7mdk
- Merge with rh patches.

* Sun Jul 29 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.2.3-6mdk
- fixed typo in Summary (s/librairies/libraries).
- added glibc PDF documentation.

* Thu Jul 26 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.3-5mdk
- Reverted strncpy patch for ia64 (caused segfaults in stage1-install/slang)
- Merge with latest rh (2.2.3-14) :
  - kill non-pic code in libm.so
  - fix getdate
  - fix some locales (RH-#49402)
  - add floating stacks on IA-64, Alpha, Sparc (RH-#49308)

* Mon Jul 23 2001 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.3-4mdk
- no -freorder-blocks on PPC, Requires gcc 2.96 bypassed on glibc-devel for PPC

* Fri Jul 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.2.3-3mdk
- Merge with latest rh (2.2.3-13).

* Tue May 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.3-2mdk
- Add wins to default host of nsswitch.conf (staburet).
- Merge with latest Red Hat (2.2.3-10) :
- fix #include <signal.h> with -D_XOPEN_SOURCE=500 on ia64 (#35968)
- fix a dlclose reldeps handling bug
- some more profiling fixes
- fix tgmath.h

* Mon May 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.3-1mdk
- 2.2.3.

* Sun Apr 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.2-5mdk
- Upgrade to the rh version of glibc (pre 2.2.3 with fixes).
- This release fix Oracle and JVM problems.

* Wed Feb 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.2-4mdk
- Exclude libpthread to be stripped also.

* Tue Feb 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.2-3mdk
- Define PATH_VI to /bin/vi and not /usr/bin/vi.

* Sat Feb 17 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.2-2mdk
- Add a __truncate64 for 64 bytes arch.
- Add updated patch from pablo for the new charsets.

* Fri Feb 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.2-1mdk
- 2.2.2.

* Tue Feb  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.1-7mdk
- Add new charsets from pablo.

* Wed Jan 31 2001 Francis Galiegue <fg@mandrakesoft.com> 2.2.1-6mdk
- Now compiles on ia64

* Sat Jan 27 2001 David BAUDENS <baudens@mandrakesoft.com> 2.2.1-5mdk
- PPC: rebuild with GCC 2.95.3
- PPC: use lower but safer optimizations

* Fri Jan 19 2001 David BAUDENS <baudens@mandrakesoft.com> 2.2.1-4mdk
- PPC: use default optimizations

* Mon Jan 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.1-3mdk
- Don't restart the network subsystem service also.

* Mon Jan 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.1-2mdk
- Get the getaddrinfo fix from cvs.

* Mon Jan 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.1-1mdk
- Don't restart pcmcia service when upgrading.
- 2.2.1.

* Wed Jan 10 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.2-22mdk
- added support for all the extra charsets so iconv() can convert
  between them

* Tue Dec 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-21mdk
- Default without kernel-2.4 (silly me).

* Tue Dec 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-20mdk
- Compile by default with kernel-2.4. enabled (but make it as option).

* Thu Dec  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-18mdk
- Remove useless timezone/{posix,right}.

* Wed Dec  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-17mdk
- Don't include useless /sbin/sln.

* Wed Dec  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-16mdk
- Revert to sash like before.

* Tue Dec  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-15mdk
- Make script executed thought /bin/ash.static and don't depend of bash.

* Tue Dec  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-14mdk
- Make /usr/share/locale default locale path.

* Sat Dec  2 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-13mdk
- Move ldconfig to his own package.

* Tue Nov 28 2000 David BAUDENS <baudens@mandrakesoft.com> 2.2-12mdk
- Adjust BuildFlags for GCC-2.96 (PPC)

* Sun Nov 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-11mdk
- Remove zic manpages conflicts.

* Sat Nov 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-10mdk
- New manpages from Debian.
- Include everything in zoneinfo/ dir not only [A-Z]* (fix tzselect).
- Don't launch ldconfig if we find DURING_INSTALL env.

* Sat Nov 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-9mdk
- Fix ldconfig with soname (libc-hackers@).

* Thu Nov 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-8mdk
- Provides: Obsoletes: ld.so ldconfig, add ldconfig from glibc.

* Wed Nov 22 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2-7mdk
- get compiled on alpha. (Stefan.)

* Wed Nov 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-6mdk
- Don't include %%{_includedir} and %%{_infodir} in the file list.
- Put libpcprofile.so libmemusage.so to devel package.
- Fix syntax error in script (thnks: fcrozat).
- Merge debian patch :
  o (glibc-2.2-nss-upgrade.patch.bz2)
	This patch makes future upgrades easier. It resolves problems with
    running daemons having NSS modules upgraded out from under them.

* Mon Nov 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-5mdk
- If we find broken link after install erase it to make ldconfig
  happy.

* Thu Nov 16 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.2-4mdk
- don't strip ld-2.2.so

- use sash in %%pre because bash needs the libc...
- don't resart netfs on upgrade.

* Tue Nov 14 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.2-3mdk
- added a prereq on /bin/sh.

* Fri Nov 10 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.2-2mdk
- don't abort if a service doesn't restart

* Fri Nov 10 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.2-1mdk
- 2.2
- try to restart the services on upgrade.

* Wed Nov 08 2000 David BAUDENS <baudens@mandrakesoft.com> 2.1.97-4mdk
- Try to optimize for PPC

* Tue Nov 07 2000 David BAUDENS <baudens@mandrakesoft.com> 2.1.97-3mdk
- Fix build on PPC (don't try to use gcc-2.96)

* Tue Nov  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.97-2mdk
- devel package depends on glibc %%version-%%release
- fixed the __sysconf function not present in dynamic lib.

* Tue Nov  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.97-1mdk
- 2.1.97

* Thu Oct 26 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.95-3mdk
- removed dependency on basesystem (this was doing a prereq loop).

* Wed Oct 25 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.1.95-2mdk
- changed the Prereq basesystem in Requires.
- added Prereq on /sbin/ldconfig

* Wed Oct 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.95-1mdk
- 2.1.95.

* Tue Oct 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.92-2mdk
- Fix "warning: pointer of type `void *' used in arithmetic" in string2.h.
- Fix pthreads manpages.
- Use @ifnottex instead of @ifinfo in texinfo files.
- Add BIG5_1984 eo_EO locales.
- Make ldd non-executable aware.
- Define VARDB in /var/lib/misc like FHS want.
- Fix some C++ unaligned traps on alpha.
- Add patches from Debian.

* Tue Oct 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.92-1mdk
- 2.1.92.

* Tue Oct 10 2000 David BAUDENS <baudens@mandrakesoft.com> 2.1.3-17mdk
- BuildRequires: patch, gettext

* Mon Sep  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-16mdk
- Get another security fix from cvs for locales.
- Remove security patch from caldera and get the official one from cvs.

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 2.1.3-15mdk
- move a hell lot of doc to glibc-devel
- use find_lang for mo files
- little cleanup

* Wed Aug 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-14mdk
- Strip glibc and make happy pixel (aka: his breaking my di**k).

* Fri Aug 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-13mdk
- Add security patch from caldera on ld.so :
    Remove completely the environement variable when using LD_PRELOAD
    with setuid apps.

* Thu Aug 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-12mdk
- Readd manpages.

* Wed Aug  2 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-11mdk
- Don't strip libc.
- Fix info files.

* Fri Jul 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-10mdk
- Maros.
- BM.

* Fri Jul 07 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-9mdk
- The threads fix is a wrong patch.

* Thu Jul  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-8mdk
- Remove old ChangLog.
- Fix threads (Debian).

* Wed Jun 14 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.1.3-7mdk
- added support for a few missing charsets

* Sat Jun  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-6mdk
- Make ldd handle non-executable shared objects.
- Fix some C++ unaligned traps on alpha.

* Fri May  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-5mdk
- Fix threads.

* Tue Apr 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-4mdk
- Fix bad ucontext.h headers conflicts with  ncurses and others library.
- removed iso3166.tab and posixrules from %files section, they are already
  in the filelist (Stefan van der Eijk <s.vandereijk@chello.nl>).
- fix alpha build.

* Fri Apr 14 2000 David BAUDENS <baudens@mandrakesoft.com> 2.1.3-3mdk
- i486 fix
- Comment BuildRequires: egcs (not needed; see 2.1.3-1mdk)

* Wed Apr  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-2mdk
- Merge the Adam Lesback <adam@mandrakesoft.com> powerpc change.

* Thu Mar 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-1mdk
- Recompile with gcc2.95 and get optimisations back.
- Merge rh patchs.
- Clean-up specs.
- Adjust groups.

* Tue Mar  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-0.2mdk
- Compile with egcs.
- glibc2.1.3 final.
- Merge with last rh patchs.

* Thu Feb 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-0.1mdk
- Forget also the Serial:.
- Forget the release scheme.

* Wed Feb 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-1mdk
- 2.1.3 from CVS.
- Getting the glibc like redhat does (from cvs).
- Spec rewrite.

* Wed Dec 15 1999 Frederic Lepied <flepied@kenobi.mandrakesoft.com>
- add patch for malloc (rd)

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add from pablo catalan locales.
- Bzip2 manpages.

* Sat Oct 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Last CVS snapshot.

* Thu Oct 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix stupid thing in %files (thanks pablo).
- Remove glibc-localedata

* Sun Oct 17 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Last CVS snapshot.
- Clean-up of specfile.

* Mon Oct 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add pixel patch to don't lie about k6 optimisations.

* Mon Oct 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add serial

* Fri Oct  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add Pablo (AKA: Mri18n) patch :
    - Support of new encodages in /usr/lib/gconv).
- Merge with rh patch and others.
- Update to snapshot 2.1.3 but keep the version to 2.1.2.
- disable some extra debugging messages form alpha/ioperm.c
- make /etc/localtime a real file instead of a symlink
- add sys/raw.h as anew header file.(rh)
- add the vfork patch for linuxthreads.(rh)

* Thu Sep 09 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 2.1.2final (mainly bug fixes)

* Wed Aug 26 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 2.1.2

* Fri Jul 09 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- moved locales data to separate package; don't make compilated
  locales (that will be better on separate locales-$LANG
  packages, one for language, more accurate and more numerous); so people
  can choose not to install those, or install exactly those they want.
  glibc-localedata is only needed if you want to manually build locales
  definitions.

* Fri Jul 09 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix wrong install entry in dir info files (Patch50).

* Fri Jul  9 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.de>
- 2.1.1final
- add Debian fixes
- enable SMP build

* Wed May 19 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- 2.1.1pre3

* Fri Apr 30 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS better

* Wed Apr 14 1999 Cristian Gafton <gafton@redhat.com>
- new CVS update - some patches dropped out
- updated obsoletes tag lines
- patch for the ukraine support

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- add patch for libstdc++ 2.7.2 (enable __dup, __pipe and __waitpid)
- linuxthread patch from HJLu
- add patch to make nscd respond to SIGHUP by dumping the cache

* Wed Apr 07 1999 Cristian Gafton <gafton@redhat.com>
- updated from cvs tree
- add patch for fstatvfs from HJLu

* Thu Apr 01 1999 Cristian Gafton <gafton@redhat.com>
- opentty fix
- don't call lddlibc4 on sparcs

* Thu Mar 25 1999 Cristian Gafton <gafton@redhat.com>
- version 2.1.1
- make nscd run by default at init
- nscd subpackage
- let the subpackages autoreq their own thing

* Fri Mar 12 1999 Cristian Gafton <gafton@redhat.com>
- version 2.1
- strip binaries installed by default

* Thu Feb 18 1999 Cristian Gafton <gafton@redhat.com>
- updated snapshot
- glibc-crypt might have export problems (who knows?), so we are nosource
  iit for now

* Wed Feb 03 1999 Cristian Gafton <gafton@redhat.com>
- version 2.0.112
- merge glibc-debug into glibc-devel
- new compat add-on

* Wed Jan 13 1999 Cristian Gafton <gafton@redhat.com>
- new glibc-crypt add-on
- version 2.0.109
- handle /etc/localtime separately
- don't include /usr/share in the file list
- don not build glibc-compat on the arm

* Wed Dec 02 1998 Cristian Gafton <gafton@redhat.com>
- build ver 2.0.105 on all four arches
- enabled /usr/include/scsi as part of the glibc package

* Fri Oct 02 1998 Cristian Gafton <gafton@redhat.com>
- first build for 2.0.96
