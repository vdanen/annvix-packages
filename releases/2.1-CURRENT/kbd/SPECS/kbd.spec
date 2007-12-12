#
# spec file for package kbd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		kbd
%define version		1.12
%define release		%_revrel

%define kbddir		/usr/lib/kbd
%define keymaps_ver	20071113

Summary:	Keyboard and console utilities for Linux
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Terminals
URL:		http://www.zsh.org
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kbd/kbd-%{version}.tar.bz2
Source1:	ftp://ftp.kernel.org/pub/linux/utils/kbd/kbd-%{version}.tar.bz2.sign
Source2:	ucwfonts.tar.bz2
Source3:	ftp://ftp.linux-france.org/pub/macintosh/kbd-mac-fr-4.1.tar.gz
Source4:	keytable.init
Source5:	kbd-mdv-keymaps-%{keymaps_ver}.tar.bz2
Source6:	configure_keyboard.sh
Source7:	setsysfont
# mandriva keyboard updates
Patch0: 	kbd-1.12-mandriva.patch
# tilde with twosuperior in french keyboard
Patch1: 	kbd-1.12-tilde_twosuperior_french_kbd.patch
# thai support, I tried to convert it from console-tools package
# (support added by Pablo), using also updated thay_ksym patch from
# debian and the following patches from:
# http://linux.thai.net/~thep/th-console/console-tools/console-tools-thai_ksym.patch
# http://linux.thai.net/~thep/th-console/console-data/console-data-thai_orig-1999.08.29.patch
Patch3: 	kbd-1.12-thai_ksym_deb.patch
Patch4: 	kbd-1.12-data_thai.patch
# loadkeys only works as root, and we use unicode_start in configure_keyboard.sh
Patch5: 	kbd-1.12-unicode_start_no_loadkeys.patch
# Don't allow unicode_{start,stop} to run if we aren't in a linux vt, as
# it doesn't make sense and causes bugs if we run it under X
Patch6: 	kbd-1.12-unicode_only_in_linux_vt.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel

Conflicts:	util-linux < 2.13
Obsoletes:	console-tools <= 0.2.3-7863avx
Provides:	console-tools = %{version}-%{release}

%description
This package contains utilities to load console fonts and keyboard maps.
It also includes a number of different fonts and keyboard maps.


%prep
%setup -q -a 2
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

mkdir mac_frnew
pushd mac_frnew
    tar -zxf %{_sourcedir}/kbd-mac-fr-4.1.tar.gz
    gunzip mac-fr-ext_new.kmap.gz
    mv mac-fr-ext_new.kmap ../data/keymaps/mac/all/mac-fr-ext_new.map
popd
rm -rf mac_frnew

pushd data
    tar -jxf %{_sourcedir}/kbd-mdv-keymaps-%{keymaps_ver}.tar.bz2
    cp keymaps/i386/include/delete.inc keymaps/i386/include/delete.map
popd


%build
./configure \
    --datadir=%{kbddir} \
    --mandir=%{_mandir}

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# keep some keymap/consolefonts compatibility with console-tools
ln -s fr-latin9.map.gz %{buildroot}%kbddir/keymaps/i386/azerty/fr-latin0.map.gz
ln -s us-acentos.map.gz %{buildroot}%kbddir/keymaps/i386/qwerty/us-intl.map.gz
ln -s mac-us.map.gz %{buildroot}%kbddir/keymaps/mac/all/mac-br-abnt2.map.gz
ln -s mac-us.map.gz %{buildroot}%kbddir/keymaps/mac/all/mac-gr.map.gz
ln -s mac-us.map.gz %{buildroot}%kbddir/keymaps/mac/all/mac-no-latin1.map.gz
ln -s mac-us.map.gz %{buildroot}%kbddir/keymaps/mac/all/mac-cz-us-qwertz.map.gz
ln -s mac-us.map.gz %{buildroot}%kbddir/keymaps/mac/all/mac-hu.map.gz
ln -s mac-us.map.gz %{buildroot}%kbddir/keymaps/mac/all/mac-Pl02.map.gz
ln -s mac-us.map.gz %{buildroot}%kbddir/keymaps/mac/all/mac-ru1.map.gz
ln -s mac-us.map.gz %{buildroot}%kbddir/keymaps/mac/all/mac-jp106.map.gz
ln -s iso07u-16.psfu.gz %{buildroot}%kbddir/consolefonts/iso07.f16.psfu.gz
ln -s lat2-16.psfu.gz %{buildroot}%kbddir/consolefonts/lat2-sun16.psfu.gz
ln -s lat5-16.psfu.gz %{buildroot}%kbddir/consolefonts/lat5u-16.psfu.gz

# keep further compatibility with console-tools
for toggle_file in alt_shift_toggle caps_toggle ctrl_alt_toggle \
    ctrl_shift_toggle lwin_toggle menu_toggle rwin_toggle toggle
do
    cp %{buildroot}%kbddir/keymaps/i386/include/$toggle_file.inc \
        %{buildroot}%kbddir/keymaps/i386/include/$toggle_file.map
    gzip %{buildroot}%kbddir/keymaps/i386/include/$toggle_file.map
done

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 0755 %{_sourcedir}/configure_keyboard.sh \
    %{buildroot}/%{_sysconfdir}/profile.d/configure_keyboard.sh

mkdir -p %{buildroot}%{_initrddir}
install -m 0755 %{_sourcedir}/keytable.init %{buildroot}%{_initrddir}/keytable

# some scripts expects setfont and unicode_{start,stop} inside /bin
mkdir -p %{buildroot}/bin
mv %{buildroot}%{_bindir}/unicode_{start,stop} %{buildroot}/bin
ln -s ../../bin/unicode_start %{buildroot}%{_bindir}/unicode_start
ln -s ../../bin/unicode_stop %{buildroot}%{_bindir}/unicode_stop
mv %{buildroot}%{_bindir}/setfont %{buildroot}/bin
ln -s ../../bin/setfont %{buildroot}%{_bindir}/setfont

mkdir %{buildroot}/sbin
install -m 0755 %{_sourcedir}/setsysfont %{buildroot}/sbin

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_service keytable


%preun
%_preun_service keytable


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/profile.d/configure_keyboard.sh
%config(noreplace) %{_initrddir}/keytable
%{_bindir}/chvt
%{_bindir}/deallocvt
%{_bindir}/dumpkeys
%{_bindir}/fgconsole
%{_bindir}/getkeycodes
%{_bindir}/kbd_mode
%{_bindir}/kbdrate
%{_bindir}/loadunimap
%{_bindir}/mapscrn
%{_bindir}/openvt
%{_bindir}/psfaddtable
%{_bindir}/psfgettable
%{_bindir}/psfstriptable
%{_bindir}/psfxtable
%ifarch %{ix86}
%{_bindir}/resizecons
%endif
%{_bindir}/setfont
%{_bindir}/setkeycodes
%{_bindir}/setleds
%{_bindir}/setmetamode
%{_bindir}/showconsolefont
%{_bindir}/showkey
%{_bindir}/unicode_start
%{_bindir}/unicode_stop
/bin/loadkeys
/bin/setfont
/bin/unicode_start
/bin/unicode_stop
/sbin/setsysfont
%{_mandir}/man1/chvt.1*
%{_mandir}/man1/deallocvt.1*
%{_mandir}/man1/dumpkeys.1*
%{_mandir}/man1/fgconsole.1*
%{_mandir}/man1/kbd_mode.1*
%{_mandir}/man1/loadkeys.1*
%{_mandir}/man1/openvt.1*
%{_mandir}/man1/psfaddtable.1*
%{_mandir}/man1/psfgettable.1*
%{_mandir}/man1/psfstriptable.1*
%{_mandir}/man1/psfxtable.1*
%{_mandir}/man1/setleds.1*
%{_mandir}/man1/setmetamode.1*
%{_mandir}/man1/showkey.1*
%{_mandir}/man1/unicode_start.1*
%{_mandir}/man1/unicode_stop.1*
%{_mandir}/man5/keymaps.5*
%{_mandir}/man8/getkeycodes.8*
%{_mandir}/man8/kbdrate.8*
%{_mandir}/man8/loadunimap.8*
%{_mandir}/man8/mapscrn.8*
%{_mandir}/man8/resizecons.8*
%{_mandir}/man8/setfont.8*
%{_mandir}/man8/setkeycodes.8*
%{_mandir}/man8/showconsolefont.8*
%{kbddir}


%changelog
* Fri Sep 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.12
- first Annvix build (replaces console-tools)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
