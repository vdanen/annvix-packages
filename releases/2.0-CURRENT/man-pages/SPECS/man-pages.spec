#
# spec file for package man-pages
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		man-pages
%define version		2.08
%define release 	%_revrel

%define LANG		en

Summary:	English man (manual) pages from the Linux Documentation Project
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL-style
Group:		System/Internationalization
URL:		ftp://ftp.kernel.org/pub/linux/docs/manpages/
Source:		ftp.kernel.org/pub/linux/docs/manpages/%{name}-%{version}.tar.bz2
Source1:	rpcgen.1
Source3:	ld.so.8
Source4:	ldd.1
Source5:	ldconfig.8
Source6:	man-pages-extralocale.tar.bz2
Source8:	man9-19971126.tar.bz2
Source9:	man2.tar.bz2
Source10:	strptime.3
Source11:	man-network.tar.bz2
Patch0:		man-pages-1.44-ext3.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	man => 1.5j-8mdk

Requires:	man => 1.5j-8mdk
Prereq:		sed, grep, man
Autoreqprov:	false

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP).  The man pages are organized into the
following sections:

        Section 1:  User commands (intro only)
        Section 2:  System calls
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, /etc/passwd, nfs)
        Section 6:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)
        Section 9:  Kernel internal routines


%prep
%setup -q -a 9 -a 8 -a6

cp -a %{SOURCE1} man1
cp -a %{SOURCE3} man8
cp -a %{SOURCE4} man1
cp -a %{SOURCE5} man8
cp -a %{SOURCE10} man3

%patch0 -p1


%build
rm -fv man1/{diff,chgrp,chmod,chown,cp,dd,df,dircolors,du,install,dir,vdir}.1
rm -fv man1/{ln,ls,mkdir,mkfifo,mknod,mv,rm,rmdir,touch}.1
rm -fv man2/modules.2 man2/quotactl.2 man2/get_kernel_syms.2 
rm -fv man2/{create,delete,init,query}_module.2
rm -fv man4/{console,fd}.4 man5/{exports,nfs,fstab}.5

# those conflict with ld.so package
# this one conflicts with bind-utils
rm -rf man5/resolver.5

# this conflicts with ldconfig -- Geoff
rm -f man8/ldconfig.8

# those conflict with glibc{,-devel}
rm -f man1/{getent,iconv,ldd,locale,localedef,sprof}.1
rm -f man8/{ld.so,rpcinfo}.8
rm -f man1/rpcgen.1
rm -f man3/crypt.3

# this conflict with glibc
rm -f man1/rpcgen.1.bz2
				
#mv man1/COPYING .
mv man1/README README.GNU-INFOvsMAN


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

set +x
mkdir -p %{buildroot}%{_mandir}
for n in 0p 1 1p 2 3 3p 4 5 6 7 8 9; do
    mkdir %{buildroot}%{_mandir}/man$n
done
for n in man*/*; do
    cp -a $n %{buildroot}%{_mandir}/$n
done

set -x

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LANG}.cron << EOF
#!/bin/bash
LANG='' /usr/sbin/makewhatis %{_mandir}/%{LANG}
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LANG}.cron

mkdir -p  %{buildroot}/var/cache/man/%{LANG}
mkdir -p  %{buildroot}{%{_mandir}/%{LANG},/var/catman/}
tar xfj %{SOURCE11} -C %{buildroot}%{_mandir}

 
%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(0644,root,man,755)
%doc README* *.Announce POSIX-COPYRIGHT Changes
%config(noreplace) %attr(755,root,root)%{_sysconfdir}/cron.weekly/makewhatis-%{LANG}.cron
%dir %{_mandir}/%{LANG}
%dir %{_mandir}/man*p/
%{_mandir}/man*/*


%changelog
* Wed Jan 25 2006 Vincent Danen <vdanen-at-build.annvix.org>
- 2.08
- fix unowned directories
- drop merged patches P4, P5, P6

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.07-1avx
- 2.07
- include POSIX man pages

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-4avx
- remove crypt.3 manpage (in glibc)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-2avx
- bootstrap build

* Thu Mar 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-1avx
- 2.01
- spec cleanups

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.60-4avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.60-3sls
- minor spec cleanups
- remove icon

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.60-2sls
- OpenSLS build
- tidy spec
- don't generate the whatis database

* Tue Aug 26 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.60-1mdk
- new release

* Fri Aug 22 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.59-1mdk
- new release

* Fri Jul 25 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.58-1mdk
- new release

* Fri Jul 18 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.57-1mdk
- new release

* Wed Jul 16 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.56-3mdk
- fix conflict with glibc

* Tue May 13 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.56-2mdk
- fix potentian conflict with glibc (at this stage, content/perms are the
  same so rpm does not conflict yet)
- do not own system wide directories (/var/cache/man/ and /var/catman/)

* Thu Apr 10 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.56-1mdk
- new release

* Mon Apr  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.54-4mdk
- Patch6: Note about biarch struct utmp

