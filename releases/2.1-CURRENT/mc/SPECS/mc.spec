#
# spec file for package mc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mc
%define version		4.6.1
%define release		%_revrel

Summary:	A user-friendly file manager and visual shell
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		File Tools
URL:		http://www.ibiblio.org/mc/
Source0:	ftp://ftp.gnome.org:/pub/GNOME/stable/sources/mc/%{name}-%{version}.tar.bz2
Patch0:		mc-4.6.1-fdr-utf8.patch
Patch1:		mc-4.6.1-rpm_obsolete_tags.patch
Patch2:		mc-4.6.1-mdv-bash32.patch
Patch3:		mc-4.6.1-mdv-slang2.patch
Patch4:		mc-4.6.1-mdv-tempfiles.patch
Patch5:		mc-4.6.1-mdv-2gb.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	e2fsprogs-devel
BuildRequires:	pam-devel
BuildRequires:	slang-devel
BuildRequires:	glib2-devel

Requires:	groff

%description
Midnight Commander is a visual shell much like a file manager, only with way
more features.  It is text mode, but also includes mouse support if you are
running GPM.  With mc you are able to ftp as well as view tar, zip, and rpm
files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .utf8
%patch1 -p1 -b .rpm_obsolete_tags
%patch2 -p0 -b .bash32
%patch3 -p0 -b .slang2
%patch4 -p1 -b .tempfiles
%patch5 -p1 -b .2gb


%build
%serverbuild
# libcom_err of e2fsprogs and krb5 conflict. Watch this hack. -- Geoff.
# <hack>
mkdir -p %{_lib}
ln -sf /%{_lib}/libcom_err.so.2 %{_lib}/libcom_err.so
export LDFLAGS="-L`pwd`/%{_lib}"
# </hack>


%configure2_5x \
    --with-debug \
    --without-included-gettext \
    --without-included-slang \
    --with-screen=slang \
    --enable-nls \
    --enable-charset \
    --enable-largefile \
    --without-x \
    --without-gpm-mouse

# don't use make macro, mc doesn't support parallel compilation
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/{pam.d,profile.d,X11/wmconfig}

#fix mc-wrapper.sh
perl -p -i -e 's/rm -f \"/rm -rf \"/g' lib/mc-wrapper.sh

%makeinstall

install lib/{mc.sh,mc.csh} %{buildroot}%{_sysconfdir}/profile.d

# remove unwanted locale files
rm -rf %{buildroot}%{_datadir}/locale


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-, root, root)
%{_bindir}/mc
%{_bindir}/mcedit
%{_bindir}/mcmfmt
%{_bindir}/mcview
%dir %{_libdir}/mc
%{_libdir}/mc/cons.saver
%_datadir/mc/cedit.menu
%_datadir/mc/edit.indent.rc
%_datadir/mc/edit.spell.rc
%{_datadir}/mc/mc.ext
%{_datadir}/mc/mc.hint
%_datadir/mc/mc.hint.*
%{_datadir}/mc/mc.hlp
%_datadir/mc/mc.hlp.*
%{_datadir}/mc/mc.lib
%{_datadir}/mc/mc.menu
%{_datadir}/mc/mc.menu.*
%{_datadir}/mc/mc.charsets
%{_datadir}/mc/extfs/*
%{_mandir}/man1/*
%dir %{_datadir}/mc
%dir %{_datadir}/mc/bin
%_datadir/mc/bin/*
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_datadir}/mc/syntax/
#%{_datadir}/mc/term/

%files doc
%defattr(-, root, root)
%doc FAQ COPYING NEWS README


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1
- rebuild against new e2fsprogs
- update the buildreqs

* Wed Nov 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1
- rebuild against new glib2.0

* Mon Oct 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1
- P4: fix bug that leaves temporary files lying around (upstream bug
  #13953)
- P5: fix a bug that prevents >2GB ssh file transfers from working (upstream
  bug #15524)
- rebuild against new pam

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1
- P2: fix build against recent bash
- P3: fix build against new slang
- rebuild against new slang
- rebuild against new glib2
- fix group

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1
- rebuild against new pam

* Fri Jun 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1
- spec cleanups
- rebuild against new e2fsprogs and new glib2.0

* Fri Jun 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1
- P1: remove copyright tag and s/serial/epoch tag in rpm vfs (mpol)
- rebuild against new pam
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1-2avx
- rebuild against new glib2.0

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.1-1avx
- 4.6.1
- drop all unrequired patches

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.0-12avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.0-11avx
- rebuild

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> - 4.6.0-10avx
- P16: make the wrapper script work (oden)

* Tue Sep 07 2004 Vincent Danen <vdanen-at-build.annvix.org> - 4.6.0-9avx
- renumber patches; patch policy
- update description
- sync with cooker 4.6.0-11mdk:
  - P5: image extension s/ee/gqview (bug #7907) (mpol)
  - [DIRM] (misc)
  - update P1, use gqview for images as upstream does (mpol)
  - add unzip vfs (mpol)
  - drop P2, merged in P6 to P10 (mpol)
  - P5: "secret" redhat cpio fix (mpol)
  - P7: build against slang-utf8 (mpol)
  - P8, P10, P11, P12: add utf8 patches from fedora/suse (mpol)
  - P9: (jumbo patch) several fixes, updates, etc. (mpol)
  - disable charset conversion (mpol)
  - security fix for vfs/extfs CAN-2004-0494 (mpol)
  - P14: add info/obsoletes, info/license to rpm extfs (mpol)
  - P15: fix crash on use of large syntax file (mpol)
  - P16: fix coloring of diffs of diffs (mpol)

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> - 4.6.0-8avx
- Annvix build

* Mon May 10 2004 Vincent Danen <vdanen@opensls.org> - 4.6.0-7sls
- P2 fixes CAN-2004-0226, CAN-2004-0231, CAN-2004-0232
- P3 don't build ta locale as it breaks build (sbenedict)

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> - 4.6.0-6sls
- minor spec cleanups

* Wed Jan 21 2004 Vincent Danen <vdanen@opensls.org> - 4.6.0-5sls
- OpenSLS build
- tidy spec
- security fix for CAN-2003-1023

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
