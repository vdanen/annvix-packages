%define name	iptables
%define version	1.2.8
%define release	3sls

Summary:	Tools for managing Linux kernel packet filtering capabilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://netfilter.org/
Source:		http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
Source1:	iptables.init
Source2:	ip6tables.init
Source3:	iptables.config
Source4:	ip6tables.config
Patch1:		iptables-1.2.8-stealth_grsecurity.patch.bz2 
Patch2:		iptables-1.2.8-imq.patch.bz2 
Patch3:		iptables-1.2.8-libiptc.h.patch.bz2 

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildPrereq:	/usr/bin/perl
BuildRequires:  kernel-source >= 2.4.13-3mdk

PreReq:		chkconfig, rpm-helper
Requires:	kernel >= 2.4.13
Provides:	userspace-ipfilter
Conflicts:	ipchains

%description
iptables controls the Linux kernel network packet filtering code.
It allows you to set up firewalls and IP masquerading, etc.

Install iptables if you need to set up firewalling for your
network.

Install this only if you are using the 2.4 kernels!!

%package ipv6
Summary:	IPv6 support for iptables
Group:		System/Kernel and hardware
Requires:	%name = %version-%release
Prereq:		chkconfig, rpm-helper

%description ipv6
IPv6 support for iptables.

iptables controls the Linux kernel network packet filtering code.
It allows you to set up firewalls and IP masquerading, etc.

IPv6 is the next version of the IP protocol.

Install iptables-ipv6 if you need to set up firewalling for your
network and you're using ipv6.

%prep
%setup -q 
%patch1 -p1 -b .stealth
%patch2 -p1 -b .imq
%patch3 -p1 -b .libiptc

chmod +x extensions/.IMQ-test

find . -type f | xargs perl -pi -e "s,/usr/local,%{_prefix},g"

%build
%serverbuild
%ifarch alpha
OPT=`echo $RPM_OPT_FLAGS | sed -e "s/-O./-O1/"`
%else
OPT="$RPM_OPT_FLAGS -DNDEBUG"
%endif
%make COPT_FLAGS="$OPT" LIBDIR=/lib all experimental

%install
rm -rf $RPM_BUILD_ROOT
# Dunno why this happens. -- Geoff
%makeinstall_std BINDIR=/sbin MANDIR=%{_mandir} LIBDIR=/lib COPT_FLAGS="$RPM_OPT_FLAGS -DNETLINK_NFLOG=4" install-experimental
install -c -D -m755 %{SOURCE1} %buildroot%{_initrddir}/iptables
install -c -D -m755 %{SOURCE2} %buildroot%{_initrddir}/ip6tables
install -c -D -m644 %{SOURCE3} iptables.sample
install -c -D -m644 %{SOURCE4} ip6tables.sample

%clean
rm -rf $RPM_BUILD_ROOT $RPM_BUILD_DIR/file.list.%{name}

%post
%_post_service iptables

%preun
%_preun_service iptables

%post ipv6
%_post_service ip6tables

%preun ipv6
%_preun_service ip6tables

%files
%defattr(-,root,root,0755)
%config(noreplace) %{_initrddir}/iptables
/sbin/iptables
/sbin/iptables-save
/sbin/iptables-restore
%{_mandir}/*/iptables*
%dir /lib/iptables
/lib/iptables/libipt*
%doc INSTALL KNOWN_BUGS iptables.sample

%files ipv6
%defattr(-,root,root,0755)
%config(noreplace) %{_initrddir}/ip6tables
/sbin/ip6tables
/sbin/ip6tables-save
/sbin/ip6tables-restore
%{_mandir}/*/ip6tables*
/lib/iptables/libip6t*
%doc INSTALL KNOWN_BUGS ip6tables.sample

%changelog
* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 1.2.8-3sls
- OpenSLS build
- tidy spec

* Tue Aug 26 2003 Juan Quintela <quintela@mandrakesoft.com> 1.2.8-2mdk
- added imq support.

* Wed Jul 30 2003 Juan Quintela <quintela@mandrakesoft.com> 1.2.8-1mdk
- stealth module support.
- remove patch2 (anti chrash in iptables-restore), different solution upstream.
- 1.2.8.

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.2.7a-3mdk
- rebuild
- rm -rf $RPM_BUILD_ROOT at the beginning of %%install, not in %%prep
- use %%make macro
- use %%makeinstall_std macro

* Thu Feb 27 2003 Florin <florin@mandrakesoft.com> 1.2.7a-2mdk
- rebuild 

* Tue Dec  3 2002 Juan Quintela <quintela@mandrakesoft.com> 1.2.7a-1mdk
- Prereq rpm-helper.
- really include ipv6 manpages.
- 1.2.7a.

* Sat Apr 13 2002 Juan Quintela <quintela@mandrakesoft.com> 1.2.6a-1mdk
- removed old comparation to remove default configuration in post install.
- merge with iptables-1.2.5-3 form rh.

* Mon Apr  8 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.2.5-2mdk
- Conflicts: ipchains

* Tue Jan 29 2002 Juan Quintela <quintela@mandrakesoft.com> 1.2.5-1mdk
- compile with -NDEBUG, as it is the only way to get compatibility.
- fixed source tag.
- 1.2.5.

