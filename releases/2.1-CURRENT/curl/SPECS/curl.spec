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
%define version 	7.17.0
%define release		%_revrel

%define major		4
%define libname 	%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

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
BuildRequires:	chrpath

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

%description  -n %{libname}
libcurl is a library of functions for sending and receiving files through 
various protocols, including http and ftp.


%package -n %{devname}
Summary:	Header files and static libraries for libcurl
Group:		Networking/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 3 -d
Obsoletes:	%mklibname %{name} 4 -d

%description -n %{devname}
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
%configure2_5x \
    --with-ssl \
    --with-zlib \
    --with-random
%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

chrpath -d %{buildroot}%{_bindir}/curl
chrpath -d %{buildroot}%{_libdir}/*.so*

# we can't nuke some files in docs/examples because the tests want them
cp -av docs/examples examples
rm -rf examples/{.libs,.deps,*.o}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/curl
%dir %{_datadir}/curl
%{_datadir}/curl/*
%{_mandir}/man1/curl.1*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%defattr(-,root,root)
%{_bindir}/curl-config
%{_libdir}/libcurl.so
%dir %{_includedir}/curl
%{_includedir}/curl/*
%{_libdir}/libcurl*a
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc docs/BUGS docs/KNOWN_BUGS docs/CONTRIBUTE docs/FAQ CHANGES
%doc docs/FEATURES docs/RESOURCES docs/TODO docs/THANKS examples docs/INTERNALS


%changelog
* Sun Sep 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 7.17.0
- 7.17.0
- implement devel naming policy
- implement library provides policy

* Sat Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.16.0
- 7.16.0
- library major is 4
- put the tests in %%check
- adjust some provides/obsoletes

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
