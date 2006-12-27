#
# spec file for package byacc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		byacc
%define version		1.9
%define release		%_revrel

%define date		20040328

Summary:	A public domain Yacc parser generator
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		Development/Other
URL:		http://dickey.his.com/byacc/byacc.html
Source:		ftp://invisible-island.net/byacc/byacc.tar.bz2
Patch0:		byacc-20040328-no-recreate-unionfile.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Byacc (Berkeley Yacc) is a public domain LALR parser generator which
is used by many programs during their build process.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{date}
%patch0 -p1 -b .unionfile


%build
%configure
%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
( cd %{buildroot}%{_bindir} ; ln -s yacc byacc )
ln -s yacc.1 %{buildroot}%{_mandir}/man1/byacc.1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/yacc
%{_bindir}/byacc
%{_mandir}/man1/*

%files doc
%defattr(-,root,root)
%doc ACKNOWLEDGEMENTS NEW_FEATURES NOTES
%doc NO_WARRANTY README


%changelog
* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.9
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.9
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.9
- Obfuscate email addresses and new tagging
- Uncompress patches
- drop unapplied patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9-20avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9-19avx
- rebuild for new gcc
- use the 2004-03-28 tarball from Thomas Dickey (of ncurses) which
  contains a lot of fixes and enhancements

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9-18avx
- bootstrap build
- force use of automake1.4 and autoconf2.5 (peroyvind)

* Fri Jun 25 2004 Vincent Danen <vdanen@opensls.org> 1.9-17avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.9-16sls
- minor spec cleanups

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 1.9-15sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
