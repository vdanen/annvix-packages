%define initdir %{_initrddir}

Summary:	The NIS (Network Information Service) server
Url:		http://www.linux-nis.org/
Name:		ypserv
Version:	2.11
Release:	1mdk
License:	GPL
Group:		System/Servers

Source0:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/ypserv-%{PACKAGE_VERSION}.tar.bz2
Source1:	ypserv-ypserv.init
Source2:	ypserv-yppasswdd.init
Source3:	ypserv-ypxfrd.init
Source4:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/ypserv-%{PACKAGE_VERSION}.tar.bz2.sign
Patch0:		ypserv-2.10-makefile.patch.bz2
Patch1: 	ypserv-2.1-syslog.patch.bz2
Patch2: 	ypserv-2.11-path.patch.bz2
Patch3:		ypserv-2.10-nomap.patch.bz2

Buildroot:	%_tmppath/%name-%version-%release-root
BuildRequires:	mawk, libgdbm-devel, libopenslp-devel
Requires:	portmap, mawk, make
Prereq:		/sbin/chkconfig, /sbin/service, rpm-helper

%description
The Network Information Service (NIS) is a system which provides network
information (login names, passwords, home directories, group information)
to all of the machines on a network.  NIS can enable users to login on
any machine on the network, as long as the machine has the NIS client
programs running and the user's password is recorded in the NIS passwd
database.  NIS was formerly known as Sun Yellow Pages (YP).

This package provides the NIS server, which will need to be running on
your network.  NIS clients do not need to be running the server.

Install ypserv if you need an NIS server for your network.  You'll also
need to install the yp-tools and ypbind packages onto any NIS client
machines.

%prep

%setup -q
%patch0 -p1 -b .makefix
%patch1 -p1 -b .syslog
%patch2 -p1 -b .path
%patch3 -p1 -b .nomap

%build
%serverbuild
cp etc/README etc/README.etc
%configure2_5x --enable-checkroot \
	   --enable-fqdn \
	   --enable-yppasswd \
	   --libexecdir=%{_libdir}/yp \
	   --mandir=%{_mandir}
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall libexecdir=$RPM_BUILD_ROOT%{_libdir}/yp

install -d %buildroot/%{initdir}
install -m644 etc/ypserv.conf %buildroot/%{_sysconfdir}
install -m755 %{SOURCE1} %buildroot/%{initdir}/ypserv
install -m755 %{SOURCE2} %buildroot/%{initdir}/yppasswdd
install -m755 %{SOURCE3} %buildroot/%{initdir}/ypxfrd

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" %buildroot/%{_initrddir}/*

%clean
rm -fr %buildroot

%post

%_post_service ypserv

%_post_service yppasswdd

%_post_service ypxfrd

%preun

%_preun_service ypserv

%_preun_service yppasswdd
 
%_preun_service ypxfrd
 
%files
%defattr(-,root,root)
%doc README INSTALL ChangeLog TODO NEWS
%doc etc/ypserv.conf etc/securenets etc/README.etc
%config(noreplace) %{_sysconfdir}/ypserv.conf
%config(noreplace) /var/yp/*
%config(noreplace) %{initdir}/*
%{_libdir}/yp
%{_sbindir}/*
%{_mandir}/*/*
%{_includedir}/*/*

%changelog
* Tue Jan 20 2004 Frederic Lepied <flepied@mandrakesoft.com> 2.11-1mdk
- 2.11: SLP support

* Thu Nov  6 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.10-1mdk
- 2.10

* Mon Jul 21 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.8-2mdk
- removed Obsoletes/Provides yppasswd

* Sat Feb  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.8-1mdk
- 2.8

* Thu Dec 26 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.6-2mdk
- corrected typo in ypxfrd.init (bug #207)

* Mon Nov  4 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.6-1mdk
- 2.6 (2.5 fixes an exploitable memory leak, but 2.6 is most recent)

* Fri Jul 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.4-1mdk
- 2.4
- removed patch3 (integrated upstream)

* Sun Feb 24 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2-5mdk
- Added a requires on make (Arnaud)

* Sun Feb 24 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2-4mdk
- corrected ypxfrd init script to really start the server

* Wed Feb 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.2-3mdk
- remove tcp_wrappers from Requires (use /var/yp/securenets to allow/deny
queries from other hosts).
- apply patch for ypxfr.

* Tue Dec 04 2001 Stefan van der Eijk <stefan@eijk.nu> 2.2-2mdk
- Removed %%dir /var/yp from %%files (owned by filesystem)

* Fri Nov 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.2-1mdk
- 2.2

* Wed Sep  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.12-3mdk
- patch4 from Holm: put a \0 at the right place to allow synchronisation
between slave and master to work (#4331).

* Wed Aug 29 2001 Philippe Libat <philippe@mandrakesoft.com> 1.3.12-2mdk
- libgdbm2

* Thu May 24 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.12-1mdk
- 1.3.12

* Thu Mar 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.3.11-7mdk
- use the new rpm macros for servers.

* Wed Jan 10 2001 David BAUDENS <baudens@mandrakesoft.com> 1.3.11-6mdk
- BuildRequires: mawk, libgdbm1-devel

* Sun Jan 07 2001 David BAUDENS <baudens@mandrakesoft.com> 1.3.11-5mdk
- BuildRequires: tcp_wrappers-devel
- Spec clean up

* Tue Oct 24 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.3.11-4mdk
- security fix

* Tue Oct 10 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.11-3mdk
- Fix typo in initscripts.

* Wed Aug 30 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.3.11-2mdk
- rebuild for hte user of the initrddir macro.

* Thu Aug 24 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.3.11-1mdk
- 1.3.11
- launch rpc.ypxfrd in /etc/rc.d/init.d/ypserv
- add condrestart in /etc/rc.d/init.d/ypserv to be able to restart the service
in %%postun using /sbin/service.

* Mon Jul 24 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 1.3.9-5mdk
- fixed path of makedbm in /var/yp/Makefile (was broken with 4mdk)

* Sun Jul 23 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 1.3.9-4mdk
- macroszifications
- BM

* Thu Mar 30 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.9-3mdk
- fix group
- use spechelper (resulting in spec cleanups)

* Mon Dec 6	1999 Philippe Libat <philippe@mandrakesoft.com>

- Added Makefile patch
- Spec modification

* Wed Oct 27 1999 Francis Galiegue <francis@mandrakesoft.com>

- Updated to 1.3.9 - fixes numerous security bugs
- export shadow map but set MERGE_(PASSWD|GROUP) to false

* Fri Jul 30 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- Updated to 1.3.7

* Sun Jul 18 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 1.3.6.94

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- version 1.3.6.91

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Mon Feb  8 1999 Bill Nottingham <notting@redhat.com>
- move to start before ypbind

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1
- upgraded to 1.3.5

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- yppasswd.init: lock file must have same name as init.d script, not daemon

* Sat Jul 11 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.3.4
- fixed the fubared Makefile
- link against gdbm instead of ndbm (it seems to work better)

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.3.1
- enhanced init scripts

* Fri May 01 1998 Jeff Johnson <jbj@redhat.com>
- added triggerpostun
- Use libdb fro dbp_*().

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Apr 13 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.3.0

* Wed Dec 03 1997 Cristian Gafton <gafton@redhat.com>
- updated to 1.2.5
- added buildroot; updated spec file
- added yppasswdd init file

* Tue Nov 04 1997 Erik Troan <ewt@redhat.com>
- init script shouldn't set the domain name

* Tue Oct 14 1997 Erik Troan <ewt@redhat.com>
- supports chkconfig
- updated initscript for status and restart
- turned off in all runlevels, by default
- removed postinstall script which didn't do anything

* Thu Oct 09 1997 Erik Troan <ewt@redhat.com>
- added patch to build against later glibc

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Wed Apr 23 1997 Erik Troan <ewt@redhat.com>
- updated to 1.1.7.

* Fri Mar 14 1997 Erik Troan <ewt@redhat.com>
- Updated to ypserv 1.1.5, ported to Alpha (glibc).

* Fri Mar 07 1997 Erik Troan <ewt@redhat.com>
- Removed -pedantic which confuses the SPARC :-(
