#
# spec file for package which
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		which
%define version		2.16
%define release		%_revrel

Summary:	Displays where a particular program in your path is located
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		ftp://ftp.gnu.org/gnu/which/
Source:		ftp://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.bz2
Patch0:		which-2.6.jbj.patch
Patch1:		which-2.12-fixinfo.patch
Patch2:		which-2.16-afs.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires(post):	info-install
Requires(preun): info-install

%description
The which command shows the full pathname of a specified program, if
the specified program is in your PATH.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{_infodir}/dir


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%files
%defattr(-,root,root)
%{_bindir}/which
%{_mandir}/man1/which.1*
%{_infodir}/*

%files doc
%defattr(-,root,root)
%doc README* AUTHORS EXAMPLES INSTALL NEWS


%changelog
* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.16
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.16
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.16
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16-6avx
- minor spec cleanups

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16-5avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16-4avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16-3avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.16-2avx
- require info-install, not the file
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.16-1sls
- 2.16
- rediff and simplify P3 (tvignaud)

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 2.14-7sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 2.14-6sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
