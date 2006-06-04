#
# spec file for package newt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		newt
%define version 	0.51.6
%define release 	%_revrel

%define major		0.51
%define libname		%mklibname %{name} %{major}

Summary:	A development library for text mode user interfaces
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
Source:		ftp://ftp.redhat.com/pub/redhat/linux/code/newt/newt-%{version}.tar.bz2
Patch0:		newt-gpm-fix.diff
Patch1:		newt-mdkconf.patch
Patch2:		newt-0.51.4-fix-wstrlen-for-non-utf8-strings.patch
Patch3:		newt-0.51.6-avx-nostatic.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glibc-static-devel, popt-devel, python-devel >= 2.2, slang-devel

Requires:	slang
Provides:	snack

%description
Newt is a programming library for color text mode, widget based user
interfaces.  Newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package contains a
/usr/bin/dialog replacement called whiptail.  Newt is based on the
slang library.


%package -n %{libname}
Summary:	Newt windowing toolkit development files library
Group:		Development/C
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
Newt is a programming library for color text mode, widget based user
interfaces.  Newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package contains the
shared library needed by programs built with newt. Newt is based on the
slang library.


%package -n %{libname}-devel
Summary:	Newt windowing toolkit development files
Group:		Development/C
Requires:	slang-devel %{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release} %{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel

%description -n %{libname}-devel
The newt-devel package contains the header files and libraries
necessary for developing applications which use newt.  Newt is
a development library for text mode user interfaces.  Newt is
based on the slang library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

%patch0 -p0
%patch1 -p0
%patch2 -p1
#%patch3 -p0 -b .nostatic


%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
%configure --without-gpm-support

%make
%make shared


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}
%makeinstall
ln -sf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}

rm -rf  %{buildroot}%{_libdir}/python{1.5,2.0,2.1,2.2,2.3}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr (-,root,root)
%{_libdir}/libnewt.so.*

