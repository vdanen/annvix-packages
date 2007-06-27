#
# spec file for package readline
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		readline
%define version		5.2
%define	release		%_revrel

%define major		5
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d
%define odevname	%mklibname %{name} 5 -d

Summary:	Library for reading lines from a terminal
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Source:		ftp://ftp.gnu.org/pub/gnu/readline/readline-%{version}.tar.gz
Patch0:		readline-4.1-outdated.patch
Patch1:		readline52-001
Patch2:		readline-4.3-no_rpath.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The "readline" library will read a line from the terminal and return it,
allowing the user to edit the line with the standard emacs editing keys.
It allows the programmer to give the user an easier-to-use and more
intuitive interface.


%package -n %{libname}
Summary:	Shared libraries for readline
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	%{name}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked to readline.


%package -n %{devname}
Summary:	Files for developing programs that use the readline library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{odevname}
Conflicts:	%{_lib}readline4-devel

%description -n %{devname}
The "readline" library will read a line from the terminal and return it,
using prompt as a prompt.  If prompt is null, no prompt is issued.  The
line returned is allocated with malloc(3), so the caller must free it when
finished.  The line returned has the final newline removed, so only the
text of the line remains.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .outdated
%patch1 -p0 -b .001
%patch2 -p1 -b .no_rpath


libtoolize --copy --force


%build
export CFLAGS="%{optflags}"
%configure2_5x \
    --with-curses=ncurses
perl -p -i -e 's|-Wl,-rpath.*||' shlib/Makefile
%make static shared


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall install-shared

# put all libs in /lib because some packages need it
# before /usr is mounted
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/*.so* %{buildroot}/%{_lib}
ln -s ../../%{_lib}/lib{history,readline}.so %{buildroot}%{_libdir}
for i in history readline; do
    ln -s ../%{_lib}/lib$i.so.4 %{buildroot}/%{_lib}/lib$i.so.4.1
    ln -s ../%{_lib}/lib$i.so.4 %{buildroot}/%{_lib}/lib$i.so.4.2
done


# The make install moves the existing libs with a suffix of old. Urgh.
rm -f %{buildroot}/%{_lib}/*.old

perl -p -i -e 's|/usr/local/bin/perl|/usr/bin/perl|' doc/texi2html

# fix perms
chmod 0644 examples/rlfe/ChangeLog
chmod 0755 support/{config.rpath,mkinstalldirs}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post -n %{devname}
%_install_info history.info
%_install_info readline.info


%preun -n %{devname}
%_remove_install_info history.info
%_remove_install_info readline.info


%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/lib*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_mandir}/man*/*
%{_infodir}/*info*
%{_includedir}/readline
%{_libdir}/lib*.a
%{_libdir}/lib*.so
/%{_lib}/*so

%files doc
%defattr(-,root,root)
%doc CHANGELOG CHANGES INSTALL MANIFEST README USAGE
%doc doc examples support


%changelog
* Tue Jun 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2
- renumber patches

* Sat Jun 23 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2
- 5.2
- updated P11 for this version
- drop P18, P5
- implement devel naming policy
- implement library provides policy

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1
- 5.1
- drop P2,P11-P15,P17; merged upstream
- new P11 for 5.1
- drop P4; was a fedora patch that is no longer applied
- fix perms of some doc files
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0-1avx
- 5.0
- sync with mdk 5.0-2mdk:
  - sync with fedora patches
  - drop P1 (unapplied), P100/P101 (merged upstream)
- throw in a conflicts on libreadline4-devel

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3-13avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3-12avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3-11avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3-10avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.3-9sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 4.3-8sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
