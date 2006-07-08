#
# spec file for package groff
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# mdk-1.19.1-1mdk
#
# $Id$

%define revision	$Rev$
%define name		groff
%define version		1.19.1
%define release		%_revrel

Summary:	A document formatting system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Text tools
URL:		http://www.gnu.org/directory/GNU/groff.html
Source0:	ftp://prep.ai.mit.edu/pub/gnu/groff/%{name}-%{version}.tar.bz2
Source1:	troff-to-ps.fpi
Source2:	README.A4
Patch0:		groff-1.18-info.patch
Patch1:		groff-1.19.1-nohtml.patch
Patch2:		groff-1.17.2-libsupc++.patch
Patch3:		groff-1.16.1-no-lbp-on-alpha.patch
# keeps apostrophes and dashes as ascii, but only for man pages
# -- pablo
Patch4:		groff-1.19-dashes.patch
Patch5:		groff-1.19.1-CAN-2004-0969.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, byacc, texinfo >= 4.3, xpm-devel

Requires:	mktemp, groff-for-man = %{version}-%{release}
Requires(post):	info-install
Requires(preun): info-install
Obsoletes:	groff-tools
Provides:	groff-tools

%description
Groff is a document formatting system.  Groff takes standard text and
formatting commands as input and produces formatted output.  The
created documents can be shown on a display or printed on a printer. 
Groff's formatting commands allow you to specify font type and size, bold
type, italic type, the number and size of columns on a page, and more.


%package for-man
Summary:	Parts of the groff formatting system that is required for viewing manpages
Group:		Text tools
Conflicts:	groff < 1.19-7avx

%description for-man
The groff-for-man package contains the parts of the groff text processor
package that are required for viewing manpages.
For a full groff package, install package groff.


%package perl
Summary:	Parts of the groff formatting system that require Perl
Group:		Text tools

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl. These include the afmtodit font processor
for creating PostScript font files, the grog utility that can be used
to automatically determine groff command-line options, and the
troff-to-ps print filter.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .nohtml
%patch2 -p1 -b .libsupc++
%ifarch alpha
%patch3 -p1 -b .alpha
%endif
%patch4 -p1 -b ._dashes
%patch5 -p1 -b .can-2004-0969

cp -f %{_sourcedir}/README.A4 .

WANT_AUTOCONF_2_5=1 autoconf


%build
PATH=$PATH:%{_prefix}/X11R6/bin
export MAKEINFO=$HOME/cvs/texinfo/makeinfo/makeinfo
%configure2_5x --enable-japanese
make top_builddir=$PWD top_srcdir=$PWD
cd doc
makeinfo groff.texinfo


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

PATH=$PATH:%{_prefix}/X11R6/bin
mkdir -p %{buildroot}{%{_prefix},%{_infodir},%{_bindir},%{_docdir}/%{name}/%{version}/html/momdoc}
%makeinstall manroot=%{buildroot}%{_mandir} top_builddir=$PWD top_srcdir=$PWD common_words_file=%{buildroot}%{_datadir}/%{name}/%{version} mkinstalldirs=mkdir
install -m 0644 doc/groff.info* %{buildroot}%{_infodir}

for i in s.tmac mse.tmac m.tmac; do
    ln -s $i %{buildroot}%{_datadir}/groff/%{version}/tmac/g$i
done
for i in troff tbl pic eqn neqn refer lookbib indxbib soelim nroff; do
    ln -s $i %{buildroot}%{_bindir}/g$i
done

# Build system is compressing man-pages
for i in eqn.1 indxbib.1 lookbib.1 nroff.1 pic.1 refer.1 soelim.1 tbl.1 troff.1; do
    ln -s $i%{_extension} %{buildroot}%{_mandir}/man1/g$i%{_extension}
done

mkdir -p %{buildroot}/%{_libdir}/rhs/rhs-printfilters
install -m 0755 %{_sourcedir}/troff-to-ps.fpi %{buildroot}%{_libdir}/rhs/rhs-printfilters

# call spec-helper before creating the file list
s=/usr/share/spec-helper/spec-helper ; [ -x $s ] && $s

