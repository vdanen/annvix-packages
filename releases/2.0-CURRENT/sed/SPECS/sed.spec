#
# spec file for package readline
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		sed
%define version		4.1.4
%define release		%_revrel

Summary:	A GNU stream text editor
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Editors
URL:		http://www.gnu.org/software/sed/
Source0:	ftp://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.bz2

Buildroot:	%{_buildroot}/%{name}-%{version}

Requires(post):	info-install
Requires(preun): info-install

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  Sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.


%prep
%setup -q


%build
%configure2_5x --bindir=/bin
%make LDFLAGS=-s
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{_datadir}/doc

%find_lang %{name}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%doc BUGS NEWS README doc/sed.html
/bin/sed 
%{_infodir}/sed.info*
%{_mandir}/man1/sed.1.bz2

%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4-2avx
- bootstrap build

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4-1avx
- 4.1.4
- spec cleanups

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.7-4avx
- require info-install rather than /sbin/install-info
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.0.7-3sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 4.0.7-2sls
- OpenSLS build
- use %%make macro
- tidy spec

* Fri Apr 11 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0.7-1mdk
- new release

* Wed Apr  9 2003 Warly <warly@mandrakesoft.com> 4.0.6-1mdk
- new version.
- main changes:
 Sed 4.0.6
  * added parameter to `v' for the version of sed that is expected.
  * configure switch --without-included-regex to use the system regex matcher
 Sed 4.0.5
  * improvements to some error messages
  * `a', `i', `l', `L', `r' accept two addresses except in POSIXLY_CORRECT
    mode.  Only `q' and `Q' do not accept two address in standard (GNU) mode.
 Sed 4.0.4
  * update regex matcher

* Wed Nov 27 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0.3-1mdk
- new release
- add message catalogs

* Wed Nov 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0.1-1mdk
- new release
- remove translations from spec
- no need to remove files/directories we don't include
- remove unused prefix

* Wed Oct 23 2002 Warly <warly@mandrakesoft.com> 4.0-1mdk
- new version

* Mon Jun 24 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.02-14mdk
- Rpmlint fixes: no-url-tag, strange-permission
- Make check in %%build stage, all tests must pass

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.02-13mdk
- Automated rebuild in gcc3.1 environment

* Tue May 22 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.02-12mdk
- s/Copyright/License/;

* Mon Mar 26 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.02-11mdk
- Apply sed i18n patch (Andrew Lee).

* Thu Jul 27 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.02-10mdk
- BM
- let spechelper compress info & manpages
- remove packager tag

* Sun Jun 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.02-9mdk
- Use makeinstall macros.

* Thu Apr 13 2000 Enzo Maggi <enzo@mandrakesoft.com> 3.02-8mdk
- Changed group, little fixes in the spec.

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.02

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.01

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- removed references to the -g option from the man page that we add

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
