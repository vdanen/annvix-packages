#
# spec file for package unzip
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		unzip
%define version 	5.52
%define release 	%_revrel
%define src_ver 	552

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		Archiving
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
Source0:	ftp://ftp.icce.rug.nl/infozip/src/%{name}%{src_ver}.tar.bz2
Patch1:		unzip542-size-64bit.patch
Patch2:		unzip-5.52-CAN-2005-2475.patch
Patch3:		unzip-5.52-CVE-2005-4667.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
unzip will list, test, or extract files from a ZIP archive, commonly found
on MS-DOS systems. A companion program, zip, creates ZIP archives; both
programs are compatible with archives created by PKWARE's PKZIP and
PKUNZIP for MS-DOS, but in many cases the program options or default
behaviors differ.

This version also has encryption support.


%prep
%setup -q
%patch1 -p0
%patch2 -p1 -b .can-2005-2475
%patch3 -p1 -b .cve-2005-4667

%build
%ifarch %{ix86}
%make -ef unix/Makefile linux CF="-DLZW_CLEAN %{optflags} -Wall -I. -DASM_CRC" CC=gcc LD=gcc AS=gcc AF="-Di386" CRC32=crc_gcc
%else
%make -ef unix/Makefile linux_noasm CF="-DLZW_CLEAN %{optflags} -Wall -I."
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}

ln -sf unzip zipinfo
for i in unzip funzip unzipsfx zipinfo;	do install $i %{buildroot}%{_bindir}; done
install unix/zipgrep %{buildroot}%{_bindir}

for i in man/*.1; do install -m 0644 $i %{buildroot}%{_mandir}/man1/; done

cat > README.IMPORTANT.ANNVIX << EOF
This version of unzip is a stripped-down version which doesn't include
the "unreduce" and "unshrink" algorithms. The first one is subject to
a restrictive copyright by Samuel H. Smith which forbids its use in
commercial products; and Unisys claimed a patent ("Welsh patent") on the 
second one (while their licensing would seem to mean that an
extractor-only program would not be covered).

Since the rest of the code is copyrighted by Info-Zip under a BSD-like
license, this Annvix package is covered by this license.

Please note that currently, default compilation of the Info-Zip
distribution also excludes the unreduce and unshrink code.
EOF


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc BUGS COPYING.OLD Contents History.* INSTALL README ToDo WHERE README.IMPORTANT.ANNVIX
%doc proginfo/
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- fix group

* Sat Mar 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- P3: security fix for CVE-2005-4667

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Oct 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.52-2avx
- P2: fix for CAN-2005-2475

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.52-1avx
- 5.52
- drop P0 and define LZW_CLEAN instead (waschk)
- drop P2; fixed upstream

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.50-15avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.50-14avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.50-13avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.50-12avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 5.50-11sls
- minor spec cleanups
- s/MANDRAKE/OPENSLS/ for important README

* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 5.50-10sls
- OpenSLS build
- tidy spec

* Sat Aug 16 2003 Vincent Danen <vdanen@mandrakesoft.com> 5.50-9mdk
- use a better security patch

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 5.50-8mdk
- rebuild

* Fri Jul 04 2003 Vincent Danen <vdanen@mandrakesoft.com> 5.50-7mdk
- P2: security fix

* Fri Jun 06 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 5.50-6mdk
- use %%make macro
- use $RPM_OPT_FLAGS for other archs too

* Thu Apr 24 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 5.50-5mdk
- fix missing stuff in %%doc section thx to stefan's robot

* Mon Nov 04 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 5.50-4mdk
- Remove service menu

* Sat Oct 26 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 5.50-3mdk
- Add konqueror service menu. now when we right click we can unzip zipped file

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.50-2mdk
- Automated rebuild in gcc3.1 environment

* Wed Mar 20 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 5.50-1mdk
- new version
- patch to correctly display sizes and ratios when archives is more than
  2 Gbytes

* Fri Sep 28 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 5.42-1mdk
- new version

* Thu Sep 13 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 5.41-6mdk
- excluse unreduce and unshrink code for copyright and patent issues
  (actually this is done by default with current unzip distribution),
  clarify licensing with a Mandrake specific README file, and change
  license (it's BSD-like actually now)

* Tue Sep 11 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 5.41-5mdk
- rebuild
- packager

* Mon Jan 15 2001 Francis Galiegue <fg@mandrakesoft.com> 5.41-4mdk
- Fix summary
- Fix titi-sucks English
- Fix files list

* Tue Aug 22 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.41-3mdk
- fix descrip sinde latest unzip has crypto stuff
- fix url

* Wed Jul 19 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.41-2mdk
- BM
- use more macros
- make it short-circuit compliant :-)

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.41-1mdk
- bzip2 source
- new release
- use %%{_mandir} macro for future FHS compliancy
- fix spec because of file moves in source tarball

* Mon Apr 03 2000 Jerome Martin <jerome@mandrakesoft.com> 5.40-4mdk
- spec-helper cleanup
- fix group

* Sun Nov 28 1999 Pixel <pixel@linux-mandrake.com>
- non-intel adaptation (thanks to Stefan van der Eijk)
- cleanup (was it really mandrake adapted?!)

* Wed Nov 10 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- build release.

* Mon Aug 23 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 5.40
- ix86 optimizations and various spec cleanings

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 5)

* Thu Dec 17 1998 Michael Maher <mike@redhat.com>
- built for 6.0

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Erik Troan <ewt@redhat.com>
- builds on non i386 platforms

* Mon Oct 20 1997 Otto Hammersmith <otto@redhat.com>
- updated the version

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

