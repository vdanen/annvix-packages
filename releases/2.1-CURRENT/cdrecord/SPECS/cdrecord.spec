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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
