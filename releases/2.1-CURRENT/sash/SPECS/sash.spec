#
# spec file for package sash
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		sash
%define version		3.7
%define release 	%_revrel

Summary:	A statically linked shell, including some built-in basic commands
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Shells
URL:		http://www.canb.auug.org.au/~dbell/
Source0:	http://www.canb.auug.org.au/~dbell/programs/%{name}-%{version}.tar.bz2
Patch0:		sash-3.5-optflags.patch
Patch2: 	sash-3.4-losetup.patch
Patch3: 	sash-3.4-fix-loop__remove_it_when_kernel_headers_are_fixed.patch
Patch4:		sash-3.7-linux2.6-buildfix.patch
Patch5:		sash-3.6-scriptarg.patch
Patch6:		sash-pwdfunc.patch
Patch7:		sash-3.7-segfault.patch
Patch8:		sash-3.7-special-script-call-esp-for-glibc-post.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	zlib-devel
BuildRequires:	glibc-static-devel
BuildRequires:	e2fsprogs-devel

%description
Sash is a simple, standalone, statically linked shell which includes
simplified versions of built-in commands like ls, dd and gzip.  Sash
is statically linked so that it can work without shared libraries, so
it is particularly useful for recovering from certain types of system
failures.  Sash can also be used to safely upgrade to new versions of
shared libraries.


%prep
%setup -q
%patch0 -p1 -b .misc
%patch2 -p1 -b .losetup
%patch3 -p1
%patch4 -p1 -b .linux26
%patch5 -p1 -b .scriptarg
%patch6 -p1 -b .pwd
%patch7 -p1 -b .segf
%patch8 -p1 -b .scriptarg -z .pix


%build
make RPM_OPT_FLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{/sbin,%{_mandir}/man8}

install -s -m 0755 sash %{buildroot}/sbin
install -m 0644 sash.1 %{buildroot}%{_mandir}/man8/sash.8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/sash
%{_mandir}/*/*


%changelog
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.7
- rebuild against new e2fsprogs

* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.7
- rebuild against new e2fsprogs
- update the buildreqs

* Mon Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7
- rebuild against new e2fsprogs
- spec cleanups

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.7-2avx
- rebuild against new e2fsprogs-devel

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.7-1avx
- 3.7
- P4: fix build with linux 2.6 (peroyvind)
- sync with Fedora (P5, P6, P7) (peroyvind)
- P8: P5 broke --ignore-remaining args special option (pixel)
- remove grep prereq

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.5-11avx
- rebuild against new gcc

* Thu Jun 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.5-10avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.5-9avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.5-8sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 3.5-7sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
