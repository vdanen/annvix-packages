#
# spec file for package pkgconfig
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		pkgconfig
%define version		0.20
%define release		%_revrel

Summary:	Pkgconfig helps make building packages easier
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://pkgconfig.freedesktop.org/
Source:		http://pkgconfig.freedesktop.org/releases/pkg-config-%{version}.tar.gz
Patch1:		pkg-config-0.19-biarch.patch
# (fc) 0.19-1mdk add --print-provides/--print-requires (Fedora)
Patch2:		pkgconfig-0.15.0-reqprov.patch
# (gb) 0.19-2mdk 64-bit fixes, though that code is not used, AFAICS
Patch4:		pkg-config-0.19-64bit-fixes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
pkgconfig is a program that helps gather information to make things easier
when compiling a program for those programs which support it.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n pkg-config-%{version}
%patch1 -p1 -b .biarch
%patch2 -p1 -b .reqprov
%patch4 -p1 -b .64bit-fixes

#needed by patch1
autoheader
autoconf


%build
%{?__cputoolize: %{__cputoolize} -c glib-1.2.8}
%configure2_5x \
    --enable-indirect-deps=yes
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_libdir}/pkgconfig
%if "%{_lib}" != "lib"
mkdir -p %{buildroot}%{_prefix}/lib/pkgconfig
ln -s ../../lib/pkgconfig %{buildroot}%{_libdir}/pkgconfig/32
%endif

mkdir -p %{buildroot}%{_datadir}/pkgconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/pkg-config
%{_libdir}/pkgconfig
%{_datadir}/pkgconfig
%if "%{_lib}" != "lib"
%{_prefix}/lib/pkgconfig
%{_libdir}/pkgconfig/32
%endif
%{_datadir}/aclocal/*
%{_mandir}/man1/*

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL README ChangeLog


%changelog
* Thu Jun 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.20
- 0.20
- drop P3; no longer required
- fix urls
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.19
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.19
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.15.0-9avx
- 0.19
- include some 64bit fixes (gbeauchesne)
- remove make check since it doesn't pass upstream (fcrozat)
- P1: biarch pkgconfig support (gbeauchesne)
- P2: add --print-provides/--print-requires (from Fedora)
- P3: fix overflow when using gcc4 (from Fedora)
- create %%{_datadir}/pkgconfig for arch independant .pc files (fcrozat)


* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.15.0-9avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.15.0-8avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.15.0-7avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen@opensls.org> 0.15.0-6avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.15.0-5sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 0.15.0-4sls
- OpenSLS build
- tidy spec

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.15.0-3mdk
- cputoolize since pkgconfig people don't use a single config.* script

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.15.0-2mdk
- rebuild
- don't rm -rf %{buildroot} in %%prep

* Tue Jan 21 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 0.15.0-1mdk
- Release 0.15.0

* Tue Oct 29 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.14.0-1mdk
- Release 0.14.0

* Tue Oct  8 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.13.0-1mdk
- Release 0.13

* Tue Jul 16 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.12.0-2mdk
- Costlessly make check in %%build stage

* Wed Mar 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.12.0-1mdk
- Release 0.12.0

* Mon Feb  4 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.10.0-1mdk
- Release 0.10.0

* Sat Aug 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.8.0-2mdk
- Sanity build for 8.1.

* Thu Jul 12 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.8.0-1mdk
- Release 0.8.0

* Tue Jun 12 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.7.0-1mdk
- s/Copyright/License/;

* Mon Jun 11 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.7.0-1mdk
- Release 0.7
- new URL
- Add missing files

* Sun Apr 29 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.5.0-3mdk
- Take out some snailtalk favored pkgconfig aka remove the buildroot
  from the binary (DindinX).
  
* Fri Apr 20 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.5.0-2mdk
- Change the description (Abel Cheung), yes it's terribly misleading.

* Thu Apr 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.5.0-1mdk
- Made an RPM for the purposes of compiling glib2.

