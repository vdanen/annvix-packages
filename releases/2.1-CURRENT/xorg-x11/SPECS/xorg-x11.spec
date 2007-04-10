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

Source0:	http://freedesktop.org/~xorg/X11R%{version}/src/single/X11R%{version}-src.tar.bz2
%if %{build_nosrc}
NoSource:	0
%endif
Source15:	xfs.init
Source16:	xfs.config
#Source18:	xdm.init
Source19:	twm.method
Source20:	system.twmrc
#Source21:	http://keithp.com/~keithp/fonts/XftConfig
# from Arnd Bergmann <std7652@et.FH-Osnabrueck.DE>
# only used when not build with fontconfig
Source21:	XftConfig

Source50:	http://freedesktop.org/~xlibs/release/render-%{renderver}.tar.bz2
Source51:	http://freedesktop.org/~xlibs/release/libXrender-%{xrenderver}.tar.bz2
Source52:	http://freedesktop.org/~xlibs/release/libXft-%{xftver}.tar.bz2

Source100:	Euro.xmod
Source102:	eurofonts-X11.tar.bz2
# extra *.enc files for xfs server not (yet) in XFree86 -- pablo
Source152:	xfsft-encodings.tar.bz2
# locale.dir, compose.dir, locale.alias files.
# maintaining them trough patches is a nightmare, as they change
# too much too often; it is easier to manage them separately -- pablo
Source153:	XFree86-compose.dir
Source154:	XFree86-locale.alias
Source155:	XFree86-locale.dir
#
Source156:	gemini-koi8-u.tar.bz2
# the new default unicode compose file is too human-unfriendly; keeping
# the old one...
Source157:	X_Compose-en_US.UTF-8

# I18n updates from Pablo
# Devanagari OpenType font, to install for the indic opentype patch -- pablo
Source160:	XFree86-extrascalablefonts-font.tar.bz2

# Wonderland mouse cursor (Fedora)
Source212:	wonderland-cursors.tar.bz2

Patch4:		X11R6.7.0-libfreetype-xtt2-1.2a.patch
Patch5:		Xorg-6.7.0-isolate_device.patch
#Patch5:	XFree86-4.3-PrefBusID-v3.patch.bz2

# Libs patches #################################################################

# X server patches #############################################################

Patch200:	XFree86-4.2.99.3-parallel-make.patch
Patch201:	XFree86-4.2.99.3-mandrakelinux-blue.patch
Patch202:	XFree86-4.3.99.901-xwrapper.patch

# Build the following libraries with PIC: libxf86config, libXau, libxkbfile
Patch210:	XFree86-4.3-build-libs-with-pic.patch

Patch213:	XFree86-4.3.0-gb18030.patch
Patch214:	XFree86-4.3.0-gb18030-enc.patch

Patch216:	XFree86-4.3-_LP64-fix.patch

# Drivers patches ##############################################################

# Patch for building in Debug mode
Patch700:	XFree86-4.2.99.3-acecad-debug.patch

# Xorg patches
# https://bugs.freedesktop.org/show_bug.cgi?id=2164
Patch5000:	xorg-x11-6.8.2-radeon-render.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=2380
Patch5001:	xorg-x11-6.8.2-nv-ids.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=2467
Patch5002:	xorg-x11-6.8.2-void-driver.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=2698
Patch5003:	xorg-x11-6.8.2-radeon-merge.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=2599
Patch5004:	xorg-x11-6.8.2-xnest-stacking.patch

# RH patches

Patch9325:	xorg-x11-6.8.2-gcc4-fix.patch
Patch9327:	xorg-x11-6.8.2-ati-radeon-gcc4-fix.patch
#(sb) partially from fedora commits
Patch9328:	xorg-x11-6.8.2-gcc40.patch

Patch9601:	XFree86-4.3.99.902-mozilla-flash.patch

Patch10012:	xorg-redhat-libGL-exec-shield-fixes.patch
Patch10015:	XFree86-4.3.0-redhat-nv-riva-videomem-autodetection-debugging.patch

Patch10101:	XFree86-4.3.0-makefile-fastbuild.patch


# my addons (svetljo)

# build freetype2 with fPIC on x86_64
Patch40002:	lib_freetype_module.patch  

