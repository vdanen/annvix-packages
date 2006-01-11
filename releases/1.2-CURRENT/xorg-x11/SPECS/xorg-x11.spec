#
# spec file for package xorg-x11
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		xorg-x11
%define version		6.8.2
%define release		%_revrel

%global _unpackaged_files_terminate_build	0

%define renderver	0.8
%define xrenderver	0.8.4
%define xftver		2.1.6

# looks like parallel build is broken
%define single_build	1

%define with_fastbuild			1

%define x11prefix	%{_prefix}/X11R6
%define x11bindir	%{x11prefix}/bin
# Architecture independant config files
%define x11libdir	%{x11prefix}/lib
# Architecture dependent libraries and modules
%define x11shlibdir	%{x11prefix}/%{_lib}
%define _tlsdir		tls
%define x11icondir      /usr/share/icons

%define xflib  %mklibname xorg-x11
%define xfdev  %{xflib}-devel
%define xfsta  %{xflib}-static-devel

%define old_xflib  %mklibname xfree 86
%define old_xfdev  %{old_xflib}-devel
%define old_xfsta  %{old_xflib}-static-devel


# define arches that can support 32-bit DRM thunks
%define drm_ioctl32_arches noarch


%define usefreetype2		1
%define usefreetype218		0

%define build_speedo_fonts	1
%define build_type1_fonts	1

%define build_composite		1

%if %{usefreetype2}
%define usefreetype218		0
%define buildfreetype2		0
%endif

#add some comattibility symlinks ? (xf86cfg, xf86config, xkb rules )
%define build_compat		1
#We're using the new fontconfig based Xft1 1.2 lib now.
%define with_new_fontconfig_Xft 0
%define with_new_fontconfig_Xft 1

%define build_nosrc		0
%{?_with_nosrc: %global build_nosrc 1}
%{?_without_src: %global build_nosrc 1}

%define build_multiarch 1

Summary: 	Part of the X Window System
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/X11
URL:		http://www.x.org/
Requires:	pam >= 0.66-18, util-linux, sh-utils, xinitrc >= 2.4.4-10mdk
Requires:	/lib/cpp
Requires:	%{xflib} = %{version}
Requires:	%{name}-xauth

Prereq:		/sbin/chkconfig utempter X11-libs = %{version}
%if %{with_new_fontconfig_Xft}
PreReq:		fontconfig
%endif

BuildRequires:	zlib-devel flex bison groff pam-devel ncurses-devel perl
BuildRequires:	libpng-devel libexpat-devel
%if %{usefreetype2}
BuildRequires:	freetype2-devel
%endif
# We need fontconfig for the new Xft1
%if %{with_new_fontconfig_Xft}
BuildRequires:	fontconfig-devel >= 2.1-4mdk
%endif


BuildRoot: %{_buildroot}/%{name}-%{version}
Obsoletes: X11-ISO8859-2, X11-ISO8859-9
Provides: X11-ISO8859-2, X11-ISO8859-9
Obsoletes: XFree86
Provides: XFree86 = %{version}-%{release}
Provides: X11 = %{version}-%{release}
Provides: fonts-ttf-vera
Obsoletes: fonts-ttf-vera

Source0: http://freedesktop.org/~xorg/X11R%{version}/src/single/X11R%{version}-src.tar.bz2
%if %{build_nosrc}
NoSource: 0
%endif
Source13: xserver.pamd
Source14: xdm.pamd
Source15: xfs.init
Source16: xfs.config
#Source18: xdm.init
Source19: twm.method
Source20: system.twmrc
#Source21: http://keithp.com/~keithp/fonts/XftConfig
# from Arnd Bergmann <std7652@et.FH-Osnabrueck.DE>
# only used when not build with fontconfig
Source21: XftConfig

Source50: http://freedesktop.org/~xlibs/release/render-%{renderver}.tar.bz2
Source51: http://freedesktop.org/~xlibs/release/libXrender-%{xrenderver}.tar.bz2
Source52: http://freedesktop.org/~xlibs/release/libXft-%{xftver}.tar.bz2

Source100: Euro.xmod
Source102: eurofonts-X11.tar.bz2
# extra *.enc files for xfs server not (yet) in XFree86 -- pablo
Source152: xfsft-encodings.tar.bz2
# locale.dir, compose.dir, locale.alias files.
# maintaining them trough patches is a nightmare, as they change
# too much too often; it is easier to manage them separately -- pablo
Source153: XFree86-compose.dir
Source154: XFree86-locale.alias
Source155: XFree86-locale.dir
#
Source156: gemini-koi8-u.tar.bz2
# the new default unicode compose file is too human-unfriendly; keeping
# the old one...
Source157: X_Compose-en_US.UTF-8

# I18n updates from Pablo
# Devanagari OpenType font, to install for the indic opentype patch -- pablo
Source160: XFree86-extrascalablefonts-font.tar.bz2

# Wonderland mouse cursor (Fedora)
Source212: wonderland-cursors.tar.bz2

Patch4:	X11R6.7.0-libfreetype-xtt2-1.2a.patch
Patch5:	Xorg-6.7.0-isolate_device.patch
#Patch5:	XFree86-4.3-PrefBusID-v3.patch.bz2

# Libs patches #################################################################

# X server patches #############################################################

Patch200: XFree86-4.2.99.3-parallel-make.patch
Patch201: XFree86-4.2.99.3-mandrakelinux-blue.patch
Patch202: XFree86-4.3.99.901-xwrapper.patch

# Build the following libraries with PIC: libxf86config, libXau, libxkbfile
Patch210: XFree86-4.3-build-libs-with-pic.patch

Patch213: XFree86-4.3.0-gb18030.patch
Patch214: XFree86-4.3.0-gb18030-enc.patch

Patch216: XFree86-4.3-_LP64-fix.patch

# Drivers patches ##############################################################

# Patch for building in Debug mode
Patch700: XFree86-4.2.99.3-acecad-debug.patch

# Xorg patches
# https://bugs.freedesktop.org/show_bug.cgi?id=2164
Patch5000: xorg-x11-6.8.2-radeon-render.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=2380
Patch5001: xorg-x11-6.8.2-nv-ids.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=2467
Patch5002: xorg-x11-6.8.2-void-driver.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=2698
Patch5003: xorg-x11-6.8.2-radeon-merge.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=2599
Patch5004: xorg-x11-6.8.2-xnest-stacking.patch

# RH patches

Patch9325: xorg-x11-6.8.2-gcc4-fix.patch
Patch9327: xorg-x11-6.8.2-ati-radeon-gcc4-fix.patch
#(sb) partially from fedora commits
Patch9328: xorg-x11-6.8.2-gcc40.patch

Patch9601: XFree86-4.3.99.902-mozilla-flash.patch

Patch10012: xorg-redhat-libGL-exec-shield-fixes.patch
Patch10015: XFree86-4.3.0-redhat-nv-riva-videomem-autodetection-debugging.patch

Patch10101: XFree86-4.3.0-makefile-fastbuild.patch


# my addons (svetljo)

# build freetype2 with fPIC on x86_64
Patch40002: lib_freetype_module.patch  

# p5000 https://bugs.freedesktop.org/show_bug.cgi?id=2073
Patch50000: xorg-x11-6.8.2-sunffb.patch

%description
If you want to install the X Window System (TM) on
your machine, you'll need to install X11.

The X Window System provides the base technology
for developing graphical user interfaces. Simply stated,
X draws the elements of the GUI on the user's screen and
builds methods for sending user interactions back to the
application. X also supports remote application deployment--running an
application on another computer while viewing the input/output 
on your machine.  X is a powerful environment which supports
many different applications, such as games, programming tools,
graphics programs, text editors, etc.

This package contains the basic fonts, programs and documentation
for an X workstation.  You will also need the X11-server
package, which contains the program which drives your video
hardware.

In addition to installing this package, you will need to install the
drakxtools package to configure your card using XFdrake. You may also
need to install one of the X11 fonts packages.

And finally, if you are going to develop applications that run as 
X clients, you will also need to install %{xfdev}.


%package -n %{xflib}
Summary: Shared libraries needed by the X Window System version 11 release 6
Group: System/Libraries
Prereq: grep /sbin/ldconfig
Provides: libXft2
Obsoletes: libXft2
Provides: X11-libs = %{version}-%{release}
Provides: XFree86-libs = %{version}-%{release}
Obsoletes: XFree86-libs
%ifarch sparc
Obsoletes: X11R6.1-libs
%endif
Provides: %{old_xflib} = %{version}-%{release}
Obsoletes: %{old_xflib}

%description -n %{xflib}
X11-libs contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

