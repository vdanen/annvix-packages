#
# spec file for package xorg-x11
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#

%define name		xorg-x11
%define version		6.8.2
%define release		1avx

%define sis_version	160604-1
%define unichromever	r30
%define unichromexvmc	0.13.3

%define renderver	0.8
%define xrenderver	0.8.4
%define xftver		2.1.6

# New drop-in Xrender and Xft libraries
%define with_new_xft_and_xrender	0
%define with_xft_and_xrender		0

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

%define havematroxhal		0
%define usematroxhal		0

%define build_xprt		1

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

%{?_with_matroxhal: %{expand: %%define havematroxhal 1}}
%{?_without_matroxhal: %{expand: %%define havematroxhal 0}}

%define build_dev_dri_drivers	1
%define build_new_sis_driver	0
%define build_new_savage_driver	0
%define build_gatos_ati_driver	0
%define build_new_via_driver	0

%define build_prefbusid		1
%{?_with_prefbusid: %global build_prefbusid 1}
%{?_without_prefbusid: %global build_prefbusid 0}

%define build_nosrc		0
%{?_with_nosrc: %global build_nosrc 1}
%{?_without_src: %global build_nosrc 1}

%ifarch %{ix86} x86_64
%define build_voodoo_driver	1
%define with_voodoo_driver	0
%else
%define build_voodoo_driver	0
%define with_voodoo_driver	0
%endif

%if %{build_voodoo_driver}
%define voodoo_driver_name	voodoo
%else
%define voodoo_driver_name	/* */
%endif

%ifarch %{ix86}
%define build_via_driver	1
%define build_new_via_driver	1
%else
%define build_via_driver	0
%endif

%if %{build_new_via_driver}
%define via_driver_name		via
%define build_viaxvmc		1
%define build_via_dri_driver	0
%else
%define via_driver_name		/* */
%define build_viaxvmc		0
%define build_via_dri_driver	0
%endif

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

Source100: Euro.xmod.bz2
Source102: eurofonts-X11.tar.bz2
# extra *.enc files for xfs server not (yet) in XFree86 -- pablo
Source152: xfsft-encodings.tar.bz2
# locale.dir, compose.dir, locale.alias files.
# maintaining them trough patches is a nightmare, as they change
# too much too often; it is easier to manage them separately -- pablo
Source153: XFree86-compose.dir.bz2
Source154: XFree86-locale.alias.bz2
Source155: XFree86-locale.dir.bz2
#
Source156: gemini-koi8-u.tar.bz2
# the new default unicode compose file is too human-unfriendly; keeping
# the old one...
Source157: X_Compose-en_US.UTF-8.bz2

# I18n updates from Pablo
# Devanagari OpenType font, to install for the indic opentype patch -- pablo
Source160: XFree86-extrascalablefonts-font.tar.bz2

%if %{havematroxhal}
Source201: ftp://ftp.matrox.com/pub/mga/archive/linux/2003/mgadrivers-3.0-src.tgz
Source2010: ftp://ftp.matrox.com/pub/mga/archive/linux/2003/lnx30notes.txt
NoSource: 201
NoSource: 2010
%endif
# Savage driver dropin
Source202: ftp://ftp.probo.com/pub/savage-1.1.27t.tar.bz2
# S3 driver dropin 0.3.21
#Source203: ftp://devel.linuxppc.org/users/ajoshi/s3/s3-0.3.21.tar.bz2

# trident driver from 4.1.0 sources
Source206: trident-4.1.0.tar.bz2

# sis dropin from http://www.webit.at/~twinny/linuxsis630.shtml
Source207: http://www.winischhofer.net/sis/sis_drv_src_%{sis_version}.tar.bz2

# driver for VIA CLE266 RH
#Source208: ftp://people.redhat.com/alan/XFree86/VIA/via-20040102.tar.bz2
Source209: ftp://people.redhat.com/alan/XFree86/VIA/via-dri-20040102.tar.bz2

# http://sourceforge.net/projects/unichrome/
Source208: http://aleron.dl.sourceforge.net/sourceforge/unichrome/unichrome-X-%{unichromever}.tar.bz2

# driver for vodooo RH
Source210: ftp://people.redhat.com/alan/XFree86/Voodoo/voodoo-1.0-beta3.tar.bz2

# Wonderland mouse cursor (Fedora)
Source212: wonderland-cursors.tar.bz2

Patch4:	X11R6.7.0-libfreetype-xtt2-1.2a.patch.bz2
Patch5:	Xorg-6.7.0-isolate_device.patch.bz2
#Patch5:	XFree86-4.3-PrefBusID-v3.patch.bz2

# Libs patches #################################################################

# Progs patches ################################################################

# Fix xman to work with bzipped pages
Patch102: Xorg-6.7.1-xman-bzip2.patch.bz2
# modifications for  startx (argument parsing and font rendering)
# catch sigterm in xinit and startx
Patch104: XFree86-4.3.99.902-startx.patch.bz2
# Fix matrices text-look in man pages (Thierry Vignaud)
Patch106: XFree86-4.2.1-gl-matrix-man-fixes.patch.bz2

# Allow the reserve keywork in Xservers
Patch110: XFree86-4.3-xdm-reserve.patch.bz2


# X server patches #############################################################

Patch200: XFree86-4.2.99.3-parallel-make.patch.bz2
Patch201: XFree86-4.2.99.3-mandrakelinux-blue.patch.bz2
Patch202: XFree86-4.3.99.901-xwrapper.patch.bz2

# Pablo i18n patchs -- please if the patches don't apply anymore
# after an upgrade of XFree86 sources write me (pablo) instead
# of just discarding the patch, as discarding it may lead to
# loss of support for some locales. Thanks.
#
Patch203: xorg-x11-6.8.2-i18n.diff.bz2
# Keyboard fixes patches -- pablo
Patch204: xorg-x11-6.8.2-fixkbd.diff.bz2

