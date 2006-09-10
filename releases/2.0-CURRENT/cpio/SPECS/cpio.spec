#
# spec file for package cpio
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		cpio
%define version 	2.6
%define release 	%_revrel

Summary:	A GNU archiving program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving
URL:		http://www.fsf.org/software/cpio
Source:		ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.bz2
Patch0:		cpio-2.6-mtime.patch
Patch1:		cpio-2.6-svr4compat.patch
Patch2:		cpio-2.6-no-libnsl.patch
Patch3:		cpio-2.6-i18n.patch
Patch4:		cpio-2.6-CAN-1999-1572.patch
Patch5:		cpio-2.6-chmodRaceC.patch
Patch6:		cpio-2.6-dirTraversal.patch
Patch7:		cpio-2.6-compil-gcc4.patch
Patch8:		cpio-2.6-CVE-2005-4268.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo

Requires(post):	info-install
Requires(preun): info-install
Requires:	rmt

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .mtime
%patch1 -p1 -b .svr4compat
%patch2 -p1 -b .no-libnsl
%patch3 -p1 -b .i18n
%patch4 -p0 -b .can-1999-1572
%patch5 -p1 -b .can-2005-1111
%patch6 -p1 -b .can-2005-1229
%patch7 -p0 -b .gcc4
%patch8 -p1 -b .cve-2005-4268

# needed by P4
autoconf


%build
%configure2_5x \
    --bindir=/bin \
    --with-rmt=/sbin/rmt \
    CPPFLAGS=-DHAVE_LSTAT=1

%make
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%kill_lang %{name}
%find_lang %{name}

# remove unpackaged files
rm -f %{buildroot}%{_mandir}/man1/mt.1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info


%preun
%_remove_install_info %{name}.info


%files -f %{name}.lang
%defattr(-,root,root)
/bin/cpio
%{_infodir}/cpio.*
%{_mandir}/man1/cpio.1*

%files doc
%defattr(-,root,root)
%doc README NEWS AUTHORS ChangeLog


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- spec cleanups
- remove locales

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- fix group

* Fri Feb 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- P8: security fix for CVE-2005-4268

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6-3avx
- require rmt rather than tar (tar provides rmt-tar rather than rmt
  since we don't use alternatives anymore)
- P7: fix build with gcc4 (we don't use it yet, but it doesn't hurt to have)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6-2avx
- bootstrap build (new gcc, new glibc)

* Thu Jul 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6-1avx
- 2.6
- make it require tar rather than /sbin/rmt; tar is a pretty
  safe bet to have installed no matter what
- P2: no need to link with libnsl; from fedora (deaddog)
- P3: LSB compliance (sbenedict)
- do make check
- spec cleanups
- drop unrequired patches and renumber
- P11: security fix for CAN-1999-1572
- P12: security fix for CAN-2005-1111
- P13: security fix for CAN-2005-1229
- add -DHAVE_LSTAT=1 to the CPPFLAGS so that symbolic links are
  not replaced with files or directories but remain symlinks
  (re mdk bugzilla #12970)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-10avx
- bootstrap build

* Wed Feb 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5-9avx
- P13: patch to fix CAN-1999-1572

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5-8avx
- now that both tar and rmt can provide rmt, require the file
  rather than the package

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5-7avx
- Annvix build
- require packages not files

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 2.5-6sls
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 2.5-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
