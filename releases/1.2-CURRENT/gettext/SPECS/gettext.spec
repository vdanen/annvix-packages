#
# spec file for package gettext
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gettext
%define version 	0.14.5
%define release 	%_revrel

%define major		3
%define libname		%mklibname intl %{major}

Summary:	GNU libraries and utilities for producing multi-lingual messages
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.gnu.org/software/gettext/
Source:		ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz.sig
# (gb) some tests try to link non-pic static libs into a dso (XXX patch as XFAIL?)
Patch0:		gettext-0.14.5-pic.patch
Patch1:		gettext-0.14.2-charsets.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, bison, texinfo, automake1.8, flex

Requires:	%{name}-base = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%mklibname expat 0
Requires(post):	info-install
Requires(preun): info-install

%description
The GNU gettext package provides a set of tools and documentation for producing
multi-lingual messages in programs. Tools include a set of conventions about
how programs should be written to support message catalogs, a directory and
file naming organization for the message catalogs, a runtime library which
supports the retrieval of translated messages, and stand-alone programs for
handling the translatable and the already translated strings. Gettext provides
an easy to use library and tools for creating, using, and modifying natural
language catalogs and is a powerful and simple method for internationalizing
programs.

If you would like to internationalize or incorporate multi-lingual messages
into programs that you're developing, you should install gettext.


%package -n %{libname}
Summary:	The dynamic libintl library for the gettext package
Group:		System/Libraries
Provides:	libintl
Provides:	libintl2
Obsoletes:	libintl2

%description -n %{libname}
This package contains the libintl library for the gettext package.


%package devel
Summary:	GNU libraries and utilities for producing multi-lingual messages
Group:		Development/Other
Requires:	%{name} = %{version}
Requires(post):	info-install
Requires(preun): info-install

%description devel
Header files, used when the libc does not provide code of handling
multi-lingual messages.


%package base
Summary:	GNU libraries and utilities for producing multi-lingual messages
Group:		Development/Other
Requires:	%{libname} = %{version}

%description base
The base package which includes the gettext binary.


%prep
%setup -q
%patch0 -p1 -b .pic
%patch1 -p1 -b .more_charsets

# (Abel) disable lang-java test, java bytecode failed to run
sed -i -e 's/lang-java//' gettext-tools/tests/Makefile.in


%build
%configure2_5x \
    --enable-shared \
    --with-included-gettext \
    --disable-csharp

make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

# remove unwanted files
rm -f %{buildroot}%{_includedir}/libintl.h \
      %{buildroot}%{_datadir}/locale/locale.alias \
      %{buildroot}%{_libdir}/GNU.Gettext.dll \
      %{buildroot}%{_libdir}/%{name}/gnu.gettext.* \
      %{buildroot}%{_datadir}/%{name}/*.jar
rm -f gettext-runtime/intl-java/javadoc2/package-list

# remove non-standard lc directories
for i in en@boldquot en@quot ; do rm -rf %{buildroot}/%{_datadir}/locale/$i; done

# move installed doc back to %%doc
rm -rf htmldoc examples
mkdir htmldoc
for i in gettext-runtime/man/*.html; do
    rm -f %{buildroot}%{_datadir}/doc/gettext/`basename $i`
done
rm -rf %{buildroot}%{_datadir}/gettext/javadoc*
mv %{buildroot}%{_datadir}/doc/gettext/* %{buildroot}%{_datadir}/doc/libasprintf/* htmldoc

# move crucial stuff to /lib and /bin
pushd %{buildroot}
    mkdir -p bin
    mkdir -p ./%{_lib}
    mv usr/bin/gettext bin/
    ln -s ../../bin/gettext usr/bin/gettext
    mv .%{_libdir}/libintl.so.* ./%{_lib}/
    rm -f .%{_libdir}/libintl.so
    ln -s ../../%{_lib}/libintl.so.%{major} .%{_libdir}/libintl.so
popd

%find_lang %{name} --all-name


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info gettext.info


%post devel
%_install_info autosprintf.info


%post -n %{libname} -p /sbin/ldconfig


%preun
%_remove_install_info gettext.info


%preun devel
%_remove_install_info autosprintf.info


%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc README COPYING AUTHORS NEWS THANKS
%{_bindir}/msg*
%{_bindir}/xgettext
%{_bindir}/autopoint
%{_bindir}/envsubst
%{_bindir}/gettext.sh
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/hostname
%{_libdir}/%{name}/project-id
%{_libdir}/%{name}/urlget
%{_libdir}/%{name}/user-email
%{_infodir}/gettext*
%{_mandir}/man1/msg*
%{_mandir}/man1/xgettext*
%{_mandir}/man1/autopoint*
%{_mandir}/man1/envsubst*
%{_mandir}/man3/*

%files base -f gettext.lang
%defattr(-,root,root)
/bin/gettext
%{_bindir}/gettext
%{_bindir}/ngettext
%{_mandir}/man1/gettext*
%{_mandir}/man1/ngettext*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/lib*.so.*
%{_libdir}/lib*-*.*.so
%{_libdir}/lib*.so*

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.a
%{_libdir}/lib*.la
# "lib*.so" cannot be used (it should be 'lib[^\.]*\.so' regexp in fact
# but using regexp is not possible here; so we list all files manually
%{_libdir}/libgettextlib.so
%{_libdir}/libgettextsrc.so
%{_libdir}/libintl.so
%{_libdir}/libasprintf.so
%{_libdir}/libgettextpo.so
%{_bindir}/gettextize
%{_datadir}/gettext
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/autosprintf*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq
- install autosprintf.info

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14.5-1avx
- 1.14.5
- build --disabled-shared autoconf-lib-link tests --with-pic (gbeauchesne)
- BuildRequires: automake1.8 not automake1.7
- don't use parallel make

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14.1-5avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14.1-4avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14.1-3avx
- bootstrap build

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.14.1-2avx
- Annvix build

* Fri Apr 30 2004 Vincent Danen <vdanen@opensls.org> 0.14.1-1sls
- 0.14.1
- rename P5 to P1
- sorta sync with cooker (0.14.1-4mdk):
  - P0: fix libtool 1.5 DESTDIR issue (abel)
  - parallel make works now (abel)
  - bump major to 3 (peroyvind)
  - Provides: devel(libintl) on -devel pkg (charles)
  - fix %%{_libdir}/libintl.so link (tvignaud)
- fix amd64 compile (thanks gwenole)
- Requires: lib64expat0 ifarch is amd64
- hack to make it build with automake 1.7 (we don't ship 1.8)
- NOTE: should Provides/Obsoletes: libintl2 for smooth upgrade before
  1.0-RELEASE

- remove P7; LSB is going to accomodate current gettext behaviour

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 0.11.5-9sls
- remove %%build_opensls macro
- remove %%prefix
- minor spec cleanups
- remove htmldoc
- README and COPYING files should not be duplicated in each package

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 0.11.5-8sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to not require or build emacs-specific stuff

* Wed Jul  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.11.5-7mdk
- Rebuild

* Tue Jun 03 2003 Stew Benedict <sbenedict@mandrakesoft.com> 0.11.5-6mdk
- LSB/LI18NUX test requirements - patch7
- (msgfmt ignore duplicate strings in multiple domains when -o specified)
- BuildRequires: emacs-el, use %%mklibname

* Thu May 08 2003 Stefan van der Eijk <stefan@eijk.nu> 0.11.5-5mdk
- BuildRequires: autoconf2.5 bison

* Mon Apr 28 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 0.11.5-4mdk
- don't install java binaries to not depend on libgcj

* Fri Apr 25 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 0.11.5-3mdk
- use %%configure2_5x

* Fri Dec 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.11.5-2mdk
- Rebuild

* Fri Dec 13 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 0.11.5-1mdk
- shamelessly use work from Austin Acton <aacton@yorku.ca>:
  - bump version and libver
  - don't run autoconf explicitly (fails)
  - replace patch 2 (arm*-*) with perl command (easier updates)
  - add autopoint, and new files in libdir/gettext and datadir/emacs

* Tue Aug 27 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 0.11.2-8mdk
- patch to avoid segfaults on unknown encodings

* Mon Jul 08 2002 Stefan van der Eijk <stefan@eijk.nu> 0.11.2-7mdk
- BuildRequires: emacs-bin

* Sun Jul  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.11.2-6mdk
- rpmlint fixes: hardcoded-library-path

* Thu Jul  4 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 0.11.2-5mdk
- try to fix %%makeinstall call so that there are no missing files in
  po subdir (use %%makeinstall_std and don't specify additional
  directories)

* Mon Jun  3 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 0.11.2-4mdk
- use work from Götz Waschk <waschk@linux-mandrake.com>
  - change requires to %%{version}-%%{release}
  - update source 1 (emacs po-mode init)
  - fix libintl version number to 2.0.1
- fix silly html doc in /usr/doc/gettext -> %%docdir/htmldoc

* Sat Jun  1 2002 Stefan van der Eijk <stefan@eijk.nu> 0.11.2-3mdk
- BuildRequires
- fix release on previous changelog (1mdk --> 2mdk)

* Mon May 27 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 0.11.2-2mdk
- moved shared libs to the libintl sub-package

* Thu May 23 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 0.11.2-1mdk
- updated to 0.11.2
- increased major number

* Wed Oct 17 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.40-3mdk
- fix no-documentation

* Mon Oct 15 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.40-2mdk
- fix invalid-lc-messages-dir
- fix patch-not-applied
- fix obsolete-tag Copyright
- revive three Patches (please packagers -> when a patch don't "pass"
  anymore, don't just ignore it, do your work!!)
- use RH site-start Emacs resource file for po-mode
- more docs

* Fri Sep 28 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.40-1mdk
- new version

* Wed Sep 12 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.39-2mdk
- mark emacs site-start file as conffile

* Tue Jul 31 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 0.10.39-1mdk
- update to 0.10.39

* Thu Jul  5 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.38-2mdk
- rebuild

* Tue May 29 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.10.38-1mdk
- Release 0.10.38 (should correct po/Makefile generation problem)
- Add man pages
- No longer ship charset.alias, it was wrongly generated with previous version
(and it is not needed for system with glibc >= 2.1)

* Tue May 15 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 0.10.37-3mdk
- small patch to avoid issuing warning messages fro charsets we do support

* Fri May 11 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.10.37-2mdk
- Fix a dangling symlink (Abel).

* Fri Apr 20 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.10.37-1mdk
- GNU gettext 0.10.37.
- Include the charset.alias file.

* Wed Apr 18 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.10.36-1mdk
- New and shiny 0.10.36.
- Patch cleanup.
- Split out the dynamic libraries.
- Remove msghack but put in ngettext.
- Don't run aclocal before ./configure.
- Use %%{version} in the Source tag instead of a hardcoded one.
- In the Source tag s/alpha/ftp/;

* Tue Apr 17 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.35-20mdk
- move /usr/bin/gettext to /bin/gettext so that initscripts can be
  translated before /usr is ever mounted

* Tue Apr 17 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.10.35-19mdk
- Move gettextize to devel package
- Install po/Makefile.in.in in /usr/share/gettext/po.
  gettextize was broken without this.
- Install ABOUT-NLS in /usr/share/gettext.
  gettextize was broken without this.

* Thu Mar 22 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.35-18mdk
- split main package because initscripts requires gettext binary, and we
  want to have a reasonable "smallest" install
- add emacs site-start for el file
- remove elc version of the mode

* Tue Nov  7 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.35-17mdk
- fix dependency on devel package
- add documentation

* Wed Aug 23 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.35-16mdk
- automatically added packager tag

* Tue Aug 22 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.35-15mdk
- bugfixed gettextize when headers are not there
  thanks to <rchaillat@mandrakesoft.com>

* Tue Jul 18 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.35-14mdk
- macros

* Fri May  5 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 0.10.35-13mdk
- quick patch to have it work!

* Sat Apr 08 2000 John Buswell <johnb@mandrakesoft.com> 0.10.35-12mdk
- added devel package

* Thu Mar 30 2000 John Buswell <johnb@mandrakesoft.com> 0.10.35-11mdk
- fixed groups
- Removed version number from spec filename
- spec-helper

* Tue Nov 02 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- rebuild for new environment

* Wed Jun 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- s/arch-RedHat/arch-Mandrake/
- msghack updates.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Mon Mar 08 1999 Cristian Gafton <gafton@redhat.com>
- added patch for misc hacks to facilitate rpm translations

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to allow to build on ARM

* Wed Sep 30 1998 Jeff Johnson <jbj@redhat.com>
- add Emacs po-mode.el files.

* Sun Sep 13 1998 Cristian Gafton <gafton@redhat.com>
- include the aclocal support files

* Fri Sep  3 1998 Bill Nottingham <notting@redhat.com>
- remove devel package (functionality is in glibc)

* Tue Sep  1 1998 Jeff Johnson <jbj@redhat.com>
- update to 0.10.35.

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- add gettextize.
- create devel package for libintl.a and libgettext.h.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Nov 02 1997 Cristian Gafton <gafton@redhat.com>
- added info handling
- added misc-patch (skip emacs-lisp modofications)

* Sat Nov 01 1997 Erik Troan <ewt@redhat.com>
- removed locale.aliases as we get it from glibc now
- uses a buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- Built against glibc
