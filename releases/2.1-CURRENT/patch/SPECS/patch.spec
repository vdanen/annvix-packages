#
# spec file for package patch
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		patch
%define version 	2.5.9
%define release 	%_revrel

Summary:	The GNU patch command, for modifying/upgrading files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Text Tools
URL:		http://www.gnu.org/directory/GNU/patch.html
Source:		ftp://alpha.gnu.org/gnu/patch/patch-%{version}.tar.bz2
Patch1:		patch-2.5.8-sigsegv.patch
Patch2:		patch-2.5.4-unreadable_to_readable.patch
Patch3:		patch-2.5.8-stderr.patch
Patch5:		patch-2.5.4-destdir.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1


%build
# (fg) Large file support can be disabled from ./configure - it is necessary at
# least on sparcs
%ifnarch sparc sparc64 alpha
%configure 
%else
%configure --disable-largefile
%endif

make "CFLAGS=%{optflags} -D_GNU_SOURCE -W -Wall" LDFLAGS=-s


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog


%changelog
* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9
- really remove the docs from the main package

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9-8avx
- correct the buildroot

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9-7avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9-6avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9-5avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.9-4avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.5.9-3sls
- minor spec cleanups
- remove %%prefix

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 2.5.9-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
