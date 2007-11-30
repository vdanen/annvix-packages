#
# spec file for package dev86
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		dev86
%define version		0.16.17
%define release		%_revrel

%define bccdir		%{_prefix}/lib/bcc

Summary:	A real mode 80x86 assembler and linker
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://homepage.ntlworld.com/robert.debath/dev86/
Source:		http://homepage.ntlworld.com/robert.debath/dev86/Dev86src-%{version}.tar.gz
Patch0:		dev86-0.16.17-x86_64-no-elksemu.patch
Patch5:		dev86-0.16.3-missing-header.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
ExclusiveArch:	%{ix86} ppc x86_64

Obsoletes:	bin86
Provides:	bin86

%description
The dev86 package provides an assembler and linker for real mode 80x86
instructions. You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.


%package devel
Summary:	Development files for dev86
Group:		Development/Other
Requires:	%{name} = %{version}

%description devel
The dev86 package provides an assembler and linker for real mode 80x86
instructions. You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.

The dev86-devel package provides C headers need to use bcc, the C
compiler for real mode x86.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .x86_64-no-elksemu
%patch5 -p1 -b .errno

mkdir -p lib/bcc
ln -s ../../include lib/bcc/include


%build
make <<!FooBar!
5
quit
!FooBar!


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make DIST=%{buildroot} MANDIR=%{_mandir} install install-man

pushd %{buildroot}%{_bindir}
    rm -f nm86 size86
    ln objdump86 nm86
    ln objdump86 size86
popd

# %doc --parents would be overkill
for i in elksemu unproto bin86 copt dis88 bootblocks; do
    ln -f $i/README README.$i
done
ln -f bin86/README-0.4 README-0.4.bin86
ln -f bin86/ChangeLog ChangeLog.bin86


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{bccdir}
%{_bindir}/*
%dir %{bccdir}
%{bccdir}/*
%{_mandir}/man1/*
%exclude %{bccdir}/i386/lib*

%files devel
%defattr(-,root,root)
%dir %{bccdir}/include
%{bccdir}/include/*
%{bccdir}/i386/lib*

%files doc
%defattr(-,root,root)
%doc Changes Contributors COPYING MAGIC README*  


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.16.17
- 0.16.17
- drop P6; merged upstream
- P1: allow it to build on x86_64 too

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.16.16
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.16.16
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.16.16
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.16.16-1avx
- 0.16.16
- P6: fix invalid memory allocation in bcc.c:build_prefix () (from fedora)
- drop P0-P4

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.16.3-7avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.16.3-6avx
- rebuild

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.16.3-5avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 0.16.3-4sls
- minor spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 0.16.3-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
