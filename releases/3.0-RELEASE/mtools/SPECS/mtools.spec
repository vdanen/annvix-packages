#
# spec file for package mtools
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mtools
%define version		3.9.9
%define release		%_revrel

Summary:	Programs for accessing MS-DOS disks without mounting the disks
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		File Tools
URL: 		http://www.tux.org/pub/tux/knaff/mtools/index.html
Source: 	http://www.tux.org/pub/tux/knaff/mtools/%{name}-%{version}.tar.bz2 
Patch0: 	mtools-3.9.1-linux.patch
Patch1: 	mtools-3.9.7-20000619.diff
Patch2: 	mtools-3.9.6-atari.patch
Patch4: 	mtools-3.9.8-fs.patch
Patch5: 	mtools-3.9.9-supermount.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires: 	texinfo

Requires(post):	info-install
Requires(preun): info-install

%description
Mtools is a collection of utilities for accessing MS-DOS files.
Mtools allow you to read, write and move around MS-DOS filesystem
files (normally on MS-DOS floppy disks).  Mtools supports Windows95
style long file names, OS/2 Xdf disks, and 2m disks.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .linux
%patch1 -p1 -b .update
%patch2 -p1 -b .atari
%patch4 -p1 -b .compil
%patch5 -p1 -b .supermount


%build
%configure --without-x
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix} %{buildroot}%{_sysconfdir}
%makeinstall
/usr/bin/install -c -m 644 mtools.conf %{buildroot}%{_sysconfdir}
# specific handling for mformat which is setuid root
rm -f %{buildroot}%{_bindir}/mformat
cp -a %{buildroot}%{_bindir}/mtools %{buildroot}%{_bindir}/mformat


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/mtools.conf
%{_bindir}/l*
%{_bindir}/ma*
%{_bindir}/mb*
%{_bindir}/mc*
%{_bindir}/md*
%attr(04755,root,root) %{_bindir}/mformat
%{_bindir}/mi*
%{_bindir}/mk*
%{_bindir}/ml*
%{_bindir}/mm*
%{_bindir}/mp*
%{_bindir}/mr*
%{_bindir}/ms*
%{_bindir}/mt*
%{_bindir}/mx*
%{_bindir}/mz*
%{_bindir}/t*
%{_bindir}/u*
%{_mandir}/*/*
%{_infodir}/%{name}.*

%files doc
%defattr(-,root,root)
%doc COPYING Changelog README Release.notes mtools.texi


%changelog
* Wed Nov 28 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9
- rebuild

* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9-9avx
- correct the buildroot

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9-8avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9-7avx
- rebuild

* Sat Jan 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9-6avx
- build without X support

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.9.9-5avx
- Require packages not files
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 3.9.9-4sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 3.9.9-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
