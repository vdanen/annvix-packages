#
# spec file for package glibc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

#define _unpackaged_files_terminate_build 0

# alt 2.5-alt4
# rh 2.5-12
%define basevers	2.6.1
%define crypt_bf_ver	1.0.2

%define revision	$Rev$
%define name		glibc
%define version		%{basevers}
%define release		%_revrel
%define epoch		6
%define glibcsrcdir	%{name}-%{version}

# <version>-<release> tags from kernel package where headers were
# actually extracted from
%define kheaders_ver    2.6.22
%define kheaders_rel    3mdv

%define build_check	0
%define build_profile	1
%define build_locales	1
%define build_locales_utf8 0

# allow make check to fail only when running kernels where
# we know tests must pass (no missing features or bugs in the kernel)
%define check_min_kver	2.6.21

%define build_biarch	0
%ifarch x86_64
%define build_biarch	1
%endif

# Determine minium kernel versions
%define enablekernel	2.6.9

%define _slibdir	/%{_lib}
%define _slibdir32	/lib

# define target (base) architectures
%define arch		%(echo %{target_cpu}|sed -e "s/\\(i.86\\|athlon\\)/i386/" -e "s/amd64/x86_64/" -e "s/\\(sun4.*\\|sparcv[89]\\)/sparc/")
%define isarch()	%(case " %* " in (*" %{arch} "*) echo 1;; (*) echo 0;; esac)

Summary:	The GNU libc libraries
Name:		%{name}
Version: 	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	LGPL
Group:		System/Libraries
URL:		http://www.gnu.org/software/libc/

Source0:	http://ftp.gnu.org/gnu/glibc/glibc-%{version}.tar.bz2
Source2:	http://ftp.gnu.org/gnu/glibc/glibc-%{version}.tar.bz2.sig
Source1:	glibc-redhat.tar.bz2
Source3:	crypt_blowfish-%{crypt_bf_ver}.tar.gz
Source4:	crypt_freesec.c
Source5:	crypt_freesec.h
Source6:	strlcpy.3
Source7:	glibc-manpages.tar.bz2
Source8:	http://ftp.gnu.org/gnu/glibc/glibc-libidn-%{version}.tar.bz2
Source9:	http://ftp.gnu.org/gnu/glibc/glibc-libidn-%{version}.tar.bz2.sig
Source10:	glibc-find-requires.sh
Source11:	nsswitch.conf
Source12:	glibc-check.sh
Source14:       nscd.run
Source15:       nscd-log.run
Source16:       nscd.finish
# kernel-headers tarball generated from mandriva kernel in svn with:
# make INSTALL_HDR_PATH=[path] headers_install_all
Source20:       kernel-headers-%{kheaders_ver}.%{kheaders_rel}.tar.bz2
Source21:       make_versionh.sh
Source22:       create_asm_headers.sh

# Patches
# -------
# We are using the following numbering rules for glibc patches:
#    0-99 - CVS
# 100-199 - RH
# 200-219 - SuSE
# 220-239 - Gentoo
# 300-499 - ALT/Openwall
# 500-599 - Mandriva
# 600-699 - Annvix
# CVS
# Additional patches from 2.6-branch/trunk
Patch0:		glibc-cvs-nscd_dont_cache_ttl0.patch
Patch1:		glibc-cvs-utimensat.patch
Patch2:		glibc-bz4599.patch
Patch3:		glibc-bz4125.patch
Patch4:		glibc-cvs-gcc_init_fini.patch
Patch5:		glibc-bz4647.patch
Patch6:		glibc-bz4773.patch
Patch7:		glibc-_nl_explode_name_segfault_fix.patch
Patch8:		glibc-bz4776.patch
Patch9:		glibc-bz4775.patch
Patch10:	glibc-cvs-popen_bug_fix.patch
Patch11:	glibc-bz4792.patch
Patch12:	glibc-cvs-_cs_posix_v6_width_restricted_envs.patch
Patch13:	glibc-bz4813.patch
Patch14:	glibc-bz4812.patch
Patch15:	glibc-bz4772.patch
Patch16:	glibc-cvs-warning_patrol_fixes.patch
Patch17:	glibc-cvs-getconf_add_missing_lvl4_cache_linesize.patch
Patch18:	glibc-cvs-libc_texinfo_update.patch
Patch19:	glibc-cvs-ix86_rwlock_fixes.patch
Patch20:	glibc-cvs-gettext_memleak_fixes.patch
Patch21:	glibc-cvs-strtod_handle_minuszero.patch
Patch22:	glibc-cvs-ar_SA-dz_BT-LC_TIME-fixes.patch
Patch23:	glibc-cvs-po_updates.patch
Patch24:	glibc-cvs-rh250492.patch
# RH
# SuSE
Patch200:	glibc-2.3.2-suse-resolv-response-length.diff
# Gentoo
# ALT/Openwall
Patch300:	glibc-2.3.3-owl-crypt_freesec.diff
Patch301:	glibc-2.6.1-avx-openbsd-strlcpy-strlcat.patch
Patch303:	glibc-2.5-alt-pt_chown.patch
Patch304:	glibc-2.3.5-alt-string2.patch
Patch305:	glibc-2.5-alt-sys-mount.patch
Patch306:	glibc-2.5-alt-getopt-optind.patch
Patch307:	glibc-2.5-alt-tmpfile.patch
Patch308:	glibc-2.5-alt-asprintf.patch
Patch309:	glibc-2.5-alt-libio-bound.patch
Patch310:	glibc-2.5-owl-alt-syslog-ident.patch
Patch311:	glibc-2.5-mjt-owl-alt-syslog-timestamp.patch
Patch312:	glibc-2.5-owl-alt-res_randomid.patch
Patch313:	glibc-2.5-alt-iconv_prog-replace.patch
Patch314:	glibc-2.5-alt-versioning.patch
Patch315:	glibc-2.5-alt-ldconfig-exit-during-install.patch
Patch316:	glibc-2.5-alt-i18n.patch
Patch317:	glibc-2.5-alt-relocate-helper-libs.patch
Patch318:	glibc-2.5-alt-xtrace-xvt.patch
Patch319:	glibc-2.6.1-avx-owl-alt-ldd.patch
Patch320:	glibc-2.5-alt-ldconfig-search_dir.patch
Patch321:	glibc-2.5-alt-linux-dl-execstack.patch
Patch322:	glibc-2.5-alt-assume_kernel.patch
Patch323:	glibc-2.5-alt-libgd.patch
Patch324:	glibc-2.6.1-avx-alt-tmp-scripts.patch
Patch325:	glibc-2.5-owl-rpcgen-cpp.patch
Patch326:	glibc-2.5-owl-alt-resolv-QFIXEDSZ-underfills.patch
Patch327:	glibc-2.6.1-avx-owl-alt-sanitize-env.patch
Patch328:	glibc-2.5-alt-__locale_getenv.patch
Patch329: 	glibc-2.5-alt-getconf.patch
Patch331:	glibc-2.5-alt-default_nss.patch
# Mandriva
Patch501:       kernel-headers-gnu-extensions.patch
Patch503:	glibc-2.2.5-share-locale.patch
Patch504:	glibc-2.2.2-mdv-fhs.patch
Patch505:	glibc-2.6-mdv-multiarch.patch
Patch506:	glibc-2.6.1-avx-mdv-suse-ldconfig-old-cache.patch

# Annvix
Patch600:	glibc-2.3.5-avx-relocate_fcrypt.patch
Patch601:	glibc-2.3.6-avx-increase_BF_FRAME.patch
Patch603:	glibc-2.4-avx-owl-crypt.patch
Patch604:	glibc-2.5-avx-nscd.conf.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	patch
BuildRequires:	gettext
BuildRequires:	perl
BuildRequires:	autoconf2.5
# we need suitable linker for -Wl,--hash-style=both
BuildRequires:	binutils >= 2.16.91.0.7
BuildRequires:	gcc >= 4.1.0
BuildRequires:	gd-devel

AutoReq:	false
Provides:	glibc-crypt_blowfish = %{crypt_bf_ver}
Provides:	glibc-localedata
Provides:	ld.so
Provides:	ldconfig = %{epoch}:%{version}-%{release}
Provides:	/sbin/ldconfig
# the dynamic linker supports DT_GNU_HASH
Provides:	rtld(GNU_HASH)
Obsoletes:	ldconfig
Obsoletes:	libc-static
Obsoletes:	libc-devel
Obsoletes:	libc-profile
Obsoletes:	libc-headers
Obsoletes:      linuxthreads
Obsoletes:	gencat
Obsoletes:	locale
Obsoletes:	glibc-localedata
Obsoletes:	ld.so
Conflicts:	kernel < %{enablekernel}

%description
The glibc package contains standard libraries which are used by
multiple programs on the system.  In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs.  This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library.  Without these two libraries, a
Linux system will not function.  The glibc package also contains
national language (locale) support.


%package utils
Summary:	The GNU libc miscellaneous utilities
Group:		Development/Other
Requires: 	%{name} >= %{epoch}:%{version}-%{release}

%description utils
The glibc-utils package contains miscellaneous glibc utilities.


%package devel
Summary:	Header and object files for development using standard C libraries
Group:		Development/C
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	glibc-crypt_blowfish-devel = %{crypt_bf_ver}
Obsoletes:	kernel-headers
Provides:	kernel-headers = 1:%{kheaders_ver}
Conflicts:	texinfo < 3.11
Requires(post):	info-install
Requires(post):	coreutils
Requires(preun): info-install
Requires(postun): coreutils
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


%package static-devel
Summary:        Static libraries for GNU C library
Group:          Development/C
Requires:       %{name}-devel = %{epoch}:%{version}-%{release}

%description static-devel
The glibc-static-devel package contains the static libraries necessary
for developing programs which use the standard C libraries. Install
glibc-static-devel if you need to statically link your program or
library.


%if %{build_profile}
%package profile
Summary:	The GNU libc libraries, including support for gprof profiling
Group:		Development/C
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	libc-profile
Provides:	libc-profile = %{version}-%{release}
Autoreq:	true

%description profile
The glibc-profile package includes the GNU libc libraries and support
for profiling using the gprof program.  Profiling is analyzing a
program's functions to see how much CPU time they use and determining
which functions are calling other functions during execution.  To use
gprof to profile a program, your program needs to use the GNU libc
libraries included in glibc-profile (instead of the standard GNU libc
libraries included in the glibc package).
%endif


%package -n nscd
Summary:	A Name Service Caching Daemon (nscd)
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(preun): rpm-helper
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Autoreq:	true

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS+, and may help with DNS as well.


%package i18ndata
Summary:	Database sources for 'locale'
Group:		System/Libraries

%description i18ndata
This package contains the data needed to build the locale data files
to use the internationalization features of the GNU libc.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n glibc-%{version} -a 1 -a 3 -a 7 -a 20
tar xjf %{_sourcedir}/glibc-libidn-%{version}.tar.bz2
mv glibc-libidn-%{version} libidn

# CVS
%patch0 -p1 -b .nscd_dont_cache_ttl0
%patch1 -p1 -b .utimensat
%patch2 -p1 -b .bz4599
%patch3 -p1 -b .bz4125
%patch4 -p1 -b .gcc_init_fini
%patch5 -p1 -b .bz4647
%patch6 -p1 -b .bz4773
%patch7 -p1 -b ._nl_explode_name_segfault_fix
%patch8 -p1 -b .bz4776
%patch9 -p1 -b .bz4775
%patch10 -p1 -b .popen_bug_fix
%patch11 -p1 -b .bz4792
%patch12 -p1 -b ._cs_posix_v6_width_restricted_envs
%patch13 -p1 -b .bz4813
%patch14 -p1 -b .bz4812
%patch15 -p1 -b .bz4772
%patch16 -p1 -b .warning_patrol_fixes
%patch17 -p1 -b .getconf_add_missing_lvl4_cache_linesize
%patch18 -p1 -b .libc_texinfo_update
%patch19 -p1 -b .ix86_rwlock_fixes
%patch20 -p1 -b .gettext_memleak_fixes
%patch21 -p1 -b .strtod_handle_minuszero
%patch22 -p1 -b .ar_SA-dz_BT-LC_TIME-fixes
%patch23 -p1 -b .po_updates
%patch24 -p1 -b .rh250492

