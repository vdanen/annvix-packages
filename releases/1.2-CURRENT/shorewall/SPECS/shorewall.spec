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
Source5:	shorewall.init
Source10:	http://shorewall.net/pub/shorewall/errata/2.0.10/bogons
Source11:	http://shorewall.net/pub/shorewall/2.4/shorewall-%{version}/errata/firewall

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	iptables, chkconfig
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Conflicts:	kernel <= 2.2

%description
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.


%prep
%setup -q

cp %{SOURCE5} init.sh
mkdir samples
pushd samples
    tar xzf %{SOURCE2}
    tar xzf %{SOURCE3}
    tar xzf %{SOURCE4}
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

install -m 0600 %{SOURCE10} %{buildroot}%{_datadir}/%{name}/bogons
install -m 0544 %{SOURCE11} %{buildroot}%{_datadir}/%{name}/firewall

mkdir -p %{buildroot}%{_initrddir}
mv %{buildroot}/etc/init.d/shorewall %{buildroot}%{_initrddir}/
rm -rf %{buildroot}/etc/init.d

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
%doc %attr(-,root,root) COPYING INSTALL changelog.txt releasenotes.txt tunnel samples
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


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Mon Dec 01 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.4.8-2.1.92mdk
- bugfix update for 9.2

* Tue Nov 18 2003 Florin <florin@mandrakesoft.com> 1.4.8-2mdk
- rebuld

* Wed Nov 12 2003 Florin <florin@mandrakesoft.com> 1.4.8-1mdk
- 1.4.8
- samples 1.4.8

* Sun Nov 02 2003 Florin <florin@mandrakesoft.com> 1.4.8-0.RC2.1mdk
- 1.4.8-RC2

* Sun Oct 26 2003 Florin <florin@mandrakesoft.com> 1.4.7c-1mdk
- 1.4.7c

* Sat Oct 25 2003 Florin <florin@mandrakesoft.com> 1.4.7b-1mdk
- 1.4.7b

* Tue Oct 07 2003 Florin <florin@mandrakesoft.com> 1.4.7b-1mdk
- 1.4.7 and samples 1.4.7
- add accounting, users and usersets new configuration files

* Mon Sep 08 2003 Florin <florin@mandrakesoft.com> 1.4.6c-2mdk
- replace the stop patch with SOURCE1

* Wed Sep 03 2003 Florin <florin@mandrakesoft.com> 1.4.6c-1mdk
- 1.4.6c

* Thu Aug 07 2003 Florin <florin@mandrakesoft.com> 1.4.6b-1mdk
- 1.4.6b
- samples 1.4.6

* Mon Jun 23 2003 Florin <florin@mandrakesoft.com> 1.4.5-1mdk
- 1.4.5

* Tue Jun 10 2003 Florin <florin@mandrakesoft.com> 1.4.4-1mdk
- 1.4.4b
- samples 1.4.4

* Fri Apr 25 2003 Florin <florin@mandrakesoft.com> 1.4.2-1mdk
- 1.4.2

* Thu Apr 03 2003 Florin <florin@mandrakesoft.com> 1.4.1a-1mdk
- 1.4.1a
- 1.4.0 samples version
- icmp.def has been removed
- _libdir files are now in _datadir
- ecn is the new file

* Fri Feb 21 2003 Florin <florin@mandrakesoft.com> 1.3.14-3mdk
- use simplified initscript
- stop acts as clear
- stop-> rstopped

* Thu Feb 20 2003 Florin <florin@mandrakesoft.com> 1.3.14-2mdk
- really fix chkconfig

* Mon Feb 17 2003 Florin <florin@mandrakesoft.com> 1.3.14-1mdk
- 1.3.14
- fix the chkconfig part 

* Tue Jan 21 2003 Florin <florin@mandrakesoft.com> 1.3.13-1mdk
- 1.3.13
- samples 1.3.12

* Fri Jan 10 2003 Florin <florin@mandrakesoft.com> 1.3.12-1mdk
- 1.3.12
- add missing files

* Fri Nov 29 2002 Florin <florin@mandrakesoft.com> 1.3.11-1mdk
- 1.3.11
- samples-1.3.11

