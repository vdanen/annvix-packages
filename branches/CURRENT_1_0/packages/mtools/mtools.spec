Summary:	Programs for accessing MS-DOS disks without mounting the disks
Name: 		mtools
Version: 	3.9.9
Release: 	2mdk
License: 	GPL
Group: 		File tools
BuildRequires: 	XFree86-devel, texinfo
Source: 	http://www.tux.org/pub/tux/knaff/mtools/%{name}-%{version}.tar.bz2 
Url: 		http://www.tux.org/pub/tux/knaff/mtools/index.html
Buildroot: 	%{_tmppath}/%{name}-root
Patch0: 	mtools-3.9.1-linux.patch.bz2
Patch1: 	mtools-3.9.7-20000619.diff.bz2
Patch2: 	mtools-3.9.6-atari.patch.bz2
Patch4: 	mtools-3.9.8-fs.patch.bz2
Patch5: 	mtools-3.9.9-supermount.patch.bz2
Prereq: 	/sbin/install-info

%description
Mtools is a collection of utilities for accessing MS-DOS files.
Mtools allow you to read, write and move around MS-DOS filesystem
files (normally on MS-DOS floppy disks).  Mtools supports Windows95
style long file names, OS/2 Xdf disks, and 2m disks.

Mtools should be installed if you need to use MS-DOS disks.

%prep
%setup -q
%patch0 -p1 -b .linux
%patch1 -p1 -b .update
%patch2 -p1 -b .atari
%patch4 -p1 -b .compil
%patch5 -p1 -b .supermount

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix} $RPM_BUILD_ROOT%{_sysconfdir}
%makeinstall
/usr/bin/install -c -m 644 mtools.conf $RPM_BUILD_ROOT%{_sysconfdir}
# specific handling for mformat which is setuid root
rm -f $RPM_BUILD_ROOT%{_bindir}/mformat
cp -a $RPM_BUILD_ROOT%{_bindir}/mtools $RPM_BUILD_ROOT%{_bindir}/mformat

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/mtools.conf
%doc COPYING Changelog README Release.notes mtools.texi
%{_bindir}/f*
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

%changelog
* Mon Aug 25 2003 Fran�ois Pons <fpons@mandrakesoft.com> 3.9.9-2mdk
- created patch to release supermount lock if needed.

* Tue Jul 08 2003 Fran�ois Pons <fpons@mandrakesoft.com> 3.9.9-1mdk
- removed now applied patch 20021118.
- 3.9.9.

* Fri Nov 22 2002 Fran�ois Pons <fpons@mandrakesoft.com> 3.9.8-3mdk
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
- use of %configure and %makeinstall
- updated patches

* Fri Mar 24 2000 DindinX <odin@mandrakesoft.com> 3.9.6-5mdk
- Group and spec fixes

* Fri Jan 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.9.6-4mdk
- added a defattr

* Fri Nov 12 1999 Damien Krotkine <damien@mandrakesoft.com>
- Mandrake release

* Sat Aug 07 1999 Bernhard Rosenkr�nzer <bero@linux-mandrake.com>
- 19990729 bugfix
- add patch to allow reading Atari ST disks (am I the only person
  trying to use STonX occasionally???)

* Thu Jul  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 3.9.6
- Prefixing the .spec.

* Sat May 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Remove the 1.44m in mtools.conf (reported by Jacques).

* Wed May 05 1999 Bernhard Rosenkr�nzer <bero@linux-mandrake.com>
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
