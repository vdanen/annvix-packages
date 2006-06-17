#
# spec file for package spec-helper
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		spec-helper
%define version 	0.23
%define release 	%_revrel

%define distrib		Annvix

Summary:	Tools to ease the creation of rpm packages
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.mandriva.com
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	perl ldconfig findutils python gettext

%description
Tools to ease the creation of rpm packages for the %{distrib} distribution.
Compress man pages using bzip2, strip executables, convert links...


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
# without the following, make has a hard time... stupid mkrel
perl -pi -e 's|%%mkrel||g' spec-helper.spec


%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot} bindir=%{_bindir} rpmmacrosdir=%{_sys_macros_dir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/macroszification
%{_datadir}/spec-helper
%{_sys_macros_dir}/%{name}.macros

%files doc
%defattr(-,root,root)
%doc AUTHORS Howto-spec-helper ChangeLog


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.23
- 0.23
- hack out some %%mkrel junk to make "make" happier
- add -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11-4avx
- correct the buildroot

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11-2avx
- bootstrap build

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11-1avx
- 0.11
  - handle filenames starting with - (flepid)
  - other cleanups and speedups (tvignaud)
  - use " around the section name in spec-helper (flepied)

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.2-6avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.9.2-5sls
- minor spec cleanups
- remove %%prefix
- remove %%build_openssls

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 0.9.2-4sls
- OpenSLS build
- tidy spec
- fix URL

* Thu Oct  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.2-3mdk
- also nuke /lib64/security/ paths

* Thu Oct  9 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.9.2-2mdk
- remove /lib/security from pam config files

* Fri Aug  1 2003 Pixel <pixel@mandrakesoft.com> 0.9.2-1mdk
- remove file alike /usr/lib/perl5/5.8.*/i386-linux-thread-multi/perllocal.pod

* Fri Jul 25 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.1-1mdk
- handle amd64 in main spec-helper script

* Fri Jun 20 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.9-1mdk
- don't strip /usr/lib/debug files (Götz Waschk) (bug #4087)

* Fri Feb 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.8-1mdk
- added fix-po from Pablo to fix korean translation of GNOME

* Fri Dec 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.7-1mdk
- remove /usr/share/info/dir if not a symlink

* Thu Aug 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.6.1-1mdk
- fixed clean_files to remove correctly the CVS dirs (thx to Stephane Chatty)
- clean_files removes .cvsignore

* Wed Jul 24 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6-6mdk
- fix lib64 support, use $RPM_ARCH and don't execute arch command.

* Wed Jun 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6-5mdk
- fix modules location in pam.d config files.

* Wed Feb 20 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.6-4mdk
- don't gprintify if init scripts doesn't contain a source functions

* Sat Feb 16 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.6-3mdk
- don't call gprintify if init.d is empty.

* Mon Jan 28 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.6-2mdk
- requires /usr/bin/python for gprintify (Florin)

* Tue Jan 15 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.6-1mdk
- correct gprintify to protect the shell variables by ""

* Thu Nov 22 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.5-1mdk
- gprintify init scripts.

* Tue Aug 21 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.4-2mdk
- work cleanly with the packages without file

* Mon Nov 13 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.4-1mdk
- added lib_symlinks to call ldconfig which builds the right symlinks
to libraries.

* Fri Oct 20 2000 François Pons <fpons@mandrakesoft.com> 0.3-7mdk
- clean_files: remove CVS directories.

* Mon Sep  4 2000 Pixel <pixel@mandrakesoft.com> 0.3-6mdk
- fix EXCLUDE_FROM_STRIP in strip_files

* Sat Aug 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3-5mdk
- macroszification: Add initrddir macroszification.
- spec-helper.spec: macroszification :-(

* Fri Aug 18 2000 Pixel <pixel@mandrakesoft.com> 0.3-4mdk
- clean_perl: remove the -x (silly me), don't remove *.ix (used for devel)

* Thu Aug 17 2000 Pixel <pixel@mandrakesoft.com> 0.3-3mdk
- spec-helper: add a rule to call clean_perl
- clean_perl: created, removes .packlist and empty *.bs
- Makefile (rpm): change the dependency to dis

* Thu Jul 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3-2mdk
- macroszification: Check Prefix only when %{?prefix}? is present in
the spec file

* Sat Jul 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.3-1mdk
- macroszification:	Add check for Docdir: it's not good !!
- macroszification: checking configure/makeinstall only if there is no
  nocheck
- macroszification:	Add the -o option to only process docdir and mandir

* Thu Jul 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-9mdk
- macroszification: a new greatest hit.

* Tue May  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.2-8mdk
- exit 0 if no RPM_BUILD_ROOT variable set to allow build with no BuildRoot.

* Sat Apr 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-7mdk
- relative_me_babe: a new greatest hit.

* Fri Apr  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-6mdk
- compress_files: Remove orphan link only for manpage.

* Wed Apr  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-5mdk
- compress_files: When we find an orphan man pages, erase it (any better 
  idea ?)

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-4mdk
- spec-helper.spec: Adjust groups.
- initscripts.spec: Requires: perl

* Fri Mar 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-3mdk
- compress_files: If we found gzip file decompress and bzip2 them.

* Thu Mar 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.2-2mdk
- compress_files: Don't compress whatis and dir in /usr/{info|man}.

* Mon Feb 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.2-1mdk
- 0.2: added EXCLUDE_FROM_COMPRESS and EXCLUDE_FROM_STRIP environment
variables.

* Tue Feb 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1-3mdk
- Add mail of fred about spec-helper as doc.

* Fri Feb 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1-2mdk
- cvs import.

* Fri Feb 18 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.1-1mdk
- first version.

# end of file
