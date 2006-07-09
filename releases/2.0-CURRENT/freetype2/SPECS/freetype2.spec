#
# spec file for package freetype2
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		freetype2
%define	version		2.1.10
%define release		%_revrel

%define major		6
%define libname		%mklibname freetype %{major}

Summary:	A free and portable TrueType font rendering engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	FreeType License/GPL
Group:		System/Libraries
URL:		http://www.freetype.org/
Source0:	ftp://ftp.freetype.org/pub/freetype/freetype2/freetype-%{version}.tar.bz2
# (fc) 2.1.10-2mdk CVS bug fixes, mostly for embolding
Patch0:		freetype-2.1.10-cvsfixes.patch
# (fc) 2.1.10-3mdk put back internal API, used by xorg (Mdk bug #14636) (David Turner)
Patch1:		freetype-2.1.10-xorgfix.patch
# (fc) 2.1.10-5mdk fix autofit render setup (CVS)
Patch2:		freetype-2.1.10-fixautofit.patch
# (fc) 2.1.10-5mdk fix memleak (CVS)
Patch3:		freetype-2.1.10-memleak.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}-%{release}-root
BuildRequires:	zlib-devel, multiarch-utils

%description
The FreeType2 engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of
platforms and environments. Note that FreeType2 is a library, not a
stand-alone application, though some utility applications are included


%package -n %{libname}
Summary:	Shared libraries for a free and portable TrueType font rendering engine
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
The FreeType2 engine is a free and portable TrueType font rendering
engine.  It has been developed to provide TT support to a great
variety of platforms and environments. Note that FreeType2 is a
library, not a stand-alone application, though some utility
applications are included


%package -n %{libname}-devel
Summary:	Header files and static library for development with FreeType2
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	zlib-devel
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libfreetype-devel = %{version}-%{release}

%description -n %{libname}-devel
This package is only needed if you intend to develop or compile applications
which rely on the FreeType2 library. If you simply want to run existing
applications, you won't need this package.


%package -n %{libname}-static-devel
Summary:	Static libraries for programs which will use the FreeType2 library
Group:		Development/C
Requires:	%{libname}-devel = %{version}
Obsoletes:	%{name}-static-devel
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n %{libname}-static-devel
This package includes the static libraries necessary for 
developing programs which will use the FreeType2 library.


%prep
%setup -q -n freetype-%{version}
%patch0 -p1 -b .cvsfixes
%patch1 -p1 -b .xorgfix
%patch2 -p1 -b .fixautofit
%patch3 -p1 -b .memleak


%build
%{?__cputoolize: %{__cputoolize} -c builds/unix}
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

%multiarch_binaries %{buildroot}%{_bindir}/freetype-config
%multiarch_includes %{buildroot}%{_includedir}/freetype2/freetype/config/ftconfig.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%{_bindir}/freetype-config
%{_libdir}/*.so
%{_libdir}/*.la
%dir %{_includedir}/freetype2
%{_includedir}/freetype2/*
%{_includedir}/ft2build.h
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%multiarch %{multiarch_bindir}/freetype-config
%multiarch %dir %{multiarch_includedir}/freetype2
%multiarch %{multiarch_includedir}/freetype2/*


%files -n %{libname}-static-devel
%defattr(-, root, root)
%{_libdir}/*.a


%changelog
* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10
- Obfuscate email addresses and new tagging
- Uncompress patches
- rpmlint fix: %%{libname}-devel also provides libfreetype-devel

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10-2avx
- drop P4; not needed

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.10-1avx
- 2.1.10
- sync patches with mandriva 2.1.10-6mdk (not that we really care about
  having a 100% freetype, but it's no real skin off our back)
- drop the docs
- multiarch support

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.4-11avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.4-10avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen@opensls.org> 2.1.4-9avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.1.4-8sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.1.4-7sls
- OpenSLS build
- tidy spec
- remove PLF stuff

* Wed Aug 28 2003 Laurent Culioli <laurent@pschit.net> 2.1.4-6mdk
- fix conditional build

* Fri Aug  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.4-5mdk
- Libification, cputoolize

* Wed Jul  9 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.1.4-4mdk
- Rebuild for latest rpm provides

* Mon May 12 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.1.4-3mdk
- Rebuild to get new devel dep/requires

* Sat Apr 26 2003 Stefan van der Eijk <stefan@eijk.nu> 2.1.4-2mdk
- rebuild

* Wed Apr 16 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.1.4-1mdk
- Release 2.1.4
- Remove patches 0, 1, 2, 3, 4, 5 (merged upstream)

* Tue Mar 11 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.3-12mdk
- Patch5: Fix possible double free condition exhausted by OOo and some
  other 3rd-party fonts having embedded bitmaps

* Wed Mar  5 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.1.3-11mdk
- Patch4 (CVS): fix zlib endless loop (touch 0123456789 ; gzip 0123456789 ; ftdump 0123456789.gz to test :)

* Thu Feb 27 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.1.3-10mdk
- Moved freetype2-tools to a standalone package, to avoid
  cyclical dependencies with XFree86.

* Thu Feb 27 2003 Stefan van der Eijk <stefan@eijk.nu> 2.1.3-9mdk
- BuildRequires: XFree86-devel

* Mon Feb 24 2003 Pixel <pixel@mandrakesoft.com> 2.1.3-8mdk
- fix memory leak with .pcf.gz files

* Fri Feb 21 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.1.3-7mdk
- Added tools

* Sun Feb  2 2003 Stefan van der Eijk <stefan@eijk.nu> 2.1.3-6mdk
- move Requires: zlib-devel from -static-devel package to -devel

* Wed Jan 22 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.3-5mdk
- Update patch0 to fix gzip file detection (from CVS)

* Mon Jan 13 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.3-4mdk
- Update patch0 to really link with zlib

* Mon Jan 13 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.3-3mdk
- Patch0 (CVS): use external zlib
- Patch1 (CVS): implement light hint
- Patch2 (CVS): fix bug with corrupted fonts and recursive composite glyphs

* Wed Nov 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.3-2mdk
- Remove patch0 (replaced with perl search&remplace) (Guillaume Rousse)

* Tue Nov 19 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.3-1mdk
- Release 2.1.3
- Remove patches 1, 2, 3, 4, 5, 6, 7 (merged upstream), 8 (no longer needed)

* Wed Nov 13 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.2-3mdk
- Add static subpackage (Mats D. Wichmann)

* Mon Nov  4 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.2-2mdk
- Patch8 (rawhide) : Add an experimental FT_Set_Hint_Flags() call

* Tue Oct 29 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.2-1mdk
- Release 2.1.2
- configure macro is back
- Patch1 (Rawhide): fix bug in PS hinter
- Patch2 (Rawhide): Support Type1 BlueFuzz value
- Patch3 (Rawhide): Another PS hinter bug fix (rawhide)
- Patch4 (CVS): fix outline transformation
- Patch5 (CVS): Backport autohinter improvements 
- Patch6 (Anthony Fok): prevent crash with broken TT fonts
- Patch7 (Rawhide): fix bug with PCF metrics
- Update patch0

* Thu May 16 2002 Yves Duret <yduret@mandrakesoft.com> 2.0.9-3mdk
- removed the 43 unusefull blank lines (??)
- plf-isazacion by Buchan Milne <bgmilne@cae.co.za>
  * enable the bytecode interpreter when built with --with plf

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.9-2mdk
- Automated rebuild in gcc3.1 environment

* Wed Mar 20 2002 David BAUDENS <baudens@mandrakesoft.com> 2.0.9-1mdk
- 2.0.9
- devel: Requires: %%{version}-%%{release} and not only %%{version}
- Use ./configure
- Don't build static libraries
- Move documentation in devel package
- Spec clean up

* Tue Jan 25 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.0.6-1mdk
- Release 2.0.6.
- Added URL.

* Sun Oct 28 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.5-1mdk
- Release 2.0.5.
- fixed executable permission on docs files.
- s/Copyright/License/.

* Thu Jun 28 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.4-1mdk
- Release 2.0.4

* Wed May 30 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.3-1mdk
- Release 2.0.3
- Remove patch0 (Type1 fonts are corrected)

* Wed Apr 25 2001 Geoffrey Lee <snailtalk@mandrakesot.com> 2.0.2-4mdk
- Spec patch from Abel Cheung to fix build on certain machines 
  (personally I have no idea why it happens).

* Mon Apr 09 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.2-3mdk
- patched t1load patch (Arnd Bergmann).

* Mon Apr 09 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.2-2mdk
- added Tom Kacvinsky patch to fix problem with ancient URW fonts,
  libXft segfaults, etc. (thanks to Arnd Bergmann).

* Sat Mar 31 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.0.2-1mdk
- 2.0.2 final.
- removedft2build patch.

* Mon Dec 11 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.2-0.20001211.1mdk
- Snapshot version from CVS (needed for xrender)
- Patch ft2build.h to use correct path (Fred Lepied)
- Remove patch1 (not longer needed)
- Remove patch2 (merged upstream)

* Sat Dec 02 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0.1-1mdk
- new and shiny source bumped into cooker.
- obsolete patch as the bug is fixed.
- use RPM_OPT_FLAGS.

* Tue Nov 21 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0-3mdk
- Include all modules in lib (no longer apply patch1)

* Tue Nov 21 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0-2mdk
- Add config script to devel package
- correctly configure package

* Fri Nov 10 2000 Geoffrey Lee <snailtalk@manrakesoft.com> 2.0-1mdk
- really 2.0 release.

* Wed Nov  8 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0-0.8.1mdk
- First mandrake release

* Thu Oct  5 2000 Ramiro Estrugo <ramiro@eazel.com>
- Created this thing
