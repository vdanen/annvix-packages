%define name	xterm
%define version	179
%define release	4avx

Summary:	The standard terminal emulator for the X Window System
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Terminals
URL:		http://dickey.his.com/xterm
Source0:	ftp://dickey.his.com/xterm/%name-%version.tar.bz2
Patch1:		xterm-172-alt-meta-mod.patch.bz2
Patch2:		xterm-177-biarch-utmp.patch.bz2

BuildRoot:	%_tmppath/%name-%version-buildroot
BuildRequires:	XFree86-devel libtermcap-devel

Conflicts:	XFree86 < 3.3.6-13mdk
Prereq:		/usr/sbin/update-alternatives

%description
The XTerm program is the standard terminal emulator for the X Window System. It
provides DEC VT102/VT220 and Tektronix 4014 compatible terminals for programs
that can't use the window system directly. If the underlying operating system
supports terminal resizing capabilities (for example, the SIGWINCH signal in
systems derived from 4.3bsd), xterm will use the facilities to notify programs
running in the window whenever it is resized.

%prep
%setup -q
%patch1 -p1 -b .alt-meta-mod
%patch2 -p1 -b .biarch-utmp

%build
%configure --enable-wide-chars

make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
r=$RPM_BUILD_ROOT
make install appsdir=$r/usr/X11R6/lib/X11/app-defaults bindir=$r/usr/X11R6/bin  mandir=$r/usr/X11R6/man/man1 

# NOTE: encodingMode: locale means to follow the charset encoding of the
# locale.i A quite complete unicode font is set as the default (instead of the
# very poor "fixed" one). a quick cat is used instead of patching the sources;
# it shoulmd be made the default imho -- pablo
cat << EOF >> $r/usr/X11R6/lib/X11/app-defaults/XTerm
*.vt100.font: -misc-fixed-medium-r-normal--15-140-75-75-c-90-iso10646-1
*.vt100.encodingMode: locale
*.PtyInitialErase: on
*.backarrowKeyIsErase: on
EOF

## strange, if xterm isn't launched with -name xxxx parameter it doesn't
## take in account the ressources --> wrong font in unicode mode --> segfault
## there is not time to fix the sources; using a script to ensure there
## is always a -nae xxxx used
mv $RPM_BUILD_ROOT/usr/X11R6/bin/xterm $RPM_BUILD_ROOT/usr/X11R6/bin/xterm.real
cat << EOF >> $r/usr/X11R6/bin/xterm
#!/bin/bash

if echo "\$@" | grep -- '-name' >&/dev/null ; then
	 exec /usr/X11R6/bin/xterm.real "\$@"
else exec /usr/X11R6/bin/xterm.real -name Terminal "\$@"
fi
EOF
chmod a+rx $r/usr/X11R6/bin/xterm

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AAA_README_VMS.txt MANIFEST README README.os390
%_prefix/X11R6/bin/*
%_prefix/X11R6/man/*/*
%_prefix/X11R6/lib/X11/app-defaults/*

%changelog
* Fri Jun 18 2004 Vincent Danen <vdanen@annvix.org> 179-4avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 179-3sls
- minor spec cleanups
- remove menu entry and icons

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 179-2sls
- OpenSLS build
- tidy spec

* Wed Jul 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 179-1mdk
- new release

* Tue Apr 29 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 177-6mdk
- really fix #3680

* Tue Apr 15 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 177-5mdk
- %%post / %%postun scripts do fail when update-alternatives got mad

* Mon Apr 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 177-4mdk
- Patch4: Handle biarch struct utmp

* Mon Apr 07 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 177-3mdk
- fix #3683

* Mon Apr 07 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 177-2mdk
- force install ordering for post-scripts (#3680)

* Wed Mar 26 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 177-1mdk
- new release

* Sat Feb  8 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 172-3mdk
- Don't screwd the Shift-Letter stuff make a new meta-alt patch much
  cleaner.

* Fri Jan 17 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 172-2mdk
- Fix meta-alt patch to make actually works.

* Thu Jan 16 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 172-1mdk
- Release 172
- Rebuild against latest XFree 4.2.99 to get real Xft support
- Convert Requires into Conflicts
- Remove patches 1 & 2 (merged upstream)

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 170-2mdk
- build release

* Tue Nov 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 170-1mdk
- new release
- rediff patch 0
- spec cleaning
- merge SOURCES 1, 2 & 3 icons into a tarball, which simplify %%install
- better summary
- menu entry: automatically reuse package group & summary

* Tue May 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 166-1mdk
- new release

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 165-4mdk
- Automated rebuild in gcc3.1 environment

* Tue Jan 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 165-3mdk
- spec clean
- xpm to png icons conversion

* Tue Jan 22 2002 David BAUDENS <baudens@mandrakesoft.com> 165-2mdk
- Rebuild

* Sun Jan 20 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 165-1mdk
- 165 all new out for general consumption.

* Wed Dec 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 164-1mdk
- First attempt at 164.

* Thu Oct 11 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 161-1mdk
- new release
- sanitize

* Thu Sep 18 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 156-7mdk
- ensure that -name parameter is used (otherwise it segfaults)

* Fri Sep 14 2001 Pixel <pixel@mandrakesoft.com> 156-6mdk
- fix segfault when no LANG
- fix backspace in cooked mode (eg: insert mode vim-minimal)

* Tue Sep 13 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 156-5mdk
- change command line from menu file so it is launched with suitable
  parameters

* Mon Aug 06 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 156-4mdk
- build release

* Wed May 09 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 156-3mdk
- actually enabled support for use of locales and bidi

* Tue May 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 156-2mdk
- add bidirectional support (ie for semitic languages)

* Tue May 01 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 156-1mdk
- new release
- fix render test

* Mon Apr 23 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 155-1mdk
- newrelease

* Thu  Apr 12 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 154-1mdk
- New and shiny 154 bumped into cooker.

* Sat Mar 31 2001 Frederic Lepied <flepied@mandrakesoft.com> 152-3mdk
- enable unicode

* Thu Mar 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 152-2mdk
- recompiled to activate the Render extension.

* Thu Mar 15 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 152-1mdk
- new release

* Mon Mar 12 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 151-1mdk
- new version

* Thu Feb  8 2001 Pixel <pixel@mandrakesoft.com> 150-2mdk
- add as alternative xvt

* Sun Dec 31 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 150-1mdk
- new and shiny source.

* Tue Dec 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 149-1mdk
- Fix compilation with last XFree.
- 149.

* Thu Nov 16 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 148-1mdk
- new release

* Fri Aug 25 2000 David BAUDENS <baudens@mandrakesoft.com> 144-2mdk
- Fix Menu entry (fix name, add longtitle and provide icons)
- Fix Sumary and Description
- Fix %%doc

* Thu Aug 24 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 144-1mdk
- s|143|144|.

* Mon Aug 21 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 143-1mdk
- new and shiny version.

* Sun Aug 20 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 142-1mdk
- even more use of the _menudir macro.
- a new and shiny version.

* Thu Aug 17 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 141-2mdk
- fix usage of macro before its definition: you don't get any chickens before
  they hatch.!

* Tue Aug 15 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 141-1mdk
- s|140|141|.

* Tue Aug 08 2000 Frederic Lepied <flepied@mandrakesoft.com> 140-2mdk
- automatically added BuildRequires

* Mon Jul 24 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 140-1mdk
- more macros (_menudir and the like : geoffroy sucks:-) )
- new release

* Mon Jul 24 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 139-2mdk
- fix silly typo in summary

* Sat Jul 22 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 139-1mdk
- xterm source has moved
- new version
- some macro-ization

* Fri May  5 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 131-4mdk
- remove full path of icon in menu entry

* Tue Apr  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 131-3mdk
- Set menu in /Terminals.

* Sat Apr  1 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 131-2mdk
- Requires: XFree86 >= 3.3.6-13mdk to avoid conflicts.

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 131-1mdk
- Menu.
- First version.
- Fix meta-alt keys (Hey hey fred ;)).

# end of file
