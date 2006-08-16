#
# spec file for package bison
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		bison
%define version 	2.1
%define release 	%_revrel

Summary:	A GNU general-purpose parser generator
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/bison/bison.html
Source:		http://alpha.gnu.org/gnu/bison/%{name}-%{version}.tar.bz2
Patch0:		bison-1.32-extfix.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	m4
Requires(post):	info-install
Requires(preun): info-install


%description
Bison is a general purpose parser generator which converts a grammar
description for an LALR context-free grammar into a C program to parse
that grammar.  Bison can be used to develop a wide range of language
parsers, from ones used in simple desk calculators to complex programming
languages.  Bison is upwardly compatible with Yacc, so any correctly
written Yacc grammar should work with Bison without any changes.  If
you know Yacc, you shouldn't have any trouble using Bison (but you do need
to be very proficient in C programming to be able to use Bison).  Many
programs use Bison as part of their build process. Bison is only needed
on systems that are used for development.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .extfix


%build
%configure2_5x
%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mv %{buildroot}%{_bindir}/yacc %{buildroot}%{_bindir}/yacc.bison

# Remove unpackaged files
rm -f %{buildroot}%{_libdir}/liby.a

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info bison.info


%preun
%_remove_install_info bison.info


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_datadir}/bison
%{_datadir}/bison/*
%{_infodir}/bison.info*
%{_datadir}/aclocal

%files doc
%defattr(-,root,root)
%doc COPYING ChangeLog NEWS README


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1
- spec cleanups
- remove locales

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1
- 2.1
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0-1avx
- 2.0
- new-style requires
- fix url
- drop P1; fixed upstream
- own %%{_datadir}/bison

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.875-9avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.875-8avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.875-7avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> - 1.875-6avx
- Annvix build
- require packages not files
- remove Prefix

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> - 1.875-5sls
- minor spec cleanups

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> - 1.875-4sls
- OpenSLS build
- tidy spec
