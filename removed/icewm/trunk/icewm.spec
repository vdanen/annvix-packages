%define name	icewm
%define version	1.2.13
%define release 0.3.4avx

%define theirversion	1.2.13pre3
%define prefix		/usr/X11R6

Summary:	Light X11 Window Manager
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		Graphical desktop/Icewm
URL:		http://www.icewm.org/
Source:		http://download.sourceforge.net/icewm/icewm-%{theirversion}.tar.bz2
Source1:	opensls.xpm.bz2
Source2:	themes.tar.bz2
Source3:	%{name}.menu
Source4:	%{name}.menu-method
Source5:	%{name}-16.png.bz2
Source6:	%{name}-32.png.bz2
Source7:	%{name}-48.png.bz2
Source8:	%{name}-starticewm
Patch0:		%{name}-1.2.9-mdkconf.patch.bz2
Patch1:		%{name}-1.0.8-xcin_bindy.patch.bz2
Patch2:		%{name}-1.2.13pre3-defaultfont.patch.bz2
Patch3:		%{name}-1.2.10pre9-always-fontset.patch.bz2
Patch4:		%{name}-1.2.0-winoptions.patch.bz2
Patch7:		%{name}-1.2.0pre1-libsupc++.patch.bz2
Patch8:		%{name}-1.2.5-lib64.patch.bz2
Patch9:		%{name}-1.2.10pre11-default.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	XFree86, autoconf2.5, gettext, libpcap-devel, xpm-devel

Requires:	xterm

%description
Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.

This is the light version with minimal features.

%prep
%setup -q -n %name-%theirversion
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .defaultfont
%patch3 -p1 -b .fontset
%patch4 -p1 -b .winoptions
%patch7 -p1 -b .libsupc++
%patch8 -p1 -b .lib64
%patch9 -p1 -b .default
autoconf

#perl -pi -e "s|charset=952|charset=ISO-8895-2|" po/hu.po
#perl -pi -e "s|charset=iso8859-1|charset=ISO-8895-1|" po/fr.po
#perl -pi -e "s|icewm.xpm|opensls.xpm|" src/wmtaskbar.cc

%build
bzcat %{SOURCE1} > lib/taskbar/opensls.xpm

CXXFLAGS="$RPM_OPT_FLAGS" %configure --sysconfdir=/etc \
--disable-debug --enable-i18n --enable-nls --disable-guievents \
--without-gnome-menus --with-xpm --with-docdir=%{_docdir}
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install \
	BINDIR=$RPM_BUILD_ROOT%{prefix}/bin \
	LIBDIR=$RPM_BUILD_ROOT%{prefix}/lib/X11/%{name} \
	ETCDIR=$RPM_BUILD_ROOT/etc/X11/%{name} \
	DOCDIR=$RPM_BUILD_ROOT%{_datadir}/doc \
	CFGDIR=$RPM_BUILD_ROOT/etc/X11/X11 \
	LOCDIR=$RPM_BUILD_ROOT%{_datadir}/locale

install src/%{name} $RPM_BUILD_ROOT%{prefix}/bin/

#rm -rf $RPM_BUILD_ROOT%{prefix}/lib/X11/%{name}/themes
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib/X11/%{name}/
echo RPM_BUILD_DIR $RPM_BUILD_DIR
echo RPM_BUILD_DIR/name-version $RPM_BUILD_DIR/%{name}-%{theirversion}
bzcat %{SOURCE2}|tar x -C $RPM_BUILD_ROOT%{prefix}/lib/X11/%{name}/
chmod -R a+rX $RPM_BUILD_ROOT%{prefix}/lib/X11/%{name}

#don't ship the .xvpics
(cd %buildroot
find -name ".xvpics"|xargs rm -rf
)

# icon
mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}
bzcat %{SOURCE5} > $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
bzcat %{SOURCE6} > $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
bzcat %{SOURCE7} > $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

excludes_patt="\(themes/microGUI\|icons/\(app_\|xterm_\)\)"
(cd $RPM_BUILD_ROOT%{prefix} ; find lib/X11/%{name}/{icons,themes} ! -type d -printf "%{prefix}/%%p\n") | grep -v "$excludes_patt" > other.list
(cd $RPM_BUILD_ROOT%{prefix} ; find lib/X11/%{name}/{icons,themes}   -type d -printf "%%%%dir %{prefix}/%%p\n") | grep -v "$excludes_patt" >> other.list

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{prefix}/bin/genpref
find  $RPM_BUILD_ROOT%{prefix}/lib/X11/%{name}/themes -regex ".*$excludes_patt.*" | grep -v microGUI | xargs rm -f

