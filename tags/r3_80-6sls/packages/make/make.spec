%define name	make
%define version	3.80
%define release	6sls

Summary:	A GNU tool which simplifies the build process for users
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/directory/GNU/make.html
Source:		ftp://ftp.gnu.org/pub/gnu/make/%name-%version.tar.bz2
# to remove once those po files are included in standard sources
Source1:	%{name}-pofiles.tar.bz2
Patch0:		make-3.80-no-hires-timestamp.patch.bz2

BuildRoot:	%_tmppath/%name-root
BuildRequires:	gettext-devel

Prereq:		/sbin/install-info

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files.  Make
allows users to build and install packages without any significant
knowledge about the details of the build process.  The details about how
the program should be built are provided for make in the program's
makefile.

The GNU make tool should be installed on your system because it is
commonly used to simplify the process of installing programs.

%prep
%setup -q -a1
# WARNING: only configure script is patched
%patch0 -p1 -b .no-hires-timestamp

%build
%configure2_5x
%make
# all tests must pass
make check

%install
rm -rf $RPM_BUILD_ROOT/

%makeinstall

ln -sf make $RPM_BUILD_ROOT%_bindir/gmake

# some hand dealing; to remove when the %{name}-pofiles.tar.bz2 is removed
for i in i18n/*.po ; do
  mkdir -p $RPM_BUILD_ROOT/%{_datadir}/locale/`basename $i .po`/LC_MESSAGES
  msgfmt -v -o $RPM_BUILD_ROOT/%{_datadir}/locale/`basename $i .po`/LC_MESSAGES/%{name}.mo $i
done

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info make.info

%preun
%_remove_install_info make.info

%files -f %name.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS COPYING ChangeLog README README.customs SCOPTIONS NEWS
%doc glob/COPYING.LIB glob/ChangeLog
%_bindir/make
%_bindir/gmake
%_mandir/man1/make.1*
%_infodir/make.info*

%changelog
* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 3.80-6sls
- OpenSLS build
- tidy spec

* Fri Jul 25 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.80-5mdk
- Patch0: Don't use high resolution timestamp to nuke librt dep

* Wed Jul 23 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 3.80-4mdk
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
- corrected problem with %preun script

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
