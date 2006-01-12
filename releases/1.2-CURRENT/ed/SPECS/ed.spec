#
# spec file for package ed
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ed
%define version		0.2
%define release		%_revrel

%define _exec_prefix	/

Summary:	The GNU line editor
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Text tools
URL:		http://www.gnu.org/software/ed/ed.html 
Source:		ftp://ftp.gnu.org/pub/gnu/ed/ed-0.2.tar.bz2
Patch0:		ed-0.2-security-tempfile.patch
Patch1:		ed-0.2-fixinfo.patch
Patch2:		ed-0.2-li18nux-patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.1

Requires(post):	info-install
Requires(preun): info-install

%description
Ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).  For most
purposes, ed has been replaced in normal usage by full-screen editors
(emacs and vi, for example).

Ed was the original UNIX editor, and may be used by some programs.  In
general, however, you probably don't need to install it and you probably
won't use it much.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
rm -f ./configure
WANT_AUTOCONF_2_1=1 autoconf
rm -f regex.*
%configure

%make CFLAGS="%{optflags}"

# all tests must pass
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall mandir=%{buildroot}%{_mandir}/man1/


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,0755)
%doc NEWS POSIX README THANKS
/bin/ed
/bin/red
%{_infodir}/ed.info*
%{_mandir}/*/*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2-37avx
- fix requires

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2-36avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2-35avx
- rebuild for new gcc

* Sat Jun 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2-34avx
- bootstrap build
- for the use of autoconf2.1 (peroyvind)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.2-33avx
- Annvix build
- require packages not files

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 0.2-32sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 0.2-31sls
- OpenSLS build
- tidy spec

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.2-30mdk
- rebuild
- drop Packager tag
- use %%make macro

* Mon Nov 11 2002 Stew Benedict <sbenedict@mandrakesoft.com> 0.2-29mdk
- Patch for Li18NUX/LSB compliance

* Thu Jul 11 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.2-28mdk
- Costlessly make check in %%build stage

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.2-27mdk
- Automated rebuild in gcc3.1 environment

* Wed Jan  2 2002 Warly <warly@mandrakesoft.com> 0.2-26mdk
- add url tag

* Thu Aug 30 2001 Warly <warly@mandrakesoft.com> 0.2-25mdk
- new distribution tag

* Fri Mar 02 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-24mdk
- Fix info files.

* Sat Dec  9 2000 Etienne Faure  <etienne@mandraksoft.com> 0.2-23mdk
- Rebuilt for release

* Mon Nov 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-22mdk
- Optimisations.
- Add security patch for tempfile open.

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2-21mdk
- fix bad script

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2-20mdk
- minor fix

* Tue Jul 25 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.2-19mdk
- macroszifications
- BM
* Wed Jun 07 2000 Etienne Faure <etienne@mandrakesoft.com> 0.2-18mdk
- rebuild on kenobi

* Thu Apr 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-17mdk
- Clean-up specs.
- * Sun Apr 23 2000 Stefan van der Eijk <s.vandereijk@chello.nl>
- let the spechelper handle compressing man / info pages

* Wed Mar 22 2000 Daouda Lo <daouda@mandrakesoft.com> 0.2-16mdk
- move to Text tools group

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add defattr

* Wed May 19 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- fix typo in %preun
- fix download URL

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added install-info support
- added BuildRoot
- correct URL in Source line

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
