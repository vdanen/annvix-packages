#
# spec file for package gcc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision		$Rev$
%define name			gcc
%define version			4.1.1
%define release			%_revrel

%define _unpackaged_files_terminate_build 0
%define build_mudflap		0

%define branch			4.1
%define branch_tag		%(perl -e 'printf "%%02d%%02d", split(/\\./,shift)' %{branch})
%define biarches		x86_64 ppc64
%define color_gcc_version	1.3.2

%define libgcc_major		1
%define libstdcxx_major		6
%define libstdcxx_minor		8
%define libobjc_major		1
%define libmudflap_major	0
%define libssp_major		0
%define libgcc_name_orig	libgcc
%define libgcc_name		%{libgcc_name_orig}%{libgcc_major}
%define libstdcxx_name_orig	libstdc++
%define libstdcxx_name		%{libstdcxx_name_orig}%{libstdcxx_major}
%define libobjc_name_orig	libobjc
%define libobjc_name		%{libobjc_name_orig}%{libobjc_major}
%define libmudflap_name_orig	libmudflap
%define libmudflap_name		%{libmudflap_name_orig}%{libmudflap_major}
%define libssp_name_orig	libssp
%define libssp_name		%{libssp_name_orig}%{libssp_major}

%define nof_arches		ppc
%ifarch x86_64
%define multilib_32_arch	i586
%endif
%ifarch ppc64
%define multilib_32_arch	ppc
%endif
%ifarch %{biarches}
%define gcc32_target_platform	%{multilib_32_arch}=%{_real_vendor}-%{_target_os}%{?_gnu}
%endif

%define alternative_priority	40%{branch_tag}
%define _alternativesdir	/etc/alternatives

# Define GCC target platform, and arch we built for
%define arch			%(echo %{_target_cpu}|sed -e "s/i.86/i386/" -e "s/athlon/i386/" -e "s/amd64/x86_64/")
%define gcc_libdir		%{_prefix}/lib/gcc

# We now have versioned libstdcxx_includedir, that is c++/<VERSION>/
%define libstdcxx_includedir	%{_prefix}/include/c++/%{version}

%{expand:%%define avx_version %(awk '{print $3}' /etc/annvix-release | cut -d '-' -f 1)}

%define build_debug		0
# Allow --with[out] <feature> at rpm command line build
%{expand: %{?_without_DEBUG:	%%global build_debug 0}}
%{expand: %{?_with_DEBUG:	%%global build_debug 1}}

Summary:	GNU Compiler Collection
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/C
URL:		http://gcc.gnu.org/

Source0:	ftp://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Source1:	http://www.mindspring.com/~jamoyers/software/colorgcc/colorgcc-%{color_gcc_version}.tar.bz2
# FIXME: unless we get proper help2man package
Source6:	gcc35-help2man.pl

Patch0:		colorgcc-1.3.2-mdk-conf.patch
Patch1:		gcc35-pch-mdkflags.patch
Patch2:		gcc41-visibility1.patch
Patch3:		gcc41-visibility2.patch
Patch4:		gcc40-linux32.patch
Patch5:		gcc40-linux32-build-env.patch
Patch6:		gcc4-libtool1.4-lib64.patch
Patch8:		gcc4-mtune-generic.patch
Patch9:		gcc41-ldbl-default.patch
Patch10:	gcc41-ldbl-default-libstdc++.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
# Want updated alternatives priorities
# We want -pie support
BuildRequires:	binutils >= 2.16.91.0.2
BuildRequires:	zlib-devel
BuildRequires:	gettext
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	texinfo >= 4.1
BuildRequires:	glibc-devel >= 2.2.5-14mdk
BuildRequires:	glibc-static-devel >= 2.2.5-14mdk
BuildRequires:	dejagnu
BuildRequires:	gawk >= 3.1.4

Requires:	binutils >= 2.16.91.0.2
Requires:	%{name}-cpp = %{version}-%{release}
# FIXME: We need a libgcc with 3.4 symbols
Requires:	%{libgcc_name_orig} >= 3.3.2-5mdk
# Make sure pthread.h doesn't contain __thread keyword
Requires:	glibc-devel >= 2.2.5-14mdk
Requires:	setup >= 2.6
Requires(post):	/usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
Obsoletes:	gcc%{branch}
Provides:	gcc%{branch} = %{version}-%{release}
# Make sure gdb will understand DW_FORM_strp
Conflicts:	gdb < 5.1.1

%description
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.
This package is required for all other GCC compilers, namely C++
and Objective C.

If you have multiple versions of GCC installed on your system, it is
preferred to type "gcc-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU C compiler version %{version}.


%package -n %{libgcc_name}
Summary:	GNU C library
Group:		System/Libraries
Provides:	%{libgcc_name_orig} = %{version}-%{release}
Obsoletes:	%{libgcc_name_orig}%{branch}
Provides:	%{libgcc_name_orig}%{branch} = %{version}-%{release}
Obsoletes:	%{libgcc_name_orig}3.0
Provides:	%{libgcc_name_orig}3.0 = %{version}-%{release}
Provides:	%{libgcc_name_orig}3.2 = %{version}-%{release}

%description -n %{libgcc_name}
The %{libgcc_name} package contains GCC shared libraries for gcc %{branch}


####################################################################
# C++ Compiler

%package c++
Summary:	C++ support for gcc
Group:		Development/C++
Obsoletes:	gcc%{branch}-c++
Provides:	gcc%{branch}-c++ = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Requires:	%{libstdcxx_name} = %{version}
Requires:	%{libstdcxx_name}-devel = %{version}

%description c++
This package adds C++ support to the GNU C compiler. It includes support
for most of the current C++ specification, including templates and
exception handling. It does include the static standard C++
library and C++ header files; the library for dynamically linking
programs is available separately.

If you have multiple versions of GCC installed on your system, it is
preferred to type "g++-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU C++ compiler version %{version}.


####################################################################
# C++ Libraries

%package -n %{libstdcxx_name}
Summary:	GNU C++ library
Group:		System/Libraries
Obsoletes:	%{libstdcxx_name_orig}%{branch}
Provides:	%{libstdcxx_name_orig}%{branch} = %{version}-%{release}
Provides:	%{libstdcxx_name_orig} = %{version}-%{release}

%description -n %{libstdcxx_name}
This package contains the GCC Standard C++ Library v3, an ongoing
project to implement the ISO/IEC 14882:1998 Standard C++ library.


%package -n %{libstdcxx_name}-devel
Summary:	Header files and libraries for C++ development
Group:		Development/C++
Requires:	%{libstdcxx_name} = %{version}-%{release}
Obsoletes:	%{libstdcxx_name_orig}%{branch}-devel
Provides:	%{libstdcxx_name_orig}%{branch}-devel = %{version}-%{release}
Provides:	%{libstdcxx_name_orig}-devel = %{version}-%{release}

%description -n %{libstdcxx_name}-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development.


%package -n %{libstdcxx_name}-static-devel
Summary:	Static libraries for C++ development
Group:		Development/C++
Requires:	%{libstdcxx_name}-devel = %{version}-%{release}
Obsoletes:	%{libstdcxx_name_orig}%{branch}-static-devel
Provides:	%{libstdcxx_name_orig}%{branch}-static-devel = %{version}-%{release}
Provides:	%{libstdcxx_name_orig}-static-devel = %{version}-%{release}

%description -n %{libstdcxx_name}-static-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the static libraries needed for C++ development.


####################################################################
# Objective C Compiler

%package objc
Summary:	Objective C support for gcc
Group:		Development/Other
Obsoletes:	gcc%{branch}-objc
Provides:	gcc%{branch}-objc = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description objc
This package adds Objective C support to the GNU C compiler. Objective
C is an object oriented derivative of the C language, mainly used on
systems running NeXTSTEP. This package does not include the standard
Objective C object library.


####################################################################
# Objective C Libraries

%package -n %{libobjc_name}
Summary:	Objective C runtime libraries
Group:		System/Libraries
Obsoletes:	%{libobjc_name_orig}3.0
Obsoletes:	%{libobjc_name_orig}3.1
Provides:	%{libobjc_name_orig} = %{version}-%{release}
Provides:	%{libobjc_name_orig}3.0 = %{version}-%{release}
Provides:	%{libobjc_name_orig}3.1 = %{version}-%{release}

%description -n %{libobjc_name}
Runtime libraries for the GNU Objective C Compiler.


%if %{build_mudflap}
####################################################################
# mudflap headers and libraries

%package -n %{libmudflap_name}
Summary:	GCC mudflap shared support library
Group:		System/Libraries

%description -n %{libmudflap_name}
This package contains GCC shared support library which is needed
for mudflap support.

For front-ends that support it (C and C++), instrument all risky
pointer/array dereferencing operations, some standard library
string/heap functions, and some other associated constructs with
range/validity tests.  Modules so instrumented should be immune to
buffer overflows, invalid heap use, and some other classes of C/C++
programming errors.

Refer to the documentation for -fmudflap and -fmudflapth.


%package -n %{libmudflap_name}-devel
Summary:	GCC mudflap support
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libmudflap_name} = %{version}-%{release}
Obsoletes:	%{libmudflap_name_orig}-devel
Provides:	%{libmudflap_name_orig}-devel = %{version}-%{release}

%description -n %{libmudflap_name}-devel
This package contains headers and static libraries for building
mudflap-instrumented programs.

To instrument a non-threaded program, add -fmudflap' option to GCC
and when linking add -lmudflap'. For threaded programs also add
-fmudflapth' and -lmudflapth'.
%endif

####################################################################
# SSP headers and libraries

%package -n %{libssp_name}
Summary:	GCC SSP shared support library
Group:		System/Libraries

%description -n %{libssp_name}
This package contains GCC shared support library which is needed
for SSP support.

%package -n %{libssp_name}-devel
Summary:	GCC SSP support
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libssp_name} = %{version}-%{release}
Obsoletes:	%{libssp_name_orig}-devel
Provides:	%{libssp_name_orig}-devel = %{version}-%{release}

%description -n %{libssp_name}-devel
This package contains headers and static libraries for building
SSP-instrumented programs.

Refer to the documentation for -fstack-protector.


####################################################################
# Preprocessor

%package cpp
Summary:	The C Preprocessor
Group:		Development/C
Obsoletes:	gcc%{branch}-cpp
Provides:	gcc%{branch}-cpp = %{version}-%{release}
Requires(post):	/usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives

%description cpp
The C preprocessor is a 'macro processor' which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define 'macros,' which are abbreviations for longer
constructs.

The C preprocessor provides four separate facilities that you can use as
you see fit:

* Inclusion of header files. These are files of declarations that can be
  substituted into your program.
* Macro expansion. You can define 'macros,' which are abbreviations for 
  arbitrary fragments of C code, and then the C preprocessor will replace
  the macros with their definitions throughout the program.
* Conditional compilation. Using special preprocessing directives,
  you can include or exclude parts of the program according to various
  conditions.
* Line control. If you use a program to combine or rearrange source files
  into an intermediate file which is then compiled, you can use line
  control to inform the compiler about where each source line originated.

If you have multiple versions of GCC installed on your system, you
will have to type "cpp -V%{version}" or "cpp-%{version}" (without double quotes)
in order to use the GNU C Preprocessor version %{version}.


####################################################################
# ColorGCC

%package colorgcc
Summary:	GCC output colorizer
Group:		Development/Other
Obsoletes:	gcc2.96-colorgcc
Obsoletes:	gcc%{branch}-colorgcc
Provides:	gcc%{branch}-colorgcc = %{version}-%{release}
Requires:	%{name} = %{version}
Requires(post):	/usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
Requires:	perl

%description colorgcc
ColorGCC is a Perl wrapper to colorize the output of compilers with
warning and error messages matching the GCC output format.

This package is configured to run with the associated system compiler,
that is GCC version %{version}. If you want to use it for another
compiler (e.g. gcc 2.96), you may have to define gccVersion: 2.96 and
uncomment the respective compiler paths in %{_sysconfdir}/colorgccrc
for a system-wide effect, or in ~/.colorgccrc for your user only.


####################################################################
# Documentation

%package doc
Summary:	GCC documentation
Group:		Development/Other
Obsoletes:	gcc%{branch}-doc
Provides:	gcc%{branch}-doc = %{version}-%{release}
Requires(post):	info-install
Requires(postun): info-install

%description doc
GCC is a compiler suite aimed at integrating all the optimizations and
features necessary for a high-performance and stable development
environment. This package contains the compiler documentation in INFO
pages.


%prep
%setup -q -a 1
# ColorGCC patch
pushd colorgcc-%{color_gcc_version}
%patch0 -p1 -b .conf
perl -pi -e 's|GCC_VERSION|%{version}|' colorgcc*
popd

%patch1 -p1 -b .pch-mdkflags
%patch2 -p1 -b .visibility1
%patch3 -p1 -b .visibility2
%patch4 -p1 -b .linux32
%patch5 -p1 -b .linux32-build-env
%patch6 -p1 -b .libtool-lib64
%patch8 -p1 -b .generic
%patch9 -p0 -b .ldbl-default
%patch10 -p1 -b .ldbl-default-libstdc++

# FIXME: use a configure flag
optflags=`echo $RPM_OPT_FLAGS| sed -e 's/-mcpu=/-mtune=/'`
perl -pi -e "s|\@MDK_OPT_FLAGS\@|$optflags|" \
	libstdc++-v3/include/Makefile.am \
	libstdc++-v3/include/Makefile.in

# Annvix information for bug reports
perl -pi -e "/bug_report_url/ and s/\"[^\"]+\"/\"<URL:https:\/\/bugs.annvix.org\/>\"/;" \
         -e '/version_string/ and s/([0-9]*(\.[0-9]*){1,3}).*(\";)$/\1 \(Annvix %{avx_version} %{version}-%{release}\)\3/;' \
         gcc/version.c


%build
# Force a seperate object dir
rm -fr obj-%{_target_platform}
mkdir obj-%{_target_platform}
cd obj-%{_target_platform}

# FIXME: extra tools needed
mkdir -p bin
cp %{_sourcedir}/gcc35-help2man.pl bin/help2man
export PATH=$PATH:$PWD/bin

# Make bootstrap-lean
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g' -e 's/-mcpu=pentiumpro//g'`
%if %{build_debug}
OPT_FLAGS=`echo "$OPT_FLAGS -g" | sed -e "s/-fomit-frame-pointer//g"`
%endif
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-fomit-frame-pointer//g'`

# update config.{sub,guess} scripts
%{?__cputoolize: %{__cputoolize} -c ..}
%{?__cputoolize: %{__cputoolize} -c ../boehm-gc}
CC="%{__cc}" CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
    ../configure \
	--prefix=%{_prefix} \
	--libexecdir=%{_prefix}/lib \
	--with-slibdir=/%{_lib} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--enable-shared \
	--enable-threads=posix \
	--enable-checking=release \
	--enable-long-long \
	--enable-__cxa_atexit \
	--enable-clocale=gnu \
	--disable-libunwind-exceptions \
	--enable-languages="c,c++,objc" \
	--host=%{_target_platform} \
	--target=%{_target_platform} \
%ifarch %{ix86} x86_64
	--with-cpu=generic \
%endif
	--with-system-zlib \
%if !%{build_mudflap}
	--disable-libmudflap \
%endif
	--enable-ssp --enable-libssp
touch ../gcc/c-gperf.h
%ifarch %{ix86} x86_64
%make profiledbootstrap BOOT_CFLAGS="$OPT_FLAGS"
%else
%make bootstrap-lean BOOT_CFLAGS="$OPT_FLAGS"
%endif

# Make protoize
make -C gcc CC="./xgcc -B ./ -O2" proto
cd ..

# Copy various doc files here and there
mkdir -p rpm.doc/{objc,libobjc,libstdc++-v3,cp}

pushd gcc/objc
     for i in README*; do
         cp -p $i ../../rpm.doc/objc/
     done
popd
pushd libobjc
    for i in README* THREADS* ChangeLog; do
	cp -p $i ../rpm.doc/libobjc/
    done
popd
pushd libstdc++-v3
    for i in README* ChangeLog*; do
	cp -p $i ../rpm.doc/libstdc++-v3/
    done
popd
cp -pr libstdc++-v3/docs/html rpm.doc/libstdc++-v3/
pushd gcc/cp
    for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/cp/
    done
popd

# Run tests
%ifarch %{biarches}
RUNTESTFLAGS="--target_board 'unix{-m32,}'"
%endif
echo ====================TESTING=========================
pushd obj-%{_target_platform}
    %make -k RUNTESTFLAGS="$RUNTESTFLAGS" check || true
    logfile="$PWD/../%{name}-%{version}-%{release}.log"
    ../contrib/test_summary > $logfile
popd
echo ====================TESTING END=====================


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# Fix HTML docs for libstdc++-v3
perl -pi -e \
    's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
    libstdc++-v3/docs/html/documentation.html
ln -sf documentation.html libstdc++-v3/docs/html/index.html
find libstdc++-v3/docs/html -name CVS | xargs rm -rf

# Create some directories, just to make sure (e.g. ColorGCC)
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_infodir}
mkdir -p %{buildroot}%{_sysconfdir}

# ColorGCC stuff
pushd colorgcc-%{color_gcc_version}
    install -m 0750 colorgcc %{buildroot}%{_bindir}/colorgcc-%{version}
    ln -s colorgcc-%{version} %{buildroot}%{_bindir}/colorgcc
    install -m 0644 colorgccrc %{buildroot}%{_sysconfdir}/
    for i in COPYING CREDITS ChangeLog; do
        [ ! -f ../$i.colorgcc ] && mv -f $i ../$i.colorgcc
    done
popd

pushd obj-%{_target_platform}
    %makeinstall_std
popd

FULLVER=`%{buildroot}%{_bindir}/%{_target_platform}-gcc --version | head -n 1 | cut -d' ' -f3`
FULLPATH=$(dirname %{buildroot}%{gcc_libdir}/%{_target_platform}/%{version}/cc1)

