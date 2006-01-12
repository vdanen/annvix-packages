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
%define version		2.5.4a
%define release		%_revrel

Summary:	A tool for creating scanners (text pattern recognizers)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL: 		http://www.gnu.org/software/flex/flex.htm
Source:		ftp.gnu.org:/non-gnu/flex/flex-2.5.4a.tar.bz2
Patch0:		flex-2.5.4a-skel.patch
Patch1:         flex-2.5.4-glibc22.patch
Patch2:		flex-2.5.4-c++fixes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	byacc

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

You should install flex if you are going to use your system for
application development.


%prep
%setup -q -n flex-2.5.4
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .c++fixes
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

cd %{buildroot}%{_mandir}/
mkdir man1
mv flex.1 man1
cd man1
ln -s flex.1 lex.1
ln -s flex.1 flex++.1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,755)
%doc COPYING NEWS README
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/libfl.a
%{_includedir}/FlexLexer.h


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Fri Jul 18 2003 Warly <warly@mandrakesoft.com> 2.5.4a-21mdk
- rebuild

* Fri Jun  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5.4a-20mdk
- Sanitize specfile (use %%configure, bzip2 patches)
- Patch2: ISO C++ fixes

* Wed May 29 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5.4a-19mdk
- Automated rebuild with gcc 3.1-1mdk

* Wed Jan  2 2002 Warly <warly@mandrakesoft.com> 2.5.4a-18mdk
- really apply the patch

* Tue Dec  4 2001 Warly <warly@mandrakesoft.com> 2.5.4a-17mdk
- Fix generation of broken code (conflicting isatty() prototype w/ glibc 2.2) (redhat fix)

* Sun Sep 09 2001 Stefan van der Eijk <stefan@eijk.nu> 2.5.4a-16mdk
- BuildRequires: byacc

* Wed Sep  5 2001 Warly <warly@mandrakesoft.com> 2.5.4a-15mdk
- fix some rpmlint errors

* Fri Apr 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.5.4a-14mdk
- Rebuild to fix an obscure problem I had building the kernel with aic7xxx
  enabled (donno why).

* Tue Sep 12 2000 David BAUDENS <baudens@mandrakesoft.com> 2.5.4a-13mdk
- Allow to build (aka don't use %%configure macro)
- Macrozification for other parts of spec

* Wed May 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.5.4a-12mdk
- Use %{ _tmppath}
- Really use spec-helper.

* Sun Apr 02 2000 Jerome Martin <jerome@mandrakesoft.com> 2.5.4a-11mdk
- Fix rpm group
- specfile cleanup for spec-helper

* Wed Nov 10 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- avoid uninitialized variable warning.

* Mon May 17 1999 Axalon Bloodstone <axalon@jumpstart.netpirate.org>
- incorrect symlinks

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree

* Mon Aug 10 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.5.4 to 2.5.4a

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 20 1997 Michael Fulbright <msf@redhat.com>
- Updated to v. 2.5.4
