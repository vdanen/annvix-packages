#
# spec file for package module-init-tools
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		module-init-tools
%define version		3.3
%define release		%_revrel
%define realver		%{version}-pre11

%define major		0
%define libname		%mklibname modprobe %{major}
%define devname		%mklibname modprobe -d

%define _bindir		/bin
%define _sbindir	/sbin
%define _libdir		/lib
%define _libexecdir	/lib

Summary: 	Tools for managing Linux kernel modules
Name:		module-init-tools
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.kerneltools.org/pub/downloads/module-init-tools/
Source0:	ftp://ftp.kernel.org/pub/linux/kernel/people/rusty/modules/%{name}-%{realver}.tar.bz2
Source1:	module-init-tools-man.tar.bz2
Source2:	blacklist-mdv
Source3:	modprobe.default
Source4:	modprobe.compat
Source5:	modprobe.preload
Source6:	blacklist-compat
Patch1:		module-init-tools-libify.patch
Patch2: 	module-init-tools-3.2-pre8-dont-break-depend.patch
Patch3:		module-init-tools-3.2-pre8-all-defaults.patch
Patch7:		module-init-tools-3.2-pre8-modprobe-default.patch
Patch8:		module-init-tools-3.2.2-generate-modprobe.conf-no-defaults.patch
Patch9:		module-init-tools-3.0-failed.unknown.symbol.patch
Patch10:	module-init-tools-3.3-pre11-insmod-strrchr.patch
Patch11:	module-init-tools-libify-2.patch
Patch12:	module-init-tools-3.3-pre11-avx-no-docbook2man.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf
BuildRequires:	glibc-static-devel
BuildRequires:	zlib-devel
BuildRequires:	dietlibc-devel

Obsoletes:	modutils
Conflicts:	modutils < 2.4.22-10mdk
Conflicts:	devfsd < 1.3.25-31mdk


%description
This package contains a set of programs for loading, inserting, and
removing kernel modules for Linux (versions 2.5.47 and above). It
serves the same function that the "modutils" package serves for Linux
2.4.


%package -n %{libname}
Summary:	Library for %{name}
Group: 		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
Library for %{name}.


%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	modprobe-devel = %{version}-%{release}

%description -n %{devname}
Development files for %{name}


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{realver}
%patch1 -p1 -b .lib
%patch2 -p1 -b .dont-break-depend
%patch3 -p1 -b .all-defaults
%patch7 -p1 -b .modprobe-default
%patch8 -p1 -b .generate-modprobe.conf-no-defaults
%patch9 -p1 -b .failed-symb
%patch10 -p1 -b .fix_insmod_strrchr
%patch11 -p1 -b .liberror
%patch12 -p0 -b .no-docbook2man


%build
%serverbuild
rm -f Makefile{,.in}
libtoolize -c
aclocal --force
automake -c -f
autoconf

mkdir -p objs-diet
pushd objs-diet
    %ifarch x86_64
    COMP="diet x86_64-annvix-linux-gnu-gcc"
    %else
    COMP="diet gcc"
    %endif
    CONFIGURE_TOP=.. %configure2_5x --enable-zlib --disable-shared
    %make CFLAGS="-Os" CC="$COMP"
popd


mkdir -p objs
pushd objs
    CONFIGURE_TOP=.. %configure2_5x --enable-zlib
     %make CFLAGS="%{optflags} -fPIC"
popd

pushd doc
    tar xvjf %{_sourcedir}/module-init-tools-man.tar.bz2
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

pushd objs
    %makeinstall transform=
    mv %{buildroot}%{_bindir}/lsmod %{buildroot}%{_sbindir}
popd

install -d %{buildroot}%{_prefix}/lib/dietlibc/lib-%{_arch}
install objs-diet/.libs/libmodprobe.a %{buildroot}%{_prefix}/lib/dietlibc/lib-%{_arch}/libmodprobe.a

