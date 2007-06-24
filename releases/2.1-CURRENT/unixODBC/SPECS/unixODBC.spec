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
%define devname		%mklibname %{name} -d
%define odevname	%mklibname %{name} 1 -d

Summary: 	Unix ODBC driver manager and database drivers
Name: 		%{name}
Version: 	%{version}
Release:	%{release}
Group: 		Databases
License: 	LGPL
URL: 		http://www.unixODBC.org
Source0: 	http://www.unixodbc.org/%{name}-%{version}.tar.bz2
Source2:	odbcinst.ini
Source3:	qt-attic.tar.bz2
Source4:	qt-attic2.tar.bz2
Patch0:		unixODBC-2.2.6-lib64.patch
Patch1:		unixODBC-2.2.11-libtool.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
# don't take away readline, we do want to build unixODBC with readline.
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	readline-devel
BuildRequires:	libltdl-devel
BuildRequires:	automake1.7
BuildRequires:	autoconf2.5 >= 2.52

%description
UnixODBC is a free/open specification for providing application developers 
with a predictable API with which to access Data Sources. Data Sources include 
SQL Servers and any Data Source with an ODBC Driver.


%package -n %{libname}
Summary:	Libraries unixODBC 
Group:		System/Libraries

%description -n %{libname}
unixODBC libraries.


%package -n %{devname}
Summary: 	Includes and static libraries for ODBC development
Group: 		Development/Other
Requires: 	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	libodbc.so
Provides:	libodbcinst.so
Obsoletes:	%{name}-devel
Obsoletes:	%{odevname}

%description -n %{devname}
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

install -m 0644 %{_sourcedir}/odbcinst.ini %{buildroot}%{_sysconfdir}/
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

%files -n %{devname} 
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/*.a
%{_libdir}/*.la

%files doc
%defattr(-,root,root)
%doc AUTHORS INSTALL ChangeLog NEWS README doc


%changelog
* Sun Jun 24 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.11
- rebuild against new readline
- implement devel naming policy
- implement library provides policy

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
