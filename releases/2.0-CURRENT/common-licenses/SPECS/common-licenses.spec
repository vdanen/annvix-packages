#
# spec file for package common-licenses
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		common-licenses
%define version 	1.0
%define release 	%_revrel

Summary:	Contains the various common licenses uses by the distribution
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
Source0:	%{name}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

%description
Contains the various common licenses uses by the distribution. Instead of
including the COPYING file in every package, just refer to this one.


%prep
%setup -q


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}%{_datadir}
cp -a %{name} %{buildroot}%{_datadir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_datadir}/%{name}


%changelog
* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- remove pre-Annvix changelog

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0-13avx
- FSF has changed it's address
- updated GPL from http://www.gnu.org/licenses/gpl.txt
- added GNU Free Documentation License (GFDL)
- added the Apache v2 license

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0-12avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0-11avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0-10avx
- Annvix build

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.0-9sls
- minor spec cleanups

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.0-8sls
- OpenSLS build
- tidy spec