* Wed Nov  7 2001 Juan Quintela <quintela@mandrakesoft.com> 1.2.4-2mdk
- Added support for newnat, now iptables should also work for 2.4
  linus kernels.

* Wed Oct 31 2001 Juan Quintela <quintela@mandrakesoft.com> 1.2.4-1mdk
- %config are (noreplace) again.
- 1.2.4

* Mon Oct  8 2001 Juan Quintela <quintela@mandrakesoft.com> 1.2.3-1mdk
- remove .mport-test chmod.
- Added Ben Reser <ben@reser.org> optimization of not flushing the 
  channels before calling iptables-restore & adopted that for ip6tables.
- removed this time also ip6tables if it is the default one.
- removed cvs-fixes & save patches (integrated upstream).
- 1.2.3.

* Thu Sep 27 2001 Juan Quintela <quintela@mandrakesoft.com> 1.2.2-9mdk
- /etc/sysconfig/iptables moved to %doc iptables.sample.
- /etc/sysconfig/iptables moved to %doc ipt6ables.sample.
- We need that because we don't want something for default in a firewall.
- We remove the /etc/sysconfig/ip[6]tables if it is the default one, we need 
  that to let drakgw to work, agreed with gc (drakgw author) on this change.

* Mon Sep 24 2001 Juan Quintela <quintela@mandrakesoft.com> 1.2.2-8mdk
- changed init level from 08 to 03 (vdanen).

* Fri Sep 14 2001 Juan Quintela <quintela@mandrakesoft.com> 1.2.2-7mdk
- remove the $NAME var as rpmlint don't like it :(

* Fri Sep 14 2001 Juan Quintela <quintela@mandrakesoft.com> 1.2.2-6mdk
- put a $NAME macro.
- More fixes from Ben Reser <ben@reser.org>:
  - s/ipt6ables/ip6tables/ (I found another like this).


* Thu Sep 13 2001 Juan Quintela <quintela@mandrakesoft.com> 1.2.2-5mdk
- ipv6 initscript is the same style than ipv4 one.
- %doc added
- fix a lot of rpmlint errors.
- merge the fixes of Ben Reser (some of them have conflicts).
- vdanen merger a lof of Ben Reser fixes.
- many fixes from Ben Reser <ben@reser.org>:
  - fixed segfault in iptables-restore
  - added ipv6 initscript
  - changed iptables initscript to use iptables-restore
  - added default config files in /etc/sysconfig
  - added ip6tables-save and ip6tables-restore
- fixed mport-test

* Sun Aug  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.2-4mdk
- Merge with rh changes (init/patches).

* Mon Jun 25 2001 Juan Quintela <quintela@mandrakesoft.com> 1.2.2-3mdk
- Simple rebuilt due to kernel changes.

* Sat Jun 02 2001 Geoffrey Lee <snaitalk@mandrakesoft.com> 1.2.2-2mdk
- Silently rebuild iptables.

* Tue May 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.2-1mdk
- new version

* Thu Apr 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.1a-1mdk
- Put 1.2.1a in cooker.
- While I am at it, fix the URL, kernelnotes seems to be down. 
- No need to define NETLINK_NFGLOG=4 anymore.

* Wed Mar 28 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.1-4mdk
- Provides: userspace-ipfilter (Jay Beale).
- use server macros

* Sat Mar 24 2001 David BAUDENS <baudens@mandrakesoft.com> 1.2.1-3mdk
- PPC: build with gcc
- Requires: %%version-%%release and not only %%version

* Fri Mar 23 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.1-2mdk
- Patches from Abel Cheung <maddog@linuxhall.org>
  - Cleaner build routine.
  - (noreplace) and %%config for the SysV initscripts.
  
* Sun Mar 18 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.1-1mdk
- Update to 1.2.1.
- Stock build w/o patch-o-matic was broke so fix it.

* Mon Mar 05 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2-4mdk
- Really fix the init script (Sebastian Dransfeld).

* Sun Mar 04 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2-3mdk
- Fix the broken iptables SysV init script (Sebastian Dransfeld).

* Fri Mar 02 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2-2mdk
- Merge with rh packages (build iptables-* add ipv6 package, add CVS fixes).

* Tue Jan 09 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2-1mdk
- new and shiny source.

* Sat Dec 16 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.1.2-2mdk
- really build it on the alpha with egcs.

* Sat Dec 16 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.1.2-1mdk
- shamelessly rip a rpm from Red Hat.
- update to 1.1.2.
- build on alpha as well.

* Thu Aug 17 2000 Bill Nottingham <notting@redhat.com>
- build everywhere

* Tue Jul 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.1

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Preston Brown <pbrown@redhat.com>
- move iptables to /sbin.
- excludearch alpha for now, not building there because of compiler bug(?)

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- don't obsolete ipchains either
- update to 1.1.0

* Mon Jun  4 2000 Bill Nottingham <notting@redhat.com>
- remove explicit kernel requirement

* Tue May  2 2000 Bernhard Rosenkränzer <bero@redhat.com>
- initial package
