#
# spec file for package chrpath
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		chrpath
%define version		0.13
%define release		%_revrel

Summary: 	Dynamic library load path (rpath) alterer
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Development/Other
URL:		http://www.tux.org/pub/X-Windows/ftp.hungry.com/chrpath/
Source:		%{name}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}

%description
Chrpath allows you to modify the dynamic library load path (rpath) of
compiled programs.  Currently, only removing and modifying the rpath
is supported.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall 
rm -fr %{buildroot}%{_prefix}/doc


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr (-,root,root)
%{_bindir}/chrpath
%{_mandir}/man1/chrpath.1*

%files doc
%defattr (-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README


%changelog
* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.13
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.13
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.13
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.13-1avx
- 0.13

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-5avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-4avx
- build against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.12-3avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.12-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.12-1sls
- 0.12
- remove P0; merged upstream

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.10-6sls
- minor spec cleanups

* Mon Dec 13 2003 Vincent Danen <vdanen@opensls.org> 0.10-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
