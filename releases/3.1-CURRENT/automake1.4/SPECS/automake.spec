#
# spec file for package automake1.4
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		%{amname}%{amversion}
%define version 	1.4p6
%define release 	%_revrel

%define amname		automake
%define amversion	1.4
%define patchlevel	p6

%define docheck		1
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://sourceware.cygnus.com/automake
Source:		ftp://ftp.gnu.org/gnu/automake/%{amname}-%{amversion}-%{patchlevel}.tar.bz2
Patch0:		automake-1.4p6-infofiles.patch
Patch1:		automake-1.4-p6-stdc-headers.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl

Requires(post):	info-install
Requires(preun): info-install
Requires:	perl
Conflicts:	automake1.5
Obsoletes:	automake <= 1.4-0.p6.26avx

%description
Automake is a tool for automatically generating Makefiles compliant with the
GNU Coding Standards.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{amname}-%{amversion}-%{patchlevel}
%patch0 -p1 -b .parallel
%patch1 -p1 -b .gcc3.4


%build
%configure
make
perl -pi -e 's/\berror\.test\b//' tests/Makefile


%check
%if %{docheck}
make check  # VERBOSE=1
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

install -D -m 0644 %{name}.info %{buildroot}%{_infodir}/%{name}.info

rm -f %{buildroot}%{_bindir}/{automake,aclocal}
mkdir -p %{buildroot}%{_datadir}/aclocal


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info automake.info
update-alternatives --remove automake %{_bindir}/automake-%{amversion}


%preun
%_remove_install_info automake.info


%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*-1.4
%{_infodir}/%{name}*
%dir %{_datadir}/aclocal

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO


%changelog
* Sat Oct 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.4p6
- rebuild

* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4p6
- add -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4p6
- Clean rebuild

* Sat Dec 31 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4p6
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4p6-31avx
- normalize the release tag

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4-0.p6.30avx
- this package is no longer an alternative for current "automake" (cjw)

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4-0.p6.29avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4-0.p6.28avx
- bootstrap build

* Fri Sep 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4-0.p6.27avx
- this is now automake1.4
- add --without-check option to disable 'make check' (abel)
- P0: use versioned name in info page nodes (abel)
- P1: gcc no longer acceps K&R style prototypes (unapplied until we move to gcc 3.4)
- note: mdk dropped alternative priority of this but we're not going to because we
  want 1.4 to remain the default

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4-0.p6.26avx
- Annvix build

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 1.4-0.p6.25sls
- remove %%{prefix}
- more spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 1.4-0.p6.24sls
- OpenSLS build
- tidy spec
- change naming convention to make more sense regarding patchlevel
- Epoch: 1 due to release tag change

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
