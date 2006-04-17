#
# spec file for package module-init-tools
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		module-init-tools
%define version		3.2.2
%define release		%_revrel

%define priority	20
%define _bindir		/bin
%define _sbindir	/sbin
%define _libdir		/lib
%define _libexecdir	/lib
%define toalternate	insmod lsmod modprobe rmmod depmod modinfo

Summary: 	Tools for managing Linux kernel modules
Name:		module-init-tools
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		ftp://ftp.kernel.org/pub/linux/kernel/people/rusty/modules/
Source0:	ftp://ftp.kernel.org/pub/linux/kernel/people/rusty/modules//%{name}-%{version}.tar.bz2
Source3:	modprobe.default
Source4:	modprobe.compat
Source5:	modprobe.preload
Patch1: 	module-init-tools-3.2-pre8-no-rename.patch
Patch2: 	module-init-tools-3.2-pre8-dont-break-depend.patch
Patch3:		module-init-tools-3.2-pre8-all-defaults.patch
Patch7:		module-init-tools-3.2-pre8-modprobe-default.patch
Patch8:		module-init-tools-3.2.2-generate-modprobe.conf-no-defaults.patch
Patch9:		module-init-tools-3.0-failed.unknown.symbol.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, glibc-static-devel, zlib-devel

Requires(post):	/usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
Conflicts:	modutils < 2.4.22-10mdk devfsd < 1.3.25-31mdk


%description
This package contains a set of programs for loading, inserting, and
removing kernel modules for Linux (versions 2.5.47 and above). It
serves the same function that the "modutils" package serves for Linux
2.4.


%prep
%setup -q
%patch1 -p1 -b .no-rename
%patch2 -p1 -b .dont-break-depend
%patch3 -p1 -b .all-defaults
%patch7 -p1 -b .modprobe-default
%patch8 -p1 -b .generate-modprobe.conf-no-defaults
%patch9 -p1 -b .failed-symb


%build
%serverbuild
%configure2_5x --enable-zlib
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall transform=

mv %{buildroot}%{_bindir}/lsmod %{buildroot}%{_sbindir}

pushd %{buildroot}%{_sbindir} && {
    for i in %{toalternate};do
        mv $i $i-25
    done
} && popd

rm -rf %{buildroot}/%{_mandir}
for n in 5 8;do
    install -d %{buildroot}/%{_mandir}/man$n/
    for i in *.$n;do
        [[ $n == 8 ]] && ext="-25" || ext=""
        install -m644 $i %{buildroot}/%{_mandir}/man${n}/${i%%.*}${ext}.$n
    done
done

pushd %{buildroot}%{_sbindir} && {
%ifnarch %{ix86}
    mv insmod.static insmod.static-25
%else
    rm -f insmod.static
%endif
} && popd

install -d -m755 %{buildroot}%{_sysconfdir}/
touch %{buildroot}%{_sysconfdir}/modprobe.conf
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}
install -d -m755 %{buildroot}%{_sysconfdir}/modprobe.d/

install -d -m755 %{buildroot}%{_libdir}/module-init-tools
install -m 644 %{SOURCE3} %{buildroot}%{_libdir}/module-init-tools
install -m 644 %{SOURCE4} %{buildroot}%{_libdir}/module-init-tools


%post
for i in %{toalternate};do
    update-alternatives --install %{_sbindir}/$i $i %{_sbindir}/$i-25 %{priority}
    update-alternatives --install \
    %{_mandir}/man8/$i.8%{_extension} man-$i %{_mandir}/man8/$i-25.8%{_extension} %{priority}
    [ -e %{_sbindir}/$i ] || update-alternatives --auto $i
    [ -e %{_mandir}/$i.8%{_extension} ] || update-alternatives --auto man-$i
done

if [ ! -s %{_sysconfdir}/modprobe.conf ]; then
    MODPROBE_CONF=%{_sysconfdir}/modprobe.conf
elif [ -e %{_sysconfdir}/modprobe.conf.rpmnew ]; then
    MODPROBE_CONF=%{_sysconfdir}/modprobe.conf.rpmnew
fi

if [ -s %{_sysconfdir}/modules.conf -a -n "$MODPROBE_CONF" ]; then
    echo '# This file is autogenerated from %{_sysconfdir}/modules.conf using generate-modprobe.conf command' >> $MODPROBE_CONF
    echo >> $MODPROBE_CONF
    %{_sbindir}/generate-modprobe.conf >> $MODPROBE_CONF 2> /dev/null
fi

if [ -s %{_sysconfdir}/modprobe.conf ]; then
    perl -pi -e 's/(^\s*include\s.*modprobe\.(default|compat).*)/# This file is now included automatically by modprobe\n# $1/' %{_sysconfdir}/modprobe.conf
fi


%postun
for i in %{toalternate};do
    if [ ! -f %{_sbindir}/$i-25 ]; then
        update-alternatives --remove $i %{_sbindir}/$i
    fi
    [ -e %{_sbindir}/$i ] || update-alternatives --auto $i

    if [ ! -f %{_mandir}/man8/$i-25.8%{_extension} ]; then
        update-alternatives --remove man-$i %{_mandir}/man8/$i.8%{_extension}
    fi
    [ -e %{_mandir}/man8/$i.8%{_extension} ] || update-alternatives --auto man-$i
done


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README 
%doc TODO stress_modules.sh
%config(noreplace) %{_sysconfdir}/modprobe.conf
%config(noreplace) %{_sysconfdir}/modprobe.preload
%dir %{_sysconfdir}/modprobe.d/
%dir %{_libdir}/module-init-tools
%{_libdir}/module-init-tools/*
%{_sbindir}/generate-modprobe.conf
%{_sbindir}/*25
%{_mandir}/*/*


%changelog
* Mon Apr 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2.2
- first Annvix package for the 2.6 kernel

* Thu Dec 22 2005 Thierry Vignaud <tvignaud@mandriva.com> 3.2.2-4mdk
- source 4: use sata_promise instead of pdc-ultra on kernel-2.6.x

* Tue Dec 20 2005 Olivier Blin <oblin@mandriva.com> 3.2.2-3mdk
- Source3: kill ppp aliases in modprobe.default, they're wrongly
  duplicated with kernel aliases and break mppe (#16419)
- create and own /etc/modprobe.d/
- kill Source2, we don't use devfs anymore

* Fri Dec 16 2005 Olivier Blin <oblin@mandriva.com> 3.2.2-2mdk
- Patch8: really use modules.conf (and use a more meaningfull variable name)

* Fri Dec  9 2005 Olivier Blin <oblin@mandriva.com> 3.2.2-1mdk
- 3.2.2
- remove Patch4, merged upstream

* Sun Aug 14 2005 Oden Eriksson <oeriksson@mandriva.com> 3.2-0.pre8.2mdk
- fix %%{_mandir}
- fix deps

* Mon Aug  8 2005 Olivier Blin <oblin@mandriva.com> 3.2-0.pre8.1mdk
- 3.2.0-pre8
- modify Patch1 to keep modname translation (s/-/_/) in rmmod
- make Patch2 a real patch, not a tarball
- cleaner way to handle /lib/module-init-tools/modprobe.default (Patch7)
- simplify Patch8 (use TESTING_MODPROBE_CONF)
- drop Patch10 (filename support merged upstream)
- Patch3: load all default config files
- Patch4: fix locking error
- remove Prefix tag

* Fri Feb 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0-7mdk
- source 4:
  o kill 1 duplicate
  o sort
  o fix spacing
  o update comments

* Wed Jan 19 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0-6mdk
- load it821x instead of it8212 and iteraid (#13099)

* Tue Jan 11 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0-5mdk
- added nfsv4 support in S3 (fedora)

* Wed Sep 08 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0-4mdk
- source 4: do not replace sonypi by i8xx_tco (Adam Williamson)

* Tue Aug 31 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0-3mdk
- source 4: add more compatibility entries:
  o aironet4500_card => airo
  o alim1535d_wdt => alim1535_wdt
  o amd7xx_tco|amd768_rng|i810_rng     => hw_random
  o i810-tco|sonypi => i8xx_tco
  o dc395x_trm => dc395x
  o tulip_old => tulip

* Sat Mar 20 2004 Thomas Backlund <tmb@mandrake.org> 3.0-2mdk
- patch10: add filename info to modinfo
  * simplifies generation of modules.description
  * patch done by Rusty, forwarded by Danny
- add missing BuildRequires: docbook-utils and docbook-dtd41-sgml

* Tue Mar 16 2004 Nicolas Planel <nplanel@mandrakesoft.com> 3.0-1mdk
- bump to version 3.0.
- patch9 (failed.unknown.symbol) is really needed to build kernel.

* Tue Feb 03 2004 Nicolas Planel <nplanel@mandrakesoft.com> 3.0-0.pre9.2mdk
- remove bcm4400 -> b44 from modprobe.compat.

* Sat Jan 31 2004 Thomas Backlund <tmb@mandrake.org> 3.0-0.pre9.1mdk
- upgrade to pre9 to actually build *.static as static
- rediff Patch2: dont-break-depend
- drop Patch9: failed.unknown.symbol (removed upstream)
- BuildRequires: autoconf2.5

* Thu Jan 29 2004 Planel Nicolas <nplanel@mandrakesoft.com> 3.0-0.pre7.2mdk
- don't break depend if 1 of module is allready loaded.

* Wed Jan 28 2004 Planel Nicolas <nplanel@mandrakesoft.com> 3.0-0.pre7.1mdk
- no more s/[-,]/_/

* Thu Jan 22 2004 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0-0.pre5.3mdk
- configure is of 2.5 style, use correct percent-configure macro

* Wed Jan 14 2004 Planel Nicolas <nplanel@mandrakesoft.com> 3.0-0.pre5.2mdk
- depmod return 1 if unknown symbol found (-e trigger)

* Sat Jan 10 2004 Andrey Borzenkov <arvidjaar@mail.ru> 3.0-0.pre5.1mdk
- new version; it makes modprobe behaviour compatible with modutils
  (do not return failure when inserting module that already exists)
- update source3 - use --first-time for install/remove as is default now.

* Wed Jan  7 2004 Andrey Borzenkov <arvidjaar@mail.ru> 3.0-0.pre2.2mdk
- update patch7:
    o This should now really behave as if "include modprobe.default" were
      the first line of modprobe.conf
    o Fix read_config call when multiple modules are present
- kernel 2.6.0 calls char-major-N-M not char-major-N; change aliases
  in modprobe.default to be char-major-N-*
- change modprpobe.default to use aliases again now when patch7 is fixed.
- kernel calls binfmt-%04x

* Tue Dec 30 2003 Andrey Borzenkov <arvidjaar@mail.ru> 3.0-0.pre2.1mdk
- new version
- remove patch6 - fixed version upstream
- fix Conflicts (should be mdk versions)

* Fri Dec 12 2003 Nicolas Planel <nplanel@mandrakesoft.com> 0.9.15-0.pre4.2mdk
- update modprobe.compat.

* Sun Nov 23 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.15-0.pre4.1mdk
- new version (isapnp and to keep current :)
- rediff patch6 (is likely to be dropped alltogether in favour of file2alias
  when hotplug is ready)
- BuildRequires glibc-static-devel not libc.a

* Sat Nov  1 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.15-0.pre2.0.2bor
- remove all modules that define MODULE_ALIAS from modprobe.default

* Mon Oct 27 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.15-0.pre2.0.1bor
- new version
- remove patch4 - integrateg upstream

* Tue Sep  9 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.14-0.pre2.0.1bor
- new version
- rediff patch4
- rediff patch7
- remove patch9 - integrated upstream
- remove patch10 - integrated upstream
- remove patch11 - integrated upstream
- automake, auutoconf no more required for build

* Mon Aug 18 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.13-0.2bor
- patch11 - fix module names in map tables for compressed modules
- sorry, had to provide better version initially

* Sat Aug 16 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.13-1bor
- 0.9.13 is out
- replace patch9 with that from Rusty to be appeared in next version
  (this also does true -A)
- rediff patch6 and put it after patch9 so it won't conflict when patch9
  is integrated
- always generate modprobe.conf if it is empty
- disable patch1 - integrated upstream
- patch10 - unused variable in modprobe.c
- fix post script - it commented out already commented out lines

* Wed Aug 13 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.13-0.pre2.0.3bor
- patch9 - support compressed (gzip) modules

* Sat Aug  9 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.13-0.pre2.0.2bor
- BuildRequires libc.a for static compilation
- replace all aliases with install commands in modprobe.default. It is
  impossible to easily disable alias given current implementation. Make it
  include modprobe.compat
- ditto for modprobe.compat
- patch7 - include modprobe.default automatically
- patch8 - do not use modprobe -c in generate-modprobe.conf by default, use
  just /etc/modules.conf. This can be overridien by --use-modprobe-c
- remove include modprobe.{default|compat} on update
- provide empty default modprobe.conf now

* Wed Aug  6 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.13-0.pre2.0.1bor
- new version
- remove patch3 - it was left by accident
- remove patch5 - modififed version integrated upstream

* Sat Aug  2 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.13-0.pre.0.3bor
- new patch5 - make depmod create temporary files and rename them. It fixes
  races between modprobe and depmod -a in rc.sysinit - it is possible
  modprobe sees empty files and fails to load module
- move patch5 -> patch6 and rediff

- patch5 -> patch6 and 
* Tue Jul 29 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.13-0.pre.0.2bor
- remove mouse-mod hack it does not work anyway
- irtty -> irtty_sir (and dongles); some dongles won't work until ported
- remove all hid etc crap from modprobe.default, it must be handled by hotlpug
- remove mouse/joystick from modprobe.devfs, it is loaded by hootplug
- patch5 - depmod support for input device ids

* Sat Jul 19 2003 Andrey Borzenkov <arvidjaar@mail.ru> 0.9.13-0.pre.1bor
- new version
- use --stdin for generate-modprobe.conf

* Wed Jul 16 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.11a-3mdk
- from Andrey Borzenkov <arvidjaar@mail.ru> :
  o Preserve insmod.static - needed for initrd until nash can handle it
  o Do not strip too much from modprobe.conf.5 -> modprobe.5
  o Install modprobe.devfs
  o patch2 with mandrake modifications to modules.devfs
  o conflicts with modutils < 2.4.22-10mdk
  o probeall support in modprobe
  o patch4: remove devfsd hack now when it is fixed in devfsd. Add conflict
    with previous devfsd versions
  o source1 - default modprobe.conf
  o source2 - default modprobe.devfs
  o source3 - modprobe.default
  o source4 - modprobe.compat
  o remove patch2 (replaced by source2)
  o generate default modprobe.conf from modules.conf on install
  o put back ide-probe-mod - removed by confusion. Oops.
  o add /etc/modprobe.preload
  o fix raw devices in modprobe.devfs
  o modprobe does not support chained aliases. Rewrite modprobe.devfs to not
    use them. Add warning to modprobe.devfs and adapt examples
  o use modprobe mouse-mod; modprobe mousedev for mouse devices. 2.5 splits
    mouse support into frontend - mousedev - and backend. Backend is
    supposed to be loaded by hotplug but until then let user configure it
    in modprobe.conf as mouse-mod
  o ditto for joysticks as joystick-mod
  o remove obsolete mice from modprobe.default. Use the same trick for
    char-major-13-32 (/dev/input/mouse0) and char-major-10-1 (/dev/psaux) -
    modprobe mouse-mod; modprobe mousedev. This probably should not be done
    for /dev/input/mice as it is supposed to be for USB mostly and USB backend
    is hotplugged.
  o replace printer by usblp in modprobe.default
  o add some hints to default modprobe.conf
  o tty-ldisc-2 is serport (serial mouse port)

* Mon Apr  7 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9.11a-1mdk
- Move lsmod to /sbin to don't break alternatives system (#3679)

* Fri Apr  4 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9.11a-1mdk
- Bump to version 0.9.11a.

* Thu Mar 27 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9.10-1mdk
- Bump to version 0.9.10.

* Thu Feb  6 2003 Chmouel Boudjnah <cuhmouel@mandrakesoft.com> 0.9.9-1mdk
- Bump to version 0.9.9.

* Wed Jan 15 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9.8-2mdk
- Remove modutils package and move it to his own package.

* Tue Jan 14 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9.8-1mdk
- Bump to version 0.9.8.

* Tue Jan 14 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9.7-5mdk
- handle gpl symbol in module-init-tools (Petr Vandrovec).

* Tue Jan 14 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9.7-4mdk
- Add modules.conf as noreplace config file.

* Fri Jan 10 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9.7-3mdk
- Silly me forgot that bloody Prereq: on update-alternatives.

* Wed Jan  8 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9.7-2mdk
- I promess i will go to temple every day light-up a candle and pray
  that update-alternatives will work this time 8-(.
- Generate modutils from here (not really necessary but easy to
  maintain) and try to make it live with new module-init package.
- New module-init-tools package.

* Wed Jan  8 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9.7-1mdk
- First version.
- Fake ChangeLog never released because of upgrade of modutils
  nevermind since i am the master of this specfile.

# end of file