* Fri Nov 22 2002 Florin <florin@mandrakesoft.com> 1.3.10-1mdk
- 1.3.10
- samples-1.3.10
- add the forgotten maclist
- add PreReq on rpm-helper
- remove some weird config(noreplace)s

* Mon Oct 28 2002 Florin <florin@mandrakesoft.com> 1.3.9b-4mdk
- use the post|preun_service macros

* Thu Oct 24 2002 Florin <florin@mandrakesoft.com> 1.3.9b-3mdk
- remove the chkconfig add in post

* Tue Oct 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.9b-2mdk
- fix cvs-internal-file
- fix %%preun

* Tue Oct 15 2002 Florin <florin@mandrakesoft.com> 1.3.9b-1mdk
- 1.3.9b
- 1.3.9 samples 

* Mon Oct 7 2002 Florin <florin@mandrakesoft.com> 1.3.9a-1mdk
- 1.3.9a
- _libdir instead of /var/lib

* Tue Sep 10 2002 Florin <florin@mandrakesoft.com> 1.3.7c-1mdk
- 1.3.7c fixes a DNAT bug
- clear the rules in preun (thx to aginies)

* Wed Aug 28 2002 Florin <florin@mandrakesoft.com> 1.3.7b-2mdk
- split the docs in a special package

* Tue Aug 27 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.7b-1mdk
- new version
- ditch P0
- samples_version is 1.3.7, not 1.3.7a

* Mon Aug 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.7a-2mdk
- update the firewall script (P0)
- misc spec file fixes
 
* Fri Aug 23 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.7a-1mdk
- new version

* Thu Aug 01 2002 Florin <florin@mandrakesoft.com> 1.3.5b-2mdk
- update the URL
- add the md5sums
- update the description

* Thu Aug 01 2002 Florin <florin@mandrakesoft.com> 1.3.5b-1mdk
- 1.3.5b
- remove the useless so-called comptability with SNF

* Tue Jul 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.4-1mdk
- new version
- misc spec file fixes

* Mon Jun 10 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.1-1mdk
- new version

* Fri May 17 2002 Florin <florin@mandrakesoft.com> 1.2.13-1mdk
- 1.2.13

* Fri May 03 2002 Florin <florin@mandrakesoft.com> 1.2.12-1mdk
- 1.2.12
- samples 1.2.1

* Tue Apr 09 2002 Florin <florin@mandrakesoft.com> 1.2.10-1mdk
- 1.2.10

* Mon Mar 11 2002 Florin <florin@mandrakesoft.com> 1.2.9-1mdk
- shorewall 1.2.9
- samples 1.2.1
- fiw some doc files permissions

* Wed Feb 20 2002 Florin <florin@mandrakesoft.com> 1.2.6-2mdk
- add misc, pptp and cbq examples in samples archive

* Tue Feb 12 2002 Florin <florin@mandrakesoft.com> 1.2.6-1mdk
- 1.2.6
- use the install.sh script
- move shorewall to /sbin
- add conflicts to the kernel <= 2.2

* Tue Jan 22 2002 Florin <florin@mandrakesoft.com> 1.2.3-2mdk
- fix the ADSL entry in description (thx to Y.Duret)

* Tue Jan 22 2002 Florin <florin@mandrakesoft.com> 1.2.3-1mdk
- 1.2.3

* Thu Jan 10 2002 Florin <florin@mandrakesoft.com> 1.2.2-1mdk
- 1.2.2
- 1.2.0 samples version
- add the /%{_sysconfdir}/%{name}/{blacklist,tcrules} files
- fix some rpmlint errors

* Mon Dec 31 2001 Florin <florin@mandrakesoft.com> 1.2.0-1mdk
- 1.2.0
- update the samples files

* Tue Dec 18 2001 Florin <florin@mandrakesoft.com> 1.1.18-2mdk
- add the original sample files
- use the ftp_path macro
- forbid the echo/gprintf substitution in the initscript
- fix the docs permissions

* Mon Dec 17 2001 Florin <florin@mandrakesoft.com> 1.1.18-1mdk
- 1.1.18

* Thu Oct 11 2001 Florin <florin@mandrakesoft.com> 1.1.13-3mdk
- add the /etc/shorewall/params file

* Wed Sep 26 2001 Florin <florin@mandrakesoft.com> 1.1.13-2mdk
- fix a typo in description (thx to Alvaro Herrera)