mkdir -p %{buildroot}{%{_includedir},%{_mandir}/man{5,8}}
install -m 0644 modprobe.h list.h %{buildroot}%{_includedir}
install -m 0644 doc/*.5 %{buildroot}%{_mandir}/man5/
install -m 0644 doc/*.8 %{buildroot}%{_mandir}/man8/

%ifarch %{ix86}
rm -f %{buildroot}%{_sbindir}/insmod.static
%endif

mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d
touch %{buildroot}%{_sysconfdir}/modprobe.conf
install -m 0644 %{_sourcedir}/modprobe.preload %{buildroot}%{_sysconfdir}
install -m 0644 %{_sourcedir}/blacklist-compat %{buildroot}%{_sysconfdir}/modprobe.d
install -m 0644 %{_sourcedir}/blacklist-mdv %{buildroot}%{_sysconfdir}/modprobe.d/blacklist-avx

mkdir -p %{buildroot}%{_libdir}/module-init-tools
install -m 0644 %{_sourcedir}/modprobe.default %{buildroot}%{_libdir}/module-init-tools
install -m 0644 %{_sourcedir}/modprobe.compat %{buildroot}%{_libdir}/module-init-tools


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post
if [ ! -s %{_sysconfdir}/modprobe.conf ]; then
    MODPROBE_CONF=%{_sysconfdir}/modprobe.conf
elif [ -e %{_sysconfdir}/modprobe.conf.rpmnew ]; then
    MODPROBE_CONF=%{_sysconfdir}/modprobe.conf.rpmnew
fi

if [ -s %{_sysconfdir}/modules.conf -a -n "$MODPROBE_CONF" ]; then
    echo '# This file is autogenerated from %{_sysconfdir}/modules.conf using generate-modprobe.conf command' >> $MODPROBE_CONF
    echo >> $MODPROBE_CONF
    %{_sbindir}/generate-modprobe.conf >> $MODPROBE_CONF 2> /dev/null
fi

if [ -s %{_sysconfdir}/modprobe.conf ]; then
    perl -pi -e 's/(^\s*include\s.*modprobe\.(default|compat).*)/# This file is now included automatically by modprobe\n# $1/' %{_sysconfdir}/modprobe.conf
fi
exit 0


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/modprobe.conf
%config(noreplace) %{_sysconfdir}/modprobe.preload
%dir %{_sysconfdir}/modprobe.d/
%config(noreplace) %{_sysconfdir}/modprobe.d/*
%dir %{_libdir}/module-init-tools
%{_libdir}/module-init-tools/*
%{_sbindir}/*
%{_mandir}/*/*

%files -n %{devname}
%defattr(-,root,root)
%_includedir/*.h
%{_libdir}/libmodprobe.a
%{_prefix}/lib/dietlibc/lib-%{_arch}/libmodprobe.a
%{_libdir}/libmodprobe.la
%{_libdir}/libmodprobe.so

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libmodprobe.so.*


%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README 
%doc TODO stress_modules.sh


%changelog
* Sun Oct 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.3-pre11
- 3.3pre11 (synced more or less with Mandriva's 3.3-pre11.30mdv)
- call this 3.3 (without the pre stuff) to prevent wierd upgrade issues later
- drop P1; broke modprobe -r
- rediffed P2, P3, and P7 from Mandriva
- new P1: libify modprobe for ldetect
- P10: fix insmod when using it without an absolute path
- P11: exit() is not a user-friendly user management method in a library
- P12: drop calls to docbook2man from the makefiles
- S1: add mandriva's blacklist
- S6: add a blacklist-compat list to blacklist certain drivers (Fedora)
- drop alternatives; we no longer support 2.4 kernels so we don't need modutils
- use dietlibc
- build a shared library and package development files
- obsoletes modutils
- package our own manpages as we won't ship docbook and friends to build them

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2.2
- add -doc subpackage
- requires packages, not files

* Mon Apr 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2.2
- first Annvix package for the 2.6 kernel

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
