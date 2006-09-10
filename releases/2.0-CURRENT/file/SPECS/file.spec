#
# spec file for package file
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		file
%define version		4.17
%define release		%_revrel

%define major		1
%define libname		%mklibname magic %{major}

Summary:	A utility for determining file types
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD 
Group:		File tools
URL:		ftp://ftp.astron.com/pub/file/
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
Source1:	magic.mime

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl, libtool, autoconf, zlib-devel

Requires:	%{libname} = %{version}

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.


%package -n %{libname}
Summary:	Shared library for handling magic files
Group:		System/Libraries

%description -n %{libname}
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on.


%package -n %{libname}-devel
Summary:	Development files to build applications that handle magic files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libmagic-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 


%package -n %{libname}-static-devel
Summary:	Static library to build applications that handle magic files
Group:		Development/C
Requires:	%{libname}-devel = %{version}

%description -n %{libname}-static-devel
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"

%configure2_5x \
    --datadir=%{_datadir}/misc
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

cat %{_sourcedir}/magic.mime > %{buildroot}%{_datadir}/misc/magic.mime
ln -sf %{name}/magic %{buildroot}%{_datadir}/misc/magic

install -m 0644 src/file.h %{buildroot}%{_includedir}/ 


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/file
%{_datadir}/misc/*
%{_mandir}/man1/file.1*
%{_mandir}/man4/magic.4*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/file.h
%{_includedir}/magic.h
%{_mandir}/man3/libmagic.3*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

%files doc
%defattr(-,root,root)
%doc README MAINT LEGAL.NOTICE ChangeLog 


%changelog
* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.17
- 4.17
- drop P2
- use the real source
- use %%_sourcdir/file instead of %%{SOURCEx}
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.15
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.15
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.15-1avx
- 4.15
- drop upstream P0

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.14-1avx
- 4.14

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.10-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.10-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.10-2avx
- bootstrap build

* Sun Sep 12 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.10-1avx
- 4.10
- remove P3: similar fix upstream
- spec cleanups

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.03-5avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 4.03-4sls
- minor spec cleanups

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 4.03-3sls
- OpenSLS build
- tidy spec

* Tue Jul 15 2003 Götz Waschk <waschk@linux-mandrake.com> 4.03-2mdk
- rebuild for new rpm

* Thu Jul 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.03-1mdk
- new release
- drop patch 1 (merged upstream)

* Mon Jun  2 2003 Stew Benedict <gbeauchesne@mandrakesoft.com> 4.02-3mdk
- LSB/FHS still want to see magic in %{_datadir}/misc

* Thu Apr  3 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.02-2mdk
- Tighten library dependency since they didn't provide/increase minor
  version number of the libmagic DSO

* Thu Apr  3 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.02-1mdk
- 4.02 (fix symlink test)
- Update Patch1 (zsh) to fix mismerged magic
- Update Patch3 (deps) to make LDFLAGS use libmagic.la

* Wed Apr  2 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.01-2mdk
- Patch3: I want parallel build

* Wed Apr  2 2003 Götz Waschk <waschk@linux-mandrake.com> 4.01-1mdk
- disable parallel build
- add some docs
- use the right configure macro
- rediff all patches (new directory structure)
- libify the package
- new version

* Tue Mar 04 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.41-1mdk
- 3.4.1 (security fixes)

* Mon Feb 17 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.40-1mdk
- new release

* Fri Jan 10 2003 Stew Benedict <sbenedict@mandrakesoft.com> 3.39-3mdk
- LSB/FHS now expects magic in /usr/share/misc

* Tue Jul 23 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.39-2mdk
- patch 2: perl is in /usr/bin

* Tue Jul 23 2002 Aurelien Lemaire <alemaire@mandrakesoft.com> 3.39-1mdk
- New version 3.39

* Fri Jun 21 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.38-2mdk
- Recognize #!/bin/zsh and #!/usr/bin/zsh.

* Tue May 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.38-1mdk
- new release

* Mon Jan 14 2002 Aurelien Lemaire <alemaire@mandraksoft.com> 3.37-1mdk
- 3.37
- Add CFLAGS to handle large files

* Thu Oct 4 2001 DindinX <odin@mandrakesoft.com> 3.36-2mdk
- rpmlint fixes

* Mon Aug 13 2001 DindinX <odin@mandrakesoft.com> 3.36-1mdk
- 3.36
- fixed source url
- removed patchs #0, #3 and #6 (merged upstream)
- removed patch #4 (obsolete)

* Fri May  4 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.35-2mdk
- sanitized specfile (s/Copyright/License, BuildRequires, etc.)
- fixed ELF output string for big endian systems (e.g. PowerPC) [patch6]
- removed patch1: instead, redefine datadir to %_datadir/magic
  As an interesting side effect, the paths in manpages are now correct

* Wed Apr 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.35-1mdk
- Make a new and shiny source.

* Sun Apr  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.34-4mdk
- Merge rh patch.
- Remove broken entry gtkalog detect since it screwed rpm detection.

* Sat Apr  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.34-3mdk
- Make sur to define magic files in /usr/share/magic/magic.

* Fri Mar 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.34-2mdk
- Print debugging information only in verbose mode.

* Thu Mar 15 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.34-1mdk
- new version

* Fri Jan 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.33-2mdk
- ask requested by Chmou move the magic files to its own directory.

* Mon Nov 13 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.33-1mdk
- new and shiny version.

* Mon Sep 18 2000 DindinX <odin@mandrakesoft.com> 3.32-3mdk
- Added missing magic.mime file (thx to Egil)

* Tue Aug 29 2000 DindinX <odin@mandrakesoft.com> 3.32-2mdk
- use %%make macro
- some more BM in the install section

* Mon Aug 07 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.32-1mdk
- new release

* Sun Jul 23 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.31-3mdk
- BM

* Mon Jul 10 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.31-2mdk

- remove old commented commands.
- Stefan van der Eijk <s.vandereijk@chello.nl> did :
	- makeinstall macro
	- macroszifications

* Mon May 15 2000 DindinX <odin@mandrakesoft.com> 3.31-1mdk
- new version 3.31
- removed all unnecessary patches

* Tue Apr 11 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 3.30-1mdk
- new version 3.30
- fix license to BSD

* Thu Mar 23 2000 DindinX <odin@mandrakesoft.com> 3.28-2mdk
- Specs updates, new Group

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- enable SMP build/check
- 3.28 :
	- Remove strip/realmedia patch (is there)
	- Remove sparc patch (perl does better, not need updateing)

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with redhat changes.
- identify ELF stripped files correctly (r).
- use SPARC (not sparc) consistently throughout (r).
- add entries for MS Office files (r).

* Tue Aug 17 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Redhat merge:
	- Thu Aug 12 1999 Jeff Johnson <jbj@redhat.com>
	- diddle magic so that *.tfm files are identified correctly.

* Thu Jul 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Reinserting po translations from MDK5.3.
- Bzip2 patch.
- 3.27.
- Removing unused stuff.

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add patch for realmedia support.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Fri Nov 27 1998 Jakub Jelinek <jj@ultra.linux.cz>
- add SPARC V9 magic.

* Tue Nov 10 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.26.

* Mon Aug 24 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.25.
- detect gimp XCF versions.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 3.24
- buildrooted

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Mon Mar 31 1997 Erik Troan <ewt@redhat.com>
- Fixed problems caused by 64 bit time_t.

* Thu Mar 06 1997 Michael K. Johnson <johnsonm@redhat.com>
- Improved recognition of Linux kernel images.

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
