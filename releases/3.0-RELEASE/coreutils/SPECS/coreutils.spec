#
# spec file for package coreutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# mdv: 5.97-4mdv
#
# $Id$

%define revision	$Rev$
%define name		coreutils
%define version		6.9
%define release		%_revrel

Summary:	The GNU core utilities: a set of tools commonly used in shell scripts
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		ftp://alpha.gnu.org/gnu/coreutils/

Source0:	http://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.bz2
Source2:	su.pamd
Source3:	help2man
Patch0:		coreutils-6.9-DIR_COLORS-mdkconf.patch
Patch1:		coreutils-5.93-spacedir.patch
Patch4:		fileutils-4.1-ls_h.patch
Patch5:		coreutils-4.5.7-touch_errno.patch
Patch6:		textutils-2.0.17-mem.patch
Patch7:		coreutils-5.93-dateman.patch
Patch8:		sh-utils-1.16-paths.patch
Patch9:		coreutils-6.9-mdv-pam.patch
Patch10:	coreutils-6.9-mdv-new-i18n.patch
Patch11:	coreutils-5.2.1-ptbrfix.patch
Patch12:	coreutils-5.1.0-64bit-fixes.patch
Patch13:	coreutils-5.2.1-uname.patch
Patch18:	coreutils-6.9-mdv-force-option--override--interactive-option.patch
Patch19:	coreutils-6.9-fdr-ls-x.patch
Patch20: 	coreutils-6.9-mdv-always-blinking-colors-on-broken-symlinks.patch
Patch21:	coreutils-6.9-fdr-futimens.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext
BuildRequires:	termcap-devel
BuildRequires:	pam-devel
BuildRequires:	texinfo >= 4.3
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	automake >= 1.10
BuildRequires:	autoconf >= 2.61

Requires:  	pam >= 0.66-12
Provides:	fileutils = %{version}
Provides:	sh-utils = %{version}
Provides:	stat
Provides:	textutils = %{version}
Obsoletes:	fileutils
Obsoletes:	sh-utils
Obsoletes:	stat
Obsoletes:	textutils
Conflicts:	tetex < 1.0.7-49mdk

%description
These are the GNU core utilities.  This package is the union of the old
GNU fileutils, sh-utils, and textutils packages.

These tools are the GNU versions of common useful and popular file & text
utilities which are used for:

- file management
- shell scripts
- modifying text file (spliting, joining, comparing, modifying, ...)

Most of these programs have significant advantages over their Unix
counterparts, such as greater speed, additional options, and fewer arbitrary
limits.

The following tools are included:

  base64 basename cat chgrp chmod chown chroot cksum comm cp csplit cut
  date dd df dir dircolors dirname du echo env expand expr factor false
  fmt fold groups head hostid id install join kill link ln logname ls
  printenv printf ptx pwd readlink rm rmdir seq sha1sum sha224sum
  sha256sum sha384sum sha512sum shred shuf sleep sort split stat stty
  su sum sync tac tail tee test touch tr true tsort tty uname unexpand
  uniq unlink users vdir wc who whoami yes


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .colors_mdkconf
%patch1 -p1 -b .space
%patch4 -p1 -b .ls_h
%patch5 -p1 -b .touch_errno

%patch6 -p1 -b .textutils_mem

%patch7 -p1 -b .dateman
%patch8 -p1 -b .paths
%patch9 -p1 -b .pam

%patch10 -p1 -b .i18n
%patch11 -p0 -b .ptbr

%patch12 -p1 -b .64bit
%patch13 -p0 -b .cpu

%patch18 -p0 -b .override
%patch19 -p1 -b .ls-x
%patch20 -p1 -b .broken_blink
%patch21 -p1 -b .futimens

cp %{_sourcedir}/help2man man/help2man
chmod +x man/help2man
chmod +w ./src/dircolors.h
./src/dcgen ./src/dircolors.hin > ./src/dircolors.h


%build
export DEFAULT_POSIX2_VERSION=199209
aclocal-1.10 -I m4
automake-1.10 --gnits --add-missing
autoconf
%configure2_5x \
    --enable-largefile \
    --enable-pam

%make HELP2MAN=$PWD/man/help2man

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
perl -pi -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi


%check
# Run the test suite.
chmod a+x tests/sort/sort-mb-tests
chmod a+x tests/ls/x-option
%make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
# for help2man:
export PATH=$PATH:RPM_BUILD_ROOT/man

%makeinstall_std

# man pages are not installed with make install
make mandir=%{buildroot}%{_mandir} install-man

# let be compatible with old fileutils, sh-utils and textutils packages :
mkdir -p %{buildroot}{/bin,%{_bindir},%{_sbindir},%{_sysconfdir}/pam.d}
for f in basename cat chgrp chmod chown cp cut date dd df echo env expr false id link ln ls mkdir mknod mv nice pwd rm rmdir sleep sort stat stty sync touch true uname unlink
do
	mv %{buildroot}/{%{_bindir},bin}/$f 
done

ln -sf ../../bin/expr %{buildroot}%{_bindir}/

# chroot was in /usr/sbin :
mv %{buildroot}/{%{_bindir},%{_sbindir}}/chroot
# {cat,sort,cut} were previously moved from bin to /usr/bin and linked into 
for i in env cut; do ln -sf ../../bin/$i %{buildroot}/usr/bin; done

install -m644 src/dircolors.hin -D %{buildroot}%{_sysconfdir}/DIR_COLORS

# su
install -m 0755 src/su %{buildroot}/bin

# These come from util-linux and/or procps.
for i in hostname uptime ; do
    rm -f %{buildroot}{%{_bindir}/$i,%{_mandir}/man1/${i}.1}
done

install -m 0644 %{_sourcedir}/su.pamd %{buildroot}%{_sysconfdir}/pam.d/su

bzip2 -9f old/*/C* || :

# fix conflicts with util-linux
rm -f %{buildroot}%{_mandir}/man1/kill.1

%kill_lang %{name}
%find_lang %{name}

# (sb) Deal with Installed (but unpackaged) file(s) found
rm -f %{buildroot}%{_datadir}/info/dir


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%preun
%_remove_install_info %{name}.info


%post
%_install_info %{name}.info
# The next true is needed: else, if there's a problem, the 
# package'll be installed 2 times because of trigger faillure
true


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/D*
%config(noreplace) %{_sysconfdir}/pam.d/su
/bin/*
%{_bindir}/*
%{_sbindir}/chroot
%{_infodir}/coreutils*
%{_mandir}/man*/*

%files doc
%defattr(-,root,root)
%doc README ABOUT-NLS NEWS THANKS TODO old/*


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 6.9
- rebuild against new attr
- don't package the Changelog, we have NEWS

* Sat Oct 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 6.9
- remove the %%optflags re-define as it's not taking our old CFLAGS
  definitions so everything is built unoptimized and unprotected

* Sat Oct 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 6.9
- 6.9
- drop S1, use P0 instead to patch dircolors.hin for custom color support
- drop P0, no longer required
- drop P2, no longer required
- drop P2, obsoleted by upstream code
- drop P14, P15, P16, P17: old ACL patches are no longer required
- updated P9, P10, P18 from Mandriva
- P19: fix ls -x (Fedora)
- P20: always blink on broken symlinks (Mandriva)
- P21: allows to build against glibc 2.6 (Fedora)
- requires newer autoconf and automake

* Sat Jun 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.97
- drop unapplied patches
- renumber patches
- P18: re-introduce rm -i -f override (Mandriva)

* Mon Jun 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.97
- rebuild against new attr and acl
- fix buildreqs as per devel naming policy

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.97
- 5.97
- add buildreq on autoconf2.5 > 2.59 (says it wants 2.59d)
- rebuild against new pam
- sync with Mandriva 5.97-4mdv:
  - updated P800, P1001 for RH
  - rediff P101, P105, P111, P703, P1003
  - drop patches P108, P112, P116, P117, P153, P908, P2000 (merged upstream)
  - drop P2001 (no longer needed)
  - drop P105 (non-standard option)
  - drop P1155 (makes the test suite work again but means 'cp -i -f' will
    behave like 'cp -i' instead of like 'cp -f')
  - drop P111, P114, P115, P710, P901, P1002 (deprecated)
  - S200: synced with fedora
  - disable P104, P1003 (broken)
  - updated P1001, P1002, P1003, P1004 (from SUSE for ACL+xattr support)

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- spec cleanups
- remove locales

* Tue Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- rebuild against new acl and new attr
- spec cleanups
- drop DIR_COLORS.xterm
- renumber sources

* Wed Jun 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- fix su's pam config
- fix -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1-1avx
- 5.2.1
- sync with mandrake 5.2.1-8mdk:
  - P801: fix some types in pt_BR.po file (chiquitto)
  - P908: fix build, make it --short-circuit aware (tvignaud)
  - P909: 64bit fixes (gbeauchesne)
  - P910: show correct CPU name (Marcin Gondek, mdk bug #7865) (tvignaud)
  - P1001, P1002, P1003: add support for posix ACLs and extended
    attributes (chiquitto)
- drop patches P103, P113, P180, P502, P903, P905

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0-12avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0-11avx
- use new %%_buildroot macro
- spec cleanups
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0-10avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.0-9avx
- Annvix build

* Mon Mar 02 2004 Vincent Danen <vdanen@opensls.org> 5.0-8sls
- minor spec cleanups
- /bin/su is not suid root anymore

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 5.0-7sls
- OpenSLS build
- tidy spec
- use a decent description for -doc package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
