#
# spec file for package bash
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		bash
%define version		3.0
%define release		%_revrel

%define i18ndate 	20010626

%define build_dietlibc	0

Summary:	The GNU Bourne Again shell (bash)
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Shells
License:	GPL
URL:		http://www.gnu.org/software/bash/bash.html

Source0:	ftp://ftp.gnu.org/pub/gnu/bash/bash-%{version}.tar.bz2
Source1:	ftp://ftp.gnu.org/pub/gnu/bash/bash-doc-%{version}.tar.bz2
Source2:	dot-bashrc
Source3:	dot-bash_profile
Source4:	dot-bash_logout
Source5:	alias.sh
Patch1:		bash-2.02-security.patch
Patch3:		bash-2.03-profile.patch
Patch4:		bash-2.05b-readlinefixes.patch
Patch6:		bash-2.04-compat.patch
Patch8:		bash-2.05b-ia64.patch
Patch9:		bash-2.05-s390x-unwind.patch
Patch13:	bash-2.05b-dietlibc.patch
Patch14:	bash-2.05b-waitpid-WCONTINUED.patch
Patch50:	ftp://ftp.cwru.edu/pub/bash/bash-2.05b-patches/bash30-001
Patch51:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-002
Patch52:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-003
Patch53:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-004
Patch54:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-005
Patch55:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-006
Patch56:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-007
Patch57:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-008
Patch58:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-009
Patch59:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-010
Patch60:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-011
Patch61:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-012
Patch62:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-013
Patch63:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-014
Patch64:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-015
Patch65:	ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/bash30-016
Patch80:	bash-2.05b-builtins.patch
Patch90:	bash-2.05b-disable-nontrivial-matches.patch
Patch1000:	bash-strcoll-bug.diff
Patch1003:	bash-2.05b-checkwinsize.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, bison, libtermcap-devel

Conflicts:	etcskel <= 1.63-11mdk, fileutils < 4.1-5mdk

%description
Bash is a GNU project sh-compatible shell or command language
interpreter. Bash (Bourne Again shell) incorporates useful features
from the Korn shell (ksh) and the C shell (csh). Most sh scripts
can be run by bash without modification.

Bash offers several improvements over sh, including command line
editing, unlimited size command history, job control, shell
functions and aliases, indexed arrays of unlimited size and 
integer arithmetic in any base from two to 64. Bash is ultimately
intended to conform to the IEEE POSIX P1003.2/ISO 9945.2 Shell and
Tools standard.


%prep
%setup -q -a 1
mv doc/README .

%patch1 -p1 -b .security
%patch3 -p1 -b .profile
%patch4 -p1 -b .readline
%patch6 -p1 -b .compat
%patch8 -p1 -b .ia64
%ifarch s390x
%patch9 -p1 -b .s390x
%endif

%patch13 -p1 -b .dietlibc
%patch14 -p1 -b .waitpid-WCONTINUED

%patch50 -p0 -b .pl1
%patch51 -p0 -b .pl2
%patch52 -p0 -b .pl3
%patch53 -p0 -b .pl4
%patch54 -p0 -b .pl5
%patch55 -p0 -b .pl6
%patch56 -p0 -b .pl7
%patch57 -p0 -b .pl8
%patch58 -p0 -b .pl9
%patch59 -p0 -b .pl10
%patch60 -p0 -b .pl11
%patch61 -p0 -b .pl12
%patch62 -p0 -b .pl13
%patch63 -p0 -b .pl14
%patch64 -p0 -b .pl15
%patch65 -p0 -b .pl16

%patch80 -p0 -b .fix_so

%patch90 -p0

%patch1000 -p1 -b .strcoll_bugx
%patch1003 -p1 -b .checkwinsize

echo %{version} > _distribution
echo %{release} > _patchlevel
perl -p -i -e s/avx// _patchlevel

# needed by P13
autoconf


%build
libtoolize --copy --force

# build statically linked bash with dietlibc
%if %{build_dietlibc}
# TODO: --enable-minimal-config?
mkdir bash-static
pushd bash-static
    export CFLAGS="%{optflags} -Os"
    export CONFIGURE_TOP=".."
    %configure2_5x \
        --disable-command-timing \
        --enable-dietlibc
#       --enable-separate-helpfiles \
#       --disable-nls
#       --enable-minimal-config \
    %make
popd
%endif

# build dynamically linked bash
mkdir bash-dynamic
pushd bash-dynamic
    export CFLAGS="%{optflags}"
    export CONFIGURE_TOP=".."
    %configure2_5x \
        --disable-command-timing
    %make CFLAGS="$RPM_OPT_FLAGS"
    # all tests must pass
    make check
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall -C bash-dynamic

rm -rf %{buildroot}%{_datadir}/locale/en@boldquot/ %{buildroot}%{_datadir}/locale/en@quot/

# Sucks
chmod +w doc/texinfo.tex
chmod 0755 examples/misc/aliasconv.*
chmod 0755 examples/misc/cshtobash
chmod 0755 %{buildroot}%{_bindir}/bashbug

# Take out irritating ^H's from the documentation
for i in `/bin/ls doc/` ; do perl -pi -e 's/.//g' doc/$i ; done

mkdir -p %{buildroot}/bin
pushd %{buildroot}/bin
    mv ..%{_bindir}/bash .
    ln -s bash sh
    ln -sf bash bash3
popd

%if %{build_dietlibc}
install -m 0755 bash-static/bash %{buildroot}/bin/bash-diet
%endif

# make manpages for bash builtins as per suggestion in DOC/README
cd doc
sed -e '
/^\.SH NAME/, /\\- bash built-in commands, see \\fBbash\\fR(1)$/{
/^\.SH NAME/d
s/^bash, //
s/\\- bash built-in commands, see \\fBbash\\fR(1)$//
s/,//g
b
}
d
' builtins.1 > man.pages
install -m 0644 builtins.1 %{buildroot}%{_mandir}/man1/builtins.1

for i in `cat man.pages` ; do
    echo .so man1/builtins.1 > %{buildroot}%{_mandir}/man1/$i.1
done

install -m 0644 rbash.1 %{buildroot}%{_mandir}/man1/rbash.1

# now turn man.pages into a filelist for the man subpackage

cat man.pages |tr -s ' ' '\n' |sed '
1i\
%defattr(0644,root,root,0755)
s:^:%{_mandir}/man1/:
s/$/.1.bz2/
' > ../man.pages

perl -p -i -e 's!.*/(printf|export|echo|pwd|test|kill).1.bz2!!' ../man.pages

mkdir -p %{buildroot}%{_sysconfdir}/{skel,profile.d}
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/skel/.bashrc
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/skel/.bash_profile
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/skel/.bash_logout
install -m 0755 %{SOURCE5} %{buildroot}%{_sysconfdir}/profile.d/alias.sh

ln -s bash %{buildroot}/bin/rbash

# These are provided by other packages
rm -f %{buildroot}{%{_infodir}/dir,%{_mandir}/man1/{echo,export,kill,printf,pwd,test}.1}

cd ..

install -m 0644 bash-dynamic/doc/bash.info %{buildroot}%{_infodir}/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f man.pages
%defattr(-,root,root)
%doc README CHANGES
%config(noreplace) %{_sysconfdir}/skel/.b*
%{_sysconfdir}/profile.d/alias.sh
/bin/rbash
/bin/bash
/bin/bash3
%if %{build_dietlibc}
/bin/bash-diet
%endif
/bin/sh
%{_infodir}/bash.info*
%{_mandir}/man1/bash.1*
%{_mandir}/man1/rbash.1*
%{_mandir}/man1/builtins.1*
%{_mandir}/man1/bashbug.1*
%{_bindir}/bashbug


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-5avx
- minor spec cleanups
- alias.sh is not a config file

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-4avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-3avx
- rebuild for new gcc
- drop unapplied patches

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-2avx
- bootstrap build

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-1avx
- 3.0
- BuildRequires: s/byacc/bison/ (stefan)
- P13: dietlibc support (gb)
- P12: fix builds with --enable-minimal-config (gb)
- P14: really check for WCONTINUED support in waitpid() calls (gb)
- look at user-defined colors in ~/.dir_colors and don't waste resources
  with DIR_COLORS if it exists (robert.vojta)
- spec cleanups

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.05b-17avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 2.05b-16sls
- remove %%build_opensls macro
- remove %%prefix
- minor spec cleanups

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 2.05b-15sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to exclude docs
- clean up the descriptions somewhat

* Mon Jul  7 2003 Warly <warly@mandrakesoft.com> 2.05b-14mdk
- really apply the patches (I sux)

* Mon Jul  7 2003 Warly <warly@mandrakesoft.com> 2.05b-13mdk
- add new patches

* Tue Jan 14 2003 Warly <warly@mandrakesoft.com> 2.05b-12mdk
- fix stupid typo

* Tue Jan 14 2003 Warly <warly@mandrakesoft.com> 2.05b-12dk
- ll is ls -l, not ls -l -k

* Sun Jan  5 2003 Stefan van der Eijk <stefan@eijk.nu> 2.05b-11mdk
- File CWRU/POSIX.NOTES was moved, added to %doc (thanks Charles)

* Sun Jan  5 2003 Stefan van der Eijk <stefan@eijk.nu> 2.05b-10mdk
- Remove CWRU/POSIX.NOTES from %%doc (file not found)

* Fri Nov 15 2002 Warly <warly@mandrakesoft.com> 2.05b-9mdk
- add new 2.05b patches

* Fri Nov 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.05b-8mdk
- fix build for new rpm

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.05b-7mdk
- fix bash-doc group
- alter a regexp to please vim spec mode

* Sat Aug 10 2002 Stefan van der Eijk <stefan@eijk.nu> 2.05b-6mdk
- BuildRequires

* Mon Aug 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.05b-5mdk
- fix command completion [P1002]

* Mon Aug 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.05b-4mdk
- fix segfault (readline patch was stolen) [P1001]

* Fri Jul 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.05b-2mdk
- gcc-3.2 rebuild
- rebuild with incore readline since applying the link patch to main readline
  may have strange side effects on other readline users

* Tue Jul 23 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.05b-2mdk
- rebuild with system readline lib

* Fri Jul 19 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.05b-1mdk
- new release
- drop arm patch
- rediff readline patch (well copied the one i just did on readline)
- rediff ia64 patch
- rediff patches 80, 81, 90

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.05a-5mdk
- Libtoolize to get updated config.{sub,guess}

* Sat Jun  1 2002 Stefan van der Eijk <stefan@eijk.nu> 2.05a-4mdk
- BuildRequires

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.05a-3mdk
- Automated rebuild in gcc3.1 environment

* Sun Mar 31 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.05a-2mdk
- disable stupid nontrivial matches (it prevented '/' from being appended
  to symlink-to-directory's)

* Thu Mar 28 2002 Warly <warly@mandrakesoft.com> 2.05a-1mdk
- new version

* Mon Feb 25 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-16mdk
- Remove DrakWM option (unused).

* Mon Nov 19 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-15mdk
- Add URL.
- Fix build with new makeinstall.

* Mon Oct 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-14mdk
- Fix rpmlint on spec file.

* Wed Oct 10 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.05-13mdk
- fix builtins man page

* Wed Oct 10 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-12mdk
- Move color_ls.sh from fileutils to alias.sh.

* Mon Oct 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.05-11mdk
- s!Linux Mandrake!Mandrake Linux!g

* Mon Sep 17 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-10mdk
- Make bash-doc requires bash (#5098).

* Sat Sep 15 2001 Pixel <pixel@mandrakesoft.com> 2.05-9mdk
- put back the alias cp="cp -i"

* Mon Sep 11 2001 David BAUDENS <baudens@mandrakesoft.com> 2.05-8mdk
- Remove cp to allow use of "cp -f"

* Thu Sep  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-7mdk
- Fix la and ll alias (#4744).

* Thu Aug  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-6mdk
- Don't link with libreadline to fix echo -n bugs (#4086).
- Merge with rh patches.

* Tue Jun 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-5mdk
- Add rbash link (flepied/charles).

* Mon May 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-4mdk
- Remove ~/.bash_alias from skel, readd the /etc/profile.d/alias.sh
  and add this semantic for loading :
	If exist a ~/.alias and the user hasn't specified a
	LOAD_SYSTEM_ALIAS variables then don't do any system aliases
	If there is no ~/.alias but the user has specified a
	IGNORE_SYSTEM_ALIASES then don't do any system aliases.

* Tue May 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-3mdk
- Add all /etc/skel/.bash* here and make ~/.bash_alias instead of
  /etc/profile.d/alias.
- Merge with rh patches.

* Tue May 01 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.05-2mdk
- Re-enable i18n patch.

* Mon Apr 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.05-1mdk
- 2.05 (disable i18n patch until i18n people come with an updated patch).

* Thu Mar 29 2001 Pixel <pixel@mandrakesoft.com> 2.04-18mdk
- re-add common mdk aliases
- fix bash_alias testing $CLASS = newbie, it should be beginner

* Sat Mar 03 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.04-17mdk
- Make sure to load /etc/profile all the time (CLE guy you have to find an
  workaround but don't disable feature).

* Mon Jan 15 2001 Geoffrey Lee <snailtalk@mandrkaesoft.com> 2.04-16mdk
- don't load /etc/profile all the time (Andrew Lee andrew@cle.linux.org.tw).

* Thu Dec 28 2000 Andrew Lee <andrew@linux.org.tw> 2.04-15mdk
- add i18n patch

* Tue Dec 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.04-14mdk
- Install as root.root the manpages.

* Tue Nov 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.04-13mdk
- Merge rh patch :
		- Fix ia64 build.
		- Fix compilation on older glibc-2.1.
- Put some files as noreplace.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.04-12mdk
- automatically added BuildRequires

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.04-11mdk
- BM

* Tue Jul 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.04-10mdk
- When we are in user newbie provide some wm alias like icewm => launch X
  and icewm (based on DrakWM parsing).

* Mon Jul 10 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.04-9mdk
- spec stephanazition (aka makeinstall cleaning :-) )
- use new macros

* Thu Jun 15 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.04-8mdk
- removed Prereq.

* Wed Jun 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.04-7mdk
- Don't do something to /etc/shells since /bin/sh should be always
  here, and clean-up the %post.

* Fri Jun  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.04-6mdk
- oops doesn't work with sash. Use Prereq instead.

* Fri Jun  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.04-5mdk
- make the %post and %postun use sash.

* Mon Jun  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.04-4mdk
- Fix alpha and unwind protect acess (debian).

* Sun Apr 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.04-3mdk
- Add ln bash2 to bash for rh compat.

* Fri Mar 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.04-2mdk
- Make bash link reative to sh.

* Wed Mar 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.04-1mdk
- Fix group for bash-doc.
- 2.04.

* Tue Mar 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.03-21mdk
- Fix build with spec-help.
- Upgrade groups.
- Spec clean-up.

* Thu Jan 20 2000 Pablo Saratxaga <pablo@mandrakesoft.com>
- fixed strcoll bug

* Mon Dec 27 1999 Pixel <pixel@mandrakesoft.com>
- added alias df in alias.sh

* Mon Dec 20 1999 Frederic Lepied <flepied@mandrakesoft.com> 2.03-18mdk

- /etc/bashrc calls /etc/profile.

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Remove ^chars from doc.
- Rewrote specs.

* Sun Aug 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Remove the alias to ls colors in bash_alias (doble with fileutils scripts).

* Fri Aug 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix wrong group in doc package.
- Increase version ;).

* Fri Aug 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix wrong man links (#20).

* Fri Jul 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
    - Ken Estes <kestes@staff.mail.com>
      - patch to detect what executables are required by a script.

* Wed Jul 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Remove 'DarkTiti' hack.

* Fri Jul 16 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- Make the `echo' builtin expand backslash-escaped characters by default,
  without requiring the `-e' option.  This makes the Bash `echo' behave
  more like the System V version.

* Tue Jul 9 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- french description

* Tue Jul 8 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- compiled against local libreadline (which is not compiled in now)
  => reduce the size of bash by 42%.
  Moreover, a part of its memory is shared with other readline programs (bc, ...)
- disable built-in time command (incompatible with standard POSIX time command)

* Tue May 25 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- handle RPM_OPT_FLAGS

* Sat May 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- alias.sh fix with the new syntax of bash2.

* Tue May 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fixing many stupid forget :-((

* Tue Apr 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Relifting of the doc-section.
- Moving the alias to a new files.

* Fri Apr  9 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- handle RPM_OPT_FLAGS
- add de locale
- add some aliases (ls=ls --color, md, rd, cd..) to bashrc
- fix download URLs
- make it compile if the release number contains non-digits
- We're NOT a %{arch}-redhat-linux

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- updated text in spec file.
- update to 2.03.

* Fri Feb 12 1999 Cristian Gafton <gafton@redhat.com>
- build it as bash2 instead of bash

* Tue Feb  9 1999 Bill Nottingham <notting@redhat.com>
- set 'NON_INTERACTIVE_LOGIN_SHELLS' so profile gets read

* Thu Jan 14 1999 Jeff Johnson <jbj@redhat.com>
- rename man pages in bash-doc to avoid packaging conflicts (#606).

* Wed Dec 02 1998 Cristian Gafton <gafton@redhat.com>
- patch for the arm
- use $RPM_ARCH-redhat-linux as the build target

* Tue Oct  6 1998 Bill Nottingham <notting@redhat.com>
- rewrite %pre, axe %postun (to avoid prereq loops)

* Wed Aug 19 1998 Jeff Johnson <jbj@redhat.com>
- resurrect for RH 6.0.

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- update to 2.02.1

* Thu Jun 11 1998 Jeff Johnson <jbj@redhat.com>
- Package for 5.2.

* Mon Apr 20 1998 Ian Macdonald <ianmacd@xs4all.nl>
- added POSIX.NOTES doc file
- some extraneous doc files removed
- minor .spec file changes

* Sun Apr 19 1998 Ian Macdonald <ianmacd@xs4all.nl>
- upgraded to version 2.02
- Alpha, MIPS & Sparc patches removed due to lack of test platforms
- glibc & signal patches no longer required
- added documentation subpackage (doc)

* Fri Nov 07 1997 Donnie Barnes <djb@redhat.com>
- added signal handling patch from Dean Gaudet <dgaudet@arctic.org> that
  is based on a change made in bash 2.0.  Should fix some early exit
  problems with suspends and fg.

* Mon Oct 20 1997 Donnie Barnes <djb@redhat.com>
- added %clean

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- added comment explaining why install-info isn't used
- added mips patch 

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc
