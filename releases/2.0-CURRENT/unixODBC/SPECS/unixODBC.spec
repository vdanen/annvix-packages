#
# spec file for package unixODBC
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		unixODBC
%define version		2.2.11
%define release		%_revrel

%define major		1
%define libname 	%mklibname %{name} %{major}

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
Patch0:		unixODBC-2.2.6-lib64.patch
Patch1:		unixODBC-2.2.11-libtool.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
# don't take away readline, we do want to build unixODBC with readline.
BuildRequires:	bison flex readline-devel libltdl-devel
BuildRequires:	automake1.7 autoconf2.5 >= 2.52

%description
UnixODBC is a free/open specification for providing application developers 
with a predictable API with which to access Data Sources. Data Sources include 
SQL Servers and any Data Source with an ODBC Driver.


%package -n %{libname}
Summary:	Libraries unixODBC 
Group:		System/Libraries
Provides:	lib%{name}2
Obsoletes:	lib%{name}2

%description -n %{libname}
unixODBC  libraries.


%package -n %{libname}-devel
Summary: 	Includes and static libraries for ODBC development
Group: 		Development/Other
Requires: 	%{libname} = %{version}
Provides:	%{name}-devel lib%{name}-devel libodbc.so libodbcinst.so lib%{name}2-devel
Obsoletes:	%{name}-devel lib%{name}2-devel

%description -n %{libname}-devel
unixODBC aims to provide a complete ODBC solution for the Linux platform.
This package contains the include files and static libraries for development.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a3 -a4
%patch0 -p1 -b .lib64
%patch1 -p1 -b .libtool

autoconf


%build
unset QTDIR

export EGREP='grep -E'
libtoolize --copy --force
%configure2_5x \
    --enable-static
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# Short Circuit Compliant (tm).
[ ! -f doc/Makefile ] && {
    cd doc
    echo -en "install:\n\n" > Makefile
    cd ..
}

export EGREP='grep -E'

%makeinstall

install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/
perl -pi -e "s,/lib/,/%{_lib}/," %{buildroot}%{_sysconfdir}/odbcinst.ini

# (sb) use the versioned symlinks, rather than the .so's, this should
# eliminate the issues with requiring -devel packages or having
# to override auto requires

pushd %{buildroot}
    newlink=`find usr/%{_lib} -type l -name 'libodbcpsql.so.*' | tail -1`
    perl -pi -e "s,usr/%{_lib}/libodbcpsql.so,$newlink,g" %{buildroot}%{_sysconfdir}/odbcinst.ini
    newlink=`find usr/%{_lib} -type l -name 'libodbcpsqlS.so.*'`
    perl -pi -e "s,usr/%{_lib}/libodbcpsqlS.so,$newlink,g" %{buildroot}%{_sysconfdir}/odbcinst.ini
popd

# drill out shared libraries for gODBCConfig *sigh*
# also drill out the Qt inst library that doesn't seem to be used at the moment
# by anyone ATM?
echo "%defattr(-,root,root)" > libodbc-libs.filelist
find %{buildroot}%{_libdir} -name '*.so.*' | sed -e "s|%{buildroot}||g" | grep -v -e gtk -e instQ >> libodbc-libs.filelist

# Uncomment the following if you wish to split off development libraries
# as well so development with ODBC does not require X11 libraries installed.
# Also you need to add in the appropriate description and filelist.
if 0; then

echo "%defattr(-, root, root)" > libodbc-devellibs.filelist
find %{buildroot}%{_libdir} -name '*.so' -o -name '*.la' -o -name '*.a' | sed -e "s|%{buildroot}||g" | grep -v -e gtk -e instQ>> libodbc-devellibs.filelist

fi

find doc -name Makefile\* -exec rm {} \;

rm -f %{buildroot}%{_bindir}/{ODBCConfig,DataManager,DataManagerII,odbctest}
rm -f %{buildroot}%{_libdir}/libodbcinstQ.so.1.0.0


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -f libodbc-libs.filelist


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files 
%defattr(-,root,root)
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/odbc*.ini
%{_bindir}/dltest
%{_bindir}/isql
%{_bindir}/odbcinst
%{_bindir}/iusql
%{_bindir}/odbc_config
	  
%files -n %{libname} -f libodbc-libs.filelist
%defattr(-,root,root)

%files -n %{libname}-devel 
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/*.a
%{_libdir}/*.la

%files doc
%defattr(-,root,root)
%doc AUTHORS INSTALL ChangeLog NEWS README doc


%changelog
* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.11
- rebuild against new readline
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.11
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.11
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.11-1avx
- 2.2.11
- built-in libtool fixes (gbeauchesne)
- define EGREP to fix 64bit builds (sbenedict)
- rebuild against new readline

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.10-3avx
- bootstrap build (new gcc, new glibc)
- drop P1 and P2; we're not building against QT

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.10-2avx
- bootstrap build

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.10-1avx
- 2.2.10
- pull out the gui pkgs completely
- correct major (1, not 2) (sbenedict)
- BuildRequires: libltdl-devel (cjw)
- remove BuildRequires: chrpath
- spec cleanups

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.2.6-9avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 2.2.6-8sls
- minor spec cleanups

* Mon Jan 12 2004 Vincent Danen <vdanen@opensls.org> 2.2.6-7sls
- remove %%build_opensls macros
- sync with 2.2.7-2mdk (sbenedict):
  - move .so symlinks back to -devel, fix /etc/odbcinst.ini to point to the
    versioned symlinks, this should satisfy Bugzilla [6769] as well as
    Anthill [15]

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 2.2.6-6sls
- sync with 5mdk (gbeauchesne): fix build on amd64
- sync with 6mdk (sbenedict): anthill bug 51 - move postgres .so symlinks to
  core lib for OOo
- sync with 7mdk (sbenedict): add explicit requires to unixODBC-gui-qt
  [Bug 6391]

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