# patch to use the old (xfree86 4.2) keyboard layouts, as the new
# ones give too much trouble (problems with emacs, missing, keys)
# the new ones should be tested again in the future to see if the
# problems have gone -- pablo
Patch207: xorg-x11-6.7.0-oldkbd.diff.bz2

# fix brazilian keyboard (bug #14721)
Patch208: xorg-x11-6.8.2-compose-pt_br-utf8.patch.bz2

# HP keyboard support (Nicolas Planel)
Patch209: XFree86-4.2.0-xkb-hp_symbols.patch.bz2

# Build the following libraries with PIC: libxf86config, libXau, libxkbfile
Patch210: XFree86-4.3-build-libs-with-pic.patch.bz2

# open mouse twice to workaround a bug in the kernel when dealing
# with a PS/2 mouse and an USB keuboard
Patch212: XFree86-4.3-mouse-twice.patch.bz2

Patch213: XFree86-4.3.0-gb18030.patch.bz2
Patch214: XFree86-4.3.0-gb18030-enc.patch.bz2

Patch216: XFree86-4.3-_LP64-fix.patch.bz2

# add the evdev input driver from HEAD
Patch217: xorg-x11-6.8.2-evdev.patch.bz2

# Drivers patches ##############################################################

Patch514: XFree86-4.1.0-agpgart-load.patch.bz2

# try to open vt starting at vt 7
Patch528: XFree86-4.2.0-vt7.patch.bz2

# report keyboard read errors
Patch531: XFree86-4.2.1-kbd-error.patch.bz2

# Chips CT69000: disable hardware accelaration for now (RH #74841)
Patch532: XFree86-4.2.1-chips-CT69000-noaccel.patch.bz2

# Chips CT65550: force software cursor for now (RH #82438)
Patch533: XFree86-4.2.1-chips-CT65550-swcursor.patch.bz2

# savage
Patch536: XFree86-4.2.99.3-savage-pci-id-fixes.patch.bz2
Patch537: XFree86-4.2.99.902-savage-Imakefile-vbe-fixup.patch.bz2
Patch538: XFree86-4.2.99.902-savage-1.1.26cvs-1.1.27t-fixups.patch.bz2
Patch539: XFree86-4.2.99.902-savage-1.1.26cvs-1.1.27t-accel-fixup.patch.bz2

# ati
Patch540: XFree86-4.3-ati-r300.patch.bz2
Patch541: XFree86-4.3-radeon-1-igp.patch.bz2
Patch542: XFree86-4.3-radeon-2-rv280.patch.bz2
Patch543: XFree86-4.3-radeon-3-lcd.patch.bz2
# Patch from Keith Whitwell/Michel D�zer to avoid Radeon dri Xserver recycle lockup
Patch544: XFree86-4.3-radeon-4-recycle-lockup.patch.bz2

# nv
Patch550: XFree86-4.3-nv-init.patch.bz2

# intel i8x0
Patch560: XFree86-4.3-vt_fix.patch.bz2
# i945 from HEAD
Patch561: xorg-x11-6.8.2-i945.patch.bz2

# (sb) mk712
Patch562: xorg-x11-6.8.2-mk712.patch.bz2 
Patch563: xorg-x11-6.8.2-calibration.patch.bz2

# (sb) nvxbox
Patch564: xorg-x11-6.8.2-nvxbox.patch.bz2

# do not change permission if not requested
Patch565: xorg-x11-6.8.2-perm.patch.bz2

# (fc) fix crash in Xft (Mdk bug #16614), remove warnings when Render is missing and
# optimize one critical case for glyph extents (CVS)
Patch567: xorg-x11-6.8.2-xftcrash.patch.bz2
# (fc) add support for freetype embolding, fix mono clipping (CVS)
Patch568: xorg-x11-6.8.2-xftembold.patch.bz2

# Patch for building in Debug mode
Patch700: XFree86-4.2.99.3-acecad-debug.patch.bz2

# Xorg patches
# https://bugs.freedesktop.org/show_bug.cgi?id=2164
Patch5000: xorg-x11-6.8.2-radeon-render.patch.bz2
# https://bugs.freedesktop.org/show_bug.cgi?id=2380
Patch5001: xorg-x11-6.8.2-nv-ids.patch.bz2
# https://bugs.freedesktop.org/show_bug.cgi?id=2467
Patch5002: xorg-x11-6.8.2-void-driver.patch.bz2
# https://bugs.freedesktop.org/show_bug.cgi?id=2698
Patch5003: xorg-x11-6.8.2-radeon-merge.patch.bz2
# https://bugs.freedesktop.org/show_bug.cgi?id=2599
Patch5004: xorg-x11-6.8.2-xnest-stacking.patch.bz2

# RH patches

Patch9325: xorg-x11-6.8.2-gcc4-fix.patch.bz2
Patch9327: xorg-x11-6.8.2-ati-radeon-gcc4-fix.patch.bz2
#(sb) partially from fedora commits
Patch9328: xorg-x11-6.8.2-gcc40.patch.bz2

Patch9601: XFree86-4.3.99.902-mozilla-flash.patch.bz2

Patch10012: xorg-redhat-libGL-exec-shield-fixes.patch.bz2
Patch10015: XFree86-4.3.0-redhat-nv-riva-videomem-autodetection-debugging.patch.bz2

Patch10101: XFree86-4.3.0-makefile-fastbuild.patch.bz2


#via unichrome again, add XvMC lib
Patch20000: XFree86-4.4-libviaXvMC-%{unichromexvmc}-patch.bz2

# my addons (svetljo)

# build freetype2 with fPIC on x86_64
Patch40002: lib_freetype_module.patch.bz2  

