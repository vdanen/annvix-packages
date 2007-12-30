#
# spec file for package etcskel
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		etcskel
%define version 	1.63
%define release 	%_revrel

Summary:	Annvix default files for new users' home directories
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Base
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	bash

%description
The etcskel package is part of the basic Annvix system.

Etcskel provides the /etc/skel directory's files. These files are then placed
in every new user's home directory when new accounts are created.


%prep
%setup -q


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install RPM_BUILD_ROOT=%{buildroot}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) /etc/skel


%changelog
* Thu Nov 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.63
- rebuild

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.63
- add -doc subpackage
- make all of /etc/skel not replaceable

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.63
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.63
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.63-20avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.63-19avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.63-18avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 1.63-17sls
- DIRM: /etc/skel

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 1.63-17sls
- more OpenSLS specific

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 1.63-16sls
- OpenSLS build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
