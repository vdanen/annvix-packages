%define name	gettext
%define version 0.11.5
%define release 9sls

%define major	2
%define libver	%{major}.2.0
%define lib_name %mklibname intl %{major}

Summary:	GNU libraries and utilities for producing multi-lingual messages.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.gnu.org/software/gettext/
Source:		ftp://ftp.gnu.org/pub/gnu/gettext-%version.tar.bz2
Source1:	po-mode-init.el
Patch1:		gettext-0.10.35-jbj.patch.bz2
Patch4:		gettext-fix-gettextize.patch.bz2
# patch to not issue error messages and warnings with some charset encodings
# we support in MDK. -- pablo
Patch5:		gettext-0.11-charsets.patch.bz2
# patch to avoid a segfault on unknown charsets -- pablo
Patch6:		gettext-0.11.2-unknowncharset.patch.bz2
Patch7:		gettext-0.11.5-msgfmt-i18n.patch.bz2	

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	autoconf2.5, bison, texinfo

Requires:	%{name}-base = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}

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

%package -n %{lib_name}
Summary:	The dynamic libintl library for the gettext package.
Group:		System/Libraries
Provides:	libintl

%description -n %{lib_name}
This package contains the libintl library for the gettext package.

%package devel
Summary:	GNU libraries and utilities for producing multi-lingual messages.
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
Header files, used when the libc does not provide code of handling
multi-lingual messages.

%package base
Summary:	GNU libraries and utilities for producing multi-lingual messages.
Group:		Development/Other
Requires:	%{lib_name} = %{version}-%{release}

%description base
The base package which includes the gettext binary.

%prep
%setup -q -n gettext-%{version}
%patch1 -p1 -b .jbj
perl -p -i -e 's/\ arm-\*/\ arm\*-\*/g' config.sub
%patch4 -p0
%patch5 -p1
# patch to avoid a segfault on unknown encodings -- pablo
%patch6 -p1
%patch7 -p1
# autoconf doesn't like "AC_IN_PATH" to happen in a variable name
find -type f | xargs perl -pi -e 's/HAVE_JAVAC_IN_PATH/HAVE_JAVA_C_IN_PATH/g'

%build
%configure2_5x --enable-shared --with-included-gettext
# (gc) #### DO NOT USE #### percent-make or you'll suffer so much that hell would be a pleasure for you
make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
rm -f $RPM_BUILD_ROOT%{_infodir}/dir $RPM_BUILD_ROOT%{_includedir}/libintl.h $RPM_BUILD_ROOT%{_libdir}/gettext/gnu.gettext.*

# remove non-standard lc directories
for i in en@boldquot en@quot ; do rm -rf $RPM_BUILD_ROOT/%{_datadir}/locale/$i; done
# 'zh' is in fact 'zh_TW'
if [ ! -d $RPM_BUILD_ROOT/%{_datadir}/locale/zh_TW ]; then
	[ -d $RPM_BUILD_ROOT/%{_datadir}/locale/zh ] && \
		mv $RPM_BUILD_ROOT/%{_datadir}/locale/zh \
			$RPM_BUILD_ROOT/%{_datadir}/locale/zh_TW
fi

%find_lang gettext

mkdir htmldoc
mv $RPM_BUILD_ROOT/usr/doc/gettext/* htmldoc

cd $RPM_BUILD_ROOT
mkdir -p bin
mkdir -p ./%{_lib}
mv usr/bin/gettext bin
ln -s ../../bin/gettext usr/bin/gettext
mv .%{_libdir}/libintl.so.* ./%{_lib}/
ln -sf ../../%{_lib}/libintl.so.%{libver} .%{_libdir}/libintl.so

rm -fr $RPM_BUILD_ROOT/%_datadir/locale/locale.alias

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_install_info gettext.info

%post -n %{lib_name} -p /sbin/ldconfig

%preun
%_remove_install_info gettext.info

%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README COPYING ABOUT-NLS AUTHORS BUGS DISCLAIM NEWS THANKS TODO
%{_bindir}/msg*
%{_bindir}/xgettext
%{_bindir}/autopoint
%{_libdir}/%name/*
%{_infodir}/gettext*
%{_mandir}/man1/msg*
%{_mandir}/man1/xgettext*
%{_mandir}/man1/autopoint*
%{_mandir}/man3/*

%files base -f gettext.lang
%defattr(-,root,root)
/bin/gettext
%{_bindir}/gettext
%{_bindir}/ngettext
%{_mandir}/man1/gettext*
%{_mandir}/man1/ngettext*

%files -n %{lib_name}
%defattr(-,root,root)
/%{_lib}/lib*.so.*
%{_libdir}/lib*-*.*.so

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.a
%{_libdir}/lib*.la
# "lib*.so" cannot be used (it should be 'lib[^\.]*\.so' regexp in fact
# but using regexp is not possible here; so we list all files manually
%{_libdir}/libgettextlib.so
%{_libdir}/libgettextsrc.so
%{_libdir}/libintl.so
%{_bindir}/gettextize
%{_datadir}/gettext
%{_datadir}/aclocal/*

%changelog
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
  - change requires to %%version-%%release
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
- Use %%version in the Source tag instead of a hardcoded one.
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
