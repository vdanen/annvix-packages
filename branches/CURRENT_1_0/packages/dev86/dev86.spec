%define name	dev86
%define version	0.16.3
%define release	3sls

Summary:	A real mode 80x86 assembler and linker.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.cix.co.uk/~mayday/
Source:		http://www.cix.co.uk/~mayday/%name-%version.tar.bz2
Patch0:		Dev86src-0.15.5-noroot.patch.bz2
Patch1:		Dev86src-0.14-nobcc.patch.bz2
Patch2:		dev86-0.16.3-bccpath.patch.bz2
Patch3:		Dev86src-0.15-mandir.patch.bz2
Patch4:		Dev86src-0.15.5-badlinks.patch.bz2
Patch5:		dev86-0.16.3-missing-header.patch.bz2

BuildRoot:	%_tmppath/dev86/
ExclusiveArch:	%ix86

Obsoletes:	bin86
Provides:	bin86

%description
The dev86 package provides an assembler and linker for real mode 80x86
instructions. You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.

You should install dev86 if you intend to build programs that run in real
mode from their source code.

%package devel
Summary:	A development files for dev86
Group:		Development/Other
Requires:	%name = %version

%description devel
The dev86 package provides an assembler and linker for real mode 80x86
instructions. You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.

The dev86-devel package provides C headers need to use bcc, the C
compiler for real mode x86.

You should install dev86 if you intend to build programs that run in real
mode from their source code.

Note that you don't need dev86-devel package in order to build
a kernel.


%prep
%setup -q
%patch0 -b .oot -p1
%patch1 -b .djb -p1
%patch2 -b .bccpaths -p1
%patch3 -b .mandir -p1
%patch4 -b .fix -p1
%patch5 -p1 -b .errno

mkdir -p lib/bcc
ln -s ../../include lib/bcc/include

%build
make <<!FooBar!
5
quit
!FooBar!

%install
rm -rf $RPM_BUILD_ROOT

make DIST=$RPM_BUILD_ROOT MANDIR=$RPM_BUILD_ROOT/%_mandir install

install -m 755 -s $RPM_BUILD_ROOT/lib/elksemu $RPM_BUILD_ROOT%_bindir
rm -rf $RPM_BUILD_ROOT/lib/

pushd $RPM_BUILD_ROOT%_bindir
rm -f nm86 size86
ln objdump86 nm86
ln objdump86 size86
popd

# %doc --parents would be overkill
for i in elksemu unproto bin86 copt dis88 bootblocks; do
	ln -f $i/README README.$i
done
ln -f bin86/README-0.4 README.bin86-0.4

# move header files out of %{_includedir} and into %{_libdir}/bcc/include
mv $RPM_BUILD_ROOT%_includedir $RPM_BUILD_ROOT%_libdir/bcc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Changes Contributors COPYING MAGIC README*  
%dir %_libdir/bcc
%dir %_libdir/bcc/i86
%dir %_libdir/bcc/i386
%_bindir/*
%_libdir/bcc/bcc-cc1
%_libdir/bcc/copt
%_libdir/bcc/unproto
%_libdir/bcc/i86/crt*
%_libdir/bcc/i386/crt*
%_libdir/bcc/i86/rules*
%_libdir/liberror.txt
%_mandir/man1/*

%files devel
%defattr(-,root,root)
%doc README
%dir %_libdir/bcc/include
%_libdir/bcc/include/*
%_libdir/bcc/i86/lib*
%_libdir/bcc/i386/lib*

%changelog
* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 0.16.3-3sls
- OpenSLS build
- tidy spec

* Thu Jul 24 2003 Götz Waschk <waschk@linux-mandrake.com> 0.16.3-2mdk
- small patch to make it compile with the current gcc

* Wed Nov 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.16.3-1mdk
- new release
- fix build
- fix %%doc overwriting README

* Tue Mar 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.15.5-3mdk
- add Url
- rpmlint cleanups

* Fri Sep 28 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.15.5-2mdk
- Provides: bin86 as well.

* Sat May 26 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.15.5-1mdk
- Merge rh patches.
- 0.15.5.

* Tue Nov 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.15.1-2mdk
- Make almost rpmlint happy.

* Thu Sep 14 2000 Francis Galiegue <fg@mandrakesoft.com> 0.15.1-1mdk
- Use links, not symlinks!
- 0.15.1
- include ar86 (why wasn't it in before?)

* Tue Aug 08 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.15.0-3mdk
- split out -devel package (needed only for elks developpers ...)
- make rpmlint happier
- use macros ...

* Wed Jul 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.15.0-2mdk
- BM.

* Wed Jun 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.15.0-1mdk
- First mandrake version from rh package.
