#
# spec file for package curl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		curl
%define version 	7.15.4
%define release		%_revrel

%define major		3
%define libname 	%mklibname %{name} %{major}

# Define to make check (default behavior)
%define do_check	1
%define __libtoolize	/bin/true

# Enable --with[out] <feature> at rpm command line
%{?_with_CHECK: %{expand: %%define do_check 1}}
%{?_without_CHECK: %{expand: %%define do_check 0}}

Summary:	Gets a file from a FTP, GOPHER or HTTP server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Networking/Other
URL:		http://curl.haxx.se/
Source:		http://curl.haxx.se/download/%{name}-%{version}.tar.bz2
Source1:	http://curl.haxx.se/download/%{name}-%{version}.tar.bz2.asc
Patch0:		curl-7.10.4-compat-location-trusted.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	groff-for-man
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel

Provides:	webfetch
Requires:	%{libname} = %{version}

%description 
curl is a client to get documents/files from servers, using any of the
supported protocols. The command is designed to work without user
interaction or any kind of interactivity.

curl offers a busload of useful tricks like proxy support, user
authentication, ftp upload, HTTP post, file transfer resume and more.

This version is compiled with SSL (https) support.


%package -n %{libname}
Summary:	A library of functions for file transfer
Group:		Networking/Other
Provides:	curl-lib = %{version}-%{release}
Obsoletes:	curl-lib

%description  -n %{libname}
libcurl is a library of functions for sending and receiving files through 
various protocols, including http and ftp.


%package -n %{libname}-devel
Summary:	Header files and static libraries for libcurl
Group:		Networking/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel
Obsoletes:	%{name}-devel

%description -n %{libname}-devel
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1


%build
export LIBS="-L%{_libdir} $LIBS"
CFLAGS="%{optflags} -O0" \
    ./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --datadir=%{_datadir} \
    --libdir=%{_libdir} \
    --includedir=%{_includedir} \
    --with-ssl
%make

skip_tests=
[ -n "$skip_tests" ] && {
    mkdir ./tests/data/skip/
    for t in $skip_tests; do
        mv ./tests/data/test$t ./tests/data/skip/
    done
}

%if %{do_check}
# At this stage, all tests must pass
make check
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%make install DESTDIR="%{buildroot}"


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/curl
%attr(0644,root,root) %{_mandir}/man1/curl.1*
%dir %{_datadir}/curl
%{_datadir}/curl/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcurl.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/curl-config
%attr(0644,root,root) %{_mandir}/man1/curl-config.1*
%{_libdir}/libcurl.so
%dir %{_includedir}/curl
%{_includedir}/curl/*
%{_libdir}/libcurl*a
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc docs/BUGS docs/KNOWN_BUGS docs/CONTRIBUTE docs/FAQ CHANGES
%doc docs/FEATURES docs/RESOURCES docs/TODO docs/THANKS docs/examples docs/INTERNALS


%changelog
* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.15.4
- rebuild against new openssl
- spec cleanups

* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.15.4
- 7.15.4
- add -doc subpackage
- rebuild with gcc4

* Tue Mar 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.15.3
- 7.15.3: many upstream bugfixes
- fix x86_64 build (re: oden)
- don't skip test 241 anymore
- drop P3, P4; merged upstream
- drop unapplied P2
- include the gpg sig

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.14.1
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.14.1
- Obfuscate email addresses and new tagging

* Wed Dec 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.14.1-2avx
- P3: fix for CVE-2005-3185
- P4: fix for CVE-2005-4077
- uncompress patches

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.14.1-1avx
- 7.14.1
- drop P2 and remove the special test case for test 517 on x86_64; works ok now
- force -O0 on CFLAGS otherwise the executables segfault (rgarciasuarez)
- drop P3; fixed upstream

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.13.0-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.13.0-2avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.13.0-1avx
- 7.13.0
- P2: 64bit fixes in the testsuite for curl_getdate() with 64bit
  time_t (gbeauchesne)
- P3: fix for CAN-2005-0490

* Wed Dec 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.12.3-1avx
- 7.12.3
- remove P0
- skip new test #241 on both archs
- skip tests 23 118 119 125 145 201 205 223 517 on x86_64

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.12.1-1avx
- 7.12.1
- remove fpons' "dynamic patch"
- set %%__libtoolize to /bin/true

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.11.1-2avx
- Annvix build

* Sat Apr 24 2004 Vincent Danen <vdanen@opensls.org> 7.11.1-1sls
- 7.11.1
- drop P2; applied upstream
- get rid of %%real_version macro, we'll never ship anything other than a
  release
- own %%{_includedir}/curl

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 7.10.7-4sls
- minor spec cleanups

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 7.10.7-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
