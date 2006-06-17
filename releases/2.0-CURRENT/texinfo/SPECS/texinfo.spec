#
# spec file for package texinfo
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		texinfo
%define version		4.8
%define release		%_revrel

Summary:	Tools needed to create Texinfo format documentation files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Publishing
URL:		http://www.texinfo.org
Source0:	ftp://ftp.gnu.org/pub/gnu/texinfo/%{name}-%{version}.tar.bz2
Source1:	info-dir
Patch1:		texinfo-3.12h-fix.patch
Patch2:		texinfo-4.7-vikeys-segfault-fix.patch
Patch3:		texinfo-4.7.test.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel, zlib-devel

Requires:	tetex
Requires(pre):	info-install
Requires(preun): info-install

%description
Texinfo is a documentation system that can produce both online information
and printed output from a single source file.  Normally, you'd have to
write two separate documents: one for online help or other online
information and the other for a typeset manual or other printed work.
Using Texinfo, you only need to write one source document.  Then when the
work needs revision, you only have to revise one source document.  The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you are
going to write documentation for the GNU Project.


%package -n info
Summary:	A stand-alone TTY-based reader for GNU texinfo documentation
Group:		System/Base
Requires(pre):	info-install
Requires(preun): info-install
Conflicts:	info-install < 4.7

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

You should install info, because GNU's texinfo documentation is a valuable
source of information about the software on your system.


%package -n info-install
Summary:	Program to update the GNU texinfo documentation main page
Group:		System/Base
Requires:	bzip2
Conflicts:	info < 4.7

%description -n info-install
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p0

%build
%configure2_5x
%make 
rm -f util/install-info
make -C util LIBS=%{_libdir}/libz.a
# all tests must pass
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_sysconfdir},/sbin}

%makeinstall
pushd %{buildroot}
    cat %SOURCE1 > .%{_sysconfdir}/info-dir
    ln -sf ../../../etc/info-dir %{buildroot}%{_infodir}/dir
    mv -f .%{_bindir}/install-info ./sbin
    mkdir -p .%{_sysconfdir}/X11/wmconfig
popd

# remove texi2pdf since it conflicts with tetex
rm -f %{buildroot}%{_bindir}/texi2pdf

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}

%preun
%_remove_install_info %{name}

%post -n info
%_install_info info.info

%preun -n info
%_remove_install_info info.info


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/makeinfo
%{_bindir}/texindex
%{_bindir}/texi2dvi
%{_infodir}/info-stnd.info*
%{_infodir}/texinfo*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man1/texindex.1*
%{_mandir}/man1/texi2dvi.1*                         
%{_mandir}/man5/texinfo.5*   
%{_datadir}/texinfo

%files -n info
%defattr(-,root,root)
%{_bindir}/info
%{_infodir}/info.info*
%{_bindir}/infokey
%{_mandir}/man1/info.1*
%{_mandir}/man1/infokey.1*
%{_mandir}/man5/info.5*

%files -n info-install
%defattr(-,root,root)
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/info-dir
%{_infodir}/dir
/sbin/install-info
%{_mandir}/man1/install-info.1*

%files doc
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL INTRODUCTION NEWS README TODO
%doc --parents info/README


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8
- fix prereq
- requires tetex
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.8-5avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.8-4avx
- rebuild for new gcc
- don't package texi2pdf since tetex already has it

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.8-3avx
- bootstrap build

* Sun Mar 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.8-2avx
- fix conflicts on info-install vs. info

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.8-1avx
- 4.8
- move info(1) and info(5) from info-install to info
- P3: fix macros support in texinfo so that groff documentation
  works (tvignaud)
- P4: make test robust against environment locales (guillomovitch)

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.6-4avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.6-3sls
- minor spec cleanups

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 4.6-2sls
- OpenSLS build
- tidy spec

* Wed Jul 16 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.6-1mdk
- new release

* Mon Jun 17 2003 Stefan van der Eijk <stefan@eijk.nu> 4.5-2mdk
- BuildRequires

* Fri Apr 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5-1mdk
- new release

* Fri Jan 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.3-3mdk
- build release

* Tue Nov 19 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.3-2mdk
- fix url (as usual, spotted by yura gusev)

* Mon Nov 18 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.3-1mdk
- new release
- fix build for new rpm

* Thu Oct 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.2c-1mdk
- new release (fix crash w/ MALLOC_CHECK_ == 2)
- remove patches 2, 103, 106 and 108 (merged upstream)
- don't overwrite README with info/README

* Mon Jul  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2-5mdk
- Costlessly make check in %%build stage

* Fri May 31 2002 Stefan van der Eijk <stefan@eijk.nu> 4.2-4mdk
- BuildRequires

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2-3mdk
- Automated rebuild in gcc3.1 environment

* Wed Apr 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.2-2mdk
- remove patch104 that chmouel steal from rh: this danish translation
  is util-linux messages translation, not texinfo one :-(

* Wed Apr 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.2-1mdk
- new release
- remove ru patch merged upstream

* Wed Apr 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1-3mdk
- remove patches 3 and 102 which cancel themselves
- clean spec

* Thu Apr 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1-2mdk
- recode russian po from windows-1251 to koi8-r [Patch105]
- reverse h<->l in vikeys [Patch106]
- fix "info --vi-keys libc:exit" segfault [Patch107]
- fix thinko in makeinfo/insertion.c comment [Patch108]

* Tue Mar 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1-1mdk
- new release
- add missing man pages

* Thu Nov  1 2001 dam's <damien@mandrakesoft.com> 4.0-22mdk
- added URL tag.

* Mon Aug 13 2001 dam's <damien@mandrakesoft.com> 4.0-21mdk
- rebuilt, spec cprrected

* Sun Mar 11 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0-20mdk
- danish translation added (rh).
- Fix recognition of .?o extensions in texi2dvi (rh).
- Fix info-dir symlink (rh).
- Recompile again the last ncurses.

* Fri Nov 24 2000 dam's <damien@mandrakesoft.com> 4.0-19mdk
- corrected config tag for _infodir/dir

* Fri Sep  1 2000 Pixel <pixel@mandrakesoft.com> 4.0-18mdk
- don't require gzip (which prereq install-info) in info-install (but bzip2, the
important one)

* Fri Sep  1 2000 Pixel <pixel@mandrakesoft.com> 4.0-17mdk
- info-install requires bzip2 and gzip

* Mon Aug 28 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 4.0-16mdk
- Correct install script

* Thu Aug 10 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 4.0-15mdk
- use more macros, add no replace to make rpmlint happy

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-14mdk
- automatically added BuildRequires


* Fri Jul 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0-13mdk
- fix broken link (Anton Graham)

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0-12mdk
- build release for BM
- use new macros

* Sat Mar 25 2000 Daouda Lo <daouda@mandrakesoft.com> 4.0-11mdk
- built for 7.1 (new group structure)
- relocate the info-tty package.

* Thu Mar 23 2000 Pixel <pixel@mandrakesoft.com> 4.0-10mdk
- add info prerequires install-info (because some packages have trigger on package "info")

* Sat Mar  4 2000 Pixel <pixel@mandrakesoft.com> 4.0-9mdk
- add info requires install-info (because some packages have trigger on package "info")

* Fri Mar  3 2000 Pixel <pixel@mandrakesoft.com> 4.0-8mdk
- have /sbin/install-info in its own package (for prereq pb at install)

* Wed Dec  1 1999 Pixel <pixel@linux-mandrake.com>
- removed the glibc prereq for info

* Mon Nov 15 1999 Pixel <pixel@mandrakesoft.com>
- changed the deps. Forced info (and so install-info) to not depends on gpm :(
- unremoved gpm as it can't be done

* Wed Nov  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Wed Sep 28 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 4.0

* Mon Aug 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Increase release (oups).

* Sun Aug 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Made a patch for install-info.c to handle bzip2 (where the old patch is gone ?)

* Tue Aug 17 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 3.12q
- rewrite zlib patch (incompatibility with 3.12q)

* Tue Jul 22 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- Updated to 3.12n
- Add french description


* Tue Jul  6 1999 Axalon Bloodstone <axalon@linux-mandrake.com>

- info Provides install-info and now knows so.

* Wed Jun 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 3.12h.
- Upgrading patch.

* Thu Apr 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add patch to handle bzip2 and other compresion on install-info.
- Making dependence explicitly from bzip2.

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add patch from RedHat 6.0.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- fix handling of RPM_OPT_FLAGS

* Thu Mar 11 1999 Cristian Gafton <gafton@redhat.com>
- version 3.12f
- make %{_infodir}/dir to be a %config(noreplace)

* Wed Nov 25 1998 Jeff Johnson <jbj@redhat.com>
- rebuild to fix docdir perms.

* Thu Sep 24 1998 Cristian Gafton <gafton@redhat.com>
- fix allocation problems in install-info

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- /sbin/install-info should not depend on %{_libdir}/libz.so.1 -- statically
  link with %{_libdir}/libz.a.

* Fri Aug 07 1998 Erik Troan <ewt@redhat.com>
- added a prereq of bash to the info package -- see the comment for a
  description of why that was done

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- add %attr to permit non-root build.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Apr 12 1998 Cristian Gafton <gafton@redhat.com>
- added %clean
- manhattan build

* Wed Mar 04 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 3.12
- added buildroot

* Sun Nov 09 1997 Donnie Barnes <djb@redhat.com>
- moved %{_infodir}/dir to /etc/info-dir and made %{_infodir}/dir a
  symlink to /etc/info-dir.

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added wmconfig entry for info

* Wed Oct 01 1997 Donnie Barnes <djb@redhat.com>
- stripped /sbin/install-info

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- added info-dir to filelist

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- added patch from sopwith to let install-info understand gzip'ed info files
- use skeletal dir file from texinfo tarball (w/ bash entry to reduce
  dependency chain) instead (and install-info command everywhere else)
- patches install-info to handle .gz names correctly

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Feb 25 1997 Erik Troan <ewt@redhat.com>
- patched install-info.c for glibc.
- added %{_bindir}/install-info to the filelist

* Tue Feb 18 1997 Michael Fulbright <msf@redhat.com>
- upgraded to version 3.9.