# wmsession support
mkdir -p $RPM_BUILD_ROOT/etc/X11/wmsession.d/
cat << EOF > $RPM_BUILD_ROOT/etc/X11/wmsession.d/07IceWM
NAME=IceWM
ICON=icewm-wmsession.xpm
EXEC=/usr/X11R6/bin/starticewm
DESC=Lightweight desktop environment
SCRIPT:
exec /usr/X11R6/bin/starticewm
EOF

install -m 755 %{SOURCE8} $RPM_BUILD_ROOT%{prefix}/bin/starticewm

#
# Auto detect the lang files.
#
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/locale
%find_lang %{name}
perl -pi -e "s|^\s*$||" %{name}.lang
cat %{name}.lang >> other.list

# Dadou - 1.0.9-0.pre1.5mdk - Change default background color for MDK color
perl -pi -e "s#\# DesktopBackgroundColor=.*#DesktopBackgroundColor=\"\"#" %buildroot/%prefix/lib/X11/icewm/preferences

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%{__rm} -rf /usr/X11R6/lib/X11/icewm/themes/tile

%files -f other.list
%defattr(-,root,root)
%doc README COPYING AUTHORS CHANGES TODO BUGS doc/*.html
%dir %{prefix}/lib/X11/%{name}
%dir %{prefix}/lib/X11/%{name}/themes
%dir %{prefix}/lib/X11/%{name}/icons
%dir %{prefix}/lib/X11/%{name}/ledclock
%dir %{prefix}/lib/X11/%{name}/taskbar
%dir %{prefix}/lib/X11/%{name}/mailbox
%config(noreplace) /etc/X11/wmsession.d/*
%{prefix}/bin/starticewm
%{prefix}/bin/icesh
%{prefix}/bin/icehelp
%{prefix}/bin/icewm
%{prefix}/bin/icewm-session
%{prefix}/bin/icewmbg
%{prefix}/bin/icewmhint
%{prefix}/bin/icewmtray
%{prefix}/lib/X11/%{name}/mailbox/*
%{prefix}/lib/X11/%{name}/taskbar/*
%{prefix}/lib/X11/%{name}/ledclock/*
%{prefix}/lib/X11/%{name}/icons/app*
%{prefix}/lib/X11/%{name}/icons/xterm*
%{prefix}/lib/X11/%{name}/keys
%{prefix}/lib/X11/%{name}/preferences
%{prefix}/lib/X11/%{name}/toolbar
%{prefix}/lib/X11/%{name}/winoptions
%{prefix}/lib/X11/%{name}/menu
#%{prefix}/lib/X11/%{name}/programs
%{prefix}/lib/X11/%{name}/themes/microGUI
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%changelog
* Thu Jun 24 2004 Vincent Danen <vdanen@annvix.org> 1.2.13-0.3.4avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.2.13-0.3.3sls
- minor spec cleanups
- update menu to include xterm
- we ship one GUI app: xterm, so let's Require it (can't do much without it)
- make an OpenSLS xpm for the start button

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 1.2.13-0.3.2sls
- OpenSLS build
- tidy spec
- make light version by default; no standard or gnome version
- don't require mandrake_desk or menu
- remove menu-related directories/files
- remove calls to %%make_session

* Tue Sep 16 2003 Florin <florin@mandrakesoft.com> 1.2.13-0.3.1mdk
- 1.2.13pre3
- update the terminal command in the menu-method
- update the defaultfont patch

* Wed Sep 10 2003 Florin <florin@mandrakesoft.com> 1.2.13-0.1.3mdk
- fix the updates alternatives

* Thu Sep 04 2003 Florin <florin@mandrakesoft.com> 1.2.13-0.1.2mdk
- buildrequires libpcap-devel instead of libpcap0-devel

* Tue Sep 02 2003 Florin <florin@mandrakesoft.com> 1.2.13-0.1.1mdk
- 1.2.13pre1

* Thu Aug 28 2003 Florin <florin@mandrakesoft.com> 1.2.12-1mdk
- 1.2.12

* Wed Aug 20 2003 Florin <florin@mandrakesoft.com> 1.2.10-0.11.1mdk
- 1.2.10pre11
- update the default patch

* Tue Aug 19 2003 Florin <florin@mandrakesoft.com> 1.2.10-0.9.1mdk
- 1.2.10pre9
- update the defaultfont, always-fontset patchces

* Tue Aug 19 2003 Florin <florin@mandrakesoft.com> 1.2.9-3mdk
- add the default font patch instead of the CLE patch

* Fri Jul 04 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.2.9-2mdk
- put / at the end of the url after strong wishes from David Walser:)

* Thu Jul 03 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.2.9-1mdk
- 1.2.9
- use double %%'s in changelog to avoid macros gettin expanded
- updated url
- rm -rf $RPM_BUILD_ROOT at the beginning of %%install
- regenerated P0
- dropped P5
- remove the programs file
- drop FAQ* from %%doc
- add the icewmtray file

* Thu Apr 03 2003 Florin <florin@mandrakesoft.com> 1.2.7-1mdk
- 1.2.7
- update the mdkconf patch

* Fri Jan 24 2003 Florin <florin@mandrakesoft.com> 1.2.6-1mdk
- 1.2.6

* Tue Jan 21 2003 Florin <florin@mandrakesoft.com> 1.2.5-2mdk
- better use of the default theme (thx piwel for pointing this out)

* Thu Jan 09 2003 Florin <florin@mandrakesoft.com> 1.2.5-1mdk
- 1.2.5
- update the mdkconf and lib64 patches
- add the programs file

* Sat Nov 30 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.2-2mdk
- Use %%find_lang macro, remove unpackaged files
- Patch8: libdatadir shall remain to %%{_prefix}/lib/X11/icewm

* Wed Oct 16 2002 Florin <florin@mandrakesoft.com> 1.2.2-1mdk
- 1.2.2
- update the mdkconf, always-fontset patches

* Tue Sep 10 2002 Florin <florin@mandrakesoft.com> 1.2.0-5mdk
- new themes, new default theme (microGUI)
- better keys file
- keep color from Xsession instead of forcing them (Flepied)

* Thu Sep 05 2002 Florin <florin@mandrakesoft.com> 1.2.0-4mdk
- fix the mozilla icon in toolbar

* Sat Aug 03 2002 Stefan van der Eijk <stefan@eijk.nu> 1.2.0-3mdk
- BuildRequires autoconf2.5

* Thu Jul 25 2002 Daouda LO <daouda@mandrakesoft.com> 1.2.0-2mdk
- remove .xvpics dir.

* Sat Jul 20 2002 Daouda LO <daouda@mandrakesoft.com> 1.2.0-1mdk
- final release 1.2.0
- zh_CN patch merged upstream
- Patch regenerations

* Mon Jul  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.0-0.pre1.3mdk
- Patch7: Link with libsupc++ to get C++ memory allocators

* Mon Jul 01 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.0-0.pre1.2mdk
- Fix zh_CN extra %% character. Doesn't show up on our own ix86 box but it 
  barfs on the Alpha. Fix applied for all architectures.

* Fri May 24 2002 Florin <florin@mandrakesoft.com> 1.2.0-0.pre1.1mdk
- 1.2.0pre1
- add the YIMP patch
- update the winoptions and the mdkconf patches

* Wed Feb 20 2002 Florin <florin@mandrakesoft.com> 1.0.9-10mdk
- fix a typo in update alternatives

* Wed Feb 20 2002 Florin <florin@mandrakesoft.com> 1.0.9-9mdk
- rm bluePlastic theme from the icewm package
- add some more winoptions (thx to D.Walser)

* Tue Feb 19 2002 Florin <florin@mandrakesoft.com> 1.0.9-8mdk
- make sure we use only png pictures

* Tue Feb 19 2002 Florin <florin@mandrakesoft.com> 1.0.9-7mdk
- update the mdkconf patch
- new colour scheme in icewm-starticewm
- add the winoptions patch
- stop removing the original themes
- update the taskbar icons names
- convert the xpm images into png 

* Wed Jan 30 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.9-6mdk
- Fix CJK fontset (this SUCKS!!)

* Fri Jan 25 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.0.9-5mdk
- rebuilt to have the correct dependency on libfreetype.

* Mon Jan 21 2002 Stefan van der Eijk <stefan@eijk.nu> 1.0.9-4mdk
- BuildRequires

* Thu Dec 13 2001 Florin <florin@mandrakesoft.com> 1.0.9-3mdk
- 1.0.9-2 sources

* Mon Oct 15 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.9-2mdk
- libpng3

* Tue Oct 09 2001 Florin <florin@mandrakesoft.com> 1.0.9-1mdk
- 1.0.9
- merge with the original spec

* Mon Oct 1 2001 Geoff <snaitlalk@mandrakesoft.com> 1.0.9-0.pre1.17mdk
- Remove mutt Requires.

* Tue Sep 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.9-0.pre1.16mdk
- Add gnome-libs-devel and xpm-devel as BuildRequires.
- Add mutt as a Requires. The mailer on the taskbar is non-configurable, it
  defaults to pine in the stock version but it's been patched to use mutt.
  
* Mon Sep 24 2001 Florin <florin@mandrakesoft.com> 1.0.9-0.pre1.15mdk
- increase the 63 char limit in menus to 128

* Sun Sep 23 2001 Florin <florin@mandrakesoft.com> 1.0.9-0.pre1.14mdk
- use mutt as default mailer instead of pine

* Sat Sep 22 2001 Florin <florin@mandrakesoft.com> 1.0.9-0.pre1.13mdk
- remove the useless update-menu for standard and gnome versions (thx F.Lepied)
- enable-i18n and enable-nls for icewm-light (G.Lee's idea)
- use xvt for the terminal and terminals_section.xpm icon (also G.Lee's idea)

* Fri Sep 21 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.0.9-0.pre1.12mdk
- fixed fontsets

* Thu Sep 20 2001 Florin <florin@mandrakesoft.com> 1.0.9-0.pre1.11mdk
- starticewm uses new colour
- back to icewm again instead of standard one (it breaks the update)
- remove the experimental stuff in icewm-gnome
- remove the -fn parameter in the default terminal entry (menu-method) 

* Tue Sep 11 2001 Florin <florin@mandrakesoft.com> 1.0.9-0.pre1.10mdk
- add the %%{release} in require to make the upgrades work

* Mon Sep 10 2001 Florin <florin@mandrakesoft.com> 1.0.9-0.pre1.9mdk
- make things work again (it's been a while)
- use the %%{name} where possible
- modify the 3 configure sections :light, gnome, standard
- fix the fr and hu po files
- modify the update alternatives sections
- add several interfaces in preferences
- merge the themes added by yves with the others
- fix the menu entries
- the main binary is now called icewm-standard
- update the icewm-menu.method (the xterm xpm)
- bring back the nice default mandrake xpm on the taskbar
- fix the mdkconf patch
- remove the links from the post icewm-gnome and icewm-standard sections

* Wed Sep 05 2001 Stefan van der Eijk <stefan@eijk.nu> 1.0.9-0.pre1.8mdk
- fix BR

* Mon Sep 03 2001 Florin <florin@mandrakesoft.com> 1.0.9-0.pre1.7mdk
- bring back the ja, pt and chinese po files
- add the po patch

* Fri Aug 31 2001 Yves Duret <yduret@mandrakesoft.com> 1.0.9-0.pre1.6mdk
- readd wmsession file.

* Fri Aug 31 2001 David BAUDENS <baudens@mandrakesoft.com> 1.0.9-0.pre1.5mdk
- Use colors from 8.1 graphical charter

* Sat Aug 25 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.0.9-0.pre1.4mdk
- use /etc/X11/icewm instead of /etc/X11/X11/icewm

* Fri Aug 10 2001 Florin <florin@mandrakesoft.com> 1.0.9-0.pre1.3mdk
- add /bin/sh in requires

* Wed Aug 08 2001 Yves Duret <yduret@mandrakesoft.com> 1.0.9-0.pre1.2mdk
- moved gnome support to icewm-gnome package
- icewm does not more requires gnome 

* Tue Aug 07 2001 Yves Duret <yduret@mandrakesoft.com> 1.0.9-0.pre1.1mdk
- version 1.0.9pre1
- removed patch{1,5,7,9,13} merged upstream
- removed patch{2,3,4,6,12} useless (not applied btw)
- adapted zh patch{10,11}
- do not mess mdkconfig and xcinintegration in patch10
- temporaly remove icesound (build broken)
- temporaly remove ja, pt_BR, zh_TW.Big5 l10n (broken)
- added some cool gradient/shapped themes (source9)

* Tue Jul 3 2001 Florin <florin@mandrakesoft.com> 1.0.8-3mdk
- add an exec in the starticewm to avoid a useless remaining process

* Sun Jul 01 2001 Stefan van der Eijk <stefan@eijk.nu> 1.0.8-2mdk
- BuildRequires:        db1-devel
- BuildRequires:        gnome-libs-devel
- BuildRequires:        libjpeg-devel
- BuildRequires:        libpng-devel
- BuildRequires:        libtiff-devel
- BuildRequires:        libungif-devel
- BuildRequires:        xpm-devel

* Thu May 10 2001 Florin <florin@mandrakesoft.com> 1.0.8-1mdk
- 1.0.8-6
- update all the patches

* Sun Apr 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.7-5mdk
- Add patch to have the option GNOMEShowMenu to display or not display
  Gnome Menus (chmoufeature).
  
* Thu Apr 11 2001 Florin <florin@mandrakesoft.com> 1.0.7-4mdk
- fix the update-alternatives (thx to Pixel)
- clean the uninstalling by adding directories in files 
- fix the rm line in post

* Thu Apr 11 2001 Florin <florin@mandrakesoft.com> 1.0.7-3mdk
- fix some postun typo bug (found my Chmouel - thanks, man)
- add the locale/*mo files


* Tue Mar 27 2001 Florin <florin@mandrakesoft.com> 1.0.7-2mdk
- 1.0.7-7
- added some configure options for the icewm package
- update-alternatives are now auto
- update all the patches
- add the includes patch

* Sun Mar 18 2001 Pixel <pixel@mandrakesoft.com> 1.0.6-4mdk
- don't enable-lite which gives a broken icewm-light

* Fri Mar  2 2001 Andrew Lee <andrew@linux.org.tw> 1.0.6-3mdk
- refine fontset
- add mozilla on toolbar
- fix bindkey conflict xcin
- Geoffrey Lee <snailtalk@mandrakesoft.com>
- Fix the build of icewm (Yuck).

* Mon Feb 19 2001 Florin Grad <florin@mandrakesoft.com> 1.0.6-2mdk
- the 1.0.6-4 release (go figure the way they give the source names)

* Fri Feb  2 2001 Etienne Faure  <etienne@mandrakesoft.com> 1.0.6-1mdk
- 1.0.6
- fixed menu entry

* Mon Dec 18 2000 Florin Grad <florin@mandrakesoft.com> 1.0.5-1mdk
- 1.0.5
- some compilation fixes: --enable-lite, --enable-guievents 

* Fri Oct 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.4-14mdk
- Fix compilation for gcc-2.96.

* Tue Oct 03 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-13mdk
- the isdn patch gives coredumps again

* Mon Oct 02 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-12mdk
- added the isdn patch (thanks to Mathias Hasselmann)
- added the logout patch (thanks again)

* Wed Sep 27 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-11mdk
- fix the theme

* Tue Sep 26 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-10mdk
- the isdn creates some conflicts so I take it away for the moment

* Tue Sep 26 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-9mdk
- added the isdn status patch
- modify the menu method for the default icon
- "new" lighter default theme

* Thu Sep 21 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-8mdk
- transparent icons
- added large icon
- fixed some dangling symlinks

* Tue Sep 19 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-7mdk
- modified the icewm-menu-method for the kde icons (locolor and hicolor ones) and added to iconPath
- added the window-transient patch
- added the tooltips-show-forever patch 
- added the non-latin(1)-(lang)fonts patch 
- added the better-ppp-status patch
- eth0 is now as default in src/default.h

* Wed Sep 6 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-6mdk
- replace rxvt with xterm in menus and shortcuts (priority package is higher)

* Tue Sep 5 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-5mdk
- adding some new themes and fix the terminal command in the task bar
- adding the alternatives method 
- adding a shortcut to rxvt Alt+Ctrl+t

* Mon Sep 4 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-4mdk
- replaced /usr/X11/bin/xsetroot with /usr/X11R6/bin/xsetroot

* Thu Aug 31 2000 David BAUDENS <baudens@mandrakesoft.com> 1.0.4-3mdk
- New wmsession support

* Tue Aug 22 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.4-2mdk
- BM
- more macros
- config(noreplace) the menu-method
- fixed %%install section which was not working anymore

* Tue Jun 13 2000 Florin Grad <florin@mandrakesoft.com> 1.0.4-1mdk
- 1.0.4
- comment the gnome-patch

* Tue May  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.3-11mdk
- added an xterm entry in toplevel menu.

* Sun May  7 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.3-10mdk
- default panel: rxvt -> xterm because xterm is always installed, not
  rxvt

* Sat Apr 29 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.3-9mdk
- added specific menu entries /IceWM/.. with help of Frederic Lepied

* Fri Apr 28 2000 dam's <damien@mandrakesoft.com> 1.0.3-8mdk
- added fndSession call

* Fri Apr 28 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.3-7mdk
- re-fixed menu-method: now prints out the submenu icons
- added icons for the menu entry

* Thu Apr 20 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.3-6mdk
- fixed icons in menu-method: now takes the mini icon if present
  before trying to take the main icon

* Wed Apr 19 2000 dam's <damien@mandrakesoft.com> 1.0.3-5mdk
- Changed iceons.

* Tue Apr 18 2000 dam's <damien@mandrakesoft.com> 1.0.3-4mdk
- Change taskbar icon.

* Fri Apr  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.3-3mdk
- Apply mdkconf patch.

* Fri Apr 07 2000 Daouda Lo <daouda@mandrakesoft.com> 1.0.3-2mdk
- remove the hardcoded gnome menu entry
- some minor fixes to spec (clean up , add -q to setup ...)

* Wed Apr  5 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.3-1mdk
- 1.0.3

* Sun Apr  2 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.2-4mdk
- added support for menu i18n

* Wed Feb 23 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.2-3mdk
- added a prereq on menu.

* Mon Feb 21 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.2-2mdk
- added menu support.

* Sun Feb 20 2000 Pixel <pixel@mandrakesoft.com> 1.0.2-1mdk
- new version
- clean up (nice spec-helper :)

* Tue Jan 18 2000 Florin Grad <florin@mandrakesoft.com>
- 1.0.1
- obviously icewm is Y2K compliant ;)

* Thu Dec 30 1999 Frederic Lepied <flepied@mandrakesoft.com> 1.0.0-2mdk
- fix perms for /usr/X11R6/lib/X11/icewm/themes/IceGTK.

* Tue Dec 28 1999 Pixel <pixel@mandrakesoft.com>
- 1.0.0

* Tue Dec 21 1999 Florin Grad <florin@mandrakesoft.com>
- add the kde2ice python script
- with-gnome-menu
- remove the background picture
- update of the Mandrake icons
- modify the IconPath in default.c 

* Mon Dec 13 1999 Florin Grad <florin@mandrakesoft.com>
- add FAQ-french
- add rpmdrake in the Mandrake menu
- use a 1024x768 background image instead of a 800x600 one
- 0.9.54

* Sun Nov 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Split icewm in multiple package icewm-light and icewm-gnome(default).

* Fri Nov 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- DesktopBackgoundColor=1 by default.

* Wed Nov 17 1999 Florin Grad <florin@mandrakesoft.com>
- Add a new default background.
- A nice theme collection.
- New default theme.
- New associative icons.
- C-x C-t between xterm and rxvt in menu.

* Wed Nov 17 1999 Damien Krotkine <damien@mandrakesoft.com>
- 0.9.50

* Wed Aug 25 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 0.9.48

* Mon Aug 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.9.47
- Remove ShowNetStatus by default.

* Fri Aug 13 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 0.9.46
- hope the date (Friday 13th) doesn't affect the stability ;)

* Wed Aug 11 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 0.9.44
- fix compilation with gcc 2.95

* Tue Jul 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add patch to have a mandrake menus.

* Tue Jul 20 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- add french description from Gregus <gregus@etudiant.net>

* Fri Jul 16 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Reinserting the mandrake pixmaps.

* Tue Jul 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Patch to have by default a mandrake background.

* Wed Jul 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 0.9.43 :
        - fixes to configure
	- fixed some focusing problems
        - some new netscape icons added
        - fixes to shell command execution (no longer crashes on restart wm)
        - improvement in shaped windows handling
        - allow relative pathname in background image specification
        - made window stacking not interfere with DND icons
        - fix: minimize action in window list is no longer a toggle
        - detect both Alt_L and Alt_R keysf for Alt modifier.
        - configure event coalescing is now done to improve performance

* Tue May 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Reinsertion of mandrake xpm.

* Sun May 23 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 0.9.41
- Recreated Chmouel's patches for 0.9.41

* Sat May 22 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 0.9.39, hoping to fix segfaults.
- disable debug

* Mon Apr 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adaptations.
- Build with Gnome Support
- Handle RPM_OPT_FLAGS.
- Add Mandrake Icons.
- Add patch to make Mandrake Icons by default.
- Add patch to have GTK theme by default instead of Win95 look (BEURK).


