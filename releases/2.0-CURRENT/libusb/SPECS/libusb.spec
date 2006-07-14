#
# spec file for package libusb
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libusb
%define	version		0.1.12
%define	release		%_revrel

%define api		0.1
%define major		4
%define libname		%mklibname usb %{api} %{major}
%define basiclibname	%{name}%{api}

Summary:	Libusb is a library which allows userspace access to USB devices
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://libusb.sf.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/libusb/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Libusb is a library which allows userspace access to USB devices.


%package -n %{libname}
Summary:        Libusb is a library which allows userspace access to USB devices
Group:          System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	%{basiclibname} = %{version}-%{release}

%description -n	%{libname}
Libusb is a library which allows userspace access to USB devices.


%package -n %{libname}-devel
Summary:        Libusb is a library which allows userspace access to USB devices
Group:          Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{basiclibname}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
This package includes the header files and shared libraries
necessary for developing programs which will access USB devices using
the %{name} library.


%package -n %{libname}-static-devel
Summary:        Static libraries for libusb
Group:          Development/C
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	%{basiclibname}-static-devel = %{version}-%{release}
Requires:	%{libname}-devel = %{version}

%description -n	%{libname}-static-devel
This package includes the static libraries necessary for developing
programs which will access USB devices using the %{name} library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x --disable-build-docs
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/libusb-config

# move libs to /%{_lib} for UPS shutdown
mkdir -p %{buildroot}/%{_lib}
pushd %{buildroot}%{_libdir}
    mv *.so.* ../../%{_lib}/
    # run lib_symlinks here so that we can remove what we want afterwards
    %{_datadir}/spec-helper/lib_symlinks
    rm -f libusb*.so.*
    export DONT_SYMLINK_LIBS=1
    # XXX: fix libusb.la if it's used with ltdlopen, i.e. current usage
    # only works to build stuff, aka .so symlink is not dispatched and.
    ln -sf ../../%{_lib}/libusb-%{api}.so.%{major} libusb.so
popd
ln -s ../usr/lib/libusb.la %{buildroot}/%{_lib}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -p /sbin/ldconfig -n %{libname}
%postun -p /sbin/ldconfig -n %{libname}


%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/libusb-config
%multiarch %{multiarch_bindir}/libusb-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
/%{_lib}/*.la

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

%files doc
%defattr(-,root,root)
%doc AUTHORS README INSTALL.libusb NEWS ChangeLog


%changelog
* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.1.12
- 0.1.12
- move *.la into the -devel package
- fix source url
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.1.8
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.1.8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.1.8-1avx
- first Annvix build (required by usbutils)

* Thu Feb 17 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.8-7mdk
- really fix build of other packages (eg: sane, kdegraphics)

* Wed Feb 16 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.8-6mdk
- fix libtoolery

* Mon Jan 31 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.8-5mdk
- fix multiarch support (workaround libtool deficienties)

* Tue Jan 25 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.8-4mdk
- move librarie from /usr/lib into /lib for UPS shutdown

* Sun Jan 23 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.1.8-3mdk
- rebuild
- wipe out buildroot at the beginning of %%install

* Thu Jul 15 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.1.8-2mdk
- add BuildRequires: docbook-dtd31-sgml docbook-style-dsssl

* Wed Jun 02 2004 Abel Cheung <deaddog@deaddog.org> 0.1.8-1mdk
- New version
- Build docs too

* Thu Jul 31 2003 Till Kamppeter <till@mandrakesoft.com> 0.1.7-1mdk
- Updated to 0.1.7 (needed for GPhoto2 2.1.2).

* Wed Jul 09 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.1.6a-5mdk
- rebuild

* Mon May 26 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 0.1.6a-4mdk
- Rebuild

* Mon Apr 14 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.6a-3mdk
- make it %%mklibname aware

* Mon Jul 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.6a-2mdk
- rpmlint fixes

* Tue Jul  2 2002 Till Kamppeter <till@mandrakesoft.com> 0.1.6a-1mdk
- Updated to 0.1.6a (needed for GPhoto2 2.1, contributed by Aaron Peromsik
  <aperomsik@mail.com>).

* Wed Jun 26 2002 Yves Duret <yduret@mandrakesoft.com> 0.1.5-3mdk
- put back the .la in devel.

* Fri May 17 2002 Yves Duret <yduret@mandrakesoft.com> 0.1.5-2mdk
- 9.0 lib policy: added %libname-static-devel
- manual rebuild in gcc3.1 environment :)

* Sat Feb 16 2002 Yves Duret <yduret@mandrakesoft.com> 0.1.5-1mdk
- version 0.1.5
- remove patch0 (disable doc generation) no more needed
- spec clean up, macros...
- fix provides name AND release
- better -devel description

* Thu Jan 31 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.1.4-2mdk
- added Conflicts to ease upgrade

* Mon Jan 28 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.1.4-1mdk
- Release 0.1.4
- Fix name of package to be rpmlint compliant
- Patch0: Disable doc generation, it fails

* Tue Oct 25 2001 Ludovic Francois <lfrancois@mandrakesoft.com> 0.1.3b-2mdk
- Rebuild for rpmlint

* Thu Mar  1 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.1.3b-1mdk
- Initial Mandrake release
