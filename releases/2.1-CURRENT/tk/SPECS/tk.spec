#
# spec file for package tk
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		tk
%define version		8.4.13
%define release		%_revrel

%define major		8.4
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	Tk GUI toolkit for Tcl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://tcl.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/tcl/%{name}%{version}-src.tar.bz2
Patch0:		tk8.4.11-rpath.diff
Patch1:		tk8.4.11-soname.diff
Requires:	%{libname} = %{version}

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	tcl-devel >= %{version}
BuildRequires:	libx11-devel

Requires:	%{libname} = %{version}

%description
Tk is a X Windows widget set designed to work closely with the tcl
scripting language. It allows you to write simple programs with full
featured GUI's in only a little more time then it takes to write a
text based interface. Tcl/Tk applications can also be run on Windows
and Macintosh platforms.


%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n	%{libname}
Tk is a X Windows widget set designed to work closely with the tcl
scripting language. It allows you to write simple programs with full
featured GUI's in only a little more time then it takes to write a
text based interface. Tcl/Tk applications can also be run on Windows
and Macintosh platforms.


%package -n %{devname} 
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 8.4 -d

%description -n	%{devname}
This package contains development files for %{name}.


%prep
%setup -q -n %{name}%{version}
%patch0 -p0 -b .rpath
%patch1 -p1 -b .soname


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
        --with-tcl=%{_libdir} \
        --includedir=%{_includedir}/tk%{version}
    %make

    cp libtk%{major}.so libtk%{major}.so.0
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
mv %{buildroot}%{_libdir}/libtk%{major}.so %{buildroot}%{_libdir}/libtk%{major}.so.0
ln -snf libtk%{major}.so.0 %{buildroot}%{_libdir}/libtk%{major}.so

# install all headers
install -d %{buildroot}%{_includedir}/tk%{version}/compat
install -d %{buildroot}%{_includedir}/tk%{version}/generic
install -d %{buildroot}%{_includedir}/tk%{version}/unix
install -m 0644 compat/*.h %{buildroot}%{_includedir}/tk%{version}/compat/
install -m 0644 generic/*.h %{buildroot}%{_includedir}/tk%{version}/generic/
install -m 0644 unix/*.h %{buildroot}%{_includedir}/tk%{version}/unix/

pushd %{buildroot}%{_bindir}
    ln -sf wish* wish
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
perl -pi -e "s|-L`pwd`/unix\b|-L%{_libdir}|g" %{buildroot}%{_libdir}/tkConfig.sh
perl -pi -e "s|`pwd`/unix/lib|%{_libdir}/lib|g" %{buildroot}%{_libdir}/tkConfig.sh
perl -pi -e "s|`pwd`|%{_includedir}/tk%{version}|g" %{buildroot}%{_libdir}/tkConfig.sh

# Arrangements for lib64 platforms
echo "# placeholder" >> %{libname}.files
echo "# placeholder" >> %{devname}.files
if [[ "%{_lib}" != "lib" ]]; then
    ln -s %{_libdir}/tkConfig.sh %{buildroot}%{_prefix}/lib/tkConfig.sh
    echo "%{_prefix}/lib/tkConfig.sh" >> %{devname}.files
    echo "%{_libdir}/%{name}%{major}/pkgIndex.tcl" >> %{libname}.files
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

%files -n %{libname} -f %{libname}.files
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{devname} -f %{devname}.files
%defattr(-,root,root)
%dir %{_includedir}/tk%{version}
%dir %{_includedir}/tk%{version}/compat
%dir %{_includedir}/tk%{version}/generic
%dir %{_includedir}/tk%{version}/unix
%attr(0644,root,root) %{_includedir}/tk%{version}/compat/*.h
%attr(0644,root,root) %{_includedir}/tk%{version}/generic/*.h
%attr(0644,root,root) %{_includedir}/tk%{version}/unix/*.h
%attr(0644,root,root) %{_includedir}/*.h
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.a
%attr(0755,root,root) %{_libdir}/tkConfig.sh


%changelog
* Sun Sep 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 8.4.13
- implement devel naming policy
- implement library provides policy

* Thu Apr 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 8.4.13
- build against modular X

* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.4.13
- 8.4.13
- break out tk from the tcltk package (ala Mandriva)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
