%define name	XFree86
%define version 4.3
%define release 27sls

%{!?build_propolice:%global build_propolice 0}

%define _unpackaged_files_terminate_build 0
%define baseversion 420

%define x11prefix	%{_prefix}/X11R6
%define x11bindir	%{x11prefix}/bin
# Architecture independant config files
%define x11libdir	%{x11prefix}/lib
# Architecture dependent libraries and modules
%define x11shlibdir	%{x11prefix}/%{_lib}

%define x11icondir      /usr/share/icons

%define xflib  %mklibname xfree 86
%define xfdev  %{xflib}-devel
%define xfsta  %{xflib}-static-devel

# Define Mandrake Linux version we are building for
%define mdkversion %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandrake-release)

%define usecvs		1
%define cvsversion	%{version}
%define usefreetype2	1
%define havematroxhal	0
%define usematroxhal	0
%define BuildDebugVersion 0
#We're using the new fontconfig based Xft1 1.2 lib now.
%define with_new_fontconfig_Xft 0
# comment this out to see if we build
#%if %mdkversion >= 910
#%define with_new_fontconfig_Xft 1
#%endif

%{?_with_debug: %{expand: %%define BuildDebugVersion 1}}
%{?_without_debug: %{expand: %%define BuildDebugVersion 0}}
%{?_with_matroxhal: %{expand: %%define havematroxhal 1}}
%{?_without_matroxhal: %{expand: %%define havematroxhal 0}}

Summary:	Part of the XFree86 implementation of the X Window System.
Name:		%{name}
Version:	%{version}
%if !%{BuildDebugVersion}
Release:	%{release}
%else
# debug with -g
Release:	%{release}g
%endif
License:	MIT
Group:		System/XFree86
Icon:		XFree86-logo.xpm
URL:		http://www.xfree86.org/
%if %{usecvs}
Source0:	XFree86-%{cvsversion}.tar.bz2
%else
Source0:	ftp://ftp.xfree86.org/pub/XFree86/%{version}/source/X%{baseversion}src-1.tar.bz2
Source1:	ftp://ftp.xfree86.org/pub/XFree86/%{version}/source/X%{baseversion}src-2.tar.bz2
Source2:	ftp://ftp.xfree86.org/pub/XFree86/%{version}/source/X%{baseversion}src-3.tar.bz2
%endif
Source3:	xserver.pamd
Source4:	xdm.pamd
Source5:	xfs.init
Source6:	xfs.config
Source8:	xdm.init
Source9:	twm.method
Source10:	system.twmrc
#Source11:	http://keithp.com/~keithp/fonts/XftConfig
# from Arnd Bergmann <std7652@et.FH-Osnabrueck.DE>
# only used when not build with fontconfig
Source11:	XftConfig
Source12:	xfs.run
Source13:	xfs-log.run
Source100:	Euro.xmod.bz2
Source102:	eurofonts-X11.tar.bz2
# some bdf fonts made by us, to cover encodings which haven't
# any available fonts so at least one font is provided for them
# it should regularly be checked and fonts added or removed
# depending on the support of new encodings and the availability
# of better fonts -- pablo
Source151:	mdk_drakx_fonts.tar.bz2
# extra *.enc files for xfs server not (yet) in XFree86 -- pablo
Source152:	xfsft-encodings.tar.bz2
# locale.dir, compose.dir, locale.alias files.
# maintaining them trough patches is a nightmare, as they change
# too much too often; it is easier to manage them separately -- pablo
Source153:	XFree86-compose.dir.bz2
Source154:	XFree86-locale.alias.bz2
Source155:	XFree86-locale.dir.bz2
#
Source156:	gemini-koi8-u.tar.bz2
# the new default unicode compose file is too human-unfriendly; keeping
# the old one...
Source157:	XFree86-4.2.0-en_US.UTF-8.old.bz2
# I18n updates from Pablo
# Devanagari OpenType font, to install for the indic opentype patch -- pablo
Source160:	XFree86-extrascalablefonts-font.tar.bz2
#source mdk icons (by deush)
Source200:	icons-%{name}.tar.bz2
%if %{havematroxhal}
Source201:	ftp://ftp.matrox.com/pub/mga/archive/linux/2003/mgadrivers-2.1-src.tgz
Source2010:	ftp://ftp.matrox.com/pub/mga/archive/linux/2003/lnx21notes.txt
%endif
# Savage driver dropin
Source202:	ftp://ftp.probo.com/pub/savage-1.1.27t.tar.bz2
# S3 driver dropin 0.3.21
#Source203:	ftp://devel.linuxppc.org/users/ajoshi/s3/s3-0.3.21.tar.bz2
# wacom driver update
Source204:	http://people.mandrakesoft.com/~flepied/wacom/xf86Wacom.c.bz2
# trident driver from 4.1.0 sources
Source206:	trident-4.1.0.tar.bz2
# sis dropin from http://www.webit.at/~twinny/linuxsis630.shtml
Source207:	http://www.webit.at/~twinny/sis/sis_drv_src_060802-2.tar.bz2
# driver for VIA CLE266
Source208:	XFree86-4.3-via.tar.bz2
Patch0:		XFree86-4.2.0-branch.patch.bz2
#
# Libs patches #################################################################
#
Patch3:		XFree86-4.2.99.3-xft-loadtarget.patch.bz2
# (fc) 4.3-11mdk update xft to 2.1.3
Patch6:		XFree86-4.3-xft212.patch.bz2
# (fc) 4.3-11mdk update xrender to 0.8.3
Patch7:		XFree86-4.3-xrender083.patch.bz2
#
# Progs patches ################################################################
#
# Fix xman to work with bzipped pages
Patch102:	XFree86-4.2.99.3-xman-bzip2.patch.bz2
# modifications for  startx (argument parsing and font rendering)
# catch sigterm in xinit and startx
Patch104:	XFree86-4.2.99.3-startx.patch.bz2
# Fix matrices text-look in man pages (Thierry Vignaud)
Patch106:	XFree86-4.2.1-gl-matrix-man-fixes.patch.bz2
#
# X server patches #############################################################
#
Patch200:	XFree86-4.2.99.3-parallel-make.patch.bz2
Patch201:	XFree86-4.2.99.3-mandrakelinux-blue.patch.bz2
Patch202:	XFree86-xwrapper.patch.bz2
# Pablo i18n patchs -- please if the patches don't apply anymore
# after an upgrade of XFree86 sources write me (pablo) instead
# of just discarding the patch, as discarding it may lead to
# loss of support for some locales. Thanks.
#
Patch203:	XFree86-4.2.99.5-i18n.diff.bz2
# Keyboard fixes patches -- pablo
Patch204:	XFree86-4.3-fixkbd.diff.bz2
# patch to use the old (xfree86 4.2) keyboard layouts, as the new
# ones give too much trouble (problems with emacs, missing, keys)
# the new ones should be tested again in the future to see if the
# problems have gone -- pablo
Patch207:	XFree86-4.2.99-oldkbd.diff.bz2
# Acecad driver from the Author
# http://perso.wanadoo.fr/edouard.tisserant/acecad/
Patch208:	XFree86-4.2.99.3-acecad.patch.bz2
# HP keyboard support (Nicolas Planel)
Patch209:	XFree86-4.2.0-xkb-hp_symbols.patch.bz2
# Build the following libraries with PIC: libxf86config, libXau, libxkbfile
Patch210:	XFree86-4.3-build-libs-with-pic.patch.bz2
# icondir support from Mike Harris
Patch211:	XFree86-4.2.99.3-Imake-make-icondir-configurable.patch.bz2
# open mouse twice to workaround a bug in the kernel when dealing
# with a PS/2 mouse and an USB keuboard
Patch212:	XFree86-4.3-mouse-twice.patch.bz2
Patch213:	XFree86-4.3.0-gb18030.patch.bz2
Patch214:	XFree86-4.3.0-gb18030-enc.patch.bz2
Patch215:	XFree86-4.3-elfloader-nonexec-page.patch.bz2
Patch216:	XFree86-4.3-_LP64-fix.patch.bz2
#
# Drivers patches ##############################################################
#
Patch514:	XFree86-4.1.0-agpgart-load.patch.bz2
Patch521:	XFree86-4.2.0-tdfx-libglide-name.patch.bz2
# try to open vt starting at vt 7
Patch528:	XFree86-4.2.0-vt7.patch.bz2
# report keyboard read errors
Patch531:	XFree86-4.2.1-kbd-error.patch.bz2
# Chips CT69000: disable hardware accelaration for now (RH #74841)
Patch532:	XFree86-4.2.1-chips-CT69000-noaccel.patch.bz2
# Chips CT65550: force software cursor for now (RH #82438)
Patch533:	XFree86-4.2.1-chips-CT65550-swcursor.patch.bz2
# savage
Patch536:	XFree86-4.2.99.3-savage-pci-id-fixes.patch.bz2
Patch537:	XFree86-4.2.99.902-savage-Imakefile-vbe-fixup.patch.bz2
Patch538:	XFree86-4.2.99.902-savage-1.1.26cvs-1.1.27t-fixups.patch.bz2
Patch539:	XFree86-4.2.99.902-savage-1.1.26cvs-1.1.27t-accel-fixup.patch.bz2
# ati
Patch540:	XFree86-4.3-ati-r300.patch.bz2
Patch541:	XFree86-4.3-radeon-1-igp.patch.bz2
Patch542:	XFree86-4.3-radeon-2-rv280.patch.bz2
Patch543:	XFree86-4.3-radeon-3-lcd.patch.bz2
# Patch from Keith Whitwell/Michel Dänzer to avoid Radeon dri Xserver recycle lockup
Patch544:	XFree86-4.3-radeon-4-recycle-lockup.patch.bz2
# nv
Patch550:	XFree86-4.3-nv-init.patch.bz2
# intel i8x0
Patch560:	XFree86-4.3-vt_fix.patch.bz2
Patch561:	XFree86-4.3-blankscreen.patch.bz2
#
# platforms specific patches start here
#
# PPC patches
# Dadou - 4.0.2-4mdk - 600 is based on sources available here:
#                      rsync -arvz linuxppc.org::xfree86-pmac .
# reworked 600 with duplicate patches picked up by 4.0.3 removed
# sbenedict
Patch600:	XFree86-4.0.2-ppc-patches-ani-joshi-tree-20010327.patch.bz2
Patch601:	XFree86-4.0.2-ppc-build-ati-drivers.patch.bz2
# Missing link flag against dl library (for dlopen(), dlsym(), ...) (Gwenole)
Patch610:	XFree86-4.1.0-glxinfo-dl.patch.bz2
# We do need PIC code for shared libraries (Gwenole)
Patch611:	XFree86-4.1.0-glx-pic.patch.bz2
# Patch for building in Debug mode
Patch700:	XFree86-4.2.99.3-acecad-debug.patch.bz2
# 4.3 branch update
Patch800:	XFree86-4.3-branch-4.3.patch.bz2
# HEAD branch update to fix deadlock using threads and Xi
Patch801:	XFree86-4.3-xi-lock.patch.bz2
# fix Multiple Unspecified Integer Overflow Vulnerabilities (bugtrag 8514)
Patch802:	XFree86-4.3-font-security.patch.bz2
# patch for propolice support
Patch803:	XFree86-4.3-propolice.patch.bz2
# fix xdm pam_setcred vulnerability (CAN-2003-0690)
Patch804:	XFree86-4.x-xdm-pam-setcred-security.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	zlib-devel flex bison groff pam-devel ncurses-devel perl
BuildRequires:	libpng-devel
%if %{usefreetype2}
BuildRequires:	freetype2-devel
%endif
# We need fontconfig for the new Xft1
%if %{with_new_fontconfig_Xft}
BuildRequires:	fontconfig-devel >= 2.1-4mdk
%endif

