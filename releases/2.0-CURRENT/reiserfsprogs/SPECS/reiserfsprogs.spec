#
# spec file for package reiserfsprogs
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		reiserfsprogs
%define version		3.6.19
%define release		%_revrel
%define epoch		1

Summary:	The utilities to manage Reiserfs volumes
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.namesys.com/
Source0:	ftp://ftp.namesys.com/pub/reiserfsprogs/%{name}-%{version}.tar.bz2
Patch1:		reiserfsprogs-3.6.2-make-the-force-option-works-in-resize_reiserfs.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Obsoletes:	reiserfs-utils
Provides:	reiserfs-utils

%description
Reiserfs is a file system using a plug-in based object oriented
variant on classical balanced tree algorithms. The results when
compared to the ext2fs conventional block allocation based file system
running under the same operating system and employing the same
buffering code suggest that these algorithms are overall more
efficient, and are becoming more so every passing month.  Loosely
speaking, every month we find another performance cranny that needs
work, and we fix it, and every month we find some way of improving our
overall general usage performance. The improvement in small file space
and time performance suggests that we may now revisit a common OS
design assumption that one should aggregate small objects using layers
above the file system layer. Being more effective at small files DOES
NOT make us less effective for other files, this is a general purpose
FS, and our overall traditional FS usage performance is high enough to
establish that. Reiserfs has a commitment to opening up the FS design
to contributions, and we are now now adding plug-ins so that you can
create your own types of directories and files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1


%build
%configure2_5x
%make OPTFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8
%makeinstall

mv %{buildroot}/{usr/,}sbin
ln -s mkreiserfs %{buildroot}/sbin/mkfs.reiserfs
ln -s reiserfsck %{buildroot}/sbin/fsck.reiserfs
ln -s mkreiserfs.8 %{buildroot}%{_mandir}/man8/mkfs.reiserfs.8
ln -s reiserfsck.8 %{buildroot}%{_mandir}/man8/fsck.reiserfs.8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README ChangeLog COPYING


%changelog
* Sat Jun 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19-2avx
- rebuild

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.6.19-1avx
- 3.6.19

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.6.11-3avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.6.11-2sls
- minor spec cleanups

* Fri Jan 09 2004 Vincent Danen <vdanen@opensls.org> 3.6.11-1sls
- 3.6.11

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 3.6.10-2sls
- OpenSLS build
- tidy spec

* Tue Jul 29 2003 Juan Quintela <quintela@mandrakesoft.com> 3.6.10-1mdk
- reiser has a fsck program.
- use %%configure2_5x.
- patch6 (pcc) integrated upstream.
- patch2 (version) integrated upstream.
- 3.6.10.

* Thu Jul 24 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.6.4-4mdk
- rebuild

* Tue Feb 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.6.4-3mdk
- Remove obsolete Patch5 (Erwan)

* Mon Feb  3 2003 Stew Benedict <sbenedict@mandrakesoft.com> 3.6.4-2mdk
- patch for PPC build - courtesy of Rock Linux

* Tue Jan  7 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.6.4-1mdk
- Bump to version 3.6.4.

* Tue Aug 13 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.6.3-1mdk
- updated to release 3.6.3 (fixes an important bug in
  reiserfsck journal replay process).

* Sat Aug 10 2002 Pixel <pixel@mandrakesoft.com> 3.6.2-2mdk
- make the force option works in resize_reiserfs

* Wed Jul 10 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.6.2-1mdk
- new release (faster, more tests, ...)
- use macros
- get rid of sub-shells
- spec simplifications
- remove useless ./ steps in links
- workaround the move from /sbin to /usr/sbin
- fix provides for updates

* Fri Jun 21 2002 Stew Benedict <sbenedict@mandrakesoft.com> 3.x.1b-2mdk
- drop endian patches - merged upstrean (P4)

* Fri Mar 29 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.x.1b-1mdk
- version 3.x.1b.

* Thu Feb 21 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.x.1a-1mdk
- version 3.x.1a.
- removed Patch0: -3.x.0i-v2message.patch.bz2 (merged).
- removed Patch1: -3.x.0i-mkstemp.patch.bz2 (unused).
- removed Patch2: -3.x.0i-non-interactive-when-force.patch.bz2 (merged),
- readapted Patch3: -3.x.0i-reformat-banner-version.patch.bz2

* Fri Sep 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.x.0j-5mdk
- Rebuild.

* Sat Aug 18 2001 Pixel <pixel@mandrakesoft.com> 3.x.0j-4mdk
- non interactive resize_reiserfs with force option 

* Sat Aug  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.x.0j-3mdk
- Add ia64 patch.

* Wed May  2 2001 Stew Benedict <sbenedict@mandrakesoft.com> 3.x.0j-2mdk
- include PPC now, with patches

* Thu Apr  5 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.x.0j-1mdk
- updated to release 3.x.0j.

* Tue Apr  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.x.0i-3mdk
- fsck.reiserfs should be symlinked to /bin/true to avoid problems at
  boot.

* Mon Apr  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.x.0i-2mdk
- Reformat banner to don't make ugly message at boot.
- Readd force patch.

* Sat Mar 31 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.x.0i-1mdk
- use reiserfsprogs only
- add RedHat mkstemp patch.
- removed unused patches.

* Tue Mar 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.6.25-7mdk
- 3.x.0i.

* Thu Mar 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.6.25-6mdk
- 3.x.0h.

* Sat Feb 24 2001 Pixel <pixel@mandrakesoft.com> 3.6.25-5mdk
- non-interactive-when-force option is used (for batch use, like DrakX)

* Tue Feb 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.6.25-4mdk
- 3.x.0d.

* Mon Jan 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.6.25-3mdk
- Readd fake fsck.reiserfs.
- Put utils in /sbin and not somewhere else.

* Fri Jan 25 2001 David BAUDENS <baudens@mandrakesoft.com> 3.6.25-2mdk
- ExcludeArch PPC

* Wed Jan 24 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.6.25-1mdk
- First version dumped from kernel.

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
