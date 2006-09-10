#
# spec file for package tcltk
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		tcltk
%define version		%{tclvers}
%define release		%_revrel

%define tcl_major	8.4
%define tk_major 	8.4
%define tclx_major 	8.3
%define expect_major	5.43
%define tix_major 	8.1
# Looks really broken
%define libtix_major	%{tix_major}.%{tcl_major}

%define tclvers 	%{tcl_major}.11
%define tkvers 		%{tk_major}.11
%define tclxvers	%{tclx_major}.5
%define expvers		%{expect_major}.0
%define tixvers		%{tix_major}.4
%define itclvers 	3.2.1
%define tcllibvers	1.7	

%define tcl_libname	%mklibname tcl %{tcl_major}
%define tk_libname	%mklibname tk %{tk_major}

Summary:	A Tcl/Tk development environment: tcl, tk, tix, tclX, expect, and itcl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
Source0:	http://prdownloads.sourceforge.net/tcl/tcl%{tclvers}-src.tar.bz2
Source1:	http://prdownloads.sourceforge.net/tcl/tk%{tclvers}-src.tar.bz2
Source2:	http://expect.nist.gov/src/expect-%{expvers}.tar.bz2
Source3:	http://prdownloads.sourceforge.net/tclx/tclx%{tclxvers}-src.tar.bz2
Source4:	http://prdownloads.sourceforge.net/tixlibrary/tix-%{tixvers}.tar.bz2
Source5:	http://prdownloads.sourceforge.net/incrtcl/itcl%{itclvers}_src.tar.bz2
Source6:	http://prdownloads.sourceforge.net/tcllib/tcllib-%{tcllibvers}.tar.bz2
Source40:	tclx-help.tar.bz2
Source41:	tix-8.1.3-tk8.4.tar.bz2
Patch0:		tcl-8.3.3-cruft.patch
Patch1:		tcl-8.3.3-heiierarchy.patch
Patch2:		tcl-8.3.3-makecfg.patch
Patch3:		tcl-8.3.3-refcount.patch
Patch4:		tcl-8.4.2-dlopen.patch
Patch5:		tcl8.4.5-64bit-fixes.patch
Patch10:	expect-5.32.2-random.patch
Patch11:	expect-5.42-alpha.patch
Patch12:	expect-5.32.2-kibitz.patch
Patch13:	expect-5.32.2-fixcat.patch
Patch14:	expect-5.32.2-weather.patch
Patch15:	expect-5.32.2-makecfg.patch
Patch16:	expect-5.32.2-spawn.patch
Patch17:	expect-5.32.2-expectk.patch
Patch18:	expect-5.32.2-setpgrp.patch
Patch19:	expect-5.32-libdir.patch
Patch20:	tix-8.2.0b1-perf.patch
Patch21:	tix-8.2.0b1-makecfg.patch
Patch22:	tix-8.2.0b1-dirtree.patch
Patch31:	itcl-3.2-makecfg.patch
Patch32:	itcl-3.2-no-wish-test.patch
Patch33:	itcl-3.2.1-destdir.patch
Patch40:	tclx-8.3-makecfg.patch
Patch41:	tclx-8.3-argv.patch
Patch42:	tclx-8.3-varinit.patch
Patch43:	tclx-8.3.5-nobuildhelp.patch
Patch50:	tk-8.3.3-makecfg.patch
Patch60:	tcllib-1.0-no-tclsh-test.patch
Patch61:	tcllib-1.4-mpexpard-buildin-tclsh.patch
Patch62:	tcllib-1.7-no-apps.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	XFree86-devel,  groff

%description
Tcl is a simple scripting language designed to be embedded into
other applications.  Tcl is designed to be used with Tk, a widget
set, which is provided in the tk package.  This package also includes
tclsh, a simple example of a Tcl application.


%package -n tcl
#Version: 8.0.3
Summary:	An embeddable scripting language
Group:		System/Libraries
URL:		http://www.scriptics.com

%description -n tcl
Tcl is a simple scripting language designed to be embedded into
other applications.  Tcl is designed to be used with Tk, a widget
set, which is provided in the tk package.  This package also includes
tclsh, a simple example of a Tcl application.


%package -n %{tcl_libname}
#Version: 8.0.3
Summary:	An embeddable scripting language, shared libraries
Group:		System/Libraries
URL:		http://www.scriptics.com
Conflicts:	tcl < 8.4.2-9avx

