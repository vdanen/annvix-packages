#
# spec file for package tcl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/   
#
# $Id$

%define revision	$Rev$
%define name		tcl
%define version		8.4.13
%define release		%_revrel

%define major		8.4
%define libname		%mklibname %{name} %{major}

Summary:	An embeddable scripting language
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License:	BSD
URL:		http://tcl.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/tcl/%{name}%{version}-src.tar.bz2
Patch0:		tcl-8.4.11-rpath.patch
Patch1:		tcl8.4.11-soname.diff
Patch2:		tcl-8.4.2-dlopen.patch
Patch3:		tcl-8.4.12-lib64-auto_path.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	%{libname} = %{version}

%description
Tcl is a simple scripting language designed to be embedded into
other applications.  Tcl is designed to be used with Tk, a widget
set, which is provided in the tk package.  This package also includes
tclsh, a simple example of a Tcl application.


%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries

%description -n %{libname}
Tcl is a simple scripting language designed to be embedded into
other applications.  Tcl is designed to be used with Tk, a widget
set, which is provided in the tk package.  This package also includes
tclsh, a simple example of a Tcl application.


%package -n %{libname}-devel 
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel = %{version}

%description -n	%{libname}-devel
This package contains development files for %{name}.


%prep
%setup -q -n %{name}%{version}
%patch0 -p0 -b .rpath
%patch1 -p1 -b .soname
%patch2 -p1 -b .dlopen
%patch3 -p1 -b .lib64


%build
pushd unix
    for f in config.guess config.sub ; do
        test -f /usr/share/libtool/$f || continue
        find . -type f -name $f -exec cp /usr/share/libtool/$f \{\} \;
    done
    autoconf-2.13
    %configure \
        --enable-gcc \
        --enable-threads \
        --enable-64bit \
        --includedir=%{_includedir}/tcl%{version}
    %make

    cp libtcl%{major}.so libtcl%{major}.so.0
#    make test
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# If %{_libdir} is not %{_prefix}/lib, then define EXTRA_TCLLIB_FILES
# which contains actual non-architecture-dependent tcl code.
if [ "%{_libdir}" != "%{_prefix}/lib" ]; then
    EXTRA_TCLLIB_FILES="%{buildroot}%{_prefix}/lib/*"
fi

%makeinstall -C unix

# fix libname
mv %{buildroot}%{_libdir}/libtcl%{major}.so %{buildroot}%{_libdir}/libtcl%{major}.so.0
ln -snf libtcl%{major}.so.0 %{buildroot}%{_libdir}/libtcl%{major}.so

# install all headers
install -d %{buildroot}%{_includedir}/tcl%{version}/compat
install -d %{buildroot}%{_includedir}/tcl%{version}/generic
install -d %{buildroot}%{_includedir}/tcl%{version}/unix
install -m 0644 compat/*.h %{buildroot}%{_includedir}/tcl%{version}/compat/
install -m 0644 generic/*.h %{buildroot}%{_includedir}/tcl%{version}/generic/
install -m 0644 unix/*.h %{buildroot}%{_includedir}/tcl%{version}/unix/

pushd %{buildroot}%{_bindir}
    ln -fs tclsh* tclsh
popd

pushd %{buildroot}%{_libdir}
cat > lib%{name}.so << EOF
/* GNU ld script
   We want -l%{name} to include the actual system library,
   which is lib%{name}%{major}.so.0  */
INPUT ( -l%{name}%{major} )
EOF
popd

# fix config script
perl -pi -e "s|-L`pwd`/unix\b|-L%{_libdir}|g" %{buildroot}%{_libdir}/tclConfig.sh
perl -pi -e "s|`pwd`/unix/lib|%{_libdir}/lib|g" %{buildroot}%{_libdir}/tclConfig.sh
perl -pi -e "s|`pwd`|%{_includedir}/tcl%{version}|g" %{buildroot}%{_libdir}/tclConfig.sh

# Arrangements for lib64 platforms
echo "# placeholder" >> %{libname}-devel.files
if [[ "%{_lib}" != "lib" ]]; then
    ln -s %{_libdir}/tclConfig.sh %{buildroot}%{_prefix}/lib/tclConfig.sh
    echo "%{_prefix}/lib/tclConfig.sh" >> %{libname}-devel.files
fi

# (fc) make sure .so files are writable by root
chmod 0755 %{buildroot}%{_libdir}/*.so*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -p /sbin/ldconfig -n %{libname}
%postun -p /sbin/ldconfig -n %{libname}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_prefix}/lib/%{name}%{major}
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/mann/*

%files -n %{libname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname}-devel -f %{libname}-devel.files
%defattr(-,root,root)
%dir %{_includedir}/tcl%{version}
%dir %{_includedir}/tcl%{version}/compat
%dir %{_includedir}/tcl%{version}/generic
%dir %{_includedir}/tcl%{version}/unix
%attr(0644,root,root) %{_includedir}/tcl%{version}/compat/*.h
%attr(0644,root,root) %{_includedir}/tcl%{version}/generic/*.h
%attr(0644,root,root) %{_includedir}/tcl%{version}/unix/*.h
%attr(0644,root,root) %{_includedir}/*.h
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.a
%attr(0755,root,root) %{_libdir}/tclConfig.sh


%changelog
* Mon May 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 8.4.13
- versioned provides

* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.4.13
- 8.4.13
- break out tcl from the tcltk package (ala Mandriva)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
