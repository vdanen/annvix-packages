#
# spec file for package iproute2
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# sync: rh-2.4.7-7
#
# $Id$

%define revision	$Rev$
%define name		iproute2
%define version		2.4.7
%define release		%_revrel

%define snap		010824

Summary: 	Advanced IP routing and network device configuration tools
Name:		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group:  	Networking/Other
URL:		ftp://ftp.inr.ac.ru/ip-routing/
Source: 	%{name}-%{version}-now-ss%snap.tar.bz2
Source2:	iproute2-man8.tar.bz2
# RH patches
Patch0:		iproute2-2.2.4-docmake.patch
Patch1:		iproute2-misc.patch
Patch2:		iproute2-config.patch
Patch4:		iproute2-in_port_t.patch
Patch6:		iproute2-flags.patch
Patch8:		iproute2-2.4.7-hex.patch
Patch9:		iproute2-2.4.7-config.patch
# MDK patches
Patch100:	iproute2-def-echo.patch
Patch102:	iproute2-2.4.7-bashfix.patch
Patch103:	iproute2-htb3.6_tc.patch
Patch104:	iproute2-2.4.7-now-ss010824-make.patch
Patch105:	iproute2-mult-deflt-gateways.patch
Patch106:	iproute2-2.4.7-netlink.patch
Patch107:	iproute2-2.4.7-avx-includes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	iputils

%description
The iproute package contains networking utilities (ip, tc and rtmon,
for example) which are designed to use the advanced networking
capabilities of the Linux 2.2.x kernels and later,  such as policy 
routing, fast NAT and packet scheduling.


%prep
%setup -q -n %{name} 
%patch0 -p1 -b .doc
%patch1 -p1 -b .misc
%patch2 -p1
%patch4 -p1 -b .glibc22
%patch6 -p1 -b .flags
%patch8 -p1 -b .hex
%patch9 -p1 -b .config

%patch100 -p1
%patch102 -p1 -b .bashfix
%patch103 -p1 -b .htb3
%patch104 -p0 -b .make
%patch105 -p1 -b .make
%patch106 -p1 -b .can-2003-0856
%patch107 -p1 -b .includes


%build
%define optflags -ggdb
%make KERNEL_INCLUDE=/usr/include


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}/{sbin,%{_sysconfdir}/iproute2}

install -m 0755 ip/ifcfg %{buildroot}/sbin
install -m 0755 ip/routef %{buildroot}/sbin
install -m 0755 ip/routel %{buildroot}/sbin
install -m 0755 ip/ip %{buildroot}/sbin
install -m 0755 ip/rtmon %{buildroot}/sbin
install -m 0755 ip/rtacct %{buildroot}/sbin
install -m 0755 tc/tc %{buildroot}/sbin
install -m 0644 etc/iproute2/rt_dsfield %{buildroot}%{_sysconfdir}/iproute2
install -m 0644 etc/iproute2/rt_protos %{buildroot}%{_sysconfdir}/iproute2
install -m 0644 etc/iproute2/rt_realms %{buildroot}%{_sysconfdir}/iproute2
install -m 0644 etc/iproute2/rt_scopes %{buildroot}%{_sysconfdir}/iproute2
install -m 0644 etc/iproute2/rt_tables %{buildroot}%{_sysconfdir}/iproute2
mkdir -p %{buildroot}/%{_mandir}
tar xfj %SOURCE2 -C %{buildroot}/%{_mandir}/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr (-,root,root)
%doc README README.iproute2+tc RELNOTES README.decnet
%doc doc/Plan examples/
%dir %{_sysconfdir}/iproute2
/sbin/*
%{_mandir}/man8/*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Fri Aug  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.7-11mdk
- nuke kernel-source dep

* Wed Jul 16 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.7-10mdk
- patch 105 : fix problem (first hop always dead) with multiple default gateway
  and load balacing in equal cost multipath enviroment (submitted Fausto
  Moretti <fausto@stayvirtual.it>, from a Julian Anastasov patch at 
  http://marc.theaimsgroup.com/?l=lartc&m=100885677229167&w=2)
  
* Wed May 21 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.7-9mdk
- resync with rh2.4.7-7
- patch 8: when specifying fwmark based routing rules, /sbin/ip silently
  assumes that the number on the command line is in hex, whether or not it is
  prefixed with 0x (anyway the rule is listed it is not indicated to be hex)
- patch 9: add missing diffserv support in config 
- %%make: do not rely on /usr/src/linux/include but on kernel-headers package
  (which will ease porters job)
- patch 104: fix build system due to previous change

* Fri Jan 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.7-8mdk
- build release

* Mon Nov 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.7-7mdk
- patch 103 : add support for htb 3

* Fri Nov 22 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.4.7-6mdk
- Fix typo in Requires

* Thu Nov 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.7-5mdk
- disable patch 101 (HTB) broken by latest kernel-headers
- remove source 1
- source 2 : add new man pages (iproute.8, tc-cbq.8, tc-htb.8, tc-pbfifo.8,
  tc-pfifo_fast.8, tc-prio.8, tc-red.8, tc-sfq.8, tc-tbf.8, tc.8)

* Mon Jul 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.7-4mdk
- /sbin/ifcfg:typeset -i for a variable so it will work instead of bailing out.

* Mon Jul  1 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.4.7-3mdk
- change BuildRequires from kernel22-source to kernel-source
- change description

* Tue Apr 16 2002 Florin <florin@mandrakesoft.com> 2.4.7-2mdk
- add the htb patch

* Mon Mar 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.7-1mdk
- new release: 20010824 snaphot
- better summary
- resync with rh-2.4.7-1

* Sat Mar 23 2002 David BAUDENS <baudens@mandrakesoft.com> 2.2.4-14mdk
- Allow build

* Tue Nov 13 2001 Stefan van der Eijk <stefan@eijk.nu> 2.2.4-13mdk
- BuildRequires: kernel-source tetex-dvips tetex-latex

* Tue Nov 13 2001 Philippe Libat <philippe@mandrakesoft.com> 2.2.4-12mdk
- include mode documentation
- include more sbin

* Tue Oct 30 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.2.4-11mdk
- add url

* Tue Oct 09 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.2.4-10mdk
- qa-ize()

* Wed Jul 11 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.2.4-9mdk
- build release
- spec cleaning

* Thu May 17 2001 Stew Benedict <sbeneict@mandrakesoft.com> 2.2.4-8mdk
- provide missing define in if_ether.h in some kernel trees

* Thu Nov 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2.4-7mdk
- Fix glibc22 compilation.

* Thu Aug 10 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.2.4-6mdk
- fix config files

* Wed Jul 19 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.2.4-5mdk
- BM

* Wed Jul 12 2000 Christian Zoffoli <czoffoli@linux-mandrake.com> 2.2.4-4mdk
- removed _sysconfdir 
- added %clean

* Wed Jul 12 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.2.4-3mdk
- fix a few typo (chrs scks :-) ) and make this spec short-circuit aware :
  *  _sysconfig/_sysconfdir
  *  creation of subdirs while installing
- Christian Zoffoli <czoffoli@linux-mandrake.com> : macroszifications

* Fri Apr 28 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.2.4-2mdk
- fix group and files section

* Wed Mar 01 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.2.4-1mdk
- mandrake build
- used latest release of 2.2.4 series / 000225
 
* Mon Apr 26 1999 Jan "Yenya" Kasprzak <kas@fi.muni.cz>
- Added $RPM_OPT_FLAGS
 
* Fri Apr 23 1999 Damien Miller <damien@ibs.com.au>
- Built RPM  