* Mon Sep 24 2001 Florin <florin@mandrakesoft.com> 1.1.13-1mdk
- 1.1.13

* Mon Sep 03 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.1.12-1mdk
- rebuild

* Wed Aug  1 2001 Sylvain de Tilly <sdetilly@ke.mandrakesoft.com> 1.1.10-1mdk
- Transforme original spec file to Mandrake's spec file

* Fri Jul 06 2001 Tom Eastep <tom@seattlefirewall.dyndns.org>
- Changed release to 10
* Tue Jun 19 2001 Tom Eastep <tom@seattlefirewall.dyndns.org>
- Changed release to 9
- Added tunnel file
- Readded tunnels file
* Mon Jun 18 2001 Tom Eastep <tom@seattlefirewall.dyndns.org>
- Changed release to 8
* Sat Jun 02 2001 Tom Eastep <tom@seattlefirewall.dyndns.org>
- Changed release to 7
- Changed iptables dependency.
* Tue May 22 2001 Tom Eastep <tom@seattlefirewall.dyndns.org>
- Changed release to 6
- Added tunnels file
* Sat May 19 2001 Tom Eastep <tom@seattlefirewall.dyndns.org>
- Changed release to 5
- Added modules and tos files
* Sat May 12 2001 Tom Eastep <tom@seattlefirewall.dyndns.org>
- Changed release to 4
- Added changelog.txt and releasenotes.txt
* Sat Apr 28 2001 Tom Eastep <tom@seattlefirewall.dyndns.org>
- Changed release to 3
* Mon Apr 9 2001 Tom Eastep <tom@seattlefirewall.dyndns.org>
- Added files common.def and icmpdef.def
- Changed release to 2
* Wed Apr 4 2001 Tom Eastep <tom@seattlefirewall.dyndns.org>
- Changed the release to 1.
* Mon Mar 26 2001 Tom Eastep <teastep@seattlefirewall.dyndns.org>
- Changed the version to 1.1
- Added hosts file
* Sun Mar 18 2001 Tom Eastep <teastep@seattlefirewall.dyndns.org>
- Changed the release to 4
- Added Zones and Functions files
* Mon Mar 12 2001 Tom Eastep <teastep@seattlefirewall.dyndns.org>
- Change ipchains dependency to an iptables dependency and 
  changed the release to 3
* Fri Mar 9 2001 Tom Eastep <teastep@seattlefirewall.dyndns.org>
- Add additional files.
* Thu Mar 8 2001 Tom EAstep <teastep@seattlefirewall.dyndns.org>
- Change version to 1.0.2
* Tue Mar 6 2001 Tom Eastep <teastep@seattlefirewall.dyndns.org>
- Change version to 1.0.1
* Sun Mar 4 2001 Tom Eastep <teastep@seattlefirewall.dyndns.org>
- Changes for Shorewall
* Thu Feb 22 2001 Tom Eastep <teastep@seattlefirewall.dyndns.org>
- Change version to 4.1.0
* Fri Feb 2 2001 Tom Eastep <teastep@seattlefirewall.dyndns.org>
- Change version to 4.0.4
* Mon Jan 22 2001 Tom Eastep <teastep@seattlefirewall.dyndns.org>
- Change version to 4.0.2
* Sat Jan 20 2001 Tom Eastep <teastep@seattlefirewall.dyndns.org>
- Changed version to 4.0
* Fri Jan 5 2001 Tom Eastep <teastep@evergo.net>
- Added dmzclients file
* Sun Dec 24 2000 Tom Eastep <teastep@evergo.net>
- Added ftpserver file
* Sat Aug 12 2000 Tom Eastep <teastep@evergo.net>
- Added "nat" and "proxyarp" files for 4.0
* Mon May 20 2000 Tom Eastep <teastep@evergo.net>
- added updown file
* Sat May 20 2000 Simon Piette <spiette@generation.net>
- Corrected the group - Networking/Utilities
- Added "noreplace" attributes to config files, so current confis is not
  changed.
- Added the version file.
* Sat May 20 2000 Tom Eastep <teastep@evergo.net>
- Converted Simon's patch to version 3.1
* Sat May 20 2000 Simon Piette <spiette@generation.net>
- 3.0.2 Initial RPM
  Patched the install script so it can take a PREFIX variable
