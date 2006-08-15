#
# spec file for package tar
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		tar
%define version		1.15.90
%define release		%_revrel

%define rmtrealname	rmt-tar
%define _bindir		/bin

Summary:	A GNU file archiving program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving
URL:		http://www.gnu.org/software/tar/tar.html
Source0:	ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.bz2
Source1:	ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.bz2.sig
Source2:	tar-help2man
Patch0:		tar-1.14-mdk-doubleslash.patch

Buildroot:	%{_buildroot}/%{name}-%{version}

Requires(post):	info-install
Requires(preun): info-install
Conflicts:	rmt < 0.4b37

%description
The GNU tar program saves many files together into one archive and
can restore individual files (or all of the files) from the archive.
Tar can also be used to add supplemental files to an archive and to
update or list files in the archive.

Tar includes multivolume support, automatic archive compression/
decompression, the ability to perform remote archives and the
ability to perform incremental and full backups.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .doubleslash

cp %{_sourcedir}/tar-help2man ./help2man
chmod +x ./help2man

gzip ChangeLog

%build
%configure2_5x \
    --enable-backup-scripts \
    --bindir=%{_bindir} \
    DEFAULT_RMT_COMMAND="/sbin/rmt"

%make

# thanks to diffutils Makefile rule
(echo '[NAME]' && sed 's@/\* *@@; s/-/\\-/; q' src/tar.c) | (./help2man -i - -S '%{name} %{version}' src/tar ) | sed 's/^\.B info .*/.B info %{name}/' > %{name}.1

make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
ln -sf tar %{buildroot}%{_bindir}/gtar
install -D -m 0644 tar.1 %{buildroot}%{_mandir}/man1/tar.1

# rmt is provided by rmt ...
mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_libexecdir}/rmt %{buildroot}/sbin/%{rmtrealname}

%kill_lang %{name}
%find_lang %{name}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/tar
%{_bindir}/gtar
%{_sbindir}/backup
%{_sbindir}/restore
/sbin/%rmtrealname
%{_libexecdir}/backup.sh
%{_libexecdir}/dump-remind
%{_infodir}/*.info*
%{_mandir}/man?/*

%files doc
%defattr(-,root,root)
%doc NEWS THANKS AUTHORS README ChangeLog.gz COPYING TODO


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15.90
- spec cleanups
- remove locales

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15.90
- 1.15.90
- drop P0, P1, P3, P4 - merged upstream
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15.1
- fix group

* Fri Mar 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15.1
- P4: security fix for CVE-2006-0300

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15.1
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15.1-3avx
- new-style prereq
- compress the ChangeLog

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15.1-2avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15.1-1avx
- 1.15.1
- remove alternatives install for rmt
- P4: fix compilation with gcc4 (rgarciasuarez)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.14-2avx
- bootstrap build

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.14-1avx
- 1.14
- patch policy
- sync with cooker (deaddog):
  - drop P0, use help2man to generate manpage
  - drop P105 (-y/-I), since -j/--bzip2 is stabilized and well known now
  - drop P8, P10: merged upstream
  - rediff and renumber remaining patches
  - install scripts as well
  - use alternatives for rmt

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.13.25-14avx
- PreReq: info-install rather than /sbin/install-info
- PreReq: rmt rather than /sbin/rmt
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.13.25-13sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 1.13.25-12sls
- OpenSLS build
- tidy spec
