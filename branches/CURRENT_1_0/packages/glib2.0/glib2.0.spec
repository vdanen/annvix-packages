%define name	glib%{api_version}
%define version	%{major_version}.%{minor_version}.%{micro_version}
%define release	3sls

# enable_gtkdoc: Toggle if gtkdoc stuff should be rebuilt
#	0 = no
#	1 = yes
%define enable_gtkdoc	0

%define req_pkgconfig_version	0.12

# Note that this is NOT a relocatable package
%define api_version	2.0
%define lib_major	0
%define lib_name	%mklibname %{name}_ %{lib_major}

%define major_version 2
%define minor_version 2
%define micro_version 3

Summary:	GIMP Toolkit and GIMP Drawing Kit support library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://www.gtk.org
Source0:	ftp://ftp.gtk.org/pub/gtk/v%{api_version}/glib-%{version}.tar.bz2
Source1:	glib20.sh.bz2
Source2:	glib20.csh.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	gettext
BuildRequires:	pkgconfig >= %{req_pkgconfig_version}
BuildRequires:	libtool >= 1.4.2-2mdk
%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.10
%endif

Requires:	common-licenses

%description
Glib is a handy library of utility functions. This C
library is designed to solve some portability problems
and provide other useful functionality which most
programs require.

Glib is used by GDK, GTK+ and many applications.
You should install Glib because many of your applications
will depend on this library.

%package -n %{lib_name}
Summary:	%{summary}
Group:		%{group}
Provides:	glib2 = %{version}-%{release}
Provides:	libglib2 = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Conflicts:	libglib1.3_13

%description -n %{lib_name}
Glib is a handy library of utility functions. This C
library is designed to solve some portability problems
and provide other useful functionality which most
programs require.

Glib is used by GDK, GTK+ and many applications.
You should install Glib because many of your applications
will depend on this library.

This package contains the library needed to run programs dynamically
linked with the glib.

%package -n %{lib_name}-devel
Summary:	Static libraries and header files of %{name}
Group:		Development/C
Provides:	glib2-devel = %{version}-%{release}
Provides:	libglib2-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}
Requires:	pkgconfig >= %{req_pkgconfig_version}
Requires:	glib-gettextize >= %{version}
Conflicts:	libglib1.3_13-devel

%description -n %{lib_name}-devel
Static libraries and header files for the support library for the GIMP's X
libraries, which are available as public libraries.  GLIB includes generally
useful data structures.


%package -n glib-gettextize
Summary:	Gettextize replacement
Group:		Development/Other

%description -n glib-gettextize
%{name} package is designed to replace gettextize completely.
Various gettext related files are modified in glib and gtk+ to
allow better and more flexible i18n; however gettextize overwrites
them with its own copy of files, thus nullifying the changes.
If this replacement of gettextize is run instead, then all gnome
packages can potentially benefict from the changes.

%prep
%setup -n glib-%{version} -q

%build

#we don't use libtool 1.5 yet
%define __libtoolize /bin/true

%configure2_5x \
	--enable-static \
%if !%enable_gtkdoc
	--enable-gtk-doc=no
%endif

%make
make check

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/glib20.sh
bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/glib20.csh
chmod a+x  $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/*

%find_lang glib20


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig


%files -n %{lib_name} -f glib20.lang
%defattr(-, root, root)
%doc README
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_libdir}/libglib-%{api_version}.so.*
%{_libdir}/libgmodule-%{api_version}.so.*
%{_libdir}/libgthread-%{api_version}.so.*
%{_libdir}/libgobject-%{api_version}.so.*

%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS
%doc %{_datadir}/gtk-doc/html/*
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a
%{_libdir}/glib-%{api_version}
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man1/*
%{_datadir}/aclocal/glib-%{api_version}.m4
%{_bindir}/glib-genmarshal
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query

%files -n glib-gettextize
%defattr(-, root, root)
%{_bindir}/glib-gettextize
%{_datadir}/aclocal/glib-gettext.m4
%{_datadir}/glib-%{api_version}

%changelog
* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.2.3-3sls
- minor spec cleanups
- remove %%build_opensls macro

* Mon Dec 22 2003 Vincent Danen <vdanen@opensls.org> 2.2.3-2sls
- OpenSLS build

* Wed Aug 27 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.2.3-1mdk
- Release 2.2.3

* Fri Jul 11 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.2.2-3mdk
- Rebuild with glib-gettextize this time.. (Never let KDE people compile GNOME packages :)

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 2.2.2-2mdk
- Rebuild

* Tue Jun 10 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.2.2-1mdk
- Release 2.2.2

* Mon May 12 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.2.1-2mdk
- Rebuild to get new devel dep/requires
- mklibnamification

* Mon Feb  3 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 1-1mdk
- Release 2.2.1

* Tue Dec 31 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.2.0-1mdk
- Release 2.2.0

* Tue Dec 17 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.5-1mdk
- Release 2.1.5

* Thu Dec 12 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.4-1mdk
- Release 2.1.4

* Tue Dec  3 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1.3-1mdk
- Release 2.1.3

* Tue Nov  5 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.7-1mdk
- Release 2.0.7
- Remove patch0 (merged upstream)

* Thu Sep 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.6-3mdk
- Patch0: Fix tests for 64-bit platforms. It's not nice to check a
  package if tests are broken.

* Wed Aug 21 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.6-2mdk
- Source 1 & 2 (rawhide): enable G_BROKEN_FILENAMES variable by default
- Add conflicts on libglib13 which was shipped with Mdk 8.2 to ease upgrade

* Mon Aug  5 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.6-1mdk
- Release 2.0.6

* Tue Jul 30 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.4-2mdk
- Fix BuildRequires (Thanks to David Walser)

* Mon Jun 17 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.4-1mdk
- Release 2.0.4

* Mon Jun  3 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.3-1mdk
- Release 2.0.3

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.1-2mdk
- Automated rebuild in gcc3.1 environment

* Tue Apr  2 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.1-1mdk
- Release 2.0.1

* Thu Mar 21 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.0-1mdk
- Release 2.0.0 
- Package based on Abel Cheung work (thanks a lot)

* Mon Feb 11 2002 Stefan van der Eijk <stefan@eijk.nu> 1.3.13-2mdk
- BuildRequires
- Removed directory of %%{_datadir}/gtk-doc and %%{_datadir}/gtk-doc/html
  this packages shouldn't own them.

* Mon Feb  4 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.13-1mdk
- Release 1.3.13

* Mon Jan  7 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.12-1mdk
- Release 1.3.12
- Remove patch0 (merged upstream)

* Fri Dec 21 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.11-2mdk
- Patch0 (rawhide) : fix for 64bit arch
- Clean specfile with help of Abel Cheung <maddog@linux.org.hk> :
 - Require newer libtool, to fix bootstrap problem
 - More verbose summaries and descriptions
 - Split glib-gettextize into new package

* Tue Dec 11 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.11-1mdk
- Release 1.3.11

* Thu Nov  8 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.10-2mdk
- Remove testgruntime from package (not needed, since we run make check)

* Wed Nov  7 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.10-1mdk
- Release 1.3.10
- Remove patch0 (merged upstream)

* Tue Nov  6 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.9-5mdk
- add patch0 to fix a function definition, which fixes 64-bit build
- un-comment-out make check tests, so that we run them
- do not use %%make, it screws up 'make check' test build

* Wed Oct 17 2001 Stefan van der Eijk <stefan@eijk.nu> 1.3.9-4mdk
- add glib-mkenums to filelist

* Sun Oct  7 2001 Stefan van der Eijk <stefan@eijk.nu> 1.3.9-3mdk
- BuildRequires:	pkgconfig

* Thu Oct  4 2001 DindinX <odin@mandrakesoft.com> 1.3.9-2mdk
- rebuild with new libtool

* Thu Sep 27 2001 DindinX <odin@mandrakesoft.com> 1.3.9-1mdk
- 1.3.9

* Tue Aug  7 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.3.6-6mdk
- Add missing provides in -devel

* Thu Aug 02 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.3.6-5mdk
- rebuild with forcing use of new libtools, included all aclocal files

* Wed Jul 11 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.6-4mdk
- explicitly list each shared lib, to prevent false build success
  with bad libtool
- Requires: common-licenses, and remove COPYING from %%doc
- run 'make check' tests for each build

* Thu Jun 21 2001 DindinX <odin@mandrakesoft.com> 1.3.6-3mdk
- new name (to follow the policy). Don't ask.

* Tue Jun 19 2001 DindinX <odin@mandrakesoft.com> 1.3.6-2mdk
- rebuild

* Fri Jun 15 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.3.6-1mdk
- Bump 1.3.6 into cooker.

* Sun May 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.3.5-1mdk
- Bump glib version 1.3.5 into cooker.
- Manually install testgruntime.
- In development package don't include the documentation twice.

* Fri Apr 27 2001 DindinX <odin@mandrakesoft.com> 1.3.4-2mdk
- added files for pkgconfig and some documentation

* Wed Apr 25 2001 DindinX <odin@mandrakesoft.com> 1.3.4-1mdk
- 1.3.4

* Tue Dec  5 2000 DindinX <odin@mandrakesoft.com> 1.3.2-4mdk
- new lib policy

* Mon Nov 20 2000 DindinX <odin@mandrakesoft.com> 1.3.2-3mdk
- redo my patch to best fit glib-1.3.2
- move %%doc to -devel

* Mon Nov 20 2000 Daouda Lo <daouda@mandrakesoft.com> 1.3.2-2mdk
- regenerate Dindinx's patch.

* Sat Nov 18 2000 Daouda Lo <daouda@mandrakesoft.com> 1.3.2-1mdk
- release

* Wed Nov 15 2000 DindinX <odin@mandrakesoft.com> 1.3.1-1mdk
- version 1.3.1 (first pre2)

