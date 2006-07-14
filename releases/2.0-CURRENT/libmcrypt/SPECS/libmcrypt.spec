#
# spec file for package libmcrypt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libmcrypt
%define version		2.5.7
%define release		%_revrel

%define major		4
%define libname		%mklibname mcrypt %{major}

Summary:	Thread-safe data encryption library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://mcrypt.sourceforge.net/
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}.tar.gz.sig.asc

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtool-devel, multiarch-utils

%description
Libmcrypt is a thread-safe library providing a uniform interface
to access several block and stream encryption algorithms.

Some algorithms which are supported:
SERPENT, RIJNDAEL, 3DES, GOST, SAFER+, CAST-256, RC2, XTEA, 3WAY,
TWOFISH, BLOWFISH, ARCFOUR, WAKE and more. 


%package -n %{libname}
Summary:	Thread-safe data encryption library
Group:		System/Libraries
Requires:	%{name} >= %{version}

%description -n %{libname}
Libmcrypt is a thread-safe library providing a uniform interface
to access several block and stream encryption algorithms.

Some algorithms which are supported:
SERPENT, RIJNDAEL, 3DES, GOST, SAFER+, CAST-256, RC2, XTEA, 3WAY,
TWOFISH, BLOWFISH, ARCFOUR, WAKE and more. 


%package -n %{libname}-devel
Summary:	Header files and libraries for developing apps with libmcrypt
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}

%description -n %{libname}-devel
This package contains the header files and libraries needed to
develop programs that use the libmcrypt library.
Install it if you want to develop such applications.


%package -n %{libname}-static-devel
Summary:	Static libraries for developing apps with libmcrypt
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	%{name}-devel = %{version}
Provides:	%{name}-static-devel = %{version}

%description -n %{libname}-static-devel
This package contains the static libraries needed to
develop programs that use the libmcrypt library.
Install it if you want to develop such applications.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

%build
%serverbuild
#libtoolize --copy --force; aclocal; autoconf

./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --disable-ltdl \
    --disable-ltdl-install \
    --enable-dynamic-loading \
    --enable-static \
    --enable-shared

#    --build %{_target_platform} \
#    --host %{_target_platform} \
#    --target %{_target_platform} \

%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

%multiarch_binaries %{buildroot}%{_bindir}/libmcrypt-config


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_libdir}/%{name}/*.la
%{_libdir}/%{name}/*.so

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%{_mandir}/man3/*
%multiarch %{multiarch_bindir}/libmcrypt-config
%{_bindir}/libmcrypt-config
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/mcrypt.h
%{_datadir}/aclocal/*.m4

%files -n %{libname}-static-devel
%defattr(-, root, root)
%{_libdir}/*.a
%{_libdir}/%{name}/*.a

%files doc
%defattr(-, root, root)
%doc AUTHORS COPYING.LIB ChangeLog INSTALL KNOWN-BUGS NEWS README THANKS TODO doc/README.* doc/*.c


%changelog
* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7-12avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7-11avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7-10avx
- bootstrap build

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7-9avx
- multiarch support
- run make check

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.7-8avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.5.7-7sls
- remove %%prefix
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.5.7-6sls
- OpenSLS build
- tidy spec

* Mon Nov 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.7-5mdk
- new url
- fix invalid-build-requires
- fix explicit-lib-dependency

* Thu Jul 10 2003 Götz Waschk <waschk@linux-mandrake.com> 2.5.7-4mdk
- rebuild for new rpm

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.7-3mdk
- fix requires (put it on the right packages...)
- use the %%mklibname macro
- misc spec file fixes

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.7-2mdk
- fix requires

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.7-1mdk
- 2.5.7
- use the %%configure2_5x macro
- misc spec file fixes

* Fri Apr 25 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.5-3mdk
- fix buildrequires, thanks to Stefan van der Eijks robot

* Sat Jan 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.5-2mdk
- fix provides in new static-devel sub package
 
* Sat Jan 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.5-1mdk
- new version
- new static-devel sub package
- misc spec file fixes

* Mon Oct 21 2002 Götz Waschk <waschk@linux-mandrake.com> 2.5.3-2mdk
- fix libification, move plugins to libmcrypt package

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.3-1mdk
- new version

* Sat Jun  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.1-1mdk
- new version

* Thu Apr 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.0-1mdk
- new version
- misc spec file fixes

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.4.19-1mdk
- 2.4.19.
- added the signature for the .gz package.
- specify to include only libmcrypt files (libltdl was included).

* Sun Dec 23 2001 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.4.18-1mdk
- new version
- misc spec file fixes

* Tue Aug 07 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.4.15-2mdk
- added by Thomas Leclerc <leclerc@linux-mandrake.com> 
	- Provides: made library policy-compliant

* Wed Jul 18 2001 Thomas Leclerc <leclerc@linux-mandrake.com> 2.4.15-1mdk
- Initial Mandrake build

# end of file
