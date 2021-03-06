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
%define version		5.97
%define release		%_revrel

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
Source1:	DIR_COLORS
Source2:	su.pamd
Source3:	help2man
Patch0:		coreutils-4.5.4-lug.patch
# fileutils
Patch101:	coreutils-5.93-spacedir.patch
Patch102:	coreutils-5.1.1-sparc.patch
Patch107:	fileutils-4.1.10-timestyle.patch
Patch118:	fileutils-4.1-ls_h.patch
Patch152:	coreutils-4.5.7-touch_errno.patch
Patch500:	textutils-2.0.17-mem.patch
# sh-utils
Patch703:	coreutils-5.93-dateman.patch
Patch704:	sh-utils-1.16-paths.patch
# RMS will never accept the PAM patch because it removes his historical
# rant about Twenex and the wheel group, so we'll continue to maintain
# it here indefinitely.
Patch706:	coreutils-5.93-pam.patch
Patch711:	sh-utils-2.0.12-hname.patch
# (sb) lin18nux/lsb compliance - normally from here:
# http://www.openi18n.org/subgroups/utildev/patch/
# this one is actually a merger of 5.2 and 5.3, as join segfaults
# compiled with gcc4 and the 5.1/5.2 patch
Patch800:	coreutils-5.97-new-i18n.patch
# small pt_BR fix
Patch801:	coreutils-5.2.1-ptbrfix.patch
Patch904:	coreutils-5.0.91-allow_old_options.patch
Patch909:	coreutils-5.1.0-64bit-fixes.patch
Patch910:	coreutils-5.2.1-uname.patch
# posix acls and extended attributes
# from http://ftp.opensuse.org/pub/opensuse/distribution/SL-OSS-factory/inst-source/suse/src/coreutils-5.97-4.src.rpm
# this one is already merged in CVS:
Patch1001:	coreutils-acl.diff
Patch1002:	coreutils-acl+posix.diff
Patch1003:	coreutils-xattr.diff
Patch1004:	coreutils-xattr-va-list.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext
BuildRequires:	termcap-devel
BuildRequires:	pam-devel
BuildRequires:	texinfo >= 4.3
BuildRequires:	libacl-devel
BuildRequires:	libattr-devel
BuildRequires:	automake1.8
BuildRequires:	autoconf2.5 > 2.59

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
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

%patch0 -p1 -b .lug
mv po/{lg,lug}.po

# fileutils
%patch101 -p1 -b .space
%patch102 -p1 -b .sparc
%patch107 -p1 -b .timestyle
%patch118 -p1
%patch152 -p1

# textutils
%patch500 -p1

# sh-utils
%patch703 -p1 -b .dateman
%patch704 -p1 -b .paths
%patch706 -p1 -b .pam

# li18nux/lsb
%patch800 -p1 -b .i18n
%patch801 -p0 -b .ptbr

#%patch904 -p1 -b .old-options
%patch909 -p1 -b .64bit
%patch910 -p0 -b .cpu

# posix acls and extended attributes
%patch1001 -p1 -b .acl
%patch1002 -p1 -b .acl+posix
%patch1003 -p1 -b .xattr
%patch1004 -p0 -b .xattr-va

cp %{_sourcedir}/help2man man/help2man
chmod +x man/help2man


%build
export DEFAULT_POSIX2_VERSION=199209
aclocal-1.8 -I m4
automake-1.8 -a -c
autoconf
%configure2_5x \
    --enable-largefile \
    --enable-pam

%make HELP2MAN=$PWD/man/help2man

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
perl -pi -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi


%check
# Run the test suite.
chmod +x ./tests/sort/sort-mb-tests
%make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[[ -f ChangeLog ]] && bzip2 -9f ChangeLog
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

install -c -m 0644 %{_sourcedir}/DIR_COLORS %{buildroot}/etc/

# su
install -m 0755 src/su %{buildroot}/bin

# These come from util-linux and/or procps.
for i in hostname uptime ; do
    rm -f %{buildroot}{%{_bindir}/$i,%{_mandir}/man1/${i}.1}
done

install -m 0644 %{_sourcedir}/su.pamd %{buildroot}%{_sysconfdir}/pam.d/su

bzip2 -f9 old/*/C* || :

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
%config(noreplace) /etc/pam.d/su
/bin/*
%{_bindir}/*
%{_sbindir}/chroot
%{_infodir}/coreutils*
%{_mandir}/man*/*

%files doc
%defattr(-,root,root)
%doc README ABOUT-NLS ChangeLog.bz2 NEWS THANKS TODO old/*


%changelog
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
