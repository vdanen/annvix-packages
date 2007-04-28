#
# spec file for package man
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		man
%define version		1.5m2
%define release		%_revrel

Summary:	A set of documentation tools:  man, apropos and whatis
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		ftp://ftp.win.tue.nl:/pub/linux-local/utils/man
Source0:	ftp://ftp.win.tue.nl/pub/linux-local/utils/man/man-%{version}.tar.bz2
Source1:	makewhatis.cronweekly
Source2:	makewhatis.crondaily
Source3:	man.config.5
# changed 'groff -Tlatin' to 'nroff' (no -T option); that makes auto-detect
# the charset to use for the output -- pablo
Patch1:		man-1.5k-confpath.patch
Patch4:		man-1.5h1-make.patch
Patch5:		man-1.5k-nonascii.patch
Patch6:		man-1.5m2-security.patch
Patch7:		man-1.5k-mandirs.patch
Patch8:		man-1.5m2-bug11621.patch
Patch9:		man-1.5k-sofix.patch
Patch10:	man-1.5m2-buildroot.patch
Patch12:	man-1.5m2-ro-usr.patch
Patch14:	man-1.5i2-newline.patch
Patch15:	man-1.5k-lookon.patch
Patch17:	man-1.5j-utf8.patch
# comment out the NJROFF line of man.conf, so that the nroff script
# can take care of japanese -- pablo
Patch18:	man-1.5k-nroff.patch
Patch19:	man-1.5i2-overflow.patch
Patch22:	man-1.5j-nocache.patch
Patch24:	man-1.5i2-initial.patch
# Japanese patches
Patch51:	man-1.5h1-gencat.patch
Patch101:	man-1.5m2-lang-aware_whatis.patch
Patch102:	man-1.5g-nonrootbuild.patch
Patch104:	man-1.5m2-tv_fhs.patch
Patch105:	man-1.5j-i18n.patch
Patch106:	man-1.5j-perlman.patch
Patch107:	man-1.5j-whatis2.patch
Patch200:	man-1.5m2-colored_groff.patch
Patch201:	man-1.5m2-l10ned-whatis.patch

Patch300:	man-1.5m2-new-sections.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	groff-for-man
Requires(pre):	setup

%description
The man package includes three tools for finding information and/or
documentation about your Linux system: man, apropos and whatis. The man
system formats and displays on-line manual pages about commands or
functions on your system. Apropos searches the whatis database
(containing short descriptions of system commands) for a string. Whatis
searches its own database for a complete word.


%prep
%setup -q
%patch1 -p0 -b .confpath
%patch4 -p1 -b .make
%patch5 -p1 -b .nonascii
%patch6 -p1 -b .security
%patch7 -p1 -b .mandirs
%patch8 -p1 -b .ad
%patch9 -p1 -b .sofix
%patch10 -p1 -b .less
%patch12 -p1 -b .usr
%patch14 -p1 -b .newline
%patch15 -p1 -b .lookon
%patch51 -p1 -b .jp2
%patch17 -p1 -b .utf8
%patch18 -p1 -b ._nroff
%patch19 -p1 -b .overflow
%patch22 -p1 -b .nocache
%patch24 -p1 -b .initial

%patch101 -p1 -b .whatbz2
%patch102 -p1
%patch104 -p1 -b .tv_fhs
%patch105 -p1 -b .i18n
%patch106 -p0 -b .perl
%patch107 -p0
%patch200 -p0 -b .color
%patch201 -p0 -b .l10n
%patch300 -p1 -b .sec

/bin/rm -f %{_builddir}/man-%{version}/man/en/man.conf.man


%build
(cd man; for i in `find -name man.conf.man`; do mv $i `echo $i|sed -e 's/conf.man/config.man/g'`;done)
install -m 0644 %{_sourcedir}/man.config.5 man/en/
./configure -default -confdir /etc +fsstnd +sgid +fhs +lang all \
    -compatibility_mode_for_colored_groff
make CC="gcc -g %{optflags} -D_GNU_SOURCE"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p  %{buildroot}%{_bindir}
mkdir -p  %{buildroot}%{_sbindir}
mkdir -p  %{buildroot}%{_mandir}
mkdir -p  %{buildroot}%{_sysconfdir}/cron.{daily,weekly}
perl -pi -e 's!/usr/man!/usr/share/man!g' conf_script
perl -pi -e 's!mandir = .*$!mandir ='"%{_mandir}"'!g' man2html/Makefile
make install PREFIX=%{buildroot}/  mandir=%{buildroot}/%{_mandir}

install -m 0755 %{_sourcedir}/makewhatis.cronweekly %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis.cron
install -m 0755 %{_sourcedir}/makewhatis.crondaily %{buildroot}%{_sysconfdir}/cron.daily/makewhatis.cron

mkdir -p %{buildroot}/var/catman{local,X11}
for i in 1 2 3 4 5 6 7 8 9 n; do
    mkdir -p %{buildroot}/var/catman/cat$i
    mkdir -p %{buildroot}/var/catman/local/cat$i
    mkdir -p %{buildroot}/var/catman/X11R6/cat$i
done


# symlinks for manpath
pushd %{buildroot}
    ln -s man .%{_bindir}/manpath
    ln -s man.1.bz2 .%{_mandir}/man1/manpath.1.bz2
    #perl -pi -e 's!nippon!latin1!g;s!-mandocj!-mandoc!g' etc/man.config
popd

/bin/rm -fr %{buildroot}/%{_mandir}/{de,fr,it,pl}
perl -pi -e 's!less -is!less -isr!g' %{buildroot}%{_sysconfdir}/man.config
#perl -pi -e 's!/usr/man!/usr/share/man!g' %{buildroot}%{_sbindir}/makewhatis

# Fix makewhatis perms
chmod 0755 %{buildroot}%{_sbindir}/makewhatis

%kill_lang %{name}

%clean
#[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sysconfdir}/cron.weekly/makewhatis.cron
%{_sysconfdir}/cron.daily/makewhatis.cron
%attr(2755,root,man) %{_bindir}/man
%{_bindir}/manpath
%{_bindir}/apropos
%{_bindir}/whatis
%{_bindir}/man2dvi
%{_bindir}/man2html
%{_sbindir}/makewhatis
%config(noreplace) %{_sysconfdir}/man.config
%{_datadir}/locale/en/man
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_mandir}/man1/*
%attr(0775,root,man)	%dir /var/catman
%attr(0775,root,man)	%dir /var/catman/cat[123456789n]
%attr(0775,root,man)	%dir /var/catman/local
%attr(0775,root,man)	%dir /var/catman/local/cat[123456789n]
%attr(0775,root,man)	%dir /var/catman/X11R6
%attr(0775,root,man)	%dir /var/catman/X11R6/cat[123456789n]


%changelog
* Fri Apr 27 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2
- update P7 to pickup manpages in /usr/local properly

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2
- spec cleanups
- remove locale stuff

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2
- rebuild with gcc4
- remove pre-Annvix changelog

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2-4avx
- P300: add new POSIX sections (tvignaud)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2-2avx
- bootstrap build

* Thu Mar 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5m2-1avx
- 1.5m2
- rediff P6, P8, P10,P104,  P201, P300 (tvignaud)
- rediff and rename P101: bzip2 whatis part was meged upstream, only keep
  LANG management part (tvignaud)
- drop P3, P11, P16, P26, and P108 (merged upstream) (tvignaud)
- spec cleanups

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.5k-16avx
- Annvix build

* Tue Jun 15 2004 Vincent Danen <vdanen@opensls.org> 1.5k-15sls
- include /usr/local/share/man in search path (modified P7)

* Sat Mar 06 2004 Vincent Danen <vdanen@mandrakesoft.com> 1.5k-14sls
- minor spec cleanups

* Mon Dec 02 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.5k-13sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
