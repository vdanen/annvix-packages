#
# spec file for package mtools
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mtools
%define version		3.9.9
%define release		%_revrel

Summary:	Programs for accessing MS-DOS disks without mounting the disks
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		File Tools
URL: 		http://www.tux.org/pub/tux/knaff/mtools/index.html
Source: 	http://www.tux.org/pub/tux/knaff/mtools/%{name}-%{version}.tar.bz2 
Patch0: 	mtools-3.9.1-linux.patch
Patch1: 	mtools-3.9.7-20000619.diff
Patch2: 	mtools-3.9.6-atari.patch
Patch4: 	mtools-3.9.8-fs.patch
Patch5: 	mtools-3.9.9-supermount.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires: 	texinfo

Requires(post):	info-install
Requires(preun): info-install

%description
Mtools is a collection of utilities for accessing MS-DOS files.
Mtools allow you to read, write and move around MS-DOS filesystem
files (normally on MS-DOS floppy disks).  Mtools supports Windows95
style long file names, OS/2 Xdf disks, and 2m disks.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .linux
%patch1 -p1 -b .update
%patch2 -p1 -b .atari
%patch4 -p1 -b .compil
%patch5 -p1 -b .supermount


%build
%configure --without-x
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix} %{buildroot}%{_sysconfdir}
%makeinstall
/usr/bin/install -c -m 644 mtools.conf %{buildroot}%{_sysconfdir}
# specific handling for mformat which is setuid root
rm -f %{buildroot}%{_bindir}/mformat
cp -a %{buildroot}%{_bindir}/mtools %{buildroot}%{_bindir}/mformat


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/mtools.conf
%{_bindir}/l*
%{_bindir}/ma*
%{_bindir}/mb*
%{_bindir}/mc*
%{_bindir}/md*
%attr(04755,root,root) %{_bindir}/mformat
%{_bindir}/mi*
%{_bindir}/mk*
%{_bindir}/ml*
%{_bindir}/mm*
%{_bindir}/mp*
%{_bindir}/mr*
%{_bindir}/ms*
%{_bindir}/mt*
%{_bindir}/mx*
%{_bindir}/mz*
%{_bindir}/t*
%{_bindir}/u*
%{_mandir}/*/*
%{_infodir}/%{name}.*

%files doc
%defattr(-,root,root)
%doc COPYING Changelog README Release.notes mtools.texi


%changelog
* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9-9avx
- correct the buildroot

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9-8avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9-7avx
- rebuild

* Sat Jan 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9-6avx
- build without X support

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9-5avx
- Require packages not files
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 3.9.9-4sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 3.9.9-3sls
- OpenSLS build
- tidy spec

* Mon Aug 25 2003 François Pons <fpons@mandrakesoft.com> 3.9.9-2mdk
- created patch to release supermount lock if needed.

* Tue Jul 08 2003 François Pons <fpons@mandrakesoft.com> 3.9.9-1mdk
- removed now applied patch 20021118.
- 3.9.9.

* Fri Nov 22 2002 François Pons <fpons@mandrakesoft.com> 3.9.8-3mdk
- added official patch 20021118.
- added patch to allow compilation of the above (linux/fs.h).

* Fri Oct  5 2001 DindinX <odin@mandrakesoft.com> 3.9.8-2mdk
- rebuild

* Mon May 28 2001 DindinX <odin@mandrakesoft.com> 3.9.8-1mdk
- 3.9.8

* Fri Jan 12 2001 David BAUDENS <baudens@mandrakesoft.com> 3.9.7-5mdk
- BuildRequires: texinfo

* Wed Aug 30 2000 DindinX <odin@mandrakesoft.com> 3.9.7-4mdk
- use noreplace for mtools.conf
- use sysconfdir instead of /etc

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.9.7-3mdk
- automatically added BuildRequires

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.9.7-2mdk
- BM
- let spechelper strip binaries

* Mon Jun 19 2000 DindinX <odin@mandrakesoft.com> 3.9.7-1mdk
- 3.9.7
- use of %%configure and %makeinstall
- updated patches

* Fri Mar 24 2000 DindinX <odin@mandrakesoft.com> 3.9.6-5mdk
- Group and spec fixes

* Fri Jan 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.9.6-4mdk
- added a defattr

* Fri Nov 12 1999 Damien Krotkine <damien@mandrakesoft.com>
- Mandrake release

* Sat Aug 07 1999 Bernhard Rosenkränzer <bero@linux-mandrake.com>
- 19990729 bugfix
- add patch to allow reading Atari ST disks (am I the only person
  trying to use STonX occasionally???)

* Thu Jul  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 3.9.6
- Prefixing the .spec.

* Sat May 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Remove the 1.44m in mtools.conf (reported by Jacques).

* Wed May 05 1999 Bernhard Rosenkränzer <bero@linux-mandrake.com>
- Mandrake adaptions
- 3.9.5

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- patch to make the texi sources compile
- fix the spec file group and description
- fixed floppy drive sizes

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0
- fixed invalid SAMPLE_FILE configuration file

* Wed Sep 02 1998 Michael Maher <mike@redhat.com>
- Built package for 5.2.
- Updated Source to 3.9.1.
- Cleaned up spec file.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to 3.8

* Tue Oct 21 1997 Otto Hammersmith
- changed buildroot to /var/tmp, rather than /tmp
- use install-info

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Apr 17 1997 Erik Troan <ewt@redhat.com>
- Changed sysconfdir to be /etc

* Mon Apr 14 1997 Michael Fulbright <msf@redhat.com>
- Updated to 3.6

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
