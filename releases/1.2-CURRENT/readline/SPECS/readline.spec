#
# spec file for package readline
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		readline
%define version		5.0
%define	release		%_revrel

%define major		5
%define libname		%mklibname %{name} %{major}

Summary:	Library for reading lines from a terminal
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Source:		ftp://ftp.gnu.org/pub/gnu/readline/readline-%{version}.tar.bz2
Patch2:		readline-4.3-guard.patch
Patch3:		readline-4.1-outdated.patch
Patch4:		readline-4.3-fixendkey.patch
Patch5:		readline-4.1-resize.patch
Patch11:	ftp://ftp.cwru.edu/pub/bash/readline-5.0-patches/readline50-001
Patch12:	ftp://ftp.cwru.edu/pub/bash/readline-5.0-patches/readline50-002
Patch13:	ftp://ftp.cwru.edu/pub/bash/readline-5.0-patches/readline50-003
Patch14:	ftp://ftp.cwru.edu/pub/bash/readline-5.0-patches/readline50-004
Patch15:	ftp://ftp.cwru.edu/pub/bash/readline-5.0-patches/readline50-005
Patch16:	readline-4.3-no_rpath.patch
Patch17:	readline-read-e-segfault.patch
Patch18:	readline-wrap.patch

Buildroot:	%{_buildroot}/%{name}-%{version}

%description
The "readline" library will read a line from the terminal and return it,
allowing the user to edit the line with the standard emacs editing keys.
It allows the programmer to give the user an easier-to-use and more
intuitive interface.


%package -n %{libname}
Summary:	Shared libraries for readline
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked to readline.


%package -n %{libname}-devel
Summary:	Files for developing programs that use the readline library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{name}-devel
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	%{_lib}readline4-devel

%description -n %{libname}-devel
The "readline" library will read a line from the terminal and return it,
using prompt as a prompt.  If prompt is null, no prompt is issued.  The
line returned is allocated with malloc(3), so the caller must free it when
finished.  The line returned has the final newline removed, so only the
text of the line remains.


%prep
%setup -q
%patch2 -p1 -b .guard
%patch3 -p1 -b .outdated
%patch4 -p1 -b .fixendkey
%patch5 -p1 -b .resize
%patch11 -p0 -b .001
%patch12 -p0 -b .002
%patch13 -p0 -b .003
%patch14 -p0 -b .004
%patch15 -p0 -b .005
%patch16 -p1 -b .no_rpath
%patch17 -p1 -b .read-e-segfault
%patch18 -p1 -b .wrap


libtoolize --copy --force


%build
export CFLAGS="%{optflags}"
%configure2_5x \
    --with-curses=ncurses
perl -p -i -e 's|-Wl,-rpath.*||' shlib/Makefile
%make static shared


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall install-shared

