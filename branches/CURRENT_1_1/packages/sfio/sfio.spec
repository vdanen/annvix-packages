%define name	sfio
%define version	1999
%define release	12avx

Summary:	A Safe/Fast I/O Library
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License:	AT&T Labs
URL:		http://www.research.att.com/sw/tools/sfio/
Source0:	sfio_1999.src.unix.tar.bz2
Source1:	sfio_1999.src.unix.README
Patch0:		sfio_1999.patch.bz2
Patch1:		sfio_1999.mdk.patch.bz2
Patch2:		sfio-1999-implicit.patch.bz2
Patch3:		sfio-1999-rettype.patch.bz2
Patch4:		sfio-1999-pic.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	ed

%description
Sfio is a library for managing I/O streams. It provides functionality
similar to that of Stdio, the ANSI C Standard I/O library, but via a
distinct interface that is more powerful, robust and efficient.

%package devel
Group:		Development/C
Summary:	Libraries, includes and other files for Safe/Fast I/O Library
Requires:	sfio = 1999

%description devel
This packages contains the libraries, include and other files
for Safe/Fast I/O Library

%prep
%setup -q 
%patch1 -p0
%patch2 -p1 -b .implicit
%patch3 -p1 -b .rettype
%patch4 -p1 -b .pic
cp -p %{SOURCE1} .

%build
export PATH=$PATH:`pwd`/bin
mkdir -p src/lib/sfio/FEATURE
mkdir -p src/lib/sfio/Stdio_b/FEATURE
make "CCFLAGS=$RPM_OPT_FLAGS -I. -I.. -Wall" -C src/lib/sfio
make -C src/lib/sfio libsfio.so install SONAME="lib%{name}.so.%{version}" CCMODE="$RPM_OPT_FLAGS -Wall"
# Since we install the headers in /usr/include/sfio we need to fix some paths
bzcat %{PATCH0} | patch -p0

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/usr/include/sfio
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
cp -a include/* $RPM_BUILD_ROOT/usr/include/sfio
cp -a man/* $RPM_BUILD_ROOT/%{_mandir}

install lib/libsfio.so $RPM_BUILD_ROOT%{_libdir}/libsfio.so.1999
install lib/*.a $RPM_BUILD_ROOT%{_libdir}/
( cd $RPM_BUILD_ROOT%{_libdir}/ ; ln -s libsfio.so.1999 libsfio.so )

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc NOTICE/* *README 
%{_libdir}/*
%{_mandir}/man*/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%changelog
* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 1999-12avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1999-11sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 1999-10sls
- OpenSLS build
- tidy spec

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1999-9mdk
- BuildRequires: ed

* Mon Jul 14 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 1999-8mdk
- rebuild

* Mon Jul 22 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 1999-7mdk
- Propagate RPM_OPT_FLAGS to PIC build via CCMODE not CFLAGS

* Mon Jul 22 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1999-6mdk
- Patch4: Correctly compile DSO with PIC
- Rpmlint fixes: hardcoded-library-path

* Mon Oct 15 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1999-5mdk
- Sanitize spec file (s/Copyright/License/)
- Patch2: Add memalign() declaration [fix sendmail crashes on IA-64]
- Patch3: Explicit return type "int"

* Thu May 24 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1999-4mdk
- Use RPM_OPT_FLAGS
- fix rpmlint warnings

* Fri Apr 06 2001 Philippe Libat <philippe@mandrakesoft.com> 1999-3mdk
- Mandrake adaptions
- shared lib, and devel package

* Mon Mar 03 1997 Hao Li <hli@wag.caltech.edu>
- initial package
