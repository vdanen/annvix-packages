%define name	lilo
%define version 22.5.7.2
%define release 8sls
%define epoch	1

Summary:	The boot loader for Linux and other operating systems.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
Group:		System/Kernel and hardware
License:	MIT
URL:		http://brun.dyndns.org/pub/linux/lilo/
Source:		http://home.san.rr.com/johninsd/pub/linux/lilo/lilo-%{version}.tar.bz2
Source2:	lilo-graphic-pictures.tar.bz2
#ftp://metalab.unc.edu/pub/Linux/system/boot/lilo/lilo-%{version}.tar.bz2
#Source: ftp://lrcftp.epfl.ch/pub/linux/local/lilo/
Patch0:		lilo-21.6-keytab-3mdk.patch.bz2
Patch1:		lilo-disks-without-partitions.patch.bz2
Patch9:		lilo-22.5.1-unsafe-and-default-table.patch.bz2
Patch20:	lilo-22.5.7.2-graphic-makefile.patch.bz2
Patch21:	lilo-22.5.1-graphic.patch.bz2
Patch22:	lilo-22.5.5-mandir.patch.bz2
Patch23:	lilo-22.5.7.2-allgraph.patch.bz2
Patch24:	lilo-22.5.7.2-progress.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	dev86 dev86-devel nasm

PreReq:		/usr/bin/perl
Conflicts:	lilo-doc < 22.5.7.2-6mdk
Exclusivearch:	%{ix86}
Provides:	bootloader

%description
LILO (LInux LOader) is a basic system program which boots your Linux
system.  LILO loads the Linux kernel from a floppy or a hard drive, boots
the kernel and passes control of the system to the kernel.  LILO can also
boot other operating systems.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch9 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1 -b .allgraph
%patch24 -p1 -b .progress

# graphic pictures.
bzip2 -dc %{SOURCE2} | tar xvf -

bzip2 -9 README*

%build
perl -p -i -e "s/-Wall -g/$RPM_OPT_FLAGS/" Makefile
make
(cd doc
make CFLAGS="$RPM_OPT_FLAGS"
dvipdfm -o User_Guide.pdf user.dvi
dvipdfm -o Technical_Guide.pdf tech.dvi
rm -f *.aux *.log *.toc)

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}
make install ROOT=%{buildroot}

