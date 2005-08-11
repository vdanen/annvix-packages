#
# spec file for package coreutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# fileutils: rh-4.1-4
# sh-utils:  rh-2.0.12-2

%define name		coreutils
%define version		5.0
%define release		12avx

# for sh-utils :
%define optflags $RPM_OPT_FLAGS -D_GNU_SOURCE=1

Summary:	The GNU core utilities: a set of tools commonly used in shell scripts
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		ftp://alpha.gnu.org/gnu/coreutils/

Source0:	ftp://prep.ai.mit.edu/pub/gnu/%{name}/%{name}-%{version}.tar.bz2
Source101:	DIR_COLORS
Source102:	DIR_COLORS.xterm
Source200:	su.pamd
Source201:	help2man
Patch0:		coreutils-4.5.4-lug.patch.bz2
# fileutils
Patch101:	fileutils-4.0-spacedir.patch.bz2
Patch102:	fileutils-4.0s-sparc.patch.bz2
Patch103:	coreutils-4.5.2-trunc.patch.bz2
Patch105:	coreutils-4.5.2-C.patch.bz2
Patch107:	fileutils-4.1.10-timestyle.patch.bz2
Patch108:	fileutils-4.1.5-afs.patch.bz2
Patch111:	coreutils-4.5.2-dumbterm.patch.bz2
Patch112:	fileutils-4.0u-glibc22.patch.bz2
Patch113:	coreutils-4.5.2-nolibrt.patch.bz2
Patch114:	fileutils-4.1-restorecolor.patch.bz2
Patch115:	fileutils-4.1.1-FBoptions.patch.bz2
Patch1155:	fileutils-4.1-force-option--override--interactive-option.patch.bz2
Patch116:	fileutils-4.1-dircolors_c.patch.bz2
Patch117:	fileutils-4.1-ls_c.patch.bz2
Patch118:	fileutils-4.1-ls_h.patch.bz2
Patch152:	coreutils-4.5.7-touch_errno.patch.bz2
Patch153:	fileutils-4.1.10-utmp.patch.bz2
Patch180:	coreutils-4.5.12-fr-fix.patch.bz2
Patch500:	textutils-2.0.17-mem.patch.bz2
Patch502:	textutils-2.0.21-man.patch.bz2
# sh-utils
Patch702:	coreutils-4.5.7-utmp.patch.bz2
Patch703:	sh-utils-2.0.11-dateman.patch.bz2
Patch704:	sh-utils-1.16-paths.patch.bz2
# RMS will never accept the PAM patch because it removes his historical
# rant about Twenex and the wheel group, so we'll continue to maintain
# it here indefinitely.
Patch706:	coreutils-4.5.2-pam.patch.bz2
Patch710:	sh-utils-2.0-rfc822.patch.bz2
Patch711:	sh-utils-2.0.12-hname.patch.bz2
# (sb) lin18nux/lsb compliance
Patch800:	http://www.li18nux.org/subgroups/utildev/patch/coreutils-4.5.9-i18n-0.2.patch.bz2
Patch901:	coreutils-4.5.3-signal.patch.bz2
Patch903:	coreutils-4.5.3-manpage.patch.bz2
Patch904:	coreutils-5.0-allow_old_options.patch.bz2
Patch905:	coreutils-5.0-du-fd_leak.patch.bz2


BuildRoot:	%_buildroot/%{name}-%{version}
BuildRequires:	gettext termcap-devel pam-devel texinfo >= 4.3

Requires:  	pam >= 0.66-12
Provides:	fileutils = %{version}, sh-utils = %{version}, stat, textutils = %{version}
Obsoletes:	fileutils sh-utils stat textutils
Conflicts:	tetex < 1.0.7-49mdk

%description
These are the GNU core utilities.  This package is the union of
the old GNU fileutils, sh-utils, and textutils packages.

These tools're the GNU versions of common useful and popular
file & text utilities which are used for:
- file management
- shell scripts
- modifying text file (spliting, joining, comparing, modifying, ...)

Most of these programs have significant advantages over their Unix
counterparts, such as greater speed, additional options, and fewer
arbitrary limits.

The following tools are included:

  basename cat chgrp chmod chown chroot cksum comm cp csplit cut date dd
  df dir dircolors dirname du echo env expand expr factor false fmt fold
  ginstall groups head hostid hostname id join kill link ln logname ls
  md5sum mkdir mkfifo mknod mv nice nl nohup od paste pathchk pinky pr
  printenv printf ptx pwd readlink rm rmdir seq sha1sum shred sleep sort
  split stat stty su sum sync tac tail tee test touch tr true tsort tty
  uname unexpand uniq unlink uptime users vdir wc who whoami yes


%package doc
Summary:	Coreutils documentation in info format
Group:		Books/Computer books
Requires:	coreutils >= 4.5.4-2mdk
Prereq:		info-install

%description doc
Documentation for the coreutils package; includes manpages, an info file,
and other miscellaneous documentation.


%prep
%setup -q

%patch0 -p1 -b .lug
mv po/{lg,lug}.po

# fileutils
%patch101 -p1 -b .space
%patch102 -p1 -b .sparc
%patch103 -p0 -b .trunc
%patch105 -p0 -b .Coption
%patch107 -p1 -b .timestyle
%patch108 -p1 -b .afs
%patch111 -p0 -b .dumbterm
%patch112 -p1 -b .glibc22
%patch113 -p1 -b .nolibrt
%patch114 -p1 -b .restore
%patch115 -p1 -b .FBopts
%patch1155 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch152 -p1
%patch153 -p1
%patch180 -p1 -b .frfix

# textutils
%patch500 -p1
# patch in new ALL_LINGUAS
%patch502 -p1

# sh-utils
%patch702 -p1 -b .utmp
%patch703 -p1 -b .dateman
%patch704 -p1 -b .paths
%patch706 -p1 -b .pam
%patch710 -p1 -b .rfc822

# li18nux/lsb
%patch800 -p1 -b .i18n

%patch901 -p1 -b .su-hang
%patch903 -p1 -b .rm-manpage
%patch904 -p1 -b .old-options
%patch905 -p0 -b .du-fd_leak

%build
touch aclocal.m4 configure config.hin Makefile.in */Makefile.in */*/Makefile.in
%configure --enable-largefile --enable-pam || :
make all CPPFLAGS="-DUSE_PAM" su_LDFLAGS="-lpam -lpam_misc"

unset LINGUAS || :
for i in AUTOMAKE ACLOCAL;do perl -pi -e "s%^$i = .*$%$i = /bin/true%g" Makefile.in;done
%configure2_5x
[[ -f ChangeLog && -f ChangeLog.bz2  ]] || bzip2 -9f ChangeLog

%make

# Run the test suite.
#make check

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
perl -pi -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi

cp %SOURCE201 man/help2man
chmod +x man/help2man


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

# man pages are not installed with make install
make mandir=%{buildroot}%{_mandir} install-man

# fix japanese catalog file
if [ -d %{buildroot}/%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES ]; then
   mkdir -p %{buildroot}/%{_datadir}/locale/ja/LC_MESSAGES
   mv %{buildroot}/%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES/*mo \
		%{buildroot}/%{_datadir}/locale/ja/LC_MESSAGES
   rm -rf %{buildroot}/%{_datadir}/locale/ja_JP.EUC
fi

# let be compatible with old fileutils, sh-utils and textutils packages :
mkdir -p %{buildroot}{/bin,%{_bindir},%{_sbindir},%{_sysconfdir}/pam.d}
for f in basename cat chgrp chmod chown cp cut date dd df echo env false id link ln ls mkdir mknod mv nice pwd rm rmdir sleep sort stat stty sync touch true uname unlink
do
	mv %{buildroot}/{%{_bindir},bin}/$f 
done

# chroot was in /usr/sbin :
mv %{buildroot}/{%{_bindir},%{_sbindir}}/chroot
# {cat,sort,cut} were previously moved from bin to /usr/bin and linked into 
for i in env cut; do ln -sf ../../bin/$i %{buildroot}/usr/bin; done

install -c -m 0644 %SOURCE101 %{buildroot}/etc/

# su
install -m 0755 src/su %{buildroot}/bin

# These come from util-linux and/or procps.
for i in hostname uptime ; do
	rm -f %{buildroot}{%{_bindir}/$i,%{_mandir}/man1/${i}.1}
done

install -m 644 %SOURCE200 %{buildroot}%{_sysconfdir}/pam.d/su

ln -sf test %{buildroot}%{_bindir}/[

bzip2 -f9 old/*/C* || :

%find_lang %{name}

# (sb) Deal with Installed (but unpackaged) file(s) found
rm -f %{buildroot}%{_datadir}/info/dir
rm -rf %{buildroot}%{_datadir}/locale/*/LC_TIME


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre doc
# We must desinstall theses info files since they're merged in
# coreutils.info. else their postun'll be runned too last
# and install-info'll faill badly because of doubles
for file in sh-utils.info textutils.info fileutils.info; do
	if [ -f /usr/share/info/$file.bz2 ]; then
		/sbin/install-info /usr/share/info/$file.bz2 --dir=/usr/share/info/dir --remove &> /dev/null
	fi
done

%preun doc
%_remove_install_info %{name}.info

%post doc
%_install_info %{name}.info
# The next true is needed: else, if there's a problem, the 
# package'll be installed 2 times because of trigger faillure
true


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/D*
%config(noreplace) /etc/pam.d/su
%doc README
/bin/*
%{_bindir}/*
%{_sbindir}/chroot

%files doc
%defattr(-,root,root)
%doc ABOUT-NLS ChangeLog.bz2 NEWS THANKS TODO old/*
%{_infodir}/coreutils*
%{_mandir}/man*/*

%changelog
* Wed Aug 10 2005 Vincent Danen <vdanen@annvix.org> 5.0-12avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen@annvix.org> 5.0-11avx
- use new %%_buildroot macro
- spec cleanups
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 5.0-10avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 5.0-9avx
- Annvix build

* Mon Mar 02 2004 Vincent Danen <vdanen@opensls.org> 5.0-8sls
- minor spec cleanups
- /bin/su is not suid root anymore

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 5.0-7sls
- OpenSLS build
- tidy spec
- use a decent description for -doc package

* Sun Aug  3 2003 Pixel <pixel@mandrakesoft.com> 5.0-6mdk
- allow old style options (eg: head -1)
  (we could keep the warning, but breaking backward compatibility is crazy)

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.0-5mdk
- BuildRequires: termcap-devel

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 5.0-4mdk
- rebuild

* Thu May 15 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0-3mdk
- fix su rejecting passwords

* Thu May 15 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0-2mdk
- patch 800: add url and update (should speed up sort)
- patch 901: su hang in some rare cases
- patch 903: fix example in rm(1)
- patch 905: fix file descriptor leak in du which resulted in faillure on big
  directories

* Mon Apr 07 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0-2mdk
- add readlink to tool list

* Mon Apr 07 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0-1mdk
- new release
- use packaged readlink

* Fri Apr 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.12-2mdk
- provide color scheme for ls in xterm too
- remove obsolete l10n updates

* Fri Apr 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.12-1mdk
- new release
- update patch 180 : fix many, many typos in french translation

* Thu Feb 13 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.7-1mdk
- new release
- rediff patch 152, 180, 702, 800

* Thu Jan 16 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.4-4mdk
- move more docs to doc subpackage to reduce minimal system

* Tue Jan 14 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.4-3mdk
- move prereq on install-info from main package to doc subpackage

* Mon Jan 13 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.4-2mdk
- split up the doc because of drakx

* Fri Jan 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.4-1mdk
- new release
- rediff patches 0, 180

* Sun Nov 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 4.5.3-2mdk
- LI18NUX/LSB compliance (patch800)
- Installed (but unpackaged) file(s) - /usr/share/info/dir

* Thu Oct 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.3-1mdk
- new release
- rediff patch 180
- merge patch 150 into 180

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-6mdk
- move su back to /bin

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-5mdk
- patch 0 : lg locale is illegal and must be renamed lug (pablo)

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-4mdk
- fix conflict with procps

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-3mdk
- patch 105 : fix install -s

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-2mdk
- fix build
- don't chmode two times su
- build with large file support
- fix description
- various spec cleanups
- fix chroot installation
- fix missing /bin/env
- add old fileutils, sh-utils & textutils ChangeLogs

* Fri Oct 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-1mdk
- initial release (merge fileutils, sh-utils & textutils)
- obsoletes/provides: sh-utils/fileutils/textutils
- fileutils stuff go in 1xx range
- sh-utils stuff go in 7xx range
- textutils stuff go in 5xx range
- drop obsoletes patches 1, 2, 10 (somes files're gone but we didn't ship
  most of them)
- rediff patches 103, 105, 111, 113, 180, 706
- temporary disable patch 3 & 4
- fix fileutils url