Requires:	pam >= 0.66-18, util-linux, sh-utils, xinitrc >= 2.4.4-10mdk
Requires:	XFree86 >= 3.3.6
Requires:	gcc-cpp
Prereq:		utempter XFree86-libs = %{version}
%if %{with_new_fontconfig_Xft}
PreReq:		fontconfig
%endif
Obsoletes:	XFree86-ISO8859-2, XFree86-ISO8859-9
Provides:	XFree86-ISO8859-2, XFree86-ISO8859-9


%description
If you want to install the X Window System (TM) on
your machine, you'll need to install XFree86.

The X Window System provides the base technology
for developing graphical user interfaces. Simply stated,
X draws the elements of the GUI on the user's screen and
builds methods for sending user interactions back to the
application. X also supports remote application deployment--running an
application on another computer while viewing the input/output 
on your machine.  X is a powerful environment which supports
many different applications, such as games, programming tools,
graphics programs, text editors, etc.  XFree86 is the version of
X which runs on Linux, as well as other platforms.

This package contains the basic fonts, programs and documentation
for an X workstation.  You will also need the XFree86-server
package, which contains the program which drives your video
hardware.

In addition to installing this package, you will need to install the
drakxtools package to configure your card using XFdrake. You may also
need to install one of the XFree86 fonts packages.

And finally, if you are going to develop applications that run as 
X clients, you will also need to install %{xfdev}.

%if %{havematroxhal}
This version was built with Matrox HALlib enabled.
%endif

%package 75dpi-fonts
Summary:	A set of 75 dpi resolution fonts for the X Window System.
Group:		System/Fonts/X11 bitmap
Prereq:		chkfontpath, psmisc, /usr/X11R6/bin/xset, XFree86 = %{version}
%ifarch sparc
Obsoletes:	X11R6.1-75dpi-fonts
%endif
Obsoletes:	XFree86-ISO8859-2-75dpi-fonts, XFree86-ISO8859-9-75dpi-fonts
Provides:	XFree86-ISO8859-2-75dpi-fonts, XFree86-ISO8859-9-75dpi-fonts

%description 75dpi-fonts
XFree86-75dpi-fonts contains the 75 dpi fonts used
on most X Window Systems. If you're going to use the 
X Window System, you should install this package, unless 
you have a monitor which can support 100 dpi resolution. 
In that case, you may prefer the 100dpi fonts available in 
the XFree86-100dpi-fonts package.

You may also need to install other XFree86 font packages.

To install the X Window System, you will need to install
the XFree86 package, the XFree86 package corresponding to
your video card, the X11R6-contrib package, the Xconfigurator
package and the XFree86-libs package.

Finally, if you are going to develop applications that run
as X clients, you will also need to install the
%{xfdev} package.

%package 100dpi-fonts
Summary:	X Window System 100dpi fonts.
Group:		System/Fonts/X11 bitmap
Prereq:		chkfontpath, psmisc, /usr/X11R6/bin/xset, XFree86 = %{version}
%ifarch sparc
Obsoletes:	X11R6.1-100dpi-fonts
%endif
Obsoletes:	XFree86-ISO8859-2-100dpi-fonts, XFree86-ISO8859-9-100dpi-fonts
Provides:	XFree86-ISO8859-2-100dpi-fonts, XFree86-ISO8859-9-100dpi-fonts

%description 100dpi-fonts
If you're going to use the X Window System and you have a
high resolution monitor capable of 100 dpi, you should install
XFree86-100dpi-fonts. This package contains a set of
100 dpi fonts used on most Linux systems.

If you are installing the X Window System, you will also
need to install the XFree86 package, the XFree86
package corresponding to your video card, the X11R6-
contrib package, the Xconfigurator package and the
XFree86-libs package. If you need to display certain
fonts, you may also need to install other XFree86 fonts
packages.

And finally, if you are going to develop applications that
run as X clients, you will also need to install the
%{xfdev} package.

%package cyrillic-fonts
Summary:	Cyrillic fonts - only needed on the server side.
Group:		System/Fonts/X11 bitmap
Prereq:		chkfontpath, psmisc, /usr/X11R6/bin/xset, XFree86 = %{version}

%description cyrillic-fonts
The Cyrillic fonts included with XFree86 3.3.2 and higher. Those who
use a language requiring the Cyrillic character set should install
this package.

%package -n %{xflib}
Summary:	Shared libraries needed by the X Window System version 11 release 6.
Group:		System/Libraries
Prereq:		grep /sbin/ldconfig
Provides:	libXft2
Obsoletes:	libXft2
Provides:	XFree86-libs = %version-%release
Obsoletes:	XFree86-libs
%ifarch sparc
Obsoletes:	X11R6.1-libs
%endif

%description -n %{xflib}
XFree86-libs contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

If you are installing the X Window System on your machine, you will need to
install XFree86-libs.  You will also need to install the XFree86 package,
the XFree86-75dpi-fonts package or the XFree86-100dpi-fonts package
(depending upon your monitor's resolution), the Xconfigurator package and
the X11R6-contrib package.  And, finally, if you are going to be developing
applications that run as X clients, you will also need to install
%{xfdev}.

%package -n %{xfdev}
Summary:	Headers and programming man pages.
Group:		Development/C
Obsoletes:	Mesa-devel
Provides:	Mesa-devel
Provides:	Xft-devel
Provides:	libXft2-devel
Provides:	XFree86-devel = %version-%release
Obsoletes:	XFree86-devel
Obsoletes:	libXft2-devel
%ifarch sparc
Obsoletes:	X11R6.1-devel
%endif
Requires:	XFree86-libs = %{version}-%{release}, glibc-devel, /lib/cpp
%if %{with_new_fontconfig_Xft}
Requires:	fontconfig-devel >= 2.1-4mdk
%endif

%description -n %{xfdev}
%{xfdev} includes the libraries, header files and documentation
you'll need to develop programs which run in X clients. XFree86 includes
the base Xlib library as well as the Xt and Xaw widget sets.

For guidance on programming with these libraries, O'Reilly & Associates
produces a series on X programming which you might find useful.

Install %{xfdev} if you are going to develop programs which
will run as X clients.

If you need the static libraries, install the %{xfsta}
package.

%package -n %{xfsta}
Summary:	X11R6 static libraries
Group:		System/Libraries
Requires:	%{xfdev} = %{version}-%{release}
Obsoletes:	XFree86-static-libs
Provides:	XFree86-static-libs = %{version}-%{release}
Provides:	XFree86-static-devel = %{version}-%{release}

%description -n %{xfsta}
%{xfsta} includes the X11R6 static libraries needed to
build statically linked programs.

%package Xvfb
Summary:	A virtual framebuffer X Windows System server for XFree86.
Group:		System/XFree86
Requires:	XFree86 = %{version}-%{release}

%description Xvfb
Xvfb (X Virtual Frame Buffer) is an X Windows System server
that is capable of running on machines with no display hardware and no
physical input devices.  Xvfb emulates a dumb framebuffer using virtual
memory.  Xvfb doesn't open any devices, but behaves otherwise as an X
display.  Xvfb is normally used for testing servers.  Using Xvfb, the mfb
or cfb code for any depth can be exercised without using real hardware
that supports the desired depths.  Xvfb has also been used to test X
clients against unusual depths and screen configurations, to do batch
processing with Xvfb as a background rendering engine, to do load testing,
to help with porting an X server to a new platform, and to provide an
unobtrusive way of running applications which really don't need an X
server but insist on having one. 

If you need to test your X server or your X clients, you may want to
install Xvfb for that purpose.

%package Xnest
Summary:	A nested XFree86 server.
Group:		System/XFree86
Requires:	XFree86-xfs
Requires:	XFree86 = %{version}-%{release}

%description Xnest
Xnest is an X Window System server which runs in an X window.
Xnest is a 'nested' window server, actually a client of the 
real X server, which manages windows and graphics requests 
for Xnest, while Xnest manages the windows and graphics 
requests for its own clients.

You will need to install Xnest if you require an X server which
will run as a client of your real X server (perhaps for
testing purposes).

%package server
Summary:	The X server and associated modules
Group:		System/XFree86
Requires:	XFree86 = %{version}-%{release}
Requires:	XFree86-xfs
Obsoletes:	xserver-wrapper

%description server
XFree86-server is the new generation of X server from XFree86.

%package xfs
Group:		System/Servers
Summary:	Font server for XFree86
Prereq:		shadow-utils setup
Requires:	initscripts >= 5.27-28mdk
Requires:	XFree86-libs = %{version}-%{release}
Prereq:		rpm-helper chkfontpath 
Obsoletes:	xtt

%description xfs
This is a font server for XFree86.  You can serve fonts to other X servers
remotely with this package, and the remote system will be able to use all
fonts installed on the font server, even if they are not installed on the
remote computer.

%package -n X11R6-contrib
Summary:	A collection of user-contributed X Window System programs
Group:		System/XFree86
Requires:	XFree86 = %{version}-%{release}

%description -n X11R6-contrib
If you want to use the X Window System, you should install X11R6-contrib. This
package holds many useful programs from the X Window System, version 11,
release 6 contrib tape. The programs, contributed by various users, include
listres, xbiff, xedit, xeyes, xcalc, xload and xman, among others.

you will also need to install the XFree86 package, the XFree86 package which
corresponds to your video card, one or more of the XFree86 fonts packages, the
Xconfigurator package and the XFree86-libs package.

Finally, if you are going to develop applications that run as X clients, you
will also need to install %{xfdev}.

%prep
%if %{usecvs}
%setup -q -c
%else
%setup -q -c -a 1 -a 2 

%patch0 -p0 -b .branch
%endif

bzcat %{SOURCE208} | tar xf -

bzcat %{SOURCE204} > xc/programs/Xserver/hw/xfree86/input/wacom/xf86Wacom.c

# cd xc/programs/Xserver/hw/xfree86/drivers
# bzcat %{SOURCE205} | tar x
# mv ati ati.old
# mv ati.2 ati
# bzcat %{SOURCE206} | tar x
# cd -
# 
cd xc/programs/Xserver/hw/xfree86/drivers
mv savage savage-1.1.26
bzcat %{SOURCE202} | tar x
cd -
# 
# cd xc/programs/Xserver/hw/xfree86/drivers/sis
# bzcat %{SOURCE207} | tar x
# patch -p0 < Imakefile_4.2.patch
# cd -

%patch6 -p1 -b .xft212
%patch7 -p1 -b .xrender083

%if %{with_new_fontconfig_Xft}
%patch3 -p0 -b .xft-loadtarget
%else
#%patch2 -p1 -b .xft-memleak
%endif

# progs patches

%patch102 -p1 -b .xman-bzip2
%patch104 -p1 -b .startx
%patch106 -p1 -b .gl-matrix-man-fixes

# X server patches

%patch200 -p1 -b .parallel-make
%patch201 -p1 -b .mandrakelinux-blue
%patch202 -p0 -b .xwrapper

%patch208 -p1 -b .acecad

# (Pablo) i18n patches
# please if there is any problem here tell me (pablo@mandrakesoft.com) instead
# of just silently discarding the patch. -- pablo
%patch203 -p1 -b .i18n
%patch204 -p1 -b .fixxkb
# it doesn't work :-( so better not to apply it for now -- pablo
#%patch205 -p1 -b .ximswitch
#===================
#%patch206 -p1 -b .en_US.UTF
%patch207 -p1 -b .old_kbd
%patch213 -p0 -b .gb18030
%patch214 -p0 -b .gb18030-enc

%patch209 -p0 -b .xkb-hp

%patch210 -p1 -b .build-libs-with-pic

%patch211 -p0 -b .Imake-make-icondir-configurable

%patch212 -p1 -b .mouse-twice

%patch215 -p1 -b .elfloader-nonexec-page
%patch216 -p1 -b ._LP64-fix

%patch514 -p1 -b .agpload

%patch521 -p1 -b .libglide-name

%if %{BuildDebugVersion}
%patch700 -p1 -b .debug
%endif

%patch528 -p1 -b .vt7

%patch531 -p1 -b .kbd-error

%patch532 -p1 -b .chips-CT69000-noaccel
%patch533 -p1 -b .chips-CT65550-swcursor

%patch536 -p0 -b .savage-pci-id-fixes
%patch537 -p0 -b .savage-Imakefile-vbe-fixup
%patch538 -p0 -b .savage-1.1.26cvs-1.1.27t-fixups
%patch539 -p0 -b .savage-1.1.26cvs-1.1.27t-accel-fixup

%patch540 -p1 -b .ati-r300
%patch541 -p0 -b .radeon-1-igp
%patch542 -p0 -b .radeon-2-rv280
%patch543 -p0 -b .radeon-3-lcd
%patch544 -p1 -b .radeonlockup

%patch550 -p1 -b .nv-init

%patch560 -p1 -b .vt-fix
%patch561 -p1 -b .blankscreen

%patch800 -p1 -b .branch-4.3
%patch801 -p1 -b .xi-lock
%patch802 -p1 -b .font-security
# (vdanen) until we get this module thing sorted out...
#%if %{build_propolice}
#%patch803 -p0 -b .propolice
#%endif
%patch804 -p0 -b .xdm-pam_setcred

# backup the original files (so we can look at them later) and use our own
cp xc/nls/compose.dir xc/nls/compose.dir.orig
cp xc/nls/locale.alias xc/nls/locale.alias.orig
cp xc/nls/locale.dir xc/nls/locale.dir.orig
cp xc/nls/Compose/en_US.UTF-8 xc/nls/Compose/en_US.UTF-8.orig
bzcat %{SOURCE153} | sed 's/#/XCOMM/g' > xc/nls/compose.dir
bzcat %{SOURCE154} | sed 's/#/XCOMM/g' > xc/nls/locale.alias
bzcat %{SOURCE155} | sed 's/#/XCOMM/g' > xc/nls/locale.dir
bzcat %{SOURCE157} | sed 's/#/XCOMM/g' > xc/nls/Compose/en_US.UTF-8

# (gb) Check for constants merging capabilities to disable
NO_MERGE_CONSTANTS=$(if %{__cc} -fno-merge-constants -S -o /dev/null -xc /dev/null >/dev/null 2>&1; then echo "-fno-merge-constants"; fi)

# Build with -fno-strict-aliasing if gcc >= 3.1 is used
NO_STRICT_ALIASING=$(%{__cc} -dumpversion | awk -F "." '{ if (int($1)*100+int($2) >= 301) print "-fno-strict-aliasing" }')

%if %{build_propolice}
# (vdanen) for the time being, build without stack protection until we can
# figure out how to build just the modules without protection
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS |sed 's/-fstack-protector//'`
%endif

%if ! %{BuildDebugVersion}
# compiling with -g is too huge
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's/-g//'`
%endif

echo "configuring with $RPM_OPT_FLAGS"

cat >xc/config/cf/host.def <<END
%if %{BuildDebugVersion}
#define XFree86Devel		YES
#define DoLoadableServer	NO
%endif

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
#define HasFreetype2		YES
#define Freetype2Dir            /usr
#define Freetype2LibDir		%{_libdir}
#define Freetype2IncDir		/usr/include/freetype2
%else
#define BuildFreetype2Library   NO
%endif
#define HasBlindFaithInUnicode	YES
#define BuildFonts		YES
#define BuildCyrillicFonts	YES
#define BuildXF86MiscExt	YES
#define BuildHtmlManPages	NO
#define XVendorString		"Mandrake Linux (XFree86 %{version}, patch level %{release})"
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

#define AdmDir 			/var/log
#define LbxproxyDir 		/etc/X11/lbxproxy
#define ProxyManagerDir 	/etc/X11/proxymngr
#define ServerConfigDir 	/etc/X11/xserver
#define XdmDir 			/etc/X11/xdm
#define XConfigDir 		/etc/X11
#define XinitDir 		/etc/X11/xinit

#define DefaultCursorTheme	core

%if %{havematroxhal}
#define HaveMatroxHal		YES
%else
#define HaveMatroxHal		NO
%endif
%if %{usematroxhal}
#define UseMatroxHal		YES
%else
#define UseMatroxHal		NO
%endif

/* Let's build libraries which only come in static form with PIC so
   that KDE can be prelink'able. */
%ifarch %{ix86}
#define StaticNeedsPicForShared YES
%endif

%ifarch %{ix86}
#define XF86ExtraCardDrivers via
%endif

%ifarch alpha
#define XF86CardDrivers mga nv tga s3virge sis rendition \
			neomagic i740 tdfx cirrus tseng trident chips apm \
			fbdev ati vga v4l glint
%endif
%ifarch x86_64
#define XF86CardDrivers mga fbdev vga ati savage nv glint vesa \
			tga s3virge sis rendition neomagic cirrus tseng \
			trident chips apm fbdev ati vga v4l tdfx \
			DevelDrivers XF86OSCardDrivers XF86ExtraCardDrivers
%endif
%ifarch ia64
#define XF86CardDrivers mga nv s3virge sis rendition i740 \
			tdfx v4l fbdev glint ati vga 
%endif
%ifarch ppc
#define XF86CardDrivers mga glint s3virge sis savage \
                        trident chips tdfx fbdev ati \
			DevelDrivers vga nv \
			XF86OSCardDrivers XF86ExtraCardDrivers
%endif

%if !%{BuildDebugVersion}
#define ExtraXInputDrivers acecad
%endif

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
%if %{havematroxhal}
(cd xc/programs/Xserver/hw/xfree86/drivers/mga/HALlib
gzip -cd %{SOURCE201} | tar xf - \
        mgadrivers-2.1-src/4.2.1/drivers/src/HALlib/mgaHALlib.a \
        mgadrivers-2.1-src/4.2.1/drivers/src/HALlib/binding.h
mv mgadrivers-2.1-src/4.2.1/drivers/src/HALlib/mgaHALlib.a .
mv mgadrivers-2.1-src/4.2.1/drivers/src/HALlib/binding.h .
rm -rf mgadrivers-2.1-src
)
cp -p xc/programs/Xserver/hw/xfree86/drivers/mga/HALlib/binding.h \
        xc/programs/Xserver/hw/xfree86/drivers/mga
%endif

# DrakX fonts
mkdir mdk-fonts
bzcat %{SOURCE151} | tar xf - -C mdk-fonts

%build
%if %{build_propolice}
# (vdanen) for the time being, build without stack protection until we can
# figure out how to build just the modules without protection
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS |sed 's/-fstack-protector//'`
%endif

%if ! %{BuildDebugVersion}
# compiling with -g is too huge
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's/-g//'`
%endif

echo "compiling with $RPM_OPT_FLAGS"

[ -z "$RPM_BUILD_NCPUS" ] && RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -gt 1 ] && PARALLELMFLAGS="-j$RPM_BUILD_NCPUS"

# Build with -fno-strict-aliasing if gcc >= 3.1 is used
NO_STRICT_ALIASING=$(%{__cc} -dumpversion | awk -F "." '{ if (int($1)*100+int($2) >= 301) print "-fno-strict-aliasing" }')

RPM_OPT_FLAGS="$RPM_OPT_FLAGS $NO_STRICT_ALIASING"

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
%if %{BuildDebugVersion}
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS|sed 's/-fomit-frame-pointer//'|sed 's/-ffast-math//')
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -g"
%else
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS|sed 's/-fomit-frame-pointer//'|sed 's/-ffast-math//')
%endif
make World -C xc CC="gcc" CXX="g++" CDEBUGFLAGS="$RPM_OPT_FLAGS" \
	CXXDEBUGFLAGS="$RPM_OPT_FLAGS" \
	DEFAULTFONTPATH="/usr/X11R6/lib/X11/fonts/misc:unscaled,unix/:-1" \
	TOPPARALLELMFLAGS="$PARALLELMFLAGS"
%endif

# DrakX fonts
for i in mdk-fonts/*.bdf ; do
	LD_LIBRARY_PATH=xc/lib/font xc/programs/bdftopcf/bdftopcf -o mdk-fonts/`basename $i .bdf`.pcf $i
done
gzip -9f mdk-fonts/*.pcf

echo PACKAGING DOCUMENTATION
# rezip these - they are in the old compress format
find xc/doc/hardcopy -name \*.PS.Z | xargs gzip -df
find xc/doc/hardcopy -name \*.PS | xargs gzip -f

groff -Tascii -ms xc/doc/misc/RELNOTES.ms > xc/doc/hardcopy/RELNOTES.txt
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

%if %{BuildDebugVersion}
(cd xc/programs/Xserver/hw/xfree86/input
for i in mouse calcomp citron digitaledge dmc dynapro elographics \
	microtouch mutouch penmount spaceorb summa wacom void hyperpen; do \
	(cd $i; make CDEBUGFLAGS="$RPM_OPT_FLAGS -fno-fast-math -g")
done)
(cd xc/programs/Xserver/GL/mesa/src/X
make CDEBUGFLAGS="$RPM_OPT_FLAGS -fno-fast-math -g"
)
%endif

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p $RPM_BUILD_ROOT/etc/pam.d
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/xserver
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/xdm
mkdir -p $RPM_BUILD_ROOT/etc/security/console.apps
touch $RPM_BUILD_ROOT/etc/security/console.apps/xserver

mkdir -p $RPM_BUILD_ROOT/usr/include
rm -f $RPM_BUILD_ROOT/usr/include/X11

make DESTDIR=$RPM_BUILD_ROOT install install.man -C xc
mkdir -p $RPM_BUILD_ROOT/etc/X11

# remove libGLU (in Mesa-common)
rm -f $RPM_BUILD_ROOT/usr/X11R6/%{_lib}/libGLU*
rm -f $RPM_BUILD_ROOT/usr/X11R6/include/GL/glu.h
rm -f $RPM_BUILD_ROOT/usr/X11R6/man/man3/glu

# XftConfig (only if not using fontconfig)
%if %{with_new_fontconfig_Xft}
cat <<-EOF > $RPM_BUILD_ROOT/etc/X11/XftConfig.README-OBSOLETE
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
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT/etc/X11/XftConfig
rm -f $RPM_BUILD_ROOT/usr/X11R6/lib/X11/XftConfig
cd $RPM_BUILD_ROOT/usr/X11R6/lib/X11; ln -s ../../../../etc/X11/XftConfig; cd -
%endif

# we don't want the libz.a from XFree86 -- it's broken
rm -f $RPM_BUILD_ROOT/usr/X11R6/%{_lib}/libz.a

# we don't want libXpm from XFree86
rm -f $RPM_BUILD_ROOT/usr/X11R6/%{_lib}/libXpm*
rm -f $RPM_BUILD_ROOT/usr/X11R6/include/X11/{Xpm.h,xpm.h}

# setup the default X server
rm -f $RPM_BUILD_ROOT/usr/X11R6/bin/X
ln -s Xwrapper $RPM_BUILD_ROOT/usr/X11R6/bin/X

# explicitly create X authdir
mkdir -p $RPM_BUILD_ROOT/etc/X11/xdm/authdir
chmod 0700 $RPM_BUILD_ROOT/etc/X11/xdm/authdir

# Move config config stuff to /etc/X11
mkdir -p $RPM_BUILD_ROOT/etc/X11
#ln -sf ../../../../etc/X11/XF86Config $RPM_BUILD_ROOT/usr/X11R6/lib/X11/XF86Config
mv $RPM_BUILD_ROOT/usr/X11R6/lib/X11/XF86Config.eg $RPM_BUILD_ROOT/usr/X11R6/lib/X11/XF86Config-4.eg

# for i in twm fs xsm; do
#     rm -rf $RPM_BUILD_ROOT/etc/X11/$i
#     cp -ar $RPM_BUILD_ROOT/usr/X11R6/lib/X11/$i $RPM_BUILD_ROOT/etc/X11
#     rm -rf $RPM_BUILD_ROOT/usr/X11R6/lib/X11/$i
#     ln -sf ../../../../etc/X11/$i $RPM_BUILD_ROOT/usr/X11R6/lib/X11/$i
# done

# This one is on xinitrc package now.
## install replacement Xsession file for xdm
#install -m 755 $RPM_SOURCE_DIR/Xsession.mandrake \
#      $RPM_BUILD_ROOT/etc/X11/xdm/Xsession

# we install our own config file for the xfs package
mkdir -p $RPM_BUILD_ROOT/etc/X11/fs
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT/etc/X11/fs/config

mkdir -p %{buildroot}%{_srvdir}/xfs/log
mkdir -p %{buildroot}%{_srvlogdir}/xfs
install -m 0750 %{SOURCE12} %{buildroot}%{_srvdir}/xfs/run
install -m 0750 %{SOURCE13} %{buildroot}%{_srvdir}/xfs/log/run

# we get xinit from a separate package
rm -rf $RPM_BUILD_ROOT/usr/X11R6/lib/X11/xinit
ln -sf ../../../../etc/X11/xinit $RPM_BUILD_ROOT/usr/X11R6/lib/X11/xinit

# Fix up symlinks
mkdir -p $RPM_BUILD_ROOT/usr/bin $RPM_BUILD_ROOT/usr/man
mkdir -p $RPM_BUILD_ROOT/usr/include $RPM_BUILD_ROOT/usr/lib
ln -sf ../X11R6/bin $RPM_BUILD_ROOT/usr/bin/X11
ln -sf ../X11R6/man $RPM_BUILD_ROOT/usr/man/X11
ln -sf ../X11R6/include/X11 $RPM_BUILD_ROOT/usr/include/X11
ln -sf ../X11R6/lib/X11 $RPM_BUILD_ROOT/usr/lib/X11

# this gets the wrong permissions by default -- I don't know or care why
chmod 755 $RPM_BUILD_ROOT/usr/X11R6/lib/X11/xkb/geometry/sgi

# this certainly doesn't need to be setuid
chmod 755 $RPM_BUILD_ROOT/usr/X11R6/bin/dga

# EURO support
cd $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/misc;
 tar xjf %{SOURCE102}
 LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{x11shlibdir} $RPM_BUILD_ROOT/usr/X11R6/bin/bdftopcf -t Xlat9-8x14.bdf |gzip -9 >Xlat9-8x14-lat9.pcf.gz;
 LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{x11shlibdir} $RPM_BUILD_ROOT/usr/X11R6/bin/bdftopcf -t Xlat9-9x16.bdf |gzip -9 >Xlat9-9x16-lat9.pcf.gz;
 rm *.bdf
 LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{x11shlibdir} $RPM_BUILD_ROOT/usr/X11R6/bin/mkfontdir $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/misc
cd -

# fixing a bug in XFree86 that uses two different directories instead
# of only one...
if [ ! -r $RPM_BUILD_ROOT/usr/X11R6/lib/X11/locale/zh_CN/XI18N_OBJS ]; then
	mv $RPM_BUILD_ROOT/usr/X11R6/lib/X11/locale/zh/XI18N_OBJS \
		$RPM_BUILD_ROOT/usr/X11R6/lib/X11/locale/zh_CN/
	rmdir $RPM_BUILD_ROOT/usr/X11R6/lib/X11/locale/zh
fi

if [ ! -r $RPM_BUILD_ROOT/usr/X11R6/lib/X11/locale/zh_CN.UTF-8/XI18N_OBJS ]; then
        cp -p $RPM_BUILD_ROOT/usr/X11R6/lib/X11/locale/zh_TW.UTF-8/XI18N_OBJS $RPM_BUILD_ROOT/usr/X11R6/lib/X11/locale/zh_CN.UTF-8/XI18N_OBJS
fi

#======================
# a dirty hack to make japanese, polish etc display correctly -- pablo
chmod u+w $RPM_BUILD_ROOT/usr/X11R6/lib/X11/locale/*/*

for i in $RPM_BUILD_ROOT/usr/X11R6/lib/X11/locale/* 
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
for i in $RPM_BUILD_ROOT/usr/X11R6/lib/X11/locale/*/Compose
do
  cp $i tmpfile
  cat tmpfile | \
  sed 's/<dead_diaeresis> <space>.*$/<dead_diaeresis> <space> : "\\"" quotedbl/' | \
  sed "s/<dead_acute> <space>.*$/<dead_acute> <space> : \"'\" apostrophe/" \
  > $i
done
rm -f tmpfile

# Encoding files for xfsft font server
bzcat %{SOURCE152} | tar xf - -C $RPM_BUILD_ROOT
gzip -9 -f $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/encodings/*.enc || :
gzip -9 -f $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/encodings/large/*.enc || :
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{x11shlibdir} $RPM_BUILD_ROOT/usr/X11R6/bin/mkfontdir -e $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/encodings \
	-e $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/encodings/large
rm -f $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/encodings/encodings.dir 
cat encodings.dir | sed "s|$RPM_BUILD_ROOT||" \
	> $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/encodings/encodings.dir
cat encodings.dir | sed "s|$RPM_BUILD_ROOT||" \
	> $RPM_BUILD_ROOT/etc/X11/encodings.dir
%if !%{with_new_fontconfig_Xft}
/usr/X11R6/bin/xftcache $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/Type1/ || \
	touch $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/Type1/XftCache
/usr/X11R6/bin/xftcache $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/TTF/ || \
	touch $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/TTF/XftCache
%endif

# gemini-koi8 fonts
tar jxvf %{SOURCE156} -C $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts
grep '^!' $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/ukr/fonts.alias > \
	README-ukr-fonts
rm -f $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/ukr/fonts.alias
cd $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/ukr
gunzip *.Z
gzip -9 *.pcf
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{x11shlibdir} $RPM_BUILD_ROOT/usr/X11R6/bin/mkfontdir
cd -
pwd

# DrakX fonts
mkdir $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/mdk
cp mdk-fonts/*.gz $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/mdk/
LD_LIBRARY_PATH=xc/lib/font $RPM_BUILD_ROOT/usr/X11R6/bin/mkfontdir $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/mdk

# installing the extra OpenType fonts
mkdir -p $RPM_BUILD_ROOT/usr/share/fonts/otf/mdk
(
	cd $RPM_BUILD_ROOT/usr/share/fonts/otf/mdk
	bzcat %{SOURCE160} | tar xvf -
	%if %{with_new_fontconfig_Xft}
    rm -f $RPM_BUILD_ROOT/usr/share/fonts/otf/mdk/XftCache
	%else
    /usr/X11R6/bin/xftcache $RPM_BUILD_ROOT/usr/share/fonts/otf/mdk/ || \
	touch $RPM_BUILD_ROOT/usr/share/fonts/otf/mdk/XftCache
	%endif
)

# List modules without glide_drv.o

rm -f modules.list
find $RPM_BUILD_ROOT%{x11shlibdir}/modules -type f -print | egrep -v 'glide_dri.so|tdfx_dri.so' | sed s@$RPM_BUILD_ROOT@@ > modules.list

# Fix list of static libs to list only static lib without a dynamic one.
FILTER='libXau|libGLw|libfntstubs|liboldX|libxf86config|libxkbfile|libxkbui|libXfontcache|libXinerama|libXdmcp|libFS|libXss|libfontbase|libXv|libXxf86dga|libXxf86misc|libXxf86rush|libXxf86vm|libXvMC|libI810XvMC'
rm -f static.list
find $RPM_BUILD_ROOT%{x11shlibdir} -type f -maxdepth 1 -name '*.a' -print | egrep -v $FILTER | sed s@$RPM_BUILD_ROOT@@ > static.list
rm -f static-only.list
find $RPM_BUILD_ROOT%{x11shlibdir} -type f -maxdepth 1 -name '*.a' -print | egrep $FILTER | sed s@$RPM_BUILD_ROOT@@ > static-only.list

#not needed, failsafe use twm
%if 0
mkdir -p $RPM_BUILD_ROOT/etc/X11/wmsession.d
cat > $RPM_BUILD_ROOT/etc/X11/wmsession.d/09Twm << EOF
NAME=Twm
DESC=TWM
EXEC=/usr/X11R6/bin/twm
SCRIPT:
exec /usr/X11R6/bin/twm
EOF
%endif

#mdk menu icons
install -d $RPM_BUILD_ROOT%{_iconsdir}
tar xjvf %{SOURCE200} -C $RPM_BUILD_ROOT%{_iconsdir}

# remove xterm resources to avoid conflicts with the xterm package
rm -f $RPM_BUILD_ROOT/etc/X11/app-defaults/*XTerm*

mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
cat << EOF > $RPM_BUILD_ROOT/etc/logrotate.d/xdm
/var/log/xdm-error.log {
    notifempty
    missingok
    nocompress
}
EOF

# for compatibility with the Linux/OpenGL standard base
mkdir -p $RPM_BUILD_ROOT/usr/include
pushd $RPM_BUILD_ROOT/usr/include
ln -sf ../X11R6/include/GL GL
popd

# quick fix
mkdir -p $RPM_BUILD_ROOT/var/lib/xdm
cd $RPM_BUILD_ROOT/etc/X11/xdm
rm -f authdir
ln -sf ../../../var/lib/xdm authdir

%if %{BuildDebugVersion}
export DONT_STRIP=1
%endif

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mv $RPM_BUILD_ROOT%{x11shlibdir}/pkgconfig/*.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig

# remove files not packaged
%if %{with_new_fontconfig_Xft}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/X11/{XftConfig,XftConfig-OBSOLETE} \
 $RPM_BUILD_ROOT%{x11bindir}/xftcache \
 $RPM_BUILD_ROOT%{x11libdir}/X11/XftConfig-OBSOLETE \
 $RPM_BUILD_ROOT%{x11prefix}/man/man1/xftcache.*
%endif
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/X11/twm/system.twmrc \
 $RPM_BUILD_ROOT%{_sysconfdir}/X11/xdm/{*Console,X*,xdm-config} \
 $RPM_BUILD_ROOT%{_sysconfdir}/X11/xdm/pixmaps \
 $RPM_BUILD_ROOT%{x11bindir}/{cxpm,luit,resize,sxpm,uxterm,xterm,xtrap*} \
 $RPM_BUILD_ROOT%{x11prefix}/man/man1/{cxpm.*,luit.*,pswrap.*,resize.*,showfont.*,sxpm.*,xterm.*,xtrap.*} \
 $RPM_BUILD_ROOT%{x11libdir}/X11/{Options,XF86Config.98} \
 $RPM_BUILD_ROOT%{x11libdir}/X11/fonts/{util,CID,local}

%post
for d in misc Speedo Type1 TTF mdk; do
    cd /usr/X11R6/lib/X11/fonts/$d
    mkfontdir || :
done

fc-cache || :

%if ! %{with_new_fontconfig_Xft}
xftcache > /dev/null 2>&1 || :
%endif

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

%post 75dpi-fonts
umask 133
cd /usr/X11R6/lib/X11/fonts/75dpi
mkfontdir || :
%if %{with_new_fontconfig_Xft}
/usr/bin/fc-cache . || :
%endif
/usr/sbin/chkfontpath -q -a /usr/X11R6/lib/X11/fonts/75dpi:unscaled

%postun 75dpi-fonts
umask 133
if [ "$1" = "0" ]; then
	/usr/sbin/chkfontpath -q -r /usr/X11R6/lib/X11/fonts/75dpi:unscaled
fi

%post 100dpi-fonts
umask 133
cd /usr/X11R6/lib/X11/fonts/100dpi
mkfontdir || :
%if %{with_new_fontconfig_Xft}
/usr/bin/fc-cache . || :
%endif
/usr/sbin/chkfontpath -q -a /usr/X11R6/lib/X11/fonts/100dpi:unscaled

%postun 100dpi-fonts
if [ "$1" = "0" ]; then
	/usr/sbin/chkfontpath -q -r /usr/X11R6/lib/X11/fonts/100dpi:unscaled
fi

%post cyrillic-fonts
umask 133
cd /usr/X11R6/lib/X11/fonts/cyrillic
mkfontdir || :
%if %{with_new_fontconfig_Xft}
/usr/bin/fc-cache . || :
%endif
/usr/sbin/chkfontpath -q -a /usr/X11R6/lib/X11/fonts/cyrillic:unscaled
cd /usr/X11R6/lib/X11/fonts/ukr
mkfontdir || :
/usr/sbin/chkfontpath -q -a /usr/X11R6/lib/X11/fonts/ukr:unscaled

%postun cyrillic-fonts
umask 133
if [ "$1" = "0" ]; then
	/usr/sbin/chkfontpath -q -r /usr/X11R6/lib/X11/fonts/cyrillic:unscaled
        /usr/sbin/chkfontpath -q -r /usr/X11R6/lib/X11/fonts/ukr:unscaled
fi

%pre xfs
%_pre_useradd xfs /etc/X11/fs /bin/false 70

# for msec high security levels
%_pre_groupadd xgrp 16 xfs


%post xfs
# as we don't overwrite the config file, we may need to add those paths
# (2=update)
if [ "$1" -gt 1 ]; then
	for i in /usr/X11R6/lib/X11/fonts/drakfont \
			/usr/X11R6/lib/X11/fonts/pcf_drakfont:unscaled \
			/usr/X11R6/lib/X11/fonts/TTF
	do
		if ! grep "$i" /etc/X11/fs/config >/dev/null 2>/dev/null ; then
			/usr/sbin/chkfontpath -q -a "$i"
		fi
	done
fi
%_post_srv xfs


%preun xfs
%_preun_srv xfs

%postun xfs
%_postun_userdel xfs

%post server

if [ $1 -gt 1 ]; then
  if [ -r /etc/X11/XF86Config-4 ] && grep -q 'Option.*"XkbOptions".*grp:' /etc/X11/XF86Config-4; then
    perl -pi -e 's/^(\s*Option\s*"XkbLayout"\s*)"([^,]*)"/$1"us,$2"/' /etc/X11/XF86Config-4
  fi
fi

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files server -f modules.list
%defattr(-,root,root,-)
%doc /usr/X11R6/lib/X11/XF86Config-4.eg
/usr/X11R6/bin/XFree86

%files
%defattr(-,root,root,-)
%docdir /usr/X11R6/lib/X11/doc

%ifarch %{ix86} alpha sparc
%doc /usr/X11R6/lib/X11/Cards
%endif

%dir /usr/X11R6/lib/X11
%dir /etc/X11
%dir /etc/X11/rstart
%dir /etc/X11/rstart/commands
%dir /etc/X11/rstart/commands/x11r6
%dir /etc/X11/rstart/contexts
%dir /usr/X11R6/lib/X11/etc
%dir /usr/X11R6/lib/X11/fonts
%dir /usr/X11R6/lib/X11/xserver
%dir /usr/X11R6/man
%dir /usr/X11R6/man/man*

%dir /etc/X11/xkb
%dir /etc/X11/twm
%dir /etc/X11/xdm
%dir %attr(0700,root,root) /etc/X11/xdm/authdir
%dir /etc/X11/xsm
/etc/X11/xdm/chooser
%dir /var/lib/xdm

%config(noreplace) /etc/pam.d/xserver
%config(noreplace) /etc/pam.d/xdm
%config(missingok noreplace) /etc/security/console.apps/xserver
%config(noreplace) /etc/X11/xsm/system.xsm
%config(noreplace) /etc/logrotate.d/xdm

%if %{with_new_fontconfig_Xft}
# XftConfig is no longer present or used
/etc/X11/XftConfig.README-OBSOLETE
%else
%if %{usefreetype2}
%config(noreplace) /etc/X11/XftConfig
/usr/X11R6/lib/X11/XftConfig
%endif
%endif
/usr/X11R6/lib/X11/XErrorDB
/usr/X11R6/lib/X11/XKeysymDB
/usr/X11R6/lib/X11/locale
%config(noreplace) /etc/X11/lbxproxy/*
%config(noreplace) /etc/X11/proxymngr/*
%dir /etc/X11/app-defaults
%config(noreplace) /etc/X11/app-defaults/*

/usr/X11R6/lib/X11/xkb
/usr/X11R6/lib/X11/xkb/*
/var/lib/xkb
/usr/X11R6/lib/X11/xinit
/usr/X11R6/lib/X11/xdm
/usr/X11R6/lib/X11/twm
/usr/X11R6/lib/X11/xsm

/usr/X11R6/lib/X11/xserver/SecurityPolicy
#/usr/X11R6/lib/X11/XF86Config
/usr/X11R6/lib/X11/rstart/rstartd.real
%config(noreplace) /etc/X11/rstart/config
/usr/X11R6/lib/X11/rstart/commands/x11r6/@List
/usr/X11R6/lib/X11/rstart/commands/x11r6/LoadMonitor
/usr/X11R6/lib/X11/rstart/commands/x11r6/Terminal
/usr/X11R6/lib/X11/rstart/commands/@List
/usr/X11R6/lib/X11/rstart/commands/ListContexts
/usr/X11R6/lib/X11/rstart/commands/ListGenericCommands
/usr/X11R6/lib/X11/rstart/contexts/@List
/usr/X11R6/lib/X11/rstart/contexts/default
/usr/X11R6/lib/X11/rstart/contexts/x11r6
/usr/X11R6/lib/X11/x11perfcomp
/usr/X11R6/lib/X11/doc
/usr/X11R6/lib/X11/etc/sun.termcap
/usr/X11R6/lib/X11/etc/sun.terminfo
#/usr/X11R6/lib/X11/etc/xterm.termcap
#/usr/X11R6/lib/X11/etc/xterm.terminfo
/usr/X11R6/lib/X11/etc/xmodmap.std
/usr/X11R6/lib/X11/etc/Xinstall.sh
%attr(4711,root,root)		/usr/X11R6/bin/Xwrapper
/usr/X11R6/bin/X
/usr/X11R6/bin/Xprt
/usr/X11R6/bin/lbxproxy
/usr/X11R6/bin/proxymngr
/usr/X11R6/bin/rstartd
/usr/X11R6/bin/xfindproxy
/usr/X11R6/bin/xfwp
#/usr/X11R6/bin/xrx
/usr/X11R6/bin/lndir
/usr/X11R6/bin/mkdirhier
/usr/X11R6/bin/mergelib
/usr/X11R6/bin/makeg
/usr/X11R6/bin/appres
/usr/X11R6/bin/bdftopcf
/usr/X11R6/bin/beforelight
/usr/X11R6/bin/bitmap
/usr/X11R6/bin/bmtoa
/usr/X11R6/bin/atobm
/usr/X11R6/bin/editres
/usr/X11R6/bin/iceauth
/usr/X11R6/bin/mkfontdir
/usr/X11R6/bin/showrgb
/usr/X11R6/bin/rstart
/usr/X11R6/bin/smproxy
/usr/X11R6/bin/twm
/usr/X11R6/bin/x11perf
/usr/X11R6/bin/x11perfcomp
/usr/X11R6/bin/Xmark
/usr/X11R6/bin/xauth
/usr/X11R6/bin/xclipboard
/usr/X11R6/bin/xcutsel
/usr/X11R6/bin/xclock
/usr/X11R6/bin/xcmsdb
/usr/X11R6/bin/xconsole
/usr/X11R6/bin/xdm
/usr/X11R6/bin/sessreg
/usr/X11R6/bin/xdpyinfo
/usr/X11R6/bin/glxinfo
/usr/X11R6/bin/xgamma
/usr/X11R6/bin/revpath
%attr(0755,root,root)		/usr/X11R6/bin/dga
/usr/X11R6/bin/xfd
/usr/X11R6/bin/xhost
/usr/X11R6/bin/xinit
/usr/X11R6/bin/startx
/usr/X11R6/bin/setxkbmap
/usr/X11R6/bin/xkbcomp
/usr/X11R6/bin/xkbevd
/usr/X11R6/bin/xkbprint
/usr/X11R6/bin/xkbvleds
/usr/X11R6/bin/xkbwatch
/usr/X11R6/bin/xkbbell
/usr/X11R6/bin/xkill
/usr/X11R6/bin/xlogo
/usr/X11R6/bin/xlsatoms
/usr/X11R6/bin/xlsclients
/usr/X11R6/bin/xlsfonts
/usr/X11R6/bin/xmag
#/usr/X11R6/bin/xmh
/usr/X11R6/bin/xmodmap
/usr/X11R6/bin/xprop
/usr/X11R6/bin/xrdb
/usr/X11R6/bin/xset
/usr/X11R6/bin/xrefresh
/usr/X11R6/bin/xsetmode
/usr/X11R6/bin/xsetpointer
/usr/X11R6/bin/xsetroot
/usr/X11R6/bin/xsm
/usr/X11R6/bin/xstdcmap
#/usr/X11R6/bin/xterm
#/usr/X11R6/bin/nxterm
#/usr/X11R6/bin/resize
/usr/X11R6/bin/xvidtune
/usr/X11R6/bin/xvinfo
/usr/X11R6/bin/xwd
/usr/X11R6/bin/xwininfo
/usr/X11R6/bin/xwud
/usr/X11R6/bin/xon
/usr/X11R6/bin/xf86cfg

/usr/X11R6/bin/bdftruncate
/usr/X11R6/bin/ccmakedep
/usr/X11R6/bin/cleanlinks
/usr/X11R6/bin/dpsexec
/usr/X11R6/bin/dpsinfo
/usr/X11R6/bin/glxgears
/usr/X11R6/bin/gtf
%ifnarch ppc sparc sparc64
/usr/X11R6/bin/ioport
%endif
/usr/X11R6/bin/makepsres
/usr/X11R6/bin/makestrs
/usr/X11R6/bin/mkcfm
/usr/X11R6/bin/mkfontscale
/usr/X11R6/bin/mkhtmlindex
/usr/X11R6/bin/mmapr
/usr/X11R6/bin/mmapw
/usr/X11R6/bin/oclock
/usr/X11R6/bin/pswrap
/usr/X11R6/bin/rman
/usr/X11R6/bin/texteroids
/usr/X11R6/bin/ucs2any
/usr/X11R6/bin/xcursor-config
/usr/X11R6/bin/xcursorgen
/usr/X11R6/bin/xfsinfo
/usr/X11R6/bin/xmh
/usr/X11R6/bin/xrandr
%if ! %{with_new_fontconfig_Xft}
/usr/X11R6/bin/xftcache
%endif
%{_iconsdir}/*.*
%{_iconsdir}/*/*

%ifarch %{ix86} alpha sparc
#/usr/X11R6/bin/reconfig
/usr/X11R6/bin/xf86config
/usr/X11R6/bin/scanpci
/usr/X11R6/bin/pcitweak
/usr/X11R6/man/man1/scanpci.1x*
/usr/X11R6/man/man1/pcitweak.1x*
%endif

/usr/X11R6/include/X11/bitmaps
/usr/X11R6/include/X11/pixmaps

%x11icondir

/usr/X11R6/man/man1/lbxproxy.1x*
/usr/X11R6/man/man1/proxymngr.1x*
/usr/X11R6/man/man1/xfindproxy.1x*
/usr/X11R6/man/man1/xfwp.1x*
#/usr/X11R6/man/man1/xrx.1x*
/usr/X11R6/man/man1/lndir.1x*
/usr/X11R6/man/man1/makestrs.1x*
/usr/X11R6/man/man1/makeg.1x*
/usr/X11R6/man/man1/mkdirhier.1x*
/usr/X11R6/man/man1/appres.1x*
/usr/X11R6/man/man1/bdftopcf.1x*
/usr/X11R6/man/man1/beforelight.1x*
/usr/X11R6/man/man1/bitmap.1x*
/usr/X11R6/man/man1/bmtoa.1x*
/usr/X11R6/man/man1/atobm.1x*
/usr/X11R6/man/man1/editres.1x*
/usr/X11R6/man/man1/iceauth.1x*
/usr/X11R6/man/man1/mkfontdir.1x*
/usr/X11R6/man/man1/showrgb.1x*
/usr/X11R6/man/man1/rstart.1x*
/usr/X11R6/man/man1/rstartd.1x*
/usr/X11R6/man/man1/smproxy.1x*
/usr/X11R6/man/man1/twm.1x*
/usr/X11R6/man/man1/x11perf.1x*
/usr/X11R6/man/man1/x11perfcomp.1x*
/usr/X11R6/man/man1/xauth.1x*
/usr/X11R6/man/man1/xclipboard.1x*
/usr/X11R6/man/man1/xcutsel.1x*
/usr/X11R6/man/man1/xclock.1x*
/usr/X11R6/man/man1/xcmsdb.1x*
/usr/X11R6/man/man1/xconsole.1x*
/usr/X11R6/man/man1/xdm.1x*
/usr/X11R6/man/man1/sessreg.1x*
/usr/X11R6/man/man1/xdpyinfo.1x*
/usr/X11R6/man/man1/glxinfo.1x*
/usr/X11R6/man/man1/xgamma.1x*
/usr/X11R6/man/man1/revpath.1x*
/usr/X11R6/man/man1/dga.1x*
/usr/X11R6/man/man1/xfd.1x*
/usr/X11R6/man/man1/xhost.1x*
/usr/X11R6/man/man1/xinit.1x*
/usr/X11R6/man/man1/startx.1x*
/usr/X11R6/man/man1/setxkbmap.1x*
/usr/X11R6/man/man1/xkbcomp.1x*
/usr/X11R6/man/man1/xkbevd.1x*
/usr/X11R6/man/man1/xkbprint.1x*
/usr/X11R6/man/man1/xkill.1x*
/usr/X11R6/man/man1/xlogo.1x*
/usr/X11R6/man/man1/xlsatoms.1x*
/usr/X11R6/man/man1/xlsclients.1x*
/usr/X11R6/man/man1/xlsfonts.1x*
/usr/X11R6/man/man1/xmag.1x*
#/usr/X11R6/man/man1/xmh.1x*
/usr/X11R6/man/man1/xmodmap.1x*
/usr/X11R6/man/man1/xprop.1x*
/usr/X11R6/man/man1/xrdb.1x*
/usr/X11R6/man/man1/xrefresh.1x*
/usr/X11R6/man/man1/xset.1x*
/usr/X11R6/man/man1/xsetmode.1x*
/usr/X11R6/man/man1/xsetpointer.1x*
/usr/X11R6/man/man1/xsetroot.1x*
/usr/X11R6/man/man1/xsm.1x*
/usr/X11R6/man/man1/xstdcmap.1x*
#/usr/X11R6/man/man1/xterm.1x*
#/usr/X11R6/man/man1/resize.1x*
/usr/X11R6/man/man1/xvidtune.1x*
/usr/X11R6/man/man1/xvinfo.1x*
/usr/X11R6/man/man1/xwd.1x*
/usr/X11R6/man/man1/xwininfo.1x*
/usr/X11R6/man/man1/xwud.1x*
/usr/X11R6/man/man1/xon.1x*
/usr/X11R6/man/man1/Xserver.1x*
/usr/X11R6/man/man1/XFree86.1x*
/usr/X11R6/man/man1/xf86cfg.1x*

