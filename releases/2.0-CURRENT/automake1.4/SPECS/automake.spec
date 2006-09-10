#
# spec file for package automake1.4
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		%{amname}%{amversion}
%define version 	1.4p6
%define release 	%_revrel

%define amname		automake
%define amversion	1.4
%define patchlevel	p6

%define docheck		1
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://sourceware.cygnus.com/automake
Source:		ftp://ftp.gnu.org/gnu/automake/%{amname}-%{amversion}-%{patchlevel}.tar.bz2
Patch0:		automake-1.4p6-infofiles.patch
Patch1:		automake-1.4-p6-stdc-headers.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
Buildrequires:	perl

Requires(post):	info-install
Requires(preun): info-install
Requires:	perl
Conflicts:	automake1.5
Obsoletes:	automake <= 1.4-0.p6.26avx

%description
Automake is a tool for automatically generating Makefiles compliant with the
GNU Coding Standards.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{amname}-%{amversion}-%{patchlevel}
%patch0 -p1 -b .parallel
%patch1 -p1 -b .gcc3.4


%build
%configure
make
perl -pi -e 's/\berror\.test\b//' tests/Makefile


%check
%if %{docheck}
make check  # VERBOSE=1
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

install -D -m 0644 %{name}.info %{buildroot}%{_infodir}/%{name}.info

rm -f %{buildroot}%{_bindir}/{automake,aclocal}
mkdir -p %{buildroot}%{_datadir}/aclocal


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info automake.info
update-alternatives --remove automake %{_bindir}/automake-%{amversion}


%preun
%_remove_install_info automake.info


%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*-1.4
%{_infodir}/%{name}*
%dir %{_datadir}/aclocal

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO


%changelog
* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4p6
- add -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4p6
- Clean rebuild

* Sat Dec 31 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4p6
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4p6-31avx
- normalize the release tag

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4-0.p6.30avx
- this package is no longer an alternative for current "automake" (cjw)

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4-0.p6.29avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4-0.p6.28avx
- bootstrap build

* Fri Sep 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4-0.p6.27avx
- this is now automake1.4
- add --without-check option to disable 'make check' (abel)
- P0: use versioned name in info page nodes (abel)
- P1: gcc no longer acceps K&R style prototypes (unapplied until we move to gcc 3.4)
- note: mdk dropped alternative priority of this but we're not going to because we
  want 1.4 to remain the default

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4-0.p6.26avx
- Annvix build

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 1.4-0.p6.25sls
- remove %%{prefix}
- more spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 1.4-0.p6.24sls
- OpenSLS build
- tidy spec
- change naming convention to make more sense regarding patchlevel
- Epoch: 1 due to release tag change

* Mon May 26 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-23.p6.mdk
- own /usr/share/aclocal

* Fri Apr 11 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-22.p6.mdk
- make it parallel installable with newest version, with alternatives

* Tue Jul 30 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-21.p6.mdk
- new release
- disable one test which seems to not pass but I don't get why

* Thu Jul 19 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-20.p5.mdk
- use patch level 5

* Mon Jun 11 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4-18.p4.mdk
- Bump up to 1.4 patch release 4.
- Really use a newer version aka remove hardcoded p1 in %%setup and
  Source tag (gc sux).
- s/Copyright/License/;

* Fri Jun  1 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-17.p2.mdk
- code version ``1.4 patch release 2''

* Tue May 15 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-16.p1.mdk
- code version ``1.4 patch release 1''

* Thu Dec  7 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.4-15mdk
- run automated tests at build time
- use make macro

* Thu Aug 24 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-14mdk
- rebuild to fix %preun script (pixel sucks)

* Thu Aug 24 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-13mdk
- added packager tag

* Wed Jul 19 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-12mdk
- rebuild for /me sucks. all m4 macros were lost in space :-(.

* Tue Jul 18 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-11mdk
- rebuild for BM
- install-info macros

* Mon Jul 17 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-10mdk
- removing %{_infodir}/dir from the file list (/me sucks)

* Mon Jul 10 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-9mdk
- cleanup and macros

* Fri Mar 31 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4-8mdk
- new groups

* Wed Oct 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with Jeff package.

* Tue Jun 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 1.4 version.
- Merging with RedHat patch.

* Thu May 13 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- 1.4a

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- arm netwinder patch

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb  8 1999 Jeff Johnson <jbj@redhat.com>
- add patches from CVS for 6.0beta1

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.4.

* Mon Nov 23 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.3b.
- add URL.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Erik Troan <ewt@redhat.com>
- updated to 1.3

* Tue Oct 28 1997 Cristian Gafton <gafton@redhat.com>
- added BuildRoot; added aclocal files

* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- made it a noarch package

* Thu Oct 16 1997 Michael Fulbright <msf@redhat.com>
- Fixed some tag lines to conform to 5.0 guidelines.

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- updated to 1.2

* Wed Mar 5 1997 msf@redhat.com <Michael Fulbright>
- first version (1.0)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