cat <<EOF > groff.list
%{_datadir}/groff/%{version}/eign
%{_datadir}/groff/%{version}/font/devX100
%{_datadir}/groff/%{version}/font/devX100-12
%{_datadir}/groff/%{version}/font/devX75
%{_datadir}/groff/%{version}/font/devX75-12
%{_datadir}/groff/%{version}/font/devdvi
%{_datadir}/groff/%{version}/font/devhtml
%{_datadir}/groff/%{version}/font/devlbp
%{_datadir}/groff/%{version}/font/devlj4
%{_datadir}/groff/%{version}/font/devps
EOF

cat <<EOF > groff-for-man.list
%{_bindir}/eqn
%{_bindir}/troff
%{_bindir}/nroff
%{_bindir}/tbl
%{_bindir}/geqn
%{_bindir}/gtbl
%{_bindir}/gnroff
%{_bindir}/grotty
%{_bindir}/groff
%{_bindir}/gtroff
%dir %{_datadir}/groff
%dir %{_datadir}/groff/%{version}
%{_datadir}/groff/%{version}/tmac
%dir %{_datadir}/groff/%{version}/font
%{_datadir}/groff/%{version}/font/devascii
#TV%{_datadir}/groff/%{version}/font/devascii8
#TV%{_datadir}/groff/%{version}/font/devkoi8-r
%{_datadir}/groff/%{version}/font/devlatin1
#TV%{_datadir}/groff/%{version}/font/devnippon
%{_datadir}/groff/%{version}/font/devutf8
%dir %{_datadir}/groff/site-tmac
%{_datadir}/groff/site-tmac/man.local
%{_datadir}/groff/site-tmac/mdoc.local
EOF

cat <<EOF > groff-perl.list
%{_bindir}/grog
%{_bindir}/mmroff
%{_bindir}/afmtodit
%{_mandir}/man1/afmtodit.1.bz2
%{_mandir}/man1/grog.1.bz2
%{_mandir}/man1/mmroff.1.bz2
EOF

dirs=usr/share/man/*
(cd %{buildroot} ; find usr/bin usr/share/man usr/share/groff/%{version}/tmac ! -type d -printf "/%%p\n") >> %{name}.list
(cd %{buildroot} ; find usr/share/groff/%{version}/tmac/* -type d -printf "%%%%dir /%%p\n") >> %{name}.list

perl -ni -e 'BEGIN { open F, "%{name}-for-man.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}.list
perl -ni -e 'BEGIN { open F, "%{name}-perl.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}.list
# japanese environment is crazy; doc.tmac seems superior than docj.tmac
ln -sf doc.tmac %{buildroot}%{_datadir}/groff/%{version}/tmac/docj.tmac

#TV cp -a {,%{buildroot}%{_datadir}/groff/%{version}/}font/devkoi8-r

for i in $(find %{buildroot} -empty -type f); do echo " ">> $i;done

mv %{buildroot}%{_docdir}/{groff/%{version}/,%{name}-%{version}/}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}

%preun
%_remove_install_info %{name}


%files -f groff.list
%defattr(-,root,root)
%doc BUG-REPORT COPYING NEWS PROBLEMS README README.A4 TODO VERSION
%{_infodir}/groff*

%files for-man -f groff-for-man.list
%defattr(-,root,root)

%files perl -f groff-perl.list
%defattr(-,root,root)
%{_libdir}/rhs/*/*

%files doc
%defattr(-,root,root)


%changelog
* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1
- add -doc subpackage
- rebuild with gcc4
- use %%_sourcdir/file instead of %%{SOURCEx}

* Fri Feb 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1
- renumber patches
- P5: security fix for CAN-2004-0969

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1-2avx
- remove BuildReq on xorg-x11 (aka rman) and don't build xditview

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.19.1-1avx
- 1.19.1
- drop unapplied P3
- drop P7
- update P5 (waschk)
- explicit groff-for-man conflict with older groff due to eqn (pixel)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.19-8avx
- rebuild for new gcc

* Sat Jun 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.19-7avx
- bootstrap build
- change buildrequires from texinfo < 4.7 to >= 4.3
- make groff depends on groff-for-man %%{version}-%%{release}
- spec cleanups

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.19-6avx
- require packages not files
- Annvix build
- merge from amd64-branch: build fixes (gbeauchesne)

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.19-5sls
- remove %%build_opensls macro
- minor spec cleanups
- don't need COPYING in each file

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 1.19-4sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to not build gxditview
- if %%build_opensls don't BuildReq: netpbm, netpbm-devel, psutils

* Thu Aug 21 2003 Pablo Saratxaga <pablo@@mandrakesoft.com> 1.19-3mdk
- keep dashes and apostrophes as ascii for man pages in UTF-8 (bug #4212)

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.19-2mdk
- BuildRequires: netpbm-devel, texinfo >= 4.3

* Wed Jul 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.19-1mdk
- new release
- update patch 3, 107 and 108 (but disable them for now due to build system
  issues)
- fix builrequires

* Thu Feb 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.18.1-5mdk
- patch 108 : fix warnings from pablo fix for utf-8 output

* Fri Jan 31 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 1.18.1-4mdk
- as groff can't handle properly utf-8, the nroff script is modified to
  run groff in the known locale, then convert to utf-8 the output.
- added to files sections a few missing directories

* Mon Jan 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.18.1-3mdk
- build release
- add missing info files

* Wed Nov 13 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.18.1-2mdk
- freshen patch 3 (multi byte support)

* Tue Nov 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.18.1-1mdk
- new release
- rediff patch 3
- remove patches 110, 111 & 112 (merged upstream)
- simplify %%install
- fix hardcoded version number
- fix url
- add japanese patch link

* Sat Oct 12 2002 Stefan van der Eijk <stefan@eijk.nu> 1.18-4mdk
- BuildRequires: texinfo

* Tue Sep 24 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.18-3mdk
- BuildRequires: libnetpbm9-devel, which grabs libnetpbm9 that
  contains necessary libpnm.so.9 library.
- Patch6: libgroff.a contains C++ code thus we may need to link with
  g++.  That patch was already there but Titi decided to nuke the
  1.17.2-13mdk release when he merged his stuff for 1.18.

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.18-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Tue Aug 13 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.18-1mdk
- new release:
	o colour support (although see below).
	o new macro set, mom, mainly for non-scientific writers. The aim of	these
	  macros is to make groff accessible for ordinary use with a minimum of
	  convoluted syntax.
	o 'eu' and 'Eu' characters available for Euro support.
	o improved support for TeX hyphenation files.
	o new means of setting the line length, which now works for -mdoc manual
	  pages as well as -man. Use man-db >= 2.4.0 to take advantage of this.
	o documentation of the differences between groff and Unix troff is now in
	  groff_diff(7).
	o groff_mwww(1) has been renamed to groff_www(1).
	o groff_ms(7) has been completely rewritten.
	o new scripts: groffer, pic2graph, and eqn2graph.
	o substantial improvements in grohtml (although it's still alpha),
	  including dealing with overstriking properly
- drop patches 5, 6 (merged upstream), 3 (better fix)
- remove useless prefix
- move mdk patches in the 10x area
- patch3: add japanase support
- patch4: fix info name
- patch5: don't build html files
- Prereq: /sbin/install-info
- process texinfo file into info one, and install it
- add %%post and %%postun to install and remove info file
- fix japanese problem: link docj.tmac to doc.tma
- rediff koi8 patch (russian support)
- mmroff.7 is now mmroff.1
- patch110: kill warnings, fix build on non-intel boxes
- patch111: make sure pointsize is initialized properly, thus fixing an
  infinite loop in the ia64 build
- patch112: freeze unbreakable spaces, preventing a failed assertion on
  latin1(7)
- add /usr/share/groff/font/devascii8 to groff-for-man and remove charon fix
- add /usr/share/groff/font/devnippon for japanese support
- add lot of docs

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.17.2-12mdk
- Automated rebuild with gcc3.2

* Sat May 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.17.2-11mdk
- gcc-3.1 build

* Wed Apr 17 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.17.2-10mdk
- fix build with gcc-3.1

* Wed Mar 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.17.2-9mdk
- fix \' in latin1 (pixel)
- use WANT_AUTOCONF_2_5 with generic autoconf for lord gc

* Mon Feb 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.17.2-8mdk
- from Andrej Borsenkow:
	* use configure2_5x
	* require autconf-2.5x due to patch7
	* patch7 - support for koi8-r. Code based on patch in FreeBSD,
	  most credits to Ruslan Ermilov <ru@FreeBSD.org>

* Tue Feb  5 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.17.2-7mdk
- remove patch4 since it breaks html formatting (mkstemp not appropriate in
  this situation... bad snailtalk)

* Wed Jan 30 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.17.2-6mdk
- patch5 for security
- patch6 to fix segfault with pic in some instances

* Tue Oct 30 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.17.2-5mdk
- remove useless %%define

* Wed Oct 10 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.17.2-4mdk
- remove safer patch since it was included in mainstream sources
- Provides:   groff-tools

* Fri Sep 07 2001 Stefan van der Eijk <stefan@eijk.nu> 1.17.2-3mdk
- BuildRequires: byacc
- Removed redundant BuildRequires.

* Mon Aug 06 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.17.2-2mdk
- add LICENSE in %%docdir

* Wed Jul 18 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.17.2-1mdk
- new release

* Wed Jul  4 2001 Pixel <pixel@mandrakesoft.com> 1.17.1-2mdk
- add an-old.tmac to groff-for-man

* Sat Jun 30 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.17.1-1mdk
- 1.17.1 bumped out into cooker.
- Remove the groff safer patch. Seems to have been incorporated into the
  source already.
- src/preproc/html/pre-html.cc: s/mktemp()/mkstemp()/;
- s/Copyright/License/;

* Tue May 15 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.16.1-10mdk
- change default from -Tascii to -Tlatin1 in /usr/bin/nroff (so man pages
  in non-latin1 can still be displayed on screen as previously)
- add /usr/share/groff/font/devutf8 to groff-for-man (we are going utf-8...)

* Mon May  7 2001 Pixel <pixel@mandrakesoft.com> 1.16.1-9mdk
- add /usr/share/groff/tmac/tmac.latin1 to groff-for-man

* Fri May  4 2001 Pixel <pixel@mandrakesoft.com> 1.16.1-8mdk
- add /usr/bin/nroff and tmac.tty-char to groff-for-man so that man works again

* Tue Dec 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.16.1-7mdk
- Don't build grolbp on alpha.

* Thu Nov 09 2000 David BAUDENS <baudens@mandrakesoft.com> 1.16.1-6mdk
- BuildRequires: XFree86

* Fri Nov 03 2000 Florin Grad <florin@mandrakesoft.com> 1.16.1-5mdk
- recompiled with gcc 2.96

* Wed Sep  6 2000 Pixel <pixel@mandrakesoft.com> 1.16.1-4mdk
- add tman.doc and mdoc to groff-for-man for ssh man page

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 1.16.1-3mdk
- move important stuff for view man pages in groff-for-man

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.16.1-2mdk
- automatically added BuildRequires

* Thu Aug  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.16.1-1mdk
- 1.16.1.

* Thu Jul 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.16-1mdk
- Remove %{config} for app-default file.
- Merge rh changes.
- Add perl pacakge.
- BM.
- 1.16.

* Sun May 13 2000 David BAUDENS <baudens@mandrakesoft.com> 1.15-4mdk
- Fix build for i486
- Use %%{_buildroot} for BuildRoot

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.15-3mdk
- Fix rpmlint error/warning.

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.15-2mdk
- Add debian patch to display kanji.
- Adjust groups.

* Mon Jan  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.15-1mdk
- 1.15.

* Thu Oct 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix building as user.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- fix handling of RPM_OPT_FLAGS

* Tue Feb 16 1999 Cristian Gafton <gafton@redhat.com>
- glibc 2.1 patch for xditview (#992)

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
- fix makefiles to work with bash2

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- use g++ for C++ code

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- manhattan and buildroot

* Mon Nov  3 1997 Michael Fulbright <msf@redhat.com>
- made xdefaults file a config file

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- split perl components into separate subpackage

* Tue Oct 21 1997 Michael Fulbright <msf@redhat.com>
- updated to 1.11a
- added safe troff-to-ps.fpi

* Tue Oct 14 1997 Michael Fulbright <msf@redhat.com>
- removed troff-to-ps.fpi for security reasons.

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc
