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

Buildroot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	libxml2-devel
BuildRequires:	libxmlrpc-devel
BuildRequires:	pkgconfig
BuildRequires:	krb5-devel
BuildRequires:	multiarch-utils >= 1.0.3

Requires:	openssl >= 0.9.7
Provides:	libneon
Provides:	neon

%description
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.

%package -n %{libname}
Summary:	An HTTP and WebDAV client library, with a C interface
Group:		System/Libraries
Provides:	libneon
Provides:	neon

%description -n %{libname}
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.

%package -n %{libname}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	libneon-devel = %{version}
Provides:	neon-devel = %{version}

%description -n	%{libname}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.


%package -n %{libname}-static-devel
Summary:	Static %{libname} library
Group:		Development/C++
Requires:	%{libname}-devel = %{version}
Provides:	libneon-static-devel = %{version}
Provides:	neon-static-devel = %{version}

%description -n	%{libname}-static-devel
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

%post -n %{libname}-devel -p /sbin/ldconfig
%postun -n %{libname}-devel -p /sbin/ldconfig


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root,755)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root,755)
%multiarch %{multiarch_bindir}/neon-config
%{_bindir}/neon-config
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/neon.pc
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libname}-static-devel
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files doc
%defattr(-,root,root,755)
%doc doc/*.txt doc/html README.neon
%doc AUTHORS BUGS ChangeLog NEWS README THANKS TODO


%changelog
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

* Wed Aug 24 2005 Pixel <pixel@mandriva.com> 0.24.7-12mdk
- documentation for a lib is better put in the devel package
  (nb: libneon is required by rpm and is always installed)

* Sat Jun 18 2005 Oden Eriksson <oeriksson@mandriva.com> 0.24.7-11mdk
- fix deps

* Thu Jun 09 2005 Buchan Milne <bgmilne@linux-mandrake.com> 0.24.7-10mdk
- Rebuild for libkrb53-devel 1.4.1

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 0.24.7-9mdk
- fix deps and provides

* Mon May 30 2005 Oden Eriksson <oeriksson@mandriva.com> 0.24.7-8mdk
- revert the last change, i'm getting nuxified

* Mon May 30 2005 Oden Eriksson <oeriksson@mandriva.com> 0.24.7-7mdk
- fix provides yet again...

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 0.24.7-6mdk
- fix provides

* Wed May 25 2005 Oden Eriksson <oeriksson@mandriva.com> 0.24.7-5mdk
- sync with fedora (P0,P1,P2)

* Sat May 21 2005 Oden Eriksson <oeriksson@mandriva.com> 0.24.7-4mdk
- rebuild

* Thu Apr 28 2005 Oden Eriksson <oeriksson@mandriva.com> 0.24.7-3mdk
- sync changelogs with the package allready in contribs

* Thu Apr 28 2005 Oden Eriksson <oeriksson@mandriva.com> 0.24.7-2mdk
- fix naming
- fix deps

* Mon Apr 25 2005 Oden Eriksson <oeriksson@mandriva.com> 0.24.7-1mdk
- rename the package to libneon0.24

* Thu Apr 15 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.24.5-1mdk
- 0.24.5

* Sun Jul 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.23.9-2mdk
- rebuilt... (uhh, huh?)

* Sun Jul 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.23.9-1mdk
- reintroduce 0.23.9 as subversion refuses to build against 0.24

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.24.0-2mdk
- rebuild

* Sun Jun 22 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.24.0-1mdk
- 0.24.0
- added one new file

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.23.9-1mdk
- 0.23.9
- make it provide
- use macros
- misc spec file fixes

* Tue Mar 04 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.23.8-2mdk
- add Obsoletes and Provides libneon0, libneono0-devel, etc.
- Oden: either get your signature into Mandrake or don't sign the packages

* Mon Mar 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.23.8-1mdk
- use the %%mklibname macro
- rebuilt against latest buildrequires
- got rpmlint to finally shut up...

* Sat Feb 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.23.7-1mdk
- 0.23.7

* Thu Jan 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.23.5-3mdk
- build against openssl-0.9.7

* Mon Jan 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.23.5-2mdk
- build release
- misc spec file fixes

* Fri Nov 01 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.23.5-2mdk
- libifiction
- added the static-devel subpackages
- enabled shared build
- huge spec file fixes

* Fri Nov 01 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.23.5-1mdk
- new version

* Wed Jul 03 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.21.3-1mdk
- 0.21.3
- enable ssl support

* Fri Nov 30 2001 Daouda LO <daouda@mandrakesoft.com> 0.18.0-1mdk
- release 0.18.0

* Thu Oct 18 2001 Daouda LO <daouda@mandrakesoft.com> 0.15.3-2mdk
- spec cleanups
- add devel package (rpmlint compliant)

* Sun Jul  1 2001  Daouda Lo <daouda@mandrakesoft.com> 0.15.3-1mdk
- mdk first package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
