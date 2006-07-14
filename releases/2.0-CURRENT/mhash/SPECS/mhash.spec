#
# spec file for package mhash
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mhash
%define version		0.9.7.1
%define release		%_revrel

%define major		2
%define libname 	%mklibname %{name} %{major}

Summary:	Thread-safe hash library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://mhash.sourceforge.net/
Source:		http://umn.dl.sourceforge.net/sourceforge/mhash/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Mhash is a thread-safe hash library, implemented in C, and provides a
uniform interface to a large number of hash algorithms (MD5, SHA-1,
HAVAL, RIPEMD128, RIPEMD160, TIGER, GOST). These algorithms can be 
used to compute checksums, message digests, and other signatures.
The HMAC support implements the basics for message authentication, 
following RFC 2104.


%package -n %{libname}
Summary:	Thread-safe hash library
Group:		System/Libraries

%description -n	%{libname}
Mhash is a thread-safe hash library, implemented in C, and provides a
uniform interface to a large number of hash algorithms (MD5, SHA-1,
HAVAL, RIPEMD128, RIPEMD160, TIGER, GOST). These algorithms can be
used to compute checksums, message digests, and other signatures.
The HMAC support implements the basics for message authentication,
following RFC 2104.


%package -n %{libname}-devel
Summary:	Header files and libraries for developing apps which will use mhash
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libmhash-devel = %{version}
Provides:	mhash-devel = %{version}

%description -n	%{libname}-devel
The mhash-devel package contains the header files and libraries needed
to develop programs that use the mhash library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x \
    --enable-static \
    --enable-shared

%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

# install all headers
install -m 0644 include/*.h %{buildroot}%{_includedir}/
install -m 0644 include/mutils/*.h %{buildroot}%{_includedir}/mutils/

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{libname}-devel
%defattr(-, root, root)
%{_mandir}/man3/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*.h
%dir %{_includedir}/mutils
%{_includedir}/mutils/*.h

%files doc
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README TODO doc/*.txt doc/*.c doc/skid2* 

%changelog
* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7.1
- 0.9.7.1
- spec cleanups
- drop buildreq's on autoconf/automake
- fix source url
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.2
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.2-1avx
- 0.9.2
- run the test suite
- drop html docs
- BuildRequires: automake1.7, autoconf2.5

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8.18-9avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8.18-8avx
- rebuild against new gcc

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8.18-7avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.8.18-6avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 0.8.18-5sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 0.8.18-4sls
- OpenSLS build
- tidy spec

* Mon Nov 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.18-3mdk
- new url
- misc spec file fixes

* Thu Jul 10 2003 Götz Waschk <waschk@linux-mandrake.com> 0.8.18-2mdk
- mklibname macro

* Wed Jun 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.18-1mdk
- 0.8.18
- use the %%configure2_5x macro

* Wed Jan 29 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.8.17-3mdk
- rebuild

* Sun Jan 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.17-2mdk
- build release

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.17-1mdk
- new version

* Sat Jun  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.16-1mdk
- new version
- misc spec file fixes

* Sun May 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.14-2mdk
- rebuilt with gcc3.1

* Thu Apr 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.14-1mdk
- new version
- misc spec file fixes

* Sun Dec 23 2001 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.13-1mdk
- new version
- misc spec file fixes

* Mon Sep 10 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.8.10-1mdk
- updated by Thomas Leclerc <leclerc@linux-mandrake.com> :
	- 0.8.10
	- forbid forcing libtoolize
	- complete doc, move it to devel

* Wed Jul 18 2001 Thomas Leclerc <leclerc@linux-mandrake.com> 0.8.9-1mdk
- 0.8.9 (0.8.10 is out, but libtool conflicts)

* Mon Jan 22 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.8.6-1mdk
- updated to 0.8.6
- apply library policy

* Mon Sep 11 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.8.2-3mdk
- clean spec
- BM

* Wed Jul 19 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.8.2-1mdk
- macrozifications

* Mon Jul 17 2000 Max Heijndijk <cchq@wanadoo.nl> 0.8.2-1
- Updated to 0.8.2
- Fixed %%doc (missing files)

* Sat Jun 10 2000 Kyle Wheeler <memoryhole@penguinpowered.com>
- Updated for version 0.8.1

* Wed Feb 9 2000 Clinton Work <clinton@scripty.com>
- Created a new spec file for version 0.6.1
- Created both a shared library and devel packages
