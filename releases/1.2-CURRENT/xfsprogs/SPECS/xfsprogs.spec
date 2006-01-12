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
%define version 	2.6.36
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
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-buildroot
BuildRequires:	libext2fs-devel, libreadline-devel, libtermcap-devel

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

You should install %{libname}-devel if you want to develop XFS
filesystem-specific programs, If you install %{libname}-devel, you'll
also want to install xfsprogs.


%prep
%setup -q
# make it lib64 aware, better make a patch?
perl -pi -e "/(libuuid|pkg_s?lib_dir)=/ and s|/lib\b|/%{_lib}|;" configure


%build
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


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/COPYING doc/CREDITS README
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
%doc README
/%{_lib}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/PORTING README
/%{_lib}/*.so
/%{_lib}/*a
%{_libdir}/*so
%{_libdir}/*a
%{_includedir}/xfs
%{_includedir}/disk
%{_mandir}/man3/*

%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Wed Aug 13 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5.4-2mdk
- Enforce current practise to BuildRequires: libxfs-devel

* Fri Aug  8 2003 Juan Quintela <quintela@mandrakesoft.com> 2.5.4-1mdk
- binaries back at /sbin & /usr/sbin.
- 2.5.4.

* Fri Jul 18 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.12-1mdk
- 2.4.12.

* Tue Jun 17 2003 Juan Quintela <quintela@trasno.org> 2.3.9-1mdk
- 2.3.9.

* Wed Apr 23 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.6-2mdk
- make it lib64 aware
- nuke files already packaged as %%doc

* Wed Jul 24 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.6-1mdk
- 2.0.6

* Wed Jul 10 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.3-2mdk
- fixed changelog typo. Thanks eagle-eye gc for pointing it out to me ;o)

* Wed Jul 10 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.3-1mdk
- 2.0.3

* Thu Mar  7 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.0.0-1mdk
- 2.0.0

* Tue Feb  5 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3.13-2mdk
- Requires: common-licenses
- use %%configure2_5x

* Tue Nov 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.13-1mdk
- 1.3.13.

* Sat Sep 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.7-1mdk
- 1.3.7.

* Fri Sep 28 2001 Stefan van der Eijk <stefan@eijk.nu> 1.3.5-3mdk
- BuildRequires: libext2fs-devel
- Copyright --> License

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.5-2mdk
- Fix provides.

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.5-1mdk
- 1.3.5.
- Split lib in subpackage.
- Rework the spec.

* Wed May  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.0-1mdk
- Fist attempt based on the SGI spec.


# end of file
