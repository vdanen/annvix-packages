#
# spec file for package rcs
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rcs
%define version		5.7
%define release		%_revrel

Summary:	Revision Control System (RCS) file version management tools
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.cs.purdue.edu/homes/trinkle/RCS/
Source:		ftp://ftp.gnu.org/pub/gnu/%{name}-%{version}.tar.bz2
Patch0:		rcs-5.7-stupidrcs.patch
Patch1:		rcs-5.7-security.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.1

%description
The Revision Control System (RCS) is a system for managing multiple
versions of files.  RCS automates the storage, retrieval, logging,
identification and merging of file revisions.  RCS is useful for text
files that are revised frequently (for example, programs,
documentation, graphics, papers and form letters).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch -p1 -b .stupidrcs
%patch1 -p1 -b .security


%build
autoconf
%configure --with-diffutils

touch src/conf.h
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall man1dir=%{buildroot}%{_mandir}/man1 man5dir=%{buildroot}%{_mandir}/man5


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%files doc
%defattr(-,root,root)
%doc NEWS REFS


%changelog
* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.7
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.7
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.7-12avx
- BuildRequires: autoconf2.1
- added URL

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.7-11avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.7-10avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.7-9avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 5.7-8sls
- minor spec cleanups
- remove %%prefix

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 5.7-7sls
- OpenSLS build
- tidy spec

* Fri May  2 2003 Frederic Lepied <flepied@mandrakesoft.com> 5.7-6mdk
- rebuilt

* Wed Mar  7 2001 Vincent Danen <vdanen@mandrakesoft.com> 5.7-5mdk
- include security patch from Caldera for possible temp races

* Wed Aug 30 2000 Frederic Lepied <flepied@mandrakesoft.com> 5.7-4mdk
- BM

* Fri Apr 07 2000 Christopher Molnar <molnarc@mandrakesoft.com> 5.7-3mdk
- New groups

* Thu Nov  4 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed the spec file; added BuildRoot

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
-built against glibc

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
