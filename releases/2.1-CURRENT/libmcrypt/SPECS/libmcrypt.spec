#
# spec file for package libmcrypt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libmcrypt
%define version		2.5.8
%define release		%_revrel

%define major		4
%define libname		%mklibname mcrypt %{major}
%define devname		%mklibname mcrypt -d
%define staticdevname	%mklibname mcrypt -d -s

Summary:	Thread-safe data encryption library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://mcrypt.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtool-devel
BuildRequires:	multiarch-utils

%description
Libmcrypt is a thread-safe library providing a uniform interface
to access several block and stream encryption algorithms.

Some algorithms which are supported:
SERPENT, RIJNDAEL, 3DES, GOST, SAFER+, CAST-256, RC2, XTEA, 3WAY,
TWOFISH, BLOWFISH, ARCFOUR, WAKE and more. 


%package -n %{libname}
Summary:	Thread-safe data encryption library
Group:		System/Libraries
Requires:	%{name} >= %{version}

%description -n %{libname}
Libmcrypt is a thread-safe library providing a uniform interface
to access several block and stream encryption algorithms.

Some algorithms which are supported:
SERPENT, RIJNDAEL, 3DES, GOST, SAFER+, CAST-256, RC2, XTEA, 3WAY,
TWOFISH, BLOWFISH, ARCFOUR, WAKE and more. 


%package -n %{devname}
Summary:	Header files and libraries for developing apps with libmcrypt
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname mcrypt 4 -d

%description -n %{devname}
This package contains the header files and libraries needed to
develop programs that use the libmcrypt library.
Install it if you want to develop such applications.


%package -n %{staticdevname}
Summary:	Static libraries for developing apps with libmcrypt
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	%{name}-devel = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%mklibname mcrypt 4 -d -s

%description -n %{staticdevname}
This package contains the static libraries needed to
develop programs that use the libmcrypt library.
Install it if you want to develop such applications.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

%build
%serverbuild
#libtoolize --copy --force; aclocal; autoconf

./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --disable-ltdl \
    --disable-ltdl-install \
    --enable-dynamic-loading \
    --enable-static \
    --enable-shared

#    --build %{_target_platform} \
#    --host %{_target_platform} \
#    --target %{_target_platform} \

%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

%multiarch_binaries %{buildroot}%{_bindir}/libmcrypt-config


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_libdir}/%{name}/*.la
%{_libdir}/%{name}/*.so

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{devname}
%defattr(-, root, root)
%{_mandir}/man3/*
%multiarch %{multiarch_bindir}/libmcrypt-config
%{_bindir}/libmcrypt-config
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/mcrypt.h
%dir %{_includedir}/mutils
%{_includedir}/mutils/mcrypt.h
%{_datadir}/aclocal/*.m4

%files -n %{staticdevname}
%defattr(-, root, root)
%{_libdir}/*.a
%{_libdir}/%{name}/*.a

%files doc
%defattr(-, root, root)
%doc AUTHORS COPYING.LIB ChangeLog INSTALL KNOWN-BUGS NEWS README THANKS TODO doc/README.* doc/*.c


%changelog
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5.8
- get rid of %%odevname

* Sat Sep 8 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5.8
- 2.5.8
- implement devel naming policy
- implement library provides policy

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7-12avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7-11avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7-10avx
- bootstrap build

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7-9avx
- multiarch support
- run make check

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7-8avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.5.7-7sls
- remove %%prefix
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.5.7-6sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
