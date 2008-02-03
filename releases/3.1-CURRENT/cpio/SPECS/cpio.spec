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
%define version 	2.9
%define release 	%_revrel

Summary:	A GNU archiving program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving
URL:		http://www.gnu.org/software/cpio
Source0:	ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.bz2.sig
Patch0:		cpio-2.7-CVE-2007-4476.patch
Patch1:		cpio-2.7-mdv-svr4compat.patch

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
%patch0 -p1 -b .cve-2007-4476
%patch1 -p1 -b .svr4compat


%build
%configure2_5x \
    --bindir=/bin \
    --with-rmt=/sbin/rmt \
    CPPFLAGS=-DHAVE_LSTAT=1

%make


%check
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
* Sun Dec 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.9
- P0: security fix for CVE-2007-4476

* Sun Nov 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.9
- 2.9
- drop P0, P2, P3, P4, P5, P6, P7, P8: fixed upstream or no longer needed
- rediffed P1
- use %%check
- fix url and source urls
- add gpg sig

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
