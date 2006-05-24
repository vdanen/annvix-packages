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
%{_datadir}/locale/*/LC_MESSAGES/*

%files doc
%defattr(-,root,root)
%doc COPYING ChangeLog NEWS README


%changelog
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

* Tue Jun 24 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.875-3mdk
- Patch1: fix gcc error in yyerrlab1

* Sat Jun 14 2003 Warly <warly@mandrakesoft.com> 1.875-2mdk
- temporaly fix the yacc conflict with byacc, will see later if an alternative is required.

* Fri Jun 13 2003 Warly <warly@mandrakesoft.com> 1.875-1mdk
- new version (main changes):
  - Changes in version 1.875, 2003-01-01:
    * syntax error processing
      - In Yacc-style parsers YYLLOC_DEFAULT is now used to compute error locations too.  This fixes bugs in error-location computation.
    * POSIX conformance
      - Semicolons are once again optional at the end of grammar rules. This reverts to the behavior of Bison 1.33 and earlier, and improves compatibility with Yacc.
      - `parse error' -> `syntax error' Bison now uniformly uses the term `syntax error';
      - Yacc command and library now available The Bison distribution now installs a `yacc' command, as POSIX requires.
      - Type clashes now generate warnings, not errors.
  - Changes in version 1.75, 2002-10-14:
    * Bison should now work on 64-bit hosts.
- port extfix patch to new version

* Fri May 02 2003 Stefan van der Eijk <stefan@eijk.nu> 1.35-4mdk
- remove unpackaged files

* Thu Jun  6 2002 Warly <warly@mandrakesoft.com> 1.35-3mdk
- fix non libdir in configure

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.35-2mdk
- Automated rebuild in gcc3.1 environment

* Thu Mar 28 2002 Warly <warly@mandrakesoft.com> 1.35-1mdk
- new version

* Fri Feb 15 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.32-2mdk
- Patch0: src/files (compute_exts_from_gf, compute_exts_from_src):
  Handle the case where header_extension is the same as src_extension,
  aka handle -d -o <file> where <file> doesn't have a known EXT to
  transform. e.g. if <file> is <something>.yxx, set the
  header_extension to <something>.yxx.h, as would do bison 1.28.

* Fri Feb  1 2002 Warly <warly@mandrakesoft.com> 1.32-1mdk
- new version

* Fri Jan 18 2002 Warly <warly@mandrakesoft.com> 1.31-1mdk
- new version

* Wed Jan  2 2002 Warly <warly@mandrakesoft.com> 1.30-4mdk
- add url tag

* Tue Oct 30 2001 Warly <warly@mandrakesoft.com> 1.30-3mdk
- fix remove install info error

* Tue Oct 30 2001 Warly <warly@mandrakesoft.com> 1.30-2mdk
- reput bison.simple in /usr/share

* Mon Oct 29 2001 Warly <warly@mandrakesoft.com> 1.30-1mdk
- new version

* Mon Jul  2 2001 Warly <warly@mandrakesoft.com> 1.28-9mdk
- clean spec

* Fri Nov 10 2000 Warly <warly@mandrakesoft.com> 1.28-8mdk
- rebuild with gcc 2.96 and glibc 2.2

* Thu Aug 03 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 1.28-7mdk
- included catalog files

* Mon Jul 24 2000 Warly <warly@mandrakesoft.com> 1.28-6mdk
- BM

* Mon Jul 10 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.28-5mdk
- fix make install as lord stefan require (pxlscks)
- really use spec-helper (idem?)

* Wed Jan 12 2000 Pixel <pixel@mandrakesoft.com> 1.28-4mdk
- spec-helper
- group update

* Wed Jan 12 2000 Pixel <pixel@mandrakesoft.com>
- fix build as non-root

* Wed Jul 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- version 1.28 :

* Tue May 18 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Bziped info files.
- Handle RPM_OPT_FLAGS

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Mon Mar  8 1999 Jeff Johnson <jbj@redhat.com>
- configure with datadir=/usr/lib (#1386).

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- updated text in spec file.
- update to 1.27

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- built for Manhattan
- added build root

* Wed Oct 15 1997 Donnie Barnes <djb@redhat.com>
- various spec file cleanups

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

