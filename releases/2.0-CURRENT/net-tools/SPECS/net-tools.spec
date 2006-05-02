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
Source1:	netplug-%{npversion}.tar.bz2
Source2:	net-tools-1.60-config.h
Source3:	net-tools-1.60-config.make
Source4:	ether-wake.c
Source5:	ether-wake.8
Source6:	mii-diag.c
Source7:	mii-diag.8
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
Patch33:	net-tools-1.60-bitkeeper.patch
Patch34:	net-tools-1.60-ifconfig_ib.patch
Patch35:	net-tools-1.60-de.patch
Patch36:	netplug-1.2.9-execshield.patch
Patch37:	net-tools-1.60-pie.patch
Patch38:	net-tools-1.60-ifaceopt.patch
Patch39:	net-tools-1.60-trim_iface.patch
Patch40:	net-tools-1.60-stdo.patch
Patch41:	net-tools-1.60-statistics.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext

%description
The net-tools package contains the basic tools needed for setting up
networking:  ifconfig, netstat, route and others.


%prep
%setup -q -a 1
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
#%patch13 -p1 -b .x25
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
%patch33 -p1 -b .bitkeeper
%patch34 -p1 -b .ifconfig_ib
%patch35 -p1 
%patch36 -p1 -b .execshield
%patch37 -p1 -b .pie
%patch38 -p1 -b .ifaceopt
%patch39 -p1 -b .trim-iface
%patch40 -p1 -b .stdo
%patch41 -p1 -b .statistics

cat %{SOURCE2} > ./config.h
cat %{SOURCE3} > ./config.make
cat %{SOURCE4} > ./ether-wake.c
cat %{SOURCE5} > ./man/en_US/ether-wake.8
cat %{SOURCE6} > ./mii-diag.c
cat %{SOURCE7} > ./man/en_US/mii-diag.8

%ifarch alpha
perl -pi -e "s|-O2||" Makefile
%endif


%build
export CFLAGS="%{optflags} $CFLAGS"

make
gcc %{optflags} -o ether-wake ether-wake.c
gcc %{optflags} -o mii-diag mii-diag.c
pushd netplug-%{npversion}
    %make
popd

#man pages conversion
#french 
iconv -f iso-8859-1 -t utf-8 -o arp.tmp man/fr_FR/arp.8 && mv arp.tmp man/fr_FR/arp.8
iconv -f iso-8859-1 -t utf-8 -o ethers.tmp man/fr_FR/ethers.5 && mv ethers.tmp man/fr_FR/ethers.5
iconv -f iso-8859-1 -t utf-8 -o hostname.tmp man/fr_FR/hostname.1 && mv hostname.tmp man/fr_FR/hostname.1
iconv -f iso-8859-1 -t utf-8 -o ifconfig.tmp man/fr_FR/ifconfig.8 && mv ifconfig.tmp man/fr_FR/ifconfig.8
iconv -f iso-8859-1 -t utf-8 -o netstat.tmp man/fr_FR/netstat.8 && mv netstat.tmp man/fr_FR/netstat.8
iconv -f iso-8859-1 -t utf-8 -o plipconfig.tmp man/fr_FR/plipconfig.8 && mv plipconfig.tmp man/fr_FR/plipconfig.8
iconv -f iso-8859-1 -t utf-8 -o route.tmp man/fr_FR/route.8 && mv route.tmp man/fr_FR/route.8
iconv -f iso-8859-1 -t utf-8 -o slattach.tmp man/fr_FR/slattach.8 && mv slattach.tmp man/fr_FR/slattach.8
#portugal
iconv -f iso-8859-1 -t utf-8 -o arp.tmp man/pt_BR/arp.8 && mv arp.tmp man/pt_BR/arp.8
iconv -f iso-8859-1 -t utf-8 -o hostname.tmp man/pt_BR/hostname.1 && mv hostname.tmp man/pt_BR/hostname.1
iconv -f iso-8859-1 -t utf-8 -o ifconfig.tmp man/pt_BR/ifconfig.8 && mv ifconfig.tmp man/pt_BR/ifconfig.8
iconv -f iso-8859-1 -t utf-8 -o netstat.tmp man/pt_BR/netstat.8 && mv netstat.tmp man/pt_BR/netstat.8
iconv -f iso-8859-1 -t utf-8 -o route.tmp man/pt_BR/route.8 && mv route.tmp man/pt_BR/route.8
#german
iconv -f iso-8859-1 -t utf-8 -o arp.tmp man/de_DE/arp.8 && mv arp.tmp man/de_DE/arp.8
iconv -f iso-8859-1 -t utf-8 -o ethers.tmp man/de_DE/ethers.5 && mv ethers.tmp man/de_DE/ethers.5
iconv -f iso-8859-1 -t utf-8 -o hostname.tmp man/de_DE/hostname.1 && mv hostname.tmp man/de_DE/hostname.1
iconv -f iso-8859-1 -t utf-8 -o ifconfig.tmp man/de_DE/ifconfig.8 && mv ifconfig.tmp man/de_DE/ifconfig.8
iconv -f iso-8859-1 -t utf-8 -o netstat.tmp man/de_DE/netstat.8 && mv netstat.tmp man/de_DE/netstat.8
iconv -f iso-8859-1 -t utf-8 -o plipconfig.tmp man/de_DE/plipconfig.8 && mv plipconfig.tmp man/de_DE/plipconfig.8
iconv -f iso-8859-1 -t utf-8 -o route.tmp man/de_DE/route.8 && mv route.tmp man/de_DE/route.8
iconv -f iso-8859-1 -t utf-8 -o slattach.tmp man/de_DE/slattach.8 && mv slattach.tmp man/de_DE/slattach.8


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make BASEDIR=%{buildroot} mandir=%{_mandir} install

