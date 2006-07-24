#
# spec file for package console-tools
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		console-tools
%define version		0.2.3
%define release		%_revrel

%define	CTVER		%{version}
%define	CDVER		1999.08.29
%define MDK_KBD_VER	20030918

%define major		0
%define fname		console
%define libname 	%mklibname %{fname} %{major}

# /usr/lib/kbd/{conslefonts,consolemaps,keymaps} instead of
# /usr/share/{conslefonts,consolemaps,keymaps}
# FIXME: data really should really go to /usr/share/*
%define kbddir		%{_prefix}/lib/kbd
%define _datadir	%{kbddir}

Summary:	Linux console tools
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Terminals
URL:		http://lct.sourceforge.net/
Source0:	ftp://metalab.unc.edu/pub/Linux/system/keyboards/console-tools-%{CTVER}.tar.bz2
Source1:	ftp://metalab.unc.edu/pub/Linux/system/keyboards/console-data-%{CDVER}.tar.bz2
Source2:	keytable.init
Source3:	ftp://ftp.dementia.org/pub/linux/pc2sun.pl
Source4:	console-tools-ucwfonts.tar.bz2
Source5:	kbd-0.96-turkish.tar.bz2
Source6:	kbd-mdk-keymaps-%{MDK_KBD_VER}.tar.bz2
Source7:	configure_keyboard.sh
Source8:	ctools-cyr.tar.bz2
# on PPC we need to see whether mac or Linux keycodes are being used - stew
Source9:	keytable.init.ppc
Source10:	mac-keymaps.tar.bz2
# taken from ftp://ftp.kernel.org/pub/linux/utils/kbd/kbd-1.12.tar.bz2, where
# it's called "us-acentos.map"
Source11:	us-intl.kmap.gz
# docbook is unable to convert the sgml files to html
# disabling them in the makefiles -- pablo
Patch5:		console-tools-0.2.3-docbook.patch
# Allow consolechars & loadkeys to run from the root partition
Patch6:		console-tools-rootpart.patch
# fixes a stupid error -- pablo
Patch8:		console-tools-0.2.3-versioncoredump.patch
# some keyboards cannot have the euro in AltGr-e -- pablo
Patch9:		console-tools-0.2.3-noteuro.patch
Patch10:	console-data-1999.08.29-mandrake.patch
Patch11:	console-tools-0.2.3-tilde-with-twosuperior-in-french-keyboard.patch
Patch12:	console-tools-0.2.3-setkeycodes-fixargument.patch
# some modifications to cover PPC using Linux keycodes
Patch13:	console-tools-0.2.3-ppc-using-linux-keycodes.patch
# Thai kbds, keysysm and fonts -- pablo
Patch14: 	http://www.links.nectec.or.th/~thep/th-console/console-data/console-data-thai_deb-1999.08.29-21.8.patch
Patch15: 	http://www.links.nectec.or.th/~thep/th-console/console-tools/console-tools-thai_ksym.patch
# gcc 3.3
Patch16: 	console-tools-gcc33.patch
# this patch removes testing of start_unicode, otherwise console font
# cannot be changed once in utf-8 mode -- pablo
Patch17: 	console-tools-start_unicode.patch
# patch for a coredump when using compressed font files -- pablo
Patch18: 	console-tools-0.2.3-compresscoredump.patch
# gcc 3.4
Patch19:	console-tools-0.2.3-gcc3.4-fix.patch
# updated french mac keymap v3 from ftp://ftp.linux-france.org/pub/macintosh/kbd-mac-fr.tar.gz
Patch20:	console-data-1999.08.29-mac.patch
# taken from debian's 30_openvt-devfs.patch patch
Patch21:	console-tools-0.2.3-fix-openvt-option--w.patch
# fgconsole exit(0) missing
Patch22:	console-tools-0.2.3-fix-fgconsole_exit_status.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	flex libtool >= 1.3.3 automake1.7 automake1.4 autoconf2.5 gettext-devel

