#
# spec file for package m4
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		m4
%define version 	1.4.3
%define release 	%_revrel

Summary:	The GNU macro processor
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.seindal.dk/rene/gnu/
Source0:	ftp://ftp.gnu.org/pub/gnu/m4-%{version}.tar.bz2
Source1:	ftp://ftp.gnu.org/pub/gnu/m4-%{version}.tar.bz2.sig

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires(post):	info-install
Requires(preun): info-install

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x
%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std infodir=%{_datadir}/info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info


%preun
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%{_bindir}/m4
%{_infodir}/*

%files doc
%defattr(-,root,root)
%doc NEWS README COPYING BACKLOG THANKS ChangeLog


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3 
- add -doc subpackage
- rebuild with gcc4
- put make check in %%check

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3-1avx
- 1.4.3
- dropped P0; not required

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4ppre2-9avx
- bootstrap build (new gcc, new glibc)
- s/mandrake/annvix/

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4ppre2-8avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4ppre2-7avx
- require packages not files
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.4ppre2-6sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 1.4ppre2-5sls
- OpenSLS build
- tidy spec

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.4ppre2-4mdk
- rebuild
- rm -rf $RPM_BUILD_ROOT in %%install, not %%prep

* Thu Jan 16 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.4ppre2-3mdk
- rebuild

* Thu Jan 17 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.4ppre2-2mdk
- url

* Fri Jul 27 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.4ppre2-1mdk
- updated to 1.4ppre2

* Thu Dec  7 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.4-19mdk
- Run automated tests at build time
- Use RPM_OPT_FLAGS.  Damn, who forgot that one.

* Fri Nov 10 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.4-18mdk
- build for gcc-2.96

* Tue Aug 29 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.4-17mdk
- BM

* Wed Mar 22 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.4-16mdk
- spechelper fixes
- group fix

* Wed Nov  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.
- Fix building as user.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- Manhattan build

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- added info file handling and BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