/usr/X11R6/man/man1/dpsexec.1x*
/usr/X11R6/man/man1/dpsinfo.1x*
/usr/X11R6/man/man1/glxgears.1x*                                             
/usr/X11R6/man/man1/libxrx.1x*
/usr/X11R6/man/man1/makepsres.1x*
/usr/X11R6/man/man1/mkcfm.1x*
/usr/X11R6/man/man1/oclock.1x*
/usr/X11R6/man/man1/rman.1x*
/usr/X11R6/man/man1/texteroids.1x*
/usr/X11R6/man/man1/xfsinfo.1x*
/usr/X11R6/man/man1/Xmark.1x*
/usr/X11R6/man/man1/xmh.1x*

/usr/X11R6/man/man1/bdftruncate.1x*
/usr/X11R6/man/man1/ccmakedep.1x*
/usr/X11R6/man/man1/cleanlinks.1x*
/usr/X11R6/man/man1/gccmakedep.1x*
/usr/X11R6/man/man1/gtf.1x*
/usr/X11R6/man/man1/mergelib.1x*
/usr/X11R6/man/man1/mkfontscale.1x*
/usr/X11R6/man/man1/mkhtmlindex.1x*
/usr/X11R6/man/man1/ucs2any.1x*
/usr/X11R6/man/man1/xcursorgen.1x*
/usr/X11R6/man/man1/xrandr.1x*

/usr/X11R6/man/man5/XF86Config.5x*
/usr/X11R6/man/man4/*
/usr/X11R6/man/man7/*

%ifarch %{ix86} alpha sparc
#/usr/X11R6/man/man1/reconfig.1x*
/usr/X11R6/man/man1/xf86config.1x*
%endif

%dir /usr/X11R6/lib/X11/fonts/Speedo
/usr/X11R6/lib/X11/fonts/Speedo/*.spd
%ghost /usr/X11R6/lib/X11/fonts/Speedo/fonts.dir
/usr/X11R6/lib/X11/fonts/Speedo/fonts.scale
/usr/X11R6/lib/X11/fonts/Speedo/encodings.dir

%dir /usr/X11R6/lib/X11/fonts/Type1
/usr/X11R6/lib/X11/fonts/Type1/*.pfa
/usr/X11R6/lib/X11/fonts/Type1/*.pfb
/usr/X11R6/lib/X11/fonts/Type1/*.afm
%if ! %{with_new_fontconfig_Xft}
/usr/X11R6/lib/X11/fonts/Type1/XftCache
%endif
%ghost /usr/X11R6/lib/X11/fonts/Type1/fonts.dir
/usr/X11R6/lib/X11/fonts/Type1/fonts.scale
/usr/X11R6/lib/X11/fonts/Type1/fonts.cache-1
/usr/X11R6/lib/X11/fonts/Type1/encodings.dir

%dir /usr/X11R6/lib/X11/fonts/TTF
/usr/X11R6/lib/X11/fonts/TTF/*.ttf
/usr/X11R6/lib/X11/fonts/TTF/fonts.cache-1
%if ! %{with_new_fontconfig_Xft}
/usr/X11R6/lib/X11/fonts/TTF/XftCache
%endif
%ghost /usr/X11R6/lib/X11/fonts/TTF/fonts.dir
/usr/X11R6/lib/X11/fonts/TTF/fonts.scale
/usr/X11R6/lib/X11/fonts/TTF/encodings.dir

%dir /usr/X11R6/lib/X11/fonts/misc
/usr/X11R6/lib/X11/fonts/misc/*.gz
%ghost /usr/X11R6/lib/X11/fonts/misc/fonts.dir
/usr/X11R6/lib/X11/fonts/misc/fonts.alias

#default bitmap fonts
%dir /usr/X11R6/lib/X11/fonts/mdk
/usr/X11R6/lib/X11/fonts/mdk/*.gz
%ghost /usr/X11R6/lib/X11/fonts/mdk/fonts.dir

# default scalable fonts
%dir /usr/share/fonts/otf/mdk
/usr/share/fonts/otf/mdk/*

/usr/X11R6/lib/X11/rgb.txt

%files -n %{xflib}
%defattr(-,root,root,-)
%{x11shlibdir}/*.so.*
#%{x11shlibdir}/libXfont*.so.*
#%{x11shlibdir}/modules/dri/*.so

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
/usr/X11R6/include/X11/*.h
/usr/X11R6/include/GL
/usr/X11R6/include/DPS
/usr/X11R6/include/*.h
/usr/include/X11
/usr/include/GL
/usr/X11R6/man/man3/*

/usr/X11R6/lib/X11/config
/usr/X11R6/bin/imake
/usr/X11R6/bin/makedepend
/usr/X11R6/bin/gccmakedep
/usr/X11R6/bin/xft-config
/usr/X11R6/bin/xmkmf

/usr/X11R6/man/man1/imake.1x*
/usr/X11R6/man/man1/makedepend.1x*
/usr/X11R6/man/man1/xmkmf.1x*

%{x11shlibdir}/*.so

%{_libdir}/pkgconfig/xcursor.pc
%{_libdir}/pkgconfig/xft.pc

%files -n %{xfsta} -f static.list
%defattr(-,root,root,-)

%files Xvfb
%defattr(-,root,root,-)
/usr/X11R6/bin/Xvfb
/usr/X11R6/man/man1/Xvfb.1x*

%files Xnest
%defattr(-,root,root,-)
/usr/X11R6/bin/Xnest
/usr/X11R6/man/man1/Xnest.1x*

%files 75dpi-fonts
%defattr(-,root,root,-)
%dir /usr/X11R6/lib/X11/fonts/75dpi
/usr/X11R6/lib/X11/fonts/75dpi/*.gz
/usr/X11R6/lib/X11/fonts/75dpi/fonts.alias
%ghost /usr/X11R6/lib/X11/fonts/75dpi/fonts.dir
/usr/X11R6/lib/X11/fonts/75dpi/encodings.dir

%files 100dpi-fonts
%defattr(-,root,root,-)
%dir /usr/X11R6/lib/X11/fonts/100dpi
/usr/X11R6/lib/X11/fonts/100dpi/*.gz
/usr/X11R6/lib/X11/fonts/100dpi/fonts.alias
%ghost /usr/X11R6/lib/X11/fonts/100dpi/fonts.dir
/usr/X11R6/lib/X11/fonts/100dpi/encodings.dir

%files cyrillic-fonts
%defattr(-,root,root,-)
%dir /usr/X11R6/lib/X11/fonts/cyrillic
/usr/X11R6/lib/X11/fonts/cyrillic/*.gz
/usr/X11R6/lib/X11/fonts/cyrillic/fonts.alias
%ghost /usr/X11R6/lib/X11/fonts/cyrillic/fonts.dir
%doc README-ukr-fonts
%dir /usr/X11R6/lib/X11/fonts/ukr
/usr/X11R6/lib/X11/fonts/ukr/*.gz
%ghost /usr/X11R6/lib/X11/fonts/ukr/fonts.dir
/usr/X11R6/lib/X11/fonts/cyrillic/encodings.dir

%files xfs
%defattr(-,root,root,-)
#%doc xtt-%{xtt_ver}/doc/*
%attr(-,xfs,xfs) %dir /etc/X11/fs
%attr(-,xfs,xfs) %config(noreplace) /etc/X11/fs/config
%dir %{_srvdir}/xfs
%dir %{_srvdir}/xfs/log
%{_srvdir}/xfs/run
%{_srvdir}/xfs/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/xfs
%config(noreplace) /etc/X11/encodings.dir
/usr/X11R6/lib/X11/fs
#/usr/X11R6/bin/fsinfo
/usr/X11R6/bin/fslsfonts
/usr/X11R6/bin/fstobdf
/usr/X11R6/bin/xfs
/usr/X11R6/bin/showfont
/usr/X11R6/man/man1/xfs.1x*
#/usr/X11R6/man/man1/fsinfo.1x*
/usr/X11R6/man/man1/fslsfonts.1x*
/usr/X11R6/man/man1/fstobdf.1x*
#/usr/X11R6/man/man1/showfont.1x*
/usr/X11R6/lib/X11/fonts/encodings

%files -n X11R6-contrib
%defattr(-,root,root,-)
/usr/X11R6/bin/ico
/usr/X11R6/bin/listres
/usr/X11R6/bin/viewres
/usr/X11R6/bin/xbiff
/usr/X11R6/bin/xcalc
/usr/X11R6/bin/xditview
/usr/X11R6/bin/xedit
/usr/X11R6/bin/xev
/usr/X11R6/bin/xeyes
/usr/X11R6/bin/xfontsel
/usr/X11R6/bin/xgc
/usr/X11R6/bin/xload
/usr/X11R6/bin/xman
/usr/X11R6/bin/xmessage
/usr/X11R6/lib/X11/xman.help
/usr/X11R6/man/man1/ico.1x*
/usr/X11R6/man/man1/listres.1x*
/usr/X11R6/man/man1/viewres.1x*
/usr/X11R6/man/man1/xbiff.1x*
/usr/X11R6/man/man1/xcalc.1x*
/usr/X11R6/man/man1/xditview.1x*
/usr/X11R6/man/man1/xedit.1x*
/usr/X11R6/man/man1/xev.1x*
/usr/X11R6/man/man1/xeyes.1x*
/usr/X11R6/man/man1/xfontsel.1x*
/usr/X11R6/man/man1/xgc.1x*
/usr/X11R6/man/man1/xload.1x*
/usr/X11R6/man/man1/xman.1x*
/usr/X11R6/man/man1/xmessage.1x*
%{x11libdir}/X11/xedit

%changelog
* Mon May 10 2004 Vincent Danen <vdanen@opensls.org> 4.3-27sls
- rebuild against new libutempter

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3-26sls
- minor spec cleanups

* Wed Feb 04 2004 Vincent Danen <vdanen@opensls.org> 4.3-25sls
- get rid of %%build_opensls macros
- remove xfs initscript; supervise scripts
- xfs is static uid/gid 70
- xgrp is static gid 16
- remove PreReq: chkconfig

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3-24.3sls
- get rid of the menu stuff so we don't need menu package
- P804: fix for CAN-2003-0690 (pam_setcred in xdm)

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.3-24.2sls
- use %%build_opensls macro to not build -doc package
- don't build glide stuff

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.3-24.1sls
- P803: enable propolice support or we get unresolved symbols
- temporarily disable stack protection because the modules can't handle it;
  need to find a way to build the modules without stack protection but keep it
  everywhere else

* Mon Dec 02 2003 Vincent Danen <vdanen@opensls.org> 4.3-24sls
- OpenSLS build
- tidy spec

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

* Mon Sep 02 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 4.2.0-26mdk
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
to be able to work with xf 3 (fix from Paulo César Pereira de Andrade of Conectiva).

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
- add preliminary s3 driver (Jürgen Zimmermann)
- rebuild libXfont.so.1 after rebuild of libtype1 (Jürgen Zimmermann)
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

* Sat Jan  6 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com>  4.0.2-3mdk
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
- added a prereq on XFree86 = %%version for font packages to allow upgrade.
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

* Mon Jul 31 2000 François Pons <fpons@mandrakesoft.com> 4.0.1-6mdk
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
