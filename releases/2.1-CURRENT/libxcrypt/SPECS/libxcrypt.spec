#
# spec file for package libxcrypt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libxcrypt
%define version		2.4
%define release		%_revrel

%define major		1
%define libname		%mklibname xcrypt %{major}
%define devname		%mklibname xcrypt -d

Summary:	Crypt library for DES, MD5, and blowfish
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
Source:		ftp://ftp.suse.com/pub/people/kukuk/libxcrypt/libxcrypt-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, and passwords with blowfish
encryption.


%package -n %{libname}
Summary:        Crypt library for DES, MD5, and blowfish
Group:          System/Libraries
Provides:       %{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}

%description -n %{libname}
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, and passwords with blowfish
encryption.


%package -n %{devname}
Summary:	Development files for Crypt library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	xcrypt-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}

%description -n %{devname}
libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports, beside DES crypt and MD5, passwords with blowfish
encryption.

This package contains the header files and static libraries, which are
necessary to develop your own software using libxcrypt.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

# remove unpackaged files
rm -f %{buildroot}%{_libdir}/libxcrypt
rm -f %{buildroot}%{_libdir}/libxcrypt.1


%check
make check


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libxcrypt.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libxcrypt.a
%{_libdir}/libxcrypt.la
%{_libdir}/libxcrypt.so

%files doc
%defattr(-,root,root)
%doc README NEWS README.ufc-crypt README.bcrypt


%changelog
* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.4
- 2.4
- implement devel naming policy
- implement library provides policy
- libify the package
- use make check

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0 
- add -doc subpackage
- rebuild with gcc4
- call ldconfig in %%post/%%postun

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0-4avx
- bootstrap build
- get rid of the ugly hacks we don't need anymore
- put the lib files in %%{_libdir} rather than /lib

* Wed Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0-3avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.0-2sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.0-1sls
- first OpenSLS package
- based on SUSE's 2.0-32 package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
