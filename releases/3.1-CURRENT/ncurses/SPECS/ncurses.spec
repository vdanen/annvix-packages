#
# spec file for package ncurses
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ncurses
%define version		5.6
%define release		%_revrel

%define major		5
%define majorminor	5.6
%define libname		%mklibname %{name} %{major}
%define utf8libname	%mklibname %{name}w %{major}
%define devname		%mklibname %{name} -d
%define utf8devname	%mklibname %{name}w -d

Summary:	A CRT screen handling and optimization package
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
URL:		http://www.gnu.org/software/ncurses/ncurses.html
Source0:	http://ftp.gnu.org/gnu/ncurses/%{name}-%{version}.tar.gz
Source1:	ncurses-resetall.sh
Source2:	ncurses-usefull-terms
# rollup patches from ftp://invisible-island.net/ncurses/5.6/
Source3:	ncurses-5.6-20070714-patch.sh
Patch0:		ncurses-5.6-xterm-debian.patch
Patch1:		ncurses-5.3-parallel.patch
Patch2:		ncurses-5.3-utf8.patch
# patches from ftp://invisible-island.net/ncurses/5.6/
Patch3:		ncurses-5.6-20070716.patch
Patch4:		ncurses-5.6-20070721.patch
Patch5:		ncurses-5.6-20070728.patch
Patch6:		ncurses-5.6-20070812.patch
Patch7:		ncurses-5.6-20070818.patch
Patch8:		ncurses-5.6-20070825.patch
Patch9:		ncurses-5.6-20070901.patch
Patch10:	ncurses-5.6-20070908.patch
Patch11:	ncurses-5.6-20070915.patch
Patch12:	ncurses-5.6-20070929.patch
Patch13:	ncurses-5.6-20071006.patch
Patch14:	ncurses-5.6-20071013.patch
Patch15:	ncurses-5.6-20071020.patch
Patch16:	ncurses-5.6-20071103.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	sharutils

Conflicts:	ncurses-extraterms < 5.6


%description
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.


%package -n %{libname}
Summary:	The development files for applications which use ncurses
Group:		System/Libraries
Requires:	ncurses
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.


%package -n %{utf8libname}
Summary:	Ncurses libraries which support UTF8
Group:		System/Libraries
Requires:	ncurses
Provides:	lib%{name}w = %{version}-%{release}

%description -n %{utf8libname}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

This package contains ncurses libraries which support wide char (UTF8),
and is not compatible with those without.


%package -n %{utf8devname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Requires:	%{utf8libname} = %{version}
Provides:	%{name}w-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name}w 5 -d

%description -n %{utf8devname}
The libraries for developing applications that use ncurses CRT screen
handling and optimization package. Install it if you want to develop
applications which will use ncurses.

Note that the libraries included here supports wide char (UTF-8),
and is not compatible with those without. When linking programs with
these libraries, you will have to append a "w" to the library names,
i.e. -lformw, -lmenuw, -lncursesw, -lpanelw.


%package extraterms
Summary:	Some exotic terminal descriptions
Group:		System/Libraries
Requires:	ncurses = %{version}-%{release}

%description extraterms
Install the ncurses-extraterms package if you use some exotic terminals.


%package -n %{devname}
Summary:	The development files for applications which use ncurses
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 5 -d

%description -n %{devname}
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
# the rollup patch comes first
cp %{_sourcedir}/ncurses-5.6-20070714-patch.sh .
/bin/sh ncurses-5.6-20070714-patch.sh
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1


#%patch1 -p1 -b .parallel
%patch2 -p1 -b .utf8
# regenerating configure needs patched autoconf, so modify configure
# directly
%patch0 -p1 -b .deb

find . -name "*.orig" | xargs rm -f
# fix some permissions
chmod 0755 c++/edit_cfg.sh test/listused.sh test/configure test/tracemunch


%build
#OPT_FLAGS="%{optflags} -DPURE_TERMINFO -fno-omit-frame-pointer"
#CFLAGS="$OPT_FLAGS -DSVR4_CURSES"
#CXXFLAGS="$OPT_FLAGS"

mkdir -p ncurses-normal
pushd ncurses-normal
    CONFIGURE_TOP=..
    %configure2_5x \
        --includedir=%{_includedir}/ncurses \
        --with-normal \
        --with-shared \
        --without-debug \
        --without-profile \
        --without-gpm \
        --enable-termcap \
        --enable-getcap \
        --enable-const \
        --enable-hard-tabs \
        --enable-hash-map \
        --enable-no-padding \
        --enable-sigwinch \
        --without-ada \
        --enable-xmc-glitch \
        --enable-colorfgbg \
        --with-ospeed=unsigned

    %make -j1
popd

mkdir -p ncurses-utf8
pushd ncurses-utf8
    CONFIGURE_TOP=..
    %configure2_5x \
        --includedir=%{_includedir}/ncursesw \
        --with-normal \
        --with-shared \
        --without-debug \
        --without-profile \
        --without-gpm \
        --enable-termcap \
        --enable-getcap \
        --enable-const \
        --enable-hard-tabs \
        --enable-hash-map \
        --enable-no-padding \
        --enable-sigwinch \
        --without-ada \
        --enable-widec \
        --enable-xmc-glitch \
        --enable-colorfgbg \
        --with-ospeed=unsigned

    %make -j1
