#
# spec file for package mt-st
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mt-st
%define version		0.8
%define release		%_revrel

Summary:	Programs to control tape device operations
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Archiving/Backup
URL:		http://ibiblio.org/pub/Linux
Source:		http://ibiblio.org/pub/Linux/system/backup/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}


%description
The mt-st package contains the mt and st tape drive management
programs. Mt (for magnetic tape drives) and st (for SCSI tape devices)
can control rewinding, ejecting, skipping files and blocks and more.


%prep
%setup -q


%build
%make CFLAGS="%{optflags} -Wall" MANDIR=%{_mandir}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/{bin,sbin}
mkdir -p %{buildroot}%{_mandir}/man{1,8}
%makeinstall \
    MANDIR=%{buildroot}%{_mandir} \
    BINDIR=%{buildroot}/bin \
    SBINDIR=%{buildroot}/sbin


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc COPYING README README.stinit mt-st-%{version}.lsm stinit.def.examples
/bin/mt
/sbin/stinit
%{_mandir}/man1/mt.1*
%{_mandir}/man8/stinit.8*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8-1avx
- first Annvix package

* Fri Aug 13 2004 Giusppe Ghibò <ghibo@mandrakesoft.com> 0.8-1mdk
- Release 0.8.

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.7-2mdk
- rebuild
- use %%make macro

* Tue Mar 26 2002 François Pons <fpons@mandrakesoft.com> 0.7-1mdk
- 0.7.

* Fri Mar 22 2002 David BAUDENS <baudens@mandrakesoft.com> 0.6-4mdk
- Clean after build
- Remove de description and summary

* Wed Nov 07 2001 François Pons <fpons@mandrakesoft.com> 0.6-3mdk
- added url tag.
- updated source url.

* Tue Jul 03 2001 François Pons <fpons@mandrakesoft.com> 0.6-2mdk
- build release, update distribution tag.

* Fri Dec 01 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.6-1mdk
- new and shiny source dumped on into cooker.
- use the version macro so that we do not have to change both the version
  for the package and the version number in the filename of the source.
- remove the obsolete datacompression command.
- remove the obsolete buildroot patch.

* Thu Jul 20 2000 François Pons <fpons@mandrakesoft.com> 0.5b-8mdk
- macroszifications.

* Fri Mar 31 2000 François Pons <fpons@mandrakesoft.com> 0.5b-7mdk
- updated Group.

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with rh changes.
- enable "datcompression" command(r).

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Wed Feb 10 1999 Preston Brown <pbrown@redhat.com>
- upgrade to .5b, which fixes some cmd. line arg issues (bugzilla #18)

* Thu Jul 23 1998 Jeff Johnson <jbj@redhat.com>
- package for 5.2.

* Sun Jul 19 1998 Andrea Borgia <borgia@cs.unibo.it>
- updated to version 0.5
- removed the touch to force the build: no binaries are included!
- added to the docs: README.stinit, stinit.def.examples
- made buildroot capable

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 20 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