Prereq:		coreutils sed rpm-helper
PreReq:		%{libname} = %{version}-%{release}
Obsoletes:	kbd
Provides:	kbd
Requires:	grep, gawk

%description
This package contains utilities to load console fonts and
keyboard maps.  It also includes a number of different fonts
and keyboard maps.


%package -n %{libname}
Summary:	Libraries for console tools
Group:		System/Libraries
Provides:	lib%{fname} = %{version}-%{release}

%description -n %{libname}
This package contains libraries for console tools


%package -n %{libname}-devel
Summary:	Include and .so files for console tools
Group:		Development/Other
PreReq:		%{libname} = %{version}-%{release}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{fname}-devel = %{version}-%{release}

%description -n %{libname}-devel
This package contains include and .so files for console tools


%package -n %{libname}-static-devel
Summary:	Static libraries for console tools
Group:		Development/Other
PreReq:		%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-static-devel
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:  	lib%{fname}-static-devel = %{version}-%{release} 

%description -n %{libname}-static-devel
This package contains static libraries for console tools.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -n %{name}-%{CTVER} -q -a 1 -a4 -a5
cd console-data-%{CDVER}
%patch10 -p1
%patch20 -p1
cd ..

%patch5 -p1 -b ._db
%patch6 -p1 -b .rootpart
%patch8 -p1
%patch9 -p0
%patch11 -p1
%patch12 -p1

%ifarch ppc
%patch13 -p1
%endif

%patch14 -p0 -b .thai1
%patch15 -p1 -b .thai2
%patch16 -p0
%patch17 -p1
%patch18 -p1
%patch19 -p1 -b .gcc34
%patch21 -p1
%patch22 -p1

# adapt for gettext >= 0.14.2 (avoid patch)
grep -q gt_LC_MESSAGES /usr/share/aclocal/lcmessage.m4 &&
perl -pi -e 's/^(\s+)AM_(LC_MESSAGES)/${1}gt_${2}/' acinclude.m4 console-data-%{CDVER}/acinclude.m4


%build
%serverbuild
%ifarch %ix86
DISABLE_RESIZECONS=
%else
DISABLE_RESIZECONS=--disable-resizecons
%endif

aclocal-1.4
automake-1.4
export FORCE_AUTOCONF_2_5=1
CFLAGS="%{optflags} -D_GNU_SOURCE"
%configure2_5x --enable-localdatadir=%{_sysconfdir}/sysconfig/console $DISABLE_RESIZECONS
%make

cd console-data-%{CDVER}
aclocal-1.7
automake-1.7
CFLAGS="%{optflags} -D_GNU_SOURCE"
%configure2_5x --enable-localdatadir=%{_sysconfdir}/sysconfig/console $DISABLE_RESIZECONS
%make
cd -


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}

make DESTDIR=%{buildroot} install
pushd console-data-%{CDVER}
    make DESTDIR=%{buildroot} install
popd

# don't give loadkeys SUID perms
chmod 0755 %{buildroot}%{_bindir}/loadkeys

# other keymaps
tar jxf %{SOURCE6} -C %{buildroot}/%{kbddir}/
tar jxf %{SOURCE8} -C %{buildroot}/%{kbddir}/
	  
install -d -m 0755 %{buildroot}%{_sysconfdir}/rc.d/init.d
%ifarch ppc
install -m 0755 %{SOURCE9} %{buildroot}%{_sysconfdir}/rc.d/init.d/keytable
%else
install -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/rc.d/init.d/keytable
%endif

install -d -m 0755 %{buildroot}%{_sysconfdir}/profile.d
install -m 0755 %{SOURCE7} %{buildroot}%{_sysconfdir}/profile.d/configure_keyboard.sh

install -d -m 0755 %{buildroot}/bin
#for i in loadkeys consolechars unicode_start; do
for i in unicode_start; do
    mv %{buildroot}%{_bindir}/$i %{buildroot}/bin
    ln -s ../../bin/$i %{buildroot}%{_bindir}/$i
