#
# spec file for package byacc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		byacc
%define version		1.9
%define release		19avx

%define date		20040328

Summary:	A public domain Yacc parser generator
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		Development/Other
URL:		http://dickey.his.com/byacc/byacc.html
Source:		ftp://invisible-island.net/byacc/byacc.tar.bz2
Patch0:		byacc-1.9-fixmanpage.patch.bz2
Patch1:		byacc-1.9-automake.patch.bz2
Patch2:		byacc-1.9-security.patch.bz2
Patch3:		byacc-1.9-includes.patch.bz2
Patch4:		byacc-20040328-no-recreate-unionfile.patch.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Byacc (Berkeley Yacc) is a public domain LALR parser generator which
is used by many programs during their build process.


%prep
%setup -q -n %{name}-%{date}
%patch4 -p1 -b .unionfile


%build
%configure
%make

make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
( cd %{buildroot}%{_bindir} ; ln -s yacc byacc )
ln -s yacc.1 %{buildroot}%{_mandir}/man1/byacc.1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc ACKNOWLEDGEMENTS NEW_FEATURES NOTES
%doc NO_WARRANTY README
%{_bindir}/yacc
%{_bindir}/byacc
%{_mandir}/man1/*


%changelog
* Wed Jul 27 2005 Vincent Danen <vdanen@annvix.org> 1.9-19avx
- rebuild for new gcc
- use the 2004-03-28 tarball from Thomas Dickey (of ncurses) which
  contains a lot of fixes and enhancements

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 1.9-18avx
- bootstrap build
- force use of automake1.4 and autoconf2.5 (peroyvind)

* Fri Jun 25 2004 Vincent Danen <vdanen@opensls.org> 1.9-17avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.9-16sls
- minor spec cleanups

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 1.9-15sls
- OpenSLS build
- tidy spec

* Wed Jul 23 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 1.9-14mdk
- rebuild

* Fri Jan 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.9-13mdk
- Rebuild
- Add some sort of make checking

* Sat Nov 10 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.9-12mdk
- BuildRequires: autoconf automake
- add URL tag

* Tue Jul 24 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.9-11mdk
- rebuild
- fix license

* Sat Apr 14 2001 Francis Galiegue <fg@mandrakesoft.com> 1.9-10mdk
- Patch3: fix include files (sizeof(int) != sizeof(void *))

* Wed Mar  7 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.9-9mdk
- patch for safer creation of temp files

* Tue Feb 27 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.9-8mdk
- more docs
- convert build to autoconf/automake for much clearer spec

* Fri Jul 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.9-7mdk
- BM
- let spechelper compress manpages

* Mon Jul 17 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 1.9-6mdk
- macroszifications
- change permision of build dir in order to remove it

* Mon Apr 17 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.9-5mdk
- removed version from spec filename

* Wed Apr  5 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.9-4mdk
- updated BuildRoot
- group now Development/Other

* Tue Nov  9 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Tue May 11 1999 Bernhard Rosenkr�nzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Wed Apr 07 1999 Preston Brown <pbrown@redhat.com>
- man page fixed.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- various spec file cleanups

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
