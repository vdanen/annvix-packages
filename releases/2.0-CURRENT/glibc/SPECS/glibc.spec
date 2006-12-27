#
# spec file for package glibc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

#define _unpackaged_files_terminate_build 0

# owl 2.3.6-owl6
%define basevers	2.3.6
#%%define snapshot	20050427
%define crypt_bf_ver	1.0.2

%define revision	$Rev$
%define name		glibc
%define version		%{basevers}%{?snapshot:.%snapshot}
%define release		%_revrel
%define epoch		6

# <version>-<release> tags from kernel package where headers were
# actually extracted from
%define kheaders_ver    2.6.16
%define kheaders_rel    2mdk

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
Source11:	nsswitch.conf
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
# 200-219 - SuSE
# 220-239 - Gentoo
# 300-399 - ALT
# 400-499 - Owl
# 500-599 - Mandriva
# 600-699 - Annvix
# CVS
Patch0:		glibc-2.3.5-cvs-20050427-canonicalize.diff
Patch1:		glibc-2.3.6-cvs-20051116-divdi3.diff
Patch2:		glibc-2.3.6-cvs-20060103-ctermid.diff
Patch3:		glibc-2.3.6-cvs-20060426-linuxthreads-i386-pt-machine.diff
Patch4:		glibc-2.3.6-up-linuxthreads-x86_64-pt-machine.diff
# RH
Patch100:	glibc-2.3.5-fedora.diff
# SuSE
Patch200:	glibc-2.3.2-suse-resolv-response-length.diff
Patch201:	glibc-2.3.4-suse-getconf-default_output.diff
# Gentoo
Patch220:	glibc-2.3.6-gentoo-alpha-xstat.diff
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
Patch403:	glibc-2.3.6-owl-alt-ldd.diff
Patch404:	glibc-2.3.3-owl-info.diff
Patch405:	glibc-2.3.5-owl-alt-syslog-ident.diff
Patch406:	glibc-2.3.5-mjt-owl-alt-syslog-timestamp.diff
Patch407:	glibc-2.3.5-owl-alt-resolv-QFIXEDSZ-underfills.diff
Patch408:	glibc-2.3.2-owl-tmpfile.diff
Patch409:	glibc-2.3.3-owl-tmp-scripts.diff
Patch410:	glibc-2.3.3-owl-rpcgen-cpp.diff
Patch411:	glibc-2.3.5-owl-alt-sanitize-env.diff
# Mandriva
Patch500:       kernel-headers-include-%{kheaders_ver}.%{kheaders_rel}.patch
Patch501:       kernel-headers-gnu-extensions.patch
Patch502:	kernel-headers-syscall-mem-clobbers.patch
Patch503:	glibc-2.2.5-share-locale.patch
# Annvix
Patch600:	glibc-2.3.5-avx-relocate_fcrypt.patch
Patch601:	glibc-2.3.6-avx-increase_BF_FRAME.patch
Patch602:	glibc-2.3.6-avx-kernel-headers-audit_support.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	patch
BuildRequires:	gettext
BuildRequires:	perl
BuildRequires:	autoconf2.5
BuildRequires:	binutils >= 2.13.90.0.18-2mdk
BuildPreReq:	gcc >= 3.1.1

AutoReq:	false
Provides:	glibc-crypt_blowfish = %{crypt_bf_ver}
Provides:	glibc-localedata
Provides:	ld.so
Obsoletes:      zoneinfo
Obsoletes:	libc-static
Obsoletes:	libc-devel
Obsoletes:	libc-profile
Obsoletes:	libc-headers
Obsoletes:      linuxthreads
Obsoletes:	gencat
Obsoletes:	locale
Obsoletes:	glibc-localedata
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
Conflicts:	kernel < 2.2.0
Requires(pre):	rpm-helper
Requires(preun): rpm-helper
Requires(preun): srv
Requires(post):	rpm-helper
Requires(post):	srv
Requires(postun): rpm-helper
Requires(postun): srv
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

# Gentoo
# Re-introduce support for building on Alpha with pre-2.6.4 kernel headers
%patch220 -p1

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
# relocate helper libraries from /%_lib to %_libdir
%patch311 -p1
# fix mprotect return code handling in _dl_make_stack_executable()
%patch312 -p1
# fix _dl_osversion_init(), _dl_non_dynamic_init() and
# dl_main() functions to not assume too old kernel version
%patch313 -p1

