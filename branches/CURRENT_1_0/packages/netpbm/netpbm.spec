%define name	netpbm
%define version 9.24
%define release 10avx

%define major			9
%define libname	%mklibname	%{name} %{major}
%define	libname_devel		%{libname}-devel
%define libname_static_devel	%{libname}-static-devel


Summary:	Tools for manipulating graphics files in netpbm supported formats
Name:		%name
Version:	%version
Release:	%release
License:	GPL Artistic MIT
Group:		Graphics
URL:		http://netpbm.sourceforge.net/
Source0:	netpbm-%version-nojbig.tar.bz2
Source1:	mf50-netpbm_filters
Source2:	test-images.tar.bz2
Patch0:		netpbm-9.8-install.patch.bz2
Patch1:		netpbm-9.9-time.patch.bz2
Patch2: 	netpbm-9.24-struct.patch.bz2
Patch3:		netpbm-9.24-security-ac.patch
Patch4:		netpbm-9.24-lib64.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	flex, png-devel, jpeg-devel, tiff-devel, perl

Requires:	%{libname} = %version-%release
Obsoletes:	libgr-progs, libgr1-progs
Provides:	libgr-progs, libgr1-progs

%description
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.

%package -n %{libname}
Summary:        A library for handling different graphics file formats
Group:          System/Libraries
Provides:	lib%name
Provides:	libgr, libgr1, libnetpbm1
Obsoletes:      libgr, libgr1, libnetpbm1

%description -n %{libname}
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.

%package -n %{libname_devel}
Summary:	Development tools for programs which will use the netpbm libraries
Group:		Development/C
Requires:	%{libname} = %version-%release
Provides:	lib%{name}-devel
Obsoletes:	libgr-devel, libgr1-devel, libnetpbm1-devel
Provides:	libgr-devel, libgr1-devel, libnetpbm1-devel, netpbm-devel

%description -n %{libname_devel}
The netpbm-devel package contains the header files and programmer's
documentation for developing programs which can handle the various
graphics file formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the
graphics file formats supported by the netpbm libraries. You'll also
need to have the netpbm package installed.


%package -n %{libname_static_devel}
Summary:	Static libraries for the netpbm libraries
Group:		Development/C
Requires:	%{libname}-devel = %version-%release
Provides:	lib%{name}-static-devel
Obsoletes:	libgr-static-devel, libgr1-static-devel, libnetpbm1-static-devel
Provides:	libgr-static-devel, libgr1-static-devel, libnetpbm1-static-devel, netpbm-static-devel

%description -n %{libname_static_devel}
The netpbm-devel package contains the staic libraries (.a)
for developing programs which can handle the various
graphics file formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the
graphics file formats supported by the netpbm libraries. You'll also
need to have the netpbm package installed.


%prep
%setup -q -a 2
%patch0 -p1 -b .install
%patch1 -p1 -b .time
%patch2 -p1 -b .struct
%patch3 -p1 -b .security
%patch4 -p1 -b .lib64

mv shhopt/shhopt.h shhopt/pbmshhopt.h
perl -pi -e 's|shhopt.h|pbmshhopt.h|g' `find -name "*.c" -o -name "*.h"` ./GNUmakefile

tar xjf %{SOURCE2}

%build
./configure <<EOF




/usr





EOF

TOP=`pwd`
make \
	CC=%{__cc} \
	CFLAGS="$RPM_OPT_FLAGS -fPIC" \
	LDFLAGS="-L$TOP/pbm -L$TOP/pgm -L$TOP/pnm -L$TOP/ppm" \
	JPEGINC_DIR=%{_includedir} \
	PNGINC_DIR=%{_includedir} \
	TIFFINC_DIR=%{_includedir}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# thanx redhat
# Nasty hack to work around a useless ldconfig script
rm -f buildtools/try_ldconfig
ln -sf /bin/true buildtools/try_ldconfig

mkdir -p %buildroot/usr/share/printconf/mf_rules
cp %{SOURCE1} %buildroot/usr/share/printconf/mf_rules/

mkdir -p %buildroot/usr/share/printconf/tests
cp test-images/* %buildroot/usr/share/printconf/tests/

PATH="`pwd`:${PATH}" make install \
	JPEGINC_DIR=%buildroot/%{_includedir} \
	PNGINC_DIR=%buildroot/%{_includedir} \
	TIFFINC_DIR=%buildroot/%{_includedir} \
	INSTALL_PREFIX=%buildroot/%{_prefix} \
	INSTALLBINARIES=%buildroot/%{_bindir} \
	INSTALLHDRS=%buildroot/%{_includedir} \
	INSTALLLIBS=%buildroot/%{_libdir} \
	INSTALLSTATICLIBS=%buildroot/%{_libdir} \
	INSTALLDATA=%buildroot/%{_datadir}/%{name}-%{version} \
	INSTALLMANUALS1=%buildroot/%{_mandir}/man1 \
	INSTALLMANUALS3=%buildroot/%{_mandir}/man3 \
	INSTALLMANUALS5=%buildroot/%{_mandir}/man5

# Install header files.
mkdir -p %buildroot/%{_includedir}
install -m644 pbm/pbm.h %buildroot/%{_includedir}/
#install -m644 pbmplus.h %buildroot/%{_includedir}/
install -m644 pgm/pgm.h %buildroot/%{_includedir}/
install -m644 pnm/pnm.h %buildroot/%{_includedir}/
install -m644 ppm/ppm.h %buildroot/%{_includedir}/
install -m644 shhopt/pbmshhopt.h %buildroot/%{_includedir}/

# Install the static-only librle.a
install -m644 urt/{rle,rle_config}.h %buildroot/%{_includedir}/
install -m644 urt/librle.a %buildroot/%{_libdir}/

# Fixup symlinks.
ln -sf gemtopnm %buildroot/%{_bindir}/gemtopbm
ln -sf pnmtoplainpnm %buildroot/%{_bindir}/pnmnoraw
rm -f %buildroot/%{_libdir}/libpbm.so
rm -f %buildroot/%{_libdir}/libpgm.so
rm -f %buildroot/%{_libdir}/libpnm.so
rm -f %buildroot/%{_libdir}/libppm.so
ln -sf libpbm.so.9 %buildroot/%{_libdir}/libpbm.so
ln -sf libpgm.so.9 %buildroot/%{_libdir}/libpgm.so
ln -sf libpnm.so.9 %buildroot/%{_libdir}/libpnm.so
ln -sf libppm.so.9 %buildroot/%{_libdir}/libppm.so


# Fixup perl paths in the two scripts that require it.
perl -pi -e 's^/bin/perl^%{__perl}^' %buildroot/%{_bindir}/{ppmfade,ppmshadow}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post   -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files 	-n %{libname}
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/lib*.so.*
%doc COPYRIGHT.PATENT GPL_LICENSE.txt HISTORY README 

%files 	-n %{libname_devel}
%defattr(-,root,root)
%doc Netpbm.programming
%{_includedir}/*.h
%attr(755,root,root) %{_libdir}/lib*.so
%{_mandir}/man3/*

%files 	-n %{libname_static_devel}
%defattr(-,root,root)
%{_libdir}/*.a

%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man[15]/*
%{_datadir}/%{name}-%{version}/*.map
%_datadir/printconf/mf_rules/*
%_datadir/printconf/tests/*


%changelog
* Tue Jun 22 2004 Vincent Danen <vdanen@annvix.org> 9.24-10avx
- require packages not files
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 9.24-9sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 9.24-8sls
- OpenSLS build
- tidy spec

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.24-7mdk
- Patch4: lib64 fixes
- Factor out mklibname invocations
- Provides: netbpm{,-static}-devel
- BuildRequires: jpeg-devel, tiff-devel

* Fri May 23 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 9.24-6mdk
- spec file changes (Per Øyvind Karlsen <peroyvind@sintrax.net>)
	use %mklibname
	added licenses(also released under Artistic and MIT)

* Tue Apr 1 2003 Vincent Danen <vdanen@mandrakesoft.com> 9.24-5mdk
- security patches

* Sun Jul  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.24-4mdk
- Move mapfiles to %_datadir/%name-%version/

* Mon Jul 01 2002 Yves Duret <yduret@mandrakesoft.com> 9.24-3mdk
- fix obsolets/provides of static-devel package thanx Frederic Crozat.

* Fri May 17 2002 Yves Duret <yduret@mandrakesoft.com> 9.24-2mdk
- 9.0 lib policy: added %libname-static-devel

* Fri Apr 19 2002 Yves Duret <yduret@mandrakesoft.com> 9.24-1mdk
- version 9.24.
- merged with redhat.
- fixed build (why are still some guys that does not use GNU autotools ??)
- added missing files.
- buildrequires

* Sun Jan 27 2002 Stefan van der Eijk <stefan@eijk.nu> 9.20-2mdk
- BuildRequires

* Tue Jan 22 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 9.20-1mdk
- Merge with RH.
- 9.20 (whooooooooooo).

* Wed Oct 10 2001 Till Kamppeter <till@mandrakesoft.com> 9.10-8mdk
- Another attempt to recompile it with libpng3

* Fri Oct 05 2001 Yves Duret <yduret@mandrakesoft.com> 9.10-7mdk
- recompiled with libpng3
- macros

* Sat Sep 09 2001 David BAUDENS <baudens@mandrakesoft.com> 9.10-6mdk
- Fix %%major number
- Requires %%version-%%release and not only %%version
- Fix %%doc

* Mon Aug 27 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.10-5mdk
- Explicitly use /sbin/ldconfig

* Wed Aug 08 2001 Yves Duret <yduret@mandrakesoft.com> 9.10-4mdk
- added a builrequires to zlib-devel (Buchan Milne <bgmilne@cae.co.za>)
- corrected the 4 no-ldconfig-symlink errors (thx titi)

* Fri Jul 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 9.10-3mdk
- added missing obsoletes on libgr1-progs

* Fri Jul 27 2001 Yves Duret <yduret@mandrakesoft.com> 9.10-2mdk
- added patch2 to fix bad include netpbm-shhopt.h
- added provides libgr

* Tue Jul 24 2001 Yves Duret <yduret@mandrakesoft.com> 9.10-1mdk
- first MandrakeSoft package (stolen from d3bi4n and PLD)
    Obsoletes libgr libgr-progs libgr-devel
