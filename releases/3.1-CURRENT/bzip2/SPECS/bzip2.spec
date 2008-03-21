#
# spec file for package bzip2
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		bzip2
%define version		1.0.5
%define release		%_revrel

%define major		1
%define libname		%mklibname %{name}_ %{major}
%define devname		%mklibname %{name} -d

Summary:	Extremely powerful file compression utility
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Archiving
URL:		http://www.bzip.org/
Source:		http://www.bzip.org/%{version}/%{name}-%{version}.tar.gz
Source2:	bzme
Source3:	bzme.1
Patch0:		bzip2-1.0.4-mdv-makefile.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo
BuildRequires:	libtool

Requires:	%{libname} = %{version}
Requires:	mktemp

%description
Bzip2 compresses files using the Burrows-Wheeler block-sorting text
compression algorithm, and Huffman coding. Compression is generally
considerably better than that achieved by more conventional LZ77/LZ78-based
compressors, and approaches the performance of the PPM family of statistical
compressors.

The command-line options are deliberately very similar to those of GNU Gzip,
but they are not identical.


%package -n %{libname}
Summary:	Libraries for developing apps which will use bzip2
Group:		System/Libraries
Provides:	lib%{name}_%{major} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
Library of bzip2 functions, for developing apps which will use the
bzip2 library (aka libz2).


%package -n %{devname}
Summary:	Header files for developing apps which will use bzip2
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Obsoletes:	%mklibname %{name}_ 1 -d

%description -n %{devname}
Header files and static library of bzip2 functions, for developing apps which
will use the bzip2 library (aka libz2).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
cp %{_sourcedir}/bzme .
%patch0 -p0 -b .makefile

echo "lib = %{_lib}" >>config.in
echo "CFLAGS = %{optflags}" >>config.in


%build
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
install -m 0755 bzme %{buildroot}%{_bindir}
install -m 0755 bzgrep %{buildroot}%{_bindir}
install -m 0644 bzgrep.1 %{buildroot}%{_mandir}/man1

cat > %{buildroot}%{_bindir}/bzless <<EOF
#!/bin/sh
%{_bindir}/bunzip2 -c "\$@" | %{_bindir}/less
EOF
chmod 0755 %{buildroot}%{_bindir}/bzless
install -m 0644 %{_sourcedir}/bzme.1 %{buildroot}%{_mandir}/man1/

install -m 0644 bzlib_private.h %{buildroot}%{_includedir}/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root,755)
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root,755)
%{_libdir}/libbz2.so.*

%files -n %{devname}
%defattr(-,root,root,755)
%{_libdir}/libbz2.a
%{_libdir}/libbz2.la
%{_libdir}/libbz2.so
%{_includedir}/*.h

%files doc
%defattr(-,root,root,755)
%doc README LICENSE *.html CHANGES


%changelog
* Fri Mar 21 2008 Vincent Danen <vdanen-at-build.annvix.org> 1.0.5
- 1.0.5: fixes CVE-2008-1372

* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.4
- get rid of %%odevname

* Tue Jul 31 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.4
- 1.0.4
- drop P2: it doesn't work with large files
- drop P0, P3, P4: merged upstream
- updated P1 (now P0) from Mandriva
- implement devel naming policy
- implement library provides policy

* Fri Jun 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- versioned provides
- provide libbzip2_1 on 64bit (lafriks)

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- add -doc subpackage
- rebuild with gcc4
- BuildRequires: libtool

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- fix group

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- P4: security fix for CVE-2005-0758 (bzgrep)
- drop S1; use the bundled bzgrep instead and install the manpage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3-3avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3-2avx
- bootstrap build

* Wed May 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3-1avx
- 1.0.3 (fixes CAN-2005-1260)
- P1: mktemp support (Requires: mktemp); rediffed from Mandriva
- P2: get rid of the automake stuff (gbeauchesne)
- P3: patch to fix CAN-2005-0953
- spec cleanups
- include bzdiff and bzmore
- bzme: allow to force compression with -F option (mandriva bug #11183);
  patch from Michael Scherer (oblin)
- fix URL/source URL
- make sure bzlib_private.h still gets included

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2-19avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.0.2-18sls
- remove %%buildpdf
- minor spec cleanups

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 1.0.2-17sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
