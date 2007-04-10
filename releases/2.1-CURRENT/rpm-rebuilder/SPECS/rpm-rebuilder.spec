#
# spec file for package rpm-rebuilder
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rpm-rebuilder
%define version		0.27
%define release		%_revrel
%define rbuver		0.6.1

Summary:	Tools to build/check distributions
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://www.mandrivalinux.com/
Source0:	%{name}-%{version}.tar.bz2
Source1:	rpmbuildupdate-%{rbuver}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	rpmlint
Requires:	strace
Requires:	rpm-build
Requires:	diffutils

%description
The rpm-rebuilder package contains a set of tools written in bourne
shell, python and perl to rebuild/check large sets of rpm source packages.

check-distrib: checks if a set of source and binary rpms are in sync.

rpm-rebuilder: build a set of rpms from a set of srpms.

compute-build-requires: trace an rpm build command to find the BuildRequires
it needs.

compute-compile-order: from the sets of binary and sources rpms, find the order
in which the source rpms must be recompiled.

rpmbuildupdate: download and rebuild the new version of a given srpm. 


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 1


%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install

install -m 0755 rpmbuildupdate-%{rbuver}/rpmbuildupdate %{buildroot}%{_bindir}/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%_datadir/rpm-rebuilder

%files doc
%defattr(-,root,root)
%doc AUTHORS README README.CVS ChangeLog


%changelog
* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.27
- 0.27
- the 0.26 release removed rpmbuildupdate to it's own package, but
  I don't see the point so include it here (0.6.1)
- add -doc subpackage

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.25
- fix group

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.25
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.25
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.25-1avx
- 0.25
- fix perms on spec file
- Requires: diffutils

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.22-1avx
- 0.22

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.21-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.21-2avx
- bootstrap build

* Tue Mar 01 2005 Vincent Danen <vdanen@mandrakesoft.com> 0.21-1avx
- first Annvix build
- don't include bash completion stuff

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
