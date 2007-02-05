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

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	binutils >= 2.15.92.0.2-1mdk
BuildRequires:	zlib-devel
BuildRequires:	gettext
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	texinfo >= 4.1
BuildRequires:	glibc-devel >= 2.2.5-14mdk
BuildRequires:	glibc-static-devel >= 2.2.5-14mdk
BuildRequires:	dejagnu

Requires:	binutils >= 2.15.92.0.2-1mdk
Requires:	%{name}-cpp = %{version}-%{release}
Requires:	%{libgcc_name_orig} >= 3.3.2-5mdk
Requires:	glibc-devel >= 2.2.5-14mdk
Requires(post):	update-alternatives
Requires(postun): update-alternatives

Conflicts:	gdb < 5.1.1
Obsoletes:	gcc%{branch}
Provides:	gcc%{branch} = %{version}-%{release}


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
Requires(post):	update-alternatives
Requires(postun): update-alternatives

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
Requires(post):	update-alternatives
Requires(postun): update-alternatives

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
         
#" (for syntax highlighting)

%build
# Force a seperate object dir
rm -fr obj-%{_target_platform}
mkdir obj-%{_target_platform}
cd obj-%{_target_platform}

# FIXME: extra tools needed
mkdir -p bin
cat %{_sourcedir}/gcc33-help2man.pl >bin/help2man
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
