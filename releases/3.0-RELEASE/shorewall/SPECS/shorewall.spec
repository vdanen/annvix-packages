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
%define version 	3.4.6
%define release 	%_revrel

Summary:	Shoreline Firewall is an iptables-based firewall for Linux systems
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.shorewall.net/
Source0:	ftp://ftp.shorewall.net/pub/shorewall/3.4/%{name}-%{version}/%{name}-%{version}.tgz
Source1:	ftp://ftp.shorewall.net/pub/shorewall/3.4/%{name}-%{version}/%{version}.sha1sums
Source2:	shorewall-avx.init

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

perl -pi -e 's/STARTUP_ENABLED=.*/STARTUP_ENABLED=Yes/' %{name}.conf
perl -pi -e 's/IP_FORWARDING=.*/IP_FORWARDING=Keep/' %{name}.conf


%build
find -name CVS -exec rm -rf {} \;
find -name '*~' -exec rm -rf {} \;


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

export PREFIX=%{buildroot}
export OWNER=`id -n -u`
export GROUP=`id -n -g`
./install.sh

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
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}
%attr(0750,root,root) %{_initrddir}/shorewall
%config(noreplace) %{_sysconfdir}/%{name}/*
%attr(0700,root,root) %dir %{_datadir}/%{name}
%attr(0640,root,root) %{_datadir}/%{name}/*
%attr(0750,root,root) %{_datadir}/%{name}/compiler
%attr(0540,root,root) /sbin/shorewall
%attr(0700,root,root) %dir %{_var}/lib/%{name}
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%files doc
%defattr(-,root,root)
%doc %attr(-,root,root) COPYING INSTALL changelog.txt releasenotes.txt tunnel Samples ipsecvpn


%changelog
* Tue Dec 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.4.6
- 3.4.6 ( please refer to http://www.shorewall.net/upgrade_issues.htm#V3.4.0 )

* Thu Dec 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2.7
- 3.2.7 ( please refer to http://www.shorewall.net/upgrade_issues.htm )
- tighten some perms and other minor cleanups

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
