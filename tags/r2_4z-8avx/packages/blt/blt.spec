%define name	blt
%define version	2.4z
%define release	8avx

%define major		2
%define	libname		%mklibname %{name} %{major}
%define	libname_devel	%mklibname %{name} %{major} -d

Summary:	A Tk toolkit extension, including widgets, geometry managers, etc.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
URL:		http://www.sourceforge.net/projects/blt
Source0:	BLT%{version}.tar.bz2
Patch0:		blt2.4z-patch-2.patch.bz2
Patch1:		blt2.4z-configure.in-disable-rpath.patch.bz2
Patch2:		blt2.4z-libdir.patch.bz2
Patch3:		blt2.4z-mkdir_p.patch.bz2
Patch4:		blt2.4z-64bit-fixes.patch.bz2

BuildRoot:	%_tmppath/%name-%version-root
BuildRequires:  XFree86-devel tcl tk

Requires:	%libname

%description
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

%package scripts
Summary:	TCL Libraries for BLT
Group:		System/Libraries

%description scripts
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

This package provides TCL libraries needed to use BLT.

%package -n %libname
Summary:	Shared libraries needed to use BLT
Group:		System/Libraries
Requires:	blt-scripts = %{version}

%description -n %libname
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

This package provides libraries needed to use BLT.

%package -n %libname_devel
Summary:	Headers of BLT
Group:		Development/Other
Requires:	%libname = %version-%release
Provides:	lib%name-devel = %version-%release
Obsoletes:	blt-devel
Provides:	blt-devel

%description -n %libname_devel
BLT is an extension to the Tk toolkiy. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to any patching
of the Tcl or Tk source file to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

This package provides headers needed to build packages based on BLT.

%prep
%setup -q -n %name%version
%patch0 -p1
%patch1 -p1 -b .rpath
%patch2 -p1 -b .libdir
%patch3 -p1 -b .mkdir_p
%patch4 -p1 -b .64bit-fixes
autoconf

%build
%configure
%make 

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

ln -sf libBLT.so.2.4 $RPM_BUILD_ROOT%_libdir/libBLT.so
ln -sf libBLTlite.so.2.4 $RPM_BUILD_ROOT%_libdir/libBLTlite.so
ln -sf bltwish-2.4 $RPM_BUILD_ROOT%_bindir/bltwish
ln -sf bltsh-2.4 $RPM_BUILD_ROOT%_bindir/bltsh

# Dadou - 2.4u-2mdk - Don't put in %%_libdir things which should be in %%_docdir
rm -fr $RPM_BUILD_ROOT/%_prefix/lib/blt2.4/demos
rm -fr $RPM_BUILD_ROOT/%_prefix/lib/blt2.4/NEWS
rm -fr $RPM_BUILD_ROOT/%_prefix/lib/blt2.4/PROBLEMS
rm -fr $RPM_BUILD_ROOT/%_prefix/lib/blt2.4/README

# Dadou - 2.4u-2mdk - Remove +x permissions in %%_docdir to be sure that RPM
#                     will don't want some strange dependencies
perl -pi -e "s|local/||" $RPM_BUILD_DIR/%name%version/demos/scripts/page.tcl
perl -pi -e "s|local/||" $RPM_BUILD_DIR/%name%version/html/hiertable.html

# Dadou - 2.4u-2mdk - Prevent conflicts with other packages
for i in bitmap graph tabset tree watch; do
	mv $RPM_BUILD_ROOT/%_mandir/mann/$i{,-blt}.n
done

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc MANIFEST NEWS PROBLEMS README
%doc demos/
%doc examples/
%doc html/
%_bindir/*
%_mandir/mann/*
%_mandir/man3/*

%files scripts
%defattr(-,root,root,-)
%doc MANIFEST NEWS PROBLEMS README
%dir %{_prefix}/lib/blt2.4
%{_prefix}/lib/blt2.4/*

%files -n %libname
%defattr(-,root,root,-)
%_libdir/*.so

%files -n %libname_devel
%defattr(-,root,root,-)
%_includedir/*
%_libdir/*.a

%changelog
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 2.4z-8avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 2.4z-7sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 2.4z-6sls
- OpenSLS build
- tidy spec

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4z-5mdk
- Patch4: Some 64-bit fixes

* Mon Jul 14 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 2.4z-4mdk
- use %%mklibname macro

* Mon Apr 14 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4z-3mdk
- fix conflict with tcllib

* Mon Apr 14 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4z-2mdk
- rebuild for tcl/tk

* Mon Apr 07 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.4z-1mdk
- 2.4z.
- Fix provides. (libblt-devel)

* Fri Jun 28 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4u-6mdk
- Do ship with blt tcl libraries, in new package blt-scripts
- Patch2: Fix lookup of tcl/tk libdir
- Patch3: Use mkdir -p to create directories

* Fri May 11 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4u-5mdk
- Fix the linking of BLT.

* Sun Dec 17 2000 David BAUDENS <baudens@mandrakesoft.com> 2.4u-4mdk
- Libdification
- Disable rpath
- Remove documentation which was put in %%_libdir
- Prevent request on strange dependencies
- Prevent conflicts with other packages

* Sun Dec 17 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4u-3mdk
- remove file conflict by renaming the manual file

* Sun Dec 17 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4u-2mdk
- Add a changelog for Stefan <s.vandereijk@chello.nl> who was too hasty
  to have forgotten to add one :) - make it use /usr/bin/tclsh, not
  /usr/local/bin/tclsh

* Fri Dec 15 2000 David BAUDENS <baudens@mandrakesoft.com> 2.4u-1mdk
- 2.4u

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4i-13mdk
- automatically added BuildRequires

* Fri Aug 04 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4i-12mdk
- rebuild to remove duplicate manpage which is provided by tcllib (stefan)

* Tue Aug 01 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 2.4i-11mdk
- macroszifications
- BM

* Tue May 16 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.4i-10mdk
- fixed broken symlink

* Thu Apr 20 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.4i-9mdk
- fixed group

* Wed Dec  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build Release.

* Mon Jul 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- s|local/bin/tclsh|bin/tclsh|

* Sat Jul 17 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- 2.4i
- set some compatibility links

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Fri Apr 16 1999 Bill Nottingham <notting@redhat.com>
- obsolete blt-devel

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Mar 11 1999 Bill Nottingham <notting@redhat.com>
- remove watch.n, tabset.n (conflicts with itcl)

* Wed Mar 10 1999 Bill Nottingham <notting@redhat.com>
- update to 2.4g
- buildrooted

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- stripped binaries
