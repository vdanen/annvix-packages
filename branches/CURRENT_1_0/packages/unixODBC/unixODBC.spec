%define name	unixODBC
%define version	2.2.6
%define release	5sls

%{!?build_opensls:%global build_opensls 0}

%define LIBMAJ 	2
%define libname %mklibname %name %LIBMAJ
%define libgtkgui_major	0
%define libgtkgui_name	%mklibname gtkodbcconfig %{libgtkgui_major}

%if %{build_opensls}
%define qt_gui  0
%define gtk_gui 0
%else
%define qt_gui  1
%define gtk_gui 1
%endif

# Allow --with[out] <feature> at rpm command line build
%{expand: %{?_without_QT:	%%global qt_gui 0}}
%{expand: %{?_without_GTK:	%%global gtk_gui 0}}

# Allow --without <front-end> at rpm command line build
%{expand: %{?_with_QT:		%%global qt_gui 1}}
%{expand: %{?_with_GTK:		%%global gtk_gui 1}}

# define to update aclocal.m4 with new libtool.m4
%define update_libtool 1
%ifarch x86_64 mips
%define update_libtool 1
%endif

Summary: 	Unix ODBC driver manager and database drivers
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
Group: 		Databases
License: 	LGPL
URL: 		http://www.unixODBC.org
Source: 	http://www.unixodbc.org/%{name}-%{version}.tar.bz2
Source2:	odbcinst.ini
Source3:	qt-attic.tar.bz2
Source4:	qt-attic2.tar.bz2
Patch0:		unixODBC-2.2.6-lib64.patch.bz2
Patch1:		unixodbc-fix-compile-with-qt-3.1.1.patch.bz2
Patch2:		unixodbc-fix-compile-with-qt-3.1.1.patch2.bz2

BuildRoot: 	%_tmppath/%name-%version-%release-root
# don't take away readline, we do want to build unixODBC with readline.
BuildRequires:	bison flex readline-devel chrpath
%if %{update_libtool}
BuildRequires:	automake1.7
%endif
%if %{qt_gui}
BuildRequires:  qt3-devel
%endif
%if %gtk_gui
BuildRequires:	gnome-libs-devel, gnome-common
%endif

%description
UnixODBC is a free/open specification for providing application developers 
with a predictable API with which to access Data Sources. Data Sources include 
SQL Servers and any Data Source with an ODBC Driver.


%package -n %{libname}
Summary:	Libraries unixODBC 
Group:		System/Libraries

%description -n %{libname}
unixODBC  libraries.

%if %gtk_gui
%package -n %{libgtkgui_name}
Summary:	gODBCConfig libraries
Group: 		System/Libraries

%description -n %{libgtkgui_name}
gODBCConfig libraries.
%endif

%package -n %{libname}-qt
Group:		System/Libraries
Summary:	unixODBC inst library, with Qt.

%description -n %{libname}-qt
unixODBC inst library, Qt flavored.

This has been split off from the main unixODBC libraries so you don't
requires X11 and qt if you wish to use unixODBC.

%package -n %{libname}-devel
Summary: 	Includes and static libraries for ODBC development
Group: 		Development/Other
Requires: 	%{libname} = %version-%release
Provides:	%{name}-devel lib%{name}-devel libodbc.so libodbcinst.so
Obsoletes:	%{name}-devel

%description -n %{libname}-devel
unixODBC aims to provide a complete ODBC solution for the Linux platform.
This package contains the include files and static libraries for development.

%package gui-qt
Summary: 	ODBC configurator, Data Source browser and ODBC test tool based on Qt
Group: 		Databases
Requires: 	%{name} = %version-%release

%description gui-qt
unixODBC aims to provide a complete ODBC solution for the Linux platform.
All programs are GPL.

This package contains two Qt based GUI programs for unixODBC: 
ODBCConfig and DataManager

%package gui-gtk
Summary: 	ODBC configurator based on GTK+ and GTK+ widget for gnome-db
Group:		Databases
Requires: 	%{name} = %version-%release

%description gui-gtk
unixODBC aims to provide a complete ODBC solution for the Linux platform.
All programs are GPL.

This package contains one GTK+ based GUI program for unixODBC: gODBCConfig

%prep
%setup -q -a3 -a4
%patch0 -p1 -b .lib64
%patch1 -p1
%patch2 -p1

%if %{update_libtool}
aclocal-1.7 && autoconf
cd Drivers/MySQL
aclocal-1.7 && autoconf
cd ../..
%endif

%build
export QTDIR=%{_libdir}/qt3

# Search for qt/kde libraries in the right directories (avoid patch)
# NOTE: please don't regenerate configure scripts below
perl -pi -e "s@/lib(\"|\b[^/])@/%_lib\1@g if /(kde|qt)_(libdirs|libraries)=/" configure

%configure2_5x --enable-static
make

%install
rm -fr %buildroot

# Short Circuit Compliant (tm).
[ ! -f doc/Makefile ] && {
	cd doc
	echo -en "install:\n\n" > Makefile
	cd ..
}

%makeinstall

install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/
perl -pi -e "s,/lib/,/%{_lib}/," $RPM_BUILD_ROOT%{_sysconfdir}/odbcinst.ini

%if %gtk_gui
# gODBCConfig must be built after installing the main unixODBC parts
cd gODBCConfig
%configure2_5x --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} --with-odbc=$RPM_BUILD_ROOT%{_prefix}

# I don't know why this happens. -- Geoff
mv po/Makefile.in po/Makefile
# (sb) can't find depcomp
cp ../depcomp .
%make
# ugly hack.
%makeinstall || true
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps/gODBCConfig
for pixmap in ./pixmaps/*;do
   install -m 644 $pixmap $RPM_BUILD_ROOT%{_datadir}/pixmaps/gODBCConfig
done
cd ..
%endif

# drill out shared libraries for gODBCConfig *sigh*
# also rill out the Qt inst library that doesn't seem to be used at the moment
# by anyone ATM?
echo "%defattr(-,root,root)" > libodbc-libs.filelist
find $RPM_BUILD_ROOT%_libdir -name '*.so.*' | sed -e "s|$RPM_BUILD_ROOT||g" | grep -v -e gtk -e instQ >> libodbc-libs.filelist

# Uncomment the following if you wish to split off development libraries
# as well so development with ODBC does not require X11 libraries installed.
# Also you need to add in the appropriate description and filelist.
if 0; then

echo "%defattr(-, root, root)" > libodbc-devellibs.filelist
find $RPM_BUILD_ROOT/%_libdir -name '*.so' -o -name '*.la' -o -name '*.a' | sed -e "s|$RPM_BUILD_ROOT||g" | grep -v -e gtk -e instQ>> libodbc-devellibs.filelist

fi

# (sb) more mess - gODBCConfig has an rpath embedded on x86 only?
%if %gtk_gui
chrpath -d $RPM_BUILD_ROOT/%{_bindir}/gODBCConfig
%endif

# Menu entries

install -d $RPM_BUILD_ROOT%{_menudir}

%if %{qt_gui}
# ODBCConfig
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/unixODBC-gui-qt
?package(%{name}-gui-qt): \
needs="x11" \
section="Applications/Databases" \
longtitle="ODBCConfig" \
title="ODBCConfig" \
icon="databases_section.png" \
command="ODBCConfig"

?package(%{name}-gui-qt): \
needs="x11" \
section="Applications/Databases" \
longtitle="DataManager" \
title="DataManager" \
icon="databases_section.png" \
command="DataManager"

?package(%{name}-gui-qt): \
needs="x11" \
section="Applications/Databases" \
longtitle="ODBCtest" \
title="ODBCtest" \
icon="databases_section.png" \
command="odbctest"
EOF
%endif

%if %gtk_gui
# gODBCConfig
# Put capital G in title and longtitle to shut rpmlint warnings
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/unixODBC-gui-gtk
?package(%{name}-gui-gtk): \
needs="x11" \
section="Applications/Databases" \
longtitle="GODBCConfig" \
title="GODBCConfig" \
icon="databases_section.png" \
command="gODBCConfig" 
EOF
%endif

find doc -name Makefile\* -exec rm {} \;

%if !%{qt_gui}
rm -f %{buildroot}%{_bindir}/{ODBCConfig,DataManager,DataManagerII,odbctest}
rm -f %{buildroot}%{_libdir}/libodbcinstQ.so.1.0.0
%endif


%clean
rm -rf $RPM_BUILD_ROOT 
rm -f libodbc-libs.filelist

%if %gtk_gui
%post -n %{libgtkgui_name} -p /sbin/ldconfig
%postun -n %{libgtkgui_name} -p /sbin/ldconfig
%endif

%if %{qt_gui}
%post -n %{libname}-qt -p /sbin/ldconfig
%postun -n %{libname}-qt -p /sbin/ldconfig
%endif

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%if %{qt_gui}
%post gui-qt
%{update_menus}

%postun gui-qt
%{clean_menus}
%endif

%if %gtk_gui
%post gui-gtk
%{update_menus}

%postun gui-gtk
%{clean_menus}
%endif


%files 
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README
%config(noreplace) %verify(not md5 size mtime)  %{_sysconfdir}/odbc*.ini
%{_bindir}/dltest
%{_bindir}/isql
%{_bindir}/odbcinst
%{_bindir}/iusql
	  


%files -n %{libname} -f libodbc-libs.filelist

%files -n %{libname}-devel 
%defattr(-,root,root)
%doc doc/
%{_includedir}/*
%_libdir/lib*.so
%_libdir/*.a
%_libdir/*.la

%if %{qt_gui}
%files -n %{libname}-qt
%defattr(-, root, root)
%_libdir/lib*instQ.so.*

%files gui-qt
%defattr(-, root, root)
%{_bindir}/DataManager
%{_bindir}/DataManagerII
%{_bindir}/ODBCConfig
%{_bindir}/odbctest
%{_menudir}/unixODBC-gui-qt
%endif

%if %gtk_gui
%files -n %{libgtkgui_name}
%defattr(-,root, root)
%_libdir/libgtk*.so.*

%files gui-gtk 
%defattr(-, root, root)
%doc NEWS README AUTHORS
%{_bindir}/gODBCConfig
%{_menudir}/unixODBC-gui-gtk
%{_datadir}/pixmaps/*
%endif

%changelog
* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 2.2.6-5sls
- OpenSLS build
- tidy spec
- use %%build_opensls to turn of QT/GTK+ stuff
- remove some installed/unpackaged stuff since we don't build QT
- move gnome-common req to only if we're building the GTK stuff as I don't
  believe it's needed otherwise

* Tue Sep  2 2003 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.6-4mdk
- fix buildrequires

* Fri Aug  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.6-3mdk
- fix mklibname for gtkodbcconfig

* Fri Aug  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.6-2mdk
- lib64 fixes, fix --without QT build

* Thu Jul 24 2003 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.6-1mdk
- 2.2.6, rework patch0, drop patch3, massage build a bit

* Thu Jul 17 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 2.2.5-2mdk
- Rebuild

* Fri Apr  4 2003 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.5-1mdk
- 2.2.5

* Thu Jan 30 2003 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.4-1mdk
- 2.2.4, rework patch0, don't build empty m4 dir (patch3)

* Tue Jan 07 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 2.2.3-2mdk
- Add patch1 : Fix compile with qt-3.1.1

* Thu Oct 31 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.3-1mdk
- new version

* Mon Oct  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.2-10mdk
- Search for qt libraries in the right directories (aka make it lib64 aware)

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.2-9mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Wed Jul 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.2.2-8mdk
- rebuild for new readline

* Tue Jul 23 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.2-7mdk
- Fix typos for qt_gui tests
- Enable build --with[out] (QT|GTK) idioms
- Patch0: Look for ODBC libraries in the right directory
- Rpmlint fixes: strange-permission, hardcoded-library-path
- Regenerate configure script with updated libtool.m4 where necessary

* Fri Jul 12 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.2-6mdk
- Add back *.la and *.a as well (oops).

* Thu Jul 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.2-5mdk
- added back *.so in devel package

* Tue Jul 09 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.2-4mdk
- Fix b0rked libs package, it required X11! a.k.a. split things up.
- Gtk+ (Gnome really) and Qt GUI are now conditionsals, but enabled by default.
- BuildRequires.
- Short Circuit Compliant (tm).

* Tue Jul 09 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.2-3mdk
- A minor description change.

* Tue Jul 09 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.2-2mdk
- Minor typo fix in description.

* Mon Jul 08 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.2.2-1mdk
- new version 2.2.2.

* Tue May 28 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.2.1-3mdk
- get rid of the require on libqt2

* Tue May 28 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.2.1-2mdk
- build with gcc 3.1.
- build against libqt3.
- use %%configure2_5x.

* Fri Apr 26 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.2.1-1mdk
- 2.2.1.

* Mon Feb 04 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.2.0-1mdk
- 2.2.0.

* Wed Jan 09 2002 David BAUDENS <baudens@mandrakesoft.com> 2.1.1-2mdk
- Fix menu entries

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.1-1mdk
- 2.1.1.
- Re-provide Qt part of the package (qmake now optional for building).
- Removed Patch1 (nodriver patch).

* Fri Nov 30 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.0-1mdk
- 2.1.0.
- Remove patch 0 (unixODBC-2.0.8-protofix.patch)
- Provides the .so libraries (Sun jre needs it).

* Wed Nov 21 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.0.11-2mdk
- Fix stange-permission warning.

* Tue Nov 20 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.0.11-1mdk
- 2.0.11
- Remove initial txt driver installation.

* Wed Oct 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.0.8-8mdk
- Remove the Prodives on the .so libraries.
- Make rpmlint happier.

* Tue Sep 11 2001 David BAUDENS <baudens@mandrakesoft.com> 2.0.8-7mdk
- Fix menu entries
- Doesn't use ugly icons

* Tue Sep 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.0.8-6mdk
- Fixed menu entries.

* Sun Sep 09 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.0.8-5mdk
- Added little and large icon.

* Thu Sep 06 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.0.8-4mdk
- Fixed menu entries.

* Thu Sep 06 2001 Stefan van der Eijk <stefan@eijk.nu> 2.0.8-3mdk
- BuildRequires:	byacc flex
- Removed BuildRequires: db1-devel (gnome-libs-devel provides this)
- Remove %%{_iconsdir} with gui-gtk and gui-qt packages, the icon is
  provided by the libunixODBC2 package.

* Wed Sep 05 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.0.8-2mdk
- Removed sources from gui packages.

* Mon Aug 27 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.0.8-1mdk
- 2.0.8.
- Added Distribution tag.
- s/Copyright/License.
- make rpmlint happy (gui-gtk & gui-qt later).

* Sun Jun 24 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.0.6-4mdk
- Apply patch to fix prototypes in code to match headers,
  which fixes build on Alpha and maybe IA64.

* Sun Jun 24 2001 Stefan van der Eijk <stefan@eijk.nu> 2.0.6-3mdk
- BuildRequires:	db1-devel
- BuildRequires:	gnome-libs-devel
- Remove BuildRequires:	XFree86-devel

* Tue May 15 2001 Matthias Badaire <mbadaire@mandrakesoft.com> 2.0.6-2mdk
- make rpmlint happy

* Fri Apr 20 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 2.0.6-1mdk
- 2.0.6
- server macros

* Wed Mar 14 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0.4-3mdk
- Use QTDIR instead.
- Use %%make and not %%__make.
- Work around an ugly installation problem.
- Include the pixmaps for GODBCConfig.

* Tue Mar 13 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 2.0.4-2mdk
- removed unnecessary patch
- added --with-qt-dir=/usr/lib/qt2 in %configure 

* Wed Mar 07 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 2.0.4-1mdk
- new release
- added gODBCConfig GUI (GTK)
- added ODBCConfig  GUI (KDE2)
- added Datamanager GUI (KDE2)
- added ODBCTest    GUI (KDE2)
- many improvements 
- bump a new and shiny source into cooker ;PP

* Tue Jan 16 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0.3-1mdk
- bump a new and shiny source into cooker.

* Sat Nov 25 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.8.13-1mdk
- new and shiny source bumped into cooker.

* Fri Aug 25 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.8.12-1mdk
- updated release.

* Wed Aug 02 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 1.8.7-2mdk
- macroszifications
- BM
- Geoff <snailtalk@mandrakesoft.com> -- fix the doc kludge

* Thu Apr 20 2000 <ghibo@mandrakesoft.com> 1.8.7-1mdk
- updated version.

* Sat Apr 15 2000 <ghibo@mandrakesoft.com> 1.8.3-1mdk
- updated to new version.
- fixed group.

* Tue Oct 19 1999 <lenny@mandrakesoft.com>
- Specfile adaptation.
- First pasckage for Mandrake
