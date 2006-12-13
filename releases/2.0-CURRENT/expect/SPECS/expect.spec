#
# spec file for package expect
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		expect
%define version		5.43.0
%define release		%_revrel
%define epoch		1

%define major		5.43
%define libname		%mklibname %{name} %{major}

Summary:	A tcl extension for simplifying program-script interaction
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License:	BSD
URL:		http://expect.nist.gov/
Source:		http://expect.nist.gov/src/%{name}-%{version}.tar.bz2
Patch0:		expect-5.32.2-random.patch
Patch1:		expect-5.32.2-fixcat.patch
Patch2:		expect-5.32.2-spawn.patch
Patch3:		expect-5.32.2-setpgrp.patch
Patch4:		expect-5.32-libdir.patch
Patch5:		expect-5.43.0.configure.patch
Patch6:		expect-5.43-soname.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	tk
BuildRequires:	tk-devel

Requires:	tcl
Requires:	%{libname} = %{epoch}:%{version}

%description
Expect is a tcl extension for automating interactive applications such
as telnet, ftp, passwd, fsck, rlogin, tip, etc.  Expect is also useful
for testing the named applications.  Expect makes it easy for a script
to control another program and interact with it.

Install the expect package if you'd like to develop scripts which interact
with interactive applications.  You'll also need to install the tcl
package.


%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries

%description -n %{libname}
Expect is a tcl extension for automating interactive applications such
as telnet, ftp, passwd, fsck, rlogin, tip, etc.  Expect is also useful
for testing the named applications.  Expect makes it easy for a script
to control another program and interact with it.

Install the expect package if you'd like to develop scripts which interact
with interactive applications.  You'll also need to install the tcl
package.


%package -n %{libname}-devel 
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{epoch}:%{version}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}

%description -n	%{libname}-devel
This package contains development files for %{name}.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{major}
%patch0 -p1 -b .random
%patch1 -p1 -b .fixcat
%patch2 -p1 -b .spawn
%patch3 -p2
%patch4 -p1 -b .libdir
%patch5
%patch6 -p1


%build
autoconf-2.13

for f in config.guess config.sub ; do
    test -f /usr/share/libtool/$f || continue
    find . -type f -name $f -exec cp /usr/share/libtool/$f \{\} \;
done

chmod u+w testsuite/configure
. %{_libdir}/tclConfig.sh

%configure \
    --enable-gcc \
    --enable-shared \
    --with-tclinclude=$TCL_SRC_DIR

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# If %{_libdir} is not %{_prefix}/lib, then define EXTRA_TCLLIB_FILES
# which contains actual non-architecture-dependent tcl code.
if [ "%{_libdir}" != "%{_prefix}/lib" ]; then
    EXTRA_TCLLIB_FILES="%{buildroot}%{_prefix}/lib/*"
fi

%makeinstall tcl_libdir=%{buildroot}%{_libdir} \
    libdir=%{buildroot}%{_libdir}/expect%{major} \
    TKLIB_INSTALLED="-L%{buildroot}%{_libdir} -ltk" \
    TCLLIB_INSTALLED="-L%{buildroot}%{_libdir} -ltcl"

# fix the shared libname
rm -f %{buildroot}%{_libdir}/lib%{name}%{major}.so*
install -m 0755 lib%{name}%{major}.so %{buildroot}%{_libdir}/lib%{name}%{major}.so.1
ln -snf lib%{name}%{major}.so.1 %{buildroot}%{_libdir}/lib%{name}%{major}.so

# remove cryptdir/decryptdir, as Linux has no crypt command (bug 6668).
rm -f %{buildroot}%{_bindir}/{cryptdir,decryptdir}
rm -f %{buildroot}%{_mandir}/man1/{cryptdir,decryptdir}.1*

# cleanup
rm -f %{buildroot}%{_libdir}/%{name}%{major}/*.a

# (fc) make sure .so files are writable by root
chmod 0755 %{buildroot}%{_libdir}/*.so


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/%{name}%{major}
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%files doc
%doc ChangeLog FAQ HISTORY NEWS README


%changelog
* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.43.0
- 5.43.0
- break out expect from the tcltk package (ala Mandriva)
- need to set epoch as the previous version was 8.x (since it came from tcltk)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
