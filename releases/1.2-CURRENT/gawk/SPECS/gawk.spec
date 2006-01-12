#
# spec file for package gawk
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gawk
%define version		3.1.4
%define release		%_revrel

Summary:	The GNU version of the awk text processing utility
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Text tools
URL:		http://www.gnu.org/software/gawk/gawk.html
Source0:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.bz2
Source1:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}-ps.tar.bz2
Patch0:		gawk-3.1.3-getpgrp_void.patch
Patch1:		gawk-3.1.4-dfacache.patch
Patch2:		gawk-3.1.4-flonum.patch
Patch3:		gawk-3.1.4-nextc.patch
Patch4:		gawk-3.1.4-uplow.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	byacc

Provides:	awk
Requires(post):	info-install
Requires(preun): info-install

%description
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.


%prep
%setup -q -b 1
%patch0 -p1 -b .getpgrp_void
%patch1 -p1 -b .dfacache
%patch2 -p1 -b .flonum
%patch3 -p1 -b .nextc
%patch4 -p1 -b .uplow


%build
%configure
%make

# all tests must pass
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall bindir=%{buildroot}/bin

%find_lang %{name}

rm -f %{buildroot}%{_infodir}/dir

mkdir -p %{buildroot}{%{_bindir},%{_datadir}/awk,%{_mandir}/man1}

pushd %{buildroot}%{_datadir}
    for  i in *.awk;do
        mv -f $i awk
    done
popd

pushd %{buildroot}%{_mandir}
    for i in *;do
        mv -f $i man1 || true
    done
    pushd man1
       ln -sf gawk.1.bz2 awk.1.bz2
    popd
popd

pushd %{buildroot}%{_bindir}
    ln -sf ../../bin/awk %{buildroot}%{_bindir}/awk 
    ln -sf ../../bin/gawk %{buildroot}%{_bindir}/gawk 
    mv %{buildroot}/bin/pgawk %{buildroot}%{_bindir}
    rm -f %{buildroot}/bin/pgawk-%{version}
popd


%post
%_install_info gawk.info

%preun
%_remove_install_info gawk.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%doc README COPYING FUTURES LIMITATIONS NEWS
/bin/*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*
%{_libdir}/*
%{_datadir}/awk


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2-8avx
- 3.1.4
- sync patches with mandrake 3.1.4-1mdk (which in turn synced with Fedora)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2-8avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2-7avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2-6avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2-5avx
- require packages not files
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 3.1.2-4sls
- minor spec cleanups
- remove %%prefix
- remove the doc package

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 3.1.2-3sls
- OpenSLS build
- tidy spec

* Mon Nov 17 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.1.2-2.1.92mdk
- added patch from Luca Berra <bluca@vodka.it> to fix segfault when 
  using character classes and locale

* Fri Apr 18 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.2-2mdk
- use rawhide patch to fix parsing of /proc pseudo-files

* Thu Apr 17 2003 Aurelien Lemaire <alemaire@mandrakesoft.com> 3.1.2-1mdk
- New version 3.1.2
- Update Sources Url
- Delete Patch0 : imposible to update this patch
- Update Patch1 to new version
- Add patch2 to fix typo

* Sat Jan 18 2003 Stefan van der Eijk <stefan@eijk.nu> 3.1.1-5mdk
- removed missing files from %%doc (ACKNOWLEDGMENT PORTS)
- add LC_MESSAGES files (unpackaged files)

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.1-4mdk
- fix doc subpackage group

* Wed Jul 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-3mdk
- Costlessly make check in %%build stage

* Fri May 10 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.1-2mdk
- replace hard link from /usr/bin to /bin by soft link to fix problems
  of people having separate /usr (patch #1)

* Thu May  9 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.1-1mdk
- new version
- remove the reducing of optimizations since gcc seems less buggy now

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.0-4mdk
- Automated rebuild in gcc3.1 environment

* Sun Jan 20 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.0-3mdk
- reduce optimizations to remove gcc bug which makes awk thinking
  that 3 < 2

* Thu Jan 17 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.0-2mdk
- move pgawk (profiling gawk) from /bin to /usr/bin
- take Debian security patch for igawk (thx pixel), but bugfix the
  patch :-)
- fix no-url-tag

* Fri Jul 06 2001 Etienne Faure <etienne@mandrakesoft.com> 3.1.0-1mdk
- version 3.1.0

* Fri May 04 2001 Etienne Faure <etienne@mandrakesoft.com> 3.0.6-4mdk
- Removed i18n patch

* Tue May 02 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.0.6-3mdk
- I18N patch.

* Sat Jan 20 2001 Etienne Faure  <etienne@mandrakesoft.com> 3.0.6-2mdk
- fixed small things to make rpmlint happy

* Wed Aug 09 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.0.6-1mdk
- s|3.0.5|3.0.6|.

* Sun Aug 06 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 3.0.5-2mdk
- some more macroszifications
- BM 

* Sat Jul 22 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 3.0.5-1mdk
- new version
- macros
- provides: awk

* Fri Jun 09 2000 Etienne Faure <etienne@mandrakesoft.com> 3.0.4-3mdk
-rebuild on kenobi

* Sat Apr 08 2000 John Buswell <johnb@mandrakesoft.com> 3.0.4-2mdk
- fixed distribution tag

* Thu Mar 30 2000 John Buswell <johnb@mandrakesoft.com> 3.0.4-1mdk
- 3.0.4 
- fixed groups
- spec helper

* Mon Nov 22 1999 Pixel <pixel@linux-mandrake.com>
- moved the doc to gawk-doc

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add defattr.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Fri Feb 19 1999 Jeff Johnson <jbj@redhat.com>
- Install info pages (#1242).

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1
- don't package /usr/info/dir

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 3.0.3
- added documentation and buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