# RH

# SuSE
# avoid read buffer overruns in apps using res_* calls
%patch200 -p1

# Gentoo

# ALT/Openwall
# copy the freesec stuff
cp %{_sourcedir}/crypt_freesec.[ch] crypt/

echo "Applying crypt_blowfish patch:"
%patch603 -p1 
#patch -p1 -s < crypt_blowfish-%{crypt_bf_ver}/glibc-2.3.2-crypt.diff
mv crypt/crypt.h crypt/gnu-crypt.h
cp -a crypt_blowfish-%{crypt_bf_ver}/*.[chS] crypt/

## FreeSec support for extended/new-style/BSDI hashes in crypt(3)
%patch300 -p1
# Import strlcpy/strlcat from OpenBSD.
%patch301 -p1
# Do not install pt_chown.
%patch303 -p1
# Fix -Wpointer-arith issue in string2.h
%patch304 -p1
# Update sys/mount.h MS_* flags from linux-2.6.17, fix for gcc -pedantic support.
%patch305 -p1
# Set proper optind when argc < 1.
%patch306 -p1
# Allow tmpfile(3) to use $TMPDIR.
%patch307 -p1
# Change asprintf/vasprintf error handling.
%patch308 -p1
# Check for potential integer overflow in fread*/fwrite*.
%patch309 -p1
# Don't blindly trust __progname for the syslog ident.
%patch310 -p1
# use ctime_r() instead of strftime_r() in syslog(3).
%patch311 -p1
# Improve res_randomid in the resolver.
%patch312 -p1
# Add "--replace" option to iconv utility.
%patch313 -p1
# Export __libc_enable_secure.
%patch314 -p1
# Change ldconfig to exit during distribution install.
%patch315 -p1
# Support more ru_* locales.  Fix tt_RU.
%patch316 -p1
# Relocate helper libraries from /%_lib to %_libdir.
%patch317 -p1
# xtrace.sh: If `TERMINAL_PROG' is not set, set it to `xvt'.
%patch318 -p1
# ldd: Always execute traced object directly with dynamic linker.
%patch319 -p1
# ldconfig: Revert symlink handling changes in search_dir().
%patch320 -p1
# Fix mprotect return code handling in _dl_make_stack_executable().
%patch321 -p1
# Fix _dl_osversion_init(), _dl_non_dynamic_init() and
# dl_main() functions to not assume too old kernel version.
%patch322 -p1
# memusagestat: Fix linkage.
%patch323 -p1
# memusage, xtrace: Fix tmp file handling.
%patch324 -p1
# Avoid hardcoding of cpp binary, use execvp instead of execv.
%patch325 -p1
# Avoid potential reads beyond end of undersized DNS responses.
%patch326 -p1
# Sanitize the environment in a paranoid way.
%patch327 -p1
# Introduce and export __locale_getenv.
%patch328 -p1
# Introduce _CS_LIBDIR and _CS_SLIB to confstr and getconf.
%patch329 -p1
# Change /etc/default/nss to /etc/nss.conf.
%patch331 -p1

# Mandriva
%patch503 -p1 -b .share_locale
%patch504 -p1 -b .fhs
%patch505 -p1 -b .multiarch
%patch506 -p1 -b .ldconfig_old_cache

# Annvix
%patch600 -p1
%patch601 -p1
%patch604 -p1

pushd kernel-headers/
TARGET=%{_target_cpu}
%patch501 -p1
%{expand:%(%__cat %{_sourcedir}/make_versionh.sh)}
%{expand:%(%__cat %{_sourcedir}/create_asm_headers.sh)}
popd

find . -type f -size 0 -o -name '*.orig' -exec rm -f {} \;

cat > find_provides.sh << EOF
#!/bin/sh
/usr/lib/rpm/annvix/find-provides | grep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_provides.sh

cat %{_sourcedir}/glibc-find-requires.sh >glibc_find_requires.sh
chmod +x glibc_find_requires.sh

cat > find_requires.sh << EOF
#!/bin/sh
%{_builddir}/%{glibcsrcdir}/glibc_find_requires.sh | grep -v "\(GLIBC_PRIVATE\|linux-gate\|linux-vdso\)"
exit 0
EOF
chmod +x find_requires.sh

%define __find_provides %{_builddir}/%{glibcsrcdir}/find_provides.sh
%define __find_requires %{_builddir}/%{glibcsrcdir}/find_requires.sh

%if %{build_locales}
mv localedata/SUPPORTED localedata/SUPPORTED.ALL
%if %{build_locales_utf8}
ln -s SUPPORTED.ALL localedata/SUPPORTED
%else
fgrep -v /UTF-8 localedata/SUPPORTED.ALL > localedata/SUPPORTED.NO-UTF-8
ln -s SUPPORTED.NO-UTF-8 localedata/SUPPORTED
%endif # %{build_locales_utf8}
%endif # %{build_locales}


%build
# Prepare test matrix in the next function
CheckList=$PWD/Check.list
rm -f $CheckList
touch $CheckList

# CompareKver <kernel version>
# function to compare the desired kernel version with running kernel
# version (package releases not taken into account in comparison). The
# function returns:
# -1 = <kernel version> is lesser than current running kernel
#  0 = <kernel version> is equal to the current running kernel
#  1 = <kernel version> is greater than current running kernel
#
function CompareKver() {
  v1=`echo $1 | sed 's/\.\?$/./'`
  v2=`uname -r | sed 's/[^.0-9].*//' | sed 's/\.\?$/./'`
  n=1
  s=0
  while true; do
    c1=`echo "$v1" | cut -d "." -f $n`
    c2=`echo "$v2" | cut -d "." -f $n`
    if [ -z "$c1" -a -z "$c2" ]; then
      break
    elif [ -z "$c1" ]; then
      s=-1
      break
    elif [ -z "$c2" ]; then
      s=1
      break
    elif [ "$c1" -gt "$c2" ]; then
      s=1
      break
    elif [ "$c2" -gt "$c1" ]; then
      s=-1
      break
    fi
    n=$((n + 1))
  done
  echo $s
}

