#
# spec file for package iptables
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		iptables
%define version		1.4.0
%define release		%_revrel

Summary:	Tools for managing Linux kernel packet filtering capabilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://netfilter.org/

Source0:	http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
Source1:	http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2.sig
Source2:	iptables-avx.init
Source3:	ip6tables-avx.init
Source4:	iptables.config
Source5:	ip6tables.config
Source6:	iptables-kernel-headers.tar.bz2
Patch2:		iptables-1.2.8-imq.patch 
Patch3:		iptables-1.3.5-libiptc.h.patch 
Patch6:		iptables-1.3.3-IFWLOG_extension.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl
BuildRequires:  kernel-source

Requires(post):	rpm-helper
Requires(preun): rpm-helper
Provides:	userspace-ipfilter
Conflicts:	ipchains

%description
iptables controls the Linux kernel network packet filtering code.
It allows you to set up firewalls and IP masquerading, etc.


%package ipv6
Summary:	IPv6 support for iptables
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description ipv6
IPv6 support for iptables.

iptables controls the Linux kernel network packet filtering code.
It allows you to set up firewalls and IP masquerading, etc.

IPv6 is the next version of the IP protocol.


%package devel
Summary:	Development package for iptables
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
#Requires:	kernel-headers

%description devel
The development files for iptables.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 6
%patch2 -p1 -b .imq
%patch3 -p1 -b .libiptc
%patch6 -p1 -b .IFWLOG

chmod +x extensions/.*-test

find . -type f | xargs perl -pi -e "s,/usr/local,%{_prefix},g"


%build
%serverbuild
OPT="%{optflags} -fPIC -DNDEBUG -DNETLINK_NFLOG=5"

make \
    LD=gcc \
    COPT_FLAGS="${OPT}" \
    KBUILD_OUTPUT=/usr/src/linux \
    KERNEL_DIR=$PWD/linux-2.6-vanilla \
    LIBDIR=/lib \
    all
# XX: once we have kernel-headers, KERNEL_DIR=/usr/src/linux


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
# Dunno why this happens. -- Geoff
%makeinstall_std \
    COPT_FLAGS="${OPT}" \
    LD=gcc \
    BINDIR=/sbin \
    MANDIR=%{_mandir} \
    LIBDIR=/lib \
    KERNEL_DIR=%{_prefix} \
    install install-experimental

make \
    DESTDIR=%{buildroot} \
    COPT_FLAGS="${OPT}" \
    LD=gcc \
    KERNEL_DIR=%{_prefix} \
    BINDIR=/sbin \
    LIBDIR=%{_libdir} \
    MANDIR=%{_mandir} \
    INCDIR=%{_includedir} \
    install-devel

install -m 0644 libiptc/libiptc.a -D %{buildroot}%{_libdir}/libiptc.a

install -c -D -m 0750 %{_sourcedir}/iptables-avx.init %{buildroot}%{_initrddir}/iptables
install -c -D -m 0750 %{_sourcedir}/ip6tables-avx.init %{buildroot}%{_initrddir}/ip6tables
install -c -D -m 0640 %{_sourcedir}/iptables.config iptables.sample
install -c -D -m 0640 %{_sourcedir}/ip6tables.config ip6tables.sample


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -rf %{_builddir}/file.list.%{name}


%post
%_post_service iptables


%preun
%_preun_service iptables


%post ipv6
%_post_service ip6tables


%preun ipv6
%_preun_service ip6tables


%files
%defattr(-,root,root,0755)
%attr(0750,root,admin) %{_initrddir}/iptables
/sbin/iptables
/sbin/iptables-save
/sbin/iptables-restore
/sbin/iptables-xml
%{_mandir}/*/iptables*
%dir /lib/iptables
/lib/iptables/libipt*
/lib/iptables/libxt*

%files ipv6
%defattr(-,root,root,0755)
%attr(0750,root,admin) %{_initrddir}/ip6tables
/sbin/ip6tables
/sbin/ip6tables-save
/sbin/ip6tables-restore
%{_mandir}/*/ip6tables*
/lib/iptables/libip6t*

%files devel
%defattr(-,root,root,0755)
%{_includedir}/libipq.h
%{_libdir}/libipq.a
%{_libdir}/libiptc.a
%{_mandir}/man3/*

%files doc
%defattr(-,root,root,0755)
%doc INSTALL INCOMPATIBILITIES iptables.sample ip6tables.sample


%changelog
* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.4.0
- 1.4.0
- fix perms on initscript (bug #64)
- initscripts are not %%config(noreplace)
- drop world readable perms on iptables sample config files
- drop useless kernel requires
- drop P1; we don't use grsecurity
- use -fPIC

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.3.8
- 1.3.8
- drop P4, no longer required
- drop P5; Mandriva doesn't apply it so neither will we
- updated P1 from Mandriva
- drop the alpha conditionals
- renumber sources

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.5
- new initscripts

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.5
- 1.3.5
- rediff P1, P3, P4
- fix download urls
- use linux-2.6-vanilla, not linux-2.6-pom as this needs patches in
  the kernel we don't have (yet)
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3-3avx
- get rid of the check command in the initscripts altogether; it's only
  required if there are multiple iptables libraries; we only ship one

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3-2avx
- fix the initscripts:
  - no longer check if we're running kernel 2.3 or higher; we've
    never shipped a 2.2 kernel
  - get rid of that braindead symlinking crap; we have one iptables
    directory, leave it alone!

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3-1avx
- 1.3.3
- drop P4; fixed upstream
- sync with mandrake 1.3.3-3mdk:
  - updated kernel headers (2.6.12 and 2.4.31)
  - fix a lot of extensions tests: Makefile check for $KERNEL_DIR/net/*/*/*.c
    but we provide only headers files ($KERNEL_DIR/include/linux/*/*.h) so the
    tests fail every time and we don't get the extension (sbellabes)
  - add ipp2p extension (sbellabes)
  - rediff P1 (herton)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1-2avx
- bootstrap build (new gcc, new glibc)

* Sat Jun 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1-1avx
- 1.3.1
- rediff P1
- sync kernel headers with 2.4.31-1avx
- get rid of this vanilla vs. avx crap; one iptables to rule them all

* Thu Nov 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.9-6avx
- fix iptables.init: s/sls/avx/

* Tue Nov 02 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.9-5avx
- P4: patch to fix CAN-2004-0986
- s/sls/avx/
- remove some docs from ip6tables that are in iptables (which ip6tables
  requires anyways)
- add the devel package (florin)

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.9-4avx
- Annvix build

* Wed Mar  3 2004 Thomas Backlund <tmb@iki.fi> 1.2.9-3sls
- sync kernel-headers with 2.4.25-4sls

* Wed Mar  3 2004 Thomas Backlund <tmb@iki.fi> 1.2.9-2sls
- require kernel(-source) 2.4.25-3sls or better
- fix symlinking for sls (not mandrake)

* Wed Mar  3 2004 Thomas Backlund <tmb@iki.fi> 1.2.9-1sls
- sync with mdk 1.2.9-5mdk
  * fix detection of iptables version at boot (again)
  * compatible with both 2.4 and 2.6 (with and without pptp_conntrack)
  * added check option to initscripts
  * IMQ should work now (cross fingers).
  * reddiff stealth patch.
  * 1.2.9.

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 1.2.8-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
