#
# spec file for package net-tools
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		net-tools
%define version 	1.60
%define release 	%_revrel

%define npversion	1.2.9

Summary:	The basic tools for setting up networking
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://www.tazenda.demon.co.uk/phil/net-tools/
Source0:	http://www.tazenda.demon.co.uk/phil/net-tools//net-tools-%{version}.tar.bz2
Source2:	net-tools-1.60-config.h
Source3:	net-tools-1.60-config.make
Source4:	ether-wake.c
Source5:	ether-wake.8
Source6:	mii-diag.c
Source7:	mii-diag.8
Source8:	bin.netstat.profile
Patch1:		net-tools-1.57-bug22040.patch
Patch2:		net-tools-1.60-miiioctl.patch
Patch3:		net-tools-1.60-manydevs.patch
Patch4:		net-tools-1.60-virtualname.patch
Patch5:		net-tools-1.60-cycle.patch
Patch6:		net-tools-1.60-nameif.patch
Patch7:		net-tools-1.60-ipx.patch
Patch8:		net-tools-1.60-inet6-lookup.patch
Patch9:		net-tools-1.60-man.patch
Patch10:	net-tools-1.60-gcc33.patch
Patch11:	net-tools-1.60-trailingblank.patch
Patch12:	net-tools-1.60-interface.patch
Patch13:	net-tools-1.60-x25.patch
Patch14:	net-tools-1.60-gcc34.patch
Patch15:	net-tools-1.60-overflow.patch
Patch19:	net-tools-1.60-siunits.patch
Patch20:	net-tools-1.60-trunc.patch
Patch21:	net-tools-1.60-return.patch
Patch22:	net-tools-1.60-parse.patch
Patch23:	net-tools-1.60-netmask.patch
Patch24:	net-tools-1.60-ulong.patch
Patch25:	net-tools-1.60-bcast.patch
Patch26:	net-tools-1.60-mii-tool-obsolete.patch
Patch27:	net-tools-1.60-netstat_ulong.patch
Patch28:	net-tools-1.60-note.patch
Patch29:	net-tools-1.60-num-ports.patch
Patch30:	net-tools-1.60-duplicate-tcp.patch
Patch31:	net-tools-1.60-statalias.patch
Patch32:	net-tools-1.60-isofix.patch
Patch34:	net-tools-1.60-ifconfig_ib.patch
Patch35:	net-tools-1.60-de.patch
Patch37:	net-tools-1.60-pie.patch
Patch38:	net-tools-1.60-ifaceopt.patch
Patch39:	net-tools-1.60-trim_iface.patch
Patch40:	net-tools-1.60-stdo.patch
Patch41:	net-tools-1.60-statistics.patch
Patch42:	net-tools-1.60-mdv-netdevice.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext

%description
The net-tools package contains the basic tools needed for setting up
networking:  ifconfig, netstat, route and others.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1 -b .bug22040
%patch2 -p1 -b .miioctl
%patch3 -p0 -b .manydevs
%patch4 -p1 -b .virtualname
%patch5 -p1 -b .cycle
%patch6 -p1 -b .nameif
%patch7 -p1 -b .ipx
%patch8 -p1 -b .inet6-lookup
%patch9 -p1 -b .man
%patch10 -p1 -b .gcc33
%patch11 -p1 -b .trailingblank
%patch12 -p1 -b .interface
%patch13 -p1 -b .x25
%patch14 -p1 -b .gcc34
%patch15 -p1 -b .overflow
%patch19 -p1 -b .siunits
%patch20 -p1 -b .trunc
%patch21 -p1 -b .return
%patch22 -p1 -b .parse
%patch23 -p1 -b .netmask
%patch24 -p1 -b .ulong
%patch25 -p1 -b .bcast
%patch26 -p1 -b .obsolete
%patch27 -p1 -b .netstat_ulong
%patch28 -p1 -b .note
%patch29 -p1 -b .num-ports
%patch30 -p1 -b .dup-tcp
%patch31 -p1 -b .statalias
%patch32 -p1 -b .isofix
%patch34 -p1 -b .ifconfig_ib
%patch35 -p1 
%patch37 -p1 -b .pie
%patch38 -p1 -b .ifaceopt
%patch39 -p1 -b .trim-iface
%patch40 -p1 -b .stdo
%patch41 -p1 -b .statistics
%patch42 -p1 -b .netdevice

cp %{_sourcedir}/net-tools-1.60-config.h config.h
cp %{_sourcedir}/net-tools-1.60-config.make config.make
cp %{_sourcedir}/ether-wake.c ether-wake.c
cp %{_sourcedir}/ether-wake.8 man/en_US/ether-wake.8
cp %{_sourcedir}/mii-diag.c mii-diag.c
cp %{_sourcedir}/mii-diag.8 man/en_US/mii-diag.8

%ifarch alpha
perl -pi -e "s|-O2||" Makefile
%endif


%build
export CFLAGS="%{optflags} $CFLAGS"

make
gcc %{optflags} -o ether-wake ether-wake.c
gcc %{optflags} -o mii-diag mii-diag.c


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make BASEDIR=%{buildroot} mandir=%{_mandir} install

install -m 0755 ether-wake %{buildroot}/sbin
install -m 0755 mii-diag %{buildroot}/sbin

mkdir -p %{buildroot}%{_profiledir}
install -m 0640 %{_sourcedir}/bin.netstat.profile %{buildroot}%{_profiledir}/bin.netstat

rm -f %{buildroot}/sbin/rarp
rm -f %{buildroot}%{_mandir}/man8/rarp.8*

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%posttrans
%_aa_reload


%files -f %{name}.lang
%defattr(-,root,root)
/bin/*
/sbin/*
%config(noreplace) %attr(0640,root,root) %{_profiledir}/bin.netstat
%{_mandir}/man[158]/*

%files doc
%defattr(-,root,root)
%doc README README.ipv6 TODO INSTALLING ABOUT-NLS COPYING


%changelog
* Sat Dec 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.60
- rebuild with new %%_aa_reload macro definition
- P42: fixes the build

* Wed Nov 28 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.60
- add apparmor profile (from Mandriva)

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.60
- spec cleanups
- remove locales

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.60
- get rid of netplug; we don't want it (dropped S1, P33, P36)
- re-enable applicaiton of P13
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.60
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.60
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.60
- Obfuscate email addresses and new tagging
- Uncompress patches
- drop P0; unwanted
- disable parallel make; synced with mdk 1.60-17mdk (without pinit stuff)
- don't apply P13 as it kills the build
- (not manually modified /usr/linux/include/if_fddi.h to get this to build; need
  to patch kernel sources)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.60-15avx
- bootstrap build (new gcc, new glibc)

* Tue Aug 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.60-14avx
- rebuild against new gcc
- sync with mdk 1.60-13mdk (which synced with fedora 1.60-54)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.60-13avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.60-12avx
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 1.60-11sls
- minor spec cleanups
- remove the non-english manpages

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 1.60-10sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