#

#
# BuildGlibc <arch> [<extra_configure_options>+]
#
function BuildGlibc() {
    arch="$1"
    shift 1

    cpu="$arch"

    KernelHeaders=$PWD/kernel-headers

    # Select optimization flags and compiler to use
    BuildAltArch="no"
    BuildCompFlags=""
    BuildFlags=""
    case $arch in
        i[3456]86 | athlon)
            BuildFlags="-march=$arch -mtune=generic"
            if [[ "`uname -m`" = "x86_64" ]]; then
                BuildAltArch="yes"
                BuildCompFlags="-m32"
            fi
            ;;
        x86_64)
            BuildFlags="-mtune=generic"
            ;;
    esac

    # Determine C & C++ compilers
    BuildCC="%{__cc} $BuildCompFlags"
    BuildCXX="%{__cxx} $BuildCompFlags"

    BuildFlags="$BuildFlags -DNDEBUG=1 -O2 -finline-functions -g"
    if $BuildCC -v 2>&1 | grep -1 'gcc version 3.0'; then
        # gcc 3.0 had really poor inline heuristics causing problems in resulting ld.so
        BuildFlags="$BuildFlags -finline-limit=2000"
    fi

    # Do not use direct references against %gs when accessing tls data
    # XXX make it the default in GCC? (for other non glibc specific usage)
    case $arch in
        i[3456]86 | x86_64)
            BuildFlags="$BuildFlags -mno-tls-direct-seg-refs"
            ;;
    esac

    # Disable fortify for glibc builds
    BuildFlags="$BuildFlags -U_FORTIFY_SOURCE"

    # Extra configure flags
    %if %{build_profile}
        ExtraFlags="$ExtraFlags --enable-profile"
    %endif

    # NPTL+TLS are now the default
    Pthreads="nptl"
    TlsFlags="--with-tls --with-__thread"

    # Add-ons
    AddOns="$Pthreads,libidn"
    if [[ "$cpu" != "$arch" ]]; then
        BuildFlags="$BuildFlags -mcpu=$cpu"
        ExtraFlags="$ExtraFlags --with-cpu=$cpu"
    fi

    # Don't build with selinux support
    ExtraFlags="$ExtraFlags --without-selinux"

    # Kernel headers directory
    KernelHeaders=$PWD/kernel-headers

    # determine library name
    glibc_cv_cc_64bit_output=no
    if echo ".text" | $BuildCC -c -o test.o -xassembler -; then
        case `/usr/bin/file test.o` in
            *"ELF 64"*)
                glibc_cv_cc_64bit_output=yes
                ;;
        esac
    fi
    rm -f test.o

    # Force a separate and clean object dir
    rm -rf build-$cpu-linux
    mkdir build-$cpu-linux
    pushd build-$cpu-linux
        [[ "$BuildAltArch" = "yes" ]] && touch ".alt" || touch ".main"
        CC="$BuildCC" CXX="$BuildCXX" CFLAGS="$BuildFlags" ../configure \
            $arch-annvix-linux-gnu \
	    --prefix=%{_prefix} \
	    --libexecdir=%{_prefix}/lib \
	    --infodir=%{_infodir} \
	    --enable-add-ons=$AddOns \
	    --without-cvs \
	    $TlsFlags \
	    $ExtraFlags \
	    --enable-kernel=%{enablekernel} \
	    --with-headers=$KernelHeaders ${1+"$@"}
        %make -r PARALLELMFLAGS=-s
    popd

    # All tests are expected to pass on certain platforms
    case $arch in
        i[3456]86 | athlon | x86_64 | ia64 | ppc | ppc64)
            if [ "`CompareKver %{check_min_kver}`" -lt 0 ]; then
                check_flags=""
            else
                check_flags="-k"
            fi
            ;;
        *)
            check_flags="-k"
            ;;
    esac

    # Generate test matrix
    [[ -d "build-$arch-linux" ]] || {
        echo "ERROR: PrepareGlibcTest: build-$arch-linux does not exist!"
        return 1
    }
    local BuildJobs="-j`getconf _NPROCESSORS_ONLN`"
    echo "$BuildJobs -d build-$arch-linux $check_flags" >> $CheckList

    case $cpu in
        i686|athlon)   base_arch=i586;;
        power*)        base_arch=$arch;;
        *)             base_arch=none;;
    esac

    [[ -d "build-$base_arch-linux" ]] && {
        check_flags="$check_flags -l build-$base_arch-linux/elf/ld.so"
        echo "$BuildJobs -d build-$arch-linux $check_flags" >> $CheckList
    }
    return 0
}

# Build main glibc
BuildGlibc %{_target_cpu}

# Build i586 libraries and preserve maximum compatibility
%if %{build_biarch}
BuildGlibc i586
%endif

# Build i686 libraries if not already building for i686/athlon
case %{_target_cpu} in
    i686 | athlon)
        ;;
    i[3-6]86)
        BuildGlibc i686 --disable-profile
        ;;
esac

make -C crypt_blowfish-%{crypt_bf_ver} man

%if %{build_check}
export TMPDIR=/tmp
export TIMEOUTFACTOR=16
Check="$PWD/glibc-check.sh"
cat %{_sourcedir}/glibc-check.sh > $Check
chmod +x $Check
while read arglist; do
    $Check $arglist || exit 1
done < $CheckList
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}
make install_root=%{buildroot} install -C build-%{_target_cpu}-linux
make install_root=%{buildroot} localedata/install-locales -C build-%{_target_cpu}-linux

pushd build-%{_target_cpu}-linux
    %make install_root=%{buildroot} install-locales -C ../localedata objdir=`pwd`
popd
sh manpages/Script.sh

# Empty filelist for non i686/athlon targets
> extralibs.filelist

%if %{build_biarch}
ALT_ARCH=i586-linux
mkdir -p %{buildroot}/$ALT_ARCH
make install_root=%{buildroot}/$ALT_ARCH install -C build-$ALT_ARCH

