%define name			%{cross_prefix}gcc%{package_suffix}
%define branch			3.3
%define branch_tag		%(perl -e 'printf "%%02d%%02d", split(/\\./,shift)' %{branch})
%define version			3.3.1

# OpenSLS defaults
%define build_propolice		1

%{expand: %{?_without_propolice:	%%global build_propolice 0}}
%{expand: %{?_with_propolice:		%%global build_propolice 1}}

%define release			3sls

%define biarches		x86_64

%define hammer_branch		1
%define hammer_date		20030520

# TODO: Provide fastjar, gccint, gcj info pages?
%define _unpackaged_files_terminate_build 0

# Define libraries major versions
%define libgcc_major		1
%define libstdcxx_major		5
%define libstdcxx_minor		5
%define libf2c_major		0
%define libgcj_major		4
%define libobjc_major		1
%define libgnat_major		1
%define libffi_major		2

# Package holding Java tools (gij, jv-convert, etc.)
%define GCJ_TOOLS		%{cross_prefix}gcj%{package_suffix}-tools

#-- JDK version
# "gcj" implements the JDK 1.1 language, "libgcj" is largely compatible with JDK 1.2
%define JDK_VERSION 1.2

#-- Alternatives for Java tools
#       Sun JDK         40
#       Kaffe           30
#       Gcj 3.2         20
%define gcj_alternative_priority 20
%define gcj_alternative_programs jar rmic rmiregistry grepjar java

# Define Mandrake Linux version we are building for
%define mdkversion		%(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandrake-release)

# Define if building a cross compiler
# FIXME: assume user does not define both cross and cross_bootstrap variables
%define build_cross		0
%define build_cross_bootstrap	0
%{expand: %{?cross:		%%global build_cross 1}}
%{expand: %{?cross_bootstrap:	%%global build_cross_bootstrap 1}}

%define system_compiler		1
%define target_cpu		%{_target_cpu}
%if %{build_cross}
%define system_compiler		0
%define target_cpu		%{cross}
%endif
%if %{build_cross_bootstrap}
%define build_cross		1
%define system_compiler		0
%define target_cpu		%{cross_bootstrap}
%endif
%if %{system_compiler}
%define alternative_priority	30%{branch_tag}
%define cross_prefix		%{nil}
%define package_suffix		%{nil}
%define program_prefix		%{nil}
%define program_suffix		%{nil}
%else
%if %{build_cross}
%define alternative_priority	10%{branch_tag}
%define cross_prefix		cross-%{target_cpu}-
%define package_suffix		%{nil}
%define program_prefix		%{target_cpu}-linux-
%define program_suffix		%{nil}
%else
%define alternative_priority	20%{branch_tag}
%define cross_prefix		%{nil}
%define package_suffix		%{branch}
%define program_prefix		%{nil}
%define program_suffix		-%{version}
%endif
%endif
%define _alternativesdir	/etc/alternatives

%define RELEASE			1
%if %{RELEASE}
%define source_package		gcc-%{version}
%define source_dir		gcc-%{version}
%else
%define snapshot		20030725
%define source_package		gcc-%{version}-%{snapshot}
%define source_dir		gcc-%{version}
%endif

# Define GCC target platform, and arch we built for
%if %{build_cross}
%define arch			%{target_cpu}
%define gcc_target_platform	%{target_cpu}-linux
%define target_prefix		%{_prefix}/%{gcc_target_platform}
%define target_libdir		%{target_prefix}/lib
%else
%define arch			%(echo %{_target_cpu}|sed -e "s/i.86/i386/" -e "s/athlon/i386/")
%define gcc_target_platform	%{_target_platform}
%define target_prefix		%{_prefix}
%define target_libdir		%{_libdir}
%endif

# Location of Java headers, don't let them in compiler specific
# directory as they are grabbed first
%define libjava_includedir	%{target_prefix}/include/libgcj-%{version}

# We now have versioned libstdcxx_includedir, that is c++/<VERSION>/
%define libstdcxx_includedir	%{target_prefix}/include/c++/%{version}

%define color_gcc_version	1.3.2
%define build_minimal		0
%define build_doc		1
%define build_pdf_doc		1
%define build_check		1
%define build_ada		0
%define gpc_snapshot		20030507
%define build_pascal		0
%define build_fortran		0
%define build_java		0
%ifarch %{ix86} x86_64
%define build_pascal		1
%endif
%ifarch %{ix86} x86_64
%define build_ada		1
%endif
%define build_cxx		1
%define build_objc		1
%define build_java		1
%define build_colorgcc		1
%define build_debug		0

%if %{build_propolice}
%define build_ada		0
%define build_doc		0
%define build_pdf_doc		0
%define build_fortran		0
%define build_java		0
%define build_pascal		0
%endif

# Allow --with[out] <feature> at rpm command line build
%{expand: %{?_without_PDF:	%%global build_pdf_doc 0}}
%{expand: %{?_without_DEBUG:	%%global build_debug 0}}
%{expand: %{?_without_CHECK:	%%global build_check 0}}
%{expand: %{?_without_MINIMAL:	%%global build_minimal 0}}
%{expand: %{?_with_PDF:		%%global build_pdf_doc 1}}
%{expand: %{?_with_DEBUG:	%%global build_debug 1}}
%{expand: %{?_with_CHECK:	%%global build_check 1}}
%{expand: %{?_with_MINIMAL:	%%global build_minimal 1}}

# Allow --without <front-end> at rpm command line build
%{expand: %{?_with_CXX:		%%global build_cxx 1}}
%{expand: %{?_with_ADA:		%%global build_ada 1}}
%{expand: %{?_with_F77:		%%global build_fortran 1}}
%{expand: %{?_with_JAVA:	%%global build_java 1}}
%{expand: %{?_with_OBJC:	%%global build_objc 1}}
%{expand: %{?_with_PASCAL:	%%global build_pascal 1}}

# Allow --with <front-end> at rpm command line build
%{expand: %{?_without_CXX:	%%global build_cxx 0}}
%{expand: %{?_without_ADA:	%%global build_ada 0}}
%{expand: %{?_without_F77:	%%global build_fortran 0}}
%{expand: %{?_without_JAVA:	%%global build_java 0}}
%{expand: %{?_without_OBJC:	%%global build_objc 0}}
%{expand: %{?_without_PASCAL:	%%global build_pascal 0}}

# A minimal build overrides all other options
%if %{build_cross_bootstrap}
%define build_minimal		1
%endif
%if %{build_minimal}
%define build_doc		0
%define build_pdf_doc		0
%define build_check		0
%define build_ada		0
%define build_cxx		0
%define build_fortran		0
%define build_objc		0
%define build_java		0
%define build_colorgcc		0
%define build_debug		0
%endif
%if %{build_cross}
%define build_doc		0
%define build_pdf_doc		0
%define build_check		0
%define build_colorgcc		0
# Unsupported front-ends when cross-compiling for now
%define build_java		0
%define build_ada		0
%endif

# Define library packages names
%define libgcc_name_orig	%{cross_prefix}libgcc
%define libgcc_name		%{libgcc_name_orig}%{libgcc_major}
%define libstdcxx_name_orig	%{cross_prefix}libstdc++
%define libstdcxx_name		%{libstdcxx_name_orig}%{libstdcxx_major}
%define libf2c_name_orig	%{cross_prefix}libf2c
%define libf2c_name		%{libf2c_name_orig}%{libf2c_major}
%define libgcj_name_orig	%{cross_prefix}libgcj
%define libgcj_name		%{libgcj_name_orig}%{libgcj_major}
%define libobjc_name_orig	%{cross_prefix}libobjc
%define libobjc_name		%{libobjc_name_orig}%{libobjc_major}
%define libgnat_name_orig	%{cross_prefix}libgnat
%define libgnat_name		%{libgnat_name_orig}%{libgnat_major}
%define libffi_name_orig	%{cross_prefix}libffi
%define libffi_name		%{libffi_name_orig}%{libffi_major}

%{expand:%%define mdk_version %(A=$(awk '{print $4}' /etc/mandrake-release); if [ -n "$A" ];then echo $A;else echo Cooker;fi)}

Summary:	GNU Compiler Collection
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/C

# Main source:	(CVS)
URL:		http://gcc.gnu.org/
Source0:	%{source_package}.tar.bz2
Source1:	gcc31-java.bz2
Source2:	gcc31-javac.bz2
Source3:	gcc32-jdk-config.bz2
# ColorGCC:	http://home.i1.net/~jamoyers/software/colorgcc/
Source4:	colorgcc-%{color_gcc_version}.tar.bz2
Source5:	gpc-%{gpc_snapshot}.tar.bz2
# FIXME: unless we get proper help2man package
Source6:	gcc33-help2man.pl.bz2


# CVS patches
Patch0: gcc33-revert-pr11420.patch.bz2
Patch1: gcc33-hammer-%{hammer_date}.patch.bz2
Patch2: gcc33-no-store-motion.patch.bz2
Patch3: gcc33-pr11536.patch.bz2
Patch4: gcc33-reload.patch.bz2
Patch5: gcc33-gcse-fix.patch.bz2
Patch6: gcc33-pr11639.patch.bz2
Patch7: gcc33-fix-__builtin_expect.patch.bz2
Patch8: gcc33-pr11319.patch.bz2
Patch9: gcc33-pr11370.patch.bz2

# Mandrake patches
Patch100: colorgcc-1.3.2-mdkconf.patch.bz2
Patch101: gcc33-pass-slibdir.patch.bz2
Patch102: gcc31-c++-diagnostic-no-line-wrapping.patch.bz2
Patch103: gcc32-pr7434-testcase.patch.bz2
Patch104: gcc33-pr8213-testcase.patch.bz2
Patch105: gcc33-x86_64-biarch-libjava.patch.bz2
Patch106: gcc33-x86_64-biarch-testsuite.patch.bz2
Patch107: gcc33-ada-64bit.patch.bz2
Patch108: gcc33-ada-addr2line.patch.bz2
Patch109: gcc33-ada-link.patch.bz2
Patch110: gcc33-ada-makefile.patch.bz2
Patch111: gcc33-multi-do-libdir.patch.bz2
Patch112: gcc33-cross-gxx_include_dir.patch.bz2
Patch113: gcc32-cross-inhibit_libc.patch.bz2
Patch114: gcc32-mklibgcc-serialize-crtfiles.patch.bz2
Patch115: gcc33-c++-classfn-member-template.patch.bz2
Patch116: gcc33-gpc.patch.bz2
Patch117: gcc33-gpc-serialize-build.patch.bz2
Patch118: gcc33-default-O2-options.patch.bz2
Patch119: gcc33-pr11631.patch.bz2

# Red Hat patches
Patch200: gcc33-2.96-RH-compat.patch.bz2
Patch201: gcc33-fde-merge-compat.patch.bz2
Patch202: gcc33-debug-pr7241.patch.bz2
Patch203: gcc33-ia64-unwind.patch.bz2
Patch204: gcc33-dwarf2-AT_comp_dir.patch.bz2
Patch205: gcc33-dwarf2-dtprel.patch.bz2
Patch206: gcc33-trunc_int_for_mode.patch.bz2
Patch207: gcc33-ppc-target_flags_explicit.patch.bz2
Patch208: gcc33-x86_64-tls-fix.patch.bz2
Patch209: gcc33-inline-label.patch.bz2
Patch210: gcc33-ia64-symbol_ref_flags.patch.bz2
Patch211: gcc33-cse-tweak.patch.bz2
Patch212: gcc33-tls-direct-segment-addressing.patch.bz2
Patch213: gcc33-pie.patch.bz2
Patch214: gcc33-note.GNU-stack.patch.bz2
Patch215: gcc33-c++-local-thunks.patch.bz2
Patch216: gcc33-pr6794.patch.bz2
Patch217: gcc33-libffi-ro-eh_frame.patch.bz2
Patch218: gcc33-ia64-libjava-locks.patch.bz2
Patch219: gcc33-rhl-testsuite.patch.bz2

# Propolice Stack Protector http://www.research.ibm.com/trl/projects/security/ssp/
Patch300:	gcc-3.3.1-protector-3.3-5.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
# Want updated alternatives priorities
%if %{build_cross}
Conflicts:	gcc-cpp < 3.2.2-4mdk
%endif
# We want -pie support
Requires:	%{cross_prefix}binutils >= 2.14.90.0.5-1mdk
BuildRequires:	%{cross_prefix}binutils >= 2.14.90.0.5-1mdk
# Make sure gdb will understand DW_FORM_strp
Conflicts:	gdb < 5.1.1
BuildRequires:	zlib-devel
%if %{build_ada}
# Ada requires Ada to build
BuildRequires:	%{name}-gnat >= 3.1, %{libgnat_name} >= 3.1
%endif
Requires:	%{name}-cpp = %{version}-%{release}
Requires:	%{libgcc_name_orig} >= %{version}-%{release}
Prereq:		/sbin/install-info
Prereq:		/usr/sbin/update-alternatives
BuildRequires:	gettext, flex, bison
BuildRequires:	texinfo >= 4.1
# Make sure pthread.h doesn't contain __thread keyword
Requires:	%{cross_prefix}glibc-devel >= 2.2.5-14mdk
%if !%{build_cross_bootstrap}
BuildRequires:	%{cross_prefix}glibc-devel >= 2.2.5-14mdk
%endif
%if %{mdkversion} >= 900
BuildRequires:	%{cross_prefix}glibc-static-devel >= 2.2.5-14mdk
%endif
%if %{system_compiler}
Obsoletes:	gcc%{branch}
Provides:	gcc%{branch} = %{version}-%{release}
%endif
%if %{build_pdf_doc}
BuildRequires:	tetex, tetex-dvips, tetex-latex
%endif
%if %{build_check}
BuildRequires:	dejagnu
%endif

%description
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.
This package is required for all other GCC compilers, namely C++,
Fortran 77, Objective C and Java.

If you have multiple versions of GCC installed on your system, it is
preferred to type "gcc-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU C compiler version %{version}.
%if %build_propolice
This version includes the Propolice stack protector (-fstack-protector)
option.
%endif

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
%if %{system_compiler}
Obsoletes:	gcc%{branch}-c++
Provides:	gcc%{branch}-c++ = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	%{libstdcxx_name} = %{version}
Requires:	%{libstdcxx_name}-devel = %{version}
Prereq:		/usr/sbin/update-alternatives

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
%if "%{branch}" == "3.3"
# By default, the libstdc++ from gcc3.3 is ABI compatible with the one
# from gcc3.2. Just tell other packages about it if they relied on that.
Provides:	%{libstdcxx_name_orig}3.2 = %{version}-%{release}
%endif

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
%if %{system_compiler}
Obsoletes:	gcc%{branch}-objc
Provides:	gcc%{branch}-objc = %{version}-%{release}
%endif
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
Obsoletes:	%{libobjc_name_orig}3.0, %{libobjc_name_orig}3.1
Provides:	%{libobjc_name_orig} = %{version}-%{release}
Provides:	%{libobjc_name_orig}3.0 = %{version}-%{release}
Provides:	%{libobjc_name_orig}3.1 = %{version}-%{release}
%if !%{system_compiler}
Conflicts:	%{name}-objc < %{branch}
%endif

%description -n %{libobjc_name}
Runtime libraries for the GNU Objective C Compiler.

####################################################################
# Pascal Compiler

%package gpc
Summary:	Pascal support for gcc
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-gpc
Provides:	gcc%{branch}-gpc = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}

%description gpc
The GNU Pascal Compiler (GPC) is, as the name says, the Pascal
compiler of the GNU family.  The compiler supports the following
language standards and quasi-standards:

  * ISO 7185 Pascal (see Resources),
  * most of ISO 10206 Extended Pascal,
  * Borland Pascal 7.0,
  * parts of Borland Delphi, Mac Pascal and Pascal-SC (PXSC). 

If you have multiple versions of GCC installed on your system, it is
preferred to type "gpc-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU Fortran 77 compiler version %{version}.

####################################################################
# Fortran 77 Compiler

%package g77
Summary:	Fortran 77 support for gcc
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-g77
Provides:	gcc%{branch}-g77 = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	%{libf2c_name_orig} = %{version}-%{release}

%description g77
This package adds support for compiling Fortran 77 programs with the GNU
compiler.

If you have multiple versions of GCC installed on your system, it is
preferred to type "g77-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU Fortran 77 compiler version %{version}.

####################################################################
# Fortran 77 Libraries

%package -n %{libf2c_name}
Summary:	Fortran 77 runtime libraries
Group:		System/Libraries
Provides:	%{libf2c_name_orig} = %{version}
Obsoletes:	%{libf2c_name_orig}%{branch}
Provides:	%{libf2c_name_orig}%{branch} = %{version}-%{release}

%description -n %{libf2c_name}
This package contains Fortran 77 shared library which is needed to run
Fortran 77 dynamically linked programs.

####################################################################
# Ada 95 Compiler

%package gnat
Summary:	Ada 95 support for gcc
Group:		Development/Other
Requires:	%{libgnat_name} = %{version}-%{release}
%if %{system_compiler}
Obsoletes:	gcc%{branch}-gnat
Provides:	gcc%{branch}-gnat = %{version}-%{release}
%endif
Obsoletes:	%{cross_prefix}gnat
Provides:	%{cross_prefix}gnat = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description gnat
This package contains an Ada95 compiler and associated development
tools based on the GNU gcc technology. Ada95 is the object oriented
successor of the Ada83 language. To build this package from sources
you must have installed a binary version to bootstrap the compiler.

####################################################################
# Ada 95 Libraries

%package -n %{libgnat_name}
Summary:	Ada 95 runtime libraries
Group:		System/Libraries
Provides:	%{libgnat_name_orig} = %{version}-%{release}
Obsoletes:	%{cross_prefix}gnat-runtime
Provides:	%{cross_prefix}gnat-runtime = %{version}-%{release}

%description -n %{libgnat_name}
This package contains the shared libraries required to run programs
compiled with the GNU Ada compiler (GNAT) if they are compiled to use
shared libraries.  It also contains the shared libraries for the
Implementation of the Ada Semantic Interface Specification (ASIS), the
implementation of Distributed Systems Programming (GLADE) and the
Posix 1003.5 Binding (Florist).

####################################################################
# Java Compiler

%package java
Summary:	Java support for gcc
Group:		Development/Java
%if %{system_compiler}
Obsoletes:	gcc%{branch}-java
Provides:	gcc%{branch}-java = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	%{GCJ_TOOLS} = %{version}-%{release}
Requires:	%{libgcj_name} >= %{version}
Requires:	%{libgcj_name}-devel >= %{version}
Prereq:		/usr/sbin/update-alternatives

%description java
This package adds experimental support for compiling Java(tm) programs
and bytecode into native code. To use this you will also need the
libgcj package.

If you have multiple versions of GCC installed on your system, it is
preferred to type "gcj-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU Java compiler version %{version}.

####################################################################
# Java Runtime Tools

%package -n %{GCJ_TOOLS}
Summary:	Java related tools from gcc %{version}
Group:		Development/Java
%if %{system_compiler}
Obsoletes:	%{cross_prefix}gcj%{branch}-tools
Provides:	%{cross_prefix}gcj%{branch}-tools = %{version}-%{release}
%endif
Provides:	%{cross_prefix}gcj-tools = %{version}-%{release}
Requires:	%{libgcj_name} >= %{version}
Requires:	%{libgcj_name}-devel >= %{version}
Conflicts:	kaffe < 1.0.7-3mdk
Prereq:		/usr/sbin/update-alternatives

%description -n %{GCJ_TOOLS}
This package includes Java related tools built from gcc %{version}:

   * gij: a Java ByteCode Interpreter
   * gcj-jar: a fast .jar archiver
   * gcjh: generating C++ header files corresponding to ``.class'' files
   * jcf-dump: printing out useful information from a ``.class'' file
   * jv-scan: printing some useful information from a ``.java'' file

If you have multiple versions of GCC installed on your system, the
above-mentioned tools are called as follows: "<gcj_tool>-$(gcc%{branch}-version)"
(without double quotes).

####################################################################
# Java Libraries

%package -n %{libgcj_name}
Summary:	GNU Java runtime libraries
Group:		System/Libraries
Requires:	zip >= 2.1
Obsoletes:	%{cross_prefix}gcc-libgcj
Provides:	%{cross_prefix}gcc-libgcj = %{version}-%{release}
Obsoletes:	%{libgcj_name_orig}%{branch}
Provides:	%{libgcj_name_orig}%{branch} = %{version}-%{release}
Obsoletes:	libgcj3

%description -n %{libgcj_name}
Runtime libraries for the GNU Java Compiler. The libgcj includes parts
of the Java Class Libraries, plus glue to connect the libraries to the
compiler and the underlying OS.

%package -n %{libgcj_name}-devel
Summary:	Header files and libraries for Java development
Group:		Development/Java
Requires:	zip >= 2.1
Requires:	zlib-devel
Requires:	%{libgcj_name} = %{version}-%{release}
Obsoletes:	%{libgcj_name_orig}%{branch}-devel
Provides:	%{libgcj_name_orig}%{branch}-devel = %{version}-%{release}
Provides:	%{libgcj_name_orig}-devel = %{version}-%{release}
Obsoletes:	libgcj3-devel

%description -n %{libgcj_name}-devel
Development headers and libraries for the GNU Java Compiler. The
libgcj includes parts of the Java Class Libraries, plus glue to
connect the libraries to the compiler and the underlying OS.

%package -n %{libgcj_name}-static-devel
Summary:	Static libraries for Java development
Group:		Development/Java
Requires:	%{libgcj_name}-devel = %{version}-%{release}
Obsoletes:	%{libgcj_name_orig}%{branch}-static-devel
Provides:	%{libgcj_name_orig}%{branch}-static-devel = %{version}-%{release}
Provides:	%{libgcj_name_orig}-static-devel = %{version}-%{release}
Obsoletes:	libgcj3-static-devel

%description -n %{libgcj_name}-static-devel
Static libraries for the GNU Java Compiler.

####################################################################
# FFI headers and libraries

# until we know what this really belongs to, wrap it improperly just to get our build
%if %{build_java}
%package -n %{libffi_name}-devel
Summary:	Development headers and static library for FFI
Group:		Development/C
Obsoletes:	%{libffi_name_orig}%{branch}-devel
Provides:	%{libffi_name_orig}%{branch}-devel = %{version}-%{release}
Obsoletes:	%{libffi_name_orig}-devel
Provides:	%{libffi_name_orig}-devel = %{version}-%{release}
Provides:	ffi-devel = %{version}-%{release}

%description -n %{libffi_name}-devel
This package contains the development headers and the static library
for libffi. The libffi library provides a portable, high level
programming interface to various calling conventions. This allows a
programmer to call any function specified by a call interface
description at run time.
%endif
####################################################################
# Preprocessor

%package cpp
Summary:	The C Preprocessor
Group:		Development/C
%if %{system_compiler}
Obsoletes:	gcc%{branch}-cpp
Provides:	gcc%{branch}-cpp = %{version}-%{release}
%endif
Prereq:		/sbin/install-info
Prereq:		/usr/sbin/update-alternatives

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
# ColorGCC

%package colorgcc
Summary:	GCC output colorizer
Group:		Development/Other
Obsoletes:	gcc2.96-colorgcc
%if %{system_compiler}
Obsoletes:	gcc%{branch}-colorgcc
Provides:	gcc%{branch}-colorgcc = %{version}-%{release}
%endif
Requires:	%{name} = %{version}
PreReq:		/usr/sbin/update-alternatives
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
%if %{system_compiler}
Obsoletes:	gcc%{branch}-doc
Provides:	gcc%{branch}-doc = %{version}-%{release}
%endif

%description doc
GCC is a compiler suite aimed at integrating all the optimizations and
features necessary for a high-performance and stable development
environment. This package contains the compiler documentation in INFO
pages.

%package doc-pdf
Summary:	GCC documentation
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-doc-pdf
Provides:	gcc%{branch}-doc-pdf = %{version}-%{release}
%endif

%description doc-pdf
GCC is a compiler suite aimed at integrating all the optimizations and
features necessary for a high-performance and stable development
environment. This package contains the compiler printable
documentation in PDF.

%prep
%setup -q -n %{source_dir} -a 4 -a 5
%if %{hammer_branch}
%patch0 -p1 -b .pr11420
%patch1 -p1 -b .hammer-branch
#%patch2 -p1 -b .no-store-motion
%endif
%patch3 -p1 -b .pr11536
%patch4 -p1 -b .reload
%patch5 -p1 -b .gcse-fix
%patch6 -p1 -b .pr11639
%patch7 -p1 -b .fix-__builtin_expect
%patch8 -p1 -b .pr11319
%patch9 -p1 -b .pr11370

# Mandrake patches
%patch101 -p1 -b .pass-slibdir
%patch102 -p1 -b .c++-diagnostic-no-line-wrapping
%patch103 -p1 -b .pr7434-testcase
%patch104 -p1 -b .pr8213-testcase
%patch105 -p1 -b .x86_64-biarch-libjava
%patch106 -p1 -b .x86_64-biarch-testsuite
%patch107 -p1 -b .ada-64bit
%patch108 -p1 -b .ada-addr2line
%patch109 -p1 -b .ada-link
%patch110 -p1 -b .ada-makefile
%patch111 -p1 -b .multi-do-libdir
%patch112 -p1 -b .cross-gxx_include_dir
%patch113 -p1 -b .cross-inhibit_libc
%patch114 -p1 -b .mklibgcc-serialize-crtfiles
%patch115 -p1 -b .c++-classfn-member-template
#%patch118 -p1 -b .default-O2-options
%patch119 -p1 -b .pr11631-testcase

# Red Hat patches
%patch200 -p0 -b .2.96-RH-compat
%patch201 -p0 -b .fde-merge-compat
%patch202 -p0 -b .debug-pr7241
%patch203 -p1 -b .ia64-unwind
%patch204 -p1 -b .dwarf2-AT_comp_dir
%patch205 -p1 -b .dwarf2-dtprel
%patch206 -p1 -b .trunc_int_for_mode
%patch207 -p1 -b .ppc-target_flags_explicit
%patch208 -p1 -b .x86_64-tls-fix
%patch209 -p0 -b .inline-label
%patch210 -p1 -b .ia64-symbol_ref_flags
%patch211 -p1 -b .cse-tweak
%patch212 -p1 -b .tls-direct-segment-addressing
%patch213 -p1 -b .pie
%patch214 -p1 -b .PT_GNU_STACK
%patch215 -p1 -b .c++-local-thunks
%patch216 -p1 -b .pr6794
%patch217 -p1 -b .libffi-ro-eh_frame
%patch218 -p1 -b .ia64-libjava-locks
%patch219 -p1 -b .rhl-testsuite

# Integrate GNU Pascal compiler
mv gpc-%{gpc_snapshot}/p gcc/p
rmdir gpc-%{gpc_snapshot}
patch -p0 < gcc/p/diffs/gcc-3.3.diff
%patch116 -p1 -b .gpc
%patch117 -p1 -b .gpc-serialize-build

# Mandrakezification for bug reports
perl -pi -e "/bug_report_url/ and s/\"[^\"]+\"/\"<URL:https:\/\/qa.mandrakesoft.com\/>\"/;" \
         -e '/version_string/ and s/([0-9]*(\.[0-9]*){1,3}).*(\";)$/\1 \(Mandrake Linux %{mdk_version} %{version}-%{release}\)\3/;' \
         gcc/version.c

# ColorGCC patch
(cd colorgcc-%{color_gcc_version};
%patch100 -p1 -b .mdkconf
perl -pi -e 's|GCC_VERSION|%{version}|' colorgcc*
)

# ProPolice Stack Protector patch
%if %build_propolice
%patch300 -p1 -b .propolice
%endif

%build
# Force a seperate object dir
rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

# FIXME: extra tools needed
mkdir -p bin
bzcat %{SOURCE6} >bin/help2man
export PATH=$PATH:$PWD/bin

# Make bootstrap-lean
CC=gcc
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-fstack-protector//g'`
%if %{build_debug}
OPT_FLAGS=`echo "$OPT_FLAGS -g" | sed -e "s/-fomit-frame-pointer//g"`
%endif
%if %{build_cross}
OPT_FLAGS="-O2 -pipe"
%endif
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-fomit-frame-pointer//g'`
LANGUAGES="c"
%if %{build_cxx}
LANGUAGES="$LANGUAGES,c++"
%endif
%if %{build_ada}
LANGUAGES="$LANGUAGES,ada"
%endif
%if %{build_fortran}
LANGUAGES="$LANGUAGES,f77"
%endif
%if %{build_objc}
LANGUAGES="$LANGUAGES,objc"
%endif
%if %{build_java}
LANGUAGES="$LANGUAGES,java"
%endif
%if %{build_pascal}
LANGUAGES="$LANGUAGES,pascal"
%endif
PROGRAM_SUFFIX=""
%if !%{system_compiler}
PROGRAM_SUFFIX="--program-suffix=%{program_suffix}"
%endif
%if %{build_cxx}
LIBSTDCXX_V3_FLAGS="--enable-long-long --enable-__cxa_atexit"
%endif
%if %{build_cross}
CROSS_FLAGS="--with-sysroot=%{_prefix}/%{target_cpu}-linux --disable-multilib"
%endif
%if %{build_cross_bootstrap}
CROSS_FLAGS="$CROSS_FLAGS --with-newlib --disable-shared --disable-threads"
%endif
[[ -n "$CROSS_FLAGS" ]] && CROSS_FLAGS="$CROSS_FLAGS --target=%{gcc_target_platform}"
# update config.{sub,guess} scripts
%{?__cputoolize: %{__cputoolize} -c ..}
%{?__cputoolize: %{__cputoolize} -c ../boehm-gc}
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --libdir=%{_libdir} --with-slibdir=/%{_lib} \
	--mandir=%{_mandir} --infodir=%{_infodir} \
	--enable-shared --enable-threads=posix --disable-checking $LIBSTDCXX_V3_FLAGS \
	--enable-languages="$LANGUAGES" $PROGRAM_SUFFIX \
	--host=%{_target_platform} $CROSS_FLAGS \
	--with-system-zlib
touch ../gcc/c-gperf.h
%if %{build_cross}
%make
%else
%ifarch alpha
%make bootstrap-lean BOOT_CFLAGS="$OPT_FLAGS"
%else
%make bootstrap-lean
%endif
%endif

%if %{build_ada}
# This doesn't work with -j$RPM_BUILD_NCPUS
make -C gcc gnatlib-shared
make -C gcc gnattools
make -C gcc ada.info
%endif

%if !%{build_cross}
# Make protoize
make -C gcc CC="./xgcc -B ./ -O2" proto
%endif
cd ..

# Copy various doc files here and there
mkdir -p rpm.doc/g77
mkdir -p rpm.doc/objc
mkdir -p rpm.doc/libjava
mkdir -p rpm.doc/libobjc
mkdir -p rpm.doc/boehm-gc
mkdir -p rpm.doc/fastjar
mkdir -p rpm.doc/gpc

%if %{build_pascal}
(cd gcc/p; for i in ChangeLog* README NEWS FAQ; do
	cp -p $i ../../rpm.doc/gpc/$i
done)
%endif
%if %{build_fortran}
(cd gcc/f; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/g77/$i.f
done)
(cd libf2c; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/g77/$i.libf2c
done)
%endif
%if %{build_objc}
(cd gcc/objc; for i in README*; do
	cp -p $i ../../rpm.doc/objc/$i.objc
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/libobjc/$i.libobjc
done)
%endif
%if %{build_java}
(cd boehm-gc; for i in ChangeLog*; do
        cp -p $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd fastjar; for i in ChangeLog* README*; do
        cp -p $i ../rpm.doc/fastjar/$i.fastjar
done)
(cd libjava; for i in README THANKS COPYING ChangeLog; do
	cp -p $i ../rpm.doc/libjava/$i.libjava
done)
(cd libjava; cp -p LIBGCJ_LICENSE ../rpm.doc/libjava/LICENSE.libjava)
%endif

# [ghibo] - build printable documentation
%if %{build_pdf_doc}
(cd gcc/doc; for file in gcc.texi cpp.texi cppinternals.texi; do
  texi2dvi -p -t @afourpaper -t @finalout -I ./include $file
done)
(cd gcc/ada; for file in gnat_rm.texi gnat_ug_unx.texi; do
  texi2dvi -p -t @afourpaper -t @finalout -I ../doc/include $file
done
mv gnat_ug_unx.pdf gnat_ug.pdf
)
(cd gcc/f;
  texi2dvi -p -t @afourpaper -t @finalout -I ../doc/include g77.texi
)
%endif

# Run tests
%ifarch %{biarches}
RUNTESTFLAGS="--target_board 'unix{-m32,}'"
%endif
echo ====================TESTING=========================
%if %{build_check}
cd obj-%{gcc_target_platform}
%make -k RUNTESTFLAGS="$RUNTESTFLAGS" check || true
logfile="$PWD/../%{name}-%{version}-%{release}.log"
../contrib/test_summary > $logfile
cd ..
%endif
echo ====================TESTING END=====================
 
%install
rm -rf $RPM_BUILD_ROOT

# Fix HTML docs for libstdc++-v3
perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/docs/html/documentation.html
ln -sf documentation.html libstdc++-v3/docs/html/index.html
find libstdc++-v3/docs/html -name CVS | xargs rm -rf

# Create some directories, just to make sure (e.g. ColorGCC)
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
mkdir -p $RPM_BUILD_ROOT%{_infodir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}

# ColorGCC stuff
%if %{build_colorgcc}
(cd colorgcc-%{color_gcc_version};
  install -m 755 colorgcc $RPM_BUILD_ROOT%{_bindir}/colorgcc-%{version}
  ln -s colorgcc-%{version} $RPM_BUILD_ROOT%{_bindir}/colorgcc
  install -m 644 colorgccrc $RPM_BUILD_ROOT%{_sysconfdir}/
  for i in COPYING CREDITS ChangeLog; do
    [ ! -f ../$i.colorgcc ] && mv -f $i ../$i.colorgcc
  done
)
%endif

pushd obj-%{gcc_target_platform};
  %makeinstall slibdir=$RPM_BUILD_ROOT/%{_lib}
  %if %{build_ada}
  make -C gcc ada.install-info DESTDIR=$RPM_BUILD_ROOT
  for f in $RPM_BUILD_ROOT%{_infodir}/gnat_ug_unx.info*; do
    sed -e "s/gnat_ug_unx/gnat_ug/g" $f > ${f/gnat_ug_unx/gnat_ug}
  done
  chmod 644 $RPM_BUILD_ROOT%{_infodir}/gnat*
  %endif
popd

FULLVER=`$RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-gcc%{program_suffix} --version | head -n 1 | cut -d' ' -f3`
FULLPATH=$(dirname $RPM_BUILD_ROOT%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/cc1)

#if [ "%{gcc_target_platform}" != "%{_target_platform}" ]; then
#   mv -f $RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-gcc $RPM_BUILD_ROOT%{_bindir}/%{_target_platform}-gcc
#fi

