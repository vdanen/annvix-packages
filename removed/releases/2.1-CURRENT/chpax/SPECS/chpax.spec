#
# spec file for package chpax
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		chpax
%define version		0.7
%define release		%_revrel

Summary:	Tool that allows PaX flags to be modified on a per-binary basis
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Configuration
URL:		http://pax.grsecurity.net/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		chpax-0.7-autotools.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7

%description
A tool that allows PaX flags to be modified on a per-binary basis. PaX is part
of common security-enhancing kernel patches, like GrSecurity. Your system needs
to be running an appropriately patched kernel, like the one provided by the
kernel-secure package, for this program to have any effect.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .autotools
chmod 0644 README


%build 
aclocal-1.7
autoheader-2.5x
autoconf-2.5x
automake-1.7 --foreign -a
%configure 
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root) 
%{_mandir}/man1/chpax.1*
%{_sbindir}/chpax

%files doc
%defattr(-,root,root) 
%doc README ChangeLog


%changelog
* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.7
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.7
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.7
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.7
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix perms on README
 
* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.7-1avx
- 0.7

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.5-5avx
- rebuild

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.5-4avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.5-3sls
- minor spec cleanups

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 0.5-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
