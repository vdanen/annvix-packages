%define name	findutils
%define version	4.2.17
%define release	2avx

Summary:	The GNU versions of find utilities (find, xargs, and locate)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File tools
URL:		http://www.gnu.org/software/findutils/findutils.html
Source0:	ftp://alpha.gnu.org/gnu/findutils-%{version}.tar.bz2
Source1:	updatedb.cron.bz2
Patch0:		findutils-4.2.15-no-locate.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	automake1.8

Prereq:		info-install

%description
The findutils package contains programs which will help you locate
files on your system.  The find utility searches through a hierarchy
of directories looking for files which match a certain set of criteria
(such as a filename pattern).  The locate utility searches a database
(create by updatedb) to quickly find a file matching a given pattern.
The xargs utility builds and executes command lines from standard
input arguments (usually lists of file names generated by the find
command).

You should install findutils because it includes tools that are very
useful for finding things on your system.

%prep
%setup -q
%patch0 -p1 -b .no-locate

# needed by P0
ACLOCAL=aclocal-1.9 AUTOMAKE=automake-1.9 autoreconf --force --install

%build
%configure2_5x
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir %{buildroot}/bin
mv %{buildroot}%{_bindir}/find %{buildroot}/bin
ln -sf ../../bin/find %{buildroot}%{_bindir}/find

%{find_lang} %{name}

%post
%_install_info find.info

%preun
%_remove_install_info find.info

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc NEWS README
/bin/find
%{_bindir}/find
%{_bindir}/xargs
%{_mandir}/man1/find.1*
%{_mandir}/man1/xargs.1*
%{_infodir}/find.info*

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 4.2.17-2avx
- bootstrap build

* Sat Mar 05 2005 Vincent Danen <vdanen@annvix.org> 4.2.17-1avx
- 4.2.17
- P4: don't build locate
- remove S1 as it's not even used
- update %%configure/%%makeinstall macros; use automake1.8

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 4.1.20-4avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 4.1.20-3sls
- minor spec cleanups

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 4.1.20-2sls
- OpenSLS build
- tidy spec

* Mon Aug 18 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1.20-1mdk
- new release

* Thu Jul 24 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 4.1.7-6mdk
- rebuild
- use %%make macro

* Thu Feb 20 2003 Giuseppe Ghib� <ghibo@mandrakesoft.com> 4.1.7-5mdk
- Merged with RH Patch 53857 and usage (Patch1, Patch2).

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1.7-4mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Thu Jan 17 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 4.1.7-3mdk
- move /usr/bin/find to /bin/find (for mkinitrd)
- fix no-url-tag

* Wed Jul  4 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 4.1.7-2mdk
- remove all %%ifarch alpha conditionals, make alpha standard

* Fri Jun 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.1.7-1mdk
- 4.1.7.

* Mon Jan 22 2001 Francis Galiegue <fg@mandrakesoft.com> 4.1.6-1mdk
- 4.1.6 (was 4.1.1!)
- patch fixing galore

* Mon Aug 14 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 4.1.1-8mdk
- fix the %post script, geoffrey sucks

* Sun Jul 23 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.1.1-7mdk
- BM
- macroszification
- bzip2 the cron source to make rpmlint happy

* Thu Apr 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.1.1-6mdk
- Don't apply gcc-2.95 patch for alpha.

* Sat Apr 08 2000 Geoffrey Lee <snailtalk@linux-mandrake.com>
- alpha fix
- fix illegal macro name

* Wed Mar 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.1.1-4mdk
- Merge rh patchs.
- Clean up specs.
- Upgrade groups.

* Wed Nov 24 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix find on alpha.

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Fri Aug 13 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 4.1.1

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add the xargs patch overflow from RedHat.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Mon Feb  8 1999 Jeff Johnson <jbj@redhat.com>
- remove further updatedb remnants (#1072).

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- added patch for glibc21

* Mon Nov 16 1998 Erik Troan <ewt@redhat.com>
- removed locate stuff (as we now ship slocate)

* Wed Jun 10 1998 Erik Troan <ewt@redhat.com>
- updated updatedb cron script to not look for $TMPNAME.n (which was
  a relic anyway)
- added -b parameters to all of the patches

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Mar 09 1998 Michael K. Johnson <johnsonm@redhat.com>
- make updatedb.cron use mktemp correctly
- make updatedb use mktemp

* Sun Nov 09 1997 Michael K. Johnson <johnsonm@redhat.com>
- nobody should own tmpfile
- ignore /net

* Wed Nov 05 1997 Michael K. Johnson <johnsonm@redhat.com>
- made updatedb.cron do a better job of cleaning up after itself.

* Tue Oct 28 1997 Donald Barnes <djb@redhat.com>
- fixed 64 bit-ism in getline.c, patch tacked on to end of glibc one

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- added patch for glibc 2.1

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot support

* Tue Oct 14 1997 Michael K. Johnson <johnsonm@redhat.com>
- made updatedb.cron work even if "nobody" can't read /root
- use mktemp in updatedb.cron

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- added missing info pages
- uses install-info

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built with glibc

* Mon Apr 21 1997 Michael K. Johnson <johnsonm@redhat.com>
- fixed updatedb.cron
