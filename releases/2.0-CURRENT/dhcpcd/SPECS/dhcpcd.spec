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

Requires(post):	rpm-helper

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
mkdir -p %{buildroot}/var/log

install -s -m 0755 dhcpcd %{buildroot}/sbin/dhcpcd
install -s -m 0755 dhcpcd.exe %{buildroot}%{_sysconfdir}/dhcpc/
install -m 0644 dhcpcd.8 %{buildroot}%{_mandir}/man8/dhcpcd.8
touch %{buildroot}/var/log/%{name}.log


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
# Create initial log files so that logrotate doesn't complain
if [ $1 = 1 ]; then # first install
	%create_ghostfile dhcpcd root root 644
fi


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/dhcpc/*
/sbin/dhcpcd
%{_mandir}/man8/dhcpcd.8*
%ghost /var/log/%{name}.log

%files doc
%defattr(-,root,root)
%doc README ChangeLog COPYING INSTALL *.lsm


%changelog
* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.3.22pl4-3mdk
- rebuild

* Mon Jan 20 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.22pl4-2mdk
- Launch /sbin/update-resolvrdv when upgrading dns.

* Sat Jan 04 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.3.22pl4-1mdk
- 1.3.22pl4

* Wed Oct 16 2002 Florin <florin@mandrakesoft.com> 1.3.22pl3-1mdk
- 1.3.22pl3
- ghost
- remove the pid patch

* Mon Feb 18 2002 Florin <florin@mandrakesoft.com> 1.3.22pl1-3mdk
- update the man page according to the pid patch

* Mon Feb 18 2002 Florin <florin@mandrakesoft.com> 1.3.22pl1-2mdk
- put the pid file in /var/run (pid patch)

* Tue Jan 29 2002 Florin <florin@mandrakesoft.com> 1.3.22pl1-1mdk
- 1.3.22pl1

* Mon Jan 14 2002 Florin <florin@mandrakesoft.com> 1.3.21pl2-1mdk
- 1.3.21pl2
- add Url tag

* Fri Oct 19 2001 Florin <florin@mandrakesoft.com> 1.3.21pl1-1mdk
- 1.3.21-pl1
- WARNING: make sure you use -R -Y -d options in the initscripts
- s/Copyright/License
- remove useless patches
- add README ChangeLog COPYING INSTALL *.lsm files
- add the %%{_sysconfdir}/dhcpcd.exe file

* Sun Apr 08 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.3.20pl0-1mdk
- Roll out 1.3.20pl0 for everyone.

* Thu Dec 21 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.3.19pl4-1mdk
- new and shiny source.

* Thu Oct 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.19pl1-2mdk
- Add patch for gcc2.96(rh).

* Tue Aug 08 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.3.19pl1-1mdk
- rebuild to use _sysconfdir
- s|1.3.18pl5|1.3.19pl1|

* Fri Jul 28 2000 Vincent Saugey <vince@mandrakesoft.com> 1.3.18pl5-3mdk
- BM, macros

* Tue Apr 18 2000 Vincent Saugey <vince@mandrakesoft.com> 1.3.18pl5-2mdk
- Add patch for dynamic build
- remove bzip and strip file

* Fri Mar 31 2000 Vincent Saugey <vince@mandrakesoft.com> 1.3.18pl5-1mdk
- Correct group
- Update to 1.3.18-pl5

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.3.18-pl3
- add /etc/dhcpc

* Sun Jul 18 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- 1.3.17pl9

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Mon Apr 19 1999 Bill Nottingham <notting@redhat.com>
- build for 6.0

* Wed Dec 23 1998 Jeff Johnson <jbj@redhat.com>
- mark default route up.

* Sun Jun  7 1998 Jeff Johnson <jbj@redhat.com>
- Fix packet alignment problems on sparc.
- build root.

* Mon Jun 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Wed May  6 1998 Alan Cox
- fixed some potential buffer exploits reported by Chris Evans

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- spec file cleanups 

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- built against glibc, updated to 0.65

* Mon Apr 21 1997 Otto Hammersmith <otto@redhat.com>
- fixed summary line... was a summary for tar.

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
