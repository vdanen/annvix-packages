#
# spec file for package glibc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

#define _unpackaged_files_terminate_build 0

# owl 2.3.5-owl5
%define basevers	2.3.5
#%%define snapshot	20050427
%define crypt_bf_ver	1.0.1

%define revision	$Rev$
%define name		glibc
%define version		%{basevers}%{?snapshot:.%snapshot}
%define release		%_revrel
%define epoch		6

# <version>-<release> tags from kernel package where headers were
# actually extracted from
%define kheaders_ver    2.4.31
%define kheaders_rel    2avx

%define build_check	0
%define build_profile	1
%define build_locales	1
%define build_locales_utf8 0

%define build_biarch	0
%ifarch x86_64
%define build_biarch	1
%endif

%define _slibdir	/%{_lib}

# define architectures acceping glibc-compat
%define glibc_compat_arches %{ix86} alpha alphaev6 sparc sparcv9
%define arch		%(echo %{_target_cpu}|sed -e "s/i.86/i386/" -e "s/athlon/i386/" -e "s/amd64/x86_64/")

Summary:	The GNU libc libraries
Name:		%{name}
Version: 	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	LGPL
Group:		System/Libraries
URL:		http://www.gnu.org/software/libc/

Source0:	ftp://ftp.gnu.org/gnu/%{name}/glibc-%{basevers}%{?snapshot:-%snapshot}.tar.bz2
%if %{?snapshot:0}%{!?snapshot:1}
Source1:	ftp://ftp.gnu.org/gnu/%{name}/glibc-linuxthreads-%{basevers}.tar.bz2
Source2:	ftp://ftp.gnu.org/gnu/%{name}/glibc-libidn-%{basevers}.tar.bz2
%endif
Source3:	crypt_blowfish-%{crypt_bf_ver}.tar.gz
Source4:	crypt_freesec.c
Source5:	crypt_freesec.h
Source6:	strlcpy.3
Source7:	glibc-manpages.tar.bz2
Source8:	glibc-redhat.tar.bz2
Source9:	glibc-compat.tar.bz2
Source10:	glibc-find-requires.sh
Source14:       nscd.run
Source15:       nscd-log.run
Source16:       nscd.finish
# Generated from Kernel-RPM
Source20:       kernel-headers-%{kheaders_ver}.%{kheaders_rel}.tar.bz2
Source21:       make_versionh.sh
Source22:       create_asm_headers.sh

# Patches
# -------
# We are using the following numbering rules for glibc patches:
#    0-99 - CVS
# 100-199 - RH
# 200-299 - SuSE
# 300-399 - ALT
# 400-499 - Owl
# 500-599 - Annvix
# CVS
Patch0:		glibc-2.3.5-cvs-20050427-2_3-branch.diff
Patch1:		glibc-2.3.5-cvs-20050427-canonicalize.diff
# RH
Patch100:	glibc-2.3.5-fedora.diff
# SuSE
Patch200:	glibc-2.3.2-suse-resolv-response-length.diff
Patch201:	glibc-2.3.4-suse-getconf-default_output.diff
# ALT
Patch300:	glibc-2.3.5-alt-doc-linuxthreads.diff
Patch301:	glibc-2.3.5-alt-string2.diff
Patch302:	glibc-2.3.5-alt-sys-mount.diff
Patch303:	glibc-2.3.5-openbsd-alt-sys-queue.diff
Patch304:	glibc-2.3.5-alt-getopt-optind.diff
Patch305:	glibc-2.3.5-alt-fts_palloc-cleanup.diff
Patch306:	glibc-2.3.5-alt-asprintf.diff
Patch307:	glibc-2.3.5-alt-libio-bound.diff
Patch308:	glibc-2.3.5-openbsd-strlcpy-strlcat.diff
Patch309:	glibc-2.3.5-alt-iconv_prog-replace.diff
Patch310:	glibc-2.3.5-alt-i18n.diff
Patch311:	glibc-2.3.5-alt-relocate-helper-libs.diff
Patch312:	glibc-2.3.5-alt-linux-dl-execstack.diff
Patch313:	glibc-2.3.5-alt-assume_kernel.diff
# Owl
Patch400:	glibc-2.3.3-owl-crypt_freesec.diff
Patch401:	glibc-2.3.5-owl-alt-res_randomid.diff
Patch402:	glibc-2.3.2-owl-iscntrl.diff
Patch403:	glibc-2.3.2-owl-quota.diff
Patch404:	glibc-2.3.5-owl-alt-ldd.diff
Patch405:	glibc-2.3.3-owl-info.diff
Patch406:	glibc-2.3.5-owl-alt-syslog-ident.diff
Patch407:	glibc-2.3.5-mjt-owl-alt-syslog-timestamp.diff
Patch408:	glibc-2.3.5-owl-alt-resolv-QFIXEDSZ-underfills.diff
Patch409:	glibc-2.3.2-owl-tmpfile.diff
Patch410:	glibc-2.3.3-owl-tmp-scripts.diff
Patch411:	glibc-2.3.3-owl-rpcgen-cpp.diff
Patch412:	glibc-2.3.5-owl-alt-sanitize-env.diff
# Annvix / Mandriva
Patch500:	glibc-2.3.5-avx-ssp.patch
Patch501:	glibc-2.3.5-fstack_protector-1.patch
Patch502:	glibc-2.3.5-arc4random-1.patch
Patch503:	glibc-2.3.5-ssp-1.patch
Patch503:       kernel-headers-include-%{kheaders_ver}.%{kheaders_rel}.patch
Patch504:       kernel-headers-%{kheaders_ver}.%{kheaders_rel}-gnu-extensions.patch
Patch505:	glibc-2.3.5-gcc4.patch
Patch506:	glibc-2.3.5-avx-relocate_fcrypt.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	patch, gettext, perl, autoconf2.5
BuildRequires:	binutils >= 2.13.90.0.18-2mdk
BuildPreReq:	gcc >= 3.1.1

AutoReq:	false
#Requires: /etc/nsswitch.conf
Provides:	glibc-crypt_blowfish = %{crypt_bf_ver}
Provides:	glibc-localedata
Provides:	ld.so
Obsoletes:      zoneinfo, libc-static, libc-devel, libc-profile, libc-headers,
Obsoletes:      linuxthreads, gencat, locale, glibc-localedata
Obsoletes:	ld.so
PreReq:		ldconfig

%description
The glibc package contains standard libraries which are used by
multiple programs on the system.  In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs.  This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library.  Without these two libraries, a
Linux system will not function.  The glibc package also contains
national language (locale) support and timezone databases.


%package -n ldconfig
Summary:	Creates a shared library cache and maintains symlinks for ld.so
Group:		System/Base

%description -n ldconfig
Ldconfig is a basic system program which determines run-time link
bindings between ld.so and shared libraries. Ldconfig scans a running
system and sets up the symbolic links that are used to load shared
libraries properly. It also creates a cache (/etc/ld.so.cache) which
speeds the loading of programs which use shared libraries.


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
Conflicts:	kernel < 2.2.0
Requires(pre):	rpm-helper
Requires(preun): rpm-helper, srv
Requires(post):	rpm-helper, srv
Requires(postun): rpm-helper, srv
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


%package -n timezone
Summary:	Time zone descriptions
Group:		System/Base
Conflicts:	glibc < 2.2.5-6mdk

%description -n timezone
These are configuration files that describe possible
time zones.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q %{!?snapshot:-a 1 -a 2} -a 3 -a 7 -a 8 -a 9 -a 20 -n %{name}-%{basevers}%{?snapshot:-%snapshot}

# CVS
# 20050427-2_3-branch
%patch0 -p0

# fix realpath(3) to return NULL and set errno to ENOTDIR for such
# pathnames like "/path/to/existing-non-directory/"
%patch1 -p0

# RH
# usual glibc-fedora.patch
%patch100 -p0

# SuSE
# avoid read buffer overruns in apps using res_* calls
%patch200 -p1
# add -a option to getconf(1)
%patch201 -p0

# ALT
# fix linuxthreads documentation
%patch300 -p1
# fix -Wpointer-arith issue in string2.h
%patch301 -p1
# fix sys/mount.h for gcc -pedantic support
%patch302 -p1
# backport sys/queue.h from OpenBSD
%patch303 -p1
# set proper optind when argc < 1
%patch304 -p1
# minor io/fts.c cleanup
%patch305 -p1
# change asprintf/vasprintf error handling
%patch306 -p1
# check for potential integer overflow in fread*/fwrite*
%patch307 -p1
# import strlcpy/strlcat from OpenBSD
%patch308 -p1
# add "--replace" option to iconv utility
%patch309 -p1
# support more ru_* locales
%patch310 -p1
# relocate helper libraries from /lib to %{_libdir}
%patch311 -p1
# fix mprotect return code handling in _dl_make_stack_executable()
%patch312 -p1
# fix _dl_osversion_init(), _dl_non_dynamic_init() and
# dl_main() functions to not assume too old kernel version
%patch313 -p1

# Owl
echo "Applying crypt_blowfish patch:"
patch -p1 -s < crypt_blowfish-%{crypt_bf_ver}/glibc-2.3.2-crypt.diff
mv crypt/{crypt.h,gnu-crypt.h}
mv crypt_blowfish-%{crypt_bf_ver}/*.[chS] crypt/
cp %_sourcedir/crypt_freesec.[ch] crypt/

# FreeSec support for extended/new-style/BSDI hashes in crypt(3)
%patch400 -p1
# improve res_randomid in the resolver
%patch401 -p1
# force known control characters for iscntrl(3)
%patch402 -p1
# sync quota.h with current kernel
%patch403 -p1
# always execute traced object directly with dynamic linker
%patch404 -p1
# fix libc's info formatting
%patch405 -p1
# don't blindly trust __progname for the syslog ident
%patch406 -p1
# use ctime_r() instead of strftime_r() in syslog(3)
%patch407 -p1
# avoid potential reads beyond end of undersized DNS responses
%patch408 -p1
# allow tmpfile(3) to use TMPDIR environment variable
%patch409 -p1
# fix temporary file handling in the scripts
%patch410 -p1
# avoid hardcoding of cpp binary, use execvp instead of execv
%patch411 -p1
# sanitize the environment in a paranoid way
%patch412 -p1

# Annvix
#%patch500 -p1 -b .ssp
#%patch501 -p1 -b .fstack-protector
#%patch502 -p1 -b .arc4random
#%patch503 -p1 -b .ssp
%patch505 -p1 -b .gcc4
%patch506 -p1 -b .relocate_fcrypt

pushd kernel-headers/
TARGET=%{_target_cpu}
%patch503 -p1
%patch504 -p1
%{expand:%(%__cat %{SOURCE21})}
%{expand:%(%__cat %{SOURCE22})}
popd

%ifnarch %{glibc_compat_arches}
    rm -rf glibc-compat
%endif

find . -type f -size 0 -o -name '*.orig' -exec rm -f {} \;

cat > find_provides.sh << EOF
#!/bin/sh
/usr/lib/rpm/annvix/find-provides | grep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_provides.sh
cat %{SOURCE10} >glibc_find_requires.sh
chmod +x glibc_find_requires.sh
cat > find_requires.sh << EOF
#!/bin/sh
%{_builddir}/%{name}-%{version}/glibc_find_requires.sh | grep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_requires.sh

%define __find_provides %{_builddir}/%{name}-%{basevers}%{?snapshot:-%snapshot}/find_provides.sh
%define __find_requires %{_builddir}/%{name}-%{basevers}%{?snapshot:-%snapshot}/find_requires.sh

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
#
# BuildGlibc <arch> [<extra_configure_options>+]
#
function BuildGlibc() {
    arch="$1"
    shift 1

    KernelHeaders=$PWD/kernel-headers
    # set a minimal kernel version
    EnableKernel=2.4.0

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
    # Temporarily don't do this on ia64, s390, and ppc
    case $arch in
        ia64 | s390 | s390x | ppc)
            ;;
        *)
            BuildFlags="$BuildFlags -freorder-blocks"
            ;;
    esac

    BuildFlags="$BuildFlags -DNDEBUG=1 -O2 -finline-functions -g"
    if $BuildCC -v 2>&1 | grep -1 'gcc version 3.0'; then
        # gcc 3.0 had really poor inline heuristics causing problems in resulting ld.so
        BuildFlags="$BuildFlags -finline-limit=2000"
    fi

    # FIXME: don't use unit at time compilation
    if $BuildCC -funit-at-a-time -S -o /dev/nulll -xc /dev/null 2>&1; then
        BuildFlags="$BuildFlags -fno-unit-at-a-tiome"
    fi

    %if !%{build_profile}
        ExtraFlags="--disable-profile"
    %endif

    %ifarch %{glibc_compat_arches}
        ADDONS=",glibc-compat"
    %endif

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

    case $arch:$glibc_cv_cc_64bit_output in
        powerpc64:yes | s390x:yes  | sparc64:yes | x86_64:yes | amd64:yes)
            glibc_libname="lib64"
            ;;
        *:*)
            glibc_libname="lib"
            ;;
    esac

    # Force a separate and clean object dir
    rm -rf build-$arch-linux
    mkdir build-$arch-linux
    pushd build-$arch-linux
        CC="$BuildCC" CFLAGS="$BuildFlags" ../configure \
            $arch-annvix-linux-gnu \
	    --prefix=%{_prefix} \
	    --exec-prefix=%{_exec_prefix} \
	    --bindir=%{_bindir} \
	    --sbindir=%{_sbindir} \
	    --sysconfdir=%{_sysconfdir} \
	    --datadir=%{_datadir} \
	    --includedir=%{_includedir} \
	    --libdir="%{_prefix}/$glibc_libname" \
	    --libexecdir="%{_prefix}/$glibc_libname" \
	    --localstatedir=%{_localstatedir} \
	    --sharedstatedir=%{_sharedstatedir} \
	    --mandir=%{_mandir} \
	    --infodir=%{_infodir} \
	    --enable-add-ons=linuxthreads,libidn$ADDONS \
	    --without-cvs \
	    --without-__thread \
	    $ExtraFlags \
	    --enable-kernel=$EnableKernel \
	    --with-headers=$KernelHeaders ${1+"$@"}
        %make -r CFLAGS="$BuildFlags" PARALLELMFLAGS=
    popd
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


make -C linuxthreads/man
make -C crypt_blowfish-%{crypt_bf_ver} man

BUILD_CHECK=
%if %{build_check}
BUILD_CHECK=yes
%endif
if [[ -n "$BUILD_CHECK" ]]; then
    echo "========== TESTING =========="
    # All tests must pass on x86, x86_64, ia64, and ppc
    %ifarch %{ix86} x86_64 ia64 ppc
    %make -C build-%{_target_cpu}-linux check PARALLELMFLAGS=-s
    case `uname -m` in
        i686 | athlon) ALT_ARCH=i686 ;;
        x86_64)        ALT_ARCH=i586 ;;
    esac
    [[ -n "$ALT_ARCH" && -d "build-$ALT_ARCH-linux" ]] &&
        %make -C build-$ALT_ARCH-linux check PARALLELMFLAGS=-s
    %else
    %make -C build-%{_target_cpu}-linux -k check PARALLELMFLAGS=-s \
        || echo make check failed
    %endif
    echo "======== TESTING END ========"
fi


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}
make install_root=%{buildroot} install -C build-%{_target_cpu}-linux
make install_root=%{buildroot} localedata/install-locales -C build-%{_target_cpu}-linux

pushd build-%{_target_cpu}-linux
    %make install_root=%{buildroot} install-locales -C ../localedata objdir=`pwd`
popd
sh manpages/Script.sh

%if %{build_biarch}
ALT_ARCH=i586-linux
mkdir -p %{buildroot}/$ALT_ARCH
make install_root=%{buildroot}/$ALT_ARCH install -C build-$ALT_ARCH
pushd build-$ALT_ARCH
    %make -C ../localedata objdir=`pwd` \
        install_root=%{buildroot}/$ALT_ARCH \
        install-locales
popd
# dispatch */lib only
mv %{buildroot}/$ALT_ARCH/lib %{buildroot}/
mv %{buildroot}/$ALT_ARCH%{_prefix}/lib %{buildroot}%{_prefix}/
rm -rf %{buildroot}/$ALT_ARCH
%endif


# These man pages require special attention
mkdir -p %{buildroot}%{_mandir}/man3
install -p -m 0644 linuxthreads/man/*.3thr %{buildroot}%{_mandir}/man3/
install -p -m 0644 crypt_blowfish-%{crypt_bf_ver}/*.3 %{buildroot}%{_mandir}/man3/
install -p -m 0644 %_sourcedir/strlcpy.3 %{buildroot}%{_mandir}/man3/
echo '.so man3/strlcpy.3' > %{buildroot}%{_mandir}/man3/strlcat.3

install -m 0644 redhat/nsswitch.conf %{buildroot}%{_sysconfdir}/nsswitch.conf

ln -s libbsd-compat.a %{buildroot}%{_libdir}/libbsd.a
%if %{build_biarch}
ln -s libbbsd-compat.a %{buildroot}%{_prefix}/lib/libbsd.a
%endif

# Relocate shared libraries used by catchsegv, memusage and xtrace
mv %{buildroot}/%{_lib}/lib{memusage,pcprofile,SegFault}.so %{buildroot}%{_libdir}/
%if %{build_biarch}
rm -f %{buildroot}/lib/lib{memusage,pcprofile}.so
%endif

# Replace the symlink with the file for our default timezone - use UTC
rm %{buildroot}/etc/localtime
cp -a %{buildroot}%{_datadir}/zoneinfo/UTC %{buildroot}/etc/localtime

# Create default ldconfig configuration file
echo "/usr/local/lib" > %{buildroot}%{_sysconfdir}/ld.so.conf
echo "/usr/X11R6/lib" >> %{buildroot}%{_sysconfdir}/ld.so.conf
if [ "%{_lib}" == "lib64" ]; then
    echo "/usr/local/lib64" >> %{buildroot}%{_sysconfdir}/ld.so.conf
    echo "/usr/X11R6/lib64" >> %{buildroot}%{_sysconfdir}/ld.so.conf
fi
chmod 0644 %{buildroot}%{_sysconfdir}/ld.so.conf
echo "include /etc/ld.so.conf.d/*.conf" >> %{buildroot}/etc/ld.so.conf
mkdir -m 0755 %{buildroot}/etc/ld.so.conf.d

# Truncate /etc/ld.so.cache, we'll create it in the %%post section
echo -n > %{buildroot}/etc/ld.so.cache

# The database support
# XXX: why is this disabled?
#mkdir -p %{buildroot}/var/db
#install -m 644 nss/db-Makefile %{buildroot}/var/db/Makefile

# Do not package obsolete pt_chown helper
rm -f %{buildroot}%{_libdir}/pt_chown
[[ -f %{buildroot}%{_prefix}/lib/pt_chown ]] && rm -f %{buildroot}%{_prefix}/lib/pt_chown

# rquota.x and rquota.h are now provided by quota
rm -f %{buildroot}%{_includedir}/rpcsvc/rquota.[hx]

gcc -O2 -o build-%{_target_cpu}-linux/hardlink redhat/hardlink.c
build-%{_target_cpu}-linux/hardlink -vc %{buildroot}%{_datadir}/locale

install -m 0644 nscd/nscd.conf %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_srvdir}/nscd/log
install -m 0740 %{SOURCE14} %{buildroot}%{_srvdir}/nscd/run
install -m 0740 %{SOURCE15} %{buildroot}%{_srvdir}/nscd/log/run
install -m 0740 %{SOURCE16} %{buildroot}%{_srvdir}/nscd/finish

rm -rf %{buildroot}%{_datadir}/zoneinfo/{posix,right}
rm -rf %{buildroot}%{_includedir}/netatalk/
rm -f %{buildroot}%{_libdir}/libNoVersion*
%ifnarch %{glibc_compat_arches}
    rm -f %{buildroot}/%{_lib}/libNoVersion*
%endif

# empty filelist for non-i686/athlon targets
> extralibs.filelist
%ifarch %{ix86}
pushd build-%{_target_cpu}-linux
    TARGETARCH="%{buildroot}%{_slibdir}/%{_target_cpu}"
    TARGETLIB="%{buildroot}%{_slibdir}"
    mkdir -p $TARGETARCH
    cp -a libc.so $TARGETARCH/`basename $TARGETLIB/libc-*.so`
    ln -sf `basename $TARGETLIB/libc-*.so` $TARGETARCH/`basename $TARGETLIB/libc.so.*`
    cp -a math/libm.so $TARGETARCH/`basename $TARGETLIB/libm-*.so`
    ln -sf `basename $TARGETLIB/libm-*.so` $TARGETARCH/`basename $TARGETLIB/libm.so.*`
    cp -a linuxthreads/libpthread.so $TARGETARCH/`basename $TARGETLIB/libpthread-*.so`
    ln -sf `basename $TARGETLIB/libpthread-*.so` $TARGETARCH/`basename $TARGETLIB/libpthread.so.*`
    cp -a linuxthreads_db/libthread_db.so $TARGETARCH/`basename $TARGETLIB/libthread_db-*.so`
    ln -sf `basename $TARGETLIB/libthread_db-*.so` $TARGETARCH/`basename $TARGETLIB/libthread_db.so.*`
    cp -a rt/librt.so $TARGETARCH/`basename $TARGETLIB/librt-*.so`
    ln -sf `basename $TARGETLIB/librt-*.so` $TARGETARCH/`basename $TARGETLIB/librt.so.*`
    echo "%dir %{_slibdir}/%{_target_cpu}" >> ../extralibs.filelist
    find %{buildroot}/%{_slibdir}/%{_target_cpu} -type f -o -type l |sed -e "s|%{buildroot}||" >> ../extralibs.filelist
popd
%endif

# Create empty %{_libdir}/gconv/gconv-modules.cache
touch %{buildroot}%{_libdir}/gconv/gconv-modules.cache
[[ -d %{buildroot}%{_prefix}/lib/gconv ]] && touch %{buildroot}%{_prefix}/lib/gconv/gconv-modules.cache

# /etc/localtime
rm -f %{buildroot}%{_sysconfdir}/localtime
cp -f %{buildroot}%{_datadir}/zoneinfo/US/Eastern %{buildroot}%{_sysconfdir}/localtime
#ln -sf ..%{_datadir}/zoneinfo/US/Eastern %{buildroot}%{_sysconfdir}/localtime


# Copy Kernel-Headers
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}/boot/
cp -avrf kernel-headers/* %{buildroot}%{_includedir}
echo "#if 0" > %{buildroot}/boot/kernel.h-%{kheaders_ver}

# The last bit: more documentation
rm -rf documentation
mkdir documentation
cp linuxthreads/ChangeLog documentation/ChangeLog.threads
cp linuxthreads/Changes documentation/Changes.threads
cp linuxthreads/README documentation/README.threads
cp linuxthreads/FAQ.html documentation/FAQ-threads.html
cp -r linuxthreads/Examples documentation/examples.threads
cp timezone/README documentation/README.timezone
cp ChangeLog* documentation
bzip2 -9qf documentation/ChangeLog*
mkdir documentation/crypt_blowfish-%{crypt_bf_ver}
cp crypt_blowfish-%{crypt_bf_ver}/{README,LINKS,PERFORMANCE} \
	documentation/crypt_blowfish-%{crypt_bf_ver}

%find_lang libc

# remove README.template and FAQ.in to allow using wildcards in the filelist
#rm README.template FAQ.in

# Final step: remove unpackaged files.
rm %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}%{_libdir}/locale
[[ -d %{buildroot}%{_prefix}/lib/locale ]] && rm -rf %{buildroot}%{_prefix}/lib/locale
mv -f %{buildroot}%{_datadir}/locale/locale.alias .
rm -rf %{buildroot}%{_datadir}/locale
mkdir -p %{buildroot}%{_datadir}/locale && mv locale.alias %{buildroot}%{_datadir}/locale/
rm -rf %{buildroot}%{_libdir}/getconf
[[ -d %{buildroot}%{_prefix}/lib/getconf ]] && rm -rf %{buildroot}%{_prefix}/lib/getconf


%clean
#[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/libc.info %{_infodir}/dir
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
if [ $1 -eq 0 ]; then
	/sbin/install-info --delete %{_infodir}/libc.info %{_infodir}/dir
fi

%pre -n nscd
%_pre_useradd nscd / /bin/false 83

%post -n nscd
if [ -d /var/log/supervise/nscd -a ! -d /var/log/service/nscd ]; then
    mv /var/log/supervise/nscd /var/log/service/
fi
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
%files -f libc.lang -f extralibs.filelist
%defattr(-,root,root)
# configs
%config(noreplace) %verify(not size md5 mtime) /etc/localtime
%config(noreplace) %verify(not size md5 mtime) /etc/nsswitch.conf
%config(noreplace) %verify(not size md5 mtime)  /etc/ld.so.conf
%ghost %config(noreplace) /etc/ld.so.cache
%config %dir /etc/ld.so.conf.d
%ghost %config(noreplace) %{_libdir}/gconv/gconv-modules.cache
%if %{build_biarch}
%ghost %config(noreplace) %{_prefix}/lib/gconv/gconv-modules.cache
%endif
%config(noreplace) /etc/rpc
# libs
%ifarch %{glibc_compat_arches}
%{_libdir}/libnss*.so.1
%endif
%dir %{_libdir}/gconv
%{_libdir}/gconv/*.so
%{_libdir}/gconv/gconv-modules
%if %{build_biarch}
%dir %{_prefix}/lib/gconv
%{_prefix}/lib/gconv/*.so
%{_prefix}/lib/gconv/gconv-modules
%endif
%{_slibdir}/ld-%{version}.so
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
%if "%{arch}" == "ppc64"
%{_slibdir}/ld64.so.1
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
%{_libdir}/libSegFault.so
%if %{build_biarch}
/lib/ld-%{version}.so
/lib/ld-linux*.so.2
/lib/lib*-[.0-9]*.so
/lib/lib*.so.[0-9]*
/lib/libSegFault.so
%endif
%{_datadir}/locale/locale.alias
# man pages
%{_mandir}/man1/*
%{_mandir}/man8/rpcinfo.8*
%{_mandir}/man8/ld.so.8*
# binaries
/sbin/sln
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
#%{_sbindir}/glibc-post-upgrade
# XXX
#%dir /var/db

#
# glibc-utils
#
%files utils
%defattr(-,root,root)
%{_libdir}/libmemusage.so
%{_libdir}/libpcprofile.so
%{_bindir}/memusage
%{_bindir}/memusagestat
%{_bindir}/mtrace
%{_bindir}/pcprofiledump
%{_bindir}/xtrace

#
# glibc-devel
#
%files devel
%defattr(-,root,root)
/boot/kernel.h-%{kheaders_ver}
%{_mandir}/man3/*.bz2
%{_infodir}/libc.info*
%dir %{_includedir}
%dir %{_includedir}/arpa
%dir %{_includedir}/asm
%dir %{_includedir}/asm-generic
%dir %{_includedir}/bits
%dir %{_includedir}/gnu
%dir %{_includedir}/linux
%dir %{_includedir}/linux/byteorder
#%dir %{_includedir}/linux/dvb
%dir %{_includedir}/linux/hdlc
%dir %{_includedir}/linux/isdn
%dir %{_includedir}/linux/lockd
#%dir %{_includedir}/linux/mmc
%dir %{_includedir}/linux/mtd
%dir %{_includedir}/linux/netfilter_arp
#%dir %{_includedir}/linux/netfilter_bridge
%dir %{_includedir}/linux/netfilter_ipv4
%dir %{_includedir}/linux/netfilter_ipv6
%dir %{_includedir}/linux/nfsd
%dir %{_includedir}/linux/raid
%dir %{_includedir}/linux/sunrpc
#%dir %{_includedir}/linux/tc_act
%dir %{_includedir}/net
%dir %{_includedir}/netinet
%dir %{_includedir}/netipx
%dir %{_includedir}/netash
%dir %{_includedir}/netax25
%dir %{_includedir}/netrom
%dir %{_includedir}/netpacket
%dir %{_includedir}/netrose
%dir %{_includedir}/neteconet
%dir %{_includedir}/nfs
%dir %{_includedir}/protocols
%dir %{_includedir}/rpc
%dir %{_includedir}/rpcsvc
%dir %{_includedir}/scsi
%dir %{_includedir}/sound
%dir %{_includedir}/sys
%{_includedir}/*.h
%{_includedir}/arpa/*.h
%{_includedir}/asm/*.h
%{_includedir}/asm-generic/*.h
%{_includedir}/bits/*.h
%{_includedir}/bits/*.def
%{_includedir}/gnu/*.h
%{_includedir}/linux/*.h
%{_includedir}/linux/*.p
%{_includedir}/linux/byteorder/*.h
#%{_includedir}/linux/dvb/*.h
%{_includedir}/linux/hdlc/*.h
%{_includedir}/linux/isdn/*.h
%{_includedir}/linux/lockd/*.h
#%{_includedir}/linux/mmc/*.h
%{_includedir}/linux/mtd/*.h
%{_includedir}/linux/netfilter_arp/*.h
#%{_includedir}/linux/netfilter_bridge/*.h
%{_includedir}/linux/netfilter_ipv4/*.h
%{_includedir}/linux/netfilter_ipv6/*.h
%{_includedir}/linux/nfsd/*.h
%{_includedir}/linux/raid/*.h
%{_includedir}/linux/sunrpc/*.h
#%{_includedir}/linux/tc_act/*.h
%{_includedir}/net/*.h
%{_includedir}/netinet/*.h
%{_includedir}/netipx/*.h
%{_includedir}/netash/*.h
%{_includedir}/netax25/*.h
%{_includedir}/netrom/*.h
%{_includedir}/netpacket/*.h
%{_includedir}/netrose/*.h
%{_includedir}/neteconet/*.h
%{_includedir}/nfs/*.h
%{_includedir}/protocols/*.h
%{_includedir}/rpc/*.h
%{_includedir}/rpcsvc/*.h
%{_includedir}/rpcsvc/*.x
%{_includedir}/scsi/*.h
%{_includedir}/sound/*.h
%{_includedir}/sys/*.h
%if "%{arch}" == "i386"
#%dir %{_includedir}/asm/mach-bigsmp
#%{_includedir}/asm/mach-bigsmp/*.h
#%dir %{_includedir}/asm/mach-default
#%{_includedir}/asm/mach-default/*.h
#%dir %{_includedir}/asm/mach-es7000
#%{_includedir}/asm/mach-es7000/*.h
#%dir %{_includedir}/asm/mach-generic
#%{_includedir}/asm/mach-generic/*.h
#%dir %{_includedir}/asm/mach-numaq
#%{_includedir}/asm/mach-numaq/*.h
#%dir %{_includedir}/asm/mach-summit
#%{_includedir}/asm/mach-summit/*.h
#%dir %{_includedir}/asm/mach-visws
#%{_includedir}/asm/mach-visws/*.h
#%dir %{_includedir}/asm/mach-voyager
#%{_includedir}/asm/mach-voyager/*.h
#%dir %{_includedir}/asm/mach-xbox
#%{_includedir}/asm/mach-xbox/*.h
%endif
%if "%{arch}" == "x86_64"
%dir %{_includedir}/asm-i386
%{_includedir}/asm-i386/*.h
#%dir %{_includedir}/asm-i386/mach-bigsmp
#%{_includedir}/asm-i386/mach-bigsmp/*.h
#%dir %{_includedir}/asm-i386/mach-default
#%{_includedir}/asm-i386/mach-default/*.h
#%dir %{_includedir}/asm-i386/mach-es7000
#%{_includedir}/asm-i386/mach-es7000/*.h
#%dir %{_includedir}/asm-i386/mach-generic
#%{_includedir}/asm-i386/mach-generic/*.h
#%dir %{_includedir}/asm-i386/mach-numaq
#%{_includedir}/asm-i386/mach-numaq/*.h
#%dir %{_includedir}/asm-i386/mach-summit
#%{_includedir}/asm-i386/mach-summit/*.h
#%dir %{_includedir}/asm-i386/mach-visws
#%{_includedir}/asm-i386/mach-visws/*.h
#%dir %{_includedir}/asm-i386/mach-voyager
#%{_includedir}/asm-i386/mach-voyager/*.h
#%dir %{_includedir}/asm-i386/mach-xbox
#%{_includedir}/asm-i386/mach-xbox/*.h
%dir %{_includedir}/asm-x86_64
%{_includedir}/asm-x86_64/*.h
%{_includedir}/asm-x86_64/*.i
%endif
%if "%{arch}" == "ppc64"
%dir %{_includedir}/asm-ppc
%{_includedir}/asm-ppc/*.h
%dir %{_includedir}/asm-ppc64
%{_includedir}/asm-ppc64/*.h
%endif
%if "%{arch}" == "sparc64"
%dir %{_includedir}/asm-sparc
%{_includedir}/asm-sparc/*.h
%dir %{_includedir}/asm-sparc64
%{_includedir}/asm-sparc64/*.h
%endif
%{_libdir}/libbsd-compat.a
%{_libdir}/libbsd.a
%{_libdir}/libc_nonshared.a
%{_libdir}/libg.a
%{_libdir}/libieee.a
%{_libdir}/libmcheck.a
%{_libdir}/libpthread_nonshared.a
%{_libdir}/librpcsvc.a
%{_libdir}/*.o
%{_libdir}/*.so
%if %{build_biarch}
%{_prefix}/lib/libbsd-compat.a
%{_prefix}/lib/libbsd.a
%{_prefix}/lib/libc_nonshared.a
%{_prefix}/lib/libg.a
%{_prefix}/lib/libieee.a
%{_prefix}/lib/libmcheck.a
%{_prefix}/lib/libpthread_nonshared.a
%{_prefix}/lib/librpcsvc.a
%{_prefix}/lib/*.o
%{_prefix}/lib/*.so
%endif
%exclude %{_libdir}/libmemusage.so
%exclude %{_libdir}/libpcprofile.so

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

%files -n ldconfig
%defattr(-,root,root)
/sbin/ldconfig
%{_mandir}/man8/ldconfig*

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
# timezone
#
%files -n timezone
%defattr(-,root,root)
%{_sbindir}/zdump
%{_sbindir}/zic
%{_mandir}/man1/zdump.1*
%dir %{_datadir}/zoneinfo
%{_datadir}/zoneinfo/*

#
# nscd
#
%files -n nscd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nscd.conf
%{_sbindir}/nscd
%{_sbindir}/nscd_nischeck
%dir %attr(0750,root,admin) %{_srvdir}/nscd
%dir %attr(0750,root,admin) %{_srvdir}/nscd/log 
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nscd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nscd/finish
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nscd/log/run  

%files doc
%doc README* NEWS* INSTALL* FAQ* BUGS NOTES* PROJECTS CONFORMANCE
%doc documentation/*
%doc hesiod/README.hesiod
%doc crypt/README.ufc-crypt


%changelog
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

* Thu Oct  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-15mdk
- Rebuild with latest rpm so that libraries in EXCLUDE_FROM_STRIP are
  kept intact during symbols extraction for -debug package

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
- devel package depends on glibc %%{version}-%%{release}
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
