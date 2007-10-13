#
# spec file for package flex
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		flex
%define version		2.5.33
%define release		%_revrel

Summary:	A tool for creating scanners (text pattern recognizers)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL: 		http://flex.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/flex/%{name}-%{version}.tar.bz2
Patch0:		flex-2.5.4a-skel.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	byacc

Requires(post):	info-install
Requires(postun): info-install

%description 
The flex program generates scanners. Scanners are
programs which can recognize lexical patterns in text.

Flex takes pairs of regular expressions and C code as input and
generates a C source file as output. The output file is compiled and
linked with a library to produce an executable.

The executable searches through its input for occurrences of the
regular expressions. When a match is found, it executes the
corresponding C code.

Flex was designed to work with both Yacc and Bison, and is used by
many programs as part of their build process.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1
# Force regeneration of skel.c with Patch2 changes
rm -f skel.c
# Force regeneration of configure script with --libdir= support
autoconf


%build
%configure
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

cd %{buildroot}%{_bindir}
ln -sf flex lex

cd %{buildroot}%{_mandir}/man1
ln -s flex.1 lex.1
ln -s flex.1 flex++.1


%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info flex.info

%postun
%_remove_install_info flex.info


%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/libfl.a
%{_includedir}/FlexLexer.h
%{_infodir}/*

%files doc
%defattr(-,root,root,755)
%doc COPYING NEWS README


%changelog
* Fri Oct 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5.33
- 2.5.33
- drop P1, P2: no longer required
- updated url
- install/uninstall info pages

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4a
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4a
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4a
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4a-27avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4a-26avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4a-25avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4a-24avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.5.4a-23sls
- minor spec cleanups

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 2.5.4a-22sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