%files 
%defattr (-,root,root)
%{_bindir}/whiptail
%{_libdir}/python%{pyver}/site-packages/*

%files -n %{libname}-devel
%defattr (-,root,root)
%{_includedir}/newt.h
%{_libdir}/libnewt.a
%{_libdir}/libnewt.so

%files doc
%defattr (-,root,root)
%doc COPYING CHANGES
%doc tutorial.sgml


%changelog
* Sat Jun 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6
- rebuild against new python
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6-5avx
- rebuild against new python

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6-4avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6-2avx
- bootstrap build
- don't apply P3 and build with stack protection

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.6-1avx
- 0.51.6
- use %%pyver macro
- spec cleanups
- P3: don't compile the test file -static as it freaks out with our
  __guard symbols and such (from SSP)

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.51.4-10avx
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 0.51.4-9sls
- minor spec cleanups
- remove %%build_opensls macro

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 0.51.4-8sls
- sync with 7mdk (gbeauchesne): fix mklibnamization

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 0.51.4-7sls
- OpenSLS build
- tidy spec
- use %%build_opensls to build without gpm support

* Mon Sep  8 2003 Warly <warly@mandrakesoft.com> 0.51.4-6mdk
- mklibnamize

* Sat Aug 30 2003 Pixel <pixel@mandrakesoft.com> 0.51.4-5mdk
- fix wstrlen() for non-utf8 strings

* Tue Aug 12 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.51.4-4mdk
- rebuild for new python

* Wed Jul 09 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.51.4-3mdk
- rebuild for new devel provides

* Mon Jun 16 2003 Warly <warly@mandrakesoft.com> 0.51.4-2mdk
- add mklibname macros

* Mon Jun 16 2003 Warly <warly@mandrakesoft.com> 0.51.4-1mdk
- new version (main changes):
  0.51.4:
    - fixed help line drawing in UTF-8
    - fixed snack.CListbox to work properly with UTF-8
  0.51.3:
    - added Ctrl-L screen refresh 
    - fixed segfault in test.c when listbox items are selected
    - accessibility: made newt useable with monochrome terms
    - error checking (curcomp exists) for formEvent, newtFormGetCurrent, removed fifty button limit
  0.51.2:
    - fixed wstrlen() it was calculating wcwidth(first wide char in  string) * strlen(str) instead of the actual width of the whole string

* Fri Oct 25 2002 Warly <warly@mandrakesoft.com> 0.51.0-1mdk
- new version

* Tue Aug 06 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.50.34-4mdk
- BuildRequires.

* Wed Jun 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.50.34-3mdk
- Patch3: Fix reference to libdir in python(bin)?dir variables
- Patch2: Don't build whiptcl.so. Nuke BuildRequires: tcl. Nobody
  appears to have used it, and wasn't in rpm either.

* Mon Jan 14 2002 Stefan van der Eijk <stefan@eijk.nu> 0.50.34-2mdk
- BuildRequires
- Remove patch2.
- fix %%files for python 2.2

* Mon Oct 29 2001 Warly <warly@mandrakesoft.com> 0.50.34-1mdk
- new version

* Fri Oct 12 2001 Stefan van der Eijk <stefan@eijk.nu> 0.50.31-2mdk
- BuildRequires: python --> python-devel

* Fri Aug 24 2001 Warly <warly@mandrakesoft.com> 0.50.31-1mdk
- new version

* Tue Jun  5 2001  Warly <warly@mandrakesoft.com> 0.50.22-1mdk
- new version

* Sun Apr 29 2001 Stefan van der Eijk <stefan@eijk.nu> 0.50.19-4mdk
- fixed patch for python 2.1
- fixed .spec file for python 2.1

* Tue Apr 12 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.50.19-3mdk
- Change buildrequires.
- More macros.
- Add obsoletes.

* Tue Feb 20 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.50.19-2mdk
- change a bit color theme of buttons and active buttons
- fix Provides

* Tue Jan 09 2001 Geoff <snailtalk@mandrakesoft.com> 0.50.19-1mdk
- new and shiny source.

* Wed Nov 29 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.50.8-8mdk
- Add missing Provides: (thx stefan, warlyscks).

* Fri Nov 24 2000 Warly <warly@mandrakesoft.com> 0.50.8-7mdk
- split libnewt0 packages

* Thu Nov 23 2000 Vincent Saugey <vince@mandrakesoft.com> 0.50.8-6mdk
- add dependencie on newt from newt-devel
- Patch for python 2.0
- Add build requires on tcl

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.50.8-5mdk
- automatically added BuildRequires

* Sun Jul 23 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.50.8-4mdk
- macro-ization
- BM

* Fri May 19 2000 Pixel <pixel@mandrakesoft.com> 0.50.8-3mdk
- add soname

* Wed Apr 5 2000 Warly <warly@mandrakesoft.com> 0.50.8-2mdk
- readd the mandrake colors patch

* Wed Apr 5 2000 Warly <warly@mandrakesoft.com> 0.50.8-1mdk
- new groups: System/Librairies and Development/C for devel

* Sat Mar 11 2000 Pixel <pixel@mandrakesoft.com> 0.50-15mdk
- really default to mandrake colors (applying the patch works better :)

* Tue Jan 11 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.50-14mdk
- By default mandrake colors.

* Tue Dec 14 1999 Frederic Lepied <flepied@mandrakesoft.com>

- fix bug when gpm isn't running

* Wed Oct 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Build release.

* Fri Oct  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 0.50.

* Wed Jun 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Patch from H.J. Lu <hjl@varesearch.com> :
- fixed tab expansion.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- add de locale

* Mon Mar 15 1999 Matt Wilson <msw@redhat.com>
- fix from Jakub Jelinek for listbox keypresses

* Fri Feb 27 1999 Matt Wilson <msw@redhat.com>
- fixed support for navigating listboxes with alphabetical keypresses

* Thu Feb 25 1999 Matt Wilson <msw@redhat.com>
- updated descriptions
- added support for navigating listboxes with alphabetical keypresses

* Mon Feb  8 1999 Matt Wilson <msw@redhat.com>
- made grid wrapped windows at least the size of their title bars

* Fri Feb  5 1999 Matt Wilson <msw@redhat.com>
- Function to set checkbox flags.  This will go away later when I have
  a generic flag setting function and signals to comps to go insensitive.

* Tue Jan 19 1999 Matt Wilson <msw@redhat.com>
- Stopped using libgpm, internalized all gpm calls.  Still need some cleanups.

* Thu Jan  7 1999 Matt Wilson <msw@redhat.com>
- Added GPM mouse support
- Moved to autoconf to allow compiling without GPM support
- Changed revision to 0.40

* Wed Oct 21 1998 Bill Nottingham <notting@redhat.com>
- built against slang-1.2.2

* Wed Aug 19 1998 Bill Nottingham <notting@redhat.com>
- bugfixes for text reflow
- added docs

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- devel package moved to Development/Libraries

* Thu Apr 30 1998 Erik Troan <ewt@redhat.com>
- removed whiptcl.so -- it should be in a separate package

* Mon Feb 16 1998 Erik Troan <ewt@redhat.com>
- added newtWinMenu()
- many bug fixes in grid code

* Wed Jan 21 1998 Erik Troan <ewt@redhat.com>
- removed newtWinTernary()
- made newtWinChoice() return codes consistent with newtWinTernary()

* Fri Jan 16 1998 Erik Troan <ewt@redhat.com>
- added changes from Bruce Perens
    - small cleanups
    - lets whiptail automatically resize windows
- the order of placing a grid and adding components to a form no longer
  matters
- added newtGridAddComponentsToForm()

* Wed Oct 08 1997 Erik Troan <ewt@redhat.com>
- added newtWinTernary()

* Tue Oct 07 1997 Erik Troan <ewt@redhat.com>
- made Make/spec files use a buildroot
- added grid support (for newt 0.11 actually)

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- Added patched from Clarence Smith for setting the size of a listbox
- Version 0.9

* Tue May 28 1997 Elliot Lee <sopwith@redhat.com> 0.8-2
- Touchups on Makefile
- Cleaned up NEWT_FLAGS_*

* Tue Mar 18 1997 Erik Troan <ewt@redhat.com>
- Cleaned up listbox
- Added whiptail
- Added newtButtonCompact button type and associated colors
- Added newtTextboxGetNumLines() and newtTextboxSetHeight()

* Tue Feb 25 1997 Erik Troan <ewt@redhat.com>
- Added changes from sopwith for C++ cleanliness and some listbox fixes.
