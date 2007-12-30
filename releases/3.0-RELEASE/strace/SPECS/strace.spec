#
# spec file for package strace
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		strace
%define version		4.5.16
%define release		%_revrel

Summary:	Tracks and displays system calls associated with a running process
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Development/Kernel
URL:		http://sourceforge.net/projects/strace/
Source0:	http://easynews.dl.sourceforge.net/sourceforge/strace/%{name}-%{version}.tar.bz2
Patch0:		strace-4.5.16-avx-alt-keep_status.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The strace program intercepts and records the system calls called
and received by a running process.  Strace can print a record of
each system call, its arguments and its return value.  Strace is useful
for diagnosing problems and debugging, as well as for instructional
purposes.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0 -b .keep_status

%ifarch x86_64
# we need to copy the right syscallent.h for x86_64 otherwise make dies with:
#  linux/x86_64/../syscallent.h:285: error: '__NR_exit_group' undeclared here (not in a function)
cp -f linux/x86_64/syscallent.h linux/
%endif


%build
%configure
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

# remove unpackaged files
rm -f %{buildroot}%{_bindir}/strace-graph


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/strace
%{_mandir}/man1/strace.1*

%files doc
%defattr(-,root,root)
%doc COPYRIGHT README* CREDITS INSTALL NEWS PORTING TODO


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.5.16
- 4.5.16
- rediff P3 and rename it to P0

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.5.14
- 4.5.14
- drop P1, P2: applied upstream
- drop P4, P5: no longer wanted
- drop the bogus autoreconf stuff, we don't need it
- build fix/workaround for x86_64
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.5.13
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.5.13
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.5.13-1avx
- 4.5.13
- sync with ALT/Openwall patches
- redefine %%optflags to add -Wall

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.98-6avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.98-5avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.4.98-4avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.4.98-3sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 4.4.98-2sls
- OpenSLS build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