done

%ifnarch %ix86
rm -f %{buildroot}%{_mandir}/man8/resizecons.8
%endif

chmod +x %{buildroot}%{_libdir}/*.so*

cp -aR console-data-%{CDVER}/doc/* doc

install -m 0644 -D include/lct/*.h %{buildroot}%{_includedir}/lct/

# more mac keymaps on ppc 
%ifarch ppc 
tar jxf %{SOURCE10} -C %{buildroot}/%{kbddir}/keymaps 
%endif

# remove unneeded files
rm -rf %{buildroot}/%{kbddir}/keymaps/{amiga,atari,sun}
%ifnarch ppc
rm -rf %{buildroot}/%{kbddir}/keymaps/mac
%endif

# us-international keymap
install -m 0644 %{SOURCE11} %buildroot/%{kbddir}/keymaps/i386/qwerty/

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_service keytable
if [ -f %{_sysconfdir}/sysconfig/keyboard ] ; then
    . %{_sysconfdir}/sysconfig/keyboard
    if [ -n "$KEYTABLE" ] ; then
        KT=`echo $KEYTABLE | sed -e "s/.*\///g" | sed -e "s/\..*//g"`
		# perl-base is required by basesystem ...
		perl -pi -e "s/KEYTABLE=.*$/KEYTABLE=$KT/g" %{_sysconfdir}/sysconfig/keyboard
    fi
fi
if [ -f %{_sysconfdir}/sysconfig/i18n ] ; then
   . %{_sysconfdir}/sysconfig/i18n
   if [ -d %{_sysconfdir}/sysconfig/console ] ; then
      if [ -n "$SYSFONT" ]; then
         mkdir -p %{_sysconfdir}/sysconfig/console/consolefonts
         cp -f %{kbddir}/consolefonts/$SYSFONT* \
			%{_sysconfdir}/sysconfig/console/consolefonts
      fi
      if [ -n "$UNIMAP" ]; then
         mkdir -p %{_sysconfdir}/sysconfig/console/consoletrans
         cp -f %{kbddir}/consoletrans/$UNIMAP* \
			%{_sysconfdir}/sysconfig/console/consoletrans
      fi
      if [ -n "$SYSFONTACM" ]; then 
         mkdir -p %{_sysconfdir}/sysconfig/console/consoletrans
         cp -f %{kbddir}/consoletrans/$SYSFONTACM* \
			%{_sysconfdir}/sysconfig/console/consoletrans
      fi
   fi
fi

