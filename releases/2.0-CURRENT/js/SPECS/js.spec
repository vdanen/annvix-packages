#
# spec file for package js
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		js
%define version		1.5.rc5a
%define release		%_revrel
%define epoch		1

%define srcver		1.5-rc5a
%define major		1
%define libname		%mklibname %{name} %{major}

Summary:	JavaScript engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	MPL
Group:		Development/Other
URL:		http://www.gingerall.com/charlie/ga/xml/d_related.xml
Source0:	%{name}-%{srcver}.tar.bz2
Patch0:		libjs-1.5.patch
Patch1:		js-va_copy.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	multiarch-utils >= 1.0.3

Requires:	%{libname} = %{epoch}:%{version}-%{release}

%description
JavaScript is the Netscape-developed object scripting languages. This
package has been created for purposes of Sablotron and is suitable for 
embedding in applications. See http://www.mozilla.org/js for details 
and sources.


%package -n %{libname}
Summary:	JavaScript engine library
Group:		System/Libraries

%description -n	%{libname}
JavaScript is the Netscape-developed object scripting languages. This
package has been created for purposes of Sablotron and is suitable for 
embedding in applications. See http://www.mozilla.org/js for details 
and sources.


%package -n %{libname}-devel
Summary:	The header files for %{libname}
Group:		Development/Other
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{libname}-devel
These are the header files for %{libname}


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}
pushd src
%patch0 -p0 
popd
%patch1 -p1 -b .va_copy

%build
pushd src
    perl -pi -e "s/-shared/-shared -lc -soname libjs.so.1/;" config/Linux_All.mk

    # undefined symbol errors, so for the moment don't enable stack protection
    #OPTFLAGS="%{optflags} -fno-stack-protector -fPIC"
    OPTFLAGS="%{optflags} -fPIC"

    #JMD: %make does *not* work!
    export CFLAGS="%{optflags} -DPIC -fPIC -D_REENTRANT"
    BUILD_OPT=1 make -f Makefile.ref 
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_bindir},%{_libdir},%{_includedir}/js}

# install headers
install -m 0644 src/*.h %{buildroot}%{_includedir}/js/
install -m 0644 src/Linux_All_OPT.OBJ/jsautocfg.h %{buildroot}%{_includedir}/js/

# install shared library
install -m 0755 src/Linux_All_OPT.OBJ/lib%{name}.so \
    %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -snf lib%{name}.so.%{major} %{buildroot}%{_libdir}/lib%{name}.so

# install static library
install -m 0755 src/Linux_All_OPT.OBJ/lib%{name}.a %{buildroot}%{_libdir}/

# install binary
install -m 0755 src/Linux_All_OPT.OBJ/%{name} %{buildroot}%{_bindir}/

%multiarch_includes %{buildroot}%{_includedir}/js/jsautocfg.h


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%multiarch %{multiarch_includedir}/js/jsautocfg.h
%{_includedir}/js
%{_libdir}/*.so
%{_libdir}/*.a

%files doc
%defattr(-,root,root)
%doc README src/README.html


%changelog
* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.rc5a
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.rc5a
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.rc5a
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.rc5a-2avx
- put the innclude directory back to what it used to be (Mandriva moved
  this due to some conflicts with some mozilla stuff)

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5.rc5a-1avx
- 1.5rc5a
- multiarch support
- we need to use an epoch here anyways, so tag the version as
  1.5.rc5a-1avx rather than 1.5-0.rc5a.1avx

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5-0.rc5.10avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5-0.rc5.9avx
- rebuild

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.5-0.rc5.8avx
- Annvix build
- remove %%build_propolice macro, build with stack protection off by default

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.5-0.rc5.7sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 1.5-0.rc5.6sls
- OpenSLS build
- tidy spec
- use %%build_propolice macro to not build with stack protection due to
  symbol errors again

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
