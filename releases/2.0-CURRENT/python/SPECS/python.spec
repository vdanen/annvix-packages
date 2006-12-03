#
# spec file for package python
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		python
%define version		2.4.3
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

Source0:	http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.bz2
Source1:	http://www.python.org/ftp/python/doc/%{docver}/html-%{docver}.tar.bz2
Source2:	python-2.4-base.list
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
Patch7:		python-2.4.3-fix-buffer_overflow_with_glibc2.3.5.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	XFree86-devel 
BuildRequires:	blt
BuildRequires:	db2-devel
BuildRequires:	db4-devel
BuildRequires:	expat-devel
BuildRequires:	gdbm-devel 
BuildRequires:	gmp-devel
BuildRequires:	termcap-devel 
BuildRequires:	ncurses-devel 
BuildRequires:	openssl-devel 
BuildRequires:	readline-devel 
BuildRequires:	tix
BuildRequires:	tk
BuildRequires:	tcl 
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
Requires:	python = %{version}
Requires:	tcl
Requires:	tk

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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n Python-%{version}
# no-local-incpath
%patch3 -p1
# lib64
%patch4 -p1
# biarch-headers
%patch5 -p1
# gdbm
%patch6 -p1
%patch7 -p0

autoconf

mkdir html
bzcat %{_sourcedir}/html-%{docver}.tar.bz2 | tar x  -C html

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
cat %{_sourcedir}/python-2.4-base.list | sed 's@%%{_libdir}@%{_libdir}@' > include.list
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

LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}%{_bindir}/python %{_sourcedir}/exclude.py %{buildroot} include.list modules-list > main.list

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

%files doc
%doc html/*/*


%changelog
* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3
- P7: fix compil
- rebuild against new ncurses

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3
- rebuild against new openssl
- spec cleanups

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3
- rebuild against new db4

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3
- rebuild against new readline

* Sat May 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3
- 2.4.3
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.2
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.2
- 2.4.2
- disable test_hotshot on x86_64
- add BuildRequires: bzip2-devel
- fix PreReq
- make sure we're using /tmp for TMP/TMPDIR settings as tests may fail
  due to delays if a homedir is on an NFS mount (misc)

* Sun Dec 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-3avx
- updated P4: fixed get_config_h_fileiname in distutils for
  multiarch headers (flepied)

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
