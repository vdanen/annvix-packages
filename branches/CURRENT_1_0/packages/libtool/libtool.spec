%define name	libtool
%define version	1.4.3
%define release	12avx

%define lib_major	3
%define lib_name_orig	libltdl
%define lib_name	%mklibname ltdl %{lib_major}

Summary:	The GNU libtool, which simplifies the use of shared libraries
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/libtool/libtool.html
Source:		ftp://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.bz2
Source1:	libtool-cputoolize.sh
# Geoff - patching ltmain.sh not ltmain.in coz that's the file that gets 
# copied over to the buildroot.
Patch0:		libtool-1.3.5-mktemp.patch.bz2
Patch1:		libtool-1.4-nonneg.patch.bz2
Patch2: 	libtool-1.4.3-relink.patch.bz2
Patch3:		libtool-1.4.3-lib64.patch.bz2
Patch4:		libtool-1.4.3-x86_64.patch.bz2
Patch5: 	libtool-1.4.2-add-x11r6-lib-in-ignores-for-rpath.patch.bz2
Patch6:		libtool-1.4.2-fix-linkage-of-cxx-code-with-gcc.patch.bz2
Patch7:		libtool-1.4.2-archive-shared.patch.bz2
Patch8:		libtool-1.4.3-ltmain-SED.patch.bz2
# http://mail.gnu.org/archive/html/libtool-patches/2002-12/msg00003.html
Patch9:		libtool-1.4.3-pass-thread-flags.patch.bz2
# http://www.daa.com.au/~james/files/libtool-1.4.2-expsym-linux.patch
Patch10:	libtool-1.4.2-expsym-linux.patch.bz2
Patch11:	libtool-1.4.3-amd64-alias.patch.bz2
Patch12:	libtool-1.4.3-libtoolize--config-only.patch.bz2
Patch13:	libtool-1.4.3-quotes.patch.bz2

BuildRoot:	%_tmppath/%name-%version-%release-root

PreReq:		info-install
Requires:	file common-licenses

%description
The libtool package contains the GNU libtool, a set of shell scripts
which automatically configure UNIX and UNIX-like architectures to
generically build shared libraries.  Libtool provides a consistent,
portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, you
should install libtool.

%package -n %{lib_name}
Group:		Development/C
Summary:	Shared library files for libtool

%description -n %{lib_name}
Shared library files for libtool DLL library from the libtool package.

%package -n %{lib_name}-devel
Group:		Development/C
Summary:	Development files for libtool
Requires:	%{name} = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{lib_name_orig}-devel
PRovides:	libtool-devel
Obsoletes:	libtool-devel

%description -n %{lib_name}-devel
Development headers, and files for development from the libtool package.

%prep
%setup -q
%patch0 -p1 -b .mktemp
%patch1 -p1 -b .nonneg
%patch2 -p1 -b .relink
%patch3 -p1 -b .lib64
%patch4 -p1 -b .x86_64
%patch5 -p0 -b .rpath-ignore-x11r6libdir
%patch6 -p1 -b .g++-link
%patch7 -p1 -b .archive-shared
%patch8 -p1 -b .ltmain-SED
%patch9 -p1 -b .pass-thread-flags
#%patch10 -p1 -b .expsym-linux
%patch11 -p1 -b .amd64-alias
%patch12 -p1 -b .libtoolize--config-only
%patch13 -p1 -b .quotes

automake --gnu --add-missing
aclocal
autoconf
( cd libltdl ; autoheader ; automake --gnu --add-missing ; \
  aclocal ; autoconf )

%build
# don't use configure macro - it forces libtoolize, which is bad -jgarzik
# Use configure macro but define __libtoolize to be /bin/true -Geoff
%define __libtoolize /bin/true
%configure

%make -C doc
%make

echo ====================TESTING=========================
%ifarch ia64 x86_64
# - ia64: SIGILL when running hellodl
# - x86_64: fail in nopic test because we actually try to build a
#   shared object from objects built without PIC (1 of 82 tests failed)
make check || echo make check failed
%else
# all tests must pass here
make check
%endif
echo ====================TESTING END=====================

( cd demo ; make clean )

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
sed -e "s,@prefix@,%{_prefix}," -e "s,@datadir@,%{_datadir}," %{SOURCE1} \
  > $RPM_BUILD_ROOT%{_bindir}/cputoolize
chmod 755 $RPM_BUILD_ROOT%{_bindir}/cputoolize

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_install_info %{name}.info

%post -n %{lib_name} -p /sbin/ldconfig

%preun
%_remove_install_info %{name}.info

%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS INSTALL NEWS README
%doc THANKS TODO ChangeLog*
%_bindir/*
%_infodir/libtool.info*
%dir %_datadir/libtool
%_datadir/libtool/co*
%_datadir/libtool/lt*
%_datadir/aclocal/libtool.m4

%files -n %{lib_name}
%defattr(-,root,root)
%doc libltdl/README
%_libdir/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc demo
%_includedir/*
%_datadir/libtool/libltdl
%_datadir/aclocal/ltdl.m4
%_libdir/*.a
%_libdir/*.so
%_libdir/*.la


%changelog
* Wed Jun 23 2004 Vincent Danen <vdanen@annvix.org> 1.4.3-12avx
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
