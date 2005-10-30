%define	name	Mesa
%define version	5.0.1
%define release	8avx

%global _unpackaged_files_terminate_build 0

%define glx_ver			20001222
%define glx_mesa_version 	3.2.1
%define mesa_so_version 	1.4.501
%define GLwrapper_version	0.1.8

%define glname			MesaGL
%define gluname			MesaGLU
%define glutname		Mesaglut
%define glmajor			1
%define glumajor		1
%define glutmajor		3
%define libglname		%mklibname %{glname} %{glmajor}
%define libgluname		%mklibname %{gluname} %{glumajor}
%define libglutname		%mklibname %{glutname} %{glutmajor}

%define prefix		/usr/X11R6
%define libdir		%{prefix}/%{_lib}

Summary:	OpenGL 1.4 compatible 3D graphics library
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
URL:		http://www.mesa3d.org
License:	MIT
Source:		ftp://ftp.mesa3d.org/pub/mesa/MesaLib-%{version}.tar.bz2
Source1:	ftp://ftp.mesa3d.org/pub/mesa/MesaDemos-%{version}.tar.bz2
Source2:	http://utah-glx.sourceforge.net/glx-%{glx_ver}.tar.bz2
Source4:	%{name}-icons.tar.bz2
Source5:	ftp://ftp.mesa3d.org/pub/mesa/MesaLib-%{glx_mesa_version}.tar.bz2
Source6:	GLwrapper-%{GLwrapper_version}.tar.bz2
Patch1:		%{name}-4.0.3-remove-rpath.patch.bz2
Patch3:		%{name}-3.3-gcc-2.96.patch.bz2
Patch4:		%{name}-3.5-opt.patch.bz2
Patch5:		Mesa-4.0.2-GLU-libsupc++.patch.bz2
Patch10:	glx-rename_glx_so.patch.bz2
Patch13:	Mesa-3.4-glxARB.patch.bz2
Patch14:	glx-mach64tmp.patch.bz2
Patch15:	Mesa-5.0.1-gcc3.3.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	XFree86-devel autoconf2.5 tcl texinfo
BuildRequires:	binutils >= 2.9.1.0.19a
BuildRequires:	libstdc++-devel >= 3.2

Prefix:		%{prefix}
Requires:	%{libglname} = %{version}-%{release}
Provides:	hackMesa = %{version}
Obsoletes:	hackMesa <= %{version}

%description
Mesa is an OpenGL 1.4 compatible 3D graphics library.

%package -n %{libglname}
Summary:	Files for Mesa (GL and GLX libs)
Group:		System/Libraries

%description -n %{libglname}
Mesa is an OpenGL 1.4 compatible 3D graphics library.
GL and GLX parts.

%package -n %{libgluname}
Summary:	Files for Mesa (GLU libs)
Group:		System/Libraries

%description -n %{libgluname}
Mesa is an OpenGL 1.4 compatible 3D graphics library.
GLU parts.

%package -n %{libgluname}-devel
Summary:	Development files for GLU libs
Group:		Development/C
Requires:	%{libgluname} = %{version}-%{release}
Provides:	lib%{gluname}-devel = %{version}-%{release}

%description -n %{libgluname}-devel
Mesa is an OpenGL 1.4 compatible 3D graphics library.
GLU parts.

This package contains the headers needed to compile Mesa programs.

%package -n %{libglutname}
Summary:	Files for Mesa (glut libs)
Group:		System/Libraries
Requires:	%{libgluname} = %{version}-%{release}
Provides:	Mesa-common = %{version}-%{release} hackMesa-common = %{version}
Obsoletes:	Mesa-common <= %{version} hackMesa-common <= %{version}

%description -n %{libglutname}
Mesa is an OpenGL 1.4 compatible 3D graphics library.
glut and GLU parts.

%package -n %{libglutname}-devel
Summary:	Development files for glut libs
Group:		Development/C
Requires:	%{libglutname} = %{version}-%{release} %{libgluname}-devel = %{version}-%{release}
Provides:	lib%{glutname}-devel = %{version}-%{release} Mesa-common-devel = %{version}-%{release} hackMesa-common-devel = %{version}
Obsoletes:	Mesa-common-devel <= %{version} hackMesa-common-devel <= %{version}

%description -n %{libglutname}-devel
Mesa is an OpenGL 1.4 compatible 3D graphics library.
glut parts.

This package contains the headers needed to compile Mesa programs.

%prep
%setup -q -n Mesa-%{version}

#Mesa-demos
tar xfj %{SOURCE1} -C ../

# utah_glx
tar xfj %{SOURCE2}

# Mesa to use with utah_glx (while waiting for support of 3.3)
tar xfj %{SOURCE5} -C glx/

# Get GLwrapper library that make a true wrapp of libGL API (fpons).
tar xfj %{SOURCE6}
cp GLwrapper-%{GLwrapper_version}/README README.GLwrapper

# (chmou) Fix gcc2.96 compilation
%ifnarch ppc
%patch3 -p1
%endif
%patch4 -p1 -b .opt

# (gb) Mesa contains C++ code from libnurbs/internals
%patch5 -p1 -b .GLU-libsupc++
# NOTE: automake is carried out in %build stage

%ifnarch alpha sparc sparc64 ppc x86_64
# patch to rename glx.so to glx-3.so
%patch10 -p1 -b .rename_glx
%endif

# patch to rename mesa.conf file to /etc/X11/mesa.conf
# all arch are taken, even if code is not compiled.
%patch13 -p1 -b .glxARB
%patch14 -p1 -b .glxtmp

%patch15 -p0

perl -pi -e "s/-O3/$RPM_OPT_FLAGS/" Make-config

pushd demos && {
	for i in *.c; do 
	perl -pi -e "s|\.\./images/|%{libdir}/mesa-demos-data/|" $i ; 
	done 
	perl -pi -e "s|isosurf.dat|%{libdir}/mesa-demos-data/isosurf.dat|" isosurf.c 
} && popd

# [FP] fix libtool.
rm -f acinclude.m4
for file in m4/*.m4; do
  case $file in
  *libtool.m4) ;; # skip, system libtool is better
  *.m4) cat $file >> acinclude.m4
  esac
done
#rm -f ltmain.sh ltconfig
libtoolize --automake --copy --force
aclocal
autoheader
automake -a -c
autoconf

# remove rpath.
%patch1 -p1

%build
# [GG] something wrong with filenames...
ln -sf ./common_x86_asm.S ./src/X86/common_x86asm.S
ln -sf ./common_x86_asm.h ./src/X86/common_x86asm.h

%ifarch i386 i486
CFLAGS="$RPM_OPT_FLAGS -DNDEBUG" CXXFLAGS=$RPM_OPT_FLAGS \
	./configure	--prefix=%{prefix} \
			--libdir=%{libdir} \
			--sysconfdir=/etc/X11 \
			--target=%{_target_cpu}-mandrake-linux-gnu \
			--disable-mmx \
			--disable-3dnow \
			--disable-sse \
			--disable-osmesa \
			--without-glide \
			--without-svga \
			--without-ggi
%endif
%ifarch i586 i686 k6 athlon
CFLAGS="$RPM_OPT_FLAGS -DNDEBUG" CXXFLAGS=$RPM_OPT_FLAGS \
	./configure	--prefix=%{prefix} \
			--libdir=%{libdir} \
			--sysconfdir=/etc/X11 \
			--target=%{_target_cpu}-mandrake-linux-gnu \
			--enable-x86 \
			--enable-mmx \
			--enable-3dnow \
			--disable-sse \
			--disable-osmesa \
			--without-glide \
			--without-svga \
			--without-ggi
# SSE seems to have problem on some apps (gtulpas) for probing.
%endif
%ifarch alpha
CFLAGS="$RPM_OPT_FLAGS -DNDEBUG" CXXFLAGS=$RPM_OPT_FLAGS \
./configure	--prefix=%{prefix} \
		--libdir=%{libdir} \
		--sysconfdir=/etc/X11 \
		--target=%{_target_cpu}-mandrake-linux-gnu \
		--enable-optimize \
		--disable-osmesa \
		--without-glide \
		--without-svga \
		--without-ggi
%endif

# (gb) Absolutely necessary, at least on those arches. Or patch better.
%ifarch x86_64 sparc64 ppc64
CONFIGURE_XPATH="--x-includes=%{prefix}/include --x-libraries=%{prefix}/%{_lib}"
%endif

%ifnarch %{ix86} alpha
./configure	--prefix=%{prefix} $CONFIGURE_XPATH \
		--libdir=%{libdir} \
		--sysconfdir=/etc/X11 \
		--target=%{_target_cpu}-mandrake-linux-gnu \
		--disable-3dnow \
		--disable-sse \
		--disable-osmesa \
		--without-glide \
		--without-svga \
		--without-ggi
%endif

%make

# Skip utah_glx for alpha - (fg) also skip it for sparc - (jb) also added skip
# for ppc - (fg) And for ia64 as well - (gb) on x86_64 as well

%ifarch alpha sparc sparc64 ppc ia64 x86_64
	echo 'Architecture is not one of x86, skipping utah_glx'
%else
cd glx
cp -fv ../config.sub ./

%ifarch i386 i486
# (Dadou) Don't remove --host. It's needed if you build on arch <> than --target
# (configuration is very bugged)
# (Dadou) Supports for mmx and 3dnow are useless for i386 and i486
CFLAGS=$RPM_OPT_FLAGS ./autogen.sh	--with-chipset=all \
					--with-mesa=Mesa-3.2.1 \
					--enable-extra \
					--disable-mtrr \
					--disable-agp \
					--disable-glut \
					--disable-GLU \
					--prefix=%{prefix} \
					--sysconfdir=/etc/X11 \
					--target=%{_target_cpu}-mandrake-linux-gnu \
					--host=%{_target_cpu}-mandrake-linux-gnu \
					--disable-mmx \
					--disable-3dnow
%else
CFLAGS=$RPM_OPT_FLAGS ./autogen.sh	--with-chipset=all \
					--with-mesa=Mesa-3.2.1 \
					--enable-extra \
    					--enable-mtrr \
					--enable-agp \
					--disable-glut \
					--disable-GLU \
    					--prefix=%{prefix} \
					--with-moduledir=%{libdir}/modules \
    					--sysconfdir=/etc/X11 \
    					--target=%{_target_cpu}-mandrake-linux-gnu \
					--host=%{_target_cpu}-mandrake-linux-gnu
%endif
# Arg docs sux ((Dadou) "are not OK", it's better ;)
pushd docs
cat <<EOF > config.cache
ac_cv_path_install=${ac_cv_path_install='/usr/bin/install -c'}
ac_cv_prog_CP=${ac_cv_prog_CP='cp -f'}
ac_cv_prog_LN_S=${ac_cv_prog_LN_S='ln -s'}
ac_cv_prog_MKDIR=${ac_cv_prog_MKDIR='mkdir -p'}
ac_cv_prog_MV=${ac_cv_prog_MV='mv -f'}
ac_cv_prog_RM=${ac_cv_prog_RM='rm -f'}
ac_cv_prog_have_dvips=${ac_cv_prog_have_dvips=no}
ac_cv_prog_have_jade=${ac_cv_prog_have_jade=no}
ac_cv_prog_have_jadetex=${ac_cv_prog_have_jadetex=no}
ac_cv_prog_have_lynx=${ac_cv_prog_have_lynx=no}
ac_cv_prog_have_ps2pdf=${ac_cv_prog_have_ps2pdf=no}
ac_cv_prog_make_make_set=${ac_cv_prog_make_make_set=yes}
EOF
./configure --enable-text
popd

make
cd ..
%endif # Skip glx for Alpha

# (gb) Fix GLwrapper Makefile.
pushd GLwrapper-%{GLwrapper_version}
perl -pi -e "s|(-L/usr/X11R6)/lib\\b|\1/%{_lib}|" Makefile
perl -pi -e "s|(\\\$\(prefix\))/lib\\b|\1/%{_lib}|" Makefile
popd

# build GLwrapper.
make prefix=%{prefix} mesa_so_version=%{mesa_so_version} -C GLwrapper-%{GLwrapper_version}

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{libdir}/mesa-demos-data
mkdir -p $RPM_BUILD_ROOT/usr/include
mkdir -p $RPM_BUILD_ROOT%{prefix}/etc
make DESTDIR=$RPM_BUILD_ROOT install
if [ ! -e $RPM_BUILD_ROOT%{libdir}/libGL.la ]; then
  echo "PROBLEM INSTALLING MESA LA LIBRARY"
  if [ -e src/libGL.la ]; then
    install -m 0644 src/libGL.la $RPM_BUILD_ROOT%{libdir}/libGL.la
  fi
fi
if [ ! -e $RPM_BUILD_ROOT%{libdir}/libGL.so.%{mesa_so_version} ]; then
  echo "PROBLEM INSTALLING MESA SO LIBRARY"
  if [ -e src/.libs/libGL.so.%{mesa_so_version} ]; then
    install -m 0755 src/.libs/libGL.so.%{mesa_so_version} $RPM_BUILD_ROOT%{libdir}/libGL.so.%{mesa_so_version}
  elif [ -e src/.libs/libGL.so.%{mesa_so_version}U ]; then
    install -m 0755 src/.libs/libGL.so.%{mesa_so_version}U $RPM_BUILD_ROOT%{libdir}/libGL.so.%{mesa_so_version}
  fi
fi

#install -m 0644 include/GL/glext.h $RPM_BUILD_ROOT%{prefix}/include/GL


%ifarch alpha sparc sparc64 ppc ia64 x86_64
echo 'Skipping utah_glx'
%else
mkdir -p $RPM_BUILD_ROOT/usr/bin
cat > $RPM_BUILD_ROOT/usr/bin/glx <<EOF
#!/bin/sh
LD_PRELOAD=%{libdir}/libGL.so.1.0 "\$@"
EOF
chmod +x $RPM_BUILD_ROOT/usr/bin/glx
cat > $RPM_BUILD_ROOT/usr/bin/noglx <<EOF
#!/bin/sh
LD_PRELOAD=%{libdir}/libGL.so.%{mesa_so_version} "\$@"
EOF
chmod +x $RPM_BUILD_ROOT/usr/bin/noglx

## glx
cd glx
#beware of installing the minimun as Mesa version are not the same!
make DESTDIR=$RPM_BUILD_ROOT sysconfdir=/etc/X11 SUBDIRS="libGL servGL" install
#
#prefix=$RPM_BUILD_ROOT/%{prefix} \
#	sysconfdir=$RPM_BUILD_ROOT/etc/X11 \
#	moduledir=$RPM_BUILD_ROOT/%{libdir}/modules \
#	install
cd ..
%endif # glx 

# install GLwrapper
make DESTDIR=$RPM_BUILD_ROOT install -C GLwrapper-%{GLwrapper_version}

cd $RPM_BUILD_ROOT/%{libdir}/
#ln -sf libGL.so.1 libGL.so
#ln -sf libGL.so.%{mesa_so_version} libGL.so.1.4
ln -sf libGLU.so.1 libGLU.so
#ln -sf libGLU.so.1 libGLU.so.3
ln -sf libglut.so.3 libglut.so

# remove any reference to unpackaged file.
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/gl.h
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/glext.h
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/gl_mangle.h
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/osmesa.h
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/svgamesa.h
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/glx.h
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/glx_mangle.h
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/xmesa.h
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/xmesa_x.h
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/xmesa_xf86.h
rm -f $RPM_BUILD_ROOT%{prefix}/include/GL/glxext.h
rm -f $RPM_BUILD_ROOT%{libdir}/libGL.so
rm -f $RPM_BUILD_ROOT%{libdir}/libGL.so.1

# finally clean any .la file with still reference to tmppath.
perl -pi -e "s|\S+$RPM_BUILD_DIR\S*||g" $RPM_BUILD_ROOT/%{libdir}/*.la

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %{libglname} -p /sbin/ldconfig

%postun -n %{libglname} -p /sbin/ldconfig

%post -n %{libgluname} -p /sbin/ldconfig 

%postun -n %{libgluname} -p /sbin/ldconfig

%post -n %{libglutname} -p /sbin/ldconfig 

%postun -n %{libglutname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc docs/COPYRIGHT docs/README docs/COPYING docs/README.*
%doc docs/RELNOTES-3* docs/RELNOTES-4.* docs/VERSIONS
%doc README.GLwrapper glx/docs/README.* glx/docs/overview.txt
%ifarch %{ix86}
/usr/bin/glx
/usr/bin/noglx
%config(noreplace) /etc/X11/glx.conf
%endif
%config(noreplace) /etc/X11/mesa.conf

%files -n %{libglname}
%defattr(-,root,root)
%{libdir}/libGL.so.1.*
%{libdir}/libGLwrapper.so*
%ifarch %{ix86}
%{libdir}/modules/*
%endif

#%files -n %{libglname}-devel
#%defattr(-,root,root)
#%doc docs/COPYRIGHT docs/README docs/README.X11 docs/COPYING docs/DEVINFO
#%doc docs/CONFORM docs/VERSIONS
#%dir %{prefix}/include/GL
#%{prefix}/include/GL/gl.h
#%{prefix}/include/GL/glext.h
#%{prefix}/include/GL/gl_mangle.h
#%{prefix}/include/GL/osmesa.h
#%ifarch %{ix86}
#%{prefix}/include/GL/svgamesa.h
#%endif
#%{prefix}/include/GL/glx.h
#%{prefix}/include/GL/glx_mangle.h
#%{prefix}/include/GL/xmesa.h
#%{prefix}/include/GL/xmesa_x.h
#%{prefix}/include/GL/xmesa_xf86.h
#%{libdir}/libGL.so
#/usr/include/GL

%files -n %{libgluname}
%defattr(-,root,root)
%{libdir}/libGLU.so.*

%files -n %{libglutname}
%defattr(-,root,root)
%{libdir}/libglut.so.*

%files -n %{libgluname}-devel
%defattr(-,root,root)
%{prefix}/include/GL/glu.h
%{prefix}/include/GL/glu_mangle.h
%{libdir}/libGL.la
%{libdir}/libGLU.so
%{libdir}/libGLU.la

%files -n %{libglutname}-devel
%defattr(-,root,root)
%{prefix}/include/GL/glut.h
%{prefix}/include/GL/glutf90.h
%{libdir}/libglut.so
%{libdir}/libglut.la

%changelog
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 5.0.1-8avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 5.0.1-7sls
- minor spec cleanups
- remove %%build_opensls macro
- get rid of redundant docs
- fix some unpackaged file errors
- don't terminate on unpackaged files

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 5.0.1-6sls
- OpenSLS build
- tidy spec
- use %%build_opensls to prevent building demos

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 5.0.1-5mdk
- Rebuild

* Thu Jun 12 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 5.0.1-4mdk
- rebuild for gcc-3.3

* Sat May 24 2003 Stefan van der Eijk <stefan@eijk.nu> 5.0.1-3mdk
- rebuild for new deps
- sort out BuildRequires (binutils and libstdc++-devel are redundant)

* Fri Apr  4 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 5.0.1-2mdk
- hail fpons, file-4.01 was broken, gwegwe said that it had a bad
  behaviour, need to rebuild to have the libraries provides back
- fix fponsux in major version of Mesaglut

* Thu Apr 03 2003 François Pons <fpons@mandrakesoft.com> 5.0.1-1mdk
- 5.0.1.

* Thu Jan 09 2003 François Pons <fpons@mandrakesoft.com> 5.0-3mdk
- added patch from Franscisco Javier Felix.
- updated GLwrapper to prefer /usr/lib/libGL.so.1 (for NVidia GLX support)

* Tue Nov 19 2002 François Pons <fpons@mandrakesoft.com> 5.0-2mdk
- fixed Summary and Description (OpenGL 1.4).
- newer GLwrapper with cosmetic changes and patch6 inside it.

* Mon Nov 18 2002 François Pons <fpons@mandrakesoft.com> 5.0-1mdk
- 5.0 releasing OpenGL 1.4 interface.
- removed files installed but not packaged.
- added libstdc++-devel >= 3.2 for BuildRequires.

* Sun Aug  4 2002 Stefan van der Eijk <stefan@eijk.nu> 4.0.3-6mdk
- Removed unneeded BuildRequires

* Fri Jul 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.3-5mdk
- Automated rebuild with gcc3.2

* Thu Jul 25 2002 François Pons <fpons@mandrakesoft.com> 4.0.3-4mdk
- make sure NDEBUG is defined for GLU.

* Mon Jul 15 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.3-3mdk
- Rpmlint fixes: configure-without-libdir-spec
- Use system libtool.m4 when regenerating configure script. Then,
  apply Patch1 (remove-rpath) to generated configure script.
- Don't care about {html,ps,pdf} docs in glx subdir. Anyway, text doc
  is not even generated. Aka. Nuke useless BuildRequires: tetex-dvips,
  ghostscript.

* Mon Jul 01 2002 François Pons <fpons@mandrakesoft.com> 4.0.3-2mdk
- fixed so version to 1.3.403 instead of 1.3.402.

* Wed Jun 26 2002 François Pons <fpons@mandrakesoft.com> 4.0.3-1mdk
- removed patch12 (no more needed, GGI configuration file location).
- 4.0.3.

* Wed May 15 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.2-5mdk
- Update Patch5 to link with libgcc_s which contains _Unwind_GetIP

* Wed May  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.2-4mdk
- Use %%make
- Patch5: Mesa contains C++ code from libnurbs/internals. So, do link
  libGLU with libsupc++. This also kills the CCLD hack to build demos

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.2-3mdk
- Automated rebuild in gcc3.1 environment

* Tue Apr 30 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.2-2mdk
- Fix build with gcc-3.1. Define CCLD to the C++ linker when building
  the demos, since libGLU contains C++ code.

* Fri Apr 05 2002 François Pons <fpons@mandrakesoft.com> 4.0.2-1mdk
- 4.0.2.

* Thu Jan 31 2002 François Pons <fpons@mandrakesoft.com> 4.0.1-4mdk
- fixed build requires for autoconf2.5.
- added missing doc files.

* Wed Jan 30 2002 François Pons <fpons@mandrakesoft.com> 4.0.1-3mdk
- removed libGL.so.1.3 as GLwrapper use it thinking it is a good
  acceleration (whatever point the link).

* Wed Jan 23 2002 François Pons <fpons@mandrakesoft.com> 4.0.1-2mdk
- fixed GLwrapper to use the right libGL Mesa library.
- using .png icon files.
- added libGL.so.1.3.

* Tue Jan 22 2002 François Pons <fpons@mandrakesoft.com> 4.0.1-1mdk
- 4.0.1.

* Sat Jan 19 2002 Stefan van der Eijk <stefan@eijk.nu> 4.0-3mdk
- BuildRequires

* Thu Nov 08 2001 François Pons <fpons@mandrakesoft.com> 4.0-2mdk
- GL library is now 1.3 instead of 1.2 (thanks to Oden Eriksson).
- updated GLwrapper with 0.1.6.

* Wed Nov 07 2001 François Pons <fpons@mandrakesoft.com> 4.0-1mdk
- 4.0.

* Tue Oct 23 2001 François Pons <fpons@mandrakesoft.com> 3.5-2mdk
- fix libglut3.so.* still in libMesaGLU1.

* Wed Oct 17 2001 François Pons <fpons@mandrakesoft.com> 3.5-1mdk
- synced with hackMesa-3.5 rpm.
- remove old compability symlinks.
- try to fix libtool use.
- split package with better naming.
- updated GLwrapper with 0.1.5.
- disabled SSE (some apps gets SIGFPE on probe).
- 3.5.

* Mon Jul 23 2001 Stefan van der Eijk <stefan@eijk.nu> 3.4.2-2mdk
- BuildRequires:		tcl XFree86-devel

* Fri May 18 2001 François Pons <fpons@mandrakesoft.com> 3.4.2-1mdk
- updated to 3.4.2.

* Tue Mar 27 2001 François Pons <fpons@mandrakesoft.com> 3.4.1-4mdk
- Fixed patch to restore GLU 1.2.
- Fixed reference to obsolete y option of tar to j.

* Sun Mar 18 2001 David BAUDENS <baudens@mandrakesoft.com> 3.4.1-3mdk
- Build with gcc on PPC

* Thu Mar 15 2001 Francis Galiegue <fg@mandrakesoft.com> 3.4.1-2mdk
- Skip utah_glx for ia64

* Thu Feb 15 2001 François Pons <fpons@mandrakesoft.com> 3.4.1-1mdk
- 3.4.1 and remove GLUtesselator patch.

* Wed Jan 24 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.4-8mdk
- patched mach64dmainit.c from CVS. Now /tmp/glx* is
  safely cleaned for mach64 on X exits.

* Tue Jan 02 2001 François Pons <fpons@mandrakesoft.com> 3.4-7mdk
- updated GLwrapper with 0.1.4.

* Sat Dec 31 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.4-6mdk
- added patch for real optimization with RPM_OPT_FLAGS.
- added glXGetProcAddressARB workaround for playing with Tuxracer :-)
- added a soft link to fixed a name typo with common_x86asm.S names
  (for --enable-x86).

* Fri Dec 22 2000 François Pons <fpons@mandrakesoft.com> 3.4-5mdk
- updated glx with 20001222 cvs snapshot (s3savage modification).
- moved mesa.conf to /etc/X11 and make sure Mesa take care of it, ugly.

* Tue Dec 05 2000 François Pons <fpons@mandrakesoft.com> 3.4-4mdk
- updated glx with 20001205 cvs snapshot (s3savage modification).
- created patch for s3savage compilation (just change include dep).

* Sun Nov 26 2000 David BAUDENS <baudens@mandrakesoft.com> 3.4-3mdk
- Fix build on PPC (again): use egcs to don't have a wonderful "Internal
  compilator error" with gcc-2.96

* Tue Nov 07 2000 François Pons <fpons@mandrakesoft.com> 3.4-2mdk
- fixed missing requires on Mesa-common for Mesa-common-devel.
- fixed Copyright (LGPL => MIT).
- updated glx with 20001107 cvs snapshot (version 0.10).
- build with glibc 2.1.97.

* Mon Nov 06 2000 François Pons <fpons@mandrakesoft.com> 3.4-1mdk
- 3.4.

* Thu Oct 19 2000 François Pons <fpons@mandrakesoft.com> 3.3-16mdk
- updated glx to 20001017.
- build release for glibc-2.1.95.

* Mon Oct 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.3-15mdk
- Fix gcc2.96 compilation.

* Fri Sep 29 2000 François Pons <fpons@mandrakesoft.com> 3.3-14mdk
- fixed menu entrie for morph.

* Tue Sep 26 2000 François Pons <fpons@mandrakesoft.com> 3.3-13mdk
- update glx to 20000926 as a lot of change on S3Savage driver has occurs and
  this driver is marked as experimental (at least get latest version as there
  are no more change for some days).

* Sat Sep 09 2000 David BAUDENS <baudens@mandrakesoft.com> 3.3-12mdk
- Fix build for PPC (i.e. remove Patch #1, it's included in sources now)

* Sun Sep 03 2000 François Pons <fpons@mandrakesoft.com> 3.3-11mdk
- added libMesaGL.so.3 symlink.
- added missing icons.
- moved menu file inside spec file.

* Mon Aug 28 2000 David BAUDENS <baudens@mandrakesoft.com> 3.3-10mdk
- Fix menu entries

* Fri Aug 25 2000 François Pons <fpons@mandrakesoft.com> 3.3-9mdk
- really change to glx 20000825, removed obsolete gart_ver.
- rebuild glx-rename patch for new glx.

* Fri Aug 25 2000 François Pons <fpons@mandrakesoft.com> 3.3-8mdk
- updated to GLwrapper 0.1.3 to select support of Mesa extension,
  enable OSMesa and disable XMesa (it breaks hardware acceleration of DRI).
- updated glx to 20000825.
- changed symlink libMesaGL* to true Mesa libraries (avoid wrapper).
- enabled previously disabled agp support for glx.

* Fri Aug 18 2000 François Pons <fpons@mandrakesoft.com> 3.3-7mdk
- updated GLwrapper to 0.1.2, added some missing X Mesa functions.
- removed Mesa-devel as now provided by XFree86-devel.
- removed SVGA support, as Mesa-devel has gone.

* Thu Aug 03 2000 François Pons <fpons@mandrakesoft.com> 3.3-6mdk
- created patch to restore GLUtesselator as needed by some program.
- updated libGLU version to 1.2.
- added GLwrapper README in doc.

* Mon Jul 31 2000 François Pons <fpons@mandrakesoft.com> 3.3-5mdk
- added /usr/include/GL into Mesa-devel.
- added missing glext.h into %{prefix}/include/GL.
- some macroszifications.

* Thu Jul 27 2000 François Pons <fpons@mandrakesoft.com> 3.3-4mdk
- updated GLwrapper to 0.1.1.
- now work with DRI in accelerated.
- removed glide support as it is enabled in XFree 4.0.1.

* Wed Jul 26 2000 François Pons <fpons@mandrakesoft.com> 3.3-3mdk
- created GLwrapper to get a true GL API.
- removed conflict with XFree86 version greater than 4.

* Mon Jul 24 2000 François Pons <fpons@mandrakesoft.com> 3.3-2mdk
- created patch to rename glx.so to glx-3.so as warnings are dumped else.

* Mon Jul 24 2000 François Pons <fpons@mandrakesoft.com> 3.3-1mdk
- 3.3.
- update glx to CVS version of 2000/07/24.
- moved module glx.so to glx-3.so.
- using Mesa-3.2.1 for glx.

* Thu Jun 28 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.2-4mdk
- added conflicts with XFree86 >= 4.0.

* Sat Jun 17 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.2-3mdk
- disabled ggi in ./configure.
- added option to compile with Voodoo glide support.

* Tue Jun 13 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.2-2mdk
- fix: remove need on libggi and libgii

* Sat Jun 10 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.2-1mdk
- updated to version 3.2.
- glx updated to version 2000611.
- disabled MTRR for i386/i486.
- moved glx script to /usr/bin.
- added --disable-glut and --disable-GLU in glx building as the
  respective libraries are already built in the main Mesa tree.

* Tue May 16 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.1-16mdk
- fix fix for i486 to allow compilation on other archs !

* Sun May 14 2000 David BAUDENS <baudens@mandrakesoft.com> 3.1-15mdk
- Fix build for i486
- Clean after build
- Fix some typos

* Sun May  7 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1-14mdk
- added more compatibility links to Mesa for Fermigier

* Fri Apr 28 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1-13mdk
- really fixed hardcoded path

* Fri Apr 28 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1-12mdk
- added 32x32 icons, fixed hardcoded path in menu entries

* Mon Apr 17 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1-11mdk
- added symlinks to libMesaGL and libMesaGLU for compatibility
  with older applications

* Wed Apr 12 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1-10mdk
- fixed group for Mesa-demos
- added menu entries for best demos
- fixed ftp, added url
- added documentation
- patched ltconfig to remove binary-or-shlib-defines-rpath

* Mon Apr  3 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.1-9mdk
- split glut and GLU in common and common-devel packages to ease
  the upgrade to XFree86 4.0.

* Sun Mar 19 2000 John Buswell <johnb@mandrakesoft.com> 3.1-8mdk
- Added patch for PPC arch
- Included PPC in GLX skip
- Added ifarch 

* Fri Jan 28 2000 Francis Galiegue <francis@mandrakesoft.com>
- Added .so symlinks in -devel

* Mon Jan 17 2000 Francis Galiegue <francis@mandrakesoft.com>
- Made demos fully functional

* Mon Jan 17 2000 Francis Galiegue <francis@mandrakesoft.com>
- Also skip svgalib for sparcs

* Thu Jan 13 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.1-4mdk
- Make sure to get the right link.

* Tue Jan 11 2000 Pixel <pixel@mandrakesoft.com>
- fix build for non-svgalib architectures

* Mon Dec 20 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- id k6 chipset as i586 for glx

* Tue Dec 14 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Mesa 3.1 final.
- rewrite files

* Sat Dec 11 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
-  Really fix alpha build (no glx for you)
- and use _tmppath in Buildroot

* Tue Dec 07 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Fix alpha build (i think)
- Clean up .spec (scared chmou, big wuss) ;)
- make cheesie 'glx' script to LD_PRELOAD the libGL.so.1.0 for the demos

* Fri Nov 26 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Update cvs snaps
- Use new --with-chipset=both for glx
- (this is not backwards compatible, you must recompile) don't blame me ask the Mesa people
- use the right --target (must say they did a damned fine job of optimizing the code

* Tue Nov 02 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- add arch's, defattr
- integrate glx (mga_gxl.so, tnt_glx.so)

* Mon Oct 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Back to old Mesa lib.

* Fri Jul 16 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.de>
- remove the -ffast-math removal stuff - Mesa 3.1 works with -ffast-math
  and is actually 11.7% faster than without it.

* Fri Jul 16 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.de>
- 3.1beta2

* Wed Jun 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build in the new environement (rel: 3mdk).

* Thu May 06 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- ldconfig to %post and %postun.

* Mon Feb 15 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- initial RPM; changes to base:
- Handle RPM_OPT_FLAGS
- link with pthread library