%preun
%_preun_service keytable

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/profile.d/configure_keyboard.sh
%config(noreplace) %{_sysconfdir}/rc.d/init.d/keytable
%{_libdir}/*.la
%dir %{kbddir}
%{kbddir}/consolefonts
%{kbddir}/consoletrans
%dir %{kbddir}/keymaps
%{kbddir}/unidata
%{kbddir}/keymaps/include
# Warning: keyboards are not cpu-dependent but machine-dependent.
# How to distinguish Linux/PPC on Amiga/PPC (amiga kbd) and Linux/PPC
# on Apple/ppc (mac kbd) ?
#
# for now an ugly hack: ppc -> mac, sparc -> sun, i386/alpha -> i386
#%{kbddir}/keymaps/amiga
#%{kbddir}/keymaps/atari
#
# (fg) 20010411 Also ia64 has PC-like keyboards, added it here
#
# (sb) move to Linux keycodes PPC
#
# (OT) if all need it, why set an %ifarch
#%ifarch %ix86 alpha ia64 ppc x86_64 sparc
%{kbddir}/keymaps/i386
#%endif

# (sb) leave in the event user really wants mac keymaps
%ifarch ppc
%{kbddir}/keymaps/mac
%endif
/bin/unicode_start
%{_bindir}/charset
%{_bindir}/chvt
%{_bindir}/codepage
%{_bindir}/consolechars
%{_bindir}/deallocvt
%{_bindir}/dumpkeys
%{_bindir}/fgconsole
%{_bindir}/fix_bs_and_del
%{_bindir}/font2psf
%{_bindir}/getkeycodes
%{_bindir}/kbd_mode
%{_bindir}/loadkeys
%{_bindir}/loadunimap
%{_bindir}/mk_modmap
%{_bindir}/mapscrn
%{_bindir}/openvt
%{_bindir}/psfaddtable
%{_bindir}/psfgettable
%{_bindir}/psfstriptable
%ifarch %ix86
%{_bindir}/resizecons
%endif
%{_bindir}/saveunimap
%{_bindir}/screendump
%{_bindir}/setfont
%{_bindir}/setkeycodes
%{_bindir}/setleds
%{_bindir}/setmetamode
%{_bindir}/setvesablank
%{_bindir}/showcfont
%{_bindir}/showkey
%{_bindir}/splitfont
%{_bindir}/unicode_start
%{_bindir}/unicode_stop
%{_bindir}/vcstime
%{_bindir}/vt-is-UTF8
%{_bindir}/writevt
%{_mandir}/man1/*
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*


%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.so
%dir %{_includedir}/lct
%{_includedir}/lct/*

%files -n %{libname}-static-devel
%defattr(-,root,root,-)
%{_libdir}/*.a

%files doc
%defattr(-,root,root)
%doc README NEWS RELEASE
%doc BUGS TODO doc/[cdf]* doc/keymaps doc/README* doc/*.txt


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3 
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3-55avx
- adapt for gettext >= 0.14.2 (gt_LC_MESSAGES) (gbeauchesne)
- added us-intl console keyboard map for people with US keyboards but
  who need better cedilla support (andreas)
- fix manpage location (andreas)
- use make with DESTDIR instead of %%makeinstall (andreas)
- rebuild for new gettext

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3-54avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3-53avx
- rebuild against new gcc
- enable P19
- P21: fix openvt -w; from debian (pixel)
- P22: fix fgconsole exit(0) missing (nicolas.brouard)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3-52avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3-51avx
- sync with cooker 0.2.3-49mdk:
  - fix gcc-3.4 build (P19) (peroyvind)
  - force use of automake1.{4,7} and autoconf2.5 (peroyvind)
  - only put files not linked with /usr/lib libraries in /bin to allow
    to boot on a separated /usr without error [bug #11042] (flepied)
  - BuildRequires: gettext-devel (cjw)
  - P20: update french mac keymap (cjw)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3-50avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 0.2.3-49sls
- require packages, not files

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.2.3-48sls
- minor spec cleanups

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 0.2.3-47sls
- OpenSLS build
- remove dependency on sgml-tools so we save 16MB of useless docbook stuff
- tidy spec

* Mon Sep 22 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-46mdk
- fixed post install scripts to use right paths under /etc/sysconfig/console
- added Uzbek cyrillic keyboard and font
- renabled compressed fonts

* Thu Sep 18 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-45mdk
- removed tests of start_unicode

* Tue Jul 08 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.2.3-44mdk
- fix gcc 3.3 build (patch16)
- remove %%ifarch for some files, all arch want it...
- my dear %%mklibname

* Wed Apr 23 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-43mdk
- fixed permissions of Czek files
- small fix of Spanish keyboard

* Tue Mar 04 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-42mdk
- added Thai patches
- Turkish keyboard and fonts fixes
- added unicode keyboards for all keyboard maps used by drakkeyboard

* Wed Dec 18 2002 Stew Benedict <sbenedict@mandrakesoft.com> 0.2.3-41mdk
- add some more mac keymaps for those so inclined

* Tue Nov 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.2.3-40mdk
- x86-64 has PC-like keyboards too
- Introduce %%kbddir currently hardcoded to %{_prefix}/lib/kbd, this
  really should go into %%{_datadir}/kbd, IMHO

* Mon Nov 18 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.2.3-39mdk
- libified
- put unicode_start in /bin because it's used by rc.sysinit (bug #518)

* Thu Nov 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.3-38mdk
- %%post sanity check on KEYTABLE variable in /etc/sysconfig/keyboard
  happilly removed other options, which is not so nice.

* Tue Nov 12 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.3-37mdk
- add url (yura gusev)

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.3-36mdk
- requires s/fileutils/coreutils/
- Prereq: rpm-helper
- rpmlint fixes

* Tue Sep 03 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-35mdk
- added nice Turkish fonts
- small correction on ro2 file

* Tue Aug 27 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-34mdk
- commented out the "dead_abovedot" keysyms (not supported)

* Mon Aug 26 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-33mdk
- added missing keyboards
- make bi-mode (eg: latin/cyrillic) keyboards use the same toggle key as
  defined for X11 trough drakx/drakkeyboard
- add sfm tables to all fonts set by DrakX

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.2.3-32mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon May 13 2002 Pixel <pixel@mandrakesoft.com> 0.2.3-31mdk
- remove Prereq docbook-utils (unused)

* Tue May 07 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-30mdk
- New docbook2html is unable to convert to html the sgml file;
  disabling them

* Mon Mar 11 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-29mdk
- corrected Ctrl-C problem

* Fri Mar  8 2002 Warly <warly@mandrakesoft.com> 0.2.3-28mdk
- remove the > /dev/tty0 from initscripts not to conflict with bootsplash
redirections

* Tue Feb 26 2002 Stew Benedict <sbenedict@mandrakesoft.com> 0.2.3-27mdk
- map Apple to AltGr, shift-Apple to compose for PPC using Linux keycodes

* Tue Feb 12 2002 Stew Benedict <sbenedict@mandrakesoft.com> 0.2.3-26mdk
- additional mods for PPC using Linux keycodes

* Sat Jan 19 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.3-25mdk
- dadou said "Don't use y option when we untar/unbzip2", but me say "don't use
  tar at all"
- clean spec for sir rpmlint:
	* fix patches permissions
	* don't use RPM_SOURCE_DIR

* Sat Jan 19 2002 David BAUDENS <baudens@mandrakesoft.com> 0.2.3-24mdk
- Fix Group: for devel package
- Add PreReq: for devel package
- Move static libraries in static-devel package
- Fix and use macros
- Don't use y option when we untar/unbzip2
- Add missing files

* Tue Oct 09 2001 Stew Benedict <sbenedict@mandrakesoft.com> 0.2.3-23mdk
- "big move" to Linux keycodes for PPC

* Thu Sep 06 2001 Stefan van der Eijk <stefan@eijk.nu> 0.2.3-22mdk
- BuildRequires:	flex

* Wed Aug 29 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-21mdk
- corrected problem with Euro and CZ/SK keyboards

* Fri Aug 10 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-20mdk
- fixed several keyboard and font bugs 

* Thu Apr 26 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2.3-19mdk
- Fix setkeycodes argument.

* Wed Apr 11 2001 Francis Galiegue <fg@mandrakesoft.com> 0.2.3-18mdk
- Install keymaps on ia64 :(

* Wed Apr  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.2.3-17mdk
- use server macro

* Tue Jan 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2.3-16mdk
- Make twosuperior and shift product tilde on french keyboard.

* Wed Sep 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2.3-15mdk
- Add include files to devel package.

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 0.2.3-14mdk
- remove pablo's hack for stty failing (completly removed the stty stuff until
someone find something better)

* Fri Sep  1 2000 Pixel <pixel@mandrakesoft.com> 0.2.3-13mdk
- move the *.a and *.so in the -devel package

* Thu Aug 31 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-12mdk
- added various keyboards and fonts, to sync whith what is offered by DrakX

* Wed Aug 30 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.2.3-11mdk
- use /var/lock/subsys file to avoid relaunch in run level change.

* Thu Jul 27 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-10mdk
- fixed Japanese 106keys keyboard

* Fri Jul 21 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-9mdk
- fix Swiss romand keyboard

* Thu Jul 20 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-8mdk
- make sure meta_keys.inc file is included for the sparc
- use mandir macros
- added Tamil console font
- some keyboard fixes

* Tue Jun 20 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.2.3-7mdk
- fixed configure_keyboard.sh to not run in non-interactive sessions.

* Mon Jun  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2.3-6mdk
- Remove nasty stuff from pablo.

* Mon Jun 05 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-5mdk
- a tar file was not installed due to wrong format, fixed

* Fri May 26 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-4mdk
- fixed Swedish keyboard
- added more keyboards to be in sync with DrakX
- added cyrillic add-ons from IP-Labs

* Mon May 22 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-3mdk
- removed no longer needed call to setsysfont

* Tue May  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.2.3-2mdk
- fixed sparc compile.

* Wed Apr 19 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.3-1mdk
- updated to 0.2.3
- fixed some files permissions
- made the BackSpace key configuration (eg sending ^H or ^?)
  consistent accross platforms (SUN, mac and PC)
- make the three supplementary keys of PC 105 keys kbds, and the 
  three keys meta(L,R) and Compose on SUNs, behave the same.
- corrected Brazilian keyboard
- updated Swedish keyboard

* Fri Apr 14 2000 David BAUDENS <baudens@mandrakesoft.com> 0.2.2-15mdk
- Add missing x86 archs

* Wed Mar 29 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.2-14mdk
- Oops, /usr/lib/lib* were missing... fixed

* Wed Mar 29 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.2-13mdk
- in %%files section only kmaps for the building target (needs improving)
- new Group: naming
- new armenian keyboards
- included the sun4 norwegian keyboard in our kbd-mdk tarball; it's easier

* Wed Mar 08 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.2-12mdk
- corrected the keyboard map "il-8859_8.kmap" (keyboard used in Israel),
  it was wrongly identiqual to "hebrew.kmap" (phonetical keyboard)

* Sat Jan 15 2000 Francis Galiegue <francis@mandrakesoft.com>
- sparc patch fixing galore
- bzip2'ed all patches which weren't
- spec file fixes

* Tue Jan 11 2000 Pixel <pixel@mandrakesoft.com>
- alphaev6 adaptation (libtoolize call added)
- buildreq sgml-tools added (for sgml2html)

* Fri Jan  7 2000 Pixel <pixel@mandrakesoft.com>
- really hide output of loadkeys (msg4pablo: >& is csh, not sh :pp)

* Tue Jan  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2.2-8mdk
- remove configure_keyboard.sh.

* Mon Jan 03 2000 Pablo Saratxaga <pablo@mandrakesoft.com>
- Hide outpout of loadkeys {backspace,delete}.in, 
  only show the [OK] or [FAILED].
- added a cp852 encoded version of the "t" font.

* Thu Dec 30 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- improved the BackSpace key handling
- added fonts for latin7 and latin8, and various trans and uni files

* Mon Dec 27 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- corrected the problem with the euro.inc file (the keysyms are locale
  dependent! the names 'currency' and 'cent' are not valid for all
  charset encodings, changed them with hexa values)
- corrected the estonian keyboard (s/asciircum/asciicircum/)

* Fri Nov 26 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- changed keymap.init and added a profile.d/ script to fix the BackSpace key;
  with the default being sending a "Delete", but user configurable.

* Tue Nov 23 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- added my collection of keyboards (in sync with DrakX installer)
- removed ro.map and sr.map from outside (they are already on console-data)
- added my compose.* files
- replaced the keymap.init by mine (uses compose.* files and correct the
  BakcSpace key (unless asked otherwise on /etc/sysconfig/keyboard))
- removed /usr/bin/fix_bs_and_del as it is no longer need (the keymap.init
  does the proper thing) 
- it is my birthday
- corrected the US intl (us-latin1) keymap to have dead keys

* Wed Sep  1 1999 Daouda LO <daouda@mandrakesoft.com>
- 0.2.2
- bug fixes

* Thu Jun  3 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Mandrake adaptions
- console-tools 0.2.0, console-data 1999.04.15
- Euro support
- Support for Windoze keys
- Support for Alt+AltGr=Compose
- cleanups

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- make keytable %%post handle us.map better

* Thu Apr 15 1999 Jeff Johnson <jbj@redhat.com>
- hotwire sun fonts.

* Wed Apr 14 1999 Bill Nottingham <notting@redhat.com>
- %%post changes; just copy the user's configured font/map/etc.

* Wed Apr 14 1999 Matt Wilson <msw@redhat.com>
- added fonts RUSCII_*, koi8u_*, and acm koi8u2ruscii from
  Leon Kanter <leon@geon.donetsk.ua>

* Mon Apr 12 1999 Bill Nottingham <notting@redhat.com>
- removed sh-utils from prereq.
- added sed to prereq

* Fri Apr  9 1999 Jeff Johnson <jbj@redhat.com>
- more latin2 fonts (Peter Ivanyi).

* Thu Apr  8 1999 Bill Nottingham <notting@redhat.com>
- added sh-utils to prereq.

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- /etc/sysconfig/console support
- add setsysfont to init script

* Mon Mar 29 1999 Peter Ivanyi <ivanyi@internet.sk>
- more fixes.

* Thu Mar 25 1999 Peter Ivanyi <ivanyi@internet.sk>
- add ucw-fonts-1.1.tar.gz
- delete obsolete sk keymaps from console-tools-1998.08.11.add-ons.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- added norwegian sun4 keymap support

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 1999.03.02.

* Tue Feb 16 1999 Jeff Johnson <jbj@redhat.com>
- repackage for Red Hat 6.0

* Wed Jan 30 1999 Alex deVries <puffin@redhat.com>
- added amiga support for Jes Sorensen

* Mon Dec 07 1998 Jakub Jelinek <jj@ultra.linux.cz>
- some keymaps were including "*.map", which has to be
  replaced by "*.kmap"

* Fri Dec 04 1998 Jakub Jelinek <jj@ultra.linux.cz>
- upgrade to console-tools, added new sun keymaps,
  new sun fonts for latin0/1 and latin2, iso15.acm
  and iso02+euro.acm.
- Print the verbose messages only if verbose was 
  specified on command line.

* Thu Oct 01 1998 Cristian Gafton <gafton@redhat.com>
- added Euro (latin0) support from Guylhem Aznar

* Sun Sep 27 1998 Cristian Gafton <gafton@redhat.com>
- fix the name the ro and sr maps are installed under
- slovak keymaps
- ro.map and sr.map are welcomed to the club
- enable turkish again

* Mon Aug 24 1998 Cristian Gafton <gafton@redhat.com>
- KEYTABLE should not have the full patch name (%%post hack)

* Fri Aug 21 1998 Jeff Johnson <jbj@redhat.com>
- install keymaps on tty0 w/o using (non-installed) open(1).

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- updated to 0.96a.

* Thu Jun 11 1998 Mikael Hedin <micce@irf.se>
- specify VT0 in case we use a serial console

* Wed Jun 10 1998 Jeff Johnson <jbj@redhat.com>
- quotes permit multiple keytables in keytable.init (problem #675)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu May 07 1998 Donnie Barnes <djb@redhat.com>
- added some extra turkish support

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- fixes for building on alpha
- completed buildroot usage

* Thu Apr 23 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscript

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 0.95

* Wed Mar 25 1998 Erik Troan <ewt@redhat.com>
- fixed /tmp exploit

* Wed Nov 05 1997 Donnie Barnes <djb@redhat.com>
- added SPARC stuff (finally!), Thanks to eduardo@medusa.es for most of it.
- added buildroot
- cleaned up the file list
- moved to rev 5 because the contrib ver rel was 4

* Mon Oct 20 1997 Donnie Barnes <djb@redhat.com>
- updated from 0.91 to 0.94
- added chkconfig support
- spec file cleanups

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
