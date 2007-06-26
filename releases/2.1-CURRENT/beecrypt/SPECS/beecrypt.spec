#
# spec file for package beecrypt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		beecrypt
%define version		4.1.2
%define release		%_revrel

%define major		6
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d
%define odevname	%mklibname %{name} 6 -d

Summary:	An open source cryptography library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://beecrypt.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/beecrypt/%{name}-%{version}.tar.gz
Patch0:		beecrypt-4.1.2-fdr-base64.patch
Patch1:		beecrypt-4.1.2-fdr-python-api.patch
Patch2:		beecrypt-4.1.2-fdr-biarch.patch
Patch3:		beecrypt-4.1.2-avx-lib64.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	doxygen
BuildRequires:	python-devel >= 2.4

%description
Beecrypt is a general-purpose cryptography library.


%package -n %{libname}
Summary:	An open source cryptography library
Group:		System/Libraries

%description -n %{libname}
Beecrypt is a general-purpose cryptography library.


%package -n %{devname}
Summary:	Files needed for developing applications with beecrypt
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{odevname}

%description -n %{devname}
Beecrypt is a general-purpose cryptography library.  This package contains
files needed for developing applications with beecrypt.


%package python
Summary:	Files needed for python applications using beecrypt
Group:		Development/C
Requires:	python >= %{pyver}
Requires:	%{libname} = %{version}-%{release}

%description python
Beecrypt is a general-purpose cryptography library.  This package contains
files needed for using python with beecrypt.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .base64
%patch1 -p1 -b .python-api
%patch2 -p1 -b .biarch
%patch3 -p0 -b .lib64
./autogen.sh


%build
%configure \
    --enable-shared \
    --enable-static \
    --with-python \
    CPPFLAGS="-I%{_includedir}/python%{pyver}"

%make
doxygen


%check
make check || :
cat /proc/cpuinfo
make bench || :


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

# XXX nuke unpackaged files, artifacts from using libtool to produce module
rm -f %{buildroot}%{py_platsitedir}/_bc.*a


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so

%files python
%defattr(-,root,root)
%{py_platsitedir}/_bc.so

%files doc
%defattr(-,root,root)
%doc README BENCHMARKS BUGS docs/html docs/latex


%changelog
* Tue Jun 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.1.2
- 4.1.2
- synced patches with Fedora
- use python macros
- implement devel naming policy
- implement library provides policy
- rebuild with SSP
- P3: fix build on x86_64

* Fri May 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- rebuild againt new python

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-6avx
- bootstrap build (new gcc, new glibc)

* Mon Aug 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-5avx
- P2: alpha doesn't use lib64
- minor spec cleanups

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-4avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-3avx
- bootstrap build
- always build with python support as we need python-devel to compile
  even without the python package (eh?)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-2avx
- Annvix build

* Fri May 09 2004 Vincent Danen <vdanen@opensls.org> 3.1.0-1sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
