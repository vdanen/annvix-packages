%define name	zsh
%define version	4.1.1
%define release	4sls

%{!?build_opensls:%define build_opensls 0}

%define doc_version 4.1.1
%define url	ftp://ftp.zsh.org/pub/

%define beta	0

%if %beta
#%{expand:%%define full_preversion %(echo %version-%beta|sed -e 's!dev!dev-!g')}
%define full_preversion %{expand:%(echo %version-%beta|sed -e 's!dev!dev-!g')}
%define release	0.%beta.1sls
%else
%define full_preversion %version
%endif

Summary:	A shell with lots of features.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	GPL
Group:		Shells
URL:		http://www.zsh.org
Source0:	%{url}/%name-%{full_preversion}.tar.bz2
Source1:	%{url}/%name-%doc_version-doc.tar.bz2
Source2:	zcfg-mdk.tar.bz2
Source3:	http://zsh.sunsite.dk/Guide/zshguide.tar.bz2
Patch1:		zsh-3.1.6-dev-22-path.patch.bz2
Patch2:		zsh-4.0.1-pre-3-rpmnewopt.patch.bz2
Patch101:	zsh-serial.patch.bz2
Patch102:	zsh-4.1.0-dev-7-rebootin.patch.bz2

BuildRoot:	%_tmppath/%name-buildroot
BuildRequires:	gcc libtermcap2-devel texinfo
%if !%{build_opensls}
BuildRequires:	yodl
%endif

Prereq: coreutils grep rpm-helper >= 0.7

%description
Zsh is a UNIX command interpreter (shell) usable as an
interactive login shell and as a shell script command
processor. Of the standard shells, zsh most closely resembles
ksh but includes many enhancements. Zsh has command-line editing,
built-in spelling correction, programmable command completion,
shell functions (with autoloading), a history mechanism, and a
lots of other features

Install the zsh package if you'd like to try out a different shell.

%if !%{build_opensls}
%package doc
Summary:	The doc package of zsh
Group:		Books/Computer books

%description doc
Zsh is a UNIX command interpreter (shell) usable as an
interactive login shell and as a shell script command
processor. Of the standard shells, zsh most closely resembles
ksh but includes many enhancements. Zsh has command-line editing,
built-in spelling correction, programmable command completion,
shell functions (with autoloading), a history mechanism, and a
lots of other features

This package include doc guid examples and manual for zsh.
%endif

