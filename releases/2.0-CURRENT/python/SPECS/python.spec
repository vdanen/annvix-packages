#
# spec file for package python
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


#
# $Id$

%define revision	$Rev$
%define name		python
%define version		2.4.2
%define release		%_revrel

%define docver  	2.4
%define dirver  	2.4

%define lib_major	%{dirver}
%define libname_orig	libpython
%define libname	%mklibname %{name} %{lib_major}

Summary:	An interpreted, interactive object-oriented programming language
Name:		%{name}
Version: 	%{version}
Release:	%{release}
License:	Modified CNRI Open Source License
Group:		Development/Python
URL:		http://www.python.org/

Source:		http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.bz2
Source1:	http://www.python.org/ftp/python/doc/%{docver}/html-%{docver}.tar.bz2
Source2:	python-2.4-base.list.bz2
Source3:	exclude.py

# Don't include /usr/local/* in search path
Patch3:		Python-2.3-no-local-incpath.patch

# Support */lib64 convention on x86_64, sparc64, etc.
Patch4:		Python-2.4.1-lib64.patch

# Do handle <asm-XXX/*.h> headers in h2py.py
# FIXME: incomplete for proper bi-arch support as #if/#else/#endif
# clauses generally should have been handled
Patch5:		Python-2.2.2-biarch-headers.patch
# detect and link with gdbm_compat for dbm module
Patch6:		Python-2.4.1-gdbm.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	XFree86-devel 
BuildRequires:	blt
BuildRequires:	db2-devel, db4-devel
BuildRequires:	expat-devel
BuildRequires:	gdbm-devel 
BuildRequires:	gmp-devel
BuildRequires:	termcap-devel 
BuildRequires:	ncurses-devel 
BuildRequires:	openssl-devel 
BuildRequires:	readline-devel 
BuildRequires:	tix, tk, tcl 
BuildRequires:	autoconf2.5
BuildRequires:	bzip2-devel

Conflicts:	tkinter < %{version}
Requires:	%{libname} = %{version}
Requires:	%{name}-base = %{version}

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that
need a programmable interface. This package contains most of the
standard Python modules, as well as modules for interfacing to the
Tix widget set for Tk and RPM.


%package -n %{libname}
Summary:	Shared libraries for Python %{version}
Group:		System/Libraries
Requires(post):	ldconfig
Requires(postun): ldconfig

%description -n %{libname}
This packages contains Python shared object library.  Python is an
interpreted, interactive, object-oriented programming language often
compared to Tcl, Perl, Scheme or Java.


%package -n %{libname}-devel
Summary:	The libraries and header files needed for Python development
Group:		Development/Python
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}

%description -n %{libname}-devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.


%package -n tkinter
Summary:	A graphical user interface for the Python scripting language
Group:		Development/Python
Requires:	python = %{version}, tcl, tk

%description -n tkinter
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.


%package base
Summary:	Python base files
Group:		Development/Python
Requires:	%{libname} = %{version}

%description base
This packages contains the Python part that is used by the base packages
of a Annvix distribution.


%prep
%setup -q -n Python-%{version}
%patch3 -p1 -b .no-local-incpath
%patch4 -p1 -b .lib64
%patch5 -p1 -b .biarch-headers
%patch6 -p1 -b .gdbm
autoconf

mkdir html
bzcat %{SOURCE1} | tar x  -C html

find . -type f -print0 | xargs -0 perl -p -i -e 's@/usr/local/bin/python@/usr/bin/python@'


%build
rm -f Modules/Setup.local
cat > Modules/Setup.local << EOF
linuxaudiodev linuxaudiodev.c
EOF

OPT="%{optflags} -g"
export OPT
%configure2_5x \
    --with-threads \
    --with-cycle-gc \
    --with-cxx=g++ \
    --without-libdb \
    --enable-ipv6 \
    --enable-shared

# fix build
perl -pi -e 's/^(LDFLAGS=.*)/$1 -lstdc++/' Makefile

%make
# all tests must pass
%ifarch x86_64
addtest="-x test_hotshot"
%else
addtest=""
%endif

export TMP="/tmp" TMPDIR="/tmp"
make test TESTOPTS="-l -x test_linuxaudiodev -x test_openpty -x test_nis ${addtest}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}

# fix Makefile to get rid of reference to distcc
perl -pi -e "/^CC=/ and s/distcc/gcc/" Makefile

# set the install path
echo '[install_scripts]' >setup.cfg
echo 'install_dir='"%{buildroot}%{_bindir}" >>setup.cfg

# python is not GNU and does not know fsstd
mkdir -p %{buildroot}%{_mandir}
%makeinstall_std

(cd %{buildroot}%{_libdir}; ln -sf libpython%{lib_major}.so.* libpython%{lib_major}.so)

# Provide a libpython%{dirver}.so symlink in /usr/lib/puthon*/config, so that
# the shared library could be found when -L/usr/lib/python*/config is specified
(cd %{buildroot}%{_libdir}/python%{dirver}/config; ln -sf ../../libpython%{lib_major}.so .)

# smtpd proxy
mv -f %{buildroot}%{_bindir}/smtpd.py %{buildroot}%{_libdir}/python%{dirver}/

# idle
cp Tools/scripts/idle %{buildroot}%{_bindir}/idle

# modulator
cat << EOF > %{buildroot}%{_bindir}/modulator
#!/bin/bash
exec %{_libdir}/python%{dirver}/site-packages/modulator/modulator.py
EOF
cp -r Tools/modulator %{buildroot}%{_libdir}/python%{dirver}/site-packages/

# pynche
cat << EOF > %{buildroot}%{_bindir}/pynche
#!/bin/bash
exec %{_libdir}/python%{dirver}/site-packages/pynche/pynche
EOF
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche %{buildroot}%{_libdir}/python%{dirver}/site-packages/

chmod 0755 %{buildroot}%{_bindir}/{idle,modulator,pynche}

ln -f Tools/modulator/README Tools/modulator/README.modulator
ln -f Tools/pynche/README Tools/pynche/README.pynche

rm -f modules-list.full
for n in %{buildroot}%{_libdir}/python%{dirver}/*; do
    [ -d $n ] || echo $n
done >> modules-list.full

for mod in %{buildroot}%{_libdir}/python%{dirver}/lib-dynload/* ; do
    [ `basename $mod` = _tkinter.so ] || echo $mod
done >> modules-list.full
sed -e "s|%{buildroot}||g" < modules-list.full > modules-list


rm -f include.list main.list
bzcat %{SOURCE2} | sed 's@%%{_libdir}@%{_libdir}@' > include.list
cat >> modules-list << EOF
%{_bindir}/python
%{_bindir}/python2.4
%{_bindir}/pydoc
%{_mandir}/man1/python*
%{_libdir}/python*/bsddb/
%{_libdir}/python*/curses/
%{_libdir}/python*/distutils/
%{_libdir}/python*/encodings/*
%{_libdir}/python*/lib-old/
%{_libdir}/python*/logging/
%{_libdir}/python*/xml/
%{_libdir}/python*/compiler/
%{_libdir}/python*/email/
%{_libdir}/python*/hotshot/
%{_libdir}/python*/site-packages/README
%{_libdir}/python*/plat-linux2/
$MODULESEXTRA
EOF

LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}%{_bindir}/python %{SOURCE3} %{buildroot} include.list modules-list > main.list

# fix non real scripts
chmod 0644 %{buildroot}%{_libdir}/python*/test/test_{binascii,grp,htmlparser}.py*
# fix python library not stripped
chmod u+w %{buildroot}%{_libdir}/libpython2.4.so.1.0

%multiarch_includes %{buildroot}/usr/include/python*/pyconfig.h


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -f modules-list main.list


%files -f main.list
%defattr(-, root, root, 755)
%dir %{_libdir}/python*/lib-dynload
%dir %{_libdir}/python*/site-packages

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libpython*.so.1*

%files -n %{libname}-devel
%defattr(-, root, root, 755)
%{_libdir}/libpython*.so
%dir %{_includedir}/python*
%multiarch %multiarch_includedir/python*/pyconfig.h
%{_includedir}/python*/*
%{_libdir}/python*/config/
%{_libdir}/python*/test/


%files -n tkinter
%defattr(-, root, root, 755)
%dir %{_libdir}/python*/lib-tk
%{_libdir}/python*/lib-tk/*.py*
%{_libdir}/python*/lib-dynload/_tkinter*.so
%{_libdir}/python*/idlelib
%{_libdir}/python*/site-packages/modulator
%{_libdir}/python*/site-packages/pynche
%{_bindir}/idle
%{_bindir}/pynche
%{_bindir}/modulator

%files base -f include.list
%defattr(-, root, root, 755)
%dir %{_libdir}/python*


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org>
- 2.4.2
- disable test_hotshot on x86_64
- add BuildRequires: bzip2-devel
- fix PreReq
- make sure we're using /tmp for TMP/TMPDIR settings as tests may fail
  due to delays if a homedir is on an NFS mount (misc)

* Sun Dec 25 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-3avx
- updated P4: fixed get_config_h_fileiname in distutils for
  multiarch   headers (flepied)

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-2avx
- rebuild against new expat

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-1avx
- 2.4.1
- dropped P6; merged upstream
- new P6 from mandriva to link gdbm support

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4-5avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4-4avx
- rebuild for new gcc
- multiarch support

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4-3avx
- bootstrap build

* Wed Feb 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4-2avx
- P6: fix for CAN-2005-0089
- make test without testing test_openpty since it fails if python is built
  in a chroot

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4-1avx
- 2.4
- drop P6; applied upstream
- rediff P3, P4 (misc)
- multiarch tagging (flepied)
- tkinter is behaving odd... not sure if it works (not sure if i care)

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.4-2avx
- rebuild against latest openssl

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.4-1avx
- 2.3.4
- BuildRequires: autoconf2.5, tk, tcl
- tkinter requires tcl and tk (mdk bug #10278) (misc)
- s/Mandrake Linux/Annvix/
- fix [DIRM] (misc)

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.3-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.3.3-1sls
- 2.3.3
- add traceback.py* to python-base
- remove icons

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.3-7sls
- minor spec cleanups
- remove %%build_opensls macro
- remove menu entry for tkinter

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 2.3-6sls
- sync with 4mdk (gbeauchesne): fix mklibnamification

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 2.3-5sls
- get rid of all the emacs stuff

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 2.3-4sls
- OpenSLS build
- tidy spec
- don't build doc package for OpenSLS

* Sun Aug 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3-3mdk
- Fix lib64 patch and introduce sys.lib
- Patch6: 64-bit fixes to zipimport module

* Fri Aug  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.3-2mdk
- corrected patch on distutils for lib64 management
- byte compile without storing the build path

* Thu Aug  7 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.3-1mdk
- 2.3

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.3-6mdk
- Fix libpython2.2.so symlink

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.3-5mdk
- BuildRequires: termcap-devel

* Thu Jul 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.3-4mdk
- Fix libification
- Patch8: Fix test_compile.py test for 64-bit platforms (CVS)

* Tue Jul  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.2.3-3mdk
- remove compilation path from library
- compiled with ipv6 support (bug #2045)

* Wed Jun 25 2003 Stefan van der Eijk <stefan@eijk.nu> 2.2.3-2mdk
- remove redundant BuildRequires
- disable test on alpha & x86_64 for now, see SF bug: #660455 

* Wed Jun  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.2.3-1mdk
- 2.2.3

* Mon May  5 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.2.2-9mdk
- applied fix for tkinter from pysol site (bug #3760)

* Sat May  3 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.2.2-8mdk
- fix tkinter (bug #3760)

* Mon Apr 14 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.2.2-7mdk
- rebuild for tcl/tk

* Wed Feb  5 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.2.2-6mdk
- rebuild for libssl

* Sat Jan  4 2003 Pixel <pixel@mandrakesoft.com> 2.2.2-5mdk
- robotparser patch, esp. fixes linkchecker on https (http://python.org/sf/499513)

* Thu Dec  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.2-4mdk
- added BuildRequires db2-devel

* Thu Dec  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.2-3mdk
- use %%mklibname

* Sat Nov 23 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.2-2mdk
- s/distcc/gcc/ Makefile in case the former was used to build Python
- Patch5: Let h2py.py handle "-" in headers file name. This fixes
  build on x86-64 where kernel-headers are now bi-arch'ed.

* Fri Nov 15 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.2-1mdk
- activated check by default
- 2.2.2

* Thu Nov 14 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.2.1-15mdk
- include /usr/bin/pydoc and /usr/bin/python2.2
- clean up changelog to use (double-percent) everywhere; I think that was
  causing some wierd issues with newer rpm

* Wed Nov 13 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.2.1-14mdk
- security fix (execvpe local execution vulnerability)

* Mon Sep  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.1-13mdk
- put time.so in python-base

* Tue Aug 27 2002 David BAUDENS <baudens@mandrakesoft.com> 2.2.1-12mdk
- Fix icon (menu)

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.1-11mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Tue Aug 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.1-10mdk
- fix setup step

* Mon Jul 29 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.2.1-9mdk
- Remove NO_XALF from menu entries

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.1-8mdk
- Automated rebuild with gcc3.2

* Wed Jul 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.2.1-7mdk
- rebuild for new readline

* Mon Jul  1 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.1-6mdk
- Update Patch4 to get correct "site-specific" directory

* Sun Jun 30 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.1-5mdk
- Menu dir is %%_menudir, not %%{_libdir}/menu
- Update Source2 (baselist) to be %%{_libdir} compliant
- Update Patch1 (shlib) to really build importdl with PIC code
- Patch4: Look for and install libraries in the right directory
- Rpmlint fixes: configure-without-libdir-spec, hardcoded-library-path

* Sun Jun  2 2002 Stefan van der Eijk <stefan@eijk.nu> 2.2.1-4mdk
- BuildRequires

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.1-3mdk
- Automated rebuild in gcc3.1 environment

* Thu Apr 18 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.1-2mdk
- Patch2: Do use g++ as the linker when objects were built with g++,
  namely ccpython.o for the Python interpreter. Fix build with gcc3+.
- Patch3: Don't include /usr/local/* in search path

* Wed Apr 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2.1-1mdk
- 2.2.1

* Sun Feb 24 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2-9mdk
- rebuild PPC against libdb3.3 - thx Jeff

* Tue Feb 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2-8mdk
- requires explictly the lib+version+release for python-base.

* Mon Feb 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2-7mdk
- don't use %%exclude
- patch for path (Ralf Ahlbrin)

* Thu Jan 17 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2-6mdk
- split python in python and python-base to lower the size of the
base packages .

* Wed Jan  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2-5mdk
- added missing subdirs.

* Wed Jan 09 2002 David BAUDENS <baudens@mandrakesoft.com> 2.2-4mdk
- Fix menu entry (png icon)

* Thu Jan  3 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2-3mdk
- bytecompile with a -d option to avoid putting the RPM_BUILD_ROOT in
the byte compiled file.

* Wed Jan  2 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2-2mdk
- rebuild to have the right dependencies

* Sun Dec 23 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.2-1mdk
- 2.2

* Wed Oct 24 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.1-5mdk
- Libification
- Enhanced Patch2 thanks to a Debian patch so that a shared library is
  built as well. Fix linuxconf, koffice builds on IA-64.

* Tue Oct  9 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.1-4mdk
- Remove BuildRequires: libxode1-devel
- Remove Requires: libtcl8.3.so libtk8.3.so for tkinter

* Thu Aug 30 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.1-3mdk
- Patch2: DSO must have PIC code. Actually, kludge the configure script
  if MACHDEP is set
- Add BuildRequires: autoconf

* Mon Aug 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.1.1-2mdk
- updated doc (#4263).

* Fri Jul 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.1.1-1mdk
- 2.1.1

* Tue Jul  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.1-2mdk
- rebuild for db3.2

* Fri Apr 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.1-1mdk
- 2.1

* Wed Apr 11 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0-9mdk
- Correct GNOME menu entry

* Sun Apr  8 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.0-8mdk
- added missing xml directory
- added an optional make test at the end of the %%build section

* Fri Mar 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.0-6mdk
- correct launching of scripts (#2802)

* Tue Mar 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.0-5mdk
- added libtermcap-devel to BuildRequires.

* Sat Mar 24 2001 David BAUDENS <baudens@mandrakesoft.com> 2.0-4mdk
- BuildRequires: libxode1-devel
- Requires: %%{version}-%%{release} and not only %%{version}

* Mon Mar 19 2001 Pixel <pixel@mandrakesoft.com> 2.0-3mdk
- fix the python.el (\\. -> \\\\.)

* Fri Dec  8 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.0-2mdk
- added blt and expat-devel BuildRequires:

* Fri Nov 17 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.0-1mdk
- 2.0 (95 tests OK. 12 tests skipped: test_al test_cd test_cl test_dl test_gl test_imgfile test_largefile
test_linuxaudiodev test_nis test_sunaudiodev test_winreg test_winsound)
- added emacs mode
- html doc.

* Wed Sep 27 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.5.2-12mdk
- removed dependency on tkinter for python to avoid loop.

* Mon Sep 11 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.5.2-11mdk
- fixed some hardcoded paths (Geoffrey Lee).
- removed menu entry for interpreter.

* Thu Aug 10 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.5.2-10mdk
- fixed typo %%updates_menus -> %%update_menus

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.5.2-9mdk
- automatically added BuildRequires

* Thu Aug  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.5.2-8mdk
- Merge rh patch.
- Macros.
- compile with new tcl.

* Tue May  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.5.2-7mdk
- added locale module.

* Thu Mar 30 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.5.2-6mdk
- menu

* Tue Mar  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.5.2-5mdk
- idle 0.5.
- compiled with optimization.

* Fri Jan 14 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.5.2-4mdk

- added a BuildRequires.

* Sat Dec 4 1999 Florent Villard <warly@mandrakesoft.com>
- add idle, pynche and modulator in the package

* Tue Oct 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with redhat changes.
- added modulator, and pynche to the python-tools package(r)
- using a files list in the %%files section for python-tools(r)
- added conflicts/requires between subpackages so that you cannot
  have an older tkinter installed with a new python.(r)
- added more tools(r)
- rebuild to fix broken tkinter.(r)
- fixed bogus /usr/local/bin/python requirements.(r)
- added patch to import global symbols until we get libtool patched(r)

* Fri Aug 20 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- updated to 1.5.2
- updated patches
- use macro %%{_arch} instead of %%{_target_cpu} for file paths

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Remove the dbm support (doen't work with GLBC2.1)

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- add de locale
- fix handling of RPM_OPT_FLAGS

* Thu Feb 11 1999 Michael Johnson <johnsonm@redhat.com>
- added mpzmodule at user request (uses gmp)
- added bsddbmodule at user request (uses db 1.85 interface)

* Mon Feb 08 1999 Michael Johnson <johnsonm@redhat.com>
- add --with-threads at user request
- clean up spec file

* Fri Jan 08 1999 Michael K. Johnson <johnsonm@redhat.com>
- New libc changes ndbm.h to db1/ndbm.h and -ldb to -ldb1

* Thu Sep  3 1998 Jeff Johnson <jbj@redhat.com>
- recompile for RH 5.2.

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- python-docs used to require /usr/bin/sed. Changed to /bin/sed instead

* Wed Apr 29 1998 Cristian Gafton <gafton@redhat.com>
- fixed the spec file for version 1.5.1
- buildroot (!)

* Mon Apr 20 1998 Michael K. Johnson <johnsonm@redhat.com>
- updated to python 1.5.1
- created our own Python-Doc tar file from 1.5 to substitute for the
  not-yet-released Doc package.
- build _tkinter properly
- use readline again
- build crypt module again
- install rand replacement module
- added a few modules

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- updated to python 1.5
- made /usr/lib/python1.5 file list automatically generated

* Tue Nov 04 1997 Michael K. Johnson <johnsonm@redhat.com>
- Fixed dependencies for python and tkinter

* Mon Nov 03 1997 Michael K. Johnson <johnsonm@redhat.com>
- pulled out tk-related stuff into tkinter package

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- bunches of scripts used /usr/local/bin/python instead of /usr/bin/python

* Tue Sep 30 1997 Erik Troan <ewt@redhat.com>
- updated for tcl/tk 8.0

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
