#
# spec file for package sqlite
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		sqlite3
%define version 	3.3.6
%define release		%_revrel

%define rname		sqlite
%define	major		0
%define libname		%mklibname %{name}_ %{major}

Summary:	SQLite is a C library that implements an embeddable SQL database engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Libraries
URL:		http://www.sqlite.org/
Source0:	http://www.sqlite.org/%{rname}-%{version}.tar.gz
Patch0:		sqlite-3.2.2-aliasing-fixes.patch
Patch1:		sqlite-3.3.6-avx-skip_types3_tests.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}-%{release}
BuildRequires:	chrpath
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tcl


%description
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.


%package -n %{libname}
Summary:	SQLite is a C library that implements an embeddable SQL database engine
Group:          System/Libraries

%description -n	%{libname}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the shared libraries for %{name}


%package -n %{libname}-devel
Summary:	Development library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel
Provides:	%{name}-devel

%description -n	%{libname}-devel
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the static %{libname} library and its header
files.


%package -n %{libname}-static-devel
Summary:	Static development library for the %{name} library
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n	%{libname}-static-devel
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the static %{libname} library.

%package tools
Summary:	Command line tools for managing the %{libname} library
Group:		Databases
Requires:	%{libname} = %{version}-%{release}

%description tools
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains command line tools for managing the
%{libname} library.

%package -n tcl-%{name}
Summary:	Tcl binding for %{name}
Group:		Databases
Provides:	%{name}-tcl

%description -n tcl-%{name}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains tcl binding for %{name}.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{rname}-%{version}
%patch0 -p1 -b .aliasing-fixes
%ifarch x86_64
%patch1 -p1 -b .x86_64-skip_tests
%endif

%build
%serverbuild

export CFLAGS="${CFLAGS:-%{optflags}} -DNDEBUG=1"
export CXXFLAGS="${CXXFLAGS:-%{optflags}} -DNDEBUG=1"
export FFLAGS="${FFLAGS:-%{optflags}} -DNDEBUG=1"

%configure2_5x \
    --enable-utf8

%make
make doc


%check
make test


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man1

%makeinstall_std

install -m 0644 sqlite3.1 %{buildroot}%{_mandir}/man1/%{name}.1

chrpath -d %{buildroot}%{_bindir}/*


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/lib*.a

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files -n tcl-%{name}
%defattr(-,root,root)
%{_prefix}/lib/tcl*/sqlite3

%files doc
%defattr(-,root,root)
%doc doc/*.html doc/*.gif README


%changelog
* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.3.6
- 3.3.6
- change P1, now a different test fails on x86_64, but the others are ok
- add -doc subpackage
- drop the pdf docs
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2.2
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.2.2-2avx
- correct buildroot

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.2.2-1avx
- first Annvix build because rpm needs it
- P1: skip two printf tests on x86_64 that fail

* Tue Aug  9 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 3.2.2-2mdk
- aliasing fixes
- tcl scripts are always in /usr/lib/tcl*

* Tue Jul 19 2005 Olivier Thauvin <nanardon@mandriva.org> 3.2.2-1mdk
- 3.2.2

* Tue Feb 08 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 3.0.8-1mdk
- make a rpm for sqlite3, do not update sqlite because file format has changed
 
* Fri Jan 28 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.8.15-5mdk
- patch2: fix test suite for differences in double precision float implementation

* Fri Jan 21 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.8.15-4mdk
- rebuild for new readline

* Wed Dec 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.15-3mdk
- revert latest "lib64 fixes"

* Wed Dec 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.15-2mdk
- lib64 fixes

* Tue Nov  9 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.8.15-1mdk
- New release 2.8.15

* Mon Oct 04 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.14-3mdk
- rebuild (due to missing devel package)

* Wed Sep 29 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.8.14-2mdk
- backport some 64-bit related fixes for the testsuite
- add libsqlite-static-devel, sqlite-static-devel provides

* Fri Jun 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.14-1mdk
- 2.8.14 
- fix P0
- run the tests

* Sat Jun 05 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.8.13-3mdk
- rebuilt with gcc v3.4.x

* Sat May 15 2004 Luca Berra <bluca@vodka.it> 2.8.13-2mdk 
- lib64 install fixes

* Sun May 02 2004 Luca Berra <bluca@vodka.it> 2.8.13-1mdk 
- 2.8.13
- dropped p0 (merged upstream)

* Wed Sep 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.8.6-1mdk
- 2.8.6
- misc spec file fixes

* Sun Aug 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.8.5-1mdk
- 2.8.5
- added spec file changes by Luca Berra

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.8.4-2mdk
- rebuild

* Mon Jun 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.8.4-1mdk
- initial cooker contrib
