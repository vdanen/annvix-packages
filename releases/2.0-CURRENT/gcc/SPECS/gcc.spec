#
# spec file for package gcc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision		$Rev$
%define name			gcc%{package_suffix}
%define version			3.4.4
%define release			%_revrel

%define package_suffix		%{branch}
%define program_suffix		-%{version}

%define _unpackaged_files_terminate_build 0
%define _provides_exceptions libstdc++.so.6\\|devel(libstdc++)

%define branch			3.4
%define branch_tag		%(perl -e 'printf "%%02d%%02d", split(/\\./,shift)' %{branch})
%define biarches		x86_64
%define color_gcc_version	1.3.2

%define libgcc_major		1
%define libstdcxx_major		6
%define libstdcxx_minor		3
%define libgcc_name_orig	libgcc
%define libgcc_name		%{libgcc_name_orig}%{branch}
%define libstdcxx_name_orig	libstdc++
%define libstdcxx_name		%{libstdcxx_name_orig}%{branch}

%define alternative_priority	30%{branch_tag}
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
# FIXME: unless we get proper help2man package
Source6:	gcc33-help2man.pl

Patch1:		gcc-3.4.0-mdk-pchflags.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
# Want updated alternatives priorities
# We want -pie support
Requires:	binutils >= 2.15.92.0.2-1mdk
BuildRequires:	binutils >= 2.15.92.0.2-1mdk
# Make sure gdb will understand DW_FORM_strp
Conflicts:	gdb < 5.1.1
BuildRequires:	zlib-devel
Requires:	%{name}-cpp = %{version}-%{release}
# FIXME: We need a libgcc with 3.4 symbols
Requires:	%{libgcc_name_orig} >= 3.3.2-5mdk
Requires(post):	/usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
BuildRequires:	gettext, flex, bison
BuildRequires:	texinfo >= 4.1
# Make sure pthread.h doesn't contain __thread keyword
Requires:	glibc-devel >= 2.2.5-14mdk
BuildRequires:	glibc-devel >= 2.2.5-14mdk
BuildRequires:	glibc-static-devel >= 2.2.5-14mdk
Obsoletes:	gcc%{branch}
Provides:	gcc%{branch} = %{version}-%{release}
BuildRequires:	dejagnu

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
Requires(post):	/usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives

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
#Provides:	%{libstdcxx_name_orig} = %{version}-%{release}

%description -n %{libstdcxx_name}
This package contains the GCC Standard C++ Library v3, an ongoing
project to implement the ISO/IEC 14882:1998 Standard C++ library.

%package -n %{libstdcxx_name}-devel
Summary:	Header files and libraries for C++ development
Group:		Development/C++
Requires:	%{libstdcxx_name} = %{version}-%{release}
Obsoletes:	%{libstdcxx_name_orig}%{branch}-devel
Provides:	%{libstdcxx_name_orig}%{branch}-devel = %{version}-%{release}
#Provides:	%{libstdcxx_name_orig}-devel = %{version}-%{release}

%description -n %{libstdcxx_name}-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development.


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

You should install this package if you are a programmer who is searching for
such a macro processor.

If you have multiple versions of GCC installed on your system, you
will have to type "cpp -V%{version}" or "cpp-%{version}" (without double quotes)
in order to use the GNU C Preprocessor version %{version}.

####################################################################
# Documentation

%package doc
Summary:	GCC documentation
Group:		Development/Other
Obsoletes:	gcc%{branch}-doc
Provides:	gcc%{branch}-doc = %{version}-%{release}
Conflicts:	gcc-doc < %{branch}
Requires(post):	info-install
Requires(preun): info-install

%description doc
GCC is a compiler suite aimed at integrating all the optimizations and
features necessary for a high-performance and stable development
environment. This package contains the compiler documentation in INFO
pages.


%prep
%setup -q -n gcc-%{version}

%patch1 -p1 -b .pch-mdkflags

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
cat %{SOURCE6} >bin/help2man
export PATH=$PATH:$PWD/bin

# Make bootstrap-lean
CC=gcc
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g' -e 's/-mcpu=pentiumpro//g'`
%if %{build_debug}
OPT_FLAGS=`echo "$OPT_FLAGS -g" | sed -e "s/-fomit-frame-pointer//g"`
%endif
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-fomit-frame-pointer//g'`

# update config.{sub,guess} scripts
%{?__cputoolize: %{__cputoolize} -c ..}
%{?__cputoolize: %{__cputoolize} -c ../boehm-gc}
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
    ../configure \
	--prefix=%{_prefix} \
	--libexecdir=%{_prefix}/lib \
	--with-slibdir=/%{_lib} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--enable-shared \
	--enable-threads=posix \
	--disable-checking \
	--enable-long-long \
	--enable-__cxa_atexit \
	--enable-clocale=gnu \
	--disable-libunwind-exceptions \
	--enable-languages="c,c++" \
	--host=%{_target_platform} \
	--target=%{_target_platform} \
	--with-system-zlib \
	--program-suffix=%{program_suffix}
touch ../gcc/c-gperf.h
%ifarch %{ix86} x86_64
%make profiledbootstrap BOOT_CFLAGS="$OPT_FLAGS"
%else
%make bootstrap-lean BOOT_CFLAGS="$OPT_FLAGS"
%endif

# Make protoize
make -C gcc CC="./xgcc -B ./ -O2" proto
cd ..

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

pushd obj-%{_target_platform}
    %makeinstall_std
popd