# p5000 https://bugs.freedesktop.org/show_bug.cgi?id=2073
Patch50000:	xorg-x11-6.8.2-sunffb.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	zlib-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	groff
BuildRequires:	ncurses-devel
BuildRequires:	perl
BuildRequires:	libpng-devel
BuildRequires:	libexpat-devel
%if %{usefreetype2}
BuildRequires:	freetype2-devel
%endif
# We need fontconfig for the new Xft1
%if %{with_new_fontconfig_Xft}
BuildRequires:	fontconfig-devel >= 2.1-4mdk
%endif

Provides:	X11-ISO8859-2
Provides:	X11-ISO8859-9
Provides:	XFree86 = %{version}-%{release}
Provides:	X11 = %{version}-%{release}
Provides:	fonts-ttf-vera
Obsoletes:	fonts-ttf-vera
Obsoletes:	XFree86
Obsoletes:	X11-ISO8859-2
Obsoletes:	X11-ISO8859-9

%description
The X Window System provides the base technology
for developing graphical user interfaces. Simply stated,
X draws the elements of the GUI on the user's screen and
builds methods for sending user interactions back to the
application. X also supports remote application deployment--running an
application on another computer while viewing the input/output 
on your machine.  X is a powerful environment which supports
many different applications, such as games, programming tools,
graphics programs, text editors, etc.


%package -n %{xflib}
Summary:	Shared libraries needed by the X Window System version 11 release 6
Group:		System/Libraries
Requires(post):	grep
Requires(post):	ldconfig
Requires(postun): grep
Requires(postun): ldconfig
Provides:	libXft2
Obsoletes:	libXft2
Provides:	X11-libs = %{version}-%{release}
Provides:	XFree86-libs = %{version}-%{release}
Obsoletes:	XFree86-libs
%ifarch sparc
Obsoletes:	X11R6.1-libs
%endif
Provides:	%{old_xflib} = %{version}-%{release}
Obsoletes:	%{old_xflib}

%description -n %{xflib}
X11-libs contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).


%package -n %{xfdev}
Summary:	Headers and programming man pages
Group:		Development/C
Obsoletes:	Mesa-devel
Provides:	Mesa-devel
Provides:	Xft-devel
Provides:	libXft2-devel
Provides:	XFree86-devel = %{version}-%{release}
Provides:	X11-devel
Obsoletes:	XFree86-devel
Obsoletes:	libXft2-devel
%ifarch sparc
Obsoletes:	X11R6.1-devel
%endif
Requires:	%{xflib} = %{version}
Requires:	glibc-devel
Requires:	/lib/cpp
%if %{with_new_fontconfig_Xft}
Requires:	fontconfig-devel >= 2.1-4mdk
%endif
%if %{build_multiarch}
Requires:	multiarch-utils >= 1.0.7-1mdk
BuildRequires:	multiarch-utils >= 1.0.7-1mdk
%endif
Provides:	%{old_xfdev} = %{version}-%{release}
Obsoletes:	%{old_xfdev}

%description -n %{xfdev}
%{xfdev} includes the libraries, header files and documentation
you'll need to develop programs which run in X clients. X11 includes
the base Xlib library as well as the Xt and Xaw widget sets.


%package -n %{xfsta}
Summary:	X11R6 static libraries
Group:		System/Libraries
Requires:	%{xfdev} = %{version}
Obsoletes:	XFree86-static-libs
Provides:	XFree86-static-libs = %{version}-%{release}
Provides:	XFree86-static-devel = %{version}-%{release}
Provides:	X11-static-devel = %{version}-%{release}
Provides:	%{old_xfsta} = %{version}-%{release}
Obsoletes:	%{old_xfsta}

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
* Sun Jun 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.8.2
- drop S13 and S14: pam-related
- drop buildrequires: pam-devel

* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.8.2
- drop the requires needed for the main xorg-x11 package which we don't ship

* Mon Jun 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.8.2
- rebuild with gcc4
- spec cleanups
- remove the pre/post stuff for the main package for font cache
  manipulation since we don't care about that stuff and don't even
  ship the server

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.8.2
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.8.2
- Obfuscate email addresses and new tagging
- Uncompress patches
- remove %%_iconsdir reference

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
