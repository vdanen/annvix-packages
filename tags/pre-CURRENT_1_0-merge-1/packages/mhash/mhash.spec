%define name	mhash
%define version	0.8.18
%define release	3mdk

%define major 2
%define libname %mklibname %{name} %{major}

Summary:	Thread-safe hash library
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
Source:		%{name}-%{version}.tar.bz2
License:	BSD
URL:		http://mhash.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
Mhash is a thread-safe hash library, implemented in C, and provides a
uniform interface to a large number of hash algorithms (MD5, SHA-1,
HAVAL, RIPEMD128, RIPEMD160, TIGER, GOST). These algorithms can be 
used to compute checksums, message digests, and other signatures.
The HMAC support implements the basics for message authentication, 
following RFC 2104.

%package -n	%{libname}
Summary:	Thread-safe hash library
Group:		System/Libraries

%description -n	%{libname}
Mhash is a thread-safe hash library, implemented in C, and provides a
uniform interface to a large number of hash algorithms (MD5, SHA-1,
HAVAL, RIPEMD128, RIPEMD160, TIGER, GOST). These algorithms can be
used to compute checksums, message digests, and other signatures.
The HMAC support implements the basics for message authentication,
following RFC 2104.

%package -n	%{libname}-devel
Summary:	Header files and libraries for developing apps which will use mhash
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libmhash-devel

%description -n	%{libname}-devel
The mhash-devel package contains the header files and libraries needed
to develop programs that use the mhash library.

Install the mhash-devel package if you want to develop applications that
will use the mhash library.

%prep

%setup -q

%build

%configure2_5x \
    --enable-static \
    --enable-shared

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README TODO doc/*.txt doc/*.html doc/*.c doc/skid2* 
%{_mandir}/man3/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Mon Nov 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.18-3mdk
- new url
- misc spec file fixes

* Thu Jul 10 2003 G�tz Waschk <waschk@linux-mandrake.com> 0.8.18-2mdk
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
- Fixed %doc (missing files)

* Sat Jun 10 2000 Kyle Wheeler <memoryhole@penguinpowered.com>
- Updated for version 0.8.1

* Wed Feb 9 2000 Clinton Work <clinton@scripty.com>
- Created a new spec file for version 0.6.1
- Created both a shared library and devel packages