file %{buildroot}/%{_bindir}/* | grep ELF | cut -d':' -f1 | xargs strip || :
strip $FULLPATH/cc1
strip $FULLPATH/cc1plus

# Create /usr/bin/gcc%{branch}-version that contains the full version of gcc
cat >%{buildroot}%{_bindir}/gcc%{branch}-version <<EOF
#!/bin/sh
echo "$FULLVER"
EOF
chmod 0755 %{buildroot}%{_bindir}/gcc%{branch}-version

# Fix program names
# (gb) For each primary program in every package, I want it to be
# named <program>-<version>
pushd %{buildroot}%{_bindir}
    for file in cpp gcc c++ g++ gij gpidump; do
        file_version="${file}-%{version}"
        if [ -x "$file" -a "(" ! -x "$file_version" -o -L "$file_version" ")" ]; then
            cp -f $file $file_version
            rm -f $file
            ln -s $file_version $file
        fi
        file="$file" file_version="$file_version"
        if [ -x "$file" -a ! -x "$file_version" ]; then
            cp -f $file $file_version
            rm -f $file
            ln -s $file_version $file
        fi
    done
popd

# Fix some links
ln -sf gcc %{buildroot}%{_bindir}/cc
rm -f %{buildroot}%{_infodir}/dir

# Strip debug info from libraries
STRIP_DEBUG=
%if !%{build_debug}
STRIP_DEBUG="strip -g"
%endif

# Dispatch libraries to the right directories
DispatchLibs() {
	libname=$1 libversion=$2
	rm -f $libname.so $libname.a
	$STRIP_DEBUG ../../../../%{_lib}/$libname.so.$libversion
	$STRIP_DEBUG ../../../../%{_lib}/$libname.a
	ln -s ../../../../%{_lib}/$libname.so.$libversion $libname.so
	rm -f ../../../../%{_lib}/$libname.so
	cp -f ../../../../%{_lib}/$libname.a $libname.a
	rm -f ../../../../%{_lib}/$libname.a
%ifarch %{biarches}
	    [ -d 32 ] || mkdir 32
	    pushd 32
	        mkdir -p %{buildroot}%{_prefix}/lib
                skip32=
                [[ -z "$skip32" ]] && {
	            $STRIP_DEBUG ../../../../$libname.so.$libversion
	            $STRIP_DEBUG ../../../../$libname.a
	            ln -s ../../../../$libname.so.$libversion $libname.so
	            rm -f ../../../../$libname.so
	            [ -r "../../../../$libname.a" ] && {
	                cp -f ../../../../$libname.a $libname.a
	                rm -f ../../../../$libname.a
	            }
                }
	    popd
%endif
%ifarch %{nof_arches}
	    [ -d nof ] || mkdir nof
	    pushd nof
	        $STRIP_DEBUG ../../../../nof/$libname.so.$libversion
	        $STRIP_DEBUG ../../../../nof/$libname.a
	        ln -s ../../../../nof/$libname.so.$libversion $libname.so
	        rm -f ../../../../nof/$libname.so
	        [ -r "../../../../nof/$libname.a" ] && {
	            cp -f ../../../../nof/$libname.a $libname.a
	            rm -f ../../../../nof/$libname.a
	        }
	    popd
%endif
}

pushd $FULLPATH;
    DispatchLibs libssp		%{libssp_major}.0.0
    mv ../../../../%{_lib}/$crosslibdir/libssp_nonshared.a libssp_nonshared.a
%ifarch %{biarches}
    mv ../../../libssp_nonshared.a 32/libssp_nonshared.a
%endif
%if %{build_mudflap}
    DispatchLibs libmudflap	%{libmudflap_major}.0.0
    DispatchLibs libmudflapth	%{libmudflap_major}.0.0
%endif
    DispatchLibs libstdc++	%{libstdcxx_major}.0.%{libstdcxx_minor}
    mv ../../../../%{_lib}/libsupc++.a libsupc++.a
%ifarch %{biarches}
       mv -f ../../../libsupc++.a 32/libsupc++.a
%endif
%ifarch %{nof_arches}
        mv -f ../../../nof/libsupc++.a nof/libsupc++.a
%endif
    DispatchLibs libobjc	%{libobjc_major}.0.0
popd

# Move <cxxabi.h> to compiler-specific directories
mkdir -p $FULLPATH/include/bits/
mv %{buildroot}%{libstdcxx_includedir}/cxxabi.h $FULLPATH/include/
mv $RPM_BUILD_ROOT%{libstdcxx_includedir}/%{_target_platform}/bits/cxxabi_tweaks.h $FULLPATH/include/bits/

# Ship with biarch c++config.h headers
pushd obj-%{_target_platform}
    cxxconfig="`find %{_target_platform}/libstdc++-v3/include -name c++config.h`"
    for i in `find %{_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
        if ! diff -up $cxxconfig $i; then
            file_32=x file_64=x
            case $i in
                %{_target_platform}/32/*) file_32=$i; file_64=$cxxconfig ;;
                %{_target_platform}/64/*) file_32=$cxxconfig; file_64=$i ;;
            esac
            { [[ -f "$file_32" ]] && [[ -f "$file_64" ]]; } ||
                { echo "c++config.h dispatch error"; exit 1; }

            cat > %{buildroot}%{libstdcxx_includedir}/%{_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
`cat $file_32`
#else
`cat $file_64`
#endif
#endif
EOF

            break
        fi
    done
popd

%if %{build_mudflap}
# Move <mf-runtime.h> to compiler-specfic directory
mv %{buildroot}%{_includedir}/mf-runtime.h $FULLPATH/include/
%endif


# Fix links to binaries
pushd %{buildroot}%{_bindir};
    progs="cpp gcc"
    progs="$progs g++ c++"
    for file in $progs; do
        [[ -L $file ]] && rm -f $file
        [[ -x $file ]] && mv $file "$file"-%{version}
        [[ -x "$file"-%{version} ]] || { echo "ERROR: no versioned binary for $file"; exit 1; }
    done
popd

# Create an empty file with perms 0755
FakeAlternatives() {
    for file in ${1+"$@"}; do
        rm -f $file
        touch $file
        chmod 0755 $file
    done
}

# Alternatives provide /lib/cpp and %{_bindir}/cpp
(cd %{buildroot}%{_bindir}; FakeAlternatives cpp)
(mkdir -p %{buildroot}/lib; cd %{buildroot}/lib; ln -sf %{_bindir}/cpp cpp)

# Alternatives provide /usr/bin/c++
(cd %{buildroot}%{_bindir}; FakeAlternatives c++)

# Move libgcc_s.so* to /%{_lib}
pushd %{buildroot}/%{_lib}
    chmod 0755 libgcc_s.so.%{libgcc_major}
    mv -f  libgcc_s.so.%{libgcc_major} libgcc_s-%{version}.so.%{libgcc_major}
popd
pushd %{buildroot}%{_libdir}
    ln -sf libgcc_s-%{version}.so.%{libgcc_major} %{buildroot}/%{_lib}/libgcc_s.so.%{libgcc_major}
    ln -sf ../../%{_lib}/libgcc_s.so.%{libgcc_major} %{buildroot}%{_libdir}/libgcc_s.so
%ifarch %{nof_arches}
    chmod 0755 nof/libgcc_s.so.%{libgcc_major}
    mkdir -p %{buildroot}/%{_lib}/nof
    mv -f  nof/libgcc_s.so.%{libgcc_major} %{buildroot}/%{_lib}/nof/libgcc_s-%{version}.so.%{libgcc_major}
    ln -sf libgcc_s-%{version}.so.%{libgcc_major} %{buildroot}/%{_lib}/nof/libgcc_s.so.%{libgcc_major}
    ln -sf ../../%{_lib}/nof/libgcc_s.so.%{libgcc_major} %{buildroot}%{target_libdir}/nof/libgcc_s.so
%endif
popd

%ifarch %{biarches}
pushd %{buildroot}/lib
    chmod 0755 libgcc_s.so.%{libgcc_major}
    mv -f  libgcc_s.so.%{libgcc_major} %{buildroot}/lib/libgcc_s-%{version}.so.%{libgcc_major}
    ln -sf libgcc_s-%{version}.so.%{libgcc_major} %{buildroot}/lib/libgcc_s.so.%{libgcc_major}
    ln -sf ../../lib/libgcc_s.so.%{libgcc_major} %{buildroot}%{_prefix}/lib/libgcc_s.so
    ln -sf ../../lib/libgcc_s.so.%{libgcc_major} %{buildroot}%{_prefix}/lib/libgcc_s_32.so
popd
%endif

# Create c89 and c99 wrappers
cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
    case "$opt" in
        -ansi|-std=c89|-std=iso9899:1990) fl="";;
        -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	        exit 1;;
    esac
done
exec %{_bindir}/gcc-%{version} $fl ${1+"$@"}
EOF

cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
    case "$opt" in
        -std=c99|-std=iso9899:1999) fl="";;
        -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	        exit 1;;
    esac
done
exec %{_bindir}/gcc-%{version} $fl ${1+"$@"}
EOF

chmod 0755 %{buildroot}%{_prefix}/bin/c?9

# Fix info pages
if [[ "%{name}" = "gcc%{branch}" ]]; then
    pushd %{buildroot}%{_infodir}/
        for f in cpp cppinternals gcc; do
            if [[ -f "$f.info" ]]; then
                perl -pe "/^START-INFO-DIR-ENTRY/ .. /^END-INFO-DIR-ENTRY/ and s/($f)/\${1}-%{branch}/ig" $f.info > ${f}-%{branch}.info
                rm -f $f.info
            fi
        done
    popd
fi

# Remove unpackaged files
rm -rf %{buildroot}%{_prefix}/doc

# remove propaganda manpages
rm -rf %{buildroot}%{_mandir}/man7


%if %{build_debug}
# Don't strip in debug mode
export DONT_STRIP=1
%endif

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
/usr/sbin/update-alternatives --install %{_bindir}/gcc gcc %{_bindir}/gcc-%{version} %{alternative_priority}
[ -e %{_bindir}/gcc ] || /usr/sbin/update-alternatives --auto gcc


%postun
if [ ! -f %{_bindir}/gcc-%{version} ]; then
    /usr/sbin/update-alternatives --remove gcc %{_bindir}/gcc-%{version}
fi


%post colorgcc
/usr/sbin/update-alternatives --install %{_bindir}/gcc gcc %{_bindir}/colorgcc %(expr %{alternative_priority} + 50000)


%postun colorgcc
if [ ! -f %{_bindir}/colorgcc-%{version} ]; then
    /usr/sbin/update-alternatives --remove gcc %{_bindir}/colorgcc
    # update-alternatives silently ignores paths that don't exist
    /usr/sbin/update-alternatives --remove g++ %{_bindir}/colorgcc
fi


%triggerin colorgcc -- %{name}-c++
/usr/sbin/update-alternatives --install %{_bindir}/g++ g++ %{_bindir}/colorgcc %(expr %{alternative_priority} + 50000) --slave %{_bindir}/c++ c++ %{_bindir}/colorgcc


%triggerpostun colorgcc -- %{name}-c++
if [ ! -f %{_bindir}/g++-%{version} ]; then
    /usr/sbin/update-alternatives --remove g++ %{_bindir}/colorgcc
fi


%post c++
/usr/sbin/update-alternatives --install %{_bindir}/g++ g++ %{_bindir}/g++-%{version} %{alternative_priority} --slave %{_bindir}/c++ c++ %{_bindir}/g++-%{version}
[ -e %{_bindir}/g++ ] || /usr/sbin/update-alternatives --auto g++


%postun c++
if [ ! -f %{_bindir}/g++-%{version} ]; then
    /usr/sbin/update-alternatives --remove g++ %{_bindir}/g++-%{version}
fi


%post -n %{libstdcxx_name} -p /sbin/ldconfig
%postun -n %{libstdcxx_name} -p /sbin/ldconfig


%post -n %{libgcc_name} -p /sbin/ldconfig
%postun -n %{libgcc_name} -p /sbin/ldconfig


%post cpp
/usr/sbin/update-alternatives --install %{_bindir}/cpp cpp %{_bindir}/cpp-%{version} %{alternative_priority} --slave /lib/cpp lib_cpp %{_bindir}/cpp-%{version}
[ -e %{_bindir}/cpp ] || /usr/sbin/update-alternatives --auto cpp


%postun cpp
if [ ! -f %{_bindir}/cpp-%{version} ]; then
    /usr/sbin/update-alternatives --remove cpp %{_bindir}/cpp-%{version}
fi


%post -n %{libobjc_name} -p /sbin/ldconfig
%postun -n %{libobjc_name} -p /sbin/ldconfig

%if %{build_mudflap}
%post -n %{libmudflap_name} -p /sbin/ldconfig
%postun -n %{libmudflap_name} -p /sbin/ldconfig
%endif


%post -n %{libssp_name} -p /sbin/ldconfig
%postun -n %{libssp_name} -p /sbin/ldconfig


%post doc
%_install_info gcc.info
%_install_info cpp.info


%preun doc
if [ "$1" = "0" ];then /sbin/install-info %{_infodir}/gcc.info.bz2 --dir=%{_infodir}/dir --remove;fi;
%_remove_install_info cpp.info


%files -f %{name}.lang
%defattr(-,root,root)
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
#
%attr(0750,root,ctools) %{_bindir}/gcc%{branch}-version
%attr(0750,root,ctools) %{_bindir}/gcc-%{version}
%attr(0750,root,ctools) %{_bindir}/%{_target_platform}-gcc
%attr(0750,root,ctools) %{_bindir}/%{_target_platform}-gcc-%{version}
%attr(0750,root,ctools) %{_bindir}/protoize
%attr(0750,root,ctools) %{_bindir}/unprotoize
%attr(0750,root,ctools) %{_bindir}/gcov
%attr(0750,root,ctools) %{_bindir}/cc
%attr(0750,root,ctools) %{_bindir}/c89
%attr(0750,root,ctools) %{_bindir}/c99
#
%{_libdir}/libgcc_s.so
%ifarch %{nof_arches}
%{_libdir}/libgcc_s_nof.so
%endif
%ifarch %{biarches}
%{_prefix}/lib/libgcc_s.so
%{_prefix}/lib/libgcc_s_32.so
%endif
#
%dir %{gcc_libdir}/%{_target_platform}
%dir %{gcc_libdir}/%{_target_platform}/%{version}
#
%{gcc_libdir}/%{_target_platform}/%{version}/collect2
%{gcc_libdir}/%{_target_platform}/%{version}/crt*.o
%if "%{arch}" == "ppc"
%{gcc_libdir}/%{_target_platform}/%{version}/ecrt*.o
%{gcc_libdir}/%{_target_platform}/%{version}/ncrt*.o
%endif
%if "%{arch}" == "ppc64"
%{gcc_libdir}/%{_target_platform}/%{version}/ecrt*.o
%{gcc_libdir}/%{_target_platform}/%{version}/ncrt*.o
%endif
%{gcc_libdir}/%{_target_platform}/%{version}/libgcc.a
%{gcc_libdir}/%{_target_platform}/%{version}/libgcov.a
%{gcc_libdir}/%{_target_platform}/%{version}/libgcc_eh.a
%{gcc_libdir}/%{_target_platform}/%{version}/SYSCALLS.c.X
%ifarch %{biarches}
%dir %{gcc_libdir}/%{_target_platform}/%{version}/32
%{gcc_libdir}/%{_target_platform}/%{version}/32/crt*.o
%if "%{arch}" == "ppc64"
%{gcc_libdir}/%{_target_platform}/%{version}/32/ecrt*.o
%{gcc_libdir}/%{_target_platform}/%{version}/32/ncrt*.o
%endif
%{gcc_libdir}/%{_target_platform}/%{version}/32/libgcc.a
%{gcc_libdir}/%{_target_platform}/%{version}/32/libgcc_eh.a
%{gcc_libdir}/%{_target_platform}/%{version}/32/libgcov.a
%endif
%ifarch %{nof_arches}
%dir %{gcc_libdir}/%{_target_platform}/%{version}/nof
%{gcc_libdir}/%{_target_platform}/%{version}/nof/crt*.o
%{gcc_libdir}/%{_target_platform}/%{version}/nof/ecrt*.o
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libgcc.a
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libgcc_eh.a
%endif
#
%dir %{gcc_libdir}/%{_target_platform}/%{version}/include
%{gcc_libdir}/%{_target_platform}/%{version}/include/float.h
%if "%{arch}" == "i386"
%{gcc_libdir}/%{_target_platform}/%{version}/include/mm3dnow.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/mm_malloc.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/mmintrin.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/xmmintrin.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/pmmintrin.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/emmintrin.h
%endif
%if "%{arch}" == "x86_64"
%{gcc_libdir}/%{_target_platform}/%{version}/include/mm3dnow.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/mm_malloc.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/mmintrin.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/xmmintrin.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/pmmintrin.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/emmintrin.h
%endif
%if "%{arch}" == "ppc"
%{gcc_libdir}/%{_target_platform}/%{version}/include/spe.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/altivec.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/ppc-asm.h
%endif
%if "%{arch}" == "ppc64"
%{gcc_libdir}/%{_target_platform}/%{version}/include/spe.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/altivec.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/ppc-asm.h
%endif
%if "%{arch}" == "ia64"
%{gcc_libdir}/%{_target_platform}/%{version}/include/ia64intrin.h
%endif
%if "%{arch}" == "m68k"
%{gcc_libdir}/%{_target_platform}/%{version}/include/math-68881.h
%endif
%{gcc_libdir}/%{_target_platform}/%{version}/include/iso646.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/limits.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/stdarg.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/stdbool.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/stddef.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/syslimits.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/unwind.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/varargs.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/README

%files -n %{libgcc_name}
%defattr(-,root,root)
/%{_lib}/libgcc_s-%{version}.so.%{libgcc_major}
/%{_lib}/libgcc_s.so.%{libgcc_major}
%ifarch %{biarches}
/lib/libgcc_s-%{version}.so.%{libgcc_major}
/lib/libgcc_s.so.%{libgcc_major}
%endif
%ifarch %{nof_arches}
/%{_lib}/nof/libgcc_s-%{version}.so.%{libgcc_major}
/%{_lib}/nof/libgcc_s.so.%{libgcc_major}
%endif

%if %{build_mudflap}
%files -n %{libmudflap_name}
%defattr(-,root,root)
#
%{_libdir}/libmudflap.so.%{libmudflap_major}
%{_libdir}/libmudflap.so.%{libmudflap_major}.0.0
%{_libdir}/libmudflapth.so.%{libmudflap_major}
%{_libdir}/libmudflapth.so.%{libmudflap_major}.0.0
%ifarch %{biarches}
%{_prefix}/lib/libmudflap.so.%{libmudflap_major}
%{_prefix}/lib/libmudflap.so.%{libmudflap_major}.0.0
%{_prefix}/lib/libmudflapth.so.%{libmudflap_major}
%{_prefix}/lib/libmudflapth.so.%{libmudflap_major}.0.0
%endif

%files -n %{libmudflap_name}-devel
%defattr(-,root,root)
#
%{gcc_libdir}/%{_target_platform}/%{version}/include/mf-runtime.h
%{gcc_libdir}/%{_target_platform}/%{version}/libmudflap.a
%{gcc_libdir}/%{_target_platform}/%{version}/libmudflap.so
%{gcc_libdir}/%{_target_platform}/%{version}/libmudflapth.a
%{gcc_libdir}/%{_target_platform}/%{version}/libmudflapth.so
%ifarch %{biarches}
%{gcc_libdir}/%{_target_platform}/%{version}/32/libmudflap.a
%{gcc_libdir}/%{_target_platform}/%{version}/32/libmudflap.so
%{gcc_libdir}/%{_target_platform}/%{version}/32/libmudflapth.a
%{gcc_libdir}/%{_target_platform}/%{version}/32/libmudflapth.so
%endif
%endif

%files -n %{libssp_name}
%defattr(-,root,root)
%{_libdir}/libssp.so.%{libssp_major}
%{_libdir}/libssp.so.%{libssp_major}.0.0
%ifarch %{biarches}
%{_prefix}/lib/libssp.so.%{libssp_major}
%{_prefix}/lib/libssp.so.%{libssp_major}.0.0
%endif

%files -n %{libssp_name}-devel
%defattr(-,root,root)
%dir %{gcc_libdir}/%{_target_platform}/%{version}/include/ssp
%{gcc_libdir}/%{_target_platform}/%{version}/include/ssp/*.h
%{gcc_libdir}/%{_target_platform}/%{version}/libssp.a
%{gcc_libdir}/%{_target_platform}/%{version}/libssp_nonshared.a
%{gcc_libdir}/%{_target_platform}/%{version}/libssp.so
%ifarch %{biarches}
%{gcc_libdir}/%{_target_platform}/%{version}/32/libssp.a
%{gcc_libdir}/%{_target_platform}/%{version}/32/libssp_nonshared.a
%{gcc_libdir}/%{_target_platform}/%{version}/32/libssp.so
%endif


%files cpp
%defattr(-,root,root)
%{_mandir}/man1/cpp.1*
/lib/cpp
%ghost %attr(0750,root,ctools) %{_bindir}/cpp
%attr(0750,root,ctools) %{_bindir}/cpp-%{version}
%attr(0750,root,ctools) %{gcc_libdir}/%{_target_platform}/%{version}/cc1

%files c++
%defattr(-,root,root)
%{_mandir}/man1/g++.1*
%ghost %attr(0750,root,ctools) %{_bindir}/c++
%attr(0750,root,ctools) %{_bindir}/g++-%{version}
%attr(0750,root,ctools) %{_bindir}/c++-%{version}
%attr(0750,root,ctools) %{_bindir}/%{_target_platform}-g++
%attr(0750,root,ctools) %{_bindir}/%{_target_platform}-c++
#
%attr(0750,root,ctools) %{gcc_libdir}/%{_target_platform}/%{version}/cc1plus

%files -n %{libstdcxx_name}
%defattr(-,root,root)
%{_libdir}/libstdc++.so.%{libstdcxx_major}
%{_libdir}/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%ifarch %{biarches}
%{_prefix}/lib/libstdc++.so.%{libstdcxx_major}
%{_prefix}/lib/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%endif
%ifarch %{nof_arches}
%dir %{_libdir}/nof
%{_libdir}/nof/libstdc++.so.%{libstdcxx_major}
%{_libdir}/nof/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%endif

%files -n %{libstdcxx_name}-devel
%defattr(-,root,root)
%dir %{libstdcxx_includedir}
%{libstdcxx_includedir}/*
%{gcc_libdir}/%{_target_platform}/%{version}/include/cxxabi.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/bits/cxxabi_tweaks.h
#
%{gcc_libdir}/%{_target_platform}/%{version}/libstdc++.so
%{gcc_libdir}/%{_target_platform}/%{version}/libsupc++.a
%ifarch %{biarches}
%{gcc_libdir}/%{_target_platform}/%{version}/32/libstdc++.so
%{gcc_libdir}/%{_target_platform}/%{version}/32/libsupc++.a
%endif
%ifarch %{nof_arches}
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libstdc++.so
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libsupc++.a
%endif

%files -n %{libstdcxx_name}-static-devel
%defattr(-,root,root)
%{gcc_libdir}/%{_target_platform}/%{version}/libstdc++.a
%ifarch %{biarches}
%{gcc_libdir}/%{_target_platform}/%{version}/32/libstdc++.a
%endif
%ifarch %{nof_arches}
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libstdc++.a
%endif

%files objc
%defattr(-,root,root)
%attr(0750,root,ctools) %{gcc_libdir}/%{_target_platform}/%{version}/cc1obj
%{gcc_libdir}/%{_target_platform}/%{version}/libobjc.a
%{gcc_libdir}/%{_target_platform}/%{version}/libobjc.so
%ifarch %{biarches}
%{gcc_libdir}/%{_target_platform}/%{version}/32/libobjc.a
%{gcc_libdir}/%{_target_platform}/%{version}/32/libobjc.so
%endif
%ifarch %{nof_arches}
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libobjc.a
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libobjc.so
%endif
#
%dir %{gcc_libdir}/%{_target_platform}/%{version}/include/objc
%{gcc_libdir}/%{_target_platform}/%{version}/include/objc/*.h

%files -n %{libobjc_name}
%defattr(-,root,root)
%{_libdir}/libobjc.so.%{libobjc_major}
%{_libdir}/libobjc.so.%{libobjc_major}.0.0
%ifarch %{biarches}
%{_prefix}/lib/libobjc.so.%{libobjc_major}
%{_prefix}/lib/libobjc.so.%{libobjc_major}.0.0
%endif

%files colorgcc
%defattr (-,root,root)
%config(noreplace) %{_sysconfdir}/colorgccrc
%attr(0750,root,ctools) %{_bindir}/colorgcc
%attr(0750,root,ctools) %{_bindir}/colorgcc-%{version}

%files doc
%defattr(-,root,root)
%doc gcc/README* gcc/*ChangeLog*
%doc COPYING.colorgcc CREDITS.colorgcc ChangeLog.colorgcc
%doc rpm.doc/libobjc
%doc rpm.doc/objc
%doc rpm.doc/libstdc++-v3
%doc rpm.doc/cp
%{_infodir}/cppinternals.info*
%{_infodir}/cpp.info*
%{_infodir}/gcc.info*


%changelog
* Wed Nov 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.1
- P9, P10: two additional patches from Mandriva
- don't build mudflap support (use %%build_mudflap to define it; we may
  want it later)

* Tue Oct 31 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.1
- 4.1.1
- enable building SSP and libssp (we must build libssp until we move to glibc 2.4)
- P8: add -mtune=generic (gb)
- updated P2, P3 from Mandriva
- drop P7
- fix some file permissions; all compiler binaries should be mode 0750 and owned
  root:ctools (as a result, requires a newer setup)

* Wed Aug 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3
- spec cleanups
- remove locales

* Sat May 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3
- rebuild the toolchain against itself (gcc/glibc/libtool/binutils)
- change the avx_version macro to say '2.0' rather than '2.0-CURRENT'

* Fri May 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3
- 4.0.3
- update S6
- new patches from mdk's 4.0.3-1mdk
- fix buildreq's and prereq
- move all the docs to the -doc package

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3
- drop all SSP-related patches and all SSP-related stuff; this is a
  time sink for a one-man-show

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3
- for frick's sake... rebuild without SSP support to start the
  reversal (getting everything except the kernel and syslinux to
  build is good progress, but not good enough and something is wrong
  with the implementation in some way (why are we getting undefined
  references when -fstack-protector-all isn't even being passed?)

* Fri Dec 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3
- rebuild with SSP enabled gcc, glibc, and binutils
- don't patch the gcc specs just yet; for now direct the application
  of -fstack-protector-all via the rpm %%optflags
- use new %%_revrel macro
- obfuscate emails

* Wed Dec 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3-6avx
- uncompress patches
- get rid of the binutils_version macro
- re-enable the original SSP patch

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3-5avx
- rebuild on Annvix against new glibc

* Tue Aug 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3-4avx
- rebuild on Mandrake 10.2 (aka a 100% non-SSP system)

* Sat Jul 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3-3avx
- due to problems with compiling glibc, we are disabling SSP system-wide
  for the time being which will result in a full rebuild of the system
  but cannot be avoided... SSP support will hopefully be introduced at
  a later date; the important thing right now is to have a fully working
  and compilable system

* Thu Jul 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3-2avx
- don't apply P2 as it messes up the x86_64 build
- relocate where we apply the hardened specs patch so we can still
  use -bi --short-circuit
- fix the x86_64 biarch stuff
- fix the specs patch to not include PIE support for now

* Wed Jul 20 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3-1avx
- 3.4.3
- merge with mandrake 3.4.3-7mdk (from 10.2)
- completely remove java support
- completely remove ada support
- completely remove pdf doc support
- completely remove fortran support
- completely remove pascal support
- completely remove libffi support
- build colorgcc by default
- remove support for snapshots; we'll only ever use final builds
- remove all support for cross-compilation; we don't need it and it
  adds too much complexity
- always build as the system compiler
- always make check
- always build c++ support
- always build objc support
- always build the doc package (just info files)
- massive spec cleanup
- drop all patches except the colorgcc patch and the pch-mdkflags patch
- include the HLFS gcc patches (P1-P4)
- update P5 to include PIE support

* Thu Jun 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.3.1-8avx
- recompile with stack protection enabled
- note in version string that ssp is enabled
- P302: patch the specs file during build; using perl seems to fail

* Thu Jun 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.3.1-7avx
- use the HLFS SSP patches (P301) and regen P300 for rejects
  [gcc/Makefile.in]
- fix url for bug reports
- remove /etc/profile.d/ssp.{sh,csh} files as the only specs with
  %%build_ssp are gcc and rpm
- remove %%build_ssp macro; *always* build with SSP
- update specs to make gcc always compile stuff with -fstack-protector-all
  (thanks Robert)
- some macros
- bootstrap build; don't build with -fstack-protector-all

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.3.1-6avx
- Annvix build
- ssp 3.3.2-2; regenerated patch

* Sat Feb 07 2004 Vincent Danen <vdanen@opensls.org> 3.3.1-5sls
- ssp 3.3-7; regenerated patch
- s/propolice/ssp/ (aka use the real name)
- build with new macros
- more branding

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 3.3.1-4sls
- sync with 3mdk (gbeauchesne): fix regmove, aka. fix gsl miscompilation on
  amd64 (mainline CVS)
- sync with 4mdk (gbeauchesne): really ship with {,x}mmintrin.h on amd64

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 3.3.1-3sls
- propolice 3.3-5; regenerated patch
- make profile.d files mode 0755
- when we do our propolice build (opensls default), we don't make
  ada, doc-pdf, doc, fortran, pascal, or java packages
- fix inclusion of libffi stuff (should only be built when java is built)

* Wed Oct 22 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.3.1-2.2mdks
- create profile.d files to set STACK_PROTECTOR=true

* Fri Oct  3 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.3.1-2.1mdks
- build with propolice as default

* Sun Sep 21 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.3.1-2mdks
- Added Propolice Stack Protector and regenerated its patch (Patch300)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
