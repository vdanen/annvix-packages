#
# spec file for package libneon
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libneon
%define version		0.24.7
%define release		%_revrel

%define	major		0.24
%define libname		%mklibname neon %{major}
%define devname		%mklibname neon -d
%define staticdevname	%mklibname neon -d -s

Summary: 	An HTTP and WebDAV client library, with a C interface
Name: 		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License: 	GPL
URL: 		http://www.webdav.org/neon/
Source0: 	http://www.webdav.org/neon/neon-%{version}.tar.gz
Source1: 	http://www.webdav.org/neon/neon-%{version}.tar.gz.asc
Patch0:		neon-0.23.9-config.patch
Patch1:		neon-0.24.7-gssapi.patch
Patch2:		neon-0.24.7-min.patch
Patch3:		neon-0.24.7-avx-no_wildcard_match.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	libxml2-devel
BuildRequires:	libxmlrpc-devel
BuildRequires:	pkgconfig
BuildRequires:	multiarch-utils >= 1.0.3
BuildConflicts:	krb5-devel

%description
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.


%package -n %{libname}
Summary:	An HTTP and WebDAV client library, with a C interface
Group:		System/Libraries
Provides:	libneon = %{version}-%{release}
Provides:	neon = %{version}-%{release}
Requires:	openssl >= 0.9.7

%description -n %{libname}
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.


%package -n %{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	libneon-devel = %{version}-%{release}
Provides:	neon-devel = %{version}-%{release}
Obsoletes:	%mklibname neon 0.24 -d

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.


%package -n %{staticdevname}
Summary:	Static %{libname} library
Group:		Development/C++
Requires:	%{devname} = %{version}
Provides:	libneon-static-devel = %{version}-%{release}
Provides:	neon-static-devel = %{version}-%{release}
Obsoletes:	%mklibname neon -d -s 0.24

%description -n	%{staticdevname}
Static %{libname} library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n neon-%{version}
%patch0 -p1 -b .config
%patch1 -p1 -b .gssapi
%patch2 -p1 -b .min
%patch3 -p1 -b .no_wildcard_match

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done


%build
# wierd stuff...
%define __libtoolize /bin/true

%serverbuild

%configure2_5x \
    --enable-shared \
    --enable-static \
    --with-ssl \
    --with-libxml2

%make

make check


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall

mv src/README README.neon

# fix this
rm -rf %{buildroot}%{_datadir}/doc

%multiarch_binaries %{buildroot}%{_bindir}/neon-config


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post -n %{devname} -p /sbin/ldconfig
%postun -n %{devname} -p /sbin/ldconfig


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root,755)
%{_libdir}/lib*.so.*

%files -n %{devname}
%defattr(-,root,root,755)
%multiarch %{multiarch_bindir}/neon-config
%{_bindir}/neon-config
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/neon.pc
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{staticdevname}
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files doc
%defattr(-,root,root,755)
%doc doc/*.txt doc/html README.neon
%doc AUTHORS BUGS ChangeLog NEWS README THANKS TODO


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7
- rebuild against new openssl

* Sun Sep 23 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7
- rebuild against new libxmlrpc

* Tue Aug 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7
- implement devel naming policy
- implement library provides policy

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7
- build against new libxml2 

* Sun Dec 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7
- make it conflict with krb-devel because if we krb5-config exists, GSSAPI support
  will be enabled which will prevent rpm from compiling with the new krb5 (which
  it can't seem to do with the new version, and will also prevent rpm-devel
  from requiring krb5-devel)

* Mon Dec 18 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7
- rebuild against new krb5

* Sat Jun 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7
- rebuild against new libxml2
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7-2avx
- correct the buildroot

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.24.7-1avx
- first Annvix build (required by new rpm)
- P3: disable the ssl wildcard_match test (just sits there doing nothing)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
