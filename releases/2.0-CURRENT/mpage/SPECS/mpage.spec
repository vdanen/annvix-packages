#
# spec file for package mpage
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mpage
%define version		2.5.4
%define release		%_revrel

Summary:	A tool for printing multiple pages of text on each printed page
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Configuration
URL:		http://www.mesa.nl/pub/mpage
Source:		http://www.mesa.nl/pub/mpage/%{name}-%{version}.tar.bz2
Patch0:		mpage-2.5.4-config.patch
Patch1:		mpage-2.5.4-gcc4.patch
# Japanese patch.bz2
Patch10:	mpage-2.5.3-j.patch
Patch20:	mpage-mfix.patch
Patch21:	mpage-psprint.patch
Patch22:	mpage-2.5.3-japanese-fix.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The mpage utility takes plain text files or PostScript(TM) documents
as input, reduces the size of the text, and prints the files on a
PostScript printer with several pages on each sheet of paper.  Mpage
is very useful for viewing large printouts without using up tons of
paper.  Mpage supports many different layout options for the printed
pages.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .config
%patch1 -p1 -b .gcc4
%patch10 -p1 -b .jp
%patch20 -p1 -b .fix
%patch21 -p1
%patch22 -p0


%build
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/mpage
%{_mandir}/man1/mpage.1*
%dir %{_datadir}/mpage
%{_datadir}/mpage/*

%files doc
%defattr(-,root,root)
%doc CHANGES Copyright README NEWS TODO


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4-1avx
- 2.5.4
- P1: gcc4 & makefilery fixes (gbeauchesne)
- move encodings where that are expected to be: %%_datadir/mpage (gbeauchesne)

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.3-10avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.3-9avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.3-8avx
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 2.5.3-7sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.5.3-6sls
- OpenSLS build
- tidy spec

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.5.3-5mdk
- rebuild
- drop unapplied patch (P2)

* Mon Mar 10 2003 Till Kamppeter <till@mandrakesoft.com> 2.5.3-4mdk
- Fixed converting of japanese plain text files when "LC_ALL=ja" is set
  (patch 22)

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5.3-3mdk
- build release

* Mon Nov 18 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5.3-2mdk
- fix bad generated postscript
- add %%_datadir/mpage

* Tue Nov 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5.3-1mdk
- new release
- drop patch 4 since now man page is generated from a template that
  use prefix
- rediff patch 10
- drop patch 20 since now Makefile is correct

* Sat Jul 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5.2-1mdk
- new release
- fix source url
- rediff patch 0 and 10; drop merged bits
- rediff patches 2, 4 and 22
- drop patches 3 and 11 (merged upstream)

* Wed May 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5.1-15mdk
- gcc-3.1  build
- bugfix to handle dvi2ps files (Patch 2)
- security: use /tmp rather than /usr/tmp & use mkstemp (Patch 3)
- fix man pages location in mpage.1 (Patch 4)
- add japanese support (patches 10 and 11)
- fix mfix (Patch 20)
- psprint: default to sh, not ksh (Patch 21)
- fix Makefile for man path (Patch 22)
- safer macro, .. in file.c (Patch 23)

* Tue Oct 30 2001 Ludovic Francois <lfrancois@mandrakesoft.com> 2.5.1-14mdk
- added URL.

* Sat Jul 07 2001 Etienne Faure <etienne@mandrakesoft.com> 2.5.1-13mdk
- rebuild on cluster

* Fri Jul 28 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 2.5.1-12mdk
- BM + macroszification
- clean spec

* Wed Mar 22 2000 Daouda Lo <daouda@mandrakesoft.com> 2.5.1-11mdk
- relocate to group Networking/File transfer

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Build release.


* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- 2.5.1
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Tue Jan 24 1999 Michael Maher <mike@redhat.com>
- changed group

* Thu Dec 17 1998 Michael Maher <mike@redhat.com>
- 6.0 build stuff.

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 15 1997 Michael Fulbright <msf@redhat.com>
- (Re)applied patch to correctly print dvips output.

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