# Owl
# copy the freesec stuff
cp %{_sourcedir}/crypt_freesec.[ch] crypt/

echo "Applying crypt_blowfish patch:"
patch -p1 -s < crypt_blowfish-%{crypt_bf_ver}/glibc-2.3.2-crypt.diff
mv crypt/crypt.h crypt/gnu-crypt.h
cp -a crypt_blowfish-%{crypt_bf_ver}/*.[chS] crypt/

# FreeSec support for extended/new-style/BSDI hashes in crypt(3)
%patch400 -p1
# improve res_randomid in the resolver
%patch401 -p1
# force known control characters for iscntrl(3)
%patch402 -p1
# always execute traced object directly with dynamic linker
# fix ldd error reporting on multilib platforms like x86-64
# fix "ldd -u"
%patch403 -p1
# fix libc's info formatting
%patch404 -p1
# don't blindly trust __progname for the syslog ident
%patch405 -p1
# use ctime_r() instead of strftime_r() in syslog(3)
%patch406 -p1
# avoid potential reads beyond end of undersized DNS responses
%patch407 -p1
# allow tmpfile(3) to use TMPDIR environment variable
%patch408 -p1
# fix temporary file handling in the scripts
%patch409 -p1
# avoid hardcoding of cpp binary, use execvp instead of execv
%patch410 -p1
# sanitize the environment in a paranoid way
%patch411 -p1

# Mandriva
%patch503 -p1 -b .share_locale

# Annvix
%patch600 -p1
%patch601 -p1

pushd kernel-headers/
TARGET=%{_target_cpu}
%patch500 -p1
%patch501 -p1
%patch502 -p1
%patch602 -p1
%{expand:%(%__cat %{_sourcedir}/make_versionh.sh)}
%{expand:%(%__cat %{_sourcedir}/create_asm_headers.sh)}
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
cat %{_sourcedir}/glibc-find-requires.sh >glibc_find_requires.sh
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

install -m 0644 %{_sourcedir}/nsswitch.conf %{buildroot}%{_sysconfdir}/nsswitch.conf

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
install -m 0740 %{_sourcedir}/nscd.run %{buildroot}%{_srvdir}/nscd/run
install -m 0740 %{_sourcedir}/nscd-log.run %{buildroot}%{_srvdir}/nscd/log/run
install -m 0740 %{_sourcedir}/nscd.finish %{buildroot}%{_srvdir}/nscd/finish

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
    install -m 0755 libc.so $TARGETARCH/`basename $TARGETLIB/libc-*.so`
    ln -sf `basename $TARGETLIB/libc-*.so` $TARGETARCH/`basename $TARGETLIB/libc.so.*`
    install -m 0755 math/libm.so $TARGETARCH/`basename $TARGETLIB/libm-*.so`
    ln -sf `basename $TARGETLIB/libm-*.so` $TARGETARCH/`basename $TARGETLIB/libm.so.*`
    install -m 0755 linuxthreads/libpthread.so $TARGETARCH/`basename $TARGETLIB/libpthread-*.so`
    ln -sf `basename $TARGETLIB/libpthread-*.so` $TARGETARCH/`basename $TARGETLIB/libpthread.so.*`
    install -m 0755 linuxthreads_db/libthread_db.so $TARGETARCH/`basename $TARGETLIB/libthread_db-*.so`
    ln -sf `basename $TARGETLIB/libthread_db-*.so` $TARGETARCH/`basename $TARGETLIB/libthread_db.so.*`
    install -m 0755 rt/librt.so $TARGETARCH/`basename $TARGETLIB/librt-*.so`
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
%dir %{_includedir}/linux/amba
%dir %{_includedir}/linux/byteorder
%dir %{_includedir}/linux/dvb
%dir %{_includedir}/linux/hdlc
%dir %{_includedir}/linux/isdn
%dir %{_includedir}/linux/lockd
%dir %{_includedir}/linux/mmc
%dir %{_includedir}/linux/mtd
%dir %{_includedir}/linux/netfilter
%dir %{_includedir}/linux/netfilter_arp
%dir %{_includedir}/linux/netfilter_bridge
%dir %{_includedir}/linux/netfilter_ipv4
%dir %{_includedir}/linux/netfilter_ipv6
%dir %{_includedir}/linux/nfsd
%dir %{_includedir}/linux/raid
%dir %{_includedir}/linux/spi
%dir %{_includedir}/linux/sunrpc
%dir %{_includedir}/linux/tc_act
%dir %{_includedir}/linux/tc_ematch
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
#%dir %{_includedir}/usb
%{_includedir}/*.h
%{_includedir}/arpa/*.h
%{_includedir}/asm/*.h
%{_includedir}/asm-generic/*.h
%{_includedir}/bits/*.h
%{_includedir}/bits/*.def
%{_includedir}/gnu/*.h
%{_includedir}/linux/*.h
#%{_includedir}/linux/*.p
%{_includedir}/linux/amba/*.h
%{_includedir}/linux/byteorder/*.h
%{_includedir}/linux/dvb/*.h
%{_includedir}/linux/hdlc/*.h
%{_includedir}/linux/isdn/*.h
%{_includedir}/linux/lockd/*.h
%{_includedir}/linux/mmc/*.h
%{_includedir}/linux/mtd/*.h
%{_includedir}/linux/netfilter/*.h
%{_includedir}/linux/netfilter_arp/*.h
%{_includedir}/linux/netfilter_bridge/*.h
%{_includedir}/linux/netfilter_ipv4/*.h
%{_includedir}/linux/netfilter_ipv6/*.h
%{_includedir}/linux/nfsd/*.h
%{_includedir}/linux/raid/*.h
%{_includedir}/linux/sunrpc/*.h
%{_includedir}/linux/spi/*.h
%{_includedir}/linux/tc_act/*.h
%{_includedir}/linux/tc_ematch/*.h
%{_includedir}/linux/usb/*.h
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
%dir %{_includedir}/asm/mach-bigsmp
%{_includedir}/asm/mach-bigsmp/*.h
%dir %{_includedir}/asm/mach-default
%{_includedir}/asm/mach-default/*.h
%dir %{_includedir}/asm/mach-es7000
%{_includedir}/asm/mach-es7000/*.h
%dir %{_includedir}/asm/mach-generic
%{_includedir}/asm/mach-generic/*.h
%dir %{_includedir}/asm/mach-numaq
%{_includedir}/asm/mach-numaq/*.h
%dir %{_includedir}/asm/mach-summit
%{_includedir}/asm/mach-summit/*.h
%dir %{_includedir}/asm/mach-visws
%{_includedir}/asm/mach-visws/*.h
%dir %{_includedir}/asm/mach-voyager
%{_includedir}/asm/mach-voyager/*.h
%dir %{_includedir}/asm/mach-xen
%dir %{_includedir}/asm/mach-xen/asm
%{_includedir}/asm/mach-xen/*.h
%{_includedir}/asm/mach-xen/asm/*.h
%endif
%if "%{arch}" == "x86_64"
%dir %{_includedir}/asm-i386
%{_includedir}/asm-i386/*.h
%dir %{_includedir}/asm-i386/mach-bigsmp
%{_includedir}/asm-i386/mach-bigsmp/*.h
%dir %{_includedir}/asm-i386/mach-default
%{_includedir}/asm-i386/mach-default/*.h
%dir %{_includedir}/asm-i386/mach-es7000
%{_includedir}/asm-i386/mach-es7000/*.h
%dir %{_includedir}/asm-i386/mach-generic
%{_includedir}/asm-i386/mach-generic/*.h
%dir %{_includedir}/asm-i386/mach-numaq
%{_includedir}/asm-i386/mach-numaq/*.h
%dir %{_includedir}/asm-i386/mach-summit
%{_includedir}/asm-i386/mach-summit/*.h
%dir %{_includedir}/asm-i386/mach-visws
%{_includedir}/asm-i386/mach-visws/*.h
%dir %{_includedir}/asm-i386/mach-voyager
%{_includedir}/asm-i386/mach-voyager/*.h
%dir %{_includedir}/asm-i386/mach-xen
%dir %{_includedir}/asm-i386/mach-xen/asm
%{_includedir}/asm-i386/mach-xen/*.h
%{_includedir}/asm-i386/mach-xen/asm/*.h
%dir %{_includedir}/asm-x86_64
%{_includedir}/asm-x86_64/*.h
#%{_includedir}/asm-x86_64/*.i
%dir %{_includedir}/asm-x86_64/mach-xen
%dir %{_includedir}/asm-x86_64/mach-xen/asm
%{_includedir}/asm-x86_64/mach-xen/*.h
%{_includedir}/asm-x86_64/mach-xen/asm/*.h
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
