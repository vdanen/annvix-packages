%define name	grub
%define version 0.93
%define release 6sls

Summary:	GRand Unified Bootloader
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.gnu.org/software/grub/
Source0:	ftp://alpha.gnu.org/gnu/grub/%{name}-%{version}.tar.bz2
Patch0:		grub-0.5.96.1-ezd.patch.bz2
Patch1:		grub-0.5.96.1-init-config-end--prepatch.patch.bz2
Patch2:		grub-0.90-i18n-messages-and-keytable2.patch.bz2
Patch3:		grub-0.91-altconfigfile2.patch.bz2
Patch4:		grub-0.90-grub-install.patch.bz2
Patch6:		grub-0.5.96.1-special-raid-devices.patch.bz2
Patch7:		grub-0.91-nice-magic.patch.bz2
Patch8:		grub-0.93-gcc33.patch.bz2
Patch9:		grub-0.93-add-our-own-memcpy.patch.bz2

Patch10:	grub-0.93-configfile.patch
Patch11:	grub-0.90-symlinkmenulst.patch
Patch12:	grub-0.90-staticcurses.patch
Patch13:	grub-0.93-largedisk.patch
Patch14:	grub-0.93-graphics.patch.bz2
Patch15:	grub-0.91-splashimagehelp.patch
Patch16:	grub-0.93-graphics-bootterm.patch
Patch17:	grub-0.92-hammer.patch
Patch18:	grub-0.93-autoconf-fix.patch

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	ncurses-devel, tetex

Exclusivearch:	%ix86 amd64 x86_64
Conflicts:	initscripts <= 6.40.2-15mdk
Provides:	bootloader

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems.  In addition to loading the Linux and *BSD kernels,
it implements the Multiboot standard, which allows for flexible loading
of multiple boot images (needed for modular kernels such as the GNU
Hurd).

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1 -z .pix
%patch10 -p1 -b .10
%patch11 -p1 -b .11
%patch12 -p1 -b .12
%patch13 -p0 -b .13
%patch14 -p1 -b .14
%patch15 -p1 -b .15
%patch16 -p1 -b .16
%patch17 -p1 -b .17
%patch18 -p0 -b .autofix

%build
rm -f configure && autoconf
%ifarch amd64 x86_64
LDFLAGS="-Wl,-static" ; export LDFLAGS
%endif
CFLAGS="-Os -g" %configure --sbindir=/sbin --disable-auto-linux-mem-opt
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT/

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

