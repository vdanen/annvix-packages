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
%define version 	2.1.3
%define release 	%_revrel

%define major		2
%define	libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	The shared library for the S-Lang extension language
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.s-lang.org
Source0:	ftp://space.mit.edu/pub/davis/slang/v2.1/%{name}-%{version}.tar.bz2
Source1:	ftp://space.mit.edu/pub/davis/slang/v2.1/%{name}-%{version}.tar.bz2.asc
Patch0:		slang-2.1.0-mdv-no_glibc_private.patch
Patch1:		slang-2.1.3-fdr-makefile.patch
Patch2:		slang-2.0.5-fdr-LANG.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glibc-devel
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRequires:	pcre-devel
BuildRequires:	png-devel
BuildRequires:	x11-devel

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
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	slang

%description -n %{libname}
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.


%package -n %{devname}
Summary:	The static library and header files for development using S-Lang
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 -d

%description -n %{devname}
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
%patch0 -p1 -b .no_glibc_private
%patch1 -p1
%patch2 -p1


%build
%configure2_5x --includedir=%{_includedir}/slang

%make all


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std DESTDIR=%{buildroot} install

# Remove unpackages files
rm -rf	%{buildroot}%{_docdir}/{slang,slsh}
rm -f %{buildroot}%{_bindir}/slsh
rm -rf %{buildroot}%{_datadir}/slsh
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_sysconfdir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libslang.so.%{major}*
%dir %{_libdir}/slang
%{_libdir}/slang/v%{major}

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/lib*.so
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h

%files doc
%defattr(-,root,root)
%doc README changes.txt NEWS


%changelog
* Fri Feb 22 2008 Vincent Danen <vdanen-at-build.annvix.org> 2.1.3
- 2.1.3
- drop P1; we don't ship slsh anyways, and it's no longer required
- new P1, P2 from Fedora
- buildrequires x11-devel

* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1
- 2.1.1
- drop UTF8 patches; implemented upstream
- dropped P7, no longer required
- updated URL
- P0: don't use private glibc symbols (fdr bug #161536)
- P1: fix slsh install
- drop S0
- don't package slsh
- update buildrequires
- make tests
- build against new pcre
- implement devel naming policy
- implement library provides policy

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