install -m 0755 ether-wake %{buildroot}/sbin
install -m 0755 mii-diag %{buildroot}/sbin

pushd netplug-%{npversion}
    make install prefix=%{buildroot} \
        initdir=%{buildroot}%{_initrddir} \
        mandir=%{buildroot}%{_mandir}
    mv README README.netplugd
    mv TODO TODO.netplugd
popd

rm %{buildroot}/sbin/rarp
rm %{buildroot}%{_mandir}/man8/rarp.8*
rm %{buildroot}%{_mandir}/*/man8/rarp.8*

rm -rf %{buildroot}%{_mandir}/{de,fr,pt}*

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%doc netplug-%{npversion}/TODO.netplugd netplug-%{npversion}/README.netplugd COPYING
%doc README README.ipv6 TODO INSTALLING ABOUT-NLS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/netplug/netplugd.conf
%dir %{_sysconfdir}/netplug.d
%attr(0755,root,root) %{_sysconfdir}/netplug.d/*
%attr(0755,root,root) %{_initrddir}/netplugd
/bin/*
/sbin/*
%{_mandir}/man[158]/*


%changelog
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

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.60-9mdk
- fix gcc-3.3 patch (P5)

* Sat Jul 19 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.60-8mdk
- fix gcc-3.3 build (P5), updated S5
- fix invalid locales (s/fr_FR/fr/ & s/de_DE/de/)
- fix url

* Thu Apr 17 2003 Erwan Velu <erwan@mandrakesoft.com> 1.60-7mdk
- New version of ether-wake (1.06)
* Tue Feb 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.60-6mdk
- Rebuild

* Wed Aug 21 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.60-5mdk
- merged with rh

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.60-4mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Sun Jun  2 2002 Stefan van der Eijk <stefan@eijk.nu> 1.60-3mdk
- BuildRequires
- Copyright --> License

* Thu Jun 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.60-2mdk
- Add ether-wake from donald-becker.
- Clean up specs.
- Fix man-pages.

* Mon Apr 16 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.60-1mdk
- Version 1.60 on Easter Monday.

* Fri Feb 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.59-1mdk
- 1.59.

* Thu Feb 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.58-4mdk
- Add ipvs patch.

* Fri Feb 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.58-3mdk
- Fix ifconfig: don't close a socket that we are going to use.

* Thu Feb 15 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.58-2mdk
- Really put in the i18n man-pages.

* Sun Feb 11 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.58-1mdk
- New and shiny source.
- Dump the fhs patch, as things get intalled in the correct location now.
- Put the i18n man-pages in the location where they should belong.

* Wed Nov  8 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.57-5mdk
- Enable all protocol options.
- Build and install mii-tool.
- Really handle RPM_OPT_FLAGS.
- Add documentation.
- Update description.

* Thu Aug  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.57-4mdk
- Clean-up.

* Fri Jul 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.57-3mdk
- More macros.
- Readd man pages :-(

* Thu Jul 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.57-2mdk
- BM.

* Fri Jun 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.57-1mdk
- 1.57.
- Use mandir macros for FHS compatibilty.

* Tue Apr  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.55-1mdk
- 1.55.

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.54-1mdk
- Spec-helper clean-up.
- Merge with rh-patchs.
- use find_lang macros for locales.
- Adjust groups.

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- %lang in man/-locale.
- big spec cleanup.

* Sun Aug 29 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 1.53:	- fixes several buffer overruns
	- adds german man pages
	- adds french ethers.5 translation
	- adds estonian
- fix up .spec

* Mon Jul 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release (8mdk).

* Sat Jul 10 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- moved french manpages from fr_FR to fr
- compressed all man pages
- added french, spanish and wallon descriptions

* Fri Jun 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix potentional bufer overruns.
- patch to recognize ESP and GRE protocols for VPN masquerade
  <jhardin@wolfenet.com>.

* Wed Apr 28 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Update to 1.52

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add patch from RedHat6.0.
- Update to 1.51.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- handle RPM_OPT_FLAGS

* Tue Feb  2 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.50.
- added slattach/plipconfig/ipmaddr/iptunnel commands.
- enabled translated man pages.

* Tue Dec 15 1998 Jakub Jelinek <jj@ultra.linux.cz>
- update to 1.49.

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.48.

* Thu Nov 12 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.47.

* Wed Sep  2 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.46

* Thu Jul  9 1998 Jeff Johnson <jbj@redhat.com>
- build root
- include ethers.5

* Thu Jun 11 1998 Aron Griffis <agriffis@coat.com>
- upgraded to 1.45
- patched hostname.c to initialize buffer
- patched ax25.c to use kernel headers

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Feb 27 1998 Jason Spangler <jasons@usemail.com>
- added config patch

* Fri Feb 27 1998 Jason Spangler <jasons@usemail.com>
- changed to net-tools 1.432
- removed old glibc 2.1 patch
 
* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added extra patches for glibc 2.1

* Tue Oct 21 1997 Erik Troan <ewt@redhat.com>
- included complete set of network protocols (some were removed for
  initial glibc work)

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- updated glibc patch for glibc 2.0.5

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- updated to 1.33
