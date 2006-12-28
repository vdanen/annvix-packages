#
# spec file for package rp-pppoe
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rp-pppoe
%define version		3.8
%define release		%_revrel

%define pppver		2.4.4

Summary:	ADSL/PPPoE userspace driver
Name:		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.roaringpenguin.com/pppoe
Source0:	http://www.roaringpenguin.com/files/download/%{name}-%{version}.tar.gz
Source1:	pppoe-avx.init
Patch0:		rp-pppoe-3.6-CAN-2004-0564.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ppp = %{pppver}
BuildRequires:	autoconf2.5

Requires:	ppp >= 2.4.1
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many ADSL Internet Service Providers. Roaring Penguin has a free
client for Linux systems to connect to PPPoE service providers.

The client is a user-mode program and does not require any kernel
modifications. It is fully compliant with RFC 2516, the official PPPoE
specification.

It has been tested with many ISPs, such as the Canadian Sympatico HSE (High
Speed Edition) service.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .can-2004-0564


%build
pushd src
    autoconf
    %configure2_5x
    %make

    perl -pi -e 's|/etc/ppp/plugins/|%{_libdir}/pppd/%{pppver}|g' doc/KERNEL-MODE-PPPOE
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d -m 0755 %{buildroot}

pushd src
    make install RPM_INSTALL_ROOT=%{buildroot}
popd

mkdir -p %{buildroot}%{_initrddir}
install -m 0750 %{_sourcedir}/pppoe-avx.init %{buildroot}%{_initrddir}/pppoe

rm -rf %{buildroot}/usr/doc
rm -f %{buildroot}%{_sysconfdir}/ppp/plugins/README
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}


%preun
%_preun_service pppoe


%post
%_post_service pppoe


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/ppp/pppoe.conf
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%config(noreplace) %{_sysconfdir}/ppp/firewall-masq
%config(noreplace) %{_sysconfdir}/ppp/firewall-standalone
%{_sbindir}/pppoe
%{_sbindir}/pppoe-connect
%{_sbindir}/pppoe-relay
%{_sbindir}/pppoe-server
%{_sbindir}/pppoe-setup
%{_sbindir}/pppoe-sniff
%{_sbindir}/pppoe-start
%{_sbindir}/pppoe-status
%{_sbindir}/pppoe-stop
%{_mandir}/man[58]/*
%config(noreplace)%{_initrddir}/pppoe

%files doc
%defattr(-,root,root)
%doc doc/* README SERVPOET


%changelog
* Thu Dec 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.8
- 3.8
- build against ppp 2.4.4

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7
- provide our own initscript and drop the patch to the old initscript
- add the %%_post and %%_preun service scriptlets
- requires on rpm-helper

* Mon Jun 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.7
- 3.7
- update P1 from Mandriva
- updated P0 for new initscript name
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.5
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.5
- Obfuscate email addresses and new tagging
- Uncompress patches
- install the initscript (for some reason it's now installing on it's own anymore)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.5-10avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.5-9avx
- rebuild

* Sat Dec 04 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.5-8avx
- P1: patch to fix CAN-2004-0564

* Mon Jul 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.5-7avx
- start adsl after network but before shorewall

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.5-6avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.5-5sls
- minor spec cleanups

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 3.5-4sls
- OpenSLS build
- tidy spec
- drop gui package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