* Mon Mar 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.54-3mdk
- source 11: add ifcfg.5, ifdown.8 and ifup.8 man pages

* Wed Feb 12 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.54-2mdk
- remove offensive man pages

* Mon Jan 06 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.54-1mdk
- new release

* Tue Dec 03 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.53-3mdk
- patch 5 : fix time man page (reported by Brian Gallaway)
- fix makewhatis path in %%install
- fix extra man pages installation (sex, guru & baby)

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.53-2mdk
- fix build

* Thu Oct 10 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.53-1mdk
- new release

* Tue Aug  6 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.52-2mdk
- use %%verify for whatis db

* Mon Jul 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.52-1mdk
- new release

* Tue Jun 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.51-1mdk
- new release

* Tue Jun 04 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.50-1mdk
- new release
- spec clean: s!tar!-aX!
- add cron entry to nightly update whatis db
- requires man => 1.5j-8mdk for new man-pages framework
- use new std makewhatis to build whatis in spec and in cron entry 
- whatis db goes into /var/cache/man (so enable ro /usr)

* Mon Apr 08 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.48-2mdk
- remove FIXME (not anymore in sources)
- add ext3 man pages
- bzme SOURCE2

* Tue Mar 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.48-1mdk
- new man-pages (dirfd.3, endfsent.3, getfsent.3, getfsfile.3,
  getfsspec.3, memrchr.3, setfsent.3, strtoll.3, strtoull.3, 
  vsyslog.3, urandom.4)
- typo fixes

* Thu Jan 03 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.47-1mdk
- new release

* Thu Nov 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.43-1mdk
- new release

* Sun Oct 21 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.42-1mdk
- change source url
- new release

* Mon Oct 15 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.41-2mdk
- re-compress patches
- new release
- readd missing files (jesse?)
- minor rpmlint fix

* Mon Oct 08 2001 Jesse Kuang <kjx@mandrakesoft.com> 1.40-2mdk
- rm man conflict with glibc-devel

* Sun Oct 07 2001 Jesse Kuang <kjx@mandrakesoft.com> 1.40-1mdk
- upgrade to 1.40

* Mon Sep 24 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.39-2mdk
- Really do the big move aka change locations in the hier.7 man page.

* Thu Jul 26 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.39-1mdk
- new release

* Wed Jun 27 2001 Francis Galiegue <fg@mandrakesoft.com> 1.38-3mdk

- Argh! Put in changelog this time
- Document the quad interpretation "feature" into inet(3)

* Tue Jun 12 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.38-1mdk
- Bump up to 1.38.

* Fri May 18 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.36-2mdk
- Remove the ldconfig.8 manpage.

* Fri May 18 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.36-1mdk
- Make a new and shiny RPM from a new and shiny source.
- Hide install output as it is really too disgusting to watch.

* Wed May 09 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.35-3mdk
- Add back the dl* manpages (used to conflict with ld.so package).

* Tue Mar 27 2001 Pixel <pixel@mandrakesoft.com> 1.35-2mdk
- remove the require locales-en (otherwise man-pages are only installed for
english installs)

* Mon Mar 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.35-1mdk
- 1.35.

* Mon Dec 25 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.34-1mdk
- new and shiny man-pages.

* Wed Dec 13 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.33-1mdk
- new version

* Mon Dec 11 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.32-1mdk
- untar filter with bzip2 the right way: use -j.
- new and shiny man-pages for everyone to read.

* Wed Dec  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.31-2mdk
- Remove diff manpages from here.

* Wed Aug 16 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.31-1mdk
- new release

* Tue Jul 25 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.30-4mdk
- fix permissions

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.30-3mdk
- build release for BM

* Tue Jun 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.30-2mdk
- Add URL
- Use mandir macros for FHS compatibilty

* Mon Jun 19 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.30-1mdk
- new release (1.30 : various fixes & a few more pages)
- suppress the tzet path which is now useless

* Wed Apr  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.29-4mdk
- Rebuild with the good spec-helper to remove orphan link to orphan
  man-page.

* Thu Mar 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>
- new group scheme
- spechelper

* Fri Mar 17 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 1.29-2mdk
- removed various pages that conflict with pages included in new
  rpm packages (ld.so and bind-utils)

* Wed Mar 08 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 1.29-1mdk
- 1.29 is out
- moved man1/{COPYING,README} to /usr/doc

* Fri Feb 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.28-3mdk
- Remove dir and vdir.1 (conflicts with last fileutils).

* Wed Jan 26 2000 Pablo Saratxaga <pablo@mandrakesoft.com>
- added humoristic man pages sex(6), baby(1) and guru(n).

* Mon Nov 29 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- 1.28

* Fri Nov 19 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- added requires locales-en (english man pages require english lang. support)
- added nice icon similar to other man-pages-* packages
- added obsoletes man9 (as we now include the man9 pages)

* Wed Aug 25 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 1.26
- add man9

* Thu Jul 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.25.

* Mon Jun 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 1.24 version.
- Removed some obsolete patchs.

* Mon May 24 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- remove fd.4 - we get a far more recent version from fdutils
