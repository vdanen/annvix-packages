%define name	rcs
%define version	5.7
%define release	9avx

Summary:	Revision Control System (RCS) file version management tools.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source:		ftp://ftp.gnu.org/pub/gnu/rcs-5.7.tar.bz2
Patch:		rcs-5.7-stupidrcs.patch.bz2
Patch1:		rcs-5.7-security.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root

%description
The Revision Control System (RCS) is a system for managing multiple
versions of files.  RCS automates the storage, retrieval, logging,
identification and merging of file revisions.  RCS is useful for text
files that are revised frequently (for example, programs,
documentation, graphics, papers and form letters).

The rcs package should be installed if you need a system for managing
different versions of files.

%prep
%setup -q
%patch -p1 -b .stupidrcs
%patch1 -p1 -b .security

%build
#CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s ./configure --prefix=%{prefix} --with-diffutils
autoconf
%configure --with-diffutils

touch src/conf.h
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall
mkdir -p $RPM_BUILD_ROOT%{_mandir}
mv $RPM_BUILD_ROOT/usr/man/* $RPM_BUILD_ROOT%{_mandir}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc NEWS REFS
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 5.7-9avx
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