install -d %{buildroot}%{_bindir}
mv %{buildroot}%{_sbindir}/* %{buildroot}%{_bindir}

# graphic addons, keep default options for bmp2mdk

#%{__perl} ./bmp2mdk	mode:0x101 \
#			timer:444,458,64+102,64+3 \
#			entry:28,380,0,15,24,22 \
#	<boot8.1.bmp >%{buildroot}/boot/lilo-graphic/message
#%{__perl} ./bmp2mdk	mode:0x101 \
#			timer:63+280,80+358,64+83,64+79 \
#			entry:63+144,80+70,64+84,64+79,9,42 \
#			clear:480,640,64+79 \
#			pos:63,80 \
#	<boot8.2.bmp >%{buildroot}/boot/message-graphic
#%{__perl} ./bmp2mdk	mode:0x103 \
#			timer:425,562,64+70,64+0 \
#			entry:218,174,64+0,64+19,11,55 \
#			clear:600,800,64+70 \
#			pos:0,0 \
#	<boot9.0.bmp >%{buildroot}/boot/message-graphic
#%{__perl} ./bmp2mdk	mode:0x103 \
#			timer:425,562,64+127,64+72 \
#			entry:218,174,64+72,64+22,11,55 \
#			clear:600,800,64+54 \
#			pos:0,0 \
#	<boot9.1.bmp >%{buildroot}/boot/message-graphic
%{__perl} ./bmp2mdk	mode:0x103 \
			timer:357,610,64+126,15 \
			entry:161,144,64+127,15,13,54 \
			progress:405,166,11,14,15 \
			clear:600,800,64+127 \
			pos:0,0 \
	<boot9.2.bmp >%{buildroot}/boot/message-graphic

install bmp2mdk %{buildroot}%{_bindir}/lilo-bmp2mdk

mkdir -p %{buildroot}/%{_mandir}/man{5,8}/
install -m644 manPages/*.5 %{buildroot}/%{_mandir}/man5/
install -m644 manPages/*.8 %{buildroot}/%{_mandir}/man8/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
if [ -f /etc/lilo.conf ]; then

  if [ -L /boot/lilo ]; then

      # upgrading from old lilo boot.b based

      # before:
      # - message is a symlink to either lilo-text/message, lilo-menu/message or lilo-graphic/message
      # - lilo-text/message and lilo-menu/message are created by DrakX (and are usually the same file)
      # - lilo-graphic/message is in the RPM (will be removed by RPM after %post)
      # after:
      # - message-text is the text message
      # - message-graphic is the old lilo-graphic/message

      # transforming the /boot/message symlink in non-symlink
      if [ -e /boot/lilo-text/message ]; then
	  mv -f /boot/lilo-text/message /boot/message-text
      fi 
      if [ -e /boot/lilo-menu/message ]; then
	  mv -f /boot/lilo-menu/message /boot/message-text
      fi

      if [ -e /boot/message-text ]; then
          ln -sf message-text /boot/message
      fi

      # ensuring the right choice is taken

      link=`perl -e 'print readlink("/boot/lilo")'`
      case $link in
        lilo-menu) ;; # chosen by default
        lilo-bmp) ;; # automatically chosen by lilo based on "bitmap=..."
        lilo-graphic)
  	  ln -sf message-graphic /boot/message
          ;; # chosen based on /boot/message containing 0x0E at the beginning
        lilo-text)
          # need a special install=... 
  	  perl -pi -e 's|^install=.*\n||; $_ = "install=text\n$_" if $. == 1' /etc/lilo.conf ;;
        *)
	  echo "ERROR: unknown lilo scheme, it is DROPPED (please tell pixel@mandrakesoft.com)"
	  sleep 1 ;;
      esac

      rm -f /boot/lilo
  fi

  chmod 600 /etc/lilo.conf
  if [ -x /usr/sbin/detectloader ]; then
    LOADER=$(/usr/sbin/detectloader -q)
    if [ "$LOADER" = "LILO" ]; then
      /sbin/lilo > /dev/null
    fi
  fi
fi

%files
%defattr(-,root,root)
%doc README* COPYING
/boot/message-graphic
/boot/diag1.img
/boot/diag2.img
/sbin/*
%{_bindir}/*
%{_mandir}/*/*


%changelog
* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 22.5.7.2-8sls
- Provides: bootloader
- remove %%build_opensls macros
- spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 22.5.7.2-7sls
- OpenSLS build
- tidy spec
- don't build doc with %%build_opensls
- fix BuildReq's

* Thu Sep 18 2003 François Pons <fpons@mandrakesoft.com> 22.5.7.2-6mdk
- added new picture for 9.2 with progress bar integrated inside.
- fixed critical bug of bmp2mdk generating wrong files if both timer
  and progress bar are given.
- added conflicts due to multiple lilo-bmp2mdk defined.

* Thu Sep 18 2003 François Pons <fpons@mandrakesoft.com> 22.5.7.2-5mdk
- fixed critical bug of freeze when an entry is selected by adding a
  progress bar in graphical mode when loading files.

* Wed Sep 03 2003 François Pons <fpons@mandrakesoft.com> 22.5.7.2-4mdk
- fixed to keep graphical mode if kernel uses it, else change to
  text mode.

* Tue Sep 02 2003 François Pons <fpons@mandrakesoft.com> 22.5.7.2-3mdk
- updated with smarter 9.2 pictures correctly handling multiple entries.

* Thu Aug 21 2003 François Pons <fpons@mandrakesoft.com> 22.5.7.2-2mdk
- updated with newer 9.2 pictures.

* Thu Aug 21 2003 Pixel <pixel@mandrakesoft.com> 22.5.7.2-1mdk
- new release

* Mon Aug 18 2003 Pixel <pixel@mandrakesoft.com> 22.5.7-2mdk
- add disks-without-partitions.patch

* Mon Aug 11 2003 Pixel <pixel@mandrakesoft.com> 22.5.7-1mdk
- new release