If you are installing the X Window System on your machine, you will need to
install X11-libs.  You will also need to install the X11 package,
the X11-75dpi-fonts package or the X11-100dpi-fonts package
(depending upon your monitor's resolution), the Xconfigurator package and
the X11R6-contrib package.  And, finally, if you are going to be developing
applications that run as X clients, you will also need to install
%{xfdev}.

%package -n %{xfdev}
Summary: Headers and programming man pages
Group: Development/C
Obsoletes: Mesa-devel
Provides: Mesa-devel
Provides: Xft-devel
Provides: libXft2-devel
Provides: XFree86-devel = %{version}-%{release}
Provides: X11-devel
Obsoletes: XFree86-devel
Obsoletes: libXft2-devel
%ifarch sparc
Obsoletes: X11R6.1-devel
%endif
Requires: %{xflib} = %{version}, glibc-devel, /lib/cpp
%if %{with_new_fontconfig_Xft}
Requires: fontconfig-devel >= 2.1-4mdk
%endif
%if %{build_multiarch}
Requires: multiarch-utils >= 1.0.7-1mdk
BuildRequires: multiarch-utils >= 1.0.7-1mdk
%endif
Provides: %{old_xfdev} = %{version}-%{release}
Obsoletes: %{old_xfdev}

%description -n %{xfdev}
%{xfdev} includes the libraries, header files and documentation
you'll need to develop programs which run in X clients. X11 includes
the base Xlib library as well as the Xt and Xaw widget sets.

For guidance on programming with these libraries, O'Reilly & Associates
produces a series on X programming which you might find useful.

Install %{xfdev} if you are going to develop programs which
will run as X clients.

If you need the static libraries, install the %{xfsta}
package.

%package -n %{xfsta}
Summary: X11R6 static libraries
Group: System/Libraries
Requires: %{xfdev} = %{version}
Obsoletes: XFree86-static-libs
Provides: XFree86-static-libs = %{version}-%{release}
Provides: XFree86-static-devel = %{version}-%{release}
Provides: X11-static-devel = %{version}-%{release}
Provides: %{old_xfsta} = %{version}-%{release}
Obsoletes: %{old_xfsta}


%description -n %{xfsta}
%{xfsta} includes the X11R6 static libraries needed to
build statically linked programs.


%define now 0

%prep
%setup -q -c

# X server patches

%patch200 -p1 -b .parallel-make
%patch201 -p1 -b .mandrakelinux-blue
%patch202 -p1 -b .xwrapper

%if %now
%patch213 -p0 -b .gb18030
%patch214 -p0 -b .gb18030-enc
%endif

%patch210 -p1 -b .build-libs-with-pic

%if %now
%patch216 -p1 -b ._LP64-fix
%endif

%patch5000 -p1 -b .radeon-render
%patch5001 -p1 -b .nv-ids
%patch5002 -p1 -b .void-driver
%patch5003 -p1 -b .radeon-merge
%patch5004 -p1 -b .xnest-stacking

%if 0
%patch9325 -p0 -b .gcc4-fix
%patch9327 -p0 -b .ati-radeon-gcc4-fix
%endif
%patch9328 -p1 -b .gcc40
%patch9601 -p0 -b .mozilla-flash
#patch10012 -p0 -b .redhat-libGL-exec-shield-fixes
%patch10015 -p0 -b .redhat-nv-riva-videomem-autodetection-debugging

%patch10101 -p0 -b .redhat_makefile-fastbuild

#disable for now

pushd xc

%ifarch alpha x86_64
%patch40002 -p1 -b .x86-64_lib_font-build_with_fPIC
%endif

popd

# https://bugs.freedesktop.org/show_bug.cgi?id=2073
%patch50000 -p0 -b .sunffb

# backup the original files (so we can look at them later) and use our own
cp xc/nls/compose.dir xc/nls/compose.dir.orig
cp xc/nls/locale.alias xc/nls/locale.alias.orig
cp xc/nls/locale.dir xc/nls/locale.dir.orig
cp xc/nls/Compose/en_US.UTF-8 xc/nls/Compose/en_US.UTF-8.orig
cat %{SOURCE153} | sed 's/#/XCOMM/g' > xc/nls/compose.dir
cat %{SOURCE154} | sed 's/#/XCOMM/g' > xc/nls/locale.alias
cat %{SOURCE155} | sed 's/#/XCOMM/g' > xc/nls/locale.dir
cat %{SOURCE157} | sed 's/^#/XCOMM/g' > xc/nls/Compose/en_US.UTF-8
# pt_BR Compose file only purpose is to allow dead_actute+c -> ccedilla
cat %{SOURCE157} | sed 's/^#/XCOMM/g' | \
	sed 's/<dead_acute> <C> : "Ć" Cacute/<dead_acute> <C> : "Ç" Ccedilla/' | \
	sed 's/<dead_acute> <c> : "ć" cacute/<dead_acute> <c> : "ç" ccedilla/' \
	> xc/nls/Compose/pt_BR.UTF-8


# (gb) Check for constants merging capabilities to disable
NO_MERGE_CONSTANTS=$(if %{__cc} -fno-merge-constants -S -o /dev/null -xc /dev/null >/dev/null 2>&1; then echo "-fno-merge-constants"; fi)

# Build with -fno-strict-aliasing if gcc >= 3.1 is used
NO_STRICT_ALIASING=$(%{__cc} -dumpversion | awk -F "." '{ if (int($1)*100+int($2) >= 301) print "-fno-strict-aliasing" }')

# compiling with -g is too huge
RPM_OPT_FLAGS=`echo %{optflags} | sed 's/-g//'`

echo "configuring with $RPM_OPT_FLAGS"
%if %{build_multiarch}
HostDef=host-%{_arch}.def
cp /usr/X11R6/lib/X11/config/multiarch-dispatch-host.def xc/config/cf/multiarch-dispatch-host.def
cat >xc/config/cf/host.def <<END
#if defined(UseInstalled)
#include "/usr/X11R6/lib/X11/config/multiarch-dispatch-host.def"
#else
#include "multiarch-dispatch-host.def"
#endif
END
%else
HostDef=host.def
%endif

cat >xc/config/cf/$HostDef <<END

#define DefaultGcc2i386Opt	$RPM_OPT_FLAGS $NO_STRICT_ALIASING -fno-strength-reduce
#define DefaultGcc2AxpOpt	$RPM_OPT_FLAGS $NO_STRICT_ALIASING
#define DefaultGcc2PpcOpt	$RPM_OPT_FLAGS $NO_STRICT_ALIASING
#define DefaultGcc2x86_64Opt	$RPM_OPT_FLAGS $NO_STRICT_ALIASING

#define NeedModuleRanlib	YES
#define ModuleCFlags \$(CDEBUGFLAGS) \$(CCOPTIONS) $NO_MERGE_CONSTANTS \
\$(THREAD_CFLAGS) \$(ALLDEFINES) -fno-strength-reduce
#define ModuleRanlibCmd		RanlibCmd
#define UseImplicitMake		YES

#define HasAgpGart		YES
#define HasLdRunPath		NO
#define InstallXserverSetUID	NO
#define BuildServersOnly        NO
#define HasPam			YES
#define HasZlib			YES
#define HasExpat		YES
#define HasLibxml2		YES
%if %{with_new_fontconfig_Xft}
#define UseFontconfig		YES
#define HasFontconfig		YES
%endif
#define UseFreetype2		YES
#define FreeTypeLibDir		%{_libdir}
#define FreeTypeIncDir		/usr/include/freetype
#define FreeTypeLibName		ttf
%if %{usefreetype2}
%if %{buildfreetype2}
#define BuildFreetype2Library   YES
%else
#define HasFreetype2		YES
#define Freetype2Dir            /usr
#define Freetype2LibDir		%{_libdir}
#define Freetype2IncDir		/usr/include/freetype2
%endif
%else
#define BuildFreetype2Library   NO
%endif
#define HasBlindFaithInUnicode	YES
#define BuildFonts		YES
#define BuildCyrillicFonts	YES
%if %{build_speedo_fonts}
#define BuildSpeedo		YES
#define BuildSpeedoFonts	YES
%endif
%if %{build_type1_fonts}
#define BuildType1		YES
%endif
#define BuildXF86MiscExt	YES

%if %{build_composite}
#define BuildComposite		YES
%else
#define BuildComposite		NO
%endif

#define XprtServer		NO

#define UseDeprecatedKeyboardDriver Yes

#define XVendorString		"Mandriva Linux (X.Org X11 %{version}, patch level %{release})"
#define UseInternalMalloc	NO
#define ForceNormalLib		YES
#define NormalLibFont		YES
#define UseXserverWrapper	YES
#define BuildXF86DRI		YES
#define BuildXF86DRM		NO
#define UseGccMakeDepend	NO
#define HasLinuxInput		YES
#define LinkGLToUsrInclude	NO
#define LinkGLToUsrLib		NO

#define SharedLibXdmGreet       NO
#define SharedLibXxf86dga       NO
#define SharedLibXv             NO
#define NormalLibXxf86dga       YES
#define NormalLibXv             YES

#define NormalLibXinerama	YES
#define NormalLibFS		YES
#define NormalLibXxf86vm	YES
#define NormalLibXxf86misc	YES
#define NormalLibFontEnc	YES
#define NormalLibXss		YES

#define SharedLibXinerama	YES
#define SharedLibFS		YES
#define SharedLibXxf86vm	YES
#define SharedLibXxf86misc	YES
#define SharedLibFontEnc	YES
#define SharedLibXss		YES

#define LbxproxyDir 		/etc/X11/lbxproxy
#define ProxyManagerDir 	/etc/X11/proxymngr
#define ServerConfigDir 	/etc/X11/xserver
#define XdmDir 			/etc/X11/xdm
#define XConfigDir 		/etc/X11
#define XinitDir 		/etc/X11/xinit

#define DefaultCursorTheme	wonderland

#define HaveMatroxHal		NO
#define UseMatroxHal		NO

/* Let's build libraries which only come in static form with PIC so
   that KDE can be prelink'able. */
%ifarch %{ix86}
#define StaticNeedsPicForShared YES
%endif


%ifarch %{ix86}
#define DevelDRIDrivers

#define DriDrivers            gamma i810 i915 mga r128 radeon r200 \
                                sis tdfx DevelDRIDrivers
%endif

%ifarch alpha
#define XF86CardDrivers mga nv tga s3virge sis rendition \
			neomagic i740 tdfx cirrus tseng trident chips apm \
			fbdev ati vga v4l glint
%endif
%ifarch x86_64
#define XF86CardDrivers mga fbdev vga ati savage nv glint vesa i810 \
			tga s3virge sis rendition neomagic cirrus tseng \
			trident chips apm fbdev ati vga v4l tdfx vmware \
			DevelDrivers XF86OSCardDrivers XF86ExtraCardDrivers
%endif
%ifarch ia64
#define XF86CardDrivers mga nv s3virge sis rendition i740 \
			tdfx v4l fbdev glint ati vga 
%endif
%ifarch ppc
#define DevelDRIDrivers
                  
#define DriDrivers            gamma mga r128 radeon r200 \
                                tdfx DevelDRIDrivers

#define XF86CardDrivers mga glint s3virge sis savage \
                        trident chips tdfx fbdev ati \
			DevelDrivers vga nv \
			XF86OSCardDrivers XF86ExtraCardDrivers
%endif

#define ExtraXInputDrivers acecad

/* Make the chapter 4 and 7 manpages FHS compliant.  The \ escape is */
/* necessary to avoid command subsitution in the here document.        */
#define DriverManDir    \$(MANSOURCEPATH)4
#define DriverManSuffix 4x /* use just one tab or cpp will die */
#define MiscManDir      \$(MANSOURCEPATH)7
#define MiscManSuffix   7x /* use just one tab or cpp will die */

/* font encodings not to build */ 
#define BuildISO8859_3Fonts		NO
#define BuildISO8859_4Fonts		NO
#define BuildISO8859_10Fonts	NO
#define BuildISO8859_14Fonts	NO
END

cp xc/config/cf/$HostDef xc/config/cf/$HostDef.tls
echo '#define GlxUseThreadLocalStorage YES' >> xc/config/cf/$HostDef.tls



%build

# compiling with -g is too huge
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's/-g//'`

echo "compiling with $RPM_OPT_FLAGS"

[ -z "$RPM_BUILD_NCPUS" ] && RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -gt 1 ] && PARALLELMFLAGS="-j$RPM_BUILD_NCPUS"

# Build with -fno-strict-aliasing if gcc >= 3.1 is used
NO_STRICT_ALIASING=$(%{__cc} -dumpversion | awk -F "." '{ if (int($1)*100+int($2) >= 301) print "-fno-strict-aliasing" }')

RPM_OPT_FLAGS="$RPM_OPT_FLAGS $NO_STRICT_ALIASING -DHAVE_FT_BITMAP_SIZE_Y_PPEM"

%ifarch alpha
make World -C xc CDEBUGFLAGS="$RPM_OPT_FLAGS -Wa,-m21164a" \
	DEFAULTFONTPATH="/usr/X11R6/lib/X11/fonts/misc:unscaled,unix/:-1"
#	MAKE="make -j$NPROCS"
# we are having problems with the compiler on alpha.
make -C xc/programs/xterm CDEBUGFLAGS="-Wa,-m21164a"
make -C xc
rm xc/programs/xfs/os/io.o
pushd xc/programs/xfs/os
make CDEBUGFLAGS=""
cd ..
rm xfs
make CDEBUGFLAGS=""
popd
%else
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS|sed 's/-fomit-frame-pointer//'|sed 's/-ffast-math//')
make World -C xc CC="gcc" CXX="g++" CDEBUGFLAGS="$RPM_OPT_FLAGS" \
	CXXDEBUGFLAGS="$RPM_OPT_FLAGS" \
	DEFAULTFONTPATH="/usr/X11R6/lib/X11/fonts/misc:unscaled,unix/:-1" \
%if ! %single_build
	TOPPARALLELMFLAGS="$PARALLELMFLAGS" \
%endif
%if %{with_fastbuild}
	WORLDOPTS= FAST=1 \
%endif
	
%endif

echo PACKAGING DOCUMENTATION
# rezip these - they are in the old compress format
find xc/doc/hardcopy -name \*.PS.Z | xargs gzip -df
find xc/doc/hardcopy -name \*.PS | xargs gzip -f

#groff -Tascii -ms xc/doc/misc/RELNOTES.ms > xc/doc/hardcopy/RELNOTES.txt
cp -f xc/programs/Xserver/hw/xfree86/doc/RELNOTES xc/doc/hardcopy/RELNOTES.txt
rm -rf xc/doc/hardcopy/BDF/*
groff -Tascii -ms xc/doc/specs/BDF/bdf.ms > xc/doc/hardcopy/BDF/bdf.txt
rm -rf xc/doc/hardcopy/CTEXT/*
groff -Tascii -ms xc/doc/specs/CTEXT/ctext.tbl.ms >xc/doc/hardcopy/CTEXT/ctext.tbl.txt
rm -rf xc/doc/hardcopy/FSProtocol/*
groff -Tascii -ms xc/doc/specs/FSProtocol/protocol.ms >xc/doc/hardcopy/FSProtocol/protocol.txt
rm -rf xc/doc/hardcopy/ICCCM/*
groff -Tascii -ms xc/doc/specs/ICCCM/icccm.ms >xc/doc/hardcopy/ICCCM/icccm.txt
rm -rf xc/doc/hardcopy/ICE/*
groff -Tascii -ms xc/doc/specs/ICE/ICElib.ms >xc/doc/hardcopy/ICE/ICElib.txt
groff -Tascii -ms xc/doc/specs/ICE/ice.ms > xc/doc/hardcopy/ICE/ice.txt
cp xc/doc/specs/PM/PM_spec xc/doc/hardcopy/ICE
rm -rf xc/doc/hardcopy/SM/*
groff -Tascii -ms xc/doc/specs/SM/SMlib.ms > xc/doc/hardcopy/SM/SMlib.txt
rm -rf xc/doc/hardcopy/XDMCP/*
groff -Tascii -ms xc/doc/specs/XDMCP/xdmcp.ms >xc/doc/hardcopy/XDMCP/xdmcp.txt
rm -rf xc/doc/hardcopy/XIM/*
groff -Tascii -ms xc/doc/specs/XIM/xim.ms > xc/doc/hardcopy/XIM/xim.txt
rm -rf xc/doc/hardcopy/XLFD/*
groff -Tascii -ms xc/doc/specs/XLFD/xlfd.tbl.ms >xc/doc/hardcopy/XLFD/xlfd.tbl.txt


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/etc/pam.d
install -m 644 %{SOURCE13} %{buildroot}/etc/pam.d/xserver
install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/xdm
mkdir -p %{buildroot}/etc/security/console.apps
touch %{buildroot}/etc/security/console.apps/xserver

mkdir -p %{buildroot}/usr/include
rm -f %{buildroot}/usr/include/X11

make DESTDIR=%{buildroot} install install.man -C xc
mkdir -p %{buildroot}/etc/X11

# remove libGLU (in Mesa-common)
rm -f %{buildroot}/usr/X11R6/%{_lib}/libGLU*
rm -f %{buildroot}/usr/X11R6/include/GL/glu.h
rm -f %{buildroot}/usr/X11R6/man/man3/glu

# XftConfig (only if not using fontconfig)
%if %{with_new_fontconfig_Xft}
cat <<-EOF > %{buildroot}/etc/X11/XftConfig.README-OBSOLETE
# IMPORTANT NOTICE about XftConfig:
#
# The XftConfig config file has been deprecated and obsoleted by
# /etc/fonts/fonts.conf, which is the new font configuration file for Xft2, and
# is provided by "fontconfig".  A backward compatible Xft1 library is also
# provided which has been converted to use fontconfig also and provide users
# with a single way of configuring client side fonts, while retaining binary
# compatibility. For information on configuring fonts using fontconfig,
# please consult the fontconfig documentation.
EOF
%else
install -m 644 %{SOURCE21} %{buildroot}/etc/X11/XftConfig
rm -f %{buildroot}/usr/X11R6/lib/X11/XftConfig
cd %{buildroot}/usr/X11R6/lib/X11; ln -s ../../../../etc/X11/XftConfig; cd -
%endif

# we don't want the libz.a from XFree86 -- it's broken
rm -f %{buildroot}/usr/X11R6/%{_lib}/libz.a

# we don't want libXpm from XFree86
rm -f %{buildroot}/usr/X11R6/%{_lib}/libXpm*
rm -f %{buildroot}/usr/X11R6/include/X11/{Xpm.h,xpm.h}

# setup the default X server
rm -f %{buildroot}/usr/X11R6/bin/X
ln -s Xwrapper %{buildroot}/usr/X11R6/bin/X

# explicitly create X authdir
mkdir -p %{buildroot}/etc/X11/xdm/authdir
chmod 0700 %{buildroot}/etc/X11/xdm/authdir

# Move config config stuff to /etc/X11
mkdir -p %{buildroot}/etc/X11
#ln -sf ../../../../etc/X11/XF86Config %{buildroot}/usr/X11R6/lib/X11/XF86Config
#mv %{buildroot}/usr/X11R6/lib/X11/XF86Config.eg %{buildroot}/usr/X11R6/lib/X11/xorg.conf.eg

# for i in twm fs xsm; do
#     rm -rf %{buildroot}/etc/X11/$i
#     cp -ar %{buildroot}/usr/X11R6/lib/X11/$i %{buildroot}/etc/X11
#     rm -rf %{buildroot}/usr/X11R6/lib/X11/$i
#     ln -sf ../../../../etc/X11/$i %{buildroot}/usr/X11R6/lib/X11/$i
# done

# This one is on xinitrc package now.
## install replacement Xsession file for xdm
#install -m 755 $RPM_SOURCE_DIR/Xsession.mandrake \
#      %{buildroot}/etc/X11/xdm/Xsession

# we install our own config file for the xfs package
mkdir -p %{buildroot}/etc/X11/fs
install -m 644 %{SOURCE16} %{buildroot}/etc/X11/fs/config
mkdir -p %{buildroot}/etc/rc.d/init.d
rm -rf %{buildroot}/etc/init.d
rm -rf %{buildroot}/etc/rc.d/rc*
rm -rf %{buildroot}/etc/rc{0,1,2,3,4,5,6}.d
install -m 755 %{SOURCE15} %{buildroot}/etc/rc.d/init.d/xfs

# install service for xdm
#install -m 755 $RPM_SOURCE_DIR/xdm.init \
#	%{buildroot}/etc/rc.d/init.d/xdm

# we get xinit from a separate package
rm -rf %{buildroot}/usr/X11R6/lib/X11/xinit
ln -sf ../../../../etc/X11/xinit %{buildroot}/usr/X11R6/lib/X11/xinit

# Fix up symlinks
mkdir -p %{buildroot}/usr/bin %{buildroot}/usr/man
mkdir -p %{buildroot}/usr/include %{buildroot}/usr/lib
ln -sf ../X11R6/bin %{buildroot}/usr/bin/X11
ln -sf ../X11R6/man %{buildroot}/usr/man/X11
ln -sf ../X11R6/include/X11 %{buildroot}/usr/include/X11
ln -sf ../X11R6/lib/X11 %{buildroot}/usr/lib/X11

%if %build_compat
# some more compatibility links

#ln -sf ../../../../../../etc/X11/xkb/rules/xorg.lst %{buildroot}/usr/X11R6/lib/X11/xkb/rules/xfree.lst
#ln -sf ../../../../../../etc/X11/xkb/rules/xorg-it.lst %{buildroot}/usr/X11R6/lib/X11/xkb/rules/xfree-it.lst
#ln -sf ../../../../../../etc/X11/xkb/rules/xorg.xml %{buildroot}/usr/X11R6/lib/X11/xkb/rules/xfree.xml

ln -sf xorg.lst %{buildroot}/usr/X11R6/lib/X11/xkb/rules/xfree86.lst
ln -sf xorg-it.lst %{buildroot}/usr/X11R6/lib/X11/xkb/rules/xfree86-it.lst
ln -sf xorg.xml %{buildroot}/usr/X11R6/lib/X11/xkb/rules/xfree86.xml

# binaries
ln -sf Xorg %{buildroot}/usr/X11R6/bin/XFree86
ln -sf xorgcfg %{buildroot}/usr/X11R6/bin/xf86cfg
ln -sf xorgconfig %{buildroot}/usr/X11R6/bin/xf86config
%endif
# this gets the wrong permissions by default -- I don't know or care why
chmod 755 %{buildroot}/usr/X11R6/lib/X11/xkb/geometry/sgi

# this certainly doesn't need to be setuid
chmod 755 %{buildroot}/usr/X11R6/bin/dga

# setup paths to use the build tree instead of the system one
PATH=%{buildroot}/usr/X11R6/bin:$PATH
export PATH
LD_LIBRARY_PATH=%{buildroot}%{x11shlibdir}
export LD_LIBRARY_PATH


%define mkfontdir mkfontscale -b -s -l

# EURO support
cd %{buildroot}/usr/X11R6/lib/X11/fonts/misc;
 tar xjf %{SOURCE102}
 bdftopcf -t Xlat9-8x14.bdf |gzip -9 >Xlat9-8x14-lat9.pcf.gz;
 bdftopcf -t Xlat9-9x16.bdf |gzip -9 >Xlat9-9x16-lat9.pcf.gz;
 rm -f *.bdf
 chmod +w %{buildroot}/usr/X11R6/lib/X11/fonts/misc/fonts.dir
 %mkfontdir %{buildroot}/usr/X11R6/lib/X11/fonts/misc
cd -

# fixing a bug in XFree86 that uses two different directories instead
# of only one...
if [ ! -r %{buildroot}/usr/X11R6/lib/X11/locale/zh_CN/XI18N_OBJS ]; then
	mv %{buildroot}/usr/X11R6/lib/X11/locale/zh/XI18N_OBJS \
		%{buildroot}/usr/X11R6/lib/X11/locale/zh_CN/
	rmdir %{buildroot}/usr/X11R6/lib/X11/locale/zh
fi

if [ ! -r %{buildroot}/usr/X11R6/lib/X11/locale/zh_CN.UTF-8/XI18N_OBJS ]; then
        cp -p %{buildroot}/usr/X11R6/lib/X11/locale/zh_TW.UTF-8/XI18N_OBJS %{buildroot}/usr/X11R6/lib/X11/locale/zh_CN.UTF-8/XI18N_OBJS
fi

#======================
# a dirty hack to make japanese, polish etc display correctly -- pablo
chmod u+w %{buildroot}/usr/X11R6/lib/X11/locale/*/*

for i in %{buildroot}/usr/X11R6/lib/X11/locale/* 
do
	# make empty Compose files for some locales
	# CJK must not have that file (otherwise XIM don't works some times)
	case `basename $i` in
	C|microsoft-*|iso8859-*|koi8-*)
		if [ -d $i ]; then
        	touch $i/Compose
		fi
		;;
	ja*|ko*|zh*)
		if [ -r "$i/Compose" ]; then
			rm $i/Compose
		fi
		;;
	esac

done

# fix dead_{acute,diaeresesis} + space (needed for us_intl kbd)
for i in %{buildroot}/usr/X11R6/lib/X11/locale/*/Compose
do
  cp $i tmpfile
  cat tmpfile | \
  sed 's/<dead_diaeresis> <space>.*$/<dead_diaeresis> <space> : "\\"" quotedbl/' | \
  sed "s/<dead_acute> <space>.*$/<dead_acute> <space> : \"'\" apostrophe/" \
  > $i
done
rm -f tmpfile

# Encoding files for xfsft font server
bzcat %{SOURCE152} | tar xf - -C %{buildroot}
gzip -9 -f %{buildroot}/usr/X11R6/lib/X11/fonts/encodings/*.enc || :
gzip -9 -f %{buildroot}/usr/X11R6/lib/X11/fonts/encodings/large/*.enc || :
%mkfontdir -e %{buildroot}/usr/X11R6/lib/X11/fonts/encodings \
	-e %{buildroot}/usr/X11R6/lib/X11/fonts/encodings/large
rm -f %{buildroot}/usr/X11R6/lib/X11/fonts/encodings/encodings.dir 
cat encodings.dir | sed "s|%{buildroot}||" \
	> %{buildroot}/usr/X11R6/lib/X11/fonts/encodings/encodings.dir
cat encodings.dir | sed "s|%{buildroot}||" \
	> %{buildroot}/etc/X11/encodings.dir
%if !%{with_new_fontconfig_Xft}
/usr/X11R6/bin/xftcache %{buildroot}/usr/X11R6/lib/X11/fonts/Type1/ || \
	touch %{buildroot}/usr/X11R6/lib/X11/fonts/Type1/XftCache
/usr/X11R6/bin/xftcache %{buildroot}/usr/X11R6/lib/X11/fonts/TTF/ || \
	touch %{buildroot}/usr/X11R6/lib/X11/fonts/TTF/XftCache
%endif

# gemini-koi8 fonts
tar jxvf %{SOURCE156} -C %{buildroot}/usr/X11R6/lib/X11/fonts
grep '^!' %{buildroot}/usr/X11R6/lib/X11/fonts/ukr/fonts.alias > \
	README-ukr-fonts
rm -f %{buildroot}/usr/X11R6/lib/X11/fonts/ukr/fonts.alias
cd %{buildroot}/usr/X11R6/lib/X11/fonts/ukr
gunzip *.Z
gzip -9 *.pcf
%mkfontdir
cd -
pwd

# installing the extra OpenType fonts
mkdir -p %{buildroot}/usr/share/fonts/otf/mdk
(
	cd %{buildroot}/usr/share/fonts/otf/mdk
	bzcat %{SOURCE160} | tar xvf -
	%if %{with_new_fontconfig_Xft}
    rm -f %{buildroot}/usr/share/fonts/otf/mdk/XftCache
	%else
    /usr/X11R6/bin/xftcache %{buildroot}/usr/share/fonts/otf/mdk/ || \
	touch %{buildroot}/usr/share/fonts/otf/mdk/XftCache
	%endif
)

# List modules without glide_drv.o
rm -f %{buildroot}%{x11shlibdir}/modules/dri/tdfx_dri.so

rm -f modules.list
find %{buildroot}%{x11shlibdir}/modules -type f -print | egrep -v 'glide_dri.so' | sed s@%{buildroot}@@ > modules.list

# temporary hack: we build with freetype2 from the source but we don't ship it
rm -f %{buildroot}%{x11libdir}/libfreetype*
rm -rf %{buildroot}%{x11prefix}/include/freetype2
rm -f %{buildroot}%{x11bindir}/freetype-config

# Fix list of static libs to list only static lib without a dynamic one.
FILTER='libXau|libGLw|libfntstubs|liboldX|libxorgconfig|libxkbfile|libxkbui|libXfontcache|libXinerama|libXdmcp|libFS|libXss|libfontbase|libXv|libXxf86dga|libXxf86misc|libXxf86rush|libXxf86vm|libXvMC|libI810XvMC'
rm -f static.list
find %{buildroot}%{x11shlibdir} -type f -maxdepth 1 -name '*.a' -print | egrep -v $FILTER | sed s@%{buildroot}@@ > static.list
rm -f static-only.list
find %{buildroot}%{x11shlibdir} -type f -maxdepth 1 -name '*.a' -print | egrep $FILTER | sed s@%{buildroot}@@ > static-only.list

#not needed, failsafe use twm
%if 0
mkdir -p %{buildroot}/etc/X11/wmsession.d
cat > %{buildroot}/etc/X11/wmsession.d/09Twm << EOF
NAME=Twm
DESC=TWM
EXEC=/usr/X11R6/bin/twm
SCRIPT:
exec /usr/X11R6/bin/twm
EOF
%endif

# remove xterm resources to avoid conflicts with the xterm package
rm -f %{buildroot}/etc/X11/app-defaults/*XTerm*

mkdir -p %{buildroot}/etc/logrotate.d
cat << EOF > %{buildroot}/etc/logrotate.d/xdm
/var/log/xdm-error.log {
    notifempty
    missingok
    nocompress
}
EOF

# for compatibility with the Linux/OpenGL standard base
mkdir -p %{buildroot}/usr/include
pushd %{buildroot}/usr/include
ln -sf ../X11R6/include/GL GL
popd

# quick fix
mkdir -p %{buildroot}/var/lib/xdm
pushd %{buildroot}/etc/X11/xdm
rm -f authdir
ln -sf ../../../var/lib/xdm authdir
popd

mkdir -p %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}%{x11shlibdir}/pkgconfig/*.pc %{buildroot}%{_libdir}/pkgconfig

%if 0
# Generate xrender.pc using 'EOF' style here document with no expansion
    cat <<-'EOF' > %{buildroot}%{_libdir}/pkgconfig/xrender.pc
        prefix=%{x11prefix}
        exec_prefix=%{x11bindir}
        libdir=%{x11shlibdir}
        includedir=%{x11prefix}/include

        Name: Xrender
        Description: X Render Library
        Version: %{xrenderver}
        Cflags: -I${includedir} -I%{x11prefix}/include
        Libs: -L${libdir} -lXrender -lX11
EOF
%endif

chmod 0644 %{buildroot}%{_libdir}/pkgconfig/*

mkdir -p %{buildroot}%{_iconsdir}
mv %{buildroot}/usr/X11R6/lib/X11/icons/* %{buildroot}%{_iconsdir}


# multiarch support
# XXX: properly fix imake later
%multiarch_binaries %{buildroot}%{x11bindir}/xcursor-config
%multiarch_binaries %{buildroot}%{x11bindir}/xft-config
%multiarch_binaries %{buildroot}%{x11bindir}/imake
[[ -f xc/config/cf/host-%{_arch}.def ]] && \
install -m 644 xc/config/cf/host-%{_arch}.def %{buildroot}%{x11libdir}/X11/config/

#make sure shared lib are writable by root
chmod 755 %{buildroot}%{x11shlibdir}/modules/dri/*.so %{buildroot}%{x11shlibdir}/modules/fonts/*.so 

# remove CVS dirs
find %{buildroot} -type d -a -name CVS | xargs rm -rf

# remove files not packaged

# this comes with hwdata
rm -f %{buildroot}%{x11libdir}/X11/Cards

%if %{with_new_fontconfig_Xft}
rm -f %{buildroot}%{_sysconfdir}/X11/{XftConfig,XftConfig-OBSOLETE} \
    %{buildroot}%{x11bindir}/xftcache \
    %{buildroot}%{x11libdir}/X11/XftConfig-OBSOLETE \
    %{buildroot}%{x11prefix}/man/man1/xftcache.*
%endif
# enabled luit [%{x11bindir}/luit, %{x11prefix}/man/man1/luit.*] (pablo)
rm -rf %{buildroot}%{_sysconfdir}/X11/twm/system.twmrc \
 %{buildroot}%{_sysconfdir}/X11/xdm/{*Console,X*,xdm-config} \
 %{buildroot}%{_sysconfdir}/X11/xdm/pixmaps \
 %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc \
 %{buildroot}%{x11bindir}/{cxpm,resize,sxpm,uxterm,xterm,xtrap*} \
 %{buildroot}%{x11prefix}/man/man1/{cxpm.*,pswrap.*,resize.*,showfont.*,sxpm.*,xterm.*,xtrap.*} \
 %{buildroot}%{x11libdir}/X11/{Options,XF86Config.98} \
 %{buildroot}%{x11libdir}/X11/fonts/{util,CID,local} \
 %{buildroot}%{x11prefix}/src/linux \
 %{buildroot}%{_bindir}/X11 \
 %{buildroot}%{_prefix}/lib/X11 \
 %{buildroot}/usr/man/X11

rm -f  %{buildroot}/usr/X11R6/bin/xphelloworld \
 %{buildroot}/usr/X11R6/bin/xplsprinters \
 %{buildroot}/usr/X11R6/bin/xprehashprinterlist \
 %{buildroot}/usr/X11R6/bin/xpsimplehelloworld \
 %{buildroot}/usr/X11R6/bin/xpxthelloworld \
 %{buildroot}/usr/X11R6/man/man1/xphelloworld.* \
 %{buildroot}/usr/X11R6/man/man1/xplsprinters.* \
 %{buildroot}/usr/X11R6/man/man1/xprehashprinterlist.* \
 %{buildroot}/usr/X11R6/man/man1/xpsimplehelloworld.* \
 %{buildroot}/usr/X11R6/man/man1/xpxthelloworld.* 
# %{buildroot}%{_sysconfdir}/X11/rstart \
# %{buildroot}%{_sysconfdir}/X11/xkb \


%post
%make_session

for d in misc Speedo Type1 TTF; do
    cd /usr/X11R6/lib/X11/fonts/$d
    mkfontdir || :
done

fc-cache -f /usr/X11R6/lib/X11/fonts || :

%if ! %{with_new_fontconfig_Xft}
xftcache > /dev/null 2>&1 || :
%endif

%postun
%make_session


%pre
# here, we put things that we have moved around (like directories)
# that need to be cleaned up prior to the RPM's installation.  
# Ugly. Necessary.
while read old new link; do
  if [ -d `dirname $old` -a ! -L $old ]; then
     echo "moving $old to $new linking to $link"
     if [ ! -d $new ]; then
        mkdir -p $new
     fi
     if [ -d $old ]; then
         mv -f $old/* $new
         rmdir $old
     fi
     ln -sf $link $old
  fi
done << EOF
/usr/X11R6/lib/X11/xkb /etc/X11/xkb ../../../../etc/X11/xkb
/usr/X11R6/lib/X11/xkb/compiled /var/lib/xkb ../../../../../var/lib/xkb
/usr/X11R6/lib/X11/app-defaults /etc/X11/app-defaults ../../../../etc/X11/app-defaults
/usr/X11R6/lib/X11/lbxproxy /etc/X11/lbxproxy ../../../../etc/X11/lbxproxy
/usr/X11R6/lib/X11/proxymngr /etc/X11/proxymngr ../../../../etc/X11/proxymngr
/usr/X11R6/lib/X11/rstart /etc/X11/rstart ../../../../etc/X11/rstart
/usr/X11R6/lib/X11/xserver /etc/X11/xserver ../../../../etc/X11/xserver
/etc/X11/xdm/authdir /var/lib/xdm ../../../var/lib/xdm
EOF

#%postun
#if [ $1 = 0 ]; then
#    /sbin/chkconfig --del xdm
#fi

%post -n %{xflib}
grep -q "^%{x11shlibdir}$" /etc/ld.so.conf || echo "%{x11shlibdir}" >> /etc/ld.so.conf
/sbin/ldconfig

%postun -n %{xflib}
if [ "$1" = "0" ]; then
    rm -f /etc/ld.so.conf.new
    grep -v "^%{x11shlibdir}$" /etc/ld.so.conf > /etc/ld.so.conf.new
    mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi
/sbin/ldconfig

%verifyscript -n %{xflib}
echo -n "Looking for %{x11shlibdir} in /etc/ld.so.conf... "
if ! grep -q "^%{x11shlibdir}$" /etc/ld.so.conf; then
    echo "missing"
    echo "%{x11shlibdir} missing from /etc/ld.so.conf" >&2
else
    echo "found"
fi

%triggerpostun -n %{xflib} -- XFree86-libs
grep -q "^%{x11shlibdir}$" /etc/ld.so.conf || echo "%{x11shlibdir}" >> /etc/ld.so.conf
/sbin/ldconfig

%triggerpostun -n %{xflib} -- libxfree86
grep -q "^%{x11shlibdir}$" /etc/ld.so.conf || echo "%{x11shlibdir}" >> /etc/ld.so.conf
/sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{xflib}
%defattr(-,root,root,-)
%{x11shlibdir}/*.so.*
#%{x11shlibdir}/libXfont*.so.*
#%{x11shlibdir}/modules/dri/*.so
%dir /usr/X11R6/lib/X11/locale/%{_lib}
%dir /usr/X11R6/lib/X11/locale/%{_lib}/common
/usr/X11R6/lib/X11/locale/%{_lib}/common/*

%files -n %{xfdev} -f static-only.list
%defattr(-,root,root,-)
# XXX /usr/X11R6/include/X11/bitmaps is already in XFree86
#/usr/X11R6/include/X11/
/usr/X11R6/include/X11/extensions
/usr/X11R6/include/X11/fonts
/usr/X11R6/include/X11/ICE
/usr/X11R6/include/X11/PM
/usr/X11R6/include/X11/SM
/usr/X11R6/include/X11/Xaw
/usr/X11R6/include/X11/Xmu
/usr/X11R6/include/X11/Xcursor
/usr/X11R6/include/X11/Xft
/usr/X11R6/include/X11/XprintAppUtil
/usr/X11R6/include/X11/XprintUtil
/usr/X11R6/include/X11/*.h
/usr/X11R6/include/GL
/usr/X11R6/include/DPS
/usr/X11R6/include/*.h
/usr/include/X11
/usr/include/GL
/usr/X11R6/man/man3/*

/usr/X11R6/lib/X11/config
/usr/X11R6/bin/imake
%multiarch %{multiarch_x11bindir}/imake
/usr/X11R6/bin/makedepend
/usr/X11R6/bin/gccmakedep
/usr/X11R6/bin/xft-config
%multiarch %{multiarch_x11bindir}/xft-config
/usr/X11R6/bin/xmkmf

/usr/X11R6/man/man1/imake.1x*
/usr/X11R6/man/man1/makedepend.1x*
/usr/X11R6/man/man1/xmkmf.1x*

%{x11shlibdir}/*.so

%{_libdir}/pkgconfig/xcursor.pc
%{_libdir}/pkgconfig/xft.pc
%{_libdir}/pkgconfig/xrender.pc
%{_libdir}/pkgconfig/xcomposite.pc
%{_libdir}/pkgconfig/xdamage.pc
%{_libdir}/pkgconfig/xfixes.pc
%{_libdir}/pkgconfig/xevie.pc

%files -n %{xfsta} -f static.list
%defattr(-,root,root,-)


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Mon Aug 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.8.2-3avx
- remove xorg-x11-{100dpi,75dpi,cyrillic}-fonts
- remove xorg-x11-Xdmx
- remove xorg-x11-Xnest
- remove xorg-x11-Xprt
- remove xorg-x11-Xvfb
- remove xorg-x11-doc
- remove xorg-x11-server
- remove xorg-x11-xauth
- remove xorg-x11-xfs
- remove X11R6-contrib
- remove xorg-x11 (the only thing that needed it was groff for rman
  but I fixed that puppy)
- drop a whole bunch of useless drivers, patches, sourcefiles, etc.
  that we don't need since we're not using xorg as a server, but rather
  only shipping the libs and devel files for other packages to build from

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.8.2-2avx
- remove /usr/X11R6/lib/X11/Cards (hwdata provides this)

* Thu Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.8.2-1avx
- drop XFree86 and use xorg.org instead
- don't build the Glide module
- drop the build debug stuff
- don't build the vnc module
- get rid of menus and icons
- drop TLS support
- get rid of support for CVS builds
- don't build new wacom driver

* Tue Aug 02 2005 Frederic Crozat <fcrozat@mandriva.com> 6.8.2-16mdk
- Remove workaround for libvgahw.a, fixed with gcc 4.0.1-1mdk
- Remove patch50, no longer needed with latest freetype (Mdk bug #16951)
- Patch 568 (CVS): Add support for freetype embolding, fix mono clipping

* Tue Jul 12 2005 Frederic Crozat <fcrozat@mandriva.com> 6.8.2-15mdk
- Patch567 (CVS): update from Xft 2.1.7 : fix crash (Mdk bug #16614), don't
  complain when Render is missing and optimize one critical glyph extents case

* Fri Jul  8 2005 Frederic Lepied <flepied@mandriva.com> 6.8.2-14mdk
- updated wacom driver to 0.6.8
- i945 support from HEAD
- added evdev input driver from HEAD

* Wed Jul  6 2005 Stew Benedict <sbenedict@mandriva.com> 6.8.2-13mdk
- really build libvgahw.a with no optimization

* Tue Jun 14 2005 Danny Tholen <obiwan@mailmij.org> 6.8.2-12mdk
- add the rest of http://gate.crashing.org/~benh/xorg patches

* Tue May 31 2005 Stew Benedict <sbenedict@mandriva.com> 6.8.2-11mdk
- build libvgahw.a with no optimization (#16183)
- redo radeon-ppc patches using http://gate.crashing.org/~benh/xorg

* Fri May 27 2005 Stefan van der Eijk <stefan@eijk.nu> 6.8.2-10mdk
- don't build new wacom driver on alpha & sparc
- add patch 5000 https://bugs.freedesktop.org/show_bug.cgi?id=2073
- add BuildRequires: jpeg-devel for %%if %%{build_vnc_module}

* Wed May 25 2005 Stew Benedict <sbenedict@mandriva.com> 6.8.2-9mdk
- build vnc module without requiring xmkmf (thx Christiaan)
- bugzilla #16066 (Xnest, P5004 - heads up from Nick Brown)

* Mon May 23 2005 Stew Benedict <sbenedict@mandriva.com> 6.8.2-8mdk
- vnc module (P566), adapted from xf4vnc.sf.net, xf4vnc-doc.html
- more gcc-4.0 fixes (P9328)

* Wed Apr  6 2005 Pablo Saratxaga <pablo@mandrakesoft.com> 6.8.2-7mdk
- updated canadian keyboard to follow official standard
- fixed use of pt_BR.UTF-8 Compose file (#14721)

* Wed Mar 23 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.8.2-6mdk
- add i810 (i915) & vmware drivers to x86_64
- fix dead_acute+x -> cedilla (#14721, pablo)
- standard moroccan tifinagh keyboard (pablo)

* Tue Mar 22 2005 Frederic Lepied <flepied@mandrakesoft.com> 6.8.2-5mdk
- fixed Brazilian ccedilla in pt_BR.UTF8 (Helio Chissini, bug #14721)
- fixed pam file for xdm (bug #14713)

* Mon Mar 14 2005 Frederic Lepied <flepied@mandrakesoft.com> 6.8.2-4mdk
- enable artificial bold style to CJK glyphs (bug #14469)
- build new via driver (r30, 0.13.3)
- fix radeon driver (xorg bug #2698)

* Tue Mar  8 2005 Frederic Lepied <flepied@mandrakesoft.com> 6.8.2-3mdk
- Compose: fixes tg keyboard use (bug #13544) (Pablo)
- XKB: fixes to lt,pt,hr,nl,mt kbd (Pablo)
- XKB: added sin (sinhala) keyboard (Pablo)
- updated linuxwacom to 0.6.6

* Tue Mar  8 2005 Frederic Lepied <flepied@mandrakesoft.com> 6.8.2-2mdk
- do not change permission if not requested (patch565, bug #13971)
- fix for the void input driver (xorg bug #2467)
- fix for the NVidia driver (xorg bug #2533)
- merged new ids (NVidia cards) (xorg bug #2380)
- fixed render bug in radeon driver (xorg bug #2164)

* Mon Mar  7 2005 Frederic Lepied <flepied@mandrakesoft.com> 6.8.2-1mdk
- obsoletes fonts-ttf-vera
- added fixes for radeon (rh)
- final tar ball (Michael)

* Fri Feb 25 2005 Pablo Saratxaga <pablo@mandrakesoft.com> 6.8.2-0.7mdk
- enabled luit
- some keyboard improvements (enable user-chosen toggle sequence for 
  Laotian keyboard) 
- improved default Compose file (added polytonic greek dead key sequences)
- make "zh_CN.GB2312" work as an alias of "zh_CN.gb2312"
- improved XLC_LOCALE for default UTF-8 so that better fonts are used,
  if present (there were ugly problems with cyrillic and greek)

* Wed Feb 23 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.8.2-0.6mdk
- remove obsolete (and unwanted) x86_64 glx patch
- better multiarch support, temporarily make imake multiarch dispatched

* Sun Feb 06 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.8.2-0.5mdk
- 6.8.2rc4
- respun patch203

* Mon Jan 31 2005 Frederic Lepied <flepied@mandrakesoft.com> 6.8.2-0.4mdk
- make a xauth subpackage to be used with ssh without installing the whole xorg-x11 package.
- multiarch
- fixed some rpmlint reports

* Fri Jan 14 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.8.2-0.3mdk
- 6.8.2rc2
- fix some rpmlint warnings on source rpm

* Sun Jan  9 2005 Stew Benedict <sbenedict@mandrakesoft.com> 6.8.2-0.2mdk
- mk712 and calibration support (touchscreen, P562, 563)
- nvxbox support (P564)

* Wed Dec 22 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.8.2-0.1mdk
- 6.8.2rc1
- Patch40020: fix Xvfb backingstore problem
- Patch40021: quick fix for segfault on ppc due to missing ddc info
- specfile cleanup
- disable TLS patch for now

* Wed Dec 08 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.8.1-6mdk
- add some patches selected for 6.8.2
- drop Danny's radeon patch for ppc
- add Benjamin Herrenschmidt's radeon patch for ppc

* Mon Dec 06 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.8.1-5mdk
- Patch803: fix fonts build (upstream bug #1560)

* Fri Dec 03 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.8.1-4mdk
- revert to vanilla 6.8.1

* Wed Dec 01 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.8.1-3mdk
- patch40018: install xorgversion.def

* Wed Dec 01 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.8.1-2mdk
- restore some source files from 6.7.0-2mdk

* Tue Nov 30 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.8.1-1mdk
- from Svetoslav Slavtchev <svetljo@gmx.de>
  - 6.8.1
  - add savage DRI and Dual Display tweaks
  - fix build on amd64
  - old keyboard driver still doesn't build :( ?
    switch to new "kbd" driver in server post skriplet
  - add and enable TLS build
  - try enabling composite
  - disable Xprt
  - drop two manpages with missing binaries
    dumpkeymap and XDarwin
  - enable the shipped voodoo driver
  - use the shipped sis via drivers
  - enable dri modules for mach64, savage, via
  - fix via_dri build
- build mach64 dri on ppc as well

* Mon Oct 18 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.7.0-4mdk
- fix pkgconfig files for lib64 arches

* Thu Sep 23 2004 Frederic Lepied <flepied@mandrakesoft.com> 6.7.0-3mdk
- fixes Print key (bug #, freedesktop #1238) (patch205)
- fixes for keyboards (Pablo)
- lookup wacom USB device name dynamically in case of failure to open the
  configured device. (patch40013)

* Mon Sep 13 2004 Frederic Lepied <flepied@mandrakesoft.com> 6.7.0-2mdk
- apply patch for XVideo (bug #10538)
- adapted i18n/kbd patches to new sources (Pablo)
- various new keyboards (Pablo)
- removed old mdk pcf fonts (Pablo)
- improved compose sequences (Pablo)
- added some new locales (Pablo)

* Sat Sep 11 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-1mdk
- fix build on amd64 (and maybe ppc64 ?)
- bump release to 1mdk now that the next version is already out

* Tue Aug 17 2004 Frederic Crozat<fcrozat@mandrakesoft.com> 6.7.0-0.2.12mdk
- add source212 (Fedora): Wonderland mouse cursor by default

* Fri Jul 30 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 6.7.0-0.2.11mdk
- Ensure fontconfig cache is always rebuild, otherwise strange things
  can happen when doing upgrade

* Tue Jul 27 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.2.10mdk
- sparc fixes from redhat

* Fri Jul 09 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 6.7.0-0.2.9mdk
- Don't use separate Xft/Xrender, they have been merged upstream
- Don't build freetype2, use system one (fix Mdk bug #9652)

* Wed Jun 30 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.7.0-0.2.8mdk
- fix wacom build (tried to build libwacomcfg even when disabled)

* Wed Jun 16 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.2.7mdk
- wacom-0.6.3

* Wed Jun 16 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.2.6mdk
- fix lib obsolates on amd64

* Wed Jun 16 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.2.5mdk
- fix unpackaged files on amd64
- via unichrome r20
- via unichrome XvMC 0.9.3
- sis 20040616

* Tue Jun 15 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.2.4mdk
- drop more club stuff
- make it build on alpha & compile on amd64
- xfs restart fix
- obsolate XFree86-doc

* Mon Jun 07 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.2.3mdk
- try to please rpmlint (patch permissions)

* Mon Jun 07 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.2.2mdk
- fix changelog

* Mon Jun 07 2004 Frederic Lepied <flepied@mandrakesoft.com> 6.7.0-0.2.1mdk
- drop club obsolates/provides
- s/Conflict/Obsolate/ XFree86
 
* Mon Jun 07 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.2.0mdk
- s/Mandrake Linux/Mandrakelinux in version string
  if mdkversion > mdk-10.0
- disable parallel build (it's broken)
- bzip2 some missed patches

* Mon Jun 07 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.1.7mdk
- build freetype2 with -fPIC on x86_64
- add another xkb map for Cherry CyMotion Master XPress
- support reserver extended syntax in Xservers
  to avoid timeout in xdm (patch110 from XFree86-4.3-28mdk)
- sis 040604-1
- via unichrome r1 r19

* Wed Jun 01 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.1.6mdk
- update freetypelib only for cooker/10.1 and up

* Mon May 24 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.1.5mdk
- update locale to mdk XFree-4.3-32mdk

* Mon May 24 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.1.4mdk
- fixup xrender pkgconfig file
- update sis driver to 220504-1

* Mon May 24 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.1.3mdk
- update libfreetype-xtt2 to 1.2a
- update libXrender to 0.8.4
- update render to 0.8
- update libXft to 2.1.6
- fixup Xorg update (ld.so.conf )
- unichrome-r18
- libviaXvMC-0.9.2


* Wed May 19 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.1.2mdk
- try to make urpmi happy
  ( 
   do not only obsolate Xorg-x11,
   but also provide it:
   urpmi tries to install instead of update
  )

* Wed May 19 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.1.1mdk
- add more suse fixes (ppc64 & x86_64)
- update sis driver to 040504-1
- drop synaptics source (they were never build)

* Wed May 19 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.1.0mdk
- rename to xorg-x11 (all other distros use this name)
- obsolate the old/club version

* Fri Apr 30 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.0.10mdk
- fix the fix for xkb rules

* Fri Apr 30 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.0.9mdk
- more changes in order to be able to revert to XFree86

* Fri Apr 30 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.0.8mdk
- may be fix "uninstall"
     conflicts XFree86 < 5.0.0
     add virtual provide X11
  
* Thu Apr 29 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.0.8mdk
- update to latest sis driver
- add synaptics-0.13.0 
  but disable it for now
  will probably add a separate package

* Wed Apr 28 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.0.7mdk
- add a fix for mozilla & flash
- add via unichrome XvMC library
- add more XFree86 compatibility links

* Tue Apr 27 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.0.6mdk
- fix postun XFree-server
- add two more xkb compatibility links
- update via to unichrome-X-r16

* Wed Apr 21 2004 Svetoslav Slavtchev <svetljo@gmx.de> 6.7.0-0.0.5mdk
- add vodoo drivers (Fedora)
- prot-exec fixes (Fedora)
- multi-user support
- update use_matrox_hal to mgadrivers-3.0src
- fix deps & provides (maybe)
- rename to Xorg-x11 ( still don't like it, but .. )
- add --with nosrc

* Sun Apr 18 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.7.0-0.0.4mdk
- made replacement of /etc/X11/X symlink unconditional
  no need to keep XFree86 3.x selected when installing the xorg-server package

* Mon Apr 12 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.7.0-0.0.3mdk
- fixed missing whitespace in xorg-server %post script addition for xorg.conf

* Sun Apr 11 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.7.0-0.0.2mdk
- symlink /etc/X11/xorg.conf to XF86Config-4 in %post
- added %postun_trigger scripts for ld.so.conf, xfs service, and fonts

* Sun Apr 11 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.7.0-0.0.1mdk
- X11R6.7.0

* Mon Jan 19 2004 Frederic Lepied <flepied@mandrakesoft.com> 4.4-0.902.1mdk
- startx fix [bug #6659] (Olivier Blin)
- changed numbering
- fix build on ppc and sparc (Christiaan Welvaart)
- DIRM: %{x11shlibdir}/modules %{x11shlibdir}/modules/*
- updates from cvs 20040120-0736

* Fri Dec 19 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3.99.902-1mdk
- 4.4 rc2
- fixed startx

* Mon Dec 15 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3.99.901-1mdk
- first pre 4.4

* Tue Oct  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3-24mdk
- Requires: /lib/cpp instead of gcc-cpp
- locale DSOs are arch-dependent, move them to lib{,86}xfree86

* Wed Sep 10 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 4.3-23mdk
- Update patch 6 with FULL xft code (fix mdk bug 4580)

* Mon Sep 08 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 4.3-22mdk
- Update patch 7 with CVS code to fix XRender on xinerama (Mdk bug #5290)
- Patch802: fix Multiple Unspecified Integer Overflow Vulnerabilities (bugtrag 8514) 

* Thu Sep 04 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-21mdk
- Update source208 (via driver) with memory size detection fix.

* Tue Sep 02 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 4.3-20mdk
- Update source208 with latest CVS snapshot and with working TV output..
- Remove Buildrequires on freetype 1.3

* Wed Aug 20 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 4.3-19mdk
- Add source208 : VIA CLE266 driver (not fully stable yet, CRT works, 
  TV ouput doesn't work for me) 
- Remove explicit freetype 1.3 dependency (fix bug #4213)

* Mon Aug 11 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3-18mdk
- Update/fix Patch210 (build-libs-with-pic) to include xkbui
- Merge from amd64-branch:
  - Build more drivers for x86-64
  - Patch532: Chips CT69000: disable hardware accelaration for now (RH #74841)
  - Patch533: Chips CT65550: force software cursor for now (RH #82438)

* Tue Aug  5 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3-17mdk
- Provides: XFree86-static-libs, XFree86-static-devel
- Update Patch210 (build-libs-with-pic) to include libxkbfile

* Mon Aug 04 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 4.3-16mdk
- fixed/improved several keyboards (ua, ben, uz, mng, us_intl)
- added recognition of various new locales
- extended and fixed UTF-8 default Compose file (now it allows to type
  all vietnamese and pinyin double accented letters)

* Sun Aug  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3-15mdk
- Patch216: Fix build on linux LP64 platforms

* Fri Jul 25 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-14mdk
- fixed some distlint DIRM
- added patch to make the pages executable on all arch (Gwenole)
- libified

* Tue Jul  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-13mdk
- applied patch from HEAD to fix deadlock with threads and Xi
- Patch6: update to Xft 2.1.2
- Patch7: update to Xrender 0.8.3
- Remove patches 3 & 4 (obsoleted by patches 6 & 7)

* Tue Jul  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-12mdk
- updated to 4.3 branch

* Wed Jul  2 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-11mdk
- put back xedit lisp files in X11R6-contrib (bug #3831)

* Mon Jun 16 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-10mdk
- apply sparc patch from Olivier Thauvin
- rebuild without -g

* Thu Jun  5 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-9mdk
- correct XF86Config-4 on upgrade (Pixel)
- fixed host.def

* Thu May 15 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-8mdk
- rebuild for auto-provides
- fixed spec file to allow to build with HAL (bug #3289) (svetljo)
- Fixed build with Matrox %%havematroxhal enabled and typo
  on --with matroxhal option (Giuseppe)
- Added patch (544) to avoid XFree86 lockup on server exit (bug #1307) (Giuseppe)
- Applied patch () to fix an Xft problem in mozilla

* Wed Apr 30 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-7mdk
- Applied blank patch (561) to avoid lockup on screen blank on i830

* Thu Apr 10 2003 Nicolas Planel <nplanel@mandrakesoft.com> 4.3-6mdk
- Applied vt-fix patch (560), fix server lockup when switiching to console
  on intel chipset.

* Tue Mar 11 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-5mdk
- update for zh_CN.GB18030 (Pablo)
- dblquote => quotebdl (bug #3192) (Pablo)
- fixed some broken compose for us, us_intl, de(nodeadkeys),
 dvorak(no) and dvorak(se). (Pablo)

* Mon Mar 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-4mdk
- applied patches for radeon from Hui Yu

* Mon Mar 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-3mdk
- applied fix to Xft from Keith Packard
- added back afm files (bug #2784)
- applied fix to nv driver from Mark Vojkovich
- launch fc-cache without parameter in XFree86 package

* Fri Mar  7 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-2mdk
- update locales (Pablo)
- applied patch for radeon R300

* Thu Feb 27 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-1mdk
- updated snapshot
- fixed %%BuildDebugVersion flag to let debug version compiling flawlessly. (Giuseppe)

* Mon Feb 24 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-0.20030224.1mdk
- updated snapshot
- added savage 1.27t (bug #1385)

* Mon Feb 17 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-0.20030218.1mdk
- added patch212 for PS/2 mouse and USB keyboard problem (bug #1347)
- updated snapshot to 4.3 rc2
- updated patch204

* Mon Feb 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-0.20030210.1mdk
- updated snapshot

* Wed Feb  5 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-0.20030204.2mdk
- patches for i8xx family

* Tue Feb  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.3-0.20030204.1mdk
- updated snapshot

* Fri Jan 31 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 4.2.99.5-0.20030127.2mdk
- reverted back latin keyboards to old layouts (as the 4 elements per group of
  the new layouts give problems in some cases)
- corrected errors making Turkish and Azeri keyboards to fail loading.
- changed default locale encodings to match what is defined in locales-*
  packages.

* Mon Jan 27 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2.99.5-0.20030127.1mdk
- applied patch from bug #728
- updated snapshot
- default cursors back (bug #795)

* Wed Jan 22 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2.99.5-0.20030122.2mdk
- 4.2.99.5 snapshot

* Wed Jan 15 2003 Pablo Saratxaga <pablod@mandrakesoft.com> 4.2.99.4-0.20030110.2mdk
- adapted the i18n and fixkbd patches
- removed some i18n and kbd patches no more needed
- replaced the new automatically-generated en_US.UTF-8 Compose file, with
  the old one, more human-friendly
- xfs path from Frederic Crozat

* Fri Jan 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2.99.4-0.20030110.1mdk
- 4.2.99.4 snapshot
 * Thu Jan  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.99.3-1.20021223.5mdk
- Temptatively enable it to build on 9.0 since FredC hasn't done so
- Remove bunch of x86-64 patches already present since 4.2.99.2,
  though build static libXau, libxf86config with PIC is still required
- Let's build libraries which only come in static form with PIC so
  that KDE can be prelink'able

* Mon Jan  6 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 4.2.99.3-1.20021223.4mdk
- Add missing files for Xft
- Remove patches 534, 535 & 536, source 208 (merged upstream)

* Tue Dec 31 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.99.3-1.20021223.3mdk
- obsoletes/provides libXft2(-devel)
- add pkgconfig files in -devel

* Tue Dec 31 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.99.3-1.20021223.2mdk
- use whiteglass cursor theme by default
- added BuildRequires libpng-devel (Stefan)
- don't list ioport in file list on ppc (Stew)

* Fri Dec 27 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.99.3-1.20021223.1mdk
- parallel make is back
- patch201: make blue the default background of the root window

* Mon Dec 23 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.99.3-0.20022312.1mdk
- 4.3 branch

* Wed Dec  4 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 4.2.1-14mdk
- Regenerate patch536 again to fix the DataInt32 unresolved symbol

* Tue Dec  3 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 4.2.1-13mdk
- Update patch536 : updating Xrender to fcpackage version wasn't such 
  a good idea.. Reverting to XF 4.2.1 version but keep 
  XRenderCompositeString16/XRenderCompositeString32 length computation fix

* Mon Dec  2 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 4.2.1-12mdk
- Patch 536: update XRender to fcpackage 2.1 version (and fix 
  XRenderCompositeString16/XRenderCompositeString32 length computation BTW)
- Untitification

* Tue Nov 12 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 4.2.1-11mdk
- Really fix bootstrapping this time
- Disable _unpackaged_files_terminate_build macro for this package

* Thu Nov  7 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 4.2.1-10mdk
- Patch535: allow bootstrapping when building Xft1

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.2.1-9mdk
- XFree86-xfs : add prereq on rpm-helper chkfontpath 
- require s/sh-utils/coreutils/

* Wed Nov  6 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 4.2.1-8mdk
- Add PreReq to fontconfig

* Tue Nov  5 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 4.2.1-7mdk
- Source208: use Xft1 from fcpackage 2.0 (fontconfig support)
- Don't use patch2 if build with fontconfig

* Mon Nov  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.1-6mdk
- Build more drivers for x86-64
- Patch217: Build with -fno-strict-aliasing with any gcc >= 3.1 to
  avoid XFree86 source bugs. Aka let's have 3D acceleration there with
  an ATI Radeon 7500 (Egbert Eich, 4.3-branch)
- Patch106: Fix matrices text-look in man pages (Thierry Vignaud)

* Tue Oct 22 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.1-5mdk
- updated savage driver to 1.1.25t

* Tue Oct  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.1-4mdk
- Clean up specfile so that it is more lib64 aware
- Patch533: Fix build of ati-radeon driver if DRI is not enabled
- Patch534: Fix i810 crash when switching VT (CVS)
- Merge x86-64 support with SuSE releases (Egbert Eich, 4.2.99.2-branch):
  - Make X modules go in the right directories (lib64 support)
  - Add x86-64 specific configuration bits
  - Add configury so that some static libraries could be built with
    PIC, that includes those that are to be linked into shared objects
  - Build the following libraries with PIC (needs Patch212):
    libXinerama, libXv, libXxf86dga, libXxf86misc, libXxf86vm,
    libxf86config, libXau
  - Add x86-64 support and updates to int10 code from CVS
  - Don't use VarArgs in functions that don't need them actually

* Fri Sep 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.1-3mdk
- fixed bootstrap
- corrected build
- keyboard fixes (Pablo)

* Thu Sep 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.1-2mdk
- fixed XFree86 -configure
- fixed kill message in startx (bug #234)
- fixes for matrox G450 and G550

* Sat Sep  7 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.1-1mdk
- updated patch204
- removed patch1, patch523 (merged upstream)
- updated to 4.2.1 (security fix)
- updated gatos

* Tue Sep  3 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-26mdk
- updated to last 4.2 branch

* Mon Sep 02 2002 Giuseppe Ghib�<ghibo@mandrakesoft.com> 4.2.0-26mdk
- updated entry for Matrox HAL module (but disabled).
- Get BuildDebugVersion flag compiling.
- Fixed permission of trident_41_drv.o and ati_old_drv.o modules.

* Fri Aug 30 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-25mdk
- don't build freetype2

* Thu Aug 29 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 4.2.0-24mdk
- improved XftConfig file and added fontpath for a default opentype dir
- included a modified opentype font providing all cyrillic and latin letters
  used by supported languages, to have a last ressort fallback for Xft

* Wed Aug 21 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 4.2.0-23mdk
- updated xfs.config and XftConfig with new fontpaths;
- various new aliases for XftConfig,
- improved UTF-8 Compose file for latin languages, corrected various typos and
  added arabic digraphs support
- locale.alias: fixed "vi", "ta"; added "mn"; separate CJK UTF-8 locales to put
  for each language the legacy encoding first.
- Compose/XLC_LOCALE: added tscii-0 and CJK UTF-8
- added missing (lost) keyboards; and "lao" and "mng" and "tscii"

* Tue Aug 20 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-22mdk
- handle sigterm in startx and xinit
- change the init sequence of xfs on upgrade

* Wed Aug 14 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-21mdk
- try to find a free vt starting at vt 7

* Tue Aug 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-20mdk
- sis630 dropin from http://www.webit.at/~twinny/linuxsis630.shtml

* Mon Aug 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-19mdk
- updated savage driver to 1.1.23t

* Mon Aug 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-18mdk
- wacom driver update from Ping Cheng
- PrintScreen key support
- xdm realloc bug fix
- i845 and trident update from cvs
- i810 fixes

* Wed Jul 24 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 4.2.0-17mdk
- removed no more needed hacks in fontsets and netscape support
- corrected some locale aliases and ro,tr,az keyboards
- applied patch to enable use of ximswitch

* Tue Jun 18 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-16mdk
- really fix xfs mess

* Sun Jun 16 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-15mdk
- corrected xfs mess

* Fri Jun 14 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-14mdk
- fixed xman
- corrected hyperpen module loading
- updated decription

* Mon Jun 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-13mdk
- added hp keyboards (Nicolas Planel)
- updated Patch524 (v4l) from main branch for Thierry

* Wed May 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-12mdk
- updated i810 from cvs (Nicolas Planel)
- start xfs earlier in the boot sequence

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.0-11mdk
- Automated rebuild in gcc3.1 environment

* Fri Mar  8 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-10mdk
- added drakfont/{ttf,type1} to XftConfig (Danny Tholen)

* Fri Mar  8 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-9mdk
- compose/locale modifications (Pablo)
- install ro2 keyboard (Pablo)
- wacom alpha26
- mem leak fix in libXft (Lars Knoll)
- provide trident_41 and ati_old drivers

* Fri Mar  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-8mdk
- ref count module loading in IM (rh)
- xfs reports log de LOG_DAEMON and change dir to / (rh)

* Mon Feb 25 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-7mdk
- kbd patch redone (Pablo)
- mach64 fixes
- acecad driver update from Edouard Tisserant.
- add missing resources for X11R6-contrib (Goetz Waschk)
- launch xvt as default instead of xterm in xinit
- patch to allow xv for DVB (Marcus Metzler)

* Tue Feb 19 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-6mdk
- fix entry for ca_enhanced
- by popular demand, use ati.2 drivers.
- use built mkfondir instead of the system one to allow rebuild from scratch.

* Mon Feb 18 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 4.2.0-5mdk
- added recognition of "zh_HK" for LI18NUX2000 compliance

* Fri Feb 15 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 4.2.0-4mdk
- fixed fontpath, keyboards and some i18n glitches

* Wed Feb  6 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-3mdk
- requires explicitely libglide3.so.3 in XFree86-glide-module as the lib
is now dynamically loaded.
- fix the name of glide lib to load for 3D acceleration for tdfx driver.
- added nv to the list of drivers for ppc (David)
- corrected hostname call in startx (Thierry)
- i810 fix for DRI (Sottek, Matthew J)

* Tue Jan 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-2mdk
- load agpgart before loading drm module
- corrected the description of the XFre86 package (gc)
- updated to 4.2 branch of cvs.

* Mon Jan 21 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.0-1mdk
- 4.2
- updated I18n support (Pablo)
- corrected startx
- corrected X11R6-contrib menu file
- put back the --no-merge-constant check

* Tue Jan 15 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.1.99.6-2mdk
- remove icons dir from files list
- corrected duplicates between devel and static-libs
- corrected conflict with xpm-devel
- build X11R6-contrib from this source (need to be finalized)

* Tue Jan 15 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.1.99.6-1mdk
- 4.1.99.6

* Thu Oct  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-19mdk
- updated trident driver from CVS (p519).
- updated SIS driver from CVS (p518).

* Fri Sep 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-18mdk
- really upgrade savage driver to 1.1.19 (#5501)
- IA64 patches (Gwenole)
- updated XftConfig (Andrej Borsenkow)

* Fri Sep 21 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-17mdk
- xkb and Compose fixes (Pablo).

* Wed Sep 19 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-16mdk
- load agpgart kernel module before trying to access /dev/agpgart
- updated xkill icons (David).
- removed patch602 for ia64 merged upstream (Gwenole).
- updated locales.alias and locales.dir (Pablo).
- cyrillic-fonts: add :unscaled to ukr font path (Pablo).
- fs/config: append :unscaled to mdk and misc dirs (Pablo).

* Thu Sep 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-15mdk
- updated patch506 to allow startx Gnome (req Borsenkow Andrej)
- fixed XftConfig to use aa even on small fonts.

* Tue Sep 11 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-14mdk
- Matrox G550 support from Randall Watt <rwatt@matrox.com>.
- disabled patch155 for radeon.

* Sun Sep  9 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-13mdk
- radeon updates from cvs (need feedback from r128 and radeon users)
- really use last wacom driver

* Mon Sep  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-12mdk
- finished rh merge

* Mon Sep  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-11mdk
- merged rh patches
- updated to the last cvs branch xf-4_1
- savage driver update (1.1.19)

* Wed Aug 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-10mdk
- updated xfs startup script
- updated to the last cvs branch xf-4_1 to benefit from the fix of xfs
to be able to work with xf 3 (fix from Paulo C�ar Pereira de Andrade of Conectiva).

* Mon Aug 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-9mdk
- try to load agpgart when needed (patch513).
- updated to the last cvs branch xf-4_1
- savage driver update (1.1.18)
- s3 drivers update (0.3.21)
- Compose for en_US.UTF-8 (Pablo)
- updated patch205 (Pablo)
- wacom driver alpha 25

* Tue Aug  7 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-8mdk
- added BuildRequires bison (Nic Roets).
- added missing provides.
- added session support for twm (fcrozat)
- Xinerama fix (patch512).

* Fri Jul 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-7mdk
- added BuildRequires: Glide_V3-DRI-devel >= cvs-2mdk
- added libXss.a to -devel

* Mon Jul 16 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 4.1.0-6mdk
- added recognition of GKB/BIG5HKSCS encodings
- some more xkb keyboards (al, ar, la, pl2)
- font packages logic is redone (no more charset specific font packages,
  as now unicode fonts are the preferred font encoding)

* Wed Jul 11 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 4.1.0-5mdk
- Patch511: Fix sis_alloc.c build

* Wed Jun 13 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 4.1.0-4mdk
- adapted the i18n patch
- fixed Romanian keyboard
- added UTF-8 Compose file
- added XftCache file for Type1 directory
- added alias for Thai fonts

* Tue Jun 12 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-3mdk
- added after release patch from cvs branch 4.1

* Mon Jun 11 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-2mdk
- XftConfig: don't antialias fonts with size between 8 and 14 or in
the webdings/wingding families (Laurent Culioli).
- Fix build on PPC (Dadou)
- patched the wacom driver to work with the way the kernel 2.4.5 usb driver
reports usb events.

* Sun Jun  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.1.0-1mdk
- 4.1.0

* Sat Jun  2 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.99.902-1mdk
- 4.0.99.902

* Thu May 31 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.99.901-2mdk
- added optimization for alpha in config file (Jeff).

* Wed May 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.99.901-1mdk
- restored startx like in 8.0
- removed PEX and XIE extensions
- 4.0.99.901

* Mon May 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.99.900-4mdk
- add Xft headers to devel package
- add preliminary s3 driver (Jrgen Zimmermann)
- rebuild libXfont.so.1 after rebuild of libtype1 (Jrgen Zimmermann)
- updated CVS snapshot

* Tue May 22 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.99.900-3mdk
- add ids for r128 ultra.
- use makedepend instead of gccmakedep to avoid breaking Mesa compilation.
- remove glu devel stuff (gc).
- compile libtype1 with -fno-fast-math to avoid a rendering bug (Arnd Bergmann).
- added patch to have the frameWidth resource behave correctly in xdm (Thierry Godefroy).
- removed patch 328 for alpha (Jeff).
- fixed error on %post
- build Xxf86dga and Xv libs as shared libs.

* Mon May 21 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.99.900-2mdk
- 3dfx is back
- updated CVS snapshot
- fixed fonts
- removed libGLU

* Sat May 12 2001 Arnd Bergmann <arnd@itreff.de> 4.0.99.900-1mdk
- upgrade to current CVS version
- add some files that were not included
- break 3dfx acceleration (sorry)
- build with integrated freetype2 (system lib did not work)
- run xftcache after install

* Fri May  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-9mdk
- recompile to have tdfx_dri.so dynamically linked.

* Sun Apr  8 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-8mdk
- fix for tdfx dga

* Sun Apr  8 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-7mdk
- xfs user creation/removal is back

* Sat Apr  7 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-6mdk
- corrected startx to allow to start another server
- hack to be able to use CJK languages with Netscape (pablo)
- patch to support trident cyberglade XP and XPm

* Thu Apr  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-5mdk
- user -deferplyphs 16 in startx command line (Andrew Lee)
- use gcc on ppc (Dadou)
- updated locale.dir (Pablo)
- use server macros for xfs
- don't compile kernel modules
- don't compile Glide2 support

* Mon Apr  2 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-4mdk
- don't activate sw_cursor on neomagic
- corrected and enabled patch600 for ppc (Stew)
- various i18n fixes (Pablo)

* Wed Mar 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-3mdk
- XftConfig now in /etc/X11 and a config file.
- don't run chkconfig -add xfs on upgrade
- stop xfs on remove
- merged with rh

* Mon Mar 26 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-2mdk
- use XftConfig from Arnd Bergmann.
- compile with normal gcc on ppc
- updated wacom driver.

* Mon Mar 19 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-1mdk
- 4.0.3

* Thu Mar 15 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.2-11mdk
- added patch to have working G450 dual head.

* Wed Mar 14 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.2-10mdk
- 4.0.2b

* Tue Mar 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.2-9mdk
- merge with rh patches
- savage driver 1.1.15 + fix
- added patch to avoid failure for parallel build

* Thu Mar  8 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.2-8mdk
- updated to current 4.0.2-branch
- applied patch to Xft to make it prefer familly over spacing (for Qt).
- remove lines referencing Compose files for CJK locales, that
causes problems with KDE. To keep until Qt/KDE is fixed (srtxg).
- xinit calls xvt instead of xterm.
- add patch for matrox.

* Fri Mar  2 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.2-7mdk
- 4.0.2a
- added xvinfo to file lists

* Mon Jan 22 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.2-6mdk
- removed taipeifonts.
- added XftConfig from keith's site (Michel Goraczko).
- removed Xlat9-10x20-lat9.pcf font from eurofonts.

* Thu Jan 18 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.0.2-5mdk
- initial merge of the taipeifonts into the main XF86 package.

* Tue Jan 09 2001 David BAUDENS <baudens@mandrakesoft.com> 4.0.2-4mdk
- Patches for PPC
- added patch to fix Sis startup.

* Sat Jan  6 2001 Giuseppe Ghib�<ghibo@mandrakesoft.com>  4.0.2-3mdk
- make freetype2 conditional in SPEC file (for Mandrake 7.2 backport).
- make HAL conditional in SPEC file (e.g. mgaHALlib.a).
- added glxinfo, xgamma, pcitweak, showfont, revpath and their
  man pages to %files.

* Fri Jan  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.2-2mdk
- don't compile with HAL (Stefan van der Eijk)
- include XftConfig (Giuseppe)
- correct syntax error in %%pre

* Wed Dec 20 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.2-1mdk
- 4.0.2

* Tue Dec 12 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1za-1mdk
- 4.0.1Za
- activate freetype2 support in the Render extension.
- don't compile glide support on other arch than ix86 (Jeff).

* Mon Dec 11 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1z-2mdk
- PPC: build with egcs (Dadou).
- moved gccmakedep to -devel package (Vince).
- added BuildRequires on pam-devel (Fred Crozat).

* Sat Dec  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1z-1mdk
- 4.0.1Z

* Wed Dec  6 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1h-2mdk
- fix xfs to be able to start as a user.

* Tue Dec  5 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1h-1mdk
- 4.0.1h

* Wed Nov 29 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1g-1mdk
- added BuildRequires flex and groff.
- 4.0.1g

* Wed Nov 22 2000 David BAUDENS <baudens@mandrakesoft.com> 4.0.1f-3mdk
- Remove patch for PPC (#600). Fix is now included by default in XFree86 4.0.1

* Tue Nov 21 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1f-2mdk
- added fix to xkbcomp/rules/xfree86.lst (Pablo).
- added libGlw and static libs that have no dynamic version to -devel
file list (thanks to J. A. Magallon).

* Sat Nov 18 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1f-1mdk
- 4.0.1f
- xkb files are back.

* Tue Nov 14 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 4.0.1-30mdk
- fixed Norwegian kbd bug (bugs #1295 and #908)
- fixed Korean TTF font support 

* Tue Nov 14 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-29mdk
- enabled back pam support (bug #1250).

* Wed Oct 18 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 4.0.1-28mdk
- some i18n improvements
- display of 16bit encoding still needs a hack in XLC_LOCALE files

* Wed Oct 18 2000 David BAUDENS <baudens@mandrakesoft.com> 4.0.1-27mdk
- Patch for PPC

* Mon Oct  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-26mdk
- added missing /var/lib/xdm dir.

* Mon Oct  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-25mdk
- corrected manipulation of ld.so.conf in libs %%post.

* Tue Oct 03 2000 Daouda Lo <daouda@mandrakesoft.com> 4.0.1-24mdk
- provide large icons and make others transparents

* Fri Sep 29 2000 Daouda Lo <daouda@mandrakesoft.com> 4.0.1-23mdk
- add icons to twm menu entry
- add icons to X small utilities like Xkill, Xrefresh ...
- more macrozifications

* Fri Sep 29 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-22mdk
- corrected static-libs package.
- added current CVS tree for neomagic.

* Wed Sep 27 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-21mdk
- put static only libs in the devel package.
- added a prereq on XFree86 = %%{version} for font packages to allow upgrade.
- corrected xfs startup script (thanks to Guillaume Rousse for pointing it).
- corrected startx to allow to launch multiple servers.

* Mon Sep 25 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-20mdk
- switched to pam_stack for xdm pam setup.
- added current CVS tree for GeForce2.

* Fri Sep 22 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-19mdk
- rewrite of xfs startup script (reload target).
- modified xinit and startx to allow runlevel changes from 3 to 5 to kill autologin.
- applied patches for sparc and alpha from redhat.
- updated xfs patch.

* Tue Sep 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.1-18mdk
- Fixe tdfx drm acceleration with the last framework of our kernels.

* Fri Sep 15 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-17mdk
- fixed VidMode extension to work with 3.3 servers.

* Tue Sep 12 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 4.0.1-16mdk
- fixed locales names and aliases

* Mon Sep 11 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 4.0.1-15mdk
- fixed problem with a duplicated mdk font
- added option deferplyphs 16 to xfs config (useful for CJK)
- added :unsaled to directories added by the chkfontpath (for non scalable
  fonts)

* Fri Sep  8 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-14mdk
- commented autologin patch
- cleanup of menu entries.
- compile support for Voodoo2.

* Thu Sep  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-13mdk
- noreplace
- launch mkfontdir in %%post of fonts package.

* Wed Sep 06 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 4.0.1-12mdk
- fixed XLC_LOCALE files for Chinese
- added full support for Greek typing
- added encoding files for xfsft font server

* Tue Sep  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.1-11mdk
- Learn to be safe, remove cvs updates.

* Wed Aug 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.1-10mdk
- Update to last drm from cvs..

* Mon Aug 28 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 4.0.1-9mdk
- merged back the i18n patches
- lots of new kbd layouts
- several new charset encodings

* Thu Aug 24 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-8mdk
- compiled with Glide_V3-DRI.

* Fri Aug 18 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-7mdk
- GLX headers are back.

* Mon Jul 31 2000 Fran�is Pons <fpons@mandrakesoft.com> 4.0.1-6mdk
- fixed %%pre script of XFree86.
- removed provide to Mesa-devel in XFree86-devel.

* Fri Jul 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-5mdk
- oops fixed bad %%post of XFree86

* Fri Jul 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-4mdk
- remove Obsoletes Mesa.
- removed Xpm from the packages.
- %%post modifications for ld.so.conf are back.
- cleanup %%post to work on fresh install.
- don't compile DRM on architectures other than ix86.
- moved app-defaults, rstart, lbxproxy and proxymngr to /etc/X11 in
  the filelist.

* Fri Jul 21 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-3mdk
- applied patch for autologin with xdm
- added logrotate of /var/log/xdm-error.log
- make symlink from /usr/X11R6/include/GL to /usr/include/GL

* Thu Jul  6 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-2mdk
- included missing headers.
- tdfx_drv.o is back.

* Mon Jul  3 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.1-1mdk
- 4.0.1

* Wed Apr  5 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-6mdk
- removed xterm stuff.
- enabled the elographics touchscreen driver.
- Fix missing -L/usr/X11R6/lib in generated Makefiles.
- Fixed empty man pages.

* Fri Mar 24 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-5mdk
- split the static libraries in their own package.

* Tue Mar 21 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-4mdk
- add back the static libraries.
- better menu support.
- compiled glide driver and put it in its own package.

* Fri Mar 17 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-3mdk
- fix bad .so symlinks in XFree86-devel.
- fixed conflicts with X11R6-contrib.
- added menu support.

* Tue Mar 14 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-2mdk
- corrected xfs startup.

* Mon Mar 13 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-1mdk
- 4.0
- config file is no longer called XF86Config.experimental. Use the
standard name XF86Config-4 instead.
- patch from Daryll Strauss for tdfx.

* Mon Mar  6 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.9.18-2mdk
- enabled i810.
- build all the packages.

* Wed Feb 23 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.9.18-1mdk
- 3.9.18.

* Mon Jan 24 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.9.17-1mdk

- first mandrake version.
- named config file XF86Config.experimental to avoid confusion with 3.3 releases.
