%define name	unzip
%define version 5.50
%define release 10sls
%define src_ver 550

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		Archiving/Compression
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
Source0:	ftp://ftp.icce.rug.nl/infozip/src/%{name}%{src_ver}.tar.bz2
Patch0:		unzip541-patent-and-copyright-clean.patch.bz2
Patch1:		unzip542-size-64bit.patch.bz2
Patch2:		unzip-5.50-dotdot.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
unzip will list, test, or extract files from a ZIP archive, commonly found
on MS-DOS systems. A companion program, zip, creates ZIP archives; both
programs are compatible with archives created by PKWARE's PKZIP and
PKUNZIP for MS-DOS, but in many cases the program options or default
behaviors differ.

This version also has encryption support.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1 -b .dotdot

%build
%ifarch %{ix86}
%make -ef unix/Makefile linux CF="$RPM_OPT_FLAGS -Wall -I. -DASM_CRC" CC=gcc LD=gcc AS=gcc AF="-Di386" CRC32=crc_gcc
%else
%make -ef unix/Makefile linux_noasm CF="$RPM_OPT_FLAGS -Wall -I."
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

ln -sf unzip zipinfo
for i in unzip funzip unzipsfx zipinfo;	do install $i $RPM_BUILD_ROOT%{_bindir}; done
install unix/zipgrep $RPM_BUILD_ROOT%{_bindir}

for i in man/*.1; do install -m 644 $i $RPM_BUILD_ROOT%{_mandir}/man1/; done

cat > README.IMPORTANT.MANDRAKE << EOF
This version of unzip is a stripped-down version which doesn't include
the "unreduce" and "unshrink" algorithms. The first one is subject to
a restrictive copyright by Samuel H. Smith which forbids its use in
commercial products; and Unisys claimed a patent ("Welsh patent") on the 
second one (while their licensing would seem to mean that an
extractor-only program would not be covered).

Since the rest of the code is copyrighted by Info-Zip under a BSD-like
license, this Mandrake package is covered by this license.

Please note that currently, default compilation of the Info-Zip
distribution also excludes the unreduce and unshrink code.

Please contact MandrakeSoft at <bugs@linux-mandrake.com> if you have
any problems regarding this issue.
EOF



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BUGS COPYING.OLD Contents History.* INSTALL README ToDo WHERE README.IMPORTANT.MANDRAKE
%doc proginfo/
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 5.50-10sls
- OpenSLS build
- tidy spec

* Sat Aug 16 2003 Vincent Danen <vdanen@mandrakesoft.com> 5.50-9mdk
- use a better security patch

* Fri Jul 18 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 5.50-8mdk
- rebuild

* Fri Jul 04 2003 Vincent Danen <vdanen@mandrakesoft.com> 5.50-7mdk
- P2: security fix

* Fri Jun 06 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 5.50-6mdk
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

