#
# spec file for package symlinks
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	revision	$Rev$
%define	name		symlinks
%define	version		1.2
%define release		%_revrel

Summary:	A utility which maintains a system's symbolic links
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		File tools
License:	BSD-style
URL:		http://www.ibiblio.org/pub/Linux/utils/file/
Source0:	ftp://sunsite.unc.edu/pub/Linux/utils/file/%{name}-%{version}.tar.bz2
Patch0:		symlinks-1.2-mdk-noroot.patch
Patch1:		symlinks-1.2-mdk-static.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glibc-static-devel

%description
The symlinks utility performs maintenance on symbolic links.  Symlinks
checks for symlink problems, including dangling symlinks which point to
nonexistent files.  Symlinks can also automatically convert absolute
symlinks to relative symlinks.


%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .static


%build
%make CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -s -m 0755 %{name} -D %{buildroot}%{_bindir}/%{name}
install -m 0644 %{name}.8 -D %{buildroot}%{_mandir}/man8/%{name}.8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*


%changelog
* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- rebuild

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- rebuild with gcc4
- pass %%optflags directly to make rather than mess with the Makefile

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2-21avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2-20avx
- rebuild for new gcc
- P1: fix static build (gbeauchesne)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2-19avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2-18avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.2-17sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 1.2-16sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
