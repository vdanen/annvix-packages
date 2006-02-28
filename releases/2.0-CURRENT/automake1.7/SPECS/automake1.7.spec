#
# spec file for package automake1.7
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		automake%{amversion}
%define version 	1.7.9
%define release 	%_revrel

%define amversion 	1.7

%define docheck		0
%{?_with_check: %global docheck 1}

%define alternatives_install_cmd update-alternatives --install %{_bindir}/automake automake %{_bindir}/automake-%{amversion} 20 --slave %{_bindir}/aclocal aclocal %{_bindir}/aclocal-%{amversion}

Summary:	A GNU tool for automatically creating Makefiles
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://sources.redhat.com/automake/
Source:		ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
Patch0:		automake-1.7.9-infofiles.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	autoconf2.5 byacc flex gawk perl tetex texinfo

Requires(post):	info-install, update-alternatives
Requires(preun): info-install, update-alternatives
Requires:	perl, autoconf2.5
Provides:	automake = %{version}-%{release}
Obsoletes:	automake1.5

%description
Automake is a tool for automatically generating Makefiles compliant with
the GNU Coding Standards.


%prep
%setup -q -n automake-%{version}
%patch0 -p0 -b .parallel


%build
export WANT_AUTOCONF_2_5=1
%configure2_5x
%make

%if %{docheck}
# (Abel) reqd2.test tries to make sure automake won't work if ltmain.sh
# is not present.  But automake behaviour changed, now it can handle missing
# libtool file as well, so this test is bogus.
perl -pi -e 's/reqd2.test//g' tests/Makefile
make check  # VERBOSE=1
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -f %{buildroot}%{_bindir}/{automake,aclocal}
rm -f %{buildroot}%{_infodir}/*
install -m 0644 automake*info* %{buildroot}%{_infodir}

pushd %{buildroot}%{_infodir}
    for i in *.info*; do
        mv $i %{name}${i#automake}
    done
popd

mkdir -p %{buildroot}%{_datadir}/aclocal


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info
update-alternatives \
    --install %{_bindir}/automake automake %{_bindir}/automake-%{amversion} 20 \
    --slave   %{_bindir}/aclocal  aclocal  %{_bindir}/aclocal=%{amversion}

%preun
%_remove_install_info %{name}.info
if [ $1 = 0 ]; then
    update-alternatives --remove automake %{_bindir}/automake-%{amversion}
fi


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%{_bindir}/*
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Dec 31 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9-5avx
- set alternatives priority to 20

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9-2avx
- bootstrap build

* Fri Sep 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9-1avx
- 1.7.9
- tune up alternative priority (abel)
- add -with-check option to enable 'make check' (abel)
- adjust P0 to refer to the actual command (*-1.7 rather than *1.7) (abel)
- also owns /usr/share/aclocal (abel)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.7.6-4avx
- Annvix build
- require packages not files

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 1.7.6-3sls
- remove %%{prefix}
- minor spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 1.7.6-2sls
- OpenSLS build
- tidy spec
- remove conflicts since it breaks new automake naming scheme

* Fri Jul 11 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.7.6-1mdk
- new version

* Wed May 21 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.7.5-1mdk
- new version

* Tue May 13 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.7.4-2mdk
- don't obsoletes automake1.6 so that we can put an automake1.6 package
  in contribs for some peculiar packages needing it absolutely

* Wed Apr 30 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.7.4-1mdk
- new version

* Thu Apr 24 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.7.3-2mdk
- fix buildrequires thx to stefan's robot

* Fri Apr 11 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.7.3-1mdk
- new version
- call the package automake1.7
- make it parallel installable with 1.4 (at last), with alternatives

* Fri Dec 13 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.7.2-1mdk
- new version
- take work from Götz Waschk <waschk@informatik.uni-rostock.de> for not
  breaking info entry when switching between automake versions

* Sun Oct 27 2002 Stefan van der Eijk <stefan@eijk.nu> 1.7.1-2mdk
- BuildRequires: autoconf2.5 byacc flex 

* Sat Oct 19 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.7.1-1mdk
- new version

* Wed Oct  9 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.7-1mdk
- new version

* Wed Jul 31 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.6.3-1mdk
- new version

* Fri Jun 14 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.6.2-1mdk
- new version

* Fri May 10 2002 Stefan van der Eijk <stefan@eijk.nu> 1.6.1-2mdk
- Provides automake
- Add version to Conflicts

* Mon Apr 15 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.6.1-1mdk
- new version

* Wed Apr  3 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.6-1mdk
- new version

* Mon Jan 28 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.5-1mdk
- base on work by Han Boetes <han@mijncomputer.nl> for automake1.5

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

# End of file