file $RPM_BUILD_ROOT/%{_bindir}/* | grep ELF | cut -d':' -f1 | xargs strip || :
strip $FULLPATH/cc1
%if %{build_cxx}
strip $FULLPATH/cc1plus
%endif
%if %{build_pascal}
strip $FULLPATH/gpc1
%endif
%if %{build_fortran}
strip $FULLPATH/f771
%endif
%if %{build_java}
strip $FULLPATH/{jc1,jvgenmain}
%endif

# Create /usr/bin/%{program_prefix}gcc%{branch}-version that contains the full version of gcc
cat >$RPM_BUILD_ROOT%{_bindir}/%{program_prefix}gcc%{branch}-version <<EOF
#!/bin/sh
echo "$FULLVER"
EOF
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/%{program_prefix}gcc%{branch}-version

# Fix program names
# (gb) For each primary program in every package, I want it to be
# named <program>-<version>
(cd $RPM_BUILD_ROOT%{_bindir}; for file in cpp gcc g++ gcj g77 gpc gpidump; do
  file_version="${file}-%{version}"
  if [ -x "$file" -a "(" ! -x "$file_version" -o -L "$file_version" ")" ]; then
    cp -f $file $file_version
    rm -f $file
    ln -s $file_version $file
  fi
  file="%{program_prefix}$file" file_version="%{program_prefix}$file_version"
  if [ -x "$file" -a ! -x "$file_version" ]; then
    cp -f $file $file_version
    rm -f $file
    ln -s $file_version $file
  fi
done)

# Fix some links
ln -sf gcc $RPM_BUILD_ROOT%{_bindir}/cc
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# First, move 32-bit libraries to the right directories
%ifarch %{biarches}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib
mv $RPM_BUILD_ROOT%{_libdir}/32/* $RPM_BUILD_ROOT%{_prefix}/lib
rm -rf $RPM_BUILD_ROOT%{_libdir}/32
ln -sf ../lib $RPM_BUILD_ROOT%{_libdir}/32

mkdir -p $RPM_BUILD_ROOT/lib
rm -rf $RPM_BUILD_ROOT/%{_lib}/32
ln -sf ../lib $RPM_BUILD_ROOT/%{_lib}/32
%endif

# Dispatch Ada 95 libraries (special case)
%if %{build_ada}
pushd $FULLPATH/adalib
  rm -f libgnarl.so* libgnat.so*
  mv -f libgnarl-*.so.* $RPM_BUILD_ROOT%{_libdir}/
  ln -s ../../../../../%{_lib}/libgnarl-*.so.* libgnarl.so
  mv -f libgnat-*.so.* $RPM_BUILD_ROOT%{_libdir}/
  ln -s ../../../../../%{_lib}/libgnat-*.so.* libgnat.so
popd
%endif

# Strip debug info from libraries
STRIP_DEBUG=
%if !%{build_debug}
STRIP_DEBUG="strip -g"
if [[ "%{_target_cpu}" != "%{target_cpu}" ]]; then
  STRIP_DEBUG="%{target_cpu}-linux-$STRIP_DEBUG"

fi
%endif

# Dispatch libraries to the right directories
DispatchLibs() {
	libname=$1 libversion=$2
	rm -f $libname.so $libname.a
	$STRIP_DEBUG ../../../$crosslibdir/$libname.so.$libversion
	$STRIP_DEBUG ../../../$crosslibdir/$libname.a
	ln -s ../../../$crosslibdir/$libname.so.$libversion $libname.so
	rm -f ../../../$crosslibdir/$libname.so
	cp -f ../../../$crosslibdir/$libname.a $libname.a
	rm -f ../../../$crosslibdir/$libname.a
	%ifarch %{biarches}
	[ -d 32 ] || mkdir 32
	(cd 32;
	mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib
	$STRIP_DEBUG ../../../../32/$crosslibdir/$libname.so.$libversion
	$STRIP_DEBUG ../../../../32/$crosslibdir/$libname.a
	ln -s ../../../../32/$libname.so.$libversion $libname.so
	rm -f ../../../../32/$libname.so
	[ -r "../../../../32/$libname.a" ] && {
	cp -f ../../../../32/$libname.a $libname.a
	rm -f ../../../../32/$libname.a
	})
	%endif
	%ifarch ppc
	[ -d nof ] || mkdir nof
	(cd nof;
	$STRIP_DEBUG ../../../../nof/$crosslibdir/$libname.so.$libversion
	$STRIP_DEBUG ../../../../nof/$crosslibdir/$libname.a
	ln -s ../../../../nof/$libname.so.$libversion $libname.so
	rm -f ../../../../nof/$libname.so
	[ -r "../../../../nof/$libname.a" ] && {
	cp -f ../../../../nof/$libname.a $libname.a
	rm -f ../../../../nof/$libname.a
	})
	%endif
}
(cd $FULLPATH;
	if [[ "%{_target_cpu}" != "%{target_cpu}" ]]; then
	crosslibdir="../%{gcc_target_platform}/lib"
	fi
	%if %{build_cxx}
	DispatchLibs libstdc++	%{libstdcxx_major}.0.%{libstdcxx_minor}
	mv ../../../$crosslibdir/libsupc++.a libsupc++.a
	%ifarch %{biarches}
	mv -f ../../../32/libsupc++.a 32/libsupc++.a
	%endif
	%ifarch ppc
	mv -f ../../../nof/libsupc++.a nof/libsupc++.a
	%endif
	%endif
	%if %{build_java}
	DispatchLibs libgcj	%{libgcj_major}.0.0
	DispatchLibs lib-org-xml-sax 0.0.0
	DispatchLibs lib-org-w3c-dom 0.0.0
	%endif
	%if %{build_objc}
	DispatchLibs libobjc	%{libobjc_major}.0.0
	%endif
	%if %{build_fortran}
	DispatchLibs libg2c	%{libf2c_major}.0.0
	mv -f ../../../$crosslibdir/libfrtbegin.a libfrtbegin.a
	[ -r "../../../32/libfrtbegin.a" ] &&
	mv -f ../../../32/libfrtbegin.a 32/libfrtbegin.a
	[ -r "../../../nof/libfrtbegin.a" ] &&
	mv -f ../../../nof/libfrtbegin.a nof/libfrtbegin.a
	%endif
)

# Move Java headers to /usr/include/libgcj-<version>
%if %{build_java}
if [ "%{libjava_includedir}" != "%{_includedir}" ]; then
  mkdir -p $RPM_BUILD_ROOT%{libjava_includedir}
  mv $RPM_BUILD_ROOT%{_includedir}/j*.h $RPM_BUILD_ROOT%{libjava_includedir}/
  for dir in gcj gnu java javax; do
    mkdir -p $RPM_BUILD_ROOT%{libjava_includedir}/$dir
    mv $RPM_BUILD_ROOT%{_includedir}/$dir/* $RPM_BUILD_ROOT%{libjava_includedir}/$dir/
    rmdir $RPM_BUILD_ROOT%{_includedir}/$dir
  done

  # move <gcj/libgcj-config.h> too
  mv $FULLPATH/include/gcj/libgcj-config.h $RPM_BUILD_ROOT%{libjava_includedir}/gcj/
  rmdir $FULLPATH/include/gcj

  # include <libgcj/XXX.h> should lead to <libgcj-VERSION/XXX.h>
  ln -s %{libjava_includedir} $RPM_BUILD_ROOT%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/libgcj
  ln -s %{libjava_includedir} $RPM_BUILD_ROOT%{_includedir}/libgcj
fi
%endif

# Move libgcj.spec to compiler-specific directories
%if %{build_java}
mv $RPM_BUILD_ROOT%{_libdir}/libgcj.spec $FULLPATH/libgcj.spec
%endif

# Rename jar because it could clash with Kaffe's if this gcc
# is primary compiler (aka don't have the -<version> extension)
%if %{build_java}
(cd $RPM_BUILD_ROOT%{_bindir}/;
  mv jar%{program_suffix} gcj-jar-%{version}
  for app in grepjar rmic rmiregistry; do
    mv $app%{program_suffix} gcj-$app-%{version}
  done
)
%endif

# Add java and javac wrappers
%if %{build_java}
(cd $RPM_BUILD_ROOT%{_bindir}/;
  SED_PATTERN="s|@GCJ_VERSION@|%{version}|;s|@JDK_VERSION@|%{JDK_VERSION}|;s|@JDK_INCLUDES@|-I%{libjava_includedir}|;"
  bzcat %{SOURCE1} | sed -e "$SED_PATTERN" > gcj-java-%{version}
  chmod 0755 gcj-java-%{version}
  bzcat %{SOURCE2} | sed -e "$SED_PATTERN" > gcj-javac-%{version}
  chmod 0755 gcj-javac-%{version}
  bzcat %{SOURCE3} | sed -e "$SED_PATTERN" > gcj-jdk-config-%{version}
  chmod 0755 gcj-jdk-config-%{version}
)
%endif

# Move <cxxabi.h> to compiler-specific directories
%if %{build_cxx}
mv $RPM_BUILD_ROOT%{libstdcxx_includedir}/cxxabi.h $FULLPATH/include/
%endif

# Fix links to binaries
(cd $RPM_BUILD_ROOT%{_bindir};
	for file in cpp gcc; do [ -x $file ] && mv $file "$file"-%{version}; done
	%if %{build_cxx}
	for file in g++ c++; do [ -x $file ] && mv $file "$file"-%{version}; done
	%endif
	%if %{build_java}
	for file in gcjh jcf-dump jv-scan; do [ -x $file -a -n "%{program_suffix}" ] && mv $file "$file"-%{version}; done
	%endif
)

# Link gnatgcc to gcc
ln -sf gcc $RPM_BUILD_ROOT%{_bindir}/gnatgcc

# Create an empty file with perms 0755
FakeAlternatives() {
  for file in ${1+"$@"}; do
    rm -f $file
    touch $file
    chmod 0755 $file
  done
}

# Alternatives provide /lib/cpp and %{_bindir}/cpp
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives cpp)
(mkdir -p $RPM_BUILD_ROOT/lib; cd $RPM_BUILD_ROOT/lib; ln -sf %{_bindir}/cpp cpp)

# Alternatives provide /usr/bin/{g77,f77}
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives g77 f77)

# Alternatives provide /usr/bin/c++
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives c++)

# Alternatives provide java programs
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives %{gcj_alternative_programs} javac)

# Alternatives provide jdk-config script
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives jdk-config)

# Move libgcc_s.so* to /%{_lib}
(cd $RPM_BUILD_ROOT/%{_lib};
  chmod 0755 libgcc_s.so.%{libgcc_major}
%if %{build_cross}
  mkdir -p $RPM_BUILD_ROOT%{target_libdir}
  mv -f libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_libdir}/libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_libdir}/libgcc_s.so.%{libgcc_major}
  ln -sf libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_libdir}/libgcc_s.so
%else
  mv -f libgcc_s.so.%{libgcc_major} libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} libgcc_s.so.%{libgcc_major}
  ln -sf ../../%{_lib}/libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{_libdir}/libgcc_s.so
%endif
%ifarch ppc
  chmod 0755 libgcc_s_nof.so.%{libgcc_major}
  mv -f libgcc_s_nof.so.%{libgcc_major} libgcc_s_nof-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s_nof-%{version}.so.%{libgcc_major} libgcc_s_nof.so.%{libgcc_major}
  ln -sf ../../%{_lib}/libgcc_s_nof.so.%{libgcc_major} $RPM_BUILD_ROOT%{_libdir}/libgcc_s_nof.so
%endif
)
# Handle 32-bit libgcc
%ifarch %{biarches}
(cd $RPM_BUILD_ROOT/lib;
  chmod 0755 libgcc_s.so.%{libgcc_major}
  mv -f libgcc_s.so.%{libgcc_major} libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} libgcc_s.so.%{libgcc_major}
  ln -sf ../../lib/libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{_prefix}/lib/libgcc_s.so
  ln -sf ../../lib/libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{_prefix}/lib/libgcc_s_32.so
)
%endif

# Create c89 and c99 wrappers
%if %{system_compiler}
cat > $RPM_BUILD_ROOT%{_prefix}/bin/c89 <<"EOF"
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
cat > $RPM_BUILD_ROOT%{_prefix}/bin/c99 <<"EOF"
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
chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/c?9
%endif

# FIXME: cpp, gcov manpages names
(cd $RPM_BUILD_ROOT%{_mandir}/man1;
  if [[ -n "%{program_prefix}%{program_suffix}" ]]; then
    for f in gcov cpp gcc g++ g77 gpc; do
      [[ -f "$f.1" ]] && mv $f.1 %{program_prefix}$f%{program_suffix}.1
    done
  fi
)

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

# In case we are cross-compiling, don't bother to remake symlinks and
# don't let spec-helper when stripping files either
%if "%{name}" != "gcc"
export DONT_SYMLINK_LIBS=1
export DONT_STRIP=1
%endif

%if %{build_debug}
# Don't strip in debug mode
export DONT_STRIP=1
%endif

%if %{build_propolice}
# create propolice profile
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
echo "# This tells rpm to compile everything with stack protection" >> $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/propolice.sh
echo "" >> $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/propolice.sh
echo "export STACK_PROTECTOR=true" >> $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/propolice.sh
echo "# This tells rpm to compile everything with stack protection" >> $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/propolice.csh
echo "" >> $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/propolice.csh
echo "set STACK_PROTECTOR=true" >> $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/propolice.csh
chmod 0755 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/propolice.*
%endif


%clean
#rm -rf $RPM_BUILD_ROOT

%post
update-alternatives --install %{_bindir}/gcc gcc %{_bindir}/%{program_prefix}gcc-%{version} %{alternative_priority}
[ -e %{_bindir}/gcc ] || update-alternatives --auto gcc

%postun
if [ ! -f %{_bindir}/gcc-%{version} ]; then
  update-alternatives --remove gcc %{_bindir}/%{program_prefix}gcc-%{version}
fi

%post colorgcc
update-alternatives --install %{_bindir}/gcc gcc %{_bindir}/%{program_prefix}colorgcc %(expr %{alternative_priority} + 50000)

%postun colorgcc
if [ ! -f %{_bindir}/colorgcc-%{version} ]; then
  update-alternatives --remove gcc %{_bindir}/colorgcc
  # update-alternatives silently ignores paths that don't exist
  update-alternatives --remove g++ %{_bindir}/colorgcc
  update-alternatives --remove g77 %{_bindir}/colorgcc
  update-alternatives --remove gcj %{_bindir}/colorgcc
fi

%triggerin colorgcc -- %{name}-c++
update-alternatives --install %{_bindir}/g++ g++ %{_bindir}/colorgcc %(expr %{alternative_priority} + 50000) --slave %{_bindir}/c++ c++ %{_bindir}/colorgcc

%triggerpostun colorgcc -- %{name}-c++
if [ ! -f %{_bindir}/g++-%{version} ]; then
  update-alternatives --remove g++ %{_bindir}/colorgcc
fi

%triggerin colorgcc -- %{name}-g77
update-alternatives --install %{_bindir}/g77 g77 %{_bindir}/colorgcc %(expr %{alternative_priority} + 50000) --slave %{_bindir}/f77 f77 %{_bindir}/colorgcc

%triggerpostun colorgcc -- %{name}-g77
if [ ! -f %{_bindir}/g77-%{version} ]; then
  update-alternatives --remove g77 %{_bindir}/colorgcc
fi

%triggerin colorgcc -- %{name}-java
update-alternatives --install %{_bindir}/gcj gcj %{_bindir}/colorgcc %(expr %{alternative_priority} + 50000)

%triggerpostun colorgcc -- %{name}-java
if [ ! -f %{_bindir}/gcj-%{version} ]; then
  update-alternatives --remove gcj %{_bindir}/colorgcc
fi

%if %{build_cxx}
%post c++
update-alternatives --install %{_bindir}/g++ g++ %{_bindir}/%{program_prefix}g++-%{version} %{alternative_priority} --slave %{_bindir}/c++ c++ %{_bindir}/%{program_prefix}g++-%{version}
[ -e %{_bindir}/g++ ] || update-alternatives --auto g++

%postun c++
if [ ! -f %{_bindir}/g++-%{version} ]; then
  update-alternatives --remove g++ %{_bindir}/%{program_prefix}g++-%{version}
fi
%endif

%if %{build_cxx}
%post -n %{libstdcxx_name} -p /sbin/ldconfig
%postun -n %{libstdcxx_name} -p /sbin/ldconfig
%endif

%post -n %{libgcc_name} -p /sbin/ldconfig
%postun -n %{libgcc_name} -p /sbin/ldconfig

%post cpp
update-alternatives --install %{_bindir}/cpp cpp %{_bindir}/%{program_prefix}cpp-%{version} %{alternative_priority} --slave /lib/cpp lib_cpp %{_bindir}/%{program_prefix}cpp-%{version}
[ -e %{_bindir}/cpp ] || update-alternatives --auto cpp

%postun cpp
if [ ! -f %{_bindir}/cpp-%{version} ]; then
  update-alternatives --remove cpp %{_bindir}/%{program_prefix}cpp-%{version}
fi

%if %{build_pascal}
%post gpc
update-alternatives --install %{_bindir}/gpc gpc %{_bindir}/%{program_prefix}gpc-%{version} %{alternative_priority} --slave %{_bindir}/f77 f77 %{_bindir}/%{program_prefix}gpc-%{version} --slave %{_bindir}/gpidump gpidump %{_bindir}/%{program_prefix}gpidump-%{version}
[ -e %{_bindir}/gpc ] || update-alternatives --auto gpc

%postun gpc
if [ ! -f %{_bindir}/gpc-%{version} ]; then
  update-alternatives --remove gpc %{_bindir}/%{program_prefix}gpc-%{version}
fi
%endif

%if %{build_fortran}
%post g77
update-alternatives --install %{_bindir}/g77 g77 %{_bindir}/%{program_prefix}g77-%{version} %{alternative_priority} --slave %{_bindir}/f77 f77 %{_bindir}/%{program_prefix}g77-%{version}
[ -e %{_bindir}/g77 ] || update-alternatives --auto g77

%postun g77
if [ ! -f %{_bindir}/g77-%{version} ]; then
  update-alternatives --remove g77 %{_bindir}/%{program_prefix}g77-%{version}
fi
%endif

%if %{build_java}
%post java
update-alternatives --install %{_bindir}/gcj gcj %{_bindir}/gcj-%{version} %{alternative_priority}
[ -e %{_bindir}/gcj ] || update-alternatives --auto gcj
# Remove binaries if not alternativeszificated yet
[ ! -L %{_bindir}/javac ] && /bin/rm -f %{_bindir}/javac
update-alternatives --install %{_bindir}/javac javac %{_bindir}/gcj-javac-%{version} %{gcj_alternative_priority}
update-alternatives --install %{_bindir}/jdk-config jdk-config %{_bindir}/gcj-jdk-config-%{version} %{gcj_alternative_priority}

%postun java
if [ ! -f %{_bindir}/gcj-%{version} ]; then
  update-alternatives --remove gcj %{_bindir}/gcj-%{version}
fi
if [ ! -f %{_bindir}/gcj-javac-%{version} ]; then
  update-alternatives --remove javac %{_bindir}/gcj-javac-%{version}
fi
if [ ! -f %{_bindir}/gcj-jdk-config-%{version} ]; then
  update-alternatives --remove jdk-config %{_bindir}/gcj-jdk-config-%{version}
fi
%endif

%if %{build_java}
%post -n %{GCJ_TOOLS}
for app in %{gcj_alternative_programs}; do
  # Remove binaries if not alternativeszificated yet
  [ ! -L %{_bindir}/$app ] && /bin/rm -f %{_bindir}/$app
  # Build slaves list
  [[ "$app" != java ]] && slaves="$slaves --slave %{_bindir}/$app $app %{_bindir}/gcj-$app-%{version}"
done
update-alternatives --install %{_bindir}/java java %{_bindir}/gcj-java-%{version} %{gcj_alternative_priority} $slaves
%endif

%if %{build_java}
%postun -n %{GCJ_TOOLS}
if [ ! -f "%{_bindir}/gcj-java-%{version}" ]; then
  update-alternatives --remove java %{_bindir}/gcj-java-%{version}
fi
%endif

%if %{build_java}
%post -n %{libgcj_name}-devel
update-alternatives --install %{_includedir}/libgcj libgcj %{_includedir}/libgcj-%{version} %{gcj_alternative_priority}
%endif

%if %{build_java}
%postun -n %{libgcj_name}-devel
if [ ! -d %{_includedir}/libgcj-%{version} ]; then
  update-alternatives --remove gcj %{_includedir}/libgcj-%{version}
fi
%endif

%if %{build_java}
%post -n %{libgcj_name} -p /sbin/ldconfig
%postun -n %{libgcj_name} -p /sbin/ldconfig
%endif

%if %{build_objc}
%post -n %{libobjc_name} -p /sbin/ldconfig
%postun -n %{libobjc_name} -p /sbin/ldconfig
%endif

%if %{build_fortran}
%post -n %{libf2c_name} -p /sbin/ldconfig
%postun -n %{libf2c_name} -p /sbin/ldconfig
%endif

%if %{build_ada}
%post -n %{libgnat_name} -p /sbin/ldconfig
%postun -n %{libgnat_name} -p /sbin/ldconfig
%endif

%post doc
%_install_info gcc.info
%_install_info cpp.info
%if %{build_pascal}
%_install_info gpc.info
%_install_info gpcs.info
%endif
%if %{build_fortran}
%_install_info g77.info
%endif
%if %{build_ada}
%_install_info gnat_rm.info
%_install_info gnat_ug.info
%endif

%preun doc
if [ "$1" = "0" ];then /sbin/install-info %{_infodir}/gcc.info.bz2 --dir=%{_infodir}/dir --remove;fi;
%_remove_install_info cpp.info
%if %{build_pascal}
%_remove_install_info gpc.info
%_remove_install_info gpcs.info
%endif
%if %{build_fortran}
%_remove_install_info g77.info
%endif
%if %{build_ada}
%_remove_install_info gnat_rm.info
%_remove_install_info gnat_ug.info
%endif

%files
%defattr(-,root,root)
#
%doc gcc/README* gcc/*ChangeLog*
%if %{build_propolice}
%config(noreplace) %{_sysconfdir}/profile.d/propolice.sh
%config(noreplace) %{_sysconfdir}/profile.d/propolice.csh
%endif
%{_mandir}/man1/%{program_prefix}gcc%{program_suffix}.1*
%if "%{name}" == "gcc"
%{_mandir}/man1/gcov%{program_suffix}.1*
%endif
#
%{_bindir}/%{program_prefix}gcc%{branch}-version
%{_bindir}/%{program_prefix}gcc-%{version}
%{_bindir}/%{gcc_target_platform}-gcc%{program_suffix}
%if "%{name}" == "gcc"
%{_bindir}/protoize%{program_suffix}
%{_bindir}/unprotoize%{program_suffix}
%{_bindir}/gcov%{program_suffix}
%endif
%if %{system_compiler}
%{_bindir}/cc
%{_bindir}/c89
%{_bindir}/c99
%endif
#
%{target_libdir}/libgcc_s.so
%if "%{name}" == "gcc"
%ifarch ppc
%{_libdir}/libgcc_s_nof.so
%endif
%ifarch %{biarches}
%{_prefix}/lib/libgcc_s.so
%{_prefix}/lib/libgcc_s_32.so
%endif
%endif
#
%ifarch %{biarches}
/%{_lib}/32
%{_libdir}/32
%endif
#
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/cc1
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/collect2
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/crt*.o
%if "%{arch}" == "ppc"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/ecrt*.o
%endif
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcc.a
%if !%{build_cross_bootstrap}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcc_eh.a
%endif
%if "%{name}" == "gcc"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/SYSCALLS.c.X
%endif
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/specs
%ifarch %{biarches}
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/crt*.o
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libgcc.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libgcc_eh.a
%endif
%ifarch ppc
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/crt*.o
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/ecrt*.o
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libgcc.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libgcc_eh.a
%endif
#
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/float.h
%if %{build_fortran}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/g2c.h
%endif
%if "%{arch}" == "i386"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/mmintrin.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/xmmintrin.h
%endif
%if "%{arch}" == "x86_64"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/mmintrin.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/xmmintrin.h
%endif
%if "%{arch}" == "ppc"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/altivec.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/ppc-asm.h
%endif
%if "%{arch}" == "ia64"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/ia64intrin.h
%endif
%if "%{arch}" == "m68k"
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/math-68881.h
%endif
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/iso646.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/limits.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/stdarg.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/stdbool.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/stddef.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/syslimits.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/unwind.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/varargs.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/README

%files -n %{libgcc_name}
%defattr(-,root,root)
%if "%{name}" == "gcc"
/%{_lib}/libgcc_s-%{version}.so.%{libgcc_major}
/%{_lib}/libgcc_s.so.%{libgcc_major}
%endif
%if %{?cross:1}%{!?cross:0}
%{target_libdir}/libgcc_s-%{version}.so.%{libgcc_major}
%{target_libdir}/libgcc_s.so.%{libgcc_major}
%endif
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
#
%{_mandir}/man1/%{program_prefix}cpp%{program_suffix}.1*
#
/lib/cpp
%ghost %{_bindir}/cpp
%{_bindir}/%{program_prefix}cpp-%{version}

%if %{build_cxx}
%files c++
%defattr(-,root,root)
#
%doc gcc/cp/ChangeLog*
%{_mandir}/man1/%{program_prefix}g++%{program_suffix}.1*
#
%ghost %{_bindir}/c++
%{_bindir}/%{program_prefix}g++-%{version}
%{_bindir}/%{gcc_target_platform}-g++%{program_suffix}
%{_bindir}/%{gcc_target_platform}-c++%{program_suffix}
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/cc1plus
%endif

%if %{build_cxx}
%files -n %{libstdcxx_name}
%defattr(-,root,root)
%{target_libdir}/libstdc++.so.%{libstdcxx_major}
%{target_libdir}/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%ifarch %{biarches}
%{_prefix}/lib/libstdc++.so.%{libstdcxx_major}
%{_prefix}/lib/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%endif
%ifarch ppc
%dir %{_libdir}/nof
%{_libdir}/nof/libstdc++.so.%{libstdcxx_major}
%{_libdir}/nof/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%endif
%endif

%if %{build_cxx}
%files -n %{libstdcxx_name}-devel
%defattr(-,root,root)
#
%doc libstdc++-v3/ChangeLog* libstdc++-v3/README* libstdc++-v3/docs/html/
#
%dir %{libstdcxx_includedir}
%{libstdcxx_includedir}/*
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/cxxabi.h
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libstdc++.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libsupc++.a
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libstdc++.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libsupc++.a
%endif
%ifarch ppc
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libstdc++.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libsupc++.a
%endif
%endif

%if %{build_cxx}
%files -n %{libstdcxx_name}-static-devel
%defattr(-,root,root)
%doc libstdc++-v3/README
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libstdc++.a
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libstdc++.a
%endif
%ifarch ppc
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libstdc++.a
%endif
%endif

%if %{build_objc}
%files objc
%defattr(-,root,root)
#
%doc rpm.doc/objc/*
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/cc1obj
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libobjc.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libobjc.so
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libobjc.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libobjc.so
%endif
%ifarch ppc
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libobjc.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libobjc.so
%endif
#
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/objc
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/objc/*.h
%endif

%if %{build_objc}
%files -n %{libobjc_name}
%defattr(-,root,root)
#
%doc rpm.doc/libobjc/*
%doc libobjc/THREADS* libobjc/ChangeLog
#
%{target_libdir}/libobjc.so.%{libobjc_major}
%{target_libdir}/libobjc.so.%{libobjc_major}.0.0
%ifarch %{biarches}
%{_prefix}/lib/libobjc.so.%{libobjc_major}
%{_prefix}/lib/libobjc.so.%{libobjc_major}.0.0
%endif
%endif

%if %{build_pascal}
%files gpc
%defattr(-,root,root)
#
%doc rpm.doc/gpc/*
%{_mandir}/man1/%{program_prefix}gpc%{program_suffix}.1*
%{_mandir}/man1/%{program_prefix}/gpc-run%{program_suffix}.1*
#
%{_bindir}/gpc-run
%{_bindir}/binobj
%ghost %{_bindir}/gpc
%ghost %{_bindir}/gpidump
%{_bindir}/%{program_prefix}gpc-%{version}
%{_bindir}/%{program_prefix}gpidump-%{version}
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/gpc1
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/gpcpp
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgpc.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/gpc-in-c.h
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units/*.c
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units/*.h
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units/*.s
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units/*.inc
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/units/*.pas
%endif

%if %{build_fortran}
%files g77
%defattr(-,root,root)
#
%doc gcc/f/README rpm.doc/g77/*
%{_mandir}/man1/%{program_prefix}g77%{program_suffix}.1*
#
%ghost %{_bindir}/g77
%ghost %{_bindir}/f77
%{_bindir}/%{program_prefix}g77-%{version}
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/f771
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libfrtbegin.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libg2c.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libg2c.so
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libfrtbegin.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libg2c.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libg2c.so
%endif
%ifarch ppc
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libg2c.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libg2c.so
%endif
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/g2c.h
%endif

%if %{build_fortran}
%files -n %{libf2c_name}
%defattr(-,root,root)
#
%{target_libdir}/libg2c.so.%{libf2c_major}
%{target_libdir}/libg2c.so.%{libf2c_major}.0.0
%ifarch %{biarches}
%{_prefix}/lib/libg2c.so.%{libf2c_major}
%{_prefix}/lib/libg2c.so.%{libf2c_major}.0.0
%endif
%endif

%if %{build_java}
%files java
%defattr(-,root,root)
%doc gcc/java/ChangeLog*
%{_bindir}/gcj-%{version}
%{_bindir}/gcj-javac-%{version}
%{_bindir}/gcj-jdk-config-%{version}
%ghost %{_bindir}/javac
%ghost %{_bindir}/jdk-config
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/jc1
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/jvgenmain
%endif

%if %{build_java}
%files -n %{GCJ_TOOLS}
%defattr(-,root,root)
%doc rpm.doc/fastjar/*
%{_bindir}/gcj-java-%{version}
%{_bindir}/gcj-jar-%{version}
%{_bindir}/gcj-grepjar-%{version}
%{_bindir}/gcj-rmic-%{version}
%{_bindir}/gcj-rmiregistry-%{version}
%ghost %{_bindir}/java
%ghost %{_bindir}/jar
%ghost %{_bindir}/grepjar
%ghost %{_bindir}/rmic
%ghost %{_bindir}/rmiregistry
%{_bindir}/gij%{program_suffix}
%{_bindir}/gcjh%{program_suffix}
%{_bindir}/jcf-dump%{program_suffix}
%{_bindir}/jv-scan%{program_suffix}
#
%{_mandir}/man1/gij*.1*
%{_mandir}/man1/gcjh*.1*
%{_mandir}/man1/jv-scan*.1*
%{_mandir}/man1/jcf-dump*.1*
%endif

%if %{build_java}
%files -n %{libgcj_name}
%defattr(-,root,root)
#
%{target_libdir}/libgcj.so.%{libgcj_major}
%{target_libdir}/libgcj.so.%{libgcj_major}.0.0
%{target_libdir}/lib-org-xml-sax.so.0
%{target_libdir}/lib-org-xml-sax.so.0.0.0
%{target_libdir}/lib-org-w3c-dom.so.0
%{target_libdir}/lib-org-w3c-dom.so.0.0.0
%ifarch %{biarches}
%{_prefix}/lib/libgcj.so.%{libgcj_major}
%{_prefix}/lib/libgcj.so.%{libgcj_major}.0.0
%{_prefix}/lib/lib-org-xml-sax.so.0
%{_prefix}/lib/lib-org-xml-sax.so.0.0.0
%{_prefix}/lib/lib-org-w3c-dom.so.0
%{_prefix}/lib/lib-org-w3c-dom.so.0.0.0
%endif
#
%dir %{_datadir}/java
%{_datadir}/java/libgcj-%{version}.jar
%endif

%if %{build_java}
%files -n %{libgcj_name}-devel
%defattr(-,root,root)
#
%doc rpm.doc/boehm-gc/*
%doc rpm.doc/libjava/*
#
%{_bindir}/jv-convert%{program_suffix}
#
%ghost %{_includedir}/libgcj
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/include/libgcj
#
%dir %{libjava_includedir}
%{libjava_includedir}/jni.h
%{libjava_includedir}/jvmpi.h
%dir %{libjava_includedir}/gcj
%{libjava_includedir}/gcj/*.h
%dir %{libjava_includedir}/gnu
%{libjava_includedir}/gnu/*
%dir %{libjava_includedir}/java
%{libjava_includedir}/java/*
%dir %{libjava_includedir}/javax
%{libjava_includedir}/javax/*
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcj.spec
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcj.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/lib-org-w3c-dom.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/lib-org-xml-sax.so
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libgcj.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/lib-org-w3c-dom.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/lib-org-xml-sax.so
%endif
%ifarch
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libgcj.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/lib-org-w3c-dom.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/lib-org-xml-sax.so
%endif
%endif

%if %{build_java}
%files -n %{libgcj_name}-static-devel
%defattr(-,root,root)
%doc libjava/README libjava/LIBGCJ_LICENSE
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/libgcj.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/lib-org-w3c-dom.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/lib-org-xml-sax.a
%ifarch %{biarches}
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/libgcj.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/lib-org-w3c-dom.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/32/lib-org-xml-sax.a
%endif
%ifarch ppc
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/libgcj.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/lib-org-w3c-dom.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/nof/lib-org-xml-sax.a
%endif
%endif

%if %{build_ada}
%files gnat
%defattr(-,root,root)
#
%{_bindir}/gnat*
#
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/gnat1
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adainclude
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adainclude/*.adb
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adainclude/*.ads
%dir %{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/*.ali
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/Makefile.adalib
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/libgmem.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/libgnat.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/libgnat.so
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/libgnarl.a
%{_libdir}/gcc-lib/%{gcc_target_platform}/%{version}/adalib/libgnarl.so
%endif

%if %{build_java}
%files -n %{libffi_name}-devel
%defattr(-,root,root)
%doc libffi/README libffi/LICENSE libffi/ChangeLog*
%{_includedir}/ffi*.h
%{_libdir}/libffi.a
%%ifarch %{biarches}
%{_prefix}/lib/libffi.a
%%endif
%endif

%if %{build_ada}
%files -n %{libgnat_name}
%defattr(-,root,root)
#
%{target_libdir}/libgnat-*.so.*
%{target_libdir}/libgnarl-*.so.*
%ifarch %{biarches}
# FIXME: not biarch ada yet
#%{_prefix}/lib/libgnat-*.so.*
#%{_prefix}/lib/libgnarl-*.so.*
%endif
%endif

%if %{build_colorgcc}
%files colorgcc
%defattr (-,root,root)
%doc COPYING.colorgcc CREDITS.colorgcc ChangeLog.colorgcc
%config(noreplace) %{_sysconfdir}/colorgccrc
%{_bindir}/colorgcc
%{_bindir}/colorgcc-%{version}
%endif

%if %{build_doc}
%files doc
%defattr(-,root,root)
%{_infodir}/cppinternals.info*
%{_infodir}/cpp.info*
%{_infodir}/gcc.info*
%if %{build_ada}
%{_infodir}/gnat-style.info*
%{_infodir}/gnat_rm.info*
%{_infodir}/gnat_ug.info*
%endif
%if %{build_java}
%{_infodir}/gcj.info*
%endif
%if %{build_pascal}
%{_infodir}/gpc.info*
%{_infodir}/gpcs.info*
%endif
%if %{build_fortran}
%{_infodir}/g77.info*
%endif
%endif

%if %{build_pdf_doc}
%files doc-pdf
%defattr(-,root,root)
%doc gcc/doc/cppinternals.pdf
%doc gcc/doc/gcc.pdf
%doc gcc/doc/cpp.pdf
%if %{build_ada}
%doc gcc/ada/gnat_rm.pdf
%doc gcc/ada/gnat_ug.pdf
%endif
%if %{build_fortran}
%doc gcc/f/g77.pdf
%endif
%endif

%changelog
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
