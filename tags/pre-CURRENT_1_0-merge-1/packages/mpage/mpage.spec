Summary: A tool for printing multiple pages of text on each printed page.
Name: mpage
Version: 2.5.3
Release: 5mdk
License: BSD
Group: System/Configuration/Printing
Source: http://www.mesa.nl/pub/mpage/%name-%version.tar.bz2
Patch0: mpage252-config.patch.bz2
#Patch2: mpage-debian.patch.bz2
# Japanese patch.bz2
Patch10: mpage-2.5.3-j.patch.bz2
Patch20: mpage-mfix.patch.bz2
Patch21: mpage-psprint.patch.bz2
Patch22: mpage-2.5.3-japanese-fix.patch.bz2

URL: http://www.mesa.nl/pub/mpage
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
The mpage utility takes plain text files or PostScript(TM) documents
as input, reduces the size of the text, and prints the files on a
PostScript printer with several pages on each sheet of paper.  Mpage
is very useful for viewing large printouts without using up tons of
paper.  Mpage supports many different layout options for the printed
pages.

Mpage should be installed if you need a useful utility for viewing
long text documents without wasting paper.

%prep
%setup -q
%patch0 -p1 -b .config
#%patch2 -p1 -b .debian
%patch10 -p1 -b .jp
%patch20 -p1 -b .fix
%patch21 -p1
%patch22 -p0

%build
%make

%install
rm -rf $RPM_BUILD_ROOT

make PREFIX=$RPM_BUILD_ROOT%_prefix MANDIR=$RPM_BUILD_ROOT%_mandir/man1 install
mkdir -p $RPM_BUILD_ROOT%_libdir/%name
cp -a Encodings/* $RPM_BUILD_ROOT%_libdir/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES Copyright README NEWS TODO

%_bindir/mpage
%_mandir/man1/mpage.1*
%_libdir/mpage
%_datadir/mpage

%changelog
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
- add %_datadir/mpage

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
