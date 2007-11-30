#
# spec file for package dhcpcd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		dhcpcd
%define	version		1.3.22pl4
%define release		%_revrel

%define	rversion	1.3.22-pl4

Summary:	DHCPC Daemon
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.phystech.com/download/dhcpcd.html
Source:		ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/dhcpcd-%{rversion}.tar.bz2
Patch0:		dhcpcd-1.3.22-pl4-resolvrdv.patch
Patch1:		dhcpcd-1.3.22pl4-CAN-2005-1848.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
dhcpcd is an implementation of the DHCP client specified in
draft-ietf-dhc-dhcp-09 (when -r option is not specified) and RFC1541
(when -r option is specified).

It gets the host information (IP address, netmask, broad- cast address,
etc.) from a DHCP server and configures the network interface of the
machine on which it is running.  It also tries to renew the lease time
according to RFC1541 or draft-ietf-dhc-dhcp-09.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{rversion}
%patch0 -p1 -b .resolvrdv
%patch1 -p1 -b .can-2005-1848


%build
%configure2_5x
%make DEFS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/sbin 
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_sysconfdir}/dhcpc/

install -s -m 0755 dhcpcd %{buildroot}/sbin/dhcpcd
install -m 0755 dhcpcd.exe %{buildroot}%{_sysconfdir}/dhcpc/
install -m 0644 dhcpcd.8 %{buildroot}%{_mandir}/man8/dhcpcd.8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/dhcpc/*
/sbin/dhcpcd
%{_mandir}/man8/dhcpcd.8*

%files doc
%defattr(-,root,root)
%doc README ChangeLog COPYING INSTALL *.lsm


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.3.22pl4
- rebuild

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.3.22pl4
- get rid of the %%post stuff; all it does is drop a useless file in /
  and there's no logrotating going on here
- don't install dhcpcd.exe with "-s" (aka strip)
- drop the %%ghost logfile too

* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.22pl4
- add -doc subpackage
- rebuild with gcc4
- add requires(post) on rpm-helper

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.22pl4
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.22pl4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.22pl4-9avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.22pl4-8avx
- P1: fix CAN-2005-1848 (low security; no official update issued)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.22pl4-7avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.22pl4-6avx
- spec cleanups

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.3.22pl4-5avx
- Annvix build

* Sat May 29 2004 Vincent Danen <vdanen@opensls.org> 1.3.22pl4-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