# dispatch */lib only
mv %{buildroot}/$ALT_ARCH/lib %{buildroot}/
rm -f %{buildroot}/$ALT_ARCH%{_prefix}/lib/pt_chown
mv %{buildroot}/$ALT_ARCH%{_prefix}/lib/getconf/* %{buildroot}%{_prefix}/lib/getconf/
rmdir %{buildroot}/$ALT_ARCH%{_prefix}/lib/getconf
mv %{buildroot}/$ALT_ARCH%{_prefix}/lib/* %{buildroot}%{_prefix}/lib/
rm -rf %{buildroot}/$ALT_ARCH
# XXX Dispatch 32-bit stubs
(sed '/^@/d' include/stubs-prologue.h; LC_ALL=C sort $(find build-$ALT_ARCH -name stubs)) \
> %{buildroot}%{_includedir}/gnu/stubs-32.h
%endif

# Install extra glibc libraries
function InstallGlibc() {
    local BuildDir="$1"
    local SubDir="$2"
    local LibDir="$3"

    case $BuildDir in
    *)      Pthreads=nptl         ;;
    esac

    [[ -z "$LibDir" ]] && LibDir="%{_slibdir}"

    pushd $BuildDir
    mkdir -p %{buildroot}$LibDir/$SubDir/
    install -m 0755 libc.so %{buildroot}$LibDir/$SubDir/`basename %{buildroot}$LibDir/libc-*.so`
    ln -sf `basename %{buildroot}$LibDir/libc-*.so` %{buildroot}$LibDir/$SubDir/`basename %{buildroot}$LibDir/libc.so.*`
    install -m 0755 math/libm.so %{buildroot}$LibDir/$SubDir/`basename %{buildroot}$LibDir/libm-*.so`
    ln -sf `basename %{buildroot}$LibDir/libm-*.so` %{buildroot}$LibDir/$SubDir/`basename %{buildroot}$LibDir/libm.so.*`
    install -m 0755 $Pthreads/libpthread.so %{buildroot}$LibDir/$SubDir/`basename %{buildroot}$LibDir/libpthread-*.so`
    ln -sf `basename %{buildroot}$LibDir/libpthread-*.so` %{buildroot}$LibDir/$SubDir/`basename %{buildroot}$LibDir/libpthread.so.*`
    install -m 0755 ${Pthreads}_db/libthread_db.so %{buildroot}$LibDir/$SubDir/`basename %{buildroot}$LibDir/libthread_db-*.so`
    ln -sf `basename %{buildroot}$LibDir/libthread_db-*.so` %{buildroot}$LibDir/$SubDir/`basename %{buildroot}$LibDir/libthread_db.so.*`
    install -m 0755 rt/librt.so %{buildroot}$LibDir/$SubDir/`basename %{buildroot}$LibDir/librt-*.so`
    ln -sf `basename %{buildroot}$LibDir/librt-*.so` %{buildroot}$LibDir/$SubDir/`basename %{buildroot}$LibDir/librt.so.*`
    echo "%dir $LibDir/$SubDir" >> ../extralibs.filelist
    find %{buildroot}$LibDir/$SubDir -maxdepth 1  -type f -o -type l | sed -e "s|%{buildroot}||" >> ../extralibs.filelist
    popd
}

# Install arch-specific optimized libraries
%ifarch %{ix86}
case %{target_cpu} in
    i[3-5]86)
        InstallGlibc build-i686-linux i686
    ;;
esac
%endif

# NPTL <bits/stdio-lock.h> is not usable outside of glibc, so include
# the generic one (RH#162634)
install -m 0644 bits/stdio-lock.h %{buildroot}%{_includedir}/bits/stdio-lock.h

# Remove the files we don't want to distribute
rm -f %{buildroot}%{_libdir}/libNoVersion*
rm -f %{buildroot}%{_slibdir}/libNoVersion*

ln -sf libbsd-compat.a %{buildroot}%{_libdir}/libbsd.a
%if %{build_biarch}
ln -sf libbbsd-compat.a %{buildroot}%{_prefix}/lib/libbsd.a
%endif

# These man pages require special attention
mkdir -p %{buildroot}%{_mandir}/man3
install -p -m 0644 crypt_blowfish-%{crypt_bf_ver}/*.3 %{buildroot}%{_mandir}/man3/
install -p -m 0644 %{_sourcedir}/strlcpy.3 %{buildroot}%{_mandir}/man3/
echo '.so man3/strlcpy.3' > %{buildroot}%{_mandir}/man3/strlcat.3

install -m 0644 %{_sourcedir}/nsswitch.conf %{buildroot}%{_sysconfdir}/nsswitch.conf

# useless
rm -rf %{buildroot}%{_datadir}/zoneinfo/{posix,right}

# Create default ldconfig configuration file
echo "/usr/local/lib" > %{buildroot}%{_sysconfdir}/ld.so.conf
echo "/usr/X11R6/lib" >> %{buildroot}%{_sysconfdir}/ld.so.conf
if [ "%{_lib}" == "lib64" ]; then
    echo "/usr/local/lib64" >> %{buildroot}%{_sysconfdir}/ld.so.conf
    echo "/usr/X11R6/lib64" >> %{buildroot}%{_sysconfdir}/ld.so.conf
fi
chmod 0644 %{buildroot}%{_sysconfdir}/ld.so.conf
echo "include %{_sysconfdir}/ld.so.conf.d/*.conf" >> %{buildroot}%{_sysconfdir}/ld.so.conf
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d

# ldconfig cache
mkdir -p %{buildroot}%{_var}/cache/ldconfig
touch %{buildroot}%{_var}/cache/ldconfig/aux-cache

# Include %{_libdir}/gconv/gconv-modules.cache
> %{buildroot}%{_libdir}/gconv/gconv-modules.cache
chmod 0644 %{buildroot}%{_libdir}/gconv/gconv-modules.cache

# Strip libpthread but keep some symbols
find %{buildroot}%{_slibdir} -type f -name "libpthread-*.so" | \
    xargs strip -g -R .comment

%if %{build_biarch}
find %{buildroot}/lib -type f -name "libpthread-*.so" | \
    xargs strip -g -R .comment
%endif

# Strip debugging info from all static libraries
pushd %{buildroot}%{_libdir}
    for i in *.a; do
        if [ -f "$i" ]; then
            case "$i" in
                *_p.a) ;;
                *) strip -g -R .comment $i ;;
            esac
        fi
    done
popd

# rquota.x and rquota.h are now provided by quota
rm -f %{buildroot}%{_includedir}/rpcsvc/rquota.[hx]

# hardlink identical locale files together
gcc -O2 -o build-%{_target_cpu}-linux/hardlink redhat/hardlink.c
build-%{_target_cpu}-linux/hardlink -vc %{buildroot}%{_datadir}/locale

install -m 0644 nscd/nscd.conf %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_srvdir}/nscd/log
install -m 0740 %{_sourcedir}/nscd.run %{buildroot}%{_srvdir}/nscd/run
install -m 0740 %{_sourcedir}/nscd-log.run %{buildroot}%{_srvdir}/nscd/log/run
install -m 0740 %{_sourcedir}/nscd.finish %{buildroot}%{_srvdir}/nscd/finish
mkdir -p %{buildroot}/var/{db/nscd,run/nscd}

rm -rf %{buildroot}%{_datadir}/zoneinfo
rm -rf %{buildroot}%{_includedir}/netatalk/

# these are in the timezone package
rm -f %{buildroot}%{_sbindir}/{zdump,zic}
rm -f %{buildroot}%{_sysconfdir}/localtime

# Build file list for devel package
find %{buildroot}%{_includedir} -type f -or -type l > devel.filelist
find %{buildroot}%{_includedir} -type d  | sed "s/^/%dir /" | \
    grep -v "%{_libdir}/libnss1.*.so$" | \
    grep -v "%{_includedir}$" | >> devel.filelist
find %{buildroot}%{_libdir} -maxdepth 1 -name "*.so" -o -name "*.o" | egrep -v "(libmemusage.so|libpcprofile.so)" >> devel.filelist
# biarch libs
%if %{build_biarch}
find %{buildroot}%{_prefix}/lib -maxdepth 1 -name "*.so" -o -name "*.o" | egrep -v "(libmemusage.so|libpcprofile.so)" >> devel.filelist
%endif
perl -pi -e "s|%{buildroot}||" devel.filelist


# Copy Kernel-Headers
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}/boot/
cp -avrf kernel-headers/* %{buildroot}%{_includedir}
echo "#if 0" > %{buildroot}/boot/kernel.h-%{kheaders_ver}

# The last bit: more documentation
rm -rf documentation
mkdir documentation
cp ChangeLog* documentation
bzip2 -9qf documentation/ChangeLog*
mkdir documentation/crypt_blowfish-%{crypt_bf_ver}
cp crypt_blowfish-%{crypt_bf_ver}/{README,LINKS,PERFORMANCE} \
    documentation/crypt_blowfish-%{crypt_bf_ver}

# we only want to keep locale.alias; the rest of the locales are in our locales package
mkdir %{buildroot}%{_datadir}/locale.bk
mv -f %{buildroot}%{_datadir}/locale/locale.alias %{buildroot}%{_datadir}/locale.bk/
rm -rf %{buildroot}%{_datadir}/locale
mv %{buildroot}%{_datadir}/locale.bk %{buildroot}%{_datadir}/locale

# Generate final rpm filelist, with localized libc.mo files
rm -f rpm.filelist
%find_lang libc
perl -ne '/^\s*$/ or print' libc.lang > rpm.filelist
cat extralibs.filelist >> rpm.filelist

# Final step: remove unpackaged files.
rm -f  %{buildroot}%{_infodir}/dir.old*
rm -f  %{buildroot}%{_prefix}/lib/pt_chown
rm -rf %{buildroot}%{_includedir}/asm-*/mach-*/