* Sun Aug  3 2003 Pixel <pixel@mandrakesoft.com> 22.5.6.1-1mdk
- new release (fix bug cause "L 40 40 ..." at boot)

* Tue Jul 29 2003 Pixel <pixel@mandrakesoft.com> 22.5.6-1mdk
- new release
- BuildRequires: dev86-devel (thanks to bluca at comedia dot it)

* Wed Jun 18 2003 Pixel <pixel@mandrakesoft.com> 22.5.5-1mdk
- new release (with images diag1.img and diag2.img)

* Mon May 12 2003 Pixel <pixel@mandrakesoft.com> 22.5.3-1mdk
- new release

* Mon May  5 2003 Pixel <pixel@mandrakesoft.com> 22.5.2-1mdk
- new release

* Mon May  5 2003 Pixel <pixel@mandrakesoft.com> 22.5.1-2mdk
- add "BuildRequires: nasm"

* Wed Apr  2 2003 Pixel <pixel@mandrakesoft.com> 22.5.1-1mdk
- new release (update patches)

* Wed Feb 05 2003 François Pons <fpons@mandrakesoft.com> 22.4.1-2mdk
- fixed picture with smoother dithering.

* Fri Jan 31 2003 Pixel <pixel@mandrakesoft.com> 22.4.1-1mdk
- new release

* Thu Jan 30 2003 François Pons <fpons@mandrakesoft.com> 22.4-2mdk
- new picture for newer distribution.

* Sat Jan 25 2003 Pixel <pixel@mandrakesoft.com> 22.4-1mdk
- new release

* Mon Nov  4 2002 Pixel <pixel@mandrakesoft.com> 22.3.4-1mdk
- new release

* Thu Oct 10 2002 Pixel <pixel@mandrakesoft.com> 22.3.3-1mdk
- new release

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 22.3.2-5mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Aug 02 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 22.3.2-4mdk
- removed duplicated PostScript files.
- PDF documentation instead of PostScript one.

* Fri Jul 19 2002 Pixel <pixel@mandrakesoft.com> 22.3.2-3mdk
- have bmp2mdk in /usr/bin/lilo-bmp2mdk (in lilo-doc)

* Thu Jul 18 2002 François Pons <fpons@mandrakesoft.com> 22.3.2-2mdk
- updated boot image for 9.0.

* Fri Jul 12 2002 Pixel <pixel@mandrakesoft.com> 22.3.2-1mdk
- new release

* Thu Jun 27 2002 Pixel <pixel@mandrakesoft.com> 22.3.1-1mdk
- new release

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 22.3-2mdk
- Nuke egcs requirement
- Patch22: Workaround manpath bug that returns /usr/local/man as first
  man dir (aka Titi woes)

* Mon May 27 2002 Pixel <pixel@mandrakesoft.com> 22.3-1mdk
- new release

* Tue Feb 07 2002 François Pons <fpons@mandrakesoft.com> 22.2-2mdk
- fixed lost part of image on some hardware (i810).
- very small reduction of graphic patch size.

* Wed Feb 06 2002 François Pons <fpons@mandrakesoft.com> 22.2-1mdk
- 22.2.

* Wed Jan 30 2002 François Pons <fpons@mandrakesoft.com> 22.1-5mdk
- extend message file to 512Kb instead of 64Kb.

* Mon Jan 28 2002 François Pons <fpons@mandrakesoft.com> 22.1-4mdk
- removed ghost property on hilited entry.
- modified color of timer and hilited text to be dimer.

* Fri Jan 25 2002 François Pons <fpons@mandrakesoft.com> 22.1-3mdk
- updated graphic patch to allow simple scrolling.

* Fri Jan 25 2002 François Pons <fpons@mandrakesoft.com> 22.1-2mdk
- updated picture.

* Thu Jan 24 2002 François Pons <fpons@mandrakesoft.com> 22.1-1mdk
- changed picture and extended entry height to 15 instead of 7.
- updated graphic patch with 22.1.
- 22.1.

* Wed Jan 09 2002 François Pons <fpons@mandrakesoft.com> 21.7.5-3mdk
- updated graphic patch (newer bmp2mdk and typo updates in README.graphic).
- new 8.2 boot image.

* Sun Dec  9 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 21.7.5-2mdk
- Patch1: fix build, by including linux/genhd.h not linux/fs.h, and
  not including bad defines for older kernels
- s/Serial/Epoch/

* Sun Aug  5 2001 Pixel <pixel@mandrakesoft.com> 21.7.5-1mdk
- new release (how did i miss it?)
- drop the leading 0. from the release number

* Thu Jul 26 2001 François Pons <fpons@mandrakesoft.com> 0.21.7-18mdk
- added another patch from VMWare.

* Tue Jul 24 2001 François Pons <fpons@mandrakesoft.com> 0.21.7-17mdk
- fixed blank chars on timeout boot.
- added patch from VMWare to fix unsupported banked videoram.
- added missing build requires.

* Thu Jul 19 2001 François Pons <fpons@mandrakesoft.com> 0.21.7-16mdk
- new graphic message for next release.

* Tue Jul 03 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.21.7-15mdk
- make /etc/lilo.conf unreadable but for root as it may contain
  passwords. (sly0.21.7-15mdk)

* Tue Jun 19 2001 Pixel <pixel@mandrakesoft.com> 0.21.7-14mdk
- make /boot/lilo-* directories belong to lilo

* Tue Jun 19 2001 Stefan van der Eijk <stefan@eijk.nu> 0.21.7-13mdk
- BuildRequires: tetex-dvips tetex-latex

* Fri Jun 01 2001 François Pons <fpons@mandrakesoft.com> 0.21.7-12mdk
- Reworked graphic patch to include needed tools and README and
  multi stage2 available.
- Moved pictures in a standalone archive.

* Fri Apr 27 2001 François Pons <fpons@mandrakesoft.com> 0.21.7-11mdk
- Created patch to handle more nicely all lilo stage2 (boot.b).

* Sun Apr  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.21.7-10mdk
- Call detectloader with -q.

* Sun Apr  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.21.7-9mdk
- By default don't include the boot.b file if there is no exiting
  boot.b file then link it to boot-menu.b (this allow to keep
  graphical boot menu when upgrading if it set).

* Thu Apr  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.21.7-8mdk
- Reinsert manpages in doc packages.

* Thu Mar 22 2001 François Pons <fpons@mandrakesoft.com> 0.21.7-7mdk
- fixed systematic change to text mode.

* Tue Mar 13 2001 François Pons <fpons@mandrakesoft.com> 0.21.7-6mdk
- modified graphic patch to include mode 0x13 (320x200) and
  true LF interpretation for display.

* Tue Mar  6 2001 Pixel <pixel@mandrakesoft.com> 0.21.7-5mdk
- merge patch from redhat (mainly CCISS)

* Mon Mar 05 2001 François Pons <fpons@mandrakesoft.com> 0.21.7-4mdk
- used new picture by default.

* Thu Mar 01 2001 François Pons <fpons@mandrakesoft.com> 0.21.7-3mdk
- changed graphic patch license to the one used by LILO so BSD.

* Wed Feb 28 2001 François Pons <fpons@mandrakesoft.com> 0.21.7-2mdk
- created graphic patch as in syslinux-graphic but not
  activated by default, use /boot/boot-graphic.b and
  /boot/message-graphic for graphic activation (first sample).

* Mon Feb 26 2001 Pixel <pixel@mandrakesoft.com> 0.21.7-1mdk
- new version

* Wed Jan 24 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.21.6.1-2mdk
- Remove argument parsing patch for the new version.

* Tue Jan  2 2001 Pixel <pixel@mandrakesoft.com> 0.21.6.1-1mdk
- new version

* Thu Nov 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.21.6-5mdk
- Fix argument parsing.

* Tue Nov  7 2000 Pixel <pixel@mandrakesoft.com> 0.21.6-4mdk
- capitalize summary of -doc

* Mon Nov  6 2000 Pixel <pixel@mandrakesoft.com> 0.21.6-3mdk
- fix keytab lilo so that things like "\n" aren't badly remapped (qc-latin1)

