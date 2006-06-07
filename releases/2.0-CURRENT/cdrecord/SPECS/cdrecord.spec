#
# spec file for package cdrecord
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		cdrecord
%define version 	2.01.01a03
%define release 	%_revrel
%define epoch		4

%define archname	cdrtools

%define mkisofs_ver	2.01.01
%define mkisofs_rel	%{release}
%define mkisofs_epoch	1

Summary:	A command line CD/DVD-Recorder
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Archiving
URL:		http://cdrecord.berlios.de/old/private/cdrecord.html
Source:		ftp://ftp.berlios.de/pub/cdrecord/%{archname}-%{version}.tar.bz2
Patch0:		cdrecord-2.01-CAN-2004-0806.patch
Patch6:		cdrtools-2.01.01-CAN-2005-0866.patch
Patch10:	cdrtools-2.01.01a03-dvd.patch
Patch11:	cdrtools-2.01a28-o_excl.patch
Patch12:	cdrtools-2.01a27-writemode.patch
Patch13:	cdrtools-2.01.01a03-rawio.patch
Patch14:	cdrtools-2.01.01a03-warnings.patch
Patch15:	cdrtools-2.01.01a01-scanbus.patch
Patch16:	cdrtools-2.01.01a03-rezero.patch
Patch17:	cdrtools-2.01.01-scsibuf.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libpcap-devel

Requires:	mkisofs
Obsoletes:	cdrecord-dvdhack =< 4:2.01-0.a15.2mdk
Provides:	cdrecord-dvdhack = %{epoch}:%{version}-%{release}

%description
Cdrecord allows you to create CDs on a CD-Recorder (SCSI/ATAPI).
Supports data, audio, mixed, multi-session and CD+ discs etc.


%package devel
Summary:	The libschily SCSI user level transport library
Group:		Development/C

%description devel
The cdrecord distribution contains a SCSI user level transport
library.  The SCSI library is suitable to talk to any SCSI device
without having a special driver for it.

Cdrecord may be easily ported to any system that has a SCSI device
driver similar to the scg driver.


%package -n mkisofs
Summary:	Creates an image of an ISO9660 filesystem
Version:	%{mkisofs_ver}
Release:	%{mkisofs_rel}
Epoch:		%{mkisofs_epoch}
Group:		Archiving

%description -n mkisofs
This is the mkisofs package.  It is used to create ISO 9660
file system images for creating CD-ROMs. Now includes support
for making bootable "El Torito" CD-ROMs.


%package isotools
Summary:	Collection of ISO file related tools
Group:		Archiving

%description isotools
The following tools are included: isodebug, isodump, isoinfo,
and isovfy.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{archname}-%{version}
%patch0 -p1 -z .can-2004-0806
%patch6 -p1 -z .can-2005-0866
%patch10 -p1 -z .dvd
#%patch13 -p1 -z .rawio
%patch14 -p1 -z .warnings
%patch15 -p1 -z .scanbus
%patch16 -p1 -z .rezero
%patch17 -p1 -z .scsibuf


%build
ln -sf i586-linux-cc.rul RULES/ia64-linux-cc.rul
ln -sf i586-linux-cc.rul RULES/x86_64-linux-cc.rul
ln -sf i586-linux-cc.rul RULES/amd64-linux-cc.rul
ln -sf i686-linux-cc.rul RULES/athlon-linux-cc.rulf

perl -pi -e 's|/usr/src/linux/include|/usr/include|' DEFAULTS/Defaults.linux
perl -pi -e 's|^KX_ARCH:=.*|XK_ARCH:=  %{_target_cpu}|' RULES/mk-gmake.id

./Gmake

mkdir mkisofs-doc
cp -a mkisofs/{COPYING,ChangeLog,TODO,README.*} mkisofs-doc/
cp -a doc/mkisofs.ps mkisofs-doc/


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

./Gmake "INS_BASE=%{buildroot}/%{_prefix}" install MANDIR=share/man

rm -f %{buildroot}%{_bindir}/cdda2wav
rm -f %{buildroot}%{_mandir}/man1/cdda2wav.1*
rm -f %{buildroot}%{_mandir}/man1/cdda2ogg.1*

