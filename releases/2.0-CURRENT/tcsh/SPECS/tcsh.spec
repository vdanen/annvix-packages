#
# spec file for package tcsh
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		tcsh
%define version		6.14
%define release		%_revrel
%define rversion	%{version}.00

Summary:	An enhanced version of csh, the C shell
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Shells
URL:		http://www.tcsh.org/
Source:		ftp://ftp.funet.fi/pub/unix/shells/tcsh/tcsh-%{version}.00.tar.bz2
Source1:	alias.csh
Patch1:		tcsh-6.09.00-termios.patch
Patch3:		tcsh-6.14.00-lsF.patch
Patch4:		tcsh-6.14.00-dashn.patch
Patch5:		tcsh-6.14.00-read.patch
Patch6:		tcsh-6.10.00-glibc_compat.patch
Patch7:		tcsh-6.14.00-getauthuid-is-not-in-auth_h.patch

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtermcap-devel groff-for-man

Provides:	csh = %{version}
Requires(post):	rpm-helper
Requires(postun): rpm-helper

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell.  Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{rversion}
%patch1 -p1 -b .termios
%patch3 -p1 -b .lsF
%patch4 -p1 -b .dashn
%patch5 -p1 -b .read
%patch6 -p1 -b .glibc_compat
%patch7 -p1


%build
%configure \
    --bindir=/bin \
    --without-hesiod
%make
nroff -me eight-bit.me > eight-bit.txt


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man1 %{buildroot}/bin
install -s tcsh %{buildroot}/bin/tcsh
install -m 0644 tcsh.man %{buildroot}%{_mandir}/man1/tcsh.1
ln -s tcsh.1 %{buildroot}%{_mandir}/man1/csh.1
ln -sf tcsh %{buildroot}/bin/csh

mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
install %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/$(basename %{SOURCE1})


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
/usr/share/rpm-helper/add-shell %{name} $1 /bin/csh
/usr/share/rpm-helper/add-shell %{name} $1 /bin/tcsh

%postun
/usr/share/rpm-helper/del-shell %{name} $1 /bin/csh
/usr/share/rpm-helper/del-shell %{name} $1 /bin/tcsh


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/profile.d/*
/bin/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc NewThings FAQ Fixes eight-bit.txt complete.tcsh
%doc Ported README* WishList Y2K


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.14
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.14
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.14
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.14-1avx
- 6.14
- drop P0, P5, P7
- P3, P4, new P5: from fedora
- build eight-bit.txt in build stage (pixel)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.12-11avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.12-10avx
- rebuild

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 6.12-9avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 6.12-8sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 6.12-7sls
- OpenSLS build
- tidy spec

* Tue Jul 29 2003 Pixel <pixel@mandrakesoft.com> 6.12-6mdk
- fix patch dspmbyte which was completly dumb/broken/...
  now dspmbyte is only set for kanji locales as expected
  (bug #4360)

* Mon May 12 2003 Pixel <pixel@mandrakesoft.com> 6.12-5mdk
- apply patches from redhat to enable dspmbyte (bug #3909)

* Wed Feb 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.12-4mdk
- Rebuild, let it link against ncurses

* Tue Nov 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.12-3mdk
- Prereq: rpm-helper >= 0.7
- use {add,del}-shell
- requires s/fileutils/coreutils
- rpmlint fixes

* Tue Aug 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.12-2mdk
- Fix Patch0 (utmp) for 6.12.00

* Fri Aug  2 2002 Pixel <pixel@mandrakesoft.com> 6.12-1mdk
- new release

* Fri Jun 14 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 6.11-5mdk
- Add groff-for-man as BuildRequires.

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.11-4mdk
- Automated rebuild in gcc3.1 environment

* Thu Oct 11 2001 Pixel <pixel@mandrakesoft.com> 6.11-3mdk
- fix rights on alias.csh

* Wed Oct 10 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.11-2mdk
- Add alias.csh which is the color_ls.csh from fileutils.

* Fri Oct  5 2001 Pixel <pixel@mandrakesoft.com> 6.11-1mdk
- new version

* Thu Sep  6 2001 Pixel <pixel@mandrakesoft.com> 6.10-4mdk
- rebuild

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 6.10-3mdk
- Use %%{_buildroot} for BuildRoot

* Mon Mar 12 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 6.10-2mdk
- fix build on glibc22 due to more strict glibc 2.2.2 headers
- more docs

* Tue Nov 21 2000 Pixel <pixel@mandrakesoft.com> 6.10-1mdk
- new version

* Mon Nov 13 2000 Pixel <pixel@mandrakesoft.com> 6.09.04-1mdk
- new version

* Wed Nov  8 2000 Pixel <pixel@mandrakesoft.com> 6.09.03-5mdk
- add man page for csh.1 (link to tcsh.1)

* Tue Nov  7 2000 Pixel <pixel@mandrakesoft.com> 6.09.03-4mdk
- nicer %%post scripts

* Tue Nov  7 2000 Pixel <pixel@mandrakesoft.com> 6.09.03-3mdk
- change the suffix of /etc/shells temporary file to remove rpmlint error

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 6.09.03-2mdk
- automatically added BuildRequires

* Thu Jul 27 2000 Pixel <pixel@mandrakesoft.com> 6.09.03-1mdk
- new version

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 6.09.02-2mdk
- _mandir ization
- BM

* Thu Jul  6 2000 Pixel <pixel@mandrakesoft.com> 6.09.02-1mdk
- new version (cleanup of patches)

* Fri Jun 16 2000 Pixel <pixel@mandrakesoft.com> 6.09-4mdk
- new version
- merge with redhat

* Sat Mar 25 2000 Pixel <pixel@mandrakesoft.com> 6.08.00-9mdk
- new group + cleanup

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies

* Thu Jan 27 2000 Jeff Johnson <jbj@redhat.com>
- append entries to spanking new /etc/shells.

* Mon Jan 10 2000 Jeff Johnson <jbj@redhat.com>
- update to 6.09.
- fix strcoll oddness (#6000, #6244, #6398).

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with rh.
- Fix $shell to use --bindir(r)

* Sat Sep 25 1999 Michael K. Johnson <johnsonm@redhat.com>
- fix $shell by using --bindir

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- fix handling of RPM_OPT_FLAGS

* Wed Feb 24 1999 Cristian Gafton <gafton@redhat.com>
- patch for using PATH_MAX instead of some silly internal #defines for
  variables that handle filenames.

* Fri Nov  6 1998 Jeff Johnson <jbj@redhat.com>
- update to 6.08.00.

* Fri Oct 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 6.07.09 from the freebsd
- security fix

* Wed Aug  5 1998 Jeff Johnson <jbj@redhat.com>
- use -ltermcap so that /bin/tcsh can be used in single user mode w/o /usr.
- update url's

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 6.07; added BuildRoot
- cleaned up the spec file; fixed source url

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- added termios hacks for new glibc
- added /bin/csh to file list

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>
 - Provides csh, adds and removes /bin/csh from /etc/shells if csh package
isn't installed.
