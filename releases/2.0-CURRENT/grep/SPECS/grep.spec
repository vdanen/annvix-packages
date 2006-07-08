#
# spec file for package grep
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		grep
%define version 	2.5.1a
%define release 	%_revrel

%define _bindir 	/bin

Summary:	The GNU versions of grep pattern matching utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File tools
URL:		http://www.gnu.org/software/grep/grep.html
Source:		ftp://ftp.gnu.org/pub/gnu/grep/%{name}-%{version}.tar.bz2
Patch1:		grep-2.5.1-i18n-0.1.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext pcre-devel texinfo

Requires:	libpcre

%description
The GNU versions of commonly used grep utilities.  Grep searches one or
more input files for lines which contain a match to a specified pattern
and then prints the matching lines.  GNU's grep utilities include grep,
egrep and fgrep.  


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1 -b .i18n


%build
%configure2_5x \
    --exec-prefix=/ \
    --without-included-regex
%make

make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{_infodir}

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
/bin/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc AUTHORS THANKS TODO NEWS README ChangeLog


%changelog
* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1a
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1a
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1a
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1a-1avx
- 2.5.1a
- rebuild against new pcre

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1-12avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1-11avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1-10avx
- bootstrap build

* Thu Jun 24 2004 Vincent Danen <vdanen@opensls.org> 2.5.1-9avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 2.5.1-8sls
- Requires: libpcre, not /lib/libpcre.so.0

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 2.5.1-7sls
- drop unapplied P0
- drop BuildRequires: bison
- use %%makeinstall_std
- drop S10 and S11
- updated P1 from openi18n (re: abel)

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.5.1-6sls
- minor spec cleanups
- get rid of doc package (who needs info pages for grep anyways?!?)

* Sat Jan 04 2004 Vincent Danen <vdanen@opensls.org> 2.5.1-5sls
- requires pcre-devel not libpcre-devel (for amd64)

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 2.5.1-4sls
- OpenSLS build
- tidy spec

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5.1-3mdk
- Requires: /%{_lib}/libpcre.so.0

* Sat Jul 19 2003 Götz Waschk <waschk@linux-mandrake.com> 2.5.1-2mdk
- some cleanup
- buildrequires texinfo
- drop buildrequirement on recode

* Wed Jul 16 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.5.1-1mdk
- 2.5.1

* Tue Jan 14 2003 François Pons <fpons@mandrakesoft.com> 2.5-7mdk
- split info into separate grep-doc package.

* Mon Nov 11 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.5-6mdk
- LI18NUX/LSB compliance (patch1)

* Fri Aug 16 2002 Götz Waschk <waschk@linux-mandrake.com> 2.5-5mdk
- fix german translation

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5-4mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Sun Jul 21 2002 Stefan van der Eijk <stefan@eijk.nu> 2.5-3mdk
- BuildRequires

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5-2mdk
- Costlessly make check in %%build stage
- Rebuild with gcc3.1

* Tue Apr  2 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.5-1mdk
- final version
- temporary disable patch #0 (factorize code) because integrated
  upstream, but not remove it from SRPM since it should be reverted
  soon (it offends the GNU standard)

* Sun Feb  3 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.5-0.f.3mdk
- requires a libpcre0 release that has its lib in /lib

* Fri Feb  1 2002 Stefan van der Eijk <stefan@eijk.nu> 2.5-0.f.2mdk
- BuildRequires

* Thu Jan 24 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.5-0.f.1mdk
- unecessary to duplicate "grep" for "egrep" and "fgrep", apply a
  patch to factorize code [Patch #0], saves 200 kbytes in /
- base on RH's grep-2.5-1.f.5.i386.rpm, to get a coloured grep :-), and
  the recent Bero work on grep
  - i18n patches seem integrated upstream
- fix no-url-tag

* Thu Jan 24 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.4.2-10mdk

* Wed Sep 12 2001 Warly <warly@mandrakesoft.com> 2.4.2-9mdk
- change distribution tag

* Sun May 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.2-8mdk
- Fix the Chinese locale msgfmt problem with gettext (Abel Cheung).

* Tue May 01 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.2-7mdk
- Add yet another i18n patch.
- We have programs with the Chinese po files. Comment that out for the time
  being (too lazy to fix).

* Sun Jan 28 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.2-6mdk
- put in Chinese translations.

* Tue Sep 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-5mdk
- Fix %post/%postun (thanks flepied).

* Mon Sep 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-4mdk
- Add patch to get the i18n like the old behavior (rh).

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 2.4.2-3mdk
- use find_lang

* Wed Jul 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-2mdk
- BM.
- Macros.
- CLean-up.

* Thu Mar 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-1mdk
- Clean up specs.
- Adjust groups.
- 2.4.2.

* Tue Mar  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-1mdk
- 2.4.1.

* Fri Dec  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- adjust URL.
- 2.4.

* Tue Nov 02 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Prereq install-info.

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.
- Fix buid as user.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to grep 2.3, added install-info %post/%preun for info

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Sat May 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.0 to 2.1
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
