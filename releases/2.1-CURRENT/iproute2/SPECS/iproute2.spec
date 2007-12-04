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
%define version		2.6.20
%define release		%_revrel

%define snap		070313

Summary: 	Advanced IP routing and network device configuration tools
Name:		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group:  	Networking/Other
URL:		http://linux-net.osdl.org/index.php/Iproute2
Source: 	%{name}-%{version}-%{snap}.tar.bz2
Source2:	iproute2-man8.tar.bz2
Patch0:		iproute2-2.6.16-rh-flags.patch
Patch1:		iproute2-mdv-def-echo.patch
Patch2:		iproute2-2.4.7-mdv-bashfix.patch
Patch3:		iproute2-2.6.X-mdv-ss040702-build-fix.patch
Patch4:		iproute2-2.6.16-rh-libdir.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	db4-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	kernel-source

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
%setup -q -n iproute-%{version}-%{snap} 
%patch0 -p1 -b .flags
%patch1 -p1
%patch2 -p1 -b .bashfix
%patch3 -p1 -b .build
%patch4 -p1 -b .libdir


%build
%define optflags -ggdb
%make KERNEL_INCLUDE=/usr/src/linux/include LIBDIR=%{_libdir}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std SBINDIR=/sbin
mv -f %{buildroot}/sbin/arpd %{buildroot}/sbin/iproute-arpd

# do not install q_atm.so as it adds a dep on libatm
rm -f %{buildroot}%{_libdir}/tc/q_atm.so
rm -rf %{buildroot}%{_docdir}/%{name}

tar xjf %{_sourcedir}/iproute2-man8.tar.bz2 -C %{buildroot}%{_mandir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr (-,root,root)
%dir %{_sysconfdir}/iproute2
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
/sbin/*
%{_libdir}/tc
%{_mandir}/man3/*
%{_mandir}/man8/*

%files doc
%defattr (-,root,root)
%doc README README.iproute2+tc RELNOTES README.decnet
%doc doc/Plan examples/


%changelog
* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.20
- 2.6.20, snap 070313
- simplify the install
- P4: fix libdir in tc
- buildrequires: kernel-source
- update url

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
