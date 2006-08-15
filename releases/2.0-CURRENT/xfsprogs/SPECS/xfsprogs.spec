#
# spec file for package xfsprogs
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		xfsprogs
%define version 	2.8.10
%define release 	%_revrel

%define libname_orig	libxfs
%define major		1
%define libname		%mklibname xfs %{major}

Summary:	Utilities for managing the XFS filesystem
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-1.tar.gz

BuildRoot:	%{_buildroot}/%{name}-buildroot
BuildRequires:	libext2fs-devel
BuildRequires:	libreadline-devel
BuildRequires:	libtermcap-devel
BuildRequires:	libtool

Requires:	common-licenses

%description
A set of commands to use the XFS filesystem, including mkfs.xfs.

XFS is a high performance journaling filesystem which originated
on the SGI IRIX platform.  It is completely multi-threaded, can
support large files and large filesystems, extended attributes,
variable block sizes, is extent based, and makes extensive use of
Btrees (directories, extents, free space) to aid both performance
and scalability.

Refer to the documentation at http://oss.sgi.com/projects/xfs/
for complete details.  This implementation is on-disk compatible
with the IRIX version of XFS.


%package -n %{libname}
Summary:	Main library for %{libname_orig}
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{libname_orig}.


%package -n %{libname}-devel
Summary:	XFS filesystem-specific static libraries and headers
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	xfs-devel = %{version}-%{release}
Obsoletes:	xfs-devel

%description -n %{libname}-devel
%{libname}-devel contains the libraries and header files needed to
develop XFS filesystem-specific programs.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
# make it lib64 aware, better make a patch?
perl -pi -e "/(libuuid|pkg_s?lib_dir)=/ and s|/lib\b|/%{_lib}|;" configure


%build
aclocal && autoconf
%configure2_5x \
    --libdir=/%{_lib} \
    --libexecdir=%{_libdir} \
    --sbindir=/sbin \
    --bindir=%{_sbindir} \
    --enable-gettext=yes \
    --enable-readline=yes \
    --enable-editline=no \
    --enable-termcap=yes \
    --enable-shared=yes \
    --enable-shared-uuid=yes

%make DEBUG=-DNDEBUG OPTIMIZER="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/

# nuke files already packaged as %doc
rm -rf %{buildroot}%{_datadir}/doc/xfsprogs/

# remove unwanted locales
rm -rf %{buildroot}%{_datadir}/locale

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_sbindir}/xfs_admin
%{_sbindir}/xfs_bmap
%{_sbindir}/xfs_check
%{_sbindir}/xfs_copy
%{_sbindir}/xfs_db
%{_sbindir}/xfs_freeze
%{_sbindir}/xfs_growfs
%{_sbindir}/xfs_info
%{_sbindir}/xfs_io
%{_sbindir}/xfs_logprint
%{_sbindir}/xfs_mkfile
%{_sbindir}/xfs_ncheck
%{_sbindir}/xfs_quota
%{_sbindir}/xfs_rtcp
/sbin/fsck.xfs
/sbin/mkfs.xfs
/sbin/xfs_repair
%{_mandir}/man[85]/*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
/%{_lib}/*.so
/%{_lib}/*a
%{_libdir}/*so
%{_libdir}/*a
%{_includedir}/xfs
%{_includedir}/disk
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/COPYING doc/CREDITS doc/PORTING README


%changelog
* Mon Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.10
- 2.8.10
- spec cleanups

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.36
- rebuild against new readline

* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.36
- add -doc subpackage
- rebuild with gcc4
- buildrequires: libtool

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.36
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.36
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.36-1avx
- 2.6.36
- BuildRequires: libreadline-devel, libtermcap-devel

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.13-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.13-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.13-2avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.13-1avx
- 2.6.13
- Annvix build

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 2.6.3-1sls
- remove %%{prefix}
- 2.6.3

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.5.4-3sls
- OpenSLS build
- tidy spec