# Move libraries to the right directories
[[ "%{_lib}" != "lib" ]] && \
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%attr(0755,root,cdwriter) %{_bindir}/cdrecord
%attr(755,root,cdwriter) %{_bindir}/devdump
%attr(755,root,cdwriter) %{_bindir}/scgcheck
%attr(0750,root,cdwriter) %{_bindir}/readcd
%attr(755,root,cdwriter) %{_bindir}/skel
%attr(755,root,cdwriter) %{_sbindir}/rscsi
%attr(644,root,root) %{_mandir}/man1/cdrecord.1*
%attr(644,root,root) %{_mandir}/man1/readcd.1*
%attr(644,root,root) %{_mandir}/man1/scgcheck.1*
%attr(644,root,root) %{_mandir}/man5/makefiles.5*
%attr(644,root,root) %{_mandir}/man5/makerules.5*
%attr(644,root,root) %{_mandir}/man8/isoinfo.8*

%files devel
%defattr(-,root,root)
%attr(644,root,root) %{_libdir}/*.a
%attr(644,root,root) %{_includedir}/*.h

%files -n mkisofs
%defattr(-,root,root)
%{_bindir}/mkisofs
%{_bindir}/mkhybrid
%attr(644,root,root) %{_mandir}/man8/mkisofs.8*
%attr(644,root,root) %{_mandir}/man8/mkhybrid.8*

%files isotools
%defattr(-,root,root)
%attr(755,root,cdwriter) %{_bindir}/isodump
%attr(755,root,cdwriter) %{_bindir}/isodebug
%attr(755,root,cdwriter) %{_bindir}/isoinfo
%attr(755,root,cdwriter) %{_bindir}/isovfy

%files doc
%doc Changelog README* AN-* mkisofs-doc


%changelog
* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.01.01a03
- add -doc subpackage
- rebuild with gcc4
- fix groups some more

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.01.01a03
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.01.01a03
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.01.01a03
- Obfuscate email addresses and new tagging
- Uncompress patches
- remove unneeded prereq on rpm-helper

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01.01a03-1avx
- 2.01.01a03
- rediff P6
- fix url
- normalize version and release
- sync most mandrake patches
- cdrecord and readcd are no longer suid

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-0.a38.5avx
- rebuild against new libpcap

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-0.a38.4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-0.a38.3avx
- rebuild

* Wed Apr 20 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-0.a38.2avx
- P6: security patch for CAN-2005-0866

* Tue Sep 07 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.01-0.a38.1avx
- 2.0.1alpha38
- apply security fix for CAN-2004-0806
- don't apply P3; needs 2.6 kernel support?
- sync with cooker 2.01-0.a38.1mdk (warly):
  - fix format syntax problem in command line
  - use glibc kernel headers
  - remove a get_configuration which was disabling DMA on some burners,
    based on a CJ Kucera suggestion
  - default to ATA probing in scanbus if no SCSI devices found
  - fix DVD+R detection on some burners
  - add -dvd in version
  - does not display ATA bus devices if dev= is passed with scanbus
    (needed by xcdroast DVD patch)
  - fix DVD+RW formating
  - fix arch detection to use %%_target_cpu 
  - get inspiration from Red Hat patch to open with E_EXCL to lock the device
    and prevent some broken burners to interupt the burning when magicdev, for
    example, poll the device
  - fix burning speed multiplier for DVD
  - fix bad dvd extension added to wrong place
  - does not fisplay the burning mode warning
  - fix a typeo in command line parsing (thanks to Stephen Beahm)
  - add speed selection support in DVD mode
  - fix DVD+RW formating when done for the first time
  - fix speed selection on LG burner
  - fix speed factor when burning CD in a DVD burner
  - add a warning to scanbus when the ATA bus is selected
  - new package: isotools; with ISO files related commands
  - add Couriousous patch to keep rawio capabilities to be able to burn as
   user with linux 2.6.8
  - remove some warnings

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.01-0.a18.6avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 2.01-0.a18.5sls
- remove %%prefix
- minor spec cleanups
- get rid of .ps docs

* Fri Feb 06 2004 Vincent Danen <vdanen@opensls.org> 2.01-0.a18.4sls
- remove %%build_opensls macro
- group cdwriter is already in setup; not needed here
- remove icons

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.01-0.a18.3sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to not build cdda2wav

* Thu Aug 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.01-0.a18.2mdk
- Clean-up never used bits, older code is available in CVS ;-)
- Remove arch-fix, i.86-linux-* are linked altogether to i586-linux-*

* Mon Aug 11 2003 Warly <warly@mandrakesoft.com> 4:2.01-0.a18.1mdk
- new version
  Rscsi:
    -   Security update. Forbid to write arbitrary debug files, only allow
        a debug file name that has been configured in /etc/default/rscsi.
        Writing arbitrary files with a siud root program could be used to become
        root on a local machine if you are already logged into that local machine.


* Mon Jun 23 2003 Warly <warly@mandrakesoft.com> 4:2.01-0.a16.1mdk
- new version (main changes):
  Readcd:
    -	New option fs=# (same syntax as with cdrecord fs=#) to allw the
	user to set the maximum transfer size even in non-interactive mode.
	This may help is the OS (as it has been the case for Solaris 9 x86)
	reports a wrong maximum DMA size or there is a bug in libscg.
    -	Speed printing with meshpoints=# now is based on 1000 bytes == 1 kb
	as documented in the SCSI standard.
    -	New option -factor will cause the read speed values to be printed
	be based on the single speed of the current medium. This is only
	possible if readcd is able to find out the current medium type.

* Mon Jun 23 2003 Warly <warly@mandrakesoft.com> 4:2.01-0.a15.6mdk
- Better note phrasing (thanks to Michael Bushey)
- Try to display better error message when DVD image is too big.

* Thu Jun 19 2003 Warly <warly@mandrakesoft.com> 4:2.01-0.a15.5mdk
- add "-dvd" in version so that k3b knows it is a DVD capable cdrecord

* Mon Jun 16 2003 Warly <warly@mandrakesoft.com> 4:2.01-0.a15.4mdk
- add "Note:" in front of each line to show that it is an unofficial 
  version in order to have a easier parsing in xcdroast
- improve the DVD patch not to have any interaction with CD recording 
  (fix this packet writing setting with an quite ugly workarroud)

* Mon Jun 16 2003 Warly <warly@mandrakesoft.com> 4:2.01-0.a15.3mdk
- merge DVD code into standard cdrecord

* Fri Jun 06 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.01-0.a15.2mdk
- increase epoch to permit upload for all arch (warly sucks)

* Mon Jun  2 2003 Warly <warly@mandrakesoft.com> 2.01-0.a15.1mdk
- new version (main changes):
  Libscg: 
   - Fixed another printf buffer vulnerability in scsi-remote.c
  Cdrecord:
   - Restructured the main program of cdrecord so that cdrecord overall
     behaves smilar to before when cue sheets are used.
     e.g. cdrecord -eject cuefile=xxx did only eject the disk instead of
     first writing and then ejecting.
   - CD-Text handling reworked:

* Fri May 30 2003 Warly <warly@mandrakesoft.com> 2.01-0.a14.2mdk
- try to fix dvd patch

* Thu May 15 2003 Warly <warly@mandrakesoft.com> 2.01-0.a14.1mdk
- new version (main changes):
Mkisofs (By Jörg Schilling and James Pearson j.pearson@ge.ucl.ac.uk):
-	New options -XA & -xa
	-XA	Generate XA iso-directory attributes with original owner and mode information.
	-xa	Generate XA iso-directory attributes with rationalized owner and mode information (user/group == 0).
-	Try to support files >= 2 GB.
Cdrecord:
-	Fixed a bug that caused cdrecord not to abort if Tracks with unknown length are present in RAW write mode.
-	Track parsing completely restructured to allow new features. One of the features is to write audio CDs from a pipe,
-	Cdrecord now resets euid to the uid of the caller (if called suid root) before it opens data files.
-	Allow cdrecord to copy audio CDs from a pipe from cdda2wav without using an intermediate file on disk.
       To copy an audio CD  from  a  pipe  (without  intermediate
       files), first run
           cdda2wav dev=1,0 -vall cddb=0 -info-only
       and then run
           cdda2wav dev=1,0 -no-infofile -B -Oraw - | cdrecord dev=2,0 -v -dao -audio -useinfo -text *.inf
-	New option -abort allows you to send a write abort sequence to a drive.
-	New 'xio' module allows to open a file virtually more than once to
	support CDRWIN CUE sheets in cdrecord.

* Thu Apr 10 2003 Warly <warly@mandrakesoft.com> 2.1-0.a09.1mdk
- new version (main changes):
Rscsi: Support for IPv6
Mkisofs:
  -	Second attempt to support ISO-9660:1999 (Version 2) via -iso-level 4
  -	isoinfo is now able to recognise ISO-9660:1999 
  -	Abort with a warning message if the total size of the image data
	created by mkisofs would differ from the size printed by -print-size
  -	UDF now uses the same 'now' timestamp as the ISO-9660 part of the FS.
  -	New Stream File feature and new options: -stream-file-name and 	-stream-media-size
	star -c . | mkisofs -stream-media-size 333000 | cdrecord dev=b,t,l -dao tsize=333000s -
  -	The final padding that is added by default is now 150 sectors
	which is the required size of the track post gap on a CD.
  -	Inter partition paddin is now only choosen to make the next partition
	start on a sector number that is a multiple of 16.
  -	isoinfo now also prints root directory extent # in debug mode
  -	First step to allow mkisofs to support Kodak Photo CD and
	Kodak Picture CD format
  -	insoinfo now prints the ISO-9660 directory flags.
  -	Now using character code translation for 8 Bit characters that
	are used with -iso-level 4 (ISO-9660-1999).
Cdrecord:
  -	Workaround for broken Firmware for LG (Lucky Goldstar) drives.
  -	Man page now correctly describes the data formats used with -xa1 & -xa2
  -	Trying to catch SIGHUP to aviod hung recorders after people close X windows by accident
  -	Trying to print hints if the SCSI error core looks like a buffer underrun occured.
  -	First TAO writing support for the Matsushita CW-7501
  -	New option -setdropts to allow cdrecord to set driver specific parameters and exit.
  -	Added support to disable/enable the Plextor PowerRec feature. Use driveropts=forcespeed
  -	Added support to enable/disable the Plextor SpeedRead feature. Use driveropts=speedread
  -	Added support to enable/disable the Plextor SingleSession feature. Use driveropts=singlesession
  -	Added support to enable/disable the Plextor Hide CD-R feature. Use driveropts=hidecdr
  -	Added reading out "real" Burn-Proof counter for Plextor drives.
  -	Try to do a more correct job when doing Buffer Underun estimation counts.
  -	Make the explicit Buffer underrun error checking work for Plextor drives too.
  -	Fixed the command line parser for driveropts= parameters.
  -	Now also supporting SAO/DAO write mode for the CW-7501
  -	New option -lock (similar to -load) that loads the media but leaves the drive in locked status.
  -	New driver interface to allow SAO recording for the CW-7501
  -	Removed the internal implication that -packet is a TAO write mode.
Readcd:
  -	First (hacky) implementation of a way to meter the read speed
	as a function of the disk location modeled after a idea from
	Markus Plail <cdrecord@gitteundmarkus.de>
	Call:
		readcd dev=b,t,l meshpoints=1000 > outfile
	then
		gnuplot
		gnuplot> plot "outfile" w l   or    replot "outfile" w l
Cdda2wav (By Heiko Eißfeldt heiko@hexco.de):
  -	old Toshiba's usable again
  -	Multisession Non-CD-Extra disks now work again
	Now also a lot more broken disks are readable again.

* Mon Jan 06 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0-2mdk
- add cdda2ogg

* Thu Dec 26 2002 Warly <warly@mandrakesoft.com> 3:2.0-1mdk
- new version

* Wed Nov 27 2002 Warly <warly@mandrakesoft.com> 3:1.11-0.a40.1mdk
- new version

* Wed Nov 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.11-0.a39.2mdk
- Fix %%doc, make it lib64 aware
- Add correct RULES links for x86-64 and ia64

* Fri Nov 15 2002 Warly <warly@mandrakesoft.com> 1.11-0.a39.1mdk
- new version

* Wed Oct 16 2002 Warly <warly@mandrakesoft.com> 1.11-0.a37.1mdk
- new version

* Thu Sep 12 2002 Warly <warly@mandrakesoft.com> 1.11-0.a33.1mdk
- new version

* Mon Sep  2 2002 Warly <warly@mandrakesoft.com> 1.11-0.a32.1mdk
- new version

* Mon Aug 26 2002 Warly <warly@mandrakesoft.com> 1.11-0.a31.1mdk
- new version

* Tue Aug 20 2002 Warly <warly@mandrakesoft.com> 1.11-0.a30.1mdk
- new version

* Wed Aug 14 2002 Warly <warly@mandrakesoft.com> 1.11-0.a29.2mdk
- add cdwriter group creation for cdrecord and cdda2wav

* Tue Aug 13 2002 Warly <warly@mandrakesoft.com> 1.11-0.a29.1mdk
- new version

* Wed Jul 31 2002 Warly <warly@mandrakesoft.com> 1.11-0.a28.1mdk
- new version

* Mon Jul 22 2002 Warly <warly@mandrakesoft.com> 1.11-0.a27.1mdk
- new version

* Wed Jul 17 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.11-0.a26.4mdk
- added missed readcd manpage to %%files list.

* Wed Jul 17 2002 Warly <warly@mandrakesoft.com> 1.11-0.a26.3mdk
- add a disclaimer on Joerg Schilling's request

* Mon Jul 15 2002 Warly <warly@mandrakesoft.com> 1.11-0.a26.2mdk
- fix dvd build

* Mon Jul  8 2002 Warly <warly@mandrakesoft.com> 1.11-0.a26.1mdk
- new version

* Mon Jun 03 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.11-0.a24.1mdk
- new release

* Mon May 13 2002 Warly <warly@mandrakesoft.com> 1.11-0.a23.1mdk
- new version

* Thu Apr 18 2002 Daouda LO <daouda@mandrakesoft.com> 1.11-0.a21.1mdk
- 1.11-0.a21.1mdk

* Thu Apr  4 2002 Warly <warly@mandrakesoft.com> 1.11-0.a20.1mdk
- new version

* Wed Mar 27 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.11-0.a19.1mdk
- new release
- alter spec file so that we've only one place to alter on update

* Wed Mar 27 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.11-0.a18.2mdk
- bzip2 sources
- let athlon optimised build be possible

* Wed Mar 20 2002 Warly <warly@mandrakesoft.com> 1.11-0.a18.1mdk
- new version

* Thu Feb 28 2002 Warly <warly@mandrakesoft.com> 1.11-0.a15.2mdk
- change mkisofs permission to standard ones

* Tue Feb 26 2002 Warly <warly@mandrakesoft.com> 1.11-0.a15.1mdk
- new version

* Tue Feb 12 2002 Warly <warly@mandrakesoft.com> 1.11-0.a14.1mdk
- new version

* Fri Feb  1 2002 Warly <warly@mandrakesoft.com> 1.11-0.a13.4mdk
- add new package cdrecord-dvdhack with DVD support

* Tue Jan 29 2002 Warly <warly@mandrakesoft.com> 1.11-0.a13.3mdk
- change cdda2wav to 755

* Mon Jan 28 2002 Warly <warly@mandrakesoft.com> 1.11-0.a13.2mdk
- change permission of cdda2wav to 6755 to make it works.

* Fri Jan 25 2002 Daouda LO <daouda@mandrakesoft.com> 1.11-0.a13.1mdk
- patch level a13

* Mon Jan  7 2002 Warly <warly@mandrakesoft.com> 1.11-0.a12.1mdk
- new version

* Thu Aug  2 2001 Warly <warly@mandrakesoft.com> 1.10-2mdk
- real version of mkisofs

* Tue Apr 24 2001 Warly <warly@mandrakesoft.com> 1.10-1mdk
- 1.10

* Tue Apr 10 2001 Warly <warly@mandrakesoft.com> 1.10-0.1.a18mdk
- devel version

* Fri Mar 02 2001 Francis Galiegue <fg@mandrakesoft.com> 1.9-5mdk

- Fix build on ia64

* Mon Jan 29 2001 Daouda Lo <daouda@mandrakesoft.com> 1.9-4mdk
- back to version 1.9 ("xcdroast don't work for OTHER VERSION than 1.9 ")-> big warly sux.
  
* Sat Sep  2 2000 Till Kamppeter <till@mandrakesoft.com> 1.9-3mdk
- To make X-CD-Roast 0.98 working for non-root users made following
  executables SGID cdwriter:

    readcd
    mkisofs
    mkhybrid

  and the following both SUID root and SGID cdwriter

    cdrecord
    cdda2wav

  All these executable access to /dev/scd? and /dev/sg? devices which
  are accessable for the group cdwriter. cdrecord and cdda2wav have real
  time scheduling and memory locking capabilities which needs them running
  SUID root. The author of these programs has implemented security measures
  to run this programs safely with these privileges.
- Set permissions so that the user who wants to burn must be member of
  "cdwriter" group.

* Fri Jul 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.9-2mdk
- change version of sub package mkisofs since it has been upgraded

* Fri Jul 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.9-1mdk
- new release, BM

* Fri Jun  2 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.8.1-4mdk
- Fix buffer overflow (yoann).

* Mon May 29 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.8.1-3mdk
- no more nasty i686-pc-linux-gnu, now uses %{ _target_cpu } 
- fixed some file not found

* Wed May 03 2000 Warly <warly@mandrakesoft.com> 1.8.1-2mdk
- add serial for upgrade

* Thu Apr 27 2000 Warly <warly@mandrakesoft.com> 1.8.1-1mdk
- 1.8.1

* Tue Apr 4 2000 Warly <warly@mandrakesoft.com> 1.8.1a03-2mdk
- correct group, remove the other 

* Sat Mar 25 2000 Warly <warly@mandrakesoft.com> 1.8.1a03-1mdk
- new group: Archiving/Other/Cd burning 
- 1.8.1a03

* Thu Mar  9 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.8a29-5mdk
- Remove ugly mknod in %post, move them to dev package (#78).
- Remove ugly groupadd in %pre already in setup package (#78)

* Fri Jan 14 2000 Francis Galiegue <francis@mandrakesoft.com>

- one-liner fix to libscg/scg/scgcmd.h
- gcc defines __sparc__, not __sparc nor sparc

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Grhh fix building as user.

* Sun Nov 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Mon Sep 20 1999 Bernhard Rosenkränzer <bero@linux-mandrake.com>
- 1.8a29
- Prereq /usr/sbin/groupadd

* Mon Sep 13 1999 Daouda LO <daouda@mandrakesoft.com>
- 1.8a27

* Sat Aug 14 1999 Bernhard Rosenkränzer <bero@mandrakesoft.de>
- 1.8a24

* Mon Aug 09 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- mkisofs was missing a Summary line...

* Fri Jul 16 1999 Bernhard Rosenkränzer <bero@mandrakesoft.de>
- 1.8a23

* Wed Jul 07 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- inc %{release} just to be safe

* Wed Jul 07 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- cdrecord should be sgid
- out of the rpm ready devices

* Tue Jul 06 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build for new environement (VER: 3mdk).

* Mon May 17 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 1.8a22
- Make use of group cdwriter (as introduced in xcdroast)
- move device creation here (used to be in xcdroast, which is nonsense).
- spec fixes
- add xcdroast (-x) patch to mkisofs

* Sat May 01 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Update to 1.8a20

* Wed Mar 10 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- 1.8a19
- create mkisofs and cdda2wav packages, add readcd to main RPM

* Sun Feb 7 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- 1.8a16

* Tue Dec 8 1998 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- start with FM release 1
- bzip2 man page

* Mon Nov 30 1998 Ryan Weaver <ryanw@infohwy.com>
  [cdrecord-1.8a13-1]
- Updated to 1.8a1
- NEW features of cdrecord-1.8a13:
- First Advent: First separate scg library ;-)
	Currently only the low level and mid level transport stuff
- corrected error detection code in scsierrs.c to fix
	- missing NULL ptr at end of CCS error table
	- <= -> < problem for invalid sense code vs. vendor uniqe sense code

* Fri Nov 27 1998 Ryan Weaver <ryanw@infohwy.com>
  [cdrecord-1.8a12-1]
- Updated to 1.8a12
- NEW features of cdrecord-1.8a12:
- Fixed a typo in scsitransp.c that prevented compilation
	on some Linux releases.

* Wed Nov 25 1998 Ryan Weaver <ryanw@infohwy.com>
  [cdrecord-1.8a11-1]
- Upadted to 1.8a11
- Got patch from Jörg Schilling <schilling@fokus.gmd.de>
  to compile on linux.
- NEW features of cdrecord-1.8a11:
- Starting with official support for SCO Openserver 5
	NOTE: You will need to have a CD in the closed tray of the 
	drive otherwise cdrecord is not able to open the device.
- Fixed a bug in scsi-sco.c that prevented compilation.
- Added DEFAULTS files for SCO
- Fixed the autoconf detection stuff for major()/minor()
- Fixed the autoconf detection stuff for not working mlockall() on SCO/HP-UX
- Fixed mkisofs-1.12b4/diag/isoinfo.c to allow compilation on SCO
- New S_IS*() macros to allow compilation on OS/2 with missing S_IFBLK
- Added a static configuration for VMS
- Some fixes that are needed for VMS
- Added a file cdrecord/build_all.com to compile cdrecord on VMS
- Fixed isnan() code to fit SCO Openserver and VMS
- Incorporating now an experimental version of cdda2wav-0.95beta08
	Report problems to: heiko@colossus.escape.de
- NOTE: cdda2wav and mkisofs are not included in cdrecord rpm.

* Fri Nov 20 1998 Ryan Weaver <ryanw@infohwy.com>
  [cdrecord-1.8a10-1]
- Updated to 1.8a10