popd


%install
pushd ncurses-utf8
    %makeinstall_std
popd

pushd ncurses-normal
    %makeinstall_std
popd

ln -sf ../l/linux %{buildroot}%{_datadir}/terminfo/c/console
ln -sf ncurses/curses.h %{buildroot}%{_includedir}/ncurses.h
for I in curses unctrl eti form menu panel term; do
    ln -sf ncurses/$I.h %{buildroot}%{_includedir}/$I.h
done

# the resetall script
install -m 0755 %{_sourcedir}/ncurses-resetall.sh %{buildroot}%{_bindir}/resetall
# we don't want this in doc
rm -f c++/demo

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libncurses.so* %{buildroot}/%{_lib}
ln -s /%{_lib}/libncurses.so.%{majorminor} %{buildroot}%{_libdir}/libncurses.so.%{majorminor}
ln -s /%{_lib}/libncurses.so.%{majorminor} %{buildroot}%{_libdir}/libncurses.so.%{major}
ln -s /%{_lib}/libncurses.so.%{majorminor} %{buildroot}%{_libdir}/libncurses.so

#
# FIXME
# OK do not time to debug it now
#
cp %{buildroot}%{_datadir}/terminfo/x/xterm %{buildroot}%{_datadir}/terminfo/x/xterm2
cp %{buildroot}%{_datadir}/terminfo/x/xterm-new %{buildroot}%{_datadir}/terminfo/x/xterm

#
# remove unneeded/unwanted files
# have to be done before find commands below
#
rm -f %{buildroot}%{_libdir}/terminfo

#
# FIXME
#
(cd %{buildroot} ; find usr/share/terminfo      -type d | perl -pe 's||%%dir /|') > %{name}.list
(cd %{buildroot} ; find usr/share/terminfo -not -type d | perl -pe 's||/|')       > %{name}-extraterms.list
perl -pe 's||%{_datadir}/terminfo/|' %{_sourcedir}/ncurses-usefull-terms >> %{name}.list

perl -ni -e 'BEGIN { open F, "%{name}.list"; /^%/ or $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}-extraterms.list

find %{buildroot}%{_libdir} -name 'lib*.a' -not -type d -not -name "*_g.a" -not -name "*_p.a" -not -name "*w.a" | sed -e "s#^%{buildroot}##" > %{devname}.list


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{utf8libname} -p /sbin/ldconfig
%postun -n %{utf8libname} -p /sbin/ldconfig


%files -f %{name}.list
%defattr(-,root,root)
%dir %{_datadir}/terminfo
%{_datadir}/tabset
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files -n %{libname}
%defattr(-,root,root)
%attr(0755,root,root) /%{_lib}/lib*.so.*
%attr(0755,root,root) %{_libdir}/lib*.so.*
%exclude %{_libdir}/lib*w.so.*

%files -n %{utf8libname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/lib*w.so.*

%files extraterms -f %{name}-extraterms.list
%defattr(-,root,root)

%files -n %{devname} -f %{devname}.list
%defattr(-,root,root)
/%{_lib}/lib*.so
%{_libdir}/lib*.so
%exclude %{_libdir}/lib*w.so
%{_includedir}/ncurses
%{_includedir}/*.h
%{_mandir}/man3/*

%files -n %{utf8devname}
%defattr(-,root,root)
%{_libdir}/lib*w.so
%{_libdir}/lib*w.a
%{_includedir}/ncursesw

%files doc
%defattr(-,root,root)
%doc README ANNOUNCE doc c++ test


%changelog
* Fri Dec 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.6
- 5.6, patches through 20071103 (S3, P3-P16)
- updated P0 from Mandriva
- add screen.linux, cygwin, and putty as a useful terms instead of
  being in the extraterms
- don't provide old major

* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.5
- implement devel naming policy
- implement library provides policy

* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.5
- 5.5
- drop P6, P8, P14, P15
- renumber sources and patches
- new P2, P3, P4
- spec cleanups
- put the parallel patch back

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.4
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.4
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.4-3avx
- don't embed the patch date in the release string anymore

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.4-1.20050108.2avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.4-1.20050108.1avx
- 5.4 with pathset 20050108
- rebuild for new gcc
- enable wide char support and split into different libraries (deaddog)
- use %%configure2_5x and %%makeinstall_std to fix ugly build issues (deaddog)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.3-1.20030215.8avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.3-1.20030215.7avx
- Require packages not files
- Annvix build

* Sat Jun 12 2004 Vincent Danen <vdanen@opensls.org> 5.3-1.20030215.6sls
- own /usr/share/terminfo

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 5.3-1.20030215.5sls
- minor spec cleanups
- remove %%build_opensls macro
- remove unpackaged files

* Sat Dec 06 2003 Vincent Danen <vdanen@opensls.org> 5.3-1.20030215.4sls
- OpenSLS build
- tidy spec
- use %%build_opensls to build without gpm support

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
