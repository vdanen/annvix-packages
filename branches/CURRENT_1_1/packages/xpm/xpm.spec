#
# spec file for package xpm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		xpm
%define version		3.4k
%define release		32avx

%define prefix		/usr/X11R6
%define	major		4
%define	LIBVER		4.11
%define libname		%mklibname %{name} %{major}
%define libnamedev	%mklibname %{name} %{major} -d

Summary:	A pixmap library for the X Window System
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
URL:		http://freshmeat.net/redir/libxpm/18465/url_homepage/
Source0:	ftp://ftp.x.org/contrib/libraries/xpm-%{version}.tar.bz2
Source1:	ftp://ftp.x.org/contrib/libraries/xpm-doc-A4.PS.gz 
Source2:	ftp://ftp.x.org/contrib/libraries/xpm-tutorial.PS.gz 
Source3:	ftp://ftp.x.org/contrib/libraries/xpm-FAQ.html
Source4:	ftp://ftp.x.org/contrib/libraries/xpm-README.html
Source5:	ftp://ftp.x.org/contrib/libraries/xpm_examples.tar.bz2
Patch0:		xpm-3.4k-shlib.patch.bz2
Patch1:		xpm-3.4k-fixes.patch.bz2
Patch2:		xpm-3.4k-alpha.patch.bz2
Patch3:		xpm-3.4k-xfree43merge.patch.bz2
Patch4:		xpm-3.4k-64bit-fixes.patch.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	XFree86-devel, xorg-x11

%description
The xpm package contains the XPM pixmap library for the X Window
System.  The XPM library allows applications to display color,
pixmapped images, and is used by many popular X programs.


%package -n %{libname}
Summary:	A pixmap library for the X Window System
Group:		System/Libraries
Provides:	%{name}, xpm3.4k
Obsoletes:	%{name}, xpm3.4k

%description -n %{libname}
The xpm package contains the XPM pixmap library for the X Window
System.  The XPM library allows applications to display color,
pixmapped images, and is used by many popular X programs.


%package -n %{libnamedev}
Summary:	Tools for developing apps which will use the XPM pixmap library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel, lib%{name}-devel, xpm3.4k-devel
Obsoletes:	%{name}-devel, xpm3.4k-devel

%description -n %{libnamedev}
The xpm-devel package contains the development libraries and header
files  necessary for developing applications which will use the XPM
library.  The XPM library is used by many programs for displaying
pixmaps in the X Window System.


%prep
%setup -q
%patch0 -p1 -b .shlib
%patch1 -p1 -b .fixes
%patch2 -p1 -b .alpha
%patch3 -p1 -b .xf86-4.3-merge
%patch4 -p1 -b .64bit-fixes
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} .


%build
xmkmf
make Makefiles
mkdir -p exports/include/X11
cp lib/*.h exports/include/X11
# %%make doesn't work on more than 2 cpu
%make CDEBUGFLAGS="%{optflags}" CXXDEBUGFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
ln -sf libXpm.so.%{LIBVER} %{buildroot}%{prefix}/%{_lib}/libXpm.so


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%doc CHANGES COPYRIGHT FAQ.html FILES README.html
%{prefix}/%{_lib}/libXpm.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc xpm-FAQ.html xpm-README.html xpm_examples.tar.bz2
%{prefix}/bin/*
%{prefix}/include/X11/*
%{prefix}/%{_lib}/libXpm.a
%{prefix}/%{_lib}/libXpm.so


%changelog
* Wed Aug 10 2005 Vincent Danen <vdanen@annvix.org> 3.4k-32avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 3.4k-31avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen@annvix.org> 3.4k-30avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 3.4k-29sls
- minor spec cleanups
- remove postscript docs

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 3.4k-28sls
- OpenSLS build
- tidy spec

* Thu Nov 13 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.4k-27mdk
- Patch3: Merge code base to XFree86 4.3-25mdk
- Patch4: 64-bit fixes, aka finally make rfb to work

* Thu Jul 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 3.4k-26mdk
- rebuild

* Wed Jul  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.4k-25mdk
- Rebuild, remove dead code

* Tue May 07 2003 Stefan van der Eijk <stefan@eijk.nu> 3.4k-24mdk
- fix alpha build: don't compile against XFree86

* Thu Dec  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 3.4k-23mdk
- added missing parts for %%mklibname switch

* Thu Dec  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 3.4k-22mdk
- use %%mklibname

* Wed Jun 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.4k-21mdk
- Patch1: Portability fixes
- Rpmlint fixes: hardcoded-library-path, use-of-RPM_SOURCE_DIR

* Tue May 21 2002 Stew Benedict <sbenedict@mandrakesoft.com> 3.4k-20mdk
- include libXpm.a on PPC too, so xforms will build
- add URL tag, remove use of SOURCE_DIR for rpmlint

* Thu Jan 17 2002 David BAUDENS <baudens@mandrakesoft.com> 3.4k-19mdk
- Provide again xpm.h

* Wed Jan 16 2002 David BAUDENS <baudens@mandrakesoft.com> 3.4k-18mdk
- Fix conflict with XFree86-devel-4.1.99.6-1mdk

* Sat Jun 30 2001 Stefan van der Eijk <stefan@eijk.nu> 3.4k-17mdk
- BuildRequires:	XFree86-devel

* Sat Dec 09 2000 David BAUDENS <baudens@mandrakesoft.com> 3.4k-16mdk
- PPC: fix %%files
- mv Copyright License

* Wed Dec 06 2000 David BAUDENS <baudens@mandrakesoft.com> 3.4k-15mdk
- Fix provide to make QA happy

* Mon Dec 04 2000 David BAUDENS <baudens@mandrakesoft.com> 3.4k-14mdk
- Make really compliant to new LMDK lib policy

* Fri Nov 24 2000 David BAUDENS <baudens@mandrakesoft.com> 3.4k-13mdk
- Add Provides xpm (were not requires by rpmlint)

* Fri Nov 24 2000 David BAUDENS <baudens@mandrakesoft.com> 3.4k-12mdk
- Make compliant to new LMDK lib policy
- Add missing file
- Add documentation

* Thu Nov 23 2000 David BAUDENS <baudens@mandrakesoft.com> 3.4k-11mdk
- Build with glibc-2.2 and gcc-2.96
- Macros
- Add packager tag

* Thu Sep 05 2000 Francis Galiegue <fg@mandrakesoft.com> 3.4k-10mdk
- More macros
- Let spec-helper do its job...

* Tue Aug 08 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.4k-9mdk
- automatically added BuildRequires

* Mon Apr  3 2000 Adam Lebsack <adam@mandrakesoft.com> 3.4k-8mdk
- Release build.

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Increase release for compat with cassini.

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with rh specs.
- 3.4k.

* Thu May 06 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- upgraded to 3.4j
- spec file cleanups
- added docs to the devel package

* Mon Jun 16 1997 Erik Troan <ewt@redhat.com>
- built against glibc
