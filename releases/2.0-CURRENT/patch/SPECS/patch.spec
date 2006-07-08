#
# spec file for package patch
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		patch
%define version 	2.5.9
%define release 	%_revrel

Summary:	The GNU patch command, for modifying/upgrading files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Text tools
URL:		http://www.gnu.org/directory/GNU/patch.html
Source:		ftp://alpha.gnu.org/gnu/patch/patch-%{version}.tar.bz2
Patch1:		patch-2.5.8-sigsegv.patch
Patch2:		patch-2.5.4-unreadable_to_readable.patch
Patch3:		patch-2.5.8-stderr.patch
Patch5:		patch-2.5.4-destdir.patch

Buildroot:	%{_buildroot}/%{name}-%{version}

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1


%build
# (fg) Large file support can be disabled from ./configure - it is necessary at
# least on sparcs
%ifnarch sparc sparc64 alpha
%configure 
%else
%configure --disable-largefile
%endif

make "CFLAGS=%{optflags} -D_GNU_SOURCE -W -Wall" LDFLAGS=-s


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog
%{_bindir}/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog


%changelog
* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9-8avx
- correct the buildroot

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9-7avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9-6avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9-5avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9-4avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.5.9-3sls
- minor spec cleanups
- remove %%prefix

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 2.5.9-2sls
- OpenSLS build
- tidy spec

* Wed Jul 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5.9-1mdk
- new release

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5.8-3mdk
- build release

* Mon Nov 04 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5.8-2mdk
- alter url for project page (Yura Gusev)

* Thu Oct 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5.8-1mdk
- new release
- add url
- rediff patch 1, 3
- remove patch 4 (merged upstream)

* Wed May 29 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5.4-11mdk
- Automated rebuild with gcc 3.1-1mdk

* Tue Nov 20 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.5.4-10mdk
- DESTDIR support.

* Sat Aug 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.5.4-9mdk
- Sanity build for 8.1.
- s/Copyright/License/;

* Tue Dec  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.5.4-8mdk
- Merge rh patch :
	* Fix the case where stderr isnt flushed for ask(). Now the
	 'no such file' appears before the skip patch question, not at
	 the very end, Doh!
	* use .orig as default suffix, as per man page and previous
      behaviour

* Tue Jul 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.5.4-7mdk
- Fix possible sigsev (deb).
- By default create empty backup files as readable !!!.

* Tue Jul 25 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.5.4-6mdk
- really move the strip (titiscks)
- BM

* Tue Jul 11 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>  2.5.4-5mdk
- add alpha for largefile
- remove binaries stripping & {info,man}-pages compression because of
  spec-helper
- Stefan van der Eijk <s.vandereijk@chello.nl> :
	* makeinstall macro
	* macroszifications

* Sun Apr 02 2000 Adam Lebsack <adam@mandrakesoft.com> 2.5.4-4mdk
- Fixed powerpc by adding -D_GNU_SOURCE flag.

* Mon Jan 17 2000 Francis Galiegue <francis@mandrakesoft.com>

- No large file support for sparc - now done from ./configure

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- build release.

* Wed Sep 08 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 2.5.4

* Fri Aug 06 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- 2.5.3

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Mon Mar 22 1999 Jeff Johnson <jbj@redhat.com>
- (ultra?) sparc was getting large file system support.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Tue Sep  1 1998 Jeff Johnson <jbj@redhat.com>
- bump release to preserve newer than back-ported 4.2.

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- Fix for problem #682 segfault.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- added buildroot

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 2.5

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