* Thu Oct 12 2000 Pixel <pixel@mandrakesoft.com> 0.21.6-2mdk
- fix-segfault-for-floppy-entry.patch

* Tue Oct 10 2000 Pixel <pixel@mandrakesoft.com> 0.21.6-1mdk
- new version

* Fri Sep 29 2000 Pixel <pixel@mandrakesoft.com> 0.21.5.1-4mdk
- fix keytab-lilo so that keycodes > 59 are not taken into account. -> fix the
'.' giving '<' on french keyboard (should not break anything...)

* Mon Sep 25 2000 Pixel <pixel@mandrakesoft.com> 0.21.5.1-3mdk
- merge in redhat's patches
  - fix up "unsafe" <johnsonm@redhat.com>
  - add i2o boot support <johnsonm@redhat.com>
  - patches for Compaqs SA5300 controller <karsten@redhat.de>
  - add bug-fix to not have lilo core-dump on some config files <Florian.LaRoche@redhat.com>
  - work around broken 2.4 kernel headers <pbrown@redhat.com>

* Tue Aug 29 2000 Pixel <pixel@mandrakesoft.com> 0.21.5.1-2mdk
- added requires dev86

* Sun Aug 27 2000 Pixel <pixel@mandrakesoft.com> 0.21.5.1-1mdk
- new version

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 0.21.5-1mdk
- new version

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 0.21.4.4-2mdk
- use detectloader in %%post to know wether to call lilo or not
- BM

* Mon Jun 12 2000 Pixel <pixel@mandrakesoft.com> 0.21.4.4-1mdk
- new version

* Mon May  8 2000 Pixel <pixel@mandrakesoft.com> 0.21.4.3-1mdk
- new version (RAID patches)

* Thu Apr 27 2000 Pixel <pixel@mandrakesoft.com> 0.21.4.2-2mdk
- new version

* Sat Mar 25 2000 Pixel <pixel@mandrakesoft.com> 0.21.4-1mdk
- bzip'ed README
- separated postscript doc
- really is 21-4 (serial added)

* Wed Feb 23 2000 Pixel <pixel@mandrakesoft.com> 0.22-19mdk
- Really is 0.22 (non <<official>> version with EDD enabled)
  (EDD means no more 1024 cylinder problem)

* Fri Feb 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.22-18mdk
- Silly me reuploading and upgrade the ChangeLog.

* Wed Feb 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.22-17mdk
- Add loopdev and second patch (r).

* Tue Oct 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Remove the EBDA patch from zab and put in the EBDA patch
  from the VA Research RPM.  This fixes the EBDA issues.(r)
- Added ONE_SHOT to the compile options so that the lilo
  prompt won't timeout once you hit a key at the boot prompt(r)

* Wed Sep 22 1999 Pixel <pixel@mandrakesoft.com>
- added defattr (no comment)

* Tue Sep 21 1999 Pixel <pixel@mandrakesoft.com>
- patched keytab-lilo.pl (again!) to make it work (better) (changed a regexp)

* Sun Sep 19 1999 Pixel <pixel@mandrakesoft.com>
- added -DONE_SHOT to patch lilo-ebda (that way timeout is disabled as soon as a
  key is pressed)
- patched keytab-lilo.pl to make it work (removed bad suffix .map)

* Sun Aug 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add the patch to boot on Compaq Smart Array 3200.

* Wed Jul 21 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- recommend manual lilo installation if post fails

* Mon Jul 19 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- added turkish description

* Mon Jul 19 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- Add french description from Gregus <gregus@etudiant.net>

* Wed Jun 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Use the ebda patch from VA-Research.

* Thu Jun 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Use -DIGNORECASE -DVARSETUP -DREWRITE_TABLE -DLCF_LARGE_EBDA
  -DLARGE_EBDA by default. LARGE_EBDA is needed for some SMP systems.

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add patch for Mandrake-6.0.
- Add keyab-lilo.pl to the file-list

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- handle RPM_OPT_FLAGS

* Sun Dec  6 1998 Matt Wilson <msw@redhat.com>
- updated to release 0.21
- patched to build on 2.1.x kernels

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- updated to release 0.20
- uses a build root

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- built against glibc
