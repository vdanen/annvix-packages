%define name	sablotron
%define version 0.98
%define release 4sls

%define	altname		Sablot
%define builddir	$RPM_BUILD_DIR/%{altname}-%{version}
%define lib_name_orig	libsablotron
%define lib_major	0
%define lib_name	%mklibname %{name} %{lib_major}

Summary: 	XSLT processor
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	MPL/GPL
Group: 		Development/Other
URL:		http://www.gingerall.cz
Source: 	http://www.gingerall.com:/perl/rd?url=sablot/%{altname}-%{version}.tar.bz2
Patch:		sablot-lib-0.71.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:  expat-devel >= 1.95.2

Requires:	expat >= 1.95.2
Requires:	%{lib_name}

%description
Sablotron is a fast, compact and portable XML toolkit
implementing XSLT, DOM and XPath.

The goal of this project is to create a lightweight,
reliable and fast XML library processor conforming to the W3C
specification, which is available for public and can be used as a base
for multi-platform XML applications.

%package -n %{lib_name}
Summary:	Main library for sablotron
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{version}-%{release}

%description -n %{lib_name}
Contains the library for sablotron.

%package -n %{lib_name}-devel
Summary: 	The development libraries and header files for Sablotron
Requires: 	sablotron = %{version}
Group: 		System/Libraries
Requires: 	%{lib_name} = %{version}
Provides: 	%{lib_name_orig}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
These are the development libraries and header files for Sablotron

%prep
%setup -q -n %{altname}-%{version}
%patch

%build
export CXXFLAGS="${RPM_OPT_FLAGS}"
%configure --prefix=%{_prefix}
%make 
#strip Sablot/engine/.libs/libsablot.a
#strip Sablot/engine/.libs/libsablot.so*

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall prefix=$RPM_BUILD_ROOT/%{_prefix}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(755,root,root)
%{_bindir}/sabcmd
%{_bindir}/sablot-config
%_mandir/man1/*

%files -n %{lib_name}
%defattr(-,root,root)
%doc README RELEASE
%{_libdir}/libsablot.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_includedir}/*.h

%changelog
* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.98-4sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 0.98-3sls
- OpenSLS build
- tidy spec

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.98-2mdk
- rebuild

* Mon Jun  2 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 0.98-1mdk
- 0.98
- fix patch

* Mon Feb 10 2003 Stew Benedict <sbenedict@mandrakesoft.com> 0.97-1mdk
- 0.97 - fixes PPC build, %%mklibname, sablot-config

* Fri Dec 13 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.96-1mdk
- 0.96

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.95-4mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Wed Aug 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.95-3mdk
- fix Provides (thanx to Olivier).

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.95-2mdk
- Automated rebuild with gcc3.2

* Tue Jun 25 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.95-1mdk
- new version 0.95.

* Tue May 28 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.90-2mdk
- rebuild with gcc 3.1.

* Wed Apr 03 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.90-1mdk
- release 0.90.
- patch to add -lexpat and -lstdc++ in libsablot.so (required for php4)

* Mon Feb 04 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.82-1mdk
- release 0.82.

* Wed Jan 16 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.81-1mdk
- release 0.81.
- Removed patch for 0.80.

* Tue Jan 15 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.80-1mdk
- release 0.80.

* Wed Nov 21 2001 Christian Belisle <cbelisle@mandrakesoft.com> 0.71-1mdk
- release 0.71.
- bzip2 the source.
- remove the patch.

* Tue Nov 06 2001 Philippe Libat <philippe@mandrakesoft.com> 0.70-2mdk
- %macros
- move sabcmd in sablotron rpm

* Mon Nov 05 2001 Christian Belisle <cbelisle@mandrakesoft.com> 0.70-1mdk
- first mdk release.

* Tue Sep 18 2001 Petr Cimprich <petr@gingerall.cz>
- sablotron 0.70 RPM release 1

* Wed Aug 15 2001 Petr Cimprich <petr@gingerall.cz>
- sablotron 0.65 RPM release 1

* Thu Jun 14 2001 Petr Cimprich <petr@gingerall.cz>
- sablotron 0.60 RPM release 1
- build under RedHat 7.1 with rpm 4.0.2

* Wed Apr 22 2001 Petr Cimprich <petr@gingerall.cz>
- sablotron 0.52 RPM release 1
- based on 0.51-5 spec by Henri Gomez

* Thu Feb 22 2001 Henri Gomez <hgomez@slib.fr>
- sablotron 0.51 RPM release 5
- apply patch to add -lexpat and -lstdc++ in libsablot.so
  REQUIRED for use with PHP4

* Thu Feb 22 2001 Henri Gomez <hgomez@slib.fr>
- sablotron 0.51 RPM release 4
- follow Redhat way to dispatch between pack and pack-devel

* Tue Feb 20 2001 Henri Gomez <hgomez@slib.fr>
- sablotron 0.51 RPM release 3
- added ldconfig is post/preun and cleanup stuff
- build under Redhat 6.2 + updates with rpm 3.0.5

* Mon Feb 19 2001 Henri Gomez <hgomez@slib.fr>
- sablotron 0.51 RPM release 2
- added Requires expat >= 1.95.1

* Mon Feb 19 2001 Henri Gomez <hgomez@slib.fr>
- sablotron 0.51 RPM release 1
- updated spec file 