%description -n %{tcl_libname}
Tcl is a simple scripting language designed to be embedded into
other applications.  Tcl is designed to be used with Tk, a widget
set, which is provided in the tk package.  This package also includes
tclsh, a simple example of a Tcl application.



%package -n tk
#Version: 8.0.3
Summary:	Tk GUI toolkit for Tcl
Group:		System/Libraries
URL:		http://www.scriptics.com

%description -n tk
Tk is a X Windows widget set designed to work closely with the tcl
scripting language. It allows you to write simple programs with full
featured GUI's in only a little more time then it takes to write a
text based interface. Tcl/Tk applications can also be run on Windows
and Macintosh platforms.


%package -n %{tk_libname}
#Version: 8.0.3
Summary:	Tk GUI toolkit for Tcl, shared libraries
Group:		System/Libraries
URL:		http://www.scriptics.com
Conflicts:	tk < 8.4.2-9avx

%description -n %{tk_libname}
Tk is a X Windows widget set designed to work closely with the tcl
scripting language. It allows you to write simple programs with full
featured GUI's in only a little more time then it takes to write a
text based interface. Tcl/Tk applications can also be run on Windows
and Macintosh platforms.


%package -n expect
#Version: %{expvers}
Summary:	A tcl extension for simplifying program-script interaction
Group:		System/Libraries
Requires:	tcl

%description -n expect
Expect is a tcl extension for automating interactive applications such
as telnet, ftp, passwd, fsck, rlogin, tip, etc.  Expect is also useful
for testing the named applications.  Expect makes it easy for a script
to control another program and interact with it.



%package -n tclx
#Version: %{tclXvers}
Summary:	Tcl/Tk extensions for POSIX systems
Group:		System/Libraries
URL:		http://www.neosoft.com/

%description -n tclx
TclX is a set of extensions which make it easier to use the Tcl
scripting language for common UNIX/Linux programming tasks.  TclX
enhances Tcl support for files, network access, debugging, math, lists,
and message catalogs.  TclX can be used with both Tcl and Tcl/Tk
applications.


%package -n tix
#Version: %{Tixvers}.6
Summary:	A set of capable widgets for Tk
Group:		System/Libraries

%description -n tix
Tix (Tk Interface Extension), an add-on for the Tk widget set, is an
extensive set of over 40 widgets.  In general, Tix widgets are more
complex and more capable than the widgets provided in Tk.  Tix widgets
include a ComboBox, a Motif-style FileSelectBox, an MS Windows-style
FileSelectBox, a PanedWindow, a NoteBook, a hierarchical list, a
directory tree and a file manager.


%package -n itcl
#Version: %{itclvers}
Summary:	object-oriented extension of the Tcl language
Group:		System/Libraries

%description -n itcl
[incr Tcl] is an object-oriented extension of the Tcl language.  It
was created to support more structured programming in Tcl.  Tcl scripts
that grow beyond a few thousand lines become extremely difficult to
maintain.  This is because the building blocks of vanilla Tcl are
procedures and global variables, and all of these building blocks
must reside in a single global namespace.  There is no support for
protection or encapsulation.

[incr Tcl] introduces the notion of objects.  Each object is a bag
of data with a set of procedures or "methods" that are used to
manipulate it.  Objects are organized into "classes" with identical
characteristics, and classes can inherit functionality from one
another.  This object-oriented paradigm adds another level of
organization on top of the basic variable/procedure elements, and
the resulting code is easier to understand and maintain.


%package -n tcllib
#Version: %{tcllibvers}
Summary:	Library of utility modules for tcl
Group:		Development/Other

%description -n tcllib
Tcllib is a collection of utility modules for tcl. These modules provide
a wide variety of functionality,  from implementation  of standard data
structures  to implementation of common networking protocols.  the intent
is to collect commoly used function into a single library, which users can 
rely on to be available  and stable.

%prep
%setup -q -c -a 1 -a 2 -a 3 -a 4 -a 5 -a 6

cd tcl%{tclvers}
#%patch0 -p1 -b .cruft
#%patch1 -p1 -b .heiiearchy
#%patch2 -p1 -b .makecfg
#%patch3 -p1 -b .refcount
%patch4 -p1 -b .dlopen
#%patch5 -p1 -b .64bit-fixes
cd ..

# cruft. ugh
ln -s tcl%{tclvers} tcl%{tcl_major}

cd expect-%{expect_major}
%patch10 -p1 -b .random
#%patch11 -p1 -b .alpha
#%patch12 -p1 -b .kibitz
%patch13 -p1 -b .fixcat
#%patch14 -p1 -b .weather
#%patch15 -p1 -b .makecfg
%patch16 -p1 -b .spawn
#%patch17 -p1 -b .expectk
%patch18 -p2
%patch19 -p1 -b .libdir
cd ..

cd itcl%{itclvers}
#%patch31 -p1 -b .makecfg
%patch32 -p1 -b .nowish
%patch33 -p1 -b .libdir
cd ..

cd tclx%{tclxvers}
#%patch40 -p1 -b .makecfg
#%patch41 -p1 -b .argv
%patch42 -p1 -b .varinit
%patch43 -p1 -b .buildhelp
cd ..

cd tk%{tkvers}
#%patch50 -p1 -b .makecfg
cd ..

cd tcllib-%{tcllibvers}
%patch60 -p1 -b .tclsh
%patch61 -p1 -b .buildin_tclsh
%patch62 -p1 -b .no-apps
cd ..

cd tix-%{tixvers}
cd ..


#==========================================
%build
for f in config.guess config.sub ; do
    test -f /usr/share/libtool/$f || continue
    find . -type f -name $f -exec cp /usr/share/libtool/$f \{\} \;
done

# Drill out rpath.
cat << EOF > rmrpath.sh
#!/bin/sh
find \$1 -name 'Makefile' -exec perl -pi -e 's|-Wl,-rpath,.*%{_lib}||g' {} \;
find \$1 -name 'Makefile' -exec perl -pi -e 's|-Wl,-rpath,\\$\{.*\}||g' {} \;

EOF
chmod +x rmrpath.sh
scriptpath=$(pwd)
%define rmrpath $scriptpath/rmrpath.sh $(pwd)


#------------------------------------------
# Tcl
#
cd tcl%{tclvers}/unix
%configure \
    --enable-gcc \
    --enable-64bit
%rmrpath
make
cd ../..

#------------------------------------------
# Tk
#
cd tk%{tkvers}/unix
%configure \
    --enable-gcc \
    --with-tcl=../../tcl%{tclvers}/unix \
    --enable-64bit \
    --with-x
%rmrpath
make
cd ../..

#------------------------------------------
# tclX
#
cd tclx%{tclxvers}/unix
# (couriousous) Force detection of clock_t type.
# configure script check in the wrong header ( sys/types.h instead of sys/times.h )
perl -pi -e "s|ac_cv_type_clock_t=no|ac_cv_type_clock_t=yes|" configure
%configure \
    --enable-tk=YES \
    --with-tcl=../../tcl%{tclvers}/unix \
    --with-tk=../../tk%{tkvers}/unix \
    --enable-gcc \
    --enable-64bit
%rmrpath
find . -name 'Common.mk' -exec perl -pi -e 's|-Wl,-rpath,\$\{.*\}||g' {} \;
make
cd ../..

#------------------------------------------
# Expect
#
cd expect-%{expect_major}
chmod u+w testsuite/configure
%configure \
    --with-tclconfig=../tcl%{tclvers}/unix \
    --with-tkconfig=../tk%{tclvers}/unix \
    --with-tclinclude=../tcl%{tclvers}/generic \
    --enable-shared \
    --with-x=yes \
    --with-tkinclude=../tk%{tclvers}/generic \
    --enable-gcc
%rmrpath
make
cd ..

#------------------------------------------
# Itcl
#
cd itcl%{itclvers}
# For patch33 we have to run autoconf.
(cd itcl; rm -f configure; autoconf)
# For patch32 we have to run autoconf.
(cd itk; rm -f configure; autoconf)
# FIXME: probably need to run autoconfig for iwidgets* too
%configure \
    --enable-gcc \
    --with-tcl=../../tcl%{tclvers}/unix \
    --with-tk=../../tk%{tkvers}/unix \
    --enable-shared
%rmrpath
make
cd ..

#------------------------------------------
# Tix
#
cd tix-%{tixvers}/unix
%configure \
    --enable-gcc \
    --with-tcl=../../tcl%{tclvers}/unix \
    --with-tk=../../tk%{tkvers}/unix

tar xjf %{SOURCE41}
cd tk%{tk_major}
%configure \
    --enable-shared
%rmrpath
make
cd ..
cd ../..

#------------------------------------------
# tcllib
#
cd tcllib-%{tcllibvers}
autoconf
%configure
%rmrpath
make TCLSH_PROG=../tcl%{tclvers}/unix/tclsh LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{_builddir}/%{name}-%{version}/tcl%{tclvers}/unix
cd ../..


#==========================================

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}
rm -f *.files

# If %{_libdir} is not %{_prefix}/lib, then define EXTRA_TCLLIB_FILES
# which contains actual non-architecture-dependent tcl code.
if [ "%{_libdir}" != "%{_prefix}/lib" ]; then
    EXTRA_TCLLIB_FILES="%{buildroot}%{_prefix}/lib/*"
fi

# JMD: some .h files are missing, include them
for dirs in tcl%{tclvers}/unix tcl%{tclvers}/generic tcl%{tclvers}/compat tk%{tkvers}/unix \
  tk%{tkvers}/generic tk%{tkvers}/compat tclx%{tclxvers}/tcl/generic tclx%{tclxvers}/tcl/unix \
  tix-%{tixvers}/generic tix-%{tixvers}/unix itcl%{itclvers}/itcl/generic \
  itcl%{itclvers}/itk/generic; do
    mkdir -p $RPM_BUILD_ROOT/%{_includedir}/$dirs
    cp $dirs/*.h $RPM_BUILD_ROOT/%{_includedir}/$dirs
done

#------------------------------------------
# Helper functions to generate ld scripts
#

function GenerateLinkerScript() {
name=$1 major=$2
cat > lib${name}.so << EOF
/* GNU ld script
   We want -l${name} to include the actual system library,
   which is lib${name}${major}.so.  */
INPUT ( -l${name}${major} )
EOF
}

#------------------------------------------
# Tcl
#
cd tcl%{tclvers}/unix
%makeinstall
cd ../..

pushd %{buildroot}%{_bindir}
    ln -fs tclsh* tclsh
popd

pushd %{buildroot}%{_libdir}
    GenerateLinkerScript tcl %{tcl_major}
popd

echo "%%defattr(-,root,root)" > tcl.files
(find %{buildroot}%{_bindir} %{buildroot}%{_includedir} \
    %{buildroot}%{_mandir} -type f -o -type l;
 find %{buildroot}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
    | sort | uniq -u >> tcl.files


#------------------------------------------
# Tk
#
cd tk%{tkvers}/unix
%makeinstall
cd ../..

pushd %{buildroot}%{_bindir}
    ln -sf wish* wish
popd

pushd %{buildroot}%{_libdir}
    GenerateLinkerScript tk %{tk_major}
popd

echo "%%defattr(-,root,root)" > tk.files
(find %{buildroot}%{_bindir} %{buildroot}%{_includedir} \
    %{buildroot}%{_mandir} -type f -o -type l;
 find %{buildroot}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
    | sort | uniq -u >> tk.files

#------------------------------------------
# TclX
#

cd tclx%{tclxvers}/unix
%makeinstall \
    TCLX_INST_LIB=%{buildroot}%{_libdir} \
    TKX_INST_LIB=%{buildroot}%{_libdir}
cd ../..

bzip2 -dc %SOURCE40 | tar -C %{buildroot} -xf -

if [ "%{_mandir}" = "%{_prefix}/share/man" ]; then
    ( cd %{buildroot}%{_prefix}/man; tar cf - ./man[13n] ) | 
    ( cd %{buildroot}%{_mandir}; tar xf - )
    ( cd %{buildroot}%{_prefix}/man; rm -rf ./man[13n] )
fi

echo "%%defattr(-,root,root)" > tclx.files
(find %{buildroot}%{_bindir} %{buildroot}%{_includedir} \
    %{buildroot}%{_mandir} -type f -o -type l;
 find %{buildroot}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
    | sort | uniq -u >> tclx.files

#------------------------------------------
# Expect
#
cd expect-%{expect_major}
%makeinstall tcl_libdir=%{buildroot}%{_libdir} \
    libdir=%{buildroot}%{_libdir}/expect%{expect_major} \
    TKLIB_INSTALLED="-L%{buildroot}%{_libdir} -ltk%{tk_major}" \
    TCLLIB_INSTALLED="-L%{buildroot}%{_libdir} -ltcl%{tcl_major}"
cd ..

# remove cryptdir/decryptdir, as Linux has no crypt command (bug 6668).
rm -f %{buildroot}%{_bindir}/{cryptdir,decryptdir}
rm -f %{buildroot}%{_mandir}/man1/{cryptdir,decryptdir}.1*

echo "%%defattr(-,root,root)" > expect.files
(find %{buildroot}%{_bindir} %{buildroot}%{_includedir} \
    %{buildroot}%{_mandir} -type f -o -type l;
 find %{buildroot}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
    | sort | uniq -u >> expect.files

set +x +H
for n in `cat expect.files`; do
    test -f $n || continue
    head -1 $n | grep -q ^#! || continue
    chmod u+w $n
    perl -pi -e "s|%{buildroot}||" $n
done
set -x -H

#------------------------------------------
# Tix
#
cd tix-%{tixvers}/unix
%makeinstall datadir=%{buildroot}%{_prefix}/lib \
    LIB_DIR=%{buildroot}%{_libdir} \
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{_builddir}/%{name}-%{version}/tcl%{tclvers}/unix
cd ../..

# Not needed anymore?
rm -rf %{buildroot}%{_libdir}/libtixsam*

# aesthetic: make libtix*.so executable
chmod +x %{buildroot}%{_libdir}/libtix*.so

pushd %{buildroot}%{_bindir}
    ln -s tixwish%{libtix_major} tixwish
popd

if [ "%{_mandir}" = "%{_prefix}/share/man" ]; then
    ( cd %{buildroot}%{_prefix}/man; tar cf - ./man[13n] ) | 
    ( cd %{buildroot}%{_mandir}; tar xf - )
    ( cd %{buildroot}%{_prefix}/man; rm -rf ./man[13n] )
fi

# tixwish.1 in /usr/share/man/man1.
mv %{buildroot}/usr/share/man/mann/tixwish.1 \
    %{buildroot}/usr/share/man/man1
	
echo "%%defattr(-,root,root)" > tix.files
(find %{buildroot}%{_bindir} %{buildroot}%{_includedir} \
    %{buildroot}%{_mandir} -type f -o -type l;
 find %{buildroot}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
    | sort | uniq -u >> tix.files

#------------------------------------------
# Itcl
#
cd itcl%{itclvers}
%makeinstall TCLSH_PROG=../../tcl%{tclvers}/unix/tclsh \
    LD_LIBRARY_PATH=../../tcl%{tclvers}/unix \
    SHLIB_LDFLAGS="-L../../tcl%{tclvers}/unix -ltclstub%{tcl_major}"
cd ..

if [ "%{_mandir}" = "%{_prefix}/share/man" ]; then
    ( cd %{buildroot}%{_prefix}/man; tar cf - ./man[13n] ) | 
    ( cd %{buildroot}%{_mandir}; tar xf - )
    ( cd %{buildroot}%{_prefix}/man; rm -rf ./man[13n] )
fi

echo "%%defattr(-,root,root)" > itcl.files
(find %{buildroot}%{_bindir} %{buildroot}%{_includedir} \
    %{buildroot}%{_mandir} -type f -o -type l;
 find %{buildroot}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
    | sort | uniq -u >> itcl.files

set +x +H
for n in `cat itcl.files`; do
    [ -f $n ] || continue
    head -1 $n | grep -q ^#! || continue
    chmod u+w $n
    perl -pi -e "s|%{buildroot}||" $n
done
set -x -H

#------------------------------------------
# Tcllib
#
cd tcllib-%{tcllibvers}
%makeinstall TCLSH_PROG=../tcl%{tclvers}/unix/tclsh \
    LD_LIBRARY_PATH="../tcl%{tclvers}/unix" 
cd ..

if [ "%{_mandir}" = "%{_prefix}/share/man" ]; then
    ( cd %{buildroot}%{_prefix}/man; tar cf - ./man[13n] ) | 
    ( cd %{buildroot}%{_mandir}; tar xf - )
    ( cd %{buildroot}%{_prefix}/man; rm -rf ./man[13n] )
fi

echo "%%defattr(-,root,root)" > tcllib.files
(find %{buildroot}%{_bindir} %{buildroot}%{_includedir} \
    %{buildroot}%{_mandir} -type f -o -type l;
 find %{buildroot}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
    | sort | uniq -u >> tcllib.files

#------------------------------------------
# post process the *.files list, removing build sys references and mark
# which are directories

set +x
for n in *.files; do
    mv $n $n.in
    sed "s|.*%{_prefix}\\>|%{_prefix}|" < $n.in | while read file; do
        if [ -d %{buildroot}/$file ]; then
            echo -n '%dir '
        fi
        echo $file
    done > $n
    rm -f $n.in
done
set -x

# Man pages can be compressed
perl -pi -e 's|(^%{_mandir}/man.*$)|\1\*|' *.files

perl -pi -e "s|%{_builddir}/tcltk-%{version}/tcl%{version}/unix|%{_includedir}|" %{buildroot}/%{_libdir}/*.sh
perl -pi -e "s|%{_builddir}/tcltk-%{version}/tk%{version}/unix|%{_includedir}|" %{buildroot}/%{_libdir}/*.sh
perl -pi -e "s|%{_builddir}/tcltk-%{version}/tclx%{tclXvers}/unix|%{_includedir}|" %{buildroot}/%{_libdir}/*.sh
perl -pi -e "s|%{_builddir}/tcltk-%{version}/tkx%{version}/unix|%{_includedir}|" %{buildroot}/%{_libdir}/*.sh
perl -pi -e "s|-L/usr/include|-L/usr/lib|g" %{buildroot}/%{_libdir}/*.sh

# (gb) FIXME: libdir patches are not good enough :-(
perl -pi -e "s|-L/usr/lib\b|-L%{_libdir}|g" %{buildroot}%{_libdir}/*.sh
perl -pi -e "s|/usr/lib/lib|%{_libdir}/lib|g" %{buildroot}%{_libdir}/*.sh

# JMD: nuke buildroot from config scripts
perl -pi -e "s|$RPM_BUILD_DIR/tcltk-%{version}|%{_includedir}|g" \
    $RPM_BUILD_ROOT%{_libdir}/tclConfig.sh \
    $RPM_BUILD_ROOT%{_libdir}/tkConfig.sh
perl -pi -e "s|$RPM_BUILD_DIR/tcltk-%{version}|%{_libdir}|g" \
    $RPM_BUILD_ROOT%{_libdir}/*.sh

# All file lists are processed, cleanup for libified files
cp -p tcl.files tcl.files.orig
cp -p tk.files tk.files.orig
perl -ni -e "m,^%{_libdir}/lib.+\d\.so, or print" tcl.files tk.files

# Arrangements for lib64 platforms
if [[ "%{_lib}" != "lib" ]]; then
    ln -s %{_libdir}/tclConfig.sh $RPM_BUILD_ROOT%{_prefix}/lib/tclConfig.sh
    echo "%{_prefix}/lib/tclConfig.sh" >> tcl.files
    ln -s %{_libdir}/tkConfig.sh  $RPM_BUILD_ROOT%{_prefix}/lib/tkConfig.sh
    echo "%{_prefix}/lib/tkConfig.sh"  >> tk.files
fi

# (fc) make sure .so files are writable by root
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/*.so


#==========================================
%post -p /sbin/ldconfig -n %{tcl_libname}
%post -p /sbin/ldconfig -n %{tk_libname}
%post -p /sbin/ldconfig -n expect
%post -p /sbin/ldconfig -n tclx
%post -p /sbin/ldconfig -n tix
%post -p /sbin/ldconfig -n itcl
%post -p /sbin/ldconfig -n tcllib

%postun -p /sbin/ldconfig -n %{tcl_libname}
%postun -p /sbin/ldconfig -n %{tk_libname}
%postun -p /sbin/ldconfig -n expect
%postun -p /sbin/ldconfig -n tclx
%postun -p /sbin/ldconfig -n tix
%postun -p /sbin/ldconfig -n itcl
%postun -p /sbin/ldconfig -n tcllib


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -f *.files


%files -f tcl.files -n tcl
%files -f tk.files -n tk
%files -f tclx.files -n tclx
%files -f expect.files -n expect
%files -f tix.files -n tix
%files -f itcl.files -n itcl
%files -f tcllib.files -n tcllib

%files -n %{tcl_libname}
%defattr(-,root,root)
%{_libdir}/libtcl*[0-9].so

%files -n %{tk_libname}
%defattr(-,root,root)
%{_libdir}/libtk*[0-9].so


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.4.11
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.4.11
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.4.11
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.4.11-1avx
- 8.4.11 (synced with mandrake 8.4.11-1mdk)
  - tcl/tk-8.4.11
  - expect-5.43.0
  - tclx-8.3.5
  - tix-8.1.4
  - itcl-3.2.1
  - tcllib-1.7
- expect requires tcl
- conflicts to ease upgrade
- add missing .h files (jmd)
- nuke buildroot from config files (jmd)

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.4.2-9avx
- rebuild against the xorg libs

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.4.2-8avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.4.2-7avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.4.2-6avx
- bootstrap build

* Mon Aug 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 8.4.2-5avx
- fix dangling symlink (tixwish)

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 8.4.2-4avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 8.4.2-3sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 8.4.2-2sls
- OpenSLS build
- tidy spec

* Mon Apr 07 2003 Nicolas Planel <nplanel@mandrakesoft.com> 8.4.2-1mdk
- 8.4.2.
- Remove patch 0,1,2,3 and tcl-encoding source.

* Sat Aug 10 2002 Stefan van der Eijk <stefan@eijk.nu> 8.3.3-21mdk
- BuildRequires

* Fri Jun 28 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 8.3.3-20mdk
- Patch19: Use $(libdir), not $(exec_prefix)/lib for libexpect install
- Patch33: Link libitk and libitcl against stub libs from built sources

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 8.3.3-19mdk
- Automated rebuild in gcc3.1 environment

* Fri May  3 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 8.3.3-18mdk
- Provide ld scripts for libtcl.so and libtk.so. This is temporary so
  that -ltcl actually grabs libtcl%{tcl_major}.so and until upstream
  conventions are fixed or until this package is libified with correct
  SONAMEs.

* Mon Apr 29 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-17mdk
- Last bits of build-without-tcl fixes in.

* Mon Apr 29 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-16mdk
- Bug reports and fixes from Ural Khassanov:
- Put expect pkgIndex.tcl in /usr/lib/expect5.32.
- Put tixwish.1 manpage in /usr/share/man/man1.
- Install /usr/lib/tix8.1/*.
- Don't require tcl in tcllib configure.
- Don't require tcl in itcl make install.

* Wed Apr 24 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-15mdk
- Rebuild to fix screwed expect package.

* Mon Apr 22 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-14mdk
- Remove the libtcl.so link (David please read my previous changelog 
  comment aboiut this one!!)
- Don't check for wish in itk configure -- breaks build if wish not 
  previously installed (Gwenole).
  
* Fri Mar 22 2002 David BAUDENS <baudens@mandrakesoft.com> 8.3.3-13mdk
- Re-add %%{_libdir}/libtcl.so

* Thu Feb 28 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-12mdk
- Really remove the versionless soft links for good -- the linker does 
  not how to follow the soft links to the actual versioned libraries,
  programs should not be able to take advantage of this to create linking
  to a versionless tcl.
  
* Thu Feb 28 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-11mdk
- Add versionless soft links to the libraries -- note this does *not* 
  mean or give you an excuse to link versionless with the tcl libraries.
- Remove the ugly buildroot from the .sh configuration files which was
  lost during the RH merge.

* Wed Feb 27 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-10mdk
- Sync with RH.

* Thu Nov 15 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-9mdk
- Drill out all the rpath.

* Tue Oct 09 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-8mdk
- Define _GNU_SOURCE for expect to make it work on the ia64.

* Fri Sep 14 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-7mdk
- Make tixindex executable.

* Fri Sep 14 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-6mdk
- Finally get this stuff to build (broke for a long time). :/

* Sat May 26 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-5mdk
- Add back the symbolic link for libtixsam, I figure that it can't hurt.
- chmod +x /usr/bin/tixindex.
- Fix the dangling symlinks from the old .so version and update it to the
  new one.
- Don't compile Tix with -fwritable-strings anymore.

* Fri May 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-4mdk
- Strap yourselves for the ride of the century boys and gals a.k.a.
  compile a tix 8.1.1 and break things.
- Add updated tcl encodings kindly provided by Markus Kuhn.

* Tue Apr 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-3mdk
- Fix broken itcl configure script and put wish (from tk) in the tcl
  directory so our dear configure script does not fail a.k.a. fix
  a bootstrapping problem (Abel Cheung maddog@linuxhall.org).

* Mon Apr 16 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-2mdk
- itcl is really broke, add back:
  libitclstub static library;
  libitkstub static library which were not installed by the Makefile.

* Tue Apr 10 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.3-1mdk
- Strap on your seatbelt:
   - Tcl /Tk 8.3.3.
   - Tcllib 0.8.
   - TclX 8.3.
   - Itcl 3.2.
- Give $RPM_OPT_FLAGS for Tcl.
- Work around a TclX helpdir problem.

* Mon Dec 11 2000 Vincent Saugey <vince@mandrakesoft.com> 8.3.2-7mdk
- Add buildrequires (groff)

* Mon Nov 27 2000 Geoffrey LEE <snailtalk@mandrakesoft.com> 8.3.2-6mdk
- use RPM_OPT_FLAGS to build tcl. (Dadou.)

* Thu Oct 13 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.2-5mdk
- fix the *.sh configuration files. (gc)

* Fri Sep 15 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.2-4mdk
- remove symlink to libtixsam.so

* Sun Sep 03 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.2-3mdk
- merge with redhat's patches.

* Thu Aug 17 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.2-2mdk
- fix a silly typo.

* Thu Aug 10 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.2-1mdk
- tcl and tk: s|8.3.1|8.3.2|.
- tcllib: s|0.4|0.6|.

* Sun Aug 06 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.1-6mdk
- remove the patch from the original version and use -fwritable-strings to 
  compile (Jeff Johnson)

* Sat Aug 05 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.1-5mdk
- patch to fix tixwish (Vladimir, orig patch by Carlos Vidal)
- add symlink for tix 

* Tue Aug 01 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.1-4mdk
- fix the broken symlink created while i was mascroising stuff

* Tue Aug 01 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.1-3mdk
- rebuild to fix up problem with /us/bin/wish symlink

* Sat Jul 29 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.1-2mdk
- rebuild and remove the individual versioning: we don't want to make 
  updates impossible, or the upload robots to reject the RPM .. :-(

* Wed Jul 26 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.3.1-1mdk
- major upgrade for this big SOB
- fix building - do not link with the ieee library (chmouel)

* Wed May 17 2000 Vicnent Saugey <vince@mandrakesoft.com> 8.0.5-20mdk
- Add patch for signal -> now build correctly on sparc

* Wed May 10 2000 Frederic Lepied <flepied@mandrakesoft.com> 8.0.5-19mdk
- fixed tclx broken symlinks.

* Fri Mar 31 2000 Frederic Lepied <flepied@mandrakesoft.com> 8.0.5-18mdk
- fix groups.

* Mon Jan 24 2000 Frederic Lepied <flepied@mandrakesoft.com> 8.0.5-17mdk
- bzipped man pages.
- remove rm -f from previous release to not loose permissions.

* Wed Jan 12 2000 Pixel <pixel@mandrakesoft.com>
- fix build as non-root
- added some rm -f cuz rights pb

* Sun Nov 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- bzip2 tixwish manpage.

* Sun Nov 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Increase release for compatibility with expect.

* Wed Nov  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 8.0.5.

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- fix handling of RPM_OPT_FLAGS and reentrance

* Thu Apr  8 1999 Jeff Johnson <jbj@redhat.com>
- use /usr/bin/write in kibitz (#1320).
- use cirrus.sprl.umich.edu in weather (#1926).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 28)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- whoops, exec-prefix for itcl was set to '/foo', changed to '/usr'.

* Tue Feb 16 1999 Jeff Johnson <jbj@redhat.com>
- expect does unaligned access on alpha (#989)
- upgrade tcl/tk/tclX to 8.0.4
- upgrade expect to 5.28.
- add itcl 3.0.1

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to allow building on the arm
- build for glibc 2.1
- strip binaries

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update tcl/tk/tclX to 8.0.3, expect is updated also.

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- expect: mkpasswd needs delay before sending password (problem #576)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- fixed expect binaries exec permissions

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- updated to Tix 4.1.0.006
- updated version numbers of tcl/tk to relflect includsion of p2

* Wed Mar 25 1998 Cristian Gafton <gafton@redhat.com>
- updated tcl/tk to patch level 2
- updated tclX to 8.0.2

* Thu Oct 30 1997 Otto Hammersmith <otto@redhat.com>
- fixed filelist for tix... replacing path to the expect binary in scripts
  was leaving junk files around.

* Wed Oct 22 1997 Otto Hammersmith <otto@redhat.com>
- added patch to remove libieee test in configure.in for tcl and tk.
  Shoudln't be needed anymore for glibc systems, but this isn't the "proper" 
  solution for all systems
- fixed src urls

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- removed version numbers from descriptions

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- updated to tcl/tk 8.0 and related versions of packages

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- fixed dangling tclx/tkx symlinks

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
