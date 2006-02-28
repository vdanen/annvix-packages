#
# spec file for package attr
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		attr
%define version 	2.4.23
%define release 	%_revrel

%define libname_orig	lib%{name}
%define major		1
%define libname		%mklibname %{name} %{major}

Summary:	Utility for managing filesystem extended attributes
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	%{name}-%{version}.src.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-buildroot

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.


%package -n %{libname}
Summary:	Main library for %{libname_orig}
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{libname_orig}.


%package -n %{libname}-devel
Summary:	Extended attribute static libraries and headers
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	attr-devel = %{version}-%{release}
Obsoletes:	attr-devel

%description -n %{libname}-devel
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

Currently only ext2, ext3, JFS and XFS support extended attributes.
The SGI IRIX compatibility API built above the Linux system calls is
used by programs such as xfsdump(8), xfsrestore(8) and xfs_fsr(8).


%prep
%setup -q


%build
%configure2_5x \
    --libdir=/%{_lib}
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/
make install-lib DIST_ROOT=%{buildroot}/

# fix conflict with man-pages-1.56
rm -rf %{buildroot}{%{_mandir}/man2,%_datadir/doc}

# Remove unpackaged symlinks
rm -rf %{buildroot}/%{_lib}/libattr.{a,la} %{buildroot}%{_libdir}/libattr.la

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/CHANGES.gz README doc/ea-conv
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%doc doc/COPYING
/%{_lib}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/COPYING README
/%{_lib}/*.so
%{_libdir}/*.so
%{_libdir}/*a
%{_mandir}/man3/*
%{_mandir}/man5/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Fri Dec 30 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.23-1avx
- 2.4.23

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.16-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.16-2avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.16-1avx
- 2.4.16
- Annvix build

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 2.4.14-1sls
- 2.4.14
- proper use of mklibname (per)

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 2.4.7-4sls
- remove %%{_prefix}
- minor spec cleanups
- remove unpackaged symlinks (stefan)

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.4.7-3sls
- OpenSLS build
- tidy spec

* Fri Aug 29 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.7-2mdk
- /usr/include/attr belongs to package.

* Fri Aug  8 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.7-1mdk
- 2.4.7.

* Fri Jul 18 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.3-1mdk
- 2.4.3.

* Fri Jul 18 2003 Juan Quintela <quintela@mandrakesoft.com> 2.2.0-1mdk
- remove patche-errno.h (included upstream).
- 2.2.0.

* Mon Jul 14 2003 Götz Waschk <waschk@linux-mandrake.com> 2.1.1-2mdk
- configure2_5x macro
- mklibname macro

* Thu Jun 19 2003 Vincent Danen <vdanen@mandrakesoft.com> 2.1.1-1mdk
- 2.1.1
- force configure to put libs in /lib

* Fri May 23 2003 Götz Waschk <waschk@linux-mandrake.com> 2.0.8-3mdk
- rebuild for devel provides

* Thu Apr 10 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.8-2mdk
- fix conflict with latest man-pages
- fix unpackaged files

* Wed Jul 24 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.8-1mdk
- 2.0.8

* Wed Jul 10 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-1mdk
- 2.0.7

* Sat Jun 15 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.0.1-2mdk
- Build fix for Alpha.

* Thu Mar  7 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.0.1-1mdk
- 2.0.1

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.3-2mdk
- Fix provides.

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.3-1mdk
- Rework the .spec.
- Make libs in subpackage.
- 1.1.3.

* Wed May  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.1-1mdk
- First attempt.


# end of file