EXCLUDE_FROM_STRIP="ld-%{version}.so libpthread $DEBUG_LIBS"
export EXCLUDE_FROM_STRIP


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


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
%if %isarch x86_64
if [ -L %{_includedir}/asm-x86_64 ]; then
    rm -f %{_includedir}/asm-x86_64
fi
if [ -L %{_includedir}/asm-i386 ]; then
    rm -f %{_includedir}/asm-i386
fi
%endif
exit 0


%post devel
%_install_info libc.info
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


%preun devel
%_remove_install_info libc.info


%pre -n nscd
%_pre_useradd nscd / /bin/false 83


%post -n nscd
%_post_srv nscd


%preun -n nscd
%_preun_srv nscd


%postun -n nscd
%_postun_userdel nscd
if [ "$1" -ge "1" ]; then
    /usr/sbin/srv --restart nscd > /dev/null 2>&1 || :
fi


#
# glibc
#
%files -f rpm.filelist
%defattr(-,root,root)
# configs
%config(noreplace) %verify(not size md5 mtime) /etc/nsswitch.conf
%config(noreplace) %verify(not size md5 mtime) /etc/ld.so.conf
%dir %{_sysconfdir}/ld.so.conf.d
%config(noreplace) %{_sysconfdir}/rpc
%{_mandir}/man1/*
%{_mandir}/man8/rpcinfo.8*
%{_mandir}/man8/ld.so*
%{_datadir}/locale/locale.alias
/sbin/sln
%dir %{_prefix}/lib/getconf
%{_prefix}/lib/getconf/*
%{_slibdir}/ld-%{version}.so
%ifarch %{ix86}
%{_slibdir}/ld-linux.so.2
%endif
%ifarch x86_64
%{_slibdir}/ld-linux-x86-64.so.2
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
#%{_bindir}/glibcbug
%{_bindir}/iconv
%{_bindir}/ldd
%ifarch %{ix86}
%{_bindir}/lddlibc4
%endif
%{_bindir}/locale
%{_bindir}/localedef
%{_bindir}/rpcgen
%{_bindir}/sprof
%{_bindir}/tzselect
%{_sbindir}/rpcinfo
%{_sbindir}/iconvconfig

%if %{build_biarch}
%{_slibdir32}/ld-%{version}.so
%{_slibdir32}/ld-linux*.so.2
%{_slibdir32}/lib*-[.0-9]*.so
%{_slibdir32}/lib*.so.[0-9]*
%{_slibdir32}/libSegFault.so
%dir %{_prefix}/lib/gconv
%{_prefix}/lib/gconv/*
%endif
#
# ldconfig
#
%defattr(-,root,root)
/sbin/ldconfig
%{_mandir}/man8/ldconfig*
%ghost %{_sysconfdir}/ld.so.cache
%dir %{_var}/cache/ldconfig
%ghost %{_var}/cache/ldconfig/aux-cache


#
# glibc-utils
#
%files utils
%defattr(-,root,root)
%if %{build_biarch}
%{_slibdir32}/libmemusage.so
%{_slibdir32}/libpcprofile.so
%endif
%{_slibdir}/libmemusage.so
%{_slibdir}/libpcprofile.so
%{_bindir}/memusage
%{_bindir}/memusagestat
%{_bindir}/mtrace
%{_bindir}/pcprofiledump
%{_bindir}/xtrace


#
# glibc-devel
#
%files devel -f devel.filelist
%defattr(-,root,root)
%{_libdir}/libbsd-compat.a
%{_libdir}/libbsd.a
%{_libdir}/libc_nonshared.a
%{_libdir}/libg.a
%{_libdir}/libieee.a
%{_libdir}/libmcheck.a
%{_libdir}/libpthread_nonshared.a
%{_libdir}/librpcsvc.a
%{_includedir}/linux
%{_includedir}/asm
%{_includedir}/asm-generic
%{_includedir}/mtd
%{_includedir}/rdma
%{_includedir}/sound
%{_includedir}/video
%ifarch x86_64
%dir %{_includedir}/asm-i386
%{_includedir}/asm-i386/*.h
%dir %{_includedir}/asm-x86_64
%{_includedir}/asm-x86_64/*.h
%endif
/boot/kernel.h-%{kheaders_ver}
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
%{_mandir}/man3/*
%{_infodir}/libc.info*


#
# glibc-static-devel
#
%files static-devel
%defattr(-,root,root)
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
# glibc-profile
#
%if %{build_profile}
%files profile
%defattr(-,root,root)
%{_libdir}/lib*_p.a
%if %{build_biarch}
%{_prefix}/lib/lib*_p.a
%endif
%endif


#
# glibc-i18ndata
#
%files i18ndata
%defattr(-,root,root)
%dir %{_datadir}/i18n
%dir %{_datadir}/i18n/charmaps
%{_datadir}/i18n/charmaps/*
%dir %{_datadir}/i18n/locales
%{_datadir}/i18n/locales/*


#
# nscd
#
%files -n nscd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nscd.conf
%{_sbindir}/nscd
%dir %attr(0750,root,admin) %{_srvdir}/nscd
%dir %attr(0750,root,admin) %{_srvdir}/nscd/log 
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nscd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nscd/finish
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nscd/log/run  
%attr(0700,root,root) /var/db/nscd
%attr(0755,root,root) /var/run/nscd


%files doc
%defattr(-,root,root)
%doc README* NEWS* INSTALL* FAQ* BUGS NOTES* PROJECTS CONFORMANCE
%doc COPYING COPYING.LIB
%doc documentation/* README.libm
%doc hesiod/README.hesiod
%doc crypt/README.ufc-crypt


%changelog
* Sat Dec 08 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.1
- 2.6.1
- don't include /etc/localtime in the file list; the timezone package
  will take care of keeping it up to date
- update to 2.6.22-3mdv kernel headers
- drop P500, P502, P602 due to the updated headers
- drop P100-P138, all merged upstream
- drop P302: don't worry about ALT's info policy
- drop P330: we use /var/db for nscd storage, not /var/lib
- drop P500: no longer required
- drop P602: kernel headers have audit support now
- rediff P301, P319, P324, P327
- updated P505 from Mandriva
- P0-P24: various fixes from upstream (synced to Mandriva 2.6.1-4mdv)
- P506: patch from Mandriva, from SUSE, rediffed against our 2.6.1, 
  to speed up ldconfig
- build libidn support
- replace S1 with the redhat equivalent
- increase minimum buildreq version on binutils, to 2.16.91.0.7 so that
  we have a suitable linker for -Wl,--hash-style=both
- provide rtld(GNU_HASH)
- use Mandriva's CompareKver() function to test if we can successfully
  run tests with the current running kernel
- add -mtune=generic to the BuildFlags
- ldconfig's cache is now in /var/cache/ldconfig/
- libmemusage.so and libpcprofile.so are now in /lib(64)
- enable %%build_check by default

* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- rebuild with new binutils

* Thu Sep 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- P602: somehow the elf-em.h part got dropped in an update, which prevents
  audit from building so put it back

* Thu Sep 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- P604: don't enable host caching by default in nscd.conf

* Wed Sep 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- add missing directories for nscd to work properly

* Mon Jun 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- 2.5-20061008T1257
- merge with RHEL 2.5-12 and ALT's 2.5-alt4 (essentially replaced all
  non-Annvix patches with these, and use the RHEL source)
- drop linuxthreads support, NPTL+TLS is default now
- drop support for non x86/x86_64 archs
- P603: crypt_blowfish patch for glibc 2.4 (rediffed from the
  crypt_blowfish package)
- use kernel headers 2.6.17
- P504: set FHS paths (Mandriva)
- P505: filter out multiarch headers in check-local-headers.sh (Mandriva)
- put ldconfig in the main glibc package
- buildrequires: gd-devel
- use info_install macros
- drop S8, S9

* Sat Mar 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- don't build the timezone package anymore

* Thu Feb 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- apply P2 to fix the segfault in ctermid

* Thu Feb 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- do some conditional testing before removing directories or, if they don't
  exist, rpm will fail in a really silly place
- enable %%clean again

* Mon Jan 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- fix the private find-requires.sh; we don't want linux-gate.so.1 showing up
- remove snapshot support/macros

* Sun Jan 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- fix nsswitch.conf (local lookups should always come before LDAP lookups)

* Tue Dec 26 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- update and execline the nscd run script

* Tue Aug 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- P602: update audit.h and add elf-em.h so that audit can compile

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- devel package needs coreutils for rm and ln
- spec cleanups

* Thu Jul 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- S11: install and use our own nsswitch.conf; tcb is now the default
- start using the new %%{_sourcedir}/file instead of %%{SOURCEx} convention

* Thu Jul 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- drop P202 and revert the changes to P400; after working with Solar we
  found the real problem (need to increase BF_FRAME)
- put back our relocate fcrypt patch as P600
- P601: increase BF_FRAME and BF_CLEAN

* Mon Jul 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- update P202 to include some missing bits
- fix P400 to go with P202

* Mon Jul 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- 2.3.6
- sync patches with openwall 2.3.6-owl6:
  - Backported configure fix: compile source test files with -fPIC for -shared (ldv)
  - Backported linuxthreads x86-64 asm syntax corrections (ldv)
  - Backported ctermid declaration fix (ldv)
  - Backported upstream patch to fix build with new GNU assembler (ldv)
  - Applied upstream linuxthreads ix86 TLS fix (ldv)
  - Fixed ldd error reporting on multilib platforms like x86-64 (ldv)
  - Fixed "ldd -u" (ldv)
  - Corrected a bug in the way salts for extended DES-based and for MD5-based
    hashes are generated; thanks to Marko Kreen for discovering this (solar)
  - Imported a patch from Gentoo (re-generated from glibc234-alpha-xstat.patch)
    to re-introduce support for building on Alpha with pre-2.6.4 kernel headers (solar)
- crypt_blowfish 1.0.2
- drop P505; integrated upstream
- P202: from SUSE to properly integrate crypt_blowfish (now it works!)
- drop P506; P202 accomplishes the same thing and more
- update P400 so it applies with the suse P202
- renumber the mdk/avx patches
- fix permissions for */lib/*.so
- fix some prereq's

* Wed Jun 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- some x86_64 include file fixes

* Mon Jun 26 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- grab the kernel 2.6.16 headers from Mandriva's glibc and use it instead
  of the 2.4 headers
- include and update appropriate patches for new kernel headers

* Sat May 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- P507: make locale know that it's stuff is in %%{_datadir}/locale rather
  than %%{_prefix}/lib/locale (we had this patch before but it was dropped
  when we moved to track owl instead of mandriva)

* Sat May 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- rebuild the toolchain against itself (gcc/glibc/libtool/binutils)

* Fri May 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- rebuild against gcc 4.0.3 (NOTE: the fedora patch (P100) already includes
  FORITFY support)
- add -doc subpackage
- P505: fix build with gcc4 (from mandriva)
- crypt_blowfish 1.0.1
- P506: relocate fcrypt definition from crypt-entry.c to crypt_blowfish's
  wrapper.c to enable gcc4 build

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- crypt_blowfish 1.0 (minor security fixes)
- fix prereq

* Fri Dec 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- uncompress patches
- reorder SSP patches and include the original SSP patch (P500); this
  doesn't integrate as nicely as it does for OpenBSD, HLFS, or Hardened
  Gentoo but it will suffice for now
- obfuscate email addresses

* Sun Oct 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5-6avx
- fix call to srv
- fix path to find-provides (/usr/lib/rpm/annvix/find-provides) so
  that the devel(foo) provides get generated properly

* Mon Sep 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5-5avx
- use execlineb for run scripts
- move logdir to /var/log/service/nscd
- run scripts are now considered config files and are not replaceable
- use kernel 2.4.31-2avx headers

* Sat Aug 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5-4avx
- fix perms on run scripts

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5-3avx
- bootstrap build

* Tue Aug 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5-2avx
- include the /usr/X11R6/lib* directories in ld.so.conf
- in the merge forgot to build the x86 libs for x86_64
- add back the BuildGlibc() function to properly build our libs

* Sat Jul 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5-1avx
- 2.3.5
- merge with openwall 2.3.5-5owl
- P500-502 from HLFS; updates for -fstack-protector, SSP, and arc4random
  but disabled for now since enabling SSP seems to break the glibc
  build
- redefine the location of %%{_libexecdir} so it matches Owl's
- for some reason the devel.filelist isn't being created properly so
  specify it all in %%files

* Thu Jun 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-27avx
- build with -fno-stack-protector; we have to build glibc unprotected
  until we upgrade to 2.3.4 now that we're moving everything from
  libgcc to libc

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-26avx
- user logger for logging

* Fri Jan 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-25avx
- P44: add SSP/frandom support from HLFS
- P102: updated sysctl.h which includes [ef]random

* Mon Dec 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-24avx
- P43: patch from Trustix to fix CAN-2004-0968

* Sat Sep 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-23avx
- update run scripts
- give nscd a finish script
- s/mandrake/annvix/
- make tests are failing on both x86 and x86_64 so build
  --without check for now
- remove the heap-protection patch since we're not using it

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-22avx
- x86_64 needs /usr/local/lib64 also

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-21avx
- Annvix build
- require packages not files
- put "/usr/local/lib" into ld.so.conf by default

* Tue Apr 13 2004 Vincent Danen <vdanen@opensls.org> 2.3.2-20sls
- fix requires for epoch

* Wed Feb 24 2004 Vincent Danen <vdanen@opensls.org> 2.3.2-19sls
- new build option: build_heapprot which enables or disables heap
  protection; for now we disable it until the author can get it fixed on
  amd64

* Sun Feb 08 2004 Vincent Danen <vdanen@opensls.org> 2.3.2-18sls
- include glibc heap protection (P43); currently unapplied
- remove %%build_opensls macros
- remove initscript for nscd; supervise scripts
- srv macros
- disable %%build_check due to a heap overflow in malloc.c when doing the
  linuxthreads test
- only include heap protection on x86 for now (problems with amd64 compile)

* Tue Dec 23 2003 Vincent Danen <vdanen@opensls.org> 2.3.2-17sls
- update kernel headers to 2.4.23-0.rc5.2mdk
- don't build doc, pdf-doc, or utils

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.3.2-16sls
- OpenSLS build
- P41: propolice patch; use %%build_opensls macros

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
