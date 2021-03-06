%define name	tar
%define version	1.14
%define release	1avx

%define rmtrealname	rmt-tar
%define _bindir		/bin

Summary:	A GNU file archiving program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving/Backup
URL:		http://www.gnu.org/software/tar/tar.html
Source:		ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.bz2
Source1:	%{SOURCE0}.sig
Source2:	tar-help2man.bz2
Patch0:		tar-1.14-mdk-sock.patch.bz2
Patch1:		tar-1.14-mdk-scandir.patch.bz2
Patch2:		tar-1.14-mdk-doubleslash.patch.bz2

Buildroot:	%{_tmppath}/%{name}-root

Prereq:		info-install
Provides:	/sbin/rmt
Conflicts:	rmt < 0.4b37

%description
The GNU tar program saves many files together into one archive and
can restore individual files (or all of the files) from the archive.
Tar can also be used to add supplemental files to an archive and to
update or list files in the archive.

Tar includes multivolume support, automatic archive compression/
decompression, the ability to perform remote archives and the
ability to perform incremental and full backups.

You should install the tar package, because you'll find its
compression and decompression utilities essential for working
with files.

%prep
%setup -q
%patch0 -p1 -b .sock
%patch1 -p1 -b .scandir
%patch2 -p1 -b .doubleslash

bzcat %{SOURCE2} > ./help2man
chmod +x ./help2man

%build
%configure2_5x \
	--enable-backup-scripts \
	--bindir=%{_bindir} \
	DEFAULT_RMT_COMMAND="/sbin/rmt"

%make

# thanks to diffutils Makefile rule
(echo '[NAME]' && sed 's@/\* *@@; s/-/\\-/; q' src/tar.c) | (./help2man -i - -S '%{name} %{version}' src/tar ) | sed 's/^\.B info .*/.B info %{name}/' > %{name}.1

make check

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std
ln -sf tar %{buildroot}%{_bindir}/gtar
install -D -m644 tar.1 %{buildroot}%_mandir/man1/tar.1

# rmt is provided by rmt ...
mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_libexecdir}/rmt %{buildroot}/sbin/%rmtrealname

%find_lang %{name}

%triggerpostun -- rmt < 0.4b37
if test ! -e /sbin/rmt; then
    %{_sbindir}/update-alternatives --install /sbin/rmt /sbin/%rmtrealname 10
fi