# put all libs in /lib because some packages need it
# before /usr is mounted
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/*.so* %{buildroot}/%{_lib}
ln -s ../../%{_lib}/lib{history,readline}.so %{buildroot}%{_libdir}
for i in history readline; do
    ln -s ../%{_lib}/lib$i.so.4 %{buildroot}/%{_lib}/lib$i.so.4.1
    ln -s ../%{_lib}/lib$i.so.4 %{buildroot}/%{_lib}/lib$i.so.4.2
done


# The make install moves the existing libs with a suffix of old. Urgh.
rm -f %{buildroot}/%{_lib}/*.old

perl -p -i -e 's|/usr/local/bin/perl|/usr/bin/perl|' doc/texi2html


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname}-devel
%_install_info history.info
%_install_info readline.info

%preun -n %{libname}-devel
%_remove_install_info history.info
%_remove_install_info readline.info

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc CHANGELOG CHANGES INSTALL MANIFEST README USAGE
%doc doc examples support
%{_mandir}/man*/*
%{_infodir}/*info*
%{_includedir}/readline
%{_libdir}/lib*.a
%{_libdir}/lib*.so
/%{_lib}/*so


%changelog
* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0-1avx
- 5.0
- sync with mdk 5.0-2mdk:
  - sync with fedora patches
  - drop P1 (unapplied), P100/P101 (merged upstream)
- throw in a conflicts on libreadline4-devel

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3-13avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3-12avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3-11avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3-10avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.3-9sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 4.3-8sls
- OpenSLS build
- tidy spec

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3-7mdk
- pfff, libification

* Wed Jul 09 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 4.3-6mdk
- Rebuild

* Mon May 26 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 4.3-5mdk
- Rebuild

* Mon Aug 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.3-4mdk
- fix non working repeating with '.' command [P100]
- fix segfault on c-arrows [P101]

* Wed Jul 24 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.3-3mdk
- Add provides as well.

* Wed Jul 24 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.3-2mdk
- Provide compatibility back to 4.2.
- Remove the chmod 755 for the shared lib. It should be ok to just have
  the readable bit set, except for ld-linux.so.2 (or maybe libc.so.6 as well).

* Tue Jul 23 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.3-1mdk
- new release
- rediff patches 2 and 4
- fix gwenole brain damage :
	o old changelogs whose version got updated on each upload
	o old changelogs whose version is garbage

* Thu Jun 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2a-3mdk
- Rpmlint fixes: strange-permission, hardcoded-library-path
- Libtoolize to get updated config.guess

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2a-2mdk
- Automated rebuild in gcc3.1 environment

* Mon Nov 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.2a-1mdk
- The shiny 4.2a hot from the oven.

* Sun Aug 26 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.2-4mdk
- Readline seems to be installed using mode 644. Hmm. Interesting.

* Sat Aug 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.2-3mdk
- Apply RH cplusplus patch.
- Sanity build for 8.1.

* Tue May 22 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.2-2mdk
- Apply updated fixendkey patch, ripped proudly and shamelessly from RH.

* Tue Apr 10 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.2-1mdk
- Update to the new and shiny source: version 4.2.

* Sun Mar 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.1-15mdk
- Apply resize patch. <mlord@pobox.com>.
- Don't make this relocatable.

* Thu Mar 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.1-14mdk
- check for arithmetic overflow (rh).
- mark the man page as currently out-of-date (rh).
- fix reading of end key termcap value (@7 is correct, was kH) (rh).

* Thu Dec 14 2000 Geoffrey lee <snailtalk@mandrakesoft.com> 1.4.13mdk
- i18n-ize readline. (Andrew Lee <andrew@cle.linux.org.tw>)

* Sat Dec 09 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.1-12mdk
- revert back to old name.

* Mon Nov 27 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.1-11mdk
- fix bad dependencies. (Dadou.)
- provides libreadline-devel.

* Sat Nov 25 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.1-10mdk
- new library naming scheme.

* Tue Aug 29 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.1-9mdk
- fix the rpm scripts. (fcrozat@mandrakesoft.com)

* Wed Jul 26 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.1-8mdk
- macrosifications
- rebuild for BM

* Mon Jun 12 2000 Pixel <pixel@mandrakesoft.com> 4.1-7mdk
- add .so's in /usr/lib for -devel
- move .a's in /usr/lib

* Mon Jun 12 2000 Pixel <pixel@mandrakesoft.com> 4.1-6mdk
- move doc to -devel (was partially done, hurk), that way, no more prerequisite
on shell.

* Fri Jun  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.1-5mdk
- move libraries in /lib.

* Fri Apr  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.1-4mdk
- s|/usr/local/bin/perl|/usr/bin/perl|;

* Fri Apr 07 2000 Christopher Molnar <molnarc@mandrakesoft.com> 4.1-3mdk
- add documentation, support and examples

* Thu Mar 23 2000 Pixel <pixel@mandrakesoft.com> 4.1-2mdk
- remove rluserman install-info

* Thu Mar 23 2000 Pixel <pixel@mandrakesoft.com> 4.1-1mdk
- new version
- much cleanup
- patch for strange buggy Makefile
- remove the trigger, i prefer require

* Tue Feb  8 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0-8mdk
- Make sure to have the *so in the %files(>#751).

* Sun Feb  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0-7mdk
- Librairies in /usr/lib no binaries on /bin/ or /sbin need
  libreadline.(#751).

* Sun Feb 06 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Leave libraries in /usr/lib/

* Tue Nov 09 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix wrong link (#426).

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Build Release.

* Sun Jul 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.de>
- move dynamic libraries to /lib rather than /usr/lib - a dynamically linked
  primary shell depends on them to run...
- Install info pages in %trigger -- info - readline has to be installed
  before info because bash depends on it.

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adptation.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- set compatibility links + provides for older versions, like those
  used in Red Hat 6.0
- add de locale

* Wed Mar 10 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- relink with ncurses 5.0

* Sat Dec  5 1998 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- bzip2 info/man pages
- use ncurses rather than termcap

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.2.1

* Wed May 06 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- don't package /usr/info/dir

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- devel package moved to Development/Libraries

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- added proper sonames

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- updated to readline 2.1

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc
