%define lib_release rc5

%define name	js
%define version	1.5
%define release	0.%{lib_release}.5mdk

%define major	1
%define libname %mklibname %{name} %{major}

Summary:	JavaScript engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}-%{lib_release}.tar.bz2
Patch0:		lib%{name}-%{version}.patch.bz2
URL:		http://www.gingerall.com/charlie/ga/xml/d_related.xml
License:	MPL
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	ADVXpackage
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
JavaScript is the Netscape-developed object scripting languages. This
package has been created for purposes of Sablotron and is suitable for 
embedding in applications. See http://www.mozilla.org/js for details 
and sources.

%package -n	%{libname}
Summary:	JavaScript engine library
Group:		System/Libraries
Provides:	ADVXpackage

%description -n	%{libname}
JavaScript is the Netscape-developed object scripting languages. This
package has been created for purposes of Sablotron and is suitable for 
embedding in applications. See http://www.mozilla.org/js for details 
and sources.

%package -n	%{libname}-devel
Summary:	The header files for %{libname}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:       ADVXpackage

%description -n	%{libname}-devel
These are the header files for %{libname}

%prep

%setup -q -n %{name}
cd src
%patch0 -p0 

%build
cd src
perl -pi -e "s/-shared/-shared -lc -soname libjs.so.1/;" config/Linux_All.mk
#JMD: %make does *not* work!
BUILD_OPT=1 CFLAGS="%{optflags} -fPIC" make -f Makefile.ref 

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}/js

# install headers
install -m644 src/*.h %{buildroot}%{_includedir}/js/
install -m644 src/Linux_All_OPT.OBJ/jsautocfg.h %{buildroot}%{_includedir}/js/

# install shared library
install -m755 src/Linux_All_OPT.OBJ/lib%{name}.so \
    %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -snf lib%{name}.so.%{major} %{buildroot}%{_libdir}/lib%{name}.so

# install static library
install -m755 src/Linux_All_OPT.OBJ/lib%{name}.a %{buildroot}%{_libdir}/

# install binary
install -m755 src/Linux_All_OPT.OBJ/%{name} %{buildroot}%{_bindir}/

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%{_bindir}/*

%files -n %{libname}
%defattr(-,root,root)
%doc src/README.html
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc README
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%changelog
* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 1.5-0.rc5.5mdk
- Rebuild to fix bad signature

* Sat Jul 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.5-0.rc5.4mdk
- make it provide
- misc spec file fixes

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.5-0.rc5.3mdk
- Fix invalid-packager rpmlint error
- add -q to %%setup

* Sun Feb 09 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.5-0.rc5.2mdk
- fix %mklibname on ppc 
- (Don't try to understand, without this change, build failed)

* Sat Jan 18 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.5-0.rc5.1mdk
- Make rpmlint happy
- use %%mklibname

* Sat Jan 18 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.5rc4-3mdk
- Add to Mandrake since it's needed by php-xslt

* Fri Jan 18 2002 Henri Gomez <hgomez@slib.fr>
* 1.5-rc4 RPM release 2
- added missing jsautocfg.h in include (needed by sablotron)

* Thu Jan 17 2002 Henri Gomez <hgomez@slib.fr>
* 1.5-rc4
- full rebuild

* Tue Dec 18 2001 Petr Cimprich <petr@gingerall.cz>
- JavaScript 1.5_rc3a RPM release 1
