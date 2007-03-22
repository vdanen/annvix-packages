#
# spec file for package file
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		file
%define version		4.20
%define release		%_revrel

%define major		1
%define libname		%mklibname magic %{major}

Summary:	A utility for determining file types
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD 
Group:		File tools
URL:		ftp://ftp.astron.com/pub/file/
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
Source1:	magic.mime

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl
BuildRequires:	libtool
BuildRequires:	autoconf
BuildRequires:	zlib-devel

Requires:	%{libname} = %{version}

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.


%package -n %{libname}
Summary:	Shared library for handling magic files
Group:		System/Libraries

%description -n %{libname}
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on.


%package -n %{libname}-devel
Summary:	Development files to build applications that handle magic files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libmagic-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 


%package -n %{libname}-static-devel
Summary:	Static library to build applications that handle magic files
Group:		Development/C
Requires:	%{libname}-devel = %{version}

%description -n %{libname}-static-devel
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"

%configure2_5x \
    --datadir=%{_datadir}/misc
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

cat %{_sourcedir}/magic.mime > %{buildroot}%{_datadir}/misc/magic.mime
ln -sf %{name}/magic %{buildroot}%{_datadir}/misc/magic

install -m 0644 src/file.h %{buildroot}%{_includedir}/ 


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/file
%{_datadir}/misc/*
%{_mandir}/man1/file.1*
%{_mandir}/man4/magic.4*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/file.h
%{_includedir}/magic.h
%{_mandir}/man3/libmagic.3*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

%files doc
%defattr(-,root,root)
%doc README MAINT LEGAL.NOTICE ChangeLog 


%changelog
* Thu Mar 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.20
- 4.20: fixes CVE-2007-1536

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.17
- 4.17
- drop P2
- use the real source
- use %%_sourcdir/file instead of %%{SOURCEx}
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.15
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.15
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.15-1avx
- 4.15
- drop upstream P0

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.14-1avx
- 4.14

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.10-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.10-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.10-2avx
- bootstrap build

* Sun Sep 12 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.10-1avx
- 4.10
- remove P3: similar fix upstream
- spec cleanups

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.03-5avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 4.03-4sls
- minor spec cleanups

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 4.03-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
