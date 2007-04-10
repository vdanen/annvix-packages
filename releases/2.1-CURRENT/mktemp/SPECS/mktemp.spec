#
# spec file for package mktemp
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mktemp
%define version		1.6
%define release		%_revrel

Summary:	A small utility for safely making /tmp files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		File Tools
URL:		ftp://ftp.openbsd.org/pub/OpenBSD/src/usr.bin/mktemp/
Source:		mktemp-%{version}.tar.bz2
Patch0:		mktemp-1.6-avx-makefile.patch
Patch1:		mktemp-1.6-avx-linux.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The mktemp utility takes a given file name template and overwrites
a portion of it to create a unique file name.  This allows shell
scripts and other programs to safely create and use /tmp files.


%prep
%setup -q
%patch0 -p0 -b .makefile
%patch1 -p0 -b .linux


%build
CFLAGS="%{optflags}" make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
perl -pi -e "s!/usr/man!%{_mandir}!g" Makefile
%makeinstall ROOT="%{buildroot}"


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/bin/mktemp
%{_mandir}/man1/mktemp.1*


%changelog
* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-2avx
- bootstrap build

* Thu Sep 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.6-1avx
- OpenBSD CVS rev 1.13 (we'll call this 1.6)
- rework patches and drop those no longer needed

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.5-14avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.5-13sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 1.5-12sls
- OpenSLS build
- tidy spec
- pass CFLAGS on to make

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