FULLVER=`%{buildroot}%{_bindir}/%{_target_platform}-gcc%{program_suffix} --version | head -n 1 | cut -d' ' -f3`
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
	        $STRIP_DEBUG ../../../../$libname.so.$libversion
	        $STRIP_DEBUG ../../../../$libname.a
	        ln -s ../../../../$libname.so.$libversion $libname.so
	        rm -f ../../../../$libname.so
	        [ -r "../../../../$libname.a" ] && {
	            cp -f ../../../../$libname.a $libname.a
	            rm -f ../../../../$libname.a
	        }
	    popd
	%endif
	%ifarch ppc
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
(cd $FULLPATH;
	DispatchLibs libstdc++	%{libstdcxx_major}.0.%{libstdcxx_minor}
	mv ../../../../%{_lib}/libsupc++.a libsupc++.a
	%ifarch %{biarches}
	    mv -f ../../../libsupc++.a 32/libsupc++.a
	%endif
	%ifarch ppc
	    mv -f ../../../nof/libsupc++.a nof/libsupc++.a
	%endif
)

# Move <cxxabi.h> to compiler-specific directories
mv %{buildroot}%{libstdcxx_includedir}/cxxabi.h $FULLPATH/include/

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
%ifarch ppc
    chmod 0755 libgcc_s_nof.so.%{libgcc_major}
    mv -f  libgcc_s_nof.so.%{libgcc_major} %{buildroot}/%{_lib}/libgcc_s_nof-%{version}.so.%{libgcc_major}
    ln -sf libgcc_s_nof-%{version}.so.%{libgcc_major} %{buildroot}/%{_lib}/libgcc_s_nof.so.%{libgcc_major}
    ln -sf ../../%{_lib}/libgcc_s_nof.so.%{libgcc_major} %{buildroot}%{_libdir}/libgcc_s_nof.so
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

# fix doc locations
mkdir docs-{cp,libstdc++-v3}
cp -a gcc/cp/ChangeLog* docs-cp/
cp -a libstdc++-v3/{ChangeLog,README}* docs-libstdc++-v3/
cp -a libstdc++-v3/docs/html/ docs-libstdc++-v3/

%if %{build_debug}
# Don't strip in debug mode
export DONT_STRIP=1
%endif


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
update-alternatives --install %{_bindir}/gcc gcc %{_bindir}/gcc-%{version} %{alternative_priority}
[ -e %{_bindir}/gcc ] || update-alternatives --auto gcc


%postun
if [ ! -f %{_bindir}/gcc-%{version} ]; then
    update-alternatives --remove gcc %{_bindir}/gcc-%{version}
fi


%post c++
update-alternatives --install %{_bindir}/g++ g++ %{_bindir}/g++-%{version} %{alternative_priority} --slave %{_bindir}/c++ c++ %{_bindir}/g++-%{version}
[ -e %{_bindir}/g++ ] || update-alternatives --auto g++

%postun c++
if [ ! -f %{_bindir}/g++-%{version} ]; then
    update-alternatives --remove g++ %{_bindir}/g++-%{version}
fi

%post -n %{libstdcxx_name} -p /sbin/ldconfig
%postun -n %{libstdcxx_name} -p /sbin/ldconfig

%post -n %{libgcc_name} -p /sbin/ldconfig
%postun -n %{libgcc_name} -p /sbin/ldconfig

%post cpp
update-alternatives --install %{_bindir}/cpp cpp %{_bindir}/cpp-%{version} %{alternative_priority} --slave /lib/cpp lib_cpp %{_bindir}/cpp-%{version}
[ -e %{_bindir}/cpp ] || update-alternatives --auto cpp

%postun cpp
if [ ! -f %{_bindir}/cpp-%{version} ]; then
    update-alternatives --remove cpp %{_bindir}/cpp-%{version}
fi

%post doc
%_install_info gcc-%{branch}.info
%_install_info cpp-%{branch}.info


%preun doc
if [ "$1" = "0" ];then /sbin/install-info %{_infodir}/gcc-%{branch}.info.bz2 --dir=%{_infodir}/dir --remove;fi;
%_remove_install_info cpp-%{branch}.info


%files
%defattr(-,root,root)
%{_mandir}/man1/gcc%{program_suffix}.1*
%{_mandir}/man1/gcov%{program_suffix}.1*
#
%{_bindir}/gcc%{branch}-version
%{_bindir}/gcc-%{version}
%{_bindir}/%{_target_platform}-gcc%{program_suffix}
%{_bindir}/protoize%{program_suffix}
%{_bindir}/unprotoize%{program_suffix}
%{_bindir}/gcov%{program_suffix}
#%{_bindir}/cc
#
%{_libdir}/libgcc_s.so
%ifarch ppc
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
%{gcc_libdir}/%{_target_platform}/%{version}/32/libgcc.a
%{gcc_libdir}/%{_target_platform}/%{version}/32/libgcc_eh.a
%{gcc_libdir}/%{_target_platform}/%{version}/32/libgcov.a
%endif
%ifarch ppc
%dir %{gcc_libdir}/%{_target_platform}/%{version}/nof
%{gcc_libdir}/%{_target_platform}/%{version}/nof/crt*.o
%{gcc_libdir}/%{_target_platform}/%{version}/nof/ecrt*.o
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libgcc.a
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libgcc_eh.a
%endif
%{gcc_libdir}/%{_target_platform}/%{version}/specs
#
%dir %{gcc_libdir}/%{_target_platform}/%{version}/include
%{gcc_libdir}/%{_target_platform}/%{version}/include/float.h
%if "%{arch}" == "i386"
%{gcc_libdir}/%{_target_platform}/%{version}/include/mmintrin.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/xmmintrin.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/pmmintrin.h
%{gcc_libdir}/%{_target_platform}/%{version}/include/emmintrin.h
%endif
%if "%{arch}" == "x86_64"
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
%ifarch ppc
/%{_lib}/libgcc_s_nof-%{version}.so.%{libgcc_major}
/%{_lib}/libgcc_s_nof.so.%{libgcc_major}
%endif

%files cpp
%defattr(-,root,root)
%{_mandir}/man1/cpp%{program_suffix}.1*
/lib/cpp
%ghost %{_bindir}/cpp
%{_bindir}/cpp-%{version}
%{gcc_libdir}/%{_target_platform}/%{version}/cc1

%files c++
%defattr(-,root,root)
%{_mandir}/man1/g++%{program_suffix}.1*
%ghost %{_bindir}/c++
%{_bindir}/g++-%{version}
%{_bindir}/c++-%{version}
%{_bindir}/%{_target_platform}-g++%{program_suffix}
%{_bindir}/%{_target_platform}-c++%{program_suffix}
#
%{gcc_libdir}/%{_target_platform}/%{version}/cc1plus

%files -n %{libstdcxx_name}
%defattr(-,root,root)
#%{_libdir}/libstdc++.so.%{libstdcxx_major}
%{_libdir}/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%ifarch %{biarches}
#%{_prefix}/lib/libstdc++.so.%{libstdcxx_major}
%{_prefix}/lib/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%endif
%ifarch ppc
%dir %{_libdir}/nof
#%{_libdir}/nof/libstdc++.so.%{libstdcxx_major}
%{_libdir}/nof/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%endif

%files -n %{libstdcxx_name}-devel
%defattr(-,root,root)
%dir %{libstdcxx_includedir}
%{libstdcxx_includedir}/*
%{gcc_libdir}/%{_target_platform}/%{version}/include/cxxabi.h
#
%{gcc_libdir}/%{_target_platform}/%{version}/libstdc++.so
%{gcc_libdir}/%{_target_platform}/%{version}/libsupc++.a
%ifarch %{biarches}
%{gcc_libdir}/%{_target_platform}/%{version}/32/libstdc++.so
%{gcc_libdir}/%{_target_platform}/%{version}/32/libsupc++.a
%endif
%ifarch ppc
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libstdc++.so
%{gcc_libdir}/%{_target_platform}/%{version}/nof/libsupc++.a
%endif


%files doc
%defattr(-,root,root)
%doc gcc/README* gcc/*ChangeLog*
%doc docs-cp docs-libstdc++-v3
%{_infodir}/cppinternals-%{branch}.info*
%{_infodir}/cpp-%{branch}.info*
%{_infodir}/gcc-%{branch}.info*


%changelog
* Sat May 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3
- exclude provides of libstdc++, libstdc++.so.6, libstdc++-devel, and
  devel(libstdc++) to avoid installation alongside the libstdc++ that
  we really want

* Sat May 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3
- don't include the libstdc++.so.6 symlink because libstdc++6 provides
  it and we need to be able to have the two packages available without
  conflicts (and also the installer pulls this libstdc++ in instead of
  the one we want since both provide the symlink)
- fix prereq's
- move all the docs to the -doc subpackage

* Sat May 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4.3
- build with a program-suffix so that we can install both gcc3 and gcc4
  together (we need gcc3 for the kernel)
- don't include cc, c89, and c99
- drop objc support
- drop colorgcc
- change the avx_version macro to say '2.0' rather than '2.0-CURRENT'

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

* Mon Sep  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.1-2mdk
- Assorted fixes from current CVS:
  - Patch6: Fix ICE when compiling busybox at -Os
  - Patch7: Fix kernel 2.6-test4 miscompilation on IA-32
  - Patch8: Fix libmcrypt miscompilation on PPC
  - Patch9: Fix -Wunreachable-code

* Wed Aug  6 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.1-1mdk
- 3.3.1
- Patch5: gcse fix (Josef Zlomek, 3.3-hammer branch)

* Fri Jul 25 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.1-0.7mdk
- Build GNU Pascal compiler on AMD64 too
- Update to 3.3-branch 2003/07/25, which fixes PRs op/8878, opt/4490,
  opt/10679, c++/10796, c++/11546, c++/11282, c++/11645, c++/11513
- Patch4: Reload fix (Jan Hubicka, PR target/9929)

* Sat Jul 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.1-0.6mdk
- Revert to 3.3-hammer 2003/05/20 for now
- Update to 3.3-branch 2003/07/19, which fixes PRs target/10907,
  target/11556, optimization/11083

* Fri Jul 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.1-0.5mdk
- Integrate GNU Pascal compiler snapshot 2003/05/07
- Patch1: Fix loop optimizer (Eric Botcazou, PR opt/11536)
- Patch2: Fix VRP on kernel compilation (Josef Zlomek, PR opt/11559)
- Patch3: Fix constant folding bug (Mark Mitchell, PR opt/11557)

* Thu Jul 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.1-0.4mdk
- Don't enable VRP at -O2 by default
- Merge with 3.3-branch 2003/07/15, which fixes PRs debug/11473,
  opt/11320, debug/11098, opt/11440, opt/10877, opt/9745,
  target/10021, opt/11368, opt/11198, opt/11304, c++/1607, opt/11440,
  c++/c++/7053, c++/11154, c++/11503, c++/9738, c++/8164, c++/10558,
  c++/10032, c++/10527, c++/10849, c++/11236, c++/11345, c++/11431,
  fortran/11301

* Wed Jul 16 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.1-0.3mdk
- Merge with 3.3-rhl-branch 2003/07/08:
  - Add gcc 2.96-RH compat, fde_merge compat
  - Fix PR debug/7241
  - Fix IA-64 libgcc unwinder
  - Add missing DW_AT_comp_dir if necessary
  - Add IA-64 and s390* DW_OP_GNU_push_tls_address
  - Fix another missing trunc_int_for_mode in combiner
  - Convert PowerPC port to target_flags_explicit
  - AMD64 TLS fix
  - Fix tree inliner
  - Fix IA-64 symbol_ref_flags usage
  - Add direct segment addressing for x86 TLS
  - Add -fpie/-fPIE support
  - Emit .note.GNU-stack section on linux arches which by default need
    executable stack
  - Make calls in virtual thunks local if possible
  - Fix __PRETTY_FUNCTION__ (PR c++/6794)
  - Make libffi .eh_frame PC-relative if -fpic/-fPIC/-mrelocatable on
    IA-64 and PPC32, thusly possibly making them into ro section
  - Use GCC intrinsics to implement locks in IA-64 libjava

* Thu Jul 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.1-0.2mdk
- Ship with 32-bit libffi.a on bi-arch platforms
- Bi-arch library packages are still named lib<foo>, not lib64<foo>

* Tue Jul  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3.1-0.1mdk
- Update to 3.3-hammer branch as of 2003/07/03

* Tue Jun 17 2003 Juan Quintela <quintela@trasno.org> 3.3-2mdk
- Add reload1 patch (fix bug http://gcc.gnu.org/bugzilla/show_bug.cgi?id=10890).

* Mon Jun  2 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3-1mdk
- Update to 3.3-hammer branch as of 2003/05/23

* Fri May  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.3-1mdk
- Handle gcj-tools (java) alternatives as suggested by Michael Reinsch
- Patch607: Install unwind.h in gcc-private directory
- Patch608: Install libffi headers and static library
- Update to 3.2-rhl8-branch 2003/05/06, with notable changes:
  - Fix PRs target/9681, c/2454, middle-end/10336, c++/10401,
    target/10377, opt/10352, c/10175, other/6955, middle-end/9967,
    target/7784, c/8224, ada/9953, target/10067, c/8281, target/10114,
    target/10084, sw-bug/10234, target/7784, optimization/10171,
    optimization/8746, target/10377, middle-end/9967, libstdc++/10167
  - Fix boehm-gc on PPC (Tom Tromey)
  - Unwind fixes for location expressions
  - Allow __REDIRECT on builtins
  - Add __builtin_memmove and __builtin_bcopy

* Thu Apr 24 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3-0.2mdk
- Update to 3.3-hammer branch as of 2003/04/20

* Wed Apr  2 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.2-5mdk
- Patch612: A member template only matches a member template (Jason
  Merrill, backport from 3.3-branch, fix PRs c++/8660, c++/10265)
- Update to 3.2-rhl8-branch 2003/03/24, with notable changes:
  - Fix PRs c/8068, c/9678, opt/9768, opt/8613, c/8828, other/3782,
    libgcj/9652, c/5059, c/6126, other/9671, opt/9226, target/8343,
    other/9638, c/9799, other/9954, opt/8726, middle-end/7796,
    opt/9888, c/9928, opt/8178, opt/8396, target/9164, target/7248,
    target/10073, opt/8746, opt/8366, doc-bug/9813, opt/10116,
    target/9797, opt/9414, c++/7050, c++/9459, c++/7982, c++/9602,
    c++/9798, c++/9420, c++/6440, c++/9993, c++/8316, c++/9315,
    c++/10136, libstdc++/9169
  - Fix RH Issue Tracker #13215, #14363, #7487
  - Handle denormal constants in hexadecimal notation
  - Fix scheduler to handle possible trapping instructions in a bundle
  - Add ldxmov support on IA-64
  - Backport the DFA scheduler and new IA-64 instruction bundling
  - Fix ifcvt on IA-64
  - Add and default to -feliminate-unused-debug-types
  - Fix postincrement before switch (miscompilations on IA-32 and X86-64)
  - Fix __builtin_expect (setjmp (buf) == 0, 1))
  - Define __LP64__ and _LP64 on x86-64
  - Fix P4 failures with -Os
  - Fix IA-64 __sync_*_compare_and_swap_si intrinsic
  - Fix typeid with reference types

* Sun Mar 16 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.2-4mdk
- Conditionalize build of C++ front-end
- Let it build a cross-compiler with --define "cross <arch>"
- Patch615: Handle gxx_include_dir for cross-compilers and don't mess
  out system headers though they are correctly arch-split
- Patch616: Workaround cross gcc bootstrap build with no glibc
  headers. Headers should really be retrieved from glibc proper
- Patch617: Serialize build of crt* files, since they may have to
  generate a new c-parse.y but two jobs could be started in parallel

* Mon Mar  3 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.2-3mdk
- Patch613: Fix -O2 -fPIC on ppc32 (PR target/9732, xvid crash)
- Patch614: Fix ICE in _Complex return values on x86-64

* Mon Feb 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.2-2mdk
- Patch610: Fix PR c/8068, an infinite recursion in fold-const.c
  (Arend Bayer & Richard Henderson in CVS 3.2-branch)
- ColorGCC updates:
  - Obsoletes: gcc2.96-colorgcc
  - Check for self-referencement
  - Enable colorgcc for gcj, g77, f77 too
  - Only support colorgcc for the system compiler by default. The user
    may still hand-edit %{_sysconfdir}/colorgccrc though. As an extra,
    enable definition of gccVersion to automatically append
    "-<gccVersion>" to user-defined compilers paths.

* Sat Feb 15 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.2-1mdk
- Update to 3.2-rhl8-branch 2003/02/13, with notable changes:
  - Fix PRs opt/7702, c/7741, c/9530, opt/9493, opt/9492, c++/8674,
    c++/7129, libstdc++/9538, libstdc++/9507
  - Fix latent bug in crossjumping
  - Fix libffi/ppc alignment bug for floats

* Sat Feb  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.1-7mdk
- Fix lib{gnarl,gnat}.so symlinks (#1414)
- Disable ada95 build on alpha
- Patch610: Fix biarch build & install
- Patch611: Fix __PRETTY_FUNCTION__ failure in C++ template
  destructors (PR c++/7768, PR c++/9622)

* Thu Feb  6 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.1-6mdk
- Split Patch102 (DESTDIR) to pass-slibdir patch and nihil
- Patch609: Fix x86-64 {ashlsi3,addsi}_1_zext splitters (Richard Henderson)
- Update to 3.2-rhl8-branch 2003/02/02, with notable changes:
  - Fix PRs ada/8344, opt/8555, c/9506, c++/9433, target/9316,
    preprocessor/9465
  - Fix ppc32 libffi closure relocations
  - Fix -fPIC on ppc32 (#79732)
  - add DW_AT_comp_dir attribute to compilation unit even if the main
    input filename is absolute, but at least one of its includes are
    relative

* Thu Feb  6 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.3-0.1mdk
- Update to 3.3-hammer branch as of 2003/02/05

* Wed Jan 29 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.1-5mdk
- Patch607: Add x86-64 closures to libffi (Andrew Haley)
- Patch608: Enable Java interpreter on x86-64
- Update to 3.2-rhl8-branch 2003/01/27, with notable changes:
  - Fix PRs objc/9267, fortran/9258, java/6748, opt/7507, c++/9328,
    c++/47, PR libstdc++/9322,
  - Fix %%xmm register moves
  - Fix loop-3c on x86 as -Os
  - Fix sse intrinsics for _mm_stream_pi()

* Fri Jan 24 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.1-4mdk
- Patch605: Make some tests PASS or XFAIL on x86-64 if building with -m32
- Patch606: Adjust gcc.dg/20020312-2.c test for x86-64 (Andreas Jaeger)

* Wed Jan 22 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.1-3mdk
- Enable Ada on x86-64
- Enable multilibs regression testing on x86-64
- Patch604: Fix libjava biarch build on x86-64
- Update to 3.2-rhl8-branch 2003/01/16, with notable changes:
  - Fix PRs opt/8794, opt/8599, preprocessor/8880, c/8032,
    inline-asm/8832, c++/8031, c++/8442, c++/8503 (aka. remove DR 295
    implementation), libstdc++/9076, libstdc++/8887, libstdc++/9168,
    libstdc++/9151, libstdc++/8707, libstdc++/9269
  - Fix MD_FALLBACK_FRAME_STATE_FOR on x86-64
  - Fix g++.dg/tls failures on IA-64
  - Fix libffi on IA-64 and PowerPC

* Fri Dec 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.1-2mdk
- Patch605: Fix loop optimizer (Eric Botcazou, PR opt/8988)

* Thu Dec 19 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2.1-1mdk
- BuildRequires: glibc-static-devel
- Update to 3.2-rhl8-branch 2002/12/10, with notable changes:
  - Forbid in-class initializers of static data members that do not
    have arithmetic or enumeration type. i.e. make it even more ISO
    C++ compliant.
  - Fix PRs c/7622, c/8639, c/8588, c/8518, c/8439, optimization/8275,
    optimization/8599, c++/8214, c++/8493, c++/8332, c++/8663,
    c++/8727, c++/5919, c++/8615, c++/8799, c++/8372,
    preprocessor/8524, libstdc++/8230, libstdc++/8708, libstdc++/8790,
    libstdc++/7445, libstdc++/6745, libstdc++/8399, libstdc++/8230
  - change -pthread so that it adds -lpthread even if -shared
  - fix .eh_frame section in crtend*.o on x86-64
  - make sure .rodata.cstNN section entries have size sh_entsize
  - readonly .eh_frame and .gcc_except_table section (needs
    binutils change too)
  - fix force_to_mode (#77756)
  - avoid creating invalid subregs in combiner (Dale Johannesen,
    #75046, #75415, #76058, #76526, #78406)
  - avoid using strtok in libstdc++-v3 for thread safety
    (Paolo Carlini, Nathan Myers)

* Sun Nov 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2-4mdk
- Get rid of -mb-step on IA-64 since production machines are available
- Move on to gcc-3.2-rhl8-branch (2002/11/17): that's actually 3.2.1 +
  several patches merged in for TLS support, better x86-64 support and
  other fixes.

* Mon Nov  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2-3mdk
- Patch65: Fix x86-64 ICE with stdarg in -fpic (Jakub Jelinek, RH 3.2-11)
- Patch610: Fix RTL sharing problems. Aka fix gmp miscompilation on
  x86-64 (Jan Hubicka)
- Patch611: Fix reload on IA-32. Aka fix hdf5 miscompilation (Jim Wilson)
- Patch612: Fix x86-64 relocations in PIC (Jan Hubicka)
- Patch613: Set proper defaults for i386 in x86-64 compiler (Jan Hubicka)

* Fri Sep 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2-2mdk
- Disable -momit-leaf-frame-pointer by default on IA-32 too
- Fix Patch603 (x86_64-struct-args) with missing hunk
- Patch64: Fix x86-64 %RIP to %rip, only output (%rip) if no other
  relocation is used (Richard Henderson, RH 3.2-4)
- Patch608: Warn about known bugs in G++ that result in incorrect
  object layouts (Mark Mitchell)
- Patch609: Fix -m32 build of libjava on x86-64 and <bits/syscall.h>
  doesn't define SYS_sigaction from native glibc
- Merge with SuSE releases (8 new patches):
  - Fix startfile_prefix_spec() check in Patch507 (x86_64-biarch)
  - Add Java support to x86-64 (libffi, boehm-gc, libffi)
  - Fix returning of structs on x86-64
  - Fix athlon alignment requirement for branch targets
  - Various x86-64 code generation fixes
  - Fix x86-64 Objective C nil_method implementation
  - Fix SPEC2000 sixtrack miscompilation

* Sat Aug 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2-1mdk
- Update to final gcc3.2 tarball
- Patch606: Strip ".." components when prior dir doesn't exist (Alan Modra)
- Jeff has Ada front-end now on alpha :)
- Nuke %%{?%%build_*} constructs in filelist for pdf-doc. Aka better
  let rpm has problems with --without PDF instead

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2-0.3mdk
- Make check by default
- Rediff Patch505 (x86_64-profile)
- Patch603: Fix computing of field's offsets in args passing on
  x86-64. Fix kdelibs miscompilation (PR target/7559, Jan Hubicka)
- Patch604: Fix ICE in change_address_1, at emit-rtl.c:1934 on
  x86-64. Fix hdf5 build.  (PR target/7434, Jan Hubicka)
- Patch605: Misc fixes on x86-64 exhausted by the regresssion
  testsuite. Handle variable sized types (Jan Hubicka)
- Explicit Requires: %{libgnat_name} for gcc-gnat
- Update to 3.2-branch 2002/08/12, with notable changes:
  - Make __m64 type 64-bit aligned on MMX targets
  - Fix virtual function ordering (C++ ABI change, PR c++/7470)
  - Lots ABI incompatible changes in libstdc++.so.5
  - ABI incompatible changes in long long bitfield layout on IA-32
    (both C and C++), oversized bitfields layout on IA-32 and
    bitfields with base type with __attribute__((aligned ()))
  - Fix strstream segfaults (#68292, Benjamin Kosnik)
- Merge with Red Hat release (16 new patches):
  - add testcases for PR c++/5857, PR c++/6381
  - make sure pic register is set up even when the only @PLT calls
    are done in EH basic blocks (Richard Henderson)
  - fix __attribute__((visibility())) together with __asm__()
    function redirection
  - fix fold-const bug (#70541)
  - fix inlining bug with labels (#70941)
  - fix PR preprocessor/7358 (Neil Booth)
  - fix K6 ICE on linux kernel (#69989, Richard Sandiford, Jan Hubicka)
  - add -mcmodel= x86-64 documentation (Andreas Jaeger)
  - fix istream::ignore() (Benjamin Kosnik)
  - various TLS fixes but we don't use TLS for MDK 9.0

* Mon Jul 29 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2-0.2mdk
- Use BOOT_CFLAGS on alpha
- Add PDF docs in a new subpackage
- Really add Ada95 info pages
- Really ship with <gcj/libgcj-config.h>
- Provide %{_includedir}/libgcj as an alternative
- Add Requires: %{GCJ_TOOLS} to gcc-java package. Add jdk-config script
- Update to 3.2-branch 2002/07/26, with notable changes:
  - Add placement delete (PR libstdc++/7286)
  - Fix placement delete signatures
  - Implement behavior mandated by DR 179 for std::dequeue<> (PR libstdc++/7186)
  - Fix char_traits for basic_streambuf, basic_stringbuf, and stringstream
  - Fix basic_iostream::traits_type to comply with DR 271 (PR libstdc++/7216)
  - Fix basic_istream::ignore() (PR libstdc++/7220)
  - Fix locale::operator ==() (PR libstdc++/7222)

* Wed Jul 24 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2-0.1mdk
- Fix typos in doc %%preun
- Use latest patchset for Gcc 3.2 update (Jakub Jelinek)
- Version script is now named %{cross_prefix}gcc%{branch}-version
- Really do libification with no incoherent-version-in-name
- Remove Requires: libobjc >= 2.96-0.59mdk for gcc-objc

* Wed Jul 24 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-1mdk
- Patch601: Fix bzero() on x86-64 (Frank van der Linden, PR opt/7291)
- Update to 3.1-branch 2002/07/24, nothing really new but this is very
  likely to become final release unless showstoppers are reported

* Mon Jul 22 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-0.10mdk
- Add Ada 95 front-end

* Mon Jul 22 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-0.9mdk
- Only Requires: perl for gcc-colorgcc
- Remove scrt objects from PPC builds (Stew)
- We now have versioned libstdcxx_incdir, that is c++/<VERSION>/
- Update to 3.1-branch 2002/07/21, with notable changes:
  - Fix ifcvt on ppc that caused miscompilation of Mozilla (PR opt/7147)
  - Bulk libstdc++-v3 documentation merge for 3.1.1 release ;-)
- Merge with Red Hat releases (2 new patches):
  - fixed DWARF-2 output for const char * (PR debug/7241)
  - fix typo in i386 specs (PR c/7242)
  - Use __cxa_atexit for standard compliance:
    if your C++ project knows it won't call atexit() from within its
    static constructors, use -fno-use-cxa-atexit to optimize it

* Thu Jul 18 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-0.8mdk
- Patch601: Add NRVO tests for PR c++/7145, PR c++/7279
- Patch602: Fix prefetch on x86-64 (Jan Hubicka)
- Patch508: Fix prefetching (Janis Johnson, SuSE 3.1.1-21)
- Add libgcj symlink to get to %{libjava_includedir}
- Update to 3.1-branch 2002/07/18, with notable changes:
  - Fix ICE in find_reloads when compiling ffmpeg (PR opt/7246)
  - Fix bad operands for 'movsbl' on IA-32 (PR c/7153)
  - Fix template regression involving sizeof (PR c++/7112)
  - Fix ICE on illegal code containing incomplete class deep inside
    some complex class structure (PR c++/6716)
  - Handle multi-dimensional arrays in default copy constructor (PR c++/6944)
  - Emission of std::__default_alloc_template<>, should be weak (PR c++/6611)
  - Fix NRVO when return value is initialized with "{...}" (PR opt/7145)
  - Fix ICE with implicit typename in a template (PR c++/6255)
  - Fix another NRVO miscompilation (PR c++/7279)
  - set_new_handler() shall be declared to not throw any exception
  - Fix operator== on hashtables (PR libstdc++/7057)

* Mon Jul  1 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-0.7mdk
- Update to 3.1-branch 2002/07/01
- Add missing 32-bit libraries on x86-64
- Remove DT_RPATH from Java binaries (#66103, from Red Hat 3.1-7)

* Sun Jun 23 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-0.6mdk
- Update to 3.1-branch 2002/06/23
- Update Source1 (java wrapper) to call gij for version information
- Update Patch506 (DESTDIR) to pass down DESTDIR into multidirs
- Patch507: Fix x86-64 biarch support (SuSE 3.1.1-10)

* Thu Jun 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-0.5mdk
- Update to 3.1-branch 2002/06/19
- Remove explicit Conflicts: gcc < 2.96-0.60mdk
- Move Java headers to %{libjava_includedir}
- Add java javac wrappers from RH jdkgcj package
- Add c89 and c99 wrappers
- Fix gcj-tools alternatives removal
- Fix x86-64 profiling (from SuSE 3.1.1-4)
- Disable leaf frame pointer elimination by default on x86-64

* Sat Jun  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-0.4mdk
- Fix typo in --disable-multilib for configure options
- Fix Conflicts: gcc < 2.96-0.60mdk
- Re-enable frame pointer elimination on x86-64
- Merge with SuSE releases (3 new patches for x86-64):
  - Fix subreg handling
  - Fix XMM register reload
  - Fix output of a case-vector element that is relative

* Sat Jun  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-0.3mdk
- Update to 3.1-branch 2002/06/07
- Use --with-slibdir, define libdir in configure options
- Disable Java on x86_64. Likewise for multilibs support
- Update Patch506 (DESTDIR) to pass slibdir variable as well
- Merge with Red Hat releases (5 new patches):
  - default to -momit-leaf-frame-pointer on i386 (Richard Henderson)
  - use linkonce section/hidden symbol for i686 pic getpc thunks (rth)
  - m$ compatibility for unnamed fields as typedef of struct/union (PR c/6660)
  - fix -fverbose-asm with unnamed fields (PR c/6809)
  - fix -mmmx ICE (PR optimization/6842)

* Tue Jun  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-0.2mdk
- Strip debug info from static libraries
- Use default libstdc++-v3 flags + only --enable-long-long
- Provide HTML docs to libstdc++-v3
- Add alternatives for %{gcj_alternative_programs}
- Add full Requires: %%{version}-%%{release} to -devel subpackages
- Add -static-devel subpackages for libstdc++ and libgcj

* Fri May 31 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-0.1mdk
- Update to 3.1-branch 2002/05/30
- Don't hardcode /lib, use /%%{_lib}. Leave /lib/cpp as is however
- Requires: %{libf2c_name} for gcc-g77. Obsoletes: libf2c%{branch}
- Shared libgcc is now in %{libgcc_name} subpackage. Obsoletes:
  and Provides: both libgcc%{branch} and libgcc3.0
- Add intrinsic headers on x86-64, include <altivec.h> on PPC
- Remove SuSE patches merged in Red Hat and FSF releases
- Remove merged parts from Patch9 (attr-visibility2)
- Remove merged parts from Patch10 (trunc_int_for_mode.patch)
- Merge with Red Hat releases (7 new patches):
  - fix C++ __PRETTY_FUNCTION__ (PR c++/6794)
  - add test for fixed mozilla miscompilation
  - fix SPARC CSE ICE (PR optimization/6759)
  - fix x86_64 dbx64_register_map typo (Jan Hubicka)
  - fix DWARF-2 with flag_asynchronous_unwind_tables set for leaf
    functions (Jan Hubicka)
  - fix DWARF-2 x86_64 __builtin_dwarf_reg_sizes (Jan Hubicka)
  - fix x86_64 movabsdi (Michael Matz)

* Fri May 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-1mdk
- Update to 3.1 release
- Merge with Red Hat releases (17 new patches):
  - fix x86_64 ICE in do_SUBST (truncate to proper mode)
  - fix x86_64 q_regs_operand (Jan Hubicka)
  - better PR c++/6381 fix (Jason Merrill)
  - fix unitialized pointer-to-member values (Alexandre Oliva)
  - fix templates with asm inputs (Jason Merrill)
  - fix -fdata-section (Andreas Schwab)
  - fix loop-2[cd].c tests on i386 (Eric Botcazou)
  - fix fold-const.c typo
  - readd warning about i386 -malign-double into documentation (Jan Hubicka)
  - fix PR libstdc++/6594 (Ben Kosnik)
  - fix PR PR libstdc++/6648 (Paolo Carlini)
  - fix libstdc++ testsuite rlimits (Rainer Orth)
  - fix PR c/6643
  - rotate testcases (Tom Rix)
  - build libiberty with -fpic on x86_64 (Andreas Schwab)
  - fix x86_64 multilib build (Bo Thorsen)
  - fix x86_64 ASM_OUTPUT_MI_THUNK (Jan Hubicka)
- Merge with SuSE releases (7 new patches):
  - Fix built-in memset() miscompilation on i386 (Jan Hubicka)
  - Fix DESTDIR macro usage in libstdc++-v3 directory
  - Various x86_64 fixes
- Use DESTDIR for libstdc++-v3 and libjava %%install
- We can now lower the gxx_include_dir hackage in %%configure
- Migrate colorgcc to colorgcc-%%{version}

* Tue May 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.12mdk
- %{_bindir}/c++ must be an alternative, not a regular executable.
  This should fix the clash with the binary from gcc3.0-c++

* Fri May 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.11mdk
- Obsoletes gcc3.1-colorgcc, gcc3.1-doc
- Patch600: cp/lex.c (cxx_init_options): By default, don't wrap lines
  since the C front-end operates that way, already. Happify Pixel.

* Tue May  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.10mdk
- Add Obsoletes: gcc3.1, Provides: gcc3.1 to packages of compilers

* Mon May  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.9mdk
- Rebuild as the system compiler
- s/multiple_gcc/system_compiler/g

* Mon May  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.8mdk
- Add MMX and SSE intrinsics to filelist
- Prerelease snapshot 2002/05/05, which brings:
  - Fix if-cvt that caused sh-utils miscrompilation on IA-64 (PR opt/6534)
  - Even more corrections to ordering of base class cleanups

* Thu May  2 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.7mdk
- [Build]Requires: binutils >= 2.12.90.0.7-1mdk
- Prerelease snapshot 2002/05/02, which brings:
  - Only run regrename and cprop-registers if optimizing (PR c++/6396)
  - Don't run crossjump optimization before bb-reorder (PR opt/6516, XF4.2)
  - Disable -dD, -dN and -dI when -M or -MM is in effect
  - ABI change for returning simple classes from functions
  - Fix destructors call ordering (PR c++/6527)
  - Assignment operators don't have to return by value (PR c++/5719)
  - Fix ICE on some illegal typedefs (PR c++/6477)
  - Avoid building cv-qualified reference types in copy constructors
    (PR c++/6486, PR c++/6506)
  - If the friend has an explicit scope, enter that scope before name
    lookup (PR c++/6492)

* Mon Apr 29 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.6mdk
- Merge package with the tree where it is the system compiler:
  - Provides: libgcc = %{version}-%{release}
  - Get rid of %%{?!%%{X}: ...} since rpm has real troubles with them
  - Always dispatch libs into $FULLPATH
  - Add %{_bindir}/cc to filelist
- Prerelease snapshot 2002/04/28, which brings:
  - Fix constant folding bug (PR c/5430)
  - Fix ICE when concatenating many, many, many strings (PR c/3581)
  - Fix handling of "weak" attribute (PR c/6343)
  - Fix zlib miscompilation with certain optflags (PR opt/6475)
  - Fix stack overflow in the garbage collector (PR c/5154)
  - Fix ICE in Blitz++ (PR c++/5504) but rebreaks PR c++/411 which was
    already there for 2.95.2, so it doesn't really matter
  - More fixes to cv-qualifiers loosage (PR c++/6331)
  - Fix mangling of arrays with cv-qualified elements
  - Fix access control bug in lookup for operator= (PR c++/6479, aspell build)
  - Fix tellg() (PR libstdc++/6414)

* Tue Apr 23 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.5mdk
- Remove s/-O3/-O2/ workaround
- Remove duplicate non-ghost c++ entry in filelist
- Prerelease snapshot 2002/04/23 with notable changes:
  - Get rid of libgcjgc
  - Fix qmake miscompilation on IA-64 (PR middle-end/6279)
  - Fix Konqueror3 miscompilation on IA-32 (PR middle-end/6247)
  - Fix ICE in remove_eh_handler (PR c++/6320)
  - Fix bug with -mfpmath=sse (PR middle-end/6205)
  - Fix SSE comparisons (PR opt/5887)
  - Fix ICE on illegal-code from ggv package (PR c/6358)
  - Fix GCSE PRE at least on ppc64 (PR c/6344)
  - Fix C++ inliner regression (PR c++/6352)
  - Fix reload on IA-32
  - Fix ICE on deferred inlining (PR c++/6316)
  - Fix regression on redefinition of a type in a derived class (PR c++/5658)
  - Fix cv-qualifiers loosage (PR c++/6331)
  - Handle templates with explicit nested names (PR c++/6256)
  - Valgrind fixes (PR libstdc++/4164)
  - Fix performance regression in iostreams (PR libstdc++/4150)
  - Allow private inner interfaces (PR java/6294)

* Tue Apr 16 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.4mdk
- Remove Patch600 now obsoleted by new libgcj.jar name and location
- Prerelease snapshot 2002/04/15 with notable changes:
  - Introduce __gnu_linux__ and __gnu__hurd__
  - Finally remove the CHILL front-end
  - libgcj now goes into %%{_datadir}/java/libgcj-<version>.jar
  - Fix ICE when compiling Altivec code (PR c/6290)
  - Fix ICE in LAPACK on IA-64 (PR optimization/6177)
  - Fix ICE when compiling Wine-20020310 (PR c/6223)
  - Fix loop miscompilation in binutils (PR optimization/6233)
  - Fix ICE in instantiate_virtual_regs_1 (PR c/5078)
  - Disable cross-jumping for highly connected graphs (PR optimization/6007)
  - Fix statement expressions in the C++ front-end (PR c++/5373)
  - Fix infinite loop when compiling some class template (PR c++/5189)
  - Fix crash in layout_virtual_bases (PR c++/6273)
  - Fix Blitz++ failures on IA-64
  - Fix infinite loop with typedef attributes
  - Remove implicit typenameness (PR c++/5507)
  - Don't free DECL_SAVED_FUNCTION_DATA for inline functions (PR c++/6189)
  - Fix exception unsafe code in locale (PR libstdc++/1072)
  - Fix filebuf::seekpos (PR libstdc++/5180)

* Mon Apr  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.3mdk
- Prerelease snapshot 2002/04/08 with notable fixes:
  - Fix tail recursive call optimization (PR c/5120)
  - Fix handling of static data members with incomplete types (PR c++/5571)
  - Fix ICE under mangle_class_name_for_template with a parm of +int()
  - Fix STLport-4.5.3 EH regression tests miscompilation (PR c++/6179)

* Wed Apr  3 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.2mdk
- Prerelease snapshot 2002/04/01

* Wed Mar 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1-0.1mdk
- Prerelease snapshot 2002/03/25
- BuildRequires: texinfo >= 4.1 (Titi sux for the delay)
- Add gcj-jar%{program_suffix} into gcj-tools package
- Likewise for {grepjar,rmic,remiregistry}%{program_suffix}
- Move libstdc++-v3 includes to /usr/include/g++-v31/
- Get rid of libg2c-pic since gcc-3.1 now provides shared libf2c
- Add more --with[out]'isms for languages selection
- First Mandrake Linux release

# Local Variables:
# tab-width: 8
# End:
