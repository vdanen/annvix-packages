#
# spec file for package am-utils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		am-utils
%define version		6.1.5
%define release		%_revrel
%define epoch		3

%define major		2
%define libname		%mklibname amu %{major}

Summary:	Automount utilities including an updated version of Amd
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	BSD
Group:		System/Servers
URL:		http://www.am-utils.org/
Source:		ftp://ftp.am-utils.org/pub/%{name}/%{name}-%{version}.tar.gz
Source1:	am-utils.conf
Source2:	am-utils.net.map
Source3:	amd.run
Source4:	amd-log.run
Source5:	AMDOPTS.env
Source6: 	MOUNTPTS.env
Patch0:		am-utils-6.0.4-nfs3.patch
Patch1:		am-utils-6.1.5-avx-nodaemon.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	db1-devel

Requires:	portmap
Requires:	setup >= 2.4-16avx
Requires(post):	rpm-helper
Requires(post):	info-install
Requires(preun): info-install
Requires(preun): rpm-helper
Obsoletes:	amd
Provides:	amd = %{version}-%{release}

%description
Am-utils includes an updated version of Amd, the popular BSD
automounter.  An automounter is a program which maintains a cache of
mounted filesystems.  Filesystems are mounted when they are first
referenced by the user and unmounted after a certain period of inactivity.
Amd supports a variety of filesystems, including NFS, UFS, CD-ROMS and
local drives.  


%package -n %{libname}
Summary:        Shared library files for am-utils
Group:          System/Servers
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
Shared library files from the am-utils package.


%package -n %{libname}-devel
Summary:        Development files for am-utils
Group:          Development/C
Requires:       %{libname} = %{epoch}:%{version}
Provides:       libamu-devel

%description -n %{libname}-devel
Development headers, and files for development from the am-utils package.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch -p1
%patch1 -p1 -b .nodaemon


%build
%serverbuild
%configure \
    --enable-shared \
    --enable-libs="-lnsl -lresolv" \
    --disable-amq-mount \
    --enable-debug=yes \
    --without-ldap

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_sysconfdir}/

install -m 0600 %{_sourcedir}/am-utils.conf %{buildroot}%{_sysconfdir}/amd.conf
install -m 0640 %{_sourcedir}/am-utils.net.map %{buildroot}%{_sysconfdir}/amd.net

mkdir -p %{buildroot}%{_srvdir}/amd/{log,env,depends} 

install -m 0740 %{_sourcedir}/amd.run %{buildroot}%{_srvdir}/amd/run
install -m 0740 %{_sourcedir}/amd-log.run %{buildroot}%{_srvdir}/amd/log/run

install -m 0640 %{_sourcedir}/AMDOPTS.env %{buildroot}%{_srvdir}/amd/env/AMD_OPTS
install -m 0640 %{_sourcedir}/MOUNTPTS.env %{buildroot}%{_srvdir}/amd/env/MOUNTPTS

%_mkdepends amd portmap

mkdir -p %{buildroot}/.automount

# remove unwanted files
rm -f %{buildroot}%{_sbindir}/ctl-amd
rm -f %{buildroot}/amd.conf
rm -f %{buildroot}/%{_sysconfdir}/*-sample
rm -f %{buildroot}/amd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_srv amd
%_install_info %{name}.info


%preun
%_preun_srv amd


%postun
%_remove_install_info %{name}.info


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/amd.conf
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/amd.net
%dir /.automount
%{_bindir}/pawd
%{_bindir}/expn
%{_sbindir}/*
%{_mandir}/man[58]/*
%{_mandir}/man1/pawd.1*
%{_mandir}/man1/expn.1*
%{_infodir}/*.info*
%dir %attr(0750,root,admin) %{_srvdir}/amd
%dir %attr(0750,root,admin) %{_srvdir}/amd/log
%dir %attr(0750,root,admin) %{_srvdir}/amd/env
%dir %attr(0750,root,admin) %{_srvdir}/amd/depends
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/amd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/amd/log/run
%attr(0640,root,admin) %config(noreplace) %{_srvdir}/amd/env/AMD_OPTS
%attr(0640,root,admin) %config(noreplace) %{_srvdir}/amd/env/MOUNTPTS
%attr(0640,root,admin) %{_srvdir}/amd/depends/portmap

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la

%files doc
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog NEWS README* scripts/*-sample INSTALL COPYING


%changelog
* Sat Dec 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.1.5
- 6.1.5
- use AMD_OPTS instead of AMDOPTS to be more consisent (./env)
- fix source url
- fix requires
- fix buildrequires (gdbm no longer enables ndbm support, db1 does)
- drop P1: no longer required
- new P1: make amd never background (for some reason, using -D nodaemon no
  longer works)

* Mon Nov 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9
- fix the run script (but see bug #36 regarding svwaitup too)

* Tue Jul 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9
- spec cleanups

* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9
- add -doc subpackage
- rebuild with gcc4
- drop the postscript docs
- remove service log relocation stuff
- P1: fix compilation with gcc4
- fix rpmlint requires-on-release

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9
- Clean rebuild

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-11avx
- quotes in runscript

* Sun Sep 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-10avx
- back down to 6.0.9 due to some very wierd amd behaviour with
  6.1.x
- bump the epoch
- change the logfile from syslog to /dev/stderr in amd.conf

* Sun Sep 25 2005 Sean P. Thomas <vdanen-at-build.annvix.org> 6.1.2.1-1avx
- Converted to env dirs, run script to execlineb, converted 
- dependencies, and upgraded to newest version. 

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.1.1-2avx
- s/supervise/service/ in log/run

* Fri Sep 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.1.1-1avx
- 6.1.1
- use execlineb for run scripts
- move logdir to /var/log/service/amd
- run scripts are now considered config giles and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-12avx
- fix perms on run scripts

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-11avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-10avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-9avx
- first Annvix build, to replace autofs

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
