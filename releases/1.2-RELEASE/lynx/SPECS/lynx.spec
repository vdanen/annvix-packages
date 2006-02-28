#
# spec file for package lynx
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		lynx
%define version 	2.8.5
%define release		%_revrel
%define epoch		1

%define versio_		2-8-5

Summary:	Text based browser for the world wide web
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Networking/WWW
URL:		http://lynx.isc.org
Source0:	http://lynx.isc.org/current/%{name}%{version}.tar.bz2
Patch0:		lynx2-8-5-adapt-to-modern-file-localizations.patch
Patch1:		lynx-2.8.5-avx-config.patch
Patch2:		lynx2-8-4-fix-ugly-color.patch
Patch10:	lynx2-8-5-tmp_dir.patch
Patch11:	lynx2-8-5-don-t-accept-command-line-args-to-telnet.patch
Patch12:	lynx-2.8.5-CAN-2005-3120.patch
Patch13:	lynx-2.8.5-CVE-2005-2929.patch
BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel, zlib-devel, gettext, ncurses-devel

Provides:	webclient lynx-ssl
Obsoletes:	lynx-ssl

%description
This a terminal based WWW browser. While it does not make any attempt
at displaying graphics, it has good support for HTML text formatting,
forms, and tables.

This version includes support for SSL encryption.


%prep
%setup  -q -n %{name}%{versio_}
%patch0 -p1
%patch1 -p1
%patch2 -p1 
%patch10 -p1
%patch11 -p1
%patch12 -p1 -b .can-2005-3120
%patch13 -p1 -b .cve-2005-2929


%build
%configure \
    --libdir=/usr/share/lynx \
    --enable-warnings \
    --with-screen=ncurses \
    --enable-8bit-toupper \
    --enable-externs \
    --enable-cgi-links \
    --enable-persistent-cookies \
    --enable-nls \
    --enable-prettysrc \
    --enable-source-cache \
    --enable-charset-choice \
    --enable-default-colors \
    --enable-ipv6 \
    --enable-nested-tables \
    --enable-read-eta \
    --with-zlib \
    --enable-internal-links \
    --enable-libjs \
    --enable-scrollbar \
    --enable-file-upload \
    --with-ssl \
    --enable-addrlist-page \
    --enable-justify-elts \
    --enable-color-style \
    --enable-nsl-fork

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std install-help

install -d %{buildroot}%{_sysconfdir}
cat >%{buildroot}%{_sysconfdir}/lynx-site.cfg <<EOF
# Place any local lynx configuration options (proxies etc.) here.
EOF