install -d $RPM_BUILD_ROOT/boot/grub
mv $RPM_BUILD_ROOT%{_datadir}/grub/*/* $RPM_BUILD_ROOT/boot/grub

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{name}.info
%_install_info multiboot.info

%preun
%_remove_install_info %{name}.info
%_remove_install_info multiboot.info

%files
%defattr(-,root,root)
%doc TODO BUGS NEWS ChangeLog docs/menu.lst
/boot/grub
%{_infodir}/*
%{_mandir}/*/*
%{_bindir}/mbchk
/sbin/*

%changelog
* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.93-6sls
- Provides: bootloader

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 0.93-5sls
- remove docs package
- don't use %%build_opensls
- docs in main package
- amd64 support
- don't remove mbchk files
- files are in /sbin not /usr/sbin
- get rid of the /boot/grub/install.sh stuff in %%post since we haven't had
  that there in forever
- sync some patches with fedora 0.93-7:
  - P10/P11: grub.conf default, not menu.lst
  - P12: link against curses statically
  - P13: support large disks
  - P14/P15/P16: graphics mode support
  - P17: support to build on amd64
- this gives us preliminary splash support but there are a lot of issues
  with it to resolve

* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 0.93-4sls
- OpenSLS build
- tidy spec
- don't build doc with %%build_opensls

* Mon Aug 18 2003 Pixel <pixel@mandrakesoft.com> 0.93-3mdk
- don't include our own memcpy when building WITHOUT_LIBC_STUBS

* Thu Aug 14 2003 Pixel <pixel@mandrakesoft.com> 0.93-2mdk
- distlint DIRM fix: now owning /boot/grub
- add patch from upstream to fix build with gcc 3.3
- include our own memcpy since gcc generates a call to memcpy for some
  assignments (and using CFLAGS=-Os doesn't do the trick anymore)

* Mon Dec  9 2002 Pixel <pixel@mandrakesoft.com> 0.93-1mdk
- new release
- use CFLAGS=-Os (so that gcc doesn't use memcpy)

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.92-2mdk
- fix doc subpackage group

* Tue Apr 30 2002 Pixel <pixel@mandrakesoft.com> 0.92-1mdk
- new release

* Thu Jan 24 2002 Pixel <pixel@mandrakesoft.com> 0.91-2mdk
- add a nice magic
- conflicts with current initscripts (=> force joe guy to update the new
initscript which understand that magic)

* Tue Jan 22 2002 Pixel <pixel@mandrakesoft.com> 0.91-1mdk
- new version

* Thu Sep  6 2001 Pixel <pixel@mandrakesoft.com> 0.90-4mdk
- update JFS patch, add XFS patch

* Wed Sep  5 2001 Pixel <pixel@mandrakesoft.com> 0.90-3mdk
- drop i18n and keytable broken patches (just keep command compatibility)

* Sun Aug  5 2001 Pixel <pixel@mandrakesoft.com> 0.90-2mdk
- add JFS support

* Wed Jul 18 2001 Pixel <pixel@mandrakesoft.com> 0.90-1mdk
- new version

* Tue Apr  3 2001 Pixel <pixel@mandrakesoft.com> 0.5.96.1-8mdk
- patch for raid (rd, ida, cciss)

* Tue Mar 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.5.96.1-7mdk
- BuildRequires: tetex.
- Conflicts: initscripts <= 5.61.1-7mdk
- Remove rebootin (moved to initscripts).

* Sat Mar  3 2001 Pixel <pixel@mandrakesoft.com> 0.5.96.1-6mdk
- modified patch i18n-messages-and-keytable for yet another layout fix

* Sat Feb 24 2001 Pixel <pixel@mandrakesoft.com> 0.5.96.1-5mdk
- small layout fix

* Fri Feb 23 2001 Pixel <pixel@mandrakesoft.com> 0.5.96.1-4mdk
- don't give parameter "mem=" to kernel (bad for 2.4 kernels, see jeff for more)

* Thu Dec 21 2000 Pixel <pixel@mandrakesoft.com> 0.5.96.1-3mdk
- capitalize summary

* Mon Dec 11 2000 Pixel <pixel@mandrakesoft.com> 0.5.96.1-2mdk
- add a call to /boot/grub/install.sh if needed

* Sat Dec  9 2000 Pixel <pixel@mandrakesoft.com> 0.5.96.1-1mdk
- new version
  * patch fixbiosbug-nbsectors no more needed (unless you define NO_BUGGY_BIOS_IN_THE_WORLD)

* Thu Aug 24 2000 Pixel <pixel@mandrakesoft.com> 0.5.95-7mdk
- %%_remove_install_info is fixed, yeepee :)

* Tue Aug 22 2000 Pixel <pixel@mandrakesoft.com> 0.5.95-6mdk
- fixbiosbug-nbsectors for some Geom Errors (warly's case)

* Wed Aug 16 2000 Pixel <pixel@mandrakesoft.com> 0.5.95-5mdk
- fix erroneous remove_info macro (sillyme)

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.5.95-4mdk
- automatically added BuildRequires

* Fri Jul 21 2000 Pixel <pixel@mandrakesoft.com> 0.5.95-3mdk
- macroization, BM

* Wed Jul 12 2000 Pixel <pixel@mandrakesoft.com> 0.5.95-2mdk
- add a patch for ezbios nonsense

* Mon Jul  3 2000 Pixel <pixel@mandrakesoft.com> 0.5.95-1mdk
- new version

* Sat May 20 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-14mdk
- add rebootin command (use altconfigfile cmd in menu.lst)
- add altconfigfile (read once)

* Mon May  8 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-12mdk
- add reiserfs handling (missing symlink handling though)

* Wed May  3 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-11mdk
- fix for linux-extended extended partition

* Tue May  2 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-10mdk
- fix case of not found keytable

* Tue Apr 18 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-9mdk
- remove a patch from caldera

* Sun Apr 16 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-8mdk
- nicer menu
- don't add automatic mem= if one is given

* Tue Apr  4 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-7mdk
- fix install path

* Mon Apr  3 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-6mdk
- integrate patches from caldera

* Fri Mar 31 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-5mdk
- re-rebuild

* Wed Mar 29 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-4mdk
- big patch (i18n & look)

* Sat Mar 25 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-3mdk
- split printable doc and some more to have smaller package (keep mainly info in
main package, very good one)
- cleanup install-info in % post scripts

* Fri Mar 24 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-2mdk
- remove unneeded patch
- use of % { ix86 }

* Wed Mar 22 2000 Pixel <pixel@mandrakesoft.com> 0.5.94-1mdk
- remove now unneeded --disable-gunzip
- added option --disable-lba-support-bitmap-check
- patch for *very* buggy bioses (tells grub every hd is gigantic)
- new version

* Mon Mar 13 2000 Pixel <pixel@mandrakesoft.com> 0.5.93.1-7mdk
- configure with --disable-gunzip
(so that initrd is not gunzip'ed and fits in memory, that's the kernel's job anyway)

* Wed Mar  1 2000 Pixel <pixel@mandrakesoft.com> 0.5.93.1-6mdk
- remove no-device-check (was stupid)
- replace by something better (option --devices)

* Tue Feb 29 2000 Pixel <pixel@mandrakesoft.com> 0.5.93.1-5mdk
- add option no-device-check for grub binary (mainly for non-interactive use)

* Sun Jan 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.5.93.1-4mdk
- Add Exclusivearch.

* Tue Jan 4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.5.93.1-3mdk
- Add install_grub_on_floppy script (thnks b.bodin).
- Add dvi docs (tknks b.bodin).

* Mon Jan  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.5.93.1-2mdk
- Add %packager (thnks rpmlint).
- Remove CFLAGS.

* Mon Jan  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- First spec file for Mandrake distribution based on debian version.
