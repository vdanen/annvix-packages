Summary:	Glide runtime for 3Dfx Voodoo Banshee and Voodoo3 boards
Name:		Glide_V3-DRI
Version:	cvs
Release:	9mdk
Source0:        glide3x.2002.04.10.tar.bz2
Source1:        swlibs.2001.01.26.tar.bz2
#Debian patches
Patch20:        swlibs-000-makefile-000.bz2
Patch21:        swlibs-001-mcpu-flag.bz2
Patch22:        swlibs-002-automake.bz2
Patch23:        swlibs-003-libm.bz2
Patch24:        swlibs-nomore-csh.bz2
Patch30:        glide3x-autoconf-update.bz2
Patch31:        glide3x-comments-warnings.bz2
Patch32:        glide3x-libtool-patch.bz2
Patch33:        glide3x-build-multiargs.bz2
Patch34:        glide3x-debug-vaargs.bz2
Patch35:        glide3x-preprocessor.bz2
License:        3dfx Glide General Public License
Group:          System/Libraries
BuildRoot:      %_tmppath/%name-%version-%release-buildroot
ExclusiveArch:  %ix86 ia64 alpha
BuildRequires:	XFree86-devel automake1.7 autoconf2.5
URL:		http://glide.sourceforge.net/

%description 
This library allows the user to use a 3dfx Interactive Voodoo Banshee
or Voodoo3 card under Linux with DRI support.  The source support DRI
versions of Glide.

# Glide3 DRI
%package devel
Summary:	Development headers for Glide 3.x
Group:		Development/C
Requires:	%name = %version-%release

%description devel
This package includes the headers files necessary for developing
applications that use the 3Dfx Interactive Voodoo3 card.

%prep
%setup -q -n glide3x -a1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch30 -p2
%patch31 -p2
%patch32 -p2
%patch33 -p2
%patch34 -p2
%patch35 -p2

%build
aclocal-1.7
libtoolize --copy --force
automake-1.7 -a
autoconf-2.5x
# Build for V3 with DRI
%configure2_5x	--enable-fx-glide-hw=h3 \
		--enable-fx-dri-build \
		--enable-fx-debug=no
make -f makefile.autoconf all CFLAGS="$RPM_OPT_FLAGS -ffast-math -fexpensive-optimizations -funroll-loops -O3"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std -f makefile.autoconf
#we don't want these
rm -f $RPM_BUILD_ROOT%{_libdir}/libglide3.*a

%postun
/sbin/ldconfig

%post
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING INSTALL
%{_libdir}/libglide3.so.3.10.0
%{_libdir}/libglide3.so.3

%files devel
%defattr(-, root, root)
%dir %{_includedir}/glide3
%{_includedir}/glide3/*
%{_libdir}/libglide3.so

%changelog
* Thu Sep 04 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> cvs-9mdk
- rebuild

* Sun Jul 27 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> cvs-8mdk
- buildrequires

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> cvs-7mdk
- merge changes from Glide_V5 package:
  o fix build (dropped old patches, updated cvs snapshot, added debian patches, etc.)
  o drop unwanted files
  o compile with $RPM_OPT_FLAGS
  o added %%clean stage
  o rm -rf $RPM_BUILD_ROOT in %%install
  o cleanups
  o build on ia64 & alpha too

* Fri Nov 29 2002 Stefan van der Eijk <stefan@eijk.nu> cvs-6mdk
- BuildRequires: XFree86-devel
- remove unpackaged file
- add %%clean

* Fri Feb  8 2002 Jeff Garzik <jgarzik@mandrakesoft.com> cvs-5mdk
- add URL tag
- add %%doc to -devel rpm
- fix source permissions

* Fri Feb  8 2002 Jeff Garzik <jgarzik@mandrakesoft.com> cvs-4mdk
- Fix ia32 build, by running 'libtoolize -f' in %%prep stage

* Mon May 21 2001 Frederic Lepied <flepied@mandrakesoft.com> cvs-3mdk
- updated cvs snapshot to 20001220

* Wed Jan 03 2001 David BAUDENS <baudens@mandrakesoft.com> cvs-2mdk
- ExclusiveArch: %%ix86
- Spec clean up

* Wed Aug 23 2000 <yoann@mandrakesoft.com> cvs-1mdk
- linux.3dfx.com doesn't distribute Glide RPM / tarball
  containing g3ext.h which is needed to compile XF4.0.1,
  
  This RPM use the Glide CVS tree.
  If something goes wrong, blame the Glide team for not doing release.
