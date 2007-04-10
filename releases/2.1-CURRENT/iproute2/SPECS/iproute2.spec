#
# spec file for package iproute2
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		iproute2
%define version		2.6.16
%define release		%_revrel

%define snap		060323

Summary: 	Advanced IP routing and network device configuration tools
Name:		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group:  	Networking/Other
URL:		http://developer.osdl.org/dev/iproute2/
Source: 	%{name}-%{version}-%{snap}.tar.bz2
Source2:	iproute2-man8.tar.bz2
Patch0:		iproute2-2.6.16-rh-flags.patch
Patch1:		iproute2-mdv-def-echo.patch
Patch2:		iproute2-2.4.7-mdv-bashfix.patch
Patch3:		iproute2-2.6.X-mdv-ss040702-build-fix.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	db4-devel
BuildRequires:	flex
BuildRequires:	bison

Requires:	iputils

%description
The iproute package contains networking utilities (ip, tc and rtmon,
for example) which are designed to use the advanced networking
capabilities of the Linux 2.2.x kernels and later,  such as policy 
routing, fast NAT and packet scheduling.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}-%{snap} 
%patch0 -p1 -b .flags
%patch1 -p1
%patch2 -p1 -b .bashfix
%patch3 -p1 -b .build


%build
%define optflags -ggdb
%make KERNEL_INCLUDE=/usr/src/linux/include


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}/{sbin,%{_sysconfdir}/iproute2}

install -m 0755 ip/ifcfg %{buildroot}/sbin
install -m 0755 ip/routef %{buildroot}/sbin
install -m 0755 ip/routel %{buildroot}/sbin
install -m 0755 ip/ip %{buildroot}/sbin
install -m 0755 ip/rtmon %{buildroot}/sbin
install -m 0755 misc/rtacct %{buildroot}/sbin
install -m 0755 misc/ss %{buildroot}/sbin
install -m 0755 tc/tc %{buildroot}/sbin
install -m 0644 etc/iproute2/rt_dsfield %{buildroot}%{_sysconfdir}/iproute2
install -m 0644 etc/iproute2/rt_protos %{buildroot}%{_sysconfdir}/iproute2
install -m 0644 etc/iproute2/rt_realms %{buildroot}%{_sysconfdir}/iproute2
install -m 0644 etc/iproute2/rt_scopes %{buildroot}%{_sysconfdir}/iproute2
install -m 0644 etc/iproute2/rt_tables %{buildroot}%{_sysconfdir}/iproute2
mkdir -p %{buildroot}/%{_mandir}
tar xfj %{_sourcedir}/iproute2-man8.tar.bz2 -C %{buildroot}/%{_mandir}/

# do not install q_atm.so as it adds a dep on libatm
mkdir -p %{buildroot}%{_libdir}/tc
install -m 0755 tc/q_netem.so %{buildroot}%{_libdir}/tc/
install -m 0755 netem/{normal,pareto,paretonormal} %{buildroot}%{_libdir}/tc/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr (-,root,root)
%dir %{_sysconfdir}/iproute2
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
/sbin/*
%{_libdir}/tc
%{_mandir}/man8/*

%files doc
%defattr (-,root,root)
%doc README README.iproute2+tc RELNOTES README.decnet
%doc doc/Plan examples/


%changelog
* Tue Jul 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16
- 2.6.16
- fix url
- drop P0, P1, P2, P4, P8, P9, P103, P104, P105, P106, P107
- renumber and rename patches
- updated P0
- P3: build fixes
- BuildRequires: db4-devel, flex, bison
- add -doc subpackage
- rebuild with gcc4
- use %%_sourcedir/file instead of %%{SOURCEx}

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7-17avx
- bootstrap build (new gcc, new glibc)
- P107: fix ip/iptunnel.c so it compiles properly

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7-16avx
- bootstrap build

* Tue Dec 07 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7-15avx
- P106: patch to fix CAN-2003-0856

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7-14avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.4.7-13sls
- minor spec cleanups
- remove some *.ps and other unwanted docs
- remove buildreq's on tetex-latex and tetex-dvips

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 2.4.7-12sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
