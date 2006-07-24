#
# spec file for package cpio
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		cpio
%define version 	2.6
%define release 	%_revrel

Summary:	A GNU archiving program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving
URL:		http://www.fsf.org/software/cpio
Source:		ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.bz2
Patch0:		cpio-2.6-mtime.patch
Patch1:		cpio-2.6-svr4compat.patch
Patch2:		cpio-2.6-no-libnsl.patch
Patch3:		cpio-2.6-i18n.patch
Patch4:		cpio-2.6-CAN-1999-1572.patch
Patch5:		cpio-2.6-chmodRaceC.patch
Patch6:		cpio-2.6-dirTraversal.patch
Patch7:		cpio-2.6-compil-gcc4.patch
Patch8:		cpio-2.6-CVE-2005-4268.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo

Requires(post):	info-install
Requires(preun): info-install
Requires:	rmt

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .mtime
%patch1 -p1 -b .svr4compat
%patch2 -p1 -b .no-libnsl
%patch3 -p1 -b .i18n
%patch4 -p0 -b .can-1999-1572
%patch5 -p1 -b .can-2005-1111
%patch6 -p1 -b .can-2005-1229
%patch7 -p0 -b .gcc4
%patch8 -p1 -b .cve-2005-4268

# needed by P4
autoconf


%build
%configure2_5x \
    --bindir=/bin \
    --with-rmt=/sbin/rmt \
    CPPFLAGS=-DHAVE_LSTAT=1

%make
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

# remove unpackaged files
rm -f %{buildroot}%{_mandir}/man1/mt.1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%files -f %{name}.lang
%defattr(-,root,root)
/bin/cpio
%{_infodir}/cpio.*
%{_mandir}/man1/cpio.1*

%files doc
%defattr(-,root,root)
%doc README NEWS AUTHORS ChangeLog


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- fix group

* Fri Feb 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- P8: security fix for CVE-2005-4268

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6-3avx
- require rmt rather than tar (tar provides rmt-tar rather than rmt
  since we don't use alternatives anymore)
- P7: fix build with gcc4 (we don't use it yet, but it doesn't hurt to have)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6-2avx
- bootstrap build (new gcc, new glibc)

* Thu Jul 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6-1avx
- 2.6
- make it require tar rather than /sbin/rmt; tar is a pretty
  safe bet to have installed no matter what
- P2: no need to link with libnsl; from fedora (deaddog)
- P3: LSB compliance (sbenedict)
- do make check
- spec cleanups
- drop unrequired patches and renumber
- P11: security fix for CAN-1999-1572
- P12: security fix for CAN-2005-1111
- P13: security fix for CAN-2005-1229
- add -DHAVE_LSTAT=1 to the CPPFLAGS so that symbolic links are
  not replaced with files or directories but remain symlinks
  (re mdk bugzilla #12970)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-10avx
- bootstrap build

* Wed Feb 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-9avx
- P13: patch to fix CAN-1999-1572

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5-8avx
- now that both tar and rmt can provide rmt, require the file
  rather than the package

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5-7avx
- Annvix build
- require packages not files

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 2.5-6sls
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 2.5-5sls
- OpenSLS build
- tidy spec

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.5-4mdk
- rebuild
- drop Prefix tag
- use %%make macro
- drop unapplied P7

* Sun Nov 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.5-3mdk
- LI18NUX/LSB compliance (patch12, disable patch7 - stdout patch)
- Deal with Installed (but unpackaged) file(s) - mt, rmt, man page

* Thu Jul 25 2002 Daouda LO <daouda@mandrakesoft.com> 2.5-2mdk
- better URL

* Wed Jul 24 2002 Daouda LO <daouda@mandrakesoft.com> 2.5-1mdk
- 2.5 release
- patches  #4(glibc 2_1 build), #5 (long dev), #8 (debian fix) merged upstream
- add URL 

* Sun Jun  2 2002 Stefan van der Eijk <stefan@eijk.nu> 2.4.2-21mdk
- BuildRequires

* Mon Jul  9 2001  Daouda Lo <daouda@mandrakesoft.com> 2.4.2-20mdk
- s|Copyright|License| 

* Mon Jul  9 2001  Daouda Lo <daouda@mandrakesoft.com> 2.4.2-19mdk
- apply RH/Debian patches.
- man updates/fixes 
- more fhs compliant.

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.2-18mdk
- fix bad script

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.2-17mdk
- BM
- more macros

* Tue Jul 11 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.2-16mdk
- clean a lot the spec (macros, install fix by Stefan van der Eijk
  <s.vandereijk@chello.nl>)
- use spechelper

* Sat Jul 08 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 2.4.2-16mdk
- fixed makeinstall problem
- some hassle getting the manpage in the right dir

* Thu Apr 4 2000 Denis Havlik <denis@mandrakesoft.com> 2.4.2-15mdk
- new Group: Archiving/Backup 


* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Specs files tweaks.
- Merge with rh patchs.
- fix infinite loop unpacking empty files with hard links (r).
- stdout chould contain progress information (r).

* Fri Apr  9 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- longlong dev wrong with "-o -H odc" headers (formerly "-oc").

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to compile on glibc 2.1, where strdup is a macro

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump package.
- Don't include /bin/mt -- use the mt from mt-st package.
- Add prereq's

* Tue Jun 30 1998 Jeff Johnson <jbj@redhat.com>
- fix '-c' to duplicate svr4 behavior (problem #438)
- install support programs & info pages

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot
- removed "(used by RPM)" comment in Summary

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- no longer statically linked as RPM doesn't use cpio for unpacking packages
