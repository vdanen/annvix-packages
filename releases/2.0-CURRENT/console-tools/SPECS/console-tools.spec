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

%define kbddir		%{_prefix}/lib/kbd

Summary:	Linux console tools
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Terminals
URL:		http://lct.sourceforge.net/
Source0:	ftp://metalab.unc.edu/pub/Linux/system/keyboards/console-tools-%{CTVER}.tar.bz2
Source1:	ftp://metalab.unc.edu/pub/Linux/system/keyboards/console-data-%{CDVER}.tar.bz2
Source3:	ftp://ftp.dementia.org/pub/linux/pc2sun.pl
Source4:	console-tools-ucwfonts.tar.bz2
Source5:	kbd-0.96-turkish.tar.bz2
Source6:	kbd-mdk-keymaps-%{MDK_KBD_VER}.tar.bz2
Source7:	configure_keyboard.sh
Source8:	ctools-cyr.tar.bz2
# on PPC we need to see whether mac or Linux keycodes are being used - stew
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
BuildRequires:	flex
BuildRequires:	libtool >= 1.3.3
BuildRequires:	automake1.7
BuildRequires:	automake1.4
BuildRequires:	autoconf2.5
BuildRequires:	gettext-devel

Requires:	grep
Requires:	gawk
Requires(pre):	rpm-helper
Requires(pre):	%{libname} = %{version}-%{release}
Requires(post):	coreutils
Requires(post):	sed
Requires(post):	perl
Requires(post):	rpm-helper
Obsoletes:	kbd
Provides:	kbd

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
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{fname}-devel = %{version}-%{release}

%description -n %{libname}-devel
This package contains include and .so files for console tools


%package -n %{libname}-static-devel
Summary:	Static libraries for console tools
Group:		Development/Other
Requires:	%{name}-devel = %{version}-%{release}
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

# relocate some files from /usr/share to /usr/lib/kbd
mkdir %{buildroot}%{kbddir}
for dir in consolefonts consoletrans keymaps unidata videomodes
do
    mv %{buildroot}%{_datadir}/${dir} %{buildroot}%{kbddir}/
done

# don't give loadkeys SUID perms
chmod 0755 %{buildroot}%{_bindir}/loadkeys

# other keymaps
tar jxf %{_sourcedir}/kbd-mdk-keymaps-%{MDK_KBD_VER}.tar.bz2 -C %{buildroot}/%{kbddir}/
tar jxf %{_sourcedir}/ctools-cyr.tar.bz2 -C %{buildroot}/%{kbddir}/
	  
install -d -m 0755 %{buildroot}%{_sysconfdir}/profile.d
install -m 0755 %{_sourcedir}/configure_keyboard.sh %{buildroot}%{_sysconfdir}/profile.d/configure_keyboard.sh

install -d -m 0755 %{buildroot}/bin
for i in consolechars unicode_start kbd_mode; do
    mv %{buildroot}%{_bindir}/$i %{buildroot}/bin
    ln -s ../../bin/$i %{buildroot}%{_bindir}/$i
done

chmod +x %{buildroot}%{_libdir}/*.so*
# libraries must be accessible before partition mounting
# if we want to be able to load console font before partition mounting
mkdir -p  %{buildroot}/lib
mv %{buildroot}/%{_libdir}/*.so* %{buildroot}/lib

%ifnarch %ix86
rm -f %{buildroot}%{_mandir}/man8/resizecons.8
%endif

cp -aR console-data-%{CDVER}/doc/* doc

install -m 0644 -D include/lct/*.h %{buildroot}%{_includedir}/lct/

# more mac keymaps on ppc 
%ifarch ppc 
tar jxf %{_sourcedir}/mac-keymaps.tar.bz2 -C %{buildroot}/%{kbddir}/keymaps 
%endif

# remove unneeded files
rm -rf %{buildroot}/%{kbddir}/keymaps/{amiga,atari,sun}
%ifnarch ppc
rm -rf %{buildroot}/%{kbddir}/keymaps/mac
%endif

# us-international keymap
install -m 0644 %{_sourcedir}/us-intl.kmap.gz %buildroot/%{kbddir}/keymaps/i386/qwerty/

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
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


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/profile.d/configure_keyboard.sh
%dir %{kbddir}
%{kbddir}/consolefonts
%{kbddir}/consoletrans
%dir %{kbddir}/keymaps
%{kbddir}/unidata
%{kbddir}/keymaps/include
%{kbddir}/keymaps/i386
# (sb) leave in the event user really wants mac keymaps
%ifarch ppc
%{kbddir}/keymaps/mac
%endif
/bin/consolechars
/bin/kbd_mode
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
/lib/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
/lib/*.so
%{_libdir}/*.la
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
* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3
- move kbd_mode and consolechars and the libs to / so they can be
  used prior to mounting other partitions
- spec cleanups
- fix the stupid relocation of %_datadir which resulted in manpages
  being installed in the wrong place

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3
- drop the useless initscripts (kdbconfig supposedly configures the
  /etc/sysconfig/keyboard file, but we don't have that program)

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2.3
- spec cleanups
- remove locales

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
