#
# spec file for package slang
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		slang
%define version 	1.4.9
%define release 	%_revrel

%define docversion	1.4.8
%define major		1
%define	libname		%mklibname %{name} %{major}

Summary:	The shared library for the S-Lang extension language
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		ftp://space.mit.edu/pub/davis/slang/
Source:		ftp://space.mit.edu/pub/davis/slang/slang-%{version}.tar.bz2
Source1:	ftp://space.mit.edu/pub/davis/slang/slang-%{docversion}-doc.tar.bz2
Source2:	README.UTF-8
# (mpol) utf8 patches from http://www.suse.de/~nadvornik/slang/
Patch1:		slang-debian-utf8.patch
Patch2:		slang-utf8-acs.patch
Patch3:		slang-utf8-fix.patch
Patch4:		slang-utf8-revert_soname.patch
Patch5:		slang-1.4.9-offbyone.patch
Patch6:		slang-1.4.5-utf8-segv.patch
Patch7:		slang-1.4.9-gcc4.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.


%package -n %{libname}
Summary:	The shared library for the S-Lang extension language
Group:		System/Libraries
Provides:	slang
Obsoletes:	slang

%description -n %{libname}
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.


%package -n %{libname}-devel
Summary:	The static library and header files for development using S-Lang
Group:		Development/C
Provides:	lib%{name}-devel slang-devel
Obsoletes:	slang-devel
Requires:	%{libname} = %{version}

%description -n %{libname}-devel
This package contains the S-Lang extension language static libraries
and header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .revert_soname
%patch5 -p1 -b .offbyone
%patch6 -p1 -b .segv
%patch7 -p1 -b .gcc4

cp %{SOURCE2} .


%build
%configure2_5x	--includedir=%{_includedir}/slang

#(peroyvind) passing this to configure does'nt work..
%make ELF_CFLAGS="%{optflags} -fno-strength-reduce -fPIC" elf
%make all


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}/slang
make prefix=%{buildroot}%{_prefix} \
    install_lib_dir=%{buildroot}%{_libdir} \
    install_include_dir=%{buildroot}%{_includedir}/slang \
    install-elf install

ln -sf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}

rm -f doc/doc/tm/tools/`arch`objs doc/doc/tm/tools/solarisobjs

# Remove unpackages files
rm -rf	%{buildroot}/usr/doc/slang


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h

%files doc
%defattr(-,root,root)
%doc COPYING COPYRIGHT README changes.txt README.UTF-8 NEWS


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-12avx
- P6: fix a segv (warly)
- P7: gcc4 build support (warly)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-11avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-10avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-9avx
- bootstrap build

* Mon Mar 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-8avx
- fix ownership

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-7avx
- put docs back in
- add utf8 patches from SUSE (mpol)
- make compat symlinks for devel package (mpol)
- P5: fix off-by-one error (mpol)
- spec cleanups

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-6avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.4.9-5sls
- minor spec cleanups
- remove %%build_opensls macro

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 1.4.9-4sls
- OpenSLS build
- tidy spec
- use %%build_opensls to prevent building -doc package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
