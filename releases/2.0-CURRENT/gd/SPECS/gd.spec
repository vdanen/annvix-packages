#
# spec file for package gd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gd
%define version		2.0.33
%define release		%_revrel

%define major		2
%define libname		%mklibname %{name} %{major}

Summary:	A library used to create PNG, JPEG, or WBMP images
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-style
Group:		System/Libraries
URL:		http://www.boutell.com/gd/
Source0:	http://www.boutell.com/gd/http/%{name}-%{version}.tar.bz2
Patch0:		gd-2.0.33-CAN-2004-0941.patch
Patch1:		gd-2.0.33-CVE-2006-2906.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, automake1.7
BuildRequires:	freetype2-devel, gettext-devel, jpeg-devel, png-devel, XFree86-devel, xpm-devel, zlib-devel

%description
gd is a graphics library. It allows your code to quickly draw
images complete with lines, arcs, text, multiple colors, cut and
paste from other images, and flood fills, and write out the result
as a PNG or JPEG file. This is particularly useful in World Wide
Webapplications, where PNG and JPEG are two of the formats
accepted for inlineimages by most browsers.


%package -n %{libname}
Summary:	A library used to create PNG, JPEG, or WBMP images
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	%{libname} = %{version}-%{release}
Obsoletes:	%{name}

%description -n	%{libname}
This package contains the library needed to run programs
dynamically linked with libgd

gd is a graphics library. It allows your code to quickly draw
images complete with lines, arcs, text, multiple colors, cut and
paste from other images, and flood fills, and write out the result
as a PNG or JPEG file. This is particularly useful in World Wide
Webapplications, where PNG and JPEG are two of the formats
accepted for inlineimages by most browsers.


%package -n %{libname}-devel
Summary:	The development libraries and header files for gd
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel

%description -n	%{libname}-devel
These are the development libraries and header files for gd,
the .png and .jpeg graphics library.

gd is a graphics library. It allows your code to quickly draw
images complete with lines, arcs, text, multiple colors, cut and
paste from other images, and flood fills, and write out the result
as a PNG or JPEG file. This is particularly useful in World Wide
Webapplications, where PNG and JPEG are two of the formats
accepted for inlineimages by most browsers.


%package -n %{libname}-static-devel
Summary:	Static GD library
Group:		Development/C
Requires:	%{libname}-devel = %{version}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n	%{libname}-static-devel
This package contains static gd library.


%package utils
Summary:	The Utils files for gd
Group:		System/Libraries
Requires:	%{libname} = %{version}

%description utils
gd is a graphics library. It allows your code to quickly draw
images complete with lines, arcs, text, multiple colors, cut and
paste from other images, and flood fills, and write out the result
as a PNG or JPEG file. This is particularly useful in World Wide
Webapplications, where PNG and JPEG are two of the formats
accepted for inlineimages by most browsers.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n gd-%{version}
%patch0 -p1 -b .CAN-2004-0941
%patch1 -p1 -b .cve-2006-2906

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal-1.7; automake-1.7 --copy --add-missing; autoconf

%configure2_5x

%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall
%multiarch_binaries %{buildroot}%{_bindir}/gdlib-config
%multiarch_includes %{buildroot}%{_includedir}/gd.h


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/gdlib-config
%multiarch %{multiarch_bindir}/gdlib-config
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*.h
%multiarch %{multiarch_includedir}/*.h

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/lib*.a

%files utils
%defattr(-,root,root)
%{_bindir}/annotate
%{_bindir}/bdftogd
%{_bindir}/gd2copypal
%{_bindir}/gd2topng
%{_bindir}/gdparttopng
%{_bindir}/gdtopng
%{_bindir}/pngtogd
%{_bindir}/pngtogd2
%{_bindir}/webpng
%{_bindir}/gd2togif
%{_bindir}/gdcmpgif
%{_bindir}/giftogd2

%files doc
%defattr(-,root,root)
%doc README.TXT index.html


%changelog
* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.33
- add -doc subpackage
- rebuild with gcc4
- P1: security fix for CVE-2006-2906

* Fri Apr 21 2006 Vincent Daen <vdanen-at-build.annvix.org> 2.0.33
- first Annvix build

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 2.0.33-4mdk
- Rebuild

* Mon Jan 31 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.33-3mdk
- some more multiarch support

* Mon Jan 31 2005 Stew Benedict <sbenedict@mandrakesoft.com> 2.0.33-2mdk
- multiarch support, remove "dot" from summaries

* Thu Nov 11 2004 Stew Benedict <sbenedict@mandrakesoft.com> 2.0.33-1mdk
- 2.0.33, still missing an overflow check - patched (patch0)

* Mon Nov  8 2004 Stew Benedict <sbenedict@mandrakesoft.com> 2.0.32-1mdk
- 2.0.32, conditional gif options go away

* Fri Oct 22 2004 Stew Benedict <sbenedict@mandrakesoft.com> 2.0.28-1mdk
- 2.0.28

* Sun Jul 25 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.0.27-3mdk
- add BuildRequires: gettext-devel

* Tue Jul 20 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.27-2mdk
- add conditional gif support (not enabled per default)
- spec file cleanups

* Mon Jul 05 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.27-1mdk
- 2.0.27

* Wed Jun  9 2004 Stew Benedict <sbenedict@mandrakesoft.com> 2.0.26-1mdk
- 2.0.26

* Sat Apr 17 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.0.22-1mdk
- 2.0.22
- fix buildrequires
- spec cosmetics

* Sat Aug  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.15-3mdk
- Remove auto-required packages, enforce current practise for libgd-devel

* Wed Jul  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.15-2mdk
- Rebuild, clean-ups, provides

* Fri Jun 27 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.15-1mdk
- 2.0.15
- use the %%configure2_5x macro
- rework the spec file
- requires or buidrequires t1libs is not needed anymore according
  to Francisco Javier Felix

* Mon May 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.12-2mdk
- misc spec file fixes
- added the static devel sub package

* Fri May 16 2003 Stew Benedict <sbenedict@mandrakesoft.com> 2.0.12-1mdk
- 2.0.12

* Mon Feb 03 2003 François Pons <fpons@mandrakesoft.com> 2.0.9-3mdk
- fix according David Walser.
- add %%mklibname.
- restored srpm gd, as no more orignial gd exists.

* Mon Jan  6 2003 Stew Benedict <sbenedict@mandrakesoft.com> 2.0.9-2mdk
- call srpm gd2, to preserve orginal gd

* Thu Dec 19 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.0.9-1mdk
- new version, do binaries need to be in /usr/sbin?

* Thu Nov 28 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.8.4-7mdk
- Patch2: Let it bootstrap without any libgd installed beforehand...

* Thu Jun 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.8.4-6mdk
- Patch1: Nuke references to /usr/local dir for include and library
  search paths. Put defines in a separate variable.

* Tue Jun 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.8.4-5mdk
- recompiled for libintl2

* Tue Oct 09 2001 Philippe Libat <philippe@mandrakesoft.com> 1.8.4-4mdk
- rebuild against libpng3

* Tue Apr 17 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.8.4-3mdk
- provide libgd1.8

* Tue Apr 17 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.8.4-2mdk
- gd-utils has no need for a name change
- lib major is 1

* Fri Apr 13 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.8.4-1mdk
- This version should fix 90% if the php-gd issues, and the Linuxconf
  segfault. The previous version was broken, it was not linked with
  the required libraries. This means that Chmou got away with a
  non-functional shared patch for two years. JMD sucks for not having
  found out before that.
- Conforms to the new library policy
- This package is only required by Linuxconf and gd, so it should not break
  anything
- Kyle VanderBeek <kylev@yaga.com> added libgd.a static library to -devel

* Sun Nov  5 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.8.3-2mdk
- added Xpm and Xbm support

* Sat Nov  4 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.8.3-1mdk
- 1.8.3
- removed "gif" from descriptions, since it supports PNG since version 1.5
  because of the Unisys GIF patent
- added JPEG support
- added WBMP (intended for wireless devices (not regular web browsers).

* Mon Oct  2 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.8.1-4mdk
- removed build requires on gd-devel.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.8.1-3mdk
- automatically added BuildRequires

* Fri May 19 2000 Pixel <pixel@mandrakesoft.com> 1.8.1-2mdk
- add soname

* Mon Apr  3 2000 Adam Lebsack <adam@mandrakesoft.com> 1.8.1-1mdk
- Upgrade to 1.8.1

* Thu Oct 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Relifting of .spec.
- New shared lib patchs.
- 1.7.
- Add package utils.

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- fix typo :-(

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- we can't use >1.5 unless we backport the gif support :-(.
- Add %defattr.

* Sun Jul 18 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.de>
- 1.5

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- add de locale

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Sep 11 1998 Cristian Gafton <gafton@redhat.com>
- built for 5.2
patch_gd2.0.26_gif_040622.bz2

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