%post
%{_sbindir}/update-alternatives --install /sbin/rmt rmt /sbin/%rmtrealname 10
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%postun
%{_sbindir}/update-alternatives --remove rmt /sbin/%rmtrealname

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc NEWS THANKS AUTHORS README ChangeLog* COPYING TODO
%{_bindir}/tar
%{_bindir}/gtar
%{_sbindir}/backup
%{_sbindir}/restore
/sbin/%rmtrealname
%{_libexecdir}/backup.sh
%{_libexecdir}/dump-remind
%{_infodir}/*.info*
%{_mandir}/man?/*


%changelog
* Fri Aug 13 2004 Vincent Danen <vdanen@annvix.org> 1.14-1avx
- 1.14
- patch policy
- sync with cooker (deaddog):
  - drop P0, use help2man to generate manpage
  - drop P105 (-y/-I), since -j/--bzip2 is stabilized and well known now
  - drop P8, P10: merged upstream
  - rediff and renumber remaining patches
  - install scripts as well
  - use alternatives for rmt

* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 1.13.25-14avx
- PreReq: info-install rather than /sbin/install-info
- PreReq: rmt rather than /sbin/rmt
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.13.25-13sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 1.13.25-12sls
- OpenSLS build
- tidy spec

* Wed Jul 23 2003 Per ?yvind Karlsen <peroyvind@sintrax.net> 1.13.25-11mdk
- rebuild

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.13.25-10mdk
- fix unpackaged files
- fix strange-permission

* Mon Nov 04 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 1.13.25-9mdk
- Remove service menu

* Sat Oct 26 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 1.13.25-8mdk
- Add konqueror service menu. Now when we right click on a tar file in konqueror we can untar it.

* Thu Oct 10 2002 Vincent Danen <vdanen@mandrakesoft.cmo> 1.13.25-7mdk
- fix traversal bug (P11) (re: MDKSA-2002:066)

* Wed Aug 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.13.25-6mdk
- add url (Yura Gusev)

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.13.25-5mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Aug 09 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.25-4mdk
- Automake fix.

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.13.25-3mdk
- Automated rebuild in gcc3.1 environment

* Mon Apr 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.13.25-2mdk
- resync with rh-1.3.25-4
- remove merged patches
- fix archive corruption in rare cases [Patch10]

* Sat Oct 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.25-1mdk
- The latest in tar innovations the all-new 1.13.25.

* Sat Sep 08 2001 David BAUDENS <baudens@mandrakesoft.com> 1.13.22-3mdk
- Fix broken patch which allows to use -y and -I option

* Wed Sep 05 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.22-2mdk
- -I is back.

* Sat Sep 01 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.22-1mdk
- A new and shiny tar to fix a security problem in the old and ugly tar.
- Obsolete some of the patches, it seems that they are no longer needed.
- Depend on librt again, until I have time to get around this.

* Tue Aug 28 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.19-7mdk
- s/Copyright/License/;

* Sat Aug 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.19-6mdk
- Sanity build before 8.1.
- RH patch merge: 
  - Don't depend on librt.
  - Bettter AC_DEFINE in acinclude.m4.
  - Return correctly in src/incremen.c.
  
* Thu Mar 15 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.13.19-5mdk
- fix info installation

* Thu Jan 18 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.19-4mdk
- I'm dumb so fix the wrong spelling in the -{y,I} filter warning.

* Wed Jan 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.19-3mdk
- put back the I filter also, dammit I really need some coffee before I work.

* Mon Jan 15 2001 Geoff <snailtalk@mandrakesoft.com> 1.13.19-2mdk
- put back the y filter, damn, how can I be so careless...

* Sun Jan 14 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.19-1mdk
- new and shiny source.

* Thu Dec  7 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.13.18-4mdk
- Run automated tests at build time
- Use optflags.

* Fri Nov 17 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.18-3mdk
- break compatibility with stock GNU tar and Solaris, but print and
  appropriate warning. :(

* Thu Nov 16 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.18-2mdk
- Red Hat patch merge a.k.a shamelessly rip patches.
- port the y_filter patch, plus add a warning with fprintf() to stderr
  indicating it is deprecated. (David Baudens, Pixel.)

* Wed Nov 15 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.13.18-1mdk
- Remove exit code patch. It's no longer needed.
- bump up version.
- remove patch1. Using -y for bzip2 is obsolete!

* Mon Sep 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.13.17-7mdk
- New exit code patch from rh.

* Sun Sep 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.13.17-6mdk
- Fix exit code (rh).

* Thu Jul 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.13.17-5mdk
- BM, add doc

* Thu Jul 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.13.17-4mdk
- BM.
- More macros.

* Tue Jun 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.13.17-3mdk
- Use makeinstall macros.

* Wed Mar 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.13.17-2mdk
- Clean up specs.
- Adjust groups.
- Merge rh patchs.

* Thu Feb 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.13.17-1mdk
- Make -y alias to -I and document it as obsoltes.
- 1.13.17.

* Tue Jan 11 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.13.11-3mdk
- call configure with LINGUAS unset.

* Mon Nov  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Reinserting -y support patchs.

* Wed Oct 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Split: back to the tar stable version for cassini.

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 1.13.13.

* Thu Oct 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 1.13.12.

* Fri Sep 03 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 1.13.11

* Fri Aug 20 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 1.13.10

* Fri Aug 13 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 1.3.6

* Tue Jul 22 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 1.13.5

* Thu Jul 15 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 1.13.2
- french description 

* Tue Jul 12 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.de>
- 1.13.1

* Fri Jul 09 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.3.
- Patch to handle bzip2.

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Update to 1.2.64011.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- add de locale
- some spec tweaks
- bzip2 man/info pages
- Mandrake adaptions
- update to 1.12.64010 to get the -y (--bzip2) option

* Mon Mar 08 1999 Michael Maher <mike@redhat.com>
- added patch for bad name cache. 
- FIXES BUG 320

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- add /usr/bin/gtar symlink (change #421)

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump.
- Turn on nls.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 1.11.8 to 1.12
- various spec file cleanups
- /sbin/install-info support

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu May 29 1997 Michael Fulbright <msf@redhat.com>
- Fixed to include rmt
