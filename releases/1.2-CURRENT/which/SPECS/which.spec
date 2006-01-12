#
# spec file for package which
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		which
%define version		2.16
%define release		%_revrel

Summary:	Displays where a particular program in your path is located
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		ftp://ftp.gnu.org/gnu/which/
Source:		ftp://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.bz2
Patch0:		which-2.6.jbj.patch
Patch1:		which-2.12-fixinfo.patch
Patch2:		which-2.16-afs.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires(post):	info-install
Requires(preun): info-install

%description
The which command shows the full pathname of a specified program, if
the specified program is in your PATH.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{_infodir}/dir


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%files
%defattr(-, root, root)
%doc README* AUTHORS EXAMPLES INSTALL NEWS
%{_bindir}/which
%{_mandir}/man1/which.1*
%{_infodir}/*


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16-6avx
- minor spec cleanups

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16-5avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16-4avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.16-3avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.16-2avx
- require info-install, not the file
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.16-1sls
- 2.16
- rediff and simplify P3 (tvignaud)

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 2.14-7sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 2.14-6sls
- OpenSLS build
- tidy spec

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.14-5mdk
- rebuild

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.14-4mdk
- build release

* Mon Oct 28 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.14-3mdk
- remove useless prefix
- patch 2 : use access instead stat in AFS environment 

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.14-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Aug  2 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 2.14-1mdk
- Version 2.14
- Use %%configure2_5x, %%makeinstall_std
- Do not regenerate autoconf/automake files, breaks build

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13-5mdk
- Automated rebuild in gcc3.1 environment

* Fri Aug 17 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.13-4mdk
- new release
- sanitize spec file

* Sun Mar 04 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.12-4mdk
- Fix info files entry.
- Fix %files.

* Fri Feb 23 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.12-3mdk
- Whoops, info files were not getting installed

* Fri Feb 23 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.12-2mdk
- Change specfile permissions (rpmlint warning)
- List more docs in doc macro
- Generate automake and autoconf-derived files in prep stage

* Mon Nov 13 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.12-1mdk
- new and shiny vesion.

* Tue Aug 22 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.11-1mdk
- BM
- 2.11
- Even More Cleanup Of Specs :-)

* Tue Jun 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.9-5mdk
- Clean up specs.
- Use makeinstall macros.

* Wed Apr  5 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 2.9-4mdk
- new group System/Base
- updated BuildRoot

* Fri Nov 5 1999 Damien Krotkine <damien@mandrakesoft.com>
- Mandrake release

* Wed Aug 18 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- add defattr

* Sun Aug 08 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 2.8 :
	* aclocal.m4 was missing from the tar, resulting in
	  a build failure if autoconf isn't installed.


* Thu Jul 08 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Upgrade to the offical version of Gnu project.
- Rewriting the spec-files.
- 2.7 :
    * Support for aliases
    * Configure/compile fix in the `tilde' directory.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- handle RPM_OPT_FLAGS
- Makefiles and source code are NOT docs.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc
