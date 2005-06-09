%define name	tcltk
%define version	%{tclvers}
%define release	6avx

%define tcl_major	8.4
%define tk_major 	8.4
%define tclx_major 	8.3
%define expect_major	5.38
%define tix_major 	8.1
# Looks really broken
%define libtix_major	%{tix_major}.%{tcl_major}

%define tclvers 	%{tcl_major}.2
%define tkvers 		%{tk_major}.2
%define tclxvers	%{tclx_major}
%define expvers		%{expect_major}.0
%define tixvers		%{tix_major}.4
%define itclvers 	3.2
%define tcllibvers	1.3	


Summary:	A Tcl/Tk development environment: tcl, tk, tix, tclX, expect, and itcl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
Source0:	ftp://tcl.activestate.com/pub/tcl/tcl8_4/tcl%{tclvers}-src.tar.bz2
Source1:	ftp://tcl.activestate.com/pub/tcl/tcl8_4/tk%{tclvers}-src.tar.bz2
Source2:	ftp://tcl.activestate.com/pub/tcl/expect/expect-%{expvers}.tar.bz2
Source3:	ftp://tcl.activestate.com/pub/tcl/tclx/tclx%{tclxvers}.tar.bz2
Source4:	http://prdownloads.sourceforge.net/tixlibrary/tix-%{tixvers}.tar.bz2
Source5:	ftp://tcl.activestate.com/pub/tcl/itcl/itcl%{itclvers}.tar.bz2
Source6:	http://prdownloads.sourceforge.net/tcllib/tcllib-%{tcllibvers}.tar.bz2
Source40:	tclx-help.tar.bz2
Source41:	tix-8.1.3-tk8.4.tar.bz2
Patch0:		tcl-8.3.3-cruft.patch.bz2
Patch1:		tcl-8.3.3-heiierarchy.patch.bz2
Patch2:		tcl-8.3.3-makecfg.patch.bz2
Patch3:		tcl-8.3.3-refcount.patch.bz2
Patch4:		tcl-8.4.2-dlopen.patch.bz2
Patch10:	expect-5.32.2-random.patch.bz2
Patch11:	expect-5.32.2-alpha.patch.bz2
Patch12:	expect-5.32.2-kibitz.patch.bz2
Patch13:	expect-5.32.2-fixcat.patch.bz2
Patch14:	expect-5.32.2-weather.patch.bz2
Patch15:	expect-5.32.2-makecfg.patch.bz2
Patch16:	expect-5.32.2-spawn.patch.bz2
Patch17:	expect-5.32.2-expectk.patch.bz2
Patch18:	expect-5.32.2-setpgrp.patch.bz2
Patch19:	expect-5.32-libdir.patch.bz2
Patch20:	tix-8.2.0b1-perf.patch.bz2
Patch21:	tix-8.2.0b1-makecfg.patch.bz2
Patch22:	tix-8.2.0b1-dirtree.patch.bz2
Patch30:	itcl-3.2-symlink.patch.bz2
Patch31:	itcl-3.2-makecfg.patch.bz2
Patch32:	itcl-3.2-no-wish-test.patch.bz2
Patch33:	itcl-3.2-libdir.patch.bz2
Patch40:	tclx-8.3-makecfg.patch.bz2
Patch41:	tclx-8.3-argv.patch.bz2
Patch42:	tclx-8.3-varinit.patch.bz2
Patch43:	tclx-8.3-nobuildhelp.patch.bz2
Patch50:	tk-8.3.3-makecfg.patch.bz2
Patch60:	tcllib-1.0-no-tclsh-test.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	XFree86-devel,  groff

%description
Tcl is a simple scripting language designed to be embedded into
other applications.  Tcl is designed to be used with Tk, a widget
set, which is provided in the tk package.  This package also includes
tclsh, a simple example of a Tcl application.

%package -n tcl
#Version: 8.0.3
Summary:	An embeddable scripting language.
Group:		System/Libraries
URL:		http://www.scriptics.com

%description -n tcl
Tcl is a simple scripting language designed to be embedded into
other applications.  Tcl is designed to be used with Tk, a widget
set, which is provided in the tk package.  This package also includes
tclsh, a simple example of a Tcl application.

If you're installing the tcl package and you want to use Tcl for
development, you should also install the tk and tclx packages.

%package -n tk
#Version: 8.0.3
Summary:	Tk GUI toolkit for Tcl, with shared libraries
Group:		System/Libraries
URL:		http://www.scriptics.com

%description -n tk
Tk is a X Windows widget set designed to work closely with the tcl
scripting language. It allows you to write simple programs with full
featured GUI's in only a little more time then it takes to write a
text based interface. Tcl/Tk applications can also be run on Windows
and Macintosh platforms.

%package -n expect
#Version: %{expvers}
Summary:	A tcl extension for simplifying program-script interaction.
Group:		System/Libraries

%description -n expect
Expect is a tcl extension for automating interactive applications such
as telnet, ftp, passwd, fsck, rlogin, tip, etc.  Expect is also useful
for testing the named applications.  Expect makes it easy for a script
to control another program and interact with it.

Install the expect package if you'd like to develop scripts which interact
with interactive applications.  You'll also need to install the tcl
package.

%package -n tclx
#Version: %{tclXvers}
Summary:	Tcl/Tk extensions for POSIX systems.
Group:		System/Libraries
URL:		http://www.neosoft.com/

%description -n tclx
TclX is a set of extensions which make it easier to use the Tcl
scripting language for common UNIX/Linux programming tasks.  TclX
enhances Tcl support for files, network access, debugging, math, lists,
and message catalogs.  TclX can be used with both Tcl and Tcl/Tk
applications.

Install TclX if you are developing applications with Tcl/Tk.  You'll
also need to install the tcl and tk packages.

%package -n tix
#Version: %{Tixvers}.6
Summary:	A set of capable widgets for Tk.
Group:		System/Libraries

%description -n tix
Tix (Tk Interface Extension), an add-on for the Tk widget set, is an
extensive set of over 40 widgets.  In general, Tix widgets are more
complex and more capable than the widgets provided in Tk.  Tix widgets
include a ComboBox, a Motif-style FileSelectBox, an MS Windows-style
FileSelectBox, a PanedWindow, a NoteBook, a hierarchical list, a
directory tree and a file manager.

Install the tix package if you want to try out more complicated widgets
for Tk.  You'll also need to have the tcl and tk packages installed.

%package -n itcl
#Version: %{itclvers}
Summary:	object oriented mega widgets for tcl
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
Summary:	Library of utility modules for tcl.
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
cd ..

# cruft. ugh
ln -s tcl%{tclvers} tcl%{tcl_major}

cd expect-%{expect_major}
%patch10 -p1 -b .random
%patch11 -p1 -b .alpha
%patch12 -p1 -b .kibitz
%patch13 -p1 -b .fixcat
%patch14 -p1 -b .weather
#%patch15 -p1 -b .makecfg
%patch16 -p1 -b .spawn
%patch17 -p1 -b .expectk
%patch18 -p2
%patch19 -p1 -b .libdir
cd ..

cd itcl%{itclvers}
%patch30 -p1 -b .symlink
#%patch31 -p1 -b .makecfg
%patch32 -p1 -b .nowish
%patch33 -p1 -b .libdir
cd ..

cd tclx%{tclx_major}
#%patch40 -p1 -b .makecfg
%patch41 -p1 -b .argv
%patch42 -p1 -b .varinit
%patch43 -p1 -b .buildhelp
cd ..

cd tk%{tkvers}
#%patch50 -p1 -b .makecfg
cd ..

cd tcllib-%{tcllibvers}
%patch60 -p1 -b .tclsh
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
%configure --enable-gcc --enable-64bit
%rmrpath
make
cd ../..

#------------------------------------------
# Tk
#
cd tk%{tkvers}/unix
%configure --enable-gcc --with-tcl=../../tcl%{tclvers}/unix --enable-64bit --with-x
%rmrpath
make
cd ../..

#------------------------------------------
# tclX
#
cd tclx%{tclx_major}/unix
%configure --enable-tk=YES --with-tcl=../../tcl%{tclvers}/unix --with-tk=../../tk%{tkvers}/unix --enable-gcc --enable-64bit
%rmrpath
find . -name 'Common.mk' -exec perl -pi -e 's|-Wl,-rpath,\$\{.*\}||g' {} \;
make
cd ../..

#------------------------------------------
# Expect
#
cd expect-%{expect_major}
chmod u+w testsuite/configure
%configure --with-tclconfig=../tcl%{tclvers}/unix --with-tkconfig=../tk%{tclvers}/unix --with-tclinclude=../tcl%{tclvers}/generic --enable-shared --with-x=yes --with-tkinclude=../tk%{tclvers}/generic --enable-gcc
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
%configure --enable-gcc --with-tcl=../../tcl%{tclvers}/unix --with-tk=../../tk%{tkvers}/unix --enable-shared
%rmrpath
make
cd ..

#------------------------------------------
# Tix
#
cd tix-%{tixvers}/unix
%configure --enable-gcc --with-tcl=../../tcl%{tclvers}/unix --with-tk=../../tk%{tkvers}/unix
tar xjf %{SOURCE41}
cd tk%{tk_major}
%configure --enable-shared
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
make TCLSH_PROG=../tcl%{tclvers}/unix/tclsh LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$RPM_BUILD_DIR/%{name}-%{version}/tcl%{tclvers}/unix
cd ../..

#==========================================

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p ${RPM_BUILD_ROOT}
rm -f *.files

# If %{_libdir} is not %{_prefix}/lib, then define EXTRA_TCLLIB_FILES
# which contains actual non-architecture-dependent tcl code.
if [ "%{_libdir}" != "%{_prefix}/lib" ]; then
  EXTRA_TCLLIB_FILES="$RPM_BUILD_ROOT%{_prefix}/lib/*"
fi

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

pushd $RPM_BUILD_ROOT%_bindir
ln -fs tclsh* tclsh
popd

pushd $RPM_BUILD_ROOT%_libdir
GenerateLinkerScript tcl %{tcl_major}
popd

echo "%%defattr(-,root,root)" > tcl.files
(find ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_includedir} \
	${RPM_BUILD_ROOT}%{_mandir} -type f -o -type l;
 find ${RPM_BUILD_ROOT}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
	| sort | uniq -u >> tcl.files


#------------------------------------------
# Tk
#
cd tk%{tkvers}/unix
%makeinstall
cd ../..

pushd $RPM_BUILD_ROOT%_bindir
ln -sf wish* wish
popd

pushd $RPM_BUILD_ROOT%_libdir
GenerateLinkerScript tk %{tk_major}
popd

echo "%%defattr(-,root,root)" > tk.files
(find ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_includedir} \
	${RPM_BUILD_ROOT}%{_mandir} -type f -o -type l;
 find ${RPM_BUILD_ROOT}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
	| sort | uniq -u >> tk.files

#------------------------------------------
# TclX
#

cd tclx%{tclxvers}/unix
%makeinstall \
	TCLX_INST_LIB=$RPM_BUILD_ROOT%{_libdir} \
	TKX_INST_LIB=$RPM_BUILD_ROOT%{_libdir}
cd ../..

bzip2 -dc %SOURCE40 | tar -C $RPM_BUILD_ROOT -xf -

if [ "%_mandir" = "%{_prefix}/share/man" ]; then
   ( cd ${RPM_BUILD_ROOT}%{_prefix}/man; tar cf - ./man[13n] ) | 
   ( cd ${RPM_BUILD_ROOT}%{_mandir}; tar xf - )
   ( cd ${RPM_BUILD_ROOT}%{_prefix}/man; rm -rf ./man[13n] )
fi

echo "%%defattr(-,root,root)" > tclx.files
(find ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_includedir} \
	${RPM_BUILD_ROOT}%{_mandir} -type f -o -type l;
 find ${RPM_BUILD_ROOT}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
	| sort | uniq -u >> tclx.files

#------------------------------------------
# Expect
#
cd expect-%{expect_major}
%makeinstall tcl_libdir=${RPM_BUILD_ROOT}%{_libdir} \
	libdir=${RPM_BUILD_ROOT}%{_libdir}/expect%{expect_major} \
	TKLIB_INSTALLED="-L$RPM_BUILD_ROOT%{_libdir} -ltk%{tk_major}" \
	TCLLIB_INSTALLED="-L$RPM_BUILD_ROOT%{_libdir} -ltcl%{tcl_major}"
cd ..

# remove cryptdir/decryptdir, as Linux has no crypt command (bug 6668).
rm -f ${RPM_BUILD_ROOT}%{_bindir}/{cryptdir,decryptdir}
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/{cryptdir,decryptdir}.1*

echo "%%defattr(-,root,root)" > expect.files
(find ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_includedir} \
	${RPM_BUILD_ROOT}%{_mandir} -type f -o -type l;
 find ${RPM_BUILD_ROOT}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
	| sort | uniq -u >> expect.files

set +x +H
for n in `cat expect.files`; do
	test -f $n || continue
	head -1 $n | grep -q ^#! || continue
	chmod u+w $n
	perl -pi -e "s|${RPM_BUILD_ROOT}||" $n
done
set -x -H

#------------------------------------------
# Tix
#
cd tix-%{tixvers}/unix
%makeinstall datadir=${RPM_BUILD_ROOT}%{_prefix}/lib \
	LIB_DIR=$RPM_BUILD_ROOT%{_libdir} \
	LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$RPM_BUILD_DIR/%{name}-%{version}/tcl%{tclvers}/unix
cd ../..

# Not needed anymore?
rm -rf $RPM_BUILD_ROOT%_libdir/libtixsam*

# aesthetic: make libtix*.so executable
chmod +x $RPM_BUILD_ROOT%_libdir/libtix*.so

pushd $RPM_BUILD_ROOT%_bindir
ln -s tixwish%{libtix_major} tixwish
popd

if [ "%_mandir" = "%{_prefix}/share/man" ]; then
   ( cd ${RPM_BUILD_ROOT}%{_prefix}/man; tar cf - ./man[13n] ) | 
   ( cd ${RPM_BUILD_ROOT}%{_mandir}; tar xf - )
   ( cd ${RPM_BUILD_ROOT}%{_prefix}/man; rm -rf ./man[13n] )
fi

# tixwish.1 in /usr/share/man/man1.
mv $RPM_BUILD_ROOT/usr/share/man/mann/tixwish.1 \
	$RPM_BUILD_ROOT/usr/share/man/man1
	
echo "%%defattr(-,root,root)" > tix.files
(find ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_includedir} \
	${RPM_BUILD_ROOT}%{_mandir} -type f -o -type l;
 find ${RPM_BUILD_ROOT}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
	| sort | uniq -u >> tix.files

#------------------------------------------
# Itcl
#
cd itcl%{itclvers}
%makeinstall TCLSH_PROG=../../tcl%{tclvers}/unix/tclsh \
	LD_LIBRARY_PATH=../../tcl%{tclvers}/unix \
	SHLIB_LDFLAGS="-L../../tcl%{tclvers}/unix -ltclstub%{tcl_major}"
cd ..

if [ "%_mandir" = "%{_prefix}/share/man" ]; then
   ( cd ${RPM_BUILD_ROOT}%{_prefix}/man; tar cf - ./man[13n] ) | 
   ( cd ${RPM_BUILD_ROOT}%{_mandir}; tar xf - )
   ( cd ${RPM_BUILD_ROOT}%{_prefix}/man; rm -rf ./man[13n] )
fi

echo "%%defattr(-,root,root)" > itcl.files
(find ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_includedir} \
	${RPM_BUILD_ROOT}%{_mandir} -type f -o -type l;
 find ${RPM_BUILD_ROOT}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
	| sort | uniq -u >> itcl.files

set +x +H
for n in `cat itcl.files`; do
	[ -f $n ] || continue
	head -1 $n | grep -q ^#! || continue
	chmod u+w $n
	perl -pi -e "s|${RPM_BUILD_ROOT}||" $n
done
set -x -H

#------------------------------------------
# Tcllib
#
cd tcllib-%{tcllibvers}
%makeinstall TCLSH_PROG=../tcl%{tclvers}/unix/tclsh \
	 LD_LIBRARY_PATH="../tcl%{tclvers}/unix" 
cd ..

if [ "%_mandir" = "%{_prefix}/share/man" ]; then
   ( cd ${RPM_BUILD_ROOT}%{_prefix}/man; tar cf - ./man[13n] ) | 
   ( cd ${RPM_BUILD_ROOT}%{_mandir}; tar xf - )
   ( cd ${RPM_BUILD_ROOT}%{_prefix}/man; rm -rf ./man[13n] )
fi

echo "%%defattr(-,root,root)" > tcllib.files
(find ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_includedir} \
	${RPM_BUILD_ROOT}%{_mandir} -type f -o -type l;
 find ${RPM_BUILD_ROOT}%{_libdir}/* $EXTRA_TCLLIB_FILES) | cat - *.files \
	| sort | uniq -u >> tcllib.files

#------------------------------------------
# post process the *.files list, removing build sys references and mark
# which are directories

set +x
for n in *.files; do
	mv $n $n.in
	sed "s|.*%{_prefix}\\>|%{_prefix}|" < $n.in | while read file; do
	    if [ -d ${RPM_BUILD_ROOT}/$file ]; then
		echo -n '%dir '
	    fi
	    echo $file
	done > $n
	rm -f $n.in
done
set -x

# Man pages can be compressed
perl -pi -e 's|(^%{_mandir}/man.*$)|\1\*|' *.files

perl -pi -e "s|$RPM_BUILD_DIR/tcltk-%{version}/tcl%{version}/unix|%{_includedir}|" $RPM_BUILD_ROOT/%{_libdir}/*.sh
perl -pi -e "s|$RPM_BUILD_DIR/tcltk-%{version}/tk%{version}/unix|%{_includedir}|" $RPM_BUILD_ROOT/%{_libdir}/*.sh
perl -pi -e "s|$RPM_BUILD_DIR/tcltk-%{version}/tclx%{tclXvers}/unix|%{_includedir}|" $RPM_BUILD_ROOT/%{_libdir}/*.sh
perl -pi -e "s|$RPM_BUILD_DIR/tcltk-%{version}/tkx%{version}/unix|%{_includedir}|" $RPM_BUILD_ROOT/%{_libdir}/*.sh
perl -pi -e "s|-L/usr/include|-L/usr/lib|g" $RPM_BUILD_ROOT/%{_libdir}/*.sh

# (gb) FIXME: libdir patches are not good enough :-(
perl -pi -e "s|-L/usr/lib\b|-L%{_libdir}|g" $RPM_BUILD_ROOT%{_libdir}/*.sh
perl -pi -e "s|/usr/lib/lib|%{_libdir}/lib|g" $RPM_BUILD_ROOT%{_libdir}/*.sh

#==========================================
%post -p /sbin/ldconfig -n tcl
%post -p /sbin/ldconfig -n tk
%post -p /sbin/ldconfig -n expect
%post -p /sbin/ldconfig -n tclx
%post -p /sbin/ldconfig -n tix
%post -p /sbin/ldconfig -n itcl
%post -p /sbin/ldconfig -n tcllib

%postun -p /sbin/ldconfig -n tcl
%postun -p /sbin/ldconfig -n tk
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

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 8.4.2-6avx
- bootstrap build

* Mon Aug 30 2004 Vincent Danen <vdanen@annvix.org> 8.4.2-5avx
- fix dangling symlink (tixwish)

* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 8.4.2-4avx
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
- Re-add %%_libdir/libtcl.so

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
