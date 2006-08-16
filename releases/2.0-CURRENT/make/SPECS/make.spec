#
# spec file for package make
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		make
%define version		3.80
%define release		%_revrel
%define epoch		1

Summary:	A GNU tool which simplifies the build process for users
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/directory/GNU/make.html
Source:		ftp://ftp.gnu.org/pub/gnu/make/%{name}-%{version}.tar.bz2
# to remove once those po files are included in standard sources
Source1:	%{name}-pofiles.tar.bz2
Patch0:		make-3.80-no-hires-timestamp.patch
Patch1:		make-3.80-lib64.patch
Patch2:		make-3.80-fix-mem-exhausting.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext-devel

Requires(post):	info-install
Requires(preun): info-install


%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files.  Make
allows users to build and install packages without any significant
knowledge about the details of the build process.  The details about how
the program should be built are provided for make in the program's
makefile.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a1
# WARNING: only configure script is patched
%patch0 -p1 -b .no-hires-timestamp
%patch1 -p1 -b .lib64
%patch2 -p0 -b .mem


%build
%configure2_5x
%make


%check
# all tests must pass
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

ln -sf make %{buildroot}%{_bindir}/gmake

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info make.info

%preun
%_remove_install_info make.info


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/make
%{_bindir}/gmake
%{_mandir}/man1/make.1*
%{_infodir}/make.info*

%files doc
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS COPYING ChangeLog README README.customs SCOPTIONS NEWS
%doc glob/COPYING.LIB glob/ChangeLog


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.80
- spec cleanups
- remove locales

* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.80
- add -doc subpackage
- rebuild with gcc4
- put the test in %%check

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.80
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.80
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.80-13avx
- P2: fix memory exhausting (mdk bug #14626) (tvignaud)
- P1: linux32 fixes, aka resolve -llib only in */lib when running under
  a 32bit personality and some lib64 fixes (gbeauchesne)
- rebuild against new gettext

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.80-12avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.80-11avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.80-10avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.80-9avx
- require packages not files
- Annvix build

* Fri May 09 2004 Vincent Danen <vdanen@opensls.org> 3.80-8sls
- rebuild against new gettext

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 3.80-7sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 3.80-6sls
- OpenSLS build
- tidy spec

* Fri Jul 25 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.80-5mdk
- Patch0: Don't use high resolution timestamp to nuke librt dep

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.80-4mdk
- rebuild
- use %%make macro

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.80-3mdk
- build release

* Wed Nov 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.80-2mdk
- alter url for gnu site rather than source url (yura gusev)
- doc : add NEWS, remove glob/ChangeLog

* Tue Nov 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.80-1mdk
- new release
- fix url
- BuildRequires: autoconf2.5
- simplify
- drop patch 0 : there's no need to play with aclocal instead of using
  WANT_AUTOCONF_2_5
- drop patch 1 (better fix upstream)

* Sun Nov 03 2002 Stefan van der Eijk <stefan@eijk.nu> 3.79.1-12mdk
- BuildRequires: gettext-devel


* Thu Oct 10 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.79.1-11mdk
- patch 2: fix bad assertion triggered by xawtv

* Fri Jul  5 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.79.1-10mdk
- Costlessly make check in %%build stage

* Wed May 22 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.79.1-9mdk
- Automated rebuild with gcc 3.1-1mdk

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.79.1-8mdk
- Automated rebuild in gcc3.1 environment

* Tue Mar 26 2002 Frederic Lepied <flepied@mandrakesoft.com> 3.79.1-7mdk
- call libtoolize explicitly

* Fri Oct 26 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 3.79.1-6mdk
- Rebuild, fix rpmlint errors and warnings.
- Add patch #0, s/AC_PROG_RANLIB/AC_PROG_LIBTOOL/ in configure.in

* Thu Aug 10 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.79.1-5mdk
- corrected problem with %%preun script

* Thu Aug 03 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 3.79.1-4mdk
- integrated catalog files

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.79.1-3mdk
- BM

* Sun Jul  9 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.79.1-2mdk
- macroszifications.

* Sun Jun 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.79.1-1mdk
- 3.79.1

* Sat Jun 03 2000 David BAUDENS <baudens@mandrakesoft.com> 3.79-3mdk
- Fix %%doc
- Spec-helper

* Wed Apr 17 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 3.79-2mdk
- more documentation in package

* Wed Apr 12 2000 Christopher Molnar <molnarc@mandrakesoft.com> 3.79-1mdk
- Update to 3.79

* Tue Apr 11 2000 Christopher Molnar <molnarc@mandrakesoft.com> 3.77-13mdk
- New Group

* Thu Jan 13 2000 Pixel <pixel@mandrakesoft.com>
- fix an rm

* Wed Oct 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with jeff package.

* Fri Aug 13 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- bzip2 info

* Tue Jul 06 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Bzip2 info pages, spec files tweaks.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- added a serial tag so it upgrades right

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Sep 16 1998 Cristian Gafton <gafton@redhat.com>
- added a patch for large file support in glob
 
* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.77

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- udpated from 3.75 to 3.76
- various spec file cleanups
- added install-info support

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
