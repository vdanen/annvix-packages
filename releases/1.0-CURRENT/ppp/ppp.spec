%define name	ppp
%define version	2.4.2
%define release	2avx

Summary:	The PPP daemon and documentation for Linux 1.3.xx and greater.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD/GPL
Group:		System/Servers
URL:		http://www.samba.org/ppp
Source0:	ftp://ftp.samba.org/pub/ppp/ppp-%{version}.tar.bz2
Source1:	ppp-2.3.5-pamd.conf
Source2:	ppp-2.4.1-mppe-crypto.tar.bz2
Source3:	README.pppoatm
Source4:	ppp.logrotate
Patch0:		ppp-2.4.2-make.patch.bz2
Patch1:		ppp-2.3.6-sample.patch.bz2
Patch2:		ppp-2.4.2-wtmp.patch.bz2
Patch3:		ppp-2.4.2-makeopt.patch.bz2
Patch4:		ppp-options.patch.bz2
Patch5:		ppp-2.4.2-pppdump-Makefile.patch.bz2
Patch6:		ppp-2.4.1-noexttraffic.patch.bz2
Patch7:		ppp-2.4.1-pcap.patch.bz2
#PPPoATM support
#Patch8:		http://www.sfgoth.com/~mitch/linux/atm/pppoatm/ppp-2.4.1-pppoatm.patch.bz2
Patch8:		http://linux-usb.sourceforge.net/SpeedTouch/download/pppoatm.diff
Patch9:		ppp-2.4.2-pie.patch.bz2
Patch10:	ppp-2.4.2-dontwriteetc.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	liblinux-atm-devel
BuildRequires:	libpcap-devel 
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pam-devel

Requires:	glibc >= 2.0.6

%description
The ppp package contains the PPP (Point-to-Point Protocol) daemon
and documentation for PPP support.  The PPP protocol provides a
method for transmitting datagrams over serial point-to-point links.

The ppp package should be installed if your machine need to support
the PPP protocol.

%package devel
Summary:	PPP development files
Group:		Development/C
Requires:	%{name} = %{version}-%{release}

%description devel
The development files for PPP.

%package pppoatm
Summary:	PPP over ATM plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}

%description pppoatm
PPP over ATM plugin for %{name}.

%package pppoe
Summary:	PPP over ethernet plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}

%description pppoe
PPP over ethernet plugin for %{name}.

%prep
%setup  -q
%patch10 -p1 -b .dontwriteetc
%patch0 -p1 -b .make
%patch1 -p1 -b .sample
%patch2 -p1 -b .wtmp
%patch3 -p1 -b .makeopt
%patch4 -p1 -b .options
%patch5 -p1 -b .pppdump-Makefile
# (gg) add noext-traffic option
%patch6 -p1 -b .noext
# use pcap-bpf.h instead of net/bpf.h
%patch7 -p1 -b .pcap
%patch8 -p1 -b .pppoatm
%patch9 -p1 -b .pie

tar -xjf %{SOURCE2}

# patch 2 depends on the -lutil in patch 0
find . -type f -name "*.sample" | xargs rm -f 

%build
# lib64 fixes
perl -pi -e "s|^(LIBDIR.*)/usr/lib|\1%{_libdir}|g" pppd/Makefile.linux pppd/plugins/Makefile.linux
# stpcpy() is a GNU extension
OPT_FLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"

perl -pi -e "s/openssl/openssl -DOPENSSL_NO_SHA1/;" openssl/crypto/sha/Makefile

CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" %configure
# remove the following line when rebuilding against kernel 2.4 for multilink
#perl -pi -e "s|-DHAVE_MULTILINK||" pppd/Makefile
%ifarch amd64 x86_64
make RPM_OPT_FLAGS="$OPT_FLAGS -DDO_BSD_COMPRESS=0 -fPIC"
%else
make RPM_OPT_FLAGS="$OPT_FLAGS -DDO_BSD_COMPRESS=0"
%endif
make -C pppd/plugins -f Makefile.linux

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/{ppp/peers,pam.d}}

%makeinstall_std \
	BINDIR=%{buildroot}/%{_sbindir} \
	MANDIR=%{buildroot}/%{_mandir} \
	ETCDIR=%{buildroot}/%{_sysconfdir}/ppp \
	LIBDIR=%{buildroot}%{_libdir}/pppd/%{version} \
	INSTALL="%{_bindir}/install"

# (florin) strip the binary
strip %{buildroot}/%{_sbindir}/pppd

# it shouldn't be SUID root be default
chmod 755 %{buildroot}%{_sbindir}/pppd

chmod go+r scripts/*
install -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/pam.d/ppp
install -m 644 %{SOURCE3} %{_builddir}/%{name}-%{version}

# (stew) fix permissions
chmod 0644 README.MSCHAP80

#mknod %{buildroot}/dev/ppp c 108 0

# Provide pointers for people who expect stuff in old places
ln -s ../../var/log/ppp/connect-errors %{buildroot}%{_sysconfdir}/ppp/connect-errors
ln -s ../../var/log/ppp/resolv.conf %{buildroot}%{_sysconfdir}/ppp/resolv.conf

# logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/ppp

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc FAQ PLUGINS README* scripts sample
%{_sbindir}/chat
%{_sbindir}/pppdump
%attr(0755,root,root)	%{_sbindir}/pppd
%attr(0755,root,daemon)	%{_sbindir}/pppstats
%{_mandir}/man*/*
%dir %{_libdir}/pppd
%{_libdir}/pppd/%{version}
%exclude %{_libdir}/pppd/%{version}/pppoatm.so
%exclude %{_libdir}/pppd/%{version}/rp-pppoe.so
%dir %{_sysconfdir}/ppp
%dir %{_sysconfdir}/ppp/peers
%dir /var/run/ppp
%attr(0700,root,root) %dir /var/log/ppp
%attr(0600,root,daemon)	%config(noreplace) %{_sysconfdir}/ppp/*
%config(noreplace) %{_sysconfdir}/pam.d/ppp
%config(noreplace) %{_sysconfdir}/logrotate.d/ppp

%files devel
%defattr(-,root,root)
%{_includedir}/pppd/*

%files pppoatm
%defattr(-,root,root)
%{_libdir}/pppd/%{version}/pppoatm.so

%files pppoe
%defattr(-,root,root)
%{_libdir}/pppd/%{version}/rp-pppoe.so

%changelog
* Thu Jan 06 2005 Vincent Danen <vdanen@annvix.org> 2.4.2-2avx
- rebuild against new openssl

* Tue Aug 17 2004 Vincent Danen <vdanen@annvix.org> 2.4.2-1avx
- 2.4.2
- own directories
- strip suid bit from pppd; we don't need it since users shouldn't
  be connecting to the internet on a server system
- pass -fPIC if compiling on x86_64
- merge with cooker 2.4.2-2mdk (florin):
  - update the make, makeopt, wtmp patches
  - remove the pam_sessions, zfree, mppe, includes, libdir, filter
    pppoe, disconnect, gcc, pcap, varargs obsolete patches
  - add the include files
  - add the README.pppoatm FAW PLUGINS files
  - add the logrotate patch and file (rh)
  - add the pie, dontwriteetc patches (rh)
  - use a different pppoatm patch

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.4.1-15avx
- Annvix build
- P16: need to include pcap-bpf.h instead of net/bpf.h

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.4.1-14sls
- minor spec cleanups

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 2.4.1-13sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.1-12mdk
- Patch15: Fix varargs on amd64

* Sun Jul 27 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.4.1-11mdk
- applied disconnection patch (Frode Isaksen <fisaksen@bewan.com>)

* Thu Jun 19 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.4.1-10mdk
- splitted pppoatm and pppoe plugins
- spec cleanup
- fixed compilation

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.4.1-9mdk
- Rebuild for new libopenssl
- PPPoE and PPPoATM kernel support 
- Contribution by Guillaume Rousse <guillomovitch@plf.zarb.org>
  Patches 11 and 12: pppoatm support (stolen from Suse)
  BuildRequires liblinux-atm-devel

* Sat Nov 02 2002 Giuseppe Ghib? <ghibo@mandrakesoft.com> 2.4.1-8mdk
- added Dieter Jurzitza's patch to add noext-traffic feature.

* Thu Oct 31 2002 Giuseppe Ghib? <ghibo@mandrakesoft.com> 2.4.1-7mdk
- Activate filter capabilities.

* Fri Aug  9 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.1-6mdk
- Hand patch for lib64
- Patch10: Add missing includes
- Patch11: Fix location of pppd modules

* Mon Jun  3 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.4.1-5mdk
- add mppe functionality for pptp VPN dialin to NT servers

* Mon Apr 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.1-4mdk
- ppp has a new home at samba.org.

* Tue Mar  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.4.1-3mdk
- rebuild

* Thu Jul 19 2001 Stefan van der Eijk <stefan@eijk.nu> 2.4.1-2mdk
- BuildRequires:	pam-devel

* Sun Apr 07 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.1-1mdk
- Version 2.4.1.
- Create /usr/lib/<pppd-version> for the new plugin feature.

* Sun Dec 10 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.0-4mdk
- try to rebuild with multilink.

* Tue Sep 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-3mdk
- Pamstackizification.
- check pam_open_session result code (rh).

* Thu Aug 31 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.0-2mdk
- add noauth, noipdefault and userpeerdns to /etc/ppp/options (pablo).

* Sun Aug 06 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.0-1mdk
- new and shiny version
- rebuild for new url

* Wed Jul 26 2000 Francis Galiegue <fg@mandrakesoft.com> 2.3.11-9mdk

- /dev/ppp is now in dev package
- some %files list cleanup

* Fri Jul 21 2000 Francis Galiegue <fg@mandrakesoft.com> 2.3.11-8mdk

- BM

* Wed May 03 2000 Jerome Martin <jerome@mandrakesoft.com> 2.3.11-7mdk
- Changed pppd perms again, to add the save to disk swap attribute in
  order to allow some sort of modem locking.
  
* Wed May 03 2000 Jerome Martin <jerome@mandrakesoft.com> 2.3.11-6mdk
- Added suid root permission to pppd
- rebuild for new environment

* Sat Apr 08 2000 John Buswell <johnb@mandrakesoft.com> 2.3.11-5mdk
- Fixed perms on /etc/ppp/peers

* Thu Mar 30 2000 John Buswell <johnb@mandrakesoft.com> 2.3.11-4mdk
- Fixed groups
- spec-helper

* Sun Feb 27 2000 Giuseppe Ghib? <ghibo@mandrakesoft.com> 2.3.11-3mdk
- added RedHat reaper (ppp-2.3.11-reap) patch and synched with
  RedHat version 2.3.11-1.
- added pppdump and pppdump.8 man pages.
- added ppp-2.3.11-makeopt patch.

* Sun Feb 06 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 2.3.11-1mdk
- 2.3.11

* Mon Nov 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- remove %post.

* Fri Nov 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- fix for double-dial problem(r).
- fix for requiring a controlling terminal problem(r).

* Wed Nov 10 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Create /etc/ppp/peers.

* Thu Nov 04 1999 John Buswell <johnb@mandrakesoft.com>
- 2.3.10
- Build Release

* Mon Sep 20 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Fix %%post ?? 

* Mon Sep 20 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Fix %%post

* Mon Sep 20 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- -DCHAPMS
- -DUSE_PAM

* Tue Sep  7 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Add /dev/ppp
- Add entries in /etc/conf.modules if they aren't there yet

* Wed Aug 25 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 2.3.9 (required for kernel 2.3.14+)

* Thu Jul 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Removing unused stuff.
- Upgrade patch.
- 2.3.8.

* Fri Jul 10 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Define the .pid to /var/run/
- Glare @Chmouel

* Fri Jul 09 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Define the .pid to /var/run not to /etc/ (reported by Nikodemus Karlsson
  <nickek@algonet.se>).

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- force pppd use the glibc's logwtmp instead of implementing its own

* Wed Apr 01 1999 Preston Brown <pbrown@redhat.com>
- version 2.3.7 bugfix release

* Tue Mar 23 1999 Cristian Gafton <gafton@redhat.com>
- version 2.3.6

* Mon Mar 22 1999 Michael Johnson <johnsonm@redhat.com>
- auth patch

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Jan 07 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Jun  5 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.3.5.

* Tue May 19 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Fri May  8 1998 Jakub Jelinek <jj@ultra.linux.cz>
- make it run with kernels 2.1.100 and above.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Mar 18 1998 Cristian Gafton <gafton@redhat.com>
- requires glibc 2.0.6 or later

* Wed Mar 18 1998 Michael K. Johnson <johnsonm@redhat.com>
- updated PAM patch to not turn off wtmp/utmp/syslog logging.

* Wed Jan  7 1998 Cristian Gafton <gafton@redhat.com>
- added the /etc/pam.d config file
- updated PAM patch to include session support

* Tue Jan  6 1998 Cristian Gafton <gafton@redhat.com>
- updated to ppp-2.3.3, build against glibc-2.0.6 - previous patches not
  required any more.
- added buildroot
- fixed the PAM support, which was really, completely broken and against any
  standards (session support is still not here... :-( )
- we build against running kernel and pray that it will work
- added a samples patch; updated glibc patch

* Thu Dec 18 1997 Erik Troan <ewt@redhat.com>
- added a patch to use our own route.h, rather then glibc's (which has 
  alignment problems on Alpha's) -- I only applied this patch on the Alpha,
  though it should be safe everywhere

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- turned off the execute bit for scripts in /usr/doc

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Mar 25 1997 Erik Troan <ewt@redhat.com>
- Integrated new patch from David Mosberger
- Improved description