Patch40014: xorg-DRI-TLS-01.patch.bz2
Patch40015: xorg-Mesa-TLS-01.patch.bz2
Patch40018: xorg-x11-6.8.2-radeon-ppc-fixes.patch.bz2
Patch40019: xorg-x11-6.8.2-radeon-ppc-fixes2.patch.bz2
Patch40020: xorg-x11-6.8.1-xvfb-backingstore.patch.bz2
Patch40021: xorg-x11-6.8.2-ppc-segfault-fix.patch.bz2

# p5000 https://bugs.freedesktop.org/show_bug.cgi?id=2073
Patch50000: xorg-x11-6.8.2-sunffb.patch.bz2

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

%if %{havematroxhal}
This version was built with Matrox HALlib enabled.
%endif

%package 75dpi-fonts
Summary: A set of 75 dpi resolution fonts for the X Window System
Group: System/Fonts/X11 bitmap
Prereq: chkfontpath, psmisc, /usr/X11R6/bin/xset, %{name} = %{version}
%ifarch sparc
Obsoletes: X11R6.1-75dpi-fonts
%endif
Obsoletes: XFree86-ISO8859-2-75dpi-fonts, XFree86-ISO8859-9-75dpi-fonts
Provides: XFree86-ISO8859-2-75dpi-fonts, XFree86-ISO8859-9-75dpi-fonts
Obsoletes: XFree86-75dpi-fonts
Provides: XFree86-75dpi-fonts = %{version}-%{release}
Provides: X11-75dpi-fonts
Requires: %{xflib} = %{version}

%description 75dpi-fonts
X11-75dpi-fonts contains the 75 dpi fonts used
on most X Window Systems. If you're going to use the 
X Window System, you should install this package, unless 
you have a monitor which can support 100 dpi resolution. 
In that case, you may prefer the 100dpi fonts available in 
the X11-100dpi-fonts package.

You may also need to install other X11 font packages.

To install the X Window System, you will need to install
the X11 package, the X11 package corresponding to
your video card, the X11R6-contrib package, the Xconfigurator
package and the X11-libs package.

Finally, if you are going to develop applications that run
as X clients, you will also need to install the
%{xfdev} package.

%package 100dpi-fonts
Summary: X Window System 100dpi fonts
Group: System/Fonts/X11 bitmap
Prereq: chkfontpath, psmisc, /usr/X11R6/bin/xset, %{name} = %{version}
%ifarch sparc
Obsoletes: X11R6.1-100dpi-fonts
%endif
Obsoletes: XFree86-ISO8859-2-100dpi-fonts, XFree86-ISO8859-9-100dpi-fonts
Provides: XFree86-ISO8859-2-100dpi-fonts, XFree86-ISO8859-9-100dpi-fonts
Obsoletes: XFree86-100dpi-fonts
Provides: XFree86-100dpi-fonts = %{version}-%{release}
Provides: X11-100dpi-fonts
Requires: %{xflib} = %{version}

%description 100dpi-fonts
If you're going to use the X Window System and you have a
high resolution monitor capable of 100 dpi, you should install
X11-100dpi-fonts. This package contains a set of
100 dpi fonts used on most Linux systems.

If you are installing the X Window System, you will also
need to install the X11 package, the X11
package corresponding to your video card, the X11R6-
contrib package, the Xconfigurator package and the
X11-libs package. If you need to display certain
fonts, you may also need to install other X11 fonts
packages.

And finally, if you are going to develop applications that
run as X clients, you will also need to install the
%{xfdev} package.

%package cyrillic-fonts
Summary: Cyrillic fonts - only needed on the server side
Group: System/Fonts/X11 bitmap
Prereq: chkfontpath, psmisc, /usr/X11R6/bin/xset, %{name} = %{version}
Obsoletes: XFree86-cyrillic-fonts
Provides: XFree86-cyrillic-fonts = %{version}-%{release}
Provides: X11-cyrillic-fonts
Requires: %{xflib} = %{version}

%description cyrillic-fonts
The Cyrillic fonts included with XFree86 3.3.2 and higher. Those who
use a language requiring the Cyrillic character set should install
this package.

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

%package doc
Summary: Documentation on various X11 programming interfaces
Group: System/X11
Obsoletes: XFree86-doc
Provides: XFree86-doc = %{version}-%{release}
Provides: X11-doc 

%description doc
X11-doc provides a great deal of extensive PostScript documentation
on the various X APIs, libraries, and other interfaces.  If you need
low level X documentation, you will find it here.  Topics include the
X protocol, the ICCCM window manager standard, ICE session management,
the font server API, etc.

%package Xvfb
Summary: A virtual framebuffer X Windows System server for X11
Group: System/X11
Requires: %{name} = %{version}
Requires: %{xflib} = %{version}
Obsoletes: XFree86-Xvfb
Provides: XFree86-Xvfb = %{version}-%{release}
Provides: X11-Xvfb 

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

%package xauth
Summary: Authentication information tool for X
Group: System/X11
Obsoletes: xauth
Provides: xauth = %{version}-%{release}

%description xauth
The xauth program is used to edit and display the authorization information
used in connecting to the X server.

%package Xnest
Summary: A nested X11 server
Group: System/X11
Requires: %{name}-xfs
Requires: %{name} = %{version}
Requires: %{xflib} = %{version}
Obsoletes: XFree86-Xnest
Provides: XFree86-Xnest = %{version}-%{release}
Provides: X11-Xnest 

%description Xnest
Xnest is an X Window System server which runs in an X window.
Xnest is a 'nested' window server, actually a client of the 
real X server, which manages windows and graphics requests 
for Xnest, while Xnest manages the windows and graphics 
requests for its own clients.

You will need to install Xnest if you require an X server which
will run as a client of your real X server (perhaps for
testing purposes).

%package Xdmx
Summary: Distributed Multi-head X server
Group: System/X11
Requires: %{name}-xfs
Requires: %{name} = %{version}
Requires: %{xflib} = %{version}
Provides: XFree86-Xdmx = %{version}-%{release}
Provides: X11-Xdmx 
%description Xdmx
Xdmx is a proxy X server that uses one or more other X servers
as its display devices. It provides multi-head X functionality 
for displays that might be located on different machines. 
 Xdmx functions as a front-end X server that acts as a proxy 
to a set of back-end X servers. All of the visible rendering is
passed to the back-end X servers. Clients connect to the Xdmx 
front-end, and everything appears as it would in a regular 
multi-head configuration. If Xinerama is enabled (e.g., 
with +xinerama on the command line), the clients see a single large screen.

Xdmx communicates to the back-end X servers using the standard X11 protocol,
and standard and/or commonly available X server extensions.


%package Xprt
Summary: A X11 Print server
Group: System/X11
Requires: %{name}-xfs
Requires: %{name} = %{version}
Requires: %{xflib} = %{version}
Provides: XFree86-Xprint = %{version}-%{release}
Provides: X11-Xprint 
%description Xprt
A X11 Print server.

%package server
Summary: The X server and associated modules
Group: System/X11
Requires: %{name}-xfs
Requires: %{name} = %{version}
Requires: %{xflib} = %{version}
Obsoletes: xserver-wrapper
Obsoletes: XFree86-server
Provides: XFree86-server  = %{version}-%{release}
Provides: X11-server

%description server
X11-xorg-server is the new generation of X server from X.Org.


%package xfs
Group: System/Servers
Summary: Font server for X11
Prereq: shadow-utils setup
Requires: initscripts >= 5.27-28mdk
Requires: %{xflib} = %{version}
Prereq: rpm-helper chkfontpath 
Obsoletes: xtt
Obsoletes: XFree86-xfs
Provides: XFree86-xfs = %{version}-%{release}

%description xfs
This is a font server for X11.  You can serve fonts to other X servers
remotely with this package, and the remote system will be able to use all
fonts installed on the font server, even if they are not installed on the
remote computer.

%package -n X11R6-contrib
Summary:	A collection of user-contributed X Window System programs
Group:		System/X11
Requires: 	%{xflib} = %{version}
Requires:	%{name} = %{version}


%description -n X11R6-contrib
If you want to use the X Window System, you should install X11R6-contrib. This
package holds many useful programs from the X Window System, version 11,
release 6 contrib tape. The programs, contributed by various users, include
listres, xbiff, xedit, xeyes, xcalc, xload and xman, among others.

you will also need to install the X11 package, the X11 package which
corresponds to your video card, one or more of the X11 fonts packages, the
Xconfigurator package and the X11-libs package.

Finally, if you are going to develop applications that run as X clients, you
will also need to install %{xfdev}.

%define now 0

%prep
%setup -q -c


# Replace XFree86 Xft2 and Xrender with updated versions from fontconfig.org
%if %{with_new_xft_and_xrender}
{
    pushd xc/lib
    bzcat %{SOURCE50} | tar xv
    mv render-%{renderver}/render*.h ../include/extensions/
    mkdir -p ../doc/hardcopy/render
    cp render-%{renderver}/{protocol,library} ../doc/hardcopy/render

    mv Xrender Xrender.old
    bzcat %{SOURCE51} | tar xv
    mv libXrender-%{xrenderver} Xrender
    cp Xrender.old/Imakefile Xrender/Imakefile

    rm {Xrender,Xft}/Makefile*
    touch {Xrender,Xft}/config.h
#    pushd Xrender
       # Generate config.h because it's needed
#       touch config.h
#    popd

    mv Xft Xft.old
    bzcat %{SOURCE52} | tar xv
    mv libXft-%{xftver} Xft
    cp Xft.old/Imakefile Xft/Imakefile
    ln -sf ../Xft.old/config Xft/config

    pushd Xft
    #patch -p1 < %{PATCH30101}
    # Generate config.h because it's needed
#       touch config.h
       mv Xft.3 Xft.man
       perl -p -i -e 's/\@VERSION\@/%{xftver}/' xft.pc.in
    popd

    popd
}
%endif


pushd xc

%if %{usefreetype218}
%patch4 -p1 -b .xtt2-1.2a
%endif

%if %{build_prefbusid}
%patch5 -p1 -b .isolatedev
%endif

popd

%if %{with_voodoo_driver}
{
   pushd xc/programs/Xserver/hw/xfree86/drivers
   bzcat %{SOURCE210} | tar x
   popd
}
%endif

%if %{build_gatos_ati_driver}
{
   pushd xc/programs/Xserver/hw/xfree86/drivers
   bzcat %{SOURCE205} | tar x
   mv ati ati.old
   mv ati.2 ati
   bzcat %{SOURCE206} | tar x
   popd
}
%endif

%if %{build_new_savage_driver}
{
   echo "Updating SAVAGE driver with %{SOURCE202}"
   pushd xc/programs/Xserver/hw/xfree86/drivers
   mv savage savage-4.3.0
   bzcat %{SOURCE202} | tar x
   popd
}
%endif

%if %{build_new_sis_driver}
{
   echo "Updating SIS driver with %{SOURCE207}"
   mkdir -p xc/programs/Xserver/hw/xfree86/drivers/sis.new
   pushd xc/programs/Xserver/hw/xfree86/drivers/sis.new
   bzcat %{SOURCE207} | tar x
   rm Imakefile*
   rm Makefile*
   cp -df *.{c,h} ../sis/
   popd
}
%endif


%if %{build_new_via_driver}
{
   echo "Updating VIA driver with %{SOURCE208}"
   pushd xc/programs/Xserver/hw/xfree86/drivers
   echo "Updating via driver to Unichrome %{unichromever}"
   bzcat %{SOURCE208} | tar xv
   mv unichrome-X-%{unichromever}/* via/ \
   && touch via/unichrome-X-%{unichromever}
   popd
}
%endif

# libs patches
%patch567 -p1 -b .xftcrash
%patch568 -p1 -b .xftembold

# progs patches

%patch102 -p1 -b .xman-bzip2
%patch104 -p1 -b .startx
%patch106 -p1 -b .gl-matrix-man-fixes
%patch110 -p1 -b .xdm-reserve

# X server patches

%patch200 -p1 -b .parallel-make
%patch201 -p1 -b .mandrakelinux-blue
%patch202 -p1 -b .xwrapper

%patch208 -p1 -b .compose-pt_br-utf8

# (Pablo) i18n patches
# please if there is any problem here tell me (pablo@mandriva.com) instead
# of just silently discarding the patch. -- pablo
%patch203 -p1 -b .i18n
%patch204 -p1 -b .fixxkb
#===================
%patch207 -p1 -b .old_kbd
%if %now
%patch213 -p0 -b .gb18030
%patch214 -p0 -b .gb18030-enc
%endif

%patch209 -p0 -b .xkb-hp

%patch210 -p1 -b .build-libs-with-pic

%patch212 -p1 -b .mouse-twice

%if %now
%patch216 -p1 -b ._LP64-fix
%endif

%patch217 -p1 -b .evdev

%patch514 -p1 -b .agpload

%patch528 -p1 -b .vt7

%patch531 -p1 -b .kbd-error

%patch532 -p1 -b .chips-CT69000-noaccel
%patch533 -p1 -b .chips-CT65550-swcursor

%patch536 -p0 -b .savage-pci-id-fixes

%if %now
%patch537 -p0 -b .savage-Imakefile-vbe-fixup
%patch538 -p0 -b .savage-1.1.26cvs-1.1.27t-fixups
%patch539 -p0 -b .savage-1.1.26cvs-1.1.27t-accel-fixup

%patch540 -p1 -b .ati-r300
%patch541 -p0 -b .radeon-1-igp
%patch542 -p0 -b .radeon-2-rv280
%patch543 -p0 -b .radeon-3-lcd
%patch544 -p1 -b .radeonlockup

%patch550 -p1 -b .nv-init
%endif

%patch560 -p1 -b .vt-fix
%patch561 -p1 -b .i945
%patch562 -p1 -b .mk712
%patch563 -p1 -b .calib
%patch564 -p1 -b .xbox
%patch565 -p1 -b .perm

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

%if %build_viaxvmc
pushd xc
%patch20000 -p1 -b .viaXvMC
popd
%endif

#disable for now

pushd xc

%ifarch alpha x86_64
%patch40002 -p1 -b .x86-64_lib_font-build_with_fPIC
%endif

popd
%patch40018 -p0 -b .radeon_ppc_fixes
%patch40019 -p0 -b .radeon_ppc_fixes2
%patch40020 -p0 -b .xvfb_backingstore
%patch40021 -p0 -b .ppc_missing_ddc_segfault_fix

# https://bugs.freedesktop.org/show_bug.cgi?id=2073
%patch50000 -p0 -b .sunffb

# backup the original files (so we can look at them later) and use our own
cp xc/nls/compose.dir xc/nls/compose.dir.orig
cp xc/nls/locale.alias xc/nls/locale.alias.orig
cp xc/nls/locale.dir xc/nls/locale.dir.orig
cp xc/nls/Compose/en_US.UTF-8 xc/nls/Compose/en_US.UTF-8.orig
bzcat %{SOURCE153} | sed 's/#/XCOMM/g' > xc/nls/compose.dir
bzcat %{SOURCE154} | sed 's/#/XCOMM/g' > xc/nls/locale.alias
bzcat %{SOURCE155} | sed 's/#/XCOMM/g' > xc/nls/locale.dir
bzcat %{SOURCE157} | sed 's/^#/XCOMM/g' > xc/nls/Compose/en_US.UTF-8
# pt_BR Compose file only purpose is to allow dead_actute+c -> ccedilla
bzcat %{SOURCE157} | sed 's/^#/XCOMM/g' | \
	sed 's/<dead_acute> <C> : "Ć" Cacute/<dead_acute> <C> : "Ç" Ccedilla/' | \
	sed 's/<dead_acute> <c> : "ć" cacute/<dead_acute> <c> : "ç" ccedilla/' \
	> xc/nls/Compose/pt_BR.UTF-8


# (gb) Check for constants merging capabilities to disable
NO_MERGE_CONSTANTS=$(if %{__cc} -fno-merge-constants -S -o /dev/null -xc /dev/null >/dev/null 2>&1; then echo "-fno-merge-constants"; fi)

# Build with -fno-strict-aliasing if gcc >= 3.1 is used
NO_STRICT_ALIASING=$(%{__cc} -dumpversion | awk -F "." '{ if (int($1)*100+int($2) >= 301) print "-fno-strict-aliasing" }')

# compiling with -g is too huge
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's/-g//'`

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

%if %{build_xprt}
#define XprtServer		YES
%else
#define XprtServer		NO
%endif

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


/* Only include these drivers if they've been enabled via RPM macros above */
#define XF86ExtraCardDrivers %{via_driver_name} %{voodoo_driver_name}

%ifarch %{ix86}
%if %{build_dev_dri_drivers}
#define BuildDevelDRIDrivers	YES
#define DevelDRIDrivers      ffb mach64 unichrome savage
%else
#define DevelDRIDrivers
%endif

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
%if %{build_dev_dri_drivers}
#define BuildDevelDRIDrivers    YES
#define DevelDRIDrivers      mach64
%else             
#define DevelDRIDrivers
%endif
                  
#define DriDrivers            gamma mga r128 radeon r200 \
                                tdfx DevelDRIDrivers

#define XF86CardDrivers mga glint s3virge sis savage \
                        trident chips tdfx fbdev ati \
			DevelDrivers vga nv \
			XF86OSCardDrivers XF86ExtraCardDrivers
%endif

#define ExtraXInputDrivers acecad evdev

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



%if %{havematroxhal}
(cd xc/programs/Xserver/hw/xfree86/drivers/mga/HALlib
gzip -cd %{SOURCE201} | tar xf - \
        mgadrivers-3.0-src/4.3.0/drivers/src/HALlib/mgaHALlib.a \
        mgadrivers-3.0-src/4.3.0/drivers/src/HALlib/binding.h
mv mgadrivers-3.0-src/4.3.0/drivers/src/HALlib/mgaHALlib.a .
mv mgadrivers-3.0-src/4.3.0/drivers/src/HALlib/binding.h .
rm -rf mgadrivers-3.0-src
)
cp -p xc/programs/Xserver/hw/xfree86/drivers/mga/HALlib/binding.h \
        xc/programs/Xserver/hw/xfree86/drivers/mga
%endif

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
%if %{build_xprt}
install -m 755  %{buildroot}/etc/init.d/xprint %{buildroot}/etc/rc.d/init.d/xprint
%endif
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

%if ! %{build_xprt}
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
%endif
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

%triggerpostun 75dpi-fonts -- XFree86-75dpi-fonts
/usr/sbin/chkfontpath -q -a /usr/X11R6/lib/X11/fonts/75dpi:unscaled

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

%triggerpostun 100dpi-fonts -- XFree86-100dpi-fonts
/usr/sbin/chkfontpath -q -a /usr/X11R6/lib/X11/fonts/100dpi:unscaled

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
%_pre_useradd xfs /etc/X11/fs /bin/false

# for msec high security levels
%_pre_groupadd xgrp xfs


%post xfs
# as we don't overwrite the config file, we may need to add those paths
# (2=update)
if [ "$1" -gt 1 ]; then
	for i in /usr/X11R6/lib/X11/fonts/drakfont \
			/usr/X11R6/lib/X11/fonts/pcf_drakfont:unscaled \
			/usr/X11R6/lib/X11/fonts/TTF
	do
		if ls `dirname $i`/`basename $i :unscaled`/*.* >/dev/null 2>/dev/null
		then
			if ! grep "$i" /etc/X11/fs/config >/dev/null 2>/dev/null ; then
				/usr/sbin/chkfontpath -q -a "$i"
			fi
		else
			if grep "$i" /etc/X11/fs/config >/dev/null 2>/dev/null ; then
				/usr/sbin/chkfontpath -q -r "$i"
			fi
		fi
	done
fi
%_post_service xfs

# handle init sequence change
if [ -f /etc/rc5.d/S90xfs ] && grep -q 'chkconfig: 2345 20 10' /etc/init.d/xfs; then
	/sbin/chkconfig --add xfs
fi

%preun xfs
%_preun_service xfs

%postun xfs
%_postun_userdel xfs

%triggerpostun xfs -- XFree86-xfs
%_post_service xfs
if [ ! -f /var/lock/subsys/xfs ]
then
  /sbin/service xfs start
fi

%post server

if [ $1 -gt 1 ]; then
  if [ -r /etc/X11/XF86Config-4 ] && grep -q 'Option.*"XkbOptions".*grp:' /etc/X11/XF86Config-4; then
    perl -pi -e 's/^(\s*Option\s*"XkbLayout"\s*)"([^,]*)"/$1"us,$2"/' /etc/X11/XF86Config-4
  fi
fi
if [ -r /etc/X11/XF86Config-4 ] && [ ! -e /etc/X11/xorg.conf ]; then
  ln -s XF86Config-4 /etc/X11/xorg.conf
fi

perl -pi -e 's/^(\s*Driver\s*)"Keyboard"/$1"kbd"/' /etc/X11/xorg.conf

%triggerpostun server -- XFree86-server
rm -f /etc/X11/X
ln -s ../../usr/X11R6/bin/Xorg /etc/X11/X


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files server -f modules.list
%defattr(-,root,root,-)
#doc /usr/X11R6/lib/X11/xorg.conf.eg
#doc /usr/X11R6/lib/X11/XF86Config.indy
/usr/X11R6/bin/Xorg
%if %build_compat
/usr/X11R6/bin/XFree86
%endif
%dir %{x11shlibdir}/modules
#dir #{x11shlibdir}/modules/codeconv
%dir %{x11shlibdir}/modules/dri
%dir %{x11shlibdir}/modules/drivers
%dir %{x11shlibdir}/modules/extensions
%dir %{x11shlibdir}/modules/fonts
%dir %{x11shlibdir}/modules/input
%dir %{x11shlibdir}/modules/linux


%files
%defattr(-,root,root,-)
%docdir /usr/X11R6/lib/X11/doc

%dir /usr/X11R6/lib/X11
%dir /etc/X11
%dir /etc/X11/rstart
/etc/X11/rstart/commands
#%dir /etc/X11/rstart/commands/x11r6
/etc/X11/rstart/contexts
/etc/X11/rstart/rstartd.real
%dir /usr/X11R6/lib/X11/etc
%dir /usr/X11R6/lib/X11/fonts
%dir /usr/X11R6/lib/X11/xserver
%dir /usr/X11R6/man
%dir /usr/X11R6/man/man*

%config(noreplace) /etc/X11/xkb
%dir /etc/X11/twm
%dir /etc/X11/xdm
%dir %attr(0700,root,root) /etc/X11/xdm/authdir
%dir /etc/X11/xsm
/etc/X11/xdm/chooser
%dir /var/lib/xdm

#%config /etc/rc.d/init.d/xdm
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
/usr/X11R6/lib/X11/locale/*
%exclude %dir /usr/X11R6/lib/X11/locale/%{_lib}
%exclude %dir /usr/X11R6/lib/X11/locale/%{_lib}/common
%exclude /usr/X11R6/lib/X11/locale/%{_lib}/common/*
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

/etc/X11/xserver/SecurityPolicy
/usr/X11R6/lib/X11/xserver/SecurityPolicy
#/usr/X11R6/lib/X11/xorg.conf
/usr/X11R6/lib/X11/rstart/rstartd.real
%config(noreplace) /etc/X11/rstart/config

/usr/X11R6/lib/X11/rstart
#/usr/X11R6/lib/X11/rstart/commands/x11r6/@List
#/usr/X11R6/lib/X11/rstart/commands/x11r6/LoadMonitor
#/usr/X11R6/lib/X11/rstart/commands/x11r6/Terminal
#/usr/X11R6/lib/X11/rstart/commands/@List
#/usr/X11R6/lib/X11/rstart/commands/ListContexts
#/usr/X11R6/lib/X11/rstart/commands/ListGenericCommands
#/usr/X11R6/lib/X11/rstart/contexts/@List
#/usr/X11R6/lib/X11/rstart/contexts/default
#/usr/X11R6/lib/X11/rstart/contexts/x11r6
/usr/X11R6/lib/X11/x11perfcomp
/usr/X11R6/lib/X11/doc
/usr/X11R6/lib/X11/etc/sun.termcap
/usr/X11R6/lib/X11/etc/sun.terminfo
/usr/X11R6/lib/X11/etc/xterm.termcap
/usr/X11R6/lib/X11/etc/xterm.terminfo
/usr/X11R6/lib/X11/etc/xmodmap.std
/usr/X11R6/lib/X11/etc/Xinstall.sh
/usr/X11R6/lib/X11/getconfig
/usr/X11R6/lib/X11/lbxproxy
/usr/X11R6/lib/X11/proxymngr
/usr/X11R6/lib/X11/Xcms.txt
/usr/X11R6/lib/X11/app-defaults

%attr(4711,root,root)		/usr/X11R6/bin/Xwrapper
/usr/X11R6/bin/X
#/usr/X11R6/bin/Xprt
/usr/X11R6/bin/lbxproxy
/usr/X11R6/bin/proxymngr
/usr/X11R6/bin/rstartd
/usr/X11R6/bin/xfindproxy
/usr/X11R6/bin/xfwp
/usr/X11R6/bin/xrx
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
/usr/X11R6/bin/luit
/usr/X11R6/bin/mkfontdir
/usr/X11R6/bin/showrgb
/usr/X11R6/bin/rstart
/usr/X11R6/bin/smproxy
/usr/X11R6/bin/twm
/usr/X11R6/bin/x11perf
/usr/X11R6/bin/x11perfcomp
/usr/X11R6/bin/Xmark
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
/usr/X11R6/bin/xmore
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
/usr/X11R6/bin/xorgcfg
%if %build_compat
/usr/X11R6/bin/xf86cfg
%endif
/usr/X11R6/bin/xdriinfo
#/usr/X11R6/bin/fonttosfnt
/usr/X11R6/bin/getconfig
/usr/X11R6/bin/getconfig.pl
%ifnarch ppc sparc
/usr/X11R6/bin/inb
/usr/X11R6/bin/inl
/usr/X11R6/bin/inw
/usr/X11R6/bin/outb
/usr/X11R6/bin/outl
/usr/X11R6/bin/outw
%endif

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
%multiarch %{multiarch_x11bindir}/xcursor-config
/usr/X11R6/bin/xcursorgen
/usr/X11R6/bin/xfsinfo
/usr/X11R6/bin/xmh
/usr/X11R6/bin/xrandr
%if ! %{with_new_fontconfig_Xft}
/usr/X11R6/bin/xftcache
%endif
#%{_iconsdir}/*.*
#%{_iconsdir}/*/*

%ifarch %{ix86} alpha sparc ppc x86_64
#/usr/X11R6/bin/reconfig
%if %build_compat
/usr/X11R6/bin/xf86config
%endif
/usr/X11R6/bin/xorgconfig
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
/usr/X11R6/man/man1/xrx.1x*
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
/usr/X11R6/man/man1/luit.1x*
/usr/X11R6/man/man1/mkfontdir.1x*
/usr/X11R6/man/man1/showrgb.1x*
/usr/X11R6/man/man1/rstart.1x*
/usr/X11R6/man/man1/rstartd.1x*
/usr/X11R6/man/man1/smproxy.1x*
/usr/X11R6/man/man1/twm.1x*
/usr/X11R6/man/man1/x11perf.1x*
/usr/X11R6/man/man1/x11perfcomp.1x*
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
%exclude /usr/X11R6/man/man1/XDarwin.1x*
/usr/X11R6/man/man1/Xorg.1x*
/usr/X11R6/man/man1/xorgcfg.1x*
/usr/X11R6/man/man1/xdriinfo.1x.*
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
/usr/X11R6/man/man1/xmore.1x.*
/usr/X11R6/man/man1/bdftruncate.1x*
/usr/X11R6/man/man1/ccmakedep.1x*
/usr/X11R6/man/man1/cleanlinks.1x*
%exclude /usr/X11R6/man/man1/dumpkeymap.1x*
/usr/X11R6/man/man1/gccmakedep.1x*
/usr/X11R6/man/man1/gtf.1x*
/usr/X11R6/man/man1/mergelib.1x*
/usr/X11R6/man/man1/mkfontscale.1x*
/usr/X11R6/man/man1/mkhtmlindex.1x*
/usr/X11R6/man/man1/ucs2any.1x*
/usr/X11R6/man/man1/xcursorgen.1x*
/usr/X11R6/man/man1/xrandr.1x*

#/usr/X11R6/man/man1/fonttosfnt.1x*
/usr/X11R6/man/man1/getconfig.1x*
/usr/X11R6/man/man5/getconfig.5x*

/usr/X11R6/man/man5/xorg.conf.5x*
/usr/X11R6/man/man4/*
/usr/X11R6/man/man7/*

%ifarch %{ix86} alpha sparc ppc x86_64
#/usr/X11R6/man/man1/reconfig.1x*
/usr/X11R6/man/man1/xorgconfig.1x*
%endif

%if %{build_speedo_fonts}
%dir /usr/X11R6/lib/X11/fonts/Speedo
/usr/X11R6/lib/X11/fonts/Speedo/*.spd
%ghost /usr/X11R6/lib/X11/fonts/Speedo/fonts.dir
/usr/X11R6/lib/X11/fonts/Speedo/fonts.scale
/usr/X11R6/lib/X11/fonts/Speedo/encodings.dir
%endif

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
/usr/X11R6/lib/X11/fonts/misc/fonts.scale

# default scalable fonts
%dir /usr/share/fonts/otf/mdk
/usr/share/fonts/otf/mdk/*

/usr/X11R6/lib/X11/rgb.txt

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

%files xauth
%defattr(-,root,root,-)
/usr/X11R6/bin/xauth
#/usr/X11R6/bin/xauth_switch_to_sun-des-1
/usr/X11R6/man/man1/xauth.1x*

%files Xvfb
%defattr(-,root,root,-)
/usr/X11R6/bin/Xvfb
/usr/X11R6/man/man1/Xvfb.1x*

%files Xnest
%defattr(-,root,root,-)
/usr/X11R6/bin/Xnest
/usr/X11R6/man/man1/Xnest.1x*

%files Xdmx
%defattr(-,root,root,-)
/usr/X11R6/bin/Xdmx
/usr/X11R6/man/man1/Xdmx.1x.*
/usr/X11R6/man/man1/dmxtodmx.1x.*
/usr/X11R6/man/man1/vdltodmx.1x.*
/usr/X11R6/man/man1/xdmxconfig.1x.*

%if %{build_xprt}
%files Xprt
%defattr(-,root,root,-)
/usr/X11R6/bin/Xprt
/etc/X11/xserver/*
#/etc/X11/xserver/C
#/etc/X11/xserver/POSIX
#/etc/X11/xserver/README
%exclude /etc/X11/xserver/SecurityPolicy

/etc/X11/Xsession.d/92xprint-xpserverlist.sh
/etc/X11/xinit/xinitrc.d/92xprint-xpserverlist.sh

/etc/rc.d/init.d/xprint
/etc/profile.d/xprint.csh
/etc/profile.d/xprint.sh

#/usr/X11R6/bin/xpawhelloworld
/usr/X11R6/bin/xphelloworld
/usr/X11R6/bin/xplsprinters
/usr/X11R6/bin/xprehashprinterlist
/usr/X11R6/bin/xpsimplehelloworld
#/usr/X11R6/bin/xpxmhelloworld
/usr/X11R6/bin/xpxthelloworld

/usr/X11R6/man/man1/Xprt.1x.*
#/usr/X11R6/man/man1/xpawhelloworld.1x.*
/usr/X11R6/man/man1/xphelloworld.1x.*
/usr/X11R6/man/man1/xplsprinters.1x.*
/usr/X11R6/man/man1/xprehashprinterlist.1x.*
/usr/X11R6/man/man1/xpsimplehelloworld.1x.*
#/usr/X11R6/man/man1/xpxmhelloworld.1x.*
/usr/X11R6/man/man1/xpxthelloworld.1x.*
%endif

%files doc
%defattr(-,root,root,-)
%doc xc/doc/hardcopy/*

%files 75dpi-fonts
%defattr(-,root,root,-)
%dir /usr/X11R6/lib/X11/fonts/75dpi
/usr/X11R6/lib/X11/fonts/75dpi/*.gz
/usr/X11R6/lib/X11/fonts/75dpi/fonts.scale
/usr/X11R6/lib/X11/fonts/75dpi/fonts.alias
%ghost /usr/X11R6/lib/X11/fonts/75dpi/fonts.dir
/usr/X11R6/lib/X11/fonts/75dpi/encodings.dir

%files 100dpi-fonts
%defattr(-,root,root,-)
%dir /usr/X11R6/lib/X11/fonts/100dpi
/usr/X11R6/lib/X11/fonts/100dpi/*.gz
/usr/X11R6/lib/X11/fonts/100dpi/fonts.scale
/usr/X11R6/lib/X11/fonts/100dpi/fonts.alias
%ghost /usr/X11R6/lib/X11/fonts/100dpi/fonts.dir
/usr/X11R6/lib/X11/fonts/100dpi/encodings.dir

%files cyrillic-fonts
%defattr(-,root,root,-)
%dir /usr/X11R6/lib/X11/fonts/cyrillic
/usr/X11R6/lib/X11/fonts/cyrillic/*.gz
/usr/X11R6/lib/X11/fonts/cyrillic/fonts.scale
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
%config(noreplace) /etc/rc.d/init.d/xfs
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
* Fri Aug 19 2005 Vincent Danen <vdanen@annvix.org> 6.8.2-2avx
- remove /usr/X11R6/lib/X11/Cards (hwdata provides this)

* Thu Aug 10 2005 Vincent Danen <vdanen@annvix.org> 6.8.2-1avx
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
