%define name	gmp
%define version	4.1.2
%define release	3mdk

%define lib_major	3
%define lib_name_orig	%mklibname %{name}
%define lib_name	%{lib_name_orig}%{lib_major}

Summary:	A GNU arbitrary precision library
Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://www.swox.com/gmp/

Source:		ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.bz2
Patch0:		gmp-4.1-x86_64.patch.bz2
Patch1:		gmp-4.1-gcc-version.patch.bz2
Patch2:		gmp-4.1.2-mpz_gcd_ui-retval.patch.bz2

License:	LGPL 
Group:		System/Libraries
BuildRoot:	%_tmppath/%name-%version-%release-root

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands.

GNU MP is fast for several reasons:
   - it uses fullwords as the basic arithmetic type,
   - it uses fast algorithms,
   - it carefully optimizes assembly code for many CPUs' most common
     inner loops
   - it generally emphasizes speed over simplicity/elegance in its
     operations

%package -n %{lib_name}
Summary:	A GNU arbitrary precision library
Group:		System/Libraries

%description -n %{lib_name}
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands.

GNU MP is fast for several reasons:
  - it uses fullwords as the basic arithmetic type,
  - it uses fast algorithms
  - it carefully optimizes assembly code for many CPUs' most common
    inner loops
  - it generally emphasizes speed over simplicity/elegance in its
    operations

%package -n %{lib_name}-devel
Summary:	Development tools for the GNU MP arbitrary precision library
Group:		Development/C
PreReq:		/sbin/install-info
Requires:	%{lib_name} = %version-%release
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
The static libraries, header files and documentation for using the GNU MP
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%prep
%setup -q
# Don't bother touching to configure.in for the following two
# patches. Instead, patch out configure directly.
%patch0 -p1 -b .x86_64
%patch1 -p1 -b .gcc-version
%patch2 -p1 -b .mpz_gcd_ui-retval

%build
%define __libtoolize /bin/true
%configure
%make
# All tests must pass
%make check

%install
install -d %buildroot/%_libdir %buildroot/%_infodir %buildroot/%_includedir
%makeinstall
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%post -n %{lib_name}-devel
%_install_info %{name}.info

%preun -n %{lib_name}-devel
%_remove_install_info %{name}.info

%clean
rm -fr %buildroot

%files -n %{lib_name}
%defattr(-,root,root)
%doc COPYING.LIB NEWS README
%{_libdir}/libgmp.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc doc demos
%{_libdir}/libgmp.so
%{_libdir}/libgmp.a
%{_libdir}/libgmp.la 
%{_includedir}/gmp.h
#%{_includedir}/gmp-mparam.h
%{_infodir}/gmp.info*

%changelog
* Thu Jul 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1.2-3mdk
- Fix libification
- Patch2: Fix mpz_gcd_ui() on longlong limb systems (upstream patch)

* Thu Jul 10 2003 Götz Waschk <waschk@linux-mandrake.com> 4.1.2-2mdk
- rebuild for new rpm

* Wed Jan 22 2003 Warly <warly@mandrakesoft.com> 4.1.2-1mdk
- new version

* Mon Dec  2 2002 Warly <warly@mandrakesoft.com> 4.1.1-1mdk
- new version

* Sun Jul  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1-3mdk
- Patch4: Nuke broken assert in randraw.c (upstream patch)

* Thu Jul  4 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.1-2mdk
- Patch1: Correctly check for gcc version
- Patch2: Don't inline fudge() in t-cmp_d since gcc 3.1+ is now too
  smart at inlining C, thus rendering the "fudge" inoperant
- Patch3: Fix t-scanf. i.e. Don't assume va-functions (<things>, ...)
  are equivalent to (<things>, void *)

* Mon Jul  3 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.1-1mdk
- New and shiny gmp aka bump release.
- Remove patch for ia64 --it seems to be already integrated.
- %%configure-ize.

* Thu Jun 27 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-8mdk
- Libtoolize to get updated config.guess.
- Make check in %%build stage.

* Fri May 24 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.1.1-7mdk
- License should be LGPL.

* Mon Oct 29 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-6mdk
- Patch1: get_str.c: decrement s pointer until it's below or equal to
  str, not simply equal to str. For some reason, that pointer could
  have been already set to something below str. This is a workaround
  to Sawfish crashes on IA-64, under Gnome for example.

* Thu Oct 25 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-5mdk
- Patch0: Fix IA-64 support (RH patch)
- Make rpmlint happier and fix:
  - E: gmp description-line-too-long
  - W: gmp strange-permission gmp.spec 0664

* Thu Aug 30 2001 Warly <warly@mandrakesoft.com> 3.1.1-4mdk
- some rpmlint fixes

* Sun Mar 18 2001 David BAUDENS <baudens@mandrakesoft.com> 3.1.1-3mdk
- Fix build on PPC
- Requires: %%version-%%release and not only %%version

* Tue Mar 13 2001 Warly <warly@mandrakesoft.com> 3.1.1-2mdk
- fix optimizations flag not used

* Mon Mar  5 2001 Warly <warly@mandrakesoft.com> 3.1.1-1mdk
- new version

* Fri Jan 12 2001 Francis Galiegue <fg@mandrakesoft.com> 2.0.2-17mdk

- Fixed file list
- Some spec file changes
- Fixed Requires

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.2-16mdk
- fix bad script

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.2-15mdk
- BM
- add doc

* Thu Jul 13 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 2.0.2-14mdk
- makeinstall macro
- macroszifications

* Sat Mar 25 2000 Daouda Lo <daouda@mandrasoft.com> 2.0.2-13mdk
- fix group

* Sun Nov 28 1999 John Buswell <johnb@mandrakesoft.com>
- Added PPC support

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Release version.

* Tue Jul 22 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- add french description

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- .spec optimizations

* Thu Feb 11 1999 Michael Johnson <johnsonm@redhat.com>
- include the private header file gmp-mparam.h because several
  apps seem to assume that they are building against the gmp
  source tree and require it.  Sigh.

* Tue Jan 12 1999 Michael K. Johnson <johnsonm@redhat.com>
- libtoolize to work on arm

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
- yet another touch of the spec file

* Wed Sep  2 1998 Michael Fulbright <msf@redhat.com>
- looked over before inclusion in RH 5.2

* Sat May 24 1998 Dick Porter <dick@cymru.net>
- Patch Makefile.in, not Makefile
- Don't specify i586, let configure decide the arch

* Sat Jan 24 1998 Marc Ewing <marc@redhat.com>
- started with package from Toshio Kuratomi <toshiok@cats.ucsc.edu>
- cleaned up file list
- fixed up install-info support
