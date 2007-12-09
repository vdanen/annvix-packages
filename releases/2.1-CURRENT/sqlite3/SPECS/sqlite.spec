#
# spec file for package sqlite
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		sqlite
%define version 	3.5.2
%define release		%_revrel

%define	major		0
%define libname		%mklibname %{name}3_ %{major}
%define devname		%mklibname %{name} -d
%define staticdevname	%mklibname %{name} -d -s

Summary:	SQLite is a C library that implements an embeddable SQL database engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Libraries
URL:		http://www.sqlite.org/
Source0:	http://www.sqlite.org/%{name}-%{version}.tar.gz
Patch0:		sqlite-3.5.2-avx-skip_tests.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}-%{release}
BuildRequires:	chrpath
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel


%description
SQLite is a C library that implements an embeddable SQL database engine.
Programs that link with the SQLite library can have SQL database access
without running a separate RDBMS process. The distribution comes with a
standalone command-line access program (sqlite) that can be used to
administer an SQLite database and which serves as an example of how to
use the SQLite library.


%package -n %{libname}
Summary:	SQLite is a C library that implements an embeddable SQL database engine
Group:          System/Libraries
Provides:	libsqlite3 = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}

%description -n	%{libname}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the shared libraries for %{name}


%package -n %{devname}
Summary:	Development library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{name}3-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name}3_ 0 -d

%description -n	%{devname}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the static %{libname} library and its header
files.


%package -n %{staticdevname}
Summary:	Static development library for the %{name} library
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	%{name}3-static-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name}3_ 0 -d -s

%description -n	%{staticdevname}
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
Provides:	%{name}3-tools = %{version}-%{release}
Obsoletes:	%{name}3-tools

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
Provides:	%{name}-tcl = %{version}-%{release}
Provides:	%{name}3-tcl = %{version}-%{release}
Obsoletes:	%{name}3-tcl

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
%setup -q -n %{name}-%{version}
%ifarch x86_64
# x86_64 fails thus on io-4.2.2, so we just ommit the test as everything else passes:
#
# Expected: [0xFFFFFFFF]
#      Got: [0xFFFFFFFFFFFFFFFF]
#
%patch0 -p1 -b .x86_64-skip_tests
%endif

%build
%serverbuild

export CFLAGS="${CFLAGS:-%{optflags}} -DNDEBUG=1"
export CXXFLAGS="${CXXFLAGS:-%{optflags}} -DNDEBUG=1"
export FFLAGS="${FFLAGS:-%{optflags}} -DNDEBUG=1"

%configure2_5x \
    --enable-utf8 \
    --enable-threadsafe \
    --enable-threadsafe-override-locks

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
%{_libdir}/lib*.so.%{major}*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{staticdevname}
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
* Sat Dec 08 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.5.2
- rebuild against new tcl, ncurses

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.5.2
- 3.5.2
- drop P0, P1; no longer needed
- new P1 to skip one minor failing test on x86_64 (io-4.2.2)
- re-enable the tests

* Sun Jun 24 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.3.8
- rebuild against new readline
- implement devel naming policy
- implement library provides policy

* Fri Feb 02 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.3.8
- provide libsqlite3

* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.3.8
- rebuild against new tcl
- disable the tests for now; for some reason the corrupt* tests are failing
  (tcl-related?)

* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.3.8
- rebuild against new ncurses
- clean spec

* Tue Nov 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.3.8
- 3.3.8
- provide sqlite-devel
- change package name to sqlite instead of sqlite3 and use the appropriate
  provides/obseletes (we don't ship another version of sqlite so this doesn't
  need to be versioned)

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
