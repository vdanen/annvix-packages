#
# spec file for package vim
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# Notes / Warning :
# - this package is not prefixable
# - to update official patches, aka SOURCE4, see README.mdk in SOURCE4
#
# $Id$

%define revision	$Rev$
%define name		vim
%define version		7.0
%define release		%_revrel

%define patch_level	1
%define localedir	%{buildroot}%{_datadir}/locale/

%define perl_version	%(rpm -q --qf '%%{epoch}:%%{version}' perl)

Summary:	VIsual editor iMproved 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Charityware
Group:		Editors
URL:		http://www.vim.org
Source0:	ftp://ftp.vim.org/pub/vim/unix//%{name}-%{version}.tar.bz2
Source2:	ftp://ftp.vim.org/pub/vim/unix//extra/%{name}-%{version}-lang.tar.bz2
Source4:	vim-%{version}.%{patch_level}-patches.tar.bz2
# http://vim.sourceforge.net/scripts/script.php?script_id=98
Source5:	vim-spec-3.0.tar.bz2
# MDK patches
Patch2:		vim-5.6a-paths.patch
Patch3:		vim-6.4-mdk-rpm-spec-syntax.patch
Patch8:		vim-6.0af-man-path.patch
Patch10:	xxd-locale.patch
Patch11:	vim-6.2-gcc31.patch
Patch20:	vimrc_hebrew.patch
Patch22:	vim-6.1-fix-xterms-comments.patch
Patch23:	vim-6.3-remove-docs.patch
Patch24:	vim-6.1-outline-mode.patch 
Patch25:	vim-6.1-xterm-s-insert.patch 
Patch26:	vim-7.0-mdk-changelog-mode.patch
Patch27:	vim-6.1-rpm42.patch
Patch28:	vim-6.4-mdk-po-mode.patch
Patch29:	vim-7.0-mdk-po-buildfix.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel, python-devel, termcap-devel, acl-devel

%description
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-common package
contains files which every VIM binary will need in order to run.


%package common
Summary:	The common files needed by any version of the VIM editor
Group:		Editors
Requires:	perl = %{perl_version}
Requires(pre):	coreutils
Requires(preun): coreutils
Requires(post):	coreutils
Requires(postun): coreutils

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-common package
contains files which every VIM binary will need in order to run.


%package minimal
Summary:	A minimal version of the VIM editor
Group:		Editors
Provides:	vim
Requires(post):	/usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-minimal package
includes a minimal version of VIM, which is installed into /bin/vi for use
when only the root partition is present.


%package enhanced
Summary:	A version of the VIM editor which includes recent enhancements
Group:		Editors
Requires:	vim-common >= %{version}
Obsoletes:	vim-color
Provides:	vim vim-color
Requires(post):	/usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-enhanced package
contains a version of VIM with extra, recently introduced features like
Python and Perl interpreters.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -b 2 -n vim70 -a4
# spec plugin
rm -f runtime/doc/pi_spec.txt
rm -f runtime/ftpplugin/spec.vim
tar tjf %{SOURCE5} -C runtime
#official patches
for i in vim-%{version}.%{patch_level}-patches/%{version}*; do
    patch -p0 -s < $i
done

#mdk patches
%patch2 -p1
%patch3 -p0 -b .spec
%patch8 -p1 -b .manpath
%patch10 -p1 -b .xxdloc
%patch11 -p1 -b .gcc31
%patch20 -p1 -b .warly
%patch22 -p0
%patch23 -p0 -b .doc
%patch24 -p0
%patch25 -p0
%patch26 -p0
%patch27 -p0
%patch28 -p0
%patch29 -p0

perl -pi -e 's|SYS_VIMRC_FILE "\$VIM/vimrc"|SYS_VIMRC_FILE "%{_sysconfdir}/vim/vimrc"|' src/os_unix.h
# disable command echo
perl -pi -e 's|^set showcmd|set noshowcmd|' runtime/vimrc_example.vim
perl -pi -e 's|\Qsvn-commit.*.tmp\E|svn-commit*.tmp|' ./runtime/filetype.vim


%build
# First build: vim-enhanced

CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"  ./configure \
    --prefix=%{_prefix} \
    --enable-acl \
    --enable-pythoninterp \
    --enable-perlinterp \
    --with-features=huge \
    --libdir=%{_libdir} \
    --with-compiledby="%{packager}" \
    --with-x=no \
    --enable-gui=no \
    --disable-gpm \
    --exec-prefix=%{_prefix}

make
mv src/vim src/vim-enhanced
make -C src/ clean

# Second build: vim-minimal
CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" ./configure  \
    --prefix=%{_prefix} \
    --with-features=tiny \
    --disable-tclinterp \
    --disable-cscope \
    --disable-multibyte \
    --disable-hangulinput \
    --disable-xim \
    --disable-fontset \
    --disable-gui \
    --disable-acl \
    --disable-pythoninterp \
    --disable-perlinterp \
    --libdir=%{_libdir} \
    --with-compiledby="%packager" \
    --with-x=no \
    --enable-gui=no \
    --exec-prefix=%{_prefix} \
    --with-tlib=termcap \
    --disable-gpm

make
cp src/vim src/vim-minimal
make -C src

cp -al runtime/doc doc
# apply os_doc.diff
pushd doc
    rm -f *.1
    rm -f os_{390,dos,msdos,risc,win32,amiga,mac,os2,beos,mint,qnx,vms}.txt
    rm -f gui_{w16,w32}.txt
    rm -f vim2html.pl Makefile *awk
popd

# britton support
ln -s tutor.fr runtime/tutor/tutor.br
ln -s menu_fr_fr.iso_8859-15.vim runtime/lang/menu_br


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

[ ! -e annvix ] && mv vim-%{version}.%{patch_level}-patches annvix

perl -pi -e 's!LOCALEDIR=\$\(DEST_LANG\)!LOCALEDIR=\$(DESTDIR)\$\(prefix\)/share/locale!g' src/Makefile

mkdir -p %{buildroot}{/bin,%{_bindir},%{_datadir}/{vim,locale},%{_mandir}/man1,%localedir}
%makeinstall_std VIMRTDIR=""


make -C src installmacros prefix=%{buildroot}%{_prefix} VIMRTDIR=""

install -s -m 0755 src/vim-enhanced %{buildroot}%{_bindir}
install -s -m 0755 src/vim-minimal %{buildroot}/bin/vim-minimal

pushd %{buildroot}
    rm -f ./bin/rvim
    for i in ex vimdiff; do
        ln -sf vim-enhanced ./usr/bin/$i
    done
    rm -f ./usr/man/man1/rvim.1.bz2
popd

# installing man pages
for i in %{buildroot}%{_mandir}/man1/{vi,rvi}; do
    cp %{buildroot}%{_mandir}/man1/vim.1 $i.1
done

ln -sf vimrc_example.vim %{buildroot}/usr/share/vim/vimrc

pushd %{buildroot}/%{_prefix}/share/vim/tools
    # i need to make a choice :(.
    rm -f vim132
    perl -p -i -e 's|#!/usr/bin/nawk|#!/usr/bin/gawk|' mve.awk
    perl -p -i -e 's|#!/usr/local/bin/perl|#!/usr/bin/perl|' *.pl
    perl -p -i -e 's|#!/usr/gnu/bin/perl|#!/usr/bin/perl|' *
popd
 
# Be short-circuit aware :
ln -f runtime/macros/README.txt README_macros.txt
ln -f runtime/tools/README.txt README_tools.txt
perl -p -i -e "s|#!/usr/local/bin/perl|#!/usr/bin/perl|" runtime/doc/*.pl

# fix the paths in the man pages
for i in %{buildroot}/usr/share/man/man1/*.1; do
    perl -p -i -e "s|%{buildroot}||" $i
done

# prevent including twice the doc
rm -fr %{buildroot}/usr/share/vim/doc
ln -sf ../../../%{_defaultdocdir}/%{name}-common-%{version}/doc %{buildroot}/usr/share/vim/doc

# but first delete some uncommon locale files
rm -rf %{buildroot}%{_datadir}/locale/zh_{TW,CN}.UTF-8*

# and delete unwanted translated manpages
rm -rf %{buildroot}%{_mandir}/{it,pl,fr,ru}*

# symlink locales in right place so that %find_land put needed %lang:
# see %pre common why this is needed
pushd %{buildroot}%{_datadir}/vim/lang
    ln -s ../../locale/* .
popd

rm -f %{buildroot}%{_bindir}/{rview,view,rvim}

%find_lang %{name}

find %{buildroot}%{_datadir}/vim/ -name "tutor.*" | egrep -v 'tutor(|\.vim)$' |
     sed -e "s^%{buildroot}^^" -e 's!^\(.*tutor.\)\(..\)!%lang(\2) \1\2!g' >> %{name}.lang

find %{buildroot}%{_datadir}/vim/ -name "menu*" |
    sed -e "s^%{buildroot}^^" -e 's!^\(.*menu_\)\(..\)\(_\)!%lang(\2) \1\2\3!g' \
        -e 's!^\(.*menu\)\(_chinese\)!%lang(zh) \1\2!g' \
        -e 's!^\(.*menu\)\(_czech_\)!%lang(cs) \1\2!g' \
        -e 's!^\(.*menu\)\(_french\)!%lang(fr) \1\2!g' \
        -e 's!^\(.*menu\)\(_german\)!%lang(de) \1\2!g' \
        -e 's!^\(.*menu\)\(_japanes\)!%lang(ja) \1\2!g' \
        -e 's!^\(.*menu\)\(_polish\)!%lang(pl) \1\2!g' \
        -e 's!^\(.*menu\)\(_slovak\)!%lang(sk) \1\2!g' \
        -e 's!^\(.*menu\)\(_spanis\)!%lang(es) \1\2!g' \
    >> %{name}.lang
rm -f %{buildroot}%{_bindir}/vim

rm -f %{buildroot}%{_mandir}/man1/evim.1*

mkdir -p %{buildroot}%{_sysconfdir}/vim
cat << EOF >> %{buildroot}%{_sysconfdir}/vim/vimrc
" Place your system-wide modifications here.
" %{_datadir}/vim/ files are overwritten on package update.

source %{_datadir}/vim/vimrc
EOF


%pre common
# This is needed since locales have been moved to /usr/share/locale
# thus enabling us to install only requested locales
# the problem is that vim look for anything in %{_datadir}/vim/lang
# So we've to symlink locales there
# But to prevent update faillure, we must first be sure a link
# creation won't fail because old directory is still there
if test -d %{_datadir}/vim/lang -a ! -L %{_datadir}/vim/lang
then rm -fr %{_datadir}/vim/lang
else rm -f %{_datadir}/vim/lang
fi


%post minimal
update-alternatives --install /usr/bin/vi uvi /bin/vim-minimal 10
update-alternatives --install /bin/vi     vi  /bin/vim-minimal 10
update-alternatives --install /bin/vim    vim /bin/vim-minimal 10
for i in view ex rvi rview rvim; do
    update-alternatives --install /bin/$i $i /bin/vi 10 || :
done
:


%postun minimal
[ $1 = 0 ] || exit 0
update-alternatives --remove uvi /usr/bin/vim-minimal
update-alternatives --remove vi  /bin/vim-minimal
update-alternatives --remove vim /bin/vim-minimal

for i in view ex rvi rview rvim; do
    update-alternatives --remove $i /bin/$i || :
done
:


%post enhanced
update-alternatives --install /usr/bin/vi uvi /usr/bin/vim-enhanced 20
update-alternatives --install /bin/vi  vi     /usr/bin/vim-enhanced 20
update-alternatives --install /bin/vim vim    /usr/bin/vim-enhanced 20
:


%postun enhanced
[ $1 = 0 ] || exit 0
update-alternatives --remove uvi /usr/bin/vim-enhanced
update-alternatives --remove vi  /usr/bin/vim-enhanced
update-alternatives --remove vim /usr/bin/vim-enhanced
:


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files common -f vim.lang
%defattr(-,root,root)
%dir %{_datadir}/vim/
%{_datadir}/vim/*
%{_datadir}/vim/doc
%{_mandir}/man1/vim.1*
%{_mandir}/man1/ex.1*
%{_mandir}/man1/vi.1*
%{_mandir}/man1/view.1*
%{_mandir}/man1/rvi.1*
%{_mandir}/man1/rview.1*
%{_mandir}/man1/vimdiff.1*
%{_mandir}/man1/vimtutor.1*
%{_mandir}/man1/rvim.1*
%{_mandir}/man1/xxd.1*
%{_bindir}/xxd
%{_bindir}/vimtutor
#%exclude %{_bindir}/rview
#%exclude %{_bindir}/rvim
#%exclude %{_bindir}/view
%dir %{_sysconfdir}/vim
%config(noreplace) %{_sysconfdir}/vim/vimrc

%files minimal
%defattr(-,root,root)
/bin/vim-minimal

%files enhanced
%defattr(-,root,root)
%{_bindir}/vim-enhanced
%{_bindir}/ex
%{_bindir}/vimdiff

%files doc
%doc README*.txt runtime/termcap
%doc --parents annvix/README*
%doc doc


%changelog
* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.0
- 7.0; patchlevel 1
- added P9
- updated P26
- BuildRequires: acl-devel; enable ACL support for vim-enhanced
- add -doc subpackage
- build against perl 5.8.8
- drop P31

* Wed Jan 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.4
- 6.4; patchlevel 1
- updated P3, P28 from Mandriva
- fix prereq
- remove useless triggers
- adapt P31 as tcltags is no longer shipped
- delete some uncommon locale files

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.3
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.3
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.3
- Obfuscate email addresses and new tagging
- Uncompress patches
- make S5 look like the tar file it is

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-6avx
- update to patchlevel 86
- update spec mode to 3.0
- fix perl version eval (nanardon)
- fix svn commit file detection (misc)
- BuildRequires: python-devel
- rebuild against new python and new perl
- drop S3; unused menu entry

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-4avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-3avx
- rebuild against new python

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-2avx
- rebuild against new perl

* Tue Feb 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-1avx
- 6.3; patchlevel 54
- S5: spec mode from Guillaume Rousse
- use a system-wide configfile in /etc/vim/ (misc)
- drop P29
- remove evim manpage, add rview symlink (bluca)
- disable command echo by default
- drop P30 (applied upstream)
- spec cosmetics

* Tue Feb 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.2-16avx
- P30: fix for CAN-2004-1138
- P31: fix for CAN-2005-0069

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 6.2-15avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 6.2-14sls
- minor spec cleanups

* Mon Jan 12 2004 Vincent Danen <vdanen@opensls.org> 6.2-13sls
- remove %%build_opensls tags

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 6.2-12sls
- OpenSLS build
- don't build vim-x11 (use %%build_opensls macro)
- don't enable gpm support in vim-enhanced

* Thu Sep 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.2-11mdk
- fix buildrequires for 64bit ports
- update up to official patchlevel 72: using foldlevel() in 'foldexpr' cannot
  get level of prev. line

* Wed Sep 03 2003 David Baudens <baudens@mandrakesoft.com> 6.2-10mdk
- Don't wrap in spec mode (long lines can be usefull and wrap was badly
  done)

* Wed Aug 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.2-9mdk
- patch 29: update spec mode to guillaume rousse one (fix error when editing
  spec file in the same buffer, add support for rpmlint and the like)
  [frederic crozat request]

* Mon Aug 18 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.2-8mdk
- update up to official patchlevel 71:
  o ":command -range=" doesn't give an error message
  o ":options" causes a couple of errors
  o ":windo 123" only updates other windows when entering them
  o GUI: shift-left-click scrolls text instead of doing "*"
  o Netbeans: file name with special characters causes trouble
  o a couple of messages are not translated
  o backslash in trail byte doesn't work inside strings
  o compiling with both netbeans and workshop doesn't work
  o confusing error message for ":au" about wrong event name
  o crash when 'autochdir' is set and buffer has no name
  o crash while starting up when using +xsmp feature
  o cscope may kill wrong process
  o limit for nr of items in 'statusline' is too low
  o missing prototype for sigaltstack()
  o obtaining the '( mark changes the '' mark
  o part of window not updated after listing completions
  o prototype for bzero() differs from what most systems use
  o redraw error when searched text starts with composing char
  o resolve() only does one symlink; add the simplify() function
  o syntax highlighting wrong when using "containedin"
  o the Ruby interface doesn't work with Ruby 1.8
  o the lpc filetype was never recognized
  o using remote server may cause memory to leak
  o various compiler warnings
  o when using "\=submatch(0)" in ":s" line breaks become NUL
  o when using custom completion end up with no matches
  o with error in function arguments the function is still called
  o wrong result when using col('.') after CTRL-O in Insert mode

* Wed Aug 13 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.2-7mdk
- BuildRequires: libtermcap-devel

* Fri Aug 08 2003 Frederic Lepied <flepied@mandrakesoft.com> 6.2-6mdk
- python 2.3

* Wed Jul 09 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.2-5mdk
- fix vimtutor not availlable (Buchan Milne)

* Sun Jul 06 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.2-4mdk
- vim-X11: use gnome widgets too
- update up to official patchlevel 21:
  o (lang) Portugese menu contains a split line
  o Unix: may need to press a key when reading from stdin
  o small problems with cscope, also on Win32
  o test 11 sometimes prompts the user for a changed file
  o the "Syntax/Set syntax only" menu item causes an error message
  o the +xsmp feature is never enabled
  o the user manual section on exceptions contains small mistakes

* Wed Jul 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.2-3mdk
- vim-common: pre-requires coreutils (really fix #3411)
- update up to official patchlevel 14:
  o small problems with cscope, also on Win32
  o test 11 sometimes prompts the user for a changed file
  o the +xsmp feature is never enabled

* Wed Jun 25 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.2-2mdk
- switch from gtk+1 to gtk+2 (Olav Vitters)

* Tue Jun 24 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.2-1mdk
- new release
- rediff patches 3 and 11
- remove patch 21 (merged upstream)
- fill in the packager name
- update up to official patchlevel 14:
  o GTK 2: wide characters between 128 and 256 not displayed right
  o GTK: Find and Find-Replace dialogs don't work
  o XIM with GTK 2: preedit chars wrong after using backspace
  o XSMP doesn't work when using poll()
  o compilation problem when stat() is a macro
  o crash for UTF-8 char when compiled without +eval feature
  o cursor can't move with multi-byte char and 'virtualedit' set
  o help tags for ":stopinsert" were missing
  o listing Cscope tag matches does not always work
  o may hang when polling for a character when XSMP is supported
  o put in Visual-line selection at end of file goes wrong
  o the netbeans code had an obsolete function with "vim61"

* Fri May 23 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-41mdk
- patch 28: add po editing support

* Mon May 12 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-40mdk
- rebuild for new perl
- vim-common really needs perl, so it's useless to requires perl-base
  only in upper packages (because of getopts.pl)
- patch 27: fake buggy automatic dependancies finder (because of
  fcsking getopts.pl which is *not* a module)
- update up to official patchlevel 451:
  o ":jumps" output doesn't stop after pressing "q" at more-prompt
  o ":mksession" stores folds for unrestorable buffers
  o 'fillchars' cannot contain utf-8 characters
  o (lang) wrong Polish msgs on MS-Windows; English translations
  o Perl interface doesn't work with Perl 5.6
  o add 'ambiwidth' option to chose cell width of Unicode chars
  o add --nofork argument as an alternative to -f
  o an X11 IO error may cause Vim to exit unexpectedly
  o compilation problems with Cygwin
  o compiler warning for pointer
  o crash adding sign without sign icons support
  o crash when using complicated syntax highlighting
  o empty register in viminfo causes conversion failure
  o first character typed in Select mode isn't keymapped
  o get stuck when opening the commandline window in Ex mode
  o scrolling one line with scrollbar doesn't always work
  o setting window title to Chinese doesn't work properly
  o the gzip plugin uses a weird name for writing compressed file
  o wiping out a buffer in autocommands may cause a crash

* Mon Apr 07 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-39mdk
- force install ordering for post-scripts (#3411)
- typo fixes in README.mdk
- update up to official patchlevel 451:
  o add line number to warning for illegal byte when reading file
  o add configure check to disable Perl when it has thread support
  o Netbeans: implement the missing "create" function
  o ":@*" didn't obtain the actual contents of the clipboard
  o "zj" and "zk" cannot be used after an operator
  o update multi-byte tables for Unicode 3.2
  o don't use "make" directly, use $(MAKE)
  o max field width default in 'titlestring' was an arbitrary 50
  o with "1a" in 'fo' appending moves every word to the next line
  o back-tab termcap/terminfo code is not used
  o get backslash before '/' and '?' in GUI find dialog text

* Fri Apr 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-38mdk
- update README.mdk to explain *current* build process and fix a typo btw

* Wed Apr 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-37mdk
- update up to official patchlevel 435:
  o when 'mouse' is "n" the mouse may still start Visual mode
  o ":registers" doesn't stop for "q" at more prompt
  o drag vert. separator may crash Vim; keep focus when dragging
  o in an xterm shift-Tab is not recognized
  o searching may result in reading from uninitialzed data
  o UTF-8 characters in mbyte.txt help file are unreadable
  o missing prototype for enc_canon_search()
  o expanding ":Cmd %" does not work properly for file "a b c"
  o GUI: keypad keys produce same code as normal keys
  o in a translated help file "LOCAL ADDITIONS" cannot be found
  o Hebrew characters drawn wrong
  o failure of obtaining position/size is ignored
  o "finish" in debug mode doesn't stop at end of each function
  o in Insert mode files changed outside of Vim are not detected
  o cmdline completion for ":let g:" doesn't work
  o can't build with Perl interface
  o problems with double-wide chars in Insert mode
  o cursor wrong for "c" on double-wide char
  o can't compile with(out) some features
  o ":silent filetype" writes to the message history
  o make the scroll wheel scroll the window at the mouse pointer
  o tags listed for cscope are sometimes in the wrong order
  o ":set wildmode=list,full" sometimes returned wrong entry
  o "vim --serverlist" didn't work properly without Vim servers
  o ":bnext" may overrule cursor position from autocommand
  o crash on first startup in an X server
  o crash when setting 'imd' in vimrc
  o problem drawing multi-byte chars
  o notepad can't paste from clipboard
  o '\n' in a regexp will never match anything in a string
  o fix compiler warnings
  o in Insert mode CR in quickfix window doesn't jump to error
  o tutor does not select another local version correctly
  o ^R ESC in Insert mode garbles multi-byte
  o cannot jump to another file with ":'M"
  o error code from tgetent() and tgetflag() may be misinterpreted
  o byte2line() can return one more than the number of lines
  o the FileChangedShell event does not allow nesting
  o ":breakadd" doesn't work for a relative file name
  o add the Netbeans interface, 'autochdir', -bg and -fg for GTK
  o can't set a breakpoint in a function
  o ":map" completion and ":mkexrc" misses <silent> and <script>
  o #ifdef nesting is unclear in os_unix.c
  o "%V" in 'statusline' doesn't show "0-1" in an empty line
  o warnings when using 16 bit ints in syntax.c
  o 'printheader' and 'titleold' are not translated
  o ':!dir "%"' doesn't work if file name contains spaces
  o "vim --help" and "vim --version" have a non-zero exit code
  o can't add words to 'lispwords' option
  o two ambiguous buffer-local user commands obscure global one
  o Linux: busy hang if terminal exits and compiled with threading
  o quickfix window can be zero lines high
  o window closed even when a BufWriteCmd fails to write the file
  o multi-byte characters in 'statusline' cause filling to fail
  o cannot detect if a certain patch has been included
  o compilation problem without +multi_byte
  o duplicate tags when using ":helptags"
  o compiler warning
  o add +balloon_eval and sign icons for GTK
  o extend Netbeans, support multi-byte signs
  o ml_get error when using 'virtualedit'
  o highlighting in 'statusline' positioned wrong when truncating
  o Linux + Python: Vim loops forever when the terminal is killed
  o can't define multi-byte text glyph through Netbeans interface
  o compiler warnings for using enum
  o default diff command doesn't work with space in path
  o add command to avoid saving typeahead in debug mode
  o compiler warning for unused variable two_or_more
  o a BufWriteCmd that wipes out a buffer causes trouble
  o error in evaluationg curly braces is not handled consistently
  o various small fixes, additions and corrections
  o a few files are missing from the toplevel Makefile
  o not fitting statusline item causes arbitrary text to appear
  o 'scrollbind' can be set in help window
  o unprintable char 0x0c was displayed as >c0< if 'rightleft' set
  o generating help tags doesn't work in some locales
  o linking fails with +netbeans_intg but without sign icons
  o with 'virtualedit' set Visual block can be displayed wrong
  o shell prompt after hit-enter prompt when using ":gui"
  o "p" doesn't work in Visual mode if "unnamed" is in 'clipboard'
  o wrong window layout when reducing height with quickfix window
  o Netbeans: can't change a line with a sign
  o unprintable multi-byte characters are not handled correctly
  o strftime() can be used with wrong encoding
  o cannot compile on AIX 5.1
  o inconsistent use of convert_input(), string_convert()
  o don't get hit-enter prompt for error message from .vimrc
  o add ":helpgrep" command to be able to search in help files
  o ":helptags $VIMRUNTIME/doc" doesn't add "help-tags" tag
  o "vim --remote-wait +cmd file" waited forever
  o many messages for using regexp patterns are not translated
  o FreeBSD: using system() in a startup script may cause a hang
  o when using a text sign and removing the text Vim may crash
  o Lisp: when matching parens skip over backslashed ()[]{}
  o debug commands end up in redirected text
  o make ":popup" work for GTK
  o click on scrollbar arrow didn't always scroll one line
  o ":winsize" and ":winpos" don't check for wrong arguments

* Wed Feb 05 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-36mdk
- update up to official patchlevel 320 :
  o in debugging mode ":silent" needs to be disabled
  o ":drop fname" didn't use another window containing "fname"
  o	missing backslash in syntax menu item
  o hostname() may return garbage
  o may get 'file changed' warning when using ":wq"
  o window position wrong after closing a window with splits
  o quotes in compiler flags cause trouble in auto/pathdef.c
  o :vim --remote +cmd file" did not execute "cmd"
  o '\' in ":drop file\ name" not removed


* Thu Jan 30 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-35mdk
- update up to official patchlevel 311 :
  o with 'verbose' >= 14 listing a function causes a crash
  o display mess after double-byte char with illegal tail byte
  o can't reset the Visual mode returned by visualmode()
  o add German and Greek tutor translations
  o all double-byte chars displayed as XX

* Tue Jan 28 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-34mdk
- update up to official patchlevel 302 :
  o missing file name in French file save dialog
  o size of Visual area is incorrect for closed folds

* Tue Jan 21 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-33mdk
- update up to official patchlevel 300 :
  o multi-byte string in message box truncated wrong
  o byte2line() returns a wrong line number for some values
  o support "\u1234": multi-byte character in a string
  o error when processing cs.po, Czech message translations
  o test 6 fails in an UTF-8 environment
  o redraw error for sign in first line of closed fold
  o "+cmd" argument for edit commands didn't handle '\' correctly
  o simplify handling of ETO_IGNORELANGUAGE

* Thu Jan 16 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-32mdk
- update up to official patchlevel 289 :
  o triggering an abbreviation with a multi-byte char may fail
  o text written by ":redir" gets extra indent after using input()
  o gcc 3.2.1 still has an optimizer bug
  o compiling with +syntax feature causes errors
  o crash after using ":set define<"
  o GUI: cursor invisible after redrawing an exposed area
  o resetting iconv() state is wrong for an incomplete sequence
  o using "v" in a startup script gives warning message
  o "gvim --remote file" doesn't work for encrypted file
  o compilation error without GUI
  o using signs causes line number in closed fold to be misaligned
  o prototype for smgs() didn't match function definition
  o no error for using lastline and firstline as function args
  o after CTRL-X CTRL-G in Insert mode cursor is in wrong position
  o accept "se " in a modeline where "set " is accepted
  o cannot use a space in icon file name for ":sign" command
  o warning for "struct utimbuf" on Solaris                                      
  o can't wipe out a buffer with the 'bufhidden' option
  o 'showbreak' cannot contain multi-byte characters
  o mixed up "wipe"/"delete" in 'bufhidden'
  o ":silent function F" hangs
  o compiler warning for char pointer

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-31mdk
- update up to official patchlevel 267 :
  o exists() does not work for builtin func
  o security problem: 'foldexpr' may use libcall() or rename()
  o "p" with Visual selection may cause a crash    

* Thu Nov 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-30mdk
- update up to official patchlevel 263 : fix crash on menu.vim reload
  o ":delfunc" leaks memory
  o ":cwindow" doesn't remember previous window correctly
  o buffers menu entries can't shorten multi-byte file names
  o gcc 3.2 has an optimizer bug
  o Perl interface: Delete() may move cursor in wrong window
  o "z[" and "zj" don't set the previous context mark
  o multi-byte char that triggers an abbreviation was lost

* Wed Nov 13 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-29mdk
- update up to official patchlevel 255 : fix crash on menu.vim reload
- patch 26 : highlight *.log with "changelog" syntax too

* Tue Nov 12 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-28mdk
- update from 248 up to official patchlevel 254 :
  o fix expand faillures with multi-byte characters
  o fix crash when altering "lines" value inside  expression set with diffexpr
  o fix completion faillure with ":lcd" and ":lchdir" like ":cd"
  o fix "vi}" not including the line brek when "}" start the following line
  o fix braces in "exists()", ":let()", ":unlet"
- automatize patches directory rename after update
- automatically convert patches from context to unidiff format (smaller
  & easier to read)

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-27mdk
- update from 247 up to official patchlevel 248
- automatize more thinks in vim-%%{version}.%%{official_ptchlvl}-patches/Makefile
- automatically strip headers & footer of patches mail, leaving only
  patches and their description

* Mon Nov 04 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-26mdk
- "saves 837kb" release (aka 9% of vim-common size) :
  o remove mswin.vim vim2html.pl Makefile *awk from doc
  o don't include two copies of :
	* tutorial (saves 321kb)
	* man pages (saves 36kb)
	* vimrc examples (saves 12kb)
  o remove :
	* non unix os specific docs (saves 132kb)
	* non x11 gui specific docs (saves 32kb)
  o %%lang-ify menus & tutorials (saves 260 kb on typical system)
- move back the doc from %_defaultdocdir/%{name}-common-%{version}/ to
  /usr/share/vim/doc
- add briton support (menu, tutorial)
- patch 23 : remove references for deleted docs in :help (see above)
- patch 24 : add emacs outline mode
- patch 25 : make shift-insert work like in xterm in default vimrc
- improve mandrake/README.mdk : add notes about tutorial & on-line help

* Thu Oct 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-25mdk
- patch 22 : on dark X terminal emulators, fix foreground colors of comments
- mandrake/ :
  o rename README README.upstream_patches
  o add a note about where to find long description of patches
  o explain how to zsh-ify bash with bash-completion

* Thu Oct 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-24mdk
- fix symlink-should-be-relative
- add a mini-faq at top of README.mdk
- describe all upstream patches in README

* Thu Oct 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-23mdk
- rpm spec mode :
  o merge patches 4 and 9 into patch 3
  o make mdk alterations more visible and easier to maintain
  o highlist triggers too
  o add new keywords : perl_vendorarch, perl_vendorlib
  o add new macros : _install_info, _postun_groupdel, _pre_groupadd,
    _remove_install_info, clean_menus, configure2_5, old_makeinstall, update_menus
  o highlight these macros as well as configure even when not at beginning of the line
  o highlight pushd popd perl command
  o add GFDL OPL Artistic QPL MPL licences
- BuildRequires: tclx
- s/multubyte/multibyte/

* Wed Oct 30 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-22mdk
- update from 222 up to official patchlevel 247
- fix dangling-relative-symlink by using alternatives & triggers
  btw, this reduce number of soft link indirections
- this package is not prefixable, so get rid of %%prefix, thus making
  everything homogenous with %%{_prefix}
- update vim-6.1.???-patches/README.mdk so that other people can understand
  the vim rule of thumb
- include README.mdk in vim-common

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-21mdk
- update from 153 up to official patchlevel 222
- move vimtutor from /bin to /usr/bin/
- fix vim-minimal looking for wrong .vimrc

* Sat Aug 17 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-20mdk
- update from 152 up to official patchlevel 153: fix searching in included files
- simplify the official patches managment
	o replace all 153 official patches by  a tarball of patches, thus making
	  easier to add new official patches;
	o what's more this result in a very big spec cleaning (304 lines deleted);
	o see README.mdk inclued in the tarball for further informations about
	  adding new patches or stripped patches 
- mdk patches comes back in the 0-100 range
- patch 1009: add _post_service, _preun_service and serverbuild macros
- kill useless %%vimversion

* Tue Aug 13 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-18mdk
- update from 142 up to official patchlevel 152:
     o 6.1.143: Auto formatting near the end of the file moves the cursor
       to a wrong position. In Insert mode some lines are made one char
       too narrow. When deleting a line undo might not always work properly.
     o 6.1.144: Obtaining the size of a line in screen characters can be
       wrong. A pointer may wrap around zero.
     o 6.1.145: GTK: Drag&drop with more than 3 files may cause a
       crash. (Mickael Marchand)
     o 6.1.152: When $LANG is iso8859-1 translated menus are not used.

* Mon Aug  5 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 6.1-18mdk
- rebuild vi for threaded perl

* Thu Aug 01 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-17mdk
- update from 141 up to official patchlevel 142:
  fix "Defining paragraphs without a separating blank line isn't possible.
  Paragraphs can't be formatted automatically."

* Mon Jul 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-15mdk
- add perl_vendor{arch,lib} to spec mode
- update from 125 up to official patchlevel 141

* Tue Jul  9 2002 Warly <warly@mandrakesoft.com> 6.1-15mdk
- rebuilt for new perl

* Mon Jul 08 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-14mdk
- add %%make to mdk rpm macros
- update from 118 up to official patchlevel 125:
	o fix C-f with scrolloff
	o fix "cursor for Insert mode one character to the left"
	o fix ":match" command with more than one argument
	o don't list buffer for alternate name
	o fix "exit is impossible when there's a hidden buffer with 'eol' off
	  and 'bin' on
	o don't save altered buffer which're open in other windows
      in explorer plugin

* Mon Jul 01 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-13mdk
- update from 112 up to official patchlevel 118:
	- fix ":bufdo bwipe
	- don't allocate an array when it's size is zero
	- don't exclude the last character when it is not white space in :das
	- altering eol means binary file is altered
	- fix editing a file over ftp
	- after reloading a file in diff mode mark all windows in diff mode
	  for redraw.

* Tue Jun 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-12mdk
- update from 94 up to official patchlevel 112:
	- fix wide character erasing
	- fix c-f at eof
	- fix memory corruption
	- fix :options
	- fix non printable characters display in status bar
	- fix return values while debugging
	- fix tests for gcc-3.1 (our old friend -fno-strength-reduce ...)
	- fix maze crash
	- fix list setting
	- fix ro file on filter interrupt
	- ignore 'eadirection' in c-w
	- fix :badd
	- fix c-o
- remove rh brain damage "vim is not vi" [P1001]
- update Patch1009 : add %%makeinstall_std support
- remove uneeded patches 1000, 1003 (old rh plain stupid stuff)
- disable patch 1005 which should not be needed
- fix rpmlint's configure-without-libdir-spec

* Wed Jun 12 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-11mdk
- apply fixed official patches 49 and 50

* Wed Jun 12 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-10mdk
- update from 82 up to official patchlevel 94 (skip patches 88 (win32),
  93 (macos))
- rediff patch 1011 (gcc-3.1 support)

* Fri May 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-9mdk
- update from 81 up to official patchlevel 82

* Wed May 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-8mdk
- rediff gcc3 patch
- update from 63 up to official patchlevel 81 (but 17[36]):
    - handle all types of url, with user login, password, protocol, ...
    - don't fore raw mode on term
    - fix viminfo
    - fix diff mode for updated files
	- minor unsigned vs signed comparison fixes
	- fix character cound in visual mode
	- really open urls
	- fixes for vms, borland c 5, windows, macos (don't care)
	- fix cdpath vs change directory
	- fix linking with libacl
	- fix foldmethod
	- fix insertion in visual mode
	- don't include gcc std include directories
	- fix in help for c-_ c-n

* Tue May 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-7mdk
"46 patches" release :
- update from 18 up to official patchlevel 63 (but 19,23,35,44,49,50 ones)
- add the command i use to format official patches names
- rebuild with gcc-3.1
- fix speed_t definition [Patch1000]
- Patch 1002 -> 1001
- fix perl path in scripts [Patch1002] (optimize away env call)
- Patch 1004 -> 1104
- fix keys [Patch1003]
- fix spec mode [Patch1004] (highlighting)
- fix c-v [Patch1005]
- Patch 1010 -> 1110
- add --disable-acl support [Patch1010]
- fix build with gcc-3.1 [Patch1011] (aka i hate gwenole :-( )
- explain why i didn't apply some patches (that is zindoz or vms specific ...)
- fix installation of link instead of directory doc so that 7mdk had as many
  files as 6mdk

* Tue Apr 23 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-6mdk
- provides compatibility /usr/bin/vi link for util-linux
- uses png icon

* Thu Apr 18 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-5mdk
- carefully whether $datadir/vim/lang is a real directory before removing it
  (R.I.P. Deaddog)

* Wed Apr 17 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-4mdk
- compiled-by string: s!tv!Thierry Vignaud!g
- explain where come the official patches
- put the locales in right place as in 2mdk and achieve decent update from
  old releases (aka keep 3mdk no-link-where-there-was-a-directory fix)
  thus enable to get %%lang support from %%find_lang
- apply official patches up to 18, thus fixing "error message
  when using cterm highlighting"

* Wed Apr 17 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-3mdk
- vim is now --short-circuit aware
- spec cleanups
- vim-X11 should requires recent enough vim-common (Michal 'hramrach' Suchanek)
- vim-enhanced should also do
- in order to be able to upgrade from older distro releases, apply a better fix
  to force vim to search for locales in the right place
- apply official patches up to 17, thus fixing :
	6.1.001  Multi-byte: composing char on space isn't formatted properly
	6.1.003  when 'laststatus' is zero vertical separator drawn wrong
	6.1.004  Multi-byte: update for Unicode 3.2
	6.1.005  using more than 50 items in 'statusline' causes a crash
	6.1.006  using "P" or "p" in Visual mode may give wrong results
	6.1.007  error message for ":filetype plugin off" when no plugins used
	6.1.008  "%" didn't correctly ignore \" inside a string
	6.1.009  crash when using a huge maxwid in 'statusline'
	6.1.010  "?\?", ":s?\??" and ":g?\??" didn't work
	6.1.011  XIM: problem when 'number' is set; also a focus problem
	6.1.012  system() fails when fread() does CR-LF to LF translation
	6.1.014  "r" in Visual block mode is wrong when 've' is "block" 
	6.1.015  fix missing define of patch 6.1.014


* Tue Apr 02 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-2mdk
- links /usr/share/vim/lang on /usr/share/locale for buggy program

* Mon Mar 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.1-1mdk
- new release
- add vimtutor (both binary and man)
- add {r,e}vim man-pages
- fix %%Source2 Url
- simplify (cd src;make) and the like into make -C src (lighter cost)
- remove official patches that get merged upstream
- prevent including twice the doc
- %%install: early rm -fr rpm build root
- let the spec be --short-circuit aware

* Mon Mar  4 2002 Warly <warly@mandrakesoft.com> 6.0-7mdk
- remove local path in man pages

* Mon Dec 10 2001 Warly <warly@mandrakesoft.com> 6.0-6mdk
- remove libacl dependencies

* Thu Nov 22 2001 Warly <warly@mandrakesoft.com> 6.0-5mdk
- rpmlint fixes

* Mon Oct 22 2001 DindinX <odin@mandrakesoft.com> 6.0-4mdk
- include the official patches up to 019

* Tue Oct 16 2001 DindinX <odin@mandrakesoft.com> 6.0-3mdk
- include the offical patches 001-011

* Tue Oct 09 2001 DindinX <odin@mandrakesoft.com> 6.0-2mdk
- make rpmlint a little happier

* Wed Sep 27 2001 DindinX <odin@mandrakesoft.com> 6.0-1mdk
- 6.0 final!
- include vimdiff symlink

* Mon Sep 10 2001 DindinX <odin@mandrakesoft.com> 6.0-0.40mdk
- 6.0av

* Mon Sep  3 2001 DindinX <odin@mandrakesoft.com> 6.0-0.39mdk
- 6.0au

* Tue Aug 28 2001 DindinX <odin@mandrakesoft.com> 6.0-0.38mdk
- 6.0at
- removed patch #10 (merged upstream)

* Wed Aug 22 2001 DindinX <odin@mandrakesoft.com> 6.0-0.37mdk
- fix the perl filetype plugin (thanks to chmouel)

* Mon Aug 20 2001 DindinX <odin@mandrakesoft.com> 6.0-0.36mdk
- 6.0as

* Fri Aug 17 2001 DindinX <odin@mandrakesoft.com> 6.0-0.35mdk
- added libgtk+1.2-devel to buildrequires, so gvim is correctly built
  (reported by Michael Jarvis <michael@jarvis.com>)

* Mon Aug 13 2001 DindinX <odin@mandrakesoft.com> 6.0-0.34mdk
- 6.0ar

* Sat Aug  4 2001 Pixel <pixel@mandrakesoft.com> 6.0-0.33mdk
- add require the perl-base used for building (the libperl.so auto-require is not enough)

* Mon Jul 16 2001 DindinX <odin@mandrakesoft.com> 6.0-0.32mdk
- fixed the paths in the man page.

* Fri Jul 13 2001 DindinX <odin@mandrakesoft.com> 6.0-0.31mdk
- 6.0an

* Mon Jul  2 2001 DindinX <odin@mandrakesoft.com> 6.0-0.30mdk
- 6.0am

* Mon Jun 25 2001 DindinX <odin@mandrakesoft.com> 6.0-0.29mdk
- 6.0al

* Mon Jun 18 2001 DindinX <odin@mandrakesoft.com> 6.0-0.28mdk
- 6.0ak

* Mon Jun 11 2001 DindinX <odin@mandrakesoft.com> 6.0-0.27mdk
- 6.0aj

* Tue Jun  5 2001 DindinX <odin@mandrakesoft.com> 6.0-0.26mdk
- 6.0ai

* Mon May 28 2001 DindinX <odin@mandrakesoft.com> 6.0-0.25mdk
- 6.0ah

* Mon May 21 2001 DindinX <odin@mandrakesoft.com> 6.0-0.24mdk
- 6.0ag

* Mon May 14 2001 DindinX <odin@mandrakesoft.com> 6.0-0.23mdk
- 6.0af
- regenerate man-path (#8) spec.vim (#9) patches

* Thu May 10 2001 DindinX <odin@mandrakesoft.com> 6.0-0.22mdk
- updated vim-5.7.man.patch.bz2 to vim-6.0.man.patch.bz2 and added
  libtermcap2-devel to BuildRequires (reported by Wayne Davison <wayne@blorf.net>)

* Wed May  9 2001 DindinX <odin@mandrakesoft.com> 6.0-0.21mdk
- 6.0ae

* Wed May  2 2001 DindinX <odin@mandrakesoft.com> 6.0-0.20mdk
- 60ad

* Wed Apr 25 2001 Pixel <pixel@mandrakesoft.com> 6.0-0.19mdk
- rebuild with new perl

* Tue Apr 24 2001 Pixel <pixel@mandrakesoft.com> 6.0-0.18mdk
- rebuild with new perl

* Mon Apr 23 2001 DindinX <odin@mandrakesoft.com> 6.0-0.17mdk
- 6.0ac

* Mon Mar 26 2001 DindinX <odin@mandrakesoft.com> 6.0-0.16mdk
- 6.0z

* Thu Mar 22 2001 DindinX <odin@mandrakesoft.com> 6.0-0.15mdk
- added BuildRequires: perl-devel (thanks to Jeff Garzik)

* Mon Mar 19 2001 DindinX <odin@mandrakesoft.com> 6.0-0.14mdk
- Added support for fontset in gvim (from Pablo)
- 6.0y

* Tue Feb 27 2001 DindinX <odin@mandrakesoft.com> 6.0-0.13mdk
- 6.0w

* Mon Feb  5 2001 DindinX <odin@mandrakesoft.com> 6.0-0.12mdk
- 6.0u
- fix the vim-common description (vim-minimal does not requires,
  nor suggest vim-common)

* Tue Jan 30 2001 DindinX <odin@mandrakesoft.com> 6.0-0.11mdk
- fix the vim-minimal package (the vi executable was missing!)
- better use of alternatives (/bin/vi and /bin/vim are now links)

* Tue Jan 23 2001 DindinX <odin@mandrakesoft.com> 6.0-0.10mdk
- resurect patch #9
- use alternatives

* Tue Jan 23 2001 DindinX <odin@mandrakesoft.com> 6.0-0.09mdk
- 6.0t
- temporary removed the patch #9 (mandrakesoft-specific spec.vim syntax file)

* Tue Jan 2 2001 DindinX <odin@mandrakesoft.com> 6.0-0.08mdk
- 6.0r

* Wed Dec 13 2000 DindinX <odin@mandrakesoft.com> 6.0-0.07mdk
- 6.0p

* Tue Dec  5 2000 DindinX <odin@mandrakesoft.com> 6.0-0.06mdk
- 6.0o

* Mon Nov 27 2000 DindinX <odin@mandrakesoft.com> 6.0-0.05mdk
- really set CFLAGS to RPM_OPT_FLAGS (should make Dadou happier)
  (thanks to Guillaume)

* Mon Nov 27 2000 DindinX <odin@mandrakesoft.com> 6.0-0.04mdk
- fix ./configure call (--enable-max-feature is now --with-features=huge)
- include some fix in spec.vim from Geoffrey Lee

* Sat Nov 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.0-0.03mdk
- 6.0n.

* Wed Nov 08 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.0-0.02mdk
- Upgrade spec.vim and mandrakizifications.

* Tue Nov  7 2000 DindinX <odin@mandrakesoft.com> 6.0-0.01mdk
- 6.0
- remove ctags from this package

* Tue Sep 19 2000 DindinX <odin@mandrakesoft.com> 5.7-7mdk
- Added a patch to fix the paths in the man pages
  (Thx to Jerome Dumonteil for reporting this)

* Thu Aug 31 2000 DindinX <odin@mandrakesoft.com> 5.7-6mdk
- Rebuild on ke
- Macrozifications
- BM

* Tue Jun 27 2000 DindinX <odin@mandrakesoft.com> 5.7-5mdk
- really fix the help files
- now vi is very spartiate (VI-like) and vim has syntax highlighting

* Mon Jun 26 2000 DindinX <odin@mandrakesoft.com> 5.7-4mdk
- make vim-minimal very, very minimal

* Mon Jun 26 2000 DindinX <odin@mandrakesoft.com> 5.7-3mdk
- fix a typo which prevent the help files to be found
- remove syntax highlighting by default
- remove all trace of indenting

* Mon Jun 26 2000 DindinX <odin@mandrakesoft.com> 5.7-2mdk
- Corrected the ctags version: 3.5.1

* Mon Jun 26 2000 DindinX <odin@mandrakesoft.com> 5.7-1mdk
- 5.7
- use a more standard vimrc file

* Thu May 25 2000 DindinX <odin@mandrakesoft.com> 5.6-19mdk
- Upgrade to 5.6.072
- remove autoindentation :(

* Tue May  2 2000 DindinX <odin@mandrakesoft.com> 5.6-18mdk
- wrap option now defaults to FALSE

* Fri Apr 28 2000 DindinX <odin@mandrakesoft.com> 5.6-17mdk
- remove menu icon path

* Tue Apr 18 2000 Pixel <pixel@mandrakesoft.com> 5.6-16mdk
- fix for perl 5.6
- fix for ctags (i modified patch vim-typo)
- rebuild on true compile box (*with* spec-helper)
- remove abusive provides ctags (not needed)

* Tue Apr 18 2000 DindinX <odin@mandrakesoft.com> 5.6-15mdk
- Fix the online documentation

* Tue Apr 18 2000 DindinX <odin@mandrakesoft.com> 5.6-14mdk
- Make a separate rpm for ctags

* Mon Apr 17 2000 DindinX <odin@mandrakesoft.com> 5.6-13mdk
- fix the name of the menu entry
- remove etags
- move ctags from /bin to /usr/bin
- Added the ctags man page

* Tue Mar 28 2000 DindinX <odin@mandrakesoft.com> 5.6-12mdk
- Do the Right Thing for the menus with the help of 
  Guillaume Cottenceau

* Tue Mar 28 2000 DindinX <odin@mandrakesoft.com> 5.6-11mdk
- Fix the menu group once again (sic)
  Thanks to Guillaume Cottenceau

* Mon Mar 27 2000 DindinX <odin@mandrakesoft.com> 5.6-10mdk
- Added icons

* Mon Mar 27 2000 DindinX <odin@mandrakesoft.com> 5.6-9mdk
- fix menu

* Fri Mar 24 2000 DindinX <odin@mandrakesoft.com> 5.6-8mdk
- remove the RPM_ROOT_BUILD references in %post
  (thanks to Thierry Vignaud for pointing this)
- some changes to the default vimrc
  
* Wed Mar 22 2000 Pixel <pixel@mandrakesoft.com> 5.6-7mdk
- add provides vim for X11 enhanced and minimal
- changed license from freeware to OpenSource

* Mon Mar 20 2000 DindinX <odin@mandrakesoft.com> 5.6-6mdk
- Specs fixes
- removed absolute links
- Added menu entry
- Remove the hlsearch by default (cause it might be puzzling)

* Thu Feb 10 2000 DindinX <odin@mandrakesoft.com> 5.6-5mdk
- Finally include ctags in vim-common :-/

* Thu Feb 10 2000 DindinX <odin@mandrakesoft.com> 5.6-4mdk
- fix a typo in the call to the ./configure script so more features
  are now enabled.

* Sun Feb  6 2000 DindinX <odin@mandrakesoft.com> 5.6-3mdk
- Added support for Chinese/Japanese/Corean support for gvim
  (Thanks to Pablo)
- added a link for the default vimrc.

* Mon Jan 31 2000 DindinX <odin@mandrakesoft.com> 5.6-2mdk
- Added the doc/ subdirectory in /usr/doc/vim-common-5.6/doc
- Correctly install vimrc_hebrew

* Sun Jan 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.6-1mdk
- 5.6.
- Enable right to left mode.
- Add vimrc_hebrew from Tzafrir Cohen <tzafrir@technion.ac.il>

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Build release.

* Tue Sep 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 5.5.

* Mon Aug  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Reinserting old patch.

* Thu Jul 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- First spec file for Mandrake distribution.

# end of file
