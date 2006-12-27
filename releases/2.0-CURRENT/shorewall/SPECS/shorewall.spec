#
# spec file for package shorewall
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		shorewall
%define version 	2.4.1
%define release 	%_revrel

%define samples_version	2.0.1

Summary:	Shoreline Firewall is an iptables-based firewall for Linux systems
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.shorewall.net/
Source0:	ftp://ftp.shorewall.net/pub/shorewall/2.4/shorewall-%{version}/%{name}-%{version}.tgz
Source1:	ftp://ftp.shorewall.net/pub/shorewall/2.4/shorewall-%{version}/%{version}.md5sums
Source2:	ftp://ftp.shorewall.net/pub/shorewall/Samples/samples-%{samples_version}/one-interface.tgz
Source3:	ftp://ftp.shorewall.net/pub/shorewall/Samples/samples-%{samples_version}/two-interfaces.tgz
Source4:	ftp://ftp.shorewall.net/pub/shorewall/Samples/samples-%{samples_version}/three-interfaces.tgz
Source5:	shorewall-avx.init
Source10:	http://shorewall.net/pub/shorewall/errata/2.0.10/bogons
Source11:	http://shorewall.net/pub/shorewall/2.4/shorewall-%{version}/errata/firewall

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	iptables
Requires:	runit
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Conflicts:	kernel <= 2.2

%description
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

cp %{_sourcedir}/shorewall-avx.init init.sh
mkdir samples
pushd samples
    tar xzf %{_sourcedir}/one-interface.tgz
    tar xzf %{_sourcedir}/two-interfaces.tgz
    tar xzf %{_sourcedir}/three-interfaces.tgz
popd


%build
find -name CVS | xargs rm -fr
find -name "*~" | xargs rm -fr
find samples/ -type f | xargs chmod 0644 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# enable startup (new as of 2.1.3)
perl -pi -e 's/STARTUP_ENABLED=.*/STARTUP_ENABLED=yes/' %{name}.conf
export PREFIX=%{buildroot} ; \
export OWNER=`id -n -u` ; \
export GROUP=`id -n -g` ;\
./install.sh

install -m 0600 %{_sourcedir}/bogons %{buildroot}%{_datadir}/%{name}/bogons
install -m 0544 %{_sourcedir}/firewall %{buildroot}%{_datadir}/%{name}/firewall

# Suppress automatic replacement of "echo" by "gprintf" in the shorewall
# startup script by RPM. This automatic replacement is broken.
export DONT_GPRINTIFY=1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_service shorewall


%preun
%_preun_service shorewall


%files
%defattr(-,root,root)
%attr(700,root,root) %dir /etc/shorewall
%attr(750,root,root) %{_initrddir}/shorewall

%config(noreplace) %{_sysconfdir}/%{name}/accounting
%config(noreplace) %{_sysconfdir}/%{name}/actions
%config(noreplace) %{_sysconfdir}/%{name}/blacklist
%config(noreplace) %{_sysconfdir}/%{name}/continue
%config(noreplace) %{_sysconfdir}/%{name}/ecn
%config(noreplace) %{_sysconfdir}/%{name}/hosts
%config(noreplace) %{_sysconfdir}/%{name}/init
%config(noreplace) %{_sysconfdir}/%{name}/initdone
%config(noreplace) %{_sysconfdir}/%{name}/interfaces
%config(noreplace) %{_sysconfdir}/%{name}/ipsec
%config(noreplace) %{_sysconfdir}/%{name}/maclist
%config(noreplace) %{_sysconfdir}/%{name}/masq
%config(noreplace) %{_sysconfdir}/%{name}/modules
%config(noreplace) %{_sysconfdir}/%{name}/netmap
%config(noreplace) %{_sysconfdir}/%{name}/nat
%config(noreplace) %{_sysconfdir}/%{name}/params
%config(noreplace) %{_sysconfdir}/%{name}/policy
%config(noreplace) %{_sysconfdir}/%{name}/providers
%config(noreplace) %{_sysconfdir}/%{name}/proxyarp
%config(noreplace) %{_sysconfdir}/%{name}/routes
%config(noreplace) %{_sysconfdir}/%{name}/routestopped
%config(noreplace) %{_sysconfdir}/%{name}/rules
%config(noreplace) %{_sysconfdir}/%{name}/shorewall.conf
%config(noreplace) %{_sysconfdir}/%{name}/start
%config(noreplace) %{_sysconfdir}/%{name}/started
%config(noreplace) %{_sysconfdir}/%{name}/stop
%config(noreplace) %{_sysconfdir}/%{name}/stopped
%config(noreplace) %{_sysconfdir}/%{name}/tcrules
%config(noreplace) %{_sysconfdir}/%{name}/tos
%config(noreplace) %{_sysconfdir}/%{name}/tunnels
%config(noreplace) %{_sysconfdir}/%{name}/zones
%attr(544,root,root) /sbin/shorewall
%attr(700,root,root) %dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%files doc
%defattr(-,root,root)
%doc %attr(-,root,root) COPYING INSTALL changelog.txt releasenotes.txt tunnel samples


%changelog
* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1
- new initscript
- spec cleanups
- requires runit, not chkconfig

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-1avx
- 2.4.1
- add %%_post_service and %%_preun_service macros
- rename initscript

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.6-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.6-3avx
- rebuild

* Wed Sep 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.6-2avx
- remove some macros; now we add shorewall via chkconfig if it's an
  install, otherwise leave it alone as there is no need to restart
  the "service" on upgrade

* Mon Jul 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.6-1avx
- 2.0.6
- start shorewall at S12, after the network

* Mon Jun 28 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.3-1avx
- 2.0.3
- remove S4 (bogons), S5 (rfc1918); already included
- remove P0 (kernel-suffix); already integrated
- make shorewall start just after the network does otherwise it
  fails to fully init
- remove the doc package; put samples in the docdir of the main
  package
- use pristine sources all the way around
- fix source urls

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.1-3avx
- Annvix build

* Sat Jun 12 2004 Vincent Danen <vdanen@opensls.org> 2.0.1-2sls
- own /usr/share/shorewall
- small spec cleaning

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.0.1-1sls
- 2.0.1
- add netmap file
- add the kernel modules extension patch (mdk bug #9311) (florin)
- patch also fixes broken insmod (use modprobe instead) (florin)
- add the bogons and rfc1918 sources (thomas)

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.4.8-4sls
- minor spec cleanups
- remove %%prefix

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 1.4.8-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