%find_lang lynx


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f lynx.lang
%defattr(-,root,root)
%doc README
%config(noreplace,missingok) %{_sysconfdir}/lynx-site.cfg
%{_mandir}/*/*
%{_bindir}/*
%{_datadir}/lynx


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Dec 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-7avx
- P13: fix for CVE-2005-2929
- drop compressed patches

* Wed Oct 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-6avx
- updated P12 to fully fix the issue

* Sat Oct 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-5avx
- P12: fix for CAN-2005-3120

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-3avx
- rebuild

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-2avx
- update P1 so startfile points to our site

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-1avx
- 2.8.5

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.8.5-0.dev.12.17avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 2.8.5-0.dev.12.16sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.8.5-0.dev.12.15sls
- OpenSLS build
- tidy spec
- Epoch: 1 because we make the release tag make more sense

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.8.5-0.14mdk.dev.12
- rebuild

* Wed Jan 22 2003 Pixel <pixel@mandrakesoft.com> 2.8.5-0.13mdk.dev.12
- cleanup config file location. 
  this implies moving from lynx.cfg from /etc to /usr/share/lynx
  (my nice trigger script should handle it nicely :)
- this fixes up lynx help (bug #523)
- /etc/lynx-site.cfg now works!

* Thu Jan 16 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.5-0.12mdk.dev.12
- new pre-release
- rediff patch 0
- rebuild for new openssl

* Sun Nov 17 2002 Stefan van der Eijk <stefan@eijk.nu> 2.8.5-0.11mdk.dev.8
- BuildRequires

* Fri Sep 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.8.5-0.10mdk.dev.8
- Nuke BuildRequires: smtpdaemon

* Fri Aug  9 2002 Pixel <pixel@mandrakesoft.com> 2.8.5-0.9mdk.dev.8
- new pre-release
- make it build
- remove the menu entry (people don't expect such a browser in a menu)
- remove /usr/share/lynx/test/*.html
- freshen patches
- drop patch ipv6-salen (not needed)
- drop patch i18ncfg (not used in mandrake, used to allow lynx.cfg.ja for example)
- add lynx-site.cfg (same as redhat)
- use configure options from both redhat and debian
- fix url

* Thu Apr 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.5-0.8mdk
- new release (dev7)
- fix url

* Fri Feb 22 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.8.5-0.7mdk
- corrected mad BuildRequires

* Sun Jan 27 2002 Stefan van der Eijk <stefan@eijk.nu> 2.8.5-0.6mdk
- BuildRequires

* Tue Jan 22 2002 David BAUDENS <baudens@mandrakesoft.com> 2.8.5-0.5mdk
- Fix menu entry (icon)

* Tue Oct 09 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.5-0.4mdk
- dev.3 release
- fix url
- compress small patch for fredl's bot
- provides lynx-ssl as we already obsoletes it

* Thu Aug 30 2001 David BAUDENS <baudens@mandrakesoft.com> 2.8.5-0.3mdk
- Use new icons

* Thu Aug 16 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.5-0.2mdk
- dev2

* Thu Jul 26 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.5-0.1mdk
- dev1

* Wed Jul 18 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4-2mdk
- remove epoch as qa requires: not needed for a cooker package that exists
  only a few days

* Wed Jul 18 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4-1mdk
- final release
- s!Serial!Epoch

* Mon Jul 16 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4-0.1mdk
- new release (pre5)
- add menu icons
- fix fcrozat changelog

* Wed Jul 11 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4pre.4-1mdk
- new release
- fix buildrequires

* Wed Apr 11 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.4dev.11-9mdk
- Correct icon in menu entry

* Tue Jan 30 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.8.4dev.11-8mdk
- --with-included-gettext.
- include the locales.

* Sun Jan  7 2001 Pixel <pixel@mandrakesoft.com> 2.8.4dev.11-7mdk
- use --enable-default-colors so that at last it doesn't use black foreground in my
rxvt :)

* Thu Dec 28 2000 Daouda Lo <daouda@mandrakesoft.com> 2.8.4dev.11-6mdk
- remove hardcoded path in menu

* Thu Nov 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.11-5mdk
- fix help location 

* Tue Nov 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.8.4dev.11-4mdk
- Another color fix patch :p.

* Tue Nov 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.8.4dev.11-3mdk
- Install lynx.lss from the samples/ directory (much better color).

* Fri Nov 03 2000 Daouda Lo <daouda@mandrakesoft.com> 2.8.4dev.11-2mdk
- rebuild for gcc-2.96

* Thu Oct 19 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.11-1mdk
- new release

* Sat Oct 07 2000 David BAUDENS <baudens@mandrakesoft.com> 2.8.4dev.8-4mdk
- Fix menu entry (#736)
- Use %%make macro

* Wed Sep 06 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.8-3mdk
- really add SSL (ginette sucks)
- buildrequires&obsoletes fixes for ssl support
- more macros
- add a menu entry

* Tue Sep  5 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.8.4dev.8-2mdk
- add support for SSL

* Fri Aug 25 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.8-1mdk
- new version

* Thu Aug 10 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.7-3mdk
- fix config for lord fred^h^h^hrpmlint
- remove useless wmconfig file

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.8.4-2mdk
- automatically added BuildRequires


* Fri Aug 04 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.7-1mdk
- new release

* Tue Jul 25 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.6-2mdk
- BM
- make it short-circuit compliant

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.6-1mdk
- new release

* Mon Jul 17 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.5-1mdk
- new release ...
- use new macros
- use spechelper for binaries stripping
- bzip2 doc instead of gzip it

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.4-1mdk
- new release

* Thu Jun 08 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.8.4dev.3-1mdk
- new release

* Mon Apr 24 2000 Pixel <pixel@mandrakesoft.com> 2.8.3dev.22-2mdk
- add provides webclient

* Thu Mar 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>
- update to 2.8.3dev.22

* Thu Mar 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>
- use the new group naming scheme
- use spechelper

* Mon Dec  6 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Define the TEMPDIR to ~/tmp, create it if is no here or fallback to
  /tmp is he can't.

* Sat Nov  6 1999 John Buswell <johnb@mandrakesoft.com>
- Build Release

* Tue Oct  5 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix wrong helpfile url (#291).

* Tue Sep  7 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Fix compliance with FTP RFC (needed for wu-ftpd 2.6.0 and other servers)
- 2.8.3dev.8
- Enable file-upload feature

* Fri Aug 20 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 2.8.3dev.6

* Tue Jul 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Redefine the temporary dir to /tmp/ (definitively !!!).

* Thu Jul 15 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- update to 2.8.3dev.4

* Wed Jun 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 2.8.3.2 version.
- Updated patch.

* Fri May 21 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 2.8.2pre5
- remove no-root patch

* Mon May 10 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 2.8.2pre2
- change group to Applications/Internet (used to be the only app in
  group Networking).
- handle RPM_OPT_FLAGS

* Tue May 04 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add lynx.lss files.

* Thu Apr 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adptations.

* Tue Feb 16 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.8.2dev.16-2d]
- build with socks5 support -- if avaiable .. 

* Tue Feb 16 1999 Artur Frysiak <wiget@usa.net>
  [2.8.2dev.16-1d]
- moved help and test files to %{_datadir}/lynx
- added not_for_root patch (this is bugi software, run from root account
  is dangerus)
- changed default color scheme

* Fri Feb 05 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.8.2dev15-2d]
- changed group,
- compressed documentation.

* Sun Jan 10 1999 Artur Frysiak <wiget@usa.net>
  [2.8.2dev.12-1d]
- added URL and Group(pl) tags

* Mon Sep 01 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.8-5d]
- build against glibc-2.1,
- changed Buildroot to /var/tmp/%%{name}-%%{version}-%%{release}-root,
- changed permission of lynx to 711,
- translation modified for pl.

* Sun Aug 30 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [2.8-5]
- added -q %setup parameter,
- changed Buildroot to /tmp/%%{name}-%%{version}-root,
- URL in HELPFILE in /etc/lynx.cfh changed to localhost,
- removed INSTALLATION from %doc,
- added %attr and %defattr macros in %files (allow build package from
  non-root account).

