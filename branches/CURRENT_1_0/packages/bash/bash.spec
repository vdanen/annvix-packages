%define name	bash
%define version	2.05b
%define release	17avx

%define i18ndate 20010418

Summary:	The GNU Bourne Again shell (bash).
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
Patch0:		bash-2.03-paths.patch.bz2
Patch1:		bash-2.02-security.patch.bz2
Patch3:		bash-2.03-profile.patch.bz2
Patch4:		bash-2.05b-readlinefixes.patch.bz2
Patch5:		bash-2.04-requires.patch.bz2
Patch6:		bash-2.04-compat.patch.bz2
Patch7:		bash-2.04-shellfunc.patch.bz2
Patch8:		bash-2.05b-ia64.patch.bz2
Patch9:		bash-2.05-s390x-unwind.patch.bz2
Patch10:	bash-2.05-ipv6-20010418.patch.bz2
Patch51:	ftp://ftp.cwru.edu/pub/bash/bash-2.05b-patches/bash205b-001.bz2
Patch52:	ftp://ftp.cwru.edu/pub/bash/bash-2.05b-patches/bash205b-002.bz2
Patch53:	ftp://ftp.cwru.edu/pub/bash/bash-2.05b-patches/bash205b-003.bz2
Patch54:	ftp://ftp.cwru.edu/pub/bash/bash-2.05b-patches/bash205b-004.bz2
Patch55:	ftp://ftp.cwru.edu/pub/bash/bash-2.05b-patches/bash205b-005.bz2
Patch56:	ftp://ftp.cwru.edu/pub/bash/bash-2.05b-patches/bash205b-006.bz2
Patch57:	ftp://ftp.cwru.edu/pub/bash/bash-2.05b-patches/bash205b-007.bz2
Patch80:	bash-2.05b-builtins.patch.bz2
Patch81:	bash-2.05b-configure-destdir.patch.bz2
Patch90:	bash-2.05b-disable-nontrivial-matches.patch.bz2
#i18n
Patch100:	http://oss.software.ibm.com/developer/opensource/linux/patches/i18n/bash-2.05-%i18ndate.patch.bz2
Patch101:	http://oss.software.ibm.com/developer/opensource/linux/patches/i18n/bash-2.05-readline-%i18ndate.patch.bz2
Patch102:	http://oss.software.ibm.com/developer/opensource/linux/patches/i18n/bash-2.05-readline-i18n-0.4.patch.bz2
Patch103:	http://oss.software.ibm.com/developer/opensource/linux/patches/i18n/bash-2.05-i18n-0.5.patch.bz2
Patch1000:	bash-strcoll-bug.diff.bz2
Patch1002:	bash-2.05b-completion-fix.diff.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	autoconf2.5
BuildRequires:	byacc
BuildRequires:	libtermcap-devel

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
%setup -q -n bash-%{version} -a 1

%patch0 -p1 -b .paths
%patch1 -p1 -b .security
%patch3 -p1 -b .profile
%patch4 -p1 -b .readline
# 20020328 warly: integrated in mainstream
#%patch5 -p1 -b .requires
%patch6 -p1 -b .compat
# 20020328 warly
#%patch7 -p1 -b .shellfunc
%patch8 -p1 -b .ia64
%ifarch s390x
%patch9 -p1 -b .s390x
%endif
# 20020328 warly: integrated in mainstream
#%patch10 -p1 -b .ipv6
#%patch51 -p0 -b .pl1
#%patch52 -p0 -b .pl2
#%patch53 -p0 -b .pl3
#%patch54 -p0 -b .pl4
#%patch55 -p0 -b .pl5
#%patch56 -p0 -b .pl6

%patch51 -p0 -b .pl1
%patch52 -p0 -b .pl2
%patch53 -p0 -b .pl3
%patch54 -p0 -b .pl4
%patch55 -p0 -b .pl5
%patch56 -p0 -b .pl6
%patch57 -p0 -b .pl7

%patch80 -p0 -b .fix_so
%patch81 -p1 -b .destdir

%patch90 -p0

#%patch100 -p1 -b .i18n
#%patch101 -p1 -b .readline-i18n
#%patch102 -p1 -b .i18n
#%patch103 -p1 -b .readline-i18n

%patch1000 -p1 -b .strcoll_bugx
%patch1002 -p1 -b .cmplt

echo %{version} > _distribution
echo %{release} > _patchlevel
perl -p -i -e s/mdk// _patchlevel

%build
libtoolize --copy --force
%configure --disable-command-timing
%make -j1 CFLAGS="$RPM_OPT_FLAGS"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
#Sucks
chmod +w doc/texinfo.tex
mv doc/README .

# Take out irritating ^H's from the documentation
for i in `/bin/ls doc/` ; \
	do cat doc/$i > $i ; \
	cat $i | perl -p -e 's/.//g' > doc/$i ; \
	rm $i ; \
	done

mkdir -p $RPM_BUILD_ROOT/bin
pushd $RPM_BUILD_ROOT && mv usr/bin/bash bin/bash && popd
pushd $RPM_BUILD_ROOT/bin && ln -s bash sh && popd
pushd $RPM_BUILD_ROOT/bin && ln -sf bash bash2 && popd

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
install -m 644 builtins.1 $RPM_BUILD_ROOT%{_mandir}/man1/builtins.1

for i in `cat man.pages` ; do
  echo .so man1/builtins.1 > $RPM_BUILD_ROOT%{_mandir}/man1/$i.1
done

# now turn man.pages into a filelist for the man subpackage

cat man.pages |tr -s ' ' '\n' |sed '
1i\
%defattr(0644,root,root,0755)
s:^:%{_mandir}/man1/:
s/$/.1.bz2/
' > ../man.pages

perl -p -i -e 's!.*/(printf|export|echo|pwd|test|kill).1.bz2!!' ../man.pages

mkdir -p %buildroot/etc/skel
install -c -m644 %{SOURCE2} %buildroot/etc/skel/.bashrc
install -c -m644 %{SOURCE3}	%buildroot/etc/skel/.bash_profile
install -c -m644 %{SOURCE4}	%buildroot/etc/skel/.bash_logout
install -D -c -m755 %{SOURCE5} %buildroot/etc/profile.d/alias.sh

ln -s bash %buildroot/bin/rbash

# These're provided by other packages
rm -f %buildroot{%_infodir/dir,%_mandir/man1/{echo,export,kill,printf,pwd,test}.1}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files -f man.pages
%defattr(-,root,root)
%doc README CHANGES
%config(noreplace) /etc/skel/.b*
%config(noreplace) /etc/profile.d/alias.sh
/bin/rbash
/bin/bash
/bin/bash2
/bin/sh
%{_infodir}/bash.info*
%{_mandir}/man1/bash.1*
%{_mandir}/man1/builtins.1*
%{_mandir}/man1/bashbug.1*
%{_bindir}/bashbug


%changelog
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 2.05b-17avx
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
