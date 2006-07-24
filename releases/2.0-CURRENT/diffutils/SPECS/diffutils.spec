#
# spec file for package diffutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		diffutils
%define version 	2.8.4
%define release 	%_revrel

Summary:	A GNU collection of diff utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/diffutils/
Source:		ftp://ftp.gnu.org/pub/gnu/diffutils-%{version}.tar.bz2
Source1:	%{name}-manpages.tar.bz2
Patch2:		diffutils-2.8.4-i18n.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5

Requires(post):	info-install
Requires(preun): info-install

%description
Diffutils includes four utilities:  diff, cmp, diff3 and sdiff.

  * Diff compares two files and shows the differences, line by line.
  * The cmp command shows the offset and line numbers where two files differ,
    or cmp can show the characters that differ between the two files.
  * The diff3 command shows the differences between three files. Diff3 can be
    used when two people have made independent changes to a common original;
    diff3 can produce a merged file that contains both persons' changes and
    warnings about conflicts.
  * The sdiff command can be used to merge two files interactively.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch2 -p1 -b .i18n


%build
autoconf
%configure
%make PR_PROGRAM=%{_prefix}/bin/pr


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

mkdir -p %{buildroot}%{_mandir}/man1
bzcat %{_sourcedir}/%{name}-manpages.tar.bz2 | tar xf - -C %{buildroot}%{_mandir}/man1/

rm -fr %{buildroot}%{_infodir}/dir
   
%find_lang %{name}


%post 
%_install_info diff.info

%preun
%_remove_install_info diff.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/diff.info*

%files doc
%defattr(-,root,root)
%doc NEWS README


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4
- fix changelog
- really remove docs from the main package

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4-10avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4-9avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4-8avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4-7avx
- requiere packages not files
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.8.4-6sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.8.4-5sls
- OpenSLS build
- tidy spec

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.8.4-4mdk
- rebuild
- use %%make macro
- drop unapplied P1

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4-3mdk
- build release

* Mon Nov 18 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.8.4-2mdk
- LI18NUX/LSB compliance patch
- add installed but not packaged locale files

* Thu Oct 10 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4-1mdk
- new release

* Sun Aug  4 2002 Stefan van der Eijk <stefan@eijk.nu> 2.8.1-3mdk
- BuildRequires: autoconf2.5

* Wed Jul 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.8.1-2mdk
- rpmlint fixes: strange-permission, no-url-tag
- Rebuild with latest gcc3.1

* Mon Apr 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.8.1-1mdk
- Diffutils 2.8.1 hot from the oven (gc).
- Remove the suffix patch (-k option). (if you really need this feature
  please send a patch).
- Obsolete security patch, should no longer be needed.

* Tue Nov 20 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.7-30mdk
- DESTDIR support.

* Sat Aug 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.7-29mdk
- Sanity rebuild for 8.1.
- Run make check.
- s/Copyright/License/;

* Tue May 15 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.7-28mdk
- Minor cosmetic changes to the diff.1 manual page (chmou).

* Thu Apr 19 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.7-27mdk
- put diff.1.bz2 back in since man-pages doesn't supply it anymore

* Wed Jan 10 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.7-26mdk
- fix conflict with man-pages (diff.1.bz2)

* Wed Jan 10 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.7-25mdk
- security fix for insecure tempfiles

* Tue Dec  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.7-24mdk
- Update manpages.
- Add updated patch for -k options.

* Fri Nov 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.7-23mdk
- Add -k option to get a default suffix (Peter Samuelson <peter@cadcamlab.org>).

* Tue Sep 05 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.7-22mdk
- really fix the info page (pxlscks).

* Fri Sep  1 2000 Pixel <pixel@mandrakesoft.com> 2.7-21mdk
- fix info page

* Wed Jul 26 2000 David BAUDENS <baudens@mandrakesoft.com> 2.7-20mdk
- Human readable description

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7-19mdk
- BM
- major spec simplification

* Thu Apr 4 2000 Denis Havlik <denis@mandrakesoft.com> 2.7-18mdk
- new group: Development/Other
- spechelper conform

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add defattr.

* Wed Jun 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- listing man-pages in %%files.

* Fri Apr  9 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Sun Mar 14 1999 Jeff Johnson <jbj@redhat.com>
- add man pages (#831).
- add %%configure and Prefix.

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul 14 1998 Bill Kawakami <billk@home.com>
- included the four man pages stolen from Slackware

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun May 03 1998 Cristian Gafton <gafton@redhat.com>
- fixed spec file to reference/use the %%{buildroot} always

* Wed Dec 31 1997 Otto Hammersmith <otto@redhat.com>
- fixed where it looks for 'pr' (/usr/bin, rather than /bin)

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
