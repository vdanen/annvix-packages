#
# spec file for package gdbm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gdbm
%define version 	1.8.3
%define release 	%_revrel

%define major		3
%define libname	%mklibname gdbm %{major}

Summary:	A GNU set of database routines which use extensible hashing
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.gnu.org/software/gdbm/
Source:		ftp://ftp.gnu.org/pub/gnu/gdbm/%{name}-%{version}.tar.bz2
Patch0:		gdbm-1.8.0-jbj.patch
# (deush) regenerate patch to apply with -p1
Patch1:		gdbm-1.8.3-asnonroot.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7

%description
Gdbm is a GNU database indexing library, including routines
which use extensible hashing.  Gdbm works in a similar way to standard UNIX
dbm routines.  Gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.


%package -n %{libname}
Summary:	Main library for gdbm
Group:		System/Libraries
Obsoletes:	%{name}, libgdbm1
Provides:	libgdbm1
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package provides library needed to run programs dynamically linked
with gdbm.


%package -n %{libname}-devel
Summary:	Development libraries and header files for the gdbm library
Group:		Development/Databases
Requires:	%{libname} = %{version}
Requires(post):	info-install
Requires(preun): info-install
Obsoletes:	%{name}-devel, libgdbm1-devel
Provides:	%{name}-devel, libgdbm1-devel
Provides:	lib%{name}-devel
Conflicts:	%{mklibname gdbm 2}-devel

%description -n %{libname}-devel
Gdbm-devel contains the development libraries and header files
for gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .jbj
%patch1 -p1

libtoolize -f
aclocal-1.7
FORCE_AUTOCONF_2_5=1 autoconf
autoheader


%build
%configure
%make all info


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall install-compat includedir=%{buildroot}%{_includedir}/gdbm man3dir=%{buildroot}%{_mandir}/man3
ln -sf gdbm/gdbm.h %{buildroot}%{_includedir}/gdbm.h

chmod 0644 COPYING INSTALL NEWS README


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post -n %{libname}-devel
%_install_info gdbm.info

%preun -n %{libname}-devel
%_remove_install_info gdbm.info


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libgdbm*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libgdbm*.so
%{_libdir}/libgdbm*.la
%{_libdir}/libgdbm*.a
%dir %{_includedir}/gdbm
%{_includedir}/gdbm/*.h
%{_includedir}/gdbm.h
%{_infodir}/gdbm*
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc NEWS README


%changelog
* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3
- add -doc subpackage
- rebuild with gcc4
- fix prereq

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3
- Obfuscate email addresses and new tagging
- Uncompress patches
- remove useless provides on %%{libname}-devel

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3-2avx
- bootstrap build

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3-1avx
- 1.8.3
- sync with cooker 1.8.3-2mdk:
  - force the use of autoconf2.5 and automake1.7 (peroyvind)
  - change major name (daouda)
  - added compat libs (daouda)
  - conflicts libgdbm2-devel (gb)
  - drop P2 and P3


* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.8.0-27avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.8.0-26sls
- minor spec cleanups

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 1.8.0-25sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.8.0 -24mdk
- fix mklibname

* Mon Jul 28 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.8.0 -23mdk
- mkbliname

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.8.0 -22mdk
- Rebuild

* Wed Jun 04 2003 Stefan van der Eijk <stefan@eijk.nu> 1.8.0-21mdk
- rebuild for deps

* Fri Apr 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.8.0-20mdk
- Patch3: Teach it to use standard configure macros, make it lib64 aware too

* Thu Mar 06 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 1.8.0-19mdk
- Fix .la file (need to add prefix to build stage)

* Wed Sep 19 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.8.0-18mdk
- fix access rights of the doc files
- provides libgdm1 and libdbm1-devel to allow upgrade.

* Wed Aug  1 2001 Daouda LO <daouda@mandrakesoft.com> 1.8.0 -17mdk
- fix the major lib number (thanx to thomas)

* Mon Jul  9 2001  Daouda Lo <daouda@mandrakesoft.com> 1.8.0 -16mdk
- rebuild
- s|Copyright|License|

* Sat Jun 23 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.8.0-15mdk
- run libtoolize/aclocal/autoconf/autoheader to fix build
- use RPM_OPT_FLAGS

* Fri Dec  8 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.8.0-14mdk
- libgdbm1-devel provides gdbm-devel for backward compatibility.

* Wed Dec  6 2000  Daouda Lo<daouda@mandrakesoft.com> 1.8.0-13mdk
- fix again (i have no brain)

* Wed Dec  6 2000  Daouda Lo <daouda@mandrakesoft.com> 1.8.0-12mdk
- fix typos (install-info ) 

* Wed Dec  6 2000  Daouda<daouda@mandrakesoft.com> 1.8.0-11mdk
- fix Provides typo

* Tue Nov 28 2000 Daouda Lo <daouda@mandrakesoft.com> 1.8.0-10mdk
- obsoleted gdbm-devel 

* Tue Nov 28 2000 Daouda Lo <daouda@mandrakesoft.com> 1.8.0-9mdk
- add a BuildRequires tag (texinfo) 
- Use Opt (-O3)
- New lib naming schema
- macroz
- add doc section

* Mon Sep  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.8.0-8mdk
- Fix info files installation.

* Sun Aug 06 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 1.8.0-7mdk
- some more macroszifications
- BM

* Wed May 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.8.0-6mdk
- Use tmpppath macros.

* Fri May 19 2000 Pixel <pixel@mandrakesoft.com> 1.8.0-5mdk
- add soname

* Mon Apr  3 2000 Adam Lebsack <adam@mandrakesoft.com> 1.8.0-4mdk
- Release build.

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix building as non root.
- Merge with redhat patchs.
- make sure created database header is initialized (r).
- repackage to include /usr/include/gdbm/*dbm.h compatibility includes(r)
- make sure created database header is initialized (r).

* Wed Jun 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 1.8.0

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- gdbm-devel moved to Development/Libraries

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- buildroot and built for Manhattan

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Thu Jun 12 1997 Erik Troan <ewt@redhat.com>
- built against glibc