%prep
%setup -q -a 2 -a 1 -n %name-%full_preversion
mv %name-%doc_version/Doc/* Doc/
%patch1 -p1
%patch2 -p1
%patch101 -p1
%patch102 -p1

# remove temporary files
find | grep '~$' | xargs rm -f

%build
%ifnarch sparc
%configure --enable-etcdir=%_sysconfdir --enable-function-subdirs --disable-debug
%else
%configure --enable-etcdir=%_sysconfdir --enable-function-subdirs --disable-lfs
%endif

make all

%install
rm -rf $RPM_BUILD_ROOT

make install-strip DESTDIR=%buildroot
make install.info DESTDIR=%buildroot

# copy Mandrake Configuration files.
mkdir -p $RPM_BUILD_ROOT/{bin,etc}
cp -a zcfg/etc/z* $RPM_BUILD_ROOT%_sysconfdir
cp -a zcfg/share/zshrc_default %buildroot%_datadir/zsh/%full_preversion/zshrc_default

# Backward compatibilie should be removed in the others times.
pushd $RPM_BUILD_ROOT/bin && {
    mv ..%_bindir/zsh ./zsh
} && popd

rm -f $RPM_BUILD_ROOT%_bindir/zsh-%full_preversion

# Copy documentation.
rm -rf docroot
mkdir -p docroot/{Info_html,Examples,Documentation}/

cp -a README docroot/
cp -a Functions/Misc/* Misc/* Util/* docroot/Examples/
cp -a INSTALL ChangeLog* docroot/Documentation 
cp -a StartupFiles docroot/
cp -a Etc/* docroot/Documentation
mv docroot/Documentation/NEWS docroot/
cp -a Doc/*html docroot/Info_html/

mkdir -p docroot/Zsh_Guide
tar xjf %SOURCE3 -C docroot/Zsh_Guide
mv docroot/Zsh_Guide/zshguide/*html docroot/Zsh_Guide/
rmdir docroot/Zsh_Guide/zshguide

# Doc
rm -f docroot/{StartupFiles/.distfiles,Examples/{Makefile*,*.yo},Documentation/{Makefile*,*.yo}}
find docroot/ -name 'Makefile*' -o -name '.yo'|xargs rm -f
find docroot/ -type f|xargs perl -pi -e 's@^#!%_prefix/local/bin/(perl|zsh)@#!%_bindir/\1@'
mv docroot/Examples/compctl-examples docroot/StartupFiles

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/share/rpm-helper/add-shell %name $1 /bin/zsh
%_install_info %name.info

%postun
/usr/share/rpm-helper/del-shell %name $1 /bin/zsh
%_remove_install_info %name.info

%files
%defattr(-,root,root,0755)
%doc docroot/README docroot/NEWS
%config(noreplace) %_sysconfdir/z*
/bin/%name
%_mandir/man1/*.1*
%_infodir/*.info*
%dir %_datadir/zsh
%dir %_datadir/zsh/%{full_preversion}/
%_datadir/zsh/%{full_preversion}/functions
%_datadir/zsh/%{full_preversion}/zshrc_default
%_libdir/zsh/%{full_preversion}/
%_datadir/zsh/site-functions/

%if !%{build_opensls}
%files doc
%defattr(-,root,root)
%doc docroot/Documentation/ docroot/Examples/ docroot/Info_html/ docroot/StartupFiles/
%doc docroot/Zsh_Guide ChangeLog*
%endif

%changelog
* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 4.1.1-4sls
- OpenSLS build
- tidy spec
- don't build doc for %%build_opensls
- don't need yodl as a BuildReq

* Mon Jul 21 2003 Warly <warly@mandrakesoft.com> 1:4.1.1
- rebuild to fix segfault

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.1.1-2mdk
- rebuild

* Tue Jul 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1.1-1mdk
- new release

* Mon Apr 21 2003 Chmouel Boudjnah <chmouel@chmouel.com> 4.1.0-0.dev7.2mdk
- Add rebootin completion (need to be merged upstream).

* Mon Mar 24 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1.0-0.dev7.1mdk
- new pre release
- remove patches 102, 103, 104, 106, 107, 109, 110 and 111 (merged upstream)

* Tue Nov 12 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1.0-0.dev5.2mdk
- patch 110 : fix links completion
  o add missing options
  o describe all options
- patch 111 : add -{no-}verify-rpm options to urpmi completion (and describe them)

* Tue Nov 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.1.0-0.dev5.1mdk
- new pre release
- big spec cleaning
- PreReq: rpm-helper
- use {add,del}-shell in %%post{,un}
- remove patches 100, 105 & 108 (merged upstream)
- rediff patch 103
- requires coreutils instead of fileutils

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0.6-4mdk
- patch 108 : upstream fixes:
  o bzip2 : recognise also .tbz and .tbz2 files
  o add support for -H option to completion
  o add some missing apt-get options.
  o add support for the pkg_create command
  o revent typeset of a positional parameter before it can do damage,
    and improve the error message about it.
- patch 109 : fix mem leak
- fix doc subpackage group

* Wed Oct 09 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0.6-3mdk
- patch104: fix ssh-keygen completion
- patch105: fix :
  o unzip/_path_files interaction,
  o broken xli completion
  o CVS completion with respect to filenames containing spaces.
- patch106: fix "case foo in (foo)echo foo;;(bar)echo bar;;esac"
  construction (ie no space between right paren and list)
  when in sh emulation mode.
- patch107: add missing apt-get options to completion

* Fri Sep 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0.6-2mdk
- patch102: fix typo in clint prompt
- patch103: update lynx command list

* Thu Aug 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0.6-1mdk
- new release
- kill patches 3, 4 and 5 (merged upstream)
- patch 100: complete multiple -j's after cvs update
- patch 101: make it work on serial ports

* Wed May 29 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.4-7mdk
- Automated rebuild with gcc 3.1-1mdk

* Tue Jan 22 2002 Stefan van der Eijk <stefan@eijk.nu> 4.0.4-6mdk
- BuildRequires

* Mon Jan 14 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.4-5mdk
- Upgrade urpmi completion (Andrej).

* Mon Dec 10 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.4-4mdk
- Add bash-functions from cvs.
- Add %_datadir/zsh also as %dir.

* Tue Nov 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.4-3mdk
- Make /usr/share/zsh/version as %dir.

* Thu Nov 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.4-2mdk
- Upgrade zshguide.
- Add urpmi completion from Andrej.

* Fri Nov  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.4-1mdk
- s|Epoch|Serial|;
- 4.0.4.

* Sun Jul 01 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.0.2-2mdk
- s/Copyright/License/;
- Rebuild to get /bin/zsh back, is it just a weird problem which I have 
  on my own machine?

* Wed Jun 27 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.2-1mdk
- 4.0.2.

* Tue Jun  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.1-1mdk
- Make the Alt-Backspace bash alike with WORDCHARS set to ''.
- 4.0.1 final.

* Sun May 27 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.1-0.4mdk
- upgrade to 052701 cvs.

* Wed May 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.1-0.3mdk
- Remove most of the mdk-system-wide options and put it in a
  distribution files sourced if not ~/.zshrc is present.
- 4.0.1-pre-5.

* Mon May 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.1-0.2mdk
- 4.0.1-pre-4.

* Mon Apr 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.1-0.1mdk
- 4.0.1-pre-3.
- Redo the configuration.

* Fri Mar  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.9-6mdk
- Source /etc/profile.d/ files.

* Thu Mar  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.9-5mdk
- Don't build help since it look it doen't works.

* Sat Aug 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.9-4mdk
- Set some %config file to (noreplace).
- Make -A to complete spec file for _rpm.

* Thu Jul 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.9-3mdk
- Get /usr/share/man also in the completion for perl manpages.
- BM.

* Wed Jul  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.9-2mdk
- Fix buildroot hardcoded in binary.

* Wed Jun 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.9-1mdk
- Use makeinstall macros (not easy this one :\).
- 3.1.9.

* Mon Jun  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.8-1mdk
- 3.1.8.

* Sun May 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev22-3mdk
- Fix path (%{prefix}/ucb -> %{_bindir}/X11)
- Fix keys (home-end-suppr-delete) directly in the zsh binary.

* Sun Apr 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev22-2mdk
- Remove doble .so in %{_libdir}/zsh/*.

* Thu Apr 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev22-1mdk
- 3.1.6dev22.

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev20-3mdk
- Fix completion of rpm with -qp*.

* Mon Mar 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev20-2mdk
- Upgrade zshguide.

* Sat Mar 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev20-1mdk
- 3.1.6-dev20

* Wed Mar 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev19-3mdk
- Move global configuration here.
- Adjust groups.

* Tue Feb 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev19-2mdk
- Add new zshguide from pws.
- Separate the doc to the doc package

* Sun Feb 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev19-1mdk
- Clean Up spec (thanks specs-helper).
- Remove all our patchs (now all is commited to upstream main).
- 3.1.6dev19.

* Fri Feb 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev18-3mdk
- Recompile with glibc2.1.3 (first one).

* Thu Feb 17 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev18-2mdk
- Add --freshen completion.

* Tue Feb 15 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev18-1mdk
- Fix descriptions and summary.
- 3.1.6dev18.

* Thu Feb 10 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev17-2mdk
- Remove Makefile in %doc.
- BuildRequires: autoconf tetex.
- Lot of modications in the default config as suggested by Bart
  Schaefer <schaefer@zsh.org>.
- 3.1.6dev17.

* Mon Jan 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev16-1mdk
- dev16.
- Redo the tar_archive patchs.

* Tue Jan 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev15-1mdk
- dev15.
- Fix doc generation with dev15.
- remove META-FAQ.
- disable lfs on sparc.

* Thu Jan  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6dev14-1mdk
- dev14 (note the name change).

* Mon Jan  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1.6pws13-3mdk
- Remove temporary files.

* Fri Dec 31 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 3.1.6pws13 (mainly bug fixes).
- fix %post.
- fix rpm completion

* Thu Dec 09 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 3.1.6pws11 (mainly bug fixes).

* Tue Dec  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add run-help and perl-build the documentation.

* Tue Nov 30 1999 Francis Galiegue <francis@mandrakesoft.com>

- Completion machine patch - we use GNU make and GNU tar
- Small fix to %post script

* Tue Nov 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 3.1.6pws10
- Fix zprofile.
- Clean-up Franciseries.
- Clean-up specs.

* Mon Nov 29 1999 Francis Galiegue <francis@mandrakesoft.com>
- Grrr... Rebuilt on kenobi, toy ain't a cooker

* Mon Nov 29 1999 Francis Galiegue <francis@mandrakesoft.com>

- Completion system now handles bzip2'ed manpages and tarballs
- Some cool options

* Wed Nov 10 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add zshguide.txt to documentation.

* Thu Oct 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix bug in %{_sysconfdir}/zsh use USERNAME instead of USER.
- Improve %{_sysconfdir}/z* to source the /etc/profile.d/ files.

* Mon Oct 04 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 3.1.6-pws6
- Fix bad link.
- Fix bad manpages.

* Tue Aug 17 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- fix typo in examples directory name

* Sun Aug  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Copy documentation (yes a lot).
- Remove the completion machine and put them in [[ {etc,root}(skel|files) ]] package.

* Sat Aug  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- By defaut we launch the completion machine.
- Put zsh in %{_bindir}/
- Rewrite of Spec file for this new major version.

# end of file

# Local Variables:
# rpm-spec-insert-changelog-version-with-shell: t
# End:
