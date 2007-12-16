de#
# spec file for package elfutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		elfutils
%define version		0.129
%define release		%_revrel

%define major		1
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d
%define staticdevname	%mklibname %{name} -d -s

%define _programprefix 	eu-

%define build_check		1
%{expand: %{?_without_CHECK:	%%define build_check 0}}
%{expand: %{?_with_CHECK:	%%define build_check 1}}

Summary:	A collection of utilities and DSOs to handle compiled objects
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source:		ftp://sources.redhat.com/pub/systemtap/elfutils/%{name}-%{version}.tar.gz
# these 2 patches are from ftp://sources.redhat.com/pub/systemtap/elfutils/
Patch0:		elfutils-robustify.patch
Patch1:		elfutils-strip-copy-symtab.patch
Patch2:		elfutils-0.128-mdv-elflint.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gcc >= 3.4
BuildRequires:	sharutils
BuildRequires:	libtool-devel

Requires:	%{libname} = %{version}-%{release}

%description
Elfutils is a collection of utilities, including:

   * %{_programprefix}nm: for listing symbols from object files
   * %{_programprefix}size: for listing the section sizes of an object or archive file
   * %{_programprefix}strip: for discarding symbols
   * %{_programprefix}readelf: the see the raw ELF file structures
   * %{_programprefix}elflint: to check for well-formed ELF files


%package -n %{devname}
Summary:	Development libraries to handle compiled objects
License:	GPL
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 -d

%description -n %{devname}
This package contains the headers and dynamic libraries to create
applications for handling compiled objects.

   * libelf allows you to access the internals of the ELF object file
     format, so you can see the different sections of an ELF file.
   * libebl provides some higher-level ELF access functionality.
   * libasm provides a programmable assembler interface.


%package -n %{staticdevname}
Summary:	Static libraries for development with libelfutils
License:	GPL
Group:		Development/Other
Requires:	%{devname} = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 -d -s

%description -n %{staticdevname}
This package contains the static libraries to create applications for
handling compiled objects.


%package -n %{libname}
Summary:	Libraries to read and write ELF files
License:	OSL
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}
Provides:	libelf = %{version}-%{release}

%description -n %{libname}
This package provides DSOs which allow reading and writing ELF files
on a high level.  Third party programs depend on this package to read
internals of ELF files.  The programs of the elfutils package use it
also to generate new ELF files.

Also included are numerous helper libraries which implement DWARF,
ELF, and machine-specific ELF handling.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

# Don't use -Werror with -Wformat=2 -std=gnu99 as %a[ won't be caught
# as the GNU %a extension.
perl -pi -e '/AM_CFLAGS =/ and s/-Werror//g' ./tests/Makefile.{in,am}

%patch0 -p1 -b .robustify
%patch1 -p1 -b .strip_copy_symtab
%patch2 -p1 -b .erllint

%build
%ifarch x86_64
# cheap hack to yank -Werror out since it kills the build on x86_64
perl -pi -e s'/-Werror//g' */Makefile.{in,am}
%endif

mkdir build-%{_target_platform}
pushd build-%{_target_platform}
    CONFIGURE_TOP=.. \
    %configure2_5x \
        --program-prefix=%{_programprefix} \
        --enable-shared
    %make
popd


%check
%if %{build_check}
pushd build-%{_target_platform}
    %make check
# || :
popd
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}

%makeinstall_std -C build-%{_target_platform}

chmod +x %{buildroot}%{_libdir}/lib*.so*
chmod +x %{buildroot}%{_libdir}/elfutils/lib*.so*

# XXX Nuke unpackaged files
{ cd %{buildroot}
    rm -f .%{_bindir}/eu-ld
    rm -f .%{_bindir}/eu-objdump
    rm -f .%{_includedir}/elfutils/libasm.h
    rm -f .%{_libdir}/libasm{-%{version},}.so
    rm -f .%{_libdir}/libasm.{a,so}
}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/eu-addr2line
%{_bindir}/eu-ar
%{_bindir}/eu-elfcmp
%{_bindir}/eu-findtextrel
%{_bindir}/eu-elflint
%{_bindir}/eu-nm
%{_bindir}/eu-ranlib
%{_bindir}/eu-readelf
%{_bindir}/eu-size
%{_bindir}/eu-strings
%{_bindir}/eu-strip
%{_bindir}/eu-unstrip
%{_libdir}/libdw-%{version}.so
%{_libdir}/libdw*.so.*
%dir %{_libdir}/elfutils
%{_libdir}/elfutils/lib*.so

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/dwarf.h
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/libebl.h
%{_includedir}/elfutils/libdw.h
%{_includedir}/elfutils/libdwfl.h
%{_libdir}/libelf.so
%{_libdir}/libdw.so

%files -n %{staticdevname}
%defattr(-,root,root)
%{_libdir}/libebl.a
%{_libdir}/libelf.a
%{_libdir}/libdw.a

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf*.so.%{major}*

%files doc
%defattr(-,root,root)
%doc README NEWS TODO NOTES


%changelog
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.129
- get rid of %%odevname

* Sun Sep 9 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.129
- 0.129
- P0-P1: new upstream patches from Red Hat
- P2: elflint fix (Mandriva)
- do the tests
- don't redefine _gnu to %%{nil}
- drop libelf[0] obsoletes/provides
- versioned provides
- implement devel naming policy
- implement library provides policy

* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.120
- 0.120
- dropped P0, P1
- moved make check to %%check
- new P0: robustification patch (from Mandriva, who took it from Fedora)
- update license (GPL for everything but libs)
- disable make check; it fails on run-strings-test.sh and I see that Mandriva
  also comments it out (despite the %%build_check switch)
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.109
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.109
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.109-1avx
- 0.109

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.99-3avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.99-2avx
- rebuild for new gcc

* Fri Jul 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.99-1avx
- 0.99
- change License: s/GPL/OSL/
- drop P0

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.89-2avx
- bootstrap build

* Sun Sep 12 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.89-1avx
- 0.89
- P0: fix some -Werror issues (gbeauchesne)
- P1: atime alpha patch, obtained from Gentoo; bug #27372 (stefan)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.84-4avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 0.84-3sls
- minor spec cleanups
- remove some more unpackaged files

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 0.84-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
