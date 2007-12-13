#
# spec file for package libtool
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libtool
%define version		1.5.24
%define release		%_revrel

%define major		3
%define libname		%mklibname ltdl %{major}
%define devname		%mklibname ltdl -d
%define odevname	%mklibname ltdl 3 -d

# define biarch platforms
%define biarches 	x86_64 ppc64 sparc64
%ifarch x86_64
%define alt_arch 	i586
%endif
%ifarch ppc64
%define alt_arch 	ppc
%endif
%ifarch sparc64
%define alt_arch 	sparc
%endif

Summary:	The GNU libtool, which simplifies the use of shared libraries
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/libtool/libtool.html
Source:		ftp://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.gz
Source1:	ftp://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.gz.sig
Source2:	libtool-cputoolize.sh
# (Abel) Patches please only modify ltmain.in and don't touch ltmain.sh
# otherwise ltmain.sh will not be regenerated, and patches will be lost
Patch0:		libtool-1.5.6-relink.patch
Patch1:		libtool-1.5.18-lib64.patch
Patch2:		libtool-1.5.6-ltmain-SED.patch
Patch3:		libtool-1.5.6-libtoolize--config-only.patch
Patch4:		libtool-1.5.6-test-dependency.patch
Patch5:		libtool-1.5-testfailure.patch
Patch8:		libtool-1.5.22-fdr-anygcc.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	automake1.8
BuildRequires:	autoconf2.5
%ifarch %{biarches}
BuildRequires:	setarch
%endif

Requires:	file
Requires:	sed
Requires(post):	info-install
Requires(preun): info-install


%description
The libtool package contains the GNU libtool, a set of shell scripts
which automatically configure UNIX and UNIX-like architectures to
generically build shared libraries.  Libtool provides a consistent,
portable interface which simplifies the process of using shared
libraries.


%package -n %{libname}
Summary:	Shared library files for libtool
Group:		Development/C
License:	LGPL
Provides:	libltdl = %{version}-%{release}

%description -n %{libname}
Shared library files for libtool DLL library from the libtool package.


%package -n %{devname}
Summary:	Development files for libtool
Group:		Development/C
License:	LGPL
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Provides:	libltdl-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{odevname}

%description -n %{devname}
Development headers, and files for development from the libtool package.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .relink
%patch1 -p1 -b .lib64
%patch2 -p1 -b .ltmain-SED
%patch3 -p1 -b .libtoolize--config-only
%patch4 -p1 -b .test-dependency
%patch5 -p1
%patch8 -p1 -b .anygcc

./bootstrap


%build
# don't use configure macro - it forces libtoolize, which is bad -jgarzik
# Use configure macro but define __libtoolize to be /bin/true -Geoff
%define __libtoolize /bin/true
# And don't overwrite config.{sub,guess} in this package as well -- Abel
%define __cputoolize /bin/true

# build alt-arch libtool first
# NOTE: don't bother to make libtool biarch capable within the same
# "binary", use the multiarch facility to dispatch to the right script.
%ifarch %{biarches}
mkdir -p build-%{alt_arch}-%{_target_os}
pushd    build-%{alt_arch}-%{_target_os}
    ../configure --prefix=%{_prefix} --build=%{alt_arch}-%{_real_vendor}-%{_target_os}%{?_gnu}
    make
popd
%endif

mkdir -p build-%{_target_cpu}-%{_target_os}
pushd build-%{_target_cpu}-%{_target_os}
    CONFIGURE_TOP=.. %configure2_5x
    make
popd


%check
pushd build-%{_target_cpu}-%{_target_os}
    # this README is required or make check fails
    touch libltdl/README
    set +x
    echo ====================TESTING=========================
    set -x
    # all tests must pass here
    make check
    set +x
    echo ====================TESTING END=====================
    set -x

    make -C demo clean
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std -C build-%{_target_cpu}-%{_target_os}

sed -e "s,@prefix@,%{_prefix}," -e "s,@datadir@,%{_datadir}," %{SOURCE2} \
    > %{buildroot}%{_bindir}/cputoolize
chmod 0755 %{buildroot}%{_bindir}/cputoolize

# biarch support
%ifarch %{biarches}
%multiarch_binaries %{buildroot}%{_bindir}/libtool
install -m 0755 build-%{alt_arch}-%{_target_os}/libtool %{buildroot}%{_bindir}/libtool
linux32 /bin/sh -c '%multiarch_binaries %{buildroot}%{_bindir}/libtool'
%endif

mv libltdl/README libltdl/README.libltdl

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info


%preun
%_remove_install_info %{name}.info


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/libtool.info*
%{_datadir}/libtool
%{_datadir}/aclocal/*.m4
%ifarch %{biarches}
%define alt_multiarch_bindir %(linux32 /bin/rpm --eval %%multiarch_bindir)                                                                                                         
%{multiarch_bindir}                                                                                                                                                                
%{multiarch_bindir}/libtool                                                                                                                                                        
%{alt_multiarch_bindir}                                                                                                                                                            
%{alt_multiarch_bindir}/libtool                                                                                                                                                    
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la

%files doc
%doc demo libltdl/README.libltdl
%doc AUTHORS INSTALL NEWS README THANKS TODO


%changelog
* Wed Dec 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5.24
- 1.5.24
- update P1 from Mandriva
- drop P6, P7: merged upstream

* Sat Oct 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5.22
- 1.5.22
- libs are LGPL licensed
- updated P6 from Mandriva
- P7: fix link.test check (Mandriva)
- P8: detect gcc path at runtime instead of requiring a specific version (Fedora)
- don't package changelogs; we have NEWS
- use %%check

* Sat Jun 23 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5.20
- implement devel naming policy
- implement library provides policy
- rebuild against gcc 4.1.2

* Tue Oct 31 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.20
- 1.5.20
- build against gcc 4.1
- fix the filelist for biarch archs (cjw)
- requires sed (for cputoolize)

* Sat May 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.18
- rebuild the toolchain against itself (gcc/glibc/libtool/binutils)

* Fri May 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.18
- rebuild against gcc 4.0.3
- add -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.18
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.18
- setarch is required for biarchs (for linux32)

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.18
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.18-1avx
- 1.5.18
- re-add the strict gcc requirement
- drop P7
- rediff P1
- fix requires

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-6avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-5avx
- rebuild
- drop BuildReq on setarch if we're a biarch
- run the configure/make scripts without linux32 or else configure
  and make think gcc doesn't work; at any rate, libtool is a shell script
  and things are done properly with or without using linux32

* Thu Jul 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-4avx
- rebuild against gcc 3.4.4
- BuildRequires: setarch

* Thu Jul 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-3avx
- multiarch
- don't use the crappy hack to get the gcc version and just make it
  require gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-2avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-1avx
- 1.5.12
- sync all patches with Mandrake 1.5.12-4mdk
- prepare for multiarch (from gb)
- /usr/bin/libtool is compiler dependent

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3-12avx
- require packages not files
- Annvix build

* Sat Jun 11 2004 Vincent Danen <vdanen@opensls.org> 1.4.3-11sls
- own /usr/share/libtool

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.4.3-10sls
- minor spec cleanups

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 1.4.3-9sls
- sync with 8mdk (gbeauchesne): fix mklibnamification

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 1.4.3-8sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
