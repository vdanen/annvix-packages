#
# spec file for package bdflush
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		bdflush
%define version 	1.5
%define release 	%_revrel

Summary:	The process which starts the flushing of dirty buffers back to disk
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Kernel and hardware
URL:		ftp://tsx-11.mit.edu/pub/linux/sources/system/v1.2
Source:		ftp://tsx-11.mit.edu/pub/linux/sources/system/v1.2/bdflush-1.5.tar.bz2
Patch0:		bdflush-1.5-axp.patch
Patch1:		bdflush-1.5-glibc.patch
Patch2:		bdflush-1.5-no-bdflush.patch
Patch3:		bdflush-1.5-limit.patch
Patch4:		bdflush-1.5_include_errno.patch

Buildroot:	%{_buildroot}/%{name}-%{version}

Obsoletes:	bdflush-lowmem
Provides:	bdflush-lowmem

%description
The bdflush process starts the kernel daemon which flushes dirty
buffers back to disk (i.e., writes all unwritten data to disk).
This helps to prevent the buffers from growing too stale.

Bdflush is a basic system process that must run for your system
to operate properly.


%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .glibc
%patch2 -p1 -b .no-bdflush
%patch3 -p1 -b .limit
%patch4 -p1 -b .errno

perl -p -i -e "s/-Wall -O2/%{optflags}/" Makefile


%build
%make bdflush


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{/sbin,%{_mandir}/man8}

install -m 0755 bdflush %{buildroot}/sbin/update
install -m 0644 bdflush.8 %{buildroot}/%{_mandir}/man8/update.8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/update
%{_mandir}/man8/update.8*

%changelog
* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5-29avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5-28avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.5-27avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.5-26sls
- minor spec cleanups
- since the binary is named update, not bdflush, don't have a manpage named
  bdflush

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.5-25sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
