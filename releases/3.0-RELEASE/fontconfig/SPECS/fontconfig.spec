#
# spec file for package fontconfig
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		fontconfig
%define version		2.5.0
%define release		%_revrel

%define major		1
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

%define freetype_ver	2.1.7

Summary:	Font configuration library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/X11
URL:		http://fontconfig.org/
Source:		http://fontconfig.org/release/fontconfig-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ed
BuildRequires:	freetype2-devel >= %{freetype_ver}
BuildRequires:	expat-devel
BuildRequires:	autoconf2.5 >= 2.54

Requires(post):	%{libname} >= %{version}-%{release}

%description
Fontconfig is designed to locate fonts within the system and select them
according to requirements specified by applications.


%package -n %{libname}
Summary:	Font configuration and customization library
Group:		System/Libraries
Requires:	%{name} >= %{version}
Provides:	lib%{name} = %{version}-%{release}
Provides:	%{name}-libs = %{version}-%{release}

%description -n %{libname}
Fontconfig is designed to locate fonts within the system and select them
 according to requirements specified by applications.


%package -n %{devname}
Summary:	Font configuration and customization library
Group:		Development/C
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Requires:	freetype2-devel >= %{freetype_ver}
Requires:	expat-devel
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 -d

%description -n %{devname}
The fontconfig-devel package includes the header files, and developer docs
for the fontconfig package.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x \
    --with-add-fonts="/usr/X11R6/lib/X11/fonts,/opt/ttfonts,/usr/share/yudit/fonts" \
    --disable-docs
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

# remove unpackaged files
rm -rf %{buildroot}%{_datadir}/doc/fontconfig
rm -rf %{buildroot}%{_sysconfdir}/fonts/conf.d
rm -rf %{buildroot}%{_sysconfdir}/fonts/conf.avail


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%{_bindir}/fc-cache -f >/dev/null


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/fc-cache
%{_bindir}/fc-cat
%{_bindir}/fc-match
%{_bindir}/fc-list
%dir %{_sysconfdir}/fonts
%config %{_sysconfdir}/fonts/fonts.dtd
%config(noreplace) %{_sysconfdir}/fonts/*.conf
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files doc
%defattr(-,root,root)
%doc README AUTHORS COPYING doc/fontconfig-user.html doc/fontconfig-user.txt
%doc doc/fontconfig-devel doc/fontconfig-devel.txt 


%changelog
* Tue Dec 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5.0
- 2.5.0
- drop all patches

* Sun Sep 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2
- implement devel naming policy
- implement library provides policy

* Fri Feb 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2
- rebuild against patched freetype

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2
- geez, really remove docs from the devel package

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2
- really remove docs from main package

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-2avx
- rebuild against new expat

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-1avx
- 2.3.2
- built-in libtool fixes (gbeauchesne)
- sync patches with mandriva 2.3.2-5mdk

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.1-11avx
- bootstrap build (new gcc, new glibc)

* Sat Jun 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.1-10avx
- bootstrap build
- fix build, use %%configure2_5x

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> - 2.2.1-9avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> - 2.2.1-8sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> - 2.2.1-7sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
