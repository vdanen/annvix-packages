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
%define version		1.3.5
%define release		%_revrel

Summary:	Tools for managing Linux kernel packet filtering capabilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://netfilter.org/

Source:		http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
Source6:	http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2.sig
Source1:	iptables.init
Source2:	ip6tables.init
Source3:	iptables.config
Source4:	ip6tables.config
Source5:	iptables-kernel-headers.tar.bz2
Patch1:		iptables-1.3.5-stealth_grsecurity.patch 
Patch2:		iptables-1.2.8-imq.patch 
Patch3:		iptables-1.3.5-libiptc.h.patch 
Patch4:		iptables-1.3.5-fix_extension_test.patch
Patch5:		iptables-1.3.2-ipp2p_extension.patch
Patch6:		iptables-1.3.3-IFWLOG_extension.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl
BuildRequires:  kernel-source >= 2.4.24-3avx

Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires:	kernel >= 2.4.25-3avx
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
Requires:	%{name} = %{version}

%description devel
The development files for iptables.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 5
%patch1 -p1 -b .stealth
%patch2 -p1 -b .imq
%patch3 -p1 -b .libiptc
%patch4 -p1 -b .fix_extension_test
%patch5 -p1 -b .ipp2p
%patch6 -p1 -b .IFWLOG

chmod +x extensions/.IMQ-test
chmod +x extensions/.ipp2p-test
chmod +x extensions/.IFWLOG-test

find . -type f | xargs perl -pi -e "s,/usr/local,%{_prefix},g"


%build
%serverbuild
%ifarch alpha
    OPT=`echo %{optflags} | sed -e "s/-O./-O1/"`
%else
    OPT="%{optflags} -DNDEBUG"
%endif

make COPT_FLAGS="$OPT" KERNEL_DIR=$PWD/linux-2.6-vanilla LIBDIR=/lib all


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
# Dunno why this happens. -- Geoff
%makeinstall_std \
    BINDIR=/sbin \
    MANDIR=%{_mandir} \
    LIBDIR=/lib \
    COPT_FLAGS="%{optflags} -DNETLINK_NFLOG=4" \
    KERNEL_DIR=/usr \
    install-experimental

make install-devel \
    DESTDIR=%{buildroot} \
    KERNEL_DIR=/usr \
    BINDIR=/sbin \
    LIBDIR=%{_libdir} \
    MANDIR=%{_mandir}

install -c -D -m 0755 %{_sourcedir}/iptables.init %{buildroot}%{_initrddir}/iptables
install -c -D -m 0755 %{_sourcedir}/ip6tables.init %{buildroot}%{_initrddir}/ip6tables
install -c -D -m 0644 %{_sourcedir}/iptables.config iptables.sample
install -c -D -m 0644 %{_sourcedir}/ip6tables.config ip6tables.sample


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
%config(noreplace) %{_initrddir}/iptables
/sbin/iptables
/sbin/iptables-save
/sbin/iptables-restore
%{_mandir}/*/iptables*
%dir /lib/iptables
/lib/iptables/libipt*

%files ipv6
%defattr(-,root,root,0755)
%config(noreplace) %{_initrddir}/ip6tables
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
