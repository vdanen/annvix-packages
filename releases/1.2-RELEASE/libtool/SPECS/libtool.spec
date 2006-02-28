#
# spec file for package libtool
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libtool
%define version		1.5.18
%define release		%_revrel

%define lib_major	3
%define libname_orig	libltdl
%define libname		%mklibname ltdl %{lib_major}

%define gcc_ver		%(gcc -dumpversion)

# do "make check" by default
%define do_check 	1
%{?_without_check: %global do_check 0}

# define biarch platforms
%define biarches 	x86_64 ppc64 sparc64
%ifarch x86_64
%define alt_arch 	i586
%endif
%ifarch ppc64
%define alt_arch 	ppc
%endif
%ifarch sparc64
%define alt_arch 	sparc
%endif

Summary:	The GNU libtool, which simplifies the use of shared libraries
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/libtool/libtool.html
Source:		ftp://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.gz
Source1:	ftp://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.gz.sig
Source2:	libtool-cputoolize.sh
# (Abel) Patches please only modify ltmain.in and don't touch ltmain.sh
# otherwise ltmain.sh will not be regenerated, and patches will be lost
Patch0:		libtool-1.5.6-relink.patch
Patch1:		libtool-1.5.18-lib64.patch
Patch2:		libtool-1.5.6-ltmain-SED.patch
Patch3:		libtool-1.5.6-libtoolize--config-only.patch
Patch4:		libtool-1.5.6-test-dependency.patch
Patch5:		libtool-1.5-testfailure.patch
Patch6:		libtool-1.5.6-old-libtool.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	automake1.8, autoconf2.5
%ifarch %biarches
BuildRequires:	setarch
%endif

Requires:	file, gcc = %{gcc_ver}
Requires(post):	info-install
Requires(preun): info-install


%description
The libtool package contains the GNU libtool, a set of shell scripts
which automatically configure UNIX and UNIX-like architectures to
generically build shared libraries.  Libtool provides a consistent,
portable interface which simplifies the process of using shared
libraries.


%package -n %{libname}
Group:		Development/C
Summary:	Shared library files for libtool
Provides:	%{libname_orig} = %{version}-%{release}

%description -n %{libname}
Shared library files for libtool DLL library from the libtool package.


%package -n %{libname}-devel
Group:		Development/C
Summary:	Development files for libtool
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel

%description -n %{libname}-devel
Development headers, and files for development from the libtool package.


%prep
%setup -q
%patch0 -p1 -b .relink
%patch1 -p1 -b .lib64
%patch2 -p1 -b .ltmain-SED
%patch3 -p1 -b .libtoolize--config-only
%patch4 -p1 -b .test-dependency
%patch5 -p1
%patch6 -p1 -b .old-libtool

ACLOCAL=aclocal-1.8 AUTOMAKE=automake-1.8 ./bootstrap


%build
# don't use configure macro - it forces libtoolize, which is bad -jgarzik
# Use configure macro but define __libtoolize to be /bin/true -Geoff
%define __libtoolize /bin/true
# And don't overwrite config.{sub,guess} in this package as well -- Abel
%define __cputoolize /bin/true

# build alt-arch libtool first
# NOTE: don't bother to make libtool biarch capable within the same
# "binary", use the multiarch facility to dispatch to the right script.
%ifarch %{biarches}
mkdir -p build-%{alt_arch}-%{_target_os}
pushd    build-%{alt_arch}-%{_target_os}
    ../configure --prefix=%{_prefix} --build=%{alt_arch}-%{_real_vendor}-%{_target_os}%{?_gnu}
    make
popd
%endif

mkdir -p build-%{_target_cpu}-%{_target_os}
    pushd build-%{_target_cpu}-%{_target_os}
    CONFIGURE_TOP=.. %configure2_5x
    %make

    %if %{do_check}
    set +x
    echo ====================TESTING=========================
    set -x
    #%ifarch ia64
    # - ia64: SIGILL when running hellodl
    #make check || echo make check failed
    #%else
    # all tests must pass here
    make check
    #%endif
    set +x
    echo ====================TESTING END=====================
    set -x

    make -C demo clean
    %endif
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std -C build-%{_target_cpu}-%{_target_os}

sed -e "s,@prefix@,%{_prefix}," -e "s,@datadir@,%{_datadir}," %{SOURCE2} \
    > %{buildroot}%{_bindir}/cputoolize
chmod 0755 %{buildroot}%{_bindir}/cputoolize

# biarch support
%ifarch %biarches
%multiarch_binaries %{buildroot}%{_bindir}/libtool
install -m 0755 build-%{alt_arch}-%{_target_os}/libtool %{buildroot}%{_bindir}/libtool
linux32 /bin/sh -c '%multiarch_binaries %{buildroot}%{_bindir}/libtool'
%endif


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info


%preun
%_remove_install_info %{name}.info


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc AUTHORS INSTALL NEWS README THANKS TODO ChangeLog*
%{_bindir}/*
%{_infodir}/libtool.info*
%{_datadir}/libtool
%{_datadir}/aclocal/*.m4

%files -n %{libname}
%defattr(-,root,root)
%doc libltdl/README
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc demo
%_includedir/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
- setarch is required for biarchs (for linux32)

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.18-1avx
- 1.5.18
- re-add the strict gcc requirement
- drop P7
- rediff P1
- fix requires

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-6avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-5avx
- rebuild
- drop BuildReq on setarch if we're a biarch
- run the configure/make scripts without linux32 or else configure
  and make think gcc doesn't work; at any rate, libtool is a shell script
  and things are done properly with or without using linux32

* Thu Jul 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-4avx
- rebuild against gcc 3.4.4
- BuildRequires: setarch

* Thu Jul 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-3avx
- multiarch
- don't use the crappy hack to get the gcc version and just make it
  require gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-2avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.12-1avx
- 1.5.12
- sync all patches with Mandrake 1.5.12-4mdk
- prepare for multiarch (from gb)
- /usr/bin/libtool is compiler dependent

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3-12avx
- require packages not files
- Annvix build

* Sat Jun 11 2004 Vincent Danen <vdanen@opensls.org> 1.4.3-11sls
- own /usr/share/libtool

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.4.3-10sls
- minor spec cleanups

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 1.4.3-9sls
- sync with 8mdk (gbeauchesne): fix mklibnamification

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 1.4.3-8sls
- OpenSLS build
- tidy spec

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.3-7mdk
- Patch13: quote tests correctly

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.3-6mdk
- Update cputoolize to also update ./config.{guess,sub} even though
  ./configure.{ac,in} was not found

* Sat Jul 26 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.3-5mdk
- Introduce cputoolize wrapper script
- Patch12: Add libtoolize --config-only to only update config.{sub,guess}

* Thu Jul 24 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.3-4mdk
- Patch11: Alias amd64-* to x86_64-* for config.sub

* Tue Jul  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.3-3mdk
- Patch2: Fix relink fix
- Patch9: Don't nuke -pthread et al. passed to the linker (Sebastian Wilhelmi)

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.4.3-2mdk
- rebuild to have automatic Provides

* Thu Feb 13 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.3-1mdk
- 1.4.3
- Patch8: Do define SED variable appropriately

* Mon Jul 29 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.2-9mdk
- Put back Patch6 (fix-linkage-of-cxx-code-with-gcc). Note that if you
  link a C++ shared library, you can consider using gcc and only
  -lsupc++ if you expect your library to still link from a C program.

* Fri Jul 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.2-8mdk
- Revert Patch6 as we don't want to forcibly link with g++ a C++
  library that can be linked to a C program. The latter generally
  doesn't want to grab the world.

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.2-7mdk
- Patch8: Allow link against an archive when building a shared library (SuSE)

* Tue Jul 23 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.2-6mdk
- Update Patch7 (lib64) in order to add /usr/X11R6/lib64 to ingores
  for rpath as well. Aka. extend gc's dirty hack to lib64 architectures.

* Thu Jul 11 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.2-5mdk
- Update Patch2 (test-quote) to latest RH one
- Let make check gently fail on IA-64
- Rpmlint fixes: strange-permission

* Wed May 15 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4.2-4mdk
- libtool-1.4.2-fix-linkage-of-cxx-code-with-gcc.patch.bz2
- fix one-line-command-in-percentpost

* Mon Jan  7 2002 Abel Cheung <maddog@linux.org.hk> 1.4.2-3mdk
- Patch5: Take the patch that removes duplicate library dependencies
  from libtool CVS. Use --preserve-dup-deps for preserving duplicate
  dependent libraries.

* Sat Oct 20 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.4.2-2mdk
- tired of dirty patches to fix /usr/X11R6/lib rpath's in binaries and
  shlib, so add-x11r6-lib-in-ignores-for-rpath.patch
    note that this won't be enough for the configure scripts of the 2.13
  generation since they're based on duplicating the "ltconfig" binary
  which duplicates the sys_lib_search_path_spec variable I'm patching ;
  for these packages, you'll need to search and change this variable in
  the "ltconfig" from your package, if you end up with a binary or shlib
  with /usr/X11R6/lib in the RPATH

* Thu Oct 04 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4.2-1mdk
- Update relink patch. (maddog).
- Fix nonneg and mktemp patch as we should be patching ltmain.sh not the
  .in file (maddog).
- Update to 1.4.2.
- Quietly take away the CVS patch.

* Fri Sep 28 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.4-7mdk
- Add relink patch from maddog@linuxhall.org.

* Sat Jul 07 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4-6mdk
- CVS fixes (rawhide).
- Remove compat patch.
- Use %%configure but define __libtoolize to /bin/true.

* Mon Jun 11 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4-5mdk
- Add a patch so that we don't get unary operater expected message from
  libtool (Abel).
  
* Sat May 26 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4-4mdk
- Proudly and shamelessly rip the 1.4-nonneg patch from RH.

* Fri May 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4-3mdk
- Define LT_NON_POSIX_NAMESPACE in ltdl.h to be compatible a.k.a. make 
  programs which depend on libltdl link well.
  
* Wed May 23 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4-2mdk
- Move *.la to the development package to avoid a conflict (Kudos to
  Arnd Bergmann).
  
* Sun May 23 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4-1mdk
- Bump version 1.4 out for everyone.

A
* Fri Mar 30 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.5-13mdk
- Remove dependency of lib package on main package

* Tue Mar 20 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.5-12mdk
- Do not use configure macro, it calls libtoolize.  (bug #2092)
- Fix rpmlint warnings.
- Require common-licenses.

* Fri Mar  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.5-11mdk
- Patch to use mktemp to create the tempdir (rh).
- Fix recognition of ^0[0-9]+$ as a non-negative integer (rh).
- Requires: file.

* Mon Feb 05 2001 Francis Galiegue <fg@mandrakesoft.com> 1.3.5-10mdk

- Don't make check on ia64...

* Sat Jan 07 2001 David BAUDENS <baudens@mandrakesoft.com> 1.3.5-9mdk
- Fix my typo in Requires. Sorry

* Fri Jan 05 2001 David BAUDENS <baudens@mandrakesoft.com> 1.3.5-8mdk
- Fix Requires

* Thu Dec 14 2000 David BAUDENS <baudens@mandrakesoft.com> 1.3.5-7mdk
- Obsoletes: libtool-devel

* Wed Dec 13 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.5-6mdk
- Don't obsolete libtool-devel, provide it
- Fix bugs caught by rpmlint

* Wed Dec 13 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.5-5mdk
- new library policy
- eliminate libtool-devel package

* Thu Dec  7 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.5-4mdk
- Run automated tests at build time
- Use make macro
- Fix rpmlint errors
- Move /usr/share libltdl stuff to libtool-devel package

* Fri Nov 10 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.5-3mdk
- Add fake option --build=.

* Fri Jul 28 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.5-2mdk
- BM
- remove reverted patch :-( (grrrr)
  from the spec : "i suck --Geoff" :-)
- make rpmlint go to paradise

* Wed Jun 21 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 1.3.5-1mdk
- picks up $arch-mandrake-linux-gnu not $arch-pc-linux-gnu (patch)
  well, for x86 and alpha anyway, maybe ultrasparc too ??
- new version
- fix bad source url
- add libtool url
- add devel package
- Chmouel Boudjnah <chmouel@mandrakesoft.com> - Spec Cleanup
  (makeinstall etc..).

* Wed Apr  5 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.4-2mdk
- updated BuildRoot
- group new Development/Other

* Thu Jan 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.4-1mdk
- 1.3.4.

* Wed Dec  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build Release.

* Sun Nov 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Mon Oct 25 1999  Jeff Garzik  <jgarzik@pobox.com>
- Import RedHat 6.1 spec
- s/gzip/bzip2/ for info documentation

* Thu Jul 15 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.3.

* Mon Jun 14 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.2.

* Tue May 11 1999 Jeff Johnson <jbj@redhat.com>
- explicitly disable per-arch libraries (#2210)
- undo hard links and remove zero length file (#2689)

* Sat May  1 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- disable the --cache-file passing to ltconfig; this breaks the older
  ltconfig scripts found around.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.2f

* Tue Mar 16 1999 Cristian Gafton <gafton@redhat.com>
- completed arm patch
- added patch to make it more arm-friendly
- upgrade to version 1.2d

* Thu May 07 1998 Donnie Barnes <djb@redhat.com>
- fixed busted group

* Sat Jan 24 1998 Marc Ewing <marc@redhat.com>
- Update to 1.0h
- added install-info support

* Tue Nov 25 1997 Elliot Lee <sopwith@redhat.com>
- Update to 1.0f
- BuildRoot it
- Make it a noarch package
